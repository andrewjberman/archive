# comp-denytest -- NFRA_COMPEFFICACY per-tool result

Schema: `NFRA_COMPEFFICACY_PRD.md` v0.5 @`5bbdab5ec7`, section 4. Row `T-11`, cell
`CE-t-11`. Measured by `0.8.0_AE_CloudComp~E` on 2026-09-03. Every required
section 4 field is present below. `ABSENT` and `N/A` are reported values, not
omissions. The engine is the audit object; the 12-line shell file is only its shim.

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.5 @5bbdab5ec7 s.4",
  "row": "T-11",
  "cell": "CE-t-11",
  "measured_by": "0.8.0_AE_CloudComp~E",
  "measured_at_utc": "2026-09-03T14:39Z..15:45Z",
  "read_vintage": "production fix f8f9e8809f732a95cf16b3921c508414be52290e; pre-fix engine vintage 5af83b9041595b63462a412ca858d6ca6cbf1dc5; task-order audit cut 6e5d443ad3",
  "surprises": [],
  "identity": {
    "tool": "comp-denytest",
    "shim_path": ".tools/comp-denytest (12 lines)",
    "engine_path": ".tools/comp-denytest.py (673 lines) -- resolved directly from the shim body",
    "engine_vintage": "f8f9e8809f732a95cf16b3921c508414be52290e (2026-09-03T15:01:33Z); before: 5af83b9041595b63462a412ca858d6ca6cbf1dc5 (2026-07-09T11:02:21Z)",
    "aliases": [],
    "purpose_1line": "a deny-test harness that DERIVES the expected verdict from the change type [engine docstring line 2]",
    "self_identifies": {
      "grade": "ABSENT",
      "help_prints_entrypoint": true,
      "help_prints_engine_path": false,
      "help_prints_version_or_commit": false,
      "quoted": "usage: comp-denytest [-h] ..."
    }
  },
  "disclosure": {
    "subject": {
      "grade": "PRESENT",
      "quoted": "ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS / PLAN: 1 IAM policy subject(s), but zero deny-add / allow-removal changes"
    },
    "corpus_or_backend": {
      "grade": "PRESENT",
      "quoted": "OFFLINE ANSWER-STATE SELF-TEST ... fixture plans + injected simulate stub; ZERO live IAM calls"
    },
    "vintage": {
      "grade": "ABSENT in tool output",
      "quoted": "the fixture run prints no engine commit or fixture content hash; the audit pins f8f9e8809f externally"
    },
    "denominator": {
      "grade": "PRESENT",
      "quoted": "PLAN: 1 IAM policy subject(s), but zero deny-add / allow-removal changes; WITHIN BUDGET: scanned 0 of 0 simulation_call; DEFERRED: 0 of 0 simulation_call(s) did not return"
    },
    "resolved_unresolved": {
      "grade": "PRESENT",
      "quoted": "WITHIN BUDGET: scanned 0 of 0 simulation_call; DEFERRED: 0 of 0 simulation_call(s) did not return"
    },
    "blind_spots": {
      "grade": "PRESENT",
      "quoted": "zero population without an IAM change is CORRECT; no IAM evaluation is applicable"
    },
    "pagination": {
      "grade": "N/A",
      "quoted": "NON-APPLICATION: this tool has no corpus-width loop or safe partial-verdict cursor; an incomplete explicit tuple is rerun whole"
    },
    "timeout": {
      "grade": "PRESENT after this cell",
      "quoted": "budget: 90 s (default); Rule T carrier: --budget > env COMP_BUDGET_S > default 90 s"
    }
  },
  "answer_state": {
    "SUBJECT_ABSENT_FROM_CORPUS": {
      "planted": "offline fixture plan with no IAM policy resource",
      "printed": "ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS / PLAN: no IAM policy subject exists in the fixture corpus",
      "rc": 0
    },
    "PRESENT_WITH_ZERO_RESULTS": {
      "planted": "offline fixture plan containing one no-op IAM policy subject and no deny-add or allow-removal",
      "printed": "ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS / PLAN: 1 IAM policy subject(s), but zero deny-add / allow-removal changes; zero population without an IAM change is CORRECT",
      "rc": 0
    },
    "PARTIAL_OR_BLIND": {
      "planted": "offline deny-add fixture whose injected simulator returns implicitDeny with MissingContextValues=['aws:SourceVpc']",
      "printed": "DEFERRED: 1 of 1 simulation_call(s) did not return ... conditioned implicitDeny cannot be read as a verdict / ANSWER-STATE: PARTIAL_OR_BLIND / STATE: NOT-DECIDABLE (rc=2, distinct from clean rc=0 and failing rc=1)",
      "rc": 2,
      "outer_self_test_rc": 0,
      "reason": "the outer audit harness returns 0 only after verifying the planted inner rc is 2"
    },
    "NOT_APPLICABLE": {
      "planted": "offline fixture plan changing an IAM policy only by adding an Allow, a change type this deny/allow-removal verifier does not test",
      "printed": "ANSWER-STATE: NOT_APPLICABLE / PLAN: IAM policy subjects changed, but none is a deny-add or allow-removal this tool tests",
      "rc": 0
    }
  },
  "bounds": {
    "subprocess_timeouts": "simulate() line 152 passes timeout=Clock.remaining() to the one-resource-per-call AWS CLI subprocess; resolved carrier precedence is --budget > COMP_BUDGET_S > 90 s, and --budget 0 is unbounded",
    "ceiling_behaviour": "battery arm DENY-AC4-TIMEOUT-CARRIER-AND-RC-CONSUMER plants a subprocess.TimeoutExpired at timeout<=0.25 s and observes BUDGET REACHED, ANSWER-STATE: PARTIAL_OR_BLIND, STATE: NOT-DECIDABLE, rc 2; unreadable non-timeout simulations take the same non-clean rc and never print RESULT: PASS",
    "page_contract": "N/A -- no --page/--limit/--all surface and no corpus-width output loop; help states the non-application and requires rerunning the whole explicit tuple rather than grading a partial verdict",
    "size_invariance": "PRESENT for work ceiling -- every explicit simulation subprocess receives only the remaining declared budget; no internal constant can outlive the caller budget. Cursor mechanics are N/A because there is no deterministic corpus-width scan loop with a safe partial-verdict boundary"
  },
  "passcraft": {
    "moves_1_to_8": [
      {"move": 1, "status": "DONE", "falsifier_answer": "resolved the 12-line shim to .tools/comp-denytest.py; no further delegate exists; _compbudget.py is a consumed library, not the engine"},
      {"move": 2, "status": "DONE", "falsifier_answer": "write surface is only fire-and-forget telemetry through comp_log_auto.py in the shim to org/mcp/comp-tool-runs.jsonl; the engine itself writes only an explicitly requested --precheck baseline file"},
      {"move": 3, "status": "DONE", "falsifier_answer": "no result cache exists; --from-plan reads the supplied JSON on each invocation and live mode shells to AWS per isolated resource call"},
      {"move": 4, "status": "DONE", "falsifier_answer": "the planted plan population is independently explicit in each fixture: 0 IAM subjects, 1 no-op subject, 1 unsupported-change subject, and 1 deny-add subject/1 simulation call"},
      {"move": 5, "status": "DONE", "falsifier_answer": "one real --offline-self-test invocation printed each of the four exact enum tokens once; the false-deny limb additionally printed NOT-DECIDABLE and inner rc 2"},
      {"move": 6, "status": "DONE", "falsifier_answer": "three disposable sibling-engine source mutants ran and were removed: all-state collapse, clean-on-undecidable, and timeout carrier removal; each was detected RED by its paired predicate"},
      {"move": 7, "status": "DONE", "falsifier_answer": "the independent post-commit seat 0.8.0_AE_CloudComp~C ran the real shim at f8f9e8809f and reproduced rc 0, all four tokens and 4/4; it edited no files"},
      {"move": 8, "status": "DONE", "falsifier_answer": "archetype classified below; probes found pre-cell state-collapse, conditioned-grant false-deny and unbounded-subprocess shapes, all closed by f8f9e8809f; no spec-vs-world divergence remained"}
    ],
    "archetype": "VERDICT-BEARING, plan-derived security-change verifier: the plan fixes the success criterion, one isolated simulator call supplies the observed decision, and rc 0/1/2 means clean/fail/not-decidable rather than execution success alone",
    "findings": [
      {"id": "F1", "shape": "correct-zero-vs-absent collapse", "cite": ".tools/comp-denytest.py derive_from_plan() @f8f9e8809f", "text": "before the cell, plans with no testable change collapsed into a generic error; the engine now separates no subject, present zero, and unsupported change with exact tokens"},
      {"id": "F2", "shape": "conditioned-grant false deny", "cite": ".tools/comp-denytest.py simulate()/main() @f8f9e8809f", "text": "MissingContextValues can make implicitDeny byte-identical to a real allow-removal result; it is now deferred as PARTIAL_OR_BLIND / NOT-DECIDABLE rc 2, never a verdict"},
      {"id": "F3", "shape": "unbounded verdict subprocess", "cite": ".tools/comp-denytest.py:131-152,392-521 @f8f9e8809f", "text": "before the cell the AWS CLI subprocess had no timeout or caller-visible budget; the shared Rule T carrier now bounds it and converts expiry/unreadability into rc 2"},
      {"id": "F4", "shape": "low-use retirement candidate", "cite": "TO issue census @6e5d443ad3; org/mcp/comp-tool-runs.jsonl and org/mcp/comp-which-rail.log remeasured 2026-09-03", "text": "the issuer-pinned baseline is 8 runs ever and 2/30d, low enough to surface RETIRE-candidate to Andrew. The candidate is surfaced only: no shim, registration, carrier or history was removed or disabled"}
    ]
  },
  "usage": {
    "runs_30d": {
      "issuer_pinned_baseline": "2 in 30 days, 8 ever at task-order issue; denominator 8 exact comp-denytest executions",
      "runs_jsonl_remeasurement": "6 in rolling 30 days, 12 ever among 28,480 non-empty JSONL rows at the first post-fix measurement; 17 occurrence-bearing rows parsed then, of which 12 had tool exactly comp-denytest and 5 merely mentioned the name in another tool's args. The delta includes audit/help/self-test activity after the issuer cut, including this cell's own real shim run",
      "rail_log_remeasurement": "0 exact execution-shaped rows in 50,020 physical rail-log lines at the structured measurement (49,940 non-empty at a later rg count); 1,193 name occurrences were routes/searches, not comp-denytest executions. The rail is therefore a zero-run corroborating instrument, not added to the JSONL count"
    },
    "hook_driven": "0 of 12 exact JSONL execution rows is identified by the sink as hook-driven; the sink has no hook boolean, so this is a conservative 0/12 classified, 12/12 unproven/manual-compatible rather than a claim that hook invocation is impossible",
    "battery": {
      "path": ".tools/tests/test_comp_denytest_battery.py (294 lines, new at f8f9e8809f)",
      "file_grain": "direct: 9/9 PASS; pytest -q file: 1 passed in 1.42 s; commit-gate clean 2/2 touched Python files",
      "directory_grain": "python -m pytest -q .tools/tests -> rc 1 during collection, no tests ran; pre-existing .tools/tests/test_fabric_check_classify.py:76 calls sys.exit(0) at module import after its own 14/14 classifier checks. The new battery is FILE-grain green, but the lane directory is not green",
      "red_first_mutants": ["all four state printers collapsed to PARTIAL_OR_BLIND", "NOT-DECIDABLE branch returned clean rc 0", "subprocess timeout carrier replaced with None"],
      "zero_live_iam_call_census": "0 AWS processes and 0 live IAM evaluations in the audit/battery. Offline states use fixture plans and injected functions; the timeout arm replaces subprocess.run with a local function that records timeout and raises TimeoutExpired; real subprocesses launched by the battery are only local Python engine/help/mutant processes"
    },
    "overlap": "comp-iam simulate overlaps on the raw simulate-principal-policy decision, but comp-denytest remains a separate executable-body contract: it derives the expected verdict from a Terraform plan, isolates resource ARNs, enforces precheck/discriminator/also-allowed controls, and refuses conditioned ambiguity",
    "proposed": "RETIRE-candidate, surfaced to Andrew through the L4 owner's grade because the fixed audit baseline is only 8 executions ever; NOT ACTED. No retirement mutation appears in f8f9e8809f"
  },
  "fwd9_post_commit": {
    "seat": "0.8.0_AE_CloudComp~C",
    "command": "bash -lc '.tools/comp-denytest --offline-self-test'",
    "observed_commit": "f8f9e8809f732a95cf16b3921c508414be52290e",
    "rc": 0,
    "tokens": ["SUBJECT_ABSENT_FROM_CORPUS", "PRESENT_WITH_ZERO_RESULTS", "NOT_APPLICABLE", "PARTIAL_OR_BLIND"],
    "summary": "OFFLINE ANSWER-STATE SELF-TEST: 4/4 PASS; ZERO live IAM calls",
    "edits": "none"
  },
  "push_state": {
    "measured_at_utc": "2026-09-03T15:03:35Z",
    "origin_cloud": "351f309e0a6ded1a5a5bdf3aacec18a5f9f8dbee",
    "is_f8f9e8809f_ancestor_of_origin_cloud": false,
    "state": "LOCAL ONLY; NEVER PUSH per issuer Msg-ID 93725"
  }
}
```

The answer-state grain is one invocation: `--offline-self-test` prints all four
ratified state tokens exactly once. Its outer rc is a test-harness result; each case also
prints and checks its own semantic rc. The conditioned-grant case is the discriminator:
it prints `PARTIAL_OR_BLIND` and `STATE: NOT-DECIDABLE`, checks rc 2, and never emits a
pass/fail IAM verdict.

## Exercised outputs

The real shim run used as the default fixture disclosure included:

```text
ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS
PLAN: 1 IAM policy subject(s), but zero deny-add / allow-removal changes;
zero population without an IAM change is CORRECT
WITHIN BUDGET: scanned 0 of 0 simulation_call; budget: 90 s (default)
DEFERRED: 0 of 0 simulation_call(s) did not return
```

The four-state invocation ended:

```text
ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS   [case rc=0]
ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS    [case rc=0]
ANSWER-STATE: NOT_APPLICABLE               [case rc=0]
ANSWER-STATE: PARTIAL_OR_BLIND             [case rc=2]
STATE: NOT-DECIDABLE (rc=2, distinct from clean rc=0 and failing rc=1)
OFFLINE ANSWER-STATE SELF-TEST: 4/4 PASS; ZERO live IAM calls
```

Rule T was exercised through the production `simulate()` call site with a planted local
`TimeoutExpired`; the observed subprocess timeout was non-null and at most the requested
0.25 seconds. Output contained `BUDGET REACHED` and `STATE: NOT-DECIDABLE`; rc was 2.
The help surface prints all three rc meanings and the carrier precedence. No corpus-width
loop exists, so help also says why no cursor or partial verdict is manufactured.

## Battery, diff, and bounds evidence

```text
python .tools/tests/test_comp_denytest_battery.py
  9/9 PASS

python -m pytest -q .tools/tests/test_comp_denytest_battery.py
  1 passed in 1.42s

bash .tools/commit-gate.sh .tools/comp-denytest.py .tools/tests/test_comp_denytest_battery.py
  OK: pre-commit gate clean for 2 of 2 file(s)

python -m pytest -q .tools/tests
  INTERNALERROR at .tools/tests/test_fabric_check_classify.py:76: sys.exit(0)
  no tests ran; rc 1
```

Production change `f8f9e8809f` is exactly two files: 394 changed engine lines and one new
294-line battery (`621 insertions, 67 deletions`). The shim, registries, enum, IAM roles,
policies, attachments and AWS resources are unchanged. `_compbudget.py` is imported and
consumed, not edited. No retirement act occurred. No spec-vs-world divergence was found,
so `surprises` is empty and no investigation row is owed.

FWD-9 is independent post-commit evidence, not author self-certification:
`0.8.0_AE_CloudComp~C` ran the real shim at the full `f8f9e8809f...` commit, returned rc 0,
reported all four tokens and `4/4 PASS; ZERO live IAM calls`, and made no edits.
