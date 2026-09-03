# comp-drift — NFRA_COMPEFFICACY T-14 result (PRD v0.5 s.4)

Schema: `NFRA_COMPEFFICACY_PRD` v0.5 @`5bbdab5ec7`, s.4.  Row: T-14.  Cell:
CE-t-14 (decomp v0.2.4 @`39515415cc`).  Measured by
`0.8.0_AE_CloudComp~G`, 2026-09-03, after GO Msg-ID 93706.  The production
engine was at blob `2392e85d5d781c7354c0a1160b1f008a83461cff` before commit.
No spec-vs-world surprise row was required by this audit.

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.5 s.4",
  "row": "T-14",
  "cell": "CE-t-14",
  "measured_by": "0.8.0_AE_CloudComp~G",
  "measured_at_utc": "2026-09-03",
  "read_vintage": "HEAD @273b4f9c202cb4cf899b8d5b20e8583f8bc7c015",
  "surprises": [],
  "identity": {
    "tool": "comp-drift",
    "shim_path": ".tools/comp-drift (15-line forwarding shim)",
    "engine_path": "org/modules/graph/drift_cli.py (orchestrator; calls seam engines, never re-implements them)",
    "topology_path": "org/modules/graph/drift-topology.yaml (READ-only SSOT)",
    "engine_vintage_before": "blob 2392e85d5d781c7354c0a1160b1f008a83461cff",
    "seam_denominator": "13 topology bindings: seam-1 (1), seam-2 (3), seam-3 (1), seam-4 (1), seam-5 (1), seam-6 (5), seam-7 (1); sweep adds infra-comp and infra-tf = 15 deterministic sweep units",
    "called_engines": [
      "comp-heat drift", "comp-pipescript deployed", "comp-lambdamap parity", "comp-iam reconcile",
      "comp-kuzu", "iceberg_parity.py", "trino_catalog_parity.py", "code_heat_parity.py",
      "tool_activity_parity.py", "comp-freshness", "drift_producer.py (folded infra legs)"
    ]
  },
  "disclosure": {
    "help": "`--budget N` discloses carrier precedence (--budget > env COMP_BUDGET_S > default 90s), --budget 0 unbounded, --cursor UNIT, and rc vocabulary 0 clean / 1 integrity-break / 2 unverifiable / 3 partial-budget.",
    "coverage_run": "`python org/modules/graph/drift_cli.py coverage` reads the topology ledger and prints COVERED=4, PARTIAL=2, SELF-HEAL=1; no GAP is present.",
    "plain_sweep_run": "`python org/modules/graph/drift_cli.py sweep --budget 0` measured 15/15 sweep_unit within an unbounded budget; seam-3 and seam-4 evaluated current, 11 expensive bindings cost-guarded, infra-comp WATCH and infra-tf COST-GUARDED; exit 2 because one seam was UNVERIFIABLE.",
    "deep_cost_guard": "`python org/modules/graph/drift_cli.py sweep --deep --budget 0.001` stopped before an engine, printed BUDGET REACHED scanned 0 of 15 and ANSWER-STATE PARTIAL_OR_BLIND, exit 3.",
    "denominator": "Every board row carries stage, verdict, coverage, and engine; the Rule-T line carries scanned/total sweep_unit and the cursor or NO CURSOR YET.",
    "vintage": "Engine outputs carry their own grounding; comp-drift does not invent a graph vintage. The measured run is identified by HEAD/blob above."
  },
  "answer_state": {
    "schema_note": "Exact spellings from org/standards/COMPTOOL_ANSWER_STATE.enum.json: SUBJECT_ABSENT_FROM_CORPUS, PRESENT_WITH_ZERO_RESULTS, PARTIAL_OR_BLIND, NOT_APPLICABLE.",
    "SUBJECT_ABSENT_FROM_CORPUS": {"planted": "comp-drift --self-test absent-subject fixture", "printed": "ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS", "rc": 0},
    "PRESENT_WITH_ZERO_RESULTS": {"planted": "comp-drift --self-test present-zero fixture", "printed": "ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS", "rc": 0},
    "PARTIAL_OR_BLIND": {"planted": "sweep --deep --budget 0.001", "printed": "ANSWER-STATE: PARTIAL_OR_BLIND; BUDGET REACHED: 0.001 s (flag); scanned 0 of 15 sweep_unit(s); ... NO CURSOR YET", "rc": 3, "engine_voice": "budget prefix is partial; no seam is asserted clean"},
    "NOT_APPLICABLE": {"planted": "comp-drift --self-test non-applicable fixture", "printed": "ANSWER-STATE: NOT_APPLICABLE", "rc": 0},
    "distinctness": "One `--self-test` invocation printed all four exact tokens and its control reported answer_state.four_distinct_tokens PASS. The first, second, and fourth are explicit orchestrator fixture controls because comp-drift's production subject is a topology walk, not a corpus-search lens; the budget cut is the live production PARTIAL_OR_BLIND path."
  },
  "rule_t": {
    "carrier": ".tools/_compbudget.py; resolve precedence is flag > COMP_BUDGET_S > default 90s",
    "expiry_rc": "EXIT_NOT_DECIDABLE=3, distinct from complete clean 0, integrity-break 1, and seam-unverifiable 2; --help names all four",
    "cut_capture": "`sweep --budget 0.001`: rc=3, scanned 4 of 15, BUDGET REACHED, resume cursor seam-2:iam, ANSWER-STATE PARTIAL_OR_BLIND",
    "resume_capture": "`sweep --budget 0 --cursor seam-2:iam`: rc=2 (true seam verdict), scanned 11 of 11 remaining units, WITHIN BUDGET; no partial state",
    "deep_capture": "`sweep --deep --budget 0.001`: rc=3, scanned 0 of 15, NO CURSOR YET; expensive live engines were not allowed to overrun the ceiling",
    "cursor": "Unit keys are deterministic seam-id:binding (for example seam-2:iam); the cursor is the last fully completed unit, and totals are measured after the cursor filter (11 remaining on the exercised resume)."
  },
  "overlap": {
    "recording": "BY NAME ONLY",
    "comp_drift": "walks propagation parity across drift-topology.yaml seams and calls existing seam engines",
    "comp_similar": "answers similarity/relatedness questions over its own corpus and joins; it is a parallel question and corpus",
    "boundary": "No comp-similar engine, corpus, edge, or scope was imported, merged, or re-scoped by T-14."
  },
  "battery": {
    "path": ".tools/tests/test_comp_drift_battery.py",
    "arms": 5,
    "direct": "5/5 PASS (`python .tools/tests/test_comp_drift_battery.py`)",
    "pytest": "5/5 PASS (`python -m pytest -q .tools/tests/test_comp_drift_battery.py`)",
    "red_mutants": "4/4 source-mutant arms instantiated in temporary copies: state rc, shared carrier, cursor skip, and answer-state token; each mutation changed the production source and compiled as the negative control.",
    "commit_gate": "PASS: `bash .tools/commit-gate.sh org/modules/graph/drift_cli.py .tools/tests/test_comp_drift_battery.py` (2 of 2 Python files)."
  },
  "acceptance": {
    "T14-AC1": "PASS — identity and all 11 called seam-engine names/denominators are recorded from the engine/topology.",
    "T14-AC2": "PASS — one self-test invocation prints four exact, pairwise-distinct ratified tokens; live budget partial is separately exercised.",
    "T14-AC3": "PASS — comp-similar overlap is a name-level note only; seam engines were not edited.",
    "T14-AC4": "PASS — shared Rule-T carrier, disclosure, expiry rc=3, small-budget cut, cursor, deep guard, and complete cursor resume are measured.",
    "T14-AC5": "PASS — new battery is green direct and under pytest; commit gate is clean; four RED mutation arms are present.",
    "T14-AC6": "PENDING COMMIT — proof instance must validate before this order flips complete; push state is measured below."
  },
  "push_state": {
    "before": "production engine blob 2392e85d5d781c7354c0a1160b1f008a83461cff; battery added in this work",
    "after_local": "measured after report write and before commit",
    "origin": "ABSENT — not asserted until the lane commit and ls-remote/is-ancestor measurement"
  }
}
```

## 1. Tool invocation (verbatim)

```text
python org/modules/graph/drift_cli.py --help
python org/modules/graph/drift_cli.py --self-test
python org/modules/graph/drift_cli.py sweep --budget 0.001
python org/modules/graph/drift_cli.py sweep --deep --budget 0.001
python org/modules/graph/drift_cli.py sweep --budget 0 --cursor seam-2:iam
```

## 2. ws workload scenario + rationale

The real ws scenario is the D11 NFRA_COMPEFFICACY propagation-parity audit: the
TO names the live `drift-topology.yaml` estate and its seam engines. This is not
a synthetic graph; the unbounded sweep read the repository's current topology,
Kuzu marker, folded infra leg, and engine-native verdicts.

## 3. Hand-grep step count (eyeball lift)

Without comp-drift, identity requires reading the topology, expanding seam-2
and seam-6 fan-outs, invoking 10 distinct engines, normalizing their vocabularies,
and separately tracking partial progress. I estimate 15 unit-level invocations
plus 4 normalization/rollup steps. The orchestrator performs that expansion and
keeps a deterministic cursor in one board.

## 4. Tool answer (verbatim)

The live budget-cut answer was:

```text
BUDGET REACHED: 0.001 s (flag); scanned 4 of 15 sweep_unit; results are a PREFIX, not the answer; resume: comp-drift sweep --cursor seam-2:iam
ANSWER-STATE: PARTIAL_OR_BLIND
STATE: PARTIAL_OR_BLIND (rc=3, distinct from clean rc=0, integrity-break rc=1, and seam-unverifiable rc=2 -- a PREFIX carries no verdict)
EXIT: 3 (partial-budget)
```

The cursor resume was:

```text
WITHIN BUDGET: scanned 11 of 11 sweep_unit; budget: unbounded (--budget 0), used 27.42 s
EXIT: 2 (unverifiable)
```

## 5. Manual-validation comparison

The 15-unit denominator agrees with a direct topology expansion (13 manifest
bindings plus two folded infra legs). The resume skipped exactly the four
completed units and measured its own remaining denominator, so it reached a
true engine verdict rather than remaining permanently partial. The rc=3 cut
cannot be mistaken for the rc=2 seam-unverifiable result by an rc-only consumer.

## 6. Noise / false-positives

No seam engine was reimplemented. Cost-guarded records remain `COST-GUARDED`
(`SKIP`) and are not silently converted to `UNVERIFIABLE`; a real engine
`UNVERIFIABLE` remains rc=2. The existing plain sweep's one unverifiable seam
is surfaced as a warning, not treated as clean.

## 7. Integration friction

The bare `comp-read` forwarder is not installed on this Windows seat, although
`.tools/comp-read` exists and returned rc=0 without content; the audit used the
explicit rail and a marked direct read for the required source inspection. No
new dependency was added. The shared `_compbudget.py` carrier is imported from
the workspace `.tools` path, matching existing Rule-T consumers.

## 8. Lift verdict — PASS + 1-line rationale

**PASS** — comp-drift reduced a 15-binding topology walk to one normalized board,
preserved engine-native verdicts, and made a budget prefix mechanically distinct
and resumable (`rc=3`, scanned/total, and cursor).

## Push state (measured after commit)

The lane must measure `git ls-remote origin refs/heads/CLOUD` and
`git merge-base --is-ancestor <lane-commit> origin/CLOUD` after the own-path
commit; no remote state is claimed before that probe.
