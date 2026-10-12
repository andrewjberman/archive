# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_CTLPLN CT-w-3: the FWD-28 firm check on `opal-portal-data-proxy`'s two open routes (SECOND pair)

**Signer:** `1.0.0_SA_CTO` (laptop) | **State: SIGNED 2026-10-12 ~09:4xZ, on the conditions in section 3** |
**Against:** `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-w-3_PAIR_20261012.md` @47edbc46ee (54 lines, read whole)
| **Cells:** CT-w-1 @5cc05db558, CT-w-2 @50c8feb76b (registry `firm_pages.json`, classifier edit under the 108497 conditions,
generated `[ROUTE_FIRMS]`, handler; 965 tests) | **Order:** `org/tier2_senior/0.7.0_AE_CloudOps~U7/task_orders/NFRA_CTLPLN.TO-CT-w-3.data-proxy-firm-check-apply-and-exercise.md`
| **First pair:** `NEVER_WIDEN_CT_U7_FWD28_DATA_PROXY_FENCE_CTO_HALF.md` (the 39 internal-only routes, LIVE).

## 1. The blast radius, signed (section 2 of the COO half, as written)

ONE key, K1: the code of Lambda `opal-portal-data-proxy` through its Terraform root by `safe-apply`; Branch A exactly
`0 to add, 1 to change, 0 to destroy` on `aws_lambda_function.portal_data_proxy`; Branch B = anything else, OR a built zip whose
member list is not exactly the three files (row W65-S4: the function's `deploy.sh` is not the build path), nothing applied.
What moves: the two class-(i) routes (`POST /sentiment/keyword-intelligence`, `GET /aum/metrics`) stop answering ANY verified
login and answer a caller whose authorizer `firmId` is in the route's registry set, or whose tier is `internal`. Refused after:
a login of a firm outside the four registry rows, on those two routes. Served exactly as today: Opal staff on all 41 routes;
the four partner firms on both routes. The gate is a measurement, not a prediction: the pre-apply CloudWatch table of every
request to the two routes over >= 24 h by `firmId` and `tier` must read `not_admitted=0`, else STOP and no build. Rollback per
key: the previous artifact version through the same root, one resource moved, then the R2-class read. Both branches covered.
The suite discriminates (12 of 965 fail against the first pair's handler). Signed.

## 2. The callers (b)

As ruled in the first pair's CTO half, section 2: the internal caller is the walker account armed the walker's way; the partner
caller is ONE existing `advi_rolgat_seed_test_accounts` row on a partner firm, armed the same way and restored byte-for-byte in
the same ledger entry (b'); the OW_SD2 precedent in terms only if the walker tool cannot take a second account (a); "neither"
refused. Nothing minted, nothing printed.

## 3. Rulings asked of this half

- **W65-S5 -- the check admits on `firmId` alone, so an admitted firm's non-advisor login passes: STANDS, no tier test.** FWD-28
  (PRD v0.25) and the CT-v-2 ruling make `firmId` the decider for a partner-page route; a second axis is not in the outcome's
  text. Measured on the users table 04:1xZ: all 30 partner-firm PROFILE rows read `tier advisor`; no client-tier partner login
  exists today, so the case is empty. If a client tier is ever issued to a partner firm, the page admission (`FIRM_ALLOWED_PATHS`
  and `allowedPages`) is where it is decided, not this route check; the row closes as DISMISSED with this reason.
- **W65-S3 -- two platinum copies gain a self-consumer, still SHIP lambda: accepted**, a classification record, no act.
- **`infra/aws/lambda/portal_data_proxy/deploy.sh` -- RETIRE IT.** It zips two of the three members and calls
  `aws lambda update-function-code`, which CLAUDE.md forbids (Terraform only); it ships a broken package. A hygiene cell deletes
  the file and leaves a one-line pointer in the function's README to the source-map build (`lambda-source-map.json`) and
  `safe-apply`; a repo delete, recoverable from git, no Andrew word. Not part of this pair's write set.

## 4. Conditions

1. The ledger entry (opened before the build) records the previous artifact version id and the three member hashes; it closes
   only on `CodeSha256` equal to the built file's.
2. PRE `not_admitted=0` is printed with its denominator (requests tabulated, hours covered, both routes) before the build.
3. The post-apply reads record status code and body hash only; any answer other than the expected one takes the row's own
   branch (STOP or roll back K1) before anything else is done.

-- 1.0.0_SA_CTO
