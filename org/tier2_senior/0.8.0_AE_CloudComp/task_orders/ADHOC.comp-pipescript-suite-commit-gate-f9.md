<task_order>
<to_id>ADHOC.comp-pipescript-suite-commit-gate-f9</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-08-04</date>
<status>staged</status>
<priority>P1 (Andrew-named start item 2, graph-seam/comp-blast fixes thread -- CVO ITEM-2 relay @fa4279588; F9 disposition CTO 062256Z, build via COO)</priority>

<title>comp-pipescript test suite: path-scoped commit-gate stage -- the suite runs when engine/subparser/test files are staged (F9: a gate no runner is wired to decays silently)</title>

<context>
CVO dial F9 (DIAL_RECORD_comp-pipescript_20260804.md @7900435cb): the 4-file suite sat RED for
~4 weeks unobserved -- every failure dated to a real estate change nobody replayed the suite
against. Extends memory/feedback_gate_accepted_on_observed_green_run: acceptance needs an
observed green AND a wired runner.

CTO disposition (062256Z, verbatim mechanism): "PATH-SCOPED COMMIT-GATE STAGE -- the 4-file
suite runs when comp-pipescript's engine/subparser/test files are staged (same scoped-stage
shape as rcg-sweep-check: zero cost to unrelated commits, and the suite's green becomes
observable at exactly the moments it can break -- which is precisely when your P6 fixtures went
stale). NOT a scheduled QA run: a schedule observes on a clock, the gate observes on the CAUSE."

SHAPE CLARIFICATION (do not over-copy the reference): .tools/git-hooks/rcg-sweep-check.sh keys
on AUTHOR IDENTITY -- that mechanism is specific to the RCG sweep-executor ruling and is NOT
what F9 borrows. F9 borrows only the SCOPED-STAGE wiring: a pre-commit stage that inspects the
STAGED PATHS and runs iff a watched path is staged; every other commit pays zero cost.
</context>

<scope>
1. Confirm suite membership from the dial record (P6/P7) + comp-pydeps. Candidate set:
   org/modules/graph/tests/{test_multi_pipeline.py, test_pipescript_deployed_bd_hold.py,
   test_pipescript_io_discrimination.py} (the three repaired @a35ac7af8) +
   test_sovereign_held_no_drift.py (INVOKEs pipeline_cli per comp-pydeps). Source-confirm the
   4th; if the true set differs, the WATCH LIST derives from membership, not from this TO.
2. Build the pre-commit stage: iff any of {org/modules/graph/pipeline_cli.py,
   .tools/safe_deploy_core.py, .tools/comp-pipescript (shim), the suite files} is STAGED, run
   the suite; non-green = REFUSE the commit, loud, printing the failing test names + the staged
   trigger paths. Unrelated commits: zero suite invocations (measurably -- not "fast", ZERO).
3. Wire into the existing pre-commit chain the same way rcg-sweep-check installs (idempotent
   install script alongside .tools/git-hooks/install-owned-paths.sh family); never a new
   standalone hook that races the existing chain. Bypass, if any, is an audited env marker in
   the rcg-sweep pattern -- never silent.
4. WATCH-LIST DISCIPLINE: derive the watched path set in ONE place with a comment naming this
   TO and the dial F9 -- a hand-copied list in two files is the decay class this gate exists to
   kill. If the F1 TO (sibling, same seat) adds fixtures, the suite globs must pick them up
   without editing the gate.
