# What the guarded re-mint mode leaves behind when it fails part-way (CB-bs-3, round 71)

Everything here was shown by tests against a FAKED, versioned bucket (`data/assets/scripts/silver/tests/test_commonwealth_ard_remint.py`). The mode was never run against the real bucket and no AWS call was made. Machine-readable twin: `REMINT_FAILURE_PATHS.json` beside this page.

**Read this first.** The mode stops on the first failure, deletes nothing, rolls nothing back, and prints the keys it wrote. Its printed list is NOT a list of keys that changed: a day's two keys, the sidecar and the method row's two keys are put on the list BEFORE they are put. So when a put fails, the list names keys that never changed, and nothing says which half of a pair landed. A person holding a sign-off should work from the CAPTURE (the version ids it names) and a listing of the current version ids, not from the printed list alone. If the process is killed the mode prints nothing at all about what it wrote.

| Failure | What fails | Half a pair? | Described by the mode's own output? |
|---|---|---|---|
| F1 | a listed day's data.parquet put raises | no | no |
| F2 | the day's data.parquet lands, its manifest.json put raises | YES | no |
| F3 | a day lands whole and its data read-back hash differs | no | YES |
| F4 | a day lands whole and its manifest read-back check fails | no | YES |
| F4b | a day lands whole and its manifest read-back finds nothing | no | YES |
| F5a | second listed day: data.parquet put raises after the first day is whole | no | no |
| F5b | second listed day: data.parquet lands, manifest.json put raises | YES | no |
| F5c | second listed day: data read-back hash differs after the first day is whole | no | YES |
| F6a | the sidecar put raises after all listed days landed | no | no |
| F6b | the sidecar lands and its read-back sha256 differs | no | YES |
| F7a | the method row's data.parquet put raises after the days and the sidecar landed | no | no |
| F7b | the method row's data.parquet lands, its manifest.json put raises | YES | no |
| F7c | the method row lands and its data.parquet read-back does not match the producer's row | no | YES |
| F7d | the method row's manifest.json is stored wrong and nothing notices | no | no |
| F8 | the process is killed (or any exception the mode does not catch is raised) between two puts | YES (3 of 7 stop points) | no |
| F10 | a day's data.parquet put lands but S3's returned ETag does not verify | YES | no |
| F11 | a day lands whole and the read-back get itself raises | no | YES |
| F12 | emit_day returns landed False (a producer change; not reachable with the producer at this commit) | no | YES |
| F9 | a read (a get or a head) fails during the pre-write checks, before any put | no | YES (nothing changed, nothing named) |

