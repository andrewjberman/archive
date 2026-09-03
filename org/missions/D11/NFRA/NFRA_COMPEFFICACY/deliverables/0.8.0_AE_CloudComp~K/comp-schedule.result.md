# comp-schedule -- NFRA_COMPEFFICACY T-5 result (PRD s.4)

Schema: `NFRA_COMPEFFICACY_PRD` v0.7 @`8170ddb0fe`, s.4. Row: T-5. Cell:
CE-t-5 (decomp v0.2.7 @`9c4a688102`). Measured by
`0.8.0_AE_CloudComp~K` on 2026-09-03 after GO Msg-ID 93872. The implementation
is local commit `86b4ecc2656c3bb0319e777b230c82f9b68802fe`; it has not been pushed.
No spec-vs-world surprise was found by this audit.

The JSON object below contains the required 31 s.4 fields: identity 7,
disclosure 8, answer-state 4, bounds 4, passcraft 3, and usage 5.

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.7 s.4 @8170ddb0fe",
  "row": "T-5",
  "cell": "CE-t-5",
  "measured_by": "0.8.0_AE_CloudComp~K",
  "measured_at_utc": "2026-09-03T19:06Z",
  "read_vintage": "working view after 86b4ecc2656c3bb0319e777b230c82f9b68802fe",
  "surprises": [],
  "identity": {
    "tool": "comp-schedule",
    "shim_path": ".tools/comp-schedule (self-contained executable; no separate shim)",
    "engine_path": ".tools/comp-schedule",
    "engine_vintage": "before blob 5668643c20a845047410af55fa84639ea8458db5; after blob f59d64bb57647fea0a95e3ad518fc11012692fa2 at commit 86b4ecc265",
    "aliases": [],
    "purpose_1line": "Read-time compiler for the gate ledger: what remains armed, who owns it, and whether its carrier bytes can settle armedness.",
    "self_identifies": "PASS -- default output begins 'comp-schedule -- the gate ledger (VIEW-TIME COMPILED; no artifact, nothing to go stale)' and --help names the tool and contract."
  },
  "disclosure": {
    "subject": "PRESENT -- the default run says 'the gate ledger' and reports each live gate with owner, discharge text, last-verified proxy, and evidence path.",
    "corpus_or_backend": "PRESENT -- five repo-local carrier factories in _CARRIER_FACTORIES: C1 sentinel, C2 deploy-ledger, C3 moratoria, C4 scope-guard, C5 project-blocking; no AWS, network, model, cache, or stored output.",
    "vintage": "PRESENT -- this result pins the engine blob/commit and UTC read window; individual rows expose evidence paths and last-edit dates, explicitly labelled weak proxies rather than human verification.",
    "denominator": "PRESENT -- complete run: C1=21, C2=4, C3=12, C4=20, C5=337; 21 gates armed; C5 additionally states 354 project JSON files, 337 with blocking, and 138 non-null prose fields.",
    "resolved_unresolved": "PRESENT -- C1/C2/C3 are DECIDABLE and countable; C4 is SEMI-DECIDABLE and C5 NOT-DECIDABLE, so both print PARTIAL_OR_BLIND tool-voice=NOT-DECIDABLE and are listed rather than counted.",
    "blind_spots": "PRESENT -- C4 cannot settle whether scope guards remain armed from their own bytes; C5 is free prose with negation/closure language; last-edit dates are weak proxies; ARNs are absent BY DESIGN because no AWS-resource identity spans all five carrier types.",
    "pagination": "PRESENT -- no page flags apply to a complete ledger view. C5 prints 8 of 138 prose rows and then '... 130 more. A PAGE IS NOT AN ANSWER -- the denominator above is the claim.'",
    "timeout": "PRESENT -- Rule T uses a shared wall-clock budget; default 90 seconds, --budget overrides COMP_BUDGET_S, and --budget 0 is unbounded. Expiry prints a prefix warning, reached denominators, cursor, and returns non-clean rc 3."
  },
  "answer_state": {
    "SUBJECT_ABSENT_FROM_CORPUS": {"planted": "carrier/project subject has no ledger in the corpus", "printed": "case=SUBJECT_ABSENT_FROM_CORPUS case-rc=2 ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS denominator=0", "rc": 2},
    "PRESENT_WITH_ZERO_RESULTS": {"planted": "carrier is present and compiles to zero gates", "printed": "case=PRESENT_WITH_ZERO_RESULTS case-rc=0 ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS denominator=1", "rc": 0},
    "PARTIAL_OR_BLIND": {"planted": "free-prose carrier cannot decide armedness", "printed": "case=PARTIAL_OR_BLIND case-rc=3 ANSWER-STATE: PARTIAL_OR_BLIND tool-voice=NOT-DECIDABLE denominator=7", "rc": 3, "carrier_voice": "C4 and C5 use the adopted NOT-DECIDABLE spelling and always state their reached denominator"},
    "NOT_APPLICABLE": {"planted": "selected mode has no population", "printed": "case=NOT_APPLICABLE case-rc=0 ANSWER-STATE: NOT_APPLICABLE denominator=0", "rc": 0}
  },
  "bounds": {
    "subprocess_timeouts": "ABSENT -- comp-schedule launches no subprocess. Rule T wraps its own five deterministic carrier loops through .tools/_compbudget.py rather than a per-child timeout.",
    "ceiling_behaviour": "EXERCISED -- --budget 0.001 returned rc 3, 'BUDGET REACHED', scanned 0 of 5, resume cursor START, PARTIAL_OR_BLIND / NOT-DECIDABLE, and C1=0 partial plus C2-C5 NOT-SCANNED. A prefix is never the clean answer.",
    "page_contract": "No --page/--limit/--all contract applies. Output truncation is disclosure-only: C5 shows a bounded reading-list sample while retaining and printing the true denominator; 'A PAGE IS NOT AN ANSWER'.",
    "size_invariance": "Work scales with the five live carrier populations and is therefore not size-invariant; Rule T is the bound. comp-schedule is verdict-bearing at the complete five-carrier compile boundary because its rc vocabulary now distinguishes complete rc 0 from partial rc 3. Consumer census found no runtime reader: to-pipeline-gate.py parses only textual preflight dispositions and never invokes comp-schedule or reads its rc."
  },
  "passcraft": {
    "moves_1_to_8": [
      {"move": 1, "status": "DONE", "falsifier_answer": "The executable is the 827-line self-contained engine; no forwarding shim/backend split exists."},
      {"move": 2, "status": "DONE", "falsifier_answer": "Write surface is none: stdout-only, read-only, and no cache/artifact/marker write."},
      {"move": 3, "status": "DONE", "falsifier_answer": "Oracle is current repository bytes plus git metadata; no frozen fixture or cache decides the production result."},
      {"move": 4, "status": "DONE", "falsifier_answer": "Target universe comes from source: the exact five factories C1..C5 and each carrier's native denominator, all printed."},
      {"move": 5, "status": "DONE", "falsifier_answer": "Four in-memory fixtures prove branch membership from distinct rc/text/state output in one invocation."},
      {"move": 6, "status": "DONE", "falsifier_answer": "Mutants run only against temporary copied source; production hashes remained fixed and temporary copies were removed."},
      {"move": 7, "status": "DONE", "falsifier_answer": "Independent census matched C2 filesystem membership, C4 scope-guard file count, and C5 JSON/blocking/prose counts; uppercase NEVER deliberately defines C3."},
      {"move": 8, "status": "DONE", "falsifier_answer": "Read-only view-time ledger compiler; probes targeted success-token-bound-to-wrong-step, terminal-honest/artifact-lies, correct-but-unwired, and resource-blind shapes."}
    ],
    "archetype": "Read-only view-time LEDGER COMPILER: it compiles five unlike carriers into one gate board, refuses to count prose as settled fact, and never closes a gate.",
    "findings": [
      {"id": "F1", "shape": "resource-blind (intentional/non-defect)", "owner": "1.0.0_SA_CTO", "grade": "RECORDED, NOT FIXED", "text": "ARNs absent BY DESIGN. Sentinel regexes, repo ledgers, standing law, scope guards, and free prose share no AWS-resource identifier; inventing one would conflate gate armedness with cloud resource identity."},
      {"id": "F2", "shape": "correct-but-unwired", "owner": "3.0.0_SA_CVO", "grade": "RECORDED, OUT OF BOUNDS", "text": "to-pipeline-gate requires a textual comp-schedule RUN disposition but does not invoke the tool or consume its rc. The implementation nevertheless makes the tool's own partial result non-clean."},
      {"id": "F3", "shape": "spec-vs-spec", "owner": "1.0.0_SA_CTO", "grade": "RECORDED, NO SURPRISE ROW", "text": "Current PRD s.4.4 retains a Rule-T non-application phrase while this later, tool-specific T5-AC4 requires Rule T. The exact task-order acceptance controls this implementation; the PRD text should be reconciled on its next version."}
    ]
  },
  "usage": {
    "runs_30d": "0 invocation rows in org/mcp/comp-tool-runs.jsonl; 0 direct invocation rows in org/mcp/comp-which-rail.log (12 textual mentions there are queries about the name, not comp-schedule runs).",
    "hook_driven": "0 of 25 observed explicit task-order preflight declarations are proven hook-driven. The two telemetry sinks contain zero invocations and no origin evidence; preflights are issuer/author declarations, not gate execution.",
    "battery": "New .tools/tests/test_comp_schedule_battery.py: 18/18 PASS direct and 1 passed under pytest file grain; historical .tools/tests/test_comp_schedule.py: 9/9 PASS direct; commit-gate clean 1/1 on the new Python battery. Directory collect aborts on pre-existing test_fabric_check_classify.py module-scope sys.exit after enumerating both comp-schedule files.",
    "overlap": "comp-schedule overlaps no decision engine: it reads five gate-record carriers and reports their own decidability. to-pipeline-gate validates only the existence/shape of preflight declarations. graph-call-manifest excludes comp-schedule as a records query pending the CTO curated-vocabulary batch.",
    "proposed": "CLEARED-candidate -- implementation and local evidence pass T5-AC1..AC5; final clearance remains the independent FWD-9 observation plus proof-of-spec validation and complete flip."
  }
}
```

## Default live run -- quoted

Invocation: `python .tools/comp-schedule`; rc 0.

```text
comp-schedule -- the gate ledger (VIEW-TIME COMPILED; no artifact, nothing to go stale)
budget: 90 s (default)
WITHIN BUDGET: scanned 5 of 5 carriers; budget: 90 s (default), used 19.812 s
REACHED-DENOMINATORS: C1=21; C2=4; C3=12; C4=20; C5=337

