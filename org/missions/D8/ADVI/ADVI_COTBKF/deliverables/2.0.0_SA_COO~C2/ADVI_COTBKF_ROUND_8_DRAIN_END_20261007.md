# L8 drain end -- ADVI_COTBKF round 8

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~11:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on FWD-6 / CB8h1-AC3)

Round 8 was cut as one issuance (@a80c0f84b7, `fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-7 analysis @625987b867.
E3 (a transactions re-apply to 1,415,137 rows) was not cut: its premise contradicted PRD v0.4 C-SILVER (`prd/ADVI_COTBKF_PRD.md:114`,
`:204-206`); the CTO struck it on this seat's REC (msg 393; correction @20b2b40d99).

1 of 1 orders terminal and merged; proof VALID; 0 unmerged worker branches; 0 linked worktrees for this project.

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CB-h-1 repeat count + per-kind FWD-6 page | ~24 | @57029c1bbc | VALID: AC1 PASS, AC2 PASS, AC3 JUDGMENT; 9 tests passed | `TX-REPEATS rows=1416497 exact_repeat_rows=1360 distinct=1415137 key=20_vendor_columns`; `COVERAGE-STATEMENT tables=11 kinds=6 every_kind_has_own_span=True every_not_covered_has_reason_and_row=True rows_cited=15 rows_missing=0` |

**For L9 (FWD-6, CB8h1-AC3):** `deliverables/0.9.0_WK_ADVI_COTBKF~24/COVERAGE_STATEMENT.md` now leads with six kind lines -- transactions
(1,416,497 rows, 2013-04-03 to 2026-06-22, 1,360 exact repeats kept by C-SILVER, `TX_REPEATS.md`), positions (469 on 2026-06-23, 83
accounts), statements (7,736, 2025-06-30 to 2026-05-31), tax forms (1,034, 2025-02-09 to 2026-06-06, dates from the file name), CRM (not
covered: S7, W19-S1), prices (not covered: S17).

**W23-S1 answered:** the 1,360-row gap is measured exact repeats, kept by the ratified PRD; no write skipped a drop.

## Rows filed in the round

| row | class | standing |
|---|---|---|
| W24-S1 | OBSERVATION | INERT -- STMT/TXRP mapped to statements/tax forms from CB-c-2; the tax-form span is a 16-month file-date span, which the page states, not "2 tax years" |

ARMED rows of this seat: 0. Open relay: E1-r7's price-store listing (laptop, msgs 377-378).
