# TO373I IAM leg applied 2026-10-08T22:47:14Z

CloudTrail PutRolePolicy event717f3ed8-6022-4365-b436-858805fbe9d1. Role irpt-export-render-role; inline irpt-export-render-custody-persist-policy. Signed COO7c08fe294e / CTO5f65b4f40e. Exact pair HCL committed552b019234, with no changes: live KeySchema HASH tenant / RANGE request_revision, so LeadingKeys restriction retained.

Terraform validate success. Existing inline and attached policies and function hash saved in before.json. Locked targeted saved plan and safe-apply:1add0change0destroy at aws_iam_role_policy.export_render_custody_persist only. Five statements; no wildcard resource; no UpdateItem; AccessAnalyzer0findings. Rendered resources:
- S1PutCustodyIndexAndRetentionRowsInServedFirmPartitions: arn:aws:dynamodb:us-east-1:313476888478:table/irpt-requests
- S2EncryptIndexWritesViaDynamoOnly: arn:aws:kms:us-east-1:313476888478:key/7f4d3042-10d8-49a7-b55e-3c963cea8111
- S3WriteAndVerifyCustodyReportsOnly: arn:aws:s3:::opal-data-irpt/irpt/49financial/platinum/custody_reports/*, arn:aws:s3:::opal-data-irpt/irpt/inflection/platinum/custody_reports/*, arn:aws:s3:::opal-data-irpt/irpt/cottonwood/platinum/custody_reports/*
- S4ReadRetainedRequestCompositionsOnly: arn:aws:s3:::opal-data-irpt/irpt/49financial/state/request_compositions/*, arn:aws:s3:::opal-data-irpt/irpt/inflection/state/request_compositions/*, arn:aws:s3:::opal-data-irpt/irpt/cottonwood/state/request_compositions/*
- S5KmsForThoseTwoPrefixesViaS3Only: arn:aws:kms:us-east-1:313476888478:key/7f4d3042-10d8-49a7-b55e-3c963cea8111

Live get-role-policy matches rendered-policy exactly. after.json records11/11 simulations (one ARN each, appropriate contexts): served PutItem allowed; unserved PutItem denied; UpdateItem denied; custody Put/Get allowed; composition Get allowed; performance Put denied; S2 KMS Encrypt/GenerateDataKey and S5 KMS GenerateDataKey/Decrypt allowed. Three negative cases have isolated admin-policy allowed controls. Table, bucket and KMS existence checked; S3 simulation suffix is synthetic and is not claimed to be an existing object. KMS simulation proves IAM authorization only, not a real encrypt/persist. CodeSha256 unchanged from before.json. Targeted replan no changes, exit=0.

Wrapper cross-box WARN:8 hits OPEN-CALL/OVERLAP; first named dell2 vendor-use question cf09 covering this root. WARN mode proceeded without override under this explicit laptop order. Naming plan2/2; tag authorization0candidates; tombstone1create clean. PowerShell tool process reported exit1 despite Terraform Apply complete1/0/0; no retry. Live readback, CloudTrail and no-change replan independently confirm success.

Ledger org/critical_paths/change_management/20261008T2245Z_custody-373i-iam-laptop-20261008_deploy_completion.md CLOSED A1/V1, sentinel removed. Open commit b640d76e02. Measured git ls-remote origin refs/heads/CLOUD709d093fa95f5f33bd8d8ea1937dcb6666542bf7. LOCAL, no push. Final closure commit supplied in issuer message. Route and real persist are dell2 follow-on work; no route/function changes or real persist by laptop. Issuer owns status flip.
