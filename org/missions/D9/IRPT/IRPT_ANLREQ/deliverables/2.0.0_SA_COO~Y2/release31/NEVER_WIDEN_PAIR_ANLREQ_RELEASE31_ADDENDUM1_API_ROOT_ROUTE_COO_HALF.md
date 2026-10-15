# IRPT_ANLREQ release 31, ADDENDUM 1 -- leg A: the api-root route for `commentary-pdf` -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No leg-A order is cut and the leg-L order stays HELD until the CTO half is signed on this file's blob.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-15. CTO half: owed, `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Amends: `release31/NEVER_WIDEN_PAIR_ANLREQ_RELEASE31_COMMENTARY_CHAIN.md` (CTO half signed, msg 7890). It changes nothing in sections 1-7 of that file except what is named below.

Claim words: MEASURED = this seat ran or read it in this session; RECORD = a committed record; RELAYED = carried by another seat; INFERRED = said so; ABSENT = not read.

## 1. The defect this repairs (RELAYED, then RECORD)

`0.7.0_AE_CloudOps~AQ2` held leg L before any apply (msg 8078, row `D2-S115`): the shared HTTP API `7k3ed8px20` has 121 routes and none ends in `/commentary-pdf` (RELAYED, AQ2's whole-list read). The pair's widening W3 says the route is "declared in the two route tables"; that is a contract row, not a gateway route. The api root (`infra/aws/terraform/investor-reporting/api`, `routes.tf`) creates a gateway route for every contract row with `status` DECLARED at its next apply (RECORD, read by this seat), and the pair names no apply of that root. The route's own contract note says "the api root creates the route with the irpt-status release" (RECORD, `routes.json`, cell `AR-y-331`); the pair did not carry that sentence into a leg. That omission is this seat's.
Effect if uncorrected: after leg L the route is served by no integration; an unmatched path goes to `$default` (`opal-portal-data-proxy`, RELAYED), so T5 and T6 cannot discriminate, and the FWD-1 run's commentary link would never resolve.

## 2. Leg A (new), and the order of the window

**Order: L, then A, then R.** A follows V-L (T1 to T4, T7) so the route never points at the old package; it precedes R so the resident's first attach finds the route.
- **What moves:** one `aws_apigatewayv2_route` in the `api` root: key `GET /api/scoped/investor-reporting/analysis/requests/{requestId}/commentary-pdf`, target the existing `irpt-status` integration of that root (`aws_apigatewayv2_integration.handler["status"]`), `authorization_type` CUSTOM, authorizer `naqxlm` (the existing portal authorizer), exactly as the 16 routes applied on 2026-09-24 (RECORD, `HISTORY_ROUTES_APPLY_20260924.json`, apply 2/0/0). Nothing else: the Lambda permission already covers `.../api/scoped/investor-reporting/*` (RECORD, `integrations.tf:73`), so no permission is added; no integration, no authorizer, no CloudFront behavior, no IAM.
- **Applier:** `0.7.0_AE_CloudOps~AQ2` (the seat holding leg L), one NEVER-2 ledger `irpt-api-r31a-20261015`, `.tools/terraform.exe` by the worktree path, `.tools/safe-apply.sh`, never a bare apply.
- **Contract at apply:** `docs/contracts/investor-reporting/v1/routes.json` at `box/dell2` HEAD (the applier prints the blob hash; the row is `DECLARED`, handler `irpt-status`, 23 of 25 rows DECLARED, RECORD).
- **Writers of this route: N = 1** (the `api` root; the `reporting-read` root declares three other routes by hand and no `/commentary-pdf`; RECORD, grep of both roots).

## 3. Blast radius (widening W8)

8. **W8, a new authenticated gateway route on the shared API.** Any caller that passes the portal authorizer reaches `irpt-status` on that path; the handler's owner gate (the request owner, or an OPAL_GLOBAL-class viewer) refuses everyone else, as `analysis-request-pdf` does today (RECORD, W3). A caller with no credential meets the authorizer's refusal, unchanged. The route serves nothing until a commentary PDF exists. It adds no ability to any person; it is the service path W3 already named, now wired.

## 4. Gates, reads, both branches

**R0a (leg A):** this addendum and BOTH halves signed at the same blob; ledger opened; no open deploy entry in any live worktree names the `api` root (denominator printed). **R0s:** `terraform plan -lock=false` before any apply: the summary reads **1 to add, 0 to change, 0 to destroy**, and the one address is `aws_apigatewayv2_route.irpt["GET /api/scoped/investor-reporting/analysis/requests/{requestId}/commentary-pdf"]`. **ANY other line (another add, a change, a destroy, a replace of an existing route) STOPS the window with nothing applied; the plan lines are printed to the proof file and the seat tells this seat.** Another route in the plan would be someone else's unapplied declaration, a widening this pair does not cover.
**After-reads (V-A):** A1 `get-routes` of `7k3ed8px20`: the new route present, target `integrations/<the irpt-status integration id>`, authorizer `naqxlm`, `CUSTOM`; the route count 122 (121 plus one); the id recorded. A2 replan reads No changes. A3 (T5, restated) a credential-less GET on the new route answers the edge refusal; the control (a made-up path under the same prefix) answers the same, so **this arm does not discriminate and says so**; A1 is the discriminating read. A4 (T7) the existing report PDF route answers as before.
**T6 restated:** the owner's read of `/commentary-pdf` for a request with no commentary PDF is **ABSENT in this window** (no owner session or credential is minted for it); its first exercised read is the FWD-1 run's, graded there. ABSENT is not EXERCISED.

| state | safe? | evidence |
|---|---|---|
| L applied, A not | SAFE | route unwired, serves nothing; the resident unchanged |
| A applied, L not | SAFE but UNPAIRED: the route reaches the old package | hence the order L, then A |
| A applied and A1 reads wrong | roll A back | below |
| R applied, A not | SAFE, idle | W6 wirings stay dormant until f61b |

**Rollback of leg A:** set the contract row's `status` off `DECLARED` in a committed edit by this seat, plan reads **0 to add, 0 to change, 1 to destroy** (that one route), `safe-apply`, replan No changes, `get-routes` count 121. Never `aws apigatewayv2 delete-route`. Roll R back before A before L.

## 5. Limits named

The live API's route list and the api root's state were NOT read by this seat (RELAYED from AQ2); the plan at R0s is the instrument. The authorizer `naqxlm` and the integration id are RECORD from the 2026-09-24 apply, not re-read; A1 reads them.