`Described` is YES only when the mode's lines name EVERY key whose content changed AND name no key as written that was not. 'Half a pair' means a day's (or the method row's) data.parquet and manifest.json are at different generations.

## How to restore (every point below)

The sign-off names a capture: per listed date the ETag and version id of the served `data.parquet` and `manifest.json`, plus the sidecar and the method row when they differed. To restore a key, a person copies its captured version id back over the key (S3 CopyObject, source VersionId = the captured id). That makes a new latest version equal to the captured one and deletes nothing. The mode's help text: "DELETES NOTHING and does not roll back: the bucket keeps versions; rollback is a copy of the captured version id, done by a person under the sign-off". The capture names every key the mode can write.

## F1 -- a listed day's data.parquet put raises

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1290 -> data/assets/scripts/gold/irpt_reporting/account_return_daily.py:1886 (data.parquet put); caught by the except at data/assets/scripts/silver/commonwealth_account_return_daily.py:1303 (except (Exception, SystemExit)) and handed to _remint_failure (data/assets/scripts/silver/commonwealth_account_return_daily.py:1190-1196)
- **Printed:**
      ERROR: writing 2026-06-17 stopped: An error occurred (AccessDenied) when calling the PutObject operation: synthetic denial
      ERROR: nothing was deleted and no rollback was attempted; 2 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
- **Returns:** 1 (exit value)
- **Bucket holds:** date=2026-06-17/data.parquet old; date=2026-06-17/manifest.json old; date=2026-06-19/data.parquet old; date=2026-06-19/manifest.json old. No key changed.
- **Half a pair:** no. **Described by the output:** no -- The bucket is unchanged but both of the day's keys are printed WRITTEN. Over-naming: _remint_failure prints every key in `written` as 'WRITTEN', and remint_days appends a day's two keys at data/assets/scripts/silver/commonwealth_account_return_daily.py:1288 BEFORE emit_day puts either (the sidecar at :1309 and the method row's two keys at :1318 likewise before their puts). The second ERROR line says 'written or attempted', but no line says which of the named keys landed.
- **Restore:** Nothing changed, so there is nothing to restore; confirm with a listing of the versions of the keys named WRITTEN. 
- **Test:** `test_failure_F1_day_data_put_raises_and_nothing_lands`

## F2 -- the day's data.parquet lands, its manifest.json put raises

- **Where:** data/assets/scripts/gold/irpt_reporting/account_return_daily.py:1888 (the manifest put, after the data put at :1886); caught by the except at data/assets/scripts/silver/commonwealth_account_return_daily.py:1303 (except (Exception, SystemExit)) and handed to _remint_failure (data/assets/scripts/silver/commonwealth_account_return_daily.py:1190-1196)
- **Printed:**
      ERROR: writing 2026-06-17 stopped: An error occurred (AccessDenied) when calling the PutObject operation: synthetic denial
      ERROR: nothing was deleted and no rollback was attempted; 2 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json old; date=2026-06-19/data.parquet old; date=2026-06-19/manifest.json old. HALF A PAIR for date=2026-06-17: NEW data.parquet, OLD manifest.json.
- **Half a pair:** YES. **Described by the output:** no -- The data.parquet changed and is named; the manifest.json is named too and did not change; nothing says which half landed or that the day is half a pair. Over-naming: _remint_failure prints every key in `written` as 'WRITTEN', and remint_days appends a day's two keys at data/assets/scripts/silver/commonwealth_account_return_daily.py:1288 BEFORE emit_day puts either (the sidecar at :1309 and the method row's two keys at :1318 likewise before their puts). The second ERROR line says 'written or attempted', but no line says which of the named keys landed.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F2_day_manifest_put_raises_leaves_half_a_pair`

## F3 -- a day lands whole and its data read-back hash differs

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1293-1296
- **Printed:**
      ERROR: read-back of s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet does not match the new day file's content hash (2026-06-17)
      ERROR: nothing was deleted and no rollback was attempted; 2 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet old; date=2026-06-19/manifest.json old. The day is whole (both keys NEW) but its data.parquet holds content that is not the new build's; the second listed day is untouched.
- **Half a pair:** no. **Described by the output:** YES -- Both keys changed and both are named; the error names the failing key and the date. (A second-day variant, with the first day whole, is the existing test test_a_read_back_mismatch_exits_non_zero_and_prints_the_keys_already_written and F5c.)
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F3_day_data_read_back_hash_differs`

## F4 -- a day lands whole and its manifest read-back check fails

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1297-1302 (check_day_manifest)
- **Printed:**
      ERROR: the day manifest of 2026-06-17 read back failing method_version,valuation_source,fee_treatment,price_basis
      ERROR: nothing was deleted and no rollback was attempted; 2 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet old; date=2026-06-19/manifest.json old. The day is whole (both keys NEW) but its manifest.json fails the producer's field check.
- **Half a pair:** no. **Described by the output:** YES -- Both keys changed and both are named; the error names the failing fields.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F4_day_manifest_read_back_check_fails`

## F4b -- a day lands whole and its manifest read-back finds nothing

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1297-1299
- **Printed:**
      ERROR: read-back of s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json found nothing (2026-06-17)
      ERROR: nothing was deleted and no rollback was attempted; 2 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet old; date=2026-06-19/manifest.json old. The day is whole (both keys NEW).
- **Half a pair:** no. **Described by the output:** YES -- Both keys changed and both are named; the error names the manifest key.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F4b_day_manifest_read_back_finds_nothing`

## F5a -- second listed day: data.parquet put raises after the first day is whole

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1285-1304 (the loop), second pass; caught by the except at data/assets/scripts/silver/commonwealth_account_return_daily.py:1303 (except (Exception, SystemExit)) and handed to _remint_failure (data/assets/scripts/silver/commonwealth_account_return_daily.py:1190-1196)
- **Printed:**
      (Before the ERROR lines the mode has printed one 'REPLACED date=... rows=... content_sha256=... etag=... bytes=...' line per day that completed.) One REPLACED line for date=2026-06-17.
      ERROR: writing 2026-06-19 stopped: An error occurred (AccessDenied) when calling the PutObject operation: synthetic denial
      ERROR: nothing was deleted and no rollback was attempted; 4 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet old; date=2026-06-19/manifest.json old. No pair is half; the TABLE is half re-minted: date=2026-06-17 whole and NEW, date=2026-06-19 wholly OLD.
- **Half a pair:** no. **Described by the output:** no -- The four WRITTEN lines name the two day-1 keys that changed and the two day-2 keys that did not; nothing distinguishes them. Over-naming: _remint_failure prints every key in `written` as 'WRITTEN', and remint_days appends a day's two keys at data/assets/scripts/silver/commonwealth_account_return_daily.py:1288 BEFORE emit_day puts either (the sidecar at :1309 and the method row's two keys at :1318 likewise before their puts). The second ERROR line says 'written or attempted', but no line says which of the named keys landed.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F5a_second_day_data_put_raises_after_the_first_day_is_whole`

## F5b -- second listed day: data.parquet lands, manifest.json put raises

- **Where:** data/assets/scripts/gold/irpt_reporting/account_return_daily.py:1888 on the second pass; caught by the except at data/assets/scripts/silver/commonwealth_account_return_daily.py:1303 (except (Exception, SystemExit)) and handed to _remint_failure (data/assets/scripts/silver/commonwealth_account_return_daily.py:1190-1196)
- **Printed:**
      (Before the ERROR lines the mode has printed one 'REPLACED date=... rows=... content_sha256=... etag=... bytes=...' line per day that completed.) One REPLACED line for date=2026-06-17.
      ERROR: writing 2026-06-19 stopped: An error occurred (AccessDenied) when calling the PutObject operation: synthetic denial
      ERROR: nothing was deleted and no rollback was attempted; 4 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet NEW; date=2026-06-19/manifest.json old. HALF A PAIR for date=2026-06-19 (NEW data.parquet, OLD manifest.json); date=2026-06-17 is whole and NEW.
- **Half a pair:** YES. **Described by the output:** no -- Three keys changed, four are named, nothing says which; the half pair is not flagged. Over-naming: _remint_failure prints every key in `written` as 'WRITTEN', and remint_days appends a day's two keys at data/assets/scripts/silver/commonwealth_account_return_daily.py:1288 BEFORE emit_day puts either (the sidecar at :1309 and the method row's two keys at :1318 likewise before their puts). The second ERROR line says 'written or attempted', but no line says which of the named keys landed.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id; date=2026-06-19/data.parquet <- capture ['2026-06-19'].data.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F5b_second_day_manifest_put_raises_leaves_the_table_half_reminted_and_a_half_pair`

