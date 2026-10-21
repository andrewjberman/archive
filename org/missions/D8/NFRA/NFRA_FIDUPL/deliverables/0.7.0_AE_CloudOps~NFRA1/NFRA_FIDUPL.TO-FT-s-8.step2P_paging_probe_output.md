# NFRA_FIDUPL.TO-FT-s-8 step 2P -- the read-only paging probe, run once

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Issuer GO: msg 8979 (start 04:30Z or later, ONE run, stop on any 401/403).

run: SSM 806a21bd-abfc-455b-ab61-63f5002dffef on i-028e830f7226cc685, started 04:30:40Z, Success at 04:32:04Z, exit=0
command: /opt/fidelity-uploader/venv/bin/python /opt/fidelity-uploader/box/paging_probe.py /opt/fidelity-uploader/config.json
sign-in count for the hour: this run is the FIRST in its trailing hour (the previous sign-ins were 02:49Z, 03:04Z and 03:29Z; the 03:29Z one aged out at 04:29Z). No 401 or 403 appears. The probe lands nothing and writes nothing to S3 (nothing under any prefix was touched by me).

## stdout, verbatim

```
PROBE page1 status=200 rows=2000 available=5204 distinct=2000 page_start=null page_length=2000 session=null resp_keys=accounts,firmId,numberOfAccounts,pageRequest,pageResponse,statuses,timestamp statuses=INFO:0000
PROBE form=0 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE form=1 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE form=2 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE form=3 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE form=4 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE form=5 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE form=6 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE form=7 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE form=8 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE form=9 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE form=10 status=200 rows=2000 new=0 available=5204 page_start=null session=null statuses=INFO:0000
PROBE prefix=0 status=200 available=null
PROBE prefix=1 status=200 available=null
PROBE prefix=2 status=200 available=null
PROBE prefix=3 status=200 available=null
PROBE prefix=4 status=200 available=null
PROBE prefix=5 status=200 available=null
PROBE prefix=6 status=200 available=null
PROBE prefix=7 status=200 available=null
PROBE prefix=8 status=200 available=null
PROBE prefix=9 status=200 available=null
PROBE prefix=A status=200 available=null
PROBE prefix=B status=200 available=null
PROBE prefix=C status=200 available=null
PROBE prefix=D status=200 available=null
PROBE prefix=E status=200 available=null
PROBE prefix=F status=200 available=null
PROBE prefix=G status=200 available=null
PROBE prefix=H status=200 available=null
PROBE prefix=I status=200 available=null
PROBE prefix=J status=200 available=null
PROBE prefix=K status=200 available=null
PROBE prefix=L status=200 available=null
PROBE prefix=M status=200 available=null
PROBE prefix=N status=200 available=null
PROBE prefix=O status=200 available=null
PROBE prefix=P status=200 available=null
PROBE prefix=Q status=200 available=null
PROBE prefix=R status=200 available=null
PROBE prefix=S status=200 available=null
PROBE prefix=T status=200 available=null
PROBE prefix=U status=200 available=null
PROBE prefix=V status=200 available=null
PROBE prefix=W status=200 available=null
PROBE prefix=X status=200 available=null
PROBE prefix=Y status=200 available=null
PROBE prefix=Z status=200 available=null
PROBE done requests=48
exit=0
```

## What the lines show (read from the output only; nothing here is a measurement the probe did not print)

- Page 1: 2000 rows, 2000 distinct, available 5204, page_start null, session null; the response carries the top-level keys accounts, firmId, numberOfAccounts, pageRequest, pageResponse, statuses, timestamp.
- Forms 0 to 10: every one returned status 200 and 2000 rows with new=0 (no new distinct row), available 5204 each time, statuses INFO:0000. None of the eleven pages.
- Prefix sweep: all 36 prefixes returned status 200 with available null (the response did not carry pageResponse.available for a prefixed request).
- Not in the output: the content of the response's pageRequest key (the probe prints key names only), and whether the logout ran (the probe's finally logs out; no logout line is printed).
- No 401 or 403 on any of 48 requests.
