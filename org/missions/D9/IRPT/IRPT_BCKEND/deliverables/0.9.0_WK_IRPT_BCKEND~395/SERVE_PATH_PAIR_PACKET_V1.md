# NEVER-WIDEN PAIR PACKET v1 -- IRPT_BCKEND cell IB-pr-551: hops 2, 3 and 4 of the filled-report serve path (round 1, workstream ~PS)

Status: DESIGN ONLY. This packet proposes one never-widen pair. Nothing in it is built, changed, deployed, written to AWS, invoked, signed or sent. Both halves are UNSIGNED at these packet bytes (section 13).

Base: commit 2a914408b824d91a77dd5d41a01394681137f4b4, the HEAD the design record IB199-3_serve_path_design.json names as its base_commit.

Ordered by: CTO ruling 076d (msg 7974), which ruled hops 2 to 4 IRPT_BCKEND's, to be cut as ONE never-widen pair with one issuer, 2.0.0_SA_COO~P2. The filled report's document shape is fixed by hop 1, whose owner is 2.0.0_SA_COO~D2.

## 0. What the pair is, in one paragraph

No code publishes or serves a filled report today. The filled report is one JSON object per household, with exactly two keys, household and values, as contract 0.5.1 (key document) states it. Only private-folder sample builders produce it. This pair adds three things that do not exist today: hop 2, a new platinum object per client written by the reporting-publish schedule beside series.json.gz, manifest.json and summary.json; hop 3, a new GET route that returns that object with no re-shaping and refuses unless the viewer's scope covers every account the document names; and hop 4, a filled-report source kind for the export. Hop 5, the render host, is windowed (section 8) and is not part of this pair.

## 1. Change set

Hop 2, the platinum publisher. Files, each read at the base commit:
- infra/aws/lambda/investor-reporting/reporting-publish/publisher.py line 251, SUMMARY_OBJECT: the new object-name constant is declared beside it.
- infra/aws/lambda/investor-reporting/reporting-publish/publisher.py line 313, summary_address: a report_address() beside it, built only from naming.address (line 320 pattern).
- infra/aws/lambda/investor-reporting/reporting-publish/handler.py line 192 and line 371-372: one more put beside the summary put, with the address from the builder.
- infra/logic/registry/reporting_policies.json line 51, the CLIENT_SUMMARY family: one new family row for the filled-report object.

The address. The naming builder's output, run at the base commit with the placeholder client id PLACEHOLDER and the proposed object name filled_report.json, is:
s3://opal-data-49financial/irpt/49financial/platinum/reporting/client=PLACEHOLDER/filled_report.json

The address is produced by lib/opal_naming.py address() (opal_naming is the single builder), never typed by hand. The builder accepted the object name and refused nothing. The registry row is still needed, because reporting_policies.json closes the family set for irpt-dashbd-served-reporting (three families at lines 48-52) and scopes.json line 340 says so. A row is a missing registry row to add, not a workaround.

Hop 3, the route. Files:
- infra/aws/lambda/investor-reporting/reporting/entry.py line 92, SUMMARY_ROUTE_KEY: the new route key is declared beside it.
- entry.py line 317, _summary_named_accounts, and line 332, serve_summary: a new reader and a new operation follow the same pattern.
- entry.py line 373, ROUTES: one new key. The route template is /api/scoped/investor-reporting/reporting/client/{client_id}/report.
- infra/aws/terraform/investor-reporting/reporting-read/api.tf line 34: one new aws_apigatewayv2_route beside the summary route, on the same integration and the same authorizer.
- infra/aws/terraform/investor-reporting/reporting-read/locals.tf line 75: one new route-key local.

Hop 4, the export source kind. Files:
- infra/aws/lambda/investor-reporting/export/bundle.py line 111, the platinum test, and line 191, the list of performance_source pins: one new branch for source kind filled_report.
- infra/aws/lambda/investor-reporting/export/retained_export.py line 267, platinum_row, and line 279, freeze_platinum: the filled object is frozen with its VersionId and sha256, as PATH B freezes the platinum series.

## 2. The input contract and the document's source

The document is contract org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json at version 0.5.1, key document. The sha256 prefix 0b515243b310 is the prefix of the contract file bytes, re-computed at the base commit. The document is one JSON object per household with exactly two keys, household and values. Values are keyed by member id. An absent member prints its reason in words. The publisher publishes the document and the route returns it with no re-shaping.

The source is ABSENT. The contract writer field names only the private-folder sample builders (deliverables 0.9.0_WK_IRPT_DASHBD~141 and ~175), each writing HOUSEHOLD_SAMPLE.json into its own folder. No production writer exists and no landing address for the document is named anywhere in the repository. The publisher therefore has no production input. Who writes the document, and where it lands for the publisher to read, is a question for the CTO before the pair is signed. This packet does not choose it.

## 3. The scope rule (never-widen)

The new route refuses, with OBJECT_NOT_COVERED, unless the viewer's scope covers EVERY account the document names. The named accounts are each household.accounts entry's account_id, and every account key of each values by_row map. Each is checked with the same _check_covered the summary route uses (entry.py line 344). A client id in the request is a claim, never a grant.

The summary's own _summary_named_accounts (entry.py line 317) cannot be reused as it stands. It reads the summary's firm, client_id, accounts and unpublished_account_ids keys, and the filled document carries none of the first two at top level and nests its accounts under household. A new named-account reader is needed in the pair. This is recorded as a surprise row, not decided here.

The route never reads the holdings and never reads a current object that is not the one at the hop-2 address.

## 4. Blast radius

