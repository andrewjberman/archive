# r57 direct-invoke payloads (read-only preparation for 2.0.0_SA_COO~P)

Prepared 2026-10-05 against CLOUD HEAD (re-pin target `0642c9d004`). Plan: `../RELEASE_R57_PLAN_20261005.md`.
CTO half: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_IRPT_BCKEND_RELEASE_R57_20261005.md`.
Ledger: `org/critical_paths/change_management/20261005T1453Z_irpt-r57-repin-release-20261005_deploy_completion.md`
(legs RR1/RR3, ER1/ER3, DS1/DS3, HO1/HO3).

## 1. Headline finding: three of the four refusal-code changes do not show in any response

The re-pinned `loaders.py` gives `BucketUnmapped` the code `FIRM_BINDING` and adds `FirmArtifactIncomplete` with the code
`NOT_READY` (`_authz/loaders.py:43-53` at `0642c9d004`). In these four functions, both exceptions are raised only inside
`Entry.enforcer_for` (`opaque_firm_for` -> `load_directory` -> `bucket_for`). That call site hard-codes the public code
(`_authz/served.py:1050-1054`, the same in all three served.py blobs that ship: `4624fe7f`, `54787849`, `c02999a2`):

    code = "FIRM_BINDING" if isinstance(exc, _enforce.AuthzError) else "UNEXPECTED"

That line never calls `public_reason_for`, so the response stays `UNEXPECTED` before and after the deploy. The one surface that
moves is the server-side CloudWatch record. `_record` (`served.py:89-108`) prints an `irpt_internal` JSON line whose
`extra.classifier_code` is `errors.reason_for(exc)` (`_authz/errors.py:116-143`, which reads the declared `public_reason_code`
first). This line moves from `UNEXPECTED` to `FIRM_BINDING`. The public `irpt_error` line also stays `UNEXPECTED`.

The other changed members do not reach a response through any route these functions serve:
- **S241 (`served.py` import move).** It matters only if `canonical_profile_reads` is missing, and that module is packaged.
- **S175 (`maintained_sources` / `canonical_profile_reads` subclasses).** They are raised only under
  `_service_allowed_firms`, which catches everything and returns `[]` (`served.py:949-971`).

So for reporting-read, directory-search and holdings, the closest observable is the log record, not the payload. The plan's
line "a refusal answers its class where it answered UNEXPECTED" does not hold on the wire for this release. A wire change
would need `enforcer_for` to classify through `public_reason_for`, which is `served.py` code and not part of r57.

## 2. How the functions read the principal (all four)

- **No JWT, no requestContext claims.** The boundary reads the edge validator's injected `X-*` headers from `event.headers`.
  `requestContext.headers` is only a fallback location for the same header map (`_authz/served.py:249-258`).
- **The trusted header set** is the nine names in `_scope/resolve.py:104-114`, plus the three render markers. Everything else
  is dropped.
- **Internal (Opal) principal.** These conditions make the request internal (`served.py:261-272`): `x-origin-verify:
  cloudfront`, an `x-user-email`, a role that is not `renderer`, and `x-firm-id: opal-capital` or `x-user-type: Dev`.
  - An internal request may name a partner with `selected_tenant`. That tenant must pass `bucket_for`
    (`served.py:1006-1020`).
  - The email then goes on the OPAL_GLOBAL roster for the request (`served.py:1047-1049`; `resolve.py:281-283`), which sees
    the selected firm's whole population (`resolve.py:436-441`).
  - `x-user-type` is `internal`, not `service`, so no DynamoDB profile row is read.
- **No secret in any payload.** A direct invoke bypasses the CloudFront edge and the API authorizer (`naqxlm`). The trust
  anchor is the caller's `lambda:InvokeFunction` permission.

**Happy principal** (every happy payload, and export-render's change payload): `opal@example.invalid`, `x-firm-id
opal-capital`, `x-user-type internal`, `x-user-role admin`, with `selected_tenant=49financial`. The source is the repo's own
test `_authz/tests/test_interactive_entry.py:15-21`. The header shape matches the earlier live direct-invoke event
`org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/status_live_read_event.json:1`.

**Change principal** (reporting-read, directory-search, holdings):
- An advisor-shaped header set from `_authz/tests/fixtures.py:134-140` (`ADV-A-0001`, `x-user-type Advisor`), with
  `x-firm-id` set to `mockadv` and the email set to `r57-change-probe@example.invalid`.
- `mockadv` is a registry firm of kind `test` (`data/firm_registry.json:88`). Every bucket map these functions carry holds
  client firms only, so `mockadv` is unmapped in all four. The maps: `holdings/lambda.tf:38-41`, `export/iam.tf:263`,
  `directory/iam.tf:48`, and `reporting-read/locals.tf:57-59` (49financial only).
- `bucket_for` raises before any S3 call, so this payload makes no storage read.
- Equivalent alternative: the happy principal with no `selected_tenant`. `opal-capital` is then the tenant, which is also
  unmapped.

Contract header on every payload: `x-contract-version: v1` (`served.py:71-72`).

## 3. Per function

### irpt-49f-reporting-read-lambda

- **Handler:** `entry.lambda_handler`. Source: `infra/aws/lambda/investor-reporting/reporting/entry.py:391`, Terraform
  `reporting-read/lambda.tf` (`handler`).
- **Changed members:** `canonical_profile_reads`, `loaders`, `maintained_sources`, `served`
  (`r57_census/census-irpt-49f-reporting-read-lambda.json`).
- **happy.json:** `GET /api/scoped/investor-reporting/reporting/{account_id}/{which}` (`entry.py:90`) with `account_id`
  `acc_5475ef6b78036e90a79eba33` and `which=manifest`.
  - The account is the 49F ****0090 account of the READY export: `../IRPT_BCKEND_ROUNDS_42_44_P_DRAIN_END_20261004.md:27`.
    Its raw key `acct#97c956cc` has a published platinum series
    (`surprise-channel/investigations/INVESTIGATION_v1.md:17643`, row W116-S11).
  - Read path: ListBucket on the platinum prefix and GetObject on `manifest.json`. Nothing is written.
  - **Response, before and after (identical):** the raw HTTP response, not the envelope: `statusCode` 200,
    `Content-Type application/json`, an `ETag`, `isBase64Encoded: true`, and a base64 manifest body (`entry.py:285-295`).
  - If the manifest is not published, the answer is `ok:false NOT_READY` on both sides. That is still a valid equality check.
