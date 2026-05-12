# DS Briefing — Distribution Tab Gap-Closure (Snapshot/Continuous × GEO/ADV × NNA/AUA)

**Pipeline:** Inflection partner / Advisor Intelligence
**Surface:** Distribution tab (`portal/src/pages/AdvisorIntelligence/_shared/tabs/DistributionTab.tsx`)
**Reference implementation:** 49 Financial — all 8 view combinations work end-to-end today
**Status:** Inflection FE renders the structure but state values come back **N/A · 0.0%** (firm total NNA = +$562K is computed; per-state breakdown is empty). ADV cohort and Continuous-ADV timeseries are missing entirely.

---

## 1. Summary

Close the data gaps so all 8 Distribution-tab view combinations work for Inflection:

| Cohort | View | Mode | Status |
|--------|------|------|--------|
| GEO    | Snapshot   | NNA | **GAP A — state values are N/A** |
| GEO    | Snapshot   | AUA | **GAP A — state values are N/A** |
| GEO    | Snapshot drill L1→L2 (state→city) | NNA/AUA | **GAP B — city drilldown unpopulated** |
| GEO    | Continuous | NNA/AUA | Works (cumulative_chart.geo + nna_geo populated) ✓ |
| GEO    | Continuous drill (state→city) | NNA/AUA | **GAP C — geo_drill missing per-state city timeseries** |
| ADV    | Snapshot   | NNA/AUA | **GAP D — advisor segments not surfacing 4 advisors incl. IWM catchall** |
| ADV    | Snapshot drill L1 (advisor→clients) | NNA | **GAP E — `platinum/advisors/{key}/nna_clients.json` not produced** |
| ADV    | Continuous | NNA/AUA | **GAP F — `cumulative_chart.adv` + `nna_adv` timeseries not emitted** |

Net new DS work: five gaps (A through F), all aggregations from data that already lives in silver/holdings + canonical_nna. Same schemas as 49F — no new artifact contracts; we're just populating Inflection's versions of files that already exist for 49F.

---

## 2. Reference: how 49F does it (so we mirror exactly)

**Two main artifacts back the entire Distribution tab:**

### `platinum/firm/partner_analytics_{monthly|quarterly|annual}.json` (Snapshot)

Schema (the relevant subset):
```ts
{
  views: {
    nna: {                                       // <- NNA mode
      current: {
        geo: {                                   // <- GEO cohort
          donut: {
            segments: [
              {
                key: 'CA',
                label: 'California',
                value: 1234567,                  // <- state-level NNA $$
                value_pct: 12.5,
                client_count: 45,
                cities: [                        // <- L2 drill, nested in segment
                  { key: 'san_francisco', label: 'San Francisco', value: 234567, value_pct: 1.8, aua: 45000000 },
                  ...
                ]
              },
              ...
            ]
          }
        },
        adv: {                                   // <- ADV cohort
          donut: {
            segments: [
              {
                key: 'travis_penfield',
                label: 'Travis Penfield',
                value: 567890,                   // <- advisor-level NNA $$
                value_pct: 5.4,
                client_count: 12
                // NO nested clients here — see separate nna_clients.json
              },
              ...
            ]
          }
        }
      },
      q1: {...}, q2: {...}, q3: {...}            // historical period strips
    },
    aua: { current: { geo: {...}, adv: {...} } } // <- AUA mode (parallel structure)
  }
}
```

**Same artifact serves NNA + AUA + both cohorts** — FE picks the right path based on toggle state.

### `platinum/advisors/{advisor_key}/nna_clients.json` (ADV-NNA L1 drill)

Loaded **on click** when user drills into a specific advisor in Snapshot-ADV-NNA:
```ts
{
  advisor_id: 'travis_penfield',
  period: 'current',
  total_nna: 567890,
  clients: [
    { key: 'z00000001', display_name: 'Acme Corp', nna: 234567, nna_pct: 41.3, account_count: 3 },
    ...
  ]
}
```

ADV-NNA drill is terminal — no L2 below advisor→client.

### `platinum/firm/cumulative_chart.json` (Continuous)

```ts
{
  date_range: { start, end },
  geo:     { categories: ['CA','TX',...], data: [{date,'CA':n,'TX':n,...}, ...] },
  nna_geo: { categories: [...], data: [{date,'CA':n,'CA_inflow':n,'CA_outflow':n,...}, ...] },
  adv:     { categories: [...], data: [...] },                   // <- per-advisor AUA timeseries
  nna_adv: { categories: [...], data: [...] },                   // <- per-advisor NNA + flows
  geo_drill: { 'CA': { categories: ['san_francisco',...], data: [...] }, ... },
  adv_drill: { /* per-advisor drill timeseries — currently deferred at 49F too */ }
}
```

