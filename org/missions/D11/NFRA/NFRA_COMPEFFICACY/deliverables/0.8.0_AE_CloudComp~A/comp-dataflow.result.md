# comp-dataflow -- NFRA_COMPEFFICACY per-tool result (PRD v0.4 s.4 schema)

Schema: `org/missions/D11/NFRA/NFRA_COMPEFFICACY/prd/NFRA_COMPEFFICACY_PRD.md` v0.4 @`19bf1c7322` s.4
(landed by `1.0.0_SA_CTO`; s.4.3's four answer-state spellings ratified as DATA at
`org/standards/COMPTOOL_ANSWER_STATE.enum.json`; s.4.4 "RULE T's FORM" is the grammar this cell applies).
Row: T-7 (manifest s.7 :608). Cell: CE-t-7 (decomp v0.2.2 @`b7daeaa6f0`), STAGE 2. Measured by
`0.8.0_AE_CloudComp~A`, 2026-09-03T08:16Z-09:40Z, read-vintage HEAD @`8fdc3d0602`, engine
@`8fdc3d0602` (this cell's own commit). Precedents: `deliverables/0.8.0_AE_CloudComp~A/comp-read.result.md`
@`e0f0e5a9e6`, `comp-which.result.md` @`d92fe43586`. **No surprise rows filed this cell** -- no
spec-vs-world divergence surfaced; the reason taxonomy (DYNAMIC-PATH/DEPLOY-TIME-ONLY/FIRM-TREE-ABSENT/
OTHER) is minted fresh by this TO itself (confirmed by census: 0 prior occurrences anywhere in the
estate outside this TO and its dispatch), so its design is this cell's own act, not an inherited spec.

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.4 @19bf1c7322 s.4",
  "row": "T-7",
  "measured_by": "0.8.0_AE_CloudComp~A",
  "measured_at_utc": "2026-09-03T08:16Z..09:40Z",
  "read_vintage": "HEAD @8fdc3d0602",
  "surprises": [],

  "identity": {
    "tool": "comp-dataflow",
    "shim_path": ".tools/comp-dataflow (17, bash)",
    "engine_path": "org/modules/graph/comp_dataflow.py (635) -- the shim is a THIN forwarder (cd to workspace root, python <engine> \"$@\", then a fire-and-forget self-report via comp_log_auto.py with NO Python-level subprocess.run and NO timeout at the shell level -- OUT OF SCOPE this cell, see bounds finding F3 below); ALL logic (parsing, classification, Rule T) lives in the engine, which is what this deliverable audits.",
    "engine_vintage": "8fdc3d0602 (2026-09-03, measured via git log)",
    "aliases": [],
    "aliases_note": "comp-dataflow SUBSUMES the PSTMRT item-9 gate form (its own docstring :16-17: 'PSTMRT item-9's GATE form is SUBSUMED here ... base does not double-build it') and is explicitly NOT scan_lambda_io (structurally blind to the RF-7 read, per the docstring's own grounded comparison, :24-29) -- named, not duplicated.",
    "purpose_1line": "value-origin trace + canonical-source assertion: does a value come from the canonical source, or from a served/legacy artifact?  [engine docstring :1-14]",
    "self_identifies": {
      "help_prints_name_and_version": false,
      "help_prints_engine_path": false,
      "version_flag": "UNSUPPORTED, but SAFELY so: this is a real argparse CLI with required subcommands (origin/gate), so `comp-dataflow --version` fails CLEANLY with argparse's own usage error (rc 2, 'error: the following arguments are required: cmd') rather than being silently routed or misinterpreted -- structurally different from (and safer than) comp-find/comp-read/comp-which's version-flag gaps, which all fall through to a QUESTION/PATTERN slot instead of a hard parse error.",
      "output_line_1": "usage: comp-dataflow [-h] {origin,gate} ...",
      "grade": "ABSENT -- no version identity anywhere, but the argparse-required-subcommand shape makes the absence FAIL LOUD by construction, not silently"
    },
    "registration": {
      "graph_call_manifest": "PRESENT -- org/modules/graph/graph-call-manifest.yaml:1754-1755 (canonical_call, tool), :1787 (tools_index does-line), :1319 (a cross-reference distinguishing it from comp-clobber). STALE in the same shape as every prior T-cell's own finding: the canonical_call names neither --budget nor the enriched unresolved reason.",
      "comp_tools_yaml": "ABSENT (0 hits / 1 file scanned, org/modules/graph/comp-tools.yaml) -- not a routing gap: comp-which's own posterior already routes to comp-dataflow by name (confirmed live in the rail log, ROUTE-POSTERIOR intent=comp-dataflow+... rows).",
      "skill": ".claude/skills/comp-dataflow/ -- ABSENT (0 files across 86 scanned, 8 ephemeral-floor)."
    }
  },

  "disclosure": {
    "run": "DEFAULT flags, `comp-dataflow origin <script.py>` -- rc varies with findings, quoted below",
    "subject":             {"grade": "PRESENT", "quoted": "ORIGIN TRACE: <script>", "note": "the traced script IS the subject; echoed verbatim as the header, same shape as comp-which's question echo."},
    "corpus_or_backend":   {"grade": "PRESENT", "quoted": "'producer output layer(s): gold' -- states which layer(s) the SCRIPT ITSELF writes, orienting the reads that follow"},
    "vintage":             {"grade": "PARTIAL", "quoted": "the engine docstring states 'PLANE: mixed | VINTAGE: parsed producer .py at working-tree HEAD' via _emit_contract() to STDERR only -- a caller capturing stdout alone (as this cell's own battery and every quoted specimen below do) never sees it. No git sha, no mtime is printed anywhere in the observable stdout stream.", "finding": "F1 below."},
    "denominator":         {"grade": "PRESENT, ENRICHED (this cell)", "quoted": "'DENOMINATOR: 3 reads scanned, 1 unresolved-dynamic (blind) [DYNAMIC-PATH=1, DEPLOY-TIME-ONLY=0, FIRM-TREE-ABSENT=0, OTHER=0], 0 served-origin flagged, 0 exempt' -- all four reason classes ALWAYS printed, even at 0 (Rule 24 (i): a class reading 0 is a measured zero over the sweep, never an omitted member)"},
    "resolved_unresolved": {"grade": "PRESENT, ENRICHED (this cell)", "quoted": "'UNRESOLVED             {*}' followed by 'reason: DYNAMIC-PATH' on the line beneath -- WHY, not just THAT, without opening the producer"},
    "blind_spots":         {"grade": "PRESENT", "quoted": "the engine docstring's own named BLIND SPOTS section (:31-37): a fully-dynamic key with no resolvable prefix; a non-S3 read hop; a cross-module constant import -- all named, all COUNTED, never silently skipped (R1 contract, unchanged by this cell)"},
    "pagination":          {"grade": "N/A -- no --page/--limit exists on either subcommand", "quoted": "N/A"},
    "timeout":             {"grade": "PRESENT (this cell, gate only)", "quoted": "'WITHIN BUDGET: scanned 101 of 101 producer_file; budget: 90 s (default), used 0.92 s' or 'BUDGET REACHED: 0.001 s (flag); scanned 1 of 532 producer_file; ... resume: comp-dataflow gate data/ --budget 0.001 --cursor <last-file>'", "before_this_cell": "ABSENT -- the engine had NO subprocess anywhere and NO caller-settable ceiling of any kind; the manifest's own words at cut: 'no timeout'. The gate sweep, run over the full estate, measured 8.8s for 532 files -- fast today, but a caller-settable ceiling did not exist even as a safety margin against a future slower sweep."}
  },

  "answer_state": {
    "schema_note": "Spellings per the RATIFIED enum (PRD v0.4 s.4.3, org/standards/COMPTOOL_ANSWER_STATE.enum.json). GRAIN NOTE: comp-dataflow's 'subject' is the PRODUCER SCRIPT (origin) or the PRODUCER TREE (gate); its 'corpus' is the working-tree .py files under it. All four cases below are exercised entirely on the SOURCE plane -- zero AWS calls, per the TO's own bound.",
    "SUBJECT_ABSENT_FROM_CORPUS": {"planted": "comp-dataflow origin ZZZ_NONEXISTENT_SCRIPT_0903.py", "printed": "\"REFUSE: 'ZZZ_NONEXISTENT_SCRIPT_0903.py' did not resolve to a producer .py file -- nothing traced, nothing concluded (input-resolution refusal, NOT a clean 'no served reads')\"", "rc": 3, "finding": "the tool's own words explicitly name the trap this state exists to prevent ('NOT a clean no served reads') -- a genuinely strong specimen, matching this project's best examples so far (comp-read's explicit ERROR line) rather than comp-find/comp-which's silent-degrade gaps."},
    "PRESENT_WITH_ZERO_RESULTS": {"planted": "comp-dataflow gate data/inf/scripts/silver (a real, non-empty producer subtree, VERIFIED to resolve files and scan reads, with genuinely zero served-origin findings)", "printed": "'comp-dataflow GATE (layer-grammar / PSTMRT item-9): 0 finding(s)' with 'DENOMINATOR: 22 producer files swept, 38 reads scanned, 23 unresolved-dynamic (blind) [...], 0 exempt' -- a MEASURED zero over a real, non-empty, non-zero-file sweep, carrying its own denominator, never silence. CONTRAST, verified live: the neighboring data/mdpf/scripts/gold subtree is NOT this case -- it swept clean the first time this cell tried it, then a wider mdpf sweep DID surface a real finding, confirming the zero above is a genuine measured zero on ITS OWN population, not an artifact of an accidentally-narrow probe.", "rc": 0, "note": "a swept subtree that IS traced (subject present, files resolved, reads scanned) but has zero SERVED-ORIGIN findings is comp-dataflow's own version of this state -- the 'gate' verdict (rc=0, 0 findings, non-zero denominator) IS this state at the whole-sweep grain."},
    "PARTIAL_OR_BLIND":           {"planted": "the honest-unresolved read itself -- two REAL production specimens named at cut by this cell's own baseline gate sweep (2026-09-03, over data/): build_cottonwood_interpolated_backfill.py:196 (DYNAMIC-PATH) and runners_49f/a01_runner.py:86 (FIRM-TREE-ABSENT)", "printed": "'UNRESOLVED             {*}' / 'reason: DYNAMIC-PATH' and 'UNRESOLVED             {*}/dimensions/dim_relationship/date={*}/' / 'reason: FIRM-TREE-ABSENT' -- both COUNTED in the denominator, NEVER resolved by guessing (this cell's own ONE code change)", "rc": 0, "says_which_part": true, "this_cells_own_case": "this IS the TO's own named case: 'an UNRESOLVED read is PARTIAL_OR_BLIND said in the tool's own voice with WHY'. MET."},
    "NOT_APPLICABLE":             {"planted": "comp-dataflow gate ZZZ_NONEXISTENT_DIR_0903 (a pathspec that resolves to zero producer files -- the gate MODE has no population for this subject)", "printed": "\"REFUSE: no producer .py files resolved under ['ZZZ_NONEXISTENT_DIR_0903'] -- nothing swept, nothing concluded (NOT a clean pass)\"", "rc": 3, "declared_by_tool": false, "finding": "F2 below -- this printed shape and rc are IDENTICAL to the SUBJECT_ABSENT_FROM_CORPUS case above (same REFUSE wording pattern, same rc=3), even though the underlying question is different (origin: 'this ONE path is not a file' vs gate: 'this pathspec resolved to NO files at all'). The two states are conflated into one printed shape by the tool."},
    "verdict": "PASS on the PRD criterion as measured (T7-AC2): the four planted cases produce four cases, all on the SOURCE plane, all rc + text quoted. TWO findings recorded: F1 (vintage disclosure is stderr-only, invisible to a stdout-only reader) and F2 (SUBJECT_ABSENT_FROM_CORPUS and NOT_APPLICABLE render as the SAME REFUSE shape and rc, distinguishable only by reading the argument list echoed in the message, not by a structurally different signal) -- and the CELL'S OWN OWED WORK, the PARTIAL_OR_BLIND enrichment, is the strongest of the four: two REAL production specimens, named at cut, preserved unresolved, with a machine-rejectable reason on the line."
  },

  "bounds": {
    "subprocess_timeouts": [],
    "subprocess_timeouts_note": "comp_dataflow.py (the ENGINE) has NO subprocess of its own anywhere -- it is pure AST parsing + file reads (SOURCE plane, per its own docstring: 'Read-only. No writes, no S3 calls'). The ONE Rule T ceiling this cell adds governs a CPU-bound LOOP (cmd_gate's per-file trace_file() sweep), not a subprocess -- a genuinely different shape from CE-t-1/CE-t-2/CE-t-3's subprocess-timeout sites, closer to comp-find's ORIGINAL corpus-width design than to comp-read/comp-which's fire-and-forget telemetry pattern. The shim (.tools/comp-dataflow) DOES have an un-budgeted subprocess (its own self-report call to comp_log_auto.py, at the BASH level, no timeout) -- explicitly OUT OF SCOPE this cell (the TO's own words: 'the ONE code change this cell owes' is the gate sweep + enriched print; BOUNDS: no new dependency), carried as finding F3.",
    "ceiling_behaviour": {
      "exercised": true,
      "how": "the REAL PRODUCTION BINARY, no mutant needed to force the ceiling (it is a caller flag on gate now) -- the same exercise style as every prior T-cell in this project",
      "healthy_default": "`comp-dataflow gate data/assets/scripts/gold` (a 101-file population) -> 'WITHIN BUDGET: scanned 101 of 101 producer_file; budget: 90 s (default), used 0.92 s'; DEFERRED: 0 of 101",
      "forced_tiny_budget": "`comp-dataflow gate data/ --budget 0.001` (the full 532-file population) -> 'BUDGET REACHED: 0.001 s (flag); scanned 1 of 532 producer_file; results are a PREFIX, not the answer; resume: comp-dataflow gate data/ --budget 0.001 --cursor <last-completed-file>'; DEFERRED: 531 of 532, each naming 'budget exhausted before this unit could start'",
      "cursor_resume": "EXERCISED end-to-end: re-running with the printed --cursor value skipped exactly the files up to and including it (verified: the second run's first deferred entry is the NEXT file in sorted order after the resumed one), a REAL resumable sweep, not a cosmetic flag",
      "finding_partial_gate_rc": "F4 below -- a BUDGET-REACHED (partial) gate sweep with 0 findings among the files it DID reach still returns rc=0, the SAME rc a genuinely clean full sweep returns. Disclosed, not hidden: this matches every prior T-cell's own F3/F5-class finding ('rc stays 0/clean regardless of completeness; the LINE is the rejectable state, not the rc', PRD s.4.4's own words) -- a caller checking rc alone on a budget-constrained gate run cannot tell 'no violations found' from 'no violations found in the PREFIX we had time to check'."
    },
    "page_contract": {"page_flag": false, "limit_flag": false, "all_flag": false, "true_total_printed": true, "cap_flags": "--budget N / --cursor PATH (new, this cell, gate only)", "help_discloses_flags": "PRESENT -- `comp-dataflow gate --help` documents --budget's carrier/precedence/default and --cursor's resume semantics; `comp-dataflow origin --help` correctly shows NEITHER flag (the non-application is structural, not a doc gap)", "note": "no pre-existing pagination exists to preserve; BOUNDS: item-9 semantics (served-origin flagging, exemption list) unchanged, verified by this cell's own battery arm 4 against the RF-7 charter specimen."},
    "size_invariance": {"work": "cmd_gate's per-file trace_file() cost scales with producer-tree width (measured: 8.8s for 532 files pre-budget, i.e. ~16.5ms/file average, pure local AST parsing -- no network, no subprocess). Rule T's ceiling now bounds this loop directly via a REAL per-unit remaining() check between files, the same shape as comp-find's original corpus-width design, not a fire-and-forget wrapper around a single call.", "time": "measured worst case (the full data/ tree, 532 files) is 8.8s, well under the 90s default -- this cell's own ceiling has generous headroom TODAY, unlike CE-t-3's comp-which finding (an 82.7s near-miss); disclosed as the honest contrast, not asserted as guaranteed to stay that way as the producer tree grows.", "rule_P": "N/A (no pagination in this tool)", "rule_T": "MET (this cell) for the ONE corpus-width loop that exists -- carrier, expiry disclosure, a REAL resumable cursor, and the WITHIN BUDGET completion all exercised live on the real binary; the non-application half (origin has no loop at all, and the shim's own un-budgeted self-report subprocess is out of this cell's scope, F3) stated honestly"}
  },

  "passcraft": {
    "recon": "comp-passcraft recon comp-dataflow -- MOVES 1-3 hand-checked (no comp-passcraft catalog entry for this tool at cut; the engine is invoked via its own shim, not the .tools/ flat-file convention comp-passcraft's auto-observation targets); MOVES 4-8 hand-run below",
    "moves_1_to_8": [
      {"move": 1, "status": "DONE", "falsifier_answer": "the shim (17 lines, bash) is a THIN forwarder; ALL logic lives in the real engine, org/modules/graph/comp_dataflow.py (635 lines) -- confirmed by reading both files directly, not inferred from naming"},
      {"move": 2, "status": "DONE", "falsifier_answer": "write surface: the shim's own self-report call to org/mcp/comp-tool-runs.jsonl (bash-level, fire-and-forget, `2>/dev/null` -- errors silently swallowed even at the shell). The ENGINE ITSELF makes ZERO writes (docstring: 'Read-only. No writes, no S3 calls')."},
      {"move": 3, "status": "DONE", "falsifier_answer": "no cache anywhere -- every run re-parses the target .py file(s) fresh from the working tree at invocation time; no frozen fixture used as the measure, confirmed by reading trace_file()'s own body (a fresh ast.parse() per call, no memoization)"},
      {"move": 4, "status": "DONE", "falsifier_answer": "target universe FROM SOURCE: this cell's own baseline gate sweep over data/ (2026-09-03, BEFORE any code change) measured 532 producer files, 1036 reads scanned, 604 unresolved -- a non-sharing instrument (a throwaway Python script calling trace_file() directly on the SAME population _iter_producers() resolves) cross-checked the 604 total and its 542/62 shape split, matching the tool's own DENOMINATOR exactly"},
      {"move": 5, "status": "DONE", "falsifier_answer": "the four answer-state branches AND all four reason-class branches verified from the OUTPUT differing structurally (a REFUSE line + rc 3, a clean DENOMINATOR with 0 served-origin, an UNRESOLVED+reason pair, a findings list), never asserted by name; DYNAMIC-PATH and FIRM-TREE-ABSENT confirmed on REAL production files; DEPLOY-TIME-ONLY and OTHER confirmed on PLANTED fixtures, all four exercised via direct execution"},
      {"move": 6, "status": "DONE", "falsifier_answer": "mutations only in a scratch mirror tree (matching comp_dataflow.py's own _WS-resolution depth: org/modules/graph/comp_dataflow.py + .tools/_compbudget.py under a tempdir), never touching the real production files; production sha256 measured before and after this cell's commit; mutant copies removed via tempfile.TemporaryDirectory's own context-manager teardown, confirmed"},
      {"move": 7, "status": "DONE", "falsifier_answer": "ground truth from a NON-SHARING instrument for MOVE 4 (above); separately, the reason-class SPLIT (DYNAMIC-PATH vs FIRM-TREE-ABSENT) was independently re-derived by a Python one-liner checking `raw.replace('{*}','').strip('/')` against every unresolved raw string outside the tool's own code path, matching the engine's classification on all 604 rows"},
      {"move": 8, "status": "DONE", "falsifier_answer": "archetype hand-classified below; lead probes hunted: guard-asymmetry (PASS -- a real served-origin read flags, a real clean read does not, both directions confirmed on the RF-7 specimen), success-token-bound-to-wrong-step (FOUND, F4 above -- a partial budget-limited gate sweep's rc=0 is indistinguishable from a genuinely clean full sweep at the rc alone), skip-on-missing-field (clean -- every unresolved read gets a reason, the OTHER fallback is a real reachable branch not a silent drop, exercised via a planted fixture), resource-blind (clean -- the served-origin verdict correctly changes with the read's actual layer, confirmed across multiple real specimens), undiscriminating/constant-gate (clean -- findings count and denominator both demonstrably vary with the pathspec swept)"}
    ],
    "archetype": "STRUCTURED-FINDING instrument (a real GATE, PRD's own vocabulary): rc is bound to WHETHER A FINDING EXISTS (1 if findings, 0 if none, 3 on a resolution refusal) -- genuinely different from comp-find/comp-read/comp-which's GRADED-MEASUREMENT archetype (where rc is bound to execution, never to the answer). This makes F4 (a partial sweep's 0-findings rc=0) a SHARPER risk here than the analogous finding in prior T-cells: a caller who DOES treat rc as the verdict (reasonably, for a real gate) is exactly the caller F4 warns.",
    "findings": [
      {"id": "F1", "shape": "disclosure gap (vintage stderr-only)", "cite": "org/modules/graph/comp_dataflow.py:_emit_contract() @8fdc3d0602 (unchanged by this cell)", "text": "the PLANE/VINTAGE line is printed to stderr only; a caller capturing stdout alone (this cell's own battery included) never sees it -- present in the tool, invisible to the common capture pattern"},
      {"id": "F2", "shape": "answer-state conflation (mirrors comp-which's own F1/F2 class)", "cite": "org/modules/graph/comp_dataflow.py:cmd_origin()/cmd_gate() REFUSE branches @8fdc3d0602 (unchanged by this cell)", "text": "SUBJECT_ABSENT_FROM_CORPUS (origin: the named file does not exist) and NOT_APPLICABLE (gate: the pathspec resolves to zero files) render the SAME 'REFUSE: ... nothing swept/traced, nothing concluded' shape and the SAME rc=3 -- distinguishable only by reading which subcommand and which argument text is echoed, not by a structurally different signal"},
      {"id": "F3", "shape": "un-budgeted subprocess, out of this cell's scope, owner named", "cite": ".tools/comp-dataflow:16-17 (the shim's own self-report call to comp_log_auto.py) @unchanged", "text": "the shim's telemetry self-report has NO timeout at the bash level -- unlike CE-t-1/CE-t-2/CE-t-3's Python-level self-report subprocesses (all now Rule-T-budgeted), this one is a bash-to-python invocation the TO's own words scope OUT ('the ONE code change this cell owes' names only the gate sweep + print enrichment). Owner: a future cell under this same project, or whoever next touches the shim -- not self-assigned here."},
      {"id": "F4", "shape": "success-token-bound-to-wrong-step, SHARPER here than in prior cells (see archetype note)", "cite": "org/modules/graph/comp_dataflow.py:cmd_gate() @8fdc3d0602 (this cell's own new code)", "text": "a BUDGET-REACHED (partial) gate sweep with 0 findings among the reached files still returns rc=0 -- byte-identical to a genuinely complete clean sweep's rc. Disclosed in --help's own carrier description and in this deliverable, not hidden; the BUDGET REACHED line is the rejectable signal, per Rule T's own stated form, but this tool's GATE archetype (rc IS the verdict, by design) makes an rc-only caller's mis-read materially more consequential than in the three prior T-cells."}
    ]
  },

  "usage": {
    "runs_30d": {
      "runs_jsonl": {"count": "TO's own issuance-time figure: 11 runs at org/mcp/comp-tool-runs.jsonl (device-local, gitignored)", "note": "NOT independently re-derived: a raw content search for the string 'comp-dataflow' in that file returns 49 hits, but the great majority carry to_id='NFRA_MSBEFF.R2.comp-dataflow-canonical-source' (the tool's OWN BUILD project's TO id containing the string) rather than tool='comp-dataflow' -- a GRAIN trap (Rule 22): the string search measures MENTIONS, not INVOCATIONS. The TO's own '11 runs' figure is cited as-is, not re-derived, because this cell's own instrument would need a tool= field filter to be a sound re-derivation, and that re-derivation was not performed."},
      "rail_log":   {"count": "TO's own issuance-time figure: not separately stated for this tool; a raw content search for 'comp-dataflow' in org/mcp/comp-which-rail.log returns 390 hits, dominated by comp-which's OWN ROUTE-POSTERIOR rows citing comp-dataflow as a routing candidate (intent=comp-dataflow+comp-describe+comp-pipescript) -- again a mentions-vs-invocations grain trap, not re-derived to a clean count this cell."}
    },
    "hook_driven": {"fraction": "not measured this cell; no specific evidence of a PreToolUse-hook-driven caller was found or claimed"},
    "battery": {
      "files": [{"path": ".tools/tests/test_comp_dataflow_battery.py (320 lines, NEW -- 0 files existed for this tool at cut)", "collects_under_pytest": "1 test, ~16s (dominated by the full data/ tree gate sweep exercised twice -- once for BUDGET-CARRIER's forced-tiny-budget arm, once inside MUTANT-BUDGET's mirror)", "red_first_mutant": true, "mutant_forms": "THREE, matching three of the five logical arms: NEVER-GUESS (an unresolved Name falls back to a live os.environ read), MUTANT-REASON (the classifier always returns OTHER), MUTANT-BUDGET (the carrier ignores --budget) -- all three built in a scratch mirror tree matching comp_dataflow.py's own _WS-resolution depth (mirroring comp-which-routing-test.py's build_mirror() precedent), all three RUN (not crash) and FAIL their sibling arm's own predicate"}],
      "file_grain_result": "8 of 8 rec()-calls PASS (4 logical arms as real+mutant pairs, plus REASON-CONSERVATION and ITEM-9-UNCHANGED as standalone regression controls needing no mutant) -- confirmed direct AND under pytest -q",
      "lane_sweep": "pytest --collect-only .tools/tests/ -> still INTERNALERROR / SystemExit at test_fabric_check_classify.py:76 (one of CTO's three named F6 files), UNCHANGED from the census this seat's sibling cells ran; 35 tests collected before the abort (up from 25 at CE-t-1/CE-t-2's own read, since this cell's new battery file sorts alphabetically before the abort point) -- not this cell's to fix (CTO's)."
    },
    "overlap": "SUBSUMES the PSTMRT item-9 GATE form (named, not duplicated, per the engine's own docstring); explicitly NOT scan_lambda_io (structurally blind to the RF-7 acceptance case, per a grounded 2026-07-23 comparison in the same docstring); the write-target index exists only to establish a producer's OUTPUT layer, never re-implementing comp-clobber's own collision detection (named sibling, not a fork).",
    "proposed": "CLEARED-candidate for Rule T + the never-guess/enrichment work specifically (T7-AC1..AC6 as measured above); the project-wide CLEARED disposition is CVO's grade to render. Four findings (F1-F4) named above: F1 and F2 are pre-existing, not introduced by this cell, not fixed here (BOUNDS: item-9 classification does not change; disclosure improvements beyond the unresolved-reason enrichment were not asked); F3 is carried with an owner named, explicitly out of this cell's scope; F4 is THIS cell's own new code and is disclosed honestly rather than hidden, with an explicit note that this tool's GATE archetype makes it a sharper risk than the analogous finding in CE-t-1/CE-t-2/CE-t-3."
  }
}
```

## The four planted answer-state cases, quoted

**SUBJECT_ABSENT_FROM_CORPUS** -- a nonexistent script path, rc 3:
```
comp-dataflow origin ZZZ_NONEXISTENT_SCRIPT_0903.py
REFUSE: 'ZZZ_NONEXISTENT_SCRIPT_0903.py' did not resolve to a producer .py file -- nothing traced,
nothing concluded (input-resolution refusal, NOT a clean 'no served reads')
```

**PRESENT_WITH_ZERO_RESULTS** -- a real, non-empty producer subtree, gate mode, zero findings, rc 0:
```
comp-dataflow gate data/inf/scripts/silver
comp-dataflow GATE (layer-grammar / PSTMRT item-9): 0 finding(s)
  DENOMINATOR: 22 producer files swept, 38 reads scanned, 23 unresolved-dynamic (blind)
  [DYNAMIC-PATH=23, DEPLOY-TIME-ONLY=0, FIRM-TREE-ABSENT=0, OTHER=0], 0 exempt
  WITHIN BUDGET: scanned 22 of 22 producer_file; budget: 90 s (default), used 0.24 s
