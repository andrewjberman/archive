# Brief — Drill-scoped breakdowns for `new_clients_by_period` (Inflection)

**Author:** 0.4.2_RD_AdvisorIntelligence
**For:** 0.4.0_DS_ClientPlatform~A
**Date:** 2026-05-15
**Origin:** Andrew direct — "total clients need to be adjusted by GEO and ADV drills, not only by window"
**Follow-up to:** `brief_ds_inflection_new_clients_by_period.md` (shipped as `4e4a3c321`)
**Lane:** DS — extends the same gold function. **No new FE work needed** — the FE consumer shipped defensively (`1bc8e4ad`).

---

## 1. Context

`4e4a3c321` added firm-wide `new_clients_by_period` to `INF_D_00d.cumulative_chart.py`. The Continuous-view "New Clients" tile now reflects the selected Window — but it reads the **firm-wide** count regardless of GEO/ADV drill. Drilling into Washington (or a city, or an advisor) still shows the firm-wide number.

Andrew wants the tile drill-scoped: per-state at GEO L1, per-city at GEO L2, per-advisor at ADV L1.

The FE cannot derive this — it has only firm-level period counts. It needs per-segment breakdowns in the artifact. This brief specifies them.

---

## 2. Exact FE-expected shape (contract — already wired in `1bc8e4ad`)

Extend `chart['new_clients_by_period']` with three optional sibling keys alongside the existing `quarterly/monthly/annually`:

```json
"new_clients_by_period": {
  "quarterly": [ {period,label,count}, ... ],     // firm-wide — UNCHANGED
  "monthly":   [ ... ],
  "annually":  [ ... ],
  "by_geo":      { "<stateKey>": {quarterly:[...],monthly:[...],annually:[...]}, ... },
  "by_geo_city": { "<cityKey>":  {quarterly:[...],monthly:[...],annually:[...]}, ... },
  "by_adv":      { "<advKey>":   {quarterly:[...],monthly:[...],annually:[...]}, ... }
}
```

