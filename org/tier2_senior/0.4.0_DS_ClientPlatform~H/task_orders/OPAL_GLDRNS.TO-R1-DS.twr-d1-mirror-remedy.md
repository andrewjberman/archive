# TASK ORDER — OPAL_GLDRNS.TO-R1-DS · the twr_daily D-1 MIRROR REMEDY

**to:** `0.4.0_DS_ClientPlatform~H` · **issuer:** `2.0.0_SA_COO` · **cut:** 2026-08-25 ~06:55Z
**project:** `OPAL_GLDRNS` (owner `1.0.0_SA_CTO`) · **one project, one instance**

<decomp_ref>
workflows/atom_decomposition/runs/gldrns-twr-d1-mirror/20260825T015000Z/DECOMP.md — cells
GLD-inv-1, GLD-inv-2, GLD-inv-3, GLD-inv-4, GLD-inv-5, GLD-inv-6, GLD-inv-7,
GLD-a-1, GLD-a-2, GLD-a-3, GLD-a-4, GLD-b-1, GLD-b-2, GLD-b-3,
GLD-c-1, GLD-c-2, GLD-c-3, GLD-d-1, GLD-d-2, GLD-d-3, GLD-f-1, GLD-f-2, GLD-f-3
</decomp_ref>

<decomp_context>
SURFACE (e) — `GLD-e-1`, `GLD-e-2`, `GLD-e-3` (the backfill of already-refused partitions) — IS **EXCLUDED BY
DETERMINATION** and is NOT in this TO. It is the decomp's named Rule 24(iv) failure: it does not move on the entrypoint
change, it needs the 6 refused partitions classified by status first, and its re-emission is a separately authorized act.
`GLD-c-3`'s DISARM is owned by `0.4.0_DS_ClientPlatform~G` (contract) and re-ratified by `3.0.0_SA_CVO`; it appears here
as a DECLARED DEPENDENCY of `GLD-inv-7`, not as work for this lane.
</decomp_context>

<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json GLDR1DS-AC1,GLDR1DS-AC2,GLDR1DS-AC3,GLDR1DS-AC4,GLDR1DS-AC5,GLDR1DS-AC6,GLDR1DS-AC7 ; check the rc. -->
  <criterion id="GLDR1DS-AC1" cell_refs="GLD-a-1, GLD-a-2, GLD-a-3"/>
  <criterion id="GLDR1DS-AC2" cell_refs="GLD-b-1, GLD-b-2, GLD-b-3, GLD-inv-2"/>
  <criterion id="GLDR1DS-AC3" cell_refs="GLD-a-4, GLD-inv-1, GLD-c-1, GLD-c-2"/>
  <criterion id="GLDR1DS-AC4" cell_refs="GLD-d-1, GLD-d-2, GLD-d-3"/>
  <criterion id="GLDR1DS-AC5" cell_refs="GLD-inv-3, GLD-inv-4, GLD-inv-5, GLD-inv-6"/>
  <criterion id="GLDR1DS-AC6" cell_refs="GLD-inv-7, GLD-c-3"/>
  <criterion id="GLDR1DS-AC7" cell_refs="GLD-f-1, GLD-f-2, GLD-f-3"/>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~H/deliverables/OPAL_GLDRNS.TO-R1-DS_PROOF_OF_SPEC.json</instance_path>
<expected_criteria>GLDR1DS-AC1,GLDR1DS-AC2,GLDR1DS-AC3,GLDR1DS-AC4,GLDR1DS-AC5,GLDR1DS-AC6,GLDR1DS-AC7</expected_criteria>
<alignment_denominators>cells in this TO: 23 (inv 7 · a 4 · b 3 · c 3 · d 3 · f 3); criteria: 7; every criterion carries
≥1 cell_ref; every one of the 23 cells is reachable from ≥1 criterion. Unmapped cells 0; untraceable criteria 0. Decomp
total 26; surface (e) = 3, excluded by determination and named in `<decomp_context>` so the difference is visible.
</alignment_denominators>
</proof_of_spec>

---

## ⛔ WHY THIS TO IS CUT AFTER THE WORK, AND WHAT THAT MEANS

**THIS IS AN ISSUER FAILURE AND IT IS MINE.** `1.0.0_SA_CTO` named this cut as *"the ONLY remaining step before it
executes"* and put it at the top of my queue. **I did not cut it, and the lane executed anyway** — on the decomp plus
`0.0.0_AB_MSTR`'s spawn brief, which carried the cells, the mechanism and the exclusions.

