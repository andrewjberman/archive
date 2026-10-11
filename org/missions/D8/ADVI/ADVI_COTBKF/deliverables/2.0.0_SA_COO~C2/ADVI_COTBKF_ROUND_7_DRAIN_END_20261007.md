# L8 drain end -- ADVI_COTBKF round 7

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~10:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on FWD-8 and FWD-6)

Round 7 was cut as one issuance (@28e63ee8e6, `fanout: 3 of 3 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-6 analysis @1c9c98e652.
3 of 3 orders terminal and merged; 3 of 3 proof instances VALID; 0 unmerged worker branches; 0 linked worktrees for this project.

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CB-g-1 price-store scanner (FWD-3) | ~21 | @d97b008a7c | VALID: AC1 11 passed (denied-vs-empty control), AC2 PASS | `PRICE-STORE-SCAN bucket=opal-data-cottonwood prefix=irpt/cottonwood/ status=DENIED objects=0 candidates=0 security_days_possible=0 need=9388961` rc 3, probed again 10:4xZ after the fence join landed on two other buckets (msgs 359, 372). The real listing is relayed to the laptop (msgs 377-378); E1 criteria (2)-(3) wait on that FILE |
| CB-g-2 FWD-8 read | ~22 | @ce7a734b92 | VALID: AC1 6 passed, AC2 PASS | `FWD8-READ matched_read=439 lined_up=1 near_matches_awaiting=21 near_matches_linked=0`; page `deliverables/0.9.0_WK_ADVI_COTBKF~22/FWD8_READ.md` (old acct#cdf76705, advisor HKJ -> acct#efafd1dc, R2 score 1.0, 7 of 7 positions carried) |
| CB-g-3 FWD-6 coverage statement | ~23 | @03244ba441 | VALID: AC1 4 passed, AC2 PASS, AC3 JUDGMENT | `COVERAGE-STATEMENT tables=11 every_not_covered_has_reason_and_row=True rows_cited=15 rows_missing=0`; page `deliverables/0.9.0_WK_ADVI_COTBKF~23/COVERAGE_STATEMENT.md` |

Drain hygiene: `py_compile` and ruff (py39) clean on the three scripts and their tests. Real-run outputs went to `.scratch/` so the
committed deliverables are the workers' own.

**For L9:** FWD-8's DONE WHEN on `FWD8_READ.md`; FWD-6's DONE WHEN and CB7g3-AC3 on `COVERAGE_STATEMENT.md`. Worker ~23's notes for the
grade: the transactions section reads 1,416,497 applied rows where W2-S1 says 1,415,137 after de-duplication (row W23-S1, unexplained);
the 1,544 account-less documents are classified by document type, not by the vendor's listing text; prices come from the S17 census file.

## Rows filed in the round

| row | class | standing |
|---|---|---|
| W22-S1 | OBSERVATION | INERT -- the lined-up account has no 2026-06-23 holdings; the read compares to its first holdings (2026-06-30), the crosswalk rule's own basis |
| W23-S1 | OBSERVATION | INERT -- transactions 1,416,497 applied vs 1,415,137 in W2-S1 |
| W23-S2 | OBSERVATION | INERT -- silver positions is one snapshot (2026-06-23): 469 rows, 83 of 1,533 accounts |
| W23-S3 | OBSERVATION | INERT -- 1,544 of 11,119 documents carry no account |
| W23-S4 | OBSERVATION | INERT -- the coverage table grades only five record kinds |
| W23-S5 | OBSERVATION | INERT -- 14 of 1,533 transacting accounts have no performance record |

ARMED rows of this seat: 0. Open relay: E1's listing (laptop).
