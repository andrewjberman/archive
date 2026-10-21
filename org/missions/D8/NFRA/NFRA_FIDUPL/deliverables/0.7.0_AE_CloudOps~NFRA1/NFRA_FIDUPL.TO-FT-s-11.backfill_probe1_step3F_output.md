# NFRA_FIDUPL.TO-FT-s-11 step 3F -- the backfill run to the channel's limit, run once

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Order GO: msg 9071 (CTO msgs 9042 and 9036). Ledger nfra-fidupl-backfill-probe1-3f-20261021 opened BEFORE the run. Started only after `date -u` read 11:20:39Z with no unread message (no hold). No cookie or profile directory was touched.

run: SSM 5ad1ff0a-efad-406f-9697-173a387b91c4 on i-028e830f7226cc685, started 11:20:39Z, Success (transport) at 11:22:36Z, backfill exit=0
command: /opt/fidelity-uploader/venv/bin/python -u /opt/fidelity-uploader/backfill_main.py --config /opt/fidelity-uploader/config.json --skip-files transact.txt --max-seconds 480 --max-sessions 12 (SSM executionTimeout 660)
code on the box: the thirtieth delivery (a973776db99), fu10m R1-FU10M-OK all 23 files.
sign-in count for the hour: THREE in the trailing hour ending 11:20Z (10:27Z manual start, 11:05Z one-shot, and this run at 11:20Z). One sign-in in this run; logout line CLOSE ok. No 401, 403 or lockout line.

## stdout, verbatim

```
SIGNIN ok secs=34
REQ POST status.json status=200 secs=0
FILE account.txt status=200 bytes=3797333 secs=1
FILE position.txt status=200 bytes=30333376 secs=5
FILE balance.txt status=200 bytes=1222782 secs=0
FILE prices.txt status=200 bytes=647773 secs=0
FILE security.txt status=200 bytes=657657 secs=0
FILE transact.txt status=skipped bytes=0 secs=0
DAY 2026-10-21 result=completed secs=33
REQ POST status.json status=200 secs=0
FILE account.txt status=200 bytes=3794367 secs=0
FILE position.txt status=200 bytes=30334785 secs=5
FILE balance.txt status=200 bytes=1221776 secs=0
FILE prices.txt status=200 bytes=646731 secs=0
FILE security.txt status=200 bytes=656599 secs=0
FILE transact.txt status=skipped bytes=0 secs=0
DAY 2026-10-20 result=completed secs=20
REQ POST status.json status=200 secs=0
FILE account.txt status=200 bytes=3794179 secs=1
FILE position.txt status=200 bytes=30326543 secs=5
FILE balance.txt status=200 bytes=1223747 secs=1
FILE prices.txt status=200 bytes=645722 secs=0
FILE security.txt status=200 bytes=655578 secs=1
FILE transact.txt status=skipped bytes=0 secs=0
DAY 2026-10-19 result=completed secs=22
REQ POST status.json status=200 secs=0
DAY 2026-10-16 result=empty secs=0
REQ POST status.json status=200 secs=0
DAY 2026-10-15 result=empty secs=0
REQ POST status.json status=200 secs=0
DAY 2026-10-14 result=retention secs=0
CLOSE ok secs=0
OK: backfill run_id=20261021T112040Z scope=domain sign_ins=1 stop=retention
FILETYPE position days=0 bytes=0 earliest=none
FILETYPE prices days=0 bytes=0 earliest=none
FILETYPE security days=0 bytes=0 earliest=none
FILETYPE account days=1 bytes=3794179 earliest=20261019
FILETYPE balance days=0 bytes=0 earliest=none
FILETYPE transact days=0 bytes=0 earliest=none
exit=0
```

## stderr, verbatim

```
WARN: trading_calendar: pandas_market_calendars absent; answering from the hardcoded NYSE fallback NYSE/hardcoded-fallback-2010-2027 (covers 2010-2027; regenerate with lib/tests/gen_nyse_closures.py --write before 2028)
```

## ft11r, verbatim

```
R1-FT11R-OK backfill record: sign_ins=1 stop=retention earliest account:20261019,balance:None,position:None,prices:None,security:None,transact:None
```

## The completion record, s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261021/backfill-20261021T112040Z.json (6779 bytes, 11:22:35Z)

- backfill true; sign_ins 1; run_error null; partial false; skip_files ["transact.txt"]; caps max_days 125, max_exports_per_run 12, max_seconds 480, max_sessions_per_day 12.
- stop: reason "retention", evidence "empty listing x3". walk: earliest_date "20261019", stop_reason "retention".
- transact_history_source: "per-account historical route (CRO date-range method), not the standing export".
- days (date, result, secs; landing):
  - 2026-10-21: completed, 33 s; account, balance, position, prices, security "ok" and skipped_existing; transact skipped_by_option (landing "failed:read:file absent from the handoff directory"); missing ["transact.txt"].
  - 2026-10-20: completed, 20 s; the same five ok and skipped_existing; transact as above.
  - 2026-10-19: completed, 22 s; account.txt "landed"; balance, position, prices, security skipped_existing; transact as above.
  - 2026-10-16: empty, 0 s (all six "empty listing", not_downloaded).
  - 2026-10-15: empty, 0 s (all six "empty listing").
  - 2026-10-14: retention, 0 s (all six "empty listing").
- per file type (bytes landed, days landed, earliest_date, earliest_served, served_days):
  - account: 3794179 bytes, 1 day, earliest_date 20261019, earliest_served 20261019, served_days 3
  - balance: 0, 0 days, none, 20261019, 3
  - position: 0, 0 days, none, 20261019, 3
  - prices: 0, 0 days, none, 20261019, 3
  - security: 0, 0 days, none, 20261019, 3
  - transact: 0, 0 days, none, earliest_served none, served_days 0 (skipped by option)

## What S3 shows (read-only, 11:23Z)

Data keys written since 11:19Z (excluding `_runs/`): ONE, fidelity/alongside/bronze/account/20261016/account.txt (3794179 bytes, 11:22:33Z). The other four served file types of 2026-10-19 were landed by the step 3E run (09:05Z) under content date 20261016 and read skipped_existing here. Run records written during the run: `_runs/20261020/run-20261021T112148Z.json`, `_runs/20261019/run-20261021T112209Z.json`, `_runs/20261016/run-20261021T112232Z.json`.

## What the lines show (read from the output only)

- The empirical limit of the standing export channel: it serves three business-day exports (2026-10-19, 2026-10-20, 2026-10-21) for the five served file types; 2026-10-16, 2026-10-15 and 2026-10-14 list empty three days running, and the run stopped on retention.
- The first earlier-date result: 2026-10-16, empty. The earliest date served per file type (export day): 2026-10-19 for account, balance, position, prices and security. The landed content date for the 2026-10-19 export is 20261016 (the key date), as the lander rule places an as-of that is not a trading day.
- transact.txt: skipped by option on all three days; its landing line reads "failed:read:file absent from the handoff directory" because nothing was downloaded; the record names the per-account historical route as its history source.
- The run ended by itself in 117 s, exit 0, with CLOSE ok.
- stderr: the calendar WARN only.
