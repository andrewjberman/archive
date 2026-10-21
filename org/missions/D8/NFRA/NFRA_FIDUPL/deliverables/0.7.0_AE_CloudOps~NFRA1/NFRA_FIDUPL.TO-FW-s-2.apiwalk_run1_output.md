# NFRA_FIDUPL.TO-FW-s-2 -- API walk, first run (the short proof): stop error, SigninError

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Order TO-FW-s-2 released by msg 9184. Runs ledger nfra-fidupl-apiwalk-runs-20261021 open before the run. Started after delivery (fu10m R1-FU10M-OK all 25 shipped files), with no run in progress on the box (0 automation executions, 0 SSM commands) and no unread message. No cookie or profile directory was touched.

run: SSM ee9500dc-1067-4746-a68e-34e69efe1c3f on i-028e830f7226cc685, START 17:53:45Z, Success (transport) at 17:56:19Z, api_walk.py exit=1
command: /opt/fidelity-uploader/venv/bin/python -u /opt/fidelity-uploader/api_walk.py --config /opt/fidelity-uploader/config.json --surfaces open --max-accounts 100 --max-seconds 600 (SSM executionTimeout 3000)
sign-in count: one sign-in attempt in this run, which failed. Earlier in the trailing hour: my histwalk run 3 at 17:05Z (ok). At most 2 of my runs started in the rolling hour.

## stdout, verbatim

```
ERROR: apiwalk did not finish: SigninError
ERROR: apiwalk run_id=20261021T175344Z sign_ins=1 stop=error
exit=1
```

stderr: empty.

## The apiwalk record (s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261021/apiwalk-20261021T175344Z.json, 719 bytes)

```
keys: ['anchor', 'apiwalk', 'caps', 'earliest_by_account', 'finished_at', 'partial', 'per_surface', 'run_error', 'run_id', 'scope', 'sign_ins', 'started_at', 'stop']
apiwalk = true
sign_ins = 1
run_error = "SigninError"
stop = {"evidence": "SigninError", "reason": "error"}
run_id = "20261021T175344Z"
started_at = "2026-10-21T17:53:44Z"
finished_at = "2026-10-21T17:56:11Z"
caps = {"gap": 0.3, "max_accounts": 100, "max_seconds": 600}
```

## What the output shows

- The run ended in 147 s with stop=error, run_error SigninError: the sign-in did not complete. No surface was worked and no data key was written (the only key written since 17:50Z is the record itself).
- The record names no sign-in step or failure class; the reason is not in the output.
- No retry, per the order. All further sign-ins from this seat are on hold until the issuer decides.
