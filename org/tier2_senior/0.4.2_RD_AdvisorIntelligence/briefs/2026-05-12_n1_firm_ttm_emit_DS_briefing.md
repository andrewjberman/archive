# DS Briefing — N1 firm-level emit for capital_gains_ttm + book_growth (Inflection)

**Recipient:** `0.4.0_DS_ClientPlatform~B`
**From:** `0.4.2_RD_AdvisorIntelligence`
**Pipeline:** Inflection partner / Advisor Intelligence
**Surface:** N1 firm dashboard — Cost Basis & Tax Status panel + Book Growth (TTM) strip
**Status:** L2/L3 already shipped (DS~B commit `2e5539bac`). N1 emit was explicitly flagged as follow-up.

---

## Summary

Extend the L2/L3 TTM-locked emit you just shipped to **N1 (firm-level)** in `INF_D_00.portal_aggregates.py`. The slim consumer in INF_D_04 (`build_clients_tab_slim`) already reads these fields at firm scope — they currently return defaults because INF_D_00 doesn't emit them.

Three fields to add to the firm `summary` block in `clients_tab.json`:

1. `summary.tax.capital_gains_ttm` — sum across **all** firm accounts (same TTM-delta-in-unrealized-gain semantics as L2)
2. `summary.tax.top_gain_positions` — top 20 firm-wide positions by current market_value, with TTM price change (same shape as L2/L3)
3. `summary.book_growth` — `{ttm_start_aua, ttm_end_aua, ttm_growth_abs, ttm_growth_pct, quarterly_series: [...5 anchors]}` rolled up across all firm accounts

## Implementation pattern

Mirror the L2 emit from `2e5539bac` exactly, just one scope level up. All inputs are the same:
- `gold/timeseries/account_performance.parquet` for `total_aua` and `unrealized_gain` daily series
- `gold/canonical/holdings_<latest>.parquet` + nearest-to-365d-prior holdings for TTM per-position price change
- No account-filter at N1 (sum across everything Inflection)

## Acceptance criteria

- [ ] `clients_tab.json#summary.tax.capital_gains_ttm` non-null, equals sum of L2 values across all 4 advisors (sanity check)
- [ ] `clients_tab.json#summary.top_gain_positions` length === 20 (or fewer if firm has <20 positions)
- [ ] `clients_tab.json#summary.book_growth.quarterly_series.length === 5`
- [ ] `book_growth.ttm_growth_abs = ttm_end_aua - ttm_start_aua` (sanity)
- [ ] Slim consumer at `INF_D_04:3332-3340` now picks up populated values

## Out of scope

- 49F equivalent (separate brief — Andrew deferred)
- `cost_basis_by_year` at any scope (separate brief — data gap)
- Schema changes to existing fields

## Open question

None — this is mechanically the same emit as L2, just at firm scope. If anything breaks, ping back.

---

*Drafted by 0.4.2_RD_AdvisorIntelligence · 2026-05-12*
*Companion to: `b28dd2419` (canonical tax-status), `2e5539bac` (L2/L3 TTM-locked).*
