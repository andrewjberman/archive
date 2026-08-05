# MDPF_CANRTE.GRF — Global T+2 Roll-Forward: SCOPING (design-only)

**TO:** `MDPF_CANRTE.GRF.global-t2-rollforward-scoping` · **Seat:** `0.4.0_DS_ClientPlatform`
**Issued:** 2026-08-04 (`2.0.0_SA_COO`) · **GO:** 2026-08-05T161409Z · **This document:** 2026-08-05
**Grounding vintage:** every `file:line` below is read at **HEAD `49d4537e62`** unless stamped otherwise.
**Status:** design-only. Zero code written. Zero serve contact. No carry engine built. No window widened.

---

## 0. THE ONE-PARAGRAPH ANSWER

Andrew's roll-forward is **already built for two of his three surfaces, and needs building for one.**
`aggregate-aua-timeseries.json` carries today (ruled, labeled, self-overwriting). `aum-metrics.json`
inherits that carry **by construction** — it is a thin projection off the fold's frontier row and already
emits a `carried` flag — so it needs no carry design, only one count-path correction.
**`account-distribution.json` is the entire real design surface**: it has no carry machinery at all, it sits
*upstream* of the fold that carries, and it is a **count** artifact — which collides with a ruled law that
counts are never carried. That law has a narrow ruled exception whose shape is exactly what this needs.
**The implementation surface for `0.5.0_AE_OpalETL` is one producer, not three.**

---

## 1. SEAT WALL (Andrew's own naming — recorded per the TO)

> **`0.5.0_AE_OpalETL` implements the cloud side and ANDREW BRINGS THEM IN HIMSELF.**

This document **hands off** to that seat. **Nobody — not me, not COO, not CTO — dispatches `0.5.0_AE` on
this.** It is written cold-readable so that seat can act on it without a briefing. It is delivered to COO +
CTO for review only; it travels to `0.5.0_AE` **when that seat arrives asking, citing Andrew's word.**

## 2. THE RULING (verbatim — the phrasing is the ruling)

Andrew-direct, CTO terminal, 2026-08-04 ~17:15Z:

> "Also I have a better idea for 'Cottonwood'. Here is the issue, 49 Financial and Inflection are both
> reliably T+1, but Black Diamond, which is the Cottonwood data sources, is for all practical purposes T+2.
> The issue that we're encountering is that we don't know how to aggregate the 'Global' Scope
> aggregate-aua-timeseries.json and aum-metrics.json with that lag. Here is my solution: We just roll
> forward the last day's value as an interim solution and that is overwritten by the real value as it comes
> in. This keeps everyone in the same time period. This change would have to be managed in both the 'Global'
> aum-metrics.json, account-distribution.json, and aggregate-aua-timeseries.json. Let's get it scoped by
> 0.4.0_DS_ClientPlatform and I will bring in 0.5.0_AE_OpalETL to handle the cloud implementation."

## 3. THE TWO LAW DISPOSITIONS — CARRIED VERBATIM, NOT RE-LITIGATED

1. **no-LOCF remains the PER-FIRM law, untouched.** The Global fold gets a **declared, marked** carry — the
   same family as the existing carry-window machinery. Per-firm artifacts stay honest-None. This design
   touches no per-firm artifact.
2. **The 1646Z frontier-clamp edict [a] STANDS** as the immediate fix. The roll-forward is the durable layer
   that makes the clamp *naturally non-binding*. It is **NOT read as replacing the clamp absent Andrew's
   word.** This design does not remove, modify, or gate the clamp. (See §8.)

---

## 4. THE DEPENDENCY ORDER IS THE DESIGN

Derived from `comp-pipescript io --pipeline mdpf` on all three producers (run log in §11):

```
  order 70   dim_mdpf_account_distribution.py       -> account_distribution.json    [NO CARRY]
                 |  reads gold/mdpf_revamp/cottonwood/account_units.json (sidecar)
                 v  (the fold reads this for its FRONTIER counts -- ad_frontier)
  order 80   dim_mdpf_aggregate_aua_timeseries.py   -> aggregate_aua_timeseries.json [CARRIES]
                 |  the carry lives HERE and only here
                 v
  order 90   dim_mdpf_aum_metrics.py                -> aum_metrics.json             [INHERITS]
                 thin projection off the fold's frontier row
```

