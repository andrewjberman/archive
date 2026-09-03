# comp-iam -- NFRA_COMPEFFICACY per-tool result (PRD v0.4 s.4 schema)

Schema: `org/missions/D11/NFRA/NFRA_COMPEFFICACY/prd/NFRA_COMPEFFICACY_PRD.md` v0.4 @`19bf1c7322` s.4
(s.4.3's four answer-state spellings ratified as DATA at `org/standards/COMPTOOL_ANSWER_STATE.enum.json`
@`19bf1c7322`; s.4.4 "RULE T's FORM" is the grammar this cell applies). Row: T-8 (manifest s.7 :609).
Cell: CE-t-8 (decomp v0.2.1 @`070907b56e`, STAGE 2's first). Measured by `0.8.0_AE_CloudComp`,
2026-09-03T06:10Z-07:10Z, read-vintage the cell's own fix commit `eb7966105a` (before-cell
`c2f70f7ca4`, 2026-08-11). Every value below is MEASURED on this box unless its own field says
otherwise; every run's full output is quoted from a saved capture. **No surprise row was filed for
this cell** -- every finding below is the audit's own content (S9's own precedent: an audit finding
inside a per-tool deliverable rides the project's per-tool carrier, it is not a spec-vs-world
divergence, and is not a row).

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.4 @19bf1c7322 s.4",
  "row": "T-8",
  "measured_by": "0.8.0_AE_CloudComp",
  "measured_at_utc": "2026-09-03T06:10Z..07:10Z",
  "read_vintage": "cell fix commit @eb7966105a (before-cell: c2f70f7ca4, 2026-08-11)",
  "surprises": [],

  "identity": {
    "tool": "comp-iam",
    "shim_path": ".tools/comp-iam (8 lines)",
    "engine_path": "org/modules/graph/iam_cli.py (1,759 lines after this cell, was 1,624) -- the ENGINE, not the shim; three sibling engine files also in this TO's lane: comp_iam_live.py (461), comp_iam_census.py (230), comp_iam_investigate.py (299) -- 2,749 lines across the four, imported by iam_cli.py at :986-988, not delegated to",
    "engine_vintage": "eb7966105a (2026-09-03T02:55:35-04:00 = 2026-09-03T06:55:35Z)",
    "aliases": [],
    "aliases_note": ".tools/comp-iam-usage is a DIFFERENT, SEPARATE tool (own engine org/modules/graph/comp_iam_usage.py) answering a DIFFERENT question -- lifecycle/coldness (RoleLastUsed, who-can-reach, reach-check) vs comp-iam's deploy-time correctness (does this role hold this grant). Same 'comp-iam' name prefix, not an alias resolving to this engine, not a mode of it -- the comp-find precedent's comp-grep/comp-glob pattern, one surface over.",
    "purpose_1line": "IAM permission cross-reference for Lambda and EC2 scripts -- flags calls a script makes that its role may not permit  [engine docstring :3-7]",
    "self_identifies": {
      "help_prints_name_and_version": false,
      "help_prints_engine_path": false,
      "version_flag": "UNSUPPORTED -- argparse has no top-level --version; `comp-iam --version` errors 'invalid choice' via argparse's own subparser dispatch (unlike comp-find, where --version silently becomes a search pattern -- comp-iam's argparse-subcommand shape makes this the SAFER failure of the two: loud, not silent).",
      "output_line_1": "comp-iam: NOTE -- TF role label '<x>' is reused across modules ... (printed unconditionally at import time on every invocation that hits a collision; when there is none, the first output line is the subcommand's own header)",
      "grade": "ABSENT -- no version identity anywhere in this tool either; --help is the only way to confirm which build is running (no printed engine sha)"
    },
    "registration": {
      "graph_call_manifest": "PRESENT -- org/modules/graph/graph-call-manifest.yaml names comp-iam (not re-verified line-by-line this cell; out of this TO's circle -- BOUNDS: no new file outside the named surfaces)",
      "comp_tools_yaml": "not re-verified this cell (out of circle; T-8's BOUNDS is the engine + battery + deliverable, not the routing catalog)",
      "skill": ".claude/skills/comp-iam/ -- not checked this cell"
    }
  },

  "disclosure": {
    "run": "DEFAULT flags, `comp-iam stats` -- rc 0, real output quoted below",
    "subject": {"grade": "ABSENT for the DESIRED plane's own scope; PRESENT per-subject in named-subject subcommands", "quoted": "`comp-iam stats`/`gaps` never echo which Terraform trees were the CALLER's intent vs the tool's hard-coded EI.TF_SCAN_ROOTS -- there is no pathspec argument to echo (unlike comp-find). `comp-iam service <name>` / `role <name>` DO echo the subject verbatim in the header line ('SERVICE: <name> [<type>]', 'ROLE: <name>')."},
    "corpus_or_backend": {"grade": "PRESENT", "quoted": "'scanned 3 trees (396 .tf files): infra/aws/terraform, infra/aws/multi-account/terraform, infra/aws/ec2' (_print_plane_banner, shown by gaps/service/resource-sweep)"},
    "vintage": {"grade": "SPLIT -- PRESENT for the APPLIED census plane (reconcile), ABSENT for the DESIRED (Terraform-parse) plane every other subcommand runs on", "quoted": "reconcile: 'CENSUS PROVENANCE: cmpaws-iam-census-20260903.json -- generated 2026-09-03T06:46:12Z (age 0.2h, TTL 24h) [FRESH]'. Every DESIRED-plane subcommand (gaps/service/role/roles/stats/resource-sweep/attach-census) prints NO git HEAD sha, mtime window, or working-tree-dirty flag anywhere -- the same gap T-1 found in comp-find's file corpus, one tool over: two runs against different Terraform states render byte-identically apart from the substantive numbers."},
    "denominator": {"grade": "PRESENT", "quoted": "'IAM roles parsed: 180 / Services scanned: 187 / Lambda services: 166 / EC2 services: 21 / Total operations: 1074 / Permission gaps: 306' (stats); resource-sweep and gaps each print their OWN, narrower denominator for their own plane (see finding F1 below -- three different 'gaps' counts coexist in this tool, each honestly labeled but easy to cross-cite by accident)"},
    "resolved_unresolved": {"grade": "PRESENT", "quoted": "'policy blocks attached 357; NOT ATTACHED 24 (a role ref this parser cannot resolve); standalone 11' (_print_plane_banner); resource-sweep/gaps additionally tally UNRESOLVABLE-RESOURCE, UNMAPPED-METHOD, UNRESOLVED-CLIENT per call"},
    "blind_spots": {"grade": "PRESENT (unconditional on some surfaces, conditional on others)", "quoted": "'DENY-OVERLAY INCOMPLETE: N deny statement(s) unparsed ... Asking this tool about a Deny it never parsed returns SILENCE, and silence must not be read as allowed' (printed only when deny_unparsed>0); cmd_service's floor caveat ('THIS OPERATION LIST IS A FLOOR, NEVER A DELETION WARRANT') prints UNCONDITIONALLY, on every call regardless of result -- stronger discipline than comp-find's zero-hit-triggered-only caveat (T-1 F-class), not weaker."},
    "pagination": {"grade": "N/A -- no pagination anywhere in this tool (no --page/--limit/--all on any subcommand); every list-shaped output (roles, services, resource-sweep FLAGGED) prints its full result every time. Not a defect Rule P governs: comp-iam's largest single list (roles: 180) is small enough that page-cost is not the tool's own problem the way it is for comp-find's 145k-file corpus.", "quoted": "n/a"},
    "timeout": {"grade": "PRESENT (this cell) for the 3 AWS-plane/corpus-width surfaces; disclosed non-application for the 2 census-file surfaces", "quoted": "simulate: 'WITHIN BUDGET' path prints 'budget: 90 s (default)' before the live call; a call that outlives it prints 'DEFERRED: call did not complete within <B>s (<source>) -- <ExceptionType>: <msg>' and 'STATE: NOT-DECIDABLE', never a hang, never a deny. resource-sweep: 'WITHIN BUDGET: scanned 166 of 166 lambda; budget: 90 s (default), used <t>s' / 'BUDGET REACHED: <B> s (<source>); scanned <n> of 166 lambda; ... resume: comp-iam resource-sweep --cursor <name>'. attach-census (no internal resumption point): 'NOT WITHIN BUDGET: the _build() pass took <t>s ... but it already RAN TO COMPLETION ... Disclosed non-application of the early-abort half of Rule T for this specific subcommand shape.'", "before_this_cell": "PRESENT-BUT-ABSENT -- the TO's own MEASURED-at-cut text: 'no timeout' (PRD s.7 T-8); simulate's live boto3 calls ran under boto3's own 60s/60s defaults, deaf to any caller ceiling; resource-sweep/attach-census's _build() pass had no ceiling or disclosure at all."}
  },

  "answer_state": {
    "schema_note": "Spellings per the RATIFIED enum (PRD v0.4 s.4.3, org/standards/COMPTOOL_ANSWER_STATE.enum.json). None of comp-iam's four planted cases below print the enum's bare state name as a literal token -- same posture as comp-find's precedent (declared_by_tool: false throughout) -- but PARTIAL_OR_BLIND's adopted tool-voice token, NOT-DECIDABLE, IS printed literally by this cell's own STATE: line (see finding F4).",
    "SUBJECT_ABSENT_FROM_CORPUS": {"planted": "comp-iam service ZZZ_NONEXISTENT_SERVICE_93999 (no Lambda profile, no IAM role matches)", "printed": "\"No service matching 'ZZZ_NONEXISTENT_SERVICE_93999'\" followed by a 15-of-187 Lambda candidate list and a 15-of-180 role candidate list, both truncated with an explicit '... and N more' count", "rc": 0, "finding": "the tool's OWN candidate-list behaviour is a real usability win over comp-find's silent zero-files degrade (T-1's F4) -- a miss here hands the caller real, present alternatives, not just a bare zero."},
    "PRESENT_WITH_ZERO_RESULTS": {"planted": "comp-iam gaps astn-wsjft-scraper (a real, TF-mapped Lambda+role pair with zero action gaps and zero resource mismatches)", "printed": "'No ACTION-plane findings for service filter: astn-wsjft-scraper' / 'No MISSING-permission gaps among MODELED services.' / 'RESOURCE PLANE: 6 call(s) verdicted across 1 mapped role(s); 5 UNRESOLVABLE-RESOURCE, 1 GRANTED-BROAD' / 'Total: 0 missing | 0 deny-present | 0 coverage-unknown | 0 resource-mismatch across 0 service(s)'", "rc": 0, "distinguishable_from_absent_by": "the RESOURCE PLANE line's second number: '1 mapped role(s)' (PRESENT, checked, clean) vs the total absence of any such line for a subject that never matched a profile at all (SUBJECT_ABSENT never reaches the plane banner or the RESOURCE PLANE line)"},
    "PARTIAL_OR_BLIND": {
      "planted_a": "comp-iam simulate-self-test case 3 (a conditioned statement with MissingContextValues, no --context passed) -- OFFLINE stub, zero live IAM calls",
      "printed_a": "'VERDICT: CONDITIONED-UNEVALUATED -- a conditioned statement was evaluated with no context, and that returns implicitDeny BYTE-IDENTICAL to a real deny (22a false-deny mode 2). This is NOT a deny verdict.' / 'STATE: NOT-DECIDABLE'", "rc_a": 2,
      "planted_b": "comp-iam reconcile --census-ttl-hours 0.0001 (forces the real, existing 20260903 census, generated 0.2h earlier, to read STALE against an artificially tiny TTL)",
      "printed_b": "'CENSUS PROVENANCE: ... (age 0.2h, TTL 0.0001h) [STALE]' / 'REFUSED: APPLIED reconcile NOT PERFORMED -- the census is STALE (older than the 0.0001h TTL). This is a COVERAGE refusal, not a clean result ... Override (AUDITED ...): --allow-stale-census'", "rc_b": 3,
      "both_never_deny_never_allow": "neither case's rc or text is DENIED/ALLOWED-shaped: (a) is NOT-DECIDABLE by its own explicit STATE line; (b) is REFUSED at rc 3, a THIRD distinct rc from reconcile's own 0=clean/1=drift-found -- 'refused' is comp-reconcile's tool-voice for this state, a different word from simulate's NOT-DECIDABLE but the same state, matching the TO's own acceptance text verbatim ('both must read NOT-DECIDABLE / refused, never DENIED and never ALLOWED')",
      "rc": "2 (a) / 3 (b)"
    },
    "NOT_APPLICABLE": {"planted": "comp-iam service opal-inf-value-parity (a real, matched profile whose entry point, infra/aws/compdiff/lambda_function.py, binds no boto3 client at all -- the exact specimen resource-sweep's own docstring names)", "printed": "'SERVICE: opal-inf-value-parity [lambda]' / 'IAM role: (not mapped)' / [the two unconditional floor caveats] / 'No AWS operations detected.'", "rc": 0, "declared_by_tool": false, "distinguishable_from_absent_by": "the SERVICE header prints (subject matched, present in the corpus) before the zero-population statement -- SUBJECT_ABSENT never reaches that header at all", "finding": "the tool has no literal NOT_APPLICABLE voice for 'this subject exists but has no population for the question' -- it reads 'No AWS operations detected', a correct but un-enum-worded statement, same shape as T-16's own original finding on a different tool"},
    "verdict": "PASS on T8-AC2/AC3 as measured: the four planted cases (five printed shapes, PARTIAL_OR_BLIND carrying two) are pairwise DISTINGUISHABLE by rc, by header presence, and by the RESOURCE PLANE's second number -- never by rc alone (SUBJECT_ABSENT, PRESENT_WITH_ZERO, and NOT_APPLICABLE all share rc 0). The deny three-state (T8-AC3's own graded surface) never mis-reads a false deny as ALLOWED or a genuine unproven deny as DENIED across all 6 stub cases (see Rule-T/three-state section below)."
  },

  "three_state": {
    "schema_note": "The CELL's own closes-on, a narrower axis than the four-state answer_state above: every deny-shaped answer cmd_simulate prints is exactly one of STATE_ALLOWED / STATE_DENIED / STATE_NOT_DECIDABLE (org/modules/graph/iam_cli.py :48-50), machine-rejectable by the literal 'STATE: <TOKEN>' line this cell added.",
    "real_deny_case": {"stub": "role holds s3:GetObject on arn:...:A/held (control); target arn:...:B/new denies", "printed": "'VERDICT: DENIED (implicitDeny), control-proven -- the instrument demonstrably CAN say allowed for this role, so this deny discriminates.' / 'STATE: DENIED'", "rc": 1},
    "false_deny_case": {"stub": "target arn:...:B/new returns implicitDeny WITH MissingContextValues=['aws:SourceVpc'] (22a false-deny mode 2)", "printed": "'VERDICT: CONDITIONED-UNEVALUATED ... This is NOT a deny verdict.' / 'STATE: NOT-DECIDABLE'", "rc": 2},
    "side_by_side": "the pair above is the TO's own required 'real deny vs false deny, shown side by side' -- both from the OFFLINE stub suite (_simulate_self_test cases 2 and 3), zero live IAM calls, both exercised together in this cell's new external battery (IAM-AC3-STATE-TOKEN-CENSUS)",
    "multi_arn_refusal": "'REFUSED: one resource ARN per call ... a call carrying 2+ --resource-arns flips the HELD ones to implicitDeny' printed and the call REFUSED (rc 2, zero simulate_principal_policy calls made) before any decision -- never a HELD ARN silently read as denied",
    "deferred_bucket_new_this_cell": "case 6 (added this cell): a transport exception on the TARGET call -> 'DEFERRED: call did not complete within 90s (default) -- TimeoutError: ...' / 'STATE: NOT-DECIDABLE', rc 2 -- Rule T's DEFERRED bucket landing INSIDE the three-state machine rather than beside it: a deferred call is NOT-DECIDABLE, never silently absent from the state, never misread as a deny",
    "census_past_ttl": "reconcile's stale-census refusal (rc 3, 'REFUSED') is a DIFFERENT subcommand's tool-voice for the same state family, not a fourth STATE: token -- the three literal STATE_* constants live only in cmd_simulate; reconcile's refusal is text-shaped, not token-shaped (finding F5)"
  },

  "rule_t": {
    "carrier": "the ONE shared module .tools/_compbudget.py @2718cffc45 (landed by CE-t-1), imported at iam_cli.py:42, consumed not edited -- precedence --budget > env COMP_BUDGET_S > default 90s, disclosed on every run via disclosure_line()",
    "help_discloses_it": "quoted verbatim above (identity.self_identifies + disclosure.timeout) for all three of simulate/resource-sweep/attach-census's --help text; --budget documented nowhere before this cell",
    "three_call_shapes_this_cell_wired": [
      {"shape": "networked, per-call timeout", "subcommand": "simulate", "mechanism": "botocore.config.Config(connect_timeout=budget_s, read_timeout=budget_s); a transport failure lands in the DEFERRED bucket (_one_call's except), never a hang, never a decision"},
      {"shape": "resumable per-unit loop", "subcommand": "resource-sweep", "mechanism": "Clock.remaining() checked once per lambda in the deterministic sorted-by-name loop; a mid-loop expiry stops at the last FULLY-checked unit and prints a real --resume-after cursor (exercised: default budget completes 166 of 166; --resume-after <first-name> completes exactly 165 of 165, the true population minus one; --budget 0.00001 prints BUDGET REACHED with NO CURSOR YET, zero lambdas completing before expiry)"},
      {"shape": "one opaque non-resumable call", "subcommand": "attach-census", "mechanism": "Clock measures _build()'s wall time post-hoc (no internal abort point exists inside a synchronous Terraform parse); WITHIN BUDGET on a generous budget, an honest 'NOT WITHIN BUDGET ... but it already RAN TO COMPLETION ... Disclosed non-application' on a tiny one -- never a fabricated partial answer"}
    ],
    "non_application_stated": "attach-census's early-abort half is the ONE disclosed non-application in this cell (matches CE-t-1's own unscoped-aws-pull non-application, same PRD s.4.4 grammar, different underlying reason -- there it was a measured 247.5s discovery cost, here it is a synchronous parse with no safe mid-point to abort at)",
    "exercised_end_to_end": true
  },

  "bounds": {
    "zero_iam_change": "no principal, policy, role, attachment or resource was created, changed or granted this cell. Live calls made: ZERO -- every case above (three-state, DEFERRED, Rule T) was planted through the OFFLINE stub suite (_simulate_self_test's Stub class, zero AWS); resource-sweep/attach-census's real _build() calls are a LOCAL Terraform parse, not an AWS API call; reconcile's stale-TTL case forced a REFUSAL specifically so the comparison against the live-shaped census.json never ran. The only genuinely live-API-capable path in this tool (cmd_simulate's real boto3.client path) was never invoked with a real client this cell.",
    "census_format_gap_semantics_unchanged": "confirmed by inspection -- no field added/removed/renamed in comp_iam_census.py, no verdict enum member added/removed in extract_iam.py this cell; the three-state is additive VOICE on cmd_simulate's existing rc contract (0/1/2 unchanged), never a new census shape",
    "no_new_dependency_no_new_file_outside_named": "git diff --stat c2f70f7ca4..eb7966105a -- org/modules/graph/iam_cli.py: 144 insertions(+), 9 deletions(-), 0 files added/removed besides the one new battery file (.tools/tests/test_comp_iam_battery.py, TOOL_BATTERIES lane) and this deliverable + its proof instance",
    "spec_vs_world_divergence": "none surfaced this cell that rises to a row (S9's own precedent, see header); one audit finding (F4) noted for the record instead"
  },

  "passcraft": {
    "moves_1_to_8": [
      {"move": 1, "status": "DONE", "falsifier_answer": "the shim (.tools/comp-iam, 8 lines) forwards verbatim to iam_cli.py, the real engine (1,759 lines); iam_cli.py imports three SIBLING engine files (comp_iam_live/census/investigate) directly, not through a further delegate, plus two LIBRARY imports (extract_iam for TF parsing, _compbudget for Rule T)"},
      {"move": 2, "status": "DONE", "falsifier_answer": "write surfaces: org/mcp/comp-tool-runs.jsonl + org/mcp/comp-which-rail.log (fire-and-forget telemetry via comp_log_auto.py in the shim, same pattern as comp-find); refresh-census additionally WRITES docs/briefs/cmpaws-iam-census-<date>.json -- a real, load-bearing artifact other subcommands (reconcile) read back, not a pure sink"},
      {"move": 3, "status": "DONE", "falsifier_answer": "no cache for the DESIRED plane (fresh Terraform parse every _build() call, no memoization -- confirmed by reading _build()'s one-line body); the APPLIED plane (reconcile) reads a dated JSON snapshot on disk, explicitly NOT live at call time -- its own vintage gate exists BECAUSE it is a cache with a TTL, not a live oracle"},
      {"move": 4, "status": "DONE", "falsifier_answer": "target universe FROM SOURCE: `comp-iam stats` (180 roles, 187 services, 1074 operations) cross-checked against `comp-iam gaps` default run (same _build() call, same process) -- consistent by construction (one shared parse, two views); NOT independently re-derived from a raw Terraform grep this cell (out of circle; BOUNDS: no new file/tooling)"},
      {"move": 5, "status": "DONE", "falsifier_answer": "five printed shapes across four states verified from OUTPUT differing (rc: 0/0/2-or-3/0; header presence; the RESOURCE PLANE second number; the literal STATE: token) -- confirmed by direct execution each, not asserted from reading the source alone"},
      {"move": 6, "status": "DONE", "falsifier_answer": "both battery mutants live BESIDE the real engine (org/modules/graph/_tmp_iam_mutant_<kind>_<pid>.py) so the depth-sensitive _WORKSPACE = 3-parents-up computation resolves correctly -- a lesson one layer stricter than comp-find's sibling-import fixture defect, found and fixed live (see battery docstring); both mutant files confirmed removed after each run"},
      {"move": 7, "status": "PARTIAL", "falsifier_answer": "the --resume-after arm's ground truth (the sorted lambda population and its first name) was derived from a SECOND, independent direct in-process _build() call inside the battery, not from the subprocess run being graded -- a real corroborating instrument, though both ultimately read the same underlying Terraform tree (not a fully non-sharing substrate the way comp-find's raw Cypher count was against a separate DB engine)"},
      {"move": 8, "status": "DONE", "falsifier_answer": "archetype hand-classified below; probed: guard-asymmetry (clean -- SUBJECT_ABSENT and NOT_APPLICABLE both rc 0, distinguished by header/plane-line presence, not by an asymmetric guard), success-token-bound-to-wrong-step (FOUND, F5 below -- reconcile's REFUSED at rc 3 is a DIFFERENT token-shape from simulate's STATE: NOT-DECIDABLE for the same PARTIAL_OR_BLIND state), aging-oracle (clean for the APPLIED plane -- reconcile reads the census's own generated_utc field, never a filesystem mtime; DIRTY for the DESIRED plane -- F2/vintage finding above), terminal-honest/artifact-lies (clean -- DENOMINATOR lines cross-checked against stats), correct-but-unwired (clean -- Rule T's --help disclosure is live and this cell's own battery exercises it)"}
    ],
    "archetype": "TWO-PLANE cross-reference instrument (DESIRED via Terraform parse, APPLIED via live simulate or a dated census) whose rc is bound to EXECUTION on most subcommands (0 regardless of gap count) but bound to VERDICT SEVERITY on the two rc-gating surfaces this cell touched: resource-sweep (1 if flagged) and reconcile (0 clean / 1 drift / 2 usage-error / 3 refused) and cmd_simulate (0 allowed / 1 denied-proven / 2 everything-else-including-refused). A consumer must read WHICH surface it called before trusting rc at all -- the three surfaces disagree with each other on what rc means by design, not by drift.",
    "findings": [
      {"id": "F1", "shape": "success-token-bound-to-wrong-step (three coexisting denominators)", "cite": "org/modules/graph/iam_cli.py cmd_stats vs cmd_gaps vs cmd_gaps' own resource plane @eb7966105a", "text": "'Permission gaps: 306' (stats, ALL raw gap objects incl. deny-present+unmodeled) vs 'Total: 14 missing' (gaps' action plane, ERROR severity only) vs '2 resource-mismatch' (gaps' resource plane) -- three real, honestly-labeled, non-overlapping counts that all answer 'how many gaps' differently enough to mis-cite by accident if a reader quotes one without its qualifier"},
      {"id": "F2", "shape": "aging-oracle (split by plane)", "cite": "iam_cli.py's DESIRED-plane subcommands @eb7966105a vs cmd_reconcile's CENSUS PROVENANCE line", "text": "every Terraform-parse subcommand (gaps/service/role/roles/stats/resource-sweep/attach-census) prints no git sha, mtime, or dirty-flag for the trees it read -- the exact T-1 file-corpus vintage gap, one tool over. The APPLIED-plane census DOES disclose vintage; the DESIRED plane, which is most of this tool's surface, does not."},
      {"id": "F3", "shape": "guard-asymmetry-adjacent (naming collision, not a routing gap)", "cite": ".tools/comp-iam-usage vs .tools/comp-iam @eb7966105a", "text": "two separate tools sharing a name prefix and no cross-reference in either's --help; a reader typing 'comp-iam usage' style guesses could reasonably expect a usage-stats mode of THIS tool rather than a different engine entirely"},
      {"id": "F4", "shape": "positive (convergent carrier, stated for the record)", "cite": "org/standards/COMPTOOL_ANSWER_STATE.enum.json states[PARTIAL_OR_BLIND].tool_voice.carrier vs org/modules/graph/iam_cli.py:919,852,843 @eb7966105a", "text": "the enum's carrier census (taken 2026-09-03 before this cell) names ONLY .tools/comp-schedule as a live carrier of the adopted 'NOT-DECIDABLE' token. This cell's own STATE_NOT_DECIDABLE constant, chosen independently from CLAUDE.md 22a's own vocabulary (never by reading the enum file), is a SECOND, now-existing code carrier of the byte-identical hyphenated spelling -- a convergence, not a copy. Not a spec-vs-world divergence (nothing in the enum's BINDING is violated; 'binds by reading', no gate); recorded here as the audit's own content per S9's precedent, not filed as a row. Residual, not urgent: the enum's carrier list is now one entry stale; updating it is the L4 owner's (1.0.0_SA_CTO's) act, not this cell's -- no task order exists for it."},
      {"id": "F5", "shape": "success-token-bound-to-wrong-step", "cite": "cmd_simulate's STATE: NOT-DECIDABLE vs cmd_reconcile's REFUSED (rc 3) @eb7966105a", "text": "both are the SAME PARTIAL_OR_BLIND state (per the TO's own acceptance text) but print in two structurally different shapes -- a literal grep-able token in one subcommand, a prose word plus a distinct rc in the other. A consumer that greps only for 'STATE: NOT-DECIDABLE' across this tool's whole surface would miss reconcile's stale-census refusal entirely."}
    ]
  },

  "usage": {
    "runs_30d": {
      "runs_jsonl": {"count": "354 rows mentioning \"comp-iam\" of 27,775 total (org/mcp/comp-tool-runs.jsonl, device-local, gitignored)", "note": "not decomposed into 30d-vs-all-time at this read; the file's own retention window is not verified this cell"},
      "rail_log": {"count": "3,523 rows mentioning comp-iam of 49,193 total (org/mcp/comp-which-rail.log)", "note": "device-local instrument per CLAUDE.md's own warning; the TO's own MEASURED-at-cut figure was 113 runs (a narrower or differently-scoped count than either instrument above -- not reconciled this cell)"}
    },
    "hook_driven": {"fraction": "not sampled this cell (out of circle; T-1's identical check found 0 of 143+ carrying a to_id, offered as the closest prior)"},
    "battery": {
      "files": [
        {"path": "org/modules/graph/iam_cli.py's own _simulate_self_test (embedded, :923-988, was 5 cases, now 6/6 with this cell's DEFERRED case)", "collects_under_pytest": "not a pytest entry point (direct-invocation self-test, `comp-iam simulate-self-test`); run directly: 6/6 PASS", "red_first_mutant": "not applicable -- each case IS its own planted defect against a stub, not a mutant of the tool"},
        {"path": ".tools/tests/test_comp_iam_battery.py (NEW this cell, 254 lines)", "collects_under_pytest": "1 test, 67.77s (real _build() calls dominate: 5 of 8 arms parse this repo's live Terraform tree)", "red_first_mutant": true, "mutant_forms": "state_flip (STATE: NOT-DECIDABLE -> STATE: ALLOWED on the missing-context branch, proving the self-test's OWN rc-based grading is insufficient) AND budget_ignored (resource-sweep's per-iteration clock.remaining() check neutered) -- BOTH mutants RUN (not crash) and FAIL their sibling arm's predicate; both DO"}
      ],
      "file_grain_result": "8/8 PASS (IAM-AC3-STATE-TOKEN-CENSUS, IAM-AC3-MUTANT-FALSE-ALLOW-DETECTED, IAM-AC5-SWEEP-WITHIN-BUDGET, IAM-AC5-SWEEP-RESUME-AFTER, IAM-AC5-SWEEP-BUDGET-REACHED-NO-CURSOR, IAM-AC5-ATTACH-CENSUS-WITHIN-BUDGET, IAM-AC5-ATTACH-CENSUS-DISCLOSED-NONAPPLICATION, IAM-AC5-MUTANT-BUDGET-IGNORED-DETECTED) -- confirmed direct AND under pytest -q; commit-gate clean 2/2 files",
      "lane_sweep": "not re-run this cell (T-1's 2026-09-02 census of the known pytest --collect-only INTERNALERROR at test_fabric_check_classify.py is the closest prior, unchanged in nature; not independently re-confirmed here -- out of this TO's circle)"
    },
    "overlap": "comp-iam-usage remains a live, separate implementation answering the lifecycle question comp-iam does not (F3); comp-iam does not consume or wrap it",
    "proposed": "CLEARED-candidate for T8-AC1..AC5 as measured above; the project-wide CLEARED disposition is CVO's grade to render. Five findings (F1-F5) named above, none blocking; F1/F2/F3 are pre-existing (not introduced by this cell); F4 is a positive convergence, not a defect; F5 is introduced by this cell's own new voice and is named for the record, not fixed (BOUNDS: census format and gap semantics do not change under this TO -- reconcile's rc/text shape is reconcile's own surface, unchanged here)."
  }
}
```

## The four planted answer-state cases, quoted in full

**SUBJECT_ABSENT_FROM_CORPUS** -- `comp-iam service ZZZ_NONEXISTENT_SERVICE_93999`, rc 0:
```
No service matching 'ZZZ_NONEXISTENT_SERVICE_93999'

  Lambda services (187):
    access-anomaly-scanner
    advi-49f-gold-dispatch
    ... and 172 more (use 'comp-iam services' to list all)

  IAM roles (180):
    ... and 165 more (use 'comp-iam roles' to list all)
