# IB-rtj-2 RESULT -- the L4 bounded test principal: created, exercised, destroyed

**Order:** `IRPT_BCKEND.TO-IB-rtj-2` (round 10, decomp v0.14 s.R10.1; CTO ruling 99312 CALL 1). **Assignee:** `0.7.0_AE_CloudOps~V`.
**Verdict:** the fence DISCRIMINATES. A non-exempt principal granted `s3:ListBucket` is denied on both new firm buckets,
and the denial comes from the bucket policy's explicit Deny, not from a missing grant. The role is destroyed and
verified gone. **R102-AC1: every element below holds.**

## 1. The role, and its exact policy (as applied, read back by `iam get-role` / `get-role-policy`)

- Role `arn:aws:iam::313476888478:role/irpt-fence-probe-l4-role`, created 2026-09-22T01:58:40Z (Terraform root
  `infra/aws/terraform/investor-reporting/l4-fence-probe/`, `.tools/safe-apply.sh`: *"Apply complete! Resources: 2 added,
  0 changed, 0 destroyed."*). Name = `lib/opal_naming.py name("irpt", None, "fence-probe", "role", "l4")`.
- Its ONLY policy, inline `irpt-fence-probe-l4-policy`, as read back:
  ```json
  {"Version": "2012-10-17", "Statement": [{"Action": "s3:ListBucket", "Effect": "Allow",
   "Resource": ["arn:aws:s3:::opal-data-inflection", "arn:aws:s3:::opal-data-cottonwood",
                "arn:aws:s3:::opal-313476888478-lambda-artifacts"], "Sid": "ListBucketOnlyThreeBuckets"}]}
  ```
  ListBucket only, on exactly 3 buckets. Attached managed policies: 0. Inline policies: 1.
- Trust: `sts:AssumeRole` by `arn:aws:iam::313476888478:user/Andrew_Berman` only.

## 2. The name beside both live `ArnNotLike` lists (read fresh 2026-09-22 ~00:4xZ; neither matches)

| role ARN vs | `opal-data-inflection` | `opal-data-cottonwood` |
|---|---|---|
| `arn:aws:iam::313476888478:role/*-inf-*` / `role/*-cot-*` | no match | no match |
| `arn:aws:iam::313476888478:user/Andrew_Berman` | no match | no match |
| `arn:aws:iam::313476888478:user/Andrew_Berman_Console` | no match | no match |
| `arn:aws:iam::313476888478:user/Opal_Terminal` | no match | no match |

0 of 4 on each bucket. Matcher positive control: `role/irpt-inf-x-role` vs `role/*-inf-*` -> match.

## 3. The arms, under ONE assumed session (`IB-rtj-2_arms_output.txt`, run 2026-09-22T01:59:48Z)

Session: `arn:aws:sts::313476888478:assumed-role/irpt-fence-probe-l4-role/ib-rtj-2-l4-probe`.

- **POSITIVE ARM:** `list-objects-v2 opal-313476888478-lambda-artifacts` -> **OK**, KeyCount 5, IsTruncated True (key
  names not printed). The role, the assumption and the instrument work.
- **NEGATIVE ARMS, 2 of 2, each ATTRIBUTED by S3's own error context** (not the bare code):
  - `opal-data-inflection` -> `AccessDenied`: *"User: arn:aws:sts::313476888478:assumed-role/irpt-fence-probe-l4-role/ib-rtj-2-l4-probe
    is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::opal-data-inflection" **with an explicit deny
    in a resource-based policy**"*
  - `opal-data-cottonwood` -> `AccessDenied`: *"... s3:ListBucket on resource: "arn:aws:s3:::opal-data-cottonwood" **with an
    explicit deny in a resource-based policy**"*
- **ATTRIBUTION CONTROL** (accepted by both halves): `opal-data-assets`, which is not granted and has no ListBucket Deny ->
  `AccessDenied`: *"... **because no identity-based policy allows** the s3:ListBucket action"*. The same instrument names
  the OTHER cause for a missing grant, so the fenced buckets' wording is evidence about the fence and not a generic
  deny.

## 4. Destroyed, then verified

- Destroy in the same session: saved `plan -destroy` gated to exactly the 2 deletions -> `.tools/safe-apply.sh apply`:
  *"Apply complete! Resources: 0 added, 0 changed, 2 destroyed."* (02:01:35Z-02:02:21Z).
- **Verification, verbatim** (`IB-rtj-2_nosuchentity.txt`):
  `An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name irpt-fence-probe-l4-role cannot be found.`
- The declaration is removed @`d1fa987b2d` (main.tf + role.tf deleted), so no later apply recreates the role.

## 5. Ledgers

- This cell's ledger `20260922T0050Z_irpt-bckend-ib-rtj-2-l4-fence-probe`: opened before the apply, **CLOSED**, 5 of 5 legs.
- **Leg L4 of `20260918T1949Z_irpt-bckend-ib-rte-3-lgic-firm-buckets` is CLOSED by this result.** All 4 of that
  entry's legs are now proven; the entry's own close is its owner's act (`2.0.0_SA_COO~B`, per CTO 99312).

## 6. Sign-off

Packet blob `e2f521e5b55e236da0ae83f80254a10a1cbe84a8`. Halves committed before the apply (01:57:54Z), each naming the
blob and the role:
- `1.0.0_SA_CTO` @`088669b331` (01:21:52Z);
- `2.0.0_SA_COO~F` in `4.0.0_SA_CRO`'s stead @`580fd0f374` (01:31:40Z), under Andrew-direct 2026-09-11 *"If CRO is not
  online, can do COO in their stead"*, with the CRO down on 529s per Andrew;
- `4.0.0_SA_CRO`'s own half @`dba9199222` (01:57:09Z), after it recovered.
This seat verified the CTO and COO~F halves at HEAD before planning the apply; the CRO's landed 45 s before the apply ran.

IBR102-BOUNDED-PRINCIPAL-DISCRIMINATES-AND-IS-DESTROYED
