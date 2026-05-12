# DS Briefing — Advisor Analytics: fee-status backfill, audit table, per-advisor growth_decomposition (Inflection)

**Recipient:** `0.4.0_DS_ClientPlatform~C` (DS lead for Inflection — coordinate with ~B/~D if helpful)
**From:** `0.4.2_RD_AdvisorIntelligence`
**Pipeline:** Inflection partner / Advisor Intelligence
**Surface:** AdvisorPublicProfile — **new** `AdvisorAnalytics` Lifetime Activity panel + existing Executive Summary card
**Status:** FE shipped today — `AdvisorAnalytics` mirrors firm-level Assets Overview structure (commits portal `563d045c`, CLOUD pointer forthcoming). Component is ready to consume what this brief produces.

---

## 1. Summary

Three coupled asks to make the advisor-level Lifetime Activity panel and Executive Summary card fully functional under fee-view slicing:

1. **Per-advisor `growth_decomposition` data** — for the GRO mode toggle on the new `AdvisorAnalytics` panel (mirrors the firm-level GRO mode).
2. **Fee-split canonical fields on advisor timeseries** — `*_fee_paying` / `*_no_fee` sub-streams for `total_aua`, `nna_canonical`, `inflows_canonical`, `outflows_canonical` (Inflection currently emits only aggregate; FE has the picker logic ready and falls back to aggregate with a degradation badge).
3. **Audit table + backfill for first-available-fee-information per HH/account** — when historical fee status is missing, flow the **current** fee status backwards over the relationship duration. Audit table records the first date we actually have fee status per HH so we know how far back the backfill is synthetic.

Andrew's framing (2026-05-12): *"Keep in mind everything we do has to be sliced by fee-paying, no fee, and aggregate as well. If we don't have a ton of historical fee data, then just backward flow current fees over the duration of the relationship. Need some kind of audit table however on file for first available fee information per household."*

Plus: *"Also need to make sure that we are reliably filling out the sub container for fees: Fee-Earning AUA / Non-Fee AUA / Avg Fee Rate."*

---

## 2. The three asks, decomposed

### ASK A — Per-advisor `growth_decomposition`

Firm has `growth_decomposition` in `platinum/firm/timeseries_overview.json` (quarterly / monthly / annually). Advisor scope doesn't.

**Required:** add a parallel block to `platinum/advisors/{advisor_key}/timeseries.json` (or a sibling artifact — your call):

```ts
growth_decomposition: {
  quarterly: GroPeriod[]
  monthly:   GroPeriod[]
  annually:  GroPeriod[]
}

interface GroPeriod {
  period:           string   // e.g. 'Q2 2025'
  label:            string
  end_date:         string   // YYYY-MM-DD
  period_aua_start: number
  period_aua_end:   number
  market:           number   // growth attributable to market movement
  nna:              number   // growth attributable to net new assets
  total_pct:        number   // total period growth as %
  // PLUS fee-view variants (see ASK B):
  market_fee_paying?:  number
  market_no_fee?:      number
  nna_fee_paying?:     number
  nna_no_fee?:         number
}
```

Same decomposition logic as firm-level: `AUA_end - AUA_start = market_growth + nna_flow`. Per-advisor scope filters to that advisor's accounts before the decomposition.

**Acceptance:** `AdvisorAnalytics` GRO mode renders bars for each period decomposed into market vs NNA — same visual as firm `PartnerAnalytics` GRO mode. Currently empty-states with "Growth Decomposition coming soon."

### ASK B — Fee-split sub-streams on advisor timeseries

The FE's `pickAua` / `pickNnaCanon` / `pickInflowsCanon` / `pickOutflowsCanon` already read these field names if present:

| Field | Expected when emitted |
|-------|----------------------|
| `total_aua_fee_paying`   | AUA across fee-paying accounts at snapshot date |
| `total_aua_no_fee`       | AUA across no-fee accounts at snapshot date |
| `nna_canonical_fee_paying`   | Cumulative NNA from fee-paying accounts only |
| `nna_canonical_no_fee`       | Cumulative NNA from no-fee accounts only |
| `inflows_canonical_fee_paying`  | Cumulative inflows from fee-paying accounts |
| `inflows_canonical_no_fee`      | Cumulative inflows from no-fee accounts |
| `outflows_canonical_fee_paying` | Cumulative outflows from fee-paying accounts |
| `outflows_canonical_no_fee`     | Cumulative outflows from no-fee accounts |

