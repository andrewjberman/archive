# BRIEF — Rolling Opal constituents into Cottonwood model attribution (→ Global)

**For:** Andrew · **Author:** `0.7.0_AE_CloudOps~Z` · 2026-08-07 ~04:5xZ
**Requested:** Andrew-direct at this terminal — *"we need those Opal constituent items rolled
into the model attribution for Cottonwood (and thereby aggregated into 'Global') … we need to
know what these untracked constituents are and we need to develop a system that looks for delta
of new child items with Opal tags, rather than searching only top level."*
**Basis:** live read-only BD Rebalancer scan (62 strategies, 62/62 details, 0 failures,
cross-checked against 08-06 landed bronze — zero drift) + source read of the attribution path +
the live gold dimension at `date=2026-08-06`. Andrew's 18-name list reconciled in §5.

---

## 1. THE HEADLINE — it is not a crosswalk gap, it is a FILTER-ORDER defect

**Source-confirmed** at `data/assets/scripts/gold/build_dim_model_portfolio.py:274-277`,
the comment naming it outright — *"STRICT OPAL FILTER -- gold's job, applied to the ASSIGNED
STRATEGY"*:

```
opal_ids       = set(roster[roster.is_opal].model_id)     # roster = TOP-LEVEL strategies only
opal_assigned  = assigned[assigned.model_id.isin(opal_ids)]   # <-- FILTER
    for _, acct in opal_assigned.iterrows():
        leaves = decompose(acct.model_id, blend)               # <-- DECOMPOSE, after
```

**The filter runs BEFORE decomposition and keys on the PARENT STRATEGY'S OWN NAME.** So an
account assigned to a strategy without "Opal" in its name is discarded before its Opal children
are ever walked — its Opal dollars never reach model attribution, and (Cottonwood's non_model
being a BALANCE: `partner_custody_total − model_aua`, slice `:480`) they land in **non-model**.

**The dimension itself is already correct** (`:255-268` builds roster ∪ blend-children, with
`is_opal` computed per child via `rebalancer_schemas.is_opal_name`). The defect is exclusively
the ORDER: filter-then-decompose instead of **decompose-then-filter**.

### Live proof, not just a source read

| Constituent | In BD (my scan) | Attributed in gold 08-06 | Tie |
|---|---|---|---|
| **Opal Fixed Income** | 2 accts (both Anna) | **ABSENT — no row at all** | exact |
| Opal Conservative Growth | 98 accts | 96 accts / $31,773,886.57 | **96 + 2 Anna = 98, exact** |
| Opal Intermediate-Term | 226 | 225 / $76,344,673.23 | −1 residual |
| Opal Short-Term | 107 | 106 / $16,582,075.21 | −1 residual |
| Opal Ultra Short-Term Income | 10 | 7 / $1,731,257.18 | −3 (2 Anna + 1 residual) |
| Opal Long-Term Aggressive | 12 | 12 / $1,148,350.76 | exact |

`Opal Fixed Income` existing in the vendor and being **wholly absent from the attributed
dimension** is the mechanism made visible: its ONLY parents are the two Anna strategies, and
both are filtered out by name before decomposition. The Conservative Growth tie (96+2=98)
confirms the same cause independently.
⚠ **The −1/−1/−1 residuals are NOT explained by this mechanism** and are honestly unresolved —
they need the account-level join (§6 task 1). Do not attribute them to the Anna accounts.

## 2. THE CONSTITUENT INVENTORY — what the constituents actually are

Six distinct Opal building-block models. **All six are CHILD-ONLY — not one appears in the
62-strategy roster**, so any top-level scan is structurally blind to all of them.
`wtd-accts` = accounts × effective allocation (nested-aware).

