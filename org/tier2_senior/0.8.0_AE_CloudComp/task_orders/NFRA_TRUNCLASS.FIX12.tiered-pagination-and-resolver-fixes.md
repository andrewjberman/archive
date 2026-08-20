<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-trunclass-fix12</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE_CloudComp</issued_to>
    <date>2026-08-20</date>
    <status>pending</status>
    <project_code>NFRA_TRUNCLASS</project_code>
  </metadata>

  <objective>
    Fix the 12 CONFIRMED truncation-class defects from your own SWEEP census
    (@e141eb5f30, proof @05f095148c; my routing cut per the census's "routing is your
    cut" + CTO's mandate-owner priority signal 63150). Two phases, priority-ordered:
    PHASE A = the three Tier-1 verdict-feeding guards that FAIL GREEN + the Tier-3
    first-match-wins resolver (can fire today); PHASE B = the eight Tier-2
    comp_aws_cli absent-edge sites. QUEUE POSITION: behind your two committed items
    (W15-GRAIN3 landing, then instance-3 content-hash + --help guard @6ae67e724f
    pre-gate) -- confirmed by CTO 63150. Gate: 1.0.0_SA_CTO (comp-adversary/comp-plane
    mandate owner).
  </objective>

  <context>
    Source of truth for every row: your census dataset
    org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_TRUNCLASS_SWEEP_CENSUS_20260820.json
    @e141eb5f30 (verified on disk at my seat, 223,592 bytes, commit subject matching).

    THE 12, tiered (census TRC-3):
    - Tier-1 (truncation manufactures a CLEAN PASS): comp-firmsep-sweep.py:73
      (list-roles --max-items 1000, token dropped; live margin 788 today -- CTO: "the
      margin is the fuse, not a comfort", and firm-separation is NEVER-rule-adjacent);
      comp-deadgrant.py:206 (list-secrets 500-cap; own-doc universe 78);
      clobber_scan.py:182 (list_object_versions unpaginated -- a clobber past 1000
      versions reads as none).
    - Tier-3 (wrong artifact, CONFIRMED-MEDIUM, can fire today):
      vectorize_audit_cli.py:23 -- dotted script_id stem-glob runs BEFORE the full-id
      glob, matches[0] first-match-wins -> audit verdict about a SIBLING script.
    - Tier-2 (estate-census absent-edge = the deletion-warrant shape):
      comp_aws_cli.py sites 460/472/482/531/839/1405/1454/1632 -- SNS/SQS/CloudFront/
      ECS/ESM single-page list_* with no local token walk.

    EXPLICITLY OUT OF SCOPE: surface_check_cli.py:846 is RETIRED-DEAD -- classified,
    not a fix target, NOT a deletion warrant (census + CTO concur). Do not touch it.

    THE REMEDY LAW (CLAUDE.md retrieval-control): materialise the full list (auto-
    paginate / explicit token walk) and count client-side; a count you did not paginate
    is a page size wearing a total's clothing. --no-paginate is the hazard, not the
    remedy. Every fixed read prints its DENOMINATOR beside its answer.

    RULE-24 LAYER DECLARATION for this TO's criterion set (per today's widening): the
    declared layer is the census's TRC-3 CONFIRMED set, 12 rows exactly; F1-F4 cover
    3+1, F5 covers 8 (3+1+8=12, exhaustive); F6 is a property over the same 12; F7-F8
    are verification. The one non-member (RETIRED-DEAD) is excluded with its reason
    above.
  </context>

  <compiler_tools_mandate>
    Phase 1 -- before writing:
      <run>Re-read your own census rows for the 12 (final_class + why + wrong_answer_look) and confirm each cited line still matches at HEAD</run>
      <expect>12/12 line-cites current; any drift = re-derive the site before editing</expect>
      <if_mismatch>A moved line means an intervening edit -- diff the file history before fixing, so the fix lands on the live shape.</if_mismatch>

    Phase 2 -- before committing:
      <run>Your census scanner --fixture-check + a re-scan of every TOUCHED file</run>
      <expect>Known specimens still flag (dot-split->S1, grep -c->S5); 0 NEW S1-S5 hits introduced by the fixes</expect>
      <if_mismatch>A new hit in your own fix = the class propagating through its own remedy -- fix before commit.</if_mismatch>

    Phase 3 -- after committing:
      <run>One live exercised read per fixed tool (e.g. comp-firmsep-sweep against the real 212-role estate) with the denominator printed</run>
      <expect>Full-universe counts with frames (e.g. "212 roles of 212 enumerated, 1 page-boundary crossed synthetically in test"), rc taken without a pipe</expect>
      <if_mismatch>A count without its frame is the defect this TO exists to kill -- do not close on it.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: .tools/comp-* + org/modules/graph/*.py (the comp plane)
      required_action: CTO gates as mandate owner; your instance-3 content-hash +
      --help guard commit rides the SAME files' plane -- land that first per the
      confirmed queue order so the two changes do not interleave.
  </cross_domain_coordination>

  <acceptance_criteria>
    F1  comp-firmsep-sweep.py:73 -- full token walk / materialised list; a synthetic
        page-boundary test proves the sweep sees item N+1 past a page; denominator
        printed in output.
    F2  comp-deadgrant.py:206 -- same class fix, same evidence shape.
    F3  clobber_scan.py:182 -- list_object_versions paginated; a >1-page synthetic
        fixture (or paginator-mock) proves a deep clobber is seen.
    F4  vectorize_audit_cli.py:23 -- full-id glob resolves BEFORE stem-glob (exact
        match wins); regression case: a dotted script_id beside a stem-sibling
        resolves to the RIGHT file.
    F5  comp_aws_cli.py x8 (460/472/482/531/839/1405/1454/1632) -- one consistent
        pagination pattern across all eight; per-site evidence row in the instance.
    F6  Every fixed call site's output carries its denominator/frame beside the count
        (the retrieval law made mechanical at these 12 sites).
    F7  Regression: census scanner re-run over touched files = 0 new S1-S5 hits;
        fixture-check still flags both known specimens.
    F8  proof-of-spec-check rc=0 (positional ids, rc without a pipe); CTO gate
        acceptance cited in the close.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>F1,F2,F3,F4,F5,F6,F7,F8</expected_criteria>
    <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_TRUNCLASS.FIX12_PROOF_OF_SPEC.json</instance_path>
    <!-- python .tools/proof-of-spec-check.py org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_TRUNCLASS.FIX12_PROOF_OF_SPEC.json F1,F2,F3,F4,F5,F6,F7,F8 -->
  </proof_of_spec>

  <scope>
    <files>
      <file action="modify">.tools/comp-firmsep-sweep.py (or its engine home -- resolve via the census row)</file>
      <file action="modify">comp-deadgrant.py, clobber_scan.py, vectorize_audit_cli.py (engine homes per census rows)</file>
      <file action="modify">org/modules/graph/comp_aws_cli.py (8 sites)</file>
      <file action="reference">org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_TRUNCLASS_SWEEP_CENSUS_20260820.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Phase A (F1-F4) may land as one commit, Phase B (F5) as a second -- or all in one if the diff stays reviewable; CTO's gate call. Never interleave with the instance-3 commit.</requirement>
    <requirement id="2">Surprise channel: any 13th confirmed instance found while fixing = one line to me, classify it, do NOT silently fold it into this TO's scope (the criterion set is layer-exhaustive at 12 by declaration).</requirement>
  </requirements>
</task_order>
