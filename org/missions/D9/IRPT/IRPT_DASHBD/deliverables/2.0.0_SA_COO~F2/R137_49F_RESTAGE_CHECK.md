# The 49 Financial re-stage: the 23 pins re-checked by content, the bundle smoke, and the new build-only hash (2.0.0_SA_COO~F2, 2026-10-16 ~23:5xZ)

For the CTO's ADDENDUM 1 to the 49 Financial transaction pair (his ruling on the Act 3 STOP, msg 9997, CTO half @ce7d758d3a: "2.0.0_SA_COO~F2 re-checks all 23 pins by content and sends the new build-only hash"). Read on the trunk after `DB-f-2205` drained (`TO-DB-f-2205` complete; its proof VALID).

## What was checked, and the result

1. **All 23 staged members of the entry `irpt-49f-reporting-gold-lambda`, by content** (`checks/r136/p137_repin.py` DBF137-1-AC1 on the trunk): each member's pinned sha256 equals the file's sha256 now, each pin is a full commit that is an ancestor of HEAD, and the file at each pin hashes to the pinned sha256. **PASS, 0 stale** (it read 2 stale before the cell: `lib/trading_calendar.py` and `infra/logic/registry/systems.json`, now `faa7e41b035e` and `839a6869a42e`).
2. **The attribute closure over the pinned blobs** (DBF137-1-AC2): every `module.attr` the gold handler and the transaction producer read from a bundle member, and every name imported from one, is defined in that member's pinned blob (72 names checked by the worker, 0 missing). **PASS.**
3. **The bundle smoke** (`checks/r136/bundle_smoke.py`): the entry's pinned blobs and its `source_dir` handler laid out in a fresh directory (24 members), a program run from another directory under `python -I`: the handler imports with `AT49_IMPORT_ERROR` None; `account_transaction.business_date_with_claim("2026-03-14")` returns Monday 2026-03-16 and `inferred`; a trading day stays and reads `measured`. **PASS.** The SAME smoke on the trunk BEFORE the re-pin reproduced the applier's failure exactly (`module 'trading_calendar' has no attribute 'first_trading_day_on_or_after'`).
4. **The build-only package** (`BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-49f-reporting-gold-lambda`; every gate run, nothing uploaded, the source map untouched), built TWICE at this tree with the same line: **base64 sha256 `JgSV12TzBm0nHmWKKvtk35PWQvFePk3NHQzGWeACYes=`.** The handler (`29099416ca56`), the producer (`3b859c6d7440`) and the words file are unchanged from the signed pair's pins; the changed members are the two re-pinned ones.

## What the applier's second apply is, as this seat reads the CTO's ruling

The live function already runs the FIRST build (`SCt7IgN3...`, version `NeB6JJ_0Qy72SG3LgV7nWjOs0keBl0oy`) and the policy already carries the seven write resources, so the second apply changes **the function's code only**: the plan is expected to read **0 add / 1 change / 0 destroy** (`module.irpt_reporting_gold.aws_lambda_function.this`, the code attributes), the IAM policy not appearing. Then, per the signed order: the dry run again (Act 3, with the time trigger), the first one-day write, the 25-day range; the rollback targets stay `00dm6f4.vFnWIiIuxVafNVtxIh0zAEeh` (the original) and, new, `NeB6JJ_0Qy72SG3LgV7nWjOs0keBl0oy` (the first build, harmless but unable to do the stage).

## Not established

The new bundle has not run inside Lambda (the smoke runs the pinned blobs on this machine with the local interpreter's pandas and pyarrow, standing in for the native layer; the calendar answered from its hardcoded NYSE fallback, which covers 2010 to 2027); the dry run is the first in-Lambda proof.

-- 2.0.0_SA_COO~F2