GATES ARMED: 21
NEEDS-READ:  138 project `blocking` field(s) carrying non-null PROSE -- NOT counted as
             gates. This tool does not read prose; these are a reading list.

C1  SENTINEL         DECIDABLE       denominator=21 -> 5 gate(s) answer-state=POSITIVE_RESULT [outside the s.4.3 non-positive domain]
C2  DEPLOY-LEDGER    DECIDABLE       denominator=4 -> 4 gate(s) answer-state=POSITIVE_RESULT [outside the s.4.3 non-positive domain]
C3  MORATORIA        DECIDABLE       denominator=12 -> 12 gate(s) answer-state=POSITIVE_RESULT [outside the s.4.3 non-positive domain]
C4  SCOPE-GUARD      SEMI-DECIDABLE  denominator=20 -> 0 gate(s) answer-state=PARTIAL_OR_BLIND tool-voice=NOT-DECIDABLE
C5  PROJECT-BLOCKING NOT-DECIDABLE   denominator=337 -> 0 gate(s) answer-state=PARTIAL_OR_BLIND tool-voice=NOT-DECIDABLE
    354 project json(s), 337 carry a `blocking` key: 9 empty, 190 prose-'None', 138 NON-NULL PROSE (of those: 16 SELF-NEGATE, 66 use closed/resolved language). 0 unparseable. NOT COUNTED AS GATES -- this is a READING LIST.

