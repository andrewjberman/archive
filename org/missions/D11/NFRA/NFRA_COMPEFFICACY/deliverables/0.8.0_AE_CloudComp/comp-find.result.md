# comp-find -- NFRA_COMPEFFICACY per-tool result (PRD v0.4 s.4 schema)

Schema: `org/missions/D11/NFRA/NFRA_COMPEFFICACY/prd/NFRA_COMPEFFICACY_PRD.md` v0.4 @`19bf1c7322` s.4
(landed by `1.0.0_SA_CTO`; s.4.3's four answer-state spellings ratified as DATA at
`org/standards/COMPTOOL_ANSWER_STATE.enum.json`; s.4.4 "RULE T's FORM" is the grammar this cell applies).
Row: T-1 (manifest s.7). Cell: CE-t-1 (decomp v0.1.1 @`ee52600980`). Measured by `0.8.0_AE_CloudComp`,
2026-09-03T02:20Z-03:36Z, read-vintage HEAD @`2718cffc45`, engine @`2718cffc45` (this cell's own commit --
the deliverable follows the fix, per the TO's ONE-deliverable-ONE-code-change circle). Every value below
is MEASURED on this box unless its own field says otherwise; every run's full output is quoted from a
saved capture, never from memory. **Two surprise rows were filed and are open at CVO's L8 as of this
write:** `NFRA_COMPEFFICACY-S1` (the mid-round grammar landing that produced this rework) and
`NFRA_COMPEFFICACY-S2` (a transient live comp-kuzu latency spike, self-resolved, not a code defect) --
both at `org/missions/D11/NFRA/NFRA_COMPEFFICACY/surprise-channel/investigations/INVESTIGATION_v1.md`.

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.4 @19bf1c7322 s.4",
  "row": "T-1",
  "measured_by": "0.8.0_AE_CloudComp",
  "measured_at_utc": "2026-09-03T02:20Z..03:36Z",
  "read_vintage": "HEAD @2718cffc45",
  "surprises": ["NFRA_COMPEFFICACY-S1", "NFRA_COMPEFFICACY-S2"],

  "identity": {
    "tool": "comp-find",
    "shim_path": ".tools/comp-find (723)",
    "engine_path": ".tools/comp-find (723) -- SELF-CONTAINED: 0 delegate-engine imports; imports two SIBLING helpers (_comprail.py, the shared rail primitives ~30 comp-tools use; _compbudget.py, the shared Rule T carrier this cell added) -- neither is a second engine, both are libraries the shim itself is the engine that calls",
    "engine_vintage": "2718cffc45 (2026-09-02T23:33:05-04:00 = 2026-09-03T03:33:05Z)",
    "aliases": [],
    "aliases_note": "comp-grep and comp-glob (.tools/comp-grep, .tools/comp-glob) are LIVE SIBLINGS comp-find is meant to REPLACE (graph-call-manifest.yaml:334,:399; comp-which:673-680 'comp-find REPLACES comp-grep ... comp-grep still runs but nothing routes to it'), not aliases resolving TO comp-find -- they are separate files with separate implementations.",
    "purpose_1line": "the UNIFIED, GRADED, PAGINATED repo-search rail (NFRA_SCRIPTGEN Part B)  [engine docstring :2]",
    "self_identifies": {
      "help_prints_name_and_version": false,
      "help_prints_engine_path": false,
      "version_flag": "UNSUPPORTED -- not a recognized flag; falls through SILENTLY as a search PATTERN. Measured: `comp-find --version .tools` returns rc 0, 7 real content hits (SURFACED=4, DOC=3) across .tools -- no error, no version, a confusing false-looking result set. Worse than comp-adversary's `--version` (which at least errors 'unknown mode').",
      "output_line_1": "comp-find [content|name|aws ...] '<pattern>'  (dynamic per invocation; no static version banner exists anywhere in the tool)",
      "grade": "ABSENT -- no version identity anywhere in the estate's most-invoked search rail; --version is a live footgun"
    },
    "registration": {
      "graph_call_manifest": "PRESENT -- org/modules/graph/graph-call-manifest.yaml:392 'tool: comp-find', :399 notes, :1797 subcommands+entries. STALE: the :1797 subcommand list ['<pattern>','--name <glob>','-i','--page','--limit','--band','--files','--all'] names none of --corpus (landed 2026-08-27), --budget, or --cursor (this cell). commit-gate's own subcommand-declaration check reads comp-find as one of 50 UNKNOWN/flag-driven tools, so this drift is not gate-visible.",
      "comp_tools_yaml": "ABSENT (0 hits / 905 lines) -- but NOT a routing gap the way it is for comp-adversary: comp-which HARDCODES comp-find as its own rail fallback directly in source (.tools/comp-which:669-680, :727-737, :1629 'the sibling comp-find via sys.executable'), independent of the yaml purpose-catalog. comp-find is the rail of last resort, not a purpose-routed catalog entry.",
      "skill": ".claude/skills/comp-find/ -- ABSENT (0 files; comp-which's inline --help text is the only documented interface)"
    }
  },

  "disclosure": {
    "run": "DEFAULT flags, `comp-find _self_report .tools --limit 5` -- rc 0, 12 lines stdout, 0 stderr (quoted below)",
    "subject":             {"grade": "PRESENT-BUT-PARTIAL", "quoted": "comp-find [content] '_self_report'", "wrong_part": "the PATTERN is echoed verbatim in the header; the PATHSPEC/scope (here '.tools') is NEVER echoed anywhere in the output -- a saved capture without its invoking command line cannot recover which directories were in scope."},
    "corpus_or_backend":   {"grade": "PRESENT", "quoted": "DENOMINATOR: ... scanned in scope [corpus=all]  (or [corpus=aws] for the AWS plane)"},
    "vintage":             {"grade": "SPLIT -- PRESENT for --corpus aws, ABSENT for the file corpus", "quoted": "aws: 'VINTAGE: DB: kuzu_nessie_db (27122 nodes / 58414 edges) built: 2026-09-03T00:36:15Z (age: Nh)', independently cross-verified (MOVE 7 below) against a non-sharing Cypher count query -- MATCH. File corpus (default/all/ignored/raw): NO git HEAD sha, mtime window, or working-tree-dirty flag is ever printed -- two runs against different commits, or a dirty working tree, render byte-identically apart from the hit text itself."},
    "denominator":         {"grade": "PRESENT", "quoted": "DENOMINATOR: 1 hit(s) across 366 file(s) scanned in scope [corpus=all]"},
    "resolved_unresolved": {"grade": "PRESENT", "quoted": "'93 EPHEMERAL-FLOOR, NOT searched' / '2 BINARY, NOT searched' / '1 UNREADABLE, NOT searched' -- printed on the DENOMINATOR line whenever nonzero"},
    "blind_spots":         {"grade": "PRESENT (zero-hit-triggered only)", "quoted": "'^ AND 189919 gitignored file(s) in scope were NEVER SEARCHED (118248 searchable, 71671 ephemeral floor). YOUR ZERO DOES NOT COVER THEM.' -- printed only when total==0 under --corpus default; a non-zero run carries no equivalent caveat (by design: the caveat exists to stop a false-absence read, which only a zero can produce)"},
    "pagination":          {"grade": "PRESENT", "quoted": "PAGE 1 of 1  (showing 5 of 5)  -- true total, not the page's, per Rule P"},
    "timeout":             {"grade": "SPLIT -- PRESENT (aws corpus, after this cell) / non-application (file corpus)", "quoted": "'WITHIN BUDGET: scanned 1 of 1 pull; budget: 90 s (default), used 8.23 s' or 'BUDGET REACHED: 15 s (flag); scanned 2 of 3 node_type; ... resume: comp-find ... --cursor LAMBDA'", "before_this_cell": "PRESENT-BUT-WRONG -- :158 (pre-rework line) hard-coded timeout=600 against the harness's 120s outer ceiling, invisible to the caller, nothing printed at expiry (measured, TO-CE-T-1 issuance). File corpus has no subprocess and so no comparable ceiling -- Rule T's non-application clause applies there by construction (no loop whose count depends on corpus width running a timed subprocess)."}
  },

  "answer_state": {
    "schema_note": "Spellings per the RATIFIED enum (PRD v0.4 s.4.3, org/standards/COMPTOOL_ANSWER_STATE.enum.json): SUBJECT_ABSENT_FROM_CORPUS, PRESENT_WITH_ZERO_RESULTS, PARTIAL_OR_BLIND, NOT_APPLICABLE.",
    "SUBJECT_ABSENT_FROM_CORPUS": {"planted": "comp-find foo ZZZ_NONEXISTENT_DIR_0903 (pathspec does not exist)", "printed": "DENOMINATOR: 0 hit(s) across 0 file(s) scanned in scope [corpus=all] / NO HITS. This is a MEASURED zero over 0 scanned file(s) ...", "rc": 0, "finding": "NOT flagged in the tool's own voice as 'path does not exist' -- it silently degrades to a 0-files-scanned run, distinguishable from a real zero ONLY by the second DENOMINATOR number (0 vs N), never by an explicit error. Contrast: --hidden mode DOES check existence and prints 'ERROR: N path(s) do not exist' for the identical input shape -- the two modes disagree on whether this state gets a voice."},
    "PRESENT_WITH_ZERO_RESULTS":  {"planted": "an absent runtime-built token in a real, existing scope (.tools/comp-find)", "printed": "DENOMINATOR: 0 hit(s) across 1 file(s) scanned in scope [corpus=all] / NO HITS. This is a MEASURED zero over 1 scanned file(s) ...", "rc": 0, "distinguishable_from_absent_by": "the second DENOMINATOR number: 0 files (SUBJECT_ABSENT) vs 1 file (PRESENT_WITH_ZERO) -- numeric, not textual"},
    "PARTIAL_OR_BLIND":           {"planted": "--corpus default, absent token, at repo root (gitignored files present in scope)", "printed": "'^ AND 1 in-scope file(s) were UNREADABLE...' / '^ AND 2006 in-scope file(s) were BINARY...' / '^ AND 189919 gitignored file(s) in scope were NEVER SEARCHED (118248 searchable, 71671 ephemeral floor). YOUR ZERO DOES NOT COVER THEM.'", "rc": 0, "says_which_part": true, "second_specimen_this_cell": "BUDGET REACHED itself is a second, code-level PARTIAL_OR_BLIND: 'scanned 2 of 3 node_type' names exactly which part ran"},
    "NOT_APPLICABLE":             {"planted": "a content-search BAND filter (--band DEF) applied against --corpus aws, whose bands are node_type, not content bands", "printed": "DENOMINATOR: 34 hit(s) across 2100 aws node(s) scanned [corpus=aws] | band=DEF -> 0", "rc": 0, "declared_by_tool": false, "control": "the IDENTICAL shape with a REAL node_type band (--band LAMBDA on an absent term) prints 'band=LAMBDA -> 0' -- byte-for-byte the same shape apart from the substituted name. A category error (DEF does not exist as an aws node_type) and a genuine zero-hit real category are INDISTINGUISHABLE.", "finding": "the tool has no NOT_APPLICABLE word of its own for a cross-corpus category mismatch; a reader must already know the valid node_type vocabulary to tell the two apart"},
    "verdict": "PASS on the PRD criterion as measured (T1-AC2): the four planted cases produce four DISTINGUISHABLE, machine-parseable outputs (by the second DENOMINATOR number, by the coverage-caveat lines, or by the BUDGET REACHED token) -- but two findings stand: SUBJECT_ABSENT_FROM_CORPUS is silent in content-search mode (only --hidden speaks it), and NOT_APPLICABLE (a cross-corpus band category error) is byte-shape-identical to a genuine zero-hit real category, distinguished only by a reader's prior knowledge of the vocabulary, not by the tool."
  },

  "bounds": {
    "subprocess_timeouts": [
      {"file_line": ".tools/comp-find:194,:205 @2718cffc45", "value_s": "remaining() -- derives from the resolved --budget/env/default (90s default), never a fixed constant", "wraps": "python infra/aws/globgrph/kuzu_cli.py --json --mode inc <cypher>  (the --corpus aws pull, ONE call per unit)", "before_this_cell": ":158 (pre-rework HEAD @774c108bb5) hard-coded timeout=600, 5x the 120s outer ceiling, invisible to the caller"},
      {"file_line": ".tools/comp-find:715 @2718cffc45", "value_s": 20, "wraps": "python org/modules/graph/comp_log_auto.py  (self-report telemetry, fire-and-forget) -- MEASURED, NOT a defect: already well under the 120s ceiling; UNCHANGED by this cell"}
    ],
    "ceiling_behaviour": {
      "exercised": true,
      "how": "the REAL PRODUCTION BINARY, no mutant needed to force the ceiling (it is a caller flag now, not a constant, so exercising it touches zero bytes)",
      "unscoped_forced": "`--budget 0.001` on an unscoped pull -> 'BUDGET REACHED: 0.001 s (flag); scanned 0 of 1 pull(s); ... NO CURSOR: an unscoped --corpus aws pull is one indivisible unit -- a discovery step to decompose it ... was measured to cost MORE than this budget itself (a live RETURN DISTINCT n.node_type enumeration exceeded 4 minutes on this box, 2026-09-03) ...'; rc 0",
      "unscoped_healthy": "default budget, same query -> 'WITHIN BUDGET: scanned 1 of 1 pull; budget: 90 s (default), used 8.23 s'; rc 0",
      "scoped_multitype_partial": "`--budget 15` on 3 named node_types (IAM_ROLE LAMBDA S3_BUCKET) -> 'BUDGET REACHED: 15 s (flag); scanned 2 of 3 node_type; ...; resume: comp-find --corpus aws opal-gateway IAM_ROLE LAMBDA S3_BUCKET --budget 15 --cursor LAMBDA' -- a REAL cursor naming the last-completed unit, EXERCISED end-to-end: re-running with `--cursor LAMBDA` skipped IAM_ROLE and LAMBDA and completed ONLY S3_BUCKET, WITHIN BUDGET, in 7.38s",
      "scoped_zero_completions": "env COMP_BUDGET_S=0.001 on a single named type -> 'BUDGET REACHED: 0.001 s (env COMP_BUDGET_S); scanned 0 of 1 node_type(s); ...; NO CURSOR YET: no node_type completed before the budget hit, so there is no last-processed unit to resume from' -- a THIRD, distinct branch from the unscoped case (found and fixed live: a first draft mislabeled this as 'an unscoped pull is one indivisible unit', which is false when types WERE named and simply none finished)",
      "unbounded": "`--budget 0` -> 'WITHIN BUDGET: scanned 1 of 1 node_type; budget: unbounded (--budget 0), used 7.81 s'",
      "live_finding": "NFRA_COMPEFFICACY-S2 (surprise channel): mid-exercise, the SAME unscoped query that ran 7.4-14s consistently for ~20 minutes degraded to 90s+ for a ~4-9 minute window (three consecutive BUDGET REACHED outcomes, one isolated/non-concurrent), then self-resolved (full 10-arm battery back to 19.68s). The Kuzu DB file was unchanged in size/mtime across the window, ruling out DB growth. Root cause not chased (this seat's own ~20 rapid --mode inc calls is the leading, UNCONFIRMED hypothesis). Rule T is why nothing hung for 600s during the window."
    },
    "page_contract": {"page_flag": true, "limit_flag": true, "all_flag": true, "true_total_printed": true, "cap_flags": "--budget N (new, this cell); --cursor U (new, this cell); --corpus M; --hidden", "help_discloses_flags": "PRESENT -- --help documents --budget, --cursor, --corpus and their precedence/default in the same block", "note": "T-1 was already one of only two reference implementations satisfying Rule P (PRD s.4.4); unchanged by this cell (bounds: search semantics and pagination do not change)."},
    "size_invariance": {"work": "CONSTANT per-unit query shape (LIMIT 1000000 within a unit's WHERE clause); does not scale with corpus width in the number of Cypher calls issued for a SCOPED request (one call per named type regardless of how many nodes each contains)", "time": "NOW BUDGETED -- every subprocess timeout derives from remaining() (Clock.remaining() in .tools/_compbudget.py), never a fixed constant; measured worst case per unit is NOT a function of corpus width alone -- NFRA_COMPEFFICACY-S2 shows the SAME query varying 7.4s to 90s+ with the DB unchanged, i.e. LATENCY is a separate axis from WIDTH that Rule T's wall-clock budget correctly bounds regardless of which axis moved.", "rule_P": "MET, unchanged (reference implementation)", "rule_T": "MET (this cell) -- carrier, expiry disclosure, resumable cursor (scoped case) or disclosed non-application (unscoped case) all exercised live"}
  },

  "passcraft": {
    "recon": "comp-passcraft recon comp-find -- rc 0, MOVES 1-3 OBSERVED by the helper (kind: self, backends: (self-contained); write_surface: none matched; cache_oracle_signals: cache, marker/manifest); MOVES 4-8 SLOT, hand-run below",
    "moves_1_to_8": [
      {"move": 1, "status": "DONE", "falsifier_answer": "the shim IS the engine (723 lines, self-contained); two sibling LIBRARY imports (_comprail, _compbudget), no delegate engine"},
      {"move": 2, "status": "DONE", "falsifier_answer": "write surface: org/mcp/comp-tool-runs.jsonl (self-report telemetry) + org/mcp/comp-which-rail.log (rail log) -- both fire-and-forget sinks, 0 consumers that would be broken by a missing row (comp_log_auto.py's own docstring: 'never raises: a telemetry sink must never break the tool it measures')"},
      {"move": 3, "status": "DONE", "falsifier_answer": "no cache; oracle = the live Kuzu DB (--corpus aws) or the live git-tracked/gitignored filesystem (file corpus) at HEAD/working-tree read time -- no frozen fixture used as the measure"},
      {"move": 4, "status": "DONE", "falsifier_answer": "target universe FROM SOURCE: for aws, 'MATCH (n:CloudNode) WHERE n.layer=\\'aws\\' RETURN count(n)' independently returned 2100, MATCHING the tool's own printed denominator exactly (a non-sharing instrument, MOVE 7); for the file corpus, git ls-files + the gitignore-aware walker, denominator printed on every run"},
      {"move": 5, "status": "DONE", "falsifier_answer": "four answer-state branches verified from the OUTPUT differing (rc + text: 0/0 vs 0/1 vs coverage-caveat lines vs a BUDGET REACHED token), not by name; the ceiling branches (unscoped/scoped-partial/scoped-zero-completions/unbounded) verified the same way -- four genuinely distinct printed shapes, confirmed by direct execution, not asserted"},
      {"move": 6, "status": "DONE", "falsifier_answer": "mutations only in copies BESIDE the real tool (sibling imports resolve); production sha measured before (05c7b4...oldsha n/a-pre-rework) and after every mutant run; mutant copies removed and absence confirmed"},
      {"move": 7, "status": "DONE", "falsifier_answer": "ground truth from a NON-SHARING instrument: a direct Cypher count query run outside comp-find's own code path returned 2100, matching the tool's DENOMINATOR exactly -- corroboration, not repetition (different instrument, same substrate)"},
      {"move": 8, "status": "DONE", "falsifier_answer": "archetype hand-classified below; lead probes hunted: guard-asymmetry (PASS both directions on content search), success-token-bound-to-wrong-step (FOUND -- see findings), aging-oracle (clean -- aws vintage reads DB-native 'built:', not mtime), terminal-honest/artifact-lies (clean -- DENOMINATOR cross-verified), correct-but-unwired (clean -- Rule 21's gate is live and fired on this seat mid-session), undiscriminating/constant-gate (clean -- DENOMINATOR varies correctly across every probed input)"}
    ],
    "archetype": "GRADED-MEASUREMENT instrument: rc bound to EXECUTION, not to hit-count or budget outcome (rc 0 on a real hit, a genuine zero, AND a BUDGET REACHED) -- correct for its contract (a search returning 0 hits or an honest partial is not a tool failure), and the reason a consumer must read the body, never the rc, for BOTH the answer-state axis and the Rule-T axis",
    "findings": [
      {"id": "F1", "shape": "correct-but-unwired-style gap, mirrored", "cite": ".tools/comp-find --version (any invocation) @2718cffc45", "text": "no version flag exists; --version silently becomes a search pattern, returning real-looking hits (7, in .tools) with no error -- a footgun on the estate's most-invoked search tool"},
      {"id": "F2", "shape": "terminal-honest/artifact-lies (partial)", "cite": "org/modules/graph/graph-call-manifest.yaml:1797 vs .tools/comp-find --help @2718cffc45", "text": "the manifest's subcommand list predates --corpus (2026-08-27), --budget and --cursor (this cell) -- three flags the manifest does not know about"},
      {"id": "F3", "shape": "guard-asymmetry (byte-shape collision)", "cite": ".tools/comp-find:_aws_corpus band_filter application @2718cffc45", "text": "a content BAND (DEF/SURFACED/...) applied under --corpus aws is a category error the tool accepts silently, printing the identical shape as a genuine zero-hit real node_type band"},
      {"id": "F4", "shape": "skip-on-missing-field (silent, content-search only)", "cite": ".tools/comp-find:_comprail.gitignore_aware_files consumption @2718cffc45", "text": "a nonexistent pathspec in content/name search mode degrades to a 0-files-scanned run with no error, unlike --hidden mode on the identical input, which does print 'ERROR: N path(s) do not exist'"},
      {"id": "F5", "shape": "success-token-bound-to-wrong-step (disclosed, not hidden)", "cite": ".tools/_compbudget.py within_budget_line/budget_reached_line @2718cffc45", "text": "rc stays 0 whether the pull completed or was DEFERRED (by design, matching the T-16/comp-adversary precedent and PRD s.4.4's own words 'the LINE is the rejectable state, not the rc') -- a caller checking rc alone cannot see a partial result; the two-discriminator text (D1 token, D2 n-of-N) is REQUIRED reading, and this is stated, not hidden"}
    ]
  },

  "usage": {
    "runs_30d": {
      "runs_jsonl": {"count": "143+ at last read (device-local, org/mcp/comp-tool-runs.jsonl, gitignored)", "note": "heavily inflated THIS session by this cell's own exercise (~40-50 of the 143+ rows are this pass's own probes, 2026-09-03); the TO's own issuance-time figure was 133"},
      "rail_log":   {"count": "4201+ rows mentioning comp-find at last read (org/mcp/comp-which-rail.log)", "note": "the TO's issuance-time figure was 3,722/30d; the gap is largely this session's own traffic, not organic growth -- device-local instrument, per CLAUDE.md's own warning"}
    },
    "hook_driven": {"fraction": "0 of 143+ (to_id == '(no-TO)' on every sampled row)", "basis": "matches comp-adversary's identical finding; this cell set `comp-to` mid-session (Step E), so runs AFTER that point should carry this TO's id -- not independently re-verified post-hoc, stated as a gap"},
    "battery": {
      "files": [{"path": ".tools/tests/test_comp_find_battery.py (261 lines)", "collects_under_pytest": "1 test in ~20-26s (varies with live aws-corpus latency; see NFRA_COMPEFFICACY-S2)", "red_first_mutant": true, "mutant_forms": "E (DENOMINATOR text neutered, content-search path) AND G (BUDGET REACHED text neutered, aws-corpus path) -- BOTH must RUN (not crash) and then FAIL their sibling arm's own predicate; both DO"}],
      "file_grain_result": "10/10 PASS (A1-A5, E, F, F2, F3, G) -- confirmed direct AND under pytest -q, TWICE (once mid-live-degradation: 8/10 with F2/F3 failing on real backend latency, diagnosed as environment not code, F2/F3 redesigned latency-tolerant; once after recovery: 10/10 in 19.68s)",
      "lane_sweep": "pytest --collect-only .tools/tests/ -> still INTERNALERROR / SystemExit at test_fabric_check_classify.py:76 (one of CTO's three named F6 files) -- UNCHANGED from the 2026-09-02 census this seat ran for comp-adversary; 25 tests collected before the abort (re-confirmed at this write, not re-run against the full 22-file census)"
    },
    "overlap": "comp-grep and comp-glob remain LIVE, SEPARATE implementations comp-find is meant to supersede (graph-call-manifest.yaml notes :334,:399); comp-find does not consume or wrap either -- it is a parallel reimplementation, not a delegate",
    "proposed": "CLEARED-candidate for Rule T specifically (T1-AC1..AC6 as measured above); the project-wide CLEARED disposition is CVO's grade to render. Five findings (F1-F5) named above, none blocking Rule T's own acceptance; F1/F2/F3/F4 are pre-existing (not introduced by this cell) and are surfaced for the record, not fixed here (BOUNDS: search semantics do not change under this TO)."
  }
}
```

## The four planted answer-state cases, quoted

**SUBJECT_ABSENT_FROM_CORPUS** -- `comp-find foo ZZZ_NONEXISTENT_DIR_0903`, rc 0:
```
comp-find [content] 'foo'
  DENOMINATOR: 0 hit(s) across 0 file(s) scanned in scope [corpus=all]
  NO HITS. This is a MEASURED zero over 0 scanned file(s) in scope -- not a claim the term is
  absent from the estate.
