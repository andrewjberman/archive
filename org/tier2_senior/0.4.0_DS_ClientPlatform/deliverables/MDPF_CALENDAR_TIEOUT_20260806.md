# MDPF calendar tie-out — `lib/trading_calendar` vs the mdpf-local shim

**TO:** `MDPF_CANRTE.P0-4` @ebaf5700a criterion 6 · **CTO~Z ruling condition 1** (20260806T204126Z)
**Author:** `0.4.0_DS_ClientPlatform~Z` · **Date:** 2026-08-06 · **Baseline:** SITEZ `73ca92eb3`
**Status:** DISCHARGED — validated and closed by CTO~Z (RAVC 4, arithmetic independently re-derived)

## 0. What was ruled, and what this discharges

CTO~Z ruled: **bind `lib/trading_calendar.py` via the WS-1 shared Lambda Layer; retire
`data/mdpf/scripts/gold/_trading_day_calendar.py` and both inlined privates at
`dim_mdpf_aggregate_aua_timeseries.py:154,164`.**

Condition 1: the in-window no-op claim is a **hypothesis until run**, and a tie without a positive
falsifier is not evidence. This document is that run.

## 1. The control that had to come first

**On any machine with `pandas_market_calendars` importable, both modules defer to pmc and agree for a
reason that has nothing to do with the holiday sets the ruling turns on.** The naive version of this
test structurally cannot fail in that state.

So the harness prints the runtime state before testing and then **forces `_USE_PMC = False` on both**,
comparing the fallback paths directly.

Measured runtime state on site Z, on a clean import — **before** forcing:

```
lib  _USE_PMC = False   calendar_source() = 'NYSE/hardcoded-fallback-2024-2027'
shim _USE_PMC = False   calendar_source() = 'NYSE/hardcoded-fallback-2024-2026'
```

`pandas_market_calendars` **is not importable on site Z.** The fallback was already live. This is an
independent measurement of the §4 dependency finding: a real environment where nobody installed it.

## 2. TEST 1 — in-window equality (the no-op claim)

Range 2024-01-01 .. 2026-12-31, day by day, `is_trading_day` on both.

| | |
|---|---:|
| **DENOMINATOR — dates compared** | **1096** |
| disagreements | **0** |
| lib in-window holiday entries | 31 |
| shim in-window holiday entries | 31 |
| `lib − shim` | `[]` |
| `shim − lib` | `[]` |
| `2025-01-09` (Carter mourning) in both | True |
| `2026-07-03` (Jul-4 observed) in both | True |
| lib total entries, all years | 41 |
| shim total entries, all years | 31 |

**VERDICT: the in-window swap is a no-op.** The 41−31 = 10 delta is exactly 2027 (§4).

## 3. TEST 2 — positive falsifier

Removed `2026-07-03` from the shim's set; re-ran the identical 1096-date sweep.

```
disagreements: 1  ->  [('2026-07-03', False, True)]
```

**FIRED and LOCALIZED to the mutated date.** TEST 1's tie is therefore a result, not a tautology.

## 4. TEST 3 — 2027, measured

Range 2027-01-01 .. 2027-12-31. **DENOMINATOR: 365 dates. Disagreements: 10** — every 2027 NYSE
holiday, shim `True` / lib `False`:

```
2027-01-01  2027-01-18  2027-02-15  2027-03-26  2027-05-31
2027-06-18  2027-07-05  2027-09-06  2027-11-25  2027-12-24
```

CTO~Z independently re-derived all ten against observance rules before accepting: Jun 19 2027 falls
Saturday → observed Fri 06-18; Jul 4 falls Sunday → observed Mon 07-05; Dec 25 falls Saturday →
observed Fri 12-24; Good Friday 03-26 against Easter 03-28.

**This claim was originally source-derived. It is now MEASURED.**

