# CTO never-widen half -- COMM_ASSIST round 18, cell CA-j-8: the narrowed-key resource policy (call 97c6)

**Signer:** `1.0.0_SA_CTO` (laptop, COMM_ASSIST owner) | **State: SIGNED 2026-10-14 ~05:4xZ, on the conditions below** | **Against:**
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R18B_KEY_DEPLOY_20261014.md` | **Pin:**
`3af44d523b` | **Ruling:** `CTO_RULING_20261014_052xZ_COMM_ASSIST_INGRESS_MARK_KEY_NARROWED.md`.

## Blast radius, signed

ONE key: `aws_secretsmanager_secret_policy.ca_ingress_mark`, expected `1/0/0`, with no code moving. It is one statement:
- Deny `secretsmanager:GetSecretValue` to `Principal *` on the mark's secret;
- unless `aws:PrincipalArn` equals `arn:aws:iam::313476888478:role/teams-global-chat-assist-role`, the one execution role both
  functions carry, read from the live configuration by the COO.

This NARROWS who may read the key's value. Management acts stay open (`PutSecretValue`, `PutResourcePolicy`, describe, delete).
Rollback: remove the policy (a targeted destroy of that one resource, or `delete-resource-policy`), which restores today's read set.

**Read by this seat at the pin:** the diff from `38ce5a7981` to `3af44d523b` over the root and the packaged set is
`chat_assist.tf` +17, this resource alone. `aws:PrincipalArn` resolves an assumed-role session to its role ARN, so the function
sessions match the condition. The role has no path, so the ARN form is exact.

**The failure that matters:** if the condition ever failed to match the function role, every text would break, because the producers
read the key on every text. Hence condition 1.

## Conditions

1. **After the apply, before anyone reports done:**
   - `simulate-principal-policy` (with the resource policy) reads `allowed` for the function role, and `explicitDeny` for
     `cloudops-dell1-agent-user` and `cloudops-dell2-agent-user`, for `GetSecretValue` on the secret;
   - within 10 minutes the ingress logs show `ingress_poll`, and at least one producer read of the key succeeds. That is either a
     `marks_seen` count advancing on a real text, or, with no text in the window, the handler's startup secret read logging no
     AccessDenied.

   Any AccessDenied for the function role means remove the policy at once and file a BLOCKING row.
2. The mode stays `record`. The enforce flip (CA-j-5) is its own pair and reads this policy live first.
3. Not 20:00Z-21:45Z, and no End of Day event in flight. The NEVER-2 entry is opened before the apply.

The PRD residual addendum is this seat's, landing with this sign-off.
