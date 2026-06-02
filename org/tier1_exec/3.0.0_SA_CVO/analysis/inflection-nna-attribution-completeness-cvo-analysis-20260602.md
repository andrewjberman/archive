# CVO Analysis — Inflection NNA Attribution Completeness & Cross-Platform Canonical Consistency

**archetype:** DIAGNOSE
**Author:** 3.0.0_SA_CVO (ws CVO) — independent analysis, Andrew-direct 2026-06-02
**Scope:** Inflection Wealth Management ONLY (firm_id=`inflection`, bucket `opal-data-inf`)
**Purpose:** Front-matter analysis for CTO's 3rd TBD PRD (alongside INFPRM + INFOTD). This is **diagnosis + recommended scope**, not a PRD — CTO authors the PRD; this is the evidence base.
**Data vintage:** all artifacts read live from S3 today (`platinum/firm/*.json`, generated_at 2026-06-02T15:0x Z, data_as_of 2026-06-01/02).

---

## TL;DR

The headline + advisor-dimension NNA is **canonical-consistent across the whole platform** — the ADVI_INFMVP.F5 canonical spine (`advisor_nna_canonical.json`) holds. **The gap is narrow and specific: the CONTINUOUS-view GEO drilldown (State/City) and the CONTINUOUS-view ADV→client drilldown in Segment Analytics are NOT canonical-backed.** They fall back to the weekly-sampled `cumulative_chart.json` (`nna_geo` / `nna_adv`), which undercounts the same-window firm NNA by **~65% (YTD: $1.46M shown vs $4.23M canonical)**. The root cause is that **F5 canonicalized the ADV dimension + firm only — GEO was never folded into the canonical spine, and no per-city / per-client canonical drill leaves exist.** Snapshot view (both GEO and ADV) and the L0 headline DO reconcile to the canonical to the dollar.

---

## 1. The data architecture (where NNA comes from)

| Producer | Output artifact | What it covers |
|---|---|---|
| `INF_D_00f.advisor_nna_canonical.py` (**F5 SPINE**) | `advisor_nna_canonical.json` | per-**advisor** × window × fee-view + **firm** rollup. **NO geo. NO per-city. NO per-client.** Daily-summed from `gold/canonical/canonical_nna_{date}.parquet` (account×date). |
| `INF_D_00.portal_aggregates.py` | `header_metrics.json` | L0 firm headline NNA (nna_mtd/qtd/ytd/12m) — Asset Overview |
| `INF_09.generate_partner_analytics.py` | `partner_analytics_{quarterly,monthly,annual}.json` | Segment Analytics **SNAPSHOT** — geo/adv/nna per calendar period |
| `INF_D_00d.cumulative_chart.py` | `cumulative_chart.json` | Segment Analytics **CONTINUOUS** — `nna_geo`/`nna_adv` (weekly-sampled); the path F5 was written to bypass (docstring: "fixes the 60%-flow-loss bug in INF_D_00d's weekly-sampled cumulative path") |

**FE binding (DistributionTab.tsx:914-915, 1226-1232; AdvisorAnalytics.tsx:207/327/380):**
- Continuous NNA uses the **canonical** path, but **falls back to `cumulative_chart.nna_geo / nna_adv`** when *"drillParent is set (canonical source has no per-city/per-client data)"* OR *"timeseriesNna undefined."*
- Comment line 915 verbatim: canonical "Used by: ContinuousChartView (series.*) + SnapshotDistributionView **ADV-NNA donut**." GEO-NNA is named in neither → GEO renders the non-canonical producers in both views (snapshot=partner_analytics, continuous=cumulative_chart).
- AdvisorPublicProfile "Lifetime Activity" reads `canonicalNna.advisors[advisorId]` — canonical-backed.

---

## 2. Empirical reconciliation matrix (Inflection, today's data)

| Surface | NNA source | Reconciles to canonical firm? |
|---|---|---|
| Asset Overview L0 (header_metrics) | header_metrics.total.nna_* | ✅ YTD **$4,225,486.45** = canonical firm.YTD; 1Y **$17,708,942.30** = canonical firm.1Y |
| Segment Analytics **Snapshot** — GEO donut | partner_analytics geo | ✅ ties canonical firm.q **to the dollar** (q_cur $1,619,579 / q1 $2,605,907 / q2 $6,290,449 / q3 $7,621,714) |
| Segment Analytics **Snapshot** — ADV donut | canonical | ✅ same to-the-dollar tie |
| Segment Analytics **Continuous** — ADV (advisor L1) | canonical | ✅ sum(4 advisor entries) = firm (YTD $4.23M, MAX $135.83M) |
| AdvisorPublicProfile **Lifetime Activity** (per advisor) | canonical.advisors[id] | ✅ same source as Segment Analytics ADV → ties (e.g. peter_lee YTD $1,665,551.07) |
| **Segment Analytics Continuous — GEO (state L1)** | `cumulative_chart.nna_geo` | ❌ **YTD sum $1,456,681 vs canonical $4,225,486 = 34.5% (≈65% undercount)**; only 8 states vs snapshot's 14 |
| **Segment Analytics Continuous — GEO→city (L2)** | `cumulative_chart` geo_drill (fallback) | ❌ inherits the same non-canonical undercount |
| **Segment Analytics Continuous — ADV→client (L2)** | `cumulative_chart.nna_adv` (fallback) | ❌ canonical has no per-client leaf → falls back to weekly series |

