# Brief: Two Platinum Emit Bugs — GEO 3-way NNA Schism + RFS NNA Window Cumulative-Sum

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-04-15 (post-presentation)
**Addressed to:** 1.0.0_SA_CTO
**Status:** Proposal — awaiting CTO decomposition into task orders
**Reporters:** 0.4.0_DE_ClientPlatform (both bugs)

---

## Bug 1 — State-level NNA disagrees three ways in `partner_analytics_quarterly.json`

**Surface:** Snapshot-GEO-NNA donut on AdvisorIntelligence Distribution tab, drilled into a state. FE patch (commit `51d7dc3`) made the donut center match the slices by switching to the `by_city` sum; underlying DS reconciliation gap remains.

### Three conflicting aggregates for the same (period, state)

`s3://opal-data-bd/platinum/firm/partner_analytics_quarterly.json`, period=`current`, state=TX:

| Path | Value | Grain |
|---|---|---|
| `views.nna.current.geo.donut.segments[tx].value` | +$637,212 | account × state (canonical_nna × acct_dim.client_state) |
| `sum(views.nna.current.geo.drill.tx.by_city[*].total)` (151 cities) | -$3,777,843 | relationship × city, excluding city='Unknown' |
| `views.nna.current.geo.drill.tx.total.total` | -$4,750,860 | relationship × state, all cities |

Pairwise gaps: $4.4M / $5.4M / $973K. Pattern will repeat across every state, every period, and the ADV/OFC cohorts (same emit code shape).

### Root cause

In `data/black_diamond/scripts/gold/D_01.partner_analytics.py::build_nna_geo_view` (lines 1242–1429):

1. **Donut segments** (line 1266) — `_period_nna_by_grain(canonical_nna, ..., 'state', acct_dim→state_map)`. **Account-grain** NNA joined to state via `acct_dim.client_state`. One account, one state.
2. **by_city drill** (lines 1330–1411) — `_compute_rel_period_nna(cp_end, cp_start, canonical_nna, ...)` → `rel_nna['state'] = rel_geo_lookup` → `rel_nna['city'] = rel_city_lookup` → `groupby('city').sum()`. **Relationship-grain**, state and city each via `modal_state` / `modal_city` of the relationship's accounts (`_build_rel_geo_lookup`, line 488). Multi-state relationships collapse to one state. Filter `city != 'Unknown'`.
3. **distribution.total** (line 1408, `by_segment_dist[key]`) — same relationship-grain `rel_nna` as #2, but keeps all cities including `Unknown`. Extra gap vs #2 = relationships in TX with missing-city attribution.

Each of the three is internally consistent; the join/grain/filter choices differ. Three different answers are produced for what the FE reads as one number.

### Proposal

**Option A (recommended): Build one atomic table, roll up three ways.** One row per `(period, account_id, relationship_id, state, city)` with per-period NNA. Rollups by `sum`:

- `(period, state)` → `donut.segments[<state>].value`
- `(period, state, city)` → `drill.<state>.by_city[<city>].total`
- `(period, state, relationship)` → distribution inputs

Filters applied once at the atomic layer (state/city normalization, Unknown sentinel). No more relationship→single-state collapse — an account in TX counts in TX regardless of its relationship's "primary" state. Distribution stats can still be relationship-grain for bell-curve shape, but the `total.total` becomes the account-grain state sum and reconciles by construction.

**Option B: Emit atomic only, FE sums.** Drops `donut.segments[].value` and `distribution.total`. FE sums `by_city` for every panel. Less data, no schism possible. Downside: FE re-runs the sum on load (151 cities = negligible).

Recommend A — keeps wire format stable, one-time DS refactor, no FE change.

### Validation to add

In `validate_platinum_consistency.py`:

```
assert abs(sum(by_city[state].values()) - donut.segments[state].value) < $1
```

For every state × period × cohort (GEO, ADV, OFC). Run at emit time; fail the gold run if it trips.

### Scope

- `D_01.partner_analytics.py::build_nna_geo_view`, `build_nna_adv_view`, and OFC cohort (`_period_nna_by_grain` office path at line 2118).
- All historical periods regenerate on next D_01 run. No schema change, no FE edit required (Option A).
- `validate_platinum_consistency.py` — add reconciliation asserts.

---

## Bug 2 — RFS `nna_ytd` and `nna_max` are sum-of-cumulative

**Surface:** AdvisorPublicProfile → Book → RelationshipFlowsSummary panel (QTD/YTD/MAX toggle). DE reported YTD/MAX values conflicting with inflows/outflows and with the account's inception-to-date timeseries. Book values inflated up to 11× book value on MAX.

### Evidence (bit-for-bit match to a single arithmetic error)

Per-account `z0820265531` (total_market_value $16.4M), spot-pulled post-D_02/D_04 rerun `aa261b5b`:

