# IRPT_DASHBD TO-DB-b-36 -- why the activity identity misses (counts only)

Worker 0.9.0_WK_IRPT_DASHBD~21, round 24 workstream B, cell DB-b-36. The producer `account_activity_lots.py` and the served
`account_return_daily.py` were imported read-only and not edited; S3 was read, never written. The evidence is
`GAP_DIAGNOSIS_E1.json` beside this file; `gap_diagnosis_e1.py` regenerates it. No client figure or balance is quoted here.

## Reproduction

- The producer re-run over the same 100 accounts and 24 trading days (2026-09-01..2026-10-05) grades 91 accounts; 52 tie within
  one cent and 39 do not, the same 39 as round 23 (maximum difference between the two runs: 0.0).

## The largest-gap window

- The account is the one round 23 named (largest |gap|). All seven terms were recomputed from `dim_balance`, `fact_trn`,
  `fact_rld` and `fact_uln`/`fact_ult` and tie the producer's own terms exactly (0 difference on 7 of 7). Row counts: beginning 1,
  contributions 3, withdrawals 0, realized 0, unrealized change 8, income 2, ending 1.
- Cause, in two parts, residual 0.0000 of the gap:
  1. 6 cash journal rows and 5 in-kind rows (JNL, TOA) are classed CONDITIONAL-BY-COUNTERPARTY in the shared code table. The
     served `classify_and_sum` marks that class with `_final = None` and resolves it with `_final is None`; on pandas 3.0.6
     the None becomes NaN when it is assigned into the frame, so no stage ever resolves such a row and it is not even counted as
     UNRESOLVED. The flow term never reads them. Counterfactual (same code, `pd.options.future.infer_string = False`): the 6
     cash rows enter the flow.
  2. The in-kind legs move the lots' cost basis while the lot table moves only the gain, so the basis part falls into the gap on
     3 days. A 1-day lag between the balance and the lot table nets to zero over 2 days.
- Resolving part 1 alone does not close this window: with the None kept, the gap moves to a different value, because an in-kind
  arrival carries a lot whose whole value is gain and the flow also counts the arrival. The identity needs an in-kind term (E2).

## The transaction-type census (fact_trn, 91 accounts, 24 partitions)

- 2,662 rows over 35 types (a type is tran_srcde/tr_cd/sb_cd/debit_credit). 3 types are UNSIGNED (trade legs); 18 types map to a
  term (contributions, withdrawals or income); the rest map to none.
- 10 types move value and map to no term: 7 are CONDITIONAL-BY-COUNTERPARTY (3 `$JNL`, 1 `JNL` in-kind, 3 `TOA`), plus FEE-ADMIN
  (`FEE/FC/FE/DEBIT`), withheld tax (`FTP/FC/WD/DEBIT`) and the in-kind adjusting entry (`ADJ/IC/IC/SHORT`).
- BKSWP and BRSWP sweep legs (4 types, 560 rows) move no value: on 270 of 270 account-days their signed legs net to zero.

## The 39 gaps, tolerance 0.05 per account-window (stated before the run)

- ROUNDING 30. MISSING-TERM 9. Every MISSING-TERM gap is explained to within 0.02 or better by 1 to 2 components:
  - CONDITIONAL_FLOW_NOT_READ: 4 accounts (the cash journals the rule drops).
  - LOT_BASIS_MOVED_WITHOUT_FLOW: 2 accounts (in-kind lots leaving, or a cost basis posted days after an in-kind receipt).
  - LOT_BASIS_ABOVE_ORIGINAL_COST: 3 accounts (new lots whose cost_basis_unamortized exceeds the cash paid, a basis adjustment).
  - FEE_ADMIN_HAS_NO_TERM: 1 account. WITHHELD_TAX_HAS_NO_TERM: 1 account.
- With the CONDITIONAL rows resolved (counterfactual), 38 of the 91 windows still miss by more than one cent and 7 by more than
  0.05; 2 of the 9 MISSING-TERM windows close and 2 become other gaps (in-kind lots).