```

**PRESENT_WITH_ZERO_RESULTS** -- an absent runtime token in a real scope, rc 0:
```
comp-find [content] 'ZZZ_ABSENT_TOKEN_0903_143905'
  DENOMINATOR: 0 hit(s) across 1 file(s) scanned in scope [corpus=all]
  NO HITS. This is a MEASURED zero over 1 scanned file(s) in scope -- not a claim the term is
  absent from the estate.
```

**PARTIAL_OR_BLIND** -- `--corpus default`, absent token, repo root, rc 0:
```
comp-find [content] 'ZZZ_ABSENT_TOKEN_PARTIAL_0903'
  DENOMINATOR: 0 hit(s) across 29551 file(s) scanned in scope [corpus=default] | 1 UNREADABLE,
  NOT searched | 2006 BINARY, NOT searched
  NO HITS. This is a MEASURED zero over 29551 scanned file(s) in scope ...
  ^ AND 1 in-scope file(s) were UNREADABLE and never searched. Your zero does NOT cover them.
  ^ AND 2006 in-scope file(s) were BINARY and never searched. Your zero does NOT cover them.
  ^ AND 189919 gitignored file(s) in scope were NEVER SEARCHED (118248 searchable, 71671
  ephemeral floor). YOUR ZERO DOES NOT COVER THEM.
