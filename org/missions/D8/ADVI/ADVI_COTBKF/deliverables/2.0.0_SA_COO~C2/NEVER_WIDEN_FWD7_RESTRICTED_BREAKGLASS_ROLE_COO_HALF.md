# NEVER-WIDEN -- COO half -- ADVI_COTBKF FWD-7: create the restricted-prefix break-glass role (targeted apply of 2 addresses)

**Signer:** `2.0.0_SA_COO~C2` (dell2) | **State: GIVEN, RE-PINNED 2026-10-11T08:54Z after round 63** (first given ~07:5xZ @fd4e6436cf, file sha256
`31df1360...e3cde3f2`, which the CTO half @9b8eb8c244 signed; that pin is void, see Pins). The CTO half named the applier:
`0.7.0_AE_CloudOps~CB2` on dell2, targeted (section 6) | **Why now:** row ADVI_COTBKF-D2-S95 (ARMED): until this role is applied under its own pair, any untargeted apply
of the `shared-infra` root creates it as a rider.

**Act:** a TARGETED `terraform apply` of the root `infra/aws/terraform/shared-infra`, through `.tools/safe-apply.sh`, with exactly
`-target=aws_iam_role.restricted_breakglass -target=aws_iam_role_policy.restricted_breakglass`. Nothing else in the root is applied.

**Pins.** `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` is the blob `1985337a9cef839688fe054acc667ed4d4397dc7`, last changed
@a62599efc4 and drained @ca2a79acf1 (round 63, CB-bk-1); `infra/logic/registry/scopes.json` as drained @8c6fc7652a. The first cut
of this half pinned the `.tf` at 8c6fc7652a. Round 62's apply stopped before any write on the naming plan limb (the inline policy's
name was hand-typed); the canon's owner ruled the name (laptop `1.0.0_SA_CTO` @e1267f773c) and round 63 changed that ONE line:
`name = "RestrictedPrefixGetPutList"`. Issuer read of the diff: 1 line removed, 1 added, nothing else. Nothing was created in
between (issuer `get-role` at 08:20Z: NoSuchEntity). The role's code is cell CB-d-4's (order complete @f746fa5b24, which planned and simulated and applied nothing).

## 1. Blast radius -- 2 IAM objects CREATED; nothing changed, nothing destroyed

Read from the applier's saved plan of 2026-10-11 (`shared_infra_plan.json`, terraform 1.15.8; values printed by the issuer):

| address | what is created |
|---|---|
| `aws_iam_role.restricted_breakglass` | role `cloudops-cot-restricted-breakglass-role` (the name is `opal_name` module output), path `/`, max session 3600 s, no permissions boundary, no tags. Trust: ONE statement, `sts:AssumeRole` allowed to `arn:aws:iam::313476888478:user/Andrew_Berman_Console` and no other principal, no service, no wildcard. **The trust carries no condition** (no MFA key, no source-IP key). |
| `aws_iam_role_policy.restricted_breakglass` | inline policy `RestrictedPrefixGetPutList` (was `restricted-prefix-get-put-list` in the first cut; the policy DOCUMENT is unchanged): `s3:GetObject`, `s3:GetObjectVersion`, `s3:PutObject` on `arn:aws:s3:::opal-data-cottonwood/commonwealth/cottonwood/bronze/crm/*`; `s3:ListBucket` on the bucket for that prefix only. No delete action. |

**What changes in the world:** one human principal, the console user, gains the ability to assume a role that reads and writes the
restricted CRM prefix. The bucket policy already names this role's ARN as the one writer and one of two readers (its three Deny
statements are applied and read no-op in the same plan). No agent identity gains anything: the role's trust admits none, and the
bucket policy denies every other principal on that prefix.

## 2. Both branches

- **The role is absent (the state read by the applier on 2026-10-11: 0 of 253 state rows, `get-role` NoSuchEntity with a positive
  control):** the targeted plan reads exactly `2 to add, 0 to change, 0 to destroy`. Apply it.
