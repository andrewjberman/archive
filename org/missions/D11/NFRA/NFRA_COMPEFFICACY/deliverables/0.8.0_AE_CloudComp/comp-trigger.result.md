# comp-trigger -- NFRA_COMPEFFICACY per-tool result (PRD v0.4 s.4 schema)

Schema: `org/missions/D11/NFRA/NFRA_COMPEFFICACY/prd/NFRA_COMPEFFICACY_PRD.md` v0.4 @`19bf1c7322` s.4
(s.4.3 the ratified enum; s.4.4 RULE T's FORM). Row: T-9 (manifest s.7 :610). Cell: CE-t-9 (decomp
v0.2.2 @`b7daeaa6f0`, STAGE 2). Measured by `0.8.0_AE_CloudComp`, 2026-09-03T08:22Z-09:15Z,
read-vintage the cell's own fix commit `7737320640` (before-cell `ac678ed89d`, 2026-07-13). Every
value below is MEASURED on this box unless its own field says otherwise. **No surprise row filed**
-- the one candidate off-task observation (canonical `opal-data-bd`/`-cot`/`-inf` buckets absent
from the single-account live graph's 28-bucket S3_BUCKET population) is UNDETERMINED as to cause
(account-scope of the graph read vs. a real gap) and not chased further -- stated as a bounded
open question in the findings below, not asserted as a divergence.

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.4 @19bf1c7322 s.4",
  "row": "T-9",
  "measured_by": "0.8.0_AE_CloudComp",
  "measured_at_utc": "2026-09-03T08:22Z..09:15Z",
  "read_vintage": "cell fix commit @7737320640 (before-cell: ac678ed89d, 2026-07-13)",
  "surprises": [],

  "identity": {
    "tool": "comp-trigger",
    "shim_path": ".tools/comp-trigger (bash shim)",
    "engine_path": "org/modules/graph/comp_trigger.py (474 lines after this cell, was 344) -- the ENGINE; SELF-CONTAINED (no delegate engine), one LIBRARY import added this cell (_compbudget.py, Rule T's shared carrier)",
    "engine_vintage": "7737320640 (this cell's fix commit)",
    "aliases": [],
    "aliases_note": "none found -- comp-trigger has no same-name-prefix sibling the way comp-iam-usage sits beside comp-iam",
    "purpose_1line": "EventBridge / Scheduler trigger-dispatch FORENSICS (read-only)  [engine docstring :2]",
    "self_identifies": {
      "help_prints_name_and_version": false,
      "help_prints_engine_path": false,
      "version_flag": "UNSUPPORTED -- argparse errors loud on an unknown --version (no positional/flag collision the way comp-find's silent-pattern-fallback works, since --version is not a valid flag AND there's no bare-string-becomes-pattern fallback at the top level either -- argparse's 'unrecognized arguments' is the honest failure)",
      "output_line_1": "comp-trigger -- forensics for: \"<query>\"  (or the --list census header; dynamic per invocation)",
      "grade": "ABSENT -- no version identity anywhere; consistent with every other comp-tool audited this project"
    },
    "registration": {
      "graph_call_manifest": "not re-verified this cell (out of circle)",
      "comp_tools_yaml": "not re-verified this cell (out of circle)",
      "skill": "not checked this cell"
    }
  },

  "disclosure": {
    "run": "DEFAULT flags, `comp-trigger --list` -- rc 0, real output quoted below",
    "subject": {"grade": "PRESENT", "quoted": "'comp-trigger -- forensics for: \"<query>\"' echoes the query verbatim in every non---list run"},
    "corpus_or_backend": {"grade": "PRESENT", "quoted": "'denominator: 140 events-rules + 18 schedules scanned, region us-east-1' -- printed on every query run; --list prints the same two counts in its own header line"},
    "vintage": {"grade": "N/A -- every call is a live API read at invocation time (no cached/derived artifact this tool serves); TF-DESIRED lines are a live text-scan of the CURRENT working tree per call, not a stored snapshot, so there is no separate vintage to disclose beyond the run's own timestamp", "quoted": "n/a"},
    "denominator": {"grade": "PRESENT", "quoted": "'denominator: 140 events-rules + 18 schedules scanned, region us-east-1' -- both counts now EXCLUDE census_error sentinel rows after this cell's fix (previously live_rules had no census_error path at all, so this exclusion is new for the rules count, matching the schedules count's pre-existing behavior)"},
    "resolved_unresolved": {"grade": "PRESENT (per-match, not per-scan)", "quoted": "'target: (targets UNREADABLE: <exc>)' (rule_targets' own pre-existing except-branch) and, new this cell, 'target: DEFERRED -- Rule T budget exhausted before this match's live call' -- two DIFFERENT unresolved reasons (an API error vs a budget the caller chose), never conflated"},
    "blind_spots": {"grade": "PRESENT, now STRUCTURAL not just prose", "quoted": "the SCOPE line (new this cell, printed on EVERY answer): 'scope: EventBridge rules + Scheduler schedules ONLY; S3 bucket notifications NOT scanned (v1 scope, by design). For an S3-notification/sentinel trigger, delegate to comp-aws's S3_BUCKET node fields instead: comp-find --corpus aws \\'<bucket-name>\\' -> event_notifications/notify_sns/notify_sqs (org/modules/graph/comp_aws_cli.py:273-279, measured present on 28/28 S3_BUCKET nodes read 2026-09-03).'", "before_this_cell": "the blind spot was named only in the module DOCSTRING (:20-21) and in the no-match branch's parenthetical -- never on a MATCH's own answer line, and never with a measured delegation citation"},
    "pagination": {"grade": "N/A -- no pagination; --list prints every row every time (140 rules + 18 schedules is small enough that this is not this tool's own cost problem)", "quoted": "n/a"},
    "timeout": {"grade": "PRESENT (this cell)", "quoted": "query mode: 'WITHIN BUDGET: scanned 3 of 3 match; budget: 90 s (default), used 4.28 s' or 'BUDGET REACHED: 0.05 s (flag); scanned 1 of 3 match; ... resume: comp-trigger \\'bd-gold-trigger\\' --cursor <name>'. --list mode (one opaque, already-fully-paginated pull): 'WITHIN BUDGET: scanned 1 of 1 census_pull ...' or 'NOT WITHIN BUDGET: the rules+schedules pull took <t>s ... but it already RAN TO COMPLETION ... Disclosed non-application ...'", "before_this_cell": "PRESENT-BUT-ABSENT -- MEASURED-at-cut text: 'no timeout' (PRD s.7 T-9); every boto3 call ran under boto3's own untimed defaults"}
  },

  "answer_state": {
    "schema_note": "Spellings per the RATIFIED enum. None of comp-trigger's four planted cases print the enum's bare state name as a literal token; all four are graded declared_by_tool: false, same posture as comp-find/comp-iam's own precedents.",
    "SUBJECT_ABSENT_FROM_CORPUS": {"planted": "comp-trigger ZZZ_NONEXISTENT_FUNCTION_93999 (confirmed absent from the estate: 0 hits in Terraform, not a real name)", "printed": "'NO MATCH by name or target-ARN substring. (That is a match-miss, not proof no trigger exists -- an S3-notification/sentinel trigger would not appear here; v1 scans EventBridge rules + Scheduler schedules only.)'", "rc": 0},
    "PRESENT_WITH_ZERO_RESULTS": {"planted": "comp-trigger bd-price-update -- a REAL, TF-declared Lambda (infra/aws/terraform/bd-pipeline/lambdas.tf; confirmed present via comp-find, 147 hits across 5 real TF files) that is invoked Lambda-to-Lambda by bd-allocation-processor, per that same TF tree's own comments -- genuinely zero EventBridge/Scheduler/S3 triggers of any kind", "printed": "BYTE-IDENTICAL to the SUBJECT_ABSENT case above -- 'NO MATCH by name or target-ARN substring. (...)'", "rc": 0, "finding": "SUBJECT_ABSENT_FROM_CORPUS and PRESENT_WITH_ZERO_RESULTS are STRUCTURALLY INDISTINGUISHABLE in this tool -- comp-trigger has no Lambda/function-existence check of its own (it only searches EventBridge rule names/targets and Scheduler schedule names), so it cannot tell 'this name does not exist anywhere' from 'this name exists but holds none of the two trigger kinds I scan'. Filed as finding F1 (not fixed -- the TO's ONE code change was the scope line + delegation + Rule T, not a new Lambda-population check, which would be new scope this cell was not asked for)."},
    "PARTIAL_OR_BLIND": {"planted": "comp-trigger bd-allocation-processor -- a REAL, TF-confirmed S3-notification-ONLY Lambda target (infra/aws/terraform/bd-pipeline/s3-notifications.tf's aws_s3_bucket_notification.bd_data_bucket resource, lambda_function id=ProcessAllocationFiles, on bucket opal-data-bd) with zero EventBridge/Scheduler presence", "printed": "the SAME 'NO MATCH ...' text as the two cases above, PLUS the new SCOPE line naming the S3-notification exclusion and its delegation explicitly", "rc": 0, "distinguishable_from_the_others_by": "nothing in THIS run alone (same rc, same NO MATCH text) -- the SCOPE line is what keeps the answer from ever reading as PRESENT_WITH_ZERO_RESULTS-shaped ('no trigger'): the delegation pointer is present on every miss, so a reader chasing this specific specimen is handed the correct next step (query comp-aws) regardless of which of the three miss-classes they hit. AC3's own bar ('never PRESENT_WITH_ZERO_RESULTS, never a silent no-trigger claim') is met by the WORDING applying uniformly, not by a per-query distinction the tool cannot make."},
    "NOT_APPLICABLE": {"planted": "comp-trigger --list --region us-west-2 (a real, currently-empty region for this account)", "printed": "'comp-trigger census -- 0 events-rules + 0 schedules, region us-west-2'", "rc": 0, "declared_by_tool": false, "distinguishable_from_the_others_by": "this is a --list (census) answer, not a query-match answer -- a genuinely different subcommand shape/population, not a rc or text distinction within the same shape"},
    "verdict": "PARTIAL PASS on T9-AC2: four cases planted, all real (verified via independent Terraform/comp-find reads, not invented names), each rc 0. Three of the four (SUBJECT_ABSENT, PRESENT_WITH_ZERO, PARTIAL_OR_BLIND) print BYTE-IDENTICAL bodies -- the tool cannot distinguish them from each other by rc or text alone (finding F1). What AC3 specifically asks for -- the S3-notification case reading out-of-scope, never 'no trigger' -- IS met, because the SCOPE+delegation line is now unconditional on every answer, not because the three miss-classes are separately voiced."
  },

  "scope_and_delegation": {
    "existing_machinery_check_first": "MEASURED, not assumed: comp-which found no single clean routing hit (3-way tie, score 1.50, none an obvious S3-notification reader); comp-find -i 'NotificationConfiguration|bucket_notification|sentinel' across org/modules/graph, .tools, infra/aws returned 1787 hits/11926 files (mostly vendored-package false positives: pydantic/sklearn 'sentinel' senses); the narrowing comp-read --enumerate 'event_notifications' on org/modules/graph/comp_aws_cli.py found the real carrier: lines 273-274 (S3_BUCKET node build) call s3.get_bucket_notification_configuration and store event_notifications = len(LambdaFunctionConfigurations); two more call sites at :1443, :1681. Independently EXERCISED (not just read): `comp-find --corpus aws 'event_notifications'` returned 28/28 S3_BUCKET nodes each carrying event_notifications/notify_sns/notify_sqs fields, vintage 2026-09-03T00:36:15Z (age 7.9h at read time).",
    "delegation_landed": true,
    "delegation_form": "a citation on every answer line (SCOPE_LINE), never a live cross-tool call from comp_trigger.py into comp_aws_cli.py -- consistent with BOUNDS' 'never built here' and the TO's own 'either is a valid close; the header declaration is the floor' language",
    "gap_named_not_built": "the 28-bucket population comp-aws's graph returned does NOT include opal-data-bd/-cot/-inf (the canonical pipeline buckets this cell's own TF read confirms DO carry real aws_s3_bucket_notification resources) -- whether this is an account-scope limit of the single-account (313476888478) graph read or a real coverage gap is UNDETERMINED and not chased (out of this cell's circle; see findings)."
  },

  "rule_t": {
    "carrier": "the ONE shared module .tools/_compbudget.py @2718cffc45, imported at comp_trigger.py's top (new sys.path insert for .tools this cell added, mirroring comp-iam's own pattern)",
    "help_discloses_it": "quoted verbatim above (disclosure.timeout); --budget documented nowhere before this cell",
    "two_call_shapes_this_cell_wired": [
      {"shape": "one opaque, already-fully-paginated pull", "subcommand": "--list (and the rules+schedules pull common to every invocation)", "mechanism": "a Clock measures the pull post-hoc; WITHIN BUDGET on a generous budget, an honest 'NOT WITHIN BUDGET ... but it already RAN TO COMPLETION ... Disclosed non-application' on a tiny one -- exercised on the real production binary, real live AWS calls, both directions"},
      {"shape": "resumable per-unit loop", "subcommand": "the per-MATCH enrichment sweep (targets + fired-evidence + TF-desired, one unit per match, sorted by name)", "mechanism": "_enrich_matches(): a shared Clock checked once per match; a match Rule T could not reach before expiry gets the literal string 'DEFERRED' on targets/fired/tf_desired rather than a live call or a silent omission; render()/--json both print/serialize the DEFERRED sentinel distinctly from a real empty result"}
    ],
    "deferred_bucket": "exercised with FAKE (fixture) clients in the new battery (deterministic, no live-AWS timing race) AND confirmed live: a real query under --budget 0.00001 shows 'BUDGET REACHED: ... scanned 1 of 2 match' with the second match's target/fired/tf_desired fields rendering the DEFERRED text",
    "real_bug_found_by_exercise": "live_rules() had NO exception handling at all before this cell -- a tiny --budget (this cell's own new flag) produced a raw ConnectTimeoutError traceback that CRASHED the whole tool, discovered by running the real production binary under a forced-tiny budget, not by reading the source. Fixed to mirror live_schedules()'s pre-existing UNAVAILABLE-sentinel shape exactly (a census_error row, never a crash). This is the single most consequential finding of this cell -- Rule T's OWN new flag was, before this fix, MORE likely to crash the tool than the pre-existing untimed calls ever were."
  },

  "bounds": {
    "read_only_always": "confirmed unchanged: the self-test's own nowrite.no_mutating_call_in_source check (banned method-call regex over the module's own source) still passes 14/14 after this cell's edits -- 0 mutating boto3 verbs anywhere in the file, and its sibling control (nowrite.control_can_fire) proves that detector is not a decoration (list_rules IS found as a real method call)",
    "existing_machinery_checked_never_built": "confirmed by the code diff itself: zero new AWS service clients, zero new boto3 methods called anywhere in comp_trigger.py after this cell -- the S3-notification question is answered by a CITATION to comp-aws, not a new call",
    "no_new_dependency_no_new_file_outside_named": "git diff --stat ac678ed89d..7737320640 -- org/modules/graph/comp_trigger.py: 178 insertions(+), 48 deletions(-); the one new file is .tools/tests/test_comp_trigger_battery.py (TOOL_BATTERIES lane), plus this deliverable + its proof instance -- nothing else",
    "spec_vs_world_divergence": "none filed as a row this cell -- the bd/cot/inf-bucket-coverage question is stated as UNDETERMINED, not asserted as a divergence (see scope_and_delegation.gap_named_not_built)"
  },

  "passcraft": {
    "moves_1_to_8": [
      {"move": 1, "status": "DONE", "falsifier_answer": "the shim (.tools/comp-trigger) forwards verbatim to comp_trigger.py, the real (and only) engine -- SELF-CONTAINED, zero delegate-engine imports; one new LIBRARY import this cell (_compbudget)"},
      {"move": 2, "status": "DONE", "falsifier_answer": "write surfaces: org/mcp/comp-tool-runs.jsonl + org/mcp/comp-which-rail.log (fire-and-forget telemetry via comp_log_auto.py in the shim) -- comp-trigger itself writes NOTHING else; confirmed structurally by the self-test's own nowrite invariant"},
      {"move": 3, "status": "DONE", "falsifier_answer": "no cache anywhere -- every call (list_rules, list_schedules, list_targets_by_rule, get_metric_statistics) is a fresh live API read at invocation time; TF-DESIRED is a fresh os.walk text scan of the CURRENT working tree per call, never a stored snapshot"},
      {"move": 4, "status": "DONE", "falsifier_answer": "target universe cross-checked from a SEPARATE read: this cell's own comp-find/comp-read passes independently confirmed bd-allocation-processor/bd-silver-merge/bd-price-update as real Terraform-declared Lambdas (147 hits across 5 real TF files for bd-price-update alone) BEFORE querying comp-trigger against them -- not asserted from comp-trigger's own output"},
      {"move": 5, "status": "PARTIAL", "falsifier_answer": "the NOT_APPLICABLE case (--list, empty region) IS output-distinguishable (0/0 denominator, --list shape). The other three cases are NOT output-distinguishable from each other (finding F1) -- this move's own falsifier test is what SURFACED F1, not something this move hid"},
      {"move": 6, "status": "DONE", "falsifier_answer": "all three battery mutants live BESIDE the real engine (org/modules/graph/_tmp_trigger_mutant_<kind>_<pid>.py) and are removed after each run (confirmed: none left in org/modules/graph/ post-battery)"},
      {"move": 7, "status": "DONE", "falsifier_answer": "the comp-aws delegation claim was corroborated by a NON-SHARING instrument: comp-read's static enumerate (source-level, 0.19s, no network) found the 2 write sites at comp_aws_cli.py:273-279; comp-find --corpus aws (a live Kuzu graph query, a completely different code path and data source) independently confirmed the SAME fields present on 28 real S3_BUCKET nodes -- agreement between a static read and a live query, not the same instrument run twice"},
      {"move": 8, "status": "DONE", "falsifier_answer": "archetype hand-classified below; probed: guard-asymmetry (FOUND, F1 -- three of four answer-states share one guard clause with no asymmetric check between them), success-token-bound-to-wrong-step (clean -- rc stays 0 whether WITHIN BUDGET or BUDGET REACHED, matching the estate's own T-16/PRD s.4.4 convention, disclosed not hidden), aging-oracle (N/A -- no cached artifact to age), terminal-honest/artifact-lies (clean -- the DENOMINATOR and SCOPE lines were cross-checked against real Terraform reads and matched), correct-but-unwired (FOUND AND FIXED, the live_rules crash -- Rule T's own new budget flag was unwired from any failure handling until this cell's fix)"}
    ],
    "archetype": "READ-ONLY FORENSICS instrument whose rc is bound to EXECUTION, not to match-count or budget outcome (0 on a real hit, a genuine miss, AND a Rule T expiry) -- correct for its contract (a forensic query returning no match is not a tool failure), same posture as every other comp-tool audited this project.",
    "findings": [
      {"id": "F1", "shape": "guard-asymmetry (three states, one guard)", "cite": "org/modules/graph/comp_trigger.py:render()'s `if not matches:` branch @7737320640", "text": "SUBJECT_ABSENT_FROM_CORPUS, PRESENT_WITH_ZERO_RESULTS, and PARTIAL_OR_BLIND (the S3-only case) all fall through the SAME `if not matches:` branch and print byte-identical text -- the tool has no Lambda/function-existence check, so it cannot tell 'name does not exist anywhere' from 'name exists, zero EventBridge/Scheduler triggers' from 'name exists, S3-only trigger'. Not fixed this cell (a Lambda-existence check is new scope the TO's ONE code change did not name; the TO's own SCOPE+delegation fix is what THIS finding's severity is bounded by -- a reader is still handed the correct next step regardless of which of the three they hit)."},
      {"id": "F2", "shape": "correct-but-unwired, FIXED this cell", "cite": "org/modules/graph/comp_trigger.py live_rules() before @ac678ed89d / after @7737320640", "text": "no try/except at all pre-cell; a tiny --budget (this cell's own new flag) crashed the tool with a raw ConnectTimeoutError traceback. Fixed to mirror live_schedules()'s existing UNAVAILABLE-sentinel shape. The most consequential finding of this cell: a Rule T carrier that crashes the tool it budgets is worse than the untimed calls it replaces."},
      {"id": "F3", "shape": "coverage question, UNDETERMINED (not a defect claim)", "cite": "comp-find --corpus aws 'event_notifications' 28/28 S3_BUCKET nodes vs infra/aws/terraform/bd-pipeline/s3-notifications.tf's opal-data-bd resource", "text": "the canonical opal-data-bd/-cot/-inf buckets, confirmed by this cell's own TF read to carry real aws_s3_bucket_notification resources, are ABSENT from the single-account (313476888478) live graph's 28-bucket S3_BUCKET population. Account-scope of the graph build vs. a real coverage gap is UNDETERMINED; not chased further (out of this cell's circle -- the delegation citation is accurate for whatever population comp-aws's graph DOES cover, and this finding names the boundary honestly rather than silently)."}
    ]
  },

  "usage": {
    "runs_30d": {
      "runs_jsonl": {"count": "156 rows mentioning \"comp-trigger\" (org/mcp/comp-tool-runs.jsonl, device-local, gitignored)", "note": "the TO's own MEASURED-at-cut figure was 80 runs -- a narrower or differently-scoped count, not reconciled this cell"},
      "rail_log": {"count": "468 rows mentioning comp-trigger (org/mcp/comp-which-rail.log)", "note": "device-local instrument per CLAUDE.md's own warning"}
    },
    "hook_driven": {"fraction": "not sampled this cell (out of circle)"},
    "battery": {
      "files": [
        {"path": "org/modules/graph/comp_trigger.py's own embedded _self_test() (was 8/8, now 14/14)", "collects_under_pytest": "not a pytest entry point (direct-invocation self-test, `comp-trigger --self-test`); run directly: 14/14 PASS", "red_first_mutant": "not applicable -- offline fixture cases, not mutants of the tool"},
        {"path": ".tools/tests/test_comp_trigger_battery.py (NEW this cell, 0 files existed for this tool at cut)", "collects_under_pytest": "1 test, 8.13s (fixture-driven throughout -- zero live AWS calls, zero timing races)", "red_first_mutant": true, "mutant_forms": "scope_dropped (SCOPE_LINE removed from render()), crash_reintroduced (live_rules' try/except removed -- the exact pre-fix F2 shape), enrich_budget_ignored (the per-match remaining<=0 check disabled) -- all three RUN (not crash) and FAIL their sibling arm's own predicate; all three DO"}
      ],
      "file_grain_result": "8/8 PASS (CT-AC3-SCOPE-LINE-ON-HIT-AND-MISS, CT-AC3-MUTANT-SCOPE-LINE-DROPPED-DETECTED, CT-AC4-HELP-DISCLOSES-BUDGET, CT-AC5-LIVE-RULES-NO-CRASH, CT-AC5-MUTANT-CRASH-REINTRODUCED-DETECTED, CT-AC5-ENRICH-WITHIN-BUDGET, CT-AC5-ENRICH-DEFERRED-MID-SWEEP, CT-AC5-MUTANT-ENRICH-BUDGET-IGNORED-DETECTED) -- confirmed direct AND under pytest -q; commit-gate clean 2/2 files",
      "lane_sweep": "pytest --collect-only .tools/tests/ -> still INTERNALERROR/SystemExit at test_fabric_check_classify.py:76 (the same known aborter T-1/T-8 both recorded), 36 tests collected before the abort (up from T-8's 25, other seats' new files landing this session) -- unchanged in nature, not this cell's"
    },
    "overlap": "no same-name-prefix sibling found (unlike comp-iam-usage beside comp-iam)",
    "proposed": "CLEARED-candidate for T9-AC1, AC3 (partial per F1), AC4, AC5 as measured above; the project-wide CLEARED disposition is CVO's grade to render. Three findings (F1-F3): F1 is a real, unfixed guard-asymmetry named for the record (new scope, not this cell's ONE code change); F2 is a real bug FOUND AND FIXED this cell (the most consequential of the three); F3 is an honestly-bounded open question, not a defect claim."
  }
}
```

## The four planted answer-state cases, quoted in full

**SUBJECT_ABSENT_FROM_CORPUS** -- `comp-trigger ZZZ_NONEXISTENT_FUNCTION_93999`, rc 0:
```
comp-trigger -- forensics for: "ZZZ_NONEXISTENT_FUNCTION_93999"
  denominator: 140 events-rules + 18 schedules scanned, region us-east-1
  scope: EventBridge rules + Scheduler schedules ONLY; S3 bucket notifications NOT scanned (v1
  scope, by design). For an S3-notification/sentinel trigger, delegate to comp-aws's S3_BUCKET
  node fields instead: `comp-find --corpus aws '<bucket-name>'` -> event_notifications/
  notify_sns/notify_sqs (org/modules/graph/comp_aws_cli.py:273-279, measured present on 28/28
  S3_BUCKET nodes read 2026-09-03).
  NO MATCH by name or target-ARN substring. (That is a match-miss, not proof no trigger exists
  -- an S3-notification/sentinel trigger would not appear here; v1 scans EventBridge rules +
  Scheduler schedules only.)
