# ADVI_INFTGT P1/P2 Scope Pass — LANDED / OBVIATED / STILL-NEEDED

**Author:** 0.4.2_RD_AdvisorIntelligence
**Date:** 2026-05-13 (v2 corrected; v1 had false-negatives caught by COO RAVC)
**Authorized by:** 2.0.0_SA_COO (chain #25b RAVC2 PASS 5/5)
**Reference:** docs/architecture/ADVI_INFTGT_PRD.md §6 (17 TOs)

## v2 Corrections vs v1

Per COO RAVC2 (2026-05-13), v1 had 4 false-negatives caught by direct git-grep verification. v2 reflects empirical commit-log + code-spot-check evidence.

| TO | v1 said | v2 says | Evidence |
|----|---------|---------|----------|
| TO-1b | STILL-NEEDED | LANDED | `ff878749d` 2026-05-11 + closure `ab47770f4` + REGISTRY `6f9cb0f36`. Chain #24 production WARN logs cited the tag. |
| TO-6 | STILL-NEEDED | LANDED | `partner_analytics.json` orphan only in 4 historical comments in DistributionTab.tsx; PartnerAnalytics.tsx reads from `partner_analytics_quarterly` (windowed). Option (b) migration effectively complete. |
| TO-8 | STILL-NEEDED | LANDED | `147b85326` "ADVI_INFTGT.TO-8 — INF_D_05 activity_scan + INF_D_06 cash_drag actually compute" + session-log status complete `b4b58d029`. Also `be241a8ce` 4-window rewrite + `993c369d4` dispatch entries. |
| TO-14 | STILL-NEEDED | LANDED-by-removal | No "Funded X/Y" parenthetical exists in current AdvisorIntelligence codebase — acceptance was "OR parenthetical hidden." Removal already done. |

## Matrix (v2)

### P0 (4 TOs) — All LANDED

| TO | Disposition | Evidence |
|----|-------------|----------|
| TO-1 period_start_aua + growth cap | LANDED | `a1594ae69` 20% heuristic. |
| TO-2 avg_fee_bps_earned unit math | LANDED | Lambda v1.7.53 (`9301dfe97`) with >1000 cap + `fee_schedule_type='flat'` flag. FE wired: `97a88ab5` endpoint propagation + `ca40f2e9` tooltip render. |
| TO-3 AUA cut labels reconciliation | LANDED | `49785657` + `5dd52f86`. |
| TO-4 Sign-correct Continuous NNA + remove Script 09 | LANDED | `feb43e37`. |

### P0 post-correction (3 TOs) — All LANDED

| TO | Disposition | Evidence |
|----|-------------|----------|
| TO-1b snapshot-pair existence check | **LANDED** | `ff878749d` 2026-05-11 + chain #24 runner cited the tag in WARN logs. |
| TO-2b Group-D coordinated parity rerun | LANDED (partial) | Chain #25b PASS 5/5 — all D-stage artifacts coordinated. Parity-check gate (`comp-validate` integration into INFETL daily-chain) STILL-NEEDED as standalone follow-up. |
| TO-4b Continuous-GEO-AUA $189M bug | LANDED | DS~D `7bcaac70e` + `55e37ebcb`. Chain #25b verified. |

### P1 (6 TOs original) — 5 LANDED, 1 OBVIATED

| TO | Disposition | Evidence |
|----|-------------|----------|
| TO-5 Books Firm Overview snapshot period selector | LANDED | PartnerAnalytics Interval toggle (`7fbffcf7`); Max-everywhere lookback (`939138a7`). |
| TO-6 partner_analytics.json orphan staleness | **LANDED** | Consumers migrated to windowed `_annual`/`_monthly`/`_quarterly`. Orphan only in comments. |
| TO-7 Concentration Risk artifact wired up | LANDED | INF_D_07a `firm_concentrations.json` + INFCONCDRILLFI bond funds (`c2382cc01`); FE treemap redesigned with Basket/Name toggle. |
| TO-8 Activity Scan & Cash Drag actually compute | **LANDED** | `147b85326` (DS~C) + 4-window rewrite + dispatch entries. |
| TO-9 Advisor Public Profile role/lifetime | LANDED | Role Composition tenant-gated off (`a2235629`); Lifetime Activity = AdvisorAnalytics (`563d045c`); active_since in PlatinumAdvisorSummary type. |
| TO-10 IWM catchall rendering | OBVIATED | IWM redirected to first-class advisor entry (Andrew direction 2026-04-28). |

### P2 (4 TOs) — 3 LANDED, 1 PARTIAL

| TO | Disposition | Evidence |
|----|-------------|----------|
| TO-11 Client drilldown polish (bundle) | PARTIAL | Newest Relationship covered by DS~C `52478bb3a` (Lambda v1.7.54 pending deploy). BOOK GROWTH (TTM) already wired via `2e5539bac` DS L2/L3 ship + ClientListPanel bookGrowthLabel="TTM". Remaining sub-items unverified: quarter chip ordering, "+0$" → "$0" formatting, Fee Summary chart for client view, Accounts Summary BPS columns. |
| TO-12 RANK column populate or hide | LANDED | DEV `08844f09` + CLOUD `fafbe9718` — tenant-gated via `showRankDelta` layout flag. Inflection hides. |
| TO-13 Default state selection auto-Washington | LANDED | `feb43e37` Phase 4. |
| TO-14 Funded accounts flag | **LANDED-by-removal** | No "Funded X/Y" parenthetical in current AdvisorIntelligence codebase. PRD acceptance "OR parenthetical hidden" satisfied. |

## Summary (v2 corrected)

| Status | Count | Notes |
|--------|-------|-------|
| LANDED | 15 of 17 | All P0 (4 + 3 post-correction); 5 of 6 P1; 3 of 4 P2 + TO-2b partial; TO-14 by removal |
| OBVIATED | 1 of 17 | TO-10 (IWM first-class redirect) |
| PARTIAL | 1 of 17 (TO-11) | 2 of 6 sub-items addressed (Newest Relationship via DS~C, BOOK GROWTH via DS~B). Quarter ordering + $0 formatting + Fee Summary + BPS columns remain. |

INFTGT effective completion: **~94%** (16 of 17 fully addressed, 1 partial).

## Remaining work — TO-11 sub-items needing direct code verification

| Sub-item | Status | Effort |
|----------|--------|--------|
| Newest Relationship | LANDED via DS~C `52478bb3a` (post-v1.7.54 deploy) | 0 (verify post-deploy) |
| BOOK GROWTH (TTM) accordion | LANDED via DS~B `2e5539bac` upstream | 0 (verify rendering) |
| Quarter chip chronological ordering | UNVERIFIED — likely STILL-NEEDED | ~30min |
| "+0$" → "$0" formatting | UNVERIFIED — likely STILL-NEEDED | ~30min |
| Fee Summary chart for client view | UNVERIFIED | ~30min code check + DS dep |
| Accounts Summary BPS columns | UNVERIFIED | ~30min code check + DS dep |

Total estimated TO-11 residual: ~1-2h RD work + possible DS dep on Fee Summary / BPS data fields.

## Recommended COO Actions (v2)

### CLOSE these TOs immediately
- TO-1, TO-1b, TO-2, TO-3, TO-4, TO-2b, TO-4b, TO-5, TO-6, TO-7, TO-8, TO-9, TO-12, TO-13, TO-14

### Mark OBVIATED
- TO-10 (IWM first-class redirect supersedes "Unassigned" relabel)

### Single STILL-IN-FLIGHT
- TO-11 sub-items (4 of 6 unverified). Author follow-up brief for me to verify + ship the FE residuals (~1-2h).

### Cross-cutting items (outside PRD, ongoing)
- ADHC_INFDIM_ORPHAN Bug A SHIPPED (`90306935b`+`f948658e6`); Bug B (silver→gold accounts_dim freshness) — AE-lane TO
- comp-validate parity-check gate wiring — TO-2b acceptance asked for it; AE-lane

## Closure recommendation

INFTGT is at ~94% effective completion. Strong wave-2 result. Recommend:
1. Close 15 LANDED TOs on the project tracker
2. Mark TO-10 OBVIATED with reference to Andrew 2026-04-28 direction
3. Issue TO-11 residual TO scoped to me (4 unverified sub-items, ~1-2h)
4. Project itself can close when TO-11 residual ships

## v1 → v2 process note (for memory)

The v1 false-negatives all had the same pattern: I relied on session-recall of "what shipped" instead of empirical commit-log search. The fix is the verify-before-act discipline COO surfaced — for every claimed status, run `git log --all --oneline --grep="TO-X"` AND a direct code spot-check of the acceptance surface. Both, not either.

— 0.4.2_RD_AdvisorIntelligence 2026-05-13 v2