- **change.json:** the same route with the unmapped `mockadv` principal.
  - **Response, before and after (identical):** `{"ok": false, "contract_version": "v1", "operation": "reporting-read",
    "status": {"state": "UNAVAILABLE", "public_reason_code": "UNEXPECTED", ...}}`.
  - **What moves:** the function log's `irpt_internal` line (`exception_type BucketUnmapped`). Its
    `extra.classifier_code` is `UNEXPECTED` before and `FIRM_BINDING` after.

### irpt-directory-search

- **Handler:** `entry.lambda_handler` (`directory/entry.py:428`; Terraform `directory/lambda.tf`).
- **Changed member:** `loaders` only.
- **happy.json:** `GET /api/scoped/investor-reporting/directory/browse?limit=1&selected_tenant=49financial`
  (`entry.py:343-352`, `browse` at `:272-334`). Pure over the directory artifact, so nothing is written.
  - **Response, before and after (identical):** an envelope whose `data` is `{entries:[1 DirectoryEntry], next_cursor,
    directory_revision, scope_fingerprint}`.
  - The entry carries one client display name. Compare it by shape and count, not by printing it.
- **change.json:** `directory/browse` with the `mockadv` principal.
  - **Response, before and after (identical):** `UNEXPECTED`, operation `directory-browse`.
  - **What moves:** the log's `classifier_code`, from `UNEXPECTED` to `FIRM_BINDING`.

### irpt-holdings

- **Handler:** `entry.lambda_handler` (`holdings/entry.py` at pin `21eca74f40`; Terraform `holdings/lambda.tf`).
- **Changed member:** `loaders` only. The HoldingsSnapshot contract member is unchanged.
- **happy.json: NOT USABLE AS-IS.**
  - The route is `GET /api/scoped/investor-reporting/holdings/{accountSetId}` (`holdings/snapshot.py:62`).
  - It needs a `sel_<64 hex>` selection bound to the CURRENT directory revision. `_scope/selection.py:110-124` at the pin
    refuses a selection whose `directory_revision` differs ("select again").
  - Every `sel_` id in the repo comes from 09-26 to 10-03 walks and is almost certainly stale. The payload carries the
    placeholder `REPLACE_WITH_A_CURRENT_49F_SELECTION_sel_64hex` in `pathParameters.accountSetId`, `rawPath` and
    `requestContext.http.path`.
  - **To fill it:** read a 49F `SELECTION#` row created today from the `IRPT_REQUESTS_TABLE` (a read). Creating one through
    `POST /selections` is a write.
  - **With a current selection, before and after (identical):** an envelope whose `status.public_reason_code` is
    `HOLDINGS_READY` (or `OBJECT_NOT_COVERED`/PARTIAL), with `state READY`.
  - **With a stale or placeholder id, before and after (identical):** `OBJECT_NOT_COVERED` (SelectionRefused). That is an
    acceptable baseline-equality read, but not a success.
- **change.json:** usable as-is. The `mockadv` principal with a dummy `sel_000...0` id; the refusal happens before the
  compute.
  - **Response, before and after (identical):** `UNEXPECTED`, operation `holdings-snapshot`.
  - **What moves:** the log's `classifier_code`, from `UNEXPECTED` to `FIRM_BINDING`.

### irpt-export-render

- **Handler:** `entry.lambda_handler` (`export/entry.py:444`; Terraform `export/lambda.tf`). A non-HTTP event carrying the
  `submit_async` marker takes another branch; these payloads do not carry it.
