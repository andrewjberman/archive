# Task Order: ADVI_SEGFE — advisor-drill ADV-AUM toggle: dead-controls + missing stacked-timeseries data

**Lane:** DE/RD portal + DS data (mixed — see options); 0.4.0_DE_ClientPlatform + 0.4.2_RD_AdvisorIntelligence + DS
**Priority:** P2 — 1 of Andrew's 5 Segment Analytics bugs (the non-pure-data one)
**Status:** complete -- SCOPE-CORRECTED 2026-06-12 (DE verify-before-fix 223359Z) — **product decision GATED on Andrew** (he is engaged with DE directly) -- SPRING-CLEAN 2026-08-25: ORPHAN, project code "ADVI_SEGFE" unregistered and unreferenced.

---

## SCOPE CORRECTION (supersedes the original pure-FE framing)

The original TO scoped this as "FE control-state, NOT a data gap, ADV-AUM data present." **That premise was wrong** — it rested on DE's earlier incomplete diagnosis (which COO propagated). DE's deeper line-verified check (DistributionTab.tsx) found the real asymmetry:

- **ADV-NNA drilled** reads canonical `activeAdvisor.series[granularity]` (:1496) + `activeAdvisor.windows[]` (:1537) → interval/window WORK (weekly/monthly/quarterly + 1Y/3Y/MAX all present).
- **ADV-AUM drilled** reads ONLY `relationship_stacked_periods` (:1916, :2002) — in live S3 that is **2 quarters, quarterly** (Q1'26, Q2'26), NO granularity/window dimension. There's even a "Relationship-level timeseries coming soon — placeholder + static" comment (:1896). The richer `getPlatinumAdvisorTimeseries` is NOT imported (0 refs).

**Consequence:** "restore interval+window propagation to parity" is a **NO-OP** — there is no monthly/annual/multi-year stacked-relationship data to switch to. The data gap is the real cause (same class as T1b). Threading the toggles changes nothing the user sees.

## Three options (product decision = Andrew's; he is weighing in with DE directly)

- **(a) DATA (DS):** emit `relationship_stacked_periods` at monthly/quarterly/annual + full window (the "coming soon" backend) → the existing toggles light up. Likely FOLDS with ADVI_49NNAFIX (same advisor canonical family) or a sibling.
- **(b) FE re-point (RD viz):** drilled ADV-AUM uses the advisor TOTAL-AUM timeseries (`advisors/{id}/timeseries.json`, 74 monthly pts + full window) → gains interval/window but LOSES per-relationship stacking. A product/viz change.
- **(c) FE quick-win (pure portal, no data, NO-REGRET INTERIM):** grey/disable the Interval+Window toggles in the ADV-AUM-drilled view until the data exists (precedent: Window already greyed in Snapshot mode, :1086). Stops the misleading dead controls. DE can do this NOW.

## Routing / gating
- **(c) is the no-regret interim** DE can execute immediately IF Andrew wants the stopgap (dead-control removal) while the real feature is decided. Pure-FE, schema-check clean, normal promote.
- **(a) vs (b) is a PRODUCT decision** — stacked-relationship truth vs total-advisor-AUM convenience. **Andrew owns it** (already engaged with DE). If (a): DS data work, folds with ADVI_49NNAFIX. If (b): RD viz work.
- **DE is HOLDING implementation until the scope settles** (correct — verify-before-fix).

## RAVC2 to COO
Per whichever option Andrew selects. If (c) lands as interim: the disabled-controls diff + DEV smoke. CC CTO + RD + (if data) DS.

---

*Authored 2228Z, SCOPE-CORRECTED 2234Z by 2.0.0_SA_COO — DE's verify-before-fix (223359Z) caught the wrong pure-FE premise. The premise error was COO's (propagated DE's earlier incomplete diagnosis); corrected here. Product call routed to Andrew (already engaged).*
