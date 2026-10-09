# PREDICTION -- NFRA_IAMROLES202609.TO-IAM-v-3: removing `secretsmanager:DescribeSecret` from `smartx-assets-pull-role`

Produced by `0.9.0_WK_NFRA_IAMROLES202609~13` on 2026-10-09 (read-only: no AWS write, nothing edited under `infra/`, no terraform plan or apply). The change exists only as `narrowing.patch` in this directory. Machine form: `PREDICTION.json`.

## 1. The prediction in one paragraph

Removing `secretsmanager:DescribeSecret` from the `ReadAuthBundle` statement of the inline policy `smartx-assets-pull-access` (`infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf` line 101) breaks **nothing**: `predicted_breaks = []`. The only compute identity that assumes the role, the Lambda `smartx-assets-daily-pull`, never calls DescribeSecret (not in its deployed code, not in 89 days of its CloudTrail, not in 90 days of Access Advisor). After the change, DescribeSecret on the five secrets reads `implicitDeny`, while GetSecretValue and PutSecretValue stay `allowed`. The outcome is read from the first scheduled run (cron `02 13 * * * UTC`) that starts after the apply: **zero AccessDenied, zero DescribeSecret events, GetSecretValue events present, and the same standing `DirtyRunError` signature as the previous 30 days.**

## 2. The change

```
infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf  line 101  (resource aws_iam_role_policy.assets_pull, Sid ReadAuthBundle)
-        Action = ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"]
+        Action = ["secretsmanager:GetSecretValue"]
```

`narrowing.patch` is a git diff against the base (`faeb6e4ac9`) of that one file: one line changed, no wildcard expansion, no other line moved. `git apply --check` passes; it is not applied.

Rollback: `git apply -R narrowing.patch` (or `git revert` of the v-4 commit), then the same safe-apply on `infra/aws/terraform/smartx-pipeline`. That restores line 101 to the two-action form. Verify with `simulate-principal-policy`: DescribeSecret on `smartx/jwt/current-jk8FRu` reads `allowed` again. No `put-role-policy`, no console edit, in either direction.

## 3. How each candidate rule was checked

| Rule | Check | Result |
|---|---|---|
| 1. `never-used` in the round-4 bundle, observable | bundle blob `3ac4deb7f663065bbdc32b3efb76d251c4cfab7b` (verified by `git hash-object`): `smartx-assets-pull-role` row `secretsmanager:DescribeSecret` status `never-used`, `last_used` null. The same service is tracked at action level: `GetSecretValue` and `PutSecretValue` on the same role read `used`, `last_used` 2026-10-08, so Secrets Manager is observable here and the null is a real 90-day zero, not "unobservable" | HOLDS |
| 2. Declared in Terraform | `assets-pull-iam.tf` line 84 `resource "aws_iam_role_policy" "assets_pull"`, line 101 the Action list. The instrument read the LIVE ReadAuthBundle statement: 5 resource patterns, identical to the 5 resources in Terraform lines 102-112 (username-*, password-*, jwt, cookie, yaliu-bundle) | HOLDS |
| 3. Not rows 8/10, not a portal or client login path | role is neither `opal-data-refresh-lambda-role` nor `portal-auth-lambda-role`; `iam get-role` trust policy is `lambda.amazonaws.com` only; one function uses it (233 us-east-1 functions scanned) | HOLDS |
| 4. ONE action, ONE statement | DescribeSecret appears in exactly one statement of the role (instrument section [1]: "Allow statements naming action secretsmanager:DescribeSecret: 1"); the patch changes one line | HOLDS |
| 5. Daily consumer | EventBridge Scheduler `smartx-assets-daily-pull-daily` ENABLED `cron(2 13 * * ? *)` UTC; log streams exist for every day of the last 30 | HOLDS |

Candidate search, denominator: bundle 280 roles, 199 with a never-used row, 1486 never-used rows (1329 not `logs:CreateLogGroup`). Rejected, with reasons (also in `PREDICTION.json` `candidate_search`):

