<task_order>
<to_id>OPAL_TAXSMA_PT2.WS1</to_id>
<title>BRONZE producer — 49F-scoped Cottonwood REST clone (portfolioreporting/api/*, reuse the live 49F .bd.identity session + token mint + 3 endpoints); Open Decision A CLOSED</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.2.0_DT_PortfolioAnalytics</issued_to>
<!-- Lane: CTO named 0.2.0_DT on WS-1 + WS-4 (authored the design/IAM seam + the endpoint finding + READY 210033Z).
     0.6.2_AE_PartnerETL = Cottonwood REST-pattern reference/consult (the pattern being cloned). Bronze data lands
     in the BD tree (bd<->cot separation stands). -->
<date>2026-07-17</date>
<status>pending</status>
<priority>P2 (Andrew-direct via CTO 205620Z; OPAL_TAXSMA_PT2 @a80840fb1). Head of the WS-1→2→3 chain. **HARD GATE: Andrew's vendor-egress per-use word (below) before the first LIVE reporting call.**</priority>

<authority>
Andrew-direct (0.2.0_DT's TAXSMA_PT2 briefs → CTO stood up the project @a80840fb1). PRD
docs/architecture/OPAL_TAXSMA_PT2_PRD.md. Serve settled (§4): gold dim_taxsma_report is the serve prefix
(anonymization = gold parse-down); WS-1 produces RAW bronze.
</authority>

<gate>
** HARD GATE — VENDOR EGRESS (NEVER-rule): the portfolioreporting/api/* reporting endpoints are a NEW egress
   surface vs today's datamining feeds (same vendor/property, DIFFERENT API). Per CLAUDE.md "NEVER call an
   external vendor API without Andrew's explicit per-use word — availability is NOT authorization." The first
   LIVE reporting call HOLDS for Andrew's explicit egress sanction / pipeline-remit word. Build the clone +
   mint + parser DRY (against the finding's documented shapes) with no live call; the live pull is the gated
   step. DT flagged this to CTO too. COO is surfacing the sanction to Andrew now. **
</gate>

<scope>
BRONZE producer: clone the cot REST-consume pattern, scoped 49F, + the GET /session/token mint + the 3
reporting endpoints (per DT's finding @638c91bea). Raw JSON per-endpoint prefixes. BRONZE IS RAW+UNTOUCHED
(Rule 17a) — byte-for-byte, no parse/dtype at ingest. Small pull, NO backfill, NO chunking (DT-grounded).
OPEN DECISION A = CLOSED (DT @638c91bea): the endpoints authenticate off our EXISTING 49F `.bd.identity`
session (token mint + POSTs), NOT a clientview variant — no new session to build, reuse the live one.
bd↔cot COMPLETE separation stands (never mirror/sync).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before the live call (post Andrew egress sanction)">
    <step>
      <run>Confirm DT's endpoint finding still holds: the .bd.identity session mints a token + the 3 endpoints return 200 — a single live exercise ONCE Andrew's egress word lands (Rule 22a: exercise, don't assume)</run>
      <expect>Token mint 200 + 3 endpoints 200 on the 49F session. This is the ONLY live call before Andrew's word — everything prior is DRY against the finding's shapes.</expect>
      <if_mismatch>STOP. If the session/endpoints changed since the finding, re-ground with DT before the pull.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>aws s3 ls the bronze prefix — raw JSON byte-for-byte, no parquet/coercion (Rule 17a)</run>
      <expect>Raw per-endpoint JSON present; no ingest-time parse.</expect>
      <if_mismatch>STOP. Fix before signaling WS-2.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
0.6.2_AE_PartnerETL = Cottonwood REST-pattern consult (the pattern being cloned). bd↔cot COMPLETE separation
(never mirror). Reuses: the live 49F .bd.identity session (don't rebuild). Feeds WS-2 (silver, DS) — signal DS
with the stable bronze shape so WS-2 cuts. No alarm leg (trigger/twin is WS-5, and the twin is barred by the
alert-suspension).
</cross_domain_coordination>

<acceptance_criteria>
1. **Andrew's vendor-egress per-use word obtained BEFORE the first live reporting call (NEVER-rule).**
2. Clone + mint + 3-endpoint parser built; bronze raw JSON landing byte-for-byte (Rule 17a), reusing the 49F session.
3. Bronze output shape documented so WS-2 (silver) can be cut against it.
4. Session log reproduces each mandate run + observed vs expect + the egress sanction citation.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/OPAL_TAXSMA_PT2_PRD.md (§4, §6 WS-1)</ref>
  <ref type="finding">org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/TAXSMA_PT2_BD_ENDPOINT_MECHANISM_FINDING_20260717.md @638c91bea</ref>
  <ref type="egress-rule">CLAUDE.md — vendor egress NEVER-rule; memory/feedback_availability_is_not_authorization_vendor_egress.md</ref>
</references>
</task_order>
