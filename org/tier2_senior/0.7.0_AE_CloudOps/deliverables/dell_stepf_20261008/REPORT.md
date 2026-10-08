# Dell identity step F applied2026-10-08T23:24:52Z

GO107459 by COO~C; halves COO6734d80272 / CTOb51c573d66. Root clean at c8eb88e9eb1b074c85ab66e1c15d397a36ded0bd containing db7ecaa46b. No source edit. Pre-plan simulation observed final line saved AC1-observed-last-line.txt: iamw_ok=225/225 planread_ok=422/422, all_ok=True. comp-iam service has no matching Dell group service; no clean grant claim from that instrument.

Before.json: attached group7 and deploy defaultv4. Locked default untargeted saved plan:4/1/0 exactly five signed addresses (plan-verdict.json). Added PutParameter0, secretsmanager0, PassRole1. Deploy statement diff removes only DenyEveryIamWrite and DenyPassRoleExceptNamed. One safe-apply completed4/1/0. All3changed/new live policy documents match rendered plan; UpdateDate23:24:52Z, deployv5,newpoliciesv1. Outer PowerShell reported exit1 while Terraform prints Apply complete; no retry, readback and replan independently confirm success.

Live readback, one ARN per call, simulation only:
- cloudops-dell1-agent-user iam:CreateRole: allowed; cloudops-dell-agent-iam-roles-policy / AllowIamRolesPoliciesAndInstanceProfiles
- cloudops-dell1-agent-user iam:PassRole: allowed; cloudops-dell-agent-iam-roles-policy / AllowPassAnyRole
- cloudops-dell1-agent-user ssm:GetParameter: allowed; cloudops-dell-agent-plan-reads-policy / ReadSsmParametersPlanReads
- cloudops-dell1-agent-user iam:CreateUser: explicitDeny; cloudops-dell-agent-iam-roles-policy / DenyIamUsersGroupsKeysAndAccount
- cloudops-dell1-agent-user iam:CreateAccessKey: explicitDeny; cloudops-dell-agent-iam-roles-policy / DenyIamUsersGroupsKeysAndAccount
- cloudops-dell2-agent-user iam:CreateRole: allowed; cloudops-dell-agent-iam-roles-policy / AllowIamRolesPoliciesAndInstanceProfiles
- cloudops-dell2-agent-user iam:PassRole: allowed; cloudops-dell-agent-iam-roles-policy / AllowPassAnyRole
- cloudops-dell2-agent-user ssm:GetParameter: allowed; cloudops-dell-agent-plan-reads-policy / ReadSsmParametersPlanReads
- cloudops-dell2-agent-user iam:CreateUser: explicitDeny; cloudops-dell-agent-iam-roles-policy / DenyIamUsersGroupsKeysAndAccount
- cloudops-dell2-agent-user iam:CreateAccessKey: explicitDeny; cloudops-dell-agent-iam-roles-policy / DenyIamUsersGroupsKeysAndAccount

Four refused cases have isolated admin-policy allowed controls. CreateRole/CreateUser ARNs are synthetic authorization probes, not created resources. PassRole checked existing irpt-export-render-role (outside the former fixture named list); former live DenyPassRoleExceptNamed denied * as saved. No IAM writes outside Terraform. No GetParameter value read and no PutParameter refusal claim. These are APPLIED authorization checks, not execution of Dell writes.

Group after, nine:
- cloudops-dell-agent-plan-reads-policy
- cloudops-dell-agent-create-policy
- cloudops-dell-agent-platform-secrets-policy
- cloudops-dell-agent-respol-allow-policy
- cloudops-dell-agent-deploy-policy
- cloudops-dell-agent-ssm-send-policy
- cloudops-dell-agent-routes-fn-policy
- cloudops-dell-agent-vendor-secrets-policy
- cloudops-dell-agent-iam-roles-policy

Full default root replan no changes exit=0. Ledger org/critical_paths/change_management/20261008T2323Z_dell-stepf-iam-laptop-20261008_deploy_completion.md CLOSED A1/V1; sentinel removed. Opencommit4b86f2598d; closurecommit in issuer report. Proof full TO id accompanies this report. LOCAL, no push; git ls-remote origin refs/heads/CLOUD0573ceb0c372740c370ea215311dab84966f4042. Status flip issuer-owned.

Adopted rule for both Dells, verbatim: "a Dell that creates or changes a role or policy reports it after the fact by bus (name, what it grants)". Existing before-rules remain. The CTO follow-up public-key read, cutover PutParameter narrowing, stale test retirement and conditional F1 reopening are separate work, not this apply. Prior F1 window remains closed.