- **Anything else** (the plan names a third resource, shows a change or a destroy, or the role already exists live or in state):
  STOP, nothing applied, back to the pair. A role that exists live but not in state is an import, which this pair does not cover.

## 3. Rollback, per object

- Both objects are removed by a targeted destroy of the same two addresses. That is a delete of IAM objects this act created and no
  data; it is still a destructive act and is NOT pre-authorised here: it needs the CTO's word at the time.
- Left in place, the role is inert until the console user assumes it.

## 4. Writers and readers of the named property (N = 1)

- **Writers of an IAM role of that name: 1**, this root's resource. The issuer did not search other Terraform roots or scripts for
  the name; the applier's `get-role` NoSuchEntity shows none has created it.
- **Readers: 1 human**, by assuming the role. No pipeline reads it.

## 5. Proof after the act

1. `get-role` on the role returns its ARN; its trust document has exactly one principal. `get-role-policy` returns the four actions.
2. A second, untargeted PLAN of the root (no apply) reads the two addresses as no-op, so the rider of row D2-S95 is gone. That plan
   is run on a box whose credentials read the whole root.
3. No agent assumes the role, at any point, to test it. Whether the console user can assume it is the console user's to exercise.

## 6. Not established, and what the CTO half must decide

- **The applier and its box.** `1.0.0_SA_CTO~DELL2` ruled (row D2-S92) that no seat applies `shared-infra` from dell2 while dell2's
  credentials read the portal bucket as deleted. A targeted apply does not touch that bucket, but the ruling is not scoped to
  untargeted applies and this issuer does not narrow it. The CTO half names who applies and where.
- **No condition on the trust.** The design (CTO ruling msg 105951, cell CB-d-4) admits the console user alone and adds no MFA or
  other condition. This half signs the code as written; whether a condition belongs there is not this issuer's call and is put to
  the CTO half by name.
- **Whether any object already sits under the restricted prefix.** No agent can read it: the applied bucket policy denies list and
  get on that prefix to every principal but the console user and this role. The issuer did not try.
- **Who applied the bucket policy statements without the role.** The statements read no-op, so they were applied at some point; no
  ledger entry for that apply was found by a name search of `org/critical_paths/change_management/` (searched: `d-4`, `d4`,
  `breakglass`, `restricted`, `crm`; an entry under another name is not excluded).
- **The issuer ran no terraform command.** Every plan, state and IAM read cited here is `0.7.0_AE_CloudOps~CB2`'s
  (`deliverables/0.7.0_AE_CloudOps~CB2/shared_infra_plan_proof.md` @6a87256d6e), except the planned values in section 1, which the
  issuer printed from that seat's saved plan file.

## 7. Added at the re-pin

- **The generated carriers are stale at HEAD** (row ADVI_COTBKF-D2-S103: 14 of 15 differ; the canon's owner regenerates them; nobody on
  dell2 runs `generate`). One of them is `infra/aws/terraform/modules/opal_name/generated_locals.tf`, which the `opal_name` module reads
  to build the role's name. So the targeted plan must PRINT the planned role name, and it must read
  `cloudops-cot-restricted-breakglass-role`; any other name is Branch B (CTO msg 4516).
- **The commit-time naming gate passes the ruled name with a warning, not a refusal:** `NAMING NO-SYSTEM-ASKED ...
  RestrictedPrefixGetPutList -> restricted-prefix-get-put-list-policy`, then `NAMING-GATE: PASS 1 graded` (worker ~89's commit
  a62599efc4). The gate's suggestion is not adopted; the ruled name stands. Whether the APPLY-time naming plan limb now passes is not
  established until the applier's next run: that limb is what refused in round 62.
- **Round 62's ledger** is closed by the applier with `deploy_ledger close --gate-refused` and its evidence (the laptop CTO's ruling,
  item 2), before a new entry is opened for the re-run.
