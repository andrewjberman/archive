<task_order>
  <metadata>
    <id>TRSB_LEDGER.000</id>
    <slug>ae-identity-seeding-probe</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO~B decomposition of TRSB_LEDGER PRD v0.1). Phase 0 probe -- sequences FIRST in the AE 0.7.0 serial backend lane. TO-2 hard-gates on this brief's authorizer finding; TO-8 references its seeding finding.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- gates Phase 1 TO-2 and Phase 3 TO-8. Read-only; small.</priority>
    <sla>1d wall -- an investigation brief, not a build.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 6 TO-0; section 3.1 (groups-canonical authority model); section 3.4 (identity binding); section 2.A A5 (client-asserted actor identity hole); section 7 Q5 (identity-enforcement-depth fork).</prd>
  </references>

  <objective>
    Confirm or refute the two architectural assumptions Phase 1 will lock against, before any code is written: (a) §3.4 -- that the trade API Gateway JWT authorizer passes a usable acting-party identity into the Lambda event; (b) §3.1 -- that existing `trade-users` rows carry a populated `groups` list so group-canonical authorization has data to enforce against. Deliverable is a Phase-0 brief; this TO commits no code beyond that brief.
  </objective>

  <context>
    The trade pipeline is uninstrumented in the compiler graph (PRD §5) -- comp-blast/comp-iam/comp-routes return nothing for trade-* Lambdas. This probe is direct AWS-CLI + source read.

    Two assumptions are load-bearing for Phase 1:
    - §3.4 / A5: `workflow_handler.lambda_handler` currently reads `user_email` from the request BODY (line ~100). The API Gateway has a JWT authorizer, but the handler does not cross-check the JWT principal against the body. TO-2 will repoint actor derivation to the authorizer context -- but only if the authorizer actually passes usable identity claims into `event['requestContext']['authorizer']`. This probe establishes exactly what claims are present.
    - §3.1: authorization is being canonicalized on the `trade-users` `groups` list. If existing rows do NOT carry a populated `groups` list, a seeding/backfill step is required before TO-1's group checks can enforce anything.

    Source files for reference read: infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py; infra/aws/terraform/trade-pipeline/apigateway.tf; infra/aws/terraform/trade-pipeline/dynamodb.tf.
  </context>

  <scope>
    <step>Phase 0a -- Authorizer claims. From apigateway.tf identify the JWT authorizer wired to the trade Lambda routes (approve/reject/execute). Determine what claims it passes into `event['requestContext']['authorizer']` -- inspect the authorizer config + any authorizer Lambda source, and if a deployed invocation log is available, capture an actual `requestContext.authorizer` shape. Answer: is a usable acting-party identity (email or stable principal id) present? Yes / No / Partial.</step>
    <step>Phase 0b -- trade-users seeding. `aws dynamodb scan` the `trade-users` table (read-only). Report: live row count; for each row whether `groups` is present and populated; the distinct group values in use; how many rows are in `approvers`, in `executors`, in both, in neither; whether any row has `groups` empty/absent while carrying a non-empty `role`.</step>
    <step>Phase 0c -- Write the Phase-0 brief: docs/briefs/trsb-ledger-to0-identity-seeding-probe-20260518.md. State plainly whether §3.1 and §3.4 hold. If the authorizer does NOT pass usable identity, explicitly flag the §7-Q5 fork (TO-2 forks to an authorizer change vs an accepted-risk deferral) -- COO~B routes that to CTO~B. If any trade-users row lacks a populated `groups` list, specify the seeding/backfill needed before TO-1 can enforce.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read: infra/aws/terraform/trade-pipeline/apigateway.tf (authorizer wiring) + workflow_handler.py lambda_handler (current body-read of user_email)</run>
        <expect>The JWT authorizer is identifiable and the current body-trust of user_email is confirmed at the cited line. comp-blast/comp-iam/comp-routes are NOT modeled for trade-* Lambdas (PRD §5) -- direct read is the sanctioned substitute.</expect>
        <if_mismatch>If the authorizer cannot be identified from apigateway.tf, widen to main.tf + lambdas.tf before concluding; do not guess.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>n/a -- probe deliverable is a brief, no code commit, no AWS surface change.</run>
        <expect>N/A. State so in one line in the session log.</expect>
        <if_mismatch>n/a</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Read-only investigation. No code, no data write, no reprocessing. The `aws dynamodb scan` of trade-users is read-only.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    No file overlap -- TO-0 writes only a brief under docs/briefs/. It READS workflow_handler.py / apigateway.tf / dynamodb.tf which later TOs modify, but reads do not contend. TO-0 must complete before TO-2 (gate) on the same AE 0.7.0 serial lane.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase-0 brief shipped at docs/briefs/trsb-ledger-to0-identity-seeding-probe-20260518.md.</ac>
    <ac id="AC2">The brief answers definitively: does the trade API Gateway JWT authorizer pass a usable acting-party identity into `event['requestContext']['authorizer']`? Yes / No / Partial, with the evidence (authorizer config + claim shape).</ac>
    <ac id="AC3">The brief reports the live trade-users row count and the group distribution (count in approvers / executors / both / neither), and states whether every row carries a populated `groups` list. If any do not, the required seeding/backfill is specified.</ac>
    <ac id="AC4">If the authorizer does not pass usable identity, the §7-Q5 fork is explicitly flagged for COO~B to route to CTO~B.</ac>
    <ac id="AC5">No emoji in any output. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <deliverables>
    <deliverable type="document">docs/briefs/trsb-ledger-to0-identity-seeding-probe-20260518.md -- the Phase-0 brief.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not modify workflow_handler.py, apigateway.tf, dynamodb.tf, or any trade-users row -- this is a read-only probe. The fixes are TO-1/TO-2.</rule>
    <rule>Do not assume the authorizer carries identity -- verify it empirically. The whole point of the probe is to not let TO-2 lock against an unverified assumption.</rule>
  </do_not>
</task_order>
