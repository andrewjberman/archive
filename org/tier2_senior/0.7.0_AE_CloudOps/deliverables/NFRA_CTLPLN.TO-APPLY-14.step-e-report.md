# Dell identity step E: APPLIED

Applied on laptop at **2026-10-08T18:00:17Z**, confirmed by all five CloudTrail IAM events in `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-10-08/dell_step_e/apply-cloudtrail.json`. One safe-apply: **2 added, 3 changed, 0 destroyed**, exit 0. No secret value was read and no resource-policy call was made. Status **APPLIED, not EXERCISED** until a graph query from each Dell is reported.

## Authority and exact gate

GO Msg-ID 107058; shared CLOUD HEAD 049d81ffa65d1128a8b29322c32a259642eee008 contained merge e80238bdab and the identity root was clean. COO half `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_E_TWO_GRANTS_WIDENED_20261008.md` @9a8758bddf and CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_E_TWO_GRANTS_WIDENED_20261008.md` @ee3578d886 are signed and were read in full. Both Dell before-rule ACKs are confirmed in the GO. Andrew was informed in this turn that Dell agents may use platform credentials and change the named shared-resource permissions.

Immediately before the plan:

```text
POLICY-SIM allowed_ok=22/22 denied_ok=15/15 passrole_ok=5/5 protected_ok=8/8 freed_allowed=72/72 freed_excluded=3 undo_freed=167/167 undo_still_denied=443 selfsim_ok=9/9 ssm_ok=15/15 routes_ok=5/5 vendor_ok=245/245 all_ok=True
```

The saved untargeted/default-variable plan changed exactly `aws_iam_policy.dell_agent_deploy`, `aws_iam_policy.dell_agent_create`, and `aws_iam_policy.dell_agent_respol_allow[0]`; created only `aws_iam_policy.dell_agent_platform_secrets[0]` and its group attachment. Added-line counts: **28** secret ARNs; **0** quoted `iam:` actions; **0** `secretsmanager:PutResourcePolicy`; **0** `secretsmanager:DeleteResourcePolicy`. No routes or vendor-secret-policy change. Plan SHA256 `674e6eda03b3eb8febe6c359b709fa73f3bd1d12a6686f2e965a08743fee39ec`.

## Before, rollback and result

Before attachment list and policy documents: `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-10-08/dell_step_e/before-iam.json` (six policies). Saved defaults: deploy **v3**, create **v2**, respol-allow **v1**. After defaults: deploy **v4**, create **v3**, respol-allow **v2**; new platform-secret policy **v1**. All three old versions remain available with equal documents. Rollback remains detach/delete the new policy and restore the three saved defaults, or safe-apply this root at `e80238bdab^1`. This does not undo secret reads or subsequent resource-policy changes by Dell agents.

Live group attachments, **7/7**:

- cloudops-dell-agent-routes-host-policy
- cloudops-dell-agent-create-policy
- cloudops-dell-agent-platform-secrets-policy
- cloudops-dell-agent-respol-allow-policy
- cloudops-dell-agent-deploy-policy
- cloudops-dell-agent-routes-fn-policy
- cloudops-dell-agent-vendor-secrets-policy

Live policy documents match the saved plan **10/10**, including unchanged routes/vendor/bus/SSM policies. Re-plan: **No changes. Your infrastructure matches the configuration. exit=0**; the exact AC2 shell invocation was run from `ac2.sh` and is captured in `ac2.txt`.

## Live simulator evidence

All **26/26** arms passed, one resource ARN per `aws iam simulate-principal-policy` invocation. All **6/6** denied-action positive controls against the administrator independently returned allowed with no missing context. Named statements are resolved from the AWS returned source-policy positions into the live policy documents, with a uniqueness assertion; no attribution is inferred from only a policy name. Secret/queue/function/trail/bucket/role existence was read without values or resource policies. `cloudtrail:PutResourcePolicy` uses `*` as an action-grant simulation and is not an API exercise against a particular resource.

| User | Action | Resource | Decision | Every matched statement |
|---|---|---|---|---|
| cloudops-dell1-agent-user | `secretsmanager:GetSecretValue` | `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/mcp/graph-read-token-MGAqlV` | allowed | cloudops-dell-agent-platform-secrets-policy/ReadPlatformKeys |
| cloudops-dell1-agent-user | `cloudtrail:PutResourcePolicy` | `*` | allowed | cloudops-dell-agent-respol-allow-policy/AllowResourcePolicyChanges |
| cloudops-dell1-agent-user | `s3:PutBucketPolicy` | `arn:aws:s3:::opal-cloudtrail-logs-313476888478` | allowed | cloudops-dell-agent-respol-allow-policy/AllowResourcePolicyChanges |
| cloudops-dell1-agent-user | `lambda:AddPermission` | `arn:aws:lambda:us-east-1:313476888478:function:opal-portal-rest-authorizer` | allowed | cloudops-dell-agent-respol-allow-policy/AllowResourcePolicyChanges |
| cloudops-dell1-agent-user | `sqs:SetQueueAttributes` | `arn:aws:sqs:us-east-1:313476888478:agentbus-global-dell1-queue.fifo` | allowed | cloudops-dell-agent-respol-allow-policy/AllowResourcePolicyChanges; cloudops-dell-agent-create-policy/CreateUpdateTagDataAndMessaging |
| cloudops-dell1-agent-user | `cloudtrail:StopLogging` | `arn:aws:cloudtrail:us-east-1:313476888478:trail/opal-organization-trail` | explicitDeny | cloudops-dell-agent-deploy-policy/DenyCloudTrailWrites |
| cloudops-dell1-agent-user | `s3:PutLifecycleConfiguration` | `arn:aws:s3:::opal-cloudtrail-logs-313476888478` | explicitDeny | cloudops-dell-agent-create-policy/DenyAuditTrailBucketWrites |
| cloudops-dell1-agent-user | `lambda:UpdateFunctionCode` | `arn:aws:lambda:us-east-1:313476888478:function:opal-portal-rest-authorizer` | explicitDeny | cloudops-dell-agent-deploy-policy/DenyProtectedFunctions; cloudops-dell-agent-routes-fn-policy/DenyRoutesToPrivilegedRolesFunctions |
| cloudops-dell1-agent-user | `secretsmanager:GetSecretValue` | `arn:aws:secretsmanager:us-east-1:313476888478:secret:schwab/sdd/session-u8RHot` | implicitDeny | NONE: no identity Allow (implicitDeny) |
| cloudops-dell1-agent-user | `secretsmanager:GetSecretValue` | `arn:aws:secretsmanager:us-east-1:313476888478:secret:blackdiamond/49f/otp-relay-hDQMS5` | implicitDeny | NONE: no identity Allow (implicitDeny) |
| cloudops-dell1-agent-user | `iam:CreateRole` | `arn:aws:iam::313476888478:role/opal-portal-lambda-role` | explicitDeny | cloudops-dell-agent-deploy-policy/DenyEveryIamWrite |
| cloudops-dell1-agent-user | `sqs:ReceiveMessage` | `arn:aws:sqs:us-east-1:313476888478:agentbus-global-dell1-queue.fifo` | allowed | cloudops-dell1-agent-bus-policy/ReceiveOwnInboundQueueOnly |
| cloudops-dell1-agent-user | `sqs:SendMessage` | `arn:aws:sqs:us-east-1:313476888478:agentbus-global-dell2-queue.fifo` | allowed | cloudops-dell-agent-deploy-policy/AgentbusSendToInboundQueues |
| cloudops-dell2-agent-user | `secretsmanager:GetSecretValue` | `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/mcp/graph-read-token-MGAqlV` | allowed | cloudops-dell-agent-platform-secrets-policy/ReadPlatformKeys |
| cloudops-dell2-agent-user | `cloudtrail:PutResourcePolicy` | `*` | allowed | cloudops-dell-agent-respol-allow-policy/AllowResourcePolicyChanges |
| cloudops-dell2-agent-user | `s3:PutBucketPolicy` | `arn:aws:s3:::opal-cloudtrail-logs-313476888478` | allowed | cloudops-dell-agent-respol-allow-policy/AllowResourcePolicyChanges |
| cloudops-dell2-agent-user | `lambda:AddPermission` | `arn:aws:lambda:us-east-1:313476888478:function:opal-portal-rest-authorizer` | allowed | cloudops-dell-agent-respol-allow-policy/AllowResourcePolicyChanges |
| cloudops-dell2-agent-user | `sqs:SetQueueAttributes` | `arn:aws:sqs:us-east-1:313476888478:agentbus-global-dell1-queue.fifo` | allowed | cloudops-dell-agent-respol-allow-policy/AllowResourcePolicyChanges; cloudops-dell-agent-create-policy/CreateUpdateTagDataAndMessaging |
| cloudops-dell2-agent-user | `cloudtrail:StopLogging` | `arn:aws:cloudtrail:us-east-1:313476888478:trail/opal-organization-trail` | explicitDeny | cloudops-dell-agent-deploy-policy/DenyCloudTrailWrites |
| cloudops-dell2-agent-user | `s3:PutLifecycleConfiguration` | `arn:aws:s3:::opal-cloudtrail-logs-313476888478` | explicitDeny | cloudops-dell-agent-create-policy/DenyAuditTrailBucketWrites |
| cloudops-dell2-agent-user | `lambda:UpdateFunctionCode` | `arn:aws:lambda:us-east-1:313476888478:function:opal-portal-rest-authorizer` | explicitDeny | cloudops-dell-agent-deploy-policy/DenyProtectedFunctions; cloudops-dell-agent-routes-fn-policy/DenyRoutesToPrivilegedRolesFunctions |
| cloudops-dell2-agent-user | `secretsmanager:GetSecretValue` | `arn:aws:secretsmanager:us-east-1:313476888478:secret:schwab/sdd/session-u8RHot` | implicitDeny | NONE: no identity Allow (implicitDeny) |
| cloudops-dell2-agent-user | `secretsmanager:GetSecretValue` | `arn:aws:secretsmanager:us-east-1:313476888478:secret:blackdiamond/49f/otp-relay-hDQMS5` | implicitDeny | NONE: no identity Allow (implicitDeny) |
| cloudops-dell2-agent-user | `iam:CreateRole` | `arn:aws:iam::313476888478:role/opal-portal-lambda-role` | explicitDeny | cloudops-dell-agent-deploy-policy/DenyEveryIamWrite |
| cloudops-dell2-agent-user | `sqs:ReceiveMessage` | `arn:aws:sqs:us-east-1:313476888478:agentbus-global-dell2-queue.fifo` | allowed | cloudops-dell2-agent-bus-policy/ReceiveOwnInboundQueueOnly |
| cloudops-dell2-agent-user | `sqs:SendMessage` | `arn:aws:sqs:us-east-1:313476888478:agentbus-global-dell1-queue.fifo` | allowed | cloudops-dell-agent-deploy-policy/AgentbusSendToInboundQueues |

Raw decisions, controls and policy comparison: `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-10-08/dell_step_e/readback.json`. Metadata/existence: `resource-existence.json`; after attachments/documents: `after-iam.json`. The identity simulator does not prove organization policies, resource policies or either Dell's own first use.

## Wrapper, proof and closure

Seat-gate lines (WARN is the gate mode, not a failure):

```text
safe-apply: [seat-gates] mode=WARN APPLY-WHO serial=0.7.0_AE_CloudOps kind=CLOUDOPS root=nfra-ctlpln-identity verdict=ADMITTED reason=a CLOUDOPS seat applies
safe-apply: [seat-gates] mode=WARN CROSSBOX-DEPLOY device=laptop root=nfra-ctlpln-identity open_call=clear overlap=clear upset=clear open_deploy=clear verdict=CLEAR
```

Naming policy checks passed; IAM_USER names were outside its grading domain. Tag authorization gate SKIP: no provider default_tags across 3 files. Tombstone gate checked 2 additions against 7 tombstones and was clean. No gate override. PowerShell rendered native stderr as a NativeCommandError record, but the wrapper's actual exit was 0. Verification runner initially needed the Windows `aws.cmd` shim and removal of a CLI-v2-only flag; final CLI-v1 run passed. A Python-launched bare Bash selected the unused WSL stub; the exact AC2 command succeeded through PowerShell's resolved Git Bash. Neither instrument issue triggered another apply.

Ledger: `org/critical_paths/change_management/20261008T1757Z_nfra-ctlpln-dell-step-e-laptop-20261008_deploy_completion.md` (CLOSED; all three legs proven, sentinel removed). Proof instance: `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_CTLPLN.TO-APPLY-14.dell-identity-step-e-two-grants-widened-apply-laptop.proof_of_spec.json`. No policy/Terraform/test source edits. No surprise rows filed: no live plan or permission discrepancy. Preflight commit `4522e616b7`; final evidence commit supplied in the closure message. Push state **LOCAL**, no shared-branch push; origin CLOUD measured `ce49f7adec510ebdf123c1b5682596ba2dd2af58`. No post-apply rollback was needed.
