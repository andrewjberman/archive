# NEVER-WIDEN -- COO HALF: ONE merge of branch `wk-AMGT_HARVST-139-r85` (`HVST-bz-9`, a refused pair carries its evidence and the driver refreshes once) into `lib/opal_data_harvest`

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-13 ~22:0xZ.
**Pairs with:** `1.0.0_SA_CTO~DELL1`'s producer half (owed), at `ledger/NEVER_WIDEN_ROUND85_BZ9_MERGE_CTO_HALF.md`. A merge that lands in `lib/opal_data_harvest` is a producer change under a never-widen pair (the bz-3 shape).
The change itself is ruled by his msg 5209 and `ledger/ROUND_ANALYSIS.round84.md` section 2 item 1, and by ruling (A) msg 5143. The merge does not start until both halves are on file.

## THE ACT

ONE merge of branch `wk-AMGT_HARVST-139-r85` @5309953230 (the worker's proof commit; the build is `dd5fc764d8`, on the local worktree `C:/dev/wk-harvst-139`) into `box/dell1` through `.tools/safe-merge.sh`, and nothing else. CLOUD takes it at the integrator's
box-sync. No scheduled task is registered, stopped or started by this act, and no sign-in is made.

## WHAT THE BRANCH CHANGES (read at signing, `git diff 3fc6879679 5309953230`: 8 files, +728 -8; the five lib files are below)

- `lib/opal_data_harvest/transport.py` (+16 -4): `AuthExpired` takes optional keywords `status`, `host`, `login_redirect` (default None, None, False); both raise sites set them; the message text of each raise is unchanged.
- `lib/opal_data_harvest/worker.py` (+12 -1): under `--no-sign-in` the `SignInRefused` is raised `from exc`; the job handler adds `refusal = {http_status, host, login_redirect}` to the result only when the cause is an `AuthExpired`; the run record's job entry carries it as a conditional key.
  Status, detail and every other field are unchanged. No body, header, cookie or URL query is recorded.
- `lib/opal_data_harvest/backfill_driver.py` (+85 -3): a class table over `STOP_STATUSES` (`sign_in_refused` -> `expired`, `bot_check` -> `blocked`, `account_or_harvester_unavailable` -> `entitlement`, every other member -> `other`); `drive()` prints one `REFUSAL` line and
  appends to `checkpoint["refusals"]` for every STOP-status job, **with or without the flag**; under a new flag `--refresh-once` (default OFF) a job refused as `expired` gets ONE `SessionManager.refresh(publisher)` per publisher per cycle (the budget is `checkpoint["refreshes"]`, so a
  restart inside the cycle does not re-spend it) and the same pair is replayed once; a refresh that raises is recorded `failed` by class name only, never retried, and the pair is not replayed. `drive()` raises `ValueError` if the flag is on and no refresher is given.
- `lib/opal_data_harvest/cycle_runner.py` (+4) and `install-cycle-schedule.ps1` (+4 -2): `--refresh-once` is passed through only when given; the installer's `-RefreshOnce` switch appends it. **Without the switch the installer and the driver's argv are unchanged.**
- `lib/opal_data_harvest/test_bz9_refresh_once.py` (24 tests): the AuthExpired evidence at both raise sites, the refusal object and its absence on another path, the class table over EVERY member of `STOP_STATUSES`, one refresh then a replay, a second refusal makes no second refresh, a restart from the saved checkpoint makes none,
  the three non-expiry classes make none, a raising refresher is not retried or replayed, flag OFF makes none, a planted secret string never reaches a line or a record, a MUTANT with the budget check removed makes two calls, the runner passthrough and the installer arms.
- **Re-run by this issuer in the worker's worktree:** AC1 `24 passed in 2.86s`. The worker reports AC2 `76 passed` and the full `lib/opal_data_harvest` suite `4 failed / 823 passed / 3 skipped` against `4 failed / 799 passed / 3 skipped` before (the same four known failures); AC2 and the suite are re-run on the merged tree at the act (C-b).

## BLAST RADIUS

- **Writers, N = 1 per property.** The six lib files are written by this branch only: of the 146 local `wk-*` branches, 1 (this one) differs from `HEAD` in them (`git diff --name-only HEAD...<branch>` over the five lib files); `HEAD` has not moved in `lib/opal_data_harvest` since the worktree base (`git diff --stat 3fc6879679..HEAD` empty).
  Writers of the cycle checkpoint file: `backfill_driver.drive()`, as before; this adds two keys (`refusals`, `refreshes`) and no writer.
- **What the default (flag OFF) run now does differently, all of it recording:** one extra `REFUSAL` line in the cycle log per STOP-status job, an extra `refusals` list in the checkpoint, and an extra `refusal` object in the run record's job entry for a refusal caused by an expiry. No sign-in, no extra request, no other behaviour.
  A reader that rejects unknown keys would break; the readers checked are `bz5_cycle_read.py` (reads `failures` only) and the existing runner tests (pass).
- **Running processes:** site Z's runner (pid 8792 since 18:57:48Z) executes from the PINNED worktree `wk-harvest-runner-pin-995adcaeaa`, not from the shared tree. This merge does not change it. The flag reaches it only when `HVST-bz-10` re-registers the task with `-RefreshOnce`, a separate act under its own pair.
- **Shared-tree imports at site Z:** a run from site Z's shared tree after its box-sync sees the new records and the unused flag; no sign-in unless the flag is given.
- **Not touched:** silver, bronze, gold, S3, `config.json`, any scheduled task, the old or the new pin, the Secrets Manager, any publisher.

## BOTH BRANCHES (the half is signed for BOTH or for neither)

- **Branch O (flag OFF, the default and the only state this merge creates):** recording only, as above.
- **Branch R (flag ON, reached only by `HVST-bz-10`):** NOT activated by this act. Its blast radius, a headful sign-in on the shared Dow Jones account at most once per publisher per cycle, is the next pair's.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a.** The branch head is `5309953230`; a newer head is a new pair.
- **C-b.** On the merged tree, before the close: AC1 and AC2 of the order pass, and the full `lib/opal_data_harvest` suite shows the same four failures as the base and no new one.
- **C-c.** The merge lands through `safe-merge.sh` with its guards on; nothing is forced, and a conflict is a stop, not a resolution by this seat.
- **C-d.** The branch's proof instance reads `INVALID` (its `decomp_ref.to_ref` names no governing order, which the worker's face could not supply: row `AMGT_HARVST-D1-W139-S3`). The issuer corrects that one field after the merge and re-runs `proof-of-spec-check --governing-order` before flipping the order; no flip on the INVALID instance.

## ROLLBACK

Revert the merge commit on `box/dell1` (a new commit, no rebase). Nothing served has moved, so the rollback has nothing to undo at site Z.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file.
