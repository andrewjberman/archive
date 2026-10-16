# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-27 (the internal reader reads the four prefixes OG-ap-23 found denied)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED**, 2026-10-16 ~08:5xZ.
**Ask:** `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-27.md`, sha256 `38817328cc91` (re-hashed
at signing; commit 7be8a06df4).
**Bound to:** `infra/aws/terraform/opal-gateway/gateway_release_gap_read_iam.tf` at sha256-16 `be09d3dd3aaebdd9`, re-hashed at signing.

## What was read (the whole file, and the catalog rows)

- Two `aws_iam_role_policy` resources on `aws_iam_role.int_reader`, one per bucket, named by `opal_name`.
  - Each holds `s3:GetObject` on `<bucket>/<prefix>*` and `s3:ListBucket` on the bucket, conditioned by `s3:prefix StringLike <prefix>*`.
  - No Put, Delete or wildcard resource, no bucket-wide object ARN, no trust change.
- Each prefix equals its committed catalog row's `bucket`/`prefix` (DATA_CATALOG.yaml at HEAD):
  - `opal-data-etfs` `snapshots/` and `mdpf/etfs/gold/new_securities/`;
  - `bbg/`, which covers the 7 `opal_data_etfs_silver_bbg_*` rows, all opal-internal-only;
  - `opal-data-mdpf` `mdpf/feeds/model_composition/`, stopping before the row's `<firm>/` segment.
- The model_composition row is firm-scoped and IAM does not fence its firms. The tool stays NATIVE (Opal principals only) on
  this seat's ruling (msg 34857): model composition is Opal's own model definition, not client account data.

## Correction carried

My ruling message named "opal-data-etfs/silver/*". That is the table family's label, not a key prefix, and the ask rightly
refused it. It is the second time today I have taken a catalog layer name for an S3 prefix.
