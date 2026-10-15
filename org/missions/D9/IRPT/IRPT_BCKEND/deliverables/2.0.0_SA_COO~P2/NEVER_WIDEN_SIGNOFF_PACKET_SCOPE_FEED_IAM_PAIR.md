# Never-widen sign-off packet -- the Scope account feed's IAM pair (put on two prefixes of opal-data-assets for the inf gold runner role)

**Prepared by:** `2.0.0_SA_COO~P2` (dell2), 2026-10-15 ~18:5xZ | **For:** `1.0.0_SA_CTO~DELL2` (CTO half) and `0.7.0_AE_CloudOps~IB2` (applier) | **Rules on:** the CTO's remedy (a), msg 8553 (round analysis ADDENDUM 1 @edec9ba4c4), on IB2's STOP at gate (f) of IB-pr-596 (msg 8548) | **Parent pair:** Orion pair (b) ADDENDUM 1 (blob 1e138cbeea, both halves signed) | Nothing in this packet is applied.

## Why

IB-pr-596 stopped read-only at gate (f). `address()` puts the feed in `s3://opal-data-assets/orion/inflection/` (tiers.json FIRM bronze and silver point at opal-data-assets, doctrine R4; the CTO ruled the address right). The runner's role `inf-gold-layer-ec2-role` holds `s3-scoped-inf` on `opal-data-inf` only, so `s3:PutObject` on both feed keys simulates implicitDeny. This leg grants exactly the calls the feed makes on exactly its two prefixes.

**Measured call set (code at HEAD `pull_inflection_scope_account_returns.py`, `write_day`):** each day it reads the key ABSENT first (`s3.exists`, a head or get), then `put_bytes` (PutObject). The universe load reads other prefixes already granted. No delete, no list of the feed prefixes beyond a `date=` partition listing (the scheduled window start, IB-pr-594). So: PutObject, GetObject, and ListBucket scoped by an `s3:prefix` condition. **No DeleteObject.** The bucket encryption is AES256 (measured by `get-bucket-encryption` 2026-10-15), so no KMS action is granted.

## Root, address and plan shape

- **Root:** `infra/aws/terraform/inf-pipeline` (file `iam.tf`, beside `inf_gold_layer_s3`).
- **Address:** ONE new resource `aws_iam_role_policy.inf_gold_layer_scope_feed`, name `scope-account-feed-assets-put`, role `aws_iam_role.inf_gold_layer.id`. A separate resource so that removing it is the whole rollback.
- **Plan shape:** `1 to add, 0 to change, 0 to destroy`, only that address. Any other diff is a STOP.
- **The two prefixes** are the builder output (`lib/opal_naming.address()`, printed 2026-10-15): `orion/inflection/bronze/scope_account_returns/` and `orion/inflection/silver/scope_account_returns/` in bucket `opal-data-assets` (the same literal-bucket idiom as `inf-etf-ownership-daily.tf:132`). The applier prints `address()` for both layers before the plan and the ARNs in the plan must equal it character for character.

```hcl
resource "aws_iam_role_policy" "inf_gold_layer_scope_feed" {
  name = "scope-account-feed-assets-put"
  role = aws_iam_role.inf_gold_layer.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Sid = "S1PutAndReadScopeFeedKeysOnly", Effect = "Allow",
        Action = ["s3:PutObject", "s3:GetObject"],
        Resource = ["arn:aws:s3:::opal-data-assets/orion/inflection/bronze/scope_account_returns/*",
                    "arn:aws:s3:::opal-data-assets/orion/inflection/silver/scope_account_returns/*"] },
      { Sid = "S2ListScopeFeedPrefixesOnly", Effect = "Allow",
        Action = ["s3:ListBucket"],
        Resource = ["arn:aws:s3:::opal-data-assets"],
        Condition = { StringLike = { "s3:prefix" = ["orion/inflection/bronze/scope_account_returns/*",
                                                     "orion/inflection/silver/scope_account_returns/*"] } } }
    ]
  })
}
```

**Measured, not inferred:** the bucket policy `DenyParquetUnderBronze17a` (read 2026-10-15) denies PutObject only on `*/bronze/*.parquet`; the feed's bronze object is `scope.json.gz` and its parquet is under `silver`, so it does not bite. The role's other policies hold no Deny on this bucket (IB2 simulation: implicitDeny, not explicitDeny). **Inferred:** nothing; if a call is refused after the apply, that is a STOP and a row, never a widening.

## Rollback, per statement

One resource: `terraform apply` with it removed, plan `0 to add, 0 to change, 1 to destroy`, address `aws_iam_role_policy.inf_gold_layer_scope_feed` only. S1 and S2 go together; nothing else references either. No data is written by the IAM change; with the policy gone the feed refuses at its first write (fail closed) and keys already written stay (the feed never overwrites or deletes).

## Branch A (applied) and Branch B (rolled back)

- **A:** the runner role can Put and Get only under the two feed prefixes of opal-data-assets and list only with those prefixes. It cannot delete, cannot touch any sibling key (`orion/inflection/silver/fact_positions/...` and every other key stay implicitDeny for put), cannot reach any other firm's prefix. No new principal. Nothing is written until the feed's apply order (IB-pr-596) runs.
- **B:** today's state. The feed's write fails closed; no grant elsewhere to undo.

## Writers of the changed property

The role's inline policies, written by Terraform in the inf-pipeline root only. N = 1 writer for the new resource.

## After-reads (by the applier, `aws iam simulate-principal-policy` on the role)

1. Plan and apply: `1 to add, 0 to change, 0 to destroy`; a re-plan shows no changes.
2. Simulation ALLOWED: PutObject and GetObject on one bronze feed key and one silver feed key; ListBucket with prefix `orion/inflection/silver/scope_account_returns/`.
3. Simulation DENIED (implicitDeny): PutObject on a SIBLING key `orion/inflection/silver/fact_positions/x`; DeleteObject on a feed key; PutObject on another bucket; ListBucket with prefix `orion/inflection/silver/fact_positions/`.
4. The controls IB2 already read still hold (allowed on `opal-data-inf/orion/inflection/x`, denied on an unrelated bucket).