... 130 more. A PAGE IS NOT AN ANSWER -- the denominator above is the claim.
```

The default carrier denominators are a point-in-time read of a shared working
tree. C2 changed from 5 to 4 between two clean runs as another lane closed a
deploy-ledger entry; that is correct behavior for a view-time compiler, not
nondeterminism for the same input.

## Four planted states -- one invocation, quoted

Invocation: `python .tools/comp-schedule --answer-state-cases`; outer rc 0.
`case-rc` is the branch result being planted. The grain is the **STATE TOKEN
within one invocation**.

```text
ANSWER-STATE CASES -- PLANTED in ONE invocation (case-rc is the branch rc):
  case=SUBJECT_ABSENT_FROM_CORPUS case-rc=2 ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS denominator=0 -- carrier/project subject has no ledger in the corpus
  case=PRESENT_WITH_ZERO_RESULTS case-rc=0 ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS denominator=1 -- carrier is present and compiles to 0 gate(s) across denominator=1
  case=PARTIAL_OR_BLIND case-rc=3 ANSWER-STATE: PARTIAL_OR_BLIND tool-voice=NOT-DECIDABLE denominator=7 -- free-prose carrier cannot decide gate armedness across denominator=7
  case=NOT_APPLICABLE case-rc=0 ANSWER-STATE: NOT_APPLICABLE denominator=0 -- selected mode has no population