Each daily point on `platinum/advisors/{key}/timeseries.json` should carry these alongside the existing aggregate fields. The aggregate fields (`total_aua`, `nna_canonical`, etc.) stay as-is — sum of the two sub-streams.

The FE has a `hasFeeSplitSeries` detector that checks for presence; if absent, shows a "Fee-split data unavailable — showing aggregate" badge.

**Same fields needed on firm timeseries** if not already there — `PartnerAnalytics` will benefit from the same picker pattern once it gains a top-level Fee view toggle (separate FE follow-up).

### ASK C — Fee-status audit table + backfill

**Backfill rule (Andrew's directive):** When account-level historical data lacks fee status, **flow the current fee status backwards over the relationship duration.**

So if account `A` is currently fee_paying and we have fee info from 2024-06 onwards, treat all of A's pre-2024-06 history as fee_paying for aggregation purposes.

**Audit table (required):** new silver/gold table recording, per (account_id, household_id), the **first date we have actual fee-status information** for that account. Schema:

```ts
{
  account_id:                       number    // Orion Int64
  household_id:                     number
  advisor_key:                      string
  first_fee_status_date:            string    // YYYY-MM-DD, when fee status first observed
  first_observed_fee_status:        'fee_paying' | 'no_fee'
  relationship_start_date:          string    // YYYY-MM-DD, earliest account observation
  backfill_days:                    number    // days between relationship_start and first_fee_status_date
  current_fee_status:               'fee_paying' | 'no_fee'
  backfill_method:                  'observed' | 'flow_current_back' | 'no_relationship'
}
```

**Suggested landing:** `silver/api_dims/fee_status_audit/snapshot_date=YYYY-MM-DD/data.parquet` (daily cadence — fee status changes need to be observable).

**Use of the audit in downstream artifacts:**

- Every fee-sliced aggregation in `INF_D_*` scripts joins this audit table at start
- Aggregations include a `backfill_synthetic_days` rollup so we can report how much of a metric is synthetic vs observed
- Optionally include a `_meta.backfill_coverage` block in the consuming artifacts: `{fully_observed_pct, partially_synthetic_pct, fully_synthetic_pct}` so the FE can warn when a slice is mostly synthetic

---

## 3. ASK D (related, smaller) — Executive Summary fee sub-container fields

Currently the AdvisorPublicProfile Executive Summary card shows:
```
Fee          QTD
Fee-Earning AUA   —
Non-Fee AUA       —
Avg Fee Rate      102.5 bps
```

`Avg Fee Rate` is populated; `Fee-Earning AUA` and `Non-Fee AUA` are em-dashes — those fields aren't being emitted on the Inflection advisor drilldown summary, or they are but not at QTD/YTD/Max scope.

**Required on `platinum/advisors/{advisor_key}/summary.json` (or `drilldown_summary.json` — whichever the FE reads via `getPlatinumAdvisorDrilldownSummary`):**

```ts
fees: {
  qtd: { fee_earning_aua: number; non_fee_aua: number; avg_fee_rate_bps: number }
  ytd: { fee_earning_aua: number; non_fee_aua: number; avg_fee_rate_bps: number }
  max: { fee_earning_aua: number; non_fee_aua: number; avg_fee_rate_bps: number }
}
```

Computed by joining the fee-status audit table (ASK C) at each window's end date. For pre-fee-info periods, use the backfilled current status.

**Same shape at N1 / L2 / L3 / L4** if the panel renders there too.

---

## 4. Coordination notes

**Sequencing recommendation:**
1. **ASK C first** (audit table + backfill logic) — foundational; B and D both depend on it
2. **ASK B second** (fee-split sub-streams on timeseries) — adds the columns the FE picker already reads
3. **ASK D third** (Executive Summary fee fields) — quick aggregation off the audit + current advisor summary
4. **ASK A last** (growth_decomposition) — independent of B/C/D but lowest priority since the FE GRO mode empty-states cleanly today

**Cross-cutting:** every existing Inflection artifact that currently has aggregate metrics should grow a fee-sliced variant after C lands. Triage the priority order with Andrew — but at minimum the advisor timeseries (B) and Executive Summary (D) should ship in the same wave so the AdvisorPublicProfile feels coherent under fee-view toggling.

**Existing fee-split work at 49F (BD pipeline):** check whether the BD timeseries already carries `*_fee_paying` / `*_no_fee` fields. If yes, mirror the schema exactly for Inflection. If no, this is a parallel BD-side ask Andrew has already flagged ("same should be done with 49 but we'll get to that later").

---

## 5. Acceptance criteria

- [ ] **ASK A:** `platinum/advisors/{key}/timeseries.json` carries `growth_decomposition: {quarterly, monthly, annually}` with `{market, nna, total_pct}` per period. Sum of `market + nna` ≈ `period_aua_end - period_aua_start` (sanity).
- [ ] **ASK B:** Every daily point on `platinum/advisors/{key}/timeseries.json` has the 8 `*_fee_paying` / `*_no_fee` sub-stream fields (or null if no accounts in that bucket). `total_aua_fee_paying + total_aua_no_fee ≈ total_aua` per point.
- [ ] **ASK C:** `silver/api_dims/fee_status_audit/` produces daily. Spot-check three HHs: one fully observed, one with backfill, one no-relationship. `backfill_method` field matches the spot-check.
- [ ] **ASK D:** `platinum/advisors/{key}/summary.json` `fees` block has all three windows × three fields populated. Sum of fee_earning + non_fee at each window ≈ that window's total AUA.
- [ ] **Cross-artifact parity:** for a single advisor, sum of (window-final fee_earning_aua across all 4 advisors) ≈ firm-level fee_earning_aua at same window (within rounding).
- [ ] **FE smoke:** flipping fee view on Peter Lee's profile changes Total AUA / NNA / Inflows / Outflows numerically. AdvisorAnalytics bars reshape accordingly. Fee-Earning AUA / Non-Fee AUA cells in Executive Summary populate with real values (no em-dashes).

---

## 6. Out of scope

- 49F BD-pipeline fee-split work — parallel ask, separate brief if/when prioritized
- FE-side firm-level fee toggle on `PartnerAnalytics` (separate FE follow-up once data lands)
- Backfill of `growth_decomposition` historical values (DS picks whether to emit history or forward-only)
- Real-time fee-status change detection (daily cadence on audit table is fine)
- HH-level fee aggregation (account-level audit is the source; HH-level derives downstream)

---

## 7. Open questions for DS

1. **Audit table scope** — is `silver/api_dims/fee_status_audit/` the right landing, or do you want it in `gold/`? Daily cadence acceptable, or should it be event-based?
2. **Backfill semantics** — when current fee status is `fee_paying` but the account had a long no-fee period historically, flowing current backwards is wrong (would over-credit historical fee-paying AUA). Is the directive really "always flow current backwards regardless," or "flow current backwards UNLESS there's evidence of historical change"? Worth clarifying with Andrew before coding.
3. **Aggregate field semantics post-backfill** — when historical fee status is synthetic, should the aggregate fields stay observed-only, or align with sum-of-buckets? Recommend: aggregate stays observed (single source of truth for "what was the AUA on date X"); sub-streams use synthetic backfill so they sum to aggregate at all points.
4. **Cost of fee-split timeseries** — 8 new fields per daily point per advisor. For Inflection (~700-day history × 4 advisors) that's small. Not a concern at this scale.

---

*Drafted by 0.4.2_RD_AdvisorIntelligence · 2026-05-12*
*FE consumer commit: portal `563d045c` (AdvisorAnalytics with picker logic + degradation badge ready).*
*Andrew directives: 2026-05-12 (fee-slice everything + backward-flow + audit) and same-day SYNC#2 (GRO scope).*
*Companion briefs: cash_drag account-level (`be241a8c`), firm_concentrations (`0fa96cd9`), canonical tax-status (`b28dd2419`), TTM-locked panel completeness (`2e5539bac`), N1 firm TTM emit (filed), Orion saved-query cost_basis_by_year (filed), 49F TTM correction (filed).*
