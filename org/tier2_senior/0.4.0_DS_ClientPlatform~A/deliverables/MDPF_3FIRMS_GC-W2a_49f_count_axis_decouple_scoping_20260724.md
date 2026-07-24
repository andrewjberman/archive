# GC-W2a Part 1 — SCOPE AND SIZE the 49F count-axis decouple

**TO:** `MDPF_3FIRMS.GC-W2a` @`939d7903f0` · **Agent:** `0.4.0_DS_ClientPlatform~A` · 2026-07-24
**archetype:** DIAGNOSE · **Scoping deliverable — no build, no code change, read-only on the producer.**
**Companion:** the converged class set (Part 2) is a separate file, same folder.

---

## 0. VERDICT UP FRONT

> **1. The decouple CANNOT fill ANY of the 22 holes. 0 of 22.** The per-model count for those dates does not
> exist anywhere in our retained estate — it never did. This **corroborates** an existing finding; see §6.
> **2. It is ALSO not a simple repoint going forward.** The one feed with the right grain
> (`fact_model_allocation_roster`) **does not reproduce the served count under any filter I tested** — closest
> is −3 / −13 accounts. A "repoint to the roster" fix would ship a silently-wrong count.
> **3. What IS new since the 2026-07-22 record: the roster is ACCUMULATING, not a point-in-time snapshot**
> (8 partitions then, 11 now, same start date). That is the first real forward-looking source — but it needs a
> definitional reconciliation first, not a wiring change.
> **4. There is a SECOND, ONGOING hole generator nobody has named: BUILD GAPS.** The frontier stamp writes
> only the last axis date, so every date falling between two builds is permanently un-stamped. This is
> actively creating new holes and the decouple is the thing that would stop it.

**Sizing answer for CTO's "tell me what it costs":** this is a **data workstream with an unresolved
definitional dependency**, not a wiring change. Anyone who sizes it as an afternoon will abandon it — which is
exactly what the 07-22 hold record predicted, and I now have the number that shows why.

---

## 1. THE MECHANISM — PROFILED, NOT INFERRED