**Methodology note (honest):** the MAX-window comparison (geo sum $10.15M vs canonical $135.83M = 7.5%) is **confounded by window mismatch** — `cumulative_chart` covers only 2024-06→2026-06 while canonical MAX is all-history (incl. the pre-2024 ~$129M Merge-In book migrations). The **fair within-window number is YTD: 34.5% coverage / ~65% loss**, both spanning the same 2026-YTD period. `nna_geo` and `nna_adv` produce **byte-identical totals** ($10,153,618.83) — confirming they are the same weekly-sampled producer; F5 fixed the canonical-backed ADV-L1 surface but the GEO + drill fallbacks were never repointed.

---

## 3. Root cause

**F5 (`advisor_nna_canonical.json`) was scoped to the ADV dimension + firm rollup only.** It fixed the cross-view divergence (snapshot-quarter vs continuous-cumulative window semantics) and the weekly flow-loss **for per-advisor and firm**. **GEO was never canonicalized**, and **no per-city / per-client canonical drill leaves were emitted**. The underlying `canonical_nna.parquet` is account×date and accounts carry state/city — so the data EXISTS to compute a canonical GEO rollup; it simply isn't emitted. As a result, the DistributionTab continuous fallback (to `cumulative_chart.nna_geo/nna_adv`) fires for (a) all GEO levels and (b) every drill-to-leaf, re-exposing the very weekly-sampling undercount F5 was built to eliminate.

---

## 4. Secondary findings (attribution-quality, not pure reconciliation)

1. **Unassigned-advisor bucket:** 36% of YTD firm NNA ($1,504,445 of $4,225,486) sits in the `inflection_wealth_management` advisor key — the house/untagged catch-all. The ADV partition is *complete* (sums to firm) but a third of recent NNA is un-attributed to a real advisor. (At MAX it's only 1.1% — the un-attribution is concentrated in recent flows.)
2. **Continuous GEO state coverage narrower than snapshot:** continuous carries 8 states (WA/MT/CA/IN/MN/ID/AZ/IL), snapshot carries 14+. The continuous producer drops states.
3. **Data-quality — malformed state key:** the snapshot geo donut contains a `'34'` key (a non-state code leaking into the geo dimension).

---

## 5. Recommended scope for the 3rd PRD (CVO recommendation — CTO authors)

Recommend the 3rd PRD be a **"Canonical GEO NNA spine + drill-leaf completeness"** project — the GEO analog of F5. Suggested ACs (CTO to shape):

- **For DS:** emit canonical GEO NNA (state L1 + city L2) from `canonical_nna.parquet` over the **same unified window vocabulary** as F5 (QTD/YTD/MAX/1Y/3Y/q-strip), and emit per-client canonical leaves for ADV→client — so every continuous drilldown reads the canonical, not `cumulative_chart`. Either fold into `advisor_nna_canonical.json` (rename → `nna_canonical.json` with geo+adv+ofc dimensions) or a sibling `geo_nna_canonical.json`.
- **For DE/RD (FE):** repoint DistributionTab continuous GEO + all drill paths off the `cumulative_chart.nna_geo/nna_adv` fallback onto the canonical; retire the fallback once canonical drill leaves ship.
- **For CVO (acceptance gate):** a **CVO-RIGID cross-view + partition-completeness gate** (the same bar F5 set for ADV): for every (dimension ∈ {geo, adv, ofc}, window), `sum(drill leaves) == firm canonical` AND `continuous == snapshot == canonical` to-the-cent. This is an acceptance bar, not advisory.
- **Attribution-quality (optional, Andrew call):** decide whether the 36% unassigned-advisor YTD bucket is addressed (advisor-tagging backfill) or honestly surfaced in the UI; fix the `'34'` malformed-state leak.

**Window-semantics caveat for the PRD:** the F5 lesson applies — make the canonical window vocabulary explicit for GEO too, so no GEO surface can render a window-mismatched number (the original "different in every panel" failure mode).

---

## 6. What I did NOT verify (honest limits)

- **Rendered-pixel confirmation:** headless-Chrome FE smoke is fabric-down — I verified the data layer + code bindings, not the rendered Segment Analytics panel. The continuous-GEO-undercount claim is a *data + code-binding* finding; the on-screen number falls to Andrew/visual smoke.
- **Exact flow-loss mechanism:** whether the `nna_geo` undercount is weekly-snapshot-differencing loss vs a definitional difference (fee-view, transaction-class) is a DS investigation for the PRD — I established the *magnitude and the architectural cause* (no canonical geo), not the line-level mechanism.
- **49 Financial:** out of scope per Andrew (Inflection-specific). The same architecture exists for `opal-data-bd`; the gap likely generalizes but is unverified here.

## Unknown-unknown (the question not asked)
Is the `cumulative_chart.nna_geo/nna_adv` fallback path reachable on the **ADV-L1** continuous view under any condition (e.g., a canonical fetch failure / pre-emit state, per DistributionTab:1232 "timeseriesNna undefined")? If so, even the canonical-backed ADV-L1 surface can silently degrade to the undercounted series on a fetch miss — meaning the fix isn't only "add geo canonical" but "**remove the weekly fallback entirely**" so no surface can ever render the 65%-lossy number. Recommend the PRD treat fallback-removal as a first-class AC, not just canonical-extension.

— 3.0.0_SA_CVO
