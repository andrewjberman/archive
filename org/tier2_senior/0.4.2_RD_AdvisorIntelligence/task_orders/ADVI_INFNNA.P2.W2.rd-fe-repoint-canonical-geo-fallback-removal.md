<task_order>
<metadata>
  <to_id>ADVI_INFNNA.P2.W2</to_id>
  <project>ADVI_INFNNA</project>
  <title>RD-FE: repoint continuous-GEO + ADV->client drilldowns to the canonical leaves + REMOVE the weekly cumulative_chart fallback (W6.1 honest-null on missing leaf) — DS W1 canonical emit is LIVE</title>
  <assigned_to>0.4.2_RD_AdvisorIntelligence~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>DISPATCHED — DATA LEG READY: DS W1 (canonical GEO state+city + per-client + monthly drill series) DEPLOYED + served-verified to-the-cent (fc6974fcf/820561227; advisor_nna_canonical.json generated_at 18:01:09Z; geo YTD==firm $4,225,486.45, 65% undercount eliminated). RD~B FYI'd ready. RD~B is the INFNNA/_shared FE owner.</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH — Andrew-direct (3rd Inflection PRD). Closes the ~65% continuous-GEO NNA undercount. INFNNA = own track (2nd-ish promote, separate from INFOTD).</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFNNA_P2.md (sec.3.W2 + W6.1)</ref>
    <ref type="w1_artifact">platinum/{firm}/advisor_nna_canonical.json — DS W1: additive geo{18 states/92 cities} + per-advisor clients{297 leaves} + per-city/per-client MONTHLY series (generated_at 18:01:09Z)</ref>
    <ref type="fe_sites">DistributionTab.tsx:914-915, 1226-1232 (cumulative_chart.nna_geo/nna_adv fallback); :1325-1332 (drilled-view computeLegacyBarData -> swap to canonical per-city/per-client series, per RD~B FYI 180109Z)</ref>
    <ref type="w6_scope">CTO e5b28ee4f — W6 no-silent-loss (AC7)</ref>
  </references>
</metadata>

<scope>
DS W1 made the canonical GEO/client NNA spine LIVE (additive under advisor_nna_canonical.json; geo state+city + per-client + monthly drill series; W6 self-reconciliation all_pass=True, served-verified to-the-cent). W2 is the FE half: point the continuous-view drilldowns at it + remove the lossy weekly path.

## Changes
1. **Repoint** DistributionTab.tsx continuous GEO (state L1, city L2) + ADV->client drilldown onto the new canonical leaves: :914-915, :1226-1232, and the drilled-view path :1325-1332 (swap off computeLegacyBarData/cumulative_chart -> read the canonical per-city/per-client series DS emitted). Window-explicit (F5 vocab: QTD/YTD/MAX/1Y/3Y/q-strip) so no surface renders a window-mismatched number.
2. **REMOVE the cumulative_chart.nna_geo / nna_adv fallback entirely** (W3 = universal): no NNA surface — ADV-L1 INCLUDED — may resolve the weekly series on any path or canonical-fetch-miss. grep-confirm zero cumulative_chart.nna_* references remain on any NNA surface.
3. **W6.1 HONEST-NULL (Andrew-direct, CTO e5b28ee4f):** on a missing canonical leaf, render an EXPLICIT "not available at this grain" null/empty state — NEVER a silent fallback to a non-canonical producer. This is literally what replaces the removed weekly fallback; it generalizes AC4 into a standing policy.

## MANDATORY — cross-tenant + cross-view regression (CVO W4 bar)
After repoint: continuous GEO/city/client numbers == snapshot == canonical to-the-cent for the same (dim,leaf,window); global/49F views unchanged. (CVO's W4 RIGID gate fires on your served-artifact RAVC2 — it ran 632 PASS pre-build; build to it.)
</scope>

<acceptance>
- [ ] AC3 — continuous GEO + every drill path (geo->city, adv->client) read canonical; cumulative_chart.nna_geo/nna_adv NO LONGER referenced by ANY NNA surface (grep-confirmed); continuous GEO/city/client == snapshot == canonical same-window. tsc -b + eslint green.
- [ ] AC4/AC7 (W6.1 honest-null) — NO code path on ANY NNA surface (ADV-L1 incl) can render the weekly series; a forced canonical-fetch-miss shows an explicit "not available at this grain" state, NOT a silent wrong number.
- [ ] CLOSURE: CVO W4 RIGID cross-view+partition-completeness gate (fires on this RAVC2) + Andrew/CTO visual smoke of the rendered continuous GEO/city/client drilldowns (headless fabric-down). 49F/demo/internal regression-guarded.

Lands on portal DEV. RAVC2 diff + AC3/AC4/AC7 to ws CTO + COO + CVO.
</acceptance>

<notes>
Authored by COO from ADVI_INFNNA_P2.md §3.W2 + W3 + the W6.1 scope-add (CTO e5b28ee4f, Andrew-direct). DS W1+W6 already served-verified (the 65% undercount is fixed in the DATA; this is the FE consume + the standing no-silent-loss guard). W6.2 (DS emit-stamp DONE in W1 + an AE daily-checker Lambda) is separate (AE TO incoming). RD~B owns this (the _shared DistributionTab surface + the F5/INFNNA history). Parallel to RD~C's INFPRM work + AE's INFPRM/INFNNA-checker. Drill-render-type (windowed vs monthly-series chart) — DS emitted windows-default + monthly as ready additive; pick the render per the canonical series shape.
</notes>
</task_order>