My W-1 marked "why 49F's legacy axis omits its 20 dates" as `INFERRED-and-not-claimed`. **That is now closed.**
All cites `@3efc9dc6d` (the producer's last-touching commit; the file is unmodified in the worktree).

### 1.1 The import is SELF-REFERENTIAL

`load_served_account_count` (`:557-591`) reads 49F's counts **from our own published served artifact**,
`json/mdpf/{firm}/aggregate-aua-timeseries.json`. Its docstring says so outright: *"post-cutover this loader
reads OUR OWN published artifact."* It builds a `{date: count}` dict from the served dates (`:573-576`).
`_account_count_series` (`:594-598`) then does `counts_for_key.get(d)` against the revamp axis — **any date
absent from that dict returns `None`**, with **no LOCF and no gap-fill by explicit design** (CTO 180646Z, in
the docstring).

> **So a date missing from the served artifact is written back as `None`, and the NEXT build reads THAT
> artifact. THE HOLE RE-INHERITS ITSELF EVERY BUILD.** It is a self-perpetuating freeze, not a fetch failure —
> which is why it has never healed on its own and never will.

### 1.2 WHY the 20 were missing originally — EXERCISED on the legacy bytes

I pulled the **oldest retained version** of the 49F served key
(VersionId `_4IAznK8GBjxWDd3Sqf2FFBW2xiyWK9j`, **2026-07-08T15:00:43Z**) — the legacy schema, pre-W-7 (it has
no `account_count_total` at all).

| measurement | result |
|---|---|
| legacy axis length | **426 dates**, 2024-11-01 .. 2026-07-08 |
| holes at-or-before 2026-07-08 that are **ABSENT FROM ITS AXIS ENTIRELY** | **14 of 15** |
| **CONTROL** — healthy trading dates ≤2026-07-08 present on the legacy axis | **404 of 404** |
| the single exception | **2026-05-21** — present on the legacy axis |

**The omitted dates are not NULL on the legacy artifact. They are ABSENT FROM ITS DATE AXIS.** The date-join
finds nothing because the question was never asked for those dates.

**The single exception corroborates W-1 independently.** `2026-05-21` is exactly the date W-1 classified as
**INF-model-partition-absent (class C)** rather than 49F-legacy-omitted (class A) — by a completely different
method, hours earlier. The legacy-axis read could have contradicted that classification; it did not.

### 1.3 THE SECOND GENERATOR — BUILD GAPS (not previously named)

`:1657-1658` — `if acct and ad_frontier.get(mkey) is not None: acct[-1] = ad_frontier[mkey]` — the frontier
stamp writes **only the last axis position**. So a count is captured for a date **only if a build ran while
that date was the frontier.** Build times from the served key's 9 versions:

```
2026-07-08 · 07-10 · 07-16 (x2) · 07-17 · 07-18 · 07-23 (x3)
                                          ^^^^^^^^^^^^^^^^^^ gap: 07-19, 07-20, 07-21, 07-22
```

The 07-23 build stamped only 07-22 (the then-frontier). **07-19, 07-20 and 07-21 fell inside the gap and were
never stamped by anything** — and being past `count_coverage_end` (2026-07-18) the served-real import does not
cover them either. Consistent with the earlier 07-10→07-16 gap (07-13/14/15 all null).

> **This generator is ACTIVE. Every build gap mints new permanent holes.** The 20 legacy dates are a closed
> historical set; this one is open-ended, and it is the strongest argument for the decouple as the
> forward-looking half.

---

## 2. WHAT OUR ESTATE RETAINS at per-model-count grain — the search denominator

| source | depth | verdict |
|---|---|---|
| `schwab/08242234/silver/fact_rps_s2` (custody) | **542 partitions**, 2024-05-24..2026-07-23 | FULL history, has `account_id`, **39 columns and NONE carry model attribution** → total yes, per-model **no** |
| `smartx/platform/silver/fact_model_aum_daily` | 11 partitions (2026-07-14..24) | history lives *inside* the latest partition, but **no account-count column** (10 cols: rmid/total_aum/closing_equity/…) |
| `smartx/platform/silver/fact_model_allocation_roster` | **11 partitions, 2026-07-14..24 — ACCUMULATING** | right grain (see §4). **No history before 2026-07-14.** |
| `smartx/platform/bronze/{access_roster, models_summary, nonzerosleeve}` | 11 / 8 / 1 objects | ~11 days |
| `gold/mdpf_revamp/*/account_distribution.json` | 1 key/firm, **2 object versions** | current-state only, no dated archive |
| served `json/mdpf/49financial/…` object versions | 9, oldest **2026-07-08** | oldest *is* the legacy artifact that lacks the dates |

**Conclusion: the historical per-model `account_count` does not exist anywhere in our retained estate.** That
is *why* the import is self-referential — the served artifact was the only surviving record of that quantity.

**NOT ESTABLISHED (explicitly):** whether SmartX can serve historical per-model counts. I touched no vendor
API — egress is gated and it is `0.6.2_AE_PartnerETL~B`'s lane. **My denominator above is OUR estate only.**

---

## 3. PER-DATE VERDICT OVER THE 22 (third state preserved)

| verdict | n | dates |
|---|---|---|
| **filled-by-decouple** | **0** | — the decouple is forward-looking; it cannot retroactively create data |
| **NOT-YET-DETERMINED** (pending `0.6.2~B` vendor capability) | **20** | the 20 enumerated legacy-omitted dates |
| **NOT-YET-DETERMINED** (needs the Eclipse/INF leg, independent of 49F) | **2** | 2026-05-21 · and the 5 "BOTH" dates below overlap the 20 |
| **fillable from EXISTING silver, today, no vendor pull** | **2** | **2026-07-20, 2026-07-21** — roster partitions exist for both (§4 caveat applies) |

**None of the 22 is graded `unfillable`.** Vendor capability is unassessed, so `NOT-YET-DETERMINED` is the
honest grade; it must not collapse into "unfillable."

### 3.1 WHICH FEED must supply each hole — flagged separately at 152147Z

| who must supply it | n | dates |
|---|---|---|
| SmartX (49F) leg only | 16 | 12-24, 12-30, 12-31, 01-02, 02-02, 03-02, 04-01, 05-01, 06-08, 06-26, 06-29, 06-30, 07-09, 07-10, 07-20, 07-21 |
| Eclipse (INF) leg only | 1 | **2026-05-21** |
| **BOTH, independently** | **5** | **06-01, 07-01, 07-13, 07-14, 07-15** |

Cross-check: the 6 Eclipse-side dates (1 + 5) are **exactly** `Global meta.honest_none.model_absent_dates` —
an independent confirmation, not my own derivation. **A collection scoped 21-SmartX + 1-Eclipse leaves those 5
null if the split is date-exclusive**, because the firm-axis poison (`:1656`) fires on either leg.

---

## 4. THE ROSTER — the one thing that CHANGED since 2026-07-22, and it is NOT a drop-in

The 07-22 hold record recorded `fact_model_allocation_roster` as *"only 8 `date=` partitions (07-14..07-21) —
a point-in-time roster, not a history."* **Correct when written. It has since demonstrated accumulation:**
11 partitions today, 2026-07-14..07-24, **same start date**, one per calendar day. It carries the right grain:
`allocation_id` (9,610 unique), `model_id`/`model_name`/`rmid`, `advisor_name`, and **`status`
(open/close/workingClose)** — so closures are represented, which is what defeated the `opened_ts` approach.

**But it does not reproduce the served count.** Positive control against known-good served dates:

| date | SERVED 49F | roster `open` | `open+workingClose` | all rows | exact match? |
|---|---|---|---|---|---|
| 2026-07-16 | **7,126** | 7,123 (−3) | 7,151 | 9,470 | **NONE** |
| 2026-07-17 | **7,140** | 7,127 (−13) | 7,153 | 9,475 | **NONE** |

I also tested a **T-1 offset** (roster `date=D` vs served `D-1`): also no exact match (+1 on 07-17, −5 on
07-18). And the producer's own constant is `ROSTER_OPEN_STATUS = "open"`
(`mdpf_revamp_model_crosswalk.py:43`), so `open` is already the intended filter.

> **THE DECOUPLE IS THEREFORE NOT "REPOINT TO THE ROSTER."** The roster is a *different quantity* — close
> (within ~0.2%) but definitionally distinct from what the served count counts. **A repoint would ship a
> plausible, silently-wrong number** — and being within 0.2% is precisely what would make it survive review.
> Establishing what the served count actually counts is a **prerequisite** to the decouple, and it is the
> unresolved dependency that sets the cost.
> *(The 07-22 comparison is NOT like-for-like — served 07-22 is the frontier stamp from `account_distribution`,
> a different source again; that is the +132, not a roster error.)*

**Retention caveat, stated:** 11 consecutive daily partitions with a stable start over a 2-day observation
window **demonstrates** accumulation. I have **not** read a lifecycle/retention policy on that prefix, so I
cannot guarantee it persists. Worth confirming before the forward-looking design leans on it.

---

## 5. COST / RISK / BLAST RADIUS

**Axis touched:** COUNT only. The value axis derives `model_value` independently, so a count-source change
does not move AUM. *(Caveat: `_assert_cross_axis_coherence` clause (v) ties count-presence to value-presence
where `same_source` — 49F is currently SKIPPED by that clause, and the skip is itself the recorded finding.)*

**Blast radius —** `comp-blast dim_mdpf_aggregate_aua_timeseries`: **"No downstream consumers found … NOT
provably zero"** (EXTRACTED edges only, a stated LOWER BOUND). The real consumer is the portal FE via a
dynamic key read, which the extractor cannot edge — so treat the graph's silence as *unmeasured*, not *zero*.
Known consumer: `ModelPortfolios.tsx` via `globalMdpfData` (per the PRD §2 table).

**⚠ comp-blast returned a HOLD — 4 corpus claims**, incl.
`org/critical_paths/DO_NOT_DECOMMISSION_portal-v2_json_mdpf_49financial_20260722.md`. **Read in full**, see §6.

**Risks, ranked:**
1. **A repoint that looks right.** −3/−13 is inside any plausible tolerance. **This is the top risk and it is
   the reason to resolve the definition before writing code.**
2. **Mis-dating.** The roster partition date vs the counted-state date is unresolved (§4). The producer has
   already been bitten by exactly this — `_assert_cross_axis_coherence` exists because *"2026-07-06 carried
   the 07-10 roster (540) beside correct 07-06 values (true count 474)."*
3. **Detection is absent.** Per the hold record, the fingerprint instrument is **vacuous on 49F** (returns
   `0 matched / 0 misdated` under the EXCLUDE/B basis split) — *"the detection story for this failure is:
   nothing detects it."* Any decouple must ship with its own check.
4. **Backfill persistence cuts both ways.** Because the import is self-referential, a one-time repair *sticks*
   (the next build re-reads it) — and so does any error it introduces.

**Explicitly NOT costed:** the vendor pull. Not my lane.

---

## 6. RELATIONSHIP TO THE EXISTING RECORD — corroboration, NOT discovery

**I did not discover that no per-date 49F count source exists.** `0.4.0_DS_ClientPlatform` (my own base serial)
schema-grounded it on **2026-07-22**, and it is recorded in
`DO_NOT_DECOMMISSION_portal-v2_json_mdpf_49financial_20260722.md` with a candidate table reaching the same
conclusion, an owner already named, and the warning that *"whoever picks this up and sizes it as an afternoon
will abandon it."* Reporting it as a fresh finding would be a credibility error.

**What this pass adds that the record does not contain:**

| new | what |
|---|---|
| 1 | **WHY** the dates are missing — ABSENT-from-axis, exercised on the legacy bytes, 404/404 control |
| 2 | The **self-perpetuating freeze** (the hole re-inherits every build, even with portal-v2 fully intact — the record frames the risk as decommission-triggered) |
| 3 | The **build-gap generator** (`acct[-1]`) — an ACTIVE, open-ended second cause |
| 4 | The roster is **ACCUMULATING**, and **does not reproduce the served count** — updates the record's candidate row in both directions |
| 5 | `fact_rps_s2` carries **all 22 dates** (total-only) — absent from the record's candidate table |
| 6 | The **6-vs-1 Eclipse scope** consequence for the collection |

**Line-number note:** the record cites `:476-500`, `:427`, `:628`, `:812` at the **2026-07-22** vintage; mine
are `:557-591`, `:594-598`, `:1656-1658` **@`3efc9dc6d`** (2026-07-23). Same mechanism, file moved between.

---

## 7. GROUNDING LEDGER

| claim | grade | grounding |
|---|---|---|
| import is self-referential; no LOCF | **SOURCE-CONFIRMED** | `:557-591`, `:594-598` @`3efc9dc6d` |
| the 20 are ABSENT from the legacy axis | **EXERCISED** | oldest version `_4IAznK8GBjxWDd3Sqf2FFBW2xiyWK9j` @2026-07-08T15:00:43Z; 14/15 absent, **404/404 control** |
| 05-21 is the sole legacy-axis exception, matching W-1's class C | **MEASURED, independent method** | legacy axis membership vs W-1's per-firm classification |
| frontier stamp writes last axis date only | **SOURCE-CONFIRMED** | `:1657-1658` @`3efc9dc6d` |
| build gaps ⇒ un-stamped dates | **SOURCE-CONFIRMED + consistent with version history** | mechanism at `:1657-1658`; 9 versions. *The mechanism is confirmed; that it CAUSED these specific nulls is **STRONG INFERENCE** — I did not observe a build.* |
| no retained per-model count history | **MEASURED** | 6 prefixes enumerated, denominators in §2 |
| roster accumulates | **MEASURED** | 8 partitions @07-22 (record) → 11 today, stable start. *Retention policy UNREAD.* |
| roster does not reproduce the served count | **MEASURED, pinned** | 4 filter variants × 2 known-good dates, plus a T-1 offset test — no exact match |
| all 22 present in `fact_rps_s2` | **MEASURED** | 542-partition sweep; **positive control 4/4, negative control weekends ABSENT** |
| **why SmartX's legacy axis lacked the dates upstream** | **UNDETERMINED** | I established the artifact never carried them; I did **not** establish what the vendor-side export did in 2025-12. Vendor egress is gated and not my lane. |

**Explicit-Z throughout** (`s3api` only; no `aws s3 ls`). Denominators printed on every scan. No gold run
(NEVER#4). No producer edit.
