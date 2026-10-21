# NFRA_FIDUPL.TO-FT-s-8 step 2G-v2 -- the G-scoped export probe on day 2026-10-20, run once

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Issuer GO: msg 8995, after the twenty-fifth box code sync (box/g_export_probe.py with the day argument, fu10m R1-FU10M-OK all 23 shipped files). Started only after `date -u` read 05:46:18Z.

run: SSM 36fff741-419d-469f-944a-19084631694e on i-028e830f7226cc685, started 05:46:18Z, Success at 05:47:04Z, probe exit=0, 11 requests
command: /opt/fidelity-uploader/venv/bin/python /opt/fidelity-uploader/box/g_export_probe.py /opt/fidelity-uploader/config.json 2026-10-20
sign-in count for the hour: TWO in the trailing hour (05:31Z and this run at 05:46Z; the 04:45Z sign-in aged out). No recovery sign-in line appears. No 401, 403 or refused switch. The probe writes nothing to disk or S3; the starting G was restored.

## stdout, verbatim (PROBE and exit lines)

```
PROBE gexp count=31 start_ordinal=0 day=2026-10-20
PROBE gexp ordinal=0 status=200 elements=6 completed_six=6 profiles=1 requests=1 ids_sha8=d79c7806
PROBE gexp ordinal=0 account status=200 bytes=3794367 rows=5009 sha8=94a0f611 line1_sha8=8a4cbf3b
PROBE gexp ordinal=1 status=200 elements=6 completed_six=6 profiles=1 requests=1 ids_sha8=d79c7806
PROBE gexp ordinal=1 account status=200 bytes=3794367 rows=5009 sha8=94a0f611 line1_sha8=8a4cbf3b
PROBE gexp ordinal=15 status=200 elements=6 completed_six=6 profiles=1 requests=1 ids_sha8=d79c7806
PROBE gexp ordinal=15 account status=200 bytes=3794367 rows=5009 sha8=94a0f611 line1_sha8=8a4cbf3b
PROBE gexp restore=ok
PROBE gexp done requests=11
exit=0
```

Other lines in the SSM output (stderr, verbatim):

```
	
```

## What the lines show (read from the output only)

- Day 2026-10-20: for each of the three ordinals read (0 the start, 1 and 15), the Export Status list returned status 200 with elements=6, completed_six=6, profiles=1, requests=1 and ids_sha8=d79c7806.
- The account.txt download for each ordinal: status 200, bytes=3794367, rows=5009, sha8=94a0f611, line1_sha8=8a4cbf3b. The three ordinals print identical values on every field, including the hashes.
- "PROBE gexp restore=ok": the starting G was restored. "PROBE gexp done requests=11". The probe's exit code is 0.
- For comparison, from earlier records (not this run): the accountList reported available=5204 under every ordinal (step 2P-v2).
- Not in the output: a logout line, and anything about the other five files of the export.
