# NFRA_FIDUPL.TO-FT-s-11 step 3B -- the backfill rerun, run once: killed at the SSM cap, no output

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Order GO: msg 9009 (step 3B, 06:47Z or later). Started only after `date -u` read 06:47:20Z and no newer message was unread.

run: SSM bfd976a6-b9e4-4162-8bb7-1124a1d2bd8b on i-028e830f7226cc685, started 06:47:20Z, status TimedOut at the executionTimeout 900 (read 07:02:25Z)
command: /opt/fidelity-uploader/venv/bin/python /opt/fidelity-uploader/backfill_main.py --config /opt/fidelity-uploader/config.json
sign-in count for the hour: THREE in the trailing hour (06:01Z mine, about 06:32Z the issuer's read-only sign-in, and this run at 06:47Z). No recovery sign-in exists in this walk. No 401, 403 or lockout line (there was no stdout at all).

## stdout and stderr, verbatim (the whole SSM output)

```
	WARN: trading_calendar: pandas_market_calendars absent; answering from the hardcoded NYSE fallback NYSE/hardcoded-fallback-2010-2027 (covers 2010-2027; regenerate with lib/tests/gen_nyse_closures.py --write before 2028)
```

No stdout line and no `exit=` line: the SSM agent stopped the command at 900 seconds, before the program (or the `echo exit=$?` after it) printed anything. ft11r was not run (no completion record exists to read).

## What the box and S3 show afterwards (read-only, 07:03Z)

- Records: one run record `_runs/20261019/run-20261021T064829Z.json` (2789 bytes) was written at 06:48:31Z, about 70 seconds into the run; no `backfill-<run id>.json` completion record and nothing else under `_runs/` since 06:40Z.
- Data: 0 keys under fidelity/alongside/bronze/ (excluding `_runs/`) since 06:40Z.
- Box: no backfill_main, perg_seed, signin, run.py, paging_probe or g_export process is left; the agent Chrome unit is active (chrome count 12, as before).
- Not known: whether the Fidelity session was logged out (the process was stopped by the cap, so its logout path may not have run), and which Export Status request was in flight.
