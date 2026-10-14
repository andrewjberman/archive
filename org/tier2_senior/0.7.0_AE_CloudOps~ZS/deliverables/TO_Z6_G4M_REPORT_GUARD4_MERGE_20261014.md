# TO-Z6-G4M report -- GUARD-4 merged into box/sitez (0.7.0_AE_CloudOps~ZS, 2026-10-14)

**archetype:** DEPLOY

Order: `org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/OPAL_BBGTML.TO-Z6-G4M.guard4-merge-tzero-tripwire-cix.md`
(issuer 2.0.0_SA_COO~ZB; ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_2DA6_GUARD4_MERGE_NO_HOLD_20261014_Z.md` @d8c5d77e26).

## Result: both criteria PASS; merge landed; no revert needed

| item | value |
|---|---|
| Window | started 12:30:12Z (clock read); AC1 run 12:36:15Z |
| Today's pull (07:00 ET, `bbg_tplus1_20261014_070001.log`) | `RESULT: END-TO-END OK`; `RESULT: PUBLISHED 2026-10-13`; vintage 20261013; publish-leg tripwire printed NO custom-CIX line (log lines 67-85) |
| Merge hash | `44745c9c87` on `box/sitez`; parents `3d33fc6690` and `3b65362444` |
| Ledger | `opal-bbgtml-guard4-merge-20261014`, opened 12:30Z, L1 and L2 closed with proof, CLOSED. Entry: `org/critical_paths/change_management/20261014T1230Z_opal-bbgtml-guard4-merge-20261014_deploy_completion.md` |
| Disposal | worktree `C:/tmp/rv-guard4` unlocked and removed; branch `rv-bbgtml-guard4` deleted (`-d`, was 3b65362444, contained) |
| Push state | LOCAL @44745c9c87 (ls-remote read: origin `box/sitez` @ec654ef7fb, does not contain it); box-sync carries it |

## AC2 (read-back)

```
git merge-base --is-ancestor 3b65362444 HEAD; echo "contained=$?"   -> contained=0
git diff --stat HEAD~1 HEAD -- integrations/bloomberg/ | tail -1     -> 1 file changed, 87 insertions(+)
```
The 1 file is `integrations/bloomberg/pipeline/tzero/tools/bbg_pkl_tripwire.py`. The merge changes exactly 3 files against its
first parent (that file plus the report and proof script under `org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/`); census 3 of 3,
0 outside the order's `<paths>`.

## AC1 (the one real run)

Interpreter: `PY_AWS` = `C:\Users\Opal Bloomberg\AppData\Local\Programs\Python\Python311\python.exe` (the publish leg's, per
`scheduled_daily_pull.cmd:143`), shared tree after the merge, project `output` dir, `--date 20261013`. Exit 0. Difference control:
the pre-merge publish-leg tripwire printed no custom-CIX line; this run prints:

```
      custom CIX series graded: 13 of 84 tickers in return_daily (71 vendor series are not custom and are not graded here); as-of 2026-10-13
OK:   data.return_daily: all 13 custom CIX series reach the as-of 2026-10-13
RESULT: PASS -- both PKLs safe to send (tzero vintage).
exit=0
```
All other lines equal the 07:00 ET publish-leg run (same row counts, 115660 / 29247 / 30414 / 80611 / 7260 / 1592). Nothing was
published, uploaded or requested; AC1 read PKLs already on disk.

## Deviation to record: a stale peer lock blocked `safe-merge.sh`

First `safe-merge` call REFUSED: lock held by `0.7.0_AE_CloudOps~Z` (branch `rel-nfra-oplgtw-r30c`, since 11:32Z, pid 2829449).
Measured before acting: pid not live, no `.git/MERGE_HEAD`, no unmerged paths, and that seat's broker status read "OG-ap-14 B2
COMPLETE ... ledger CLOSED ... aborted a wrong merge". The only armed piece was a leftover conflict-state file
(`.git/safe-merge-conflict*`). I cleared it with the tool's own `bash .tools/safe-merge.sh --abort`, whose no-merge-open branch
removes exactly that stale state file (`safe-merge.sh:391-401`); `safe-merge` then cleared the stale lock itself and merged. No
other seat's file was edited and no merge of theirs was aborted. Consequence for `~Z`: its `--continue` for r30c is disarmed in
this worktree, which its own status says it no longer needs.
