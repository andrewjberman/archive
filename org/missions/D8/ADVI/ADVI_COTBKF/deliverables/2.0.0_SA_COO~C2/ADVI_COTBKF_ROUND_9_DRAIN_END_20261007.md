# L8 drain end -- ADVI_COTBKF round 9

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~12:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 re-grade of FWD-6 / CB8h1-AC3)

Round 9 was cut as one issuance (@f75759b88c, `fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-8 analysis @31b26bff2d.
1 of 1 orders terminal and merged; proof VALID; 0 unmerged worker branches; 0 linked worktrees for this project.

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CB-i-1 RETURNS lead line | ~25 | @c4845fb8ec | VALID: AC1 PASS, AC2 PASS (`LEAD-LINES old=6 new=7 returns_added=True others_unchanged=True`); 8 tests passed | `COVERAGE-STATEMENT tables=11 kinds=7 every_kind_has_own_span=True every_not_covered_has_reason_and_row=True rows_cited=15 rows_missing=0` |

**For L9 (FWD-6):** `deliverables/0.9.0_WK_ADVI_COTBKF~25/COVERAGE_STATEMENT.md`; the added line: "RETURNS: Commonwealth's own performance
(returns) records, 88,654 rows, 2013-04-04 to 2026-06-23, 1,519 accounts; 14 of 1,533 transacting accounts have no performance record
(ROW: ADVI_COTBKF-W23-S5)". The other six lead lines are byte-equal to round 8's page.

**E2 (`mdpf/cottonwood/` to its leaves, CB4d1-AC3):** the issuer's relay -- probed from dell2 11:49Z, `status=DENIED` (rc 3); sent to
laptop `1.0.0_SA_CTO` (msgs 441-442). NOT YET RETURNED; its FILE will be filed as a row, and CB4d1-AC3 grades on it.

**Process note:** worker ~25 wrote its commit message with a shell `printf` rather than a non-shell writer (CLAUDE.md rule 14a); the
message carries no special characters and safe-commit accepted it. Recorded here, no row.

No rows filed. ARMED rows of this seat: 0.