---

## 3. The five gaps, mapped to deliverables

### GAP A — State-level NNA/AUA values populated

The screenshot at 2026-05-12 11:55a ET shows California/Minnesota/Washington/Hawaii/Indiana/Idaho all rendering **"N/A · 0.0%"** despite a +$562K firm total. So either:
- (i) `views.nna.current.geo.donut.segments[].value` is null/undefined per state, or
- (ii) The states array is empty and FE is rendering hardcoded labels, or
- (iii) The household → state mapping is broken for Inflection

**Action:** Run a quick diagnostic on the current Inflection `partner_analytics_quarterly.json` — check `views.nna.current.geo.donut.segments`. If empty or all-null, the aggregation from canonical_nna → state isn't joining the household_dim state field. If populated but all `value=0`, the source data may have a column-name mismatch (`state` vs `home_state` vs `state_code`).

**Schema unchanged** — just populate the existing fields.

### GAP B — City-level drilldown (L2 GEO)

For each state segment, populate the `cities[]` array with:
- `key`: lowercase_underscored slug
- `label`: human-readable city name
- `value`: NNA in dollars for that city
- `value_pct`: city's % of total firm NNA
- `aua`: city's AUA (used in AUA mode of the drill)

Inflection's household_dim should have `city` (or equivalent) joinable to state. The aggregation grain is (state, city) → sum(nna) / sum(aua). Same as the state-level rollup, one level deeper.

### GAP C — `geo_drill` in cumulative_chart for city timeseries

49F has this (ADVI_INFLEC.AUDIT-006 reference). Inflection currently doesn't emit `geo_drill`. Add it: per top-state, weekly-sampled timeseries of city-level AUA + NNA flows. Same shape as the top-level `geo` / `nna_geo` blocks.

### GAP D — ADV cohort: 4 advisors including IWM catchall

The 4 Inflection advisor_keys are:
1. Three named individual advisors (per `accounts_dim.advisor_key`)
2. `inflection_wealth_management` — the IWM catchall

Andrew has explicitly called out: **for the ADV cohort, the IWM catchall should be visible** — not stripped per the leaderboard convention.

**Action:** Populate `views.nna.current.adv.donut.segments` and `views.aua.current.adv.donut.segments` with all 4 advisor_keys. Don't filter out `inflection_wealth_management` here (it's filtered out of the **leaderboard** artifact for ranking purposes; this is a different cohort).

Each segment shape per the 49F contract:
```
{ key: 'inflection_wealth_management', label: 'Inflection Wealth Management', value, value_pct, client_count }
```

Period strips (q1/q2/q3 or m1/m2/m3) follow same pattern as GEO.

### GAP E — `nna_clients.json` per advisor

For each of the 4 advisors, emit `platinum/advisors/{advisor_key}/nna_clients.json` matching the 49F schema in §2. The clients list is the households grouped under each advisor, ranked by NNA descending. Use `canonical_nna` per-HH × advisor_key joins as the source of truth.

For `inflection_wealth_management` specifically — the catchall holds households whose primary advisor_key didn't route cleanly. The nna_clients list for IWM should include those routed-to-catchall households so the advisor breakdown is complete.

### GAP F — `adv` and `nna_adv` timeseries in cumulative_chart

49F has these in `cumulative_chart.json`. Add to Inflection's version:
```
adv:     { categories: [...4 advisor_keys...], data: [{date, advisor_key_1: aua, ...}, ...] }
nna_adv: { categories: [...4 advisor_keys...], data: [{date, advisor_key_1: nna, advisor_key_1_inflow: ..., advisor_key_1_outflow: ..., ...}, ...] }
```

`adv_drill` per advisor is deferred (49F also deferred). Don't block on this.

---

## 4. Why these are gaps and not new contracts

**All artifact paths and schemas already exist for 49F.** Inflection just needs the equivalent populated. The DS lift is:

- **GAP A**: probably a single-line bugfix in `INF_D_04.partner_analytics.py` — household-to-state join failing or column name mismatch
- **GAP B**: extend the GEO aggregation grain from state to (state, city). One additional groupby level.
- **GAP C**: per-state city timeseries — same aggregation as A/B but emitted to cumulative_chart instead of partner_analytics
- **GAP D**: ADV cohort segments — group canonical_nna by advisor_key instead of state, include catchall. Same aggregation logic, different group key.
- **GAP E**: per-advisor client breakdown artifact — group canonical_nna by (advisor_key, household_id). New artifact, same schema as 49F.
- **GAP F**: per-advisor timeseries in cumulative_chart — same aggregation as Continuous-GEO but grouped by advisor_key.

