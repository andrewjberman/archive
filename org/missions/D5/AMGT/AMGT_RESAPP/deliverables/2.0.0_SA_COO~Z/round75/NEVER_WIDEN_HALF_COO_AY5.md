# AMGT_RESAPP round 75 -- `AMGT-ay-5` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-06 ~10:5xZ

**The act** for `opal-amgt-scoped-api`, under ONE NEVER-2 entry. Executor `0.7.0_AE_CloudOps~A`. Order:
`task-orders/AMGT_RESAPP.TO-AMGT-ay-5.the-code-redeploy-and-snapshot-write.md`, with AMENDMENT 1 (the scheduled writer, per the
CTO's `ROUND_ANALYSIS.round74.md` ADDENDUM 1 @82afef1fd8, option b). Four legs, in this order:

1. **Code leg.** ONE artifact built from a DETACHED worktree at EXACTLY `ab28d0ba01`. It is never built "at or after" that commit: round
   74's ax-5 stopped on a file another project changed after the pin. Then ONE code-only `safe-apply`. `memory_size` stays 1769. Then
   `leadpanel_cold_warm.py --label after` and the cold invokes' `AMGT_PHASE` lines.
2. **Grant leg.** The function role `opal-amgt-scoped-api-role` gains `s3:GetObject` and `s3:PutObject` on EXACTLY
   `arn:aws:s3:::opal-data-harvest/amgt/harvest/state/freshness_snapshot/current/snapshot.json`. Nothing wider: no wildcard, no other
   key, no ListBucket.
3. **Schedule leg.** ONE `aws_scheduler_schedule`, a sibling of `chatter-axis-schedule.tf`'s `chatter_axis_daily`:
   - its name is `lib/opal_naming.py name()` output;
   - `cron(30 12 ? * MON-FRI *)` UTC, state ENABLED;
   - its target is the EXISTING `opal-amgt-scoped-api`, with `input` exactly `{"amgt_scheduled_action": "refresh_freshness_snapshot"}`;
   - its own scheduler role, with `lambda:InvokeFunction` on that one function only.
4. **First fire.** One direct invoke of the function with that same event: the first snapshot write.

## THE BASE, read live at signing (10:4xZ) -- the rollback per key

| object | value | rollback |
|---|---|---|
| function CodeSha256 | `0MZWPl7nGZzFI53w+vsKdS7hQpcxu4Mrd5wEMWWZQpA=` (round 74 ax-5), MemorySize 1769 | prior artifact version, one code-only safe-apply |
| function role on the snapshot key | `s3:GetObject` implicitDeny, `s3:PutObject` implicitDeny (simulated) | remove the one added statement (reverse plan) |
| the snapshot object | ABSENT (the key has never been written) | the route serves only within 24 h and falls back to compute when absent, so the rollback is a re-put of a computed view or no object; NEVER an S3 delete |
| the schedule and its role | ABSENT | the reverse plan removes both |
| open NEVER-2 entries on this function | none on the shared tree; the executor reads every live worktree | -- |

## THE CONTENT-DIFF, measured by the issuer at signing

A detached worktree at `ab28d0ba01`, `--build-only`, then `content_diff.py --zip` against deployed `0MZWPl7n`.

| class | files |
|---|---|
| CHANGED | `lib/research/api/scoped_amgt.py`, `lib/research/api/monthly_chatter.py`, `lib/research/print/render_pack.py` |
| ADDED | `lib/research/api/names_read.py`, `lib/research/api/segment_labels.py`, `lib/research/freshness/snapshot.py` |
| REMOVED | none |
| IDENTICAL | 365 of 371 |

- **Size:** 255,343,763 B against 262,144,000 B (97.4%).
- **VERIFY-SCOPE:** cold-start FATAL [] and request-time break [].
- Any other file is a STOP.

## WRITERS OF WHAT MOVES (NEVER-1)

- **The function's code: N = 1 writer,** this act.
- **The snapshot object: N = 1 writer,** `refresh_freshness_snapshot()` inside this function, reached ONLY by the schedule's
  direct-invoke event (or this act's first fire).
  - An HTTP GET never writes (plant test).
  - An unknown action returns 400 with no write.
  - A failed build or read writes nothing (500).
- **Expected effect, read from the producer's own rule:** the snapshot's rows are EQUAL to the computed view (c59 C1, 302 of 302
  locally). The route serves it while `age_hours` is 24 or less, and computes otherwise.
- **The served print, chatter, segment and passage bodies:** ay-1 adds per-figure dates and the served thesis; ay-3 changes no body
  (EQUAL 3 of 3); ay-4 changes headings and adds `passage_table` only.

## EXPECTED OUTCOMES (both branches)

| check | before (0MZWPl7n) | expected after | if not |
|---|---|---|---|
| r75 c57 / c58 / c61 deployed | FAIL (368-491 FY lines with the run date; 0 of 17; 36 bad headings, 0 of 3 tables) | YES each (local: 0, 17 of 17, 0 and 3 of 3) | rollback of the code leg |
| r75 c59 deployed C1 (snapshot served, rows EQUAL) | FAIL (no snapshot) | YES after the first fire | grant or fire fault: the route falls back; a row, then the reverse of the grant and schedule legs |
| r75 c59 C2/C3 (cold or post-hold invoke within 2 s) | FAIL (7.5 s miss) | YES (one GET of a ~2.85 MB object) | a row; not a code rollback |
| negative control: PutObject on a sibling key under `amgt/harvest/state/` | implicitDeny | implicitDeny | the grant is too wide: reverse the grant leg |
| r74 c53/c55/c56, r73 c48-c50, r71 c38 deployed | YES | YES (no regression; c55 pinned) | rollback of the code leg |
| cold chatter read (leadpanel `after`) | 3.7-4.7 s | reported (local first request 4.2-4.5 -> 3.5-4.0 s) | not a rollback; above about 2 s keeps provisioned concurrency on Andrew's list |

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-06 ~10:5xZ. The CTO half is owed at `ledger/NEVER_WIDEN_ROUND75_AY5_CTO_HALF.md`.