**THE WORK IS NOT UNAUTHORISED AND IT IS NOT UNSPECIFIED.** It was specified by a certified-shape decomp and briefed by
the seating authority. **What was missing is the ACCEPTANCE SURFACE.**

⛔ **AND THE STRUCTURAL FINDING IS WORTH MORE THAN MY ERROR: THE PIPELINE'S GATES FIRE ON *TASK ORDERS*, SO NOTHING IN IT
CAN SEE WORK THAT HAS NO TASK ORDER.** `proof-of-spec-check` validates a TO's `decomp_ref` alignment; the seating lint
refuses a TO to a multi-project instance. **Twenty-one cells of publish-path work under a sovereign publish intent
proceeded for hours and no gate could have noticed, because every gate's subject is the artifact I had not created.**
**A control whose subject is the missing artifact cannot detect its absence.**

**NOTHING HERE IS RETROACTIVE WHERE IT MATTERS: `GLD-f-1` — the 12:45Z SCHEDULED run — IS STILL AHEAD.** The acceptance
this TO exists to carry has not happened yet.

---

## ACCEPTANCE CRITERIA

| id | criterion | cells | grounding |
|---|---|---|---|
| **GLDR1DS-AC1** | The mirror at c02 time MEASURED before any change (tables × dates, denominator printed); the D-1 partition placed into the mirror; **the SOURCE RULED with its reason and the rejected option's cost named** — S3 pull reusing `_pull_canonical_for_c04`, or a `b00` re-run. | `GLD-a-1/2/3` | MEASURED + RULED |
| **GLDR1DS-AC2** | ⛔ **NEVER#1: the prior trading day DERIVED from `dim_calendar`, never wall-clock, never a literal** — this file once carried a hardcoded date. **EXERCISED across a weekend AND a market holiday, asserted BY DATE VALUE.** The oracle is *"the prior TRADING day"*, **NOT "Friday on a Monday"** — that is true 98 of 103 times and FIVE Mondays pull a Thursday. `NO-PRIOR-TRADING-DAY` at a series' first partition is CORRECT and must not be "fixed". | `GLD-b-1/2/3`, `GLD-inv-2` | EXERCISED |
| **GLDR1DS-AC3** | ⛔ **THE REFUSAL PATH SURVIVES.** A genuinely-absent D-1 still emits `REFUSED-NO-BMV`; **a MUTANT that defaults the refusal dicts must FAIL a test, run BOTH ways**; the three refusal statuses stay distinct and are never counted as one population. **The remedy makes BMV available where it exists and must never manufacture one.** | `GLD-a-4`, `GLD-inv-1`, `GLD-c-1/2` | EXERCISED |
| **GLDR1DS-AC4** | Manifest `bmv_source` names the ACTUAL prior partition **or WHICH absence it hit**; per-status `status_census` carried; **the chain's stage count DERIVED, not the hand-typed literal** — and it rides this TO because the lane touching the ordered list carries the derivation. | `GLD-d-1/2/3` | SOURCE + EXERCISED |
| **GLDR1DS-AC5** | No new schedule, trigger, alarm, SNS, monitor or freshness-checker; no shadow prefix; no comparator; **no served output moved**; built correctly once and ported; **every claim at a NAMED REF, and any trigger keyed on COMMITTED state.** | `GLD-inv-3/4/5/6` | SOURCE |
| **GLDR1DS-AC6** | ⛔ **LANDING ORDER: the consumer-side disarm is DEPLOYED before the first MIXED partition emits.** A mixed partition presents in the FULL shape carrying `bmv=NaN` — **`GLD-inv-1`'s harm reached by a route inv-1 cannot see, because pandas' column union does the defaulting.** **A DEPENDENCY, NOT AN APPROVAL STEP.** Discharged when a consumer reading the `[RATIFIED]` shape block meets the retraction AT THAT BLOCK. | `GLD-inv-7`, `GLD-c-3` | APPLIED |
| **GLDR1DS-AC7** | ⛔ **REAL RETURNS EMITTING ON THE *SCHEDULED* RUN** — an ad-hoc run is a QA instrument and **NEVER production evidence**. `REFUSED-NO-BMV` → **ZERO FOR ACCOUNTS PRESENT AT BOTH D AND D-1**; residual is accounts absent at D-1, **reported with its count and the D/D-1 account-set delta beside it**. ⛔ **The `c04` battery is NOT corroboration** — its check 7 passes `twr_daily=None` and has never evaluated a return. Rule 22a's three layers, APPLIED read on the deployed bytes against the ref that built them. | `GLD-f-1/2/3` | EXERCISED |