## F5c -- second listed day: data read-back hash differs after the first day is whole

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1293-1296 on the second pass
- **Printed:**
      (Before the ERROR lines the mode has printed one 'REPLACED date=... rows=... content_sha256=... etag=... bytes=...' line per day that completed.) One REPLACED line for date=2026-06-17.
      ERROR: read-back of s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/data.parquet does not match the new day file's content hash (2026-06-19)
      ERROR: nothing was deleted and no rollback was attempted; 4 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet NEW; date=2026-06-19/manifest.json NEW. Both days whole and NEW; date=2026-06-19's data.parquet holds content that is not the new build's.
- **Half a pair:** no. **Described by the output:** YES -- All four keys changed and all four are named; the error names the failing key. (Also exercised without bucket-state assertions by the existing test_a_read_back_mismatch_exits_non_zero_and_prints_the_keys_already_written.)
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id; date=2026-06-19/data.parquet <- capture ['2026-06-19'].data.version_id; date=2026-06-19/manifest.json <- capture ['2026-06-19'].manifest.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F5c_second_day_read_back_mismatch_after_the_first_day_is_whole`

## F6a -- the sidecar put raises after all listed days landed

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1311 (s3.put_object of the sidecar), caught at :1314
- **Printed:**
      Two REPLACED lines (one per day).
      ERROR: writing the sidecar stopped: An error occurred (AccessDenied) when calling the PutObject operation: synthetic denial
      ERROR: nothing was deleted and no rollback was attempted; 5 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily_blank_reasons/source_date=2026-06-23/ard_cottonwood_blank_reasons.parquet
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet NEW; date=2026-06-19/manifest.json NEW; sidecar old. No pair is half; both days are whole and NEW; the sidecar is OLD.
- **Half a pair:** no. **Described by the output:** no -- The sidecar is printed WRITTEN (appended at :1309 before its put) and did not change. Over-naming: _remint_failure prints every key in `written` as 'WRITTEN', and remint_days appends a day's two keys at data/assets/scripts/silver/commonwealth_account_return_daily.py:1288 BEFORE emit_day puts either (the sidecar at :1309 and the method row's two keys at :1318 likewise before their puts). The second ERROR line says 'written or attempted', but no line says which of the named keys landed.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id; date=2026-06-19/data.parquet <- capture ['2026-06-19'].data.version_id; date=2026-06-19/manifest.json <- capture ['2026-06-19'].manifest.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). The sidecar is in the capture only because the mode refuses to start when the served sidecar differs from the new build's and the capture does not name it (data/assets/scripts/silver/commonwealth_account_return_daily.py:1266-1267); when it does not differ the mode does not write it, so it cannot be touched.
- **Test:** `test_failure_F6a_sidecar_put_raises_after_all_days_landed`

## F6b -- the sidecar lands and its read-back sha256 differs

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1312-1313
- **Printed:**
      Two REPLACED lines (one per day).
      ERROR: read-back of the sidecar s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily_blank_reasons/source_date=2026-06-23/ard_cottonwood_blank_reasons.parquet does not match reasons_sidecar.sha256
      ERROR: nothing was deleted and no rollback was attempted; 5 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily_blank_reasons/source_date=2026-06-23/ard_cottonwood_blank_reasons.parquet
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet NEW; date=2026-06-19/manifest.json NEW; sidecar NEW. Both days whole and NEW; the sidecar is NEW but holds content that is not the new build's.
- **Half a pair:** no. **Described by the output:** YES -- All five keys changed and all five are named; the error names the sidecar key.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id; date=2026-06-19/data.parquet <- capture ['2026-06-19'].data.version_id; date=2026-06-19/manifest.json <- capture ['2026-06-19'].manifest.version_id; sidecar <- capture ['sidecar'].version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F6b_sidecar_read_back_mismatch`

