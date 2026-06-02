<task_order>
<metadata>
  <to_id>ADVI_INFOTD.W2F</to_id>
  <project>ADVI_INFOTD</project>
  <title>RD-FE: consume per-firm account_count series in ModelPortfolios Trend Count (type + 1-line FE) — GATED on DS INFOTD.W2D served-verify</title>
  <assigned_to>0.4.2_RD_AdvisorIntelligence~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>QUEUED — GATED on DS INFOTD.W2D: do NOT start until DS confirms account_count is live in the SERVED json/mdpf/{firm}/aggregate-aua-timeseries.json (else Count still renders 0). Trivial once the field is present.</status>
  <dispatch_held>true</dispatch_held>
  <priority>HIGH — first-promotion-bundle; trivial effort, gated on the DS data leg.</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFOTD.md (sec.3.W2 changes 2+3)</ref>
    <ref type="type_site">portal/src/api/portal-proxy.ts:407-413 (MdpfPartnerSeries['by_model'])</ref>
    <ref type="fe_site">portal/src/pages/ModelPortfolios.tsx:476-479 (per-firm timeSeriesData useMemo); read at :1359-1361/:1497-1499</ref>
  </references>
</metadata>

<scope>
The FE half of W2 (per-firm Trend Count), trivial once DS's W2D lands the account_count field in the served artifact.
1. **TYPE:** add `account_count: Array<number | null>` to `MdpfPartnerSeries['by_model']` at portal-proxy.ts:407-413 (flows into MdpfPerFirmTimeSeries automatically).
2. **FE:** in the per-firm branch of the timeSeriesData useMemo (ModelPortfolios.tsx:476-479), add `account_count: modelData.account_count?.[i] ?? 0` to each per-model point. The Count read at :1360/:1498 (`trendMetricType === 'value' ? periodData.aum : (periodData.account_count || 0)`) then resolves naturally — NO change there.
- Model-only is preserved AUTOMATICALLY: the Non-Model band's show guard (:1435-1436/:1586-1587) already restricts that band to trendMetricType==='value', so per-firm Count never includes a non-model count.
</scope>

<acceptance>
- [ ] AC2 — firm-scoped user, ModelPortfolios -> Trend -> toggle Count: renders a per-model account-count time-series (model holdings only, no non-model band), in-pattern with global Count; reconciles to the per-day partition by_model[].account_count; global Count unchanged. tsc -b + eslint green.
- [ ] CLOSURE: visual smoke (Andrew/CTO) of the rendered Count chart; W2's data half is CVO/agent-verifiable (covered by W2D).

Lands on portal DEV; bundles into the same FIRST DEV->PROD promotion as W1 + S5 + NNA (you own the single promote on CTO GO). RAVC2 diff + AC2 to ws CTO + COO.
</acceptance>

<notes>
GATED on DS INFOTD.W2D served-verify (COO will release the hold + ping you when DS confirms account_count is live in the served artifact). Decomposed by COO from ws CTO PRD e5f750f7f. After W1 + this, the INFOTD first-bundle FE is complete -> smoke -> CTO GO -> single promote ships S5+NNA+INFOTD-W1+W2.
</notes>
</task_order>
