# NEVER-WIDEN PACKET -- the 49 Financial reporting-publish function: the HOP-2 READER code (switch OFF) and the READ grant on the filled prefix (IRPT_DASHBD round 149)

**Packet author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-16 ~20:3xZ. **Applier:** `0.7.0_AE_CloudOps~IB2` (the one IRPT CloudOps lane, rule 34). **Halves:** the COO half and the CTO half, each bound to this file's sha256 (printed in each half). **Order:** `IRPT_DASHBD.TO-DB-b-312` (cut after both halves are signed).
**What this pair does, in one paragraph.** It moves the code of `irpt-49f-reporting-publish-lambda` to the hop-2 READER (`read_filled_report_gold`, with the account join `DB-b-306` and the minted account ids `DB-b-310`, plus the publisher's `validate_filled_report`) and widens the function role's READ and LIST on the one filled-report gold prefix. **The filled-report switch `FILLED_REPORT_PASS` stays OFF** (the function has no environment variable at all): the reader never runs, no filled document is written, and **no served output moves**. The series republish, the summaries and every existing event behave as they do now. Turning the switch ON, the first filled-report pass and the served route (hops 3 and 4, `IB-pr-551`) are separate, later, signed acts.

## 1. The acts (five, in order; each has its own stop)

**Act 1 -- build and upload the new bundle.** The applier builds `irpt-49f-reporting-publish-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-49f-reporting-publish-lambda` (the source-map entry key; its `artifact_s3_key` is the scope-less `investor-reporting/irpt-reporting-publish-lambda.zip`, read from the map and never typed). The build-only hash (section 2) is the base64 sha256 the real build must print, or STOP. The upload writes a NEW VERSION of the key in `opal-313476888478-lambda-artifacts` (versioned; the current version `41lfCmfJWyvHbzqC3VtGeHVm6VJ4gRZb`, 210,289 bytes, is the rollback target) and updates the entry's `artifact_sha256` only.

**Act 2 -- ONE `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-publish/`** (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 0 to add, 2 to change, 0 to destroy:** (a) `module.irpt_reporting_publish.aws_lambda_function.this`, by CODE attributes only (the artifact version and the code hash move; memory 1,024, timeout 300, handler, runtime, role, layer, no environment and no reserved concurrency stay); (b) `aws_iam_role_policy.irpt_reporting_publish` (the inline policy `irpt-49f-reporting-publish-policy`), by exactly two statements: `ListExactlyTheDeclaredGoldPrefixes` (the `s3:prefix` condition gains `irpt/49financial/gold/filled_report_values/*`, 2 prefixes become 3) and `ReadDeclaredGoldPartitionsOnly` (the `s3:GetObject` resources gain `arn:aws:s3:::opal-data-49financial/irpt/49financial/gold/filled_report_values/*`, 2 become 3). Any other line, any other attribute, any destroy STOPS the act. The two schedules, their scheduler role and policy, the log group and the other six policy statements do not appear in the plan.

**Act 3 -- ONE synchronous probe `{"filled_report": true}`** (`RequestResponse`, `--cli-read-timeout 0`), outside the fire windows. With the switch OFF the handler returns at once and reads and writes nothing. **Expected response exactly** `{"enabled": false, "clients": 0, "written": 0, "not_available": [], "refused": []}`. Anything else STOPS (it would mean the switch is read as ON).

**Act 4 -- ONE synchronous DRY-RUN event on ONE shard** `{"dry_run": true, "shard": 0, "shards": 7}` (the existing path; writes NOTHING). The applier records the COUNT of any refused accounts, never an id. **Expected:** `ok` true, the shard's `accounts` about 990, `refused` 0 (as the earlier signed pair measured); Max Memory Used and duration inside the line (80 percent of memory, 240 s).

**Act 5 -- the after-read and the receipt.** Function: `CodeSha256` equals the bundle's, memory 1,024, timeout 300, layer, no environment, no reserved concurrency. Policy: the 8 statements, with the two named above at 3 entries each and the other six byte-identical to before. Schedules: both ENABLED with their crons untouched. The platinum reporting prefix: the object count and the version count are the same before and after Acts 3 and 4 (the applier reads both; the scheduled fires are kept out by the condition below). The receipt carries the counts, memory and duration, and the words "the reader has not run against the real partition" and "the switch is off".

## 2. Pins

- Repository commit read by this seat: `4aca09a82d2aa21588baf84a67d6fbb8ce4f92bd` (branch `box/dell2`).
- `reporting-publish/handler.py` blob `dc4986544358`, sha256 `6cdd020113f60a9067bf5719e1e6223c537dcba793fc4f7afbd5c2967ee04ab4`; `reporting-publish/publisher.py` blob `3f43a0bb5ad7`, sha256 `e303c3072abd9ee7da2e33d3770fd4b0b2b6b1d21399ab7750b235965afef10f`; `terraform/investor-reporting/reporting-publish/locals.tf` blob `be15185194f8`, sha256 `47658c9149b0e29c79508e6c2e4d10349e8788ff6266aa936e20a546f511e163`.
- **Build-only hash** (BUILD_ONLY=1 at that commit, every gate run, nothing uploaded): base64 sha256 `s/OKOv98j53aFJCLrBpYP8xh3oUcuWagn0vSHVBjhIM=`, 214,089 bytes.
- The reader's criteria: `DB174-1-AC1..3` (the account join) and `DB178-1-AC1..3` (the minting) PASS on the landed tree; the pass fix `DB-b-305`.

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- Function `irpt-49f-reporting-publish-lambda`: `CodeSha256` `SX0xYFZsxH4q6psJM56yAee9wRb6vrVUN4VrTV1ouU8=`, 1,024 MB, timeout 300 s, python3.12, layer `irpt-performance-native-layer:1`, environment none, last modified 2026-10-16T13:04:26Z, role `irpt-49f-reporting-publish-role`.
- Policy `irpt-49f-reporting-publish-policy`: 8 statements (list of the gold prefixes, read of declared gold partitions (2), write of the platinum reporting prefix, read-back of it, list of it, read of the firm directory objects, invoke of its own function, its own log stream).
- Artifact: the key's current version `41lfCmfJWyvHbzqC3VtGeHVm6VJ4gRZb` (210,289 bytes, 2026-10-16T12:22:06Z); three older versions kept.
- Schedules: `irpt-49f-reporting-publish-daily` ENABLED, `irpt-49f-reporting-publish-summaries-daily` ENABLED.
- The filled prefix `irpt/49financial/gold/filled_report_values/`: 18,257 objects at packet time (read by this seat in the earlier round); it is read by this function only after the switch is ON.

## 4. What each act changes in the world

Act 1 adds an artifact version. Act 2 replaces the function's code and adds one READ and LIST prefix to its role (read only: no write grant changes). Acts 3 and 4 write nothing. Act 5 reads. **A client-facing sentence this pair can move: none (count 0 read before the write):** no series, summary or filled document is written by this pair; the served pages read what the function wrote before.

## 5. Writers of the changed properties, counted

The CODE and the POLICY of the function have ONE writer: the Terraform root `reporting-publish` through `safe-apply` (N = 1; `aws lambda update-function-code` is barred). The function's OUTPUT (the series and summaries) is written by the same rule (`publisher.py`) through ONE enabled schedule per path: `irpt-49f-reporting-publish-daily` (08:15 New York weekdays) and `irpt-49f-reporting-publish-summaries-daily` (08:45), plus its own shard fan-out invokes; 0 EventBridge rules target the function (the writer count read `RD_IRPT_REPORTING_WRITERS_COUNT_20261016.json` @867d91f704). This pair changes none of those rules.

## 6. Both branches

**Branch A:** every act returns what it states. **Branch B (a plan line outside the gate, a build hash that differs, an Act 3 response that is not exactly the expected one):** STOP before the next act; the prior artifact version and the prior policy (Terraform state) are the rollback. **Branch C (memory or time):** Act 4 peaks above 819 MB or runs over 240 s: STOP, no resize inside this pair. **Branch D (a scheduled fire overlaps an act):** kept out by the condition below.

## 7. Rollback, per key

Function: point the entry back to artifact version `41lfCmfJWyvHbzqC3VtGeHVm6VJ4gRZb` through the Terraform root (`safe-apply`), never `update-function-code`. Policy: revert `locals.tf` to the pinned blob before this pair and `safe-apply`; the two statements return to 2 entries. No data key is written by this pair, so no data rollback exists to describe.

## 8. Conditions

1. **Ledger first,** bound to this packet's sha256 (`deploy_ledger.py open --slug irpt-dashbd-49f-publish-hop2-reader-readgrant-20261016`, the applier named, legs git, build, terraform, probe, dry run, receipt); `.open_deploys/` read across every live worktree with the denominator printed.
2. **Live state re-read at the moment of the act** (function, policy, schedules); a difference from section 3 other than the scheduled fires' own outputs is recorded before the act.
3. **No act inside a scheduled fire:** none between 12:05 and 13:15 UTC on a weekday (the 08:15 and 08:45 New York fires and their fan-out).
4. **Stop at once** on a `Task timed out`, an `AccessDenied`, a Max Memory Used above 819 MB, or a response that differs from the act's expectation. Counts and words only, never an account id.
5. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no schedule change, no environment variable (the switch stays OFF), no event other than the two named.**

## 9. Questions for the CTO's half

1. Accept the read grant on the filled prefix now, with the switch OFF (the policy is the only widening; the code is inert until the switch is ON)? 2. Accept the Act 3 probe as the evidence that the deployed code reads the switch as OFF? 3. Is the later first pass (switch ON, a client-facing document written) its own packet? (This seat's answer: yes.)

## 10. Not established, and so not covered

That the reader runs against the real partition inside the function's 1,024 MB and 300 s (measured offline by this seat: 269 MB and 0.4 s for the table, 4,012 households; the function has not run it); that `validate_filled_report` accepts every real household; the served route (`IB-pr-551`); the switch and any filled document; the Cottonwood publish function, which is the next pair.