## F7a -- the method row's data.parquet put raises after the days and the sidecar landed

- **Where:** data/assets/scripts/gold/irpt_reporting/account_return_daily.py:2072 (data.parquet put) via data/assets/scripts/silver/commonwealth_account_return_daily.py:1320; caught at :1326
- **Printed:**
      Two REPLACED lines (one per day) and one REPLACED sidecar line.
      ERROR: writing the method row stopped: An error occurred (AccessDenied) when calling the PutObject operation: synthetic denial
      ERROR: nothing was deleted and no rollback was attempted; 7 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily_blank_reasons/source_date=2026-06-23/ard_cottonwood_blank_reasons.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet NEW; date=2026-06-19/manifest.json NEW; sidecar NEW; method_row/data.parquet old; method_row/manifest.json old. No pair is half; days and sidecar are NEW; the method row (both keys) is OLD.
- **Half a pair:** no. **Described by the output:** no -- The two method-row keys are printed WRITTEN and neither changed. Over-naming: _remint_failure prints every key in `written` as 'WRITTEN', and remint_days appends a day's two keys at data/assets/scripts/silver/commonwealth_account_return_daily.py:1288 BEFORE emit_day puts either (the sidecar at :1309 and the method row's two keys at :1318 likewise before their puts). The second ERROR line says 'written or attempted', but no line says which of the named keys landed.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id; date=2026-06-19/data.parquet <- capture ['2026-06-19'].data.version_id; date=2026-06-19/manifest.json <- capture ['2026-06-19'].manifest.version_id; sidecar <- capture ['sidecar'].version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). Day keys, sidecar and method row are in the capture when they differ (the mode refuses to start otherwise: data/assets/scripts/silver/commonwealth_account_return_daily.py:1276-1277).
- **Test:** `test_failure_F7a_method_row_data_put_raises_after_the_days_and_the_sidecar_landed`

## F7b -- the method row's data.parquet lands, its manifest.json put raises

