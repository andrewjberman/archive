# TO COT_RUNNER_REFACTOR.P1 — PHASE 1 SCRIPTS: the Cottonwood gold analytics runner, Groups A–C (SCOPED) + parquet writer-format

<task_order>
  <metadata>
    <to_id>COT_RUNNER_REFACTOR.P1.scripts-groups-a-c-scoped</to_id>
    <project>COT_RUNNER_REFACTOR</project>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued>2026-08-11</issued>
    <status>active</status>
    <gate>1.0.0_SA_CTO</gate>
    <verifier>3.0.0_SA_CVO</verifier>
  </metadata>

  <objective>
    Build PHASE 1 (SCRIPTS) of the COTTONWOOD gold analytics runner — Groups A/B/C SCOPED + the parquet
    writer-format — by TRANSPOSING the 49F archetype shape onto COT field sourcing. Third firm lane;
    runs in parallel with 49F (base) and INF (~A). Andrew-direct ~1450Z: *"Recs are approved for all"*
    @162965ed1c — DS~B spawn GO'd, he instantiates the session himself.
  </objective>

  <context>
    THIS TO IS ON DISK BEFORE THE DISPATCH. Andrew spawns at his convenience rather than in real time, so
    there is no boot race and the honest ordering was available (contrast the ~A lane, where an empty inbox
    at boot was the worse failure — that reasoning is recorded in INF_RUNNER_REFACTOR.P1's context block).

    PHASE ORDER (Andrew-direct @4dbf4a0d7c, SEQUENTIAL): P1 SCRIPTS -> P2 TIMING -> P3 REPOINTS ->
    P4 PUBLISHERS -> P5 DECOMMISSION. THIS TO IS P1 ONLY.

    SHAPE-TRANSPOSITION DOCTRINE (Andrew-direct @6e180df78e): instantiate the shape by SOURCING FIELDS
    (RAW / MANUFACTURABLE-as-named-computation / ABSENT-with-shape), NEVER by porting 49F or INF code.
    THE TRANSPOSITION CURVE IS NOW MEASURED, so you have a real prior: ~A's verbatim rate ran
    64% -> 79% -> 86% across Groups A/B/C. Firm-specific work FRONT-LOADS. Expect Group A to be the
    heaviest adaptation and do not read that as a problem.

    ⛔ **cot IS A COMPLETELY SEPARATE FIRM PIPELINE FROM bd — NEVER mirror or sync between them**
    (gate + IAM enforced). This is not a style preference; it is a NEVER rule.
  </context>

  <compiler_tools_mandate>
    comp-validate per gold script; comp-pipescript deployed for MATCH after any S3 upload — and NEVER accept
    a deploy on MATCH alone, read the DENOMINATOR line (it returned MATCH while executing code was 4 days
    stale, 2026-08-11).
    Run proof-of-spec-check WITH THE ID SET POSITIONAL and WITHOUT A PIPE:
      python .tools/proof-of-spec-check.py {instance}.json {that group's ids}
    ⛔ There is NO `--expected-criteria` flag. The flagged form makes argv length 4 and EXITS rc=2. And a
    piped rc is the PIPE's, not the validator's. Both errors were made and fixed today (@b67d79971f).
  </compiler_tools_mandate>

  <acceptance_criteria>
    Acceptance is NOT authored here. The per-group batteries in the RATIFIED COT_ABCD_SHAPE_SPEC are the bar,
    plus the 49F group specs as the SHAPE (A @9c294bbf15+@6fba62393b · B @d57bbf7229 ·
    C @39c41163cd+@f882b91ce2 · D @1e11389af8). Confirm every ref resolves as a commit BEFORE building
    against it — ~A did this at boot and it is the right reflex.
    Plus STAGE-BY-STAGE py_compile per script at its build stage (Andrew @4dbf4a0d7c), not one pass at the end.
  </acceptance_criteria>

  <proof_of_spec>
    <instance_path_grammar>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_COT_{GROUP}_{YYYYMMDD}.json</instance_path_grammar>
    <criterion_id_grammar>COT-{group}-{artifact}-{check}</criterion_id_grammar>

    <group id="A" status="MINTED-AND-VALIDATED" instance="org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_COT_A_20260811.json" validator="VALID rc=0 unpiped, 13 rows 0 violations" minted_by="0.4.0_DS_ClientPlatform~B" minted_at="2026-08-11T153xZ">
      COT-A-A00-ROWCOUNT, COT-A-A00-SURFACES, COT-A-A01-MAPCENSUS, COT-A-A02-DISJOINT,
      COT-A-A02-VERSION-DET, COT-A-A02-VERSION-MUT, COT-A-A03-ROWCOUNT, COT-A-A04-GAPCENSUS,
      COT-A-A05-RESOLVE, COT-A-A05-CENSUSKEY, COT-A-ALL-PROVENANCE, COT-A-ALL-MANIFEST,
      COT-A-ALL-COMPILE
      <!-- Judgment calls in the enumeration (stated per TO): SURFACES row minted (no 49F/INF
      analogue -- the union universe is COT-specific); A06 row NOT minted (BUILD-BLOCKED wait,
      lives in declared_exclusions, not a fake UNCOMPUTABLE); ALL-rows denominator = 6 built
      artifacts. -->
    </group>
    <group id="B" status="MINTED-AND-VALIDATED" instance="org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_COT_B_20260811.json" validator="VALID rc=0 unpiped, 13 rows 0 violations" minted_by="0.4.0_DS_ClientPlatform~B" minted_at="2026-08-11T161xZ">
      COT-B-B00-ROWCOUNT, COT-B-B00-COLLAPSE, COT-B-B00-DUPFIXTURE, COT-B-B00-NULLSTATUS,
      COT-B-B00-DECOMP-IDENTITY, COT-B-B01-PASSTHROUGH, COT-B-B01-FLAGS, COT-B-B02-VERDICT,
      COT-B-B03-TIE, COT-B-B03-MUTANT, COT-B-ALL-PROVENANCE, COT-B-ALL-MANIFEST, COT-B-ALL-COMPILE
      <!-- Judgment calls: COLLAPSE + DUPFIXTURE + NULLSTATUS rows minted per the CTO 074437Z
      amendment + ABSENCE-IS-SERVE-LAW (no 49F/INF analogues); B03-TIE graded on the independent
      roster leg (the OPEN-cell fallback exercised, coverage denominators carried). -->
    </group>
    <group id="C" status="MINTED-AND-VALIDATED" instance="org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_COT_C_20260811.json" validator="VALID rc=0 unpiped, 14 rows 0 violations" minted_by="0.4.0_DS_ClientPlatform~B" minted_at="2026-08-11T162xZ">
      COT-C-C00-ONECLASS, COT-C-C00-SEMANTIC, COT-C-C00-VENDORAXIS, COT-C-C00-LADDER,
      COT-C-C00-MUT, COT-C-C01-SEGREGATION, COT-C-C01-VENDORDELTA, COT-C-C02-FIXTURES,
      COT-C-C02-REFUSE, COT-C-C03-FIELDS, COT-C-C03-STATUSFN, COT-C-ALL-PROVENANCE,
      COT-C-ALL-MANIFEST, COT-C-ALL-COMPILE
      <!-- Judgment calls: VENDORAXIS + LADDER + VENDORDELTA rows minted on cot's two native
      instruments (External Flow enum + contra marks -- no sibling analogue); C_04/C_05 are
      DECLARED WAITS on the P2 probe (declared_exclusions, blocker named), not fake rows. -->
    </group>
    <group id="D" status="HOLD_FOR_RULING" ruling_event="at ~B's Group-C completion" ruling_inputs="base's B-4 emitter outcome + ~A's D outcome + ~B's C-completion" deciders="Andrew + 1.0.0_SA_CTO + 2.0.0_SA_COO"/>
    <group id="PARQUET-WRITER-FORMAT" status="MINTED-AND-VALIDATED" instance="org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_COT_PARQUET-WRITER-FORMAT_20260811.json" validator="VALID rc=0 unpiped, 4 rows 0 violations" minted_by="0.4.0_DS_ClientPlatform~B" minted_at="2026-08-11T163xZ">
      COT-PWF-RUNNERCOMMON-GRAMMAR, COT-PWF-RUNNERCOMMON-PARQUETONLY,
      COT-PWF-RUNNERCOMMON-NOROOT, COT-PWF-RUNNERCOMMON-MANIFEST
      <!-- schema note: spec_ref.group = OTHER (the enum has no writer-format member; the INF
      precedent), artifact token RUNNERCOMMON carried in the ids for the coverage matcher. -->
    </group>

    <!--
    IDS UNMINTED BY THE ISSUER BY DESIGN. The COO has NOT read the COT batteries and will not hand over
    invented id strings — a wrong id list validates STRUCTURALLY and proves the wrong thing. Enumerate each
    group's set from its own battery at that group's start, STATE YOUR JUDGMENT CALLS, and append here.
    Surface an ambiguous battery rather than guessing.
    ⚠ THE COT TOKEN IS REQUIRED: 49F minted A5-/B5-/C5- with NO firm token and INF uses INF-. CVO's cert
    step-zero reads ACROSS instances, so an untokened id collides across three live firm lanes.
    UNCOMPUTABLE IS SPLIT — do NOT mint the bare value: use `-BY-CONSTRUCTION` (names the later run, e.g. a
    month-grain identity uncomputable from one day) or `UNVERIFIABLE-BY-INSTRUMENT` (names the substitute
    oracle, e.g. a simulate limb that cannot discriminate for an admin-class principal). Bare legacy is
    tolerated only on pre-split instances.
    -->
  </proof_of_spec>

  <scope>
    <files>
      <file action="modify">data/cot/scripts/gold/runners_cot/ (Groups A–C per the transposed specs)</file>
      <file action="create">the per-group PROOF_OF_SPEC instances under the grammar above</file>
    </files>
    <declared_waits>
      A_06 (identity bridge) is BUILD-BLOCKED on RECON-5a's first deliverable. C_04/C_05 pend the P2 probe.
      These are DECLARED WAITS, not idleness — build everything else and declare these with their blocker
      named. A scoped P1 that says what it could not reach beats a full P1 that quietly guessed.
    </declared_waits>
    <tree_boundary>
      ⛔ THREE AGENTS ARE NOW IN THE DS FAMILY AND FIRM SEPARATION DOES NOT SEPARATE AGENTS INSIDE ONE TREE.
      ~B OWNS: data/cot/scripts/gold/runners_cot/*
      DS BASE holds cot DEPLOY WINDOWS and the inf silver billing dim. ~A OWNS data/inf/scripts/gold/runners_inf/*.
      ⚠ **IMMEDIATE, TIME-BOXED: DS base holds an ARMED cot deploy at 15:06Z (CPR-2/C-3 + CPR-5 carry).**
      ~B's cot S3-deploy leg EXCLUDES ~15:00–15:15Z. Building and committing are fine; do not push code to
      the cot prefix inside that window. This is the host-level concurrency class that already bit us once
      today — a republish collided mid-chain and the C_01 guard correctly refused it.
    </tree_boundary>
  </scope>

  <requirements>
    <requirement id="1">Group A — transposed by FIELD SOURCING, not code port. Expect the heaviest adaptation here per the measured curve.</requirement>
    <requirement id="2">⛔ **Group B MUST carry the RELATIONSHIP-GRAIN COLLAPSE.** cot `fact_holdings` is RELATIONSHIP-grain — a row is Relationship × Account × Asset (Andrew-direct 2026-08-04). **NAIVE SUMS DOUBLE-COUNT.** Collapse via `collapse_relationship_grain()` before any aggregate. This is the single most likely way a COT B_00 produces a confident wrong number, and 49F/INF have no analogue to warn you.</requirement>
    <requirement id="3">Group C.</requirement>
    <requirement id="4">Parquet writer-format: {table}/date={D} — WRITER FORMAT ONLY. The DESTINATION root is P3, and minting a product root is a Rule-24 taxonomy act belonging to Andrew (17b ratified direction WITHOUT migration authority). If code forces a path constant, name it in the instance's `surprises`; do not decide it.</requirement>
    <requirement id="5">Evidence captured AS THE WORK PROCEEDS, never retro-fitted.</requirement>
    <requirement id="6">06_current_state recompiles: ONCE PER WAVE at wave close, NOT per group; route to the COO exec lane.</requirement>
    <requirement id="7">Two-frame transposability tally per group: rows-verbatim % BESIDE judgment-calls-diverged %. CTO ruled both frames travel together — quoting either alone misleads by ~14 points.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Groups A–C (scoped) + parquet writer-format, stage-by-stage compile-verified</deliverable>
    <deliverable type="document">A schema-valid PROOF_OF_SPEC instance per group, validated with the POSITIONAL id set, unpiped</deliverable>
    <deliverable type="document">Session log with Compiler Tools section</deliverable>
  </deliverables>

  <andrew_direct_standing>
    2026-08-11 ~1750Z, at this lane's terminal, VERBATIM: "proceed when gates lift" (immediately
    prior turn, same channel: "proceed to the fleet"). SCOPE AS ADDRESSED: this lane's queued,
    gated COT D fleet work -- when a named gate lifts (P2 backfill; A_07 asset-classification dim;
    attribution content; billing plane; RECON-5a/A_06; lots-canonical), this lane PROCEEDS into
    the corresponding gated family builds WITHOUT a fresh GO. Recorded verbatim + broadcast to
    COO/CTO/MSTR same turn per the record+broadcast law; no wider scope adjudicated here.
  </andrew_direct_standing>

  <do_not>
    <item>Do NOT mirror or sync anything between cot and bd. Separate firms, gate + IAM enforced.</item>
    <item>Do NOT start P2/P3/P4/P5, and do NOT re-point the gold DESTINATION.</item>
    <item>Do NOT push to the cot S3 prefix during ~15:00–15:15Z (base's armed deploy).</item>
    <item>Do NOT build Group D or pre-decide its shape — HOLD FOR RULING at your C-completion.</item>
    <item>Do NOT guess a criterion id, and do NOT mint bare UNCOMPUTABLE.</item>
    <item>⚠ Do NOT let an EXEMPLAR stand in for the population. ~A treated an exemplar overlay as THE overlay and the program's central control went unexercised for 11 minutes with the exemplar's own row passing GREEN. If a check has a population, run it over the population and print the denominator.</item>
    <item>Do NOT admit anything from the quality partition's DISCARD side — EXTRACT-side only.</item>
    <item>Do NOT hold work on a finding, and do NOT manufacture an approval step. No gate exists on this lane beyond what is named here.</item>
  </do_not>
</task_order>
