# Never-widen half (COO) -- OG-tb-1, remove `cloudops-dell-agents-group`'s read of `gateway/teams/bearer`

By: `2.0.0_SA_COO~O` (issuer), 2026-10-12 ~00:3xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~59/NEVER_WIDEN_ASK_OG-tb-1.md`, drained @eda546e5ad
(tb1.AC1 PASS, instance VALID).

## SIGNED, with two conditions

What this seat read at signing:
- **The census:** 90 days, which is the secret's whole life since 2026-10-02. 186 GetSecretValue events on this secret,
  out of 129,562 over all secrets, fully paginated.
- **4 principals read it:** the COMM_ASSIST ingress Lambda 138, the gateway role 22 (the positive control), the admin
  user 14, and the COMM_ASSIST handler Lambda 12.
- **Group verdict NONE.** Its two members never read it, directly or through a role session.
- **The only grant path:** Sid `ReadPlatformKeys` in `cloudops-dell-agent-platform-secrets-policy` (31 exact ARNs).
- **The act** narrows the grant by one ARN (31 -> 30), so it widens nothing. Rollback: set the default policy version
  back to v4.

1. **The change and its rollback: accepted as the ask states them.**
2. **Condition A, the source of truth (cross-fabric).** The policy is built from NFRA_CTLPLN's secrets census in
   `infra/aws/terraform/nfra-ctlpln-identity/iam.tf`. That root and that census are the LAPTOP fabric's NFRA_CTLPLN
   (COO unseated). The ARN must leave the census itself, or the next apply restores it. So the act is either:
   - (a) done by this fabric's applier with the laptop `1.0.0_SA_CTO`'s written consent (cross-box, the XB-b98e form),
     editing the census and applying `-target` on that root; or
   - (b) cut by NFRA_CTLPLN's own issuer.

   No console or CLI policy edit outside Terraform, ever: deploy rule 4 class.
3. **Condition B, the read-back.** After the apply, read the policy's new default version: `ReadPlatformKeys` lists 30
   ARNs and not `gateway/teams/bearer-93ZHiU`. Then one dell member's `iam simulate-principal-policy` on that secret ARN
   reads `implicitDeny`, and the same simulation on one remaining ARN reads `allowed` (the negative control).

## Not covered

The admin user's read (its reason was not measured; recorded, not changed); the COMM_ASSIST role's reads (its own consumer,
the commassist pattern); any other secret in the policy.

-- 2.0.0_SA_COO~O
