# BP-a-1 -- who writes the served T-1 price (read-only census)

Record: `WRITERS.json` (grader rc=0, writers=6, unidentified=0, versions_read=665). Per-version mapping: `WRITERS_VERSIONS.tsv` (72 in-window versions, 0 unidentified). Reads run 2026-10-13 from 13:17Z; no write verb, no Lambda run, no producer run.

## The writers (opal-data-bd, silver/prices/canonical_prices.parquet and the daily keys)

| # | Writer | Where it runs | Runs 7d | Put lines (repo) | Rule copy (SOURCE_RANK / median) | Claim |
|---|---|---|---|---|---|---|
| 1 | `lambda:bd-price-update` | Lambda, invoked daily by bd-silver-merge (~00:15-00:24Z) | 7 | canonical :441, daily :498 | `infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py:60-65` (no scoped_override key); median :202 | inferred |
| 2 | `build_canonical_prices_v2.py` as S_00 | gold runner EC2 i-01003b035d2988dfb, ~04:01, ~09:4x, ~12:4x, ~23:0x | 25 | :660 (upload_file) | none in file; 4-tier rule :394-458; T1 median :239 | inferred |
| 3 | `inject_scoped_overrides.py` (auto-chained by S_00) | same runs, 15-16 s after row 2 | 25 | :253 | none; overrides imported from bd_price_update.py:80 | inferred |
| 4 | `silver/bd_price_update.py` | not run in window (code on S3 matches repo) | 0 | canonical :609, daily :666 (key :639) | `data/black_diamond/scripts/silver/bd_price_update.py:65-71` (scoped_override -2, yahoo -1); median :344 | absent |

Rule copies: two rank tables. The Lambda (row 1) has no `scoped_override` and ranks yahoo 1; the silver script (row 4) ranks scoped -2 and yahoo -1. The S_00 path (row 2) has no rank table at all: it is yahoo-first when a Yahoo series exists. Deployed bytes equal the repo for the Lambda zip (md5), and for the S3 copies of rows 2, 3 and 4 (ETag = md5).

## The pairs

Each 15-16 s pair is ONE S_00 run. The build puts the table (:660), then auto-chains inject, which puts it again (:253). The S_00 telemetry windows cover both puts: 10-13 04:01:22-04:03:44Z, 10-13 12:45:52-12:48:08Z, 10-12 00:18:44-00:21:03Z. The second put is the larger object. The single 00:15-00:24Z versions are the Lambda (row 1) and have no pair.

## Served 49F home

`opal-data-49financial`: no object key contains `price`, `canonical_prices` or `silver/` (0 matches over the whole bucket). Neither price object, nor a copy, is written there. Partial read: 9 of 86 chain `_code` objects.

## Unidentified

None by time: all 72 in-window versions match a known run (14 Lambda, 58 S_00/inject). The fourth writer named in the brief is row 2 (S_00), and the "emergency rebuild" is a daily stage.

## What stays open, and the read that closes it

1. **Trigger of the 09:4x and 12:4x S_00 runs.** Not attributed: no SSM command, Lambda REPORT or StartInstances in the reads above matches those minutes. Read the runner host's systemd/boot path and the SSM session history for those minutes.
2. **Principal per version.** Time match only (no request id on a version). Read the `opal-served-key-write-trail` log files for PutObject on `silver/prices/canonical_prices.parquet` to bind each version to its principal (claim to measured).
3. **Host copy of inject.** The subprocess ran a host copy; only the S3 copy was checked. Read the host file (SSM) and compare the md5.
4. **Effect of the Lambda rank copy on scoped rows.** The Lambda copy has no scoped_override rank; the 00:15 version is 4.3 MB smaller than the 04:03 rebuild. Compare the scoped rows for one overridden asset at 00:15 and at 04:03 on 10-13.