Writes, each named:
- One new object per client at the hop-2 address, irpt/49financial/platinum/reporting/client=<id>/filled_report.json. It is new at its address. No existing key is overwritten.
- One new family row in reporting_policies.json. It is a registry row, not a served key.
- One new API Gateway route resource for GET .../reporting/client/{client_id}/report. No other route is created.
- Filled-report source-kind items in NEW export bundles only. No existing bundle is rewritten.

Reads, each named:
- The filled-report object, through the existing s3:GetObject grant on the whole platinum reporting prefix (locals.tf lines 46-47 and iam.tf lines 75-76).
- The directory pointer and ownership map that the shared boundary reads on every request (iam.tf lines 80-84).

IAM. new_iam is false. The API invoke grant (api.tf lines 44-50) already covers the new path, because its source_arn ends in GET/api/scoped/investor-reporting/reporting/*. The S3 read grant already covers the platinum reporting prefix. The order's remark that the route owner must add an IAM read on the new key is not borne out at the base commit; that is a surprise row.

Served values. served_values_changed is false: the pair adds an object, a route and a source kind, and changes no value that any served route returns today. existing_routes_changed is false: the account route, the summary route and their integration are untouched.

The blast radius of the pair is therefore additive. Its one live effect is the new route, which is WORLD and which only the CTO's signature on both halves can release.

## 5. Rollback, per key

Per created object key, client=<id>/filled_report.json: delete that key. No prior version exists at a new address. Switch the publisher's filled-report pass off so that no further key is written.

Per declared route, GET .../client/{client_id}/report: remove its aws_apigatewayv2_route resource and its ROUTES key beside SUMMARY_ROUTE_KEY, then redeploy the previous reporting-read version. The account route and the summary route are not touched by the rollback.

Per export source kind, filled_report: refuse filled_report bodies by reverting the bundle.py branch. No existing bundle carries a pin of this kind, so no bundle needs a rewrite.

Rollback is per key and nothing else. A rollback that touched an existing key would be outside the pair.

## 6. First exercise: 49 Financial first

The first exercise is 49 Financial, and it is first. The firm is 49financial (scopes.json, the 49financial rows; the bucket is the builder's output). No other firm is exercised until the 49 Financial exercise has passed its own read-back. The first exercise reads the new object and the new route for one covered client only. No cottonwood or inflection value is read, written or served by the pair.

## 7. Build slices (after the pair is signed)

Three LOCAL build cells, each cut by the CTO after signature, each naming the files it writes:
- IB-pr-551a, the publisher and the registry row: publisher.py, handler.py, reporting_policies.json and one new test file beside the publisher.
- IB-pr-551b, the route, the scope check and the route declaration: entry.py, api.tf, locals.tf and one new test file beside the route. It depends on IB-pr-551a.
- IB-pr-551c, the export source kind: bundle.py, retained_export.py and one new test file beside the export. It depends on IB-pr-551b.

None of these slices runs, deploys or writes anything when this packet is read. Each is LOCAL until the route is deployed, and the deploy is the WORLD act the signature releases.

## 8. Hop 5 is windowed, not part of this pair

Hop 5 is the render host (infra/aws/ec2/investor-reporting-export/run-export-render.sh line 29 and render_export.cjs). It prints a print route from the frozen bundle, and the print route has no filled-report template. Its owner is UNOWNED in the repository. The render host is stopped, and starting it needs Andrew's per-use word.

The windowing of hop 5 (the render host, under 0.7.0_AE_CloudOps~IB2) is a later act under the same window: the same signed pair, a later release, after hops 2 to 4 are live. It is not released by this packet.

## 9. Stop rule

The stop rule applies to the release of the pair, at each hop and at the whole pair.

The release stops, and the packet is re-cut, if any of these holds at the release:
- a file site named in section 1 does not hold its identifier at the release commit;
- the address the builder returns for the release differs from the address in section 1;
- the registry row for the filled-report family is not in the release;
- the route's scope check does not refuse a request whose viewer covers fewer accounts than the document names;
- any existing route, any existing key or any served value changes at the release;
- the first exercise is on any firm other than 49 Financial, or is not first.

A changed address, a changed route template or a served value that moves each stops the release. A surprise row is recorded for each. None of them is a count to re-cut.

## 10. The releasing seat's own NEVER-2 ledger

The releasing seat opens its own change-management entry under org/critical_paths/change_management/ at the start of the release, naming every leg:
1. the publisher change and the registry row, as one leg;
2. the route declaration and its Lambda deploy, as a leg, with the rollback in section 5;
3. the export source kind, as a leg;
4. the first exercise on 49 Financial, its read-back of the new object and the new route, as a leg;
5. the read of the new route's scope refusal for an uncovered viewer, as a leg.

Each leg is read after it runs. This packet does not predict a value.

## 11. What the pair does NOT touch

The pair does not touch holdings, of any firm. It does not touch the summary route (the summary route, its operation and its object summary.json). It does not touch any existing object of any firm, including series.json.gz, manifest.json and summary.json. It does not touch any served value. It does not touch the account route. It does not touch the bronze or silver layers. It does not touch the cottonwood or inflection pins.

## 12. What this packet does not measure

This packet measures nothing live. The live deployment, the live IAM policy, the live schedule state and every live object were not read: no AWS call was made. The publish schedule's cron lines (85 and 122 of schedule.tf) are carried from the repository record, not re-read. The document is not built: no sample is run, and the 49 Financial document is not read. The portal's consumers of the new route are not measured. Hop 5 is not measured.

The order's file sites were checked at the base commit by the check. Their line numbers were read by this worker, and they may move at the release. A moved line is a file site the release re-reads, not a new packet.

## 13. Signatures

COO half: 2.0.0_SA_COO~P2 -- UNSIGNED at these packet bytes.

CTO half: 1.0.0_SA_CTO -- UNSIGNED at these packet bytes.

The packet's own sha256 is left for the signers and is not computed here.
