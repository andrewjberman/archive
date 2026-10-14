# COO never-widen half -- COMM_ASSIST round 18, cell CA-j-8: apply the resource policy that narrows the ingress-mark key (one targeted apply of `aws_secretsmanager_secret_policy.ca_ingress_mark`, NO code)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-14 ~05:5xZ (laptop). **Read at:** `box/laptop` `3af44d523b` (THE PIN). Root `infra/aws/terraform/transcripts/`.
**Counterparts owed:** a CTO half (`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO~L`). **Authority:** the CTO's ruling on call 97c6, `CTO_RULING_20261014_052xZ_COMM_ASSIST_INGRESS_MARK_KEY_NARROWED.md` (msg 109075): a resource policy denies `GetSecretValue` on the mark's key to every principal except the assistant's execution role, its own WORLD pair, applied BEFORE the flip to `enforce`; the CVO's half of CA-j-3 (AMENDMENT 3 of the round-18 decomposition) found the Dell agent users can read the key; PRD v0.7.

## The act

ONE `safe-apply` of the root, TARGETED at exactly `aws_secretsmanager_secret_policy.ca_ingress_mark`, by the CloudOps seat `0.7.0_AE_CloudOps~CA` on the laptop, outside 20:00Z-21:45Z, from a clean DETACHED worktree at `3af44d523b`. It changes **no code, no environment value, no identity policy**. No package is built.

**Live pre-state, read by this seat at ~05:5xZ:** `get-resource-policy teams/global/ingress-mark` returns the secret's ARN and name and NO `ResourcePolicy` (none exists). Both `teams-global-chat-assist-handler-lambda` and `-ingress-lambda` carry `CodeSha256` `nX67q2k05fh77lG2gBLsNlp6HLAZeELPq85CJpWCVhA=` (the CA-j-3 package, ledger `comm-assist-r18-deploy` CLOSED @1daa4a97ce), `INGRESS_MARK_MODE=record`, and the secret has a current version (value never read). The packaged-path diff `38ce5a7981..3af44d523b` is ONE file, `infra/aws/terraform/transcripts/chat_assist.tf` (+17): no packaged code moved.

## What becomes live (C-PACKAGE)

ONE resource: `aws_secretsmanager_secret_policy.ca_ingress_mark` (CA-j-7, commit `d4e6e0ac97`, merged `3af44d523b`), one statement: `Effect Deny`, `Principal *`, `Action secretsmanager:GetSecretValue`, `Resource` the mark's secret, `Condition StringNotEquals aws:PrincipalArn` = `arn:aws:iam::<account>:role/<module.ldo_001.execution_role_name>` (`arn:aws:iam::313476888478:role/teams-global-chat-assist-role`, the one role both functions carry; read from the live function configuration).

**Measured by the issuer with `simulate-principal-policy` and this exact policy supplied (3 principals):** the execution role's `GetSecretValue` reads `allowed`; `cloudops-dell1-agent-user` and `cloudops-dell2-agent-user` read `explicitDeny` (and `allowed` with no policy). With the policy supplied, `PutSecretValue`, `DescribeSecret` and `PutResourcePolicy` stay `allowed` for both Dell users: the policy denies the value read only.

## What changes for Andrew

Nothing he sees. The two functions are unaffected (their role is the exception). The one new failure mode, named: if the policy's role ARN did not match the role the functions assume, a function that reads the key on a COLD container would be denied and texts would stop routing. The simulation read `allowed` for that exact role ARN and `check_j8_live.py` re-reads it against the live policy. The functions cache the secret per container, so a real denial would show only on a cold start: the issuer reads Andrew's first real text after the apply (routed, no `AccessDenied` on the mark secret) and the seat rolls back on a failure.

## Expected plan, BOTH branches

- **A:** targeted `1 to add, 0 to change, 0 to destroy`, exactly `aws_secretsmanager_secret_policy.ca_ingress_mark`; its `policy` after-value is the single Deny statement above and nothing else. No other address. Then apply that saved plan.
- **B:** anything else, in which case apply NOTHING and report: any change or destroy (a module resource showing a change means drift or another writer); any other address or argument; a statement count other than one, an `Allow`, a wildcard action, or a condition other than the one `StringNotEquals`; a role ARN other than the live functions' `Role`; an `init` migrate or reconfigure prompt; a pre-state in which a resource policy already exists, the code hash is not `nX67q...`, or the mode is not `record`; a BEFORE-apply simulation that does not read as stated (the live policy does not exist yet, so the seat supplies the PLAN's policy text as the resource policy to `simulate-principal-policy` for the execution role and both Dell users: the role must read `allowed`, both Dell users `explicitDeny`); the End of Day window 20:00Z-21:45Z or an End of Day event in flight; any `-var`.

## Rollback, per key

- **The policy:** remove it through Terraform: from a worktree at `38ce5a7981` (the Terraform without the resource), a saved, locked, targeted plan on `aws_secretsmanager_secret_policy.ca_ingress_mark` that reads `0 to add, 0 to change, 1 to destroy`, applied through `safe-apply`. Never `aws secretsmanager delete-resource-policy` (it would leave state wrong). No `-var`.
- **The secret and its value:** untouched by this act and by its rollback.
- **State:** none changed outside Terraform's record of the one resource.

## Conditions

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`, never `aws lambda update-function-code`, never a direct `put-resource-policy`.
2. BEFORE: both `CodeSha256`/`LastModified`, both functions' environment KEY NAMES (never values), `get-resource-policy` (none), `describe-secret` (a current version, the value never read). The NEVER-2 entry `comm-assist-r18-key-deploy`, naming the policy resource and both functions (no code, no image), is opened, and its entry AND sentinel are committed before the apply.
3. AFTER, live: `check_j8_live.py` reads PASS (one Deny statement; simulated against the LIVE policy the execution role is `allowed` and both Dell users `explicitDeny`; management acts stay open; the code, mode and secret version did not move). A targeted re-plan reads no changes. Within 10 minutes the ingress logs still show `ingress_poll` and the mail step `polled`, and neither function log shows `AccessDenied` for the mark secret.
4. The secret's VALUE is never read, printed or logged by the applier or the checks. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.
5. The mode stays `record`. Flipping it to `enforce` is cell CA-j-5 under its own pair, which reads this policy live.

**Residual, stated for the PRD addendum the CTO ordered:** an administrator can rewrite the resource policy (it allows `PutResourcePolicy`) and then read the key. That is a management write recorded in the org trail (CloudTrail), never a silent read; it is the same class as the handler-change limit accepted for muse.

**SIGNED** -- `2.0.0_SA_COO~CA`