All inputs (canonical_nna, holdings, accounts_dim, household_dim with state/city) are already present.

---

## 5. Acceptance criteria

- [ ] **GAP A:** `partner_analytics_quarterly.json` `views.nna.current.geo.donut.segments` has non-null `value` and `value_pct` per state. Sum of segment values ≈ firm total NNA (within rounding). Spot-check California — should not be N/A.
- [ ] **GAP A:** Same check for `views.aua.current.geo.donut.segments`.
- [ ] **GAP B:** Each top state has non-empty `cities[]` array with at least 1 city. Sum of `cities[].value` ≈ state's `value`. Spot-check California cities — should match the household_dim distribution.
- [ ] **GAP C:** `cumulative_chart.json` `geo_drill` exists; top-5 states have city-level timeseries data.
- [ ] **GAP D:** `partner_analytics_quarterly.json` `views.nna.current.adv.donut.segments.length === 4` (3 named + IWM catchall). All have non-null `value`. Same for AUA.
- [ ] **GAP D:** IWM catchall segment present with `key === 'inflection_wealth_management'` and a sensible `client_count`.
- [ ] **GAP E:** `platinum/advisors/inflection_wealth_management/nna_clients.json` exists and is readable. Same for the 3 named advisors. Each has `clients[]` populated; `sum(clients[].nna) ≈ total_nna` per advisor.
- [ ] **GAP F:** `cumulative_chart.json` has `adv` and `nna_adv` blocks with 4 categories each and a date-axis matching `nna_geo`.
- [ ] **Schema matches 49F exactly** — drop into the existing FE without any FE schema change.
- [ ] **Historical period strips** (q1/q2/q3) for the new ADV cohort follow the same INFSEGSTRIP pattern as GEO.

---

## 6. Coordination notes

**FE follows.** No FE work is required to consume any of these — the Distribution tab already reads exactly these paths and field names for 49F. The moment the Inflection artifacts populate with matching schema, the tab lights up.

**IWM catchall handling** — explicit ask from Andrew: include in ADV cohort. This conflicts with the leaderboard exclusion convention. If you want a structural switch (e.g., a `include_catchall: true` config flag on D_04), file it; otherwise hardcode the include for the ADV-cohort segments path specifically.

**PII / pseudonymization on client drill** — match 49F: `display_name` shown in cleartext only when caller's auth claims `canSeeCleartext === true`; otherwise pseudonymized. The `key` field always remains the canonical household_id-equivalent so drill-to-L3 navigation works.

**`client_count` per advisor segment** — should reflect distinct household count routing to that advisor_key (not account count). For IWM catchall, this is the count of HHs whose `advisor_key === 'inflection_wealth_management'` (i.e., didn't route to a named advisor).

---

## 7. Out of scope

- `adv_drill` timeseries in `cumulative_chart.json` (per-advisor client-level breakdowns over time) — 49F also defers; not needed for the current asks.
- Adding new toggles or view combinations beyond the existing 8 — this brief is gap-closure, not new surface area.
- Restructuring the advisor_key namespace — IWM catchall stays as-is.
- Window-specific aggregations (the existing partner_analytics already has monthly/quarterly/annual variants; nothing new needed).

---

## 8. Open questions for DS

1. **GAP A diagnosis** — is the GEO state aggregation actually failing, or is the artifact populated and the FE not reading it? A quick `aws s3 cp s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json -` to inspect `.views.nna.current.geo.donut.segments` would resolve this in 30 seconds.

2. **household state column** — what's the canonical column name in Inflection's household_dim for state and city? (`state` / `home_state` / `mailing_state` / something else?) Whatever it is, GAP A and GAP B both depend on it.

3. **IWM catchall HH count** — roughly how many households route to the catchall vs the 3 named advisors? If it's >50%, the catchall would dominate the ADV donut visually and that may not be the right product framing. Worth a sanity-check before shipping.

4. **Dispatch chain entry** — same as INF_D_06 (cash_drag) and INF_D_07a (firm_concentrations), the new/modified scripts need entries in `orion-gold-dispatch.sh`. Flag any that need AE 0.6.1 / 0.7 wires.

---

*Drafted by 0.4.2_RD_AdvisorIntelligence · 2026-05-12*
*Companion briefs: cash_drag (shipped `be241a8c`), firm_concentrations (shipped `0fa96cd9`).*
*Lineage: investigated against DistributionTab.tsx, getPlatinumPartnerAnalytics / getPlatinumCumulativeChart / getPlatinumAdvisorNnaClients, INF_D_04.partner_analytics.py, INF_D_00d.cumulative_chart.py.*
