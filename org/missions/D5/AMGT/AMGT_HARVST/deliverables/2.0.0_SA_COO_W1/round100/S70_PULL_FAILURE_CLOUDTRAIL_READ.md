# Row AMGT_HARVST-D1-S70 -- a CloudTrail read of the failed pull (2.0.0_SA_COO~W1, 2026-10-21 ~06:4xZ)

Row `AMGT_HARVST-D1-S70` (SC1's, `92eac31e166`) records task `3f57aad6f7a94e299038ee5b4f16d674` failing to start at 01:32Z with `CannotPullContainerError ... for schema1 conversion ... not found`, "cause not read". The CTO ruled it is not the write run (msg 8927). This note reads the ECR side. It does not close the row (the disposition is the CVO's).

## What I read

`aws cloudtrail lookup-events` in `us-east-1` for the four ECR pull-side calls, two windows (01:31Z to 01:36Z and 01:43Z to 01:45Z), filtered to the execution-role session of each task (`assumed-role/amgt-gold-refresh-exec-role/<task id>`).

| Pull | Task | Auth token | `BatchGetImage` | `BatchCheckLayerAvailability` | `GetDownloadUrlForLayer` | error codes |
|---|---|---|---|---|---|---|
| SUCCESS (the `--help` probe, same task definition, same digest) | `e17aaac5...` | 1 (01:43:41Z) | **6** | 0 | **29**, all within 01:43:41Z to 01:43:42Z | none |
| FAILED | `3f57aad6...` | 1 (01:32:39Z) | **3** (01:32:39Z; first two ask for manifest v2, list v2, OCI manifest, OCI index and `*/*`, the third for v2 and `*/*`) | **1** at 01:33:09Z, 30 s later, with `layerDigests` = the IMAGE MANIFEST digest `sha256:4da76365...` | **0** | none |

## What it shows

- The identity, the registry, the repository and the digest were correct on both pulls: both sessions authenticated, both asked for the same digest, no `AccessDenied`, no recorded error code. **This is not an IAM denial and not a missing image** (it also matches my earlier reads that the image was in ECR with one image and the canary pulled it).
- The failed pull **never reached the layers**: zero `GetDownloadUrlForLayer`. After three manifest requests there is a 30-second gap, and then a `BatchCheckLayerAvailability` that treats the manifest digest as a layer. That second call is what the "schema1 conversion" fallback in the error text looks like from the registry's side: the agent's first resolve of the reference did not complete and it tried a legacy path, which cannot find a manifest digest among layers.
- The successful pull made six manifest requests and then 29 layer URLs (28 layers and the config) in about a second.

## What it does not show

CloudTrail records ECR reads with `responseElements: null`, so it cannot say what the registry returned to the three `BatchGetImage` calls; if the body carried an `ImageNotFound` failure for one of them, this view is blind to it. It does not say why the agent stalled for 30 s. **The cause is not determined.** The evidence fits a transient failure between the Fargate agent and the regional ECR endpoint at 01:32Z (the same task definition, role and digest pulled cleanly 11 minutes later (the probe, 01:43Z) and about 85 minutes earlier (the dry canary, started 00:07Z)), and does not fit a configuration fault in our Terraform, role or image. I would not carry it as more than that.

## For the record

- Repeat risk: unmeasured. The CTO's bound stands: a second failure to start under the pair stops and reports (a manifest problem would need a new push and a new digest).
- If the scheduled fire (Fri 10:00Z) fails the same way, the stage-8 read records `TaskFailedToStart` and the CloudTrail pattern above (3 manifest calls, a gap, a layer-probe of the manifest digest, no `GetDownloadUrlForLayer`) is the signature to look for; AWS support is the next owner, not our code.
