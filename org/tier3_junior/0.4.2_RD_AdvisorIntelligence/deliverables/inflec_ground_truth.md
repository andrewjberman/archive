# Inflection Portal Ground Truth
**Last verified:** 2026-05-11 by 0.4.2_RD_AdvisorIntelligence  
**Verify session:** INFNNA.PORTAL-VERIFY (post Merge In/Out classification fix)  
**Data as of:** 2026-05-11 (leaderboard.json generated_at)

---

## Firm-Level Totals

| Metric | Value | Source |
|--------|-------|--------|
| Total AUA | $202,958,135 ($203.0M) | header_metrics.json total.aua |
| YTD NNA | $4,289,267 | header_metrics.json total.nna_ytd |
| QTD NNA (Q2 2026) | +$547,507 | header_metrics.json total.nna_qtd |
| 12M NNA | $15,865,621 | header_metrics.json total.nna_12m |
| MTD NNA | -$307,827 | header_metrics.json total.nna_mtd |
| Total clients | 307 | header_metrics.json total.client_count |
| Total accounts | 797 | header_metrics.json total.account_count |
| NMNC AUA (new client) | $19,978,198 | header_metrics.json total.new_client_aua |
| NMEC AUA (existing client) | $181,310,868 | header_metrics.json total.nmec_aua |

**Q2 NNA restored:** Was -$1,360,000 pre-fix; now +$547,507. Joe Brandenburg (rep_id=6) attribution gap resolved.

---

## Per-Advisor NNA MAX (post Merge In/Out classification fix — 2026-05-08)

| Advisor | Advisor ID | AUA | NNA QTD | NNA YTD | NNA MAX | Accounts | Clients |
|---------|-----------|-----|---------|---------|---------|----------|---------|
| Peter Lee | peter_lee | $165,407,330 | -$136,001 | $3,232,161 | $109,388,668 | 602 | 201 |
| Patrick Scanlan | patrick_scanlan | $20,866,855 | $263,645 | $458,332 | $13,906,898 | 151 | 73 |
| Joe Brandenburg | joe_brandenburg | $16,430,886 | $196,725 | $224,581 | $11,729,310 | 67 | 21 |
| Inflection Wealth Mgmt (IWM) | inflection_wealth_management | $253,065 | $223,138 | $247,705 | -$483,000 | 404 (firm-wide) | 207 (firm-wide) |

**Firm total AUA (leaderboard QTD summary):** $202,958,135

---

## COO Expected Values vs Actuals (post Merge In/Out)

| Field | COO Expected | Actual | Diff | Status |
|-------|-------------|--------|------|--------|
| Firm AUA total | ~$199.6M | $202.96M | +1.68% | PASS |
| Firm MAX NNA | ~$136.1M | $136,084,320 | ~0% | PASS |
| Peter Lee MAX NNA | ~$107.7M | $109,388,668 | +1.6% | PASS |
| Patrick Scanlan MAX NNA | ~$13.9M | $13,906,898 | <0.1% | PASS |
| Joe Brandenburg MAX NNA | ~$11.69M | $11,729,310 | +0.3% | PASS |
| IWM MAX NNA | ~-$0.48M | -$483,000 | +0.6% | PASS |

---

## Geo States (cumulative_chart.json)

`['WA', 'MT', 'CA', 'IN', 'MN', 'ID', 'AZ', 'TX', 'Other']` — 8 real US states + catchall Other  
INF_D_00d fix (geo state mapping via household_dim.state_code) intact.

---

## Lifecycle AUA by Advisor (QTD window)

| Advisor | NMNC (new client) | NMEC (existing client) | Existing AUA |
|---------|------------------|-----------------------|--------------|
| Peter Lee | $16,826,424 | $10,746,169 | $136,172,636 |
| Patrick Scanlan | $966,892 | $571,612 | $19,321,382 |
| Joe Brandenburg | $1,931,817 | $1,482,498 | $13,016,571 |
| IWM (firm catchall) | $19,978,198 | $12,859,250 | $168,451,618 |

Note: IWM lifecycle_aua rows aggregate firm-wide (not just IWM accounts) — expected behavior per memory/project_inflection_iwm_catchall_bucket.md.

---

## Verification Chain

| Check | Result | Evidence |
|-------|--------|---------|
| 4 advisors visible (Books tab) | PASS | Playwright body text scan — all 4 advisor keys found |
| Joe Brandenburg NNA non-zero | PASS | QTD $196,725 / YTD $224,581 / MAX $11,729,310 |
| IWM AUA small (<$300K) | PASS | $253,065 AUA |
| Firm AUA ~$199.6M | PASS | $202,958,135 (1.68% above expected) |
| Joe drill-down (Books tab) | PASS | No error boundary after click |
| Geo states not regressed | PASS | 8 real states in cumulative_chart.json |
| No 5xx errors | PASS | 0 server errors captured |
| Q2 firm NNA positive | PASS | +$547,507 QTD (was -$1.36M pre-fix) |
