# NFRA_FIDUPL.TO-FT-s-11 -- backfill probe 1, live, run once

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Order GO: msg 9004 (CTO msg 8999; Andrew-direct record ANDREW_DIRECT_20261021_012xZ). Started only after `date -u` read 06:01:20Z.

run: SSM fa3700a4-30fe-414f-a377-f41a083b7663 on i-028e830f7226cc685, started 06:01:20Z, Success (transport) at 06:03:46Z, backfill exit=1
command: /opt/fidelity-uploader/venv/bin/python /opt/fidelity-uploader/backfill_main.py --config /opt/fidelity-uploader/config.json
sign-in count for the hour: THREE in the trailing hour (05:31Z, 05:46Z, and this run at 06:01Z); no recovery sign-in exists in this walk and none fired. No 401, 403 or lockout line.

## stdout, verbatim

```
ERROR: backfill run did not finish: TimeoutError
ERROR: backfill run_id=20261021T060121Z scope=domain sign_ins=1 stop=none
FILETYPE position days=0 bytes=0 earliest=none
FILETYPE prices days=0 bytes=0 earliest=none
FILETYPE security days=0 bytes=0 earliest=none
FILETYPE account days=0 bytes=0 earliest=none
FILETYPE balance days=0 bytes=0 earliest=none
FILETYPE transact days=0 bytes=0 earliest=none
exit=1
```

Other lines in the SSM output (stderr, verbatim):

```
	WARN: trading_calendar: pandas_market_calendars absent; answering from the hardcoded NYSE fallback NYSE/hardcoded-fallback-2010-2027 (covers 2010-2027; regenerate with lib/tests/gen_nyse_closures.py --write before 2028)
```

## ft11r, verbatim

```
R1-FT11R-FAIL run_error=TimeoutError
```

## The completion record, read from s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261021/backfill-20261021T060121Z.json (1074 bytes)

- backfill true; sign_ins 1; run_error "TimeoutError"; stop {reason "none", evidence "none"}; walk null.
- per file type (account, balance, position, prices, security, transact): days 0, bytes 0, earliest_date null.
- caps: max_days 125, max_exports_per_run 12, max_sessions_per_day 2; scope "domain", landing_scope "alongside".

## What the lines show (read from the output only)

- The run signed in once and ended with TimeoutError before the walk began. No stop reason, no day landed, no earlier-date result (served, empty or refused): the walk never produced one.
- Zero data keys were written under fidelity/alongside/bronze/ from 06:00Z (excluding _runs/). A run record `_runs/20261019/run-20261021T060236Z.json` (2789 bytes) was written at 06:02:37Z during the run; its content was not read.
- Not in the output: which request timed out.
