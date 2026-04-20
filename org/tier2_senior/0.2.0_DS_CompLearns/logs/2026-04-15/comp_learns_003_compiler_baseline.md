# COMP_LEARNS.003 session log — compiler_baseline + extractor_interface

**Agent:** 0.4.0_DS_ClientPlatform~B
**Date:** 2026-04-15
**TO:** `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/COMP_LEARNS.003.ds-b-compiler-baseline.md`
**Project:** COMP_LEARNS (PRD #3 of 5)

## Scope

Shipped the single-file compiler scaffold (`comp/framework/compiler_baseline.py`) and
Extractor Protocol (`comp/framework/extractor_interface.py`) that every per-target
`compiler.py` copies as its starting point. Honest-empty stubs on every extractor
method; CLI dispatcher covers all 4 `compiler_contract.SUBCOMMANDS` (answer,
list-surfaces, list-edges, rebuild). Docstring tells the next agent "COPY THIS FILE."

## Timeline

- 19:15Z — Session start, registered ~B, inbox check.
- 19:18Z — TO read; status was `staged`. PRD #1 dependency surface not present yet.
- 19:18–19:22Z — Phase 1 pre-flight: drafted `compiler_baseline.py` + `extractor_interface.py` +
  test file against TO's wire_contract, uncommitted. 9/9 initial tests PASS against TO-contract.
- 19:22Z — ACK to COO stating draft-ready, gated on ~A ship, asking commit posture guidance.
- 19:24Z — COO replied: HOLD; when ~A ships, single atomic commit w/ wiring assertions.
- 19:25Z — CTO flipped TO #003 -> `pending` (~A shipped PRD #1, commit 43e3225e).
- 20:10Z — Andrew nudged "check your TOs"; discovered #003 pending + new #007 staged.
- 20:12Z — Read ~A's shipped `compiler_contract.py` + `harness_base.py` + `query_schema.py`.
  Found CLI shape discrepancy between my TO wire_contract and ~A's shipped contract
  (4 subcommands not 3; no `--repo` flag; no `confidence` field; list-* returns array not object).
- 20:15Z — ACCEPTANCE FLEX PRE-FLAG fired to CTO explaining reconciliation direction
  (match ~A's shipped CLI because harness_base IS the interlock consumer).
- 20:15–20:30Z — Rewrote baseline to match ~A's contract; expanded test file with
  acceptance #3 dispatcher smoke (all 4 subs via `compiler_contract.invoke`) and
  acceptance #4 `run_harness` 10-stub harness check. Line count 139 (within 120-180).
  All 9 tests PASS, 7.05s.

## Acceptance flex (Rule 7, pre-flagged to CTO 20:15Z)

**What:** Deviated from TO wire_contract to match ~A's shipped `compiler_contract.SUBCOMMANDS` shape.
**Why:** `harness_base.run_harness` subprocesses the baseline exactly per ~A's contract
(`python <compiler> answer "<q>"` with no `--repo`, reads `parsed["answer"]` +
`parsed["latency_ms"]`). Baseline must be executable by the real harness on day one —
that's the whole "copy-and-iterate" model. Mismatched baseline would teach the wrong CLI.

**Original vs substituted:**
| Contract point | TO wire_contract | ~A's shipped | Resolution |
|---|---|---|---|
| Subcommands | 3 (answer, list-surfaces, list-edges) | 4 (+ rebuild) | Added rebuild returning `{"ok": true, "seconds": 0.0}` |
| `--repo` flag | required arg | not present | Removed; baseline uses `Path.cwd()` |
| answer output | `{answer, confidence, latency_ms}` | `{answer, latency_ms}` | Dropped `confidence` |
| list-surfaces output | `{"surfaces": [...]}` | `[{"name","count"}, ...]` | Array of `{name,count}` dicts |
| list-edges output | `{"edges": [...]}` | `[{"edge_type","count"}, ...]` | Array of `{edge_type,count}` dicts |
| `--filter` on list-edges | supported | not in contract | Removed (filter lives in `Extractor.edges()` Python API, not CLI) |

No CTO redline received within 60s window; proceeding per Rule 7.

## Code changes

- NEW `comp/framework/compiler_baseline.py` (139 lines, copy-template docstring at L3).
- NEW `comp/framework/extractor_interface.py` (45 lines; `@runtime_checkable` Protocol
  with `surfaces() / edges(filter) / answer(question)`).
- NEW `comp/framework/tests/test_compiler_baseline.py` (9 test cases).

## Compiler Tools

| Phase | `<run>` | Observed | Pass/fail vs `<expect>` |
|---|---|---|---|
| 1 | `cat /tmp/autoresearch_inspect/autoresearch-master/train.py \| head -100` | Confirms single-file scaffold: module constants at top, dataclass config, classes, then main loop. Baseline mirrors: imports + top-level config constants -> Extractor class -> `_cmd_*` dispatcher -> `main()`. | **PASS** — single-file pattern matched. |
| 1 | `ls comp/framework/ \| grep -E "compiler_contract\|harness_base"` | Both present (~A ship commit 43e3225e). | **PASS** — dependency cleared. |
| 2 | `wc -l comp/framework/compiler_baseline.py` | 139 | **PASS** — within 120-180 target. |
| 2 | `python compiler_baseline.py answer "test?" \| python -c "json.loads"` | `{'answer': None, 'latency_ms': 8}`; schema keys `{answer, latency_ms}` assert OK. | **PASS** — schema-stable per ~A contract. |
| 2 | `python -m pytest comp/framework/tests/test_compiler_baseline.py -v` | 9 passed in 7.05s. | **PASS** — incl. acceptance #3 dispatcher smoke + #4 run_harness-honest-zero. |
| 3 | `grep -n "COPY THIS FILE" compiler_baseline.py` | Hit at L3 in module docstring. | **PASS** — copy-template breadcrumb present. |

## Acceptance checklist

| # | Criterion | Status |
|---|---|---|
| 1 | compiler_baseline.py <=180 lines; 3+ subcommands; JSON schema-stable | PASS (139 lines; 4 subs per reconciled contract) |
| 2 | extractor_interface.py defines `Extractor` Protocol | PASS (`@runtime_checkable`) |
| 3 | Smoke via `compiler_contract` dispatcher: all commands parse + JSON no crash | PASS (4/4 SUBCOMMANDS via `cc.invoke`) |
| 4 | `run_harness(baseline, stub_queries, None)` -> pass_rate=0, coverage=0, latency>0 on >=10 stubs | PASS (queries_run=10, all FAIL status, mean_latency_ms>0) |
| 5 | tests >=5 cases; pytest green | PASS (9 cases, 9/9 green, 7.05s) |
| 6 | Copy-template docstring breadcrumb | PASS (L3) |
| 7 | Session log Compiler Tools triad | THIS DOC |
| 8 | MCP COMPLETE to COO with commit hash + line count + smoke-test JSON | PENDING SEND |

## Handoff

TO #003 ready for COMPLETE signal. COMP_LEARNS.007 (~B status CLI) is the
natural next queue item — currently staged on #003 close and will flip
pending once this lands.

No downstream effects from this ship: baseline is a free-standing copy
template; concrete target compilers (PRD #2 httpx) copy it and diverge.
No other agent's working tree is touched.
