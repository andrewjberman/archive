# NFRA_CTLPLN TO-APPLY-26 deployment report

- Applied `aws_iam_policy.dell2_ssm` once with `.tools/safe-apply.sh` at `2026-10-09T03:52:21.7867819Z`.
- The untargeted default-variable plan was exactly `0 to add, 1 to change, 0 to destroy`; the only changed address was `aws_iam_policy.dell2_ssm`.
- IAM policy default version advanced from `v6` to `v7`; AWS records the update at `2026-10-09T03:52:22Z`.
- The live `v7` policy document exactly equals `infra/aws/terraform/nfra-ctlpln-identity/dell2_ssm_policy.json`.
- `cloudops-dell2-agent-user`: `AWS-RunShellScript` plus resident host `i-0167fd745ad906a66` are allowed; `AWS-RunPowerShellScript`, `irpt-export-render-run`, and `ssm:StartSession` on `AWS-RunShellScript` are `explicitDeny`.
- `cloudops-dell1-agent-user`: the same four simulation arms are unchanged before and after the apply.
- The untargeted default-variable replan exits `0` with `No changes`.
- No SSM command was sent.
- TO-APPLY-25 leg C2 is superseded by this standing-access apply.

