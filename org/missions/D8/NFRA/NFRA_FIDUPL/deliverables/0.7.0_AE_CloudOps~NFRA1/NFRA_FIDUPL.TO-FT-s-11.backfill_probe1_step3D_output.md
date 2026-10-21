# NFRA_FIDUPL.TO-FT-s-11 step 3D -- the bounded backfill run (browser-side downloads), run once

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Order GO: msg 9032 (CTO msg 9031). Ledger nfra-fidupl-backfill-probe1-3d-20261021 opened BEFORE the run. Started only after `date -u` read 08:22:16Z with no unread message (no hold). No cookie or profile directory was touched.

run: SSM 52b0a403-ade6-4b44-b3c6-77bc8e87c4d9 on i-028e830f7226cc685, started 08:22:16Z, Success (transport) at 08:31:29Z, backfill exit=1
command: /opt/fidelity-uploader/venv/bin/python -u /opt/fidelity-uploader/backfill_main.py --config /opt/fidelity-uploader/config.json --max-seconds 480 --max-sessions 6 (SSM executionTimeout 660)
code on the box: backfill_main.py and backfill_adapter.py from the twenty-eighth delivery (ae14ca78251), fu10m R1-FU10M-OK all 23 files.
sign-in count for the hour: THREE in the trailing hour ending 08:22Z (07:22Z mine, the issuer's refused 07:49Z attempt, and this run at 08:22Z). One sign-in in this run; logout line CLOSE ok. No 401, 403 or lockout line.

## stdout, verbatim

```
SIGNIN ok secs=36
REQ POST status.json status=200 secs=0
DAY 2026-10-21 result=empty secs=0
REQ POST status.json status=200 secs=0
FILE account.txt status=200 bytes=3794367 secs=1
FILE position.txt status=200 bytes=30334785 secs=4
FILE balance.txt status=200 bytes=1221776 secs=0
FILE prices.txt status=200 bytes=646731 secs=0
FILE security.txt status=200 bytes=656599 secs=0
FILE transact.txt status=200 bytes=602207 secs=0
DAY 2026-10-20 result=completed secs=31
REQ POST status.json status=200 secs=0
FILE account.txt status=200 bytes=3794179 secs=0
FILE position.txt status=200 bytes=30326543 secs=3
FILE balance.txt status=200 bytes=1223747 secs=0
FILE prices.txt status=200 bytes=645722 secs=0
FILE security.txt status=200 bytes=655578 secs=0
DAY 2026-10-19 result=budget secs=471
ERROR: backfill run did not finish: TargetClosedError
CLOSE ok secs=0
ERROR: backfill run_id=20261021T082217Z scope=domain sign_ins=1 stop=none
FILETYPE position days=0 bytes=0 earliest=none
FILETYPE prices days=0 bytes=0 earliest=none
FILETYPE security days=0 bytes=0 earliest=none
FILETYPE account days=0 bytes=0 earliest=none
FILETYPE balance days=0 bytes=0 earliest=none
FILETYPE transact days=0 bytes=0 earliest=none
exit=1
```

## stderr, verbatim

```
WARN: trading_calendar: pandas_market_calendars absent; answering from the hardcoded NYSE fallback NYSE/hardcoded-fallback-2010-2027 (covers 2010-2027; regenerate with lib/tests/gen_nyse_closures.py --write before 2028)
Exception ignored in: <function BaseSubprocessTransport.__del__ at 0x7fed666af6a0>
Traceback (most recent call last):
  File "/usr/lib64/python3.12/asyncio/base_subprocess.py", line 126, in __del__
    self.close()
  File "/usr/lib64/python3.12/asyncio/base_subprocess.py", line 104, in close
    proto.pipe.close()
  File "/usr/lib64/python3.12/asyncio/unix_events.py", line 568, in close
    self._close(None)
  File "/usr/lib64/python3.12/asyncio/unix_events.py", line 592, in _close
    self._loop.call_soon(self._call_connection_lost, exc)
  File "/usr/lib64/python3.12/asyncio/base_events.py", line 799, in call_soon
    self._check_closed()
  File "/usr/lib64/python3.12/asyncio/base_events.py", line 545, in _check_closed
    raise RuntimeError('Event loop is closed')
RuntimeError: Event loop is closed
Future exception was never retrieved
future: <Future finished exception=TargetClosedError('Target page, context or browser has been closed')>
playwright._impl._errors.TargetClosedError: Target page, context or browser has been closed
node:events:505
    throw er; // Unhandled 'error' event
    ^

Error: write EPIPE
    at WriteWrap.onWriteComplete [as oncomplete] (node:internal/stream_base_commons:87:19)
Emitted 'error' event on Socket instance at:
    at emitErrorNT (node:internal/streams/destroy:170:8)
    at emitErrorCloseNT (node:internal/streams/destroy:129:3)
    at process.processTicksAndRejections (node:internal/process/task_queues:90:21) {
  errno: -32,
  code: 'EPIPE',
  syscall: 'write'
}

Node.js v24.21.0
```

## ft11r, verbatim

```
R1-FT11R-FAIL run_error=TargetClosedError
```

## The completion record, s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261021/backfill-20261021T082217Z.json (2525 bytes, 08:31:18Z)

- backfill true; sign_ins 1; run_error "TargetClosedError"; stop {reason "none", evidence "none"}; walk null; partial and transact_history_source keys present.
- days (date, result, secs, files, missing):
  - 2026-10-21: empty, 0 s; all six files "empty listing"; missing all six.
  - 2026-10-20: completed, 31 s; all six files "ok"; missing none.
  - 2026-10-19: budget, 471 s; no files or missing list recorded.
- per file type (account, balance, position, prices, security, transact): earliest_served "20261020", served_days 1, days 0, bytes 0, earliest_date null.
- started 08:22:17Z, finished 08:31:17Z.

## What the lines show (read from the output only)

- SIGNIN ok in 36 s. Day 2026-10-21: empty. Day 2026-10-20: six FILE lines, all status 200 (account.txt 3794367 bytes, position.txt 30334785, balance.txt 1221776, prices.txt 646731, security.txt 656599, transact.txt 602207).
- Day 2026-10-19: five FILE lines, all status 200 (account.txt 3794179 bytes, position.txt 30326543, balance.txt 1223747, prices.txt 645722, security.txt 655578); no sixth FILE line; the day then printed result=budget after 471 s. The file the output does not show for that day is the sixth in the run's order (transact.txt on the 2026-10-20 pattern); the output does not name it.
- After the budget the run printed ERROR: backfill run did not finish: TargetClosedError, CLOSE ok, and the summary with stop=none and every file type days=0 bytes=0.
- The earliest date the channel served, per file type: 2026-10-20 for all six (one day each in this run). The first earlier-date result: 2026-10-19, five of six files served and the sixth never returned inside the budget. Nothing earlier than 2026-10-19 was reached.
- Data: 0 keys under fidelity/alongside/bronze/ (excluding `_runs/`) since 08:20Z; a run record `_runs/20261019/run-20261021T082325Z.json` (2789 bytes) was written at 08:23:27Z. The five served 2026-10-19 files were not landed.
- stderr: the calendar WARN and an asyncio "Exception ignored in BaseSubprocessTransport.__del__" traceback at interpreter exit.
