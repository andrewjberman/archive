# TO INF_RUNNER_REFACTOR.P1 — PHASE 1 SCRIPTS: the Inflection gold analytics runner, Groups A–D + parquet writer-format

<task_order>
  <metadata>
    <to_id>INF_RUNNER_REFACTOR.P1.scripts-groups-a-d-parquet</to_id>
    <project>INF_RUNNER_REFACTOR</project>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued>2026-08-11</issued>
    <status>active</status>
    <gate>1.0.0_SA_CTO</gate>
    <verifier>3.0.0_SA_CVO</verifier>
  </metadata>

  <objective>
    Build PHASE 1 (SCRIPTS) of the INFLECTION gold analytics runner — Groups A–D + the parquet
    writer-format — by TRANSPOSING the 49F archetype shape onto the INF field sourcing. Runs in
    PARALLEL with DS base's 49F P1. Andrew-launched ~0924Z 2026-08-11 (his word at the CTO terminal,
    verbatim: "Ok I'm instantiating ~A now, let COO know").
  </objective>

  <context>
    ISSUANCE NOTE: dispatched by broker message at 092643Z, minutes ahead of this file, because
    Andrew instantiated the lane in real time and an EMPTY INBOX AT BOOT is worse than a TO that
    trails by minutes. This is a deliberate ordering, not the 49F failure repeated — on that lane the
    TO file was never written at dispatch at all (see MDPF_49F_BUILD.P1's own context block).

    PHASE ORDER (Andrew-direct @4dbf4a0d7c, SEQUENTIAL — each phase gates the next):
      P1 SCRIPTS -> P2 TIMING -> P3 REPOINTS -> P4 PUBLISHERS -> P5 DECOMMISSION
    THIS TO IS P1 ONLY.

    SHAPE-TRANSPOSITION DOCTRINE (Andrew-direct @6e180df78e): instantiate the shape by SOURCING
    FIELDS (RAW / MANUFACTURABLE-as-named-computation / ABSENT-with-shape), NEVER by porting 49F
    code. The field contract + script sequence are the shape; the code is not.

    WHY THIS LANE EXISTS: DS base is saturated — 49F P1 B-4/B-5a plus four armed deploy timers — so
    INF work handed to base queues behind the 49F build and three deploy windows. Parallel is the
    only way INF moves today. CTO's positioning read + COO's capacity half, synthesized to Andrew
    092331Z; he launched on it.

    ADMISSION CRITERION, STANDING: EXTRACT-side only. A build admitting anything from the quality
    partition's DISCARD side is a patch by construction, and "no patches" is his word on the archetype.
  </context>

  <compiler_tools_mandate>
    comp-validate per gold script; comp-pipescript deployed for MATCH after any S3 upload.
    MEASURED INSTRUMENT BOUNDARY: comp-pipescript deployed EXCLUDES bundle-routed scripts and
    under-reports multi-homed ones without its DENOMINATOR line read — never accept a deploy on
    MATCH alone (it returned MATCH while executing code was 4 days stale, 2026-08-11).
    Run proof-of-spec-check WITHOUT A PIPE: a piped rc is the pipe's, not the validator's.
  </compiler_tools_mandate>

  <acceptance_criteria>
    Acceptance is NOT authored here. THE PER-GROUP ACCEPTANCE BATTERIES IN THE GOVERNING SPECS ARE
    THE BAR:
      INF shape spec — org/tier1_exec/4.0.0_SA_CRO/deliverables/ADVREVIEW_49F_ABCD_AND_INF_SHAPE_SPEC_20260811.md @75db88d716
      The SHAPE (ruled 49F group specs) — A @9c294bbf15+@6fba62393b · B @d57bbf7229 ·
      C @39c41163cd+@f882b91ce2 · D @1e11389af8
    Plus, per Andrew @4dbf4a0d7c: STAGE-BY-STAGE compile verification (py_compile per stage), not a
    single pass at the end.
  </acceptance_criteria>

  <proof_of_spec>
    <instance_path_grammar>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_INF_{GROUP}_{YYYYMMDD}.json</instance_path_grammar>
    <criterion_id_grammar>INF-{group}-{artifact}-{check}</criterion_id_grammar>

    <group id="A" status="NOT_YET_MINTED"/>
    <group id="B" status="NOT_YET_MINTED"/>
    <group id="C" status="NOT_YET_MINTED"/>
    <group id="D" status="HOLD_FOR_RULING" ruling_event="at ~A's Group-C completion" ruling_inputs="DS base's B-4 emitter outcome + ~A's C-completion" deciders="Andrew + 1.0.0_SA_CTO + 2.0.0_SA_COO"/>
    <group id="PARQUET-WRITER-FORMAT" status="NOT_YET_MINTED"/>

    <!--
    THE ID SETS ARE DELIBERATELY UNMINTED BY THE ISSUER. The COO has NOT read the INF batteries and
    will not hand the assignee invented id strings — a wrong id list validates STRUCTURALLY and
    proves the wrong thing. Each group's set is enumerated FROM ITS OWN BATTERY at that group's
    start, by the surfaced-not-guessed method (judgment calls stated: a multi-part bullet split into
    independently-checkable rows; a promoted artifact-table row), and appended here at next touch.
    An ambiguous battery SURFACES rather than guesses.

    THE THREE ISSUANCE GRAMMARS above are bound BEFORE the first mint (CTO 092331Z, adopted
    fabric-wide). All three were earned from defects in the 49F lane the same hour:
      (1) per-group instance paths — the 49F TO declared ONE path matching none of three landed
          instances; a completion flip on it would have read absence as work-not-done.
      (2) firm-tokened criterion ids — 49F minted A5-/B5-/C5- with no firm token, and CVO's cert
          step-zero reads ACROSS instances, so verbatim battery transposition would collide.
      (3) UNCOMPUTABLE-with-declaration PRE-AUTHORIZED — a by-construction-impossible row must never
          force a choice between a faked PASS and a stall.

    TWO-LAYER DIVISION (unchanged): the validator catches the ASSIGNEE omitting against this list;
    CVO's cert-of-built step-zero catches THIS LIST omitting against the governing SPEC.
    Per-group validation:
      python .tools/proof-of-spec-check.py {instance}.json --expected-criteria {that group's ids}
    NOTE the issuance lint (.tools/git-hooks/to-proof-of-spec-check.sh:29) is a PRESENCE grep on NEW
    files only — it binds issuance PRESENCE, never issuance CORRECTNESS. It cannot catch a
    well-formed element naming a nonexistent path. Do not read its pass as a check of this block.
    -->
  </proof_of_spec>

  <scope>
    <files>
      <file action="modify">data/inf/scripts/gold/runners_* (Groups A–D per the transposed specs)</file>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_INF_{GROUP}_20260811.json (one per group)</file>
      <file action="reference">the INF shape spec + the four ruled 49F group specs at the commits above</file>
    </files>
    <tree_boundary>
      TWO AGENTS ARE IN THE inf TREE. Firm separation separates inf from bd/cot; it does NOT separate
      two agents inside inf.
      ~A OWNS: data/inf/scripts/gold/runners_*
      BASE RETAINS: data/inf/scripts/silver/build_billing_dim.py — two live queued defects
        (BILLING_COLUMN_MAP keys miss the real vendor headers, so silver silently drops every period
        column; parse_dollar(empty)->0.00 conflates vendor-absent with vendor-zero, understating firm
        fee-earning AUA ~30%). ~A DOES NOT TOUCH THAT FILE. If ~A's work reads ending_mv, a 0.00 there
        is a PARSE ARTIFACT, not a vendor zero.
      SHARED TOUCHPOINTS (safe_deploy_core second-targets row, lib/): already batched acts with
        owners — one comp-blast pass before touching either.
    </tree_boundary>
  </scope>

  <requirements>
    <requirement id="1">Group A — transposed by FIELD SOURCING, not code port.</requirement>
    <requirement id="2">Group B — valuation canonicals.</requirement>
    <requirement id="3">Group C.</requirement>
    <requirement id="4">Group D emitters — **HOLD FOR RULING, sovereign-explicit.** SCOPE THIS LANE A -> B -> C.
      Andrew-direct 2026-08-11 ~0928Z, VERBATIM: "Have ~A run through Groups A B C and by the time
      they're done we will likely have had time to assess DS Base attempt at the emitter and will come
      to a conclusion on how ~A should proceed to that end."
      THIS IS NOT A PASSIVE WAIT-ON-B-4 — it is a NAMED RULING EVENT with named inputs:
        RULING EVENT: at ~A's Group-C completion.
        INPUTS:       DS base's B-4 emitter outcome + ~A's C-completion.
        DECIDERS:     Andrew + CTO + COO. Outcome may be adopt-the-mechanic-verbatim, amend, or other.
      Consequence for the lane: NOBODY IDLES AND NOBODY FREELANCES AN EMITTER. ~A does not build D and
      does not pre-decide its shape; ~A reports C-completion, which is what FIRES the ruling.
      (This upgrades COO's D-wait default — which Andrew did not overrule — to sovereign-explicit.)</requirement>
    <requirement id="5">Parquet writer-format: {table}/date={D} — WRITER FORMAT ONLY.</requirement>
    <requirement id="6">Evidence captured AS THE WORK PROCEEDS, never retro-fitted. An instance assembled afterwards is weaker even when every field is filled, because the evidence was selected knowing the answer.</requirement>
    <requirement id="7">06_current_state recompiles: ONCE PER WAVE at wave close, NOT per group; route to the COO exec lane per the @7f5a958bdf precedent. Three lanes recompiling one governance artifact per group would race it under a single owner — a governance-artifact collision that a comp-blast over data trees structurally cannot see.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Groups A–C + parquet writer-format, stage-by-stage compile-verified (D on its wait's release)</deliverable>
    <deliverable type="document">A schema-valid PROOF_OF_SPEC instance per group, passing proof-of-spec-check with --expected-criteria</deliverable>
    <deliverable type="document">Session log with Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <item>Do NOT start P2 (timing), P3 (repoints), P4 (publishers) or P5 (decommission) from this TO.</item>
    <item>Do NOT RESOLVE THE F-1 ROOT QUESTION. The spec's own F-1 finding is that the default product root EXTENDS a measured-non-conforming tree against Rule 17b's ratified {vendor}/{firm}/{medallion} grammar. Minting a new root is a Rule 24 TAXONOMY ACT and 17b ratified direction WITHOUT migration authority — it is Andrew's, not a builder's. P1 is the writer FORMAT; the DESTINATION is P3. If code forces a path constant, name it in the instance's `surprises`, do not decide it.</item>
    <item>Do NOT port 49F code. Source the fields.</item>
    <item>Do NOT touch data/inf/scripts/silver/build_billing_dim.py (base's queued defects).</item>
    <item>Do NOT chase the .parquet object under s3://opal-data-inf/bronze/orion-api-v2/ — a live Rule-17a specimen routed to the P3 family by CTO. Leave it.</item>
    <item>Do NOT admit anything from the quality partition's DISCARD side.</item>
    <item>Do NOT accept a deploy on comp-pipescript MATCH alone — read its DENOMINATOR line.</item>
    <item>Do NOT guess a criterion id. Surface an ambiguous battery instead.</item>
    <item>Do NOT hold work on a finding and do NOT manufacture an approval step. No gate exists on this lane that is not named in this TO.</item>
  </do_not>
</task_order>
