# C-RESTRICTED apply write-in (ADVI_COTBKF.TO-CB-e-4)

Writer: `0.9.0_WK_ADVI_COTBKF~19` on dell2. Nothing is applied; dell2 made no AWS, terraform, IAM or S3 act.

## The request

- Request id: `dell2-20261007T085711Z-7b15`
- Path: `org/devices/role_requests/dell2/dell2-20261007T085711Z-7b15.json` (one bus line `ROLE-REQUEST ...` sent to the laptop by the writer)
- Terraform root: `infra/aws/terraform/shared-infra`; resource `aws_iam_role` / `cloudops-cot-restricted-breakglass-role`
- 12 permissions, each tied to a line of `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf`

## Bucket and prefix

- Bucket `opal-data-cottonwood` (`arn:aws:s3:::opal-data-cottonwood`)
- Restricted prefix `commonwealth/cottonwood/bronze/crm/` (file line 195)

## Role

`cloudops-cot-restricted-breakglass-role`, module `opal_name_restricted_breakglass` (file lines 236-243), role resource line 244; trust
lines 248-257 = the console user `Andrew_Berman_Console` only, `sts:AssumeRole`.

## The statements (file lines in `s3-lgic-firm-buckets.tf`)

Bucket policy denies:
- `DenyRestrictedReadExceptReaders` line 205: Deny `GetObject*`, `GetObjectVersion*`, `GetObjectAttributes`, `GetObjectTagging` on `<bucket>/<prefix>*` unless principal is the console user or the break-glass role (line 208 actions).
- `DenyRestrictedListExceptReaders` line 213: Deny `s3:ListBucket*` on the bucket for the prefix, same readers (line 216).
- `DenyRestrictedWriteExceptBreakglass` line 224: Deny `PutObject*`, `DeleteObject*`, `RestoreObject` on `<bucket>/<prefix>*` unless principal is the break-glass role (line 227).

Role inline policy `restricted-prefix-get-put-list` (lines 259-279):
- `GetPutRestrictedPrefix` line 267: Allow `s3:GetObject`, `s3:GetObjectVersion`, `s3:PutObject` on `<bucket>/<prefix>*` (line 269).
- `ListRestrictedPrefix` line 273: Allow `s3:ListBucket` on the bucket, condition `s3:prefix` = prefix (line 275).

## Gap the writer imposed (row ADVI_COTBKF-W19-S1)

The writer's schema admits only a service as `assuming_service`; the real trust is a console USER. The request carries
`signin.amazonaws.com` as a placeholder. The laptop applies the trust of the merged file (lines 248-257), not the request's service field.
The writer and schema were not edited.

## Before the apply (laptop)

Run, with terraform and the real backend (dell2 lacks both; row S7):

`python infra/aws/terraform/shared-infra/tests/check_restricted_prefix.py`

(the CB4d4-AC1 check: targeted plan plus the IAM policy simulator; applies nothing.)

## Order of acts

1. Laptop applies the policy and role (targets `aws_s3_bucket_policy.lgic_firm`, `aws_iam_role.restricted_breakglass`, `aws_iam_role_policy.restricted_breakglass`) and answers the request with `mark-applied` or `mark-refused`.
2. Laptop re-runs `python infra/aws/terraform/shared-infra/tests/check_restricted_prefix.py`.
3. Only then, the single CRM landing by Andrew through the role, on his word.
