# MDPF Generation Contracts — Bound-Law Preamble + Anchor Derivation Rule

**Status:** PREAMBLE ONLY — the per-artifact contracts (DDB rows → each served JSON) are written
against DE's read-surface enumeration (component → key → consumed fields), which is pending
(CTO 161749Z dispatch). This document pre-stages the DE-independent half so contract-writing
starts the moment the enumeration lands. Nothing here builds a generator (ownership ruling
comes after the contracts exist — do not pre-build).

**Program target (Andrew-direct, CTO 161749Z bound):** once the gold DDB carries canonical full
history (0.7.0's re-sourced emitter + full-lookback walk), a server-side process generates ALL
`/portfolios` JSONs from the TABLE daily — aum-metrics, account-distribution,
aggregate-aua-timeseries (Global/49F/INF/COT splits), AUA-tab period-end features. The staged-
artifact path of 2026-07-23 is the bridge, not the destination.

## The carried-law checklist (every per-artifact contract MUST cite each item or state N/A)

| # | Law | Source |
|---|-----|--------|
| 1 | **D1 absolute reality** — every value = the source's retrospective TRUE daily value; legacy as-known-then = audit ledger, never display | CTO 160900Z (Andrew verbatim) |
| 2 | **T1_SETTLED frontier** — the emitted frontier is the settled T-1 value; never restates | CTO 161749Z carried-law list |
| 3 | **Honest-absent / YANG_SITTW** — unreached dates absent, never fabricated or silently carried | standing |
| 4 | **LABELED_PARTIAL in table vs all-present at serve** — table rows carry `legs_present`; the generation step shapes the served artifact to its all-present-or-all-absent law | Andrew via COO 162601Z; amendment 162649Z |
| 5 | **count_coverage_end interval shape** — counts honest-None inside the DECLARED lag window | CTO 142711Z ruling (b) |
| 6 | **SMA enumerated count-preserve rides ALONGSIDE #5** — opal_growth_sma/opal_div_sma carry-forward with in-band `count_as_of`; two declared count shapes, both meta-named | CTO 161841Z confirm |
| 7 | **Per-channel basis labels** — 49F C2 (`net_mv_plus_cash`), cottonwood two-source verbatim (`bd-rebalancer-models + bd-datamining-values`), INF orion/eclipse | recorded spec doc |
| 8 | **Suppression denominators in meta** — every suppressed/estimated cohort states its denominator | NB-1 precedent |
| 9 | **Trading-day frontier per NEVER#1** — all period math on the trading calendar, never wall-clock | CLAUDE.md NEVER#1 |
| 10 | **Structural-zero vs honest-absent** — pre-launch legs (eclipse pre-2026-05-15) are labeled known-zero, distinct from unknown | launch-seam precedent; depth confirm 161643Z |

## Period-end anchor rule: FROZEN-WITH-CITED-DERIVATION (CTO 161841Z refinement)

Contracts enumerate anchor DATES explicitly (calendar-explicit — no formulas referencing a
library the generator's runtime may not ship), **and** name the derivation beside them so a
future reader re-derives and verifies against the one canonical calendar instead of trusting
frozen dates blindly. Required meta shape per artifact:

```json
"period_end_anchors": {
  "derived_from": "lib/trading_calendar @ <commit> at contract-emit time",
  "calendar_source": "<calendar_source() output at emit>",
  "frontier_basis": "T1_SETTLED",
  "anchors": { "...": "enumerated dates" }
}
```

**Worked example (emitted 2026-07-23, `lib/trading_calendar` @47b9992c2,
`calendar_source()` = `NYSE/hardcoded-fallback-2024-2027`, T1_SETTLED frontier = 2026-07-22):**

- MTD window: 2026-07-01 .. 2026-07-22 (15 trading days)
- QTD window: 2026-07-01 .. 2026-07-22 (15 — Q3 start coincides with month start)
- YTD window: 2026-01-02 .. 2026-07-22 (138 trading days)
- Prior quarter-end close anchors (q0..q3): 2026-06-30, 2026-03-31, 2025-12-31, 2025-09-30
  (each = `prev_trading_day(quarter_start)` — matches the radial's q-grid)

Derivation calls, re-runnable: `trading_days_mtd(settled)`, `trading_days_ytd(settled)`,
`trading_days_between(quarter_start, settled)`, `prev_trading_day(quarter_start)`.

**Calendar-shipping note (flagged to CTO 161818Z):** `lib/trading_calendar` is repo-side. If the
generator lands as a Lambda, the calendar ships with it (Layer per Deployment Rule 3) or anchors
arrive pre-enumerated in the contract artifact — never recomputed in two places from two
calendars. The contracts stay calendar-explicit precisely so the ownership ruling stays free.

## Per-artifact contract skeleton (filled per artifact once DE's enumeration lands)

1. **Served key + consumer** — from DE's enumeration (component → key → consumed fields).
2. **DDB row inputs** — cohort_id + fields consumed, per channel.
3. **Derivation** — row math, exact recipe (rounding stated), one-derivation rule (from table
   rows only, never a parallel silver read).
4. **Axis + frontier** — trading-day axis, T1_SETTLED, count_coverage_end declaration.
5. **Labels carried** — legs_present / point_class / basis / count shapes (#4–#7 above).
6. **Period-end anchors** — frozen-with-cited-derivation block (rule above), if the artifact
   carries period features; else N/A stated.
7. **Controls** — tie values to the current staged/served artifact at cutover (the bridge
   artifacts are the byte-controls for the generator's first emit), positive control named.