```

**PRESENT_WITH_ZERO_RESULTS** -- `comp-iam gaps astn-wsjft-scraper` (real, mapped, clean), rc 0:
```
No ACTION-plane findings for service filter: astn-wsjft-scraper

No MISSING-permission gaps among MODELED services.

  RESOURCE PLANE: 6 call(s) verdicted across 1 mapped role(s); 5 UNRESOLVABLE-RESOURCE, 1 GRANTED-BROAD
    1 GRANTED-BROAD row(s) are EXCLUDED, NOT CLEARED -- a wildcard grant cannot be falsified by a resource check

Total: 0 missing | 0 deny-present | 0 coverage-unknown | 0 resource-mismatch  across 0 service(s)
```

**PARTIAL_OR_BLIND**, two limbs of the same state -- (a) `simulate-self-test` case 3 (offline stub, missing context), rc 2:
```
VERDICT: CONDITIONED-UNEVALUATED -- a conditioned statement was evaluated with
  no context, and that returns implicitDeny BYTE-IDENTICAL to a real deny
  (22a false-deny mode 2). This is NOT a deny verdict. Re-run with:
    --context aws:SourceVpc=<type>:<value>
STATE: NOT-DECIDABLE
```
(b) `comp-iam reconcile --census-ttl-hours 0.0001` (forced stale), rc 3:
```
CENSUS PROVENANCE: cmpaws-iam-census-20260903.json -- generated 2026-09-03T06:46:12Z (age 0.2h, TTL 0.0001h) [STALE]

