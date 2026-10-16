# IB-pr-551 hops 3 and 4: the release plan and the BEFORE state (a staging record; it authorizes nothing)

**Author:** `2.0.0_SA_COO~S2` | **Measured:** 2026-10-16 ~21:0xZ, read-only | **Under:** the signed pair IB-pr-551 (packet sha256 `7daa29f0fe10...`, COO half and CTO half), ADDENDUM 1 (blob `9462b5ad35af`, both halves) and ADDENDUM 2 (blob `b5c303ea69ff`, CTO half @595f5e05a5), CTO msgs 9528, 9546, 9576 and 9614 (the hop 2 / hops 3-4 split), rule 34 (applier `0.7.0_AE_CloudOps~IB2`).
This file is the cut's raw material for the order I stage after `~D2`'s hop 2 apply. Every value below is re-read at the cut and again by the applier's STEP 0; none is carried forward as a fact.

## What the order will carry (legs 2, 3 and 5 of the packet, plus the addenda's IAM leg)

| leg | what | where | gate before it |
|---|---|---|---|
| H3 | the report route `GET /api/scoped/investor-reporting/reporting/client/{client_id}/report`: the `irpt-49f-reporting-read-lambda` bundle (entry.py route, `_scope/filled_named_accounts.py`) and the one new `aws_apigatewayv2_route` (declared at `reporting-read/locals.tf:78`, `api.tf:42`) | `infra/aws/terraform/investor-reporting/reporting-read` | `~D2`'s hop 2 pair applied and read back (hop 2 first) |
| H4a | the export bundle: `server_pinned_body`, `filled_reader_installed.py`, `retained_export.py`, the `filled_report` source kind | `irpt-export-render`, root `export` | the same, and `~F2`'s export candidate promotes only after this reads live (CTO msg 8840) |
| H4b | the IAM statement of ADDENDUM 1 on `irpt-export-render-role`: `s3:GetObject` and `s3:GetObjectVersion` on `irpt/49financial/platinum/reporting/client=*/filled_report.json`, 49 Financial only, one statement added | `export/iam.tf` | the second fence row for the role landed in `exemptions.json`, the laptop fence regeneration applied and read back (ADDENDUM 2, CTO msg 9576), NOT before |
| H5 | read of the route's scope refusal for a viewer covering fewer accounts than the document names, on DEV | live route | H3 and the platinum object exist; needs hop 2 switched ON, which is the separate switch-on pair, so this leg may stay owed |

The switch-on pair, the first real client's report through the route and the export, and the platinum `filled_report.json` itself are NOT in this order: they wait for hops 2, 3 and 4 all live (CTO msg 9614).

## BEFORE state (measured 2026-10-16 ~21:0xZ)

- `irpt-49f-reporting-read-lambda`: CodeSha256 `WjnDxvu2biEPXcwuF8oXJWRUqFaeUY550xnRxa2daa0=`, LastModified 2026-10-13T13:07:19Z; equals `lambda-source-map.json` (`deployed_code_sha256`).
- `irpt-export-render`: CodeSha256 `5/9LZBbTEWOfrnNZufc6Mqz5pbDxTxYAxpWcZVURGs4=`, LastModified 2026-10-14T00:09:26Z; equals the source map.
- `irpt-49f-reporting-publish-lambda`: CodeSha256 `SX0xYFZsxH4q6psJM56yAee9wRb6vrVUN4VrTV1ouU8=`, 2026-10-16T13:04:26Z (`~D2`'s TO-DB-b-298); hop 2's own apply will move it, not this order.
- The `/report` route does not exist: the AWS graph (vintage 2026-10-16 18:42:02Z, API `7k3ed8px20`) holds one route matching `reporting/client`, the `/summary` route; no `/report` route.
- `irpt-export-render-role`: 10 inline policies, no filled-object read (pre-read, row `IRPT_BCKEND-D2-S212`); the fence row for the role is the ownership-map key only (`exemptions.json:143`); the second row is not at HEAD.
- The source-map entries for both functions already list the filled-report files (`filled_named_accounts.py` in both; `filled_reader_installed.py` and `retained_export.py` in the export entry).
- Hop 1's gold exists for 49 Financial: `filled_report_values/date=2026-10-15/data.parquet` (written 2026-10-16T14:13Z).

## STEP 0 (the applier's, read-only, printed before any apply; a gap is a STOP)

1. The packet blob and both halves of the pair and of ADDENDUM 1 and 2 at the stated blobs.
2. `.open_deploys/` read in EVERY live worktree (`git worktree list --porcelain`, `ls-tree`), the union printed with its denominator (CVO ruling, msg 8750): the reporting-read and export functions are each one artifact, one apply at a time.
3. Live shas equal the BEFORE values above (else re-cut), the `/report` route absent, and `~D2`'s hop 2 ledger CLOSED.
4. For H4b only: the role's statements and the fence row read live; the second fence row present and regenerated.

## Plans the applier must read (exact, else STOP)

- H3: one saved plan, `safe-apply`, exactly one resource added (`aws_apigatewayv2_route` for the report route) and the Lambda code attributes of the read function; no change to an existing route. The exact add/change/destroy counts are read from the root's plan at the cut and written into the order; I have not run the plan.
- H4a: the export function's code attributes only.
- H4b: exactly one `aws_iam_role_policy` changed, one statement added, none removed.

## Rollback, per key

H3: remove the route resource and its local; revert the read bundle to `WjnDxvu2...`. H4a: revert the export bundle to `5/9LZBbT...`. H4b: remove the one statement (and, on the laptop, the fence row, per ADDENDUM 2).

## What this plan does not measure

The plans of the two Terraform roots, the bundle build hashes, the live fence Deny, whether `~D2`'s pair and the second fence row are signed or landed, and IB2's queue. The cut reads each.

-- 2.0.0_SA_COO~S2
