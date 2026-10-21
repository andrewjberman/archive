# Row AMGT_HARVST-D1-S69 -- triage part 2: which packages, and is any a Python distribution or a network client in the closure? (2.0.0_SA_COO~W1, 2026-10-21 ~01:3xZ)

Continues `S69_SCAN_TRIAGE_PART1_EXPOSURE.md` (`2dc420645c`). Image `amgt-gold-refresh-repo@sha256:4da76365a1beb45df5a642ab3b2d0b3fdcdf1564ce78a60025306574c45fdd74`.

## (b) Every finding's package, by severity (read by me from `describe-image-scan-findings`, 38 findings listed, no nextToken)

| Severity | Count | Packages |
|---|---|---|
| HIGH | 12 | curl-minimal, libcurl-minimal, openssl-fips-provider-latest, openssl-snapsafe-libs, pcre2, pcre2-syntax, rpm, rpm-libs |
| MEDIUM | 20 | libxml2, openssl-fips-provider-latest, openssl-snapsafe-libs |
| LOW | 5 | libxml2, openssl-fips-provider-latest, openssl-snapsafe-libs |
| UNDEFINED | 1 | krb5-libs |

**All 38 findings name an Amazon Linux 2023 operating-system package.** Overlap with the 13 pinned Python distributions of `requirements.txt` (pyarrow, pandas, numpy, exchange_calendars, pandas_market_calendars, pytz, python-dateutil, tzdata, toolz, pyluach, cloudpickle, six, korean_lunar_calendar): none. The scan lists no Python-package finding at all (a scan that reads only OS packages would also show none, and I have not established which of those two it is).

## (a) Outbound clients in the measured closure

`co5_closure.out` (worker `~189`, 21 lines on the closure) names no `requests`, `urllib3`, `http`, `httpx`, `socket`, `ssl`, `ftplib`, `smtplib`, `aiohttp`, `boto3`, `botocore` or `s3transfer` entry; the two driver files `gold_refresh.py` and `publication_gold.py` carry no top-level import of those names. **What this does and does not show:** the 13 pinned distributions include no HTTP client; boto3 is not pinned because the Lambda base image supplies it, and the S3 reads and puts go through it. The closure output lists repo modules and third-party distributions, NOT the standard library, so it cannot show a standard-library `urllib` or `http.client` call, and I did not read the lazy imports or the builder functions line by line. I therefore do not claim "S3 only".

## (c) A rebuild on the current base image

NOT MEASURED. The build is by digest, so a rebuild is a new digest and a new addendum; I have not pulled the current `public.ecr.aws/lambda/python:3.12` manifest or scanned it.

## Reading, for the enabling addendum

The finding set is the Amazon Linux layer of the AWS-published Lambda Python base image: curl, openssl, rpm, pcre2, libxml2, krb5. The task has no inbound path (part 1), runs the 13 pinned distributions plus boto3, and has an IAM role that can write only under three prefixes and delete nothing. The open question for the schedule is whether the daily task contacts any host beyond AWS: unmeasured. Before the enabling addendum, either read the standard-library network calls of the driver's builders (a bounded read of three build functions) or rebuild on the current base and accept the new digest. Row `AMGT_HARVST-D1-S69` stays `UNDER_INVESTIGATION` until then.
