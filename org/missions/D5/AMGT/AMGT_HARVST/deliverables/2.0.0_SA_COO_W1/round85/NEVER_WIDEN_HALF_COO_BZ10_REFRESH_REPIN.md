# NEVER-WIDEN -- COO HALF: re-register the site Z cycle runner with `-Windowless -RefreshOnce` from pin `3d88eccbc3`, `HVST-bz-10` (round 85, workstream REFRESH-SITEZ)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-13 ~22:4xZ. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half at `ledger/NEVER_WIDEN_ROUND85_BZ10_CTO_HALF.md` (owed). The CTO's bz-9 half named what this pair must carry: "which must name the account's other users and the one-per-cycle budget".
**Authority:** `ledger/ROUND_ANALYSIS.round84.md` section 2 item 1 and ruling (A), msg 5143: "the runner refreshes once per publisher per cycle through the existing SessionManager; no new credential path, no secret printed".

## THE ACT, in the order's words

At site Z, once, by `0.7.0_AE_CloudOps~ZW`, at a cycle boundary by the runner's own stop file (no kill, zero pairs lost, as bz-1 and bz-4):
1. Pin `3d88eccbc3` (the bz-12 merge, which carries bz-9) is a worktree beside the old pin, and every harvest pin is `git worktree lock`ed.
2. The task `Opal Data Harvest - Continuous Cycle` is stopped only after the cycle's record exists, then re-registered from `<new>` with `-Windowless -RefreshOnce` (the plan read first), with the state dir, runtime root and publishers (`bbg wsj barrons`) exactly as today, then started once.
3. Four reads at +3 and +15 minutes (log written, task `pythonw.exe` with `--refresh-once` in its arguments, no console host, real spawns), a signed rollback, and the account stop rule (step 9).

## THE NEW THING THIS ACT TURNS ON (named, not hidden in the re-pin)

- **A headful Dow Jones sign-in made by the RUNNER**, when and only when a `wsj` or `barrons` job is refused as expired (the class table over `STOP_STATUSES` maps `sign_in_refused` to `expired`; nothing else triggers it). The runner's driver calls `auth.SessionManager.refresh(publisher)` in its own process; that runs the CRO's
  `dowjones_harvest_session.py`, which opens a real Chrome window on the desktop of the Windows user `Opal Bloomberg` (the task's principal is `LogonType Interactive`) for up to 120 s, reads `dowjones/credentials` BY NAME, and replaces the publisher's DPAPI vault file. It prints and records no secret, cookie or username.
- **The budget:** at most ONE refresh per publisher per cycle (kept in the cycle checkpoint, so a restart inside the cycle does not re-spend it), so at most TWO sign-ins in a full pass of `wsj` then `barrons`, and none in `bbg`'s cycle. A refresh that raises is recorded by exception CLASS only, is never retried, and the pair is not replayed.
- **The account's readers (measured):** CloudTrail on `dowjones/credentials` (42 events, complete) shows 29 `GetSecretValue`, all by the one IAM principal `Andrew_Berman` (the harvester's identity), including 16 reads between 05:47 and 10:17 ET on 2026-10-01 and the two bz-6 mints on 2026-10-13; no refusal or lock was recorded. `deliverables/2.0.0_SA_COO_W1/round85/DOWJONES_SECRET_TOUCHES_20261013.txt` @dd6c8e07ac. That bounds the programmatic readers. **The account:** `wsj` and `barrons` are not two accounts; they share the ONE subscriber login in `dowjones/credentials` (CRO record `ANDREW_DIRECT_20260914_DOWJONES_HARVEST_W.md`: "Shared account; publisher-specific session bundles"). Its vendor-side lock policy is NOT READ. **Who else signs in with that login (a person at Opal, another box, another harvester) is NOT READ**:
  this seat has no instrument that lists them, and `describe-secret` returns a date-granular `LastAccessedDate` only. The pair signs with that gap named, not closed. Round 84 made exactly two sign-ins on it (bz-6's mints at 15:11Z and 15:20Z) and none was refused.

## BLAST RADIUS

- **Writers of the property N = 1.** The task's registration (its `WorkingDirectory`, arguments and interpreter) is written by `install-cycle-schedule.ps1` and by nothing else on the box; one task named `Opal Data Harvest - Continuous Cycle`. The cycle records and checkpoints are written by `cycle_runner` through `backfill_driver`, as before, plus the two keys bz-9 added.
- **What it touches in the world:** at most two vendor sign-ins per pass, plus the replays of the pairs they unblock (ordinary harvest requests the runner already makes). A visible Chrome window on the site Z desktop during a refresh; a person at that desktop would see and could disturb it (a closed window ends that refresh as `FAILED`, recorded, not retried).
- **Not touched:** `bbg`, `sa`, `ft` (the refresh is limited to `wsj` and `barrons` by `HVST-bz-12`, merged `3d88eccbc3`, so the Bloomberg-side branch of `SessionManager._refresh`, whose credential is `google/andrew-goldengate/credentials`, is unreachable from the driver; row `AMGT_HARVST-D1-S16`), the state dir, the runtime root, the publishers, S3, `config.json`, silver, bronze, gold, the old pins.
- **Served output moved:** none directly. The flag changes what the runner does on a refusal; collection continues at site Z either way.

## BOTH BRANCHES (the half is signed for BOTH or for neither)

- **Branch D (refresh `done`):** the publisher's vault is replaced, the pair is replayed once, and the leg goes on; the close read (bz-11) then waits for a full cycle with the session alive at its end.
- **Branch F (refresh `FAILED`, or a second refusal after a `done` one):** NO second attempt by anyone; one row (publisher, class, `http_status`, `host`, `login_redirect`) and the question returns to the issuer. This is the "refresh cannot fix it" finding, not a rollback of the registration.
- **Branch X (the flag is registered but no refusal occurs):** nothing happens; the runner behaves exactly as at `995adcaeaa` plus recording.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a.** P is on `origin/CLOUD` and is an ancestor of it (the reverse is the negative control). **C-b.** Both halves read SIGNED at their pins before any change. **C-c.** The old pin `995adcaeaa` stays locked and is the rollback. **C-d.** The stop is by the runner's own stop file; a runner that ignores it is a stop with a row, never a kill.
- **C-e.** From the start the seat reads the log and checkpoint for `REFRESH ... FAILED` and for a repeat `REFUSAL` after a refresh, and obeys step 9 of the order.

## ROLLBACK

Re-register from `<old>` (`995adcaeaa`) with `-Windowless` and without `-RefreshOnce`, the same state flags, start once. A vault file a refresh replaced is not rolled back (a fresh session is the intended state); a session is never restored from anywhere.

## WHAT THIS HALF DOES NOT COVER

- A sign-in by any hand other than the runner's one refresh per publisher per cycle; `--park`; any new credential path; reading or printing a secret, cookie, username or token; a change of the publishers, the state dir or the runtime root; FT; a `bbg` refresh (above).

## VERDICT: SIGNED (COO). Not started until the CTO half is on file.
