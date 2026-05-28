# /verify-channel — FIND_INSURE Phase 2A tiered rerun + Deliverable-6 v1.1 (bench-total + deeper baskets)

**Verifier:** 3.0.0_SA_CVO (independent S3 read of all 24 post-rerun). **Trigger:** my pagination finding → DS~C tiered rerun (e9a082185) + Deliverable-6 v1.1 (bedb6ca50). **Time:** 2026-05-28T~1733Z.

## VERDICT: PASS — bench-total captured + tiered baskets delivered. One minor CONCERN (allianz tier mis-key, ~1 credit).

### Bench-total (Andrew's free indicator) — CAPTURED, GREEN
`leadership_contacts_available` populated on 23/24 (annuity-solutions = None, correct — no company resolved). Captured at zero extra cost (page-0). Field lives in bronze `_meta.json` + the contacts-target v1.1 company-row (NOT gold `_company_scored` — minor; surface there too if the scoring layer wants it).
- Big annuity carriers: metlife 40,749 / nationwide 38,983 / eagle 37,510 / AIG 23,741 available (pulled 25 — tiny slice, but low-relevance).
- Genuine-WM targets: lincoln 684 / avantax 374 / futurity 356 / gradient 190 / preferred 118 / pacific 45 / retirement-network 8 (pulled 50 or all-available).
- INTERPRETATION NOTE: bench-total must be read WITH wm_classification — a huge bench at an annuity carrier (metlife 40k) is org-size, not AM-target quality. High bench + present-class = the strong signal.

### Tiered baskets — GREEN (1 exception)
present → deep (roster 50, or all-available where <50: pacific 45/45, retirement-network 8/8); adjacent → shallow 25. Correct except:
- **CONCERN: allianz-life [adjacent] roster=50, not 25.** Tier rule says adjacent→shallow. allianz has rollup_score=100 (high telemetry) — strongly suggests the tier criterion keyed on **rollup_score** (allianz=100→deep) instead of **wm_classification** (allianz=adjacent→shallow). Same rollup-vs-am_prominence axis confusion as the original subset-rule bug. Cost: ~1 extra credit (25 extra results) on a low-AM-relevance carrier. Fix: tier criterion should key on wm_classification (present=deep / adjacent=shallow), not rollup_score.

### Deliverable-6 v1.1 — re-emitted from fuller rosters
v1.1 metadata confirms: 24 companies, 114 rows, top-5/company, am_domain_relevance applied, drawn from the deeper (tiered) rosters. roster_size now reflects the tiered depth (present 50, adjacent 25).

## Routing
PASS → DS~C + COO. CONCERN (allianz tier mis-key) → DS~C: key the depth-tier on wm_classification not rollup_score (low-pri, ~1 credit, v1.x). Optional: surface `leadership_contacts_available` in gold `_company_scored` too (currently bronze _meta + serving only). The bench-total + deeper baskets fully address Andrew's pagination ask. CC CTO.
