# DS Briefing — `timeseries_chart.json` two fixes (NMNC period-specificity + monthly grain)

**Recipient:** `0.4.0_DS_ClientPlatform~C`
**From:** `0.4.2_RD_AdvisorIntelligence`
**Pipeline:** Inflection partner / Advisor Intelligence
**Artifact:** `platinum/firm/timeseries_chart.json` (the NMNC/NMEC stacked bar source for Assets Overview)
**Surface:** Distribution tab → Assets Overview panel → AUA Clients bar chart
**Status:** Two distinct bugs in the same artifact. Both visible at /Books → Distribution view today.

---

## Bug 1: Whole first year (or first 4 quarters) shows as NMNC — should be NMEC

### What the chart shows today (Inflection, AUA · Clients sub-mode, Quarterly, Max window)

The first 4 quarterly bars (Q2 2020 → Q1 2021) are stacked as **100% NMNC** (Net Money from New Clients). Visually the first year is entirely "new client" colored — including the starting ~$58M AUM as of the observation start.

### Why this is wrong

NMNC = **Net Money from NEW Clients** — money from households that *became clients in that specific period*.
NMEC = **Net Money from EXISTING Clients** — money from households that were already clients before that period.

The firm's **starting AUM** at observation start is by definition existing (the firm didn't acquire all 700+ HHs in one quarter; those HHs existed before our observation window started). Classifying it as NMNC misrepresents the firm's growth story.

### Andrew's framing (verbatim, 2026-05-12)

> "if the first period there is 58m and the next period is 65, then 58m in Q3'20 should be blue to signify existing (when viewed on the quarterly interval!)"

### What "new client" actually means per period

Per period P:
- **NMNC(P)** = sum of net flows from HHs whose `first_seen_date` falls within period P
- **NMEC(P)** = sum of net flows from HHs whose `first_seen_date` is before period P, plus any opening AUM carried forward at period start

### Implementation recipe

Most likely current implementation: `is_new_client` is being computed as "doesn't appear in prior period's HH set" — which works for periods 2+ but classifies ALL HHs as new in period 1 because there is no prior period.

Fix: anchor "new client" to a **first-observation date** per HH (which exists in `household_dim` as `first_trade_date` or `account_open_date` or similar — confirm with the dim schema).

```python
# pseudocode
for period_end in period_grid:
    period_start = previous_period_end(period_end)  # or window start for period 1
    for hh in households_active_in(period_end):
        if hh.first_seen_date >= period_start and hh.first_seen_date < period_end:
            # HH became a client DURING this period — counts as NMNC
            nmnc += hh.aua_at_period_end - hh.aua_at_period_start  # likely just hh.aua_at_period_end since they started at 0
        else:
            # HH was already a client BEFORE this period — counts as NMEC
            nmec += hh.aua_at_period_end - hh.aua_at_period_start  # net flow delta
```

For **period 1 specifically**: HHs whose `first_seen_date` is **before period 1 start** contribute their full starting AUM to NMEC. Only HHs that started DURING period 1 (or whose first_seen_date falls in period 1) contribute to NMNC.

If `first_seen_date` is unknown for some HHs (data quality gap), default to NMEC (more conservative — assumes they're existing, doesn't inflate growth).

### Acceptance for bug 1

- [ ] Q2 2020 bar: NMEC bar dominates (~$58M), NMNC bar is small (only HHs whose first_seen_date is in Q2 2020)
- [ ] Q3 2020 bar: NMEC ≈ prior period's NMEC + most of the period delta. NMNC only includes new clients in Q3 2020
- [ ] **Sanity check**: sum of NMNC across ALL periods ≤ firm-current total AUM (because every dollar in firm AUA originated as NMNC in *some* period — but never more than once)
- [ ] Most-recent quarter (last bar) still patches with current donut values per existing logic (no regression of the "last-bar donut canonical" patch)
- [ ] If `first_seen_date` is unavailable, fallback to NMEC (with a `_meta.first_seen_fallback_pct` field in the artifact so we know how much classification is synthetic)

---

## Bug 2: No NMNC/NMEC breakdown at monthly grain — chart bars AND summary card both affected

