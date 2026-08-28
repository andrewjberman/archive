# TO D4_ETFPOS.TO-D4c — ETF positioning projection producer + schedule (LAPTOP-ONLY)

<task_order id="D4_ETFPOS.TO-D4c" project="ETFS_POSITIONING">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:55Z</issued>
<dated>on TO-D4b</dated>
<status>superseded -- **SUPERSEDED-BY-DELIVERY, marked 2026-08-28 ~18:5xZ by `2.0.0_SA_COO~Z` (issuer)** on the same Andrew-direct. **The result EXISTS; another TO produced it.** Producer + schedule are LIVE: `etf-positioning-producer-daily` = `cron(0 13 * * ? *)` **ENABLED**; Phase A's holdings fetch shipped inside `etfs-netassets-daily` under Andrew's egress grant. **NO proof-of-spec instance exists for this TO** -- that absence IS the discriminator between COMPLETE and SUPERSEDED-BY-DELIVERY, not an omission. ⛔ **NOT "staged, never started" -- that wording is STALE and closing on it would record a falsehood:** Phase A is in PRODUCTION CODE. ~~staged -- GATED ON TO-D4b~~</status>
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

---
## ⚖ SPLIT INTO PHASES 2026-08-19 ~23:18Z (COO) — MY BUILD-NOT-FIRE RULING MADE THIS TO's OWN ACCEPTANCE UNREACHABLE

DS base named it before building, correctly: **D4c-1 (three artifacts SERVED), D4c-2 (field-level
asserts vs the holdings input) and D4c-3 (`comp-validate` PASS) ALL REQUIRE THE PRODUCER TO RUN ON
REAL INPUTS** — and my authorization is BUILD, NOT FIRE, with the DIVZ/IDVZ holdings feed not
existing until Andrew's scope word.

**So I ruled an authorization that its own TO could not satisfy. That is mine, and it is the third
time tonight I have written an outcome whose mechanism I fenced.** Fixing it by splitting the
acceptance rather than by softening it.

### PHASE A — TONIGHT, AUTHORIZED, and this is what "D4c done tonight" means
- **A-1 PRODUCER BUILT** as an EXTENSION of `etfs-netassets-daily` (not a new producer — build-ladder
  rung 2, DS base's own read).
- **A-2 DRY-RUN GREEN** against what actually exists: the in-repo `source_{divz,idvz}_holdings_20260731.csv`
  pair, and the **live daily PFDE/PFOE** holdings that already land.
- **A-3 FIELD-LEVEL ASSERTS ON THE AVAILABLE HALF** — PFDE/PFOE live, DIVZ/IDVZ against the 07-31
  CSVs. **State the denominator: 2 of 4 asserted live, 2 of 4 asserted against a frozen snapshot.**
- **A-4 SCHEDULE PRESENT IN TF AND EXPLICITLY DISABLED**, with the enable as a single reviewable line.
- **A-5 proof instance covering A-1..A-5 only.**

### PHASE B — ON ANDREW'S SCOPE WORD, not before
- **B-1** three artifacts SERVED · **B-2** field-level asserts vs the LIVE DIVZ/IDVZ input ·
  **B-3** `comp-validate` PASS · **B-4** schedule ENABLED.

### ⛔ PHASE B IS DEFERRED, NOT FAILED — AND NOT WAIVED
`comp-validate` PASS still binds at Phase B, and **`NO_CONFIG` / `ZERO_CHECKS` remains
never-reportable-as-safe.** Nothing in this split lowers a bar; it separates *when* each bar is
answerable. **"D4c done" without Phase B named is an overclaim** — say PHASE A COMPLETE.
