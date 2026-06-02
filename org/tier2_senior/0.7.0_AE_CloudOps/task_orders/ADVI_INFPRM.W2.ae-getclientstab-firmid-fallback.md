<task_order>
<metadata>
  <to_id>ADVI_INFPRM.W2</to_id>
  <project>ADVI_INFPRM</project>
  <title>AE: firmId-scope external-user data for the Lambda-served ?firmId=-no-fallback routes (getClientsTab / Firm Overview, Symptom 2) — JWT-firmId fallback in opal-partners-data; CONFIRM the P0 edge claims first</title>
  <assigned_to>0.7.0_AE_CloudOps</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>READY-TO-DISPATCH (Andrew-directed parallel velocity 2026-06-02). AE spawning for this (was Wed-gated on MDPF OPS1 AC4#2 — time-gated, runs independent). Runs PARALLEL to RD~B INFOTD + RD~C INFPRM-W1. CONFIRM-FIRST: the edge/Lambda claims below are subagent-traced by RD~B's P0 — AE confirms against live infra/aws before landing.</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH — Andrew-direct (Symptom 2 Firm Overview, the ONE true backend bug in INFPRM). INFPRM = 2nd PROD promotion.</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFPRM.md (sec.3.W2)</ref>
    <ref type="p0_finding">docs/briefs/advi-infprm-p0-firmoverride-resolution-sweep-finding-20260602.md (c35e3cd40) — Deliverable (b) needs-edge table + bifurcation</ref>
    <ref type="lambda">opal-partners-data lambda_function.py:1684-1688/1777-1781 (400 "Missing required query parameter: firmId", no JWT fallback); :1626 (user_firm_id already read from authorizer)</ref>
    <ref type="symptom2_chain">ClientsTab.tsx:195-199 getPlatinumFirmDashboard -> :898 getClientsTab leg -> advisor-intelligence.ts:414 throws 'firmOverride required' -> clients_tab=null -> Firm Overview gate :815 never renders</ref>
  </references>
</metadata>

<scope>
**Andrew-direct (screenshots), Symptom 2: Firm Overview panel ABSENT for external Peter but PRESENT for internal Andrew.** P0 isolated this as the ONE true backend/data bug in INFPRM (S1 + S3 are FE-only layout, handled in W1).

## CONFIRM-FIRST (P0 edge claims are subagent-traced — AE verifies against live infra/aws)
P0 (RD~B) determined firm resolution is BIFURCATED:
- **Static-S3 endpoints** (shared-advisor-router Lambda@Edge): firm from X-Firm-Id header injected from validated JWT (auth-validator-edge/index.mjs:388); ?firm= consulted ONLY for opal-capital internal (shared-advisor-router:184-198) → firmOverride=undefined HARMLESS → FE-fine.
- **Lambda-served endpoints** (opal-partners-data; /api/scoped/partners/books/* + /api/scoped/advisor-intelligence/{clients-tab,timeseries,...}): firm ONLY from ?firmId=; absent → HTTP 400 "Missing required query parameter: firmId", NO JWT fallback.
**AE FIRST STEP: confirm these two claims against live infra/aws** (the X-Firm-Id injection, the ?firm=-opal-capital-only branch, the 400-no-fallback). If they hold, proceed; if they differ, flag COO+CTO (re-scopes W2).

## The fix (P0-recommended: edge fallback, closes the class)
getClientsTab (Symptom 2): the Lambda route 400s when ?firmId= is absent for external users. **Add a JWT/authorizer-firmId fallback in opal-partners-data** — user_firm_id is ALREADY read at lambda_function.py:1626, so the routes can self-scope to the authorizer's firmId when ?firmId= is absent (mirrors the static-S3 X-Firm-Id path + closes the whole ?firmId=-no-fallback class, not just getClientsTab). This is preferred over FE-threading firmId per-call (one edge fix vs N FE call-sites). Apply to the getClientsTab route first (Symptom 2), then the sibling ?firmId=-required routes in the same Lambda (P0 Deliverable-b table: getPlatinumClientSummary, getMixViews, the advisor-drilldown PII route is Lambda-by-design — scope appropriately).

## Deploy (CLAUDE.md non-negotiables)
Terraform-only for infra (Rule 7); if the Lambda CODE changes, deploy via terraform apply through safe-apply (Rule 18 HALTGT) — NOT aws lambda update-function-code; update the source-map (Rule 4); tag after 0-diff (Rule 6). comp-iam if any new permission. If the fix is config/code in the existing Lambda, follow the Lambda deployment protocol.
</scope>

<acceptance>
- [ ] AC-W2-confirm — the P0 bifurcation claims (X-Firm-Id JWT injection on static-S3; opal-partners-data ?firmId=-no-fallback 400) CONFIRMED against live infra/aws (or discrepancy flagged to COO+CTO).
- [ ] AC2 — logged in as Peter: Firm Overview panel RENDERS (the getClientsTab leg resolves firm from the authorizer JWT firmId when ?firmId= absent); same as the internal/Andrew view. 49F/demo/internal data loads UNCHANGED (regression-guarded — the fallback only fires when ?firmId= absent, so explicit-firmId callers unaffected). Other ?firmId=-no-fallback routes in opal-partners-data closed (or scoped + documented).
- [ ] CLOSURE: CVO cross-tenant regression matrix (with W1) + Andrew/CTO visual smoke. RAVC2 to CTO + COO + CVO.

Coordinate with RD~C (W1) — W1's layout fix + W2's data fix together make Peter's full Books surface correct. INFPRM = 2nd PROD promotion.
</acceptance>

<notes>
Authored by COO from RD~B's P0 finding c35e3cd40 (Andrew-direct parallel-velocity). AE spawning for this in parallel; MDPF OPS1 AC4#2 (Wed) auto-accrues independent of AE liveness, and OPS1 D3 alarm is already live monitoring it. W2 (this, the backend data leg) runs PARALLEL to W1 (RD~C, FE layout) — independent surfaces. The edge fallback is the durable class-fix (RD~B recommendation); AE owns the build-vs-FE-thread call after confirming the trace. Regression matrix MANDATORY (CVO). CC RD~C + RD~B + CTO.
</notes>
</task_order>
