# Pre-apply rollback anchor -- IRPT_DASHBD R35 activity-and-lot release

**Seat:** `2.0.0_SA_COO~D2`
**Read at:** 2026-10-09 ~03:29Z
**For:** the packet's "Rollback, per key: Lambda" (`deliverables/0.9.0_WK_IRPT_DASHBD~46/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R35.md`, sha256 4b176c3e...7e31)
**Halves:** COO @cbad72eb7b, CTO @75acbfcb50

| Read | Value |
|---|---|
| `lambda get-function-configuration irpt-49f-reporting-gold-lambda` | CodeSha256 `Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44=`, LastModified 2026-10-03T16:57:43Z, 2048 MB, 900 s |
| `infra/aws/lambda/ci/lambda-source-map.json` `deployed_code_sha256` | `Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44=` (last_deployed_commit 829e46ed7f): **equal to live** |
| artifact `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-reporting-gold-lambda.zip` HEAD | VersionId `FzE_mt1vdAU3Jy3VQuWIDbGVuf5Rrjjn`, 2026-10-03T04:11:45Z, metadata content-sha256 `Mex71Y5g...Z44=` |
| `list-object-versions` on that key | 4 versions; IsLatest = `FzE_mt1vdAU3Jy3VQuWIDbGVuf5Rrjjn` |

**Rollback target:** artifact version `FzE_mt1vdAU3Jy3VQuWIDbGVuf5Rrjjn`, which is CodeSha256 `Mex71Y5g...Z44=`.

The module sets `s3_object_version` from `data.aws_s3_object.artifact.version_id`, so the rebuild uploads a new latest version. To roll back, restore this version as latest, or re-pin it, and then run the same targeted `safe-apply`. `aws lambda update-function-code` is barred.

**This is a read, not a gate.** The apply cell re-reads both values immediately before its `safe-apply`. Any difference from the table above is a STOP and a row.