Each leaf is the **same `{period,label,count}` shape and string formats** as the firm-wide set (per the first brief's section 2 table). Each `by_*` value is a full `{quarterly,monthly,annually}` set.

**Key conventions (critical — the FE matches with a canonical-tolerant lookup, but emit exact):**
- `by_geo` keys = the **same state keys as `chart['geo_drill']`** (and the `geo` donut segment keys).
- `by_geo_city` keys = the **same city keys** used inside `geo_drill[state]` city categories / the geo donut `cities[].key`.
- `by_adv` keys = the **same advisor keys as `chart['adv']['categories']`**.

The FE selects the slice by cohort + drill state; if a `by_*` key is missing it falls back to firm-wide. So partial emit is safe — but completeness is the goal.

---

## 3. Source + grain — reuse the existing geo/adv assignment

"New client" is unchanged from the first brief: a **household**, bucketed by the period of its **earliest `account_start_date`** (from `accounts_v2`).

The only new work is **assigning each household to its state / city / advisor segment** — and that assignment **must match the geo/adv views in the same script** so the new-client counts reconcile to the donut segments the user sees:

- **`by_geo` / `by_geo_city`:** assign each household to its state/city using the **same `hh_dim` (`state_code`, `city`) the geo views use** — i.e. the `_supplement_hh_dim_state`-patched `hh_dim` that `build_geo_view` / `build_geo_drill_view` consume. Do **not** use `accounts_v2.state` directly — `build_geo_view` deliberately routes through the supplemented `hh_dim`, and using a different source would make the new-client counts diverge from the donut.
- **`by_adv`:** assign each household to its advisor using the **same logic `build_adv_view(cp, accounts_v2, ...)` uses** to map households→advisor.

Pass `hh_dim` (and whatever the adv assignment needs) into the builder — it currently takes only `accounts_v2`.

Households with no state/city/advisor assignment: fold into the segment the geo/adv views fold them into (`Other` / `no_city`) or omit — match the view's treatment so totals reconcile.

---

## 4. Implementation sketch — `INF_D_00d.cumulative_chart.py`

Extend the existing `build_new_clients_by_period` (signature gains `hh_dim`, plus the advisor map). `hh_first` (household → earliest `account_start_date`) is already computed; the period-bucketing helper already exists. Per-segment = run the same bucketing on the household subset for that segment.

```python
def build_new_clients_by_period(accounts_v2, hh_dim, hh_to_advisor):
    # ... existing: build df, hh_first (household_id -> earliest account_start_date) ...

    def _period_set(hh_series):
        """{quarterly,monthly,annually} for a household->date Series."""
        return {g: _periods(g, hh_series) for g in ('quarterly', 'monthly', 'annually')}
        # (refactor existing _periods to take the series as an arg)

    result = _period_set(hh_first)                       # firm-wide (unchanged output)

    # household -> state / city, from the SAME supplemented hh_dim the geo views use
    hh_state = hh_dim.dropna(subset=['household_id']).set_index('household_id')['state_code']
    hh_city  = hh_dim.dropna(subset=['household_id']).set_index('household_id')['city']

    by_geo, by_geo_city, by_adv = {}, {}, {}
    for state_key, members in hh_first.groupby(hh_first.index.map(hh_state)):
        if pd.notna(state_key):
            by_geo[state_key] = _period_set(members)
    for city_key, members in hh_first.groupby(hh_first.index.map(hh_city)):
        if pd.notna(city_key):
            by_geo_city[city_key] = _period_set(members)
    for adv_key, members in hh_first.groupby(hh_first.index.map(hh_to_advisor)):
        if pd.notna(adv_key):
            by_adv[adv_key] = _period_set(members)

    result['by_geo'] = by_geo
    result['by_geo_city'] = by_geo_city
    result['by_adv'] = by_adv
    return result
```

The exact key forms for `state_key` / `city_key` / `adv_key` must equal the keys `geo_drill` / geo city categories / `adv['categories']` emit — derive them through whatever normalization those builders apply (don't hand-roll a second normalization). `_periods` already sorts ascending and formats `period`/`label` per contract.

`main()` wiring: `hh_dim` and the advisor map are already in scope (`hh_dim` is built at L547-548; the advisor assignment is inside `build_adv_view` — lift it or recompute the same way). Pass them into `build_new_clients_by_period`.

---

## 5. Verification

After the run, `new_clients_by_period.by_geo` should reconcile to the firm-wide set:

```bash
aws s3 cp s3://opal-data-inf/platinum/firm/cumulative_chart.json - | python3 -c "
import json,sys
n=json.load(sys.stdin)['new_clients_by_period']
firm=sum(e['count'] for e in n['annually'])
geo=sum(e['count'] for s in n.get('by_geo',{}).values() for e in s['annually'])
print('firm annual total:', firm, '| by_geo annual total:', geo, '| reconciles:', firm==geo)
print('by_geo keys:', sorted(n.get('by_geo',{}))[:12])
print('by_adv keys:', sorted(n.get('by_adv',{})))
print('WA annual total:', sum(e[\"count\"] for e in n.get('by_geo',{}).get('WA',{}).get('annually',[])))
"
```
- `by_geo` annual total should equal the firm-wide annual total (296 all-time, per the first brief) — every household lands in exactly one state. Same for `by_adv`. (`by_geo_city` may be < firm total if some households have no city — that's fine, matches the geo donut's `no_city`/`Other` handling.)
- `by_geo` / `by_adv` key sets should match `geo_drill` keys / `adv['categories']`.

---

## 6. Deploy

Same standard DS gold cycle as the first brief (commit-gate → commit → push CLOUD → S3 → `deployed` MATCH → next INF_D chain or SSM-direct `--single INF_D_00d`). No portal release — the FE consumer (`1bc8e4ad`) is already on portal/DEV and activates the moment the artifact carries `by_geo`/`by_geo_city`/`by_adv`.

If you fold this into the same chain run as `4e4a3c321`, both the firm-wide tile and the drill-scoped tile go live together.

---

## 7. Contacts

- FE contract questions → 0.4.2_RD_AdvisorIntelligence
- FE consumer: `resolveNewClientsByPeriod()` in `DistributionTab.tsx` (commit `1bc8e4ad`)
