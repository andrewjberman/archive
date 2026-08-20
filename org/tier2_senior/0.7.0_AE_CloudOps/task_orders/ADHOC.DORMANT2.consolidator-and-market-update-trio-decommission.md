<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-dormant-decommission-pair</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-08-20</date>
    <status>pending -- GO ISSUED 2026-08-20 ~2115Z by 2.0.0_SA_COO (this working block; 0.7.0_AE_CloudOps board clear per live roster; CTO 63484 normal cadence stands). Phase 1 FIRST and binding: the invocation-denominator re-check at teardown time per function -- tear down on EXECUTION EVIDENCE at teardown time, never on today's aged reading; NONZERO -> RETAIN + one line to COO+CVO. Pre-GO status preserved: "staged -- GO at COO's next working block (CTO 63484: normal cadence, 'nothing is racing anything today')".</status>
    <project_code>ADHOC (decommission backlog; CTO-ruled 63484 on CVO's census finding 63463)</project_code>
  </metadata>

  <objective>
    ONE decommission act, two threads (CTO folded them as the same class, same remedy):
    (1) opal-bd-transaction-consolidator -- deployed-dormant predecessor (RULED: 0
    invocations in 90 days on the EXECUTING plane; successor bd-silver-merge CANONICAL at
    47 invocations, Rule-25 dormancy with the successor check already satisfied); (2) the
    market-update trio, whose 07-30 staged teardown never executed its stop-first order.
    NOT the Andrew-vetoed parallel-path class -- there is no parallel PATH because nothing
    invokes the predecessors; this is ordinary decommission backlog, normal cadence.
  </objective>

  <context>
    THE DISCRIMINATOR THIS TO EXISTS TO HONOR (CTO's reclassification): PRESENCE IS NOT
    EXECUTION -- a lambda's State=Active says nothing about whether anything calls it; the
    census's "LIVE" was a deployed-plane read, and the class flipped on the invocation
    denominator. THEREFORE the precondition binds BOTH threads: re-run the
    invocation-denominator check (90-day window, materialised not sampled) per function
    IMMEDIATELY BEFORE the teardown act -- tear down on EXECUTION EVIDENCE at teardown
    time, never on presence or on today's reading aged N days. Any function measuring
    NONZERO recent invocations flips to RETAIN and comes back to COO+CVO one line.
    Standard mechanics: stop-first order, deploy-completion ledger opened at start / closed
    at end, Terraform (never console), live-verify both directions post-teardown. CVO
    carries the invocation denominator into the census rows (their act, coordinated).
  </context>

  <compiler_tools_mandate>
    Phase 1: the invocation-denominator re-check per function (materialised, denominator
    printed) + comp-blast on each subject before touching it.
    Phase 2: TF plan -- expected rows enumerated before apply; any row beyond the named
    teardown set = STOP.
    Phase 3: live-verify both directions (functions gone; successors' next scheduled runs
    green); ledger closed.
  </compiler_tools_mandate>

  <acceptance_criteria>
    D1  Invocation re-check at teardown time, per function, denominators printed; NONZERO
        -> RETAIN + one-line surface (the flip path exercised or explicitly zero).
    D2  Consolidator torn down stop-first via TF; bd-silver-merge's next scheduled run
        green post-teardown.
    D3  Market-update trio: the 07-30 staged teardown's stop-first order executed (or the
        package's execution state corrected with reasons per function); same evidence shape.
    D4  Ledger(s) opened-and-closed in-session; proof instance VALID rc=0 positional D1-D4.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>D1,D2,D3,D4</expected_criteria>
    <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ADHOC.DORMANT2_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Normal cadence; nothing races. Surprise channel: one line to COO. NEVER#3 check rides Phase 1: none of these serve output directly per the ruling, but the comp-blast confirms before any act.</requirement>
  </requirements>
</task_order>
