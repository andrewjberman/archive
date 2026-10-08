# TO-APPLY-17 step D apply report

APPLIED; Dell first use pending. Apply completed 2026-10-08T18:55:14.0161211Z (local wrapper completion timestamp).

Plan: 0 to add, 0 to change, 2 to destroy. Zero added lines. Exactly aws_iam_policy.dell_agent_routes_host[0] and aws_iam_group_policy_attachment.dell_agent_routes_host[0]. Apply exit=0, 0 added / 0 changed / 2 destroyed. One safe-apply; no source edits or code/document writes.

Before attachment list and full routes-host v1 document: org\tier2_senior\0.7.0_AE_CloudOps\logs\2026-10-08\dell_step_d\before-iam.json

Before:
- cloudops-dell-agent-routes-host-policy
- cloudops-dell-agent-create-policy
- cloudops-dell-agent-platform-secrets-policy
- cloudops-dell-agent-respol-allow-policy
- cloudops-dell-agent-deploy-policy
- cloudops-dell-agent-routes-fn-policy
- cloudops-dell-agent-vendor-secrets-policy

After:
- cloudops-dell-agent-create-policy
- cloudops-dell-agent-platform-secrets-policy
- cloudops-dell-agent-respol-allow-policy
- cloudops-dell-agent-deploy-policy
- cloudops-dell-agent-routes-fn-policy
- cloudops-dell-agent-vendor-secrets-policy

All six retained group documents unchanged; routes-host GetPolicy returns NoSuchEntity. No inline user/group policies.

| User | Action | Resource | Decision | Matched policy/Sid |
|---|---|---|---|---|
| cloudops-dell1-agent-user | s3:PutObject | arn:aws:s3:::opal-data-cot/code/gold/x.py | allowed | cloudops-dell-agent-deploy-policy/S3ObjectsOnOpalBuckets |
| cloudops-dell1-agent-user | ssm:UpdateDocument | arn:aws:ssm:us-east-1:313476888478:document/advi-49f-chain-dispatch | allowed | cloudops-dell-agent-create-policy/CreateUpdateTagCompute |
| cloudops-dell1-agent-user | ssm:SendCommand | arn:aws:ssm:us-east-1:313476888478:document/advi-49f-chain-dispatch | implicitDeny | None (no identity Allow) |
| cloudops-dell1-agent-user | lambda:UpdateFunctionCode | arn:aws:lambda:us-east-1:313476888478:function:opal-trending-topics-portal-publisher | explicitDeny | cloudops-dell-agent-routes-fn-policy/DenyRoutesToPrivilegedRolesFunctions |
| cloudops-dell1-agent-user | iam:CreateRole | arn:aws:iam::313476888478:role/opal-portal-lambda-role | explicitDeny | cloudops-dell-agent-deploy-policy/DenyEveryIamWrite |
| cloudops-dell2-agent-user | s3:PutObject | arn:aws:s3:::opal-data-cot/code/gold/x.py | allowed | cloudops-dell-agent-deploy-policy/S3ObjectsOnOpalBuckets |
| cloudops-dell2-agent-user | ssm:UpdateDocument | arn:aws:ssm:us-east-1:313476888478:document/advi-49f-chain-dispatch | allowed | cloudops-dell-agent-create-policy/CreateUpdateTagCompute |
| cloudops-dell2-agent-user | ssm:SendCommand | arn:aws:ssm:us-east-1:313476888478:document/advi-49f-chain-dispatch | implicitDeny | None (no identity Allow) |
| cloudops-dell2-agent-user | lambda:UpdateFunctionCode | arn:aws:lambda:us-east-1:313476888478:function:opal-trending-topics-portal-publisher | explicitDeny | cloudops-dell-agent-routes-fn-policy/DenyRoutesToPrivilegedRolesFunctions |
| cloudops-dell2-agent-user | iam:CreateRole | arn:aws:iam::313476888478:role/opal-portal-lambda-role | explicitDeny | cloudops-dell-agent-deploy-policy/DenyEveryIamWrite |

10/10 arms passed; 3/3 administrator positive controls passed on the same denied actions/resources. Resource-existence metadata saved; x.py is a prospective object, simulation only.

AC1: POLICY-SIM allowed_ok=22/22 denied_ok=15/15 passrole_ok=5/5 protected_ok=8/8 freed_allowed=72/72 freed_excluded=3 undo_freed=167/167 undo_still_denied=443 selfsim_ok=9/9 ssm_ok=15/15 routes_freed=90/138 routes_still_refused=48 vendor_ok=245/245 all_ok=True

AC2: No changes. Your infrastructure matches the configuration. exit=0.

Wrapper WARN lines:
```
bash : safe-apply: [seat-gates] mode=WARN APPLY-WHO serial=0.7.0_AE_CloudOps kind=CLOUDOPS root=nfra-ctlpln-identity 
safe-apply: [seat-gates] mode=WARN CROSSBOX-DEPLOY device=laptop root=nfra-ctlpln-identity open_call=clear 
```

Ledger: org/critical_paths/change_management/20261008T1852Z_nfra-ctlpln-dell-step-d-laptop-20261008_deploy_completion.md (closure recorded below).
Proof: org\tier2_senior\0.7.0_AE_CloudOps\deliverables\NFRA_CTLPLN.TO-APPLY-17.dell-identity-step-d-routes-host-deny-off-apply-laptop.proof_of_spec.json

Preflight commit: 148d5e171f. Closure commit is the commit containing this report. No push performed; measured origin/CLOUD ec168357172e01485cc33d799b721c36d4ee950b.

Rollback: Re-apply root at merge first parent 049d81ffa6 via safe-apply, recreating same routes-host policy and attachment. Saved v1 document and attachment list: org\tier2_senior\0.7.0_AE_CloudOps\logs\2026-10-08\dell_step_d/before-iam.json. Cannot undo subsequent Dell code/document writes.

CTO notified 18:58:15Z; MSTR relay to Dell2 requested 18:58:18Z. Required warning: ssm:SendCommand on the 12 documents stays refused until cell D2 applies. Before any privileged code/document rewrite, Dell tells laptop first and waits for its answer. Simulation does not establish bucket/SCP permission or first use. Existing S24-S26 limitations remain; no new surprise.

Closure: all three ledger legs proven and entry CLOSED; sentinel removed. Full-name proof check VALID, zero violations. Readback 10/10, administrator controls 3/3, retained policies 6/6; re-plan exit=0. No push performed.