**Mechanism.** Fallback `is_trading_day` is `iso not in _NYSE_HOLIDAYS_FALLBACK` over a set ending
2026-12-31. From 2027-01-01 **every weekday reads as a trading day** — New Year's Day, MLK, Good
Friday — silently: no raise, no warn, wrong frontier, wrong `trading_days_behind`, on a pipeline
whose entire acceptance basis is per-feed trading-day frontiers. **Under five months of runway.**

## 5. Why the dependency fails GREEN

`_trading_day_calendar.py:37-43` imports pmc under `try/except ImportError`. **Absence does not
raise.** Doc 02's prescribed remedy — *"run an import-health invocation from the built Linux artifact
before apply"* — **passes with the package missing.**

That is not a weak control. It is an **anti-control**: it reports healthy *because* the fallback
engaged. Same anti-correlated shape as the orphan-watcher `REACHABLE` verdict.

The package is absent from `requirements.txt`, has zero repo hits under its hyphenated pip name, and
is guaranteed today **only** by `mdpf-daily-dispatch.sh:183-189` and `user-data.sh:49` — inside the
artifacts teardown removes. The **`<5` pin is load-bearing** (`dispatch.sh:175`: 5.x changed the API)
and exists only as a bash comment in a file being deleted. Andrew's disposition bucket: **PORTED and
hash-tied**, never "demonstrated unnecessary."

## 6. The assertion that replaces the import-health check (criterion 7)

```
calendar_source() == "NYSE/pandas_market_calendars"
```

Per calendar-touching artifact, **at build time AND in acceptance**, and per CTO~Z it **replaces**
doc 02's import-health check rather than supplementing it.

**This is an ASSERTION inside existing scope. It is NOT an alarm, monitor, notification, or freshness
checker, and must not be written as one** — the standing moratorium binds regardless of how useful a
detector would feel here.

CTO~Z condition 3 keeps the build-time assertion **standalone**, decoupled from the artifact
comparison, so that no later stripping decision can disarm it.

## 7. Rulings on the QA-backend asymmetry (CTO~Z, 20260806T204317Z)

Both halves, and the second is load-bearing.

1. **Install `pandas_market_calendars<5` in any environment producing a QA-comparison artifact.**
   Reason is stronger than backend-matching: production will carry pmc via the layer, so a QA build
   on the fallback **validates a configuration that will never ship**.
2. **`trading_day_calendar` goes on an explicit NEVER-STRIP list in the comparison spec** — named in
   the spec, not remembered by whoever runs it. **The collision is structural:** the one field that
   discriminates the two runtimes is, by name and by shape, a *provenance* field — exactly the
   category doc 02 instructs the operator to strip. An executor following doc 02 exactly deletes the
   oracle and reports a clean tie. No rename (H6 binds).
3. **This forced-fallback test stays PINNED with `_USE_PMC = False`.** Once pmc is in the layer, the
   naive comparison passes trivially everywhere and the 2027 divergence goes invisible again on a
   horizon that has not moved. A passing assertion never made to fail has not been tested.

## 8. Scope bound

The ruling covers the MDPF port. Vendored `trading_calendar.py` copies under `bd-served-vintage-alarm`,
`inf-etf-ownership-daily`, `opal-assets-absence-check` are **other pipelines — not touched, not bound,
not swept.** WS-1's scope. *A ruling that dissolves a workaround is not a licence to sweep the estate.*

**One row routed, not adjudicated:** `build_cottonwood_mdpf_slice.py:87-93` imports the shim under
try/except via a relative hop into the MDPF tree and computes `trading_days_behind_settled_frontier`
at `:801`. It is **inside** MDPF's port scope and is **not** one of the three bounded-out pipelines.
Whether the binding covers the Cottonwood producer family is CTO~Z's call; asked to be **stated
rather than inferred**, because the failure mode is the port retiring the shim while a producer inside
the same port still imports it — across a tree boundary, under a `try/except` that will not raise.

## 9. Reproduction

Harness: `scratchpad/calendar_tieout.py` (lands as a committed test artifact with P1-1).
It prints runtime state, forces fallback on both modules, sweeps day-by-day with the denominator,
mutates, and re-sweeps. Run it before trusting any later claim that the two calendars agree.
