# comp-adversary -- NFRA_COMPEFFICACY per-tool result (PRD s.4 schema)

Schema: `org/tier1_exec/3.0.0_SA_CVO/deliverables/NFRA_COMPEFFICACY_PRD_DRAFT_v0.1.md` s.4 @`cd6d1db77d`
(the draft binds until 1.0.0_SA_CTO lands it; CVO 92791 "read the draft, do not wait for the landing").
Row: T-16. Measured by 0.8.0_AE_CloudComp, 2026-09-02 22:03Z-22:35Z, read-vintage HEAD @`5fc5038daa`,
engine @`4c3b848c97`. Every value below is MEASURED on this box unless its own field says otherwise;
every run's full output is quoted from a saved capture, never from memory.

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD_DRAFT_v0.1 s.4 @cd6d1db77d",
  "row": "T-16",
  "measured_by": "0.8.0_AE_CloudComp",
  "measured_at_utc": "2026-09-02T22:03Z..22:35Z",
  "read_vintage": "HEAD @5fc5038daa",

  "identity": {
    "tool": "comp-adversary",
    "shim_path": ".tools/comp-adversary (626)",
    "engine_path": ".tools/comp-adversary (626) -- SELF-CONTAINED: 0 sibling-engine imports; comp-passcraft MOVE 1 'kind: self, backends: (self-contained)'",
    "engine_vintage": "4c3b848c97 (2026-09-02T17:42Z)",
    "aliases": [],
    "registration": {
      "graph_call_manifest": "member of excluded_not_graph_use_cases at :33 ONLY; no tools_index row (3 hits / 1861 lines, all :33)",
      "comp_tools_yaml": "ABSENT (0 hits / 905 lines) -- the comp-which catalog cannot route to it by purpose",
      "skill": ".claude/skills/comp-adversary/SKILL.md (present)"
    },
    "purpose_1line": "validator-context COMPOSER (v1, functional -- Andrew-direct 2026-08-19)  [engine docstring :2]",
    "self_identifies": {
      "help_prints_name_and_version": true,
      "help_prints_engine_path": false,
      "version_flag": "UNSUPPORTED -- `--version` prints 'unknown mode: --version (see --help)'",
      "output_line_1": "# validation_context_declaration -- comp-adversary v1",
      "grade": "PARTIAL (name + v1 on every output; no engine path; no --about/--version mode)"
    }
  },

  "disclosure": {
    "run": "DEFAULT flags, `compose org/tier1_exec/3.0.0_SA_CVO/deliverables/CVO_FINDING_comp_similar_provenance_20260902.md` -- rc 0, 38 s, 611 lines stdout, 0 stderr",
    "subject":             {"grade": "PRESENT", "quoted": "artifact: org/tier1_exec/3.0.0_SA_CVO/deliverables/CVO_FINDING_comp_similar_provenance_20260902.md / artifact-vintage: ef7d81ad43 (2026-09-02T10:23:29)"},
    "corpus_or_backend":   {"grade": "PRESENT", "quoted": "read-vintage: HEAD @5fc5038daa at 2026-09-02T22:03:02Z  [pin kind: read-vintage]  (the repo at HEAD; stage 4 names its instrument: 'source 5: comp-read digests of the complement')"},
    "vintage":             {"grade": "PRESENT", "quoted": "read-vintage HEAD @5fc5038daa + timestamp; artifact-vintage ef7d81ad43; each cited path's last-change date ('MOVED-SINCE-AUTHORING (last change 2026-09-02T11:30:41 postdates the artifact)')"},
    "denominator":         {"grade": "PRESENT", "quoted": "complement sources: 5 run / 0 deferred-with-reason / 5 declared-excluded | source 1: (2 attempted / 2 verified / 0 UNVERIFIABLE) | total uncited siblings: 18 (showing 18 -- the CAP is declared, not silent) | selected: 12 of 18 | NOT DIGESTED: 6 of 18 siblings -- 6 beyond the budget, 0 non-text"},
    "resolved_unresolved": {"grade": "PRESENT", "quoted": "2 attempted / 2 verified / 0 UNVERIFIABLE | !! 1 hex run(s) not parsed as pins (2 were): 54e0058551"},
    "blind_spots":         {"grade": "PRESENT", "quoted": "five DECLARED EXCLUSIONS each with a reason (e.g. 'toolgraph SHARES_SUBSTRATE independence : v1: toolgraph consumption not wired'); 'trace-to-authority claims are UNANSWERABLE from this declaration alone and are not implied'; 'THE PACKET IS A SELECTION, NOT A SURVEY'"},
    "pagination":          {"grade": "PRESENT (Rule P disclosure-line form; page flags = non-application)", "quoted": "total uncited siblings: 18 (showing 1 -- the CAP is declared, not silent)  [--max-neighbors 1 run] | budget: 12 file(s) at <=2400 bytes each (raise with --digest-budget/--digest-bytes) | ... DIGEST TRUNCATED at N of M bytes", "note": "no --page/--limit/--all; output is bounded by the artifact's citation set and three constant caps, and every cap prints its true total"},
    "timeout":             {"grade": "PRESENT-BUT-WRONG", "quoted": "at the ceiling, per digest: 'DEFERRED: comp-read unavailable: TimeoutExpired' (12 of 12 when forced); rc 0", "wrong_part": "the packet's roll-up lines ('selected: 12 of 18', 'NOT DIGESTED: 6 of 18 -- 6 beyond the budget, 0 non-text') are UNCHANGED when all 12 digests time out -- no deferred bucket in the denominator (F2); no timeout flag; the outer harness ceiling is not known to the tool"}
  },

  "answer_state": {
    "SUBJECT_ABSENT_FROM_CORPUS": {"planted": "compose ./ZZZS4_NOSUCH_0902.md (path does not exist)", "printed": "ERROR: artifact not found: ./ZZZS4_NOSUCH_0902.md", "rc": 2, "lines": 1},
    "PRESENT_WITH_ZERO_RESULTS":  {"planted": "a real 3-line .md with no commit pin, path or tool mention", "printed": "pins found: 0 commits, 0 repo paths, 0 file:line cites, 0 tool mentions / !! ZERO MACHINE-EXTRACTABLE PINS ... A zero here is a signal, never a clean pass. / every source '0 attempted'", "rc": 0, "lines": 64},
    "PARTIAL_OR_BLIND":           {"planted": "the multi-pin artifact with --max-neighbors 1 --no-packet", "printed": "total uncited siblings: 18 (showing 1 -- the CAP is declared, not silent) / SKIP: --no-packet given. Stage 4 was DISABLED BY THE CALLER for this run; the complement above is POINTERS ONLY", "rc": 0, "lines": 59, "says_which_part": true},
    "NOT_APPLICABLE":             {"planted": "compose <a directory>", "printed": "Traceback ... parse_artifact :94 open(path) -> PermissionError: [Errno 13] Permission denied (IsADirectoryError on POSIX)", "rc": 1, "lines": 13, "declared_by_tool": false, "second_probe": "a .json artifact composes as prose (0 pins, treated as PRESENT_WITH_ZERO); the tool has no N/A vocabulary -- it composes or it crashes"},
    "verdict": "PASS on the PRD criterion (four cases, four distinguishable outputs) WITH finding F1: the fourth state is spoken by the interpreter, not the tool (FWD-2 'says so in a way a machine can reject': rc 1 rejects; the vocabulary is Python's and platform-dependent)"
  },

  "bounds": {
    "subprocess_timeouts": [
      {"file_line": ".tools/comp-adversary:279 @4c3b848c97", "value_s": 60,  "wraps": "python .tools/comp-read <sibling>  (stage-4 digest, once per selected file, up to 12)"},
      {"file_line": ".tools/comp-adversary:297 @4c3b848c97", "value_s": 120, "wraps": "python .tools/comp-state --json  (drift source)"}
    ],
    "ceiling_behaviour": {
      "exercised": true,
      "how": "a COPY beside the tool (.tools/.mutant-comp-adversary-s4ceiling) with :279 timeout=60 -> 0.01; production sha 824edcb54b12b933 before and after; copy removed",
      "first_attempt": "timeout=1 s did NOT fire (every digest completes under 1 s) -- 611 lines, identical to the default run",
      "printed_at_ceiling": "DEFERRED: comp-read unavailable: TimeoutExpired  -- once per digest, 12 of 12; rc 0; 109 lines",
      "not_printed": "no roll-up of the 12 deferrals: 'selected: 12 of 18' and 'NOT DIGESTED: 6 of 18 -- 6 beyond the budget, 0 non-text' read exactly as in the healthy run (F2)"
    },
    "page_contract": {"page_flag": false, "limit_flag": false, "all_flag": false, "true_total_printed": true, "cap_flags": "--max-neighbors N (default 25, :593); --digest-budget N (default 12 files, :407); --digest-bytes N (default 2400, :407)", "help_discloses_flags": "PARTIAL -- usage line :586 names only --max-neighbors; --digest-budget/--digest-bytes/--no-packet are documented only in the docstring :25-26 (F3)"},
    "size_invariance": {"work": "CONSTANT caps: 25 neighbors, 12 digests, 2400 B/digest -- does not scale with corpus width", "time": "NOT budgeted: no --budget, env, deadline or alarm; worst case 12 x 60 s = 720 s + 120 s comp-state, against a 120 s outer ceiling the tool cannot see; measured 25-38 s per run on a 2-pin artifact", "rule_P": "disclosure line MET; page flags non-application", "rule_T": "NOT MET -- same standing as T-1/T-2 (owed; a project-wide unit, not this tool's blocker)"}
  },

  "passcraft": {
    "recon": "comp-passcraft recon comp-adversary -- rc 0, 1 s, 56 lines; MOVES 1-3 OBSERVED by the helper, 4-8 SLOT hand-run below",
    "moves_1_to_8": [
      {"move": 1, "status": "DONE", "falsifier_answer": "wrapper IS the backend (self-contained, 626 lines); the read is of the tool, not a shim"},
      {"move": 2, "status": "DONE", "falsifier_answer": "write surface = the --out path only (file-write); stdout otherwise; consumers of --out files: none enumerated in .tools/ or hooks (D9 class: n/a for a stdout composer)"},
      {"move": 3, "status": "DONE", "falsifier_answer": "no cache; oracle = git at HEAD (read-vintage printed) + comp-read per digest; no frozen fixture used as the measure"},
      {"move": 4, "status": "DONE", "falsifier_answer": "target universe FROM SOURCE: COMMIT_RE/PATH_RE/TOOL_RE/FILELINE_RE at :80-90 over the artifact bytes; the tool prints its own denominator ('pins found: 2 commits, 2 repo paths, 0 file:line cites, 4 tool mentions') and the parser's miss count ('1 hex run(s) not parsed')"},
      {"move": 5, "status": "DONE", "falsifier_answer": "five branch targets (absent / zero-pin / capped / directory / ceiling), each membership verified FROM THE OUTPUT differing (rc + text), not by name"},
      {"move": 6, "status": "DONE", "falsifier_answer": "mutations only in copies beside the tool; production sha checked before and after each; probe artifacts removed and their absence printed"},
      {"move": 7, "status": "DONE", "falsifier_answer": "ground truth from non-sharing instruments: `ls` for the absent path; a probe file with zero hex runs by construction; Python's exception class for the ceiling and the crash"},
      {"move": 8, "status": "DONE", "falsifier_answer": "archetype hand-classified (recon: UNCLASSIFIED); lead probes hunted: guard-asymmetry, terminal-honest/artifact-lies, correct-but-unwired, skip-on-missing-field, success-token-bound-to-wrong-step"}
    ],
    "archetype": "evidence-pack COMPOSER: no verdict, rc bound to COMPOSITION (rc 0 on a zero-pin artifact and on a fully-deferred packet) -- correct for its contract, and the reason a consumer must read the body, never the rc",
    "findings": [
      {"id": "F1", "shape": "guard-asymmetry",             "cite": ".tools/comp-adversary:94 @4c3b848c97",        "text": "a directory subject raises through open() unhandled; the tool never says NOT_APPLICABLE in its own voice"},
      {"id": "F2", "shape": "terminal-honest/artifact-lies", "cite": ".tools/comp-adversary:349-368 @4c3b848c97",   "text": "the packet roll-up carries no deferred bucket; 12 timed-out digests leave 'selected: 12 of 18' unchanged"},
      {"id": "F3", "shape": "terminal-honest/artifact-lies", "cite": ".tools/comp-adversary:586 vs :25-26 @4c3b848c97", "text": "the usage line names one flag of four the docstring documents"},
      {"id": "F4", "shape": "correct-but-unwired",           "cite": ".tools/to-pipeline-gate.py:54 @HEAD",           "text": "PROBED, NOT A DEFECT: the mandate is enforced as a DECLARATION gate (PREFLIGHT_TOOLS names it; a TO must declare it RUN or DECLARED-NOT-APPLICABLE); the gate never invokes the tool; hook-driven runs are 0"},
      {"id": "F5", "shape": "correct-but-unwired",           "cite": "org/modules/graph/graph-call-manifest.yaml:33; org/modules/graph/comp-tools.yaml (0/905)", "text": "registered nowhere a router reads: excluded from the graph manifest by list, absent from the comp-which catalog"},
      {"id": "F6", "shape": "vacuous-that-can-block",        "cite": ".tools/tests/ (8 of 22 files) @HEAD",           "text": "the TOOL_BATTERIES lane sweep collects 0 of 37 collectable tests: pytest aborts the session on the first module-scope SystemExit; found at the 4.6 battery field; surfaced 92794"}
    ]
  },

  "usage": {
    "runs_30d": {
      "runs_jsonl": {"count": 12, "note": "ALL after 2026-09-02T17:42Z (unit 3a gave the tool its first self-report; 0 rows before, all-time); by serial: 0.8.0_AE_CloudComp 11 (self-test, 3a controls, 7 probes of this pass), 3.0.0_SA_CVO 1 -- a 4-hour window, not 30 days"},
      "rail_log":   {"count": 0, "note": "no row kind records a comp-adversary INVOCATION; the 12 rows matching the name are comp-read / comp-which rows ABOUT it (term=.tools/comp-adversary, intent=comp-adversary+...)"}
    },
    "hook_driven": {"fraction": "0 of 12", "basis": "the sink carries no origin field (keys: args_head, rc, result, route_*, serial, session_id, to_id, tool, ts_epoch, verdict_basis); to_id is '(no-TO)' on all 12; the only gate naming the tool (to-pipeline-gate.py:54) checks a TO's declaration and never runs it"},
    "battery": {
      "files": [
        {"path": ".tools/tests/test_comp_adversary_stage4_packet.py", "collects_under_pytest": "1 test in 0.09 s (03cf4d17ac)", "red_first_mutant": true, "mutant_form": "COMP_ADVERSARY_TOOL -> a copy with _comp_read_digest returning empty; DIGEST-CONTENT arm reddens"},
        {"path": ".tools/tests/test_comp_adversary_path_truncation.py", "collects_under_pytest": "ABORTS collection -- sys.exit at :120 at module scope, subprocess at :34 at import (b9cab628ce, 2026-08-19, this seat); runs direct only", "red_first_mutant": "n/a (not collectable)"}
      ],
      "lane_sweep": "pytest --collect-only .tools/tests/ -> rc 3, INTERNALERROR SystemExit, 0 collected (control: still 0 with the August file ignored); per-file census 22: abort 8 / collect >0 6 (37 tests) / collect 0 clean 8 -- F6"
    },
    "overlap": "NONE by purpose: the 11 manifest rows matching validator|validation_context|adversar|declaration name no second validator-context tool (rows are comp-manifest-check, comp-atomcheck, and notes on 'declaration' in other tools); stage 4 CONSUMES comp-read (:271-290) and comp-state (:294-300) -- consumption through subprocess, not a second digest engine (the docstring says so at :272-273 and the body agrees)",
    "proposed": "CLEARED-candidate, conditional on ONE unit: F1 (a directory/non-file subject refused in the tool's voice, ~3 lines at :93, distinguishable from 'artifact not found'). F2 and F3 ride the same commit. F4 is not a defect. F5 is a registration act for the manifest owner. F6 is the lane's, surfaced 92794, owner this seat. Rule T is carried project-wide."
  }
}
```

## The four planted cases, quoted

**SUBJECT_ABSENT_FROM_CORPUS** -- `compose ./ZZZS4_NOSUCH_0902.md`, rc 2, one line:
```
ERROR: artifact not found: ./ZZZS4_NOSUCH_0902.md
```

**PRESENT_WITH_ZERO_RESULTS** -- a three-line probe file with no pin of any kind, rc 0, 64 lines. The
relevant region:
```
artifact: ZZZS4_ZEROPIN_0902.md
artifact-vintage: UNCOMMITTED (n/a)
## AUTHOR PROFILE (what the author's evidence context WAS)
pins found: 0 commits, 0 repo paths, 0 file:line cites, 0 tool mentions
!! ZERO MACHINE-EXTRACTABLE PINS: this artifact's evidence is prose-cited or
!! externally homed -- the validator must derive the evidence set BY READING.
!! Every complement source below ran against an EMPTY profile and says so in
!! its own denominator. A zero here is a signal, never a clean pass.
### source 1: cited-commit verification (0 attempted / 0 verified / 0 UNVERIFIABLE)
### source 3: uncited neighborhood (directory siblings of cited paths)
  total uncited siblings: 0 (showing 0 -- the CAP is declared, not silent)