```

**PRESENT_WITH_ZERO_RESULTS** -- `comp-trigger bd-price-update` (real, TF-declared, Lambda-to-Lambda
invoked, zero triggers of any kind), rc 0 -- BYTE-IDENTICAL body to the case above.

**PARTIAL_OR_BLIND** -- `comp-trigger bd-allocation-processor` (real, TF-confirmed S3-notification-only
target on `opal-data-bd`), rc 0 -- the SAME body again; the SCOPE line is what keeps this reading as
out-of-scope rather than a false "no trigger" claim.

**NOT_APPLICABLE** -- `comp-trigger --list --region us-west-2` (a real, empty region), rc 0:
```
  budget: 90 s (default)
WITHIN BUDGET: scanned 1 of 1 census_pull; budget: 90 s (default), used 1.91 s
  scope: EventBridge rules + Scheduler schedules ONLY; S3 bucket notifications NOT scanned ...
comp-trigger census -- 0 events-rules + 0 schedules, region us-west-2
```

## Rule T, exercised end to end (the code change this cell owed)

```
$ comp-trigger bd-gold-trigger                     # 3 real EventBridge rules target this function
  budget: 90 s (default)
WITHIN BUDGET: scanned 3 of 3 match; budget: 90 s (default), used 4.28 s

$ comp-trigger bd-gold-trigger --budget 0.00001    # forced ceiling, mid-sweep
  budget: 1e-05 s (flag)
