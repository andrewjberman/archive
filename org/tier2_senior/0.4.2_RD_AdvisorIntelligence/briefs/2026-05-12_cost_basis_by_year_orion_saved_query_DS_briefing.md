# DS Briefing — `cost_basis_by_year` data gap (Orion per-lot saved query) for Inflection

**Recipient:** `0.4.0_DS_ClientPlatform~B` (DS lead; may want to coordinate with DE / AE for the saved-query pull)
**From:** `0.4.2_RD_AdvisorIntelligence`
**Pipeline:** Inflection partner / Advisor Intelligence
**Surface:** Cost Basis & Tax Status panel — `Cost Basis by Year` table (renders L3+ only)
**Status:** L2 + L3 TTM-locked fields shipped (`2e5539bac`). `cost_basis_by_year` remains null because Inflection has no per-lot acquisition date or per-lot cost basis in current silver/gold tables.

---

## 1. Summary

To populate the canonical `Cost Basis by Year` table at L3 (and optionally L2/N1), we need **per-tax-lot data** that doesn't exist in Inflection's current silver/gold landscape. This brief requests a new Orion saved-query feed that lands per-lot rows with:

- `account_id`
- `ticker` (or asset identifier)
- `units` (lot-level)
- `cost_basis` (lot-level, USD)
- `market_value` (lot-level, latest)
- `acquired_date` (or `purchase_year` if Orion only exposes year)
- `lot_id` or similar unique key

This feed should land as a silver table (e.g., `silver/api_dims/tax_lots/snapshot_date=YYYY-MM-DD/data.parquet`) and be consumed by INF_D_02 (advisor / client detail) to emit the canonical `tax.cost_basis_by_year` array.

---

## 2. Motivation

The FE renders a `Cost Basis by Year` table at L3 (49F canonical) with columns: Year · Held duration badge · Cost Basis · Market Value · Unrealized Gain. Each row aggregates per acquisition year:

```ts
{ purchase_year: 2023, cost_basis: 450000, market_value: 612000, unrealized_gain: 162000 }
```

For 49F, BD has lot-level data from Black Diamond's holdings feed. For Inflection, **no equivalent per-lot data exists** in any current silver/gold table:

| Table | Has cost_basis per position? | Has purchase_year per lot? |
|-------|------------------------------|----------------------------|
| `gold/canonical/holdings_{date}.parquet` | NO (market_value + units + price only) | NO |
| `silver/api_dims/tax_unrealized` | account-grain aggregate (no per-position, no per-lot) | NO |
| `gold/timeseries/account_performance` | account-grain (no per-position) | NO |

Per DS~B's investigation (SYNC #1): *"No per-lot purchase_year anywhere in INF silver/gold. tax_unrealized is account-grain aggregate; holdings is current snapshot. Would need bronze lot acquisition dates."*

## 3. Requested data feed

Most likely vehicle: a new Orion REST endpoint or saved query that returns tax-lot rows.

**Schema (target):**
```python
{
  "account_id":      int,        # Orion Int64, matches canonical key space
  "ticker":          str,
  "lot_id":          str,        # Orion's unique lot identifier
  "units":           float,      # lot-level
  "cost_basis":      float,      # lot-level USD (including any wash-sale adjustments)
  "market_value":    float,      # lot-level current valuation
  "acquired_date":   date,       # YYYY-MM-DD
  "snapshot_date":   date,       # the date this snapshot was pulled
}
```

If Orion only exposes `acquired_year` (not full date), that's acceptable — `purchase_year` is the FE's only consumer of the date field anyway.

**Suggested landing:** `silver/api_dims/tax_lots/snapshot_date=YYYY-MM-DD/data.parquet`.

**Cadence:** daily (mirroring the existing tax_unrealized / tax_realized feeds at the same snapshot frequency).

## 4. Downstream aggregation (your domain — informational)

Once the silver feed exists, INF_D_02 should aggregate per (account → HH → advisor → firm):

```python
# pseudocode
lots_for_scope = tax_lots[tax_lots['account_id'].isin(scope_accounts)]
by_year = lots_for_scope.groupby(lots_for_scope['acquired_date'].dt.year).agg(
    cost_basis=('cost_basis', 'sum'),
    market_value=('market_value', 'sum'),
)
by_year['unrealized_gain'] = by_year['market_value'] - by_year['cost_basis']
```

Output: a list of `{purchase_year, cost_basis, market_value, unrealized_gain}` rows emitted to `summary.tax.cost_basis_by_year`. The FE's existing `CostBasisByYearTable` (in `TaxCostBasisPanel.tsx:305`) does the rest — bucket floor at 2020, "Unknown" handling, totals row.

## 5. Acceptance criteria

- [ ] New Orion saved-query / endpoint identified and accessible from the data pipeline
- [ ] Silver feed `tax_lots` produced daily with the schema in §3 (or close to it — adjust schema once you see what Orion actually returns)
- [ ] INF_D_02 aggregates per-scope and emits `summary.tax.cost_basis_by_year` at L2/L3 (and N1 if simple)
- [ ] Spot-check L3 for a known HH: rows sum to that HH's total cost basis (cross-check against `tax_unrealized.total_cost_basis` per account)
- [ ] Bucket floor logic deferred to FE (DS just emits raw per-year rows)
- [ ] Empty / unknown acquired_date rows allowed; FE handles them as "Unknown" bucket

## 6. Coordination notes

**This may need AE 0.6.1 involvement** to set up the Orion API pull / saved-query in the Lambda layer that produces silver/api_dims. If the existing tax_unrealized feed has a saved-query pattern you can mirror, this is mostly extension. If Orion requires a new saved-query definition on their side, that's a customer-coordination ask — flag if so.

**Timing:** non-urgent. Andrew explicitly accepted the interim shape (skipping `cost_basis_by_year`) at SYNC #2. This is the follow-up to close the gap properly. No pressure to ship same-day.

**49F has equivalent data via BD** — the BD pipeline produces lot-level cost basis from Black Diamond's holdings feed. INF's gap is structural to the Orion source, not to Opal's pipeline shape.

## 7. Out of scope

- 49F TTM correction (separate brief)
- N1 firm-level TTM emit for the *other* fields (separate brief — small follow-up to `2e5539bac`)
- Changes to the existing `tax_unrealized` / `tax_realized` feeds — they're correct for their use case, just not granular enough for this one

## 8. Open question

What's the right entry point for an Orion saved-query addition?
- (a) DS~B can scope and route to AE 0.6.1 for the Lambda-side pull
- (b) Andrew coordinates customer-side (Inflection ops contact) for new Orion saved-query setup
- (c) Some existing endpoint already exposes lot-level data and we just haven't found it (worth a 30-min audit before committing to a new pull)

Recommend (c) first as the cheapest path. The Orion API has a lot of surface area; if there's an existing `/v1/portfolio/lots` or equivalent we just haven't hooked, that's hours of work not days.

---

*Drafted by 0.4.2_RD_AdvisorIntelligence · 2026-05-12*
*Spawned from DS~B's SYNC #1 finding: "No per-lot purchase_year anywhere in INF silver/gold. Would need bronze lot acquisition dates."*
*Companion to: `b28dd2419` (canonical tax-status), `2e5539bac` (L2/L3 TTM-locked fields).*
