# comp-pulse — T18 s.4 audit

**TO:** `NFRA_COMPEFFICACY.TO-CE-T-18` · **Cell:** `CE-t-18` · **Engine:** `org/modules/graph/comp_pulse.py` · **Read vintage:** `6e5d443ad3` / PRD v0.5 `5bbdab5ec7` · **Audit date:** 2026-09-03

## 4.1 Identity

| Field | Evidence |
|---|---|
| tool / shim | `comp-pulse`; `.tools/comp-pulse` (9 lines) |
| engine | `org/modules/graph/comp_pulse.py` (783 lines after this work; 707 at cut) |
| aliases | none measured |
| purpose_1line | **The pre-commit risk reflex; 8,359 of 8,364 cut-time runs were the hook's `diff`.** It scores a proposed file set against the danger map before commit. |
| self-identifies | `--help` declares `comp-pulse`, its `diff` reflex mode, `--budget`, and `--cursor`; the wrapper resolves directly to the engine. |

The object is the engine, not the shim. The wrapper’s only post-engine act is `comp_log_auto.py`, an append-only telemetry write. `comp-passcraft recon comp-pulse` missed that write surface; this is recorded as `NFRA_COMPEFFICACY-S25`.

## 4.2 Disclosure

Quoted production-wrapper `diff` run after the change:

```text
comp-pulse diff -- THE PRE-COMMIT RISK REFLEX (NFRA_NERVES L5)
  INVOCATION ... diff org/modules/graph/comp_pulse.py
  danger map: 8.3h old
  DENOMINATOR: 1 file(s) checked against 1906 danger node(s)
  ANSWER STATE: PRESENT_WITH_ZERO_RESULTS
  REFLEX CLEAN -- a MEASURED result (map read, every file checked), not a default.
  WITHIN BUDGET: scanned 1 of 1 file(s); budget: 90 s (default) ...
```

The default `pulse` output names every source and vintage, declares absent sources as `UNKNOWN-VINTAGE`, prints its window, and now prints Rule-T completion or prefix form for its telemetry scan. Its declared blind spots remain: coldness belongs to `comp-debris`; system-grain signals remain an explicit unknown band. Pagination is non-applicable: no output row cap hides a result. The corpus-width work is instead resumable by Rule-T cursor.

## 4.3 Answer state — four planted controls

| Ratified state | Planted invocation / control | rc | Tool voice |
|---|---|---:|---|
| `SUBJECT_ABSENT_FROM_CORPUS` | `diff <temporary nonexistent path>` | 2 | `ANSWER STATE: SUBJECT_ABSENT_FROM_CORPUS` |
| `PRESENT_WITH_ZERO_RESULTS` | `diff <temporary existing safe path>` | 0 | `ANSWER STATE: PRESENT_WITH_ZERO_RESULTS` and `REFLEX CLEAN -- a MEASURED result` |
| `PARTIAL_OR_BLIND` | real production binary with `nerves-risk-edges.json` moved aside and restored in `finally` | 2 | `ANSWER STATE: PARTIAL_OR_BLIND`; `NOT-DECIDABLE`; never `REFLEX CLEAN` |
| `NOT_APPLICABLE` | `diff --no-population` (explicitly no file population; never reads another seat's staged index) | 0 | `ANSWER STATE: NOT_APPLICABLE` |

The external battery exercises all four on the production engine and supplies a running mutant for each assertion. This closes the prior dangerous shape: absent or stale danger maps are query-only partial/blind states, never auto-rebuilt and never read clean.

## 4.4 Bounds — Rule T

`--help` now exposes `--budget <seconds>` and `--cursor <last-unit>`. The carrier is `.tools/_compbudget.py`: flag > `COMP_BUDGET_S` > documented 90-second default; `--budget 0` is unbounded. The default `pulse --days` scan uses one deterministic telemetry-row cursor across the rail and `runs.jsonl`; a tiny real budget prints:

```text
ANSWER STATE: PARTIAL_OR_BLIND
NOT-DECIDABLE: telemetry scan reached its budget
BUDGET REACHED: ... scanned n of N telemetry row(s); results are a PREFIX, not the answer; resume: comp-pulse --cursor n
```

The normal completion prints `WITHIN BUDGET: scanned N of N telemetry row(s); budget: ...`. `diff` is verdict-bearing: budget expiry returns rc 2—distinct from rc 0 clean and rc 1 danger—and prints `NOT-DECIDABLE` plus the same reached/cursor form. A stale or unreadable map follows that same non-clean branch. On a small complete file set, `diff` prints the within-budget form; the safe-commit reflex invokes it but pipes it through `|| true`, so it displays a non-clean result without blocking the commit. `safe-commit.sh` was read and not edited.

## 4.5 Passcraft

`comp-passcraft recon comp-pulse` confirmed the shim/engine pair. The hand-run controls were: real existing safe subject, nonexistent subject, temporarily absent real map, no-population mode, and tiny-budget prefix; their false twins are the per-arm production mutants. The mutation files ran beside the engine, were removed, and a crash is explicitly a failed arm. Archetype: verdict-bearing pre-commit risk reflex. Lead shapes exercised: guard asymmetry (absent map and absent subject), success-token-bound-to-wrong-step (clean only after a map read), and correct-but-unwired (safe-commit prints but ignores the non-zero reflex rc). The wrapper telemetry omission in passcraft’s write-surface report is S25, not silently accepted.

## 4.6 Usage, battery, overlap, disposition

- **Runs instrument:** `org/mcp/comp-tool-runs.jsonl` re-measured after T-1’s `f34122edfb` wiring (2026-09-02 13:17:51-04:00): 12,778 total `comp-pulse` records; 12,763 `diff`, 15 by-hand. Post-wiring window: 457 records, 456 `diff`, 1 by-hand. The cut-time census remains 8,364 total / 8,359 hook `diff` / 5 by-hand and is dated rather than substituted.
- **Rail instrument:** 1,468 `comp-pulse` references in `comp-which-rail.log`; these are routing-intent mentions, not an invocation census and therefore are not added to the run denominator.
- **Hook driven:** current run-sink proxy is 12,763/12,778 `diff` = 99.88%; the sink has no explicit caller field, so this is mode evidence, not a claim that every diff came from the hook.
- **Battery:** `.tools/tests/test_comp_pulse_battery.py`: direct 12/12 PASS; file-grain pytest 1/1 PASS; collection sees 1 test. Directory collection reached 49 tests including this battery then failed from the pre-existing module-scope `SystemExit` in `test_fabric_check_classify.py`; this is reported as shared-test interference, not a pass.
- **Overlap:** no second engine provides this danger-map-before-commit reflex. `comp-debris` owns coldness; `comp-pulse` does not duplicate it.
- **Proposed:** CLEARED-candidate for this audited behavior. S25 is an inert observation for the `comp-passcraft` owner; it does not invalidate the engine controls.

## Acceptance evidence

| Criterion | Evidence |
|---|---|
| T18-AC1 | This file states the hook purpose first, measured ratio, resolved engine and all s.4 sections. |
| T18-AC2 | Four distinct tokens exercised; absent-map real-binary control rc 2 / never clean. |
| T18-AC3 | Cut census and current post-wiring census stated with denominators and time boundary. |
| T18-AC4 | Shared carrier in help; real budget prefix; verdict-bearing `diff` rc 2; read-only consumer behavior stated. |
| T18-AC5 | New 12-arm battery, 12/12 direct, 1/1 file pytest, every paired mutant fires. |
| T18-AC6 | Proof instance accompanies this report and resolves S25 before any complete flip; push/independent-seat evidence remains pending after the implementation commit. |
