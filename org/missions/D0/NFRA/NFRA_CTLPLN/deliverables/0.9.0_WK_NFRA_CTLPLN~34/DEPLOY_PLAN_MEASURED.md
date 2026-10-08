# DEPLOY_PLAN_MEASURED -- NFRA_CTLPLN.TO-CT-i-6 (0.9.0_WK_NFRA_CTLPLN~34)

Nothing was applied, imported, tainted or uploaded. Both plans are reads: `terraform plan -no-color -input=false -lock=false`,
`TF_DATA_DIR` a scratch directory outside the repository, run from `infra/aws/terraform/transcripts/` in worktree
`wk-NFRA_CTLPLN-34` (branch cut from 56061b2d9c, plus the two statements of this order), with the estate's `.tools/` first on PATH
(so the `aws` shim is the one resolved). The texts are `PLAN_TARGETED_module_ldo_001.txt` and `PLAN_UNTARGETED.txt` beside this file.
No secret value appears in either (the one `(sensitive value)` is Terraform's own mask of a KMS grant token).

## Package and backend

- Package: `infra/aws/lambda/teams-chat-assist/dist/teams-chat-assist.zip`, 28 files, SHA-256
  `c1af3fe33556e895ec97cbf0ad6bd1915596f4daee5c259d1fca55a697d1da32`. `gen_bus_devices.py --check` read `BUS-DEVICES ok=True boxes=4 in_register=4 in_names=4`.
  The plan's new `source_code_hash` `wa8/4zVW6JXsl8vwrWvRkVWW9NruXCWdH8pVppfR2jI=` is this SHA-256 in base64 (decoded and compared).
- Second package, needed for any plan of this root (row NFRA_CTLPLN-W34-S1): `transcripts-pull/dist/transcripts-pull.zip`, 56 files, SHA-256
  `b84461a885d28f1dc5521a65a7f28616d82792f4e6151a8ea37af17c72e294bf`. Built locally, never uploaded or committed.
- `terraform init` backend line: `Successfully configured the backend "s3"! Terraform will automatically use this backend unless the backend configuration changes.`
  (bucket `opal-313476888478-terraform-state`, key `transcripts/tfstate`). No migration or reconfigure prompt; rc 0. Provider hashicorp/aws v5.100.0.

## TARGETED plan (`-target=module.ldo_001`)

Summary line: `Plan: 0 to add, 3 to change, 0 to destroy.`

| Address | Action | What the change is |
|---|---|---|
| `module.ldo_001.aws_iam_policy.exec` | update in-place | the policy document gains two Statement elements after `TellTheSiteZMstrOnTheBus`: `TellDell1OnTheBus` (`agentbus-global-dell1-queue.fifo`) and `TellDell2OnTheBus` (`agentbus-global-dell2-queue.fifo`), each Allow `sqs:GetQueueUrl` and `sqs:SendMessage`; 11 elements unchanged |
| `module.ldo_001.aws_lambda_function.handler` | update in-place | `source_code_hash` `IBrveNQC+...` -> `wa8/4zVW...` (the new zip); `last_modified` -> known after apply |
| `module.ldo_001.aws_lambda_function.ingress[0]` | update in-place | the same `source_code_hash` change and `last_modified`; handler and ingress share one zip |

Every line is inside `module.ldo_001`; no destroy, no replacement.

Lines NOT explained by this workstream's merged work alone:
- The two statements are this order's (FWD-20). The `source_code_hash` change is explained only in part. The live function was last
  modified 2026-10-04T23:04Z; the zip is rebuilt from every file the build copies, and `git log --since=2026-10-04T23:04Z` over those inputs
  lists, besides this workstream's commits (TO-CT-i-1 6975661829, TO-CT-i-3 29cdc27678, TO-CT-i-4 377ee45542, TO-CT-i-5 8b7788a834 and
  their drains), other projects' registry and schema commits (LGIC_BLANKFIX and CRO `infra/logic/registry/*.json`, `lib/opal_naming.py`,
  `org/standards/NAMING_SCHEMA.json`), which the build copies into the zip. I believe the hash change is the sum of these inputs; I did not
  diff the live zip's bytes against the new one, so the split between this workstream's code and the other projects' registry files is NOT measured.

## UNTARGETED plan

Summary line: `Plan: 9 to add, 4 to change, 0 to destroy.`

Inside `module.ldo_001` (the same three as above): `aws_iam_policy.exec`, `aws_lambda_function.handler`, `aws_lambda_function.ingress[0]` (update in-place).

Outside `module.ldo_001` (not covered by a targeted apply):
- `aws_cloudwatch_event_rule.pull` -- create
- `aws_cloudwatch_event_target.pull` -- create
- `aws_cloudwatch_log_group.pull` -- create
- `aws_iam_policy.pull` -- create
- `aws_iam_role.pull` -- create
- `aws_iam_role_policy_attachment.pull` -- create
- `aws_kms_grant.pull` -- create
- `aws_lambda_function.pull` -- create
- `aws_lambda_permission.pull_from_rule` -- create
- `aws_lambda_function.mail_pull` -- update in-place (`source_code_hash` `VGIq85Xx...` -> `uERhqIXS...`, the locally built transcripts-pull.zip; `last_modified`)

This is the Teams transcripts pull (not yet created in AWS) and the mail pull's code change, other work in the same root; an untargeted
apply would deploy them with the agent's change. The hash on `mail_pull` and the contents of `pull` depend on the locally built second zip.
