# DS Briefing — Distribution NNA donut + city-drill data gaps (Inflection)

**Recipient:** `0.4.0_DS_ClientPlatform~D`
**From:** `0.4.2_RD_AdvisorIntelligence`
**Pipeline:** Inflection partner / Advisor Intelligence
**Surface:** Distribution tab → Segment Analytics panel — Snapshot/GEO/NNA and Continuous/GEO/NNA drill paths
**Status:** Two distinct DS-side data bugs visible at 2026-05-12 ~16:17Z. FE fixes for the related FE-side bugs (left-card mismatch in drill view + ADV cohort gating) are landing in parallel.

---

## 1. Summary

Two data-side bugs in `partner_analytics_{monthly|quarterly|annual}.json` that produce nonsense numbers on the Distribution tab when in Snapshot or Continuous mode + NNA mode:

1. **Bug A — State-level NNA segment shows AUA-magnitude values.** Firm donut center: `Net New Assets +$369K`. Washington legend: `+$173M · 91.1%`. Washington's NNA is showing as $173M (= state AUA), not the ~$336K it should be at 91.1% of firm NNA. Suggests `views.nna[period].geo.donut.segments[].value` is null or populated with AUA, and FE falls back to `aua`.
2. **Bug B — City-level NNA drill data not populated.** Drilling into Washington at Snapshot/GEO/NNA renders "No city-level data available for Washington." FE reads `views.nna[period].geo.drill[state].by_city[city]` per the existing type schema (`portal/src/.../types.ts:752`). Either that path is empty in the artifact or DS produces a different key.

Both bugs are in the same emitter (`INF_D_04.partner_analytics.py` or wherever the NNA donut/drill blocks are built). The GEO/AUA path is fine — state values populate correctly and city drills render — so the NNA path has parallel work missing.

---

## 2. Bug A — Magnitude mismatch on state-level NNA donut segments

### What FE sees and renders

Per `DistributionTab.tsx:3243`, the donut legend reads:
```ts
const display = seg.value ?? seg.aua
```

For Washington at the current snapshot:
- Firm NNA donut center: `+$369K` (firm-level rollup, correct)
- Washington segment displayed: `+$173M · 91.1%`

If `seg.value` were populated correctly with Washington's NNA (~91.1% × $369K ≈ $336K), the legend would show `+$336K · 91.1%`. The fact that it shows `+$173M` means the FE is falling back to `seg.aua` — i.e., **`seg.value` is null/missing on the NNA donut entries**, OR DS is emitting AUA in the `value` field.

### Where to look

Most likely culprit: `INF_D_04.partner_analytics.py`, the function that builds `views.nna[period].geo.donut.segments`. Compare its output to the parallel `views.aua[period].geo.donut.segments` build — `value` should be populated with NNA flow ($), not AUA.

### Required schema (per 49F canonical, confirmed working at 49F)

```json
"views": {
  "nna": {
    "current": {
      "geo": {
        "donut": {
          "total": 369000,                // firm NNA total ($)
          "segments": [
            {
              "key":        "WA",
              "label":      "Washington",
              "value":      336000,        // ← STATE'S NNA ($), not AUA
              "value_pct":  91.1,          // state NNA / firm NNA × 100
              "aua":        172500000,     // state AUA (informational only)
              "aua_pct":    85.0,          // state AUA / firm AUA × 100 (informational)
              ...
            },
            ...
          ]
        },
        ...
      }
    }
  }
}
```

Critical: `value` is the period's NNA flow for that state. `aua` is informational. The two MUST NOT be conflated.

### Acceptance for Bug A