```

**PARTIAL_OR_BLIND** -- the cell's own owed case, two REAL specimens preserved and enriched, rc 0:
```
comp-dataflow origin data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py
  L196   [unknown ] UNRESOLVED             {*}
          reason: DYNAMIC-PATH

comp-dataflow origin data/assets/scripts/gold/runners_49f/a01_runner.py
  L86    [unknown ] UNRESOLVED             {*}/dimensions/dim_relationship/date={*}/
          reason: FIRM-TREE-ABSENT
```
Both COUNTED in their file's own DENOMINATOR line, never resolved by guessing.

**NOT_APPLICABLE** -- a pathspec with no producer population, rc 3:
```
comp-dataflow gate ZZZ_NONEXISTENT_DIR_0903
REFUSE: no producer .py files resolved under ['ZZZ_NONEXISTENT_DIR_0903'] -- nothing swept,
nothing concluded (NOT a clean pass)
```
Same printed shape and rc as SUBJECT_ABSENT_FROM_CORPUS above -- this IS finding F2.

## The two planted (currently-unpopulated-live) reason classes, quoted

```
# DEPLOY-TIME-ONLY (planted fixture: a name assigned from os.environ.get(...), read directly):
comp-dataflow origin deploy_time_fixture.py
  L6     [unknown ] UNRESOLVED             {*}
          reason: DEPLOY-TIME-ONLY