REFUSED: APPLIED reconcile NOT PERFORMED -- the census is STALE (older than the 0.0001h TTL).
  This is a COVERAGE refusal, not a clean result: nothing was compared, so nothing
  can be concluded about live-vs-Terraform drift. DESIRED-plane modes are unaffected
  (`comp-iam gaps` / `roles` / `role` still answer from Terraform).
  Fix: `comp-iam refresh-census` then re-run -- the newest dated census
  auto-resolves (no --census needed since 2026-08-05).
  Override (AUDITED, and it makes the verdict non-authoritative): --allow-stale-census
```

**NOT_APPLICABLE** -- `comp-iam service opal-inf-value-parity` (matched, zero population), rc 0:
```
SERVICE: opal-inf-value-parity  [lambda]
  IAM role: (not mapped)
  Source files: infra/aws/compdiff/lambda_function.py
  NOTE: operation list = literal boto3.client()/boto3.resource() call sites, PLUS helper-constructed
  clients this AST pass can resolve ('[via helper]' rows) -- a DYNAMIC service arg to a helper renders
  as UNRESOLVED-CLIENT, never silently dropped. Still a FLOOR, not a census: a cross-file helper or an
  unmodeled construction shape is untraced with no signal.
  THIS OPERATION LIST IS A FLOOR, NEVER A DELETION WARRANT: a row absent here is NOT proof a grant is
  unused -- it may be DEFERRED/UNTRACED (see below) or simply untraced by this tool. Never delete a
  grant on this list's silence alone.

  No AWS operations detected.
