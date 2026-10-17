# The Inflection gold bucket's fence blocks the runner role: the signed Inflection pair would fail at Act 7 (read by 2.0.0_SA_COO~F2, 2026-10-17 ~12:3xZ)

Read-only (live GETs and `iam simulate-principal-policy`, no change). Counts, names and decisions only.

## What was read

- **The bucket policy of `opal-data-inflection`** (`get-bucket-policy`): its first statement `DenyForeignFirmPrincipals` is `Deny s3:*` on the bucket and its objects with `ArnNotLike aws:PrincipalArn` over a list: `arn:aws:iam::313476888478:role/*-inf-*`, three operator users, `role/irpt-holdings-role`, `role/irpt-performance-adapter-role`, `role/opal-ticket-api-role`, two cloudops agent users. The runner role is `role/inf-gold-layer-ec2-role`: its name carries `inf-` at the START, so it does NOT match `*-inf-*` (the pattern needs a hyphen before `inf`), and it is on no other list. The Deny therefore applies to it for EVERY action, whatever its identity policy allows.
- **The bucket's other statements** are scoped exemptions for the performance adapter and the ticket role (Deny of any other action or prefix, Allow of the one prefix).
- **The fence's own registry** (`infra/logic/registry/exemptions.json`, per firm bucket): "each principal exempt from its DenyForeignFirmPrincipals, with the reason and the never-widen sign-off that admits it; the policy's exemption list is generated from these rows and never typed". The Inflection bucket carries one row (the operator user); no row names the runner role.

## The what-if (the planned four-statement policy attached, the live bucket policy supplied as the resource policy)

| call | without the resource policy | with the live bucket policy |
|---|---|---|
| `s3:PutObject` at the gold prefix `irpt/inflection/gold/account_transaction/` | allowed | **explicitDeny, matched statement: ResourcePolicy** |
| `s3:GetObject`/`ListBucket` of the Orion silver prefix in `opal-data-assets` (S1, S2) | allowed | allowed (the assets bucket policy does not block it) |
| Cottonwood landing role `s3:PutObject` at the NEW `irpt/cottonwood/gold/account_transaction/` (planned statement) | allowed | allowed (control: the live `account_return_daily` statement answers the same) |

So the Cottonwood pair and the 49 Financial side are not affected; the Inflection pair's WRITE (Act 7) and its S4 list would be refused by the bucket's fence even after Act 2, and Act 3's simulation as written in the signed packet (no resource policy) would read ALLOW for the same call: a false green.

## What is not established

Whether the runner role also needs the exemption for `ListBucket` on the gold bucket (yes by the same Deny); whether other principals the pair uses (the instance profile's session) evaluate as the role ARN (they do for an assumed-role session); how the fence's generator turns a registry row into a scoped Allow (the performance adapter's scoped exemption is the model, `grants` in the registry); which seat applies the shared-infra root (`infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf`).

## Routes

- **A (REC):** a registry exemption row for `inf-gold-layer-ec2-role` on `opal-data-inflection`, scoped by a grants row to `s3:PutObject` and `s3:ListBucket` on the one gold prefix `irpt/inflection/gold/account_transaction/` (the scoped-exemption form the adapter and ticket roles have), with its never-widen sign-off, applied by `safe-apply` of the shared-infra root before Act 4 of the Inflection pair; Act 3's simulation then runs WITH the bucket policy as the resource policy.
- **B:** a new role whose name carries the scope token (`...-inf-...`) in place of the existing runner role: a larger change (instance profile, trust, every policy of the old role).

-- 2.0.0_SA_COO~F2