- `etfs-canon-fanin-role` / `dynamodb:DescribeTable` (`fanin-lambda.tf:75`, daily 15:45Z): met rules 1-4 and the instrument ran on it, but its table `opal-etfs-ownership-daily` was deleted 2026-08-07 and the Lambda fails every run on `BatchWriteItem` (`ResourceNotFoundException`). A consumer that fails earlier cannot show an outcome (rule 5). Row `NFRA_IAMROLES202609-Z-W13-S2`.
- The 95 roles whose only never-used row is `logs:CreateLogGroup` (for example `inf-billing-daily-role`): the grant comes from the AWS-managed `AWSLambdaBasicExecutionRole` attachment, not a statement in the module, so rule 4 cannot hold.
- `smartx-jwt-refresher-role` / `DescribeSecret`: declared in two statements (`rest-pull-iam.tf` lines 43 and 56); removing one leaves the permission live through the other.

## 4. Evidence, then the reasoning to `predicted_breaks`

Consumers (every compute identity that assumes the role, and how each was found):

1. `aws lambda list-functions --region us-east-1`: 233 functions scanned, exactly 1 with `Role` = `smartx-assets-pull-role`: `smartx-assets-daily-pull`.
2. `aws iam get-role`: trust principal `lambda.amazonaws.com` only; `RoleLastUsed` 2026-10-08T13:24Z, us-east-1.
3. `lambda-source-map.json` entry `smartx-assets-daily-pull` (`iam_role: smartx-assets-pull-role`) and `assets-pull-lambda.tf` line 38; the instrument's section [4] agrees (1 found).
4. Role policies: inline `smartx-assets-pull-access`, `smartx-assets-pull-invoke-silver-converter`; attached `opal-assets-one-way-fan-in-fence`, `AWSLambdaBasicExecutionRole`. Only `smartx-assets-pull-access` names DescribeSecret.

What the consumer actually does (three independent planes, all agree):

- **Code.** The deployed zip (downloaded read-only through `lambda get-function`) has CodeSha256 `4Iw0TWcez71pRQoUK0GXPxGMOAsVMIgMBIGhk+JRk8k=`, equal to `lambda-source-map` `artifact_sha256`. All 8 `.py` files are byte-identical (CRLF-normalised) to `infra/aws/lambda/smartx_assets_pull/`. None contains `describe_secret` or `DescribeSecret`; `auth_bundle.py` calls only `get_secret_value` and `put_secret_value`. Backfill modes run the same code (`backfill.py` is in the zip).
- **Access Advisor** (90 days): DescribeSecret `never-used`; GetSecretValue and PutSecretValue `used`.
- **CloudTrail** `lookup-events Username=smartx-assets-daily-pull`, 89-day window: 1446 events (2026-07-14..2026-10-08): Decrypt 634, GetSecretValue 541, CreateLogStream 93, GenerateDataKey 89, PutSecretValue 89, **DescribeSecret 0**. The positive control on the plane is that the same query returns the session's real Get/Put events, so a zero here is not a blind query.

Reasoning: removing a permission breaks a caller only if the caller issues the call. Code, 90 days of Access Advisor and 89 days of CloudTrail say the single caller never issues DescribeSecret, and boto3's `get_secret_value` does not issue it implicitly. The grants that remain (GetSecretValue on the same five secrets, PutSecretValue on the two write-back secrets) cover every call the code makes. Therefore `predicted_breaks = []`.

The instrument's own PREDICTION block says "WOULD BREAK 5 live-verified caller path(s)". That sentence counts the five resource patterns on which DescribeSecret is currently `allowed` (capabilities revoked); it does not join section [3] (usage). Reading it as callers broken would contradict sections [3] and the CloudTrail count above. `predicted_breaks` is the callers broken: none. The five revoked capabilities are recorded in `predicted_post_state`. Row `NFRA_IAMROLES202609-Z-W13-S3`.

Confounder, stated so the outcome can be read against it: the consumer is not clean today. It raises `DirtyRunError` (feed9 reconciliation, PARTIAL identity table) at `lambda_function.py` line 265 on 30 of 30 daily runs (2026-09-09..2026-10-08), after the Secrets Manager auth path. That is a data defect, not IAM, and it is a stable signature, so it separates cleanly from an `AccessDenied`. Row `NFRA_IAMROLES202609-Z-W13-S1`.

