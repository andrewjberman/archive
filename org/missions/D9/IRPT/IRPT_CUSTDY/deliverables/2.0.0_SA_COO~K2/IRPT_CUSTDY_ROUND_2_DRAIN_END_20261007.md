# L8 drain end -- IRPT_CUSTDY round 2

**Issuer:** `2.0.0_SA_COO~K2` (dell2) | **Date:** 2026-10-07 ~09:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile; no JUDGMENT criteria this round)

Round 2 is the round-1 analysis's ENRICHMENT LIST (`1.0.0_SA_CTO~DELL2` @822468e309, E1-E4), cut as one issuance @e27b2bce34
(`fanout: 2 of 2 chains cut (3 in the analysis; E3 held), cap 8`) from `decompositions/IRPT_CUSTDY_DECOMP.round2.md`. Every cut order
is terminal and merged on dell2:
- 3 of 3 orders `complete`; E3 HELD, not cut (row S5);
- `proof-of-spec-check.py` VALID rc 0 on 3 of 3 instances, read at the branch head before each merge;
- drains through `.tools/safe-merge.sh`: 19ff3664fc (chain B, CU-b-3), 1c925383a4 (chain A, CU-b-1 + CU-b-2; the channel conflict was
  resolved as a union of appended rows, graded by the row gate on the merged index);
- 0 unmerged worker branches and 0 linked IRPT_CUSTDY worktrees;
- drain checks on `data/assets/scripts/gold/irpt_custody/`: `py_compile` 6 of 6, `ruff --target-version py39` clean, `pytest` 53 passed,
  four self-tests all True (the figures line now carries `held_ok=True sources_ok=True`).

Slot ~5's first subagent completed CU-b-1 and could not be continued (the harness held no transcript), so the slot was re-seated for
CU-b-2 with CU-b-1's commits (7f066bfba9, 382167a5f0) named as inherited state.

## Orders

| order | worker | drain | criteria | real run on dell2 |
|---|---|---|---|---|
| CU-b-1 (E1) pick on live data | ~5 | @1c925383a4 | VALID: AC1 6 passed, AC2 `ADVISOR-PICK scanned=190 eligible=16 pick=matthew_gooch households=10 classes=4 projection_refused=482 of=7022`, AC3 `NONE-SOURCE file=infra/aws/lambda/investor-reporting/_ids/data/custodian_key_seam.json:48 owner=IRPT_BCKEND refused=482 distinct=7022 via_none=482` | AC2 and AC3 ARE the real runs, on `s3://opal-data-bd/platinum/49financial/ownership_map.json` (LastModified 2026-10-07T05:27:37Z) |
| CU-b-2 (E2) census | ~5 (re-seated) | @1c925383a4 | VALID: AC1 `CENSUS-WRITTEN advisors=190 eligible=16 pick=matthew_gooch` | The real census: `deliverables/0.9.0_WK_IRPT_CUSTDY~5/ADVISOR_CENSUS_20260930.md`, 190 rows, no run of 8+ digits; recorded in the round-2 decomposition |
| CU-b-3 (E4) figures 2024 onward | ~6 | @19ff3664fc | VALID: AC1 11 passed, AC2 `CLIENT-FIGURES-SELFTEST contract_ok=True periods_ok=True nodata_marked=True held_ok=True sources_ok=True` | NOT RUN on real data: the returns gold is in `opal-data-49financial`, fenced from dell2 (S4); the laptop read is relayed (msgs 234/235, script @b97c663aa9), no file back yet. SI before 2024 is `HELD_CALENDAR_FIX` under HOLD A |

**FWD-1 thread: NOT LIVE.** Hop 1 now runs on real data (the pick completes). Hop 3 is built for 2024 onward but has not read real
returns (fenced). Hop 5 waits on IRPT_BCKEND a1-a4 (`~P2`, CTO ruling (a)) and on E3 (held). Hop 6 is Andrew's. Nothing of this round is
served, landed to gold or graded REALIZED; nothing of this lane on dell2 is dated before 2024-01-01.

## Rows filed in the round

| row | class | standing | note |
|---|---|---|---|
| S4 | OBSERVATION | INERT | `opal-data-49financial` explicit deny for the dell2 user; the read goes to the laptop as a file (standing rule msg 213); never widened |
| S5 | OBSERVATION | INERT | E3 held: no portal `node_modules` on dell2; installing is npm egress |
| W5-S1 | OBSERVATION | INERT | the `'None'` is IRPT_BCKEND's: `custodian_key_seam.json` holds 826 of 6202 values as the string `'None'` (null `schwab_account_id` in `dim_account_xref` 2026-09-16, stringified when written; the writer is not in the repo, commit 47f21dab95 adds the artifact only), and `ids.py:387-388`'s `mapped is not None` guard passes the string. Routed to the CTO in the drain-end message |
| W6-S1 | OBSERVATION | INERT | the per-figure `source` dict collided with the contract's `fees.source` label; the label moved to `fees.source.label`. Accepted by the issuer |

Carried to round 3, not rows: the ownership map's reader defaults to `legacy_address()` once its registry row is on origin (laptop CTO
msg 106103 via MSTR msg 246); the CLI argument stays until then.

-- 2.0.0_SA_COO~K2