5. NO alarms / SNS / scheduled runners (moratorium; and CTO explicitly ruled the schedule shape
   OUT -- the gate observes on the CAUSE).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>python -m pytest &lt;the confirmed suite files&gt; -q   (pipe-free rc)</run>
      <expect>Green at the current denominator (41/41 as repaired @a35ac7af8, or the moved count if F1 landed first -- state which).</expect>
      <if_mismatch>STOP. Building a gate on a red suite ships a gate that blocks every engine commit on arrival -- repair first (CVO owns fixture semantics; surface, do not silently re-fix).</if_mismatch>
    </step>
    <step>
      <run>read .tools/git-hooks/rcg-sweep-check.sh + its install script; enumerate the existing pre-commit chain members</run>
      <expect>Chain understood; insertion point identified; no hook ordering hazard (owned-paths must keep running).</expect>
      <if_mismatch>STOP. Surface the chain conflict to COO+CTO before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>MUTANT EXERCISE: introduce a throwaway breaking edit to pipeline_cli.py (uncommitted), stage it, attempt a commit</run>
      <expect>The gate FIRES and REFUSES, naming the failing tests + trigger path. Capture verbatim. Revert the mutant.</expect>
      <if_mismatch>STOP. A gate that does not fire on the mutant is not a gate -- rework before commit.</if_mismatch>
    </step>
    <step>
      <run>UNRELATED-COMMIT EXERCISE: stage a docs-only change, commit</run>
      <expect>Zero suite invocations (instrument it -- e.g. a probe line to stderr or a counter -- then remove the probe); commit passes untouched.</expect>
      <if_mismatch>STOP. A gate taxing every commit gets bypassed estate-wide within a week -- scoped-stage is the load-bearing property.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>FIRST REAL FIRE: the gate's acceptance is its first OBSERVED green on a real (non-authoring) commit that stages a watched path -- per memory/feedback_gate_accepted_on_observed_green_run, the authoring commit does NOT count</run>
      <expect>Cite the observed commit hash + gate output verbatim in the completion report. Until it exists, this TO closes at ACCEPTED-AT-BUILD, full acceptance pending first fire (the DT auto-append precedent).</expect>
      <if_mismatch>Do not self-mark complete on the build alone -- report ACCEPTED-AT-BUILD and name the pending observation.</if_mismatch>
    </step>
    <step>
      <run>report to COO + CTO + CVO (dial F9 closure; CVO folds the wired-runner into the dial record)</run>
      <expect>Report cites: watch list + its single derivation point, mutant capture, unrelated-commit capture, first-fire status.</expect>
      <if_mismatch>REWORK.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
(1) Sibling TO ADHOC.comp-pipescript-postdeps-f1-guard (same seat) edits the engine + adds
fixtures -- self-sequence at your seat; whichever lands second re-runs the other's exercises
against the moved state. If F1 lands after this gate, its engine edit is the natural FIRST REAL
FIRE candidate for Phase 3.
(2) 0.8.0_AE_CloudComp~B's staged assets-tree coverage build touches the same watched paths --
once this gate lands, THEIR commit becomes a gate fire; give ~B a heads-up MCP when the gate
lands so a refusal at their seat reads as the control working, not as breakage.
(3) The pre-commit chain is shared estate machinery (owned-paths + rcg-sweep-check + this) --
any chain-order change surfaces to CTO before commit.
</cross_domain_coordination>

<acceptance_criteria>
1. Suite membership source-confirmed; watch list derived in one place, citation in the gate.
2. Mutant exercise captured (fires + refuses, verbatim); unrelated-commit exercise captured
   (ZERO invocations, instrumented).
3. Wired via idempotent install in the existing chain; bypass (if any) audited.
4. First-fire status honestly stated: OBSERVED-GREEN with commit cite, or ACCEPTED-AT-BUILD
   with the pending observation named. No self-acceptance on the authoring commit.
Plus: session log includes a Compiler Tools section reproducing every <run> with observed output
and explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="authority">Andrew start word item 2 (graph-seam/comp-blast fixes) -- CVO records @74451794e + @fa4279588; CTO F9 disposition 062256Z; CTO partition note @ff160d0b5 (graph stream)</ref>
  <ref type="finding">DIAL_RECORD_comp-pipescript_20260804.md F9 + P6 (@7900435cb); repair @a35ac7af8</ref>
  <ref type="shape">.tools/git-hooks/rcg-sweep-check.sh (scoped-stage wiring ONLY -- not the identity keying)</ref>
  <ref type="law">memory/feedback_gate_accepted_on_observed_green_run_never_authoring_commit.md; memory/feedback_control_must_fire_on_the_defect_event_not_the_class_name.md</ref>
  <ref type="sibling">ADHOC.comp-pipescript-postdeps-f1-guard (same seat)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
