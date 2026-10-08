# Never-widen sign-off packet -- IB-pr-363 (E2): the custody release pair

Prepared by 0.9.0_WK_IRPT_BCKEND~171 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO~DELL2. Nothing in this packet was built, uploaded or applied.
Census file: `IB76-2_custody_release_census.json` (same folder).

## The pin

**Release pin: `1e0cdaf90cbab1f2979cfe849a1a31db1d110533`** (branch `wk-IRPT_BCKEND-171`). It is the one re-pin commit: in function
`irpt-export-render`, the `staged_from` row for `export/entry.py` moved from `34f71024a125d66b481aca2d7eaa00a4429781bc` /
sha256 `fc241d80...` to `cf6839fe3861675ee29ca4b3ef487a47dcfaf440` (the IB-pr-355 commit) / sha256 `b32032d38b94bd5768d8c09f0bc34331c64f8e466712f4ed4962e1a6a1f5e947`
(equals the blob at HEAD). Without it the build would ship the old `entry.py` and IB-pr-355's two ROUTES lines would not ship (measured: the census
at HEAD `0fdb85697e` listed only `submit_async.py` and `custody_read.py`; at the pin it lists `entry.py` too). No other row in any function was touched.

## Census (`release-census.py irpt-export-render --pin 1e0cdaf90c`, built 64 members, live 63)

| member | state | owner |
|---|---|---|
| `submit_async.py` | changed (built 5b6621f63ada, live ab033b5bdd3c) | IB-pr-352 (fd93958ce9: accept by resolved kind) |
| `custody_read.py` | added (built 73c7c812e556) | IB-pr-355 (cf6839fe38) |
| `entry.py` | changed (built b32032d38b94, live fc241d806ecc) | IB-pr-355 (cf6839fe38: ROUTES line + operation) |

No rider: every changed member is owned by a named order. Other functions: none packages any named file (`irpt-export-render` is the only
function whose `source_dir` + `files[]` carries `entry.py`, `submit_async.py`, `custody_read.py` of the export directory).
**`reports/custody_write.py` (IB-pr-351, b4073d3a57) is packaged by NO function** (absent from every `files[]` and `staged_from` row); its caller is
IRPT_CUSTDY's producer, which is outside this release pair.
The API route: `docs/contracts/investor-reporting/v1/routes.json` row `GET /api/scoped/investor-reporting/custody-report/{reportId}` (IB-pr-355, response_schema null per
60f7d8f4c8), applied from `infra/aws/terraform/investor-reporting/api/` (routes.tf reads that routes.json). It is NOT live today: `get-routes` on api `7k3ed8px20` lists 21 investor-reporting routes and no custody-report.
The print page (IB-pr-356/359, portal @63b9382a) is named here only; its DEV and PROD landings are Andrew's word and this packet moves nothing.

Note for the signer: other `staged_from` rows in this function sit at older pins than HEAD (e.g. ids.py, served.py, repository.py, composition.py); they are not changed by this release
and are out of this order's grant, so they ship as they are today.

## Order of acts (for the later release order, not this one)

1. Build and upload `irpt-export-render` at the pin; deploy the function (new `CodeSha256`). 2. Apply the `api` root (adds the one route). The route must not precede the function.
3. Print page to DEV, then PROD, on Andrew's word.

## Branch A (released)

- Opal principal (staff): can read ONE retained custody report by reference (`GET .../custody-report/{reportId}?revision=<revision>`) and receives it; the read goes through the submit's own
  authorization (`retained_export.resolve`), so scope is the same as for export.
- Firm principal: can read a custody report by reference only within their own firm and covered accounts; another firm's report, or an uncovered account, answers `OBJECT_NOT_COVERED`.
- Anyone else (no resolved scope): refused at the scoped-API auth boundary, unchanged.
- Export submit now accepts a CUSTODY_REPORT by resolved kind (reads its `as_of_date`) -- the submit path for custody reports.
- What does NOT widen: no new principal class, no new bucket or key prefix, no new function; one added route and three changed/added members in one existing function.

## Branch B (rolled back), per function

- `irpt-export-render`: redeploy the prior artifact -- S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-export-render.zip` version
  **`ZBwAzArTtDSpCIYL8CwhqqmIooS4mVPx`** (latest at read time, last modified 2026-10-07T14:10:49Z, 405052 bytes = the live CodeSize), the zip whose `CodeSha256` is
  **`aRCgH9B0pglos8cPiybPhmJShzjUts/Tr5R9R/AZYJw=`** (live today). A new upload creates a newer version, so the rollback is a redeploy of THAT version through the Terraform deploy path, never a console edit.
- `api` root: revert the routes.json row (or set it non-DECLARED) and apply the api root; this removes the one route. Do this first if the function is being rolled back, so no route points at a handler without the operation.
- Rolling back leaves the portal print page pointing at a route that answers 404; the print page's own landing is separate and is Andrew's word.
- `custody_write.py`: no function to roll back (not packaged).

## Writers of each changed property

- `irpt-export-render` code zip (`CodeSha256`): the deploy path from the source map row only (`build-and-upload.sh` + Terraform `module.irpt_export_render`); 1 writer.
- `entry.py` ROUTES / operations: the row staged at the pin (this release's re-pin commit); source authored under IB-pr-355 (~164).
- `submit_async.py`, `custody_read.py`: source-dir `files[]` at the pin; IB-pr-352 (~161), IB-pr-355 (~164).
- API route `GET .../custody-report/{reportId}`: `aws_apigatewayv2_route.irpt` in the `api` root, driven by the one contract file routes.json; 1 writer (api/routes.tf).
  (`infra/aws/terraform/investor-reporting/api/routes.json` is a stale second carrier that routes.tf does not read.)
- Customer-visible data: none written by this release; the route only reads retained CUSTODY_REPORT objects.

## The two after-reads (after release, by the later release order)

Both are `custody-report-read` operations (the routes.json `operation` of the new route).

1. **Other-firm read is REFUSED.** As a principal of firm X, `GET /api/scoped/investor-reporting/custody-report/{reportId of a report owned by firm Y}?revision=<rev>`
   returns `OBJECT_NOT_COVERED` and no body of firm Y's report. Pass = the refusal code and no report content.
2. **Opal read by ref returns it.** As an Opal principal, `GET /api/scoped/investor-reporting/custody-report/{reportId}?revision=<rev>` for one existing custody report
   returns that report (HTTP 200, the reportId and revision requested). Pass = the same report by ref, within scope.
   Also check after the deploy: the live `CodeSha256` equals the built zip's, and `release-census.py irpt-export-render --pin <pin>` prints `changed_members=0`.