# OTHER (planted fixture: a dynamic value with no Name node driving it at all):
comp-dataflow origin other_fixture.py
  L2     [unknown ] UNRESOLVED             {*}
          reason: OTHER
```
Both classes read 0 across the real 604-row baseline sweep (2026-09-03, over data/) -- disclosed
honestly, not hidden; both are real, reachable branches of the classifier, proven via the battery's
own arms, not asserted.

## Rule T, exercised end to end (the code change this cell owed)

Healthy default on a bounded pathspec:
```
comp-dataflow gate data/assets/scripts/gold
  ...
  WITHIN BUDGET: scanned 101 of 101 producer_file; budget: 90 s (default), used 0.92 s
  DEFERRED: 0 of 101 producer_file(s) did not return -- each names its reason below
```
Forced ceiling on the full estate tree -- a REAL resumable cursor:
```
comp-dataflow gate data/ --budget 0.001
  BUDGET REACHED: 0.001 s (flag); scanned 1 of 532 producer_file; results are a PREFIX, not the
  answer; resume: comp-dataflow gate data/ --budget 0.001 --cursor
  data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py
  DEFERRED: 531 of 532 producer_file(s) did not return -- each names its reason below
```
Resuming with that exact cursor -- skipped exactly the completed unit, advanced to the next:
```
comp-dataflow gate data/ --budget 0.001 --cursor data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py
  BUDGET REACHED: 0.001 s (flag); scanned 1 of 532 producer_file; ...
  DEFERRED: 530 of 532 -- first entry: data/assets/scripts/gold/build_cottonwood_mdpf_slice.py
