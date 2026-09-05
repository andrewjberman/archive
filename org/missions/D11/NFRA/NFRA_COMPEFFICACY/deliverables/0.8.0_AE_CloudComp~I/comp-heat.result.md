# comp-heat — NFRA_COMPEFFICACY T20 result

**Measured by:** `0.8.0_AE_CloudComp~I` · **Production change:** `a4b426e7ed` · **System refresh:** `5d14443dff` · **Push:** LOCAL only (issuer ruling 93774; no push).

## 4.1 Identity

`.tools/comp-heat` is the 400-line CLI shim/engine boundary. It has five executable subcommands (`freshness`, `drift`, `score`, `federated`, `compare`); its `main()` is invoked under `__main__`. `comp-similar.load_heat_live()` remains a read-only consumer and invokes `comp-heat freshness --json` as a subprocess; neither it nor estate-report wiring changed.

## 4.2 Disclosure

The ruled two-line library driver returned `RETURN type=dict entries=0 empty=True` before the change. The CLI now emits a ratified `ANSWER-STATE:` token in text mode and `answer_state` plus `vintage.measured_at_utc` in JSON mode. `python .tools/comp-heat --help` lists all five subcommands.

## 4.3 Answer states — CLI and JSON grain

| State | planted CLI case | rc | evidence |
|---|---|---:|---|
| `SUBJECT_ABSENT_FROM_CORPUS` | `freshness __T20_ABSENT_HEAT__ --json` | 2 | absent repo-relative subject; JSON state + vintage |
| `PRESENT_WITH_ZERO_RESULTS` | `freshness .git --json` | 0 | existing subject with zero scored files |
| `PARTIAL_OR_BLIND` | `COMP_HEATMAP_DIR=__T20_MISSING_HEATMAP__ freshness --json` | 3 | unavailable heat source; never an empty result |
| `NOT_APPLICABLE` | `compare .tools/comp-heat .tools/comp-heat --json` | 1 | one resource cannot form a two-resource comparison |

Each case is also asserted in human mode by exactly one `ANSWER-STATE:` token. JSON preserves existing keys and adds only `answer_state` and `vintage`; partial JSON never serializes as `{}`.

## 4.4 Rule T

Non-application: the heat engine derives one complete git-history snapshot before the CLI renders it; it has no corpus-width CLI sweep, `--budget`, or resumable cursor. The unavailable-source partial branch is execution-only and returns rc 3, never a clean rc 0.

## 4.5 Boundary and consumers

`org/modules/graph/debtscan/comp_similar.py:275-300` is named, measured, and unchanged. The daily-report wiring is recorded as `@09355b6d93` and unchanged. T20 has no historical CLI-run sink row (denominator: the exact `comp-heat` CLI run census specified at cut); this audit's four controls are explicitly test exercises, not evidence of historical adoption.

## 4.6 Battery

New `.tools/tests/test_comp_heat_battery.py`: direct `2 tests` passed; pytest `2 passed, 8 subtests passed`. Four production arms prove text+JSON state/rc/vintage. Four temporary source mutants, one per ratified state, each make its paired predicate red; each mutant is removed in `finally`.

## Findings

`NFRA_COMPEFFICACY-S29 @696fa4c6be` remains the consumer-boundary record. COO ruling 93774 resolves T20's grading boundary to comp-heat itself; consumer adoption remains CE-t-12 work and was not edited here.

## Independent FWD-9

COO completed the required distinct-seat exercise in Message 93785 at `f1dce36b9b`: a real `comp_similar.load_heat_live(timeout=120)` call returned `dict` with `[]` top-level keys, rc 0, in 0.0 s. Its opt-in/best-effort consumer path therefore returned before reaching comp-heat. This is independent evidence for the ruled CLI/engine grading boundary and confirms S29; it is not a consumer adoption claim. Push remains LOCAL only.
