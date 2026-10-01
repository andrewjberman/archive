# Never-widen ask -- OG-tr-1, the narrow opal-gateway release of the Tax SMA workbook route, capability ON

By: `2.0.0_SA_COO~O` (issuer), 2026-10-01 ~18:4xZ. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-tr-1.taxsma-route-release.md`.
Authority: Andrew-direct ~17:2xZ (site Z runs both halves; the MDPF_TAXSMA exclusion lifted for THIS release; relay
@d34037d1f5), ~17:3xZ ("ON at this deploy"; msgs 27991, 27992), ~17:4xZ (priority ahead of all site-Z work; msg 27993).
Spec: laptop CRO 103933 (relay @65e0886dc1). `1.0.0_SA_CTO~O` msg 27986 (cut; CTO half at PHASE A). PHASE A evidence:
`deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-tr-1.md`, drained @abca11d3bc. Half 1 (`OG-tt-1`, ALB rule priority 36
for exactly `/ms/taxsma-workbook`) is COMPLETE (drained @c7d51bb5b5; tt.AC2 PASS on CLOUD).

**Halves owed:** `1.0.0_SA_CTO~O` (CTO half) and `3.0.0_SA_CVO~O` (second, non-acting half), against THIS file at its
commit.

## 1. The bytes

Release branch `rel-nfra-oplgtw-taxsma-route` (`/c/tmp/og-rel6`), HEAD `3a7d6a7dc85fe3c54a4b63b27b59055abc9adca7`, two
commits on live `0a1d9079c682c640e619612f804257681c5db357` (host md5 92 of 92 equal): `b97c822b28` (the module
`app/taxsma_workbook.py` sha256 `6acc3e8c...`, its test `810148fe...`, `server.py` +5 = the import and the Route,
`config.py` +10 = the two `TAXSMA_WORKBOOK_*` fields and their comment block) and `3a7d6a7dc8` (`deploy-to-ec2.sh`
+23/-1). Census: 5 files, all under the gateway directory; `ms_ingest.py` not among them. Artifact: 96 files, 3 differ
from live. Tests on the release tree: `test_taxsma_workbook.py` 21 passed (moto 5.2.3), `test_mail_route.py` 10,
`test_mail_listing.py` 12, `test_ogz2_ac08` 1 (60 = LIVE 60 + OWN 0).

## 2. Blast radius -- what the act may touch

| key | before | after | rollback |
|---|---|---|---|
| host app files | live `0a1d9079c6`, 92 of 92 | + `app/taxsma_workbook.py`; `server.py` and `config.py` gain only the Tax lines | re-deploy `/c/tmp/og-rb6` (95 of 95 equal to live S3) with `DEPLOY_BASE_REF` = the release sha; that template needs nothing from the shell |
| host `.env` | 46 keys | 48: + `TAXSMA_WORKBOOK_BEARER` (host-side from `gateway/global/taxsma-workbook-token`, non-empty; refused when the read fails or is empty) and `TAXSMA_WORKBOOK_IDENTITY` (from the deploying shell, one `<tid>/<oid>` pair, refused when missing or malformed, never committed); the other 46 unchanged | the same re-deploy renders the 46-key `.env` |
| **served content** | none for Tax | **`GET /ms/taxsma-workbook` LIVE, capability ON**: behind ALB rule 36 (no sign-in), the route's OWN bearer is the only edge gate (refused while that value is also another route's credential); a selector, query, body or caller-supplied identity is refused before any token fetch or Graph call; it reads ONE fixed worksheet (the contract's site, item, sheet) as the bound identity and returns exactly the nine projected columns with row and snapshot metadata | re-deploy (the route unmounts); or blank the identity at the next deploy |
| bound identity | -- | `6810043e-d171-4adc-9975-068b35e179da/517aa5ee-...` = opalbloomberg@ (see 3c) | as above |
| the only caller | -- | the Gold function holds the bearer; it stays OFF until laptop `4.0.0_SA_CRO` sets its environment after this release (spec s.3) | -- |
| tool list | 65 | 65 (a headless route, not an MCP tool) | -- |
| S3 artifact / manifest | `-0a1d9079c6` | + `-3a7d6a7dc8`; manifest `deployed_commit` moves, previous `0a1d9079c6` | the live key stays; revert the manifest commit |

**Not touched, by name:** Terraform and IAM (the rule is OG-tt-1's; the role's read of the Tax secret is the laptop's
TX-i-3), the instance, every other route (`/ms/*` exact rules, `/hx/*`, `/otp/*`, `/mcp`), the roster and sender-table
host-side reads, the identity allowlist, the mcportal pin. No secret is written; no workbook is read by site Z.

## 3. The named properties and their writers

**(a) Who can read the Tax worksheet through the gateway.** N = 2 writers: the route's guard order
(`app/taxsma_workbook.py`: exact GET; constant-time bearer, refused if it equals another route's credential; no
caller-supplied identity) and the deploy render (bearer and identity). Expected: no bearer -> `UNAUTHORIZED_CAPABILITY`
with no Graph call (`tr.AC1` arm 2); only the bearer holder reads. Other branch: arm 2 reads anything else -> roll back.

**(b) The bearer's presence.** N = 1 writer: the render's host-side read, refusing an empty value (synthetic: failed
read rc 3, empty rc 3, `None` rc 3, value 0). Expected: non-empty (`tr.AC1` arm 4, `bearer_empty False`).

**(c) Whose delegated identity the route reads as.** N = 1 writer: the render from `OG_TAXSMA_WORKBOOK_IDENTITY`,
pair-validated (7 bad identities refused rc 3). The value was CONFIRMED before any upload (Andrew ~17:3xZ, CTO 27992):
6 broker records read, 2 username-match `opalbloomberg@opalinvest.com`, both the SAME oid `517aa5ee` (one person's
principal-keyed and email-keyed caches, by cache file-name hashes) -- one distinct oid, MATCH with the site-Z Part D
record. The issuer rules the gate satisfied (row W15-S19): the stop condition guards two DIFFERENT people matching.

## 4. Act and verify (PHASE B, from the order)

- **Before:** re-read live (re-cut if moved); BEFORE reads; NEVER-2 ledger `nfra-oplgtw-taxsma-route-release` committed
  before the act.
- **Act:** from `/c/tmp/og-rel6`: `OG_TAXSMA_WORKBOOK_IDENTITY=<confirmed, exported via a python eval, never printed>
  DEPLOY_BASE_REF=0a1d9079c6... HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15 bash infra/aws/ec2/safe-ec2-deploy.sh
  opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
- **Verify:** the pre-written `tr_verify.sh` immediately after the deploy (host `/health`, 93-file md5, tool list, keys
  46 -> 48, route probes), then `tr.AC1.sh` (4 arms). Any failure: roll back, re-verify, close ROLLED BACK.
- **Criteria:** `tr.AC1.sh`, `tr.AC2.sh`. Results go to `0.0.0_AB_MSTR~Z` for the laptop (spec s.4, with the rule's ARN
  and priority 36 from OG-tt-1).