```

**PARTIAL_OR_BLIND** -- the CVO finding with `--max-neighbors 1 --no-packet`, rc 0, 59 lines:
```
  total uncited siblings: 18 (showing 1 -- the CAP is declared, not silent)
  - org/modules/graph/debtscan/2026-06-12_D1_reachability_candidates.md
### source 5: comp-read digests of the complement (THE PACKET -- stage 4)
  SKIP: --no-packet given. Stage 4 was DISABLED BY THE CALLER for this run;
  the complement above is POINTERS ONLY. This is a caller's choice, recorded
```

**NOT_APPLICABLE** -- `compose org/tier2_senior/0.8.0_AE_CloudComp/deliverables` (a directory), rc 1:
```
  File ".tools/comp-adversary", line 94, in parse_artifact
    text = open(path, encoding="utf-8", errors="replace").read()
PermissionError: [Errno 13] Permission denied: 'org/tier2_senior/0.8.0_AE_CloudComp/deliverables'
```
The four outputs are distinguishable by rc and by text, so 4.3 PASSES as written. The fourth is a
Python traceback: rc 1 is machine-rejectable, but the vocabulary is the interpreter's, and the exception
class differs by platform (`IsADirectoryError` on POSIX). A JSON artifact, offered as a second N/A probe,
composed as prose with 0 pins -- the tool has no NOT_APPLICABLE word of its own. That is F1.

## The ceiling, exercised

`_comp_read_digest` (:271-290) wraps each stage-4 digest in `timeout=60`. A copy beside the tool with
that constant at 1 s ran identically to production (every digest returns in under a second; 611 lines
both). At 0.01 s every digest hit the ceiling and the tool printed, once per digest:
```
  --- digest 1/12: org/modules/graph/debtscan/2026-06-12_D1_reachability_candidates.md [class S3]
      DEFERRED: comp-read unavailable: TimeoutExpired
