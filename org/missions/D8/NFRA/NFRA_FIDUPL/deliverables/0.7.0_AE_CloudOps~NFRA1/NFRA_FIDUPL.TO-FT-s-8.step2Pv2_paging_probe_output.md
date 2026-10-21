# NFRA_FIDUPL.TO-FT-s-8 step 2P-v2 -- the read-only paging probe v2, run once

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Issuer GO: msg 8987 (CTO msg 8986), after the twenty-third box code sync (box/paging_probe.py v2, fu10m R1-FU10M-OK all 22 shipped files).

run: SSM d32938ed-3b06-4258-b799-b52a68ca2519 on i-028e830f7226cc685, started 04:45:02Z, Success at 04:46:16Z, exit=0, 71 requests
command: /opt/fidelity-uploader/venv/bin/python /opt/fidelity-uploader/box/paging_probe.py /opt/fidelity-uploader/config.json
sign-in count for the hour: TWO in the trailing hour (04:30Z and this run at 04:45Z); no recovery sign-in line appears. No 401 or 403 on any request. The probe lands nothing and writes nothing to S3.

## stdout, verbatim (PROBE and exit lines)

```
PROBE page1 status=200 rows=2000 available=5204 distinct=2000 page_start=null page_length=2000 session=null number_of_accounts=2000 pagereq_keys=accountNumber,custodianCode,length,sourceCode pageresp_keys=available,length,sessionCacheId,start resp_keys=accounts,firmId,numberOfAccounts,pageRequest,pageResponse,statuses,timestamp statuses=INFO:0000
PROBE startzero status=200 rows=2000 new=0 available=5204 page_start=null session=null number_of_accounts=2000 pagereq_keys=accountNumber,custodianCode,length,sourceCode pageresp_keys=available,length,sessionCacheId,start
PROBE echo status=200 rows=2000 new=0 available=5204 page_start=null session=null number_of_accounts=2000 pagereq_keys=accountNumber,custodianCode,length,sourceCode pageresp_keys=available,length,sessionCacheId,start
PROBE search kind=first3 status=200 rows=0 new=0 available=null page_start=null session=null number_of_accounts=0 pagereq_keys=none pageresp_keys=none
PROBE search kind=last3 status=200 rows=0 new=0 available=null page_start=null session=null number_of_accounts=0 pagereq_keys=none pageresp_keys=none
PROBE search kind=full status=200 rows=2000 new=1 available=5204 page_start=null session=null number_of_accounts=2000 pagereq_keys=accountNumber,custodianCode,length,sourceCode pageresp_keys=available,length,sessionCacheId,start
PROBE search kind=letter status=200 rows=0 new=0 available=null page_start=null session=null number_of_accounts=0 pagereq_keys=none pageresp_keys=none
PROBE g count=31 start_ordinal=0
PROBE g ordinal=0 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=1 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=2 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=3 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=4 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=5 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=6 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=7 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=8 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=9 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=10 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=11 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=12 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=13 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=14 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=15 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=16 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=17 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=18 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=19 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=20 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=21 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=22 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=23 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=24 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=25 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=26 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=27 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=28 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=29 status=200 available=5204 number_of_accounts=1
PROBE g ordinal=30 status=200 available=5204 number_of_accounts=1
PROBE g restore=ok
PROBE done requests=71
exit=0
```

Other lines in the SSM output (stderr, verbatim):

```
	
```

## What the lines show (read from the output only)

- Page 1: 2000 rows, 2000 distinct, available 5204, number_of_accounts 2000. The request echo carries the keys accountNumber, custodianCode, length, sourceCode; the response page object carries available, length, sessionCacheId, start (names only; values are null where printed null).
- start=0 test and the echo test: 2000 rows, new=0.
- Search counts: first3, last3 and letter returned 0 rows (available null); full returned 2000 rows with new=1.
- G sweep: 31 ordinals, every one status 200 with available=5204 and number_of_accounts=1; the starting G was restored (PROBE g restore=ok).
- Not in the output: the values of the echo and page keys, and a logout line.
