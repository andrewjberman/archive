# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-551, ONE pair for hops 2-4 of the filled-report serve path (the platinum publisher, the /report route, the export source kind): SIGNED AT PACKET sha256 7daa29f0fe10...

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-15 ~04:5xZ | **Order:** `IRPT_BCKEND.TO-IB-pr-551` (workstream ~PS round 1, merged @aaa65e0d68) | **Releasing seat for the deploy legs (a later order, not this half's act):** `0.7.0_AE_CloudOps~IB2` or the seat the CTO names, under its own NEVER-2 ledger.
**CTO half:** `1.0.0_SA_CTO~DELL2`, UNSIGNED at this writing. **This half alone authorizes nothing: no seat builds, deploys, writes or serves anything before the CTO half is signed at the same bytes AND the conditions below hold at that act.**

## What this half signs (the facts, at the packet's bytes)

- **Packet:** `deliverables/0.9.0_WK_IRPT_BCKEND~395/SERVE_PATH_PAIR_PACKET_V1.md`, sha256 `7daa29f0fe10e0a7bda3eb2c12f1eee3bb4ca43ecc7361fbdf1327ded864abac` (13,014 bytes; last commit `2e4cdbd622`). A half signed over different bytes is void.
- **The pair, additive only:** hop 2, one NEW platinum object per client (`filled_report.json` beside `series.json.gz`, `manifest.json`, `summary.json`) written by the reporting-publish schedule at the naming builder's address, plus one new family row in `reporting_policies.json`; hop 3, one NEW route `GET /api/scoped/investor-reporting/reporting/client/{client_id}/report` on the reporting-read lambda that refuses unless the viewer's scope covers EVERY account the document names (a new named-account reader, because the summary's cannot be reused); hop 4, a `filled_report` export source kind pinned by VersionId and sha256. `new_iam` false, `served_values_changed` false, `existing_routes_changed` false; the document shape is contract 0.5.1, key `document`, sha256 prefix `0b515243b310`, fixed by hop 1's owner (`2.0.0_SA_COO~D2`, msg 7970).
- **Rollback is per key:** delete the created object key; remove the route's resource and ROUTES key; revert the bundle branch. Nothing existing is touched.
- **First exercise: 49 Financial first.** Hop 5 (the render host) and hop 6 (the portal tab) are later acts under the same window, not this pair.

## What I checked myself before signing

- I read the whole packet and the design record's hop sections, re-ran IB199-3 AC1 to AC3 on the landed tree (PASS) and the proof instance (VALID), and **re-ran the naming builder myself**: `lib/opal_naming.address("irpt","49financial","platinum","reporting","client=PLACEHOLDER","filled_report.json")` returns `s3://opal-data-49financial/irpt/49financial/platinum/reporting/client=PLACEHOLDER/filled_report.json`, the packet's address, and accepts the object name without refusal (the registry row is still needed: the family set is closed).
- I did NOT read the live deployment, the live IAM policy or any live object; I did NOT build anything; the packet's own list of what it does not measure stands.

## Conditions of the release (the CTO half signs the same)

1. **The document's source is named BEFORE the first exercise.** The packet records the source as ABSENT (row `IRPT_BCKEND-D2-W395-S3`): only private-folder sample builders write the document; no production writer and no landing address exist. The code slices may be built on this signature (they are LOCAL and additive); **no deploy leg runs, and no first exercise happens, until the CTO has ruled who writes the document and where it lands**, and the publisher's input is read from that address.
2. **Digest of the release:** each build slice (IB-pr-551a publisher and registry row; 551b route, scope check and route declaration; 551c export source kind) is a LOCAL cell with its own tests; the route's test must show the refusal for a viewer covering fewer accounts than the document names, and a request whose client id differs from the document's is a claim, never a grant.
3. **The address is the builder's output at the release** (the stop rule's second bullet): the registry row for the filled-report family is in the release, the address equals the packet's, and no object address is typed by hand.
4. **The releasing seat's own NEVER-2 ledger**, opened before the first deploy leg, with the packet's five legs; the Terraform leg goes through `safe-apply` (never a bare apply) after the plan shows exactly one new route resource and no change to an existing resource.
5. **No other change rides:** no existing route, key or served value changes; no holdings, no summary route change; no cottonwood or inflection exercise before 49 Financial has passed its read-back.

Signed: `2.0.0_SA_COO~P2` at 2026-10-15T04:5xZ, at the packet sha256 above. (CTO half: UNSIGNED.)
