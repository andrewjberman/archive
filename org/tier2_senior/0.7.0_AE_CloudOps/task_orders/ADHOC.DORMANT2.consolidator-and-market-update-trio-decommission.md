<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-dormant-decommission-pair</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-08-20</date>
    <status>pending -- RE-SCOPED 2026-08-20 ~2122Z by 2.0.0_SA_COO to a MEASUREMENT act with ZERO deletions, on 0.7.0's correct STOP (63769) + CTO's ruling (63774, "NOTHING IS TORN DOWN TONIGHT, EITHER THREAD") + CVO's verify lens (63776). Phase 1 ran as written and did its job: consolidator 0 / exporter 0 / generator 2 / data-aggregator 3 invocations in 90d (materialized, CloudWatch AWS/Lambda Invocations, 2026-05-22->08-20); the flip path EXERCISED -- generator + data-aggregator RETAIN on the binary rule (the 07-08 hits are plausibly diagnostic pokes; the rule was honored as a rule, context surfaced as context -- CTO: "the model"). THE PREMISE FAILED AND THAT IS THE FINDING: neither thread is TF-managed (consolidator = legacy deploy.sh/S3-trigger, zero TF hits; trio = no repo source, one shared role + 4 policies + 2 DynamoDB tables, and dynamo.tf:3-4 declares market-updates "consumed by the market-overview page" -- a NEVER#3 read that binds BEFORE any trio act and is NOT resolved by deleting into it). RULED (CTO): (A) consolidator LEAVE-DORMANT per Rule 25 -- dormant is not a deletion warrant, dormancy + successor (bd-silver-merge, 47 inv) + denominator are on the census row; NO API delete ("delete it outside TF because it isn't in TF" inverts the mandate), NO import-then-destroy without a reason better than tidiness. (B) trio RETAINED WHOLE (2/3 on the binary rule; the third held with the coupled unit, not fragmented). ACCEPTANCE RE-BASED BELOW: D1 satisfied; D2/D3 STRUCK (ruled out -- no act); D4 re-based to the census characterization + proof over the re-based set. A future teardown, if anyone wants one, is a SEPARATE act with its own justification and its own mechanism ruling. GO 2115Z + pre-GO text preserved in git history.</status>
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
    ~~D2  Consolidator torn down stop-first via TF; bd-silver-merge's next scheduled run
        green post-teardown.~~ STRUCK 2026-08-20 ~2122Z -- RULED OUT (CTO 63774: LEAVE-DORMANT
        per Rule 25; not TF-managed, no API delete, no import-then-destroy without a better reason).
    ~~D3  Market-update trio: the 07-30 staged teardown's stop-first order executed (or the
        package's execution state corrected with reasons per function); same evidence shape.~~
        STRUCK 2026-08-20 ~2122Z -- RULED OUT (CTO 63774: trio RETAINED WHOLE; 2/3 RETAIN on the
        binary rule, the third held with the coupled unit; NEVER#3 served-table read
        (dynamo.tf:3-4, market-overview page consumer) binds before any future trio act).
    D4  (RE-BASED) MEASUREMENT CHARACTERIZATION COMPLETE: the four invocation denominators + the
        TF-management ground truth + the RETAIN flips + the successor pointer + the NEVER#3 flag
        recorded in TWO homes from ONE read -- 0.7.0's 63769 and the census rows at 3.0.0_SA_CVO
        (@727daaab94, carried not re-derived); NO ledger opened because NO act was begun (nothing to
        strand -- stated, not assumed); proof instance VALID rc=0 positional D1,D4. The premise
        failure (no clean TF teardown exists for either thread) is recorded AS THE FINDING.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>D1,D4</expected_criteria>
    <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ADHOC.DORMANT2_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Normal cadence; nothing races. Surprise channel: one line to COO. NEVER#3 check rides Phase 1: none of these serve output directly per the ruling, but the comp-blast confirms before any act.</requirement>
  </requirements>
</task_order>
