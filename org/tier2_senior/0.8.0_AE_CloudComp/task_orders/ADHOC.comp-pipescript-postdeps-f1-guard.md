<task_order>
<to_id>ADHOC.comp-pipescript-postdeps-f1-guard</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-08-04</date>
<status>complete</status>
<priority>P1 (Andrew-named start item 2, graph-seam/comp-blast fixes thread -- CVO ITEM-2 relay @fa4279588; SEV-HIGH on the $22M-class ad-hoc-run guard)</priority>

<title>comp-pipescript postdeps: F1 two-half guard -- unknown script_id rc=2 + kill the silent flagless bd default</title>

<context>
CVO dial record (org/tier1_exec/3.0.0_SA_CVO/deliverables/DIAL_RECORD_comp-pipescript_20260804.md
@7900435cb, amended @2c9b1bb9c) finding F1 SEV-HIGH, TWO halves -- the fix must carry BOTH:

(a) `postdeps ZZZ_NO_SUCH_SCRIPT.py --firm bd` returns rc=0 "No dependencies declared" --
    byte-identical to a known-clean script. On the mode that exists BECAUSE of the $22M incident,
    a typo answers "clear to run, no post-steps."
(b) AMENDED (CTO datum, CVO re-exercised both limbs): postdeps FLAGLESS also works and SILENTLY
    DEFAULTS to bd (rc=0, `[bd]` banner) -- the exact silent-tree-default class the 07-30 stub
    killed for the io family survives on THIS mode.

THE COMPOSITION IS THE SHARP EDGE: flagless + typo'd script = silent wrong-tree default + rc=0
no-deps = DOUBLE false-clean on the $22M guard. Per CVO (RAVC close 070735Z): the composition IS
the load-bearing test -- it ships as the acceptance FIXTURE, not a prose note.

Engine: org/modules/graph/pipeline_cli.py (shim .tools/comp-pipescript). Consumers
(comp-pydeps, denominator 5): .tools/safe_deploy_core.py [INVOKE -- DEPLOY GATING, not just
reporting], org/modules/graph/extract_s3.py [IMPORT], + 3 test files. A wrong edit here changes
deploy gating; regression controls are mandatory.
</context>

<scope>
1. Half (a): validate script_id against the tree's scripts UNION deps keys; unknown -> rc=2
   (TOOL-02 pattern), error naming the tree searched and the universe size (print the
   denominator). THE VALIDATION UNIVERSE MUST BE DERIVED FROM THE SAME MAP THE TOOL RESOLVES
   TREES FROM AT RUNTIME -- a re-derived predicate, never a hand-copied list
   (memory/feedback_a_predicate_is_not_a_roster.md). ~B's staged assets-tree widening must
   extend this guard automatically, with zero edits to it.
2. Half (b): postdeps gets the required-flag treatment (rc=2 REFUSED flagless, matching the
   07-30 io-family stub) OR an explicitly NAMED default printed loud in the banner -- builder
   proposes which with one-line reasoning; the io-family precedent (required flag) is the
   default choice unless a live caller inventory argues otherwise. If any live caller invokes
   postdeps flagless (grep callers first), enumerate them in the report -- do not break a
   caller silently.
3. The composition fixture (flagless + unknown script) lands as a PERMANENT test in the suite
   (incident-as-fixture law) -- it must FAIL against the pre-fix engine and PASS post-fix.
