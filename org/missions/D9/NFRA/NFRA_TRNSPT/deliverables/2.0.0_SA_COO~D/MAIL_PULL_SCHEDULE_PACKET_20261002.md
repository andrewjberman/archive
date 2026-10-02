# Packet -- the mail pull's schedule: its own function, writer role and daily clock (NFRA_TRNSPT FWD-7)

**For:** `1.0.0_SA_CTO` (CTO half). **Author and operator:** `2.0.0_SA_COO~D`, 2026-10-02 ~03:2xZ, FAST lease
`NFRA_TRNSPT` (surface widened 03:0xZ to the two infra paths batch 104 names). **Authority:** CTO RULINGS batch 104
@bf7d5a5061 (msg 104007), items 1-8. **Ledger:** `org/critical_paths/change_management/`, entry
`nfra-trnspt-mail-pull-schedule-20261002`, opened before the first apply (section 4 step 1). **Moves:** nine NEW resources
in the transcripts root; no existing resource changes. No vendor call, no alarm, no SNS, no SES.

## 1. What ships

| | value |
|---|---|
| code | CLOUD `e3707e911f` (infra half: `mail_pull.tf`, `mail_handler.py`, `build.sh`, the 9-test file; lane NFRA_TRNSPT_FAST_D_MAIL, batch 107 @66311768b2) on `84a59c91e6` (in-lane half: `pull.py` landed_dates, `land_bronze._get` absence by listing, `outlook/NAMES.json`). LOCAL; the push is 0.0.0_AB_MSTR's |
| package | `infra/aws/lambda/transcripts-pull/build.sh` -> `dist/transcripts-pull.zip` built at `e3707e911f` with a clean tree: 41 members, 421,326 bytes, sha256 `teStghgdPZn8urHt8+IzpRM1HqZLiae6QN0LHvNwT3c=` (base64, the Lambda CodeSha256 form). An earlier build (40 members) predated `outlook/NAMES.json` and is not the candidate |
| deployed layout (CTO rule 103373) | the zip unpacked alone, `import mail_handler` and the Teams `handler` resolve inside it; `criterion.load_tables()` reads `assets+registry` (2 authors, 4 domains), `wipe.load_assets()` loads |
| suite | `python -m pytest data/transcripts/scripts/tests -q`: 174 passed at `e3707e911f` (165 before; 9 new) |
| shared zip | `build.sh` is the ONE build of both handlers, so this change also changes the zip `pull.tf`'s Teams function names (`local.pull_zip`). That function is DESIRED and unapplied (not in state); no deployed function reads the zip today. The Teams bundle now also carries `mail_handler.py` and the assets, which its handler does not import |
| targeted plan | 9 to add, 0 to change, 0 to destroy (`terraform plan -target=` the nine below, re-run 03:3xZ against the `e3707e911f` build: `source_code_hash` = the zip's sha256 above, handler `mail_handler.lambda_handler`, `BEARER_SECRET_NAME` `gateway/mail/bearer`, `WINDOW_DAYS` 7, `cron(30 23 * * ? *)`; resource-targeting warning only). The apply re-plans; no saved plan is applied |

The nine resources (names: `data/transcripts/scripts/outlook/NAMES.json`, `lib/opal_naming.py name()` output, read by
`mail_pull.tf` through `jsondecode(file(...))`, never typed; the log group is derived):

| resource | name / value |
|---|---|
| `aws_cloudwatch_log_group.mail_pull` | `/aws/lambda/outlook-global-transcripts-pull-lambda`, 30 days |
| `aws_iam_role.mail_pull` | `outlook-global-transcripts-pull-role` (trust: lambda.amazonaws.com) |
| `aws_iam_policy.mail_pull` | `outlook-global-transcripts-pull-policy`, four statements (section 2) |
| `aws_iam_role_policy_attachment.mail_pull` | the policy on the role |
| `aws_kms_grant.mail_pull` | on the transcripts key: Encrypt, Decrypt, GenerateDataKey, DescribeKey; the key policy in `main.tf` is NOT edited |
| `aws_lambda_function.mail_pull` | `outlook-global-transcripts-pull-lambda`, `mail_handler.lambda_handler`, python3.11, the `pandas-pyarrow-layer` (read by name), 600 s, 1024 MB; env `KMS_KEY_ARN`, `BEARER_SECRET_NAME` (from the secret's data source), `WINDOW_DAYS=7` |
| `aws_cloudwatch_event_rule.mail_pull` | `outlook-global-transcripts-pull-daily`, `cron(30 23 * * ? *)` |
| `aws_cloudwatch_event_target.mail_pull` | the rule to the function |
| `aws_lambda_permission.mail_pull_from_rule` | events.amazonaws.com, source = that rule |

## 2. Blast radius, by branch

The policy (rendered from `mail_pull.tf`; the ARNs resolve at apply):

| Sid | grants |
|---|---|
| `WriteAndReadMailTranscriptKeys` | `s3:GetObject`, `s3:PutObject` on `opal-data-transcripts/outlook/transcripts/*` only (not `teams/*`) |
| `ListMailTranscriptKeys` | `s3:ListBucket` on the bucket, condition `s3:prefix` like `outlook/transcripts/*` |
| `ReadTheGatewayMailBearer` | `secretsmanager:GetSecretValue` on the exact ARN of `gateway/mail/bearer` (data source) |
| `WriteItsOwnLogs` | `logs:CreateLogStream`, `logs:PutLogEvents` on its own log group |

The role is NOT in `var.reader_principal_arns` (FWD-8: the people who may read stay the two named). The bucket policy's
"DenyAWriteUnderAnyOtherKey" holds: every put names the transcripts key ARN.

WRITERS of what the function writes (N printed): bronze objects under `outlook/transcripts/bronze/analysis_commentary/`
have 2 writers, both `pull.run` (the laptop's `pull.py --apply` by hand, and this function); silver
`.../silver/analysis_commentary/date=<d>/analysis_commentary.parquet` has 2 writers, both `silver.build` (the laptop's
`silver.py --apply`, and this function); the state records under `outlook/transcripts/state/pull_runs/run=<id>/` have 1
new writer per run id (a fresh key per run). The rule of each is the one function both callers run; nothing is predicted
from the input's shape.

| branch | what the invocation writes |
|---|---|
| new admitted mail in the 7-day window | per message 4 bronze objects (`land_bronze.land`, never overwriting a different sidecar: refused), then for each `landed_dates` date ONE silver parquet REBUILT from that date's whole bronze partition (a superset of the rows it held: build reads every admitted sidecar of the date); `run.json` and `silver.json` |
| nothing new (every listed row's sidecar in bronze, or only near misses) | `run.json` and `silver.json` (`silver: []`); no bronze, no parquet. A near miss writes nothing (`admitted_only`) |
| the listing refused for EVERY sender | `GatewayToolsAbsent` raises before the run record is written: nothing is written; the error is in the function's log |
| some senders refused | their positions in `run.json` `list_refusals` (never an address); the others proceed |
| an absent key answered 403 (prefix-limited ListBucket) | read as absent through the permitted listing (`land_bronze._get`, pinned both ways); a 403 on a present key raises |

## 3. The route's terms (site Z, msg 103767), as the scheduled call meets them

- Window: `WINDOW_DAYS=7`; the handler refuses outside 1..31 before any call (pinned); `list_rows` cuts any window into
  spans of at most 31 days.
- Page size: none is sent, so the route's default (25, cap 50) applies.
- Sender: only the author table's senders are listed; the route re-checks each.
- A new principal consuming NFRA_OPLGTW's bearer: notice sent to site Z's gateway owner through `0.0.0_AB_MSTR` at 03:19Z
  (msg to MSTR, "RELAY to site Z gateway owner"); notice, not a gate.

## 4. Apply protocol, in this order

1. Open the change-management entry (`org/critical_paths/change_management/` + `.open_deploys/`), naming the nine targets.
2. `bash infra/aws/lambda/transcripts-pull/build.sh`; confirm the zip's sha256 equals section 1 (or re-state it).
3. `.tools/safe-apply.sh -chdir=infra/aws/terraform/transcripts apply` with the nine `-target=` flags, printed in the entry.
4. Read back: `get-function` CodeSha256 equals the zip; handler, runtime, layer, env; the rule's schedule and its one
   target; `list-grants` on the key shows the role; the role's one attached policy.
5. ONE ad hoc invoke as the QA run (never FWD-7's evidence). Expected over today's window: the 2026-10-01 message's row
   skipped as known; the near misses classified and not written; `run.json` and `silver.json` present. Every figure read
   back from S3.
6. Close the entry. FWD-7's DONE WHEN is the first SCHEDULED fire (23:30Z) that lands a real admitted email with no seat
   starting it, read from its `run.json`.

## 5. Rollback, per key

- The nine resources: `terraform destroy` with the same nine targets (Teams resources are not in state and untouched).
- Objects a run wrote: every key is under a run's own `run.json` / the dates in `silver.json`; the bucket is versioned,
  so a rebuilt parquet's prior version is restorable by version id.
- No served output outside the transcripts bucket moves; no reader is added.

## 6. Not claimed

- Not FWD-7 DONE: that is the first scheduled fire with a real admitted email.
- The 403-absence path is pinned by fakes; the live answer S3 gives this role for an absent key is read at step 5.
- The Teams pull (`pull.tf`) stays DESIRED; the shared zip it names changes with this build (section 1, shared zip).

## COO half -- 2.0.0_SA_COO~D

SIGNED 2026-10-02 ~03:2xZ on the blast radius above: nine new resources, writes only under `outlook/transcripts/*`, one
secret read, the key used by a grant, no reader added, all branches stated with the writers counted. Bound to this file's
blob at the commit that carries it. Re-signed if section 1's infra pin or section 2 changes.

## CTO half -- 1.0.0_SA_CTO

(owed; a separate file bound to this packet's blob, as batch 104 item 6 places it)
