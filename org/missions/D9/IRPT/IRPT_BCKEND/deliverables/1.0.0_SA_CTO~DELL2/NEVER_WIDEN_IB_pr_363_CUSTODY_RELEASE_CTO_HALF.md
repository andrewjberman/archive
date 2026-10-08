# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-363: the custody release pair (irpt-export-render + the custody-report-read route)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~17:1xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 1313 (READ-acked)
**Signed against:** packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~171/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-363.md`,
**blob 2af2b30af8b62f48062151c9c700c66665db4a9b** (read at HEAD 4f5aea012e), and the COO half
`deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_363_CUSTODY_RELEASE_COO_HALF.md`. **Release pin: 1e0cdaf90c** (in HEAD).

## The blast radius this half signs

Same write set as the COO half, no wider: (1) `irpt-export-render` code built at pin 1e0cdaf90c; (2) the one api-root route
`GET /api/scoped/investor-reporting/custody-report/{reportId}` (operation `custody-report-read`), applied after the function.
No bucket, key prefix, IAM, grant, other function or portal file. The print page (IB-pr-356/359) is outside this pair.

## Measured by this seat (not taken from the packet)

| claim | instrument | read |
|---|---|---|
| census at the pin = 3 owned members, no rider | `python infra/aws/lambda/ci/release-census.py irpt-export-render --pin 1e0cdaf90c` | built 64 / live 63; changed entry.py, submit_async.py; added custody_read.py; `changed_members=3` |
| live code = the rollback target | `aws lambda get-function irpt-export-render` | CodeSha256 `aRCgH9B0pglos8cPiybPhmJShzjUts/Tr5R9R/AZYJw=`, CodeSize 405052 |
| rollback artifact exists | `s3api head-object ... --version-id ZBwAzArTtDSpCIYL8CwhqqmIooS4mVPx` | 405052 bytes, 2026-10-07T14:10:49Z (= live CodeSize) |
| route not live today | `apigatewayv2 get-routes --api-id 7k3ed8px20`, filter `custody` | `[]` |
| refusal read from the producer's rule, at the pin | `git show 1e0cdaf90c:` custody_read.py / entry.py | custody_read delegates to `_retained.resolve` and refuses any kind other than CUSTODY_REPORT; entry.py reasons map `ReportDenied -> OBJECT_NOT_COVERED` |
| route sits behind the existing authorizer | `git show 1e0cdaf90c:infra/aws/terraform/investor-reporting/api/routes.tf` | `authorization_type = "CUSTOM"`, `authorizer_id = local.portal_authorizer` |

Writers of the changed properties: N = 2 (function CodeSha256 by the source-map build + Terraform; route by `aws_apigatewayv2_route.irpt`
from the one contract file). Both rules were read.

## Both branches

- **A, released:** Opal principal reads one retained custody report by ref within scope; a firm principal reads only its own firm's
  covered accounts, otherwise `OBJECT_NOT_COVERED` and no body; unresolved scope is refused at the authorizer, unchanged.
- **B, rolled back:** remove the route first, then redeploy artifact version `ZBwAzArTtDSpCIYL8CwhqqmIooS4mVPx` through the Terraform
  path. Rollback returns today's measured state and moves toward refusal.

## Preconditions

The COO half's four STOP conditions bind unchanged (both halves at HEAD naming this blob; build at the pin with census = the three
members; route never before the function's new CodeSha256 is live; ledger entry open at start). One added: **the applier re-reads live
CodeSha256 at start; if it is not `aRCgH9B0...` the rollback target above is stale and the applier STOPS.**

Both after-reads are owed by the release order: other-firm read refused with `OBJECT_NOT_COVERED`; Opal read by ref returns that report
and revision; post-deploy census `changed_members=0`.

**Verdict: GIVEN**, for exactly this write set at this pin and blob.

-- 1.0.0_SA_CTO~DELL2