- [ ] `views.nna[period].geo.donut.segments[].value` is populated for every state, in $ NNA (period flow)
- [ ] `sum(segments[].value) ≈ donut.total` (= firm NNA, within rounding)
- [ ] Spot-check: Washington's `value` should be a small dollar number (hundreds of $K to low $M range), NOT the state's AUA ($173M)
- [ ] `value_pct` field also populated (currently FE reads `aua_pct` for legend % — that may be its own bug but let's leave that to FE side)
- [ ] AUA path unaffected (no regression in `views.aua[period].geo.donut.segments[].aua`)

---

## 3. Bug B — City-level NNA drill data not populated

### What FE expects

Per `DistributionTab.tsx:2660-2694` and the type schema at `portal/src/pages/AdvisorIntelligence/_shared/types.ts:752`:

```ts
views: {
  nna: {
    [period]: {
      geo: {
        drill: {
          [stateKey: string]: {                    // e.g. 'WA', 'CA'
            by_city: Record<string, DistributionStats>   // ← FE reads this
          }
        }
      }
    }
  }
}

interface DistributionStats {
  total: number    // NNA $ for the city in this period
  count?: number   // optional: HHs in this city
  // ... other DS-emitted fields
}
```

FE behavior: when user drills into a state at NNA mode, it looks up `nnaDrillData[selectedStateKey].by_city`. If absent or empty, renders "No city-level data available for {State}."

### Current state

Drilling into Washington at Snapshot/GEO/NNA → empty city drill. The AUA equivalent (`views.aua[period].geo.donut.segments[].cities[]`) is populated (DS~C confirmed in Distribution Tab brief closure that "WA→Everett, MT→Missoula, CA→Torrance" are populated under the AUA path). The NNA equivalent path is parallel but empty.

### Required emission

For each top state at each period (monthly / quarterly / annually):

```json
"views": {
  "nna": {
    "current": {
      "geo": {
        "drill": {
          "WA": {
            "by_city": {
              "Seattle":        { "total": 124000, "count": 8 },
              "Bellevue":       { "total":  87000, "count": 5 },
              "Spokane":        { "total":  21000, "count": 3 },
              ...
            }
          },
          "CA": { "by_city": {...} },
          ...
        }
      }
    },
    "q1": { ... },  "q2": { ... },  // historical period strips
    ...
  }
}
```

### Acceptance for Bug B

- [ ] `views.nna[period].geo.drill[state].by_city` populated for every state that has city-level NNA activity
- [ ] All three granularities (`monthly`, `quarterly`, `annually`) carry the drill
- [ ] All historical period strips (q1/q2/q3 for quarterly; m1..m12 for monthly) also carry the drill so the time-machine works in drilled mode
- [ ] Spot-check: sum of `by_city[city].total` ≈ corresponding state segment's `value` (city sums roll up to state, within rounding)
- [ ] States with no city splits (single-city, or city data missing) emit `by_city: {}` (empty object, not missing key — FE renders "No city data" cleanly)

---

## 4. Out of scope for this brief

- **FE-side bugs are being handled in parallel** — no DS work needed for:
  - Left-card NNA total in drill view not matching chart bars (`ContinuousNnaDivergingView` hero metrics; FE will derive from same source as chart)
  - ADV cohort toggle gating (FE layout config flip — `cohorts.adv: 'disabled'` → `enabled`)
- **AUA path is correct** — no changes to `views.aua[period].geo.*` or `views.aua[period].geo.drill[state].by_city`
- **Continuous-mode timeseries** — `cumulative_chart.json.geo_drill` is reportedly populated per DS~C's Distribution Tab brief close-out (`97796c0a` / `6967d27f`). If you find that's also missing, flag — it's a separate scope item.

---

## 5. Coordination notes

**Same-emitter fix.** Bug A (`segments[].value`) and Bug B (`drill[state].by_city`) are almost certainly both in the same INF_D_04 function or its caller. Fixing them together is one commit. DS~C shipped the AUA equivalents — review their pattern (`views.aua` paths) for the parallel structure.

**Critical for advisor-facing distribution view.** Inflection's Distribution tab is the firm-level view of where AUA is going / coming from. The state-level NNA donut at firm scope, plus the city-drill below it, are the two surfaces that explain "where did our growth come from." Currently both are broken (Bug A wrong magnitudes, Bug B no drill).

**ADV cohort note.** Andrew is asking us to surface the ADV (4-advisor) cohort in Distribution. Per DS~C's brief closure, all 4 INF advisors are already in `views.nna.current.adv.donut.segments`. FE just needs to flip a layout flag — but DS should keep that emission stable. If Bug A's `value` fix is needed in the ADV donut too (parallel structure to GEO donut), include it.

---

## 6. Acceptance summary

- [ ] Bug A: NNA donut segments populate `value` with state-level NNA flow (not AUA). Sum ≈ donut.total.
- [ ] Bug B: City-level NNA drill (`drill[state].by_city`) populates for every state with city-level activity. All granularities + period strips.
- [ ] Parallel ADV donut: same `value` field semantics (NNA, not AUA) on advisor segments — verify.
- [ ] No regressions on the AUA paths.

---

## 7. Open questions for DS

1. **Is the issue that `value` is null or that it's populated with AUA?** A quick `aws s3 cp s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json -` and inspecting `.views.nna.current.geo.donut.segments[0]` will resolve this in 30 seconds — fix is either "populate value" or "stop populating value with AUA."

2. **Was `views.nna[period].geo.drill.{state}.by_city[{city}]` ever in scope?** DS~C's Distribution Tab brief closure mentioned cities[] for AUA but didn't explicitly call out the NNA drill path. May have been overlooked. Either way, it's needed now.

3. **Routing** — DS~C handled the original Distribution Tab brief and shipped most of it. Andrew has asked me to route this follow-up to DS~D specifically. If you (DS~D) want to coordinate with DS~C on the INF_D_04 changes (to avoid stepping on each other), please loop them in — they have context.

---

*Drafted by 0.4.2_RD_AdvisorIntelligence · 2026-05-12*
*Source observations: 5 screenshots Andrew shared at 16:16-16:17Z — Continuous/GEO/NNA drilled to Washington (quarterly + monthly), Snapshot/GEO/NNA firm donut, Snapshot/GEO/NNA Washington selected, Snapshot/GEO/NNA Washington city-drill empty.*
*Companion FE work (parallel commits): left-card NNA total fix in ContinuousNnaDivergingView, ADV cohort layout flag flip in `_partners/inflection/layout.ts`.*
