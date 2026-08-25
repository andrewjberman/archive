<task_order>
<to_id>ADHOC.r4a-closeout-trigger-false-attribution-fix</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~B</issued_to>
<date>2026-08-03</date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "r4a-closeout-trigger-false-attribution-f" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>P2 (instrument-honesty defect; non-blocking, advisory-class producer)</priority>

<title>R4-A closeout trigger: stop attributing registration commits as closeouts (token-sweep over-match)</title>

<context>
You authored NFRA_MSBEFF.R4-A (`.tools/git-hooks/closeout-comp-state-post-commit.sh`, 2026-07-23).
It has now produced its first live batch of findings, and 4 of 10 were FALSE ATTRIBUTIONS:
closeout-drift findings filed against ADVI_TWR, MDPF_CHANNEL_INDEPENDENCE, OPAL_CONSOLIDATION and
OPAL_GLDRNS -- none of which were ever closed (all JSONs read status:active). Their recorded
"closing commits" were REGISTRATION commits: 8ca69b870b (registered ADVI_PERFORMANCE) and
d1cca72e10 (registered MDPF_CHANNEL_INDEPENDENCE).

MECHANISM (source-grounded @2733bfceff, closeout-comp-state-post-commit.sh:44-48): the
REGISTRY-only branch derives "closing" codes by grepping ALL `[A-Z][A-Z0-9]+_[A-Z0-9_]+` tokens
from the commit's added/removed REGISTRY.md diff rows. A registration commit ADDS a row, and any
project code appearing in that row's text (or in diff-adjacent changed rows) is swept in as
"closing." The JSON branch has a milder form of the same class: CLOSURE_RE matches any staged JSON
whose content CONTAINS a closure status -- it cannot distinguish "status flipped to closure this
commit" from "already-closed JSON edited for another reason."

Consequence class: false findings assign expiry-debt to owners of projects that were never closed,
and train agents to skim the finding surface (the exact TRIGGER_LAYER failure the instrument
exists to prevent). Full disposition record: COO log @52bcb6c1b5. CTO concurrence + routing to
this lane under COO dispatch: CTO msg 20260803T151725Z.

Note one adjacent record drift you should reconcile in passing: `.open_findings/README.md:26-28`
says the R4 triggers are "NOT yet wired live" -- yet findings were produced 07-29. Correct the
README arm-state line to reality as part of this TO.
</context>

<scope>
1. Fix code derivation so a finding is filed ONLY for a project genuinely closing in that commit:
   - JSON branch: fire only when the status VALUE flips to a closure value IN THIS COMMIT
     (compare HEAD~1:file vs HEAD:file status, handling file-added-this-commit), not when staged
     content merely contains a closure status.
   - REGISTRY branch: fire only for codes whose row MOVES INTO the Completed/Archived table (or is
     REMOVED from an Active table while appearing in Completed) -- never for all diff tokens.
2. Keep: owner = closing-commit author; async/detached non-blocking posture; scoped comp-state
   invocation; finding schema unchanged.
3. Extend `.tools/git-hooks/test-closeout-comp-state.sh` with the false-attribution controls
   (see acceptance criteria). Run the full harness, not only the new cases.
4. Fix the README arm-state line (context note above).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-grep "closeout-comp-state" .tools org</run>
      <expect>Consumer/reference set enumerated: the installer, the test harness, the README, and any breadcrumb caller. No consumer depends on the token-sweep behavior being fixed.</expect>
      <if_mismatch>STOP. If any consumer reads the derived codes downstream, surface the coupling to COO before writing.</if_mismatch>
    </step>
    <step>
      <run>bash .tools/git-hooks/test-closeout-comp-state.sh</run>
      <expect>Baseline harness PASSES pre-change (a failing baseline means the defect surface is wider than this TO; report before proceeding). Record the pass/fail census with its denominator.</expect>
      <if_mismatch>STOP. Report baseline failures to COO before any edit.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>bash .tools/git-hooks/test-closeout-comp-state.sh</run>
      <expect>Full harness PASSES including the new negative + positive controls (acceptance criteria 1-4). Print the case count -- the denominator must have GROWN vs Phase 1.</expect>
      <if_mismatch>STOP. Do not commit until every control discriminates (a control that cannot fail is not a control).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>git log --oneline -3 -- .tools/git-hooks/closeout-comp-state-post-commit.sh</run>
      <expect>Your fix commit present; no interleaved edit from another lane landed mid-flight.</expect>
      <if_mismatch>Surface to COO -- another agent touched the trigger concurrently.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. NEGATIVE CONTROL (registration): a test commit that ADDS a new Active REGISTRY row + a new JSON
   with status:active -- where the row text MENTIONS other existing project codes -- produces ZERO
   findings. This is the exact 8ca69b870b / d1cca72e10 shape and it must be a named test case.
2. POSITIVE CONTROL (genuine close): a test commit performing a 2-step atomic close (JSON status
   flip to a closure value + REGISTRY row move to Completed) produces EXACTLY ONE finding, for
   exactly that code, owner = commit author. Run in ISOLATION from the negative control.
3. NEGATIVE CONTROL (already-closed edit): editing an already-closed JSON (status unchanged,
   e.g. a phase-text amendment) produces ZERO findings.
4. POSITIVE CONTROL (created-at-close): a JSON CREATED in the closing commit already carrying a
   closure status (the NFRA_TOOLSTACK @f58d38698b shape) DOES fire -- file-added-this-commit must
   not be silently skipped by the before/after compare.
5. README.md arm-state line corrected to reality.
6. Session log includes a Compiler Tools section reproducing every <run> from
   <compiler_tools_mandate> with observed output and explicit pass/fail vs <expect>. Missing rows
   = REWORK.
</acceptance_criteria>

<cross_domain_coordination>
The trigger fires on org/projects/ commits estate-wide, so every closing agent is a consumer of
its verdicts -- but the FIX touches only .tools/git-hooks/ (your authoring lane) + the harness +
README. No shared-file collision with active TOs identified (checked against the pending-TO set
2026-08-03). If you find yourself needing to touch comp-state itself (state_scan.py), STOP and
surface -- that is a different owner surface.
</cross_domain_coordination>

<references>
  <ref type="disposition">org/tier1_exec/2.0.0_SA_COO/logs/2026-08-03/seating_mdlp_routing_and_findings_triage_1450-1520Z.md @52bcb6c1b5</ref>
  <ref type="cto-concurrence">org/mcp/inbox/2.0.0_SA_COO/read/20260803T151725Z_1.0.0_SA_CTO_W1_BLOCKED__premise_refuted_--_07-30_gar.md (item 1)</ref>
  <ref type="doctrine">org/critical_paths/.open_findings/README.md (TRIGGER_LAYER lifecycle)</ref>
</references>

<acceptance_note>
A TO completion report whose session log lacks the Compiler Tools reproduction is REWORK, not
COMPLETE (TO_COMPILER_GATE).
</acceptance_note>
</task_order>
