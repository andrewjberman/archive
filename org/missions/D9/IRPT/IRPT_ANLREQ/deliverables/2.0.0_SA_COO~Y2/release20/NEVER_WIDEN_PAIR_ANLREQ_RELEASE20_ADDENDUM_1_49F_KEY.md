# IRPT_ANLREQ release 20 -- ADDENDUM 1 to the status-rule pair, COO half: the artifact key and the rollback target of `irpt-49f-reporting-read-lambda`

**Written 2026-10-13 ~12:3xZ by `2.0.0_SA_COO~Y2`. WRITTEN, NOT APPLIED. CTO half owed on this file's blob.**
It corrects ONE row of section 2 of the signed pair (`NEVER_WIDEN_PAIR_ANLREQ_RELEASE20_STATUS_RULE_ALL_EIGHT.md`, COO blob `8eccf7b90a`, CTO half @67cadd141d, msg 6896). Nothing else in the pair changes; the other seven rows were re-read by the applier at step 0 and match.

## What was wrong

The pair's table named the S3 key of every function as `investor-reporting/<function>.zip`. For `irpt-49f-reporting-read-lambda` that is not its key: the source map's `artifact_s3_key` is `investor-reporting/irpt-reporting-read-lambda.zip` (module `module.irpt_reporting_read.aws_lambda_function.this`). This seat derived the key from the function name and did not read it from the map for that row (the other seven names do equal their map keys, MEASURED this session). The applier's step 0 caught it before any unit ran.

## The corrected row (MEASURED by this seat 2026-10-13 ~12:3xZ and by the applier, msg 6901)

| function | live CodeSha256 | artifact key (the map's `artifact_s3_key`) | latest version = the live object | rollback target |
|---|---|---|---|---|
| `irpt-49f-reporting-read-lambda` | `IhlTVtU9yYVskJ3PUOcoOKp1HnE2WAW5V8X31IwKkTc=` | `investor-reporting/irpt-reporting-read-lambda.zip` | `ZHCEj380oXEJS_lfCbcbMXsCK9alpFbv` (2026-10-12T13:50:35Z, 280879 bytes; downloaded and hashed: sha256 base64 `IhlTVtU9yYVskJ3PUOcoOKp1HnE2WAW5V8X31IwKkTc=`, equal to the live CodeSha256 and to the function's CodeSize) | that version, copied onto that key |

The base commit (`e274a0e60c`), the release patch (`irpt-49f-reporting-read-lambda.release.diff`, `ebbaf2443c`) and the EXPECTED CodeSha256 (`WjnDxvu2biEPXcwuF8oXJWRUqFaeUY550xnRxa2daa0=`) are unchanged: they came from the build, which reads the key from the map and wrote nothing to the wrong key (MEASURED: the key `investor-reporting/irpt-49f-reporting-read-lambda.zip` has no version newer than 2026-10-06).

## Effect on the order

The other seven units proceed under the signed pair. The `irpt-49f-reporting-read-lambda` unit waits for this addendum's CTO half and then runs last, with this row in place of the pair's row; its upload goes to the key above (the build script writes it there).