```

## The deny three-state, real-deny vs false-deny side by side (T8-AC3)

Real deny, control-proven, rc 1:
```
VERDICT: DENIED (implicitDeny), control-proven -- the instrument demonstrably CAN say
  allowed for this role, so this deny discriminates. APPLIED plane.
STATE: DENIED
```
False deny (22a mode 2), rc 2, NEVER printed as DENIED:
```
VERDICT: CONDITIONED-UNEVALUATED -- a conditioned statement was evaluated with
  no context, and that returns implicitDeny BYTE-IDENTICAL to a real deny
  (22a false-deny mode 2). This is NOT a deny verdict.
STATE: NOT-DECIDABLE
```
Rule T's DEFERRED bucket landing inside the same machine (case 6, new this cell), rc 2:
```
  [TARGET] s3:GetObject on arn:aws:s3:::B/new
      DEFERRED: call did not complete within 90s (default) -- TimeoutError: stub transport timeout (Rule T DEFERRED case)
STATE: NOT-DECIDABLE
```
All six `_simulate_self_test` cases: 6/6 PASS, offline, zero AWS calls.

## Rule T, exercised end to end on all three call shapes (the code change this cell owed)

```
$ comp-iam resource-sweep --budget 0
  WITHIN BUDGET: scanned 166 of 166 lambda; budget: unbounded (--budget 0), used 14.16 s

