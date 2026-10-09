# NFRA_CTLPLN TO-APPLY-27 deployment report

- Identity root applied first at `2026-10-09T05:39:17.5938654Z`: untargeted, default variables, exactly `1 to add, 1 to change, 0 to destroy` on `aws_iam_policy.dell2_ssm` and `aws_iam_user_policy_attachment.dell1_ssm`.
- Transcripts root applied second at `2026-10-09T05:40:13.6853868Z`: targeted only at `aws_kms_key.transcripts`, exactly `0 to add, 1 to change, 0 to destroy`, policy only.
- IAM policy default version advanced from `v7` to `v8`; live `v8` exactly equals `dell2_ssm_policy.json`, and dell1 holds the policy attachment exactly once.
- Both Dell users: `AWS-RunShellScript` is allowed on resident host `i-0167fd745ad906a66` and `mdpf-daily-runner` host `i-02448edb624a7a7cf`; `AWS-RunPowerShellScript` is `explicitDeny` on both hosts. Their four simulation signatures are identical.
- The live transcripts key policy adds only `DellAgentUsersGenerateDataKey`. Its principal set is exactly the two Dell users. Its only conditions are `kms:ViaService = s3.us-east-1.amazonaws.com` and `kms:EncryptionContext:aws:s3:arn = arn:aws:s3:::opal-data-transcripts`.
- Identity untargeted replan and transcripts targeted replan both exit `0` with `No changes`.
- No SSM command was sent; no secret or object value was read.
- The applied times and all three CTO conditions were sent to the COO and relayed to both Dell seats through MSTR.

