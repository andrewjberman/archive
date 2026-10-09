# Never-widen sign-off packet -- IB-pr-405: the owned request read returns the persist inputs; svc-custody-statement reads it for cottonwood only

Prepared by 0.9.0_WK_IRPT_BCKEND~268 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO msg 3088, IRPT_DASHBD ADDENDUM 9.2 (2)). Nothing here was uploaded, deployed, applied or written: BUILD_ONLY from a clean tree, offline replays, AWS reads only (2026-10-09 ~11:0xZ). Files beside this packet: `IB106-1_release_census.json`, `IB106-1_release_replay.json`, `replay/` (the scripts and the raw outcomes of both sides). Model: `0.9.0_WK_IRPT_BCKEND~262/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-394.md`.

**READ THIS FIRST.**

1. **The artifacts below are built at a CANDIDATE source map, not the real one.** `infra/aws/lambda/ci/lambda-source-map.json` pins irpt-status's `served.py`, `entry.py` and `owned_report.py` to older commits, so a build at the real map does not carry this change; the map is outside this order's grant. The builds use `BAU_SOURCE_MAP_OVERRIDE` with a scratch copy in which ONLY irpt-status's `staged_from` rows listed under Branch A step 1 are re-pinned to the pin. **The applier commits those seven rows (a map edit), rebuilds at the REAL map, and compares the printed sha256 to the table: ABORT if different.** (Row IRPT_BCKEND-D2-W268-S1.)
2. **The irpt-status release is wide, and most of it is other cells' pending work.** Live irpt-status is behind the real map already (AR-y-22's `/original` route and TO-AR-y-11's `ticket_id` are staged but not live), and the persisted-report half of `report_index` needs the retention stack the packaged zip lacks (`retention.py` has no policy-revision support, `repository.py` does not list CUSTODY_REPORT, the packaged registry has no `irpt-custody-x10-v1` row). The candidate therefore also re-pins `retention.py`, `repository.py`, `composition.py` and `reporting_policies.json`; they carry the IB-pr-386 service-principal rules and the AR-t-12 writer into irpt-status. **10 of 49 members change versus live; 3 are this cell's.** The table under "What moves" names each member's owner. (Row IRPT_BCKEND-D2-W268-S2, ARMED.)
3. **Only irpt-status needs a deploy.** The other seven functions package `served.py` too, at the old pin, so their built zips do not change (5 of 7 are byte-identical to their live zips; irpt-narrative and irpt-ycharts-generate differ from live for reasons that are not this release). They are in the census so the signer sees the whole set.
4. **Not replayed:** whether the gateway/edge admits the svc-custody-statement token on `GET .../analysis/requests/{requestId}` (outside the zip). The retention service in the replay is a double. Both are the after-read's first checks. (Row IRPT_BCKEND-D2-W268-S3.)

## What changed in code (commits `1cb1c965f3`, `9489a0fed0`)