Limits, not hidden: (a) CloudTrail `lookup-events` covers management events only; DescribeSecret is one (Get/Put of the same service appear in the same query). (b) The window is 89 days; a call pattern rarer than that is not excluded by CloudTrail, but is excluded by the code read. (c) comp-blast on the `.tf` path found no node (see section 5); the role-name query returned 4 IAM_POLICY nodes and a "lower bound" caveat.

## 5. How v-4 reads the outcome, and what proves this wrong

Observation window: let D be the UTC date of the first 13:02Z run that starts after the apply completes (apply before 13:02Z on date X gives D = X, otherwise X + 1). Read from 13:30Z on D (observed run durations 537-859 s; the stream is complete when its REPORT lines are present).

Predicted: on D, `/aws/lambda/smartx-assets-daily-pull` has no AccessDenied event; CloudTrail for `Username=smartx-assets-daily-pull` has no event with `errorCode` AccessDenied or UnauthorizedOperation and no `DescribeSecret` event of any outcome; GetSecretValue events are present (baseline about 6 per day); the only ERROR is the standing `DirtyRunError` at line 265 (or none, if that data defect has been fixed meanwhile). After apply, `simulate-principal-policy` reads DescribeSecret `implicitDeny` and GetSecretValue `allowed` on all five resources.

Proved wrong by any one of: F1 an AccessDenied log event; F2 a CloudTrail AccessDenied/UnauthorizedOperation for that session, or any DescribeSecret event; F3 zero GetSecretValue events on D (the auth path did not run, so the run says nothing); F4 an ERROR signature other than the standing DirtyRunError. F3 makes a vacuous pass impossible.

## 6. Instrument output, quoted in full

Instrument: `org/missions/D12/NFRA/NFRA_IAMROLES202609/deliverables/0.9.0_WK_NFRA_IAMROLES202609~2/preflight-blast-radius.py`, blob `bd7620790c6884d55969779812bebe9ba7565355` (`git hash-object` reproduces it). Run 2026-10-09T09:17:46Z, rc=0, under `timeout 120`:

