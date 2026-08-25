<task_order>
<to_id>OPAL_TAXSMA_PT2.WS2</to_id>
<title>SILVER fact_taxsma_report — complete standardized parse of the 3 bronze reporting feeds (dedup + dtype ONLY), one row per (account, window), loud-KeyError guards</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-07-17</date>
<status>staged</status>
<priority>P2 (OPAL_TAXSMA_PT2, Andrew-direct via CTO). CUTTABLE NOW — WS-1's bronze shape is PUBLISHED (DT @TAXSMA_PT2_WS1_BRONZE_SHAPE). Build against the shape; the live silver RUN waits on live bronze (WS-1's Andrew-egress-gated pull).</priority>

<authority>
PRD §6 WS-2. Serve chain: bronze (WS-1, DT, dry-done @454dedf0e) -> SILVER fact_taxsma_report (this) ->
gold dim_taxsma_report (WS-3). PRD §4: silver = the COMPLETE standardized parse (the anonymization is
GOLD's job, WS-3 — NOT here).
</authority>

<gate>
BUILD is GO now (against DT's published bronze shape). The live silver RUN is gated on live bronze existing —
which is WS-1's Andrew-vendor-egress-gated pull. So: build + test the converter against the shape (synthetic
bronze) NOW; run it for real when WS-1's live bronze lands. COO signals when live bronze is in.
</gate>

<scope>
SILVER fact_taxsma_report: complete parse of the 3 bronze feeds (performancePeriod / costBasis / allocation
per DT's shape doc), DEDUP + DTYPE standardization ONLY (Rule 17 — NEVER slim fields, NEVER fillna/dropna/
business-row-filter; anything needing judgment about field relevance is GOLD/WS-3). One row per (account, window).
LOUD-KeyError guards on the field set (a missing expected field RAISES, never silently drops). `from __future__
import annotations` header; passes commit-gate. Lands at silver blackdiamond/49f/silver/fact_taxsma_report/.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io on the silver converter (READS = the 3 bronze feeds per DT's shape; WRITES = fact_taxsma_report -> WS-3 consumer)</run>
      <expect>READS/WRITES match DT's published bronze shape; no COLUMN GAPS; WS-3 (gold) is the downstream consumer.</expect>
      <if_mismatch>STOP. If the bronze shape doesn't map cleanly, re-ground with DT before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Build against synthetic bronze matching DT's shape; assert one-row-per-(account,window) + loud-KeyError on a deliberately-missing field</run>
      <expect>Converter produces the fact table from synthetic bronze; a missing expected field RAISES (not silently drops) — Rule 17 dedup+dtype only, no business filter.</expect>
      <if_mismatch>STOP. A silver that slims/filters is doing gold's job — fix before commit.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Upstream: WS-1 bronze (0.2.0_DT, shape @TAXSMA_PT2_WS1_BRONZE_SHAPE_20260717.md). Downstream: WS-3 gold
dim_taxsma_report (DS) — the anonymized parse-down; bridges via existing blackdiamond/49f/silver/dim_account_xref.
bd<->cot COMPLETE separation. No alarm leg. DS OWNS the full commit->QA-deploy cycle for this silver .py (Rule 13).
</cross_domain_coordination>

<acceptance_criteria>
1. Silver converter built against DT's bronze shape; comp-pipescript io clean (no COLUMN GAPS); one-row-per-(account,window).
2. Rule 17 respected: dedup+dtype only, NO field-slim/fillna/dropna/business-filter; loud-KeyError guards exercised.
3. Dry-tested on synthetic bronze; ready to run for real when WS-1 live bronze lands (COO signals).
4. Session log reproduces each mandate run + observed vs expect.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/OPAL_TAXSMA_PT2_PRD.md (§4, §6 WS-2)</ref>
  <ref type="bronze-shape">org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/TAXSMA_PT2_WS1_BRONZE_SHAPE_20260717.md</ref>
  <ref type="rule">CLAUDE.md Rule 17 (silver = dedup+dtype only) + Rule 15 (future annotations)</ref>
</references>
</task_order>