answer-state cases: PASS 4/4 distinct state tokens
```

## Rule T -- complete and cut, quoted

`--help` discloses `--budget`, `COMP_BUDGET_S`, default 90 seconds, unbounded
`--budget 0`, deterministic cursor `START|C1..C5`, and rc 0/1/2/3. The shared
carrier is `.tools/_compbudget.py`; it was consumed, not edited.

Invocation: `python .tools/comp-schedule --budget 0.001`; rc 3.

```text
budget: 0.001 s (flag)
BUDGET REACHED: 0.001 s (flag); scanned 0 of 5 carriers; results are a PREFIX, not the answer; resume: comp-schedule --cursor START
ANSWER-STATE: PARTIAL_OR_BLIND tool-voice=NOT-DECIDABLE -- the carrier view is a PREFIX, never clean
REACHED-DENOMINATORS: C1=0 (PARTIAL; scanned 0 of UNKNOWN files); C2=NOT-SCANNED; C3=NOT-SCANNED; C4=NOT-SCANNED; C5=NOT-SCANNED
```

The default run above is the paired clean completion. Budget checks occur
inside carrier enumeration, so the ceiling bounds a large carrier rather than
only checking between carriers. A partial prefix returns rc 3, never rc 0.

## Consumer census and usage

- `.tools/to-pipeline-gate.py:307-334` validates text inside `<preflight>`;
  it neither invokes comp-schedule nor consumes its rc.
- `org/mcp/comp-tool-runs.jsonl`: 0 rows whose tool is comp-schedule.
- `org/mcp/comp-which-rail.log`: 0 direct invocation rows; 12 name mentions.
- Task-order corpus: 25 explicit `comp-schedule: RUN -- ...` declarations.
- No hook invocation was found. The instrument cannot derive a hook-origin
  fraction beyond observed 0/25 because no invocation rows carry origin.

The code therefore applies the verdict-bearing row at the tool boundary:
complete view rc 0; usage/repository error rc 2; budget-prefix
PARTIAL_OR_BLIND / NOT-DECIDABLE rc 3. The current L6 preflight remains a
declaration consumer and is F2, outside this cell's write bounds.

## Battery and controls

```text
python .tools/tests/test_comp_schedule_battery.py
18/18 PASS

python -m pytest -q .tools/tests/test_comp_schedule_battery.py
1 passed in 24.36s

python .tools/tests/test_comp_schedule.py
9/9 PASS

bash .tools/commit-gate.sh .tools/tests/test_comp_schedule_battery.py
COMMIT GATE: CLEAN (1 of 1 Python files)
```

The new battery has a RED mutant for each new behavior and rejects missing or
wrong state tokens, C4/C5 tool voice, clean expiry rc, missing expiry/denominator
text, carrier-loop budget blindness, and incomplete help disclosure. Directory
collection is not a substitute for the required file grain: `pytest
--collect-only .tools/tests` aborts on the pre-existing module-scope
`sys.exit(0)` in `test_fabric_check_classify.py:76`, after both comp-schedule
files are enumerated. This audit did not alter that unrelated file.

## Graded finding -- no remediation

**ARNs absent BY DESIGN** -- owner for any future disclosure/schema change:
`1.0.0_SA_CTO`. The five carriers do not share AWS resource identity. Adding
an ARN field would invent values for standing law, task-order scope prose, and
sentinel strings, conflating two different axes. Per T5-AC3, this is recorded
and not fixed. The diff is limited to `.tools/comp-schedule` and the new
`.tools/tests/test_comp_schedule_battery.py`; `_compbudget.py` is unchanged.

## Push state and FWD-9

- Production before: blob `5668643c20a845047410af55fa84639ea8458db5`.
- Production after: blob `f59d64bb57647fea0a95e3ad518fc11012692fa2`.
- Battery: blob `715e24ce8fe721034f50f2ec7ff6f271b7254d3d`.
- Local implementation commit: `86b4ecc2656c3bb0319e777b230c82f9b68802fe`.
- `origin/CLOUD`: `351f309e0a6ded1a5a5bdf3aacec18a5f9f8dbee`;
  `git merge-base --is-ancestor 86b4ecc265 origin/CLOUD` returned rc 1.
- Push state: **LOCAL, MEASURED; no push performed**.
- FWD-9 command sent to `2.0.0_SA_COO`: `python .tools/comp-schedule --budget 0`;
  independent output receipt pending at this report-write point.

