# NFRA_FIDUPL.TO-FT-s-11 step 3E -- the bounded backfill run (90 s per-file cap, served files land), run once

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Order GO: msg 9038 (CTO msgs 9031 and 9036), update msg 9040. Ledger nfra-fidupl-backfill-probe1-3e-20261021 opened BEFORE the run. Started only after `date -u` read 08:56:14Z with no unread message (no hold). No cookie or profile directory was touched. Done at 09:05:19Z, before the 09:30Z deadline.

run: SSM f26b9129-0448-419c-8838-4515ce3da500 on i-028e830f7226cc685, started 08:56:14Z, Success (transport) at 09:05:19Z, backfill exit=1
command: /opt/fidelity-uploader/venv/bin/python -u /opt/fidelity-uploader/backfill_main.py --config /opt/fidelity-uploader/config.json --max-seconds 480 --max-sessions 8 (SSM executionTimeout 660)
code on the box: backfill_main.py and backfill_adapter.py from the head 4d6a1aafeda (delivered 08:51Z, fu10m R1-FU10M-OK all 23 files).
sign-in count for the hour: TWO in the trailing hour ending 08:56Z (08:22Z mine and this run at 08:56Z). One sign-in in this run; logout line CLOSE ok. No 401, 403 or lockout line.

## stdout, verbatim

```
SIGNIN ok secs=36
REQ POST status.json status=200 secs=0
DAY 2026-10-21 result=empty secs=0
REQ POST status.json status=200 secs=0
FILE account.txt status=200 bytes=3794367 secs=3
FILE position.txt status=200 bytes=30334785 secs=12
FILE balance.txt status=200 bytes=1221776 secs=0
FILE prices.txt status=200 bytes=646731 secs=0
FILE security.txt status=200 bytes=656599 secs=0
FILE transact.txt status=200 bytes=602207 secs=0
DAY 2026-10-20 result=completed secs=41
REQ POST status.json status=200 secs=0
FILE account.txt status=200 bytes=3794179 secs=1
FILE position.txt status=200 bytes=30326543 secs=9
FILE balance.txt status=200 bytes=1223747 secs=0
FILE prices.txt status=200 bytes=645722 secs=0
FILE security.txt status=200 bytes=655578 secs=0
FILE_LANDED 2026-10-19 files=4
DAY 2026-10-19 result=budget secs=461
ERROR: backfill run did not finish: TargetClosedError
CLOSE ok secs=0
ERROR: backfill run_id=20261021T085615Z scope=domain sign_ins=1 stop=none
FILETYPE position days=1 bytes=30326543 earliest=20261019
FILETYPE prices days=1 bytes=645722 earliest=20261019
FILETYPE security days=1 bytes=655578 earliest=20261019
FILETYPE account days=0 bytes=0 earliest=none
FILETYPE balance days=1 bytes=1223747 earliest=20261019
FILETYPE transact days=0 bytes=0 earliest=none
exit=1
```

## stderr, verbatim

```
WARN: trading_calendar: pandas_market_calendars absent; answering from the hardcoded NYSE fallback NYSE/hardcoded-fallback-2010-2027 (covers 2010-2027; regenerate with lib/tests/gen_nyse_closures.py --write before 2028)
Exception ignored in: <function BaseSubprocessTransport.__del__ at 0x7f47fc933ba0>
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

## The completion record, s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261021/backfill-20261021T085615Z.json (2871 bytes, 09:05:18Z)

- backfill true; sign_ins 1; run_error "TargetClosedError"; stop {reason "none", evidence "none"}; partial false; walk null.
- transact_history_source: "per-account historical route (CRO date-range method), not the standing export".
- days (date, result, secs, files, missing):
  - 2026-10-21: empty, 0 s; all six files "empty listing"; missing all six.
  - 2026-10-20: completed, 41 s; all six files "ok"; missing none.
  - 2026-10-19: budget, 461 s; account, balance, position, prices, security "ok"; transact "interrupted_WallBudget"; landed_on_stop 4; missing ["transact.txt"].
- per file type (earliest_date, earliest_served, served_days, days landed, bytes landed):
  - position: 20261019, 20261019, 2, 1 day, 30326543 bytes
  - balance: 20261019, 20261019, 2, 1 day, 1223747 bytes
  - prices: 20261019, 20261019, 2, 1 day, 645722 bytes
  - security: 20261019, 20261019, 2, 1 day, 655578 bytes
  - account: null, 20261020, 1, 0 days, 0 bytes
  - transact: null, 20261020, 1, 0 days, 0 bytes
- started 08:56:15Z, finished 09:05:17Z.

## What S3 shows (read-only, 09:06Z)

Data keys written since 08:50Z (excluding `_runs/`), four, all at 09:05:17Z:

- fidelity/alongside/bronze/balance/20261016/balance.txt (1223747 bytes)
- fidelity/alongside/bronze/position/20261016/position.txt (30326543 bytes)
- fidelity/alongside/bronze/prices/20261016/prices.txt (645722 bytes)
- fidelity/alongside/bronze/security/20261016/security.txt (655578 bytes)

Run records written since 08:50Z: `_runs/20261019/run-20261021T085734Z.json` (2789 bytes, 08:57:35Z), `_runs/20261017/run-20261021T090516Z.json` (2715 bytes, 09:05:17Z) and the backfill record above.

## What the lines show (read from the output only)

- First landing by the backfill: FILE_LANDED 2026-10-19 files=4. The four landed files are the 2026-10-19 export's balance, position, prices and security; their keys sit under the content date 20261016, while the record's earliest_date for them reads 20261019 (the export day). Both are as printed; the output does not say which date the issuer expects.
- account.txt of 2026-10-19 was served (status 200, 3794179 bytes, record "ok") but is not among the four landed and its file type shows days 0; the output does not say why.
- transact.txt of 2026-10-19 was not served: the record shows "interrupted_WallBudget". The day took 461 s although a 90 s total cap per file is in the code, so the cap did not end that request before the budget.
- The walk stopped on 2026-10-19 (budget); nothing earlier than 2026-10-19 was reached.
- After the budget the run printed ERROR: backfill run did not finish: TargetClosedError, CLOSE ok, and stop=none.
- stderr: the calendar WARN and an asyncio "Exception ignored in BaseSubprocessTransport.__del__" traceback at interpreter exit.