```
twelve times, rc 0, 109 lines. The lines ABOVE the digests were byte-identical to the healthy run:
`selected: 12 of 18 uncited siblings` and `NOT DIGESTED: 6 of 18 siblings -- 6 beyond the budget, 0
non-text`. A reader of the roll-up would count 12 digests delivered; the body delivered none. The
deferral is honest per line and silent in the denominator -- F2. The second constant, `timeout=120` at
:297 around `comp-state --json`, equals the harness's default outer ceiling: at that ceiling the harness
kills the composer at the same moment the composer would defer the source.

## Findings, and the one unit they need

- **F1** (`:94`, guard-asymmetry): refuse a non-file subject in the tool's voice, e.g. `ERROR: not an
  artifact (directory): <path>` rc 2, distinguishable from `artifact not found`. ~3 lines before the
  `open()`. This is the only finding that stands between comp-adversary and CLEARED.
- **F2** (`:349-368`, terminal-honest/artifact-lies): add a `deferred: N of M` bucket to the packet
  roll-up so a timed-out packet is visible above the fold. Rides the F1 commit.
- **F3** (`:586` vs `:25-26`): the usage line prints one flag; the docstring documents four. Rides F1.
- **F4** (to-pipeline-gate.py:54): NOT a defect. The Andrew-direct mandate ("a MANDATORY element of the
  atom_decomp VALIDATION piece") is enforced as a declaration requirement on the TO, never by invoking
  the tool; hook-driven runs are therefore 0 of 12, by design.
- **F5** (manifest :33; comp-tools.yaml absent): the tool is excluded from the graph manifest by list
  and absent from the comp-which catalog. A validator asking comp-which "what shows me what the author
  did not see" cannot be routed here. Registration is the manifest owner's act, not this row's.
- **F6** (`.tools/tests/`, 8 of 22): surfaced 92794 as ARMED, owner this seat. Census below.

## The lane sweep census (F6), 2026-09-02 22:3xZ, denominator 22

| file | collect | last author |
|---|---|---|
| test_atomcheck.py | ABORT SystemExit | 0.8.0_AE_CloudComp |
| test_comp_adversary_path_truncation.py | ABORT SystemExit | 0.8.0_AE_CloudComp |
| test_comp_read_enumerate.py | ABORT SystemExit | 3.0.0_SA_CVO~C |
| test_deploy_ledger_held.py | ABORT SystemExit | 0.8.0_AE_CloudComp |
| test_fabric_check_classify.py | ABORT SystemExit | 1.0.0_SA_CTO |
| test_proof_of_spec_content_rung.py | ABORT SystemExit | 1.0.0_SA_CTO~X |
| test_proof_of_spec_decomp_ref_content.py | ABORT SystemExit | 1.0.0_SA_CTO~X |
| test_safe_deploy_receipt_names_both_legs.py | ABORT SystemExit | 0.8.0_AE_CloudComp |
| test_comp_adversary_stage4_packet.py | collects 1 | 0.8.0_AE_CloudComp |
| test_comp_find_battery.py | collects 1 | 0.8.0_AE_CloudComp |
| test_deploy_ledger_malformed.py | collects 18 | 0.8.0_AE_CloudComp |
| test_proof_of_spec_artifact_resolution.py | collects 5 | 1.0.0_SA_CTO~X |
| test_proof_of_spec_cell_id_re.py | collects 5 | 1.0.0_SA_CTO~X |
| test_substrate_card_check.py | collects 7 | 1.0.0_SA_CTO~X |
| test_audit_archive_invoker.py | collects 0 (rc 5) | 0.7.0_AE_CloudOps~ |
| test_commit_gate_oversize.py | collects 0 (rc 2) | 0.5.0_AE_OpalETL |
| test_comp_schedule.py | collects 0 (rc 124, TIMED OUT at 60 s) | 3.0.0_SA_CVO~C |
| test_etfs_parity_contract.py | collects 0 (rc 5) | 0.5.0_AE_OpalETL |
| test_project_registry.py | collects 0 (rc 5) | 2.0.0_SA_COO |
| test_proof_of_spec_alignment.py | collects 0 (rc 5) | 1.0.0_SA_CTO~X |
| test_seating_lint.py | collects 0 (rc 5) | 0.8.0_AE_CloudComp |
| test_to_decomp_ref_lint.py | collects 0 (rc 5) | 0.8.0_AE_CloudComp |

Any one of the eight aborters ends the session; the six collectable files hold 37 tests the directory
run never sees. Four of the eight are this seat's. `test_comp_schedule.py` is a ninth problem of a
different shape: it collects nothing and takes over 60 s to say so (module-scope work at import, the
T-16 pass-1 shape). The remedy per file is the T-16 pass-2 shape; the minimum that revives the sweep is
a `__main__` guard on the eight.

## Captures

Every run's full stdout/stderr is in this session's scratchpad (`s4_B_default.txt`, `s4_C1..C4b.txt`,
`s4_ceiling.txt`, `s4_ceiling2.txt`, `s4_passcraft.txt`); the numbers above are read from those files.
Probe artifacts and mutant copies were removed and their removal printed; `.tools/comp-adversary` sha
`824edcb54b12b933` before and after every mutant run; `git status` clean of everything but this file.
