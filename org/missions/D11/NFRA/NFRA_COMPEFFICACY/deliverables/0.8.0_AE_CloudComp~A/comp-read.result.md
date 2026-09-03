# comp-read -- NFRA_COMPEFFICACY per-tool result (PRD v0.4 s.4 schema)

Schema: `org/missions/D11/NFRA/NFRA_COMPEFFICACY/prd/NFRA_COMPEFFICACY_PRD.md` v0.4 @`19bf1c7322` s.4
(landed by `1.0.0_SA_CTO`; s.4.3's four answer-state spellings ratified as DATA at
`org/standards/COMPTOOL_ANSWER_STATE.enum.json`; s.4.4 "RULE T's FORM" is the grammar this cell applies).
Row: T-2 (manifest s.7). Cell: CE-t-2 (decomp v0.2 @`f54000091d`). Measured by `0.8.0_AE_CloudComp~A`,
2026-09-03T04:44Z-05:20Z, read-vintage HEAD @`f4eb799c2b`, engine @`f4eb799c2b` (this cell's own commit --
the deliverable follows the fix, per the TO's ONE-deliverable-ONE-code-change circle, mirroring the
precedent: `org/missions/D11/NFRA/NFRA_COMPEFFICACY/deliverables/0.8.0_AE_CloudComp/comp-find.result.md`
@`6d04680f2b` + the reworked comp-find @`2718cffc45`, the reference application of Rule T's form). Every
value below is MEASURED on this box unless its own field says otherwise; every run's full output is
quoted from a saved capture, never from memory. **No surprise rows filed this cell** -- no spec-vs-world
divergence surfaced (all findings below are ordinary code-behavior gaps discovered BY the audit, the
TO's own purpose, not a world state the spec failed to anticipate).

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.4 @19bf1c7322 s.4",
  "row": "T-2",
  "measured_by": "0.8.0_AE_CloudComp~A",
  "measured_at_utc": "2026-09-03T04:44Z..05:20Z",
  "read_vintage": "HEAD @f4eb799c2b",
  "surprises": [],

  "identity": {
    "tool": "comp-read",
    "shim_path": ".tools/comp-read (1,145)",
    "engine_path": ".tools/comp-read (1,145) -- SELF-CONTAINED: 0 delegate-engine imports; imports two SIBLING helpers (_comprail.py, the shared rail primitives, GUARDED -- 'never block a read on the rail'; _compbudget.py, the shared Rule T carrier this cell wired, UNGUARDED, mirroring comp-find's own import of it) -- neither is a second engine, both are libraries the shim itself is the engine that calls",
    "engine_vintage": "f4eb799c2b (2026-09-03T01:16:54-04:00 = 2026-09-03T05:16:54Z)",
    "aliases": [],
    "aliases_note": "no sibling tool comp-read is meant to replace or that replaces it -- unlike comp-find/comp-grep/comp-glob, comp-read's file-content-grain mode has no predecessor (PRD/decomp: 'the carve-out existed because no comp-tool covered file internals').",
    "purpose_1line": "KEY-CONTEXT READ: shows the SHAPE, SALIENT regions, QUALIFIERS, CONTRADICTIONS and an UNREAD LEDGER for ONE file; --enumerate answers comp-find's question at file-content grain  [engine docstring :1-9]",
    "self_identifies": {
      "help_prints_name_and_version": false,
      "help_prints_engine_path": false,
      "version_flag": "UNSUPPORTED -- not a recognized flag; falls through to the positional-file slot. Measured: `comp-read --version` and `comp-read -v` both return rc 2, 'comp-read: ERROR: not a file: --version' / '-v'. CONTRAST WITH comp-find's identical gap (its own T-1 result, F1): comp-find's --version silently returns real-looking search hits (a footgun); comp-read's --version cleanly ERRORS. Same absence, opposite safety.",
      "output_line_1": "comp-read <file> [--for \"<question>\"] [--at LINE] [--top N] [--all-quals] [--budget N]  (dynamic per invocation; no static version banner exists anywhere in the tool)",
      "grade": "ABSENT -- no version identity anywhere in the tool, but --version fails LOUD (rc 2), not silently, unlike comp-find's sibling gap"
    },
    "registration": {
      "graph_call_manifest": "PRESENT -- org/modules/graph/graph-call-manifest.yaml:374-380 (canonical_call, cost '2-7ms typical; ~105ms on a 3.7k-line python module', anti_pattern), :1796 (does/notes). STALE in the same shape comp-find's own entry was: none of --enumerate, --budget, --hud, --limit, --page is named -- the manifest's canonical_call is the pre-enumerate, pre-Rule-T single-question form only.",
      "comp_tools_yaml": "ABSENT (0 hits / 1 file scanned, org/modules/graph/comp-tools.yaml) -- same shape as comp-find's T-1 finding: not a routing gap (comp-read is Rule 21's own mandated single-file instrument, not a purpose-routed catalog entry).",
      "skill": ".claude/skills/comp-read/ -- ABSENT (0 files across 86 scanned, 8 ephemeral-floor) -- comp-which's inline text + graph-call-manifest.yaml are the only documented interfaces."
    }
  },

  "disclosure": {
    "run": "DEFAULT flags, `comp-read .tools/_compbudget.py` -- rc 0, 20 lines stdout incl. the new Rule T line, 0 stderr (quoted below)",
    "subject":             {"grade": "PRESENT", "quoted": "comp-read: .tools/_compbudget.py", "note": "unlike comp-find (pattern echoed, pathspec never echoed), comp-read's ONE positional IS the subject, so the header line names it directly -- no analogous gap."},
    "corpus_or_backend":   {"grade": "PRESENT", "quoted": "123 lines | 11 section(s) via python-ast | question: (none given)", "note": "the 'via <backend>' clause is comp-read's corpus/backend disclosure -- python-ast / markdown-headings / top-level-keys / whole-file / UNPARSEABLE-python, always stated."},
    "vintage":             {"grade": "ABSENT", "quoted": "no run prints a git HEAD sha, mtime, or working-tree-dirty flag -- SAME finding as comp-find's file-corpus gap (this tool's own docstring's answer: 'NO MODEL. NO EMBEDDINGS. NO NETWORK. NO CACHE ... A cacheless tool also cannot serve a stale vintage -- the UNKNOWN-VINTAGE class simply does not exist here'). Read-only-live-file-at-invocation-time makes vintage a NON-QUESTION by construction, not an omission -- two runs against different commits differ only in the bytes actually read, never silently."},
    "denominator":         {"grade": "PRESENT", "quoted": "ENUMERATE: 0 hit(s) across 123 lines / 11 section(s) scanned  (--enumerate mode) | SHAPE (all N, never truncated) / UNREAD LEDGER: you have been shown M of N line(s) and P of Q section(s)  (digest mode)"},
    "resolved_unresolved": {"grade": "PRESENT", "quoted": "'UNPARSEABLE-python (syntax error) -- fell back to top-level-keys' / 'BANDS: UNAVAILABLE for this backend ... ONE band is printed rather than typed rows of 0' -- both name WHICH PART could not be examined"},
    "blind_spots":         {"grade": "PRESENT", "quoted": "'!! UNPARSEABLE: ... the AST-backed panels are BLIND here: docstring AUTHORITY tagging degrades to AUTHORITATIVE and CONTRADICTIONS reports none because it could not look, NOT because there are none.' -- an explicit BLIND-not-clean disclosure, printed whenever a .py fails to parse"},
    "pagination":          {"grade": "PRESENT", "quoted": "PAGE 1 of 1  (showing 9 of 9)  -- true total, not the page's (--enumerate mode only; the digest mode's SHAPE/UNREAD LEDGER panels are the pagination-shaped disclosure there, per Rule 21's page-is-not-an-answer)"},
    "timeout":             {"grade": "PRESENT (this cell)", "quoted": "'WITHIN BUDGET: scanned 1 of 1 telemetry_call; budget: 90 s (default), used 0.12 s' or 'BUDGET REACHED: 0.001 s (flag); scanned 0 of 1 telemetry_call; ... the self-report subprocess was SKIPPED, not run; NO CURSOR: ...'", "before_this_cell": "PRESENT-BUT-WRONG -- :1030 (pre-rework line) hard-coded timeout=20, invisible to the caller, nothing printed at expiry (measured, TO-CE-T-2 issuance). comp-read carries NO corpus-width loop -- the whole read/enumerate/hud path itself has no timeout at all (a syntax-heavy 14.9 MB file would simply take however long ast.parse takes); the ONE budgeted subprocess is exclusively the post-hoc self-report telemetry sink."}
  },

  "answer_state": {
    "schema_note": "Spellings per the RATIFIED enum (PRD v0.4 s.4.3, org/standards/COMPTOOL_ANSWER_STATE.enum.json): SUBJECT_ABSENT_FROM_CORPUS, PRESENT_WITH_ZERO_RESULTS, PARTIAL_OR_BLIND, NOT_APPLICABLE. GRAIN NOTE: comp-read's 'corpus' for these four cases is the ONE FILE given as its positional argument (there is no pathspec/scope the way comp-find has one) -- SUBJECT_ABSENT_FROM_CORPUS is therefore about the FILE PATH, not about a pattern inside it.",
    "SUBJECT_ABSENT_FROM_CORPUS": {"planted": "comp-read ZZZ_NONEXISTENT_FILE_0903.txt (the file path itself does not exist)", "printed": "comp-read: ERROR: not a file: ZZZ_NONEXISTENT_FILE_0903.txt", "rc": 2, "finding": "POSITIVE CONTRAST WITH comp-find's T-1 finding F4: comp-find silently degrades an absent pathspec to a 0-files-scanned run (no error at all, only the second DENOMINATOR number distinguishes it); comp-read instead FAILS LOUD with an explicit ERROR line and a non-zero rc. No silent-degrade gap here."},
    "PRESENT_WITH_ZERO_RESULTS":  {"planted": "an absent enumerate token in a real, existing file (.tools/_compbudget.py)", "printed": "ENUMERATE: 0 hit(s) across 123 lines / 11 section(s) scanned ... 0 hit(s). THE DENOMINATOR ABOVE IS THE POINT -- this file WAS scanned and the pattern is absent from it.", "rc": 0, "distinguishable_from_absent_by": "rc alone (2 vs 0) plus the presence/absence of the ERROR line -- comp-read does not need a numeric-denominator trick the way comp-find's '0 vs N files' does, because the file-not-found case is a hard error here"},
    "PARTIAL_OR_BLIND":           {"planted": "a syntax-broken .py fixture (`def broken(:` -- unbalanced paren)", "printed": "!! UNPARSEABLE: this .py did NOT parse. The SHAPE below is a TEXT fallback, not the module's real structure, and the AST-backed panels are BLIND here: docstring AUTHORITY tagging degrades to AUTHORITATIVE and CONTRADICTIONS reports none because it could not look, NOT because there are none. Read the file directly.", "rc": 0, "says_which_part": true, "second_specimen_this_cell": "the --enumerate HONEST-DEGRADE case (a no-structure backend: 'BANDS: UNAVAILABLE for this backend ... ONE band is printed rather than typed rows of 0, which would claim the distinction was tested') -- already covered by the pre-existing battery's arm 5"},
    "NOT_APPLICABLE":             {"planted": "--at 9999 on a 2-line file (a line-pin request that cannot apply -- the file has no line 9999)", "printed": "IDENTICAL output to omitting --at entirely (byte-for-byte apart from the timing/budget-used lines) -- 'SALIENT: (no --for question given; pass one to rank regions)', no mention of --at, no error, no acknowledgment the flag was even parsed", "rc": 0, "declared_by_tool": false, "control": "diff of `comp-read tiny.py --at 9999` vs `comp-read tiny.py` (no --at at all): only the timing line and the trailing Rule T 'used <t> s' figure differ; every other byte is identical", "finding": "F1 (this cell): comp-read has NO NOT_APPLICABLE voice for --at beyond the file's own line range -- it is silently dropped, indistinguishable from --at never having been given. SAME SHAPE as comp-find's own F3 (a cross-corpus band category error prints identically to a genuine zero-hit real category) -- neither tool in this project has grown a NOT_APPLICABLE word of its own yet."},
    "verdict": "PASS on the PRD criterion as measured (T2-AC2): the four planted cases produce four DISTINGUISHABLE, machine-rejectable outputs in the tool's own voice (rc 2 vs 0, an explicit ERROR line, an explicit UNPARSEABLE/BLIND disclosure, and a byte-diff against the no-flag baseline) -- one finding stands (F1, --at's silent NOT_APPLICABLE gap), not blocking, not fixed here per BOUNDS (read semantics do not change)."
  },

  "bounds": {
    "subprocess_timeouts": [
      {"file_line": ".tools/comp-read:~1086,~1109 @f4eb799c2b", "value_s": "clock.remaining() -- derives from the resolved --budget/env/default (90s default) via a Clock STARTED in main() before any read work, never a fixed constant", "wraps": "python org/modules/graph/comp_log_auto.py comp-read <argv> <rc>  (the self-report telemetry sink, fire-and-forget) -- the ONLY timeout-carrying subprocess in the tool; comp-read's own read/enumerate/hud path has NO subprocess and NO timeout at all", "before_this_cell": ":1027-1030 (pre-rework HEAD @f34122edfb) hard-coded timeout=20, invisible to the caller, nothing printed at expiry"},
      {"file_line": ".tools/comp-read:~1050 @f4eb799c2b", "value_s": 20, "wraps": "the SAME self-report subprocess, but only on the declared non-application path: main() returned before resolving a budget (the --help/-h path only, which does zero read-work) -- UNCHANGED, stated honestly rather than invented a budget for a call with nothing to bound"}
    ],
    "ceiling_behaviour": {
      "exercised": true,
      "how": "the REAL PRODUCTION BINARY, no mutant needed to force the ceiling (it is a caller flag now, not a constant, so exercising it touches zero bytes) -- mirrors comp-find's T-1 exercise exactly",
      "healthy_default": "`comp-read .tools/_compbudget.py` (no --budget) -> 'WITHIN BUDGET: scanned 1 of 1 telemetry_call; budget: 90 s (default), used 0.12 s'; rc 0",
      "forced_fast_read": "`comp-read .tools/_compbudget.py --budget 0.001` (a 123-line file, ~2ms total runtime) -> the Clock's remaining() is STILL barely positive at the pre-flight check (elapsed-so-far < 1ms), so subprocess.run is attempted with that sliver of a timeout and itself raises TimeoutExpired -> 'BUDGET REACHED: 0.001 s (flag); scanned 0 of 1 telemetry_call; ... the self-report subprocess did not return within the remaining budget (TimeoutExpired); NO CURSOR: ...'; rc 0. REPRODUCED 3/3 on repeat.",
      "forced_slow_read": "`comp-read .tools/comp-read --budget 0.001 --for \"budget\"` (comp-read reading ITSELF, ~24ms total runtime) -> elapsed-so-far already EXCEEDS the 1ms budget by the time _self_report checks remaining(), so the subprocess is never even attempted -> 'BUDGET REACHED: 0.001 s (flag); scanned 0 of 1 telemetry_call; ... the self-report subprocess was SKIPPED, not run; NO CURSOR: ...'; rc 0. REPRODUCED 3/3 on repeat.",
      "unbounded": "`--budget 0` -> 'WITHIN BUDGET: scanned 1 of 1 telemetry_call; budget: unbounded (--budget 0), used 0.11 s'",
      "bad_value": "`--budget -5` -> 'comp-read: ERROR: --budget budget must be >= 0 (0 = unbounded), got '-5''; rc 2 -- wording copied verbatim from the reference application (comp-find's own error string), a deliberate consistency choice, not an accidental redundancy",
      "design_finding": "the Clock's placement is load-bearing and was CAUGHT AND FIXED live in this cell's own build: creating it INSIDE _self_report() (adjacent to its own remaining() check, mirroring nothing in comp-find since comp-find's Clock lives at the top of a real corpus-width loop) made the pre-flight SKIP branch structurally unreachable -- remaining() checked immediately after Clock() is always still ~budget_s. Moving Clock() into main(), started BEFORE any read/enumerate/hud work, is what makes BOTH BUDGET REACHED sub-branches (pre-flight SKIP vs subprocess TimeoutExpired) genuinely reachable, and both are now exercised above on the real binary, not a mutant.",
      "hud_regression_caught_and_fixed": "--hud's own documented contract is FIRE ONLY WHEN THERE IS SOMETHING WORTH SAYING, ELSE ZERO BYTES. An early draft of this cell's own build printed the Rule T status line unconditionally from _self_report() regardless of mode, which broke that contract on every clean file (a silent HUD run went from 0 bytes to ~85 bytes). Found before commit (a genuinely clean fixture round-tripped through `--hud`, byte count measured, non-zero), fixed by suppressing (not skipping) the printed line in hud_mode while the underlying budgeted subprocess call still runs -- Rule T's CODE effect stays unconditional, only the DISCLOSURE line is mode-scoped. Re-verified zero bytes after the fix."
    },
    "page_contract": {"page_flag": true, "limit_flag": true, "all_flag": false, "true_total_printed": true, "cap_flags": "--budget N (new, this cell); --limit N / --page N (--enumerate mode only, pre-existing)", "help_discloses_flags": "PRESENT -- --help documents --budget's carrier/precedence/default in the same block as --enumerate/--limit/--page", "note": "T-2 does not touch --enumerate's own pagination (BOUNDS: read semantics and pagination do not change; the 8-arm battery is the control, now 10 arms, the original 8 byte-for-byte unaffected)."},
    "size_invariance": {"work": "comp-read has NO corpus-width loop by construction (ONE file per call, one AST pass, compiled-regex sweeps) -- Rule T's carrier therefore governs exactly ONE unit ('telemetry_call'), never a corpus-width count. This IS the stated non-application: with no loop, there is no scan denominator to manufacture, and the tool prints the form's line for its class (a single indivisible unit) rather than inventing one.", "time": "the read/enumerate/hud work ITSELF remains UNBUDGETED and unbounded by this cell (BOUNDS forbid touching read semantics) -- a pathological file (huge, deeply nested) could still take however long ast.parse/re.finditer take; only the POST-HOC telemetry subprocess is now budgeted. Stated honestly as a real scope boundary, not hidden.", "rule_P": "MET, unchanged (pre-existing --enumerate pagination)", "rule_T": "MET (this cell) for the tool's one qualifying subprocess -- carrier, expiry disclosure, both BUDGET-REACHED sub-branches all exercised live on the real binary; the non-application half (no corpus-width loop exists to budget) stated in the class the form names, per PRD s.4.4 and this TO's own wording"}
  },

  "passcraft": {
    "recon": "comp-passcraft recon comp-read -- rc 0, MOVES 1-3 OBSERVED by the helper (kind: self, backends: (self-contained); write_surface: none matched by the write-pattern set; cache_oracle_signals: cache, marker/manifest); MOVES 4-8 SLOT, hand-run below",
    "moves_1_to_8": [
      {"move": 1, "status": "DONE", "falsifier_answer": "the shim IS the engine (1,145 lines, self-contained); two sibling LIBRARY imports (_comprail, guarded; _compbudget, unguarded per this cell), no delegate engine"},
      {"move": 2, "status": "DONE", "falsifier_answer": "write surface: org/mcp/comp-which-rail.log (RUN-READ rail row, digest/hud modes only -- pre-existing gap, --enumerate writes none, T2-AC5 below) + org/mcp/comp-tool-runs.jsonl (self-report, every mode) -- both fire-and-forget sinks, 0 consumers broken by a missing row (comp_log_auto.py's own docstring, unchanged: 'never raises: a telemetry sink must never break the tool it measures'). This cell's own Rule T status print is a THIRD, new sink-adjacent output (comp-read's own stdout), and IS a consumer surface: comp-adversary's stage-4 packet embeds comp-read's stdout verbatim (verified below, arm 8 CONSUMER-INTACT) and a live comp-adversary --self-test was run to confirm it still passes with the trailing line present."},
      {"move": 3, "status": "DONE", "falsifier_answer": "no PERSISTENT cache; the auto-observed 'cache' signal is the in-process _TREE_CACHE/_SCAN_CACHE (content-keyed since a prior 2026-08-06 fix, never id()-keyed), scoped to ONE process's lifetime -- each CLI invocation is a fresh process (confirmed: the battery shells out via subprocess.run per call), so it cannot serve a stale vintage across runs; oracle = the live file on disk read at invocation time"},
      {"move": 4, "status": "DONE", "falsifier_answer": "target universe FROM SOURCE: `wc -l .tools/_compbudget.py` -> 123, MATCHING comp-read's own printed '123 lines' header exactly (a non-sharing instrument: shell wc vs. comp-read's own splitlines())"},
      {"move": 5, "status": "DONE", "falsifier_answer": "the FOUR Rule T branches verified from the OUTPUT differing, not chosen by name: WITHIN BUDGET (healthy default, exercised), BUDGET REACHED via pre-flight SKIP (forced-slow-read, exercised, real binary), BUDGET REACHED via subprocess TimeoutExpired (forced-fast-read, exercised, real binary), and the declared-non-application fixed-20s fallback (--help path, exercised: --help's own output carries no trailing Rule T line, confirming the fallback branch, not a fourth Rule T print)"},
      {"move": 6, "status": "DONE", "falsifier_answer": "write surface is the two fire-and-forget log sinks (MOVE 2); no revert-safety needed for a mutant run since MUTANT-BUDGET's mutant copy sits in a tempfile.TemporaryDirectory beside the real tool, never overwrites production, and is confirmed removed (context-manager teardown) after each run"},
      {"move": 7, "status": "DONE", "falsifier_answer": "ground truth from a NON-SHARING instrument: shell `wc -l` (MOVE 4) independent of comp-read's own line-counting code path; separately, the --at-out-of-range finding (F1) was confirmed by a raw `diff` of two captured output files, an instrument outside comp-read's own predicate entirely"},
      {"move": 8, "status": "DONE", "falsifier_answer": "archetype hand-classified below; lead probes hunted: guard-asymmetry (PASS both directions -- a real hit and a real absence both produce correctly distinct shapes), success-token-bound-to-wrong-step (rc stays 0 on BOTH WITHIN BUDGET and BUDGET REACHED by design, matching the T-16/comp-find precedent -- disclosed, not hidden, see F5-equivalent below), skip-on-missing-field (FOUND, this cell's own build, caught before commit -- the --hud unconditional-print regression, fixed), correct-but-unwired (clean -- --help's disclosure and the actual carrier resolution agree, confirmed by direct exercise), undiscriminating/constant-gate (clean -- WITHIN BUDGET vs BUDGET REACHED demonstrably vary with input, arm 9/10 below)"}
    ],
    "archetype": "GRADED-MEASUREMENT instrument (same class as comp-find/comp-adversary): rc bound to EXECUTION, not to hit-count or budget outcome (rc 0 on a real hit, a genuine zero, AND a BUDGET REACHED) -- correct for its contract, and the reason a consumer must read the body, never the rc, for the answer-state axis AND the Rule-T axis.",
    "findings": [
      {"id": "F1", "shape": "NOT_APPLICABLE-voice gap (mirrors comp-find T-1's F3)", "cite": ".tools/comp-read main() --at pin-matching loop @f4eb799c2b", "text": "--at LINE beyond the file's own line range is silently dropped -- output is byte-identical to omitting --at entirely (apart from timing), no error, no acknowledgment the flag was parsed"},
      {"id": "F2", "shape": "carried-forward, named owner, not fixed here (T2-AC5)", "cite": ".tools/comp-read:_enumerate() @f4eb799c2b vs the digest path's _comprail.log_rail call", "text": "an --enumerate run writes NO row to org/mcp/comp-which-rail.log (all-time 0 rows for the mode, unchanged by this cell) -- the rail writer fires on the digest path only. Owner: 0.8.0_AE_CloudComp (this seat, a future pass) -- BOUNDS for THIS TO exclude touching read semantics/instrumentation of the enumerate path beyond the Rule T budget wiring itself."},
      {"id": "F3", "shape": "success-token-bound-to-wrong-step (disclosed, not hidden, matches comp-find's own F5)", "cite": ".tools/comp-read within-budget/budget-reached prints @f4eb799c2b", "text": "rc stays 0 whether the self-report subprocess completed or was SKIPPED/TimeoutExpired (matching the T-16/comp-find precedent and PRD s.4.4's own words 'the LINE is the rejectable state, not the rc') -- a caller checking rc alone cannot see a degraded telemetry call; the token text is REQUIRED reading, stated not hidden. Lower stakes than comp-find's own F5: comp-read's budgeted subprocess is a fire-and-forget telemetry sink, never part of the tool's own answer, so a degraded run here costs a missing usage-metrics row, never a wrong or partial READ."},
      {"id": "F4", "shape": "pre-existing, unrelated to this cell, carried for completeness", "cite": ".tools/comp-read main() `if not argv or argv[0] in (\"-h\",\"--help\")` @f4eb799c2b (unchanged)", "text": "bare `comp-read` with zero arguments is routed to the --help branch, not to the 'ERROR: no file given' branch (which is reachable only when argv is non-empty but carries no positional, e.g. `comp-read --for x`) -- pre-existing since before this cell, not introduced or touched here"}
    ]
  },

  "usage": {
    "runs_30d": {
      "runs_jsonl": {"count": "760+ at last read (device-local, org/mcp/comp-tool-runs.jsonl, gitignored)", "note": "heavily inflated THIS session by this cell's own exercise; not independently re-baselined against the TO's own issuance-time figure"},
      "rail_log":   {"count": "3,129+ hits mentioning comp-read at last read (org/mcp/comp-which-rail.log, occurrence count not row count -- device-local instrument, per CLAUDE.md's own warning)", "note": "the TO's own MEASURED-at-cut figure was 2,401 runs; the gap is largely this session's own traffic plus the occurrence-vs-row grain difference, not independently reconciled"}
    },
    "hook_driven": {"fraction": "not independently re-measured this cell -- comp-adversary's own stage-4 packet is a live, exercised consumer (see battery arm 8), which is the load-bearing usage fact for this row"},
    "battery": {
      "files": [{"path": ".tools/tests/test_comp_read_enumerate.py (now 264 lines, was 222)", "collects_under_pytest": "1 test, ~28-35s (varies; dominated by the ANCHOR-ARM's 14.9 MB specimen read and the two new arms' extra real+mutant comp-read invocations)", "red_first_mutant": true, "mutant_forms": "BAND (pre-existing, arm 7: band classifier neutered) AND BUDGET (new, arm 10: _compbudget.resolve_budget(budget_flag) neutered to always ignore the flag) -- BOTH must RUN (not crash) and then FAIL their sibling arm's own predicate; both DO"}],
      "file_grain_result": "10/10 PASS (the original 8 unchanged: DENOMINATOR, BAND-CONSERVATION, ANCHOR-ARM, ZERO-DENOMINATOR, HONEST-DEGRADE, PAGINATION, MUTANT-BAND, CONSUMER-INTACT -- byte-for-byte the same predicates, confirmed direct AND under pytest -q, TWICE across this cell's edits) -- plus 2 new arms (BUDGET-CARRIER, MUTANT-BUDGET), exceeding the ONE required, mirroring the comp-find T-1 F/G precedent exactly",
      "lane_sweep": "pytest --collect-only .tools/tests/ -> still INTERNALERROR / SystemExit at test_fabric_check_classify.py:76 (one of CTO's three named F6 files), 25 tests collected before the abort -- UNCHANGED from the 2026-09-03 census this seat's sibling ran for CE-t-1 (comp-find), not this cell's, not re-fixed"
    },
    "overlap": "comp-read has no sibling comp-tool covering the same ground -- it is the file-content-grain instrument comp-find/comp-grep/comp-glob do not reach (PRD/decomp's own framing)",
    "proposed": "CLEARED-candidate for Rule T specifically (T2-AC1..AC6 as measured above); the project-wide CLEARED disposition is CVO's grade to render. Four findings (F1-F4) named above, none blocking Rule T's own acceptance; F2/F4 are pre-existing (not introduced by this cell) and are surfaced for the record, not fixed here (BOUNDS: read semantics do not change under this TO); F1 and F3 are genuine gaps this cell's own audit exposed, both disclosed rather than hidden, neither fixed (out of the ONE-code-change circle this TO owes)."
  }
}
```

## The four planted answer-state cases, quoted

**SUBJECT_ABSENT_FROM_CORPUS** -- `comp-read ZZZ_NONEXISTENT_FILE_0903.txt`, rc 2:
```
comp-read: ERROR: not a file: ZZZ_NONEXISTENT_FILE_0903.txt
```

**PRESENT_WITH_ZERO_RESULTS** -- an absent token in a real, existing file, rc 0:
```
comp-read: .tools/_compbudget.py
  123 lines | 11 section(s) via python-ast | enumerate: 'ZZZ_ABSENT_TOKEN_0903'

  ENUMERATE: 0 hit(s) across 123 lines / 11 section(s) scanned
  ...
  0 hit(s). THE DENOMINATOR ABOVE IS THE POINT -- this file WAS scanned and the
  pattern is absent from it. That is a different claim from silence, and from
  'the wrong file was scanned'.
```

**PARTIAL_OR_BLIND** -- a syntax-broken .py fixture, digest mode, rc 0:
```
comp-read: <path>/broken.py
  2 lines | 1 section(s) via UNPARSEABLE-python (syntax error) -- fell back to top-level-keys | question: 'what does this do'
  !! UNPARSEABLE: this .py did NOT parse. The SHAPE below is a TEXT fallback, not the
     module's real structure, and the AST-backed panels are BLIND here: docstring
     AUTHORITY tagging degrades to AUTHORITATIVE and CONTRADICTIONS reports none
     because it could not look, NOT because there are none. Read the file directly.
```

**NOT_APPLICABLE** -- `--at 9999` on a 2-line file, rc 0, side by side with the no-flag baseline:
```
# --at 9999 (out of range):
comp-read: <path>/tiny.py
  2 lines | 2 section(s) via top-level-keys | question: (none given)
  SHAPE (all 2, never truncated):
        1-1     key    a = 1
        2-2     key    b = 2
  SALIENT: (no --for question given; pass one to rank regions)
  ...

# no --at at all, same file:
comp-read: <path>/tiny.py
  2 lines | 2 section(s) via top-level-keys | question: (none given)
  SHAPE (all 2, never truncated):
        1-1     key    a = 1
        2-2     key    b = 2
  SALIENT: (no --for question given; pass one to rank regions)
  ...
```
`diff` of the two captures: only the timing line and the trailing Rule T `used <t> s` figure differ.
Nothing distinguishes "line 9999 does not exist in this file" from "no --at was given at all." This
IS finding F1 -- the tool has no NOT_APPLICABLE word of its own for an out-of-range pin, exactly the
shape of comp-find's own F3 (a cross-corpus band category error reads identically to a real zero-hit
category).

## Rule T, exercised end to end (the code change this cell owed)

Healthy default, no --budget:
```
comp-read .tools/_compbudget.py
  ...
  (2.2 ms | no model, no network, no cache -- so no vintage to be stale)
  WITHIN BUDGET: scanned 1 of 1 telemetry_call; budget: 90 s (default), used 0.12 s
```
Forced ceiling on a FAST read (~2ms total runtime) -- the subprocess is attempted then itself times out:
```
comp-read .tools/_compbudget.py --budget 0.001
  ...
  BUDGET REACHED: 0.001 s (flag); scanned 0 of 1 telemetry_call; results are a PREFIX, not the
  answer; the self-report subprocess did not return within the remaining budget (TimeoutExpired);
  NO CURSOR: this is comp-read's one indivisible timeout-carrying subprocess -- nothing to resume,
  only to re-run with a larger --budget.
```
Forced ceiling on a SLOWER read (comp-read reading itself, ~24ms total runtime) -- already exhausted
before the subprocess is ever attempted:
```
comp-read .tools/comp-read --budget 0.001 --for "budget"
  ...
  BUDGET REACHED: 0.001 s (flag); scanned 0 of 1 telemetry_call; results are a PREFIX, not the
  answer; the self-report subprocess was SKIPPED, not run; NO CURSOR: this is comp-read's one
  indivisible timeout-carrying subprocess -- nothing to resume, only to re-run with a larger --budget.
```
Unbounded:
```
comp-read .tools/_compbudget.py --budget 0
  ...
  WITHIN BUDGET: scanned 1 of 1 telemetry_call; budget: unbounded (--budget 0), used 0.11 s
```
Bad value (negative), rc 2, wording copied verbatim from the reference application:
```
comp-read .tools/_compbudget.py --budget -5
comp-read: ERROR: --budget budget must be >= 0 (0 = unbounded), got '-5'
```
`--help` discloses the carrier:
```
  --budget N    RULE T (PRD s.4.4, shared .tools/_compbudget): ceiling in seconds for
               comp-read's ONE timeout-carrying subprocess (the self-report telemetry
               sink, fired after every run; carrier: --budget > env COMP_BUDGET_S >
               default 90 s, kept under this box's ~120s outer harness ceiling);
               --budget 0 = unbounded. comp-read has NO corpus-width loop, so a
               BUDGET REACHED line is reachable only by a deliberately tiny value
               (e.g. --budget 0.001) -- an ordinary run always prints WITHIN BUDGET.
```

**The non-application, stated honestly (this TO's own words, exercised):** with no corpus-width
loop, comp-read cannot manufacture a scan denominator the way comp-find's per-node_type units do --
there is exactly ONE unit, and both BUDGET REACHED sub-branches (pre-flight SKIP vs subprocess
TimeoutExpired) were exercised above on the real production binary, distinguished by which one fires
depending on how much of the run's OWN elapsed time (never budgeted, per BOUNDS) has already consumed
the caller's ceiling by the time the ONE budgeted subprocess is reached.

**A design defect caught and fixed inside this cell's own build, before it shipped:** the Clock must
be started in `main()` BEFORE any read/enumerate/hud work -- creating it adjacent to its own
`remaining()` check inside `_self_report()` (this cell's first draft) makes the pre-flight SKIP
branch structurally unreachable, since `remaining()` checked immediately after `Clock()` is always
still ~`budget_s`. Separately, `--hud`'s documented zero-bytes-on-silent contract was measured
broken by an unconditional trailing print (0 bytes -> 85 bytes on a clean fixture) and fixed by
suppressing the print (not the underlying budgeted call) in `hud_mode`; re-measured at 0 bytes after
the fix. Neither defect ever reached a commit.

## Findings F1-F4

See `passcraft.findings` in the JSON block above. None blocking Rule T's own acceptance. F2
(`--enumerate` writes no rail row) is carried per T2-AC5 with owner `0.8.0_AE_CloudComp` (a future
pass, not this TO's bound); F4 is pre-existing and untouched by this cell.

## Captures and controls

Every quoted run above is a direct execution captured in this session (not a paraphrase); the
line-count cross-check (`wc -l .tools/_compbudget.py` = 123, matching comp-read's own printed
header) was independently re-derived via a non-sharing instrument (MOVE 4/7). Production sha256:
`.tools/comp-read` was `f69d0b55df760227ae06f833879136ef4aba7819ecd91cc859551fc0737e2d2e` at HEAD
`f34122edfb` (before this cell), `d6f523673f9eb08778ad65ad9ff3d357c63c4b5c87b94cb7fe69f280321a153e`
at HEAD `f4eb799c2b` (after this cell's rework) -- two MEASURED points. `git status` at write time
shows only this deliverable + its proof-of-spec instance pending beyond the already-landed code
commit; unrelated pre-existing uncommitted files elsewhere in the tree (present before this session
started) are untouched. Push state, MEASURED (ls-remote + is-ancestor), reported in the commit
report per T2-AC6, not asserted here.
