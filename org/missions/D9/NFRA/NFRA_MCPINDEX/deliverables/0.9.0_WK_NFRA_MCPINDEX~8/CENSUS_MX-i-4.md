# CENSUS_MX-i-4 -- who reads `opal/bd/credentials` using `bd-exporter-ec2-role` (0.9.0_WK_NFRA_MCPINDEX~8, 2026-09-28 ~23:2xZ)

Verdict: **4 LIVE readers. Step 3 applies: the policy is NOT changed, no ledger opened, no plan or apply run, AC1 REFUSED.**

## A. Who can read the secret (grant side, read live)

`bd-exporter-ec2-role`: 15 inline policies + 1 attached (`bd-securities-access`) = 16 policies scanned. Statements that allow
`secretsmanager:*` on any resource: 2 (`AdditionalPermissions` stmt 0; `bd-securities-access` stmt 1). Only
`AdditionalPermissions` names `opal/bd/credentials-*` (5 Resource elements: anthropic-api-key, openai-api-key,
`opal/bd/credentials`, price_discovery, `blackdiamond/49f/session`). So removing that element WOULD remove the role's only grant
of the portal login. The role is held by instance profile `bd-exporter-profile`, attached to bd-allocations
(i-0800437d1dbb0b5cc), bd-transactions (i-00c7568bc510f7423), bd-assets (i-0e6f6dc014fdcf1cd, stopped), bd-fees
(i-0868fc7e7ebec26f2, stopped).

## B. Reader census -- the 11 documents read live (`ssm get-document`, denominator 11 asked, 9 registered, 2 not registered)

| Document | Reads opal/bd/credentials | Trigger (live) | Last runs (list-commands) | Verdict |
|---|---|---|---|---|
| opal-bd-allocation-download | yes (get-secret-value, then BD_PASSWORD to the Playwright script) | EventBridge `bd-allocation-pipeline-trigger` ENABLED cron(0 22 ? * MON-FRI *) | 21 runs, 21 Failed, latest 2026-09-28 22:00:04Z | **LIVE** |
| opal-bd-realized-download | yes | `bd-realized-pipeline-trigger` ENABLED cron(45 21 ...) | 21 of 21 Failed, latest 2026-09-28 21:45:17Z | **LIVE** |
| opal-bd-transaction-download | yes | `bd-transaction-pipeline-trigger` ENABLED cron(53 21 ...) | 21 of 21 Failed, latest 2026-09-28 21:53:51Z | **LIVE** |
| opal-bd-unrealized-download | yes | `bd-unrealized-pipeline-trigger` ENABLED cron(38 21 ...) | 21 of 21 Failed, latest 2026-09-28 21:39:09Z | **LIVE** |
| opal-bd-fees-download | yes | none: `bd-fees-pipeline-trigger` deleted by MX-s-12 apply (~21:14Z) | 20 Success, latest 2026-09-25 22:16Z | DEAD (registered, inert) |
| opal-bd-asset-dim-download | no (v4, REST via blackdiamond/49f/session) | `bd-asset-dim-pipeline-trigger` | Success 21 of 22 | not a reader |
| advi-49f-chain-dispatch, opal-bd-49f-session-fetch, opal-cot-bd-session-fetch | no | n/a | n/a | not readers |
| force-alloc-download, force-txn-download | in the repo file only | none: `get-document` rc 254 (not registered live) | none | DEAD |

Proof the four LIVE documents reach the read and are not blocked by the grant: for the latest run of each, the run output
contains `Fetching credentials from Secrets Manager...` and no `AccessDenied`, then `Phase 1: Login` and a Playwright
`TimeoutError` (allocation, transaction, realized, unrealized: 4 of 4 read). They fail AFTER the read, at the portal login. Failed status does not mean
no read; the read succeeds every day and would start failing (AccessDenied at the read step) if the element were removed.
The realized, unrealized and allocation runs share instance i-0800437d1dbb0b5cc; transaction runs on i-00c7568bc510f7423.

## C. Repo census (tracked script side)

`comp-find 'opal/bd/credentials' --all`: DENOMINATOR 152 hit(s) across 43424 file(s) scanned (15 ephemeral-floor and 2712 binary
files not searched); bands HEAD=7 SURFACED=46 CONFIG=26 DOC=73. The 5 secret-fetch lines (HEAD band) are line 22 of the five
`infra/aws/ssm/opal-bd-{allocation,fees,realized,transaction,unrealized}-download.json`. A native Grep outside `org/` finds 37 files;
that list is classified here (the remaining hits are under `org/`: records, not readers). Classification:
- SSM document mirrors: allocation, realized, transaction, unrealized (LIVE, table above); fees (DEAD); force-alloc, force-txn (DEAD).
- Playwright scripts not called by any live document (manual or backfill only, no trigger): `download-single-allocation.ts`,
  `download-single-week.ts`, `download-current-week.ts`, `backfill-runner.ts`, `extended-backfill.sh`, and 7 `test-*.ts` = DEAD.
- Terraform / policy text: `bd-pipeline/iam.tf`, `secrets-opal-bd.tf`, four `cross-firm-secret-deny.tf` (deny text for other firms), not readers.
- Docs, census and tools (`.tools/comp-firmsep-sweep.py`, `comp-deadgrant.py`, briefs, remediation notes, ontology census): mentions, not readers.
- The four live docs call `download-daily-{allocation,transaction,realized,unrealized}.ts`, which read the env BD_PASSWORD, not the secret name; the secret is read in the document.

## D. Consequence

The order's condition (0 live readers) is not met. Retiring the four allocation, realized, transaction and unrealized Playwright
documents (or porting them off the portal login, as MX-s-10 did for asset-dim) has to come first; only then can the element leave the role.
The secret is untouched. Nothing was changed by this order.

Limits: the census reads this role and the 9 registered documents; it does not cover a person or another role reading the secret
with their own credentials (the grant side above shows only this role's).