- **Changed members:** `bundle.py`, `ExportBundle.schema.json`, `entry.py`, `loaders`, `served`.
- **happy.json:** `GET /api/scoped/investor-reporting/export/{exportId}` (`entry.py:409-416`) for the one READY receipt.
  - The receipt is `EXP-e29b5415a06f90f943481c41a1a4821b`, firm 49financial, at
    `s3://opal-data-ycharts/firms/49financial/generations/EXP-e29b5415a06f90f943481c41a1a4821b/receipt.json`. Evidence:
    `INVESTIGATION_v1.md` rows S312 (line 16918) and W116-S11, and `../IRPT_BCKEND_ROUNDS_42_44_P_DRAIN_END_20261004.md:28`.
  - **Response, before and after:** a served envelope whose `data` is the ExportReceipt: `job_state READY`, `facts.page_count
    11`, `facts.frozen_as_of 2026-10-01`, `vendor_signed_url_exposed false`.
  - **Expected identical.** The receipt was written 10-03 22:13Z by `receipt.build`, which has minted the live route since
    `c4fedd31c5` (10-02). Its stored `download_route.route` should already be the live route, which is the "already live,
    unchanged" arm of `export/tests/test_export_receipt_live_route.py:60-63`. Not measured: read the stored route at ER1.
  - **CAUTION, not read-only if the receipt is missing.** If the GET of `receipt.json` fails with NoSuchKey or AccessDenied,
    `export_receipt` falls into `_finalize_on_read` (`entry.py:233-238`). The EXP pending pointer exists, so that path can
    FINALIZE and WRITE a receipt. Before the invoke, read the receipt key with a `head-object` (a read).
- **change.json:** the same route, with the top-level `receipt_fixture` seam (`entry.py:108-110`). API Gateway cannot set
  this key, so only a direct invoke reaches it.
  - The repo's own guarded-entry test uses the same seam (`_authz/tests/test_guarded_entries.py:159-163`).
  - The fixture is the W101-S14 test's receipt (`export/tests/test_export_receipt_live_route.py:24-46`) with the stale route
    `/api/scoped/exports/<id>/download` (the pre-IB-pr-297 mint, `REMEDIATION_v18.md:1265`). It has no `account_ids`, so
    coverage is trivially met.
  - Read path: the 49F directory and ownership map only. There is no evidence-bucket read, so no finalize is possible.
  - **Before:** `data.download_route.route = /api/scoped/exports/EXP-5757.../download`.
  - **After:** `data.download_route.route = /api/scoped/investor-reporting/export/EXP-5757.../download` (`entry.py:248-258`,
    `receipt.py:25`).
  - This is the only payload in the set whose RESPONSE differs across the deploy. It exercises the change on a fixture
    receipt, not on a stored one.
  - No READY receipt with a stale route is identifiable in the repo. The IB-rtg-1 test receipt `EXP-564ce23c...` was deleted
    (`deliverables/0.9.0_WK_IRPT_BCKEND~1/IB-rtg-1_R72-AC1_battery_output.txt`, arm 6). The 09-27 and 09-29 exports FAILED at
    the render (W18/W19 ledgers).
- **S324 (`narrative_state NOT_ATTACHED`):** no read-only request reaches it. It is on the PATH B submit, which writes. The
  CTO's condition 3 places it on the bundle-validation test against the deployed package.
- **Refusal-code alternative (log only):** the `mockadv` principal on this route behaves like the other three functions.

## 4. Offline replay (no deploy, no invoke)

Script: `<scratchpad>/r57_offline.py`, session-local and not committed. It runs each payload through the REAL entry modules.
- **Old:** the live pins, with `loaders`/`served` (and export `entry.py`) taken from `git show` of `5f582dca` / `acce3642`,
  `f9a00f73`, and `c4fedd31` / `8d08ee54`.
- **New:** HEAD (`0642c9d004` blobs).

Results:
- **Change payloads, reporting-read, directory-search and holdings:** the response is `UNEXPECTED` in both, and the log's
  `classifier_code` moves from `UNEXPECTED` (old) to `FIRM_BINDING` (new).
- **Export change payload:** the route moves from `/api/scoped/exports/...` (old) to
  `/api/scoped/investor-reporting/export/...` (new).
- **Happy payloads, with recorded fixture deps:** every payload passed the boundary as OPAL_GLOBAL for 49financial and reached
  its compute. The fixture outcomes are not the live answers.

**DISCLOSURE.** The first replay of `irpt-export-render.change.json` ran without fixture deps. It used this machine's AWS
credentials and read the 49F directory pointer, the directory artifact and the ownership map from `opal-data-bd` (S3
GetObject only, nothing written). The other runs had storage stubbed and AWS endpoints disabled. No Lambda was invoked.

## 5. Uncertain

- Whether the reporting-read manifest for `acct#97c956cc` is currently published. If not, the answer is NOT_READY on both sides.
- The stored route inside the `EXP-e29b...` receipt has not been read.
- `selected_tenant` against the live bucket maps assumes the deployed `IRPT_DIRECTORY_BUCKET_MAP` equals the Terraform
  derivation.
- CloudWatch shows the `classifier_code` move only if the function's log group retains the `irpt_internal` line. It is
  printed to stdout.
