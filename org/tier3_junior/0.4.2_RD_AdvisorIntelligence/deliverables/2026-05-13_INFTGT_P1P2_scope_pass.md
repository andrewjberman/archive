# ADVI_INFTGT P1/P2 Scope Pass — LANDED / OBVIATED / STILL-NEEDED

**Author:** 0.4.2_RD_AdvisorIntelligence
**Date:** 2026-05-13
**Authorized by:** 2.0.0_SA_COO (chain #25b RAVC2 PASS 5/5)
**Reference:** docs/architecture/ADVI_INFTGT_PRD.md §6 (17 TOs)

## Matrix

### P0 (4 TOs) — All LANDED

| TO | Disposition | Evidence |
|----|-------------|----------|
| TO-1 period_start_aua + growth cap | LANDED | `a1594ae69` 20% heuristic shipped per PRD §7-4. TO-1b architectural follow-up (snapshot-pair existence) is STILL-NEEDED. |
| TO-2 avg_fee_bps_earned unit math | LANDED | INF_D_04 emits >1000 cap; Lambda v1.7.53 (`9301dfe97`) propagates cap + `fee_schedule_type='flat'` flag. FE renders "—" + tooltip "Flat fee schedule applies" (DEV `97a88ab5` + `ca40f2e9` + types). Andrew product call locked. |
| TO-3 AUA cut labels reconciliation | LANDED | Quarterly + data_as_of chips shipped 2026-05-11 (`49785657` + `5dd52f86`). All 4 panels labeled. |
| TO-4 Sign-correct Continuous NNA + remove Script 09 | LANDED | `feb43e37` 2026-05-11. Inflows ≥ 0, Outflows ≤ 0, no "Pending Script 09" string. |

### P0 post-correction (3 TOs) — 2 LANDED, 1 STILL-NEEDED-architectural

| TO | Disposition | Evidence |
|----|-------------|----------|
| TO-1b snapshot-pair existence check | STILL-NEEDED | DS~B architectural follow-up not surfaced in commit log. TO-1's 20% heuristic is partner-demo unblock; primary architectural fix still queued. |
| TO-2b Group-D coordinated parity rerun | LANDED (partial) | Chain #25b PASS 5/5 with all D-stage artifacts in single coordinated run. Parity-check gate (`comp-validate` integration) NOT yet integrated — recommend separate cleanup TO. |
| TO-4b Continuous-GEO-AUA $189M bug | LANDED | DS~D `7bcaac70e` + `55e37ebcb` fixed NNA donut value-semantic + city-drill builder. Brief I sent 2026-05-12 `abfc0ccb1`. Chain #25b verified Bug A + Bug B both ship. |

### P1 (6 TOs original) — 4 LANDED, 1 OBVIATED, 1 STILL-NEEDED

| TO | Disposition | Evidence |
|----|-------------|----------|
| TO-5 Books Firm Overview snapshot period selector | LANDED | PartnerAnalytics Interval toggle (Quarter / Month / Year) works for Inflection — `7fbffcf7`. Window selector (1Y / 3Y / Max) wired across all modes (Max-everywhere lookback fix `939138a7`). |
| TO-6 partner_analytics.json orphan staleness | STILL-NEEDED | Andrew chose option (b) migrate per §7-2. Migration of `PartnerAnalytics.tsx` consumers off the orphan onto `_annual`/`_monthly`/`_quarterly` not yet shipped. Effort ~2h. |
| TO-7 Concentration Risk artifact wired up | LANDED | INF_D_07a `firm_concentrations.json` shipped + INFCONCDRILLFI bond funds (`c2382cc01`); new Concentration Risk treemap UI redesigned with Basket/Name toggle + 5-bucket color scale shipped 2026-05-12 (~12 portal commits). |
| TO-8 Activity Scan & Cash Drag actually compute | STILL-NEEDED | Cash Drag URL pattern fix shipped (`eb083432`) but data fix for INF_D_05.activity_scan (zero-valued rows) not confirmed shipped. INF_D_06.cash_drag audit also needed. |
| TO-9 Advisor Public Profile role/lifetime | LANDED | Role Composition tenant-gated off for Inflection (`a2235629`). Lifetime Activity = new AdvisorAnalytics panel (`563d045c`). Active Since field exists in PlatinumAdvisorSummary type. |
| TO-10 IWM catchall rendering | OBVIATED | Original spec was relabel as "Unassigned". Andrew direction 2026-04-28 changed semantics: IWM is a first-class advisor entry with its own book.json drill route. Catchall accounts route there as expected. DS~C orphan fix `52478bb3a` post-v1.7.54 makes the client list clean. |

### P2 (4 TOs) — 1 LANDED, 3 STILL-NEEDED

| TO | Disposition | Evidence |
|----|-------------|----------|
| TO-11 Client drilldown polish (bundle) | PARTIAL | Newest Relationship covered by DS~C `52478bb3a` (Lambda v1.7.54 pending deploy) + types extension. Remaining: "+0$" → "$0" formatting, quarter chip ordering, BOOK GROWTH (TTM) accordion, Fee Summary chart for client view, Accounts Summary BPS columns. Treat as 5 sub-items, all STILL-NEEDED. |
| TO-12 RANK column populate or hide | STILL-NEEDED | AdvisorsTab.tsx RANK column still "—". 1h effort. |
| TO-13 Default state selection auto-Washington | LANDED | `feb43e37` Phase 4 — Snapshot Segment Analytics auto-selects largest state (Washington) on first render. |
| TO-14 Funded accounts flag | STILL-NEEDED | INF_D_02.advisor_client_detail funded flag computation not yet fixed. 1-2h DS effort. |

## Summary

| Status | Count | Notes |
|--------|-------|-------|
| LANDED | 11 of 17 | TO-1, TO-2, TO-3, TO-4, TO-2b, TO-4b, TO-5, TO-7, TO-9, TO-13, and post-v1.7.54 the Newest Relationship piece of TO-11 |
| OBVIATED | 1 of 17 | TO-10 (IWM first-class redirect supersedes "Unassigned" relabel) |
| STILL-NEEDED | 5 of 17 | TO-1b, TO-6, TO-8, TO-12, TO-14 |
| PARTIAL | 1 of 17 (TO-11) | 1 of 6 sub-items addressed; 5 sub-items still needed |

## Recommended COO Actions

### Issue fresh TOs for STILL-NEEDED items

| TO | Owner | Effort | Priority |
|----|-------|--------|----------|
| TO-1b architectural | DS~B | 2-4h | P1 (defense-in-depth; demo unblocked by TO-1 heuristic) |
| TO-6 PartnerAnalytics migration | DE 0.4 + DS coordination | 2h | P1 (last data_as_of staleness vector for partner build) |
| TO-8 Activity Scan / Cash Drag investigation | DS | 4-6h | P1 (visible empty-state placeholders) |
| TO-12 RANK column | RD 0.4.2 (me) | 1h | P2 |
| TO-14 Funded accounts flag | DS | 1-2h | P2 |
| TO-11 sub-bundle (5 sub-items) | RD 0.4.2 (me) + DS coordination | 3-4h | P2 |

### Open architectural items spawned outside the PRD

- **ADHC_INFDIM_ORPHAN** (DS~C diagnostic complete): Bug A INF_C_07 walk-back to healthy partition (~30min DS, SHIPPED `90306935b` + `f948658e6` per COO note); Bug B silver→gold accounts_dimension_latest freshness (AE-lane).
- **comp-validate parity-check gate** (from TO-2b acceptance): Cross-artifact firm-level total_aua agreement assertion. Integration into INFETL daily-chain steady-state.

## Closure recommendation

Andrew has 11 LANDED items ready to close on the project tracker. 1 OBVIATED, 5 + partial STILL-NEEDED ready for chain #26 / chain #27 cycles.

INFTGT project is ~71% complete (12 of 17 effectively addressed, 5 + partial outstanding).

— 0.4.2_RD_AdvisorIntelligence 2026-05-13