```
timeseries: 714 daily rows, 2024-04-30 → 2026-04-13
first.nna_canonical = 0
last.nna_canonical  = 24,981,020.95           ← correct ITD NNA
sum(nna_canonical)  = 563,610,060.60          ← area under the curve

rfs.nna_max (emitted)  = 563,610,060.60        ← matches sum, not ITD delta
rfs.nna_ytd (emitted)  = 175,076,359.23        ← also a sum-of-cumulative, smaller slice
rfs.nna_qtd (emitted)  =  24,981,020.95        ← "correct" by accident (713 rows ≈ 0)
```

Book-grain `platinum/advisors/travis_penfield/summary.json`:

```
book.rfs.decomposition_max.nna = $4,824,184,200   ← 11× book value (~$428M MV)
book.rfs.decomposition_ytd.nna = $  540,427,263   ← YTD NNA on a ~$428M book
book.rfs.decomposition_qtd.nna = $   64,816,714   ← plausible, survived spot-check
```

### Root cause

`data/black_diamond/scripts/gold/D_04.client_portal_summary.py`:

- `_compute_window_decomposition` (line 676): `nna = sum(r.get('nna', 0) or 0 for r in slice_rows)`
- `_compute_window_flows` nna branch (line 747): `nna_sum = sum(r.get('nna', 0) or 0 for r in slice_rows)`

The internal `nna` column on the per-account aua_timeseries (and the advisor timeseries after the 2026-04-15 `aa261b5b` melt) is a **cumulative running total**, not a daily delta. Summing it produces the area under the curve. For QTD, the account had no pre-Q activity, so most rows are ~0 and the sum ≈ the last value = correct by coincidence. YTD (103 rows of cumulative) and MAX (714 rows) compound.

Bug 2 collapses both of DE's reported bugs. Separately observed: per-account `cum_inflows` can transit negative values at quarter boundaries (reversal/correction pattern on z0820265531). That's an upstream bronze/silver data-quality issue separate from this emit fix — worth its own investigation but does not drive the YTD/MAX NNA explosion.

### Proposal

Localized fix in `D_04.client_portal_summary.py` — two functions, preserves the internal ts contract:

```python
def _window_nna_delta(ts_rows, cutoff: str) -> float:
    if not ts_rows:
        return 0.0
    last = ts_rows[-1].get('nna', 0) or 0
    if not cutoff:
        return round(float(last), 2)              # MAX = inception-to-date
    pre = [r for r in ts_rows if r.get('date', '') < cutoff]
    base = (pre[-1].get('nna', 0) or 0) if pre else 0
    return round(float(last - base), 2)
```

Apply to both `_compute_window_decomposition` and the nna branch of `_compute_window_flows`. `cum_inflows` / `cum_outflows` branches are already delta-based and correct — leave them.

**Open verification before commit:** confirm `market_growth` and `synthetic_correction` on the internal ts are daily deltas, not cumulative. QTD values ($18M / -$2.3M on Travis's book) look delta-shaped. If MAX values reveal the same sum-of-cumulative problem on those two columns, extend the fix to them. Quick diff: `sum(mg) over 714 rows` vs `last.mg - 0` on one advisor's ts.

**Alternative (cleaner, more invasive):** change `nna` to a daily delta in `D_02.build_account_timeseries` and `build_advisor_timeseries`. Then `sum(r.nna)` is correct by construction and the reconciliation identity `market_growth + synthetic_correction + nna ≈ total_aua[last] - total_aua[pre_cutoff]` holds trivially. Changes the ts wire contract — anything else reading `nna` as cumulative would break. Not recommended.

### Validation to add

Account grain:
```
rfs.nna_max  == last.nna_canonical - first.nna_canonical   (exact)
rfs.nna_ytd  == last.nna_canonical - row_before_year_start.nna_canonical
```

Book grain (sanity ceiling):
```
book.rfs.nna_max ≤ 2 × |total_market_value|
```

Cross-grain:
```
|inflows_window - outflows_window - nna_window| < $1   (where upstream cum_inflows is clean)
```

Add to `validate_platinum_consistency.py`. Fail the gold run on violation.

---

## Ship order — D_02 → D_04 rerun

1. Both fixes localize to `D_02.py` (bug 1 / view emitters) and `D_04.py` (bug 2 / windowing). One combined commit, one gold rerun cycle.
2. AE runs `D_02 → D_03 → D_04` on QA runner (~30 min end-to-end, same path as this morning's `aa261b5b` rerun).
3. DS spot-check on rerun:
   - Bug 1 — `sum(by_city[tx].values()) == donut.segments[tx].value` exact. Re-check AR/GA (largest Q2 outflows).
   - Bug 2 — z0820265531 `rfs.nna_max == $24,981,021` exact. Travis `book.rfs.nna_max` ≤ 2× book.
4. DE wires any affected FE surfaces (Bug 1 donut center could revert to DS path after reconciliation; Bug 2 no FE change needed).

No PROD impact either bug — both emit-time only, no cross-contamination with other panels.
