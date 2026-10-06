# IRPT_YCDGEN round 6 -- what stops branch B (Andrew's principal on the allow list), measured 2026-10-06 ~02:2xZ

Author `2.0.0_SA_COO~Y`. Nothing here was changed on the host or in IAM. Branch A stays as installed.

## Measured

| # | gap | evidence | where it is fixed |
|---|---|---|---|
| 1 | The retained Opal PDF (`ycharts_opal_reports`) is written by the RUNNER role through the reporting repository, to `irpt/cottonwood/state/ycharts_opal_reports/*` in the product bucket. No statement grants it: `resident_write_prefixes` holds ORIGINAL_VENDOR_PDF, EXTRACTION_EVIDENCE, ANALYSIS, NORMALIZED_PORTFOLIO; `ycdgen_host_families` is RESPONSE and RUN only (its comment says the report is "written from the laptop", which round 6 reversed). | `iam simulate-principal-policy` on `irpt-ycharts-runner-role`, one resource per call, with a positive control (`extraction_evidence` PutObject `allowed`): PutObject, GetObjectVersion on `ycharts_opal_reports` `implicitDeny`. Trace: `reports/resident_installed.py:319,336` (host s3 client), `reports/repository.py:465-479`. | `infra/aws/terraform/investor-reporting/ycharts/resident.tf` (the `~Y` lane's resident grants) |
| 2 | The KMS grant is conditioned on the same prefix lists, so the new prefix is not covered either. | `resident.tf` `ReportEncryptionViaS3ForResidentFamiliesOnly` | same file |
| 3 | The classifier does one `dynamodb:GetItem` per ticker on `etf-classifications` as the runner role. The only grant on that table is `dynamodb:Scan` to the Lambda role (`generate.tf:220-225`). | simulate: `dynamodb:GetItem` on `etf-classifications` `implicitDeny`; control `irpt-requests` GetItem `allowed` | `resident.tf`, one new statement |
| 4 | The renderer shells out to `render_pdf.cjs`, which finds `playwright-core` through `git rev-parse` (the host has no git) or `IRPT_PLAYWRIGHT_CORE` (the unit sets only PYTHONPATH and PYTHONUNBUFFERED). | host read SSM, `host_render_probe.sh`: node present; `playwright-core` at `/opt/investor-reporting-ycharts/node_modules/playwright-core`; Chromium and headless shell at `/home/ec2-user/.cache/ms-playwright/chromium-1228`; 3.8 GB RAM | the unit's environment (install script) and the packaged `render_pdf.cjs` |
| 5 | `opal-data-etfs/bbg/*` (held fund data) is read only if the map has held groups; no grant for the runner was found in `ycharts/*.tf` (other trees UNREAD). | Explore trace `layout_overview.py:194,824,837` | to be measured: does the first-version map reach it |

## What each fix is

- **1-3: one targeted Terraform apply** in `investor-reporting/ycharts` (`safe-apply`): add `ycharts_opal_reports` to the resident's write and read prefixes and to the KMS condition; add `dynamodb:GetItem` on `etf-classifications`. This WIDENS the resident host's own role, within one firm's prefix (cottonwood, the research policy's firms) and one read-only table that the Lambda role already scans. A CTO half and a COO half are required (NEVER-1), and the plan is printed before either signs.
- **4: the install** sets `IRPT_PLAYWRIGHT_CORE=/opt/investor-reporting-ycharts/node_modules/playwright-core` in the unit's environment, a host change in the install script.
- **5:** read `deliverables/maps/overview_map.json` for HELD_DATA groups and the producer's use of them before asking for the grant.

## Order

(cell: packaging is merged) -> Terraform half for 1-3 (plan, two halves, apply, 0-diff plan, tag) -> branch B package from the named list + environment line -> branch B half (Andrew's word for `andrew@opalinvest.com`, the principal on four real 49financial retention rows) -> install -> one real Overview run under the issuer's watch.

-- `2.0.0_SA_COO~Y`
