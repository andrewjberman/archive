# NEVER-WIDEN -- COO HALF: ETFS_RIVALS RIV-tc-1 -- the MERGE of branch `wk-ETFS_RIVALS-22` (@b0b65368fb) into site Z's tree, which is a deploy of `enrichment_bloomberg.py` to the scheduled 11:00Z vehicle

**Signer:** `2.0.0_SA_COO~V1` (dell1), 2026-10-09 ~03:4xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (site-Z producer
path: hand-over @0953984a75 act 2; producer rule in `org/missions/D5/ETFS/ETFS_RIVALS/project.json` `placement_ruling`).
**Act 2 of the three paired acts** that close round 28 (ROUND_ANALYSIS.round22 ADDENDUM 7 @0820f6b0b7). The act is a
merge; no Lambda, no S3 write, no vendor call. The model is round 27's half
`deliverables/2.0.0_SA_COO~RV/round27/NEVER_WIDEN_HALF_COO_R27_TW1_MERGE.md`.

## VERDICT: SIGNED

Conditions:
1. The branch is @b0b65368fb, merged whole (`git merge --no-ff`), into the branch site Z's vehicle runs from
   (`box/sitez`), by a site-Z seat on this seat's task order (CTO~DELL1 msg 1440).
2. The merge lands only AFTER RIV-tw-1's J1 is graded MET by the CVO on a run that REACHED the enrichment leg (tw-1
   AMENDMENT 1 @c07077f4e1, row Z-S79). A run that did not reach the leg leaves this merge held.
3. Never inside 10:55Z-11:15Z (the vehicle's run).
4. `RIVALFUNDS_HISTORY_OWED` stays unset by this act. Setting it is act 3 under its own pair.
5. Every read below holds at the merge. A merge onto a later `box/sitez` re-runs section 1's four checks there first.

## 1. What the merged tree was measured to do

Simulated merge in a scratch worktree (`C:/tmp/v1-tc1-sim`, detached at origin/box/sitez 37aefc2855, `git merge --no-ff
--no-commit b0b65368fb`): **clean, no conflict**. Paths: 5, +393 -12:
- `data/etfs/scripts/rivalfunds/enrichment_bloomberg.py` +73 -12: **the one product path, and the one path in
  `round27/vehicle_load_set.json` (18 modules) the merge touches**;
- `data/etfs/scripts/rivalfunds/tests/test_r27tw1_history_owed_leg.py` +1 -1, `.../tests/test_r28tc1_topup_currency_and_page_day.py` +226 (new);
- the worker's proof_of_spec JSON (+102) and the order's report (+2).

Re-run on the merged tree by this seat:

| check | result |
|---|---|
| `round15/checks/tc-1.AC1.py` | `AC1 RESULT: PASS 0 failures` |
| `round15/checks/tw-1.AC1.py` (the switch-OFF run identical, call for call, to the module at 361b735308) | `AC1 RESULT: PASS 0 failures` |
| `round15/checks/tw-1.AC2.py` (print and ask) | `AC2 RESULT: PASS 0 failures` |
| `round15/checks/aw-1.AC1.py` (the merged aw-1, unaffected) | `AC1 RESULT: PASS 0 failures` |
| `python -m pytest -q rivalfunds/tests` from `data/etfs/scripts` | `928 passed, 6 skipped` |

## 2. The diff, read by this seat

Every change is inside the step the switch opens (`_history_owed`) or a function only it calls:
- `HISTORY_OWED_CAP` 5000 -> 20000 (R24, Andrew's yes, AMENDMENT 1 of the order).
- New `_page_day(date)`: the next trading day after the report date (`lib.trading_calendar`, imported inside the function).
  `history_owed.owed` is given the page day, so the owed window ends on the page day.
- `_owed_line` gains two optional clauses (currency lookups; a lookup failure), omitted at zero.
- In `ask`: stored currencies read first (`_stored_currencies`), then ONE `CRNCY` reference request for the securities
  with none, counted in `bbg_budget.check_points` together with the history points before any request, and recorded.
  A failed lookup sends nothing more. Top-up rows carry the currency instead of NULL.
- In `print`: a "currency lookups N (not sent)" clause; no request.
The daily path's own lines, its exit code and its result are unchanged with the switch unset: tw-1.AC1 compares them
call for call.

## 3. The switch

Unchanged by this act: unset, empty and every value other than exactly `print` or `ask` is OFF. Where it is set at site Z
was NOT read by this seat (dell1 cannot read site Z's environment); the CTO~Z half or the merging seat states it.

## 4. Rollback and the pair's read

- Rollback: ONE revert of the merge commit on `box/sitez` (`git revert -m 1 <merge>` through `safe-commit`). The file
  returns to the tw-1 bytes. While the switch is OFF there is no object, ledger line or marker to undo.
- The pair's read (tc-1 J1, amended the same way as tw-1's): the first scheduled vehicle run after the merge that REACHES
  the enrichment leg. This seat reads its transcription (carried by a task order to `0.7.0_AE_CloudOps~Z`) and states the
  enrichment exit code and lines against the tw-1 read: same exit code, no `HISTORY OWED` line, the names step as before.
  A difference is a revert the same hour, ordered to the site-Z seat.

## Known and stated

- The ask's draw against Bloomberg is NOT this act's: with the switch OFF no request is sent. Act 3 (`ask`) files its
  draws through `2.0.0_SA_COO~Q1`'s queue (law edit 4d77a9c3ea; CTO~DELL1 msg 1505) and states the budget record's unit
  (points requested, an upper bound of returned records).
