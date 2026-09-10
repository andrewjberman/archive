# EG-s-15 S15-AC2 -- THE PLAN GATE, VERBATIM TRANSCRIPTS
The pre-apply plan is NOT reproducible after the apply, so the transcript IS the
evidence. Captured by this worker's own session in this worktree; quoted whole,
never summarised. Preserved here because `.scratch/` is not committed.

## (i) PRE-APPLY TARGETED PLAN -- `.scratch/egs15_plan.txt`, mtime 2026-09-09 21:14:13.108 -0400 = **2026-09-10T01:14:13Z**
Invocation: `.tools/terraform.exe -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false -target=aws_lambda_function.orchestrator`

```
data.archive_file.orchestrator: Reading...
data.archive_file.orchestrator: Read complete after 0s [id=d345bc476bc559d3a20590391d7673a1bd3327c5]
data.aws_ssm_parameter.al2023: Reading...
aws_security_group.reporter: Refreshing state... [id=sg-090012d06e69ce82d]
aws_iam_role.orchestrator: Refreshing state... [id=etfs-reports-orchestrator-role]
aws_sns_topic.reports_alerts: Refreshing state... [id=arn:aws:sns:us-east-1:313476888478:etfs-reports-alerts]
aws_iam_role.reporter: Refreshing state... [id=etfs-reports-reporter-role]
data.aws_ssm_parameter.al2023: Read complete after 0s [id=/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64]
aws_iam_instance_profile.reporter: Refreshing state... [id=etfs-reports-reporter-profile]
aws_instance.reporter: Refreshing state... [id=i-070477bf35fc54409]
aws_lambda_function.orchestrator: Refreshing state... [id=etfs-reports-orchestrator]

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:

  # aws_lambda_function.orchestrator will be updated in-place
  ~ resource "aws_lambda_function" "orchestrator" {
        id                             = "etfs-reports-orchestrator"
      ~ last_modified                  = "2026-09-05T08:41:01.000+0000" -> (known after apply)
      ~ source_code_hash               = "CvFmg9ZmBrSMZSSlplJGd7BWp99FXn5+ODaRbKTe/QI=" -> "M5Dopbky3W1f1j97cqAB403Kh7IofIv/p0fCtRg7W80="
        tags                           = {
            "Name" = "etfs-reports-orchestrator"
        }
        # (27 unchanged attributes hidden)

        # (4 unchanged blocks hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.

Warning: Resource targeting is in effect

You are creating a plan with the -target option, which means that the result
of this plan may not represent all of the changes requested by the current
configuration.

The -target option is not for routine use, and is provided only for
exceptional situations such as recovering from errors or mistakes, or when
Terraform specifically suggests to use it as part of an error message.

─────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't
guarantee to take exactly these actions if you run "terraform apply" now.
```

**The only resource in the action list is `aws_lambda_function.orchestrator`** (the other lines are `Refreshing state...`, not changes), and the plan reads `Plan: 0 to add, 1 to change, 0 to destroy.`

## (ii) THE APPLY THAT FOLLOWED -- `.scratch/egs15_apply2.txt`, mtime 2026-09-09 21:16:19.461 -0400 = **2026-09-10T01:16:19Z** (AFTER the plan's 01:14:13Z)
Invocation: `HALT_ACK=1 .tools/safe-apply.sh -chdir=infra/aws/terraform/etfs-reports apply -input=false -auto-approve -target=aws_lambda_function.orchestrator`

Head of the transcript, proving it ran THROUGH `safe-apply.sh` and its gates:

```
HALT-GATE: worker 0.9.0_WK_ETFS_GUARDRAIL~1 has no inbox; scanning its issuer 2.0.0_SA_COO (a [STOP] to the issuer halts its workers)
safe-apply: infra/aws/terraform/etfs-reports sets default_tags -- running the comp-tagauthz pre-apply authorization gate.
------------------------------------------------------------------------------
SWEPT (derived from the account, one call: iam get-account-authorization-details):
  roles 229   local+attached policies 52   users 7   groups 1
  SCPs: NOT APPLICABLE -- account is not in an AWS Organization (AWSOrganizationsNotInUseException). Stated, not implied.
NOT SWEPT (named, not implied): S3 bucket policies, KMS key policies,
  permission boundaries, session policies, resource policies generally.
tag-conditioned statements found: 9 (4 ours, 5 AWS service-linked)
------------------------------------------------------------------------------

default_tags keys in infra/aws/terraform/etfs-reports: ['ManagedBy', 'Project', 'System']
  *** KEY COLLISION: ['Project', 'System'] are BOTH default_tags keys AND authorization keys.
```

The apply's own result line:

```
aws_lambda_function.orchestrator: Refreshing state... [id=etfs-reports-orchestrator]
aws_lambda_function.orchestrator: Modifying... [id=etfs-reports-orchestrator]
aws_lambda_function.orchestrator: Modifications complete after 6s [id=etfs-reports-orchestrator]
Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

## (iii) THE SAME TARGETED PLAN, RE-RUN NOW, WITH `-detailed-exitcode`
Invocation: `.tools/terraform.exe -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false -detailed-exitcode -target=aws_lambda_function.orchestrator` -> **rc 0**

```
data.archive_file.orchestrator: Reading...
data.archive_file.orchestrator: Read complete after 0s [id=d345bc476bc559d3a20590391d7673a1bd3327c5]
aws_iam_role.orchestrator: Refreshing state... [id=etfs-reports-orchestrator-role]
aws_iam_role.reporter: Refreshing state... [id=etfs-reports-reporter-role]
data.aws_ssm_parameter.al2023: Reading...
aws_security_group.reporter: Refreshing state... [id=sg-090012d06e69ce82d]
aws_sns_topic.reports_alerts: Refreshing state... [id=arn:aws:sns:us-east-1:313476888478:etfs-reports-alerts]
data.aws_ssm_parameter.al2023: Read complete after 0s [id=/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64]
aws_iam_instance_profile.reporter: Refreshing state... [id=etfs-reports-reporter-profile]
aws_instance.reporter: Refreshing state... [id=i-070477bf35fc54409]
aws_lambda_function.orchestrator: Refreshing state... [id=etfs-reports-orchestrator]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration
and found no differences, so no changes are needed.

Warning: Resource targeting is in effect

You are creating a plan with the -target option, which means that the result
of this plan may not represent all of the changes requested by the current
configuration.

The -target option is not for routine use, and is provided only for
exceptional situations such as recovering from errors or mistakes, or when
Terraform specifically suggests to use it as part of an error message.
```

## VERDICT

(i) pre-apply plan `0 to add, 1 to change, 0 to destroy` on `aws_lambda_function.orchestrator` and no other resource, at 01:14:13Z, PRECEDING
(ii) the `safe-apply` run at 01:16:19Z whose result line reads `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.`, and
(iii) the same plan now printing `No changes. Your infrastructure matches the configuration.` with `-detailed-exitcode` rc 0 -- the post-state `S15-AC3` also requires.

The three agree instead of contradicting.

**PLAN-GATE-HELD**