**Everything follows from this ordering.** The carry lives at 80. Whatever is downstream of 80 inherits it
for free. Whatever is upstream of 80 does not — and `account_distribution` (70) is upstream **while also
being an input to 80's frontier counts.** That is why the third surface is the hard one and the first two
are nearly free.

---

## 5. SURFACE-BY-SURFACE

### 5.1 `aggregate-aua-timeseries.json` — **NO DESIGN REQUIRED. Mechanism is LIVE.**

Per the 1738Z amendment, confirmed independently at HEAD:

| Property | Where it lives at HEAD `49d4537e62` |
|---|---|
| Carries cottonwood's last **measured** value within the declared window | `dim_mdpf_aggregate_aua_timeseries.py:1886-1906` |
| Window = roster-declared, **never inferred** | `:1897-1898` → `_cot_carry_policy` `:1780-1791` |
| Marks every carried point `carried_at_declared_cadence(as_of=...)` | `:2000` |
| Per-partner vintage map `as_of_by_partner` | `:2016-2018` |
| Carry source is the last **MEASURED** date (never a band estimate) | `:1891-1896`, rationale `:1879-1881` |
| Overwrites naturally on rebuild when real data arrives | full-rebuild producer; carry map recomputed per build |
| Same mechanism, one leg over, for inflection | `:1910-1934` |

Andrew's "marked interim, overwritten by the real value" is **already the deployed semantic, verbatim.**
The only reason today clamped to 07-30 was that the freeze **exceeded** the declared window and the bounded
carry correctly refused. **The fix for a frozen pipeline is the pipeline** (unfrozen 08-05) — never a wider
window. **Nothing to design here. Cite it and move on.**

> **RECORD NOTE (per the TO, folded in):** DE's frontier clamp and the fold's carry were built as **two
> halves of one mechanism without either seat knowing it.** The inversion Andrew intuited is those two
> halves meeting.

### 5.2 `aum-metrics.json` — **INHERITS THE CARRY. One real gap.**

`dim_mdpf_aum_metrics.py` is **by design a thin projection off the aggregate spine's frontier**
(`:218-220`, verbatim). Consequences, all source-confirmed at HEAD:

- **Headline values already carry.** `compose_current` takes total/model/non_model from *"the GLOBAL spine's
  own frontier values (as_of_last row) — the ruled one-live-composition fold, **carry-within-window, labels
  and all**"* (`:144-145`). A carried frontier row propagates with zero further work.
- **It already emits a carried marker.** The fee-basis cottonwood component emits
  `{"as_of": cot_asof, "carried": bool(cot_asof and cot_asof != period)}` (`:198-199`), read from the
  frontier row's `as_of_by_partner`. **Andrew's marked-interim semantic is already present on this surface.**
- **`by_model[].aum` inherits** — it is the `model_value` frontier off the same fold row.

**THE GAP — and it is the only one:** `by_model[].account_count` does **not** come from the fold's carried
row. It comes from `account_distribution`'s `meta.account_count_by_model_key` (`:36`, ruled CTO 190518Z (a);
producer side `dim_mdpf_account_distribution.py:373-378`). So on a cottonwood-lagged day
**`by_model[].aum` is carried-and-marked while `by_model[].account_count` beside it is not** — two vintages
in one row, unlabeled. This is the *per-model* concern scope item 1 names, and it resolves entirely into
§5.3: **fix the count at its source (70) and this row becomes coherent by construction.**

