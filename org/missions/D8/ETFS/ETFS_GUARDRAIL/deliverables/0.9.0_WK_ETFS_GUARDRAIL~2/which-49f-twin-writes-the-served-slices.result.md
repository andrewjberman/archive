# EG-s-11 result -- which bd-49f twin writes the served slices

**TO:** `ETFS_GUARDRAIL.TO-EG-s-11` | **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~2` | **Method:** live AWS reads only (no invoke, no write) + the served objects. NEVER#1: only `opal-data-etfs` (aggregation bucket) is read; no `opal-data-assets/schwab/*` or any firm bucket.

---

## 1. S11-AC1 -- the first twin is LIVE, output prefix is the served prefix

**Invocation:** `.tools/aws lambda get-function-configuration --function-name bd-49f-etf-ownership-daily --query "[FunctionName,LastModified,Environment.Variables.OUTPUT_PREFIX]" --output text`

**Output (verbatim):**
```
bd-49f-etf-ownership-daily	2026-07-29T01:46:07.000+0000	daily/49financial/
```
rc=0. Denominator: 1 of 1 named function read, 1 of 1 matches `daily/49financial/`. **PASS.**

---

## 2. S11-AC2 -- the canonical twin's live existence, read either way

**Invocation:** `.tools/aws lambda get-function-configuration --function-name bd-49f-etf-ownership-daily-canonical --query FunctionName --output text; echo rc=$?`

**Output (verbatim):**
```
An error occurred (ResourceNotFoundException) when calling the GetFunctionConfiguration operation: Function not found: arn:aws:lambda:us-east-1:313476888478:function:bd-49f-etf-ownership-daily-canonical
rc=255
```
rc=255 (non-zero, matching the amended-answer expectation). **NOT DEPLOYED** -- matches the dir header's own claim ("NOT YET DEPLOYED: the source is frozen (06-18)"). Denominator: 1 of 1 named function read, answer determinate (absent). **PASS.**

---

## 3. The census script (`twin_writer_census.py`), full run

**Invocation:** `python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~2/twin_writer_census.py`

**Output (verbatim, rc=0):**
```
WINDOW: last 3 days, start=2026-09-01T23:05:31.861460+00:00 (1788303931861 ms) end=now (2026-09-04T23:05:31.861460+00:00)
STEP1: list-functions prefix='bd-49f-etf-ownership' -- 5 page(s) scanned, 1 match(es): bd-49f-etf-ownership-daily
CONFIG bd-49f-etf-ownership-daily: LastModified=2026-07-29T01:46:07.000+0000 CodeSha256=jw2IoJeF4fOFtb9J+aU2t97Ea65l5M4qp/YCueZ3Llk= OUTPUT_PREFIX=daily/49financial/
RULES for arn:aws:lambda:us-east-1:313476888478:function:bd-49f-etf-ownership-daily: bd-49f-etf-ownership-scheduled-floor
LOGS bd-49f-etf-ownership-daily: 4 page(s) followed (manual nextToken), 3 'OK: wrote' event(s) in the 3-day window
  LOGEVT bd-49f-etf-ownership-daily 1788345911186 OK: wrote s3://opal-data-etfs/daily/49financial/2026-09-01.json (4 ETF slices, total_ownership=550288747.44, source_as_of=2026-09-01, generated_at=2026-09-02T10
  LOGEVT bd-49f-etf-ownership-daily 1788432311925 OK: wrote s3://opal-data-etfs/daily/49financial/2026-09-02.json (4 ETF slices, total_ownership=553430821.07, source_as_of=2026-09-02, generated_at=2026-09-03T10
  LOGEVT bd-49f-etf-ownership-daily 1788518711493 OK: wrote s3://opal-data-etfs/daily/49financial/2026-09-03.json (4 ETF slices, total_ownership=556753306.81, source_as_of=2026-09-03, generated_at=2026-09-04T10
CONFIG bd-49f-etf-ownership-daily-canonical: NOT LIVE (ResourceNotFoundException)
STEP3: s3 list-objects-v2 s3://opal-data-etfs/daily/49financial/ -- 1 page(s), 87 object(s) total, 3 newest shown
SLICE daily/49financial/2026-09-01.json LastModified=2026-09-02 10:45:12+00:00 source_artifact=s3://opal-data-assets/schwab/08242234/silver/fact_rps/date=2026-09-01/data.parquet source_as_of=2026-09-01
SLICE daily/49financial/2026-09-02.json LastModified=2026-09-03 10:45:12+00:00 source_artifact=s3://opal-data-assets/schwab/08242234/silver/fact_rps/date=2026-09-02/data.parquet source_as_of=2026-09-02
SLICE daily/49financial/2026-09-03.json LastModified=2026-09-04 10:45:12+00:00 source_artifact=s3://opal-data-assets/schwab/08242234/silver/fact_rps/date=2026-09-03/data.parquet source_as_of=2026-09-03
WRITER=bd-49f-etf-ownership-daily EVIDENCE=3
TWIN=bd-49f-etf-ownership-daily LIVE=True SCHEDULED=bd-49f-etf-ownership-scheduled-floor LAST_WROTE=2026-09-04T10:45:11.493000+00:00
TWIN=bd-49f-etf-ownership-daily-canonical LIVE=False SCHEDULED=(none) LAST_WROTE=none
```
**Denominators:** list-functions 5 pages scanned / 1 match; per-twin config reads 2 of 2 named twins; EventBridge rules 1 of 1 live function checked; CloudWatch log pages 4 followed (manually, see s.5) / 3 matching events found within the 3-day window; S3 list 1 page / 87 objects total / 3 newest shown, all 3 downloaded and parsed for `source_artifact`/`source_as_of`.

**Determinism control:** re-run in full a second time; the three decision lines (`WRITER=...`, `TWIN=bd-49f-etf-ownership-daily ...`, `TWIN=bd-49f-etf-ownership-daily-canonical ...`) are byte-identical across both runs.

**Mutant control:** the match-tolerance constant (5 minutes / 300 seconds, the discriminator between "this log line explains this served object" and coincidence) was shrunk to 0.001s in a throwaway scratch copy (`.scratch/census_mutant.py`, never the committed script). Result: `WRITER=UNDETERMINED REASON=no live function's 'OK: wrote' log line names a served key within 5 minutes of that object's LastModified` -- the determination flips exactly as expected when the discriminating window is broken, confirming the check is not vacuously true. Scratch file deleted after the control.

**S11-AC3 verdict:** the census ran and printed its determination line, `WRITER=bd-49f-etf-ownership-daily EVIDENCE=3` -- **this confirms `EG-s-2`'s address** (the criterion's own bar: `WRITER=bd-49f-etf-ownership-daily` needs no BLOCKING row; only `-canonical` or `UNDETERMINED` would). **PASS.**

---

## 4. S11-AC4 -- newest served September slice

**Invocation:** `.tools/aws s3api list-objects-v2 --bucket opal-data-etfs --prefix daily/49financial/2026-09 --query "Contents[-1].[Key,LastModified]" --output text`

**Output (verbatim):**
```
daily/49financial/2026-09-03.json	2026-09-04T10:45:12.000Z
```
rc=0. Denominator: 1 of 1 prefix queried, 1 newest object named. This is the same object the census script's S3 step already confirmed. **PASS.**

---

## 5. The pagination trap the TO's own literal invocation walks into (filed as `ETFS_GUARDRAIL-W2-S3`)

The deliverable's prescribed shape (`logs filter-log-events --start-time <epoch ms> --filter-pattern "OK: wrote" --limit 20`), run as a SINGLE un-paginated call, returns exactly **ONE** matching event with a `nextToken` present -- not the three that actually exist in the 3-day window. `filter-log-events` does not auto-paginate the way `list_objects_v2`/`list_functions` do under the `.tools/aws` CLI v1 shim: each internal response page can return fewer matches than `--limit` asks for while still carrying a `nextToken`, and a caller who stops at the first page under-reports coverage without any error. Confirmed by manually following the token: page 1 -> 1 event (09-02 stream), page 2 -> 1 event (09-03 stream), page 3 -> 1 event (09-04 stream), page 4 -> 0 events, no token (true end). `twin_writer_census.py` follows the token to the true end (bounded at 20 pages) rather than trusting page 1; the `EVIDENCE=3` in `WRITER=bd-49f-etf-ownership-daily EVIDENCE=3` is the full 3-day count, not the 1-event page-1 undercount a literal single-call reading of the TO's invocation would have produced. This does not change the WRITER determination (even 1 of 3 matching lines identifies the same function), but it would have understated the EVIDENCE count and, in a sparser window, could have missed the only matching event entirely.

---

## 6. Consequence for `EG-s-2` (the next-but-one order in this worker's queue)

`EG-s-2` is cut against `bd-49f-etf-ownership-daily` as the writer to port the reporting-obligation catch-up window into. This census confirms that premise on the APPLIED plane, both ends: the function side (live, scheduled, `OUTPUT_PREFIX=daily/49financial/`) and the object side (3 of 3 newest served slices in the window carry a `generated_at`/log timestamp matching this function's own `OK: wrote` lines, within the 5-minute tolerance). The `-canonical` twin is confirmed NOT LIVE (`ResourceNotFoundException`) and wrote nothing in the window -- **`EG-s-2` needs no premise correction and no BLOCKING row on this account.** The DESIRED plane (Terraform + source map) and the APPLIED plane (live function + served objects) AGREE here; no drift is stated because none was found.
