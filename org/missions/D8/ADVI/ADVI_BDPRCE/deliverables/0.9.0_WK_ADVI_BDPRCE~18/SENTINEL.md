# BP-c-6 -- the honest sentinel line, and the Monday/Tuesday header-only export

Record: `SENTINEL.json` (same folder). Read-only: nothing was run, invoked, written or edited on AWS or in the product tree. Downloads sit in `C:/dev/wk-bdprce-r3-18-data/`.

## 1. Is the honest line live, and did it hold?

Live. The deployed `bd-49f-runner` (LastModified 2026-10-07T00:50:44Z) carries the same bytes as the repo file at `3709ae40d6`: the zip's SHA-256 matches CodeSha256, and the extracted `lambda_function.py` has md5 968b33e2, the same as `git show 3709ae40d6`. The honest line is at lines 156-198: WARN at :168, a `head_object` read-back at :192-196, and OK at :198 printed only after the read-back.

It held on every run since the deploy. Seven run dates (2026-10-08 to 10-14) each print OK after the read-back, and each has its sentinel object in S3. Over the 14 run dates whose logs are readable (10-01 to 10-14), the literal count is 19 honest lines and 2 dishonest lines. The two dishonest lines are the pre-deploy runner's OK on 2026-10-05 and 10-06, when the sentinel was absent. Those two days are the ones behind the round-2 gaps.

The role's read is narrower than the commit message implied. The inline policy grants `s3:GetObject` on `bronze/*/_BRONZE_COMPLETE.json` only, not on `bronze/*`. That is enough, because the read-back reads that key, and the post-deploy RESULT lines show `sentinel: emitted`.

Log retention is 14 days. The oldest readable runner event is 2026-10-01T00:00:19Z, not the 09-30 recorded in round 2.

## 2. The Monday and Tuesday pattern

On all ten Monday and Tuesday run dates from 09-14 to 10-13, the first version of the transactions workbook is header-only (4354 to 4358 bytes). Eight of those dates have no sentinel. The two post-deploy dates, 10-12 and 10-13, do have one, so the round-2 list of six gaps is short by two (09-14 and 09-15 also have no sentinel, and bronze/2026-09-14 and 09-15 hold no objects at all).

The cause is the export window, not the vendor. The runner's newest transactions chunk is `[run_date-2, run_date]` (the shared module's `_chunk_windows`, enabled by `BD_TXN_CHUNK_DAYS=3`). The transactions table is not in the as-of lag set, so the end is the run date. A Monday run asks for Sat to Mon, and a Tuesday run asks for Sun to Tue. The log lines `txn chunk 1/5 [2026-10-10..2026-10-12]` and `[2026-10-11..2026-10-13]` show this directly.

The workbook's own Return Date column shows what BD had published. Neighbouring runs have their latest published day inside the span, so they return rows. The Sunday run's file is as of Friday 10-09, the Thursday file as of Tuesday 10-06, and the Wednesday 10-14 file as of Monday 10-12, with 2,804 Monday rows and no Tuesday rows. On a Tuesday, Monday is not yet published at 00:02Z: the Tuesday 10-13 file is header-only while its span holds Monday. Monday and Tuesday windows therefore miss the last published Friday. The Monday and Tuesday as-of values are inferred from these neighbours, not read directly.

Cause: `EXPORT_WINDOW_RULE`. Tuesday's trades do not reach Wednesday's workbook. They arrive in Thursday's, which fits the Thursday file's Tuesday rows.

## 3. The fix a later cell would make (named, not made)

Anchor the newest transactions chunk to the last published business day: extend the as-of lag at `cot_bronze_ingest.py:306` to the transactions table, or floor the newest chunk's start at that day. Then re-land and re-emit the ten Monday and Tuesday dates. Decide separately whether a measured-empty transactions export may complete a day: the runner's `EMPTY_WINDOW_OK_TABLES` (:118) currently accepts it, so the 10-12 and 10-13 sentinels exist over header-only transactions. Whether silver was built on that content is not read here.

## 4. What stays unknown

- The Monday and Tuesday as-of values are inferred, not read.
- For 09-14, 09-15, 09-21, 09-22, 09-28, 09-29, 10-05 and 10-06, the logs have expired or are unreadable for the cause, so the classification rests on S3 versions and the chunk windows.
- Why bronze has no objects for 09-14 and 09-15, and whether the sentinel existed on those dates, is not known.
- The IAM principal behind each run, and the date the narrow GetObject grant was added, were not read.
