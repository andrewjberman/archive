<task_order>
<metadata>
  <to_id>ADVI_INFNNA.P2.P0</to_id>
  <project>ADVI_INFNNA</project>
  <title>DS: flow-loss mechanism investigation for the continuous-GEO NNA undercount (weekly-snapshot-differencing vs definitional) — gates W1 canonical-GEO emit correctness</title>
  <assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>DISPATCHED — DS PRIORITY-2 (behind ADVI_INFOTD.W2D, which is bundle-critical for the held S5 promote). INFNNA P2 is its own track, NOT in the S5 bundle. P0 is the fast investigation pass that gates W1 emit correctness.</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH — Andrew-direct (3rd Inflection PRD); DS-led + CVO-gated. Own track (not the held S5 bundle). P0 gates the W1 canonical-GEO emit spec.</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFNNA_P2.md (sec.3.P0 + sec.1 root cause)</ref>
    <ref type="cvo_evidence">org/tier1_exec/3.0.0_SA_CVO/analysis/inflection-nna-attribution-completeness-cvo-analysis-20260602.md (7668bae52)</ref>
    <ref type="f5_producer">INF_D_00f.advisor_nna_canonical.py (the F5 spine — ADV+firm only; W1 extension site)</ref>
    <ref type="weekly_path">INF_D_00d.cumulative_chart.py (the lossy weekly producer to retire)</ref>
    <ref type="canonical_source">canonical_nna.parquet (account x date, carries state/city — the canonical GEO source)</ref>
  </references>
</metadata>

<scope>
**Andrew-direct (NNA-views finding) -> CVO independent analysis 7668bae52.** This is the GEO/client analog of ADVI_INFMVP F5. F5 made headline + ADV-dimension NNA canonical (ties firm to-the-dollar YTD $4,225,486.45 across Asset Overview L0 / snapshot donuts / continuous ADV-L1 / Lifetime). THE NARROW GAP: Segment Analytics CONTINUOUS-view GEO drilldown (state L1 + city L2) + ADV->client drilldown (L2) are NOT canonical-backed — they fall back to weekly-sampled cumulative_chart.nna_geo/nna_adv, undercounting same-window firm NNA ~65% YTD ($1,456,681 shown vs $4,225,486 canonical = 34.5% coverage).

## P0 deliverable (THIS TO — the investigation pass that gates W1)
CVO established the MAGNITUDE (~65% YTD) + the ARCHITECTURAL cause (no canonical GEO emitted; DistributionTab.tsx:914-915/1226-1232 falls back to cumulative_chart for cohort=geo or any drillParent). P0 must establish the LINE-LEVEL MECHANISM:
- **Determine whether the cumulative_chart.nna_geo undercount is (a) weekly-snapshot-DIFFERENCING loss** (a stock-sampling artifact — the SAME class as the F5 ADV bug: summing weekly deltas loses intra-week round-trips/flows) **vs (b) a DEFINITIONAL difference** (fee-view / transaction-class scoping divergence between cumulative_chart and canonical_nna).
- This decision GATES W1: if (a) weekly-sampling, the canonical GEO emit (W1) is a STRAIGHT re-aggregation of canonical_nna.parquet by state/city (correct-by-construction). If (b) definitional, W1 needs a definitional reconciliation FIRST (else the canonical GEO emit would tie to firm but still mismatch the intended business semantic).
- Confirm the source: canonical_nna.parquet is account x date + accounts carry state/city (the data to compute canonical GEO EXISTS, just isn't emitted) — verify this empirically (the parquet has the state/city columns populated for Inflection accounts).

## AC-P0
Mechanism identified + documented (weekly-differencing vs definitional, with the line-level evidence); the canonical-GEO emit spec for W1 is correct-by-construction against the finding. Read-only investigation (parquet + producer-code archaeology + the cumulative_chart-vs-canonical same-window diff); NO emit/data change in P0 — flag before any write. RAVC2 the mechanism finding to ws CTO + COO + CVO. On receipt, COO + CTO co-author W1 (canonical GEO state+city + per-client leaves over F5 window vocab) correct-by-construction against your finding.
</scope>

<acceptance>
- [ ] AC-P0 — flow-loss mechanism documented (weekly-snapshot-differencing vs definitional, line-level evidence); canonical_nna.parquet state/city presence empirically confirmed; W1 emit-spec determination (straight re-aggregation vs definitional-reconcile-first). RAVC2 to CTO + COO + CVO (evidence-base author).
</acceptance>

<notes>
Decomposed by COO from ws CTO PRD d1fe6ed3e (Andrew-direct, 3rd Inflection PRD; project ADVI_INFNNA reopened Phase 1->Phase 2). DS-LED, exactly like F5 (spine first, FE follows). Downstream (authored post-P0): W1 [DS] canonical GEO + per-client emit (gated on P0 mechanism); W2 [RD/DE] FE repoint + weekly-fallback REMOVAL (gated on W1); W3 [RD] ADV-L1 fetch-miss reachability (couples w/ W2 — fallback-removal universal); W4 [CVO] RIGID cross-view+partition equality gate (F5 bar extended to GEO+client); W5 [DS/RD] secondary attribution-quality (36% unassigned-house / '34' malformed-state / 8-vs-14 state coverage; Andrew-scoped). Your DS queue: ADVI_INFOTD.W2D (bundle-critical, FIRST) -> this P0. Mandatory served-verify discipline applies to W1's emit (not just partition). Window-explicitness is the F5 lesson — W1 emits over the SAME window vocab (QTD/YTD/MAX/1Y/3Y/q-strip) so no GEO surface renders a window-mismatched number.
</notes>
</task_order>