> ⛔ **A TRAP `0.5.0_AE` MUST NOT WALK INTO — source-confirmed, would hard-fail production.**
> `_assert_measured_frontier` (`:217-239`) **raises `SystemExit`** if the spine's frontier `point_class` is
> anything other than `"measured"`. Carried rows pass **only because the fold deliberately keeps
> `point_class == "measured"` on a carried row** — *"point_class stays measured on a carried row: the carried
> value IS [a measurement]"* (`dim_mdpf_aggregate_aua_timeseries.py:2345`).
> **THEREFORE: marking MUST NOT be expressed as a new `point_class` value.** Introducing
> `point_class="carried"` to mark interim points would trip the R-4 guard and take `aum-metrics` down
> **hard, at build time, on the first lag day.** Marking belongs in the *additive* channels
> (`as_of_by_partner`, `carried_at_declared_cadence(...)`, a `*_as_of` sidecar field) — never in
> `point_class`. The R-2 provenance-coherence gate (`:1619-1638`) already validates the two channels agree
> and is already carry-aware (`cot_carry` passed in at `:1530`, `:2210`).

### 5.3 `account-distribution.json` — **THE ENTIRE REAL DESIGN SURFACE**

This producer has **no carry machinery of any kind.** It is a current-snapshot builder off monolith silver,
and its Global scope folds cottonwood from a sidecar artifact:

```
COTTONWOOD_UNITS_KEY = "gold/mdpf_revamp/cottonwood/account_units.json"    :304
_cottonwood_sidecar()  -- "FAIL-CLOSED for global: once cottonwood is in the
    Global distribution contract, a missing sidecar [refuses] the global build"  :316-323
build_firm_distribution(): if firm_id == "global": sc = _cottonwood_sidecar()   :343-348
```

**Two failure modes on a cottonwood-lagged day, and they are opposite:**

| Sidecar state on the lagged date | Current behaviour | Verdict |
|---|---|---|
| **MISSING** | `_cottonwood_sidecar()` refuses → **the entire Global account-distribution build fails** | Loud. A Global surface outage. |
| **STALE** (present, T-2 vintage) | Silently folds a **T-2 cottonwood roster** into **T-1** 49F+INF counts | **Silent. Unmarked vintage mixing.** |

The stale case is the dangerous one, and **it is a class this estate has already been burned by twice, both
recorded in source at HEAD:**

- Inflection, 2026-07-06: a date-joined import put **eclipse's 07-10 roster (540) beside the true 07-06
  count (474)** — a +66/-66 jump-and-revert *"on exactly the dates the sovereign flagged"*
  (`dim_mdpf_aggregate_aua_timeseries.py:1146-1156`).
- Global, same class: **7620 on 07-06 vs the true 7554** — a +66 excursion at **0.86% of base, under every
  percentage floor we had** — and, decisively, **the composition identity `global == 49F + inflection` held
  EXACTLY 7/7 dates while the whole sum sat on the wrong day, so the coherence check PASSED and still
  shipped a foreign-day roster** (`:2111-2118`).

> **THIS IS THE DIRECT ANSWER TO SCOPE ITEM 1's "the composition gate MUST HOLD under carried legs — state
> how."**
> **The composition gate holding is NOT evidence of correctness under a carried leg, and this estate has the
> measurement to prove it.** The gate is a *within-date* identity: it checks `global == Σ(firm legs)`. A
> uniformly vintage-shifted roster satisfies that identity perfectly. **The gate cannot see the axis the
> carry moves along.** Any design that offers "the composition gate still passes" as its safety argument is
> reproducing the 07-06 defect with a green check beside it.
> **The control must therefore be a VINTAGE control, not a sum control:** the gate must assert that every
> leg contributing to a Global count declares the **same `as_of`**, or that any leg whose `as_of` differs
> is **explicitly labeled carried with its vintage**. Same-snapshot **by construction**, which is precisely
> the remedy pattern both incident comments above already reached for (`:1153`, `:2117-2118`).

#### The counts law, and the ruled exception that is the design shape

The fold states **twice**, deliberately, that counts do not carry:

> *"VALUES are carried, rosters/counts never (the signed band schema's own law, third application) — the
> count fold below is deliberately untouched."* — `:1881-1883`
> *"Counts are NEVER carried — the count loop below deliberately takes no redirect."* — `:2088-2089`