```
==============================================================================
PRE-FLIGHT BLAST RADIUS -- IAM-s-8 (FWD-5)
run at (UTC): 2026-10-09T09:17:46Z
role:         smartx-assets-pull-role
candidate removal (Allow-action, NOT applied): secretsmanager:DescribeSecret
STATUS: CHECK ONLY. No terraform apply / safe-apply / put-role-policy / delete-role-policy / attach-role-policy / detach-role-policy has been called by this run or ever will be by this file.
==============================================================================

[1] LIVE POLICY ENUMERATION (plane: DESIRED -- policy TEXT, read live via iam:List*/iam:Get*, read-only)
    role ARN: arn:aws:iam::313476888478:role/smartx-assets-pull-role
    inline + attached-managed policy documents read: statements examined = 9

    Allow statements naming action secretsmanager:DescribeSecret: 1
    DISTINCT resource patterns granting it (DENOMINATOR of resources examined): 5
      - arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-* cond=REQUIRES-NOTHING (no Condition block, plane: DESIRED, policy text)  granted by: smartx-assets-pull-access (Sid=ReadAuthBundle)
      - arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/password-* cond=REQUIRES-NOTHING (no Condition block, plane: DESIRED, policy text)  granted by: smartx-assets-pull-access (Sid=ReadAuthBundle)
      - arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu cond=REQUIRES-NOTHING (no Condition block, plane: DESIRED, policy text)  granted by: smartx-assets-pull-access (Sid=ReadAuthBundle)
      - arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/cookie/current-UOdUCI cond=REQUIRES-NOTHING (no Condition block, plane: DESIRED, policy text)  granted by: smartx-assets-pull-access (Sid=ReadAuthBundle)
      - arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/yaliu-bundle-ILu23S cond=REQUIRES-NOTHING (no Condition block, plane: DESIRED, policy text)  granted by: smartx-assets-pull-access (Sid=ReadAuthBundle)

[1a] CONDITION AXIS -- composing IAM-s-4's condition-axis-reader.py (not re-derived)
    Sid=ReadAuthBundle (source: smartx-assets-pull-access, file: infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf) -- condition-axis-reader.py says:
      [aws_iam_role_policy.assets_pull (policy)] statement 1/4 -- Sid=ReadAuthBundle Effect=Allow
          REQUIRES-NOTHING
      
      [aws_iam_role_policy.assets_pull (policy)] statement 2/4 -- Sid=WriteBackRefreshedToken Effect=Allow
          REQUIRES-NOTHING
      

[2] EXERCISE -- `aws iam simulate-principal-policy` via `.tools/comp-iam-usage reach-check`, ONE resource ARN per call (Rule-22a limit (b): batching corrupts the control). Plane moves from DESIRED to EXERCISED here.
      probe=arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-preflight-blast-radius-probe-object verdict=allowed      condition_handling=no-condition missing_context=none
      probe=arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/password-preflight-blast-radius-probe-object verdict=allowed      condition_handling=no-condition missing_context=none
      probe=arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu verdict=allowed      condition_handling=no-condition missing_context=none
      probe=arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/cookie/current-UOdUCI verdict=allowed      condition_handling=no-condition missing_context=none
      probe=arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/yaliu-bundle-ILu23S verdict=allowed      condition_handling=no-condition missing_context=none

[2a] CONTROLS (separate calls, never batched with the target -- Rule-22a limit (b))
    POSITIVE control (secretsmanager:PutSecretValue, arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu): verdict=allowed
    NEGATIVE control (iam:CreateUser, arn:aws:iam::313476888478:user/preflight-negative-control-nonexistent): verdict=UNKNOWN

[3] HISTORICAL-USAGE PLANE (composed from IAM-s-1: `.tools/comp-iam-usage permission-cold`, IAM Access Advisor ACTION_LEVEL -- never Access Analyzer)
    secretsmanager:DescribeSecret status=never-used

[4] COMPUTE IDENTITIES SHARING THIS ROLE + comp-blast (code/infra dependency graph)
    Lambda functions assuming this role (source: infra/aws/lambda/ci/lambda-source-map.json, a committed artifact): 1 found: smartx-assets-daily-pull
    comp-blast arn:aws:lambda:us-east-1:313476888478:function:smartx-assets-daily-pull: 49 downstream nodes (LOWER BOUND -- dynamic/FUNC-key consumers the extractors don't edge are NOT counted, per the tool's own caveat). IAM_POLICY band (22): opal-assets-one-way-fan-in-fence, AWSLambdaBasicExecutionRole, smartx-assets-pull-access, smartx-assets-pull-invoke-silver-converter, opal-data-assets#policy, advi-49f-gold-dispatch-scoped, opal-data-49financial#policy, opal-assets-silver-write-bd49finsurance-blackdiamond, opal-assets-silver-dlq-access, opal-assets-silver-bd49finsurance-read-bronze ...
      cross-check (comp-blast independently names): smartx-assets-pull-access

[5] comp-iam DESIRED-PLANE CROSS-REFERENCE -- named where it is BLIND, per C-NO-ACCESSDENIED
    comp-iam role 'smartx-assets-pull-role': (first 400 chars) ROLE: smartx-assets-pull-role |   tf_resource: assets_pull |   source: infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf |   statements: 6 |  |   Statement 1: Allow |     Actions (2): |       secretsmanager:DescribeSecret |       secretsmanager:GetSecretValue |     Resources: arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-*, arn:aws:secretsmanager:us-east-1:313476888478:secret
    comp-iam service smartx-assets-daily-pull: 0/2 call-site operations unmapped.
    comp-iam stats (live): Permission gaps:      338

==============================================================================
PREDICTION (EXERCISED via simulate-principal-policy, plane: APPLIED, live)
  Removing secretsmanager:DescribeSecret from smartx-assets-pull-role WOULD BREAK 5 live-verified caller path(s):
    - resource pattern arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-* (probed arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-preflight-blast-radius-probe-object) -- currently ALLOWED; granted by: smartx-assets-pull-access (Sid=ReadAuthBundle)
    - resource pattern arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/password-* (probed arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/password-preflight-blast-radius-probe-object) -- currently ALLOWED; granted by: smartx-assets-pull-access (Sid=ReadAuthBundle)
    - resource pattern arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu (probed arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu) -- currently ALLOWED; granted by: smartx-assets-pull-access (Sid=ReadAuthBundle)
    - resource pattern arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/cookie/current-UOdUCI (probed arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/cookie/current-UOdUCI) -- currently ALLOWED; granted by: smartx-assets-pull-access (Sid=ReadAuthBundle)
    - resource pattern arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/yaliu-bundle-ILu23S (probed arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/yaliu-bundle-ILu23S) -- currently ALLOWED; granted by: smartx-assets-pull-access (Sid=ReadAuthBundle)
  DENOMINATOR: 9 live statement(s) examined, 5 distinct resource pattern(s) examined (of which 5 probed via simulate, 0 unprobed/blind), 1 compute identity(ies) examined via comp-blast totaling 49 downstream graph node(s) (a LOWER BOUND).
  NOTHING WAS APPLIED TO THE WORLD BY THIS RUN.
==============================================================================
```

