# L8 drain end -- IRPT_CUSTDY round 1

**Issuer:** `2.0.0_SA_COO~K2` (dell2) | **Date:** 2026-10-07 ~08:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; no JUDGMENT criteria this round)

Round 1 is the PRD v0.2 @c2bc15f427 THREAD (FWD-1), cut as one issuance @30f94c3ab1 (`fanout: 4 of 4 chains, cap 8`) from
`decompositions/IRPT_CUSTDY_DECOMP.md`. Every order is terminal and merged on dell2:
- 4 of 4 orders `complete`;
- `proof-of-spec-check.py` reads VALID rc 0 on 4 of 4 instances, each read at its branch head before the merge;
- drains through `.tools/safe-merge.sh`: 737839f762 (CU-a-3), 06a44e56bd (CU-a-4), 9dd85cec00 (CU-a-1), 36c37ef88d (CU-a-2); the two channel
  conflicts were resolved as a union of the appended rows, graded by the row gate on the merged index;
- 0 unmerged worker branches and 0 linked IRPT_CUSTDY worktrees (`git worktree list`);
- drain checks on `data/assets/scripts/gold/irpt_custody/`: `py_compile` 4 of 4, `ruff --target-version py39` "All checks passed!",
  `pytest` 36 passed, the four `--self-test` lines all True.

## Orders

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CU-a-1 advisor client list + measured pick | ~1 | @9dd85cec00 | VALID: AC1 9 passed, AC2 SELFTEST all True | **FAILED.** `--pick --as-of 2026-09-30 --ownership s3://opal-data-bd/platinum/49financial/ownership_map.json`: Schwab silver present for both masters (08242234 rows=103863, 08335338 rows=107469), then `ids.IdRefused` in `book_of`. Census: 482 of 7022 distinct granted accounts refused by the custodian-key projection, 31 of 190 advisors. Row S3 |
| CU-a-2 figures (WORLD) | ~2 | @36c37ef88d | VALID: AC1 12 passed, AC2 `SCHWAB-COVERAGE master=08335338 read_ok=True tables=20 latest=2026-10-05 as_of_covered=True` | The worker's AC2 is the real read (also 08242234: 19 tables, `as_of_covered=True`). The figures run on real accounts was NOT made: it needs CU-a-1's account list (S3), and its SI windows can start before 2024, held by the CTO's ruling A (msg 179) until fix B. No `--apply`; no S3 write |
| CU-a-3 security describer | ~3 | @737839f762 | VALID: AC1 5 passed, AC2 SELFTEST all True | The self-test reads the real classification table (SPY, AGG, GLD described; ZZZZ undescribed) |
| CU-a-4 template + layout + render-path read | ~4 | @06a44e56bd | VALID: AC1 10 passed, AC2 SELFTEST all True | `--render-path`: `accepts_document=False evidence=infra/aws/ec2/investor-reporting-export/render_export.cjs:228`. Row W4-S1; IRPT_BCKEND's `2.0.0_SA_COO~P2` agrees with the reading (msg 167) and sends the contract question to the CTO |

**FWD-1 thread: NOT LIVE.** Hop 1 fails on real data (S3); hop 5 has no render path for a document (W4-S1). Hops 2-4 run: real Schwab
coverage read, figures and descriptions on fixtures and the real classification table. No artifact of this round is served, landed to
gold or graded REALIZED. No artifact of this lane on dell2 is dated before 2024-01-01 (ruling C: none to list).

## Rows filed in the round

| row | class | standing | note |
|---|---|---|---|
| S1 | OBSERVATION | INERT | at the cut: the render path's input is a portal export request; S07's "held" is for the path, not a document. Measured by W4-S1 |
| W4-S1 | OBSERVATION | INERT | `accepts_document=False`; three things missing (a document or its address in submit-export, a template body or its address in the host input, a print page that lays out from a data template); the third not read (no portal checkout in the worktree). Routed by S2 |
| W1-S1 | BLOCKING | INERT | the directory carries no advisor; the advisor lives in the ownership map (`d08_firm_ownership_map.py`). Ruled by S2: the map is accepted as hop 1's source |
| W2-S1 | OBSERVATION | INERT | five figure rules the contract left open, each one function in `client_report_figures.py`. Ruled by S2: accepted for round 1 |
| S2 | OBSERVATION | GRADUATED | the issuer's rulings on W1-S1, W2-S1, W4-S1 |
| S3 | BLOCKING | INERT | the real pick crashes on 482 refused accounts; repair (count a refused account as uncovered) is round 2's first item; the cause of the 482 is not measured |

Also from the round, carried to `1.0.0_SA_CTO~DELL2` in the drain-end message (msg at 08:48Z): the PRD's S01 text, a naming-registry row
for the ownership map's address, and that the map's fresh copy is in `opal-data-bd` (PRD ruling 4). The classification table's sector map
is narrower than its class map: a holding can be `described: true` with `sector: null` (FWD-6; CU-a-3 report).

-- 2.0.0_SA_COO~K2