| Opal constituent | Used by | Accts | Wtd-accts | Tracked in crosswalk? |
|---|---|---|---|---|
| Opal Intermediate-Term | 9 strategies | 226 | 172.3 | yes (`opal_intermediate`) |
| Opal Conservative Growth | 8 | 98 | 76.4 | yes (`opal_long_term_conservative`) |
| Opal Short-Term | 7 | 107 | 33.4 | yes (`opal_short_term`) |
| Opal Long-Term Aggressive | 2 | 12 | 12.0 | yes (`opal_long_term_aggressive`) |
| Opal Ultra Short-Term Income | 8 | 10 | 4.6 | yes (`opal_ultra_short_term`) |
| **Opal Fixed Income** | **2 (both Anna)** | **2** | **0.4** | **name absent — 0 hits*** |

*Positive control: `"Opal Conservative Growth"` = 2 hits in
`mdpf_revamp_model_crosswalk.py`, so the search discriminates. ⚠ **The crosswalk is
model_id-keyed with SmartX-side display names and documents an alias of exactly this kind**
(`opal_long_term_conservative` = SmartX display "Opal Conservative Growth"). **"Opal Fixed
Income" may therefore be a BD-side alias of a tracked model rather than a new one — the
model_id tie settles it (DS~Z), and that tie is task 2 below.** Either way it is unattributed
today, because §1's filter — not the crosswalk — is what excludes it.

## 3. THE STRATEGIES CURRENTLY EXCLUDED

**Opal-composed but NOT Opal-named — invisible to the current filter by construction:**

| Strategy | Accts | Opal share | Constituents |
|---|---|---|---|
| `Anna *9237` | 1 | **90%** | Conservative Growth .36, **Fixed Income .21**, Ultra Short-Term Income .33 (+ DIVZ SMA .07) |
| `Anna *9238`† | 1 | **97%** | Conservative Growth .607, **Fixed Income .16**, Ultra Short-Term Income .20 |

† name carries a **leading space** in BD (`" Anna *9238"`) — an exact-match hazard for any
name-keyed join; use ids, or trim explicitly and say so.

**Measured impact today: 2 accounts.** Small — and that is precisely the point: **the defect is
structural, not proportional.** Every future non-Opal-named strategy built from Opal models is
silently invisible on the day it is created, and the two Anna portfolios are the proof that this
is a real pattern advisors already use, not a hypothetical.

## 4. THE GLOBAL CONSEQUENCE — and it is a SEMANTIC CHANGE, by your ruling

Today these dollars sit in Cottonwood **non_model** (a balance). Under **I-1** (Global non-model
= 49 Financial ONLY), Cottonwood's non-model **does not fold into Global at all** — so today
this exposure reaches Global **nowhere**. Rolling it into Cottonwood **model** attribution moves
it into `model_aua`, which **does** fold into Global's model total.

⛔ **This therefore CHANGES A SERVED NUMBER — Global model AUM increases.** That is exactly what
you asked for, and it is your ruling to make; the brief names it explicitly so nobody downstream
treats it as a silent fix. It needs the PRD/shape discipline on the way in: pinned baseline, the
delta stated in dollars before it ships, and `point_class`/provenance labels honest about the
restatement. It is **not** in-scope for the canonical-shape program (that project is shape-only).

## 5. YOUR 18-NAME LIST, RECONCILED — 4 deltas, one of them live

Your list ties to my scan **exactly**: 22 Opal-touching strategies on the live plane − 18 named
= 4 unnamed, and they are:

| Not on your list | Accts | Read |
|---|---|---|
| `Opal Sat 50+ 15% cash` | **1** | ⚠ **carries a LIVE account** — deliberate omission or a miss? Your call. |
| `Opal Long Term Conservatiove` *(sic)* | 0 | empty; also misspelled in BD |
| `Opal Satellite 90` | 0 | empty |
| `Opal Long Term Aggressive` | 0 | empty (distinct from the constituent `Opal Long-Term Aggressive`) |

Three of four are zero-account, consistent with an empties filter — **`Opal Sat 50+ 15% cash` is
the one that does not fit that pattern.** One name differs textually: your `Moderate Income
Portfolio` is `Opal Moderate Income Portfolio` in BD (already attributed, $5,013,398.18).

