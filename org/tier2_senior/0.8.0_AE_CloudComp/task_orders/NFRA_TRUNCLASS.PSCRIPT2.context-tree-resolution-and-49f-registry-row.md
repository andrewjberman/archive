<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-pscript2-context-resolution</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE_CloudComp</issued_to>
    <date>2026-08-20</date>
    <status>complete</status>
    <!-- COMPLETE 2026-08-20: both defects fixed @52a063f50a + proof @96df8b1b5f rc=0
         (re-validated at issuer seat); CTO gate CLOSED 63302 with the repro flip
         independently re-run at their seat and BOTH refusal limbs exercised. The routed
         "calling-context-dependent" framing SUPERSEDED on the record by the assignee's
         grounding: first-match vs longest-prefix in resolve_pipeline_from_arg :109-114.
         GO condition (FIX12 close) was already met at issuance -- assignee's execute-now
         read was correct. First dispatched work under the @2804811386 engine-home
         enumeration: zero overrides. Flip by issuer 2.0.0_SA_COO on the gate close. -->

    <project_code>NFRA_TRUNCLASS</project_code>
  </metadata>

  <objective>
    Two comp-pipescript coverage defects surfaced by DS~B's R14-T1FIX deploy (63274,
    banked-not-chased; classified at CTO 63279 + CVO 63284): (1) `deployed` resolves its
    TREE from CALLING CONTEXT -- standalone on chain_49f_entrypoint.py it sweeps the mdpf
    tree and matches 0 (a clean false-ABSENT) while the SAME invocation inside safe-deploy
    verifies the advi _code/ home; (2) `io` has NO registry row for the 49f chain (bd-gold
    IDs only). A context-dependent tree resolution in a verification instrument is a
    false-ABSENT generator of exactly the class your census hunts; a comp-tool coverage
    gap is a DEFECT, not an inconvenience (standing Andrew law).
  </objective>

  <context>
    Reproduction, from the reporter: `comp-pipescript deployed
    data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py` standalone -> mdpf sweep,
    0 matches; identical invocation inside safe-deploy -> verifies
    s3://opal-data-49financial/_code/chain_49f_entrypoint.py correctly. Ground the MECHANISM
    before fixing (Rule 22): find where the tree/firm resolution diverges between the two
    calling contexts -- do not patch the symptom site. The fix should make an ABSENCE
    verdict carry its searched-tree denominator (the absence law), whatever else changes.
    Rule 24 note: if the registry-row addition enumerates values on any axis, the
    four-postulate test binds.
  </context>

  <compiler_tools_mandate>
    Phase 1: reproduce BOTH calling contexts, print each context's resolved tree + denominator.
    Phase 2: regression pair -- standalone and in-harness invocations return the SAME verdict
    on the same file; a fixture proving a wrong-tree call now names its tree instead of
    reporting a bare 0.
    Phase 3: io row exercised (comp-pipescript io chain_49f_entrypoint --pipeline &lt;tree&gt;
    returns rows, not a registry miss); census scanner re-run over touched files = 0 new
    S1-S5 hits.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: org/modules/graph/*.py (your NEW enumerated lane @2804811386 -- first
      dispatched work under it; no override needed)
      required_action: not interleaved with any other open comp-plane commit of yours.
  </cross_domain_coordination>

  <acceptance_criteria>
    P1  Mechanism grounded and named (file:line @ commit) for the context-dependent tree
        resolution; fix makes standalone == in-harness on the same input.
    P2  Every ABSENT verdict from `deployed` carries its searched-tree denominator.
    P3  io registry row for the 49f chain landed; exercised with rows returned.
    P4  Regression + census re-scan clean (0 new S1-S5); proof instance VALID rc=0
        positional P1,P2,P3,P4.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>P1,P2,P3,P4</expected_criteria>
    <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_TRUNCLASS.PSCRIPT2_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Not urgent -- after FIX12, same plane, CTO gates. Surprise channel: one line to COO.</requirement>
  </requirements>
</task_order>