- **Route and operation extended:** `GET /api/scoped/investor-reporting/analysis/requests/{requestId}`, operation `analysis-request-read` (served by irpt-status). No new route. The new member is **opt-in**, `?include=persist_inputs` (a comma list with `comparisons` and `composition`), like the two existing includes: a caller that does not ask gets `{identity, accepted_at}` key for key.
- **`persist_inputs`** (`OwnedAnalysisReader.persist_inputs`, `ops/owned_report.py`; `ops/entry.py` merges it), exactly four members, each read from the record the read already loads:
  - `artifact_id` = `composition_ref.artifact_id` of the accepted record (`ART-<64 hex>`, the retained request `custody-report-persist` takes);
  - `composition_sha256` = `composition_ref.sha256`;
  - `retention_policy` = `composition_ref.retention_ref.policy_revision` (read, never typed; the runner's DB41-3-AC1 compares it to `irpt-custody-x10-v1`, and the registry registers REQUEST_COMPOSITION under `irpt-x10-v1`, row IRPT_DASHBD-W61-S3);
  - `report_index` = `{report_id, revision, retention_ref}` of the persisted CUSTODY_REPORT row, found by the repository's own identity formula over the artifact's stored owner and one consistent prefix query (`Limit` 2) on the same table; `null` when none is persisted; more than one revision is refused, never chosen.
- **Re-authorized per request** through the read's existing path: `_materialize` (owner binding, the current grant via `authorize_current`, the retained composition reference), the report row bound to owner, tenant and retention chain with `require_live(accepted=True)`, then `_final` (record unchanged, retention `require_live`). Another firm and a non-owner are refused (replay arms below).
- **svc-custody-statement** (`_authz/served.py`): `SVC_CUSTODY_STATEMENT_OPERATIONS` gains the ONE operation `analysis-request-read` (now 4). Its firm stays the registry's cottonwood (`_svc_custody_statement_firm`), it is never `internal` (no any-firm or ALL reach, `selected_tenant` of another firm is FIRM_BINDING), and a sibling owned read (`analysis-request-history`) is still refused. Because the grant is the operation, svc can also make the plain read of a cottonwood request; as an OPAL_GLOBAL principal it reads any owner's cottonwood request, as every Opal reader does.
- **No IAM change:** `irpt-status-role` already allows `dynamodb:Query` and `GetItem` on `irpt-requests` (policy `irpt-status-policy`, Sid `ReadJobLeasesCheckpointsAndRequestRevisions`, read 2026-10-09). No route, schedule, environment or layer change.
- **Tests:** `ops/tests/test_persist_inputs.py` (11) and `_authz/tests/test_svc_custody_statement.py` (the `persist_inputs` tests): e.g. `test_persist_inputs_owner_reads_all_four_members`, `test_persist_inputs_other_firm_is_refused_before_any_read`, `test_persist_inputs_non_owner_in_the_same_firm_is_refused`, `test_svc_custody_statement_persist_inputs_read_cottonwood_admitted`, `test_svc_custody_statement_persist_inputs_other_firm_claim_refused`.

## The pin and the builds

- **Release pin P: `9489a0fed03951fb242e50a7a1f704f307946e3c`** (branch `wk-IRPT_BCKEND-268`). The code is `1cb1c965f3` and `9489a0fed0`; every later commit on the branch is deliverables only. The candidate-map rows point at P.
- BUILD_ONLY from a clean tree (`git status --porcelain` 0 lines before and after every build), each function built twice (18 builds), **byte-identical between runs: YES**, rc 0. Command: `BUILD_ONLY=1 TMPDIR=<scratch> BAU_SOURCE_MAP_OVERRIDE=<candidate map> bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>`. Zips kept only in scratch; nothing uploaded; the real source map untouched.
- Live read with `aws lambda get-function` (the downloaded zip's sha256 equals the reported CodeSha256 for all 8) and `aws s3api list-object-versions` (latest version = the rollback version).

| Function | Built sha256 (base64, = the BUILD_ONLY line) | built bytes | live_before (CodeSha256) | Rollback S3 version | Deploy? |
|---|---|---|---|---|---|
| `irpt-status` | `gff0DKwarcDa/GJHNpPN0UVV+57Bxg4VPnqxglN/EPY=` | 360665 | `E7VKvhg3E9D5euWO+S649/iyAJ05xUmFPqHEAKDTFxA=` (2026-10-09T07:43:46Z) | `2R.qpR7BQnBXtBgcR87_keqLT5Tg96Jl` | **YES** |
| `irpt-performance-adapter` | `o/643qVECx5UU4Z9sknDp5yUJZb81Zfvp873yDNsc1w=` | 441258 | `o/643qVECx5UU4Z9sknDp5yUJZb81Zfvp873yDNsc1w=` (2026-10-09T07:41:59Z) | `P2.k8l8dqM7nlKcd8O1.Hzo5ugCCceiR` | no (built = live) |
| `irpt-directory-search` | `RwgwXI5+xiss9h7OmVPqk6EujzQalXYCciQkvTBGj+c=` | 193302 | `RwgwXI5+xiss9h7OmVPqk6EujzQalXYCciQkvTBGj+c=` (2026-10-09T07:38:06Z) | `MjZTtOj09NrJCiHLBUmYt_38x9JBgCx8` | no (built = live) |
| `irpt-narrative` | `QiNRKpaCoX5gIGmt8ypj34l3noLeroXqwWLprr68Pmw=` | 215376 | `es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=` (2026-09-21T15:05:28Z) | `ELQQZdHYUJHbDZSOxC2AAKQ_nXFqApoJ` | no (built differs from, for reasons outside this release, live) |
| `irpt-ycharts-generate` | `oWO2Brnx7HWr1vPBMClJlDeRAYts1YlctqF9AgW6fiM=` | 614708 | `tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=` (2026-10-09T09:32:22Z) | `.epN9U3xZSMhU5WmEudwCrbjnydqg4N6` | no (built differs from, for reasons outside this release, live) |
| `irpt-export-render` | `c7jOyysB/zo6OjtzCNdUZiu0o4fxNE9XeCM1FxXIHhk=` | 418286 | `c7jOyysB/zo6OjtzCNdUZiu0o4fxNE9XeCM1FxXIHhk=` (2026-10-09T07:47:08Z) | `3xfTd055xcuh84iYVxtLUu3LzWt6bFha` | no (built = live) |
| `irpt-holdings` | `CKpZUMD5RVWyY/2oyo8zZwN7Ss8J2FbkeNFr2XYbXD8=` | 298954 | `CKpZUMD5RVWyY/2oyo8zZwN7Ss8J2FbkeNFr2XYbXD8=` (2026-10-09T09:11:24Z) | `EXYWixzhP1B6gsNLQC1guU6jYE8uqV_g` | no (built = live) |
| `irpt-49f-reporting-read-lambda` | `8ySmTtYXTqZgnpFY/cnFKnbsGGO/qm6qLCxGLXhIVCI=` | 280560 | `8ySmTtYXTqZgnpFY/cnFKnbsGGO/qm6qLCxGLXhIVCI=` (2026-10-09T07:36:18Z) | `2iKVUY7CiWJvX2WaCmY8hd7OTf48Uupy` | no (built = live) |

Minimal alternative for irpt-status (rows 1-3 only: `served.py`, `entry.py`, `owned_report.py`): built sha256 `FMkzsPFsg55VKLtg3tjicq1M5M6sh5CmIlQlYG6BNxI=`. With it `persist_inputs` answers three members and `report_index` null, but is **expected to refuse whenever a report IS persisted** (reasoned from the packaged `retention.py`, whose `reference()` takes no policy revision; not replayed). Not recommended: the runner's read after its own persist would refuse.

## What moves in irpt-status (10 members versus live)

| Member | Live blob | Built blob | Class | Owners since the live blob (latest first) |
|---|---|---|---|---|
| `acceptance.py` | `eeb01ee15cb0` | `06425d4731b7` | already pending in the REAL map: another cell's staged pin is ahead of the live blob | 1eed34a8c0 0.9.0_WK_IRPT_ANLREQ~1: feat(IRPT_ANLREQ TO-AR-y-11): the analysis submission carries ticket_id int |
| `composition.py` | `6d2c3696d030` | `5b896004af77` | stack row re-pinned so report_index can be read (retention policy revision support, CUSTODY_REPORT kind, the irpt-custody-x10-v1 policy row) | 2aa217ec58 0.9.0_WK_IRPT_BCKEND~177: build(IRPT_BCKEND.TO-IB-pr-369, 0.9.0_WK_IRPT_BCKEND~177): ReportReposito; f60e6f1d2a 0.9.0_WK_IRPT_YCDGEN~3: work(0.9.0_WK_IRPT_YCDGEN~3): YCD-l-6 Opal PDF under its own policy row, re |
| `entry.py` | `ab030a7479b4` | `4a5dd2e887cb` | IB-pr-405 own member (re-pinned in the candidate map) | 1cb1c965f3 0.9.0_WK_IRPT_BCKEND~268: feat(IRPT_BCKEND IB-pr-405): analysis-request-read returns persist_inputs; eb70303e8f 0.9.0_WK_IRPT_ANLREQ~3: feat(IRPT_ANLREQ AR-y-22, 0.9.0_WK_IRPT_ANLREQ~3): original-file reader in  |
| `infra/logic/registry/reporting_policies.json` | `2bd3520dd386` | `1479826b5764` | stack row re-pinned so report_index can be read (retention policy revision support, CUSTODY_REPORT kind, the irpt-custody-x10-v1 policy row) | eab13e88d3 0.9.0_WK_IRPT_YCDGEN~9: feat(IRPT_YCDGEN YCD-a-7, 0.9.0_WK_IRPT_YCDGEN~9): research policy row firm; 589aee38f0 0.9.0_WK_IRPT_ANLREQ~41: build(IRPT_ANLREQ.TO-AR-t-12 AMENDMENT 4, cell AR-t-13, 0.9.0_WK_IRPT_ANLR; 0c35aeeaa8 2.0.0_SA_COO~M2: registry(IRPT_BCKEND E8, 2.0.0_SA_COO~M2): irpt-custody-x10-v1 ACTIVE, enforcement |
| `owned_report.py` | `74e50366bc3e` | `3a6066b2e0da` | IB-pr-405 own member (re-pinned in the candidate map) | 9489a0fed0 0.9.0_WK_IRPT_BCKEND~268: fix(IRPT_BCKEND IB-pr-405): persist_inputs spells the custody report iden; 1cb1c965f3 0.9.0_WK_IRPT_BCKEND~268: feat(IRPT_BCKEND IB-pr-405): analysis-request-read returns persist_inputs; 62880e9bfc 0.9.0_WK_IRPT_ANLREQ~3: fix(IRPT_ANLREQ AR-y-22, 0.9.0_WK_IRPT_ANLREQ~3): PdfSigner.sign takes a fa |
| `pdf_link.py` | `e190527f60a3` | `41d98e94d39e` | already pending in the REAL map: another cell's staged pin is ahead of the live blob | no staged_from row |
| `repository.py` | `f255335beb26` | `d94dc2c74c75` | stack row re-pinned so report_index can be read (retention policy revision support, CUSTODY_REPORT kind, the irpt-custody-x10-v1 policy row) | 3fc99be70f 0.9.0_WK_IRPT_ANLREQ~41: feat(IRPT_ANLREQ TO-AR-t-12 amendment 5 steps 11-13): retention admits the; 589aee38f0 0.9.0_WK_IRPT_ANLREQ~41: build(IRPT_ANLREQ.TO-AR-t-12 AMENDMENT 4, cell AR-t-13, 0.9.0_WK_IRPT_ANLR; 20534db618 0.9.0_WK_IRPT_BCKEND~197: IB-pr-386: ArtifactRepository.get() admits ONE named service subject, svc |
| `retention.py` | `bdd74e5f9b90` | `9da406b7d6e4` | stack row re-pinned so report_index can be read (retention policy revision support, CUSTODY_REPORT kind, the irpt-custody-x10-v1 policy row) | 3fc99be70f 0.9.0_WK_IRPT_ANLREQ~41: feat(IRPT_ANLREQ TO-AR-t-12 amendment 5 steps 11-13): retention admits the; 20534db618 0.9.0_WK_IRPT_BCKEND~197: IB-pr-386: ArtifactRepository.get() admits ONE named service subject, svc; f60e6f1d2a 0.9.0_WK_IRPT_YCDGEN~3: work(0.9.0_WK_IRPT_YCDGEN~3): YCD-l-6 Opal PDF under its own policy row, re |
| `served.py` | `87d9ecc49747` | `ada9bf5bcfd1` | IB-pr-405 own member (re-pinned in the candidate map) | 1cb1c965f3 0.9.0_WK_IRPT_BCKEND~268: feat(IRPT_BCKEND IB-pr-405): analysis-request-read returns persist_inputs |
| `submission.py` | `9929a829047f` | `82c47bd021c5` | already pending in the REAL map: another cell's staged pin is ahead of the live blob | 1eed34a8c0 0.9.0_WK_IRPT_ANLREQ~1: feat(IRPT_ANLREQ TO-AR-y-11): the analysis submission carries ticket_id int |

Everything else in the zip (39 of 49 members) is byte-identical to live.
The `irpt-x10-v1` policy row is byte-equal at both registry pins (so no retained record's `policy_sha256` moves); the `irpt-ycdgen-research-v1` row changes state PENDING_ENFORCEMENT to ACTIVE and its firms to three (YCD-a-7), and `irpt-custody-x10-v1` and `irpt-anlreq-x10-v1` are added.

## Blast radius

- **Functions touched:** `irpt-status` only (Lambda code). **Served output:** `analysis-request-read` gains an opt-in member; every other irpt-status route answers as the pinned stack makes it (the AR-y-22 `analysis-request-original` operation is installed in the handler: replay arm `installed_handler_composes`). **Authorization reach:** svc-custody-statement gains one operation, bound to cottonwood; no other subject, firm or operation. **No** IAM, route, schedule, table, environment or layer change; no data written.
- **Carried with it (other cells' pending changes, named in the table):** TO-AR-y-11 (`acceptance.py`, `submission.py`: `ticket_id` in the accepted record), AR-y-22 (`entry.py`, `owned_report.py`, `pdf_link.py`: the `/original` link), IB-pr-369/YCD-l-6/IB-pr-386/AR-t-12 (the retention stack), E8/YCD-a-7/AR-t-12 (registry rows). Each is already staged in the real map or in a function that serves it live; the signer reads this release as carrying them.
- **Writers of the changed property:** the Lambda code object of `irpt-status` has one writer, the Terraform apply of `infra/aws/terraform/investor-reporting/ops/lambda.tf` (`module.irpt_status`, source `investor-reporting/irpt-status.zip`). N writers = 1; N rules read = 1 (the build + apply path).

## Branch A (released)

0. **Ledger:** open `org/critical_paths/change_management/` BEFORE the first act; it names every task family or function that pulls the moved key (`investor-reporting/irpt-status.zip`: the irpt-status function only); close it after the after-read.
1. **Commit the map rows** (an edit to `infra/aws/lambda/ci/lambda-source-map.json`, `functions.irpt-status.staged_from`, the applier's/issuer's act): set `pin` and `sha256` of exactly these rows to the values in the last two columns (the same values are in `replay/candidate_map_rows.json`):

| packaged_as | repo_path | pin before | pin after | sha256 after |
|---|---|---|---|---|
| `served.py` | `infra/aws/lambda/investor-reporting/_authz/served.py` | `74a62fb46c` | `9489a0fed03951fb242e50a7a1f704f307946e3c` | `ada9bf5bcfd107398eacf49d8051e61551ff253c33cf216d9dd404363f7e630e` |
| `composition.py` | `infra/aws/lambda/investor-reporting/reports/composition.py` | `80a79a7462` | `9489a0fed03951fb242e50a7a1f704f307946e3c` | `5b896004af77477ad9a49e5f98a332f9b899df9bbedd0abc5899e2d62c3e9249` |
| `repository.py` | `infra/aws/lambda/investor-reporting/reports/repository.py` | `80a79a7462` | `9489a0fed03951fb242e50a7a1f704f307946e3c` | `d94dc2c74c7552a4ba414261f314fdf3ca6bee9f9991acd7fe9b63e95760ec88` |
| `retention.py` | `infra/aws/lambda/investor-reporting/reports/retention.py` | `80a79a7462` | `9489a0fed03951fb242e50a7a1f704f307946e3c` | `9da406b7d6e442deb61a6d4a360f66a057741b21c1ecf33e3ab68ef2298c973f` |
| `infra/logic/registry/reporting_policies.json` | `infra/logic/registry/reporting_policies.json` | `80a79a7462` | `9489a0fed03951fb242e50a7a1f704f307946e3c` | `1479826b57642ff871372bbfdceccb01410ec640f77c3785c6f94ced40069990` |
| `entry.py` | `infra/aws/lambda/investor-reporting/ops/entry.py` | `eb70303e8f` | `9489a0fed03951fb242e50a7a1f704f307946e3c` | `4a5dd2e887cb2dcc63d0fb31684cb988757e7953dad83ea727146cd5b97241af` |
| `owned_report.py` | `infra/aws/lambda/investor-reporting/ops/owned_report.py` | `62880e9bfc` | `9489a0fed03951fb242e50a7a1f704f307946e3c` | `3a6066b2e0daf44cde8b4daeb58a05e0afd41c259b5f2cbfcef853b2363940ee` |

2. **Rebuild at the REAL map from a clean tree** (P or a descendant whose map, `_authz/`, `ops/` and `reports/` are unchanged): `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-status`; the printed sha256 must be `gff0DKwarcDa/GJHNpPN0UVV+57Bxg4VPnqxglN/EPY=`. ABORT if different.
3. **Upload and deploy:** the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-status.zip`), then the Terraform path of the function (`safe-apply` on the ops root; never `aws lambda update-function-code`). Expected plan: one in-place update of `module.irpt_status.aws_lambda_function.this` (`source_code_hash`), no IAM/route/env change.
4. **Before the first real call,** run the replay arm below against the bytes actually uploaded.
5. **Served effect:** owner and firm users see the same answers as today for every route they use (replay: the existing-caller arms are identical); the runner reads `?include=persist_inputs` as svc-custody-statement for cottonwood.

## Branch B (rolled back)

- `irpt-status`: redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `2R.qpR7BQnBXtBgcR87_keqLT5Tg96Jl` of `investor-reporting/irpt-status.zip` (its CodeSha256 is the `live_before` value `E7VKvhg3E9D5euWO+S649/iyAJ05xUmFPqHEAKDTFxA=`). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and that version still the latest.
- The other seven functions: nothing to roll back (not deployed by this release). Their current rollback versions are in the table.
- Revert the seven map rows with their commit. No other state: no table row, IAM, schedule or environment is written. If the svc-custody-statement read has already been used, nothing it did persists (it is a read).

## The replay (26 arms: 16 identical, 10 expected-diff, 10 negative controls)

Recorded in `IB106-1_release_replay.json`; harness `replay/run_side.py` (the REAL irpt-status modules of one extracted zip in the flat layout, `entry.build_owned_entry` and `served.lambda_entry`, offline doubles for storage only), raw outcomes of both sides in `replay/raw/`. Synthetic fixtures, no client data.

| arm | verdict | negative control |
|---|---|---|
| ctl_recovered_owner_include_persist_inputs [ctl_recovered_owner_include_persist_inputs] | expected-diff | no |
| ctl_retention_dead_owner_include_persist_inputs [ctl_retention_dead_owner_include_persist_inputs] | expected-diff | yes |
| control: owner plain read with retention dead: refused on both sides [ctl_retention_dead_owner_plain] | identical | yes |
| control: two report revisions under one report id: the built read refuses, never chooses (live refuses the include) [ctl_two_report_revisions_owner_include_persist_inputs] | identical | yes |
| non-owner in the same firm, include=composition: refused on both sides [non_owner_same_firm_include_composition] | identical | no |
| non-owner in the same firm, include=persist_inputs: refused on both sides [non_owner_same_firm_include_persist_inputs] | identical | yes |
| non-owner in the same firm, plain read: refused on both sides [non_owner_same_firm_plain] | identical | no |
| another firm, include=composition: refused on both sides [other_firm_include_composition] | identical | no |
| another firm, include=persist_inputs: refused on both sides [other_firm_include_persist_inputs] | identical | yes |
| another firm (cottonwood advisor, 49financial request), plain read: refused on both sides [other_firm_plain] | identical | no |
| existing caller, owner, include=comparisons: identical [owner_include_comparisons] | identical | no |
| existing caller, owner, include=composition: identical [owner_include_composition] | identical | no |
| owner_include_persist_inputs_not_persisted [owner_include_persist_inputs_not_persisted] | expected-diff | no |
| owner_include_persist_inputs_persisted [owner_include_persist_inputs_persisted] | expected-diff | no |
| existing caller, owner, no include: the answer {identity, accepted_at} key for key [owner_plain] | identical | no |
| svc-custody-statement claiming 49financial: not the subject, refused on both sides [svc_claims_49financial] | identical | yes |
| svc-custody-statement claiming inflection: not the subject, refused (an ordinary-user rule) on both sides [svc_claims_inflection] | identical | yes |
| svc-custody-statement (cottonwood) asking for a 49financial request: refused on both sides [svc_cottonwood_for_49financial_request] | identical | yes |
| svc-custody-statement (cottonwood) on the sibling owned read analysis-request-history: still refused on both sides (the grant is ONE operation) [svc_cottonwood_history_sibling_read] | identical | yes |
| svc_cottonwood_include_persist_inputs [svc_cottonwood_include_persist_inputs] | expected-diff | no |
| svc_cottonwood_plain_read [svc_cottonwood_plain_read] | expected-diff | no |
| another service email (svc-commentary) claiming cottonwood: refused on both sides [svc_other_email_cottonwood] | identical | yes |
| static: packaged_policy_irpt_custody_x10_v1 (what the zip carries) | expected-diff | no |
| static: packaged_retention_reference_params (what the zip carries) | expected-diff | no |
| static: packaged_repository_KINDS (what the zip carries) | expected-diff | no |
| static: installed_handler_composes (what the zip carries) | expected-diff | no |

**Arm for the applier (rerun against the uploaded bytes):** extract the live irpt-status zip (after the upload, `aws lambda get-function` Code.Location) into an EMPTY directory outside the worktree, then `python -I replay/run_side.py <dir> built <out.json>` and compare to `replay/raw/replay_built.json` arm by arm (the `static` block and every `arms.*` outcome). STOP if the `svc_cottonwood_include_persist_inputs` arm is not admitted with four members, if any `other_firm_*`, `non_owner_*` or `svc_claims_*` arm answers data, or if `ctl_retention_dead_owner_include_persist_inputs` answers data (the harness would then not be reaching the retention check).

## The after-read

1. One `GET /api/scoped/investor-reporting/analysis/requests/{requestId}?include=persist_inputs` as svc-custody-statement (cottonwood request): expect `data.persist_inputs` with exactly `artifact_id`, `composition_sha256`, `retention_policy`, `report_index`. A 403 from the gateway/edge instead of the Lambda answer means the edge does not admit the svc token on this GET route (row W268-S3): that is outside this cell and is read first.
2. The same request as an ordinary advisor of another firm: refused. The same without `include`: `{identity, accepted_at}` as before. CloudWatch shows no `TypeError` or `KeyError` in the `irpt-status` log group.
3. Until the apply, every one of these is UNEXERCISED against the live service; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.

## Rows

`IRPT_BCKEND-D2-W268-S1` (the source map pins the three members; candidate map used; OBSERVATION, INERT), `IRPT_BCKEND-D2-W268-S2` (irpt-status carries other cells' pending changes and needs the retention stack; OBSERVATION, ARMED, disarm owner 2.0.0_SA_COO~P2), `IRPT_BCKEND-D2-W268-S3` (the published contract does not name `include=persist_inputs` or the member; edge admission unverified; OBSERVATION, INERT). Related, not this cell's: `IRPT_BCKEND-D2-S43`, `IRPT_DASHBD-W61-S2/S3`.
