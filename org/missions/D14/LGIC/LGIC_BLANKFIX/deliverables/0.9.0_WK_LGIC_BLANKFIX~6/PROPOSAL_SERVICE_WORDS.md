# PROPOSAL -- move 11 AWS service words from `generic_noun` to `purpose_word`

For: `4.0.0_SA_CRO` (owns `infra/logic/registry/systems.json`). From: `0.9.0_WK_LGIC_BLANKFIX~6`, TO `LGIC_BLANKFIX.TO-BF-e-6`.
No registry file was edited; the measurement ran on a temporary copy and the real registry's 9 files hash identically before and after.
Reproduce: `python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~6/service_words.py`.

## The ask

Andrew ruled an AWS service name is never a system. `purpose_word` carries 8 such words; `generic_noun` carries 11 more that are
AWS services. Move these 11 (edit `refused_keys` in `infra/logic/registry/systems.json`):
`cloudfront codebuild ec2 ecr ecs events rds ses sns sqs ssm`.

## The words, with evidence (first IAM action in a `.tf` file)

| word | service | first evidence |
|---|---|---|
| cloudfront | Amazon CloudFront | infra/aws/terraform/bd-pipeline/iam.tf:571 `cloudfront:CreateInvalidation` |
| codebuild | AWS CodeBuild | infra/aws/terraform/estate-report/seam-freshness-publisher.tf:248 `codebuild:StartBuild` |
| ec2 | Amazon EC2 | infra/aws/iam/github-actions/gha-oidc-role.tf:124 `ec2:DescribeInstances` |
| ecr | Amazon ECR | infra/aws/terraform/c3materialize-b4/main.tf:160 `ecr:GetAuthorizationToken` |
| ecs | Amazon ECS | infra/aws/terraform/globgrph/comp_learns_producer.tf:130 `ecs:RunTask` |
| events | Amazon EventBridge | infra/aws/terraform/bd-pipeline/iam.tf:692 `events:PutEvents` |
| rds | Amazon RDS | infra/aws/terraform/globgrph/item2a.tf:191 `rds:DescribeDBInstances` |
| ses | Amazon SES | infra/aws/terraform/astn-pipeline/iam.tf:100 `ses:SendEmail` |
| sns | Amazon SNS | infra/aws/lambda/ec2-auto-shutdown-enforcer/main.tf:79 `sns:Publish` |
| sqs | Amazon SQS | infra/aws/terraform/globgrph/iam.tf:148 `sqs:ReceiveMessage` |
| ssm | AWS Systems Manager | infra/aws/iam/github-actions/gha-oidc-role.tf:109 `ssm:SendCommand` |

Service-named words left in `generic_noun` as `OTHER` (no IAM action with that prefix anywhere in the 9,816 tracked `.tf`/`.json` files):
`dynamo`, `ddb` (the IAM prefix is `dynamodb`, which is in no list; `dynamodb:PutItem` is used in etfs-canon/fanin-lambda.tf),
`fargate` (part of ECS, no prefix of its own), `sms` (the repo's SMS policy uses the `sms-voice` prefix). The other 75 words
(`data`, `send`, `github`, `x`, ...) are not service names. If the lane also wants `dynamo`/`ddb`/`fargate`/`sms` treated as service
words, that is a separate ruling; the measurement above does not support it from IAM evidence.

## The names that move (10 of 1,389 unique repo names; 1,965 items)

All 10 change `OUT-OF-PATTERN` -> `NO-SYSTEM-ASKED`; no other verdict changes (`other_changes=0`).

| type | name | where |
|---|---|---|
| ECS_TASK_DEFINITION | ecs-task | infra/aws/lambda/ci/trigger-census.py:108 |
| IAM_POLICY | cloudfront-invalidate | infra/aws/terraform/bd-pipeline/iam.tf:713 |
| IAM_POLICY | ecr-access | infra/aws/terraform/smartx-pipeline/iam.tf:186 |
| IAM_POLICY | events-emit | infra/aws/terraform/bd-pipeline/iam.tf:683 |
| IAM_POLICY | ses-send-email | infra/aws/terraform/portal-auth/iam.tf:176 |
| IAM_POLICY | ses-send-noreply | infra/aws/terraform/shared-infra/etfs-presentation.tf:110 |
| IAM_POLICY | sns-otp-alert | infra/aws/terraform/inf-pipeline/iam.tf:596 |
| IAM_POLICY | sns-publish-chainfatal | infra/aws/terraform/inf-pipeline/iam.tf:228 |
| IAM_POLICY | ssm-access | infra/aws/terraform/inf-pipeline/iam.tf:149 |
| IAM_POLICY | ssm-send-command-inf-jwt-fetch | infra/aws/terraform/inf-pipeline/iam.tf:1081 |

## Names that lead with a moved word and do NOT move

| type | name | stays | why |
|---|---|---|---|
| IAM_POLICY | ec2-ssm-deploy | OUT-OF-PATTERN | a `resources.json` row files it under system `cloudops`; it is a named-system name whose canonical form (`cloudops-ec2-ssm-deploy-policy`) is not its current name, so it stays a FIX |
| IAM_ROLE | ec2-ssm-role | OUT-OF-PATTERN | same: a `resources.json` row gives system `cloudops` (canonical `cloudops-ec2-ssm-role`) |

The NO-SYSTEM-ASKED branch fires only when no later token and no registry row resolves a system, so a service word never
overrides a system that is already attributed.

## Validation

`opal_naming.validate()` on the copy: 0 refusals. The copy was graded by pointing `opal_naming.REGISTRY_DIR` at it, which re-keys
both the registry cache and the vocabulary cache, so the vocabulary was built fresh from the copy.

SERVICE-WORDS ok=True generic_noun=90 aws_service=11 moved_names=10 to_no_system_asked=10 other_changes=0 validate_refusals=0
