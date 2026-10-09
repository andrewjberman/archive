# Step G applied2026-10-09T00:29:00Z

GO107514, COO737a66ea46 / CTO21a5ceab0f section1. Clean root carrying83326afe6f; no source edits. Shared TF_PLUGIN_CACHE_DIR=C:/Users/AndrewBerman/.terraform.d/plugin-cache explicitly set for init/plan/apply/replan; no old temporary directory deleted.

Pre-plan final line (full output AC1.txt):
POLICY-SIM allowed_ok=22/22 denied_ok=15/15 passrole_ok=5/5 protected_ok=8/8 freed_allowed=72/72 freed_excluded=3 undo_freed=167/167 undo_still_denied=443 cutover_ok=23/23 selfsim_ok=9/9 ssm_ok=15/15 iamw_ok=225/225 planread_ok=423/423 sendcmd_ok=34/34 shellwin_ok=18/18 routes_freed=114/138 routes_still_refused=24 vendor_ok=249/249 all_ok=True

Saved before.json: deployv5,platform-secretsv1. Locked default untargeted saved plan exact0/2/0 at aws_iam_policy.dell_agent_deploy and aws_iam_policy.dell_agent_platform_secrets[0]. Policy comparison proved only one ARN added (IRPT render publickey) and one statement DenyCutoverParameterWrites, exactparameter/mdpf/custody_source with Put/Delete/DeleteParameters/Label/AddTags/RemoveTags. No other statement changes. Live documents equal plan; UpdateDate00:29:00Z,deployv6,platformv2.

BothDells simulation results (no value reads):
- cloudops-dell1-agent-user ssm:PutParameter on arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source: explicitDeny; cloudops-dell-agent-deploy-policy / DenyCutoverParameterWrites
- cloudops-dell1-agent-user ssm:DeleteParameter on arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source: explicitDeny; cloudops-dell-agent-deploy-policy / DenyCutoverParameterWrites
- cloudops-dell1-agent-user ssm:GetParameter on arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source: allowed; cloudops-dell-agent-plan-reads-policy / ReadSsmParametersPlanReads
- cloudops-dell1-agent-user ssm:GetParameters on arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source: allowed; cloudops-dell-agent-plan-reads-policy / ReadSsmParametersPlanReads
- cloudops-dell1-agent-user secretsmanager:GetSecretValue on arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/auth/irpt-render-jwt-public-key-EAL0l7: allowed; cloudops-dell-agent-platform-secrets-policy / ReadPlatformKeys
- cloudops-dell1-agent-user secretsmanager:GetSecretValue on arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/auth/jwt-public-key-Z6dqNK: implicitDeny; None / none (implicitDeny)
- cloudops-dell2-agent-user ssm:PutParameter on arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source: explicitDeny; cloudops-dell-agent-deploy-policy / DenyCutoverParameterWrites
- cloudops-dell2-agent-user ssm:DeleteParameter on arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source: explicitDeny; cloudops-dell-agent-deploy-policy / DenyCutoverParameterWrites
- cloudops-dell2-agent-user ssm:GetParameter on arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source: allowed; cloudops-dell-agent-plan-reads-policy / ReadSsmParametersPlanReads
- cloudops-dell2-agent-user ssm:GetParameters on arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source: allowed; cloudops-dell-agent-plan-reads-policy / ReadSsmParametersPlanReads
- cloudops-dell2-agent-user secretsmanager:GetSecretValue on arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/auth/irpt-render-jwt-public-key-EAL0l7: allowed; cloudops-dell-agent-platform-secrets-policy / ReadPlatformKeys
- cloudops-dell2-agent-user secretsmanager:GetSecretValue on arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/auth/jwt-public-key-Z6dqNK: implicitDeny; None / none (implicitDeny)

12/12 live arms;6isolatedadmin-policy controls allowed beside denies. Secret metadata read only establishes exactARN existence. comp-iam role resolver does not support this bare IAMuser input; SDK principal simulations bind full userARN. Before simulations prove cutoverPut allowed->explicitDeny andpublickey implicitDeny->allowed. Fullroot replan no changes exit0. Outer PowerShell reported exit1 despite Terraform Apply complete0/2/0; no retry; livepolicy comparison and replan confirm success.

Ledger org/critical_paths/change_management/20261009T0027Z_dell-stepg-laptop-20261009_deploy_completion.md CLOSED A1/V1;sentinel removed. Open44f3b0fbba;finalcommit supplied in report message. Full-id proof accompanies report. LOCAL,no push;measured ls-remote origin/CLOUD e520334206126e90dc9c76b9ab6cfdf837801f79 andorigin/box/laptop02ab00e1abafc5e1f62d606484b5286302c62512. Status flip issuer-owned.

F1 remains closed; TO20 reopen waits for dell2 open now. No secret value read, no parameter write, no independent IAM mutation.
