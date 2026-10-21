# NFRA_FIDUPL.TO-FT-s-8 step 2G -- the G-scoped export probe, run once

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Issuer GO: msg 8992 (CTO msg 8990), after the twenty-fourth box code sync (box/g_export_probe.py, fu10m R1-FU10M-OK all 23 shipped files). Started only after `date -u` read 05:31:21Z.

run: SSM 3a63765f-3e40-493d-9587-2e6c7ebbaf5d on i-028e830f7226cc685, started 05:31:21Z, Success at 05:32:08Z, probe exit=1, 8 requests
command: /opt/fidelity-uploader/venv/bin/python /opt/fidelity-uploader/box/g_export_probe.py /opt/fidelity-uploader/config.json
sign-in count for the hour: TWO in the trailing hour (04:45Z and this run at 05:31Z; the 04:30Z sign-in aged out at 05:30Z). No recovery sign-in line appears. No 401, 403 or refused switch on any request. The probe writes nothing to disk or S3; the starting G was restored.

## stdout, verbatim (PROBE and exit lines)

```
PROBE gexp count=31 start_ordinal=0 day=2026-10-21
PROBE gexp ordinal=0 status=200 elements=0 completed_six=0 profiles=0 requests=0 ids_sha8=da39a3ee
PROBE gexp ordinal=0 account absent
PROBE gexp ordinal=1 status=200 elements=0 completed_six=0 profiles=0 requests=0 ids_sha8=da39a3ee
PROBE gexp ordinal=1 account absent
PROBE gexp ordinal=15 status=200 elements=0 completed_six=0 profiles=0 requests=0 ids_sha8=da39a3ee
PROBE gexp ordinal=15 account absent
PROBE gexp restore=ok
PROBE gexp done requests=8
exit=1
```

Other lines in the SSM output (stderr, verbatim):

```
	
```

## What the lines show (read from the output only)

- The probe printed count=31 and start_ordinal=0 and used day=2026-10-21.
- Three ordinals were read (0, 1 and 15). For each: status 200, elements=0, completed_six=0, profiles=0, requests=0, ids_sha8=da39a3ee (the first eight hex digits of the SHA-1 of an empty input, i.e. an empty id list), and "account absent".
- "PROBE gexp restore=ok": the starting G was restored. "PROBE gexp done requests=8".
- The probe's own exit code is 1; the output does not say why (no error line). Reading it against the lines above is the issuer's.
- Not in the output: which day the Export Status list was asked for beyond the printed day=2026-10-21 (the daily run's business_day was 2026-10-20), and a logout line.