And the code honours it: the value loop redirects through the carry map (`rd = carry.get(d, d)`, `:2091-2092`)
while the count loop **deliberately keys on `d`, never `rd`** (`:2124-2132`).

**But "never" is not absolute — there is a ruled, narrow, marked exception already in production:**

```
FLAG-2 FRONTIER-ADVANCE PRESERVE (CTO ruling 051427Z; enumerated keys ONLY):
value advanced, count source structurally lagging -> carry the last known count
forward with its date IN-BAND (count_as_of). Any other key's in-range None stays
poison at the coherence gate.                        :2154-2158, SMA_COUNT_PRESERVE_KEYS
```

**That is the exact shape this design needs, and it is precedent rather than invention:**
a count carry that is **(a) enumerated, not general; (b) stamped with its own vintage field (`count_as_of`);
(c) leaves every non-enumerated key's None as poison at the gate.**

**So the apparent collision between Andrew's ruling and the counts law is not a sovereign fork.** The law
reads *"counts are never carried **by default**; only by enumeration, with a vintage stamp, under a gate."*
Andrew's ruling names `account-distribution.json` as an enumerated surface. **The design is to extend an
existing ruled pattern to a named surface — not to overturn a law.** I flag it here rather than deciding it
silently, per §10.

#### What `0.5.0_AE` actually builds

1. **A declared-window carry on the cottonwood sidecar read**, mirroring the fold's own policy
   (`_cot_carry_policy`): if the sidecar's vintage is within cottonwood's **roster-declared 3 TD** window,
   fold it and **stamp it**; beyond the window, cottonwood is **absent for real** and the Global count goes
   honest-None — *the headline visibly drops, and that is the outage signal* (`:1876-1878`).
   **The window is read from the roster. It is not widened, and not re-inferred.**
2. **A vintage stamp on the artifact**, additive-channel only: an `as_of`-per-leg field on the Global count
   (naming shape: reuse `count_as_of` from the FLAG-2 precedent, and `as_of_by_partner` from the fold, so
   the estate keeps **one vocabulary** — the same one-vocabulary condition already invoked at `:1201`).
3. **Replace fail-closed-on-missing with carry-then-honest-None.** The current hard refusal (`:316-323`) is
   correct today *precisely because there is no carry*; once the carry exists, a missing sidecar inside the
   window is a carry, and outside it is an honest-None — **not a Global build outage.**
4. **The vintage control from the box above**, at the composition gate.

---

## 6. STEADY-STATE CONTRACT (scope item 2)

**Stated plainly:**

> Cottonwood delivers at **T+2**. Its declared window is **3 trading days**
> (`partner_roster.json:gate_policy.per_partner_max_lag_trading_days.cottonwood = 3`, provenance:
> *"D+2 vendor cadence measured 14 of 14, plus 1 trading day of slip tolerance"*). T+2 sits **inside** 3 TD
> with one day of slip margin. Therefore cottonwood is **always carried on the T+1 tail**, and the **Global
> frontier is at T+1 every day** — the same time period for everyone, which is Andrew's stated objective.
>
> **PROVIDED THE DAILY CHAIN RUNS.**

**That proviso is the whole risk, and it is not mine to absorb.** The carry is *bounded by design*: it
refuses beyond the declared window, which is exactly what produced the 07-30 clamp. **A carry cannot rescue
a pipeline that does not run** — it converts a silent freeze into a visible drop, which is the correct
behaviour and not a bug to design around.

**NAMED AS THE REAL DEPENDENCY AND ROUTED, NOT ABSORBED HERE:** the **NEVER#4 schedule work** — a production
pipeline whose only trigger is another pipeline's completion marker **has no schedule and is a defect**
(CLAUDE.md NEVER#4; measured instance: `mdpf-daily-refresh-trigger` `ScheduleExpression: None`, which froze
the client-facing Model Portfolios product for six days with fresh inputs sitting unused).
**Owner: CTO to route. This design depends on it and does not attempt to compensate for it.**