```
`--help` discloses the carrier on `gate` only; `origin --help` shows neither flag (structural
non-application, not an omission):
```
comp-dataflow gate --help
  --budget N     RULE T (PRD s.4.4, shared .tools/_compbudget): wall-clock ceiling in seconds for
                 this sweep (carrier: --budget > env COMP_BUDGET_S > default 90 s); --budget 0 =
                 unbounded. Only 'gate' has this flag -- 'origin' traces exactly one file and has
                 no corpus-width loop to bound.
  --cursor PATH  resume a budget-limited sweep after producer PATH ...
```

## Findings F1-F4

See `passcraft.findings` in the JSON block above. F1 (stderr-only vintage) and F2 (two answer-states
share one printed shape) are pre-existing, carried, not fixed under this TO's BOUNDS. F3 (the shim's
own un-budgeted self-report) is explicitly out of this cell's scope, owner named. F4 (a partial gate
sweep's rc stays 0) is this cell's own new code, disclosed honestly with an explicit note that this
tool's GATE archetype (rc IS the verdict) makes the risk sharper than the analogous finding in
CE-t-1/CE-t-2/CE-t-3.

## Captures and controls

Every quoted run above is a direct execution captured in this session (not a paraphrase); the
604-row baseline (542 DYNAMIC-PATH / 62 FIRM-TREE-ABSENT / 0 DEPLOY-TIME-ONLY / 0 OTHER) was
independently re-derived via a throwaway script calling `trace_file()` directly, outside the CLI's
own code path (MOVE 4/7). Production sha256: `org/modules/graph/comp_dataflow.py` was
`1d31da59b07f22f67c114612e246c7401138bdab79b5dca6c765df7ce9c0782f` at HEAD `6327b00060`
(2026-07-23, before this cell -- unchanged since the tool's own R2 build), `7724e1a44ebe183a843d0775ae3350477a1d99ce16dc25d189a2aab9b69ace03`
at HEAD `8fdc3d0602` (after this cell's rework) -- two MEASURED points. `git status` at write time
shows only this deliverable + its proof-of-spec instance pending beyond the already-landed code
commit. Push state, MEASURED (ls-remote + is-ancestor), reported in the commit report per T7-AC6,
not asserted here.
