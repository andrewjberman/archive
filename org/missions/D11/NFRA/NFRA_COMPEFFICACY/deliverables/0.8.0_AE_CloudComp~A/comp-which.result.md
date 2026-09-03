# comp-which -- NFRA_COMPEFFICACY per-tool result (PRD v0.4 s.4 schema)

Schema: `org/missions/D11/NFRA/NFRA_COMPEFFICACY/prd/NFRA_COMPEFFICACY_PRD.md` v0.4 @`19bf1c7322` s.4
(landed by `1.0.0_SA_CTO`; s.4.3's four answer-state spellings ratified as DATA at
`org/standards/COMPTOOL_ANSWER_STATE.enum.json`; s.4.4 "RULE T's FORM" is the grammar this cell applies).
Row: T-3 (manifest s.7 :604). Cell: CE-t-3 (decomp v0.2.1 @`070907b56e`). Measured by `0.8.0_AE_CloudComp~A`,
2026-09-03T06:00Z-07:10Z, read-vintage HEAD @`e8f67c34f5`, engine @`e8f67c34f5` (this cell's own commit --
the deliverable follows the fix, per the TO's ONE-deliverable-ONE-code-change circle). The precedents:
`deliverables/0.8.0_AE_CloudComp/comp-find.result.md` @`6d04680f2b`,
`deliverables/0.8.0_AE_CloudComp~A/comp-read.result.md` @`e0f0e5a9e6`. **No surprise rows filed this
cell** -- no spec-vs-world divergence surfaced (the two defects found below were caught and fixed BY
this cell's own audit, before either ever shipped or was even reachable by another agent).

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.4 @19bf1c7322 s.4",
  "row": "T-3",
  "measured_by": "0.8.0_AE_CloudComp~A",
  "measured_at_utc": "2026-09-03T06:00Z..07:10Z",
  "read_vintage": "HEAD @e8f67c34f5",
  "surprises": [],

  "identity": {
    "tool": "comp-which",
    "shim_path": ".tools/comp-which (2,439)",
    "engine_path": ".tools/comp-which (2,439) -- SELF-CONTAINED at the routing layer: imports two library siblings, _comprail.py-style rail primitives are NOT used here (comp-which has its own _log_rail) and _compbudget.py (Rule T carrier, this cell, UNGUARDED per the reference application). At runtime it ALSO dynamically imports comp_route.py + comp_capability_provider.py + comp_which_signals.py from org/modules/graph/ (the DR2 posterior router, NFRA_COMPROUTE) -- a real delegate, wrapped in try/except with a LEGACY-CASCADE fail-safe (comp_route errors -> None -> the pre-DR2 curated/manifest-fuzzy cascade runs instead, never a crash).",
    "engine_vintage": "e8f67c34f5 (2026-09-03T03:0xZ local = 2026-09-03T07:0xZ, measured via git log)",
    "aliases": [],
    "aliases_note": "no comp-tool comp-which replaces or is replaced by -- it is the ONE router (Rule 21's reflex tool); its own fallback primitive delegates to comp-find (comp-grep/comp-glob are kept, unrouted, per the same retire-consumers-first pattern comp-find's own T-1 result documented).",
    "purpose_1line": "maps a natural-language question to the canonical comp-* call -- Rule 21's DEFAULT for every search + inspection  [engine docstring :1-9]",
    "self_identifies": {
      "help_prints_name_and_version": false,
      "help_prints_engine_path": false,
      "version_flag": "UNSUPPORTED -- comp-which has NO dedicated flag parser for --version/-h; both fall through to the QUESTION slot and get ROUTED. Measured: `comp-which --version` -> the NOFIT-POSTERIOR shape (fuzzy guesses, none confident, honest); `comp-which -h` -> falls to the on-rails fallback (search-verb-shaped by accident, since '-h' contains no recognizable intent). SAFER than comp-find's identical gap (T-1 F1): comp-find's --version silently returns real-looking search hits; comp-which's --version at least produces the tool's own honest no-fit hedge, never a confident wrong answer.",
      "output_line_1": "comp-which \"<your question>\"  -- maps a natural-language question to the canonical comp-* call.  (dynamic; no static version banner)",
      "grade": "ABSENT -- no version identity anywhere in the tool; --version routes as a question rather than erroring, but the honest answer-state hedge (NOFIT-POSTERIOR) is a materially safer failure mode than comp-find's silent-hit footgun"
    },
    "registration": {
      "graph_call_manifest": "PRESENT -- org/modules/graph/graph-call-manifest.yaml:735-736 (canonical_call, anti_pattern), 33 total mentions across the file (comp-which is both a registered tool AND the router other entries are written to be found BY). STALE in the same shape as comp-find/comp-read's own entries: :735's canonical_call names no --budget flag (this cell's own addition).",
      "comp_tools_yaml": "ABSENT (0 hits / 1 file scanned, org/modules/graph/comp-tools.yaml) -- not a routing gap: comp-which IS the router, not a routed-to purpose-catalog entry.",
      "skill": ".claude/skills/comp-which/ -- ABSENT (0 files across 86 scanned, 8 ephemeral-floor)."
    }
  },

  "disclosure": {
    "run": "DEFAULT flags, `comp-which \"what breaks if I change this function\"` -- rc 0, quoted below",
    "subject":             {"grade": "PRESENT", "quoted": "comp-which -- candidates for: \"<question>\"", "note": "the question IS the subject; echoed verbatim in the header, unlike comp-find's pattern-only echo."},
    "corpus_or_backend":   {"grade": "PARTIAL", "quoted": "the response never states WHICH LAYER answered (curated rule / DR2 posterior / manifest-fuzzy backstop / legacy cascade) -- a reader cannot tell from the output alone whether comp_route.py ran or the fail-safe fired.", "finding": "F1 below."},
    "vintage":             {"grade": "ABSENT", "quoted": "no run prints a manifest/ledger mtime, git sha, or catalog version -- a route decided against a stale graph-call-manifest.yaml renders identically to one decided against a fresh one."},
    "denominator":         {"grade": "PRESENT", "quoted": "MATCHES (top 3 of 79 -- score is overlap, NOT a confidence)  /  ALL 79 tools, ranked + described: .comp-graph/which/rank-<N>.yaml"},
    "resolved_unresolved": {"grade": "PRESENT", "quoted": "'*** TOP SCORES ARE TIED -- THE ORDER IS NOT A RANKING. Read the descriptions. ***' / 'near-tie -- ... pick by concern (never a silent guess)' -- both name WHICH PART is uncertain"},
    "blind_spots":         {"grade": "PRESENT", "quoted": "'!! NO CURATED RULE MATCHED THIS QUESTION ... THE CATALOG DOES NOT COVER IT -- do not pick one because it was ranked first.' -- an explicit non-endorsement of its own top-ranked guess"},
    "pagination":          {"grade": "PRESENT", "quoted": "top 3 of N always states N; 'ALL N tools, ranked + described' names the escape hatch to the full ranking file"},
    "timeout":             {"grade": "PRESENT (this cell)", "quoted": "'WITHIN BUDGET: scanned 1 of 1 fallback_primitive_call; budget: 110 s (flag), used 89.53 s' or 'BUDGET REACHED: 90 s (default); scanned 0 of 1 fallback_primitive_call; ... the subprocess did not return within the remaining budget (TimeoutExpired); ...'", "before_this_cell": "PRESENT-BUT-WRONG on TWO sites -- :1678 (pre-rework) hard-coded FALLBACK_TIMEOUT_S=60 on the comp-find fallback Popen.wait() (the corrected 84-minute-hang site), and :2372 hard-coded timeout=20 on the self-report subprocess; neither printed anything at expiry beyond a bare WARN with no budget/source/denominator."}
  },

  "answer_state": {
    "schema_note": "Spellings per the RATIFIED enum (PRD v0.4 s.4.3, org/standards/COMPTOOL_ANSWER_STATE.enum.json). GRAIN NOTE: comp-which's 'subject' is the QUESTION; its 'corpus' is the 79-80-tool catalog (graph-call-manifest.yaml + the coverage ledger) the question is matched against.",
    "SUBJECT_ABSENT_FROM_CORPUS": {"planted": "a syntactically-valid gold-script ID that does not exist: 'what does gold script A_99z read and write' (GOLD_ID regex matches the SHAPE 'A_99z'; confirmed via comp-find -- 0 hits anywhere in the estate for this string)", "printed": "'1. score 2.00   comp-pipescript io A_99z' -- routed with FULL CONFIDENCE (a curated-strength score, forced high by the gold-id special-case), no hedge, no NOFIT banner, no verification the id refers to anything real", "rc": 0, "finding": "F2 below -- the router recognizes the SHAPE of a subject and routes on it without checking the subject EXISTS; a fabricated ID is indistinguishable from a real one in the tool's own voice."},
    "PRESENT_WITH_ZERO_RESULTS": {"planted": "a real historical rail-log probe reproduced live: 'asdfqwerzxcv nonsense control question' (:1545-1551's own class -- 108 no-matches measured at cut)", "printed": "'!! NO CURATED RULE MATCHED THIS QUESTION ... Every candidate scored below the vetted band. These are FUZZY GUESSES, not a routing decision. ... THE CATALOG DOES NOT COVER IT -- do not pick one because it was ranked first.' -- then still SHOWS the 3 best (below-band) guesses, explicitly disclaimed", "rc": 0, "log_tag": "NOFIT-POSTERIOR (confirmed in this cell's own routing-test run: 21 occurrences in the live rail log at cut)", "note": "this is the TO's own named case: 'NOFIT-POSTERIOR is a no-match, never a route' -- MET. The banner never claims a decision; the printed candidates are labelled guesses, not an answer."},
    "PARTIAL_OR_BLIND": {"planted": "a real historical rail-log probe reproduced live: 'registry narrative vs project json' (2026-07-01 ROUTE-POSTERIOR-DISAMBIG tag) -- a genuine top-rank tie, batch-probed warm against 11 historical DISAMBIG queries, 2 of 11 still reproduce today (catalog scoring has drifted since 2026-07-01; the other 9 no longer tie)", "printed": "'near-tie -- the surface-aware router surfaces these; pick by concern (never a silent guess): ... 1. score 1.50 comp-registry sync ... 2. score 1.50 comp-state ... *** TOP SCORES ARE TIED -- THE ORDER IS NOT A RANKING. Read the descriptions. ***'", "rc": 0, "says_which_part": true, "second_specimen_this_cell": "BUDGET REACHED itself, exactly as comp-find/comp-read's own T-1/T-2 results used it -- a second, code-level PARTIAL_OR_BLIND specimen ('scanned 0 of 1 ... call' names exactly which unit did not complete)"},
    "NOT_APPLICABLE": {"planted": "comp-which --surfaces (the taxonomy DATA VIEW, not a routing question)", "printed": "the surface-first taxonomy table (LOCAL/GIT/AWS-CLOUD/... groups with their tool lists) -- no MATCHES block, no score, no answer-state machinery invoked at all", "rc": 0, "declared_by_tool": false, "finding": "the tool correctly recognizes 'answer-state' does not apply to a browse/data-view request and renders the different, correct thing -- a CORRECT result no answer-state remedy would move, matching the enum's own definition exactly. Not stated in comp-which's own voice as 'NOT_APPLICABLE' (no tool does, per every T-1/T-2/T-3 finding so far in this project), but structurally unambiguous: nothing resembling the routing-decision shape is printed."},
    "verdict": "PASS on the PRD criterion as measured (T3-AC2): the four planted cases produce four DISTINGUISHABLE, machine-rejectable outputs in the tool's own voice (an explicit disclaimer banner, an explicit tie-banner, a data-view with no routing shape at all, and a confidently-scored route with no existence check). TWO FINDINGS recorded, not hidden: F1 (no layer-provenance disclosure) and F2 (SUBJECT_ABSENT_FROM_CORPUS is not merely undisclosed but actively MASKED by a confident score) -- F2 is the more serious of the two, a genuine wrong-object risk class."
  },

  "bounds": {
    "subprocess_timeouts": [
      {"file_line": ".tools/comp-which:~1697 @e8f67c34f5 (_run_primitive)", "value_s": "_CLOCK.remaining() -- one shared Clock started in main() before either subprocess site can fire, never a fixed constant", "wraps": "python .tools/comp-find <term>  (the on-rails fallback the tool's own footer promises: 'it would have RUN comp-find')", "before_this_cell": ":1678 (pre-rework HEAD @dffbee781c) hard-coded FALLBACK_TIMEOUT_S=60 -- the SAME constant the GATEBOUND Stage B fix (2026-07-25) introduced to close the confirmed 84-minute hang; this cell does not reopen that class, it makes the ceiling a caller-settable, disclosed budget instead of a silent fixed one"},
      {"file_line": ".tools/comp-which:~2417 @e8f67c34f5 (_self_report)", "value_s": "the SAME _CLOCK.remaining(), read a second time -- so a run that already spent budget on the fallback has correspondingly less left here, never a fresh independent allowance", "wraps": "python org/modules/graph/comp_log_auto.py comp-which <argv> <rc>  (self-report telemetry, fire-and-forget)", "before_this_cell": ":2372 (pre-rework) hard-coded timeout=20, unchanged in spirit from comp-read/comp-find's own T-1/T-2 pre-rework state"}
    ],
    "ceiling_behaviour": {
      "exercised": true,
      "how": "the REAL PRODUCTION BINARY for the fallback ceiling (no mutant needed -- the ceiling is a caller flag now); the shared-clock semantics were exercised together with a real, unforced, naturally-occurring near-timeout condition, not a synthetic one",
      "measured_finding": "an UNSCOPED comp-find fallback call (comp-which routes 'grep the repo for X' with no pathspec, since the router has no way to scope comp-find's target) measured 82.7s DIRECT on this box (146,464 files, corpus=all default). Rule T's shared 90s default is a THIN margin over this -- a repeat of the SAME query through comp-which at the default budget was independently observed to hit BUDGET REACHED (killed) on one run and complete WITHIN BUDGET (~89s used) on another, consistent with normal system-load variance around an 82-90s boundary. THIS IS NOT A REGRESSION THIS CELL INTRODUCES: the OLD fixed ceiling (FALLBACK_TIMEOUT_S=60) is STRICTLY TIGHTER than 90s, so the identical query would ALSO have been killed under the pre-Rule-T code (82.7s > 60s, trivially). Rule T's 90s default is MORE forgiving, not less, though still marginal for this specific unscoped shape.",
      "healthy_default": "`comp-which \"what breaks if I change this function\"` (a curated STRONG match, never reaches _run_primitive) -> 'WITHIN BUDGET: scanned 1 of 1 telemetry_call; budget: 90 s (default), used 0.89 s'",
      "forced_fallback_default_budget": "`comp-which \"grep the repo for ZZZ_NONEXISTENT_TOKEN_0903\"` (no --budget) -> BOTH sites print BUDGET REACHED: the fallback via TimeoutExpired ('the subprocess did not return within the remaining budget'), and the telemetry call via the pre-flight SKIP ('the self-report subprocess was SKIPPED, not run') -- the shared clock correctly propagates exhaustion from the first site to the second",
      "forced_fallback_larger_budget": "`comp-which \"grep the repo for ZZZ_NONEXISTENT_TOKEN_0903\" --budget 110` -> 'WITHIN BUDGET: scanned 1 of 1 fallback_primitive_call; budget: 110 s (flag), used 89.53 s' immediately followed by 'WITHIN BUDGET: scanned 1 of 1 telemetry_call; budget: 110 s (flag), used 89.62 s' -- both units complete because the shared budget (110s) exceeds the measured ~89s the fallback actually needed, with ~20s correctly left over for the telemetry call",
      "forced_tiny_budget": "`--budget 0.001` on a FAST read (a query that skips straight to the fallback with minimal upstream router work) -> the pre-flight remaining()<=0 check has not yet tripped by the time subprocess.run is attempted (elapsed since Clock() start is still <1ms), so Popen.wait(timeout=~0.001) itself raises TimeoutExpired -> 'BUDGET REACHED: 0.001 s (flag); ... the subprocess did not return within the remaining budget (TimeoutExpired)'. On a SLOWER read (more upstream router work before reaching the fallback), the SAME --budget 0.001 instead hits the pre-flight SKIP branch first ('the fallback was SKIPPED, not run') -- BOTH sub-branches are real and reachable depending on elapsed time at the check, mirroring exactly the CE-t-2 finding for comp-read's own single-subprocess case, now confirmed to generalize to a TWO-subprocess, shared-clock tool.",
      "unbounded": "--budget 0 not separately re-exercised this cell (identical mechanism to CE-t-1/CE-t-2, both already exercised there against the SAME shared _compbudget.Clock class)"
    },
    "page_contract": {"page_flag": false, "limit_flag": false, "all_flag": false, "true_total_printed": true, "cap_flags": "--budget N (new, this cell)", "help_discloses_flags": "PRESENT -- the bare-argv usage block now documents --budget's carrier/precedence/default alongside --surfaces", "note": "comp-which has no --page/--limit of its own (top-3 is fixed by design, Andrew-direct 'k=3, NEVER 1' per the routing-test's own header); T3's BOUNDS forbid touching routing semantics, and this cell does not."},
    "size_invariance": {"work": "comp-which's OWN routing work (scoring 79-80 curated rules + the DR2 posterior) has NO subprocess and is not budgeted by this cell -- it is bounded by construction (a fixed catalog size, no external I/O). Rule T governs exactly the TWO subprocess-bearing tails: the fallback primitive (corpus-width-DEPENDENT, since comp-find's own scan time scales with the corpus) and the fire-and-forget telemetry call (corpus-independent, always ~1 unit).", "time": "the measured 82.7-89s fallback scan time is a real, disclosed non-application boundary: Rule T bounds the CEILING, it does not make the underlying comp-find scan any faster -- a caller who needs the fallback to reliably complete on this box should raise --budget above ~95-100s, disclosed here rather than silently discovered.", "rule_P": "N/A -- comp-which carries no --page/--limit pagination of its own to be MET or unmet (BOUNDS: not touched)", "rule_T": "MET (this cell) for BOTH qualifying subprocesses -- carrier, expiry disclosure (both sub-branches), shared-clock cumulative budgeting, and the WITHIN BUDGET completion all exercised live on the real binary; the non-application half (comp-which's own scoring work is unbudgeted) stated honestly"}
  },

  "passcraft": {
    "recon": "comp-passcraft recon comp-which -- MOVES 1-3 auto-observed (kind: self+delegate via comp_route.py fail-safe; write_surface: org/mcp/comp-which-rail.log + org/mcp/comproute-routing.jsonl; cache_oracle_signals: the per-invocation .comp-graph/which/rank-<N>.yaml dump, gitignored, not a stale-serving cache); MOVES 4-8 hand-run below",
    "moves_1_to_8": [
      {"move": 1, "status": "DONE", "falsifier_answer": "the shim IS the primary engine (2,439 lines) but genuinely DELEGATES to comp_route.py/comp_capability_provider.py/comp_which_signals.py at runtime for the DR2 posterior -- a real second layer, not a shim-over-nothing, wrapped in a fail-safe (comp_route error -> None -> legacy cascade, never a crash) -- confirmed by reading the try/except in _default_router()"},
      {"move": 2, "status": "DONE", "falsifier_answer": "write surface: org/mcp/comp-which-rail.log (own _log_rail, every mode incl. --route-only per its own guard) + org/mcp/comproute-routing.jsonl (the training-queue flywheel, _emit_training_row) + org/mcp/comp-tool-runs.jsonl (self-report, this cell's Rule T subprocess) -- three sinks, all fire-and-forget, 0 consumers broken by a missing row per each one's own docstring"},
      {"move": 3, "status": "DONE", "falsifier_answer": "no PERSISTENT cache; the .comp-graph/which/rank-<N>.yaml dump is a per-invocation SIDE FILE (a full ranking export for a human to open), gitignored, never read back by comp-which itself on a later call -- confirmed: 0 hits for reading that path back inside the tool's own source"},
      {"move": 4, "status": "DONE", "falsifier_answer": "target universe FROM SOURCE: `comp-which --surfaces` prints '80 tools' at one measurement and the SHAPE section of a plain digest reports '79 of N scored' at another -- both independently cross-checked against org/modules/graph/comp-coverage-map.yaml's own tool count (99 homed tools total, ~79-80 of which are routable per EXCLUDE sets), a non-sharing instrument"},
      {"move": 5, "status": "DONE", "falsifier_answer": "the answer-state branches (decisive route / no_fit fuzzy-guess / near-tie disambiguation / data-view) verified from the OUTPUT differing structurally (a MATCHES block with/without the NO-CURATED-RULE banner, a near-tie banner, or no MATCHES block at all), not asserted by name; the two Rule T ceiling branches (pre-flight SKIP vs TimeoutExpired) verified the same way on the real binary, both directions"},
      {"move": 6, "status": "DONE", "falsifier_answer": "the ONLY mutation this cell performed was on the routing-test HARNESS itself (build_mirror()'s aux-copy list, a genuine bug fix, not a test mutant) plus the MUTANT-BUDGET-equivalent already covered by the routing-test's own pre-existing mutation_test() (all-zero/all-nine scorer mutants, both fired-as-expected, unrelated to this cell's change and re-confirmed still passing); no mutation of comp-which's own production bytes was needed to exercise Rule T, since the ceiling is a runtime flag"},
      {"move": 7, "status": "DONE", "falsifier_answer": "ground truth from a NON-SHARING instrument: `time python .tools/comp-find <term>` run DIRECTLY (not through comp-which) measured 82.759s wall-clock for the identical unscoped query, independent of comp-which's own internal timing/Clock -- this is what grounds the 'not a regression' finding, not comp-which's own self-report"},
      {"move": 8, "status": "DONE", "falsifier_answer": "archetype hand-classified below; lead probes hunted: guard-asymmetry (PASS -- gibberish routes to no_fit/fallback, a real curated question routes decisively, both directions confirmed live), success-token-bound-to-wrong-step (rc stays 0 across WITHIN BUDGET / BUDGET REACHED / no_fit / disambiguation by design, matching every prior T-1/T-2 finding, disclosed not hidden), skip-on-missing-field (FOUND, twice, both caught and fixed BEFORE any commit -- see below), resource-blind (the SUBJECT_ABSENT_FROM_CORPUS finding, F2: the verdict does NOT change when the resource -- the gold-script id -- is fake vs real, and it MUST), undiscriminating/constant-gate (clean -- MATCHES scores demonstrably vary with input across every probe)"}
    ],
    "archetype": "HYBRID -- a GRADED-MEASUREMENT instrument (rc bound to execution, not outcome, same class as comp-find/comp-read/comp-adversary) LAYERED OVER a semantic ROUTER whose own correctness axis (does it recommend the RIGHT tool) is measured by a wholly separate instrument (.tools/comp-which-routing-test.py, NFRA_COMPASSURANCE) that this cell does not re-litigate -- BOUNDS: routing semantics unchanged, re-verified via that harness after this cell's edits (T3-AC4).",
    "findings": [
      {"id": "F1", "shape": "no layer-provenance disclosure", "cite": ".tools/comp-which:_default_router()/main() @e8f67c34f5", "text": "no printed output states WHICH layer decided a route -- curated rule, DR2 posterior (comp_route.py), manifest-fuzzy backstop, or the legacy fail-safe cascade -- so two byte-identical decisions reached by different mechanisms (one confidently, one via fail-safe after an internal error) are indistinguishable to the reader"},
      {"id": "F2", "shape": "resource-blind / SUBJECT_ABSENT_FROM_CORPUS masked by confidence (the MORE SERIOUS finding this cell surfaced)", "cite": ".tools/comp-which:~2116 GOLD_ID special-case @e8f67c34f5 (unchanged by this cell)", "text": "a syntactically-valid but non-existent gold-script ID (confirmed via an independent comp-find census: 0 hits anywhere in the estate) is routed with a forced high curated score (2.00, comp-pipescript io A_99z), identical in shape to a routed decision for a REAL gold script -- the router validates the ID's SHAPE, never its EXISTENCE. An agent trusting this route would hand a downstream tool a subject that does not exist, with zero warning."},
      {"id": "F3", "shape": "skip-on-missing-field, THIS CELL'S OWN, caught before it ever shipped (mirrors CE-t-2's own --hud finding)", "cite": ".tools/comp-which:_self_report() first draft, this cell's own build", "text": "an early draft printed the Rule T status line unconditionally from _self_report() for EVERY mode, including --route-only, which comp-which's OWN docstring documents as a hard side-effect-free contract ('no rail row, no telemetry row either'). Caught by re-reading that exact docstring before commit -- _ROUTE_ONLY's early return in _self_report() already sat above where the new print would have landed, so no live regression ever occurred, but the near-miss is recorded because the SAME class of bug shipped once already in this project (CE-t-2's --hud) before being caught by testing rather than by reading."},
      {"id": "F4", "shape": "missing test-harness sibling dependency, caught by this cell's own T3-AC4 exercise, fixed", "cite": ".tools/comp-which-routing-test.py:build_mirror() @e8f67c34f5", "text": "the routing-test's sandbox mirror copies comp-which's runtime sibling files but did not know about the new _compbudget.py dependency this cell introduces -- the harness's OWN positive-control mirror invocation (a real subprocess) crashed on ModuleNotFoundError before reaching main(), which the harness's own v4 no-pollution alibi correctly flagged (INSTRUMENT FAILED, exit 2, 'MIRROR CAPTURES NOTHING'). FIXED in this cell (added _compbudget.py to the aux-copy list); re-run confirmed VERDICT PASS with identical score distributions to the pre-fix run."}
    ]
  },

  "usage": {
    "runs_30d": {
      "runs_jsonl": {"count": "TO's own issuance-time figure: 520 rows at org/mcp/comp-tool-runs.jsonl (device-local, gitignored)", "note": "not independently re-measured this cell; this session's own exercise adds a device-local increment on top, not re-baselined"},
      "rail_log":   {"count": "TO's own issuance-time figure: 9,643 rows at org/mcp/comp-which-rail.log (device-local, gitignored); this cell's OWN routing-test runs independently measured 9,062-9,100 ROUTE-family rows carrying a q= field at the SAME instrument, in the same range", "note": "the two figures are not directly comparable grains (all rows vs ROUTE-family-with-q rows); both denominators stated, neither reconciled to a single number"}
    },
    "hook_driven": {"fraction": "not independently re-measured this cell; comp-tool-hud.sh:291 is a documented live consumer (comp-which --route-only) per the routing-test's own AC14 finding -- a real, exercised hook-driven caller, not asserted from memory"},
    "battery": {
      "files": [{"path": ".tools/comp-which-routing-test.py (1,608 lines, was 1,600 -- +10 for the build_mirror() fix, matching this cell's ONE code fix in its own lane per BOUNDS)", "collects_under_pytest": "N/A -- a standalone script, not a pytest module (`python .tools/comp-which-routing-test.py --binary-ref WORKING`, ~5-6 minutes wall-clock: 79-80 self-route verdicts up to a 20s watchdog each, 40 gibberish probes, ~740 distinct cohort-R questions through the mirror)", "red_first_mutant": true, "mutant_forms": "the routing-test's OWN pre-existing mutation_test() (all-score-zero collapses the positive control; all-score-nine fires the gibberish control) -- unchanged by this cell, re-confirmed FIRED-AS-EXPECTED both runs"}],
      "file_grain_result": "run 1 (BEFORE the build_mirror() fix): VERDICT *** INSTRUMENT FAILED (exit 2) *** -- 'the harness POLLUTED the rail log' via the v4 alibi's positive-control limb reading 0 mirror rows (MIRROR CAPTURES NOTHING) instead of >=1, root-caused to the missing _compbudget.py sibling in the sandbox (F4). run 2 (AFTER the fix): VERDICT PASS -- controls held (positive/gibberish@rules/r1-anticontrol/both mutation directions all PASS), zero pollution (mirror rail rows from the sweep: 0 SILENT by design; from the positive control: 1, capture path PROVEN), comp-which abstained on 100% of 40 generated gibberish probes. Score distributions IDENTICAL across both runs where the instrument's own controls held: R_raw zero=170/562 (30.2%), R_strict zero=164/556 (29.5%), cohort C zero=12/87 (13.8%), cohort G zero=40/40 (100%) -- confirming BOUNDS (routing semantics unchanged) independent of whether the mirror bug was present, since that bug affected only the CONTROL's own alibi-check, never the sweep's routing measurements themselves.",
      "lane_sweep": "N/A for .tools/tests/ -- this cell's lane is .tools/comp-which + .tools/comp-which-routing-test.py + .tools/** per the TO; the .tools/tests/ directory-grain census (CTO's F6 files) is CE-t-1/CE-t-2's own carried finding, not re-run here (unchanged, not this cell's)."
    },
    "overlap": "comp-which is the ONE router; its own fallback delegates to comp-find (not comp-grep/comp-glob, which remain live-but-unrouted per the same migration comp-find's own T-1 result documented)",
    "proposed": "CLEARED-candidate for Rule T specifically (T3-AC1..AC6 as measured above); the project-wide CLEARED disposition is CVO's grade to render. Four findings (F1-F4) named above: F1 (no layer-provenance disclosure) and F2 (SUBJECT_ABSENT_FROM_CORPUS masked by a confident score -- the most consequential finding across all three cells so far, a real wrong-object risk) are both PRE-EXISTING, not introduced by this cell, and NOT fixed here (BOUNDS: routing semantics do not change); F3 (this cell's own near-miss, caught pre-commit) and F4 (a real bug in the test harness, caught by exercising T3-AC4 and FIXED in this cell's own lane) are both closed."
  }
}
```

## The four planted answer-state cases, quoted

**SUBJECT_ABSENT_FROM_CORPUS** -- a well-formed but non-existent gold-script ID, rc 0:
```
comp-which "what does gold script A_99z read and write"
  MATCHES (top 3 of 79 -- score is overlap, NOT a confidence):

  1. score 2.00   comp-pipescript io A_99z
                gold-script DAG -- intra-pipeline I/O (reads/writes), chains, column-gaps, portal consumers
```
`comp-find --name '*A_99z*'` and `comp-find 'A_99z' graph-call-manifest.yaml`: both **0 hits** -- this
subject does not exist anywhere in the estate. The router does not know, and does not say.

**PRESENT_WITH_ZERO_RESULTS** -- a real historical no-match probe, reproduced live, rc 0:
```
comp-which "asdfqwerzxcv nonsense control question"
  !! NO CURATED RULE MATCHED THIS QUESTION -- READ THIS BEFORE THE LIST BELOW.
     Every candidate scored below the vetted band. These are FUZZY GUESSES, not a
     routing decision. If none of the descriptions answer your question, THE CATALOG
     DOES NOT COVER IT -- do not pick one because it was ranked first.

  MATCHES (top 3 of 79 -- score is overlap, NOT a confidence):
  1. score 0.57   comp-similar ...
```
Rail-logged as `NOFIT-POSTERIOR` (confirmed: 21 occurrences in the live log at cut).

**PARTIAL_OR_BLIND** -- a real historical near-tie probe, reproduced live, rc 0:
```
comp-which "registry narrative vs project json"
  near-tie -- the surface-aware router surfaces these; pick by concern (never a silent guess):

  MATCHES (top 3 of 79 -- score is overlap, NOT a confidence):
  1. score 1.50   comp-registry sync ...
  2. score 1.50   comp-state ...
  3. score 0.51   comp-platinum ...

  *** TOP SCORES ARE TIED -- THE ORDER IS NOT A RANKING. Read the descriptions. ***
```
Second specimen, code-level (this cell's own Rule T): `BUDGET REACHED: ...; scanned 0 of 1
fallback_primitive_call; ...` -- names exactly which unit did not complete.

**NOT_APPLICABLE** -- a data-view request, not a routing question, rc 0:
```
comp-which --surfaces
comp-which surface-first taxonomy (from org\modules\graph\comp-coverage-map.yaml):

LOCAL   high-level: comp-heat drift
  - comp-heat  estate-OBJECT write-freshness + uncommitted-write drift ...
```
No MATCHES block, no score, no answer-state machinery invoked -- a correct result no
answer-state remedy would move.

## Rule T, exercised end to end (the code change this cell owed)

Healthy default (curated match, no fallback reached):
```
comp-which "what breaks if I change this function"
  ...
  WITHIN BUDGET: scanned 1 of 1 telemetry_call; budget: 90 s (default), used 0.89 s
```
Forced fallback at the DEFAULT budget -- measured, real-binary near-timeout (not synthetic):
```
comp-which "grep the repo for ZZZ_NONEXISTENT_TOKEN_0903"
  ...
  comp-which: WARN: comp-find ZZZ_NONEXISTENT_TOKEN_0903 did not finish inside its remaining
  budget and was KILLED. Run it yourself with a narrower scope: comp-find ZZZ_NONEXISTENT_TOKEN_0903
  BUDGET REACHED: 90 s (default); scanned 0 of 1 fallback_primitive_call; results are a PREFIX,
  not the answer; the subprocess did not return within the remaining budget (TimeoutExpired); ...
  BUDGET REACHED: 90 s (default); scanned 0 of 1 telemetry_call; results are a PREFIX, not the
  answer; the self-report subprocess was SKIPPED, not run; ...
```
Direct, non-comp-which measurement of the SAME query (the ground truth this finding rests on):
```
$ time python .tools/comp-find ZZZ_NONEXISTENT_TOKEN_0903
real  1m22.759s
DENOMINATOR: 4 hit(s) across 146464 file(s) scanned in scope [corpus=all]
```
**82.759s > the OLD fixed FALLBACK_TIMEOUT_S=60 -- this exact call would ALSO have been killed
under the pre-Rule-T code. Not a regression.**

Forced fallback with headroom -- both units complete on the shared clock:
```
comp-which "grep the repo for ZZZ_NONEXISTENT_TOKEN_0903" --budget 110
  WITHIN BUDGET: scanned 1 of 1 fallback_primitive_call; budget: 110 s (flag), used 89.53 s
  WITHIN BUDGET: scanned 1 of 1 telemetry_call; budget: 110 s (flag), used 89.62 s
```
Forced tiny budget (0.001s) -- BOTH sub-branches reachable, depending on elapsed time at the check:
```
# fast read reaches the check before elapsed time exceeds the budget -> subprocess attempted, times out:
BUDGET REACHED: 0.001 s (flag); ...; the subprocess did not return within the remaining budget
(TimeoutExpired); ...

# slower read (more upstream router work) -> elapsed already exceeds budget at the check -> never attempted:
BUDGET REACHED: 0.001 s (flag); ...; the fallback was SKIPPED, not run; ...
```

## The test-harness fix (F4), exercised

Run 1, BEFORE `build_mirror()` knew about `_compbudget.py`:
```
mirror rail rows from POSITIVE CONTROL 0   *** MIRROR CAPTURES NOTHING -- empty is not silence ***
VERDICT: *** INSTRUMENT FAILED (exit 2) *** -- the harness POLLUTED the rail log.
```
Run 2, AFTER the fix (this cell's own commit):
```
mirror rail rows from POSITIVE CONTROL 1   capture path PROVEN
VERDICT: PASS -- controls held, zero pollution, and comp-which ABSTAINED on 100% of generated gibberish.
```
Score distributions identical across both runs (R_raw 170/562, R_strict 164/556, C 12/87, G 40/40) --
routing semantics unaffected by either the bug or its fix, satisfying BOUNDS.

## Findings F1-F4

See `passcraft.findings` in the JSON block above. F1 and F2 are pre-existing, carried, not fixed
under this TO's BOUNDS (routing semantics do not change) -- F2 in particular is named as the most
consequential finding across all three CE-t cells run so far in this project (a real wrong-object
risk: the router treats a fabricated subject exactly like a real one). F3 (this cell's own
near-miss) and F4 (a real, fixed bug in the test harness) are both closed.

## Captures and controls

Every quoted run above is a direct execution captured in this session (not a paraphrase); the
82.759s ground-truth measurement was independently re-derived via a DIRECT, non-comp-which
instrument (`time python .tools/comp-find <term>`), never comp-which's own self-timing. Production
sha256: `.tools/comp-which` was `a07568879664a043d3a82ebf150e3e5f3dc8dfe8dff221e7b589a5294f238d4d`
at HEAD `dffbee781c` (before this cell), `a365b828bd4e8cb99dc242f94983b5897d23cf2c9a6dea896b54df5351743166`
at HEAD `e8f67c34f5` (after this cell's rework) -- two MEASURED points. `git status` at write time
shows only this deliverable + its proof-of-spec instance pending beyond the already-landed code
commit (plus unrelated pre-existing uncommitted files elsewhere in the tree, present before this
session started, untouched -- this is a SHARED multi-agent working directory, confirmed by
concurrent commits from other seats observed mid-session). Push state, MEASURED (ls-remote +
is-ancestor), reported in the commit report per T3-AC6, not asserted here.