- **Where:** data/assets/scripts/gold/irpt_reporting/account_return_daily.py:2073 (manifest put, after the data put at :2072) via data/assets/scripts/silver/commonwealth_account_return_daily.py:1320; caught at :1326
- **Printed:**
      Two REPLACED lines (one per day) and one REPLACED sidecar line.
      ERROR: writing the method row stopped: An error occurred (AccessDenied) when calling the PutObject operation: synthetic denial
      ERROR: nothing was deleted and no rollback was attempted; 7 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily_blank_reasons/source_date=2026-06-23/ard_cottonwood_blank_reasons.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet NEW; date=2026-06-19/manifest.json NEW; sidecar NEW; method_row/data.parquet NEW; method_row/manifest.json old. THE METHOD ROW IS HALF A PAIR: NEW data.parquet, OLD manifest.json. Days and sidecar NEW.
- **Half a pair:** YES. **Described by the output:** no -- Six keys changed, seven are named, nothing says the method row's manifest.json is the one that did not change; the half pair is not flagged. Over-naming: _remint_failure prints every key in `written` as 'WRITTEN', and remint_days appends a day's two keys at data/assets/scripts/silver/commonwealth_account_return_daily.py:1288 BEFORE emit_day puts either (the sidecar at :1309 and the method row's two keys at :1318 likewise before their puts). The second ERROR line says 'written or attempted', but no line says which of the named keys landed.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id; date=2026-06-19/data.parquet <- capture ['2026-06-19'].data.version_id; date=2026-06-19/manifest.json <- capture ['2026-06-19'].manifest.version_id; sidecar <- capture ['sidecar'].version_id; method_row/data.parquet <- capture ['method_row'].data.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F7b_method_row_manifest_put_raises_leaves_the_method_row_half_a_pair`

## F7c -- the method row lands and its data.parquet read-back does not match the producer's row

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1323-1325
- **Printed:**
      Two REPLACED lines (one per day) and one REPLACED sidecar line.
      ERROR: read-back of the method row s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3/data.parquet does not match the producer's row
      ERROR: nothing was deleted and no rollback was attempted; 7 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-19/manifest.json
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily_blank_reasons/source_date=2026-06-23/ard_cottonwood_blank_reasons.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet NEW; date=2026-06-19/manifest.json NEW; sidecar NEW; method_row/data.parquet NEW; method_row/manifest.json NEW. Everything NEW (days, sidecar, both method-row keys); the method row's data.parquet holds content that is not the producer's row.
- **Half a pair:** no. **Described by the output:** YES -- All seven keys changed and all seven are named; the error names the failing key.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id; date=2026-06-19/data.parquet <- capture ['2026-06-19'].data.version_id; date=2026-06-19/manifest.json <- capture ['2026-06-19'].manifest.version_id; sidecar <- capture ['sidecar'].version_id; method_row/data.parquet <- capture ['method_row'].data.version_id; method_row/manifest.json <- capture ['method_row'].manifest.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F7c_method_row_read_back_mismatch`

## F7d -- the method row's manifest.json is stored wrong and nothing notices

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1323 reads back the method row's data.parquet only
- **Printed:**
      REPLACED lines for both days, the sidecar and the method row, then: ARD-COTTONWOOD-REMINT listed=2 replaced=2 unlisted_differing=0 sidecar=replaced method_row=replaced
- **Returns:** 0 (success)
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet NEW; date=2026-06-19/manifest.json NEW; sidecar NEW; method_row/data.parquet NEW; method_row/manifest.json NEW. Everything NEW; the method row's manifest.json holds content that is not what was put.
- **Half a pair:** no. **Described by the output:** no -- The mode reports success for a run that left a wrong method-row manifest.json: the output describes a state that is not the state. Not a stop; recorded here because the read-back that exists elsewhere (days, sidecar) is absent for this key.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id; date=2026-06-19/data.parquet <- capture ['2026-06-19'].data.version_id; date=2026-06-19/manifest.json <- capture ['2026-06-19'].manifest.version_id; sidecar <- capture ['sidecar'].version_id; method_row/data.parquet <- capture ['method_row'].data.version_id; method_row/manifest.json <- capture ['method_row'].manifest.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F7d_a_method_row_manifest_that_is_stored_wrong_is_never_seen`

## F8 -- the process is killed (or any exception the mode does not catch is raised) between two puts

- **Where:** No handler: remint_days catches (Exception, SystemExit) at :1303/:1314/:1326, so a BaseException (KeyboardInterrupt, a kill) propagates; `written` is lost with the frame
- **Printed:**
      NOTHING about the keys written: no ERROR line, no WRITTEN line, no line saying the run stopped. Only the REPLACED line(s) of the day(s) / sidecar that had completed (none at n=1,2; one at n=3,4; two at n=5; two and the sidecar at n=6,7).
- **Returns:** No return value: the exception (here a BaseException subclass) propagates out of main; a real kill leaves a non-zero shell status and no Python-level information
- **Bucket holds:** date=2026-06-17/data.parquet old; date=2026-06-17/manifest.json old; date=2026-06-19/data.parquet old; date=2026-06-19/manifest.json old; sidecar old; method_row/data.parquet old; method_row/manifest.json old. Depends on where it stops, shown by seven cases (n = the put that did not happen): n=1 nothing changed; n=2 date=2026-06-17 HALF A PAIR (NEW data.parquet, OLD manifest.json); n=3 day 1 whole; n=4 day 1 whole + date=2026-06-19 HALF A PAIR; n=5 both days whole; n=6 both days + sidecar; n=7 the METHOD ROW HALF A PAIR (and everything else NEW). Half a pair in 3 of the 7 cases (n=2, 4, 7).
- **Half a pair:** YES. **Described by the output:** no -- The bucket holds up to six new keys and the mode's output names none of them. The person works from the capture plus a listing of versions of the table's keys, never from the mode's output.
- **Restore:** Nothing changed, so there is nothing to restore; confirm with a listing of the versions of the keys named WRITTEN. Because the output names nothing, the person must compare the CURRENT version id of every key in the capture (each listed date's data and manifest, the sidecar, the method row's two keys) with the captured one and restore every key that differs; the capture names all seven keys of a run that replaces everything (the restore of all seven is asserted in the F7c test).
- **What the test shows:** The put list and the bucket's version ids at the moment an exception the mode does NOT catch is raised by the nth put, and that no line names a written key. **What it cannot show:** A real process kill: no OS signal, no half-finished put (S3 makes one put whole-or-absent; a kill during a put is not modelled), no state of local temp files.
- **Test:** `test_failure_F8_a_process_killed_before_the_nth_put_prints_nothing_about_the_keys_written`

## F10 -- a day's data.parquet put lands but S3's returned ETag does not verify

- **Where:** lib/stream_parquet.py:136-148 (ChunkedParquetWriter.finalize raises StreamWriteUnverified AFTER the put) via data/assets/scripts/gold/irpt_reporting/account_return_daily.py:1886; caught by the except at data/assets/scripts/silver/commonwealth_account_return_daily.py:1303 (except (Exception, SystemExit)) and handed to _remint_failure (data/assets/scripts/silver/commonwealth_account_return_daily.py:1190-1196)
- **Printed:**
      ERROR: writing 2026-06-17 stopped: <key>/data.parquet: S3 ETag '<md5>' != local MD5 '<md5>' (<n> bytes) -- the write is NOT trusted
      ERROR: nothing was deleted and no rollback was attempted; 2 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json old; date=2026-06-19/data.parquet old; date=2026-06-19/manifest.json old. HALF A PAIR for date=2026-06-17: NEW data.parquet (the object the error calls 'NOT trusted'), OLD manifest.json (emit_day never reached its manifest put).
- **Half a pair:** YES. **Described by the output:** no -- The data.parquet landed and is named, the manifest.json is named and did not change; nothing says which, and nothing flags the half pair. The error text says the write is not trusted but the mode names the key WRITTEN like the others. (The F10 test asserts the printed lines and the bucket's state; its restore assertion is the same capture field F3 shows.)
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F10_data_put_lands_but_its_etag_does_not_verify_leaves_half_a_pair`

## F11 -- a day lands whole and the read-back get itself raises

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1293 (_read_key re-raises any non-absent ClientError), caught at :1303
- **Printed:**
      ERROR: writing 2026-06-17 stopped: An error occurred (InternalError) when calling the GetObject operation: synthetic read failure
      ERROR: nothing was deleted and no rollback was attempted; 2 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet old; date=2026-06-19/manifest.json old. The day is whole (both keys NEW); its content was never checked.
- **Half a pair:** no. **Described by the output:** YES -- Both keys changed and both are named; the error says the write stopped and carries the read error.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F11_read_back_get_raises_after_the_day_landed_whole`

## F12 -- emit_day returns landed False (a producer change; not reachable with the producer at this commit)

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1291-1292
- **Printed:**
      ERROR: emit_day returned {'address': 's3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17', 'landed': False} for 2026-06-17
      ERROR: nothing was deleted and no rollback was attempted; 2 key(s) were written or attempted before this stopped (roll back from the capture, by a person under the sign-off):
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/data.parquet
      WRITTEN s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-17/manifest.json
- **Returns:** 1
- **Bucket holds:** date=2026-06-17/data.parquet NEW; date=2026-06-17/manifest.json NEW; date=2026-06-19/data.parquet old; date=2026-06-19/manifest.json old. The test's wrapper does the real writes and flips the flag, the worst case: the day is whole (both keys NEW).
- **Half a pair:** no. **Described by the output:** YES -- Both keys changed and both are named. At this commit emit_day returns landed True whenever upload=True (data/assets/scripts/gold/irpt_reporting/account_return_daily.py:1890), so the branch is defensive.
- **Restore:** A person, under the sign-off, copies the captured version id back over each key that changed: date=2026-06-17/data.parquet <- capture ['2026-06-17'].data.version_id; date=2026-06-17/manifest.json <- capture ['2026-06-17'].manifest.version_id. The capture names every one of these keys (asserted by the point's test, F8 and F10 excepted, whose keys are the same keys that the F7c and F3 tests assert: each captured id is the id the key had before the run and is still a version of the key). 
- **Test:** `test_failure_F12_emit_day_returning_landed_false_stops_with_the_day_written`

## F9 -- a read (a get or a head) fails during the pre-write checks, before any put

- **Where:** data/assets/scripts/silver/commonwealth_account_return_daily.py:1243-1247 (heads against the capture), :1248-1255 (served-day reads, the unlisted ones in a 16-thread pool), :1261 (sidecar get), :1270 (method-row get); none is inside a try, and _read_key/_head_key re-raise any error that is not an absent-key code (:1008-1015, :1115-1123)
- **Printed:** Only the bond-check line ('ARD-COTTONWOOD-BOND-CHECK days=5 rows=10 measured_rows=10 measured_rows_on_bond_days=0 fixed_income_cusips=0'), printed before the first read of the bucket and saying nothing about it. No REFUSED, no ERROR, no WRITTEN: nothing was written, so nothing is named.
- **Returns:** The ClientError propagates out of main as an exception (a Python traceback), not an exit value and not a REFUSED line. A read that finds the key ABSENT (NoSuchKey/404) is different: it is a REFUSED exit, covered by the existing refusal tests.
- **Bucket holds:** UNCHANGED, every key keeps its version id (asserted from the fake's before/after version ids), put list empty, no put even attempted, nothing deleted
- **Restore:** Nothing to restore: no key changed. Re-run after the read error is understood.
- **Test:** `test_failure_F9_a_read_that_fails_before_any_put_leaves_nothing (4 cases)`

## Not established

- Behaviour against the real bucket: no AWS call was made. That the bucket is versioned, that the captured version ids exist there, and that a CopyObject of a captured VersionId restores the key byte for byte were not exercised (the fake keeps every version; the real bucket's versioning state is the sign-off's to confirm).
- A real process kill, an OS signal, or a kill DURING a put: F8 is the state when an uncaught BaseException is raised by the nth put (puts 1..n-1 landed). S3 makes a single put whole-or-absent; this is a statement about S3, not something the tests show.
- A put that is retried by the SDK or that stores and then times out: F10 is the stored-then-raise case through the writer's ETag check; other timing shapes are not modelled.
- A second writer to the table during the run: the mode compares the capture with the served heads once, before the writes; a write by anything else between that check and the puts is not detected and not tested.
- Local leftovers after a kill (stream_parquet temp files under the system temp directory).
- A malformed manifest.json on read-back (json.loads raising inside the try) is caught by the same handler as F4/F11 and prints 'writing <date> stopped: ...'; not given its own test.
- The order in which a person restores the keys of a half pair: the restore itself passes through states in which a pair is half; not examined.
- Whether the data that a restore returns is the data the served table showed at the capture: the capture holds ETag and version id, and the mode checks both at the start; the content behind the version id was not re-read.
