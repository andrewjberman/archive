# MDPF_TAXSMA TX-i-1 and TX-i-2 -- IAM applies, result (4.0.0_SA_CRO, FAST lease)

Each value carries its instrument, UTC time and denominator. Written 2026-10-01 ~00:4xZ.

## What was applied

| Cell | Root | safe-apply | Result | Re-plan | Ledger |
|---|---|---|---|---|---|
| TX-i-1 | `infra/aws/terraform/mdpf-pipeline` | 2026-10-01T00:03:55Z | 5 added, 0 changed, 0 destroyed | 00:06Z No changes | `org/critical_paths/change_management/20260930T2352Z_mdpf_taxsma-tx-i-1_deploy_completion.md` CLOSED @14670cf66c |
| TX-i-2 | `infra/aws/terraform/opal-assets` | 2026-10-01T00:16:59Z | 1 added, 0 changed, 0 destroyed | 00:17Z No changes | `org/critical_paths/change_management/20261001T0014Z_mdpf_taxsma-tx-i-2_deploy_completion.md` CLOSED @73ef80ab94 |

Created: `mdpf-49f-taxsma-role`, `mdpf-cot-taxsma-role`, `mdpf-49f-taxsma-policy`, `mdpf-cot-taxsma-policy`,
`mdpf-gold-taxsma-policy` (on `mdpf-gold-lambda-role`), `mdpf-publisher-taxsma-control-read-policy` (on
`opal-assets-mdpf-egress-publisher-role`). Terraform: the vendored `.tools/terraform.exe` 1.9.8.

## Departures from the orders as issued, and why

- **Two prelude roles, not one.** Measured 2026-09-30 ~21:4xZ (`get-bucket-policy`): each firm bucket's
  `DenyForeignFirmPrincipals` denies every principal whose ARN is not like that firm's short-token pattern
  (`opal-data-49financial`: `role/*-49f-*`; `opal-data-cottonwood`: `role/*-cot-*`). Contract 0.6.0 writes Tax
  state for both firms, so one role cannot hold both. TXI1-AC3's "no other firm's prefix" holds for each role.
- **The control key is global.** The publisher's role carries no firm token, so it cannot read the 49financial
  bucket. The control moved to `address(mdpf, global, state, taxsma_control, current.json)` in `opal-data-mdpf`
  (contract amendment 2 @338665c1b1).
- **TXI2-AC1's "49financial category Gold prefix" read was not granted.** The publisher reads category-views
  from the existing canonical Gold in `opal-data-assets`; the N+1 copies are not written (surprise S9).
- **Verification is SIMULATION, not exercise** (TXI1-AC6/AC7, TXI2-AC5). The roles trust only
  `mdpf-gold-lambda-role` and Lambda, so no session of them can be opened from this seat. The exercise is owed
  at TX-r-3's first Gold and publisher runs.
- **TX-i-3 not applied** (surprise S7): refused at the plan.

## SIMULATION -- TX-i-1 (not exercise)

```
SIMULATION (iam simulate-principal-policy), 2026-10-01T00:38Z, 30 rows, one resource per call
OK   49f: 0833 fact_rps_s2 read                           s3:GetObject                 -> allowed
OK   49f: 0833 fact_acc list                              s3:ListBucket                -> allowed
OK   49f: workbook Silver put                             s3:PutObject                 -> allowed
OK   49f: workbook Bronze put (json)                      s3:PutObject                 -> allowed
OK   49f: own dispositions get                            s3:GetObject                 -> allowed
OK   49f: own dispositions get by version                 s3:GetObjectVersion          -> allowed
OK   49f: own taxsma_assets put                           s3:PutObject                 -> allowed
OK   49f: own taxsma_assets list                          s3:ListBucket                -> allowed
OK   49f: bucket versioning read                          s3:GetBucketVersioning       -> allowed
OK   49f: capability secret read                          secretsmanager:GetSecretValue -> allowed
OK   49f: OTHER secret read                               secretsmanager:GetSecretValue -> implicitDeny
OK   49f: cottonwood dispositions get                     s3:GetObject                 -> explicitDeny
OK   49f: Black Diamond cottonwood read                   s3:GetObject                 -> implicitDeny
OK   49f: served category-views put                       s3:PutObject                 -> implicitDeny
OK   49f: served json/mdpf put                            s3:PutObject                 -> implicitDeny
OK   49f: own bucket OTHER prefix get                     s3:GetObject                 -> implicitDeny
OK   49f: own bucket list OTHER prefix                    s3:ListBucket                -> implicitDeny
OK   cot: Black Diamond cottonwood read                   s3:GetObject                 -> allowed
OK   cot: Black Diamond list                              s3:ListBucket                -> allowed
OK   cot: own dispositions put                            s3:PutObject                 -> allowed
OK   cot: own taxsma_assets get                           s3:GetObject                 -> allowed
OK   cot: bucket versioning read                          s3:GetBucketVersioning       -> allowed
OK   cot: 49financial dispositions get                    s3:GetObject                 -> explicitDeny
OK   cot: 0833 fact_rps_s2 read                           s3:GetObject                 -> implicitDeny
OK   cot: capability secret read                          secretsmanager:GetSecretValue -> implicitDeny
OK   cot: served category-views put                       s3:PutObject                 -> implicitDeny
OK   gold: assume the 49f Tax role                        sts:AssumeRole               -> allowed
OK   gold: assume the cot Tax role                        sts:AssumeRole               -> allowed
OK   gold: control put                                    s3:PutObject                 -> allowed
OK   gold: 49financial dispositions get (ambient role)    s3:GetObject                 -> explicitDeny
rows as expected: 30 of 30
```

## SIMULATION -- TX-i-2 (not exercise)

```
SIMULATION (iam simulate-principal-policy), 2026-10-01T00:38Z, 10 rows, one resource per call
OK   Tax control get                          s3:GetObject                   -> allowed
OK   Tax control put                          s3:PutObject                   -> implicitDeny
OK   another opal-data-mdpf key get           s3:GetObject                   -> implicitDeny
OK   49financial taxsma_assets get            s3:GetObject                   -> explicitDeny
OK   49financial dispositions get             s3:GetObject                   -> explicitDeny
OK   workbook Silver get                      s3:GetObject                   -> implicitDeny
OK   workbook Bronze get                      s3:GetObject                   -> implicitDeny
OK   capability secret get                    secretsmanager:GetSecretValue  -> implicitDeny
OK   EXISTING canonical Gold get (control)    s3:GetObject                   -> allowed
OK   EXISTING served put (control)            s3:PutObject                   -> allowed
rows as expected: 10 of 10
inline policies on the role (3): mdpf-publisher-taxsma-control-read-policy, opal-assets-mdpf-egress-publisher-live-serve, opal-assets-mdpf-egress-publisher-scoped
new policy: [{"Action": ["s3:GetObject"], "Effect": "Allow", "Resource": "arn:aws:s3:::opal-data-mdpf/mdpf/global/state/taxsma_control/current.json", "Sid": "ReadTaxsmaControlOnly"}]
```

## EXERCISE

None yet. Owed at TX-r-3: the first Gold run with `TAXSMA_PRELUDE_ROLE_ARN_<FIRM>` set (including the first-run
NoSuchKey read of dispositions under a prefix-conditioned ListBucket), and the first publisher run with the
rollout switch ON.
