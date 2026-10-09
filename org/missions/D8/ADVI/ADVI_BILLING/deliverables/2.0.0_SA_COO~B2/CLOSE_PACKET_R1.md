# ADVI_BILLING round 1 -- CLOSE PACKET (the issuer's served acts after the drain)

Author `2.0.0_SA_COO~B2`, 2026-10-09. All three orders are complete. Chain B merged @b4d9830f8c, chain A @2a97553845 (box/dell2).
This packet asks `1.0.0_SA_CTO~DELL2` for ONE half covering acts 1 and 2. Act 3 is the real run and moves nothing.

## Act 1 -- apply the read route (WORLD; new resources only)

- **What.** Build and upload the `advi-billing-read-lambda` artifact (`infra/aws/lambda/ci/build-and-upload.sh`, the source-map
  entry added in chain A). Then `safe-apply` root `infra/aws/terraform/advi/billing-read/` (state key `advi/billing-read/tfstate`).
- **Plan at the drain.** `Plan: 7 to add, 0 to change, 0 to destroy` (`deliverables/0.9.0_WK_ADVI_BILLING~1/AB_T2_PLAN.txt`):
  the API integration, route, IAM role, role policy, Lambda permission, log group, and the function `advi-49f-billing-read-lambda`.
  The apply is refused if a re-plan shows any change or destroy.
- **Blast radius.**
  - The function, role, policy, permission and log group are all new. The role holds `s3:GetObject` on
    `opal-data-49financial/advi/49financial/gold/advi_billing/*` and its own logs, nothing else.
  - The shared portal API (`local.portal_api_id`) gains ONE route,
    `GET /api/scoped/partners/books/relationship/{clientKey}/fee-quarter/{quarter}`, with CUSTOM authorization (the existing
    authorizer). No existing route is modified.
  - Because API Gateway picks the most specific route, only `.../fee-quarter/...` paths move to the new function. No handler
    serves those paths today: `opal-partners-data` has no `fee-quarter` action. That was read in its source, not probed; P3 is
    the measured control.
  - Writes: no S3 key, no existing function, no CloudFront behaviour.
- **Rollback.** `safe-apply` destroy of the same root removes exactly the 7 resources. The served gold object stays (it is read-only).
- **Ledger.** `org/critical_paths/change_management/advi-billing-read-apply-r1-20261009` is opened before the build and closed
  after these probes:
  - (P1) an in-scope fetch of `z08219260/fee-quarter/2026Q3` returns the object's bytes;
  - (P2) a viewer from another firm is refused;
  - (P3) the household's existing `platinum-summary` route answers byte-identical before and after (control).

## Act 2 -- the portal DEV candidate (LOCAL; a client-facing page, so DEV only)

- **Branch.** `wk-ADVI_BILLING-2-portal` at `de142768`, based on DEV `2d42e9b7`. Commits: `4bc11a42` (the panel, the endpoint,
  the fixture and the test), `5ea9ae81` (row-id comments), `de142768` (the issuer's one-line hookup into
  `AdvisorBookClientDetail.tsx`, below `perfrpCardsSlot`).
- **Touches a product file:** `AdvisorBookClientDetail.tsx` (+4 lines), plus 4 new files. `tsc -b` is clean; the panel's bun test
  passes 5 of 5.
- **Effect on other households.** Every household without a computed quarter shows "Fee detail is not available for this quarter."
  under its panels. Only `z08219260` has an object in round 1.
- **PROD:** not asked. It waits on Andrew's word (law edit d92d08c448).

## Act 3 -- the one real run (no write)

The running DEV page, signed in, opens household `z08219260`. The fee panel renders the served object, and a screenshot is
committed here for `3.0.0_SA_CVO`'s L9 grade of AB1-3-AC3.

## What the round measured (no client figures)

- The advisor component (BD schedule 100 bps, valuation 2026-07-01, 64/251) comes within 1% of the 07-07 TPFEE on both accounts,
  but not to the cent: DIFFERS. The leading named reason is the SMArtX prior-quarter true-up.
- The platform component (SMFEE 07-21) is DIFFERS by construction: Opal holds no per-account SMArtX platform or model rate.
- Rows ruled in-round: W1-S1 to S8 and D2-W2-S1 to S4 (`surprise-channel/investigations/INVESTIGATION_v1.md`).
- Carried to the enrichment list:
  - the advisor book scoping on this route and on platinum-summary alike (W1-S6);
  - an SMArtX statement or fee ingest (rates and true-up);
  - the rel_to_z crosswalk's absence from any durable plane.
