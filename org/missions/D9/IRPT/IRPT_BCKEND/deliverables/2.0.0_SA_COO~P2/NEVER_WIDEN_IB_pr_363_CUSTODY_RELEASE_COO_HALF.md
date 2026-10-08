# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-363: the custody release pair (irpt-export-render + the custody-report-read route)

**Signer:** `2.0.0_SA_COO~P2` (dell2), the issuer | **Date:** 2026-10-08 ~13:xZ | **Order:** `IRPT_BCKEND.TO-IB-pr-363` (issued
@0fdb85697e, complete @d0548c5536) | **Applier:** named by the release order that follows; none is cut yet.
**Signed against:** packet `NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-363.md`, **blob 2af2b30af8b62f48062151c9c700c66665db4a9b**, at commit
d0548c5536 on branch `wk-IRPT_BCKEND-171`. Read by this seat at that commit.

## What this half signs: the blast radius

**Write set: ONE function's code and ONE API route.**
1. `irpt-export-render` code, built at **release pin 1e0cdaf90c**. The census at the pin, which the issuer re-ran, changes three members:
   `entry.py` (IB-pr-355), `submit_async.py` (IB-pr-352) and `custody_read.py`, which is new (IB-pr-355). It has no rider.
2. The api root's one added route `GET /api/scoped/investor-reporting/custody-report/{reportId}` (operation `custody-report-read`), read
   by `routes.tf` from `docs/contracts/investor-reporting/v1/routes.json`. It is applied after the function, never before.

Nothing else is written: no bucket, key prefix, IAM policy, grant, other function or portal file. The print page (portal 63b9382a) is not in
this pair; its DEV and PROD landings are Andrew's word.

**Writers of each changed property: N = 2, and 2 rules were read.**
1. The function's `CodeSha256` is written only by the source-map build plus Terraform `module.irpt_export_render`.
2. The route is written only by `aws_apigatewayv2_route.irpt` in the api root, from the one contract file. The second
   `api/routes.json` is not read (row W171-S1).

**The expected refusal is read from the producer's rule, at the pin:**
- `custody_read.custody_report_read` authorizes through `retained_export.resolve` and does not re-implement it.
- The repository raises `ReportDenied` for another firm or an uncovered account.
- `entry.py`'s reasons table maps `ReportDenied` to `OBJECT_NOT_COVERED`.
- A retained object of another kind is refused by name and never returned.

## Branch A, released

- **Opal principal:** reads ONE retained CUSTODY_REPORT by reference and revision, within its scope.
- **Firm principal:** reads its own firm's custody reports for covered accounts only. Another firm's report, or an uncovered account,
  gets `OBJECT_NOT_COVERED` and no body.
- **No resolved scope:** refused at the scoped-API auth boundary, unchanged.
- **Export submit:** accepts a CUSTODY_REPORT by its resolved kind (IB-pr-352).
- **What does not widen:** no new principal class, bucket, prefix or function. The read is the same authorization the export already uses.

## Branch B, rolled back

1. Remove the route first: revert the routes.json row and apply the api root.
2. Redeploy `irpt-export-render` from artifact version `ZBwAzArTtDSpCIYL8CwhqqmIooS4mVPx`, which carries live CodeSha256
   `aRCgH9B0pglos8cPiybPhmJShzjUts/Tr5R9R/AZYJw=`, through the Terraform path.

The result is today's state: no custody read route, and submit refusing custody kinds. Rollback moves toward refusal and opens no hole.

## Preconditions this half binds

The applier STOPS and writes nothing if any of these holds:
- **Halves:** both halves are not at HEAD naming this blob.
- **Pin:** the build is not at 1e0cdaf90c, or its census shows a member other than the three above.
- **Order:** the route would be applied before the function's new CodeSha256 is live.
- **Ledger:** no change-management ledger entry is open at the start.

## The two after-reads (both owed by the release order)

1. **Other firm:** a custody-report-read for another firm's report returns `OBJECT_NOT_COVERED` and no report content.
2. **Opal by ref:** an Opal custody-report-read of one existing custody report by ref returns that report and revision.

After the deploy, `release-census.py irpt-export-render --pin 1e0cdaf90c` reads `changed_members=0`.

**Verdict: GIVEN**, for exactly this write set at this pin and blob.

-- 2.0.0_SA_COO~P2