## 7. comp-blast on the module

`comp-blast` on the terraform file path (run as `bash .tools/comp-blast infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf` from the worktree, rc=3):

```
=== served cloud graph (opal-globgrph projection) ===
  Built from the estate as of 2026-10-09 06:17:57 UTC. Stitch source: stitch-codebuild built 2026-10-09T03:01:16Z.
  vintage: 2026-10-09T06:17:57.184375+00:00
  manifest: 1089b9991c9307491e63ff206520d11ddadc9b2f08f846084defcb6cbeaf7832
  artifact: projection/2026-10-09T06:17:57.184375+00:00/
  universe: 29700 nodes / 62469 edges (served, whole estate)
  transport: HTTPS /graph/cypher -- no local database, no cache, no fallback
VINTAGE: Built from the estate as of 2026-10-09 06:17:57 UTC. Stitch source: stitch-codebuild built 2026-10-09T03:01:16Z.  [vintage=2026-10-09T06:17:57.184375+00:00 manifest=1089b9991c93 nodes=29700 edges=62469]
NOT-FOUND: no graph node matches 'infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf' -- and here is the universe that verdict is over, so typo and out-of-scope stop looking identical:
  denominator: 29700 nodes (CANONICAL KUZU GRAPH) -- C2Motif=6685, MS_FILE=5955, Field=4969, JSXElement=2205, JSXRender=1433, MS_FOLDER=1356, PipelineFunction=1226, TypeDecl=807, IAM_POLICY=608, ReactComponent=442, S3Key=387, Module=374, Prop=359, IAM_ROLE=283
  universe: the canonical kuzu resource graph -- ALL of AWS plus the GIT code plane and MS_CLOUD (Andrew ruling 2026-08-03). The old private trace universe (2,255 nodes, 4 S3 buckets) is retired.
  (comp-pydeps has no python file by this name either -- check the spelling.)
  not a typo? by question: comp-xref <symbol> (graph-wide occurrence) | comp-symbols <file> (what a file defines) | comp-grep <pattern> (on-rails text search; .tools/ + org/modules INCLUDED).
  This is a NOT-FOUND, not a 'nothing breaks' clear.
ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS
```

A path is not a graph node, so the same tool was run on the two names the file declares. `bash .tools/comp-blast smartx-assets-pull-role` (rc=0):

```
budget: 90 s (default)
WITHIN BUDGET: scanned 4 of 4 traversal; budget: 90 s (default), used 4.96148969999922 s
=== served cloud graph (opal-globgrph projection) ===
  Built from the estate as of 2026-10-09 06:17:57 UTC. Stitch source: stitch-codebuild built 2026-10-09T03:01:16Z.
  vintage: 2026-10-09T06:17:57.184375+00:00
  manifest: 1089b9991c9307491e63ff206520d11ddadc9b2f08f846084defcb6cbeaf7832
  artifact: projection/2026-10-09T06:17:57.184375+00:00/
  universe: 29700 nodes / 62469 edges (served, whole estate)
  transport: HTTPS /graph/cypher -- no local database, no cache, no fallback
=== comp-blast worktree overlay ===
  HEAD: faeb6e4ac9  dirty: no  subject-files: 0  content-digest: -  scope: none
  (no worktree file maps to this subject -- estate-only answer, kuzu vintage governs)
============================
VINTAGE: Built from the estate as of 2026-10-09 06:17:57 UTC. Stitch source: stitch-codebuild built 2026-10-09T03:01:16Z.  [vintage=2026-10-09T06:17:57.184375+00:00 manifest=1089b9991c93 nodes=29700 edges=62469]
BLAST RADIUS: arn:aws:iam::313476888478:role/smartx-assets-pull-role

  IAM_POLICY (4):
    - opal-assets-one-way-fan-in-fence
    - AWSLambdaBasicExecutionRole
    - smartx-assets-pull-access
    - smartx-assets-pull-invoke-silver-converter

WARNING: arn:aws:iam::313476888478:role/smartx-assets-pull-role affects >= 4 downstream nodes
  NOTE: counts EXTRACTED graph edges only (LOWER BOUND). Dynamic/FUNC-key consumers the extractors don't edge are NOT counted. Before treating a producer as orphan/safe, grep its artifact key for dynamic reads (comp-pipescript consumers / a literal-key grep).
```