### Two symptoms, one root cause

When Interval = Month on the Assets Overview AUA Clients view:

1. **Bar chart**: bars render as a single green segment (no NMNC/NMEC stacking) because `timeseries_chart.json` only has a `quarters: []` array — no `months: []` data. FE was patched (portal `7fbffcf7`) to fall through to single-segment `timeseries_overview.json` monthly data so the toggle has *some* visual effect. Cohort segmentation is lost.

2. **Summary card below the chart**: the **New Clients** and **Existing Clients** cells both show **$0** at monthly grain. Only Total AUA populates (e.g., May '26 = $203M / +$5.56M / +2.8% vs Apr '26). Same root cause — no NMNC/NMEC fields in the monthly fallthrough data means the summary-card reader has nothing to populate.

Andrew flagged the summary-card cells explicitly via screenshot (2026-05-12 ~16:13Z). Fixing the underlying data (this Bug 2) lights up BOTH the bars and the summary cells in one shot — no separate FE work needed.

### Required change

Extend `timeseries_chart.json` to include monthly data alongside quarterly:

```json
{
  "categories": ["nmnc", "nmec"],
  "quarters": [
    { "period": "Q2 2020", "end_date": "2020-06-30", "nmnc": ..., "nmec": ... },
    ...
  ],
  "months": [
    { "period": "May 2020", "end_date": "2020-05-31", "nmnc": ..., "nmec": ... },
    { "period": "Jun 2020", "end_date": "2020-06-30", "nmnc": ..., "nmec": ... },
    ...
  ]
}
```

Same `categories` + same per-period field names — just monthly grain. Apply the same period-specific NMNC logic from Bug 1.

### FE work needed after this lands

Small — the FE just needs to read `inflecTimeseriesChart.months` when `auaGranularity === 'monthly'` instead of falling through to single-segment. I'll patch that on FE side once DS confirms the field name (`months` vs `monthly` vs whatever).

### Acceptance for bug 2

- [ ] `timeseries_chart.json` has both `quarters` and `months` arrays
- [ ] `months.length` covers the same observation window as `quarters.length × 3`
- [ ] NMNC/NMEC per month follows the same period-specific logic from Bug 1
- [ ] Sum of any quarter's NMNC ≈ sum of its 3 constituent months' NMNC (within rounding — period-end snapshots can differ slightly but should be close)

### Optional alternative: separate file

If you prefer, ship a sibling `timeseries_chart_monthly.json` instead of extending the existing file. Either works for FE — just say which. Single-file is slightly preferable since the FE can do one fetch.

---

## 3. Coordination notes

**Bug 1 is the higher-priority fix** — the misrepresentation of starting AUM as NMNC is a substantive partner-facing inaccuracy. Bug 2 is feature-gap, can wait if bandwidth is tight.

**FE-side compensation:** the FE currently falls through to single-segment for monthly grain so the toggle "works" (does something visual), just without cohort segmentation. Once Bug 2 lands, I'll remove the fallthrough.

**Annual grain is correct already** (FE rolls last-Q-per-year client-side from your quarterly artifact) — no DS work needed at annual.

**No schema break for either bug** — Bug 1 just changes which HHs get classified into which bucket. Bug 2 adds a new field (`months`) alongside the existing (`quarters`).

---

## 4. Open question for DS

**HH `first_seen_date` field** — which column in `household_dim` (or equivalent silver source) carries the canonical "this HH became a client on date X" value? Common names: `first_trade_date`, `account_open_date`, `relationship_start_date`. Whichever it is, that's the join key for the Bug 1 fix.

If multiple candidates exist and they disagree (e.g., earliest `account_open_date` per HH vs explicit `relationship_start_date`), use the earlier one (most conservative — minimizes false NMNC classifications).

---

*Drafted by 0.4.2_RD_AdvisorIntelligence · 2026-05-12*
*Related FE fixes already shipped: portal `7fbffcf7` (granularity-aware allSortedAuaPeriods with quarterly→annual rollup + monthly fallthrough).*
*Original NMNC/NMEC artifact contract: predates my involvement; suspect logic from an earlier `INF_D_00d` or `INF_D_04` builder.*
