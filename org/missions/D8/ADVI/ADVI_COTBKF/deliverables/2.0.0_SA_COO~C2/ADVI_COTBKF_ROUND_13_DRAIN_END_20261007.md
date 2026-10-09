# L8 drain end -- ADVI_COTBKF round 13

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~15:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB13m1-AC3)

Round 13 was cut as one issuance (@65ce59b838, `fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-12 analysis @9a9384d247
(CB12l1-AC3 NOT MET: `leu` unsigned). The issuer found TWO divergent signing tables and ruled one table for all three scripts, and widened
E2's diff to both applied tables the old rules built.
2 of 2 orders terminal and merged; 2 of 2 proofs VALID; 0 unmerged worker branches; 0 linked worktrees for this project.

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CB-m-1 type census, ONE signing table, rebuild | ~29 | @79e9c35429 | VALID: AC1 PASS (control: `NO_SHARE_MOVEMENT` emptied gives 8), AC2 PASS, AC3 JUDGMENT | `TX-TYPES types=61 signed=31 unsigned=30 unsigned_with_quantity=0 unsigned_with_quantity_named=8`; `DAILY-HOLDINGS accounts=1533 account_days=1691729 holding_rows=22547096 snapshot_accounts=83 snapshot_pairs=381 snapshot_equal=381 snapshot_diffs=0 fractional_residuals=5 fractional_accounts=5` |
| CB-m-2 rule-change diff vs the APPLIED tables | ~29 | @79e9c35429 | VALID: AC1 4 passed (one-change control), AC2 PASS | `RULE-CHANGE-DIFF crosswalk_rows=1533 crosswalk_changed=65 crosswalk_matched_before=439 crosswalk_matched_after=471 account_links_rows=1450 account_links_changed=2 account_links_linked_before=212 account_links_linked_after=212` |

Drain hygiene: py_compile and ruff (py39) clean on all six scripts; silver suites 52 passed, the diff suite 4 passed.

**The signing table** (`data/assets/scripts/silver/commonwealth_signs.py`): agreed types kept; 13 types the crosswalk lacked taken from the
account-links table (every pair carrying them ends at exactly 0, 326 of 326); `leu` -1 (clears 13 of 13); `ci` and `12b1` kept +1 from the
crosswalk (measured against the snapshot); `ileu` unsigned (its one quantity row's pair already nets to 0 without it); 8 types named in
`NO_SHARE_MOVEMENT`, 5 of them measured (signing any opens snapshot pairs). The 5 fractional residuals are not `leu` (two CUSIPs after CAF
rows, one single `li`, two 0.02-0.029 on one CUSIP), listed with type histories.

**What the fix moves in SERVED tables (nothing applied):** the crosswalk gains 32 MATCHED (439 -> 471, none lost; 33 more NOT_MATCHED rows
change score); account links swap one link each way (acct#e1e2dacb -> acct#f6464238 gained; acct#d6187d4b -> acct#8f547eb0 lost to LEFT_COMMONWEALTH), 212
LINKED unchanged; 52 link reasons change text without a status change (row D2-W29-S3). Control: both scripts on the OLD tables reproduce the
applied tables with 0 changes, so every difference is the rule. A re-apply of both tables needs its own never-widen pair; the COO half is
drafted beside this packet (`NEVER_WIDEN_R13_REAPPLY_COO_HALF_DRAFT.md`).

**For L9 (CB13m1-AC3):** `deliverables/0.9.0_WK_ADVI_COTBKF~29/D49141617_read.txt` -- 3,537 rows, 8 `leu` rows on 8 securities, each pair at 0
after its last transaction; none of the account's 101 non-cash pairs under one share.

## Rows

| row | class | standing |
|---|---|---|
| D2-W29-S1 | OBSERVATION | INERT -- vendor type `csltfee ` carries a trailing space; the table keys it exactly |
| D2-W29-S2 | OBSERVATION | INERT -- one test assertion extended for the two new DAILY-HOLDINGS fields |
| D2-W29-S3 | OBSERVATION | INERT -- 52 link reasons change text without a status change (51 "no in-kind receiver" mostly become "closed to cash") |

ARMED: 0.
