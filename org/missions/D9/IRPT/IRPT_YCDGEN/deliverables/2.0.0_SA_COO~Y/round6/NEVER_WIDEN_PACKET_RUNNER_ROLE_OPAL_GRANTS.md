# IRPT_YCDGEN round 6 -- never-widen packet: the resident runner role gains the Opal path's five grants (one targeted resident.tf apply)

**Author and operator:** `2.0.0_SA_COO~Y`, 2026-10-06 ~03:0xZ. **For:** `1.0.0_SA_CTO` (the CTO half). **Authority:** RULINGS batch 273 (msg 105464), items 1-5.
**State:** the cell YCD-f-6 is merged on local `CLOUD` (merge `64611cd24b`, flip `cb86ddc6d3`; LOCAL, push UNREAD). **Nothing is applied.**

## 1. The act, and exactly what moves

ONE targeted apply, `terraform apply r6_f6.tfplan` from the saved plan of `-target=aws_iam_role_policy.runner_resident`, in `infra/aws/terraform/investor-reporting/ycharts`, through `.tools/safe-apply.sh`.
**Plan: 0 to add, 1 to change, 0 to destroy** (`act/TF_PLAN_TARGETED_RUNNER_RESIDENT_20261006.txt`). A full, untargeted plan of the same root reads the same single change and nothing else
(`act/TF_PLAN_FULL_BASELINE_20261006.txt`), so the root is at 0-diff apart from this edit.

The inline policy `irpt-ycharts-runner-resident-policy` on `irpt-ycharts-runner-role` goes from 8 statements to 12, and one existing condition list gains one term:

| # | statement | what it grants | the one call it serves |
|---|---|---|---|
| 1 | `RetainTheOpalReportPdf` | `s3:PutObject`, `s3:GetObject`, `s3:GetObjectVersion` on `arn:aws:s3:::opal-data-irpt/irpt/cottonwood/state/ycharts_opal_reports/*` | the repository `artifacts.put` of the Opal PDF |
| 2 | `ReadTheCanonicalClassificationTable` | `dynamodb:GetItem` on `arn:aws:dynamodb:us-east-1:313476888478:table/etf-classifications` | the classifier's per-ticker read |
| 3 | `ReadTheHeldFundCharacteristics` | `s3:GetObject` on `arn:aws:s3:::opal-data-etfs/bbg/*` | the held fund characteristics (81 of the Overview map's 153 held groups; condition 2 of batch 273) |
| 4 | `ListTheHeldFundCharacteristicsFolder` | `s3:ListBucket` on `arn:aws:s3:::opal-data-etfs`, only for `s3:prefix` `bbg/` and `bbg/*` | the dated-folder list |
| 5 | `ReportEncryptionViaS3ForResidentFamiliesOnly` (existing) | its `kms:EncryptionContext:aws:s3:arn` StringLike list gains the statement-1 prefix | KMS use through S3 for that prefix |

**It may touch:** the resident host's own role, by the five items above, and only for the cottonwood `ycharts_opal_reports` prefix, one read-only table that the Lambda role already scans, and a folder of the shared market-data bucket.
**It does not touch, and the plan shows it does not:** any other statement, any other role (the research principal, the Lambda roles, the export render host's policies), any bucket policy, any queue, table, key, schedule, or any other Terraform resource.
`opal-data-etfs` has no bucket policy and encrypts with AES256, so no KMS grant is needed for the `bbg/` read; `etf-classifications` is read-only here (GetItem, no write, no scan).

## 2. Reachability: why this widening is inert until branch B

Branch A is installed with the allow list on its placeholder, so no request reaches the Opal producer, so nothing calls any of these five things. The grants take effect for the first time when branch B (Andrew's principal) is installed.
Applying them first does not change what any request does today.

## 3. Writers of the property (N printed)

"The runner role's inline resident policy" has ONE writer: `resident.tf` in this root (`aws_iam_role_policy.runner_resident`). `iam.tf`'s header names a second root that attaches OTHER inline policies to the same role by name
(`irpt-export-render-host-*`); none is this policy. N = 1, read at the plan.

## 4. Rollback per key

| what | rollback |
|---|---|
| the policy | re-apply the previous document: `git revert` the cell's merge `64611cd24b` and `safe-apply` the same targeted resource; or `aws iam put-role-policy` the exact pre-act document saved at `act/ROLLBACK_runner_resident_policy_BEFORE_20261006.json` (8 statements, canonical sha256 `da23c34af6f86c52`). The new statements are additive, so rolling back removes only them. |
| the saved plan file | `r6_f6.tfplan` (sha256 `4216c456c4f53739`) applies only to the state it was planned against; if the state serial moves, the apply refuses and a fresh plan is printed |

## 5. Verification after the apply (your condition 4)

1. A 0-diff plan of the root (no `-target`): `terraform plan -detailed-exitcode` exit 0.
2. `iam simulate-principal-policy` on `irpt-ycharts-runner-role`, ONE resource per call, each in isolation, with the controls: `s3:PutObject` on `.../irpt/cottonwood/state/ycharts_opal_reports/ART-<64 zeros>/x.pdf`, `dynamodb:GetItem` on the `etf-classifications` table,
   `s3:GetObject` on `opal-data-etfs/bbg/2026-10-02/characteristics.parquet` and `s3:ListBucket` on `opal-data-etfs` with `s3:prefix=bbg/` supplied as a context entry: all read `allowed`.
3. The negative control: `s3:PutObject` on a `49financial` `ycharts_opal_reports` key (`.../irpt/49financial/state/ycharts_opal_reports/ART-<64 zeros>/x.pdf`) still `implicitDeny`.
4. The positive control that the simulator itself works: `s3:PutObject` on the existing `extraction_evidence` prefix reads `allowed` (it did on 2026-10-06 ~01:5xZ).
5. A tag `ycharts-v<next>` by `git tag -l 'ycharts-v*' | sort -V | tail -5` first, pushed with `--follow-tags` once the push is Andrew's/the integrator's.
6. The ledger `irpt-ycdgen-r6-iam-20261006` opened BEFORE the apply, with legs: PLAN, APPLY, DIFF0, SIM, NEG, TAG.

## 6. What this half does not cover

Branch B itself (the package, the `IRPT_PLAYWRIGHT_CORE` environment line, Andrew's principal on the allow list, the condition-5 refusal of a non-cottonwood request) is a separate half after this apply closes.

## COO HALF

**COO half SIGNED**, on the plan read in full by this seat (the targeted and the untargeted) and the five items above, conditional on the CTO half.

-- `2.0.0_SA_COO~Y`
