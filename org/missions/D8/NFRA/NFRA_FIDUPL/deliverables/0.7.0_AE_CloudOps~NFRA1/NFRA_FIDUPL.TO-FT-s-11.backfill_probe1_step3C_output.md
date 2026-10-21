# NFRA_FIDUPL.TO-FT-s-11 step 3C -- the bounded backfill run, run once

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Order GO: msg 9019 (CTO msg 9018). Ledger nfra-fidupl-backfill-probe1-3c-20261021 opened BEFORE the run. Started only after `date -u` read 07:22:16Z and no unread message.

run: SSM 1441ca48-d06c-42c6-9750-90239de00c39 on i-028e830f7226cc685, started 07:22:16Z, Success (transport) at 07:31:29Z, backfill exit=1
command: /opt/fidelity-uploader/venv/bin/python -u /opt/fidelity-uploader/backfill_main.py --config /opt/fidelity-uploader/config.json --max-seconds 480 --max-sessions 4 (SSM executionTimeout 660)
code on the box for this run: the file from the 170a9c69ce8 delivery (made 07:21Z). The issuer's update msg 9026 (head 3d8b85fd61d: per-day partial record, SIGTERM logout) was sent at 07:28:41Z, after the run began; the box was re-delivered from that head at 07:33Z (after the run).
sign-in count for the hour: THREE in the trailing hour (the issuer's 07:08Z read-only sign-in, 06:47Z mine, and this run at 07:22Z; 06:32Z aged out at 07:22Z). One sign-in in this run; logout line CLOSE ok. No 401, 403 or lockout line.

## stdout, verbatim

```
SIGNIN ok secs=34
REQ POST status.json status=200 secs=0
DAY 2026-10-21 result=empty secs=0
REQ POST status.json status=200 secs=0
REQ GET downloadExport.do status=200 secs=1
REQ GET downloadExport.do status=200 secs=26
REQ GET downloadExport.do status=200 secs=0
REQ GET downloadExport.do status=200 secs=0
REQ GET downloadExport.do status=200 secs=0
REQ GET downloadExport.do status=200 secs=0
DAY 2026-10-20 result=completed secs=30
REQ POST status.json status=200 secs=0
REQ GET downloadExport.do status=200 secs=0
REQ GET downloadExport.do status=200 secs=16
REQ GET downloadExport.do status=200 secs=0
REQ GET downloadExport.do status=200 secs=0
REQ GET downloadExport.do status=200 secs=1
REQ GET downloadExport.do status=error:WallBudget secs=452
DAY 2026-10-19 result=budget secs=473
ERROR: backfill run did not finish: TargetClosedError
CLOSE ok secs=0
ERROR: backfill run_id=20261021T072217Z scope=domain sign_ins=1 stop=none
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
Exception ignored in: <function BaseSubprocessTransport.__del__ at 0x7fd325edaa20>
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
```

## ft11r, verbatim

```
R1-FT11R-FAIL run_error=TargetClosedError
```

## The completion record, s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261021/backfill-20261021T072217Z.json (1373 bytes, 07:31:18Z)

- backfill true; sign_ins 1; run_error "TargetClosedError"; stop {reason "none", evidence "none"}; walk null.
- days list (date, result, secs): 2026-10-21 empty 0; 2026-10-20 completed 30; 2026-10-19 budget 473.
- per file type (account, balance, position, prices, security, transact): days 0, bytes 0, earliest_date null.
- started 07:22:17Z, finished 07:31:17Z.

## What the lines show (read from the output only)

- SIGNIN ok in 34 s. Day 2026-10-21: empty. Day 2026-10-20: completed in 30 s (one status.json call, six downloadExport.do calls, all status 200; the slowest took 26 s). Day 2026-10-19: one status.json call, five downloadExport.do calls status 200, then a sixth downloadExport.do call that ran 452 s and ended `error:WallBudget`; the day result is `budget` after 473 s.
- After the budget the run raised TargetClosedError ("backfill run did not finish"), printed CLOSE ok, then the summary with stop=none and every file type at days=0 bytes=0.
- The first earlier-date result: 2026-10-19, `budget` (a download request that did not return in 452 s); nothing earlier than 2026-10-20 was reached.
- Data: 0 keys under fidelity/alongside/bronze/ (excluding `_runs/`) since 07:20Z, although day 2026-10-20 printed `completed`; a run record `_runs/20261019/run-20261021T072323Z.json` (2789 bytes) was written at 07:23:25Z. Whether 2026-10-20 was counted as already landed is not stated in the output.
- stderr: the calendar WARN and an asyncio "Exception ignored in BaseSubprocessTransport.__del__" traceback at interpreter exit.
