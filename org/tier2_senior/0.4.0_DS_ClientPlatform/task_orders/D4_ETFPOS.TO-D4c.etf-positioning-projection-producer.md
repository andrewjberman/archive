# TO D4_ETFPOS.TO-D4c — ETF positioning projection producer + schedule (LAPTOP-ONLY)

<task_order id="D4_ETFPOS.TO-D4c" project="D4_ETF_POSITIONING">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:55Z</issued>
<dated>on TO-D4b</dated>
<status>staged -- GATED ON TO-D4b</status>
<priority>P2</priority>
<authority>D4_ETF_POSITIONING_VARIANT_PRD.md §4.2 + §6 item 3 at dispatch vintage @2ecc24d0c8. Placement: LAPTOP-ONLY (gold deploy cycle).</authority>
</task_order>

## Objective
Build the ETF positioning projection producer per §4.2 **and give it a SCHEDULE.**

## THE SCHEDULE IS AN ACCEPTANCE CRITERION, NOT A FOLLOW-UP
**A production pipeline MUST have a schedule.** Event-driven is fine as an ACCELERATOR, but **a
pipeline whose only trigger is another pipeline's success has no schedule and is a defect** — it
freezes silently and invisibly when its upstream breaks. The measured instance is in the law:
`mdpf-daily-refresh-trigger` had `ScheduleExpression: None`, fired only on an upstream completion
marker, and froze a client-facing product for six days with perfectly fresh inputs sitting unused.
**The schedule must be VISIBLE IN TERRAFORM.**

## Mandate
`comp-pipescript io --pipeline` (flag REQUIRED) + `comp-blast` + `comp-validate`. Rule 15
(`from __future__ import annotations`). Rule 17b: gold is parquet; serving-shaped work belongs in
platinum, not here.

## Acceptance criteria
- **D4c-1 THREE ARTIFACTS SERVED.**
- **D4c-2 FIELD-LEVEL ASSERTS VS THE HOLDINGS INPUT** — not row counts alone.
- **D4c-3 `comp-validate` PASS.** `NO_CONFIG`/`ZERO_CHECKS` is UNVALIDATED and must never be
  reported as safe.
- **D4c-4 SCHEDULE VISIBLE IN TF** (see above — a trigger-only wiring does not satisfy this).
- **D4c-5 proof instance VALID rc=0 positional: ids D4c-1..D4c-5.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>D4c-1,D4c-2,D4c-3,D4c-4,D4c-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D4_ETFPOS.TO-D4c_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO at artifacts-served, cc CTO. Report the DESIGN FREEZE moment explicitly -- TO-D4d gates on it.
Session log w/ Compiler Tools section.
