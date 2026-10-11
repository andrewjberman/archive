# R22_ROOT_CAUSE -- why the 4 oldest monday_meeting transcripts never landed (TO NFRA_TRNSPT.TO-TR-rc22)

Worker 0.9.0_WK_NFRA_TRNSPT~2, read at base f16365b224. LOCAL, read-only, no AWS or HTTP. Ids and times only.
Replay: `data/transcripts/scripts/tests/test_monday_skip_replay.py` (3 tests, all pass).

## What is pinned from the code

1. **The scheduled pull has no window, no date filter and no series expansion.** `pull.py:_pull_series` (lines 142-187)
   lists every row, and unless its sidecar is held (`pull.py:151`) reads and lands it. Age never enters. Replayed on the
   20-row fixture with every read served, it lands all 20 including the four oldest
   (`test_replay_skips_exactly_the_four`, negative arm).
2. **The 365-day backfill (TO-RUN-b17) did not skip them and could not have landed them.** Its entry point is
   `python data/transcripts/scripts/outlook/pull.py --gateway --days 365 --apply` (order step 4), the OUTLOOK mail pull
   for table `analysis_commentary` (result: listed 453, landed 24 on 6 dates). It lists no Teams meeting.
   The wording "the earlier 365-day backfill did not reach them" (row D2-S15) names a pipeline that is not the Teams one.
3. **The only code line that passes over a listed, not-held row and keeps going is `pull.py:161-164`:**
   `except Expired:` -> outcome `EXPIRED` -> `continue`. Replaying the four census-missing reads as `Expired` gives
   exactly 16 LANDED and 4 EXPIRED, on the four dates 2026-04-10, 04-13, 05-04, 06-01.
4. **That line is unreachable on the live transport.** `gateway_client.Expired` (`gateway_client.py:41`) is raised only by
   `FixtureTransport` (`gateway_client.py:143`). `GatewayTransport` raises a `GatewayError` subclass for any non-200
   (`gateway_client.py:228-229`, `_refusal` 170-195); its contract table (HX_TRANSCRIPTS_ROUTE_CONTRACT_COPY) has no 404 and
   maps a Graph refusal to `502 graph_error`. `pull.py` catches `Refused` on the list and `Expired` on the read, nothing else.

## What is NOT pinned (so row NFRA_TRNSPT-D2-W2-S11)

Why the four were unlanded cannot be read from code. The only dated evidence is the PRD arc (`NFRA_TRNSPT_PRD.md:129`):
"34 transcripts listed and 30 retrieved before four expired" -- consistent with these four (19 listed, 15 retrieved), but a
document, not a read of the gateway's answer for the four ids. Nothing here measured that answer (no HTTP). The cutoff
fits a retention horizon (2026-09-30 minus 06-01 is 121 days, minus 06-08 is 114) but no code carries 120 or any age constant
in the Teams pull; that is an inference and is stated as one.

## Code line

`data/transcripts/scripts/teams/pull.py:161` (`except Expired:`, branch 161-164), the only skip branch; and no window in the
selection. Path that skipped: neither the scheduled pull's selection nor the backfill dropped them by rule. The unlanded state
dates from the first hand landing (PRD arc), where the four were unreadable; the scheduled pull has attempted them on every fire
since and has not landed them.

## Scheduled-path verdict

The scheduled pull would NOT skip a meeting for being older than a window (there is none) and is not "new ones only": it retries
every listed unlanded row on each fire (`test_scheduled_path_verdict_stated`, replayed at injected clocks 2026-10-11 and 2027-10-11).
If a listed row's content read FAILS, the live path does not skip it: the `GatewayError` propagates out of `_pull_series` and ends
the run (`pull.run` loop, `pull.py:204-208`), after the rows listed before it have landed (replay: 16 landed, then the raise), and
before the run record and listing snapshot are written (`pull.py:210-217`) and before any later series is pulled. So if the gateway
fails the four reads, every hourly fire repeats that; whether it does is unmeasured.

## Smallest fix if the failure is confirmed (NOT made; TR-rf-22's)

One line at `pull.py:161`: `except (Expired, gateway_client.GatewayError):` so a failed read is recorded as EXPIRED and the loop
continues; or map the failed read to `Expired` inside `GatewayTransport.read_meeting_transcript`. Measure first what the gateway
answers for the four ids (one read-only GET each, no content kept): if it serves content, the four are landable by the existing
code and TR-rv-22 needs no fix; if it fails, the line above is the fix.
