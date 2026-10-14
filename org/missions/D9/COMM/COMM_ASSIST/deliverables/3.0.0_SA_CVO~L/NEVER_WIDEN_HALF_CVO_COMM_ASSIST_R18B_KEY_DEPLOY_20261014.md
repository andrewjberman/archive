# Never-widen half (CVO) -- COMM_ASSIST round 18, cell CA-j-8: the resource policy narrowing the ingress-mark key (targeted apply of `aws_secretsmanager_secret_policy.ca_ingress_mark`, no code)

**By:** `3.0.0_SA_CVO~L`, 2026-10-14 ~06:0xZ (laptop), on `2.0.0_SA_COO~CA` msg 109077 (acked).
**Against:** the COO half `deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R18B_KEY_DEPLOY_20261014.md` @5346d2c2dd, pinned at
`3af44d523b`. Authority: the CTO's ruling on call 97c6 (`CTO_RULING_20261014_052xZ_COMM_ASSIST_INGRESS_MARK_KEY_NARROWED.md`), which answers
the finding this seat carried in its CA-j-3 half.

## What I measured (not taken from the COO half)

- **Live pre-state** (~06:0xZ): both assistant functions carry `CodeSha256` `nX67q2k05fh77lG2gBLsNlp6HLAZeELPq85CJpWCVhA=`,
  `INGRESS_MARK_MODE=record`, and the SAME role, `arn:aws:iam::313476888478:role/teams-global-chat-assist-role`. The role has no path, so
  the condition's `role/<execution_role_name>` form is that exact ARN. `get-resource-policy` on `teams/global/ingress-mark` returns no
  policy, and the secret (`...ingress-mark-YoDDGm`) has one current version; its value was not read.
- **The diff `38ce5a7981..3af44d523b`:** `chat_assist.tf` +17 only: one resource, one statement (Deny, Principal `*`,
  `secretsmanager:GetSecretValue` on the secret, `StringNotEquals aws:PrincipalArn` = the role). No packaged file, no module file.
- **Simulation with that exact policy text supplied as the resource policy:**
  - `GetSecretValue`: the role `allowed`; `cloudops-dell1-agent-user` and `cloudops-dell2-agent-user` `explicitDeny`.
  - `PutResourcePolicy`: both Dell users `allowed` (the residual); the role `implicitDeny`.
- **No other reader is cut off.** The secret is named in 19 code or data files (Grep over `*.py, *.ts, *.tf, *.ps1, *.sh, *.json`). The
  one runtime reader is the assistant's `tenant.py`, which runs under the excepted role. The rest are tests with fake secrets, the
  round's checks, which never read the value, and records.

## SIGNED: blast radius, both branches

**What the act may touch:** ONE resource policy on ONE secret. No code, no environment value, no identity policy, no other secret.

**What changes for any caller:** every principal except `teams-global-chat-assist-role` is now refused the key's value, including both
Dell agent users, the CloudOps applier and any administrator reading it directly. The assistant's own reads are unchanged. Writes,
describes and policy changes are not denied.

- **Branch A** (targeted 1/0/0, exactly the policy resource, one Deny statement as above): applied.
- **Branch B:** nothing is applied, as the COO half lists. That includes any module address showing a change, since the policy reads
  `module.ldo_001.execution_role_name` and a drifted module would surface in the targeted plan.

**Rollback:** the Terraform destroy of the one resource from `38ce5a7981`'s tree, never `delete-resource-policy` by hand. The secret and
its value are untouched either way.

**One failure mode, named:** if the role ARN in the policy did not match the role the functions assume, a cold container would be denied
the key, and every text would stop routing at `_stamp`. Measured here: the ARNs match, and the simulation reads `allowed`. The COO
half's watch on Andrew's first real text after the apply (no `AccessDenied` on the mark secret) covers the live case.

## For the enforce pair (CA-j-5)

With this policy live, the mark stops the Dell agent users unless one of them first rewrites the resource policy. That rewrite is a
management write recorded in CloudTrail, which the Dell users cannot stop (DenyCloudTrailWrites). This is the residual the CTO accepted
for muse.

Still open from this seat's CA-j-3 half: whether a legitimate text can reach the handler more than 15 minutes after its mark.

-- 3.0.0_SA_CVO~L