BUDGET REACHED: 1e-05 s (flag); scanned 1 of 2 match; results are a PREFIX, not the answer;
  resume: comp-trigger 'bd-gold-trigger' --cursor (events census UNAVAILABLE: Connect timeout ...)

$ comp-trigger --list --budget 0.00001             # the opaque, already-fully-paginated pull
  budget: 1e-05 s (flag)
NOT WITHIN BUDGET: the rules+schedules pull took 13.53s, over the budget: 1e-05 s (flag) -- but
  it already RAN TO COMPLETION (both list calls are already fully paginated by the time any
  budget check could run; no internal resumption point to abort at). Disclosed non-application
  of the early-abort half of Rule T for this specific subcommand shape.
```
The tiny-budget run above ALSO exercises F2 in its fixed form live: `live_rules()` under a
0.00001s connect timeout now returns a `census_error` sentinel row (visible in the resume-cursor
text above) instead of crashing -- the pre-fix behavior at this exact forced ceiling was an
unhandled `ConnectTimeoutError` traceback.

## Findings F1-F3

See `passcraft.findings` above for full text. F1 (three answer-states share one guard, not fixed
-- new scope) and F3 (a bounded, undetermined coverage question, not a defect claim) are both
real but non-blocking. F2 -- the `live_rules()` crash Rule T's own new `--budget` flag exposed --
is fixed and is this cell's most consequential result: it was found by running the real production
binary under a forced-tiny budget, not by reading the source.

## Captures and controls

Every quoted run above is a direct execution captured in this session. Production sha:
`org/modules/graph/comp_trigger.py` was `ac678ed89d` (2026-07-13, before this cell) ->
`7737320640` (this cell's fix, 178 insertions / 48 deletions, one new file besides the battery +
this deliverable + its proof instance). Self-test: 8/8 -> 14/14. Battery: 8/8 PASS, new file,
confirmed direct AND under pytest (8.13s); commit-gate clean 2/2 files. Push state, MEASURED
(ls-remote + is-ancestor) at write time: `git merge-base --is-ancestor 7737320640 origin/CLOUD`
read non-zero -- LOCAL ONLY, the expected state while Andrew gates the cadence.
