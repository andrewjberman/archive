# Cross-Panel Reconciliation Matrix

**Agent:** 0.4.0_DE_ClientPlatform
**Task:** ADVI_REBORN.W3-003
**Date:** 2026-04-07
**data_as_of:** 2026-04-02 (all sources)

---

## Metric: AUA (Total Firm)

| Display Location | Source Endpoint | S3 Key | Field Path | Value | Match? |
|------------------|----------------|--------|------------|-------|--------|
| Header Metrics (DistributionTab) | getHeaderMetrics | header_metrics.json | total.aua | $1,617,903,070 | BASELINE |
| Partner Analytics (main header) | getPartnerAnalytics | header_metrics_quarterly.json | views.nna.metrics.aua | $0 | FAIL -- zeros, rebuild needed |
| Books N1 headline | getClientsTab | clients_tab.json | headline.total_aua | $1,617,903,070 | PASS |
| Leaderboard sum (any window) | getArchitectLeaderboard | architect_leaderboard.json | sum(entries[].total_aua) | $1,617,903,070 | PASS |
| Leaderboard summary | getArchitectLeaderboard | architect_leaderboard.json | windows.YTD.summary.total_aua | $1,617,903,070 | PASS |
| by_architect top-10 sum | getHeaderMetrics | header_metrics.json | sum(by_architect[].aua) | $1,305,143,529 | N/A -- top-10 only (73% coverage) |

**AUA Verdict: 3/3 PASS, 1 FAIL (partner_analytics zeros)**

---

## Metric: NNA YTD

| Display Location | Source Endpoint | S3 Key | Field Path | Value | Match? |
|------------------|----------------|--------|------------|-------|--------|
| Header Metrics | getHeaderMetrics | header_metrics.json | total.nna_ytd | $75,076,198 | BASELINE |
| Partner Analytics | getPartnerAnalytics | header_metrics_quarterly.json | views.nna.metrics.nna_ytd | $0 | FAIL -- zeros |
| Leaderboard YTD summary | getArchitectLeaderboard | architect_leaderboard.json | windows.YTD.summary.total_nna | $42,083,105 | DISCREPANCY |
| Leaderboard 1Y summary | getArchitectLeaderboard | architect_leaderboard.json | windows.1Y.summary.total_nna | $75,692,959 | ~MATCH (1Y vs YTD, close to header nna_ytd) |

**NNA YTD Verdict: DISCREPANCY**
- header_metrics NNA YTD ($75M) does not match leaderboard YTD NNA ($42M)
- header_metrics NNA YTD ($75M) is closer to leaderboard 1Y NNA ($75.7M)
- Root cause: header_metrics.total.nna_ytd may actually be trailing-12M or the YTD window definitions differ between the two gold scripts

---

## Metric: Client Count

| Display Location | Source Endpoint | S3 Key | Field Path | Value | Match? |
|------------------|----------------|--------|------------|-------|--------|
| Header Metrics | getHeaderMetrics | header_metrics.json | total.client_count | 2,833 | BASELINE |
| Books N1 headline | getClientsTab | clients_tab.json | headline.total_clients | null | FAIL -- not populated |
| Books N1 client list length | getClientsTab | clients_tab.json | len(clients[]) | 2,833 | PASS (implicit) |
| Leaderboard sum | getArchitectLeaderboard | architect_leaderboard.json | sum(entries[].client_count) | 2,833 | PASS |

**Client Count Verdict: 2/2 PASS, 1 FAIL (clients_tab.headline.total_clients is null)**

---

## Metric: Account Count

| Display Location | Source Endpoint | S3 Key | Field Path | Value | Match? |
|------------------|----------------|--------|------------|-------|--------|
| Header Metrics | getHeaderMetrics | header_metrics.json | total.account_count | 6,024 | BASELINE |
| Books N1 headline | getClientsTab | clients_tab.json | headline.total_accounts | null | FAIL -- not populated |
| Leaderboard sum | getArchitectLeaderboard | architect_leaderboard.json | sum(entries[].account_count) | 6,024 | PASS |

**Account Count Verdict: 1/1 PASS, 1 FAIL (clients_tab.headline.total_accounts is null)**

---

## Issues Found

### CRITICAL: Partner Analytics zeros
- `partner_analytics/header_metrics_quarterly.json` has AUA=0, NNA_YTD=0 across all views (nna, geo, adv)
- Generated at 2026-04-07T21:49:20Z (fresh) but data is empty
- This means the PartnerAnalytics header donut and time machine are rendering with zero values
- **Action:** DS must investigate D_01.partner_analytics.py -- the quarterly aggregation is producing empty views

### HIGH: NNA YTD mismatch ($75M vs $42M)
- header_metrics.total.nna_ytd = $75,076,198
- architect_leaderboard.windows.YTD.summary.total_nna = $42,083,105
- Gap = $32,993,093 (44% discrepancy)
- Leaderboard 1Y NNA ($75.7M) is close to header NNA YTD ($75.1M), suggesting header may be using a different window definition
- **Action:** DS must verify both scripts use the same YTD start date (Jan 1, 2026)

### MEDIUM: clients_tab null fields
- headline.total_clients = null (but clients[] has 2,833 entries)
- headline.total_accounts = null
- headline.fee_rate = null
- clients[].total_aua = 0 for all entries (but headline.total_aua is correct)
- **Action:** DS must populate these fields in the publisher Lambda

### LOW: by_architect is top-10 only
- header_metrics.by_architect[] contains only 10 architects (sum AUA = $1.3B)
- Full leaderboard has 53 architects (sum AUA = $1.6B)
- This is by design (top-10 for the header) but means AUA won't sum to firm total

---

## Summary Matrix

| Metric | Header Metrics | Partner Analytics | Books N1 | Leaderboard | Fee Efficiency |
|--------|---------------|-------------------|----------|-------------|----------------|
| AUA | $1.618B | FAIL (0) | $1.618B PASS | $1.618B PASS | PENDING (no data yet) |
| NNA YTD | $75.1M | FAIL (0) | N/A | $42.1M DISCREPANCY | PENDING |
| Client Count | 2,833 | N/A | null FAIL | 2,833 PASS | N/A |
| Account Count | 6,024 | N/A | null FAIL | 6,024 PASS | N/A |

**Overall: 7 PASS, 4 FAIL, 1 DISCREPANCY, 4 PENDING**
