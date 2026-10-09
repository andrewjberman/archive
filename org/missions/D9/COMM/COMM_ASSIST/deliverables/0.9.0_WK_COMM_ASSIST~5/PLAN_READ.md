# PLAN_READ -- COMM_ASSIST.TO-CA-d-1 (0.9.0_WK_COMM_ASSIST~5)

Nothing was applied. Both plans are `terraform plan -input=false -no-color -lock=false -target=module.ldo_001` run from
`infra/aws/terraform/transcripts/`, `TF_DATA_DIR` a scratch directory outside every git tree, after `init -input=false` against the
declared S3 backend (rc 0, no migrate or reconfigure prompt). Both packages were built locally first (`transcripts-pull` 73 files,
`teams-chat-assist` 32 files); nothing uploaded, no `dist/` committed. The texts are `PLAN_EMPTY.txt` and `PLAN_SET.txt` beside this file.

## PLAN_EMPTY.txt (variable left at its default, empty)

Summary line: `Plan: 0 to add, 2 to change, 0 to destroy.`

| Address | Action | Changed arguments |
|---|---|---|
| `module.ldo_001.aws_lambda_function.handler` | update in-place | `source_code_hash` `xWURpe/n...` -> `KjKXrypK...`; `last_modified` -> known after apply |
| `module.ldo_001.aws_lambda_function.ingress[0]` | update in-place | the same `source_code_hash` change; `last_modified` -> known after apply |

Nothing else: no `environment` block change, no `aws_iam_policy.exec` change, no address outside `module.ldo_001`. The hash change is
the repackaged zip (the package moved since the last deploy); I did not diff the live zip against the new one.

## PLAN_SET.txt (variable = the fake probe ARN `arn:aws:secretsmanager:us-east-1:000000000000:secret:comm-assist-plan-probe`)

Summary line: `Plan: 0 to add, 3 to change, 0 to destroy.`

| Address | Action | Changed arguments |
|---|---|---|
| `module.ldo_001.aws_iam_policy.exec` | update in-place | the secrets-read statement's `Resource` list gains the probe ARN (after the three existing secrets); no other statement changes |
| `module.ldo_001.aws_lambda_function.handler` | update in-place | `environment.variables` gains `MAIL_BEARER_SECRET` = the probe ARN; the same `source_code_hash` and `last_modified` changes as the empty plan |
| `module.ldo_001.aws_lambda_function.ingress[0]` | update in-place | the same `MAIL_BEARER_SECRET` addition; the same `source_code_hash` and `last_modified` changes |

The set plan is the empty plan plus exactly: the env var on both functions and the probe ARN in the secrets-read statement.
Every address is inside `module.ldo_001`; no add, no destroy.