`bash .tools/comp-blast smartx-assets-pull-access` (rc=0) answered `ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS`, "No downstream consumers found for arn:aws:iam::313476888478:role/smartx-assets-pull-role/inline/smartx-assets-pull-access (no EXTRACTED edge -- NOT provably zero)". The instrument's section [4] ran comp-blast on the function `smartx-assets-daily-pull`: 49 downstream nodes, a lower bound. The graph is read as a lower bound only; the prediction rests on the code, Access Advisor and CloudTrail reads in section 4, not on graph silence.

## 8. Rejected candidate, instrument output (for the record)

`preflight-blast-radius.py --role etfs-canon-fanin-role --remove dynamodb:DescribeTable`, run 2026-10-09T09:04:39Z, rc=0. Everything in it read as for the chosen role (never-used, one statement, `WOULD BREAK 2` capability paths), which is why the rejection rests on the live state rather than the instrument: the table it writes was deleted on 2026-08-07 and the daily run fails first on `BatchWriteItem`.

```
==============================================================================
PRE-FLIGHT BLAST RADIUS -- IAM-s-8 (FWD-5)
run at (UTC): 2026-10-09T09:04:39Z
role:         etfs-canon-fanin-role
candidate removal (Allow-action, NOT applied): dynamodb:DescribeTable
STATUS: CHECK ONLY. No terraform apply / safe-apply / put-role-policy / delete-role-policy / attach-role-policy / detach-role-policy has been called by this run or ever will be by this file.
==============================================================================

[1] LIVE POLICY ENUMERATION (plane: DESIRED -- policy TEXT, read live via iam:List*/iam:Get*, read-only)
    role ARN: arn:aws:iam::313476888478:role/etfs-canon-fanin-role
    inline + attached-managed policy documents read: statements examined = 5

    Allow statements naming action dynamodb:DescribeTable: 1
    DISTINCT resource patterns granting it (DENOMINATOR of resources examined): 2
      - arn:aws:dynamodb:us-east-1:313476888478:table/opal-etfs-ownership-daily cond=REQUIRES-NOTHING (no Condition block, plane: DESIRED, policy text)  granted by: ddb-write-ownership-daily (Sid=WriteOwnershipDailyRows)
      - arn:aws:dynamodb:us-east-1:313476888478:table/opal-etfs-ownership-daily/index/* cond=REQUIRES-NOTHING (no Condition block, plane: DESIRED, policy text)  granted by: ddb-write-ownership-daily (Sid=WriteOwnershipDailyRows)

[1a] CONDITION AXIS -- composing IAM-s-4's condition-axis-reader.py (not re-derived)
    Sid=WriteOwnershipDailyRows (source: ddb-write-ownership-daily, file: infra/aws/terraform/etfs-canon/fanin-lambda.tf) -- condition-axis-reader.py says:
      [aws_iam_role_policy.etfs_canon_fanin_ddb (policy)] statement 1/1 -- Sid=WriteOwnershipDailyRows Effect=Allow
          REQUIRES-NOTHING
      
      [aws_iam_role_policy.etfs_canon_fanin_cw (policy)] statement 1/1 -- Sid=CwMetrics Effect=Allow
          REQUIRES-NOTHING
      

[2] EXERCISE -- `aws iam simulate-principal-policy` via `.tools/comp-iam-usage reach-check`, ONE resource ARN per call (Rule-22a limit (b): batching corrupts the control). Plane moves from DESIRED to EXERCISED here.
      probe=arn:aws:dynamodb:us-east-1:313476888478:table/opal-etfs-ownership-daily verdict=allowed      condition_handling=no-condition missing_context=none
      probe=arn:aws:dynamodb:us-east-1:313476888478:table/opal-etfs-ownership-daily/index/preflight-blast-radius-probe-object verdict=allowed      condition_handling=no-condition missing_context=none

[2a] CONTROLS (separate calls, never batched with the target -- Rule-22a limit (b))
    POSITIVE control (s3:ListBucket, arn:aws:s3:::opal-data-etfs): verdict=UNKNOWN
    NEGATIVE control (iam:CreateUser, arn:aws:iam::313476888478:user/preflight-negative-control-nonexistent): verdict=UNKNOWN

[3] HISTORICAL-USAGE PLANE (composed from IAM-s-1: `.tools/comp-iam-usage permission-cold`, IAM Access Advisor ACTION_LEVEL -- never Access Analyzer)
    dynamodb:DescribeTable status=never-used

[4] COMPUTE IDENTITIES SHARING THIS ROLE + comp-blast (code/infra dependency graph)
    Lambda functions assuming this role (source: infra/aws/lambda/ci/lambda-source-map.json, a committed artifact): 1 found: etfs-canon-fanin
    comp-blast arn:aws:lambda:us-east-1:313476888478:function:etfs-canon-fanin: 40 downstream nodes (LOWER BOUND -- dynamic/FUNC-key consumers the extractors don't edge are NOT counted, per the tool's own caveat). IAM_POLICY band (12): AWSLambdaBasicExecutionRole, cloudwatch-metrics, ddb-write-ownership-daily, s3-read-etfs-daily, rivalfunds-build-canonical-shape-policy, rivalfunds-build-silver-policy, rivalfunds-publish-page-policy, opal-data-portal-v2#policy, sscn-cloudwatch-logs, sscn-s3-access ...
      cross-check (comp-blast independently names): ddb-write-ownership-daily

[5] comp-iam DESIRED-PLANE CROSS-REFERENCE -- named where it is BLIND, per C-NO-ACCESSDENIED
    comp-iam role 'etfs-canon-fanin-role': (first 400 chars) ROLE: etfs-canon-fanin-role |   tf_resource: etfs_canon_fanin |   source: infra/aws/terraform/etfs-canon/fanin-lambda.tf |   statements: 5 |  |   Statement 1: Allow |     Actions (1): |       s3:GetObject |     Resources: arn:aws:s3:::opal-data-etfs/daily/* |   Statement 2: Allow |     Actions (1): |       s3:ListBucket |     Resources: arn:aws:s3:::opal-data-etfs |     Condition: { StringLike = { "s3:prefix" = ["daily/*"]
    comp-iam service etfs-canon-fanin: 0/4 call-site operations unmapped.
    comp-iam stats (live): Permission gaps:      338

==============================================================================
PREDICTION (EXERCISED via simulate-principal-policy, plane: APPLIED, live)
  Removing dynamodb:DescribeTable from etfs-canon-fanin-role WOULD BREAK 2 live-verified caller path(s):
    - resource pattern arn:aws:dynamodb:us-east-1:313476888478:table/opal-etfs-ownership-daily (probed arn:aws:dynamodb:us-east-1:313476888478:table/opal-etfs-ownership-daily) -- currently ALLOWED; granted by: ddb-write-ownership-daily (Sid=WriteOwnershipDailyRows)
    - resource pattern arn:aws:dynamodb:us-east-1:313476888478:table/opal-etfs-ownership-daily/index/* (probed arn:aws:dynamodb:us-east-1:313476888478:table/opal-etfs-ownership-daily/index/preflight-blast-radius-probe-object) -- currently ALLOWED; granted by: ddb-write-ownership-daily (Sid=WriteOwnershipDailyRows)
  DENOMINATOR: 5 live statement(s) examined, 2 distinct resource pattern(s) examined (of which 2 probed via simulate, 0 unprobed/blind), 1 compute identity(ies) examined via comp-blast totaling 40 downstream graph node(s) (a LOWER BOUND).
  NOTHING WAS APPLIED TO THE WORLD BY THIS RUN.
==============================================================================
```
