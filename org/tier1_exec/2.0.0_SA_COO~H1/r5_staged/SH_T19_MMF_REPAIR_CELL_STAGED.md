# STAGED (not issued) -- MDPF_SECHIST round 5 repair cell SH-t-19, for the round-5 issuance on the CTO's round-4 analysis

Source: 1.0.0_SA_CTO~DELL1 msg 2778 (one batched repair cell) + msg 2791 (FWD-9 grade); PRD v0.3 C-MMF (CVO sign @cc57bafcdb).
Worker class: worker-light (batch repair cell). Risk: SERVED.

## The cell

1. `integrations/bloomberg/pipeline/etf_daily_pull.py:68-69`: drop `TOT_RETURN_INDEX_GROSS_DVDS` from `HISTORY_FIELDS` (back to
   `["PX_LAST", "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS"]`); remove `TOTAL_RETURN_LEVEL_FIELD`; the gap-fill windows (SH-t-8) stay.
2. `data/etfs/scripts/gold/etf_positioning_gold.py:917-1040`: the SALXX / FXFXX daily return reads `DAY_TO_DAY_TOT_RETURN_GROSS_DVDS`;
   a null day serves blank (never estimated, never the level); remove `TOT_RETURN_LEVEL_COL` and the level path.
3. Re-point the seam test (`test_etf_positioning_mmf_rule.py:81`): gold's money-market field equals one of the pull's `HISTORY_FIELDS`.
4. Negative arm: a null first day reads blank; after the re-request fills that day, the same day reads filled.

## Criteria (dry-run at base 290fd5e697, both FAIL)

- `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECHIST_H1/R3_CHECKS/r3_named_tests.py MMFR data/etfs/scripts/gold/test_etf_positioning_mmf_rule.py test_mmf_daily_return_from_day_to_day_field test_null_first_day_reads_blank_then_filled_after_rerequest test_mmf_rule_never_reads_level`
  -> expect `MMFR-TESTS-OK` (base: `MMFR-TESTS-BAD not-passed=all three`).
- `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECHIST_H1/R3_CHECKS/r3_named_tests.py PULLR integrations/bloomberg/pipeline/test_etf_daily_pull_history_plan.py test_history_fields_drop_total_return_level`
  -> expect `PULLR-TESTS-OK` (base: `PULLR-TESTS-BAD`).

## Paths

`integrations/bloomberg/pipeline/etf_daily_pull.py`, `integrations/bloomberg/pipeline/test_etf_daily_pull_history_plan.py`,
`data/etfs/scripts/gold/etf_positioning_gold.py`, `data/etfs/scripts/gold/test_etf_positioning_mmf_rule.py`.

## Round-5 dated reads (with it)

- FWD-9: Monday 2026-10-12 null first day served blank, re-requested, served filled on Tuesday's run (after both deploys).
- FWD-7: the 2026-10-12 07:00 ET pull's `spent_after` / `remainder` (`R3_CHECKS/r3_fwd7_read.py`).
