# TO MDPF_49F_BUILD.P1 — PHASE 1 SCRIPTS: the 49F gold analytics runner, Groups A–D + parquet writer-format

<task_order>
  <metadata>
    <to_id>MDPF_49F_BUILD.P1.scripts-groups-a-d-parquet</to_id>
    <project>MDPF_49F_BUILD</project>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued>2026-08-11</issued>
    <status>active</status>
    <gate>1.0.0_SA_CTO</gate>
    <verifier>3.0.0_SA_CVO</verifier>
  </metadata>

  <objective>
    Build PHASE 1 (SCRIPTS) of the 49F gold analytics runner — the ARCHETYPE whose SHAPE all future
    firm runners instantiate. Update per the five ratified specs with STAGE-BY-STAGE compile
    verification. Andrew-direct @a9c159f134: "Final ratification granted, decompose the build."
  </objective>

  <context>
    ISSUANCE NOTE, ON THE RECORD: this TO FILE is written AFTER the work began. P1 was dispatched by
    broker message at 081619Z (re-issued 082127Z under the proof-of-spec contract) and B-1 completed
    at 084731Z. The issuer (COO) failed to write the TO file at dispatch — see the register's §4ag
    admission. The file is landed now so the commissioning record exists and B-2..B-5a carry it
    prospectively; B-1's row is recorded as DELIVERED with its actual instance path.

    PHASE ORDER (Andrew-direct @4dbf4a0d7c, SEQUENTIAL — each phase gates the next):
      P1 SCRIPTS -> P2 TIMING -> P3 REPOINTS -> P4 PUBLISHERS -> P5 DECOMMISSION
    THIS TO IS P1 ONLY. P2 (event trigger + clock floor) and P4 (publishers read parquet) are NOT in
    scope and must not be started from this TO.

    SHAPE-TRANSPOSITION DOCTRINE (Andrew-direct @6e180df78e): the 49F runner is the SHAPE — field
    contract + script sequence. Future firms instantiate it by SOURCING FIELDS
    (RAW / MANUFACTURABLE-as-named-computation / ABSENT-with-shape), NEVER by porting code.

    ADMISSION CRITERION, STANDING: EXTRACT-side only. A build admitting anything from the quality
    partition's DISCARD side is a patch by construction, and "no patches" is his word on the archetype.
  </context>

  <compiler_tools_mandate>
    comp-validate per gold script; comp-pipescript deployed for MATCH after any S3 upload.
    NOTE the measured instrument boundary: comp-pipescript deployed EXCLUDES bundle-routed scripts and
    under-reports multi-homed ones without its DENOMINATOR line read — never accept a deploy on MATCH
    alone (it returned MATCH while executing code was 4 days stale, 2026-08-11).
  </compiler_tools_mandate>

  <acceptance_criteria>
    Acceptance is NOT authored here. THE PER-GROUP ACCEPTANCE BATTERIES IN THE RATIFIED SPECS ARE THE
    BAR, cited by spec commit:
      B-1  Group A  @9c294bbf15 + @6fba62393b
      B-2  Group B  @d57bbf7229
      B-3  Group C  @39c41163cd + @f882b91ce2
      B-4  Group D  @1e11389af8   (emitters — SHAPE-FROZEN against the DEPLOYED FE's ACTUAL reads)
      B-5a Andrew requirement: gold output = PARQUET {table}/date={D}  (WRITER-FORMAT half only;
           the DESTINATION portal/gold/{product}/{scope} is P3, NOT this TO)
    Plus, per Andrew @4dbf4a0d7c: STAGE-BY-STAGE compile verification (commit-gate py_compile per
    stage), not a single pass at the end.
    Plus, B-2 only: the B_02 materiality verdict routes MID-BUILD to Andrew + 1.0.0_SA_CTO and MUST
    STATE ITS BASIS EXPLICITLY — the rate-bearing MV numerator and the book denominator each naming
    their valuation source. (This exists because a mixed-basis figure served for months as a single
    number; see the ending_mv finding.)
  </acceptance_criteria>

  <proof_of_spec>
    <!-- ONE INSTANCE PER GROUP. The grammar, not a single path (see the ISSUER DEFECT note below):
         org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_B{n}_GROUP{X}_{YYYYMMDD}.json -->
    <instance_path_grammar>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_B{n}_GROUP{X}_{YYYYMMDD}.json</instance_path_grammar>

    <group id="B-1" status="DELIVERED" instance_path="org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_B1_GROUPA_20260811.json">
      <expected_criteria>A5-ROWCOUNT-A00,A5-A01-F5,A5-A02-DISJOINT,A5-A02-DETERMINISM,A5-A02-MUTANT,A5-A04-GAPCENSUS,A5-A05-RESOLVE,A5-A05-CENSUSKEY,A5-A06-COVERAGE,A5-A06-LOCKSTEP,A5-ALL-PROVENANCE</expected_criteria>
    </group>
    <group id="B-2" status="DELIVERED" instance_path="org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_B2_GROUPB_20260811.json">
      <expected_criteria>B5-B00-ROWCOUNT,B5-B00-IDENTITY,B5-B00-SPOTTIE,B5-B01-MVTIE,B5-B01-FLAGS,B5-B01-NODROPS,B5-B02-DENOMINATORS,B5-B02-RULING,B5-B02-MUTANT,B5-B03-CENSUS,B5-B03-DETERMINISM,B5-B03-MUTANT,B5-ALL-PROVENANCE</expected_criteria>
    </group>
    <group id="B-3" status="DELIVERED" instance_path="org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_B3_GROUPC_20260811.json">
      <expected_criteria>C5-C00-IDENTITY,C5-C00-PAIRDET,C5-C00-ICTRAP,C5-C01-DIFF,C5-C02-IDENTITIES,C5-C02-LINKING,C5-C02-ZERODENOM,C5-C02-GROSSNET,C5-C03-FIELDS,C5-C03-STATUSMUTANT,C5-C04-NINEGRADES,C5-C04-PNLCONTROL,C5-ALL-PROVENANCE</expected_criteria>
      <!-- C5-C04-PNLCONTROL landed UNCOMPUTABLE-with-declaration and is ACCEPTED as such: a month-grain
           P&L identity cannot be computed from a single day BY CONSTRUCTION; it rides the backfill,
           declared not skipped. UNCOMPUTABLE-with-declaration is PRE-AUTHORIZED for B-4/B-5a — an
           impossible row must not force a choice between a faked PASS and a stall. -->
    </group>
    <group id="B-4" status="NOT_YET_MINTED"/>
    <group id="B-5a" status="NOT_YET_MINTED"/>

    <!--
    ISSUER DEFECT, RECORDED IN THE TO ITSELF (2026-08-11, COO): this element originally declared a
    SINGLE <instance_path> (MDPF_49F_BUILD.P1_PROOF_OF_SPEC.json) while the contract delivers ONE
    INSTANCE PER GROUP. That path matched NO landed instance — a completion flip acting on it would
    have found NOTHING, and read the absence as work-not-done. The assignee's filenames were correct
    throughout; the TO was wrong.
    HOW IT SURVIVED: the issuance lint (.tools/git-hooks/to-proof-of-spec-check.sh:29) greps for the
    PRESENCE of a <proof_of_spec element on NEW files. It does not resolve instance_path, does not
    check the id set, and does not re-run on MODIFIED files. IT BINDS ISSUANCE PRESENCE, NEVER
    ISSUANCE CORRECTNESS — so a well-formed element naming a nonexistent path passes it by design.
    HOW IT WAS CAUGHT: not by a gate. The issuer guessed two wrong paths while trying to re-validate
    the assignee's instances, and the NOT-AT-THAT-PATH miss exposed the declaration. A defect found by
    an unrelated stumble is a defect with no detector.
    ADOPTED FABRIC-WIDE (CTO 092331Z) for the INF/COT lanes: {phase}_{firm}_{group}_{date} instance
    paths, and {firm}-{group}-{artifact}-{check} criterion ids declared BEFORE the first mint —
    49F's A5-/B5-/C5- prefixes carry no firm token and would collide across lanes transposing the
    batteries verbatim, while CVO's cert step-zero reads ACROSS instances.
    -->
    <!--
    PROVENANCE OF THE ID SET, STATED BECAUSE IT MATTERS WHO MINTED IT:
    The 11 ids above are GROUP A's battery, ENUMERATED BY THE ASSIGNEE (0.4.0_DS_ClientPlatform,
    084731Z) with their judgment calls stated — §5's A_02 bullet split into three independently-
    checkable rows; the F-5 line promoted from the §1 artifact table because the spec itself names it
    an "acceptance row". The issuer (COO) DECLARED at 082127Z that it had NOT independently enumerated
    the ids and refused to invent id strings it had not read. That gap was closed by the seat holding
    the spec, not by the issuer guessing.

    B-2 / B-3 / B-4 / B-5a: THEIR ID SETS ARE NOT YET MINTED. Each is enumerated from its own battery
    at that row's start, by the same surfaced-not-guessed method, and appended here at next touch (the
    lint binds ISSUANCE; CVO 084xZ ruled retrofitting in-flight TOs is the issuer's call). An id list
    that is WRONG validates structurally and proves the wrong thing — so a row whose battery is
    ambiguous SURFACES rather than guesses.

    THE TWO-LAYER DIVISION covers the issuer's exposure: the validator catches the ASSIGNEE omitting
    against this list; CVO's cert-of-built step-zero catches THIS LIST omitting against the governing
    SPEC. Per-group validation:
      python .tools/proof-of-spec-check.py {instance}.json --expected-criteria {that group's ids}
    -->
  </proof_of_spec>

  <scope>
    <files>
      <file action="modify">data/assets/scripts/gold/runners_49f/ (Groups A–D per the ratified specs)</file>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/MDPF_49F_BUILD.P1_PROOF_OF_SPEC.json</file>
      <file action="reference">the five ratified specs (A/B/C/D/W) at the commits cited above</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">B-1 Group A — DELIVERED @48bbe384f4 (instance VALID, 11 rows, 0 violations, coverage-checked; py_compile 8/8; fixtures 73/73). Recorded, not re-opened.</requirement>
    <requirement id="2">B-2 Group B — including the mid-build materiality routing with BOTH bases stated.</requirement>
    <requirement id="3">B-3 Group C.</requirement>
    <requirement id="4">B-4 Group D emitters — shape-frozen against a CENSUS of the deployed frontend's actual reads, never the docs and never the builder.</requirement>
    <requirement id="5">B-5a gold output = PARQUET {table}/date={D} — writer-format only.</requirement>
    <requirement id="6">Evidence captured AS THE WORK PROCEEDS, not retro-fitted. The contract requires re-runnable invocations, verbatim output and denominators per criterion; an instance assembled afterwards is weaker even when every field is filled, because the evidence was selected knowing the answer.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Groups A–D + parquet writer-format, stage-by-stage compile-verified</deliverable>
    <deliverable type="document">A schema-valid PROOF_OF_SPEC instance per group, passing proof-of-spec-check with --expected-criteria</deliverable>
    <deliverable type="document">Session log with Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <item>Do NOT start P2 (silver-completeness event trigger + clock floor) or P4 (publishers read parquet) from this TO — they are separate phases behind sequential gates.</item>
    <item>Do NOT re-point gold's DESTINATION. B-5a is the writer FORMAT; portal/gold/{product}/{scope} is P3.</item>
    <item>Do NOT admit anything from the quality partition's DISCARD side.</item>
    <item>Do NOT accept a deploy on comp-pipescript MATCH alone — read its DENOMINATOR line.</item>
    <item>Do NOT guess a criterion id. Surface an ambiguous battery instead.</item>
    <item>Do NOT re-cut D_02 or D_04 on the valuation basis — that is a ratified form and the basis ruling sits with Andrew.</item>
  </do_not>
</task_order>
