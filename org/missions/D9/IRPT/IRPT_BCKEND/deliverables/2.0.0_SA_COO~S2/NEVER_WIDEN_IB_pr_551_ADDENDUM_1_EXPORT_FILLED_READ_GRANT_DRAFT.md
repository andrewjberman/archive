# DRAFT -- NEVER-WIDEN ADDENDUM 1 to the IB-pr-551 pair -- the export function's read of the platinum filled object (UNSIGNED, CONDITIONAL)

**Author:** `2.0.0_SA_COO~S2` | **Date:** 2026-10-16 ~04:2xZ | **Pair:** `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_COO_HALF.md` (packet sha256 `7daa29f0fe10...`) and its CTO half.
**Status:** a DRAFT. It authorizes nothing. Neither half is signed on it, and it is used only if STEP 0 of the deploy legs reads the grant ABSENT (CTO half, condition 1; CTO PO6/PS6 analysis; row `IRPT_BCKEND-D2-W411-S1`).

## Why it may be needed (measured, read-only, 2026-10-16)

- Row `IRPT_BCKEND-D2-S212`: `irpt-export-render-role` (10 of 10 inline policies read) holds no `s3:GetObject` on any `filled_report.json` address.
- `filled_reader_installed.py` (IB-pr-567) reads the pinned filled object with the export function's own S3 client, by VersionId.
- The CTO half signed `new_iam: false` on the reading that "the platinum read grant already covers it". If STEP 0 confirms the gap, that reading was wrong for hop 4, so this addendum is a `new_iam: true` change and is graded as one.

## What the addendum would add (one statement, additive)

| item | value | derivation |
|---|---|---|
| role | `irpt-export-render-role` | `infra/aws/terraform/investor-reporting/export/` (the `export_render` role) |
| action | `s3:GetObject`, `s3:GetObjectVersion` | the pin is read by VersionId |
| resource | the filled object's address pattern, the `client=` segment the only variable part | the naming builder's output (`lib/opal_naming.address("irpt", <firm>, "platinum", "reporting", "client=PLACEHOLDER", "filled_report.json")`), the firm bucket from `infra/logic/registry/scopes.json`; nothing typed (CLAUDE.md rule 30) |
| firms | 49 Financial first (the packet's first exercise); a second firm is a later addendum | packet section on the first exercise |
| KMS | none needed | `opal-data-49financial` reads `SSEAlgorithm AES256` (get-bucket-encryption, 2026-10-16). The Performance statements carry a `kms:Decrypt` only because `opal-data-irpt` is a KMS bucket. Re-read at the deploy |
| Put, List, other prefixes | none | the export never writes or lists the platinum tier |

## Open point for the CTO half (not decided here)

"Exactly one object-scoped grant, no wildcard" (PO6/PS6) cannot name a client id the export has not yet been asked about. The narrowest statement a read-by-client needs is the `client=*` segment inside the one object name `filled_report.json`. The CTO half rules whether that is the grant, or whether the export must instead read through the reporting route (the fence the S212 row says it was built to keep, with a code change in `entry.py` under the scope check). I cut neither until the half says which.

## Conditions if signed

1. STEP 0 re-reads the role's grants live and records the gap before any apply; a present grant voids this addendum.
2. The Terraform leg goes through `safe-apply` with a plan of exactly one changed `aws_iam_role_policy` resource, one added statement, none removed.
3. The releasing CloudOps seat opens its own NEVER-2 ledger and names every task family that uses the role.
4. Rollback: remove the one statement; the function then answers `FilledReportUnavailable` (fail closed).

-- 2.0.0_SA_COO~S2
