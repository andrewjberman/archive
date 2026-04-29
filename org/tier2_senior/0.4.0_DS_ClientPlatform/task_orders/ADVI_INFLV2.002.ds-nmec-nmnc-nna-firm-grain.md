# Task Order: ADVI_INFLV2.002 — DS: NMEC/NMNC/NNA from Orion Transactions (Firm Grain)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-002</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform + 0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-27</date>
    <status>complete</status><!-- cbc4f2713 INF_D_08.nmec_nmnc_nna.py; S3 MATCH; RAVC to COO + DS~B 20260429T152000Z -->
    <priority>HIGH — gates INFLV2.003 + downstream chain rerun</priority>
  </metadata>

  <objective>
    Andrew direction (2026-04-27): "we have enough [transaction fields] to properly do
    NMEC/NMNC AUA, we can do NNA too." Confirm and implement NMEC/NMNC AUA + NNA
    derivation at firm grain from Orion transactions.

    ADVI_INFGRD.002 commit (7ecc140a) already added `_compute_hh_lifecycle()` in D_04
    for radial_12m and aua_view. This TO extends that to populate all firm-grain
    lifecycle slots across the platinum artifact suite.
  </objective>

  <scope>
    <task id="1" label="Audit current lifecycle emission completeness">
      Review D_04.client_portal_summary.py post 7ecc140a:
        - Which platinum artifacts already receive NMEC/NMNC/existing segmentation?
        - What's missing: header_metrics radial, partner_analytics donut, timeseries NNA?
      Document gaps inline (comment or brief audit note as MCP message).
    </task>

    <task id="2" label="Extend lifecycle to all firm-grain artifacts">
      In D_04 (or relevant gold script), ensure:

      header_metrics.json:
        radial_12m.nmnc.aua, radial_12m.nmec.aua, radial_12m.existing.aua
        (populated via _compute_hh_lifecycle — already landed in 7ecc140a for radial_12m)

      partner_analytics_{quarterly,monthly,annual}.json:
        views.aua.donut.segments: [{label:'NMNC', value:X}, {label:'NMEC', value:Y}, {label:'Existing', value:Z}]
        (already landed in 7ecc140a for _build_aua_view — confirm populated post-chain)

      timeseries_overview.json:
        nna per period: confirmed computed from D_04 (post 7ecc140a); verify NNA sign convention
        (inflows positive, outflows negative — confirm against BD/49F pattern)

      leaderboard.json:
        3 entries (inflection_wealth_management, peter_lee, patrick_scanlan) with NMEC/NMNC
        per entry. For IWM firm entry: aggregate of 287 HH. For Peter/Patrick: per-rep data.
    </task>

    <task id="3" label="NNA derivation confirmation">
      Confirm NNA = sum of net transaction flows (buys - sells - withdrawals + deposits)
      per period matches BD/49F lifecycle definition.
      If Orion TRN transaction-type codes map differently from Schwab, document the
      mapping explicitly (transaction type → inflow / outflow / neutral).
    </task>

    <task id="4" label="Pre-commit gate + commit">
      Run .tools/ds-commit-gate.sh on any modified gold scripts.
      from __future__ import annotations must remain first import.
      git commit --only [modified scripts] --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>"
      Do NOT run chain rerun — that is INFLV2.009 (AE scope).
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      Pre-commit gate: .tools/ds-commit-gate.sh passes for all modified gold scripts.
    </criterion>
    <criterion id="2">
      header_metrics.json radial_12m emits non-zero nmnc + nmec + existing AUA
      (validated post-INFGRD.003 chain against $200M cohort).
    </criterion>
    <criterion id="3">
      partner_analytics donut emits 3 segments (NMNC/NMEC/Existing) with non-zero values.
    </criterion>
    <criterion id="4">
      timeseries_overview.json nna per period is non-zero where expected.
    </criterion>
    <criterion id="5">
      leaderboard.json emits exactly 3 entries:
        inflection_wealth_management, peter_lee, patrick_scanlan.
    </criterion>
    <criterion id="6">
      RAVC to 2.0.0_SA_COO + 0.6.1_AE_PartnerETL with commit hash.
      Subject: RAVC — ADVI_INFLV2.002 COMPLETE | NMEC/NMNC/NNA firm grain | [hash]
      This RAVC is the go-signal for INFLV2.003 + triggers AE to queue INFLV2.009.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Gate: ADVI_INFGRD.003 chain must be COMPLETE before starting this TO.
    Work against post-chain platinum data to validate emission.</constraint>
    <constraint>No emojis in code or print statements.</constraint>
    <constraint>from __future__ import annotations first import in all modified scripts.</constraint>
    <constraint>Do NOT run silver rebuild or chain rerun — DS delivers commit only.
    AE executes INFLV2.009 chain rerun after INFLV2.005.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.1_AE_PartnerETL"
                task="ADVI_INFGRD.003"
                status="in_progress"
                note="Chain must complete and platinum must be at ~$200M before
                this TO begins. AE RAVC on INFGRD.003 is the go-signal."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">D_04 (or relevant gold scripts) extended for complete
    firm-grain NMEC/NMNC/NNA lifecycle emission.</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO + 0.6.1_AE_PartnerETL.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §7 (data scope)</ref>
    <ref type="prior">7ecc140a — _compute_hh_lifecycle() already in D_04 for radial + aua_view</ref>
    <ref type="script">data/orion/scripts/gold/D_04.client_portal_summary.py</ref>
  </references>
</task_order>
```