$ comp-iam resource-sweep --budget 0 --resume-after access-anomaly-scanner
  WITHIN BUDGET: scanned 165 of 165 lambda; budget: unbounded (--budget 0), used 13.95 s

$ comp-iam resource-sweep --budget 0.00001
  BUDGET REACHED: 1e-05s (flag); scanned 0 of 166 lambda(s); results are a PREFIX, not the
  answer; NO CURSOR YET: no lambda completed before the budget hit, so there is no
  last-processed unit to resume from; resume: re-run with a larger --budget.

$ comp-iam attach-census --budget 0
  WITHIN BUDGET: scanned 1 of 1 build_pass; budget: unbounded (--budget 0), used 13.5 s

$ comp-iam attach-census --budget 0.00001
  NOT WITHIN BUDGET: the _build() pass took 12.86s, over the budget: 1e-05 s (flag) -- but it
  already RAN TO COMPLETION (this call has no internal resumption point to abort at; a
  truthful complete answer, not a fabricated partial one). Disclosed non-application of the
  early-abort half of Rule T for this specific subcommand shape.
```
Note the byte-exact inconsistency between the two quoted BUDGET REACHED-family lines above: the
custom no-cursor branch in `cmd_resource_sweep` prints `{fmt(budget_s)}s` (no space before the
unit) while `_compbudget.budget_reached_line()` and `attach-census`'s own disclosure both print
`{fmt(budget_s)} s` (space) -- a pre-existing, this-cell-inherited formatting drift between one
inline branch and the shared carrier's own template, cosmetic only (both remain the unambiguous
BUDGET REACHED / NOT WITHIN BUDGET tokens D1 grades on), not fixed here (BOUNDS: this cell's code
change is the budget carrier + the three-state, not a carrier-template rewrite). Both resume-after
and the tiny-budget cases are exercised as automated battery arms (IAM-AC5-*), not hand-run once
and discarded -- values above are the exact predicates the battery checks (`WITHIN BUDGET: scanned
(\d+) of \1 lambda`, `total_n` and `total_n - 1` cross-checked against a second, independent
in-process `_build()` call rather than a hard-coded lambda count or name).

## Findings F1-F5 (none blocking; F4 is a positive convergence)

See `passcraft.findings` in the JSON block above for the full text. Summary: F1 (three
non-overlapping "gaps" denominators across stats/gaps/gaps-resource-plane, each honestly
labeled), F2 (the DESIRED-plane vintage gap, comp-find's own T-1 finding one tool over), F3
(comp-iam-usage is a same-name-prefix SEPARATE tool, not an alias), F4 (this cell's own
STATE_NOT_DECIDABLE independently converges on the enum's ratified NOT-DECIDABLE token without
having read the enum file -- the enum's own carrier census is now one entry stale, an L4-owned
residual, not a row per S9's precedent), F5 (the same PARTIAL_OR_BLIND state prints as a literal
token in `simulate` and as prose+rc in `reconcile` -- a grep for one misses the other).

## Captures and controls

Every quoted run above is a direct execution captured in this session. Production sha:
`org/modules/graph/iam_cli.py` was `c2f70f7ca4` (2026-08-11, before this cell) ->
`eb7966105a` (2026-09-03T06:55:35Z, this cell's fix commit, 144 insertions / 9 deletions, 0 files
added besides the new battery + this deliverable + its proof instance). Battery: 6/6
(`_simulate_self_test`, extended) + 8/8 (`.tools/tests/test_comp_iam_battery.py`, new) -- both
confirmed direct AND under pytest; commit-gate clean 2/2 files. `git status` at write time: only
this deliverable + its proof-of-spec instance uncommitted among files this cell touched (the
repo's pre-existing, pre-reboot untouched modifications named in the 2026-09-03T06:43Z
MERGE_WINDOW_CLOSE broadcast are NOT this cell's and are left alone). Push state, MEASURED
(ls-remote + is-ancestor) at write time: `origin/CLOUD` read via `git ls-remote`; `git merge-base
--is-ancestor eb7966105a origin/CLOUD` -> non-zero (LOCAL ONLY) -- the expected state while Andrew
gates the cadence (CLAUDE.md's standing push hold). T8-AC6 reads MEASURED-LOCAL on this
measurement, not asserted from the commit alone.