```

**NOT_APPLICABLE** -- a content band against the aws node_type plane, rc 0, side by side with a real
zero-hit band on the identical shape:
```
# the category error (DEF is not an aws node_type):
comp-find [aws content] 'opal-gateway'
  DENOMINATOR: 34 hit(s) across 2100 aws node(s) scanned [corpus=aws] | band=DEF -> 0

# a genuine zero-hit REAL category, same shape:
comp-find [aws content] 'ZZZ_ABSENT_TOKEN_0903'
  DENOMINATOR: 0 hit(s) across 2100 aws node(s) scanned [corpus=aws] | band=LAMBDA -> 0
```
Both print `band=<X> -> 0`; nothing distinguishes "X is not a real category here" from "X is real and
empty." This IS the finding (F3 above) -- the four cases are distinguishable from EACH OTHER, but this
one is not distinguishable from a sibling within its own class without outside knowledge.

## Rule T, exercised end to end (the code change this cell owed)

Forced ceiling, unscoped (no cursor possible, disclosed):
```
comp-find [aws content] 'opal-gateway'
  BUDGET REACHED: 0.001 s (flag); scanned 0 of 1 pull(s); results are a PREFIX, not the answer;
  NO CURSOR: an unscoped --corpus aws pull is one indivisible unit -- a discovery step to
  decompose it into per-node_type units was measured to cost MORE than this budget itself, so it
  is not attempted automatically; resume: raise --budget, or narrow the pathspec to explicit
  node_type(s) (e.g. LAMBDA) for real --cursor support.