## 6. TOMORROW'S WORK — ordered, with the discriminating question each task answers

1. **Size it in dollars.** Join the 2 Anna accounts (via `/api/accounts/search`, the runner's
   existing read) to `fact_holdings` values, split by effective allocation. *Answers: what does
   Global's model total actually move by?* Nothing ships before this number exists.
2. **Resolve `Opal Fixed Income` on model_id, not name** (DS~Z owns the crosswalk). *Answers:
   new model, or BD-side alias of a tracked one?* Two different remedies.
3. **Invert the filter order** in `build_dim_model_portfolio.py`: decompose EVERY assigned
   strategy, then apply `is_opal` **at the leaf**. Keep non-Opal leaves visible with
   `is_opal=False` (the file already does this for sleeves — `:73` *"carried so a non-Opal blend
   target is VISIBLE, not hidden"*), so `Anna *9237`'s DIVZ SMA 7% stays honestly non-Opal
   rather than being swept in. **This one change closes the whole class.**
4. **Re-verify the conservation gate.** The slice asserts `sum(by_model) == model_aua` (`:549`);
   changing what enters attribution changes both sides — exercise it against a mutation before
   trusting a pass.
5. **The delta detector (§7).**

## 7. THE DELTA SYSTEM — recursive by construction, and NOT a monitor

**What you asked for: detect new child items carrying Opal tags, not just top-level.** Design
that follows from §1 — and deliberately shaped to respect the standing moratorium:

> ⚠ **This is NOT an alarm, SNS topic, or freshness-checker.** It is a **producer-side
> assertion that lands as DATA in the run manifest**, and fail-closes the build on an
> unrecognised constituent. Detection belongs to the pipeline that already walks the tree —
> not to a second instrument watching it. If you later want a notification on top, that is a
> separate explicit ask.

**Mechanism:**
- The producer already walks `roster ∪ blend-children` (`:255-268`) and already computes
  `is_opal_name` per child. **Extend that walk to be FULLY RECURSIVE** (the current scan depth
  is 1 across today's book — every Opal constituent sits at depth 1 — so nested blends are
  **untested territory today, not proven absent**; the walk must not assume depth 1).
- **Persist the constituent set with its hash** in the run manifest: every
  `(child_model_id, child_model_name, is_opal, depth, parent_ids[])`.
- **The delta is then a set-difference against the prior run's manifest**, computed by the
  producer, recorded as manifest rows: `constituents_added` / `constituents_removed` /
  `constituents_renamed`.
- **Fail-closed rule:** a constituent that is `is_opal=True` **and** absent from the crosswalk
  → the build **refuses** and names it (the estate's existing `raise-on-unknown F5` posture,
  and the same shape as tonight's L-1 key-set gate that correctly refused a bad emission).
  A silent `WARN … folded into non_model` is exactly how `Opal Fixed Income` became invisible —
  **that warn should have been a refusal.**
- **Name-token caveat, load-bearing:** `is_opal_name` is a substring test
  (`"opal" in name.lower()`, `rebalancer_schemas.py:197-202`). It is the right default, and it
  will match any future model containing "opal" anywhere. The detector must therefore report
  **candidates for a human ruling**, never auto-enrol into attribution.

**Why this beats a scanner:** a separate scanner is a second instrument that can disagree with
the producer and drift from it. Putting the assertion INSIDE the producer means the thing that
computes attribution is the same thing that declares what it could not classify — it cannot
silently skip what it did not understand.

## 8. What is NOT in this brief

No code changed, no crosswalk edited, no schedule touched, nothing deployed. The BD scan was
read-only on the **Cottonwood tenancy only** (`blackdiamond/cot/session`); **49F was not
queried** and a 49F-side equivalent is a separate authorized run — worth asking whether the
same filter-order defect exists there, since the code path is shared.
