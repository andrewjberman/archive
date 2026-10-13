# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_CTLPLN CT-ab-2: the Dell agent users join the admin group and keep four Denies (SIXTH pair)

**Signer:** `1.0.0_SA_CTO` (laptop) | **State: SIGNED 2026-10-13 ~19:4xZ, on the conditions in section 3** |
**Against:** `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-ab-2_PAIR_20261013.md` @024c2fd428 (50 lines, read whole)
| **Cell:** CT-ab-1 merged @e4ae5f7820 (with CT-ab-12 @5dba8cb256) | **Input:** Andrew-direct ~16:5xZ rec (b),
`org/tier1_exec/2.0.0_SA_COO~C/deliverables/ANDREW_DIRECT_20261013_165xZ_DELL_USERS_ADMIN_GROUP_KEEP_THREE_DENIES.md`; CTO ruling
@d2f79ea8dd | **Order:** `0.7.0_AE_CloudOps~U7`, `NFRA_CTLPLN.TO-CT-ab-2`, staged.

## 1. The blast radius, signed (section 2 of the COO half, as written)

Six keys, K1 to K6, all in root `infra/aws/terraform/nfra-ctlpln-identity/`, one writer each (this root):
- K1 and K2 ADD the two Dell agent users to `AdministratorAccessOpalCapital`, which the root names and never manages.
- K3, K4 and K5 UPDATE three policy documents in place.
- K6 DESTROYS the routes-fn Deny policy and its group attachment.

The users gain what the admin group allows, less four explicit Denies. A leaked Dell key is then close to an admin key. That is
Andrew's ruling, and this half signs the radius, not the choice. No other principal and no resource outside IAM moves. Rollback is
one re-apply of the previous tree, recorded in the ledger before the apply, which reverses all six keys. Both branches are covered.
Signed.

**Read by this seat at the pin, not taken from the packet:**
- Tree `infra/aws/terraform/nfra-ctlpln-identity` at `738bbc654f` = `355c1c13bb926c7f22d358c191a7a5ceaffe7aaa`, equal to HEAD of
  box/laptop at signing.
- The Deny statements left at the pin are exactly four:
  - `dell_deploy_policy.json`: `DenyCloudTrailWrites`, `DenyS3DeletesOnProductionData`, `DenyTableAndDatabaseDeletes`;
  - `dell_create_policy.json`: `DenyAuditTrailBucketWrites`;
  - `dell_iam_roles_policy.json` and `dell2_ssm_policy.json`: none.

  These are the three classes Andrew kept (CloudTrail and audit writes, production S3 deletes, table and database deletes).
- `iam.tf:40-48` holds K1 and K2. `routes.tf` removes `aws_iam_policy.dell_agent_routes_fn` and its attachment (K6).
- The `main.tf` diff since `a71a0b4f68` is comments only, so it is not a key.

## 2. The three answers owed

(a) Blast radius: SIGNED as section 1. (b) Branch A counts: CONFIRMED, `2 to add, 3 to change, 2 to destroy`, exactly K1-K6.
(c) Pin: CONFIRMED, `738bbc654f`. A move of HEAD with no change under the root's tree id keeps the pin valid. Any change under the
tree id is Branch B.

## 3. Conditions

1. **POST-3 is the gate that matters.** Every one of the four refused actions must read `explicitDeny` for both users. Any `allowed`
   means the apply has widened past Andrew's ruling. The applier then rolls back at once, files a BLOCKING row, and reports to this
   seat before anything else.
2. **PRE-1 group read.** If `AdministratorAccessOpalCapital` carries an attached policy that is not AWS `AdministratorAccess`, it is
   Branch B. The radius signed here assumes the group is the admin group Andrew named and nothing broader.
3. The apply goes through `safe-apply`, with the NEVER-2 ledger entry opened at the start and closed only on POST-1 to POST-3.
4. When the applier reports complete, the Dell managers' read-backs follow:
   - dell2: decrypt under the IRPT key;
   - dell1: a policy simulation and an edge-function admit.

   Those reads stand down laptop CloudOps `~ANL` and `~FBL`, per Andrew's ~13:1xZ word.