4. NO behavior change to io / deployed / stats / inject modes; no alarms/monitors (moratorium).
   stats/inject are F3, riding WS4 -- out of scope here.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>.tools/comp-pipescript postdeps ZZZ_NO_SUCH_SCRIPT.py --firm bd; echo "rc=$?"   (pipe-free rc read)</run>
      <expect>rc=0 "No dependencies declared" reproduced (pre-fix control, half a), captured verbatim.</expect>
      <if_mismatch>STOP. If it now refuses, the guard already landed -- re-ground with CVO before building.</if_mismatch>
    </step>
    <step>
      <run>.tools/comp-pipescript postdeps ZZZ_NO_SUCH_SCRIPT.py; echo "rc=$?"   (flagless, pipe-free)</run>
      <expect>rc=0 with silent `[bd]` banner (pre-fix control, half b + the composition), captured verbatim.</expect>
      <if_mismatch>STOP. Same re-ground rule.</if_mismatch>
    </step>
    <step>
      <run>comp-pydeps consumers pipeline_cli</run>
      <expect>5 consumers incl. .tools/safe_deploy_core.py [INVOKE]; no new consumer since this TO's authoring.</expect>
      <if_mismatch>STOP. A new consumer = widen the regression set before writing.</if_mismatch>
    </step>
    <step>
      <run>python -m pytest org/modules/graph/tests/ -k "pipescript or multi_pipeline or sovereign_held" -q   (or the suite's own runner; confirm membership from the dial record P6/P7)</run>
      <expect>Baseline green (41/41 as repaired @a35ac7af8) BEFORE any edit.</expect>
      <if_mismatch>STOP. A red baseline means an estate change since the dial -- surface to CVO (re-dial trigger), do not build on red.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>the composition fixture against the PRE-fix engine (git stash-free: run from a scratch checkout or pre-edit copy), then against the fixed engine</run>
      <expect>FAILS pre-fix (proves it discriminates), PASSES post-fix. Both runs captured.</expect>
      <if_mismatch>STOP. A fixture that passes pre-fix asserts nothing -- rework it until it fails against the defect.</if_mismatch>
    </step>
    <step>
      <run>fixed-invocation regression set: comp-pipescript io + deployed on one script per tree (bd/inf/cot/mdpf), pre/post diff; full suite green</run>
      <expect>Byte-identical io/deployed outputs on every tree; suite green with the new fixture(s) counted (state the new denominator).</expect>
      <if_mismatch>STOP. Any io/deployed diff is a gating change -- surface to COO+CTO before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>both Phase-1 control invocations post-fix; report to COO + CTO + CVO</run>
      <expect>Half (a): rc=2 naming the searched universe. Half (b): flagless REFUSED rc=2 (or the NAMED-default banner if that path was chosen+justified). Report cites pre/post captures + commit + new suite denominator.</expect>
      <if_mismatch>REWORK -- an instrument fix without its exercised before/after is a filing, not a build.</if_mismatch>
    </step>
    <step>
      <run>notify 3.0.0_SA_CVO: engine/subparser changed (dial re-dial trigger 5)</run>
      <expect>MCP sent same window as the landing commit -- the dial reopens on CVO's schedule, not silently never.</expect>
      <if_mismatch>The re-dial trigger fires on the CHANGE, not on the notification -- a missed notify is a protocol violation, send it late rather than never.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
(1) 0.8.0_AE_CloudComp~B holds ADHOC.comp-pipescript-assets-tree-coverage (staged, behind 2-3
in their queue) -- SAME FILES (pipeline_cli.py + safe_deploy_core.py). MCP ~B before first edit;
whoever lands second rebases their regression captures on the moved baseline. The Scope-1
predicate-not-roster requirement exists precisely so these two builds compose without a merge
fight over the universe definition.
(2) WS4 hardening will replace the :270 refusal stub (F3 rides it) -- do NOT touch the stub
here; if your required-flag treatment for postdeps routes through it, coordinate with the WS4
owner via CTO first.
(3) safe_deploy_core.py INVOKEs the engine (deploy gating) -- the Phase-2 regression set is the
gate; a diff there is a STOP, not a note.
</cross_domain_coordination>

<acceptance_criteria>
1. Both pre-fix false-clean controls and both post-fix refusals captured verbatim (identical
   invocations, pipe-free rc reads), in the session log.
2. The composition fixture is IN the suite, shown failing pre-fix and passing post-fix.
3. Regression: byte-identical io/deployed outputs per tree, denominator stated; suite green at
   the new count; validation universe shown DERIVED (cite the file:line where the guard reads
   the tree map).
4. CVO re-dial notification sent (trigger 5).
Plus: session log includes a Compiler Tools section reproducing every <run> with observed output
and explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="authority">Andrew start word item 2 (graph-seam/comp-blast fixes) -- CVO records @74451794e + @fa4279588; CTO partition note @ff160d0b5 (this rides the graph stream, keep MDPF traffic out)</ref>
  <ref type="finding">DIAL_RECORD_comp-pipescript_20260804.md F1 (@7900435cb, amended @2c9b1bb9c)</ref>
  <ref type="law">memory/feedback_a_predicate_is_not_a_roster.md; memory/feedback_review_deploy_split_pins_the_artifact.md (incident-as-fixture)</ref>
  <ref type="sibling">ADHOC.comp-pipescript-suite-commit-gate-f9 (same seat, this TO's suite is that TO's payload)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