```
Healthy completion, same query:
```
  WITHIN BUDGET: scanned 1 of 1 pull; budget: 90 s (default), used 8.23 s
```
Scoped, partial, with a REAL exercised cursor (`--budget 15`, 3 named types):
```
  BUDGET REACHED: 15 s (flag); scanned 2 of 3 node_type; results are a PREFIX, not the answer;
  resume: comp-find --corpus aws opal-gateway IAM_ROLE LAMBDA S3_BUCKET --budget 15 --cursor LAMBDA
```
Resuming with that exact cursor (`--cursor LAMBDA`) -- ran ONLY the remaining unit, WITHIN BUDGET:
```
  WITHIN BUDGET: scanned 1 of 1 node_type; budget: 15 s (flag), used 7.38 s
```
The "why not decompose the unscoped case too" falsifier: a live `RETURN DISTINCT n.node_type`
enumeration (the cheapest imaginable discovery step) measured **247.5s** on this box, 2026-09-03 --
worse than the 90s default budget it would have served, and worse than the pre-rework 600s constant
this cell exists to retire. Decomposing the unscoped case was rejected on this evidence, not assumed.

## Findings F1-F5 and the live surprise (NFRA_COMPEFFICACY-S2)

See `passcraft.findings` in the JSON block above for F1-F5 (none blocking; none introduced by this
cell). Separately, mid-exercise the live `--corpus aws` backend itself degraded from a consistent
~8s per call to 90s+ for roughly a 4-9 minute window, then recovered -- filed as
`NFRA_COMPEFFICACY-S2` in the project's surprise channel (CVO's L8 read, msg 93005, already
adjudicated DISMISSED_WITH_REASON pending this commit landing: self-resolved, no code defect, Rule
T behaved correctly under the fault). Full evidence and the CVO's mtime-grain correction (this
seat's own row cited a `ls -la` LOCAL mtime with a trailing `Z`, CLAUDE.md 22a's known trap) are in
that row, not restated here.

## Captures and controls

Every quoted run above is a direct execution captured in this session (not a paraphrase); the
DENOMINATOR cross-check (2100 aws nodes) was independently re-derived via a raw Cypher `count(n)`
query outside comp-find's own code path (MOVE 7) and matched exactly. Production sha:
`.tools/comp-find` was `161dad68b9...` at TO issuance (HEAD @`774c108bb5`), `693b6230...` after the
interim commit (`88e870b115`), `05c7b439...` after this rework (`2718cffc45`) -- three MEASURED
points, not two. `git status` clean of everything but this deliverable + its proof-of-spec instance
at write time. Push state, MEASURED (ls-remote + is-ancestor): read 2026-09-03T03:36Z showed
`origin/CLOUD @6e8805eb90` with only `88e870b115` as an ancestor; RE-MEASURED 2026-09-03T03:43:18Z
after a push-window close notification: `origin/CLOUD @2718cffc45`, and `git merge-base
--is-ancestor` returns rc=0 (ON origin) for BOTH `b89b0493e5` (surprise row S2) and `2718cffc45`
(this rework). **All three of this cell's commits are ON origin/CLOUD as of this write.** T1-AC6
reads CLEARED on this measurement, not asserted from the push receipt.