## 7. LAG DECLARATIONS AS W-1 BINDING ROWS (scope item 3)

**A lag is a DECLARED property, never re-inferred at run time.** Status at HEAD:

- **The declaration exists** and is roster-derived:
  `route_bindings.yaml:140` — `{type: roster-derived, file: partner_roster.json, field:
  gate_policy.per_partner_max_lag_trading_days, note: "window ALONE, cadence already composed in — CTO
  233402Z; TRADING DAYS end to end"}`, with a code-literal tie at `:142`.
- **Declared values:** 49financial 2 TD · inflection 2 TD · **cottonwood 3 TD**.
- **Two properties that must survive into the L3 Global-fold contract row family, both already ruled:**
  1. **The window ALREADY CONTAINS the vendor cadence — the cadence offset is NEVER added on top**
     (CTO 233402Z; `dim_mdpf_aggregate_aua_timeseries.py:1874-1875`). Adding it would silently double the
     tolerance.
  2. **Measured from the offset-0 frontier**, not from the partner's cadence-adjusted frontier
     (`partner_roster.json:_basis_note`: *"the two bases differ by the cadence offset and silently swapping
     them would tighten or loosen every threshold at once"*).
- **THE GAP TO CLOSE IN W-1:** the `carry_window` binding row currently sits under **cottonwood's** section
  only. The **Global fold** L3 contract needs its own row family declaring, per contributing firm, the
  effective lag the fold assumes — so the Global fold's carry basis is **declared at the fold**, not
  inherited by proximity from one partner's block.
- **⚠ Flagged, not adjudicated:** `partner_roster.json` records cottonwood's window with the provenance note
  **"Not yet gated."**, and `gate_coverage` states cottonwood is `NOT_COVERED` — *"absent from the legacy
  gate's partner set entirely, so no cottonwood staleness can defer."* **The declaration this design leans
  on is real; the enforcement behind it is not yet live.** The roster's own binding says it best: *"A GATE
  THAT CANNOT SEE A PARTNER REPORTS GREEN ON THAT PARTNER'S WORST DAY."* Routed to CTO with §6.

## 8. FRONTIER-CLAMP INTERACTION (scope item 4)

The clamp **already reads carried points as PRESENT**, because a carried row keeps
`point_class == "measured"` (`:2345`) and carried rows are measurement-class per the fold's label-the-basis
law (`dim_mdpf_aum_metrics.py:126`). **Therefore, once the two derived artifacts carry, the Global frontier
is complete at T+1 every day and the clamp simply stops clamping — it becomes naturally non-binding with
zero further FE work.** **It is NOT removed by this design.** The 1646Z edict [a] stands as the immediate
fix; removal would require Andrew's word, which this document does not assume and does not request.

---

## 9. HANDOFF — `0.5.0_AE_OpalETL` (scope item 5, cold-readable)

**Read §4 first (the 70→80→90 ordering); it explains why this list is short.**

| # | Artifact | Producer | Work | Size |
|---|---|---|---|---|
| 1 | `aggregate-aua-timeseries.json` | `dim_mdpf_aggregate_aua_timeseries.py` | **NONE.** Mechanism live. Cite `:1886-1906`, `:2000`, `:2016-2018`. | zero |
| 2 | `aum-metrics.json` | `dim_mdpf_aum_metrics.py` | **NONE for values** (inherits; already emits `carried`+`as_of` at `:198-199`). Coherence of `by_model[].account_count` follows from #3. | ~zero |
| 3 | `account-distribution.json` | `dim_mdpf_account_distribution.py` | **ALL OF IT** — the four items in §5.3. | the real work |

**INPUTS**
- Window: `partner_roster.json` → `gate_policy.per_partner_max_lag_trading_days.cottonwood` = **3 TD**.
  Read it; never hardcode; never widen.
- Carry-policy reference implementation to mirror: `_cot_carry_policy` (`:1780-1791`) and the carry loop
  (`:1886-1906`). **Mirror the policy read — do not build a second carry engine.**
- Vintage-stamp vocabulary to reuse: `count_as_of` (FLAG-2, `:2154-2158`), `as_of_by_partner` (`:2016-2018`),
  `carried_at_declared_cadence(as_of=...)` (`:2000`).
- Sidecar: `gold/mdpf_revamp/cottonwood/account_units.json` (`:304`).

**HARD CONSTRAINTS — each one is a production failure if violated**
1. **NEVER express the carry marking as a `point_class` value.** `_assert_measured_frontier`
   (`dim_mdpf_aum_metrics.py:217-239`) `SystemExit`s on any non-`"measured"` frontier class. Additive
   channels only. (§5.2 box.)
2. **NEVER widen the window.** A freeze exceeding the window is the pipeline's defect (§6), and the bounded
   refusal is the outage signal.
3. **Carry source must be the last MEASURED value, never a band/interpolated estimate** — carrying an
   estimate under a carried label *"would launder the interpolation taint out of the provenance lattice"*
   (`:1879-1881`).
4. **Counts carry only by ENUMERATION, with a vintage stamp** — the FLAG-2 shape. A general count carry is
   against ruled law (§5.3).
5. **Per-firm artifacts stay honest-None.** The carry is a **Global-fold** refinement only.
6. **Do not touch the frontier clamp** (§8).

**ACCEPTANCE SHAPE — the marked-interim round trip, end to end**
The acceptance test is a **three-state round trip on one date**, not a single read:

1. **INTERIM SERVED.** On a cottonwood-lagged build date `D`: Global `account-distribution.json` contains a
   cottonwood contribution, the artifact **declares its vintage** (`as_of` < `D`) and is
   **reader-distinguishable as carried** without external knowledge. Global `aum-metrics.json` shows the
   matching `"carried": true` on the cottonwood component. **The Global frontier is `D`, not `D-1`.**
2. **REAL ARRIVES → OVERWRITE.** Cottonwood's real `D` data lands; rebuild. The same slot now shows the
   **real value**, the vintage stamp reads `D`, and the carried marker is **gone**. **Idempotent:** a second
   rebuild with no new data changes nothing (byte-stable). A third with the real data present produces the
   identical artifact as the second.
3. **BEYOND THE WINDOW → HONEST DROP.** Force a lag exceeding 3 TD: cottonwood goes **absent for real**, the
   Global count goes honest-None, and **the headline visibly drops.** *That drop is the required outcome,
   not a regression* (`:1876-1878`).

**Plus the vintage control (§5.3 box):** an assertion that every leg contributing to a Global count either
shares one `as_of` or is explicitly labeled carried with its own. **Do not accept "the composition gate
passes" as evidence** — it passed on the 07-06 defect (`:2111-2118`).

**MUTANT CONTROL (required before first gating use):** flip one carried leg's vintage stamp to the wrong
date and confirm the vintage control **FAILS**. A control never observed failing has not been tested.

## 10. WHAT I DID NOT DECIDE

Per the TO and COO's GO, I name rather than resolve:

- **The kill-path open call at Andrew** — (a) re-source 11 cohorts at their grain then kill the runner
  whole, vs (b) narrow the kill and retain the partition producer. **This design holds under BOTH**: it
  changes carry/marking semantics inside three Global surface producers and is indifferent to which producer
  ultimately owns the partition. **I presumed neither and waited on neither.** No fork surfaced that forces
  different designs.
- **PRODUCER ASSUMPTION, stated explicitly rather than assumed silently** (per COO's instruction): this
  design assumes the **canonical spine** producers — `data/mdpf/scripts/gold/dim_mdpf_*.py` at HEAD, the
  path whose first full scheduled cycle ran clean 2026-08-05 (`mdpf_daily_20260805_130109`). It does **not**
  assume the legacy runner partition. If the duality outlives this design, item 3 in §9 must land on the
  spine producer, and the legacy path's Global account-distribution would retain the unmarked
  vintage-mixing defect until it is retired.
- **The counts-law extension (§5.3)** — I read it as extending an existing ruled exception (FLAG-2), not
  overturning the counts law. **Surfaced for CTO's ruling rather than assumed.** If CTO reads it as a new
  law rather than an extension, that is a ruling I do not hold.
- **The un-gated cottonwood window (§7)** — declared but `NOT_COVERED` by the live gate. Routed, not fixed.

## 11. COMPILER TOOLS

| Tool | Invocation | Result |
|---|---|---|
| `comp-glob` | `**/dim_mdpf_*.py` | 5 producers located, with systems-context routing |
| `comp-which` | "which script produces the Global aum-metrics.json and account-distribution.json" | near-tie → `comp-estate` / `comp-pipescript io`; followed the router to `comp-pipescript` |
| `comp-pipescript io` | `dim_mdpf_aggregate_aua_timeseries.py --pipeline mdpf` | order 80; reads cottonwood agg + `{*}/account_distribution.json`; 5 monolith silver reads |
| `comp-pipescript io` | `dim_mdpf_aum_metrics.py --pipeline mdpf` | order 90; **reads `global/aggregate_aua_timeseries.json`** → established the inheritance in §5.2 |
| `comp-pipescript io` | `dim_mdpf_account_distribution.py --pipeline mdpf` | order 70; reads `cottonwood/account_units.json` → established the upstream position in §5.3 |
| `comp-grep` | `lag` in `route_bindings.yaml` | 2 matches → the roster-derived carry_window binding (§7) |
| `comp-grep` | `per_partner_max_lag_trading_days` (bare) | **0 files scanned — reported as FAILED RETRIEVAL, not a real zero.** Re-ran with an explicit pathspec. *(The tool printed its own denominator and refused to render an empty scan as a finding — the control working.)* |
| `comp-to` | `MDPF_CANRTE.GRF.global-t2-rollforward-scoping` | session TO_ID set race-free |

**`--pipeline mdpf` was passed on every `comp-pipescript io` call** (flagless is `rc=2` REFUSED since 07-30).
No gold script was run; no `comp-pipescript deployed` / `postdeps` / `comp-validate` was required —
**this TO is design-only, zero code, zero serve contact.**

---

## 12. SELF-AUDIT (Phase-2 mandate)

| Required | Status |
|---|---|
| All six scope items present | ✅ §5.1–5.3 (1) · §6 (2) · §7 (3) · §8 (4) · §9 (5) · §13 (6) |
| Marking mechanism artifact-carried + reader-distinguishable | ✅ §5.2, §5.3; vocabulary reused, not invented |
| Overwrite semantics idempotent | ✅ §9 acceptance state 2 (byte-stable re-run) |
| Lag rows declared-not-inferred | ✅ §7, roster-derived, with the gap + the un-gated caveat named |
| Clamp interaction stated | ✅ §8 — stands, becomes non-binding, not removed |
| `0.5.0_AE` handoff cold-readable | ✅ §9 — table, inputs, 6 hard constraints, 3-state acceptance, mutant control |
| Both law dispositions carried verbatim, not re-litigated | ✅ §3 |
| Seat wall recorded in the artifact | ✅ §1 |
| Zero code, zero serve contact | ✅ |
| Every claim `file:line @ commit` or labeled INFERRED | ✅ all at HEAD `49d4537e62`; §10 items labeled as undecided |
| No carry engine designed | ✅ §9 mirrors the existing policy read |
| No window widening | ✅ §6, §9 constraint 2 |

## 13. SEQUENCING (scope item 6 — mine)

GRF is delivered in this session ahead of everything else at this seat, per the GO. **W-3 (6b/6c/6e) is next**
on COO's TO. My own backlog read (61 active TOs at this seat per
`to-check.py --all --assignee`, not the 16 pending shown by `get_agent_status`) follows W-3, per COO's ask.

---

**Delivered to:** `2.0.0_SA_COO` + `1.0.0_SA_CTO` (program triangle).
**NOT delivered to `0.5.0_AE_OpalETL`** — that seat arrives on **Andrew's** bring-in, citing his word. §1.

*— `0.4.0_DS_ClientPlatform`, 2026-08-05*
