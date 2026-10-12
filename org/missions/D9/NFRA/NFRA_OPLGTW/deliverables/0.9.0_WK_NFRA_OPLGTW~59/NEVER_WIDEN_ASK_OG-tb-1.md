# Never-widen ask -- OG-tb-1, remove cloudops-dell-agents-group's read of `gateway/teams/bearer`

By: `0.9.0_WK_NFRA_OPLGTW~59` for `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O`. Order:
`org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-tb-1.teams-bearer-holders-read.md` (round 35, E3, row Z-S92).
Evidence: `TB1_READ.json` beside this file. Nothing is applied, changed or created; every call was a read.

Despite the name, this ask NARROWS access: it removes a grant. It needs the pair because it is an IAM change on a live policy.
Halves owed: `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O`, against this file at its commit. The applier is a later order.

## 1. What the read found (the CTO's ruling selects the "none" branch)

- **Window:** 90 days (2026-07-13 to 2026-10-11). The secret was created 2026-10-02, so the window covers its whole life.
- **Census:** CloudTrail `GetSecretValue`, us-east-1, fully paginated: 129,562 events across all secrets, of which **186** name
  `gateway/teams/bearer` (all with `secretId` exactly that name).
- **Readers (4 principals, 186 of 186):**

| Principal | Events |
|---|---|
| `arn:aws:sts::313476888478:assumed-role/teams-global-chat-assist-role/teams-global-chat-assist-ingress-lambda` | 138 (137 ok, 1 ResourceNotFoundException) |
| `arn:aws:sts::313476888478:assumed-role/opal-gateway-role/i-07dccb1615503ac99` | 22 |
| the account admin IAM user (ARN redacted in the record: it carries a person's name) | 14 |
| `arn:aws:sts::313476888478:assumed-role/teams-global-chat-assist-role/teams-global-chat-assist-handler-lambda` | 12 |

- **Positive control:** the gateway role read it (22 events). The read is sound.
- **Group verdict: `none`.** The group's two members (`cloudops-dell1-agent-user`, `cloudops-dell2-agent-user`) read it zero
  times, directly or through a role session. Limit, stated: a read through a role a member assumes would show as that role, and
  the only roles seen are the gateway role and the COMM_ASSIST role.

## 2. The grant path (the exact statement)

- The secret has **no resource policy** (`get-resource-policy` returned none).
- The group reaches it through ONE statement: managed policy `cloudops-dell-agent-platform-secrets-policy`
  (`arn:aws:iam::313476888478:policy/cloudops-dell-agent-platform-secrets-policy`, default version **v4**, created
  2026-10-09T12:21Z), Sid **`ReadPlatformKeys`**, `Allow`, `secretsmanager:GetSecretValue`, over 31 exact secret ARNs, of which
  one is `arn:aws:secretsmanager:us-east-1:313476888478:secret:gateway/teams/bearer-93ZHiU`.
- The policy is attached to `cloudops-dell-agents-group` only (1 group, 0 users, 0 roles). The group's other 8 attached policies
  carry no `GetSecretValue` on this secret; the group has no inline policy and neither member has one.

## 3. The change (exact)

Remove the one ARN `arn:aws:secretsmanager:us-east-1:313476888478:secret:gateway/teams/bearer-93ZHiU` from the `Resource` list of
`ReadPlatformKeys` (31 ARNs becomes 30). No action, effect or other resource changes. The gateway role, the COMM_ASSIST role and
the admin keep their own read; nothing is granted.

**How it lands:** the document is not hand-written. It is built by `module.routes_policy` from the secrets census, in
`infra/aws/terraform/nfra-ctlpln-identity/iam.tf` (`aws_iam_policy.dell_agent_platform_secrets`; its preconditions require the
census and the grant to agree). The ARN must therefore leave the census's platform-key grant class at the source, or the next
apply of that root puts it back. A live-only edit with no source change would drift and be reverted: the applier edits the census
classification, plans the root, and applies only the policy resource. Expected plan: `aws_iam_policy.dell_agent_platform_secrets`
in-place, 1 change, 0 add, 0 destroy; the description is a ForceNew field and must not change (see the comment at line 283).

## 4. Rollback (per key)

The managed policy has 4 versions (v1 to v4; the limit is 5). Applying creates v5 with the narrowed document.
Rollback is `aws iam set-default-policy-version --policy-arn arn:aws:iam::313476888478:policy/cloudops-dell-agent-platform-secrets-policy
--version-id v4`, which restores the 31-ARN grant at once and changes nothing else. If the apply ran from source, revert the census
classification in the same commit so the next plan agrees. The entry `ReadPlatformKeys` is the only key touched.

## 5. Blast radius (what the act may touch)

- **Touches:** read of ONE secret by the two dell agent users. Measured use: 0 reads in 90 days (the secret's whole life).
- **Does not touch:** any other secret in the 31, the group's other policies, the gateway, COMM_ASSIST, the admin, or the secret itself.
- **Consequence check before applying:** a dell agent that today shells a Teams route needing this bearer would lose it; none did
  in the window, and the three routes OG-ap-7 added are served by the gateway, which holds its own read.

## 6. Remaining holders and their reasons

| Holder | Reason it keeps the read |
|---|---|
| `opal-gateway-role` | The gateway serves the Teams routes and reads the bearer itself (22 reads; the positive control). |
| `teams-global-chat-assist-role` (ingress and handler Lambdas) | COMM_ASSIST's own consumer (150 reads: 138 ingress, 12 handler), its own grant. |
| the account admin IAM user | Account admin, not a group member; 14 reads over the window. The admin's own reason was not measured here, and narrowing admin is outside this cell. |

## 7. Decision wanted

Approve (or refuse) removing the one ARN from `ReadPlatformKeys` per section 3, with the rollback in section 4.
Because the verdict is `none`, the "found" branch (a separate bearer for a group consumer) does not arise.
