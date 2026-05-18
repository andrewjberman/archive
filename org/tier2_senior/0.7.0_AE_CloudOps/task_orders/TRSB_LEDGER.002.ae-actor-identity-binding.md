<task_order>
  <metadata>
    <id>TRSB_LEDGER.002</id>
    <slug>ae-actor-identity-binding</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO~B decomposition of TRSB_LEDGER PRD v0.1). Phase 1 -- HARD-GATED on TO-0's authorizer finding. Same AE 0.7.0 serial lane: TO-0 completes first, so the gate is satisfied in-lane. If TO-0's brief finds the authorizer carries NO usable identity, this TO does NOT proceed as written -- escalate to CTO~B per the fork below.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- Pillar A. Closes hole A5 (actor identity is client-asserted).</priority>
    <sla>1d wall (if the authorizer carries identity); re-scope if the fork triggers.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.A A5 (actor identity client-asserted); section 3.4 (identity binding); section 6 TO-2; section 7 Q5 (identity-enforcement-depth fork).</prd>
    <gate>TO-0 Phase-0 brief (docs/briefs/trsb-ledger-to0-identity-seeding-probe-20260518.md) -- the authorizer-claims finding is the input to this TO.</gate>
  </references>

  <objective>
    Derive the acting party for every trade workflow action from the API Gateway JWT authorizer context, not from the request body. Reject any request where the body `user_email` disagrees with the JWT principal. This closes hole A5: today a caller can assert another user's email as the acting party, and since email is the `trade-users` lookup key, a spoofed email yields a spoofed actor record end-to-end.
  </objective>

  <context>
    `workflow_handler.lambda_handler` reads `user_email` from the request body (~line 100) and looks the user up by that email. The API Gateway has a JWT authorizer but the handler never cross-checks the JWT principal against the body. Once TO-1 makes group membership load-bearing, a spoofable actor identity makes the whole authorization model defeatable -- so A5 must close in the same phase as A1.

    Target (§3.4): the handler derives the acting party from `event['requestContext']['authorizer']`. If the body `user_email` is present and disagrees with the JWT principal, reject 403. The body field becomes advisory at most; the JWT principal is authoritative.

    FORK (§7-Q5): this TO is written assuming TO-0 confirms the authorizer passes a usable identity. If TO-0's brief finds it does NOT, do NOT improvise -- STOP and escalate to CTO~B via COO~B. The fork is: (a) an authorizer change to pass identity (larger scope, new TO), or (b) an accepted-risk deferral documented by CTO~B. CTO~B adjudicates; this TO is then re-scoped or re-issued.

    TO-0 FINDING (2026-05-18, brief docs/briefs/trsb-ledger-to0-identity-seeding-probe-20260518.md): the §7-Q5 fork did NOT trigger -- the authorizer passes a verified acting-party identity at `event['requestContext']['authorizer']['lambda']['email']`. Proceed to the standard repoint. TO-0 ALSO surfaced a high-severity route-surface defect: a parallel `/api/public/trades/*` route family (`authorization_type = NONE`) hits the SAME Lambda integrations as the authenticated `/api/general/` twins -- so trade-workflow-handler is reachable UNAUTHENTICATED, arriving with NO `requestContext.authorizer` block. This TO MUST therefore hard-reject any request that arrives without an authorizer context -- the structural handler-side catch for the unauthenticated public twin. The disposition of the `/api/public/trades/*` routes themselves is TRSB_LEDGER.010 (a separate CTO~B-adjudicated TO on the shared-infra apigateway-portal module); this TO's hard-reject stands regardless of TO-10's outcome and is the defense that closes exploitability NOW.

    File: infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py.
  </context>

  <scope>
    <step>Phase 1 -- Read TO-0's brief. If the authorizer carries usable identity: proceed. If NOT: STOP, escalate to CTO~B through COO~B (§7-Q5 fork); do not write code against an unverified authorizer.</step>
    <step>Phase 1 -- In `lambda_handler`, derive the acting party from `event['requestContext']['authorizer']['lambda']['email']` (the claim path confirmed by TO-0). Use that as the authoritative actor for the trade-users lookup and for all downstream actor fields.</step>
    <step>Phase 1 -- HARD-REJECT (403) any request that arrives with NO `event['requestContext']['authorizer']` context. This is the mandatory structural catch for the unauthenticated `/api/public/trades/*` twin (TO-0 finding §3) -- a request with no authorizer context has no verifiable actor and MUST NOT fall back to the body `user_email`. This rejection is non-negotiable and stands regardless of TO-10's route-disposition outcome.</step>
    <step>Phase 1 -- If the request body still carries `user_email` and it disagrees with the JWT principal, return 403 with a specific message ("acting-party identity mismatch"). A matching or absent body field is accepted; a conflicting one is rejected.</step>
    <step>Phase 2 -- Unit coverage: a request whose body `user_email` differs from the JWT principal is rejected 403; a request with a matching body field or no body field resolves the actor from the JWT.</step>
    <step>Phase 3 -- Deploy via terraform apply (CLAUDE.md Rules 1-6). Smoke the deployed Lambda.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Read TO-0 brief docs/briefs/trsb-ledger-to0-identity-seeding-probe-20260518.md -- the authorizer-claims finding</run>
        <expect>The brief states the authorizer passes a usable acting-party identity, and names the exact claim path in `event['requestContext']['authorizer']`.</expect>
        <if_mismatch>If the brief says NO usable identity (or Partial/ambiguous), STOP. Escalate to CTO~B via COO~B per the §7-Q5 fork. Do not proceed.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Direct read: confirm iam.tf unchanged by this TO</run>
        <expect>Zero IAM delta -- identity binding is pure handler logic; comp-iam is N/A (uninstrumented, PRD §5).</expect>
        <if_mismatch>If iam.tf changed, document the grant + rationale in the session log and flag COO~B.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Deployed-Lambda smoke: invoke a workflow action with a body `user_email` that differs from the JWT principal</run>
        <expect>403 "acting-party identity mismatch". A request resolved purely from the JWT (no/matching body field) succeeds.</expect>
        <if_mismatch>If a mismatched body email is still accepted as the actor, the binding is not wired -- do not mark complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Logic change to a Lambda handler -- affects only future invocations. No silver/bronze script, no historical data write. Existing trade rows are unaffected.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py
    also_in_to: TRSB_LEDGER.001, .003, .004, .005
    last_write_owner: single agent -- 0.7.0_AE_CloudOps owns the AE backend serial lane. Execute after TO-1, before TO-3. One commit scope per TO; pull latest before writing.
    required_action: TO-2 follows TO-1 in-lane; no other agent edits workflow_handler.py during this wave.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The acting party for every trade workflow action is derived from `event['requestContext']['authorizer']`, not the request body.</ac>
    <ac id="AC2">A request whose body `user_email` conflicts with the JWT principal is rejected 403 with a specific mismatch message. A matching or absent body field is accepted.</ac>
    <ac id="AC2b">A request that arrives with NO `event['requestContext']['authorizer']` context is hard-rejected 403 -- the handler does not fall back to the body `user_email`. Verified by a smoke against the unauthenticated `/api/public/trades/workflow` route (or a synthetic event with the authorizer block absent).</ac>
    <ac id="AC3">Unit tests cover the mismatch-rejection, the no-authorizer-context rejection, and the JWT-resolved-actor path. Tests pass.</ac>
    <ac id="AC4">Deployed-Lambda smoke: a spoofed-email request returns 403. Deployed via terraform apply (0-diff plan); pipeline tag applied.</ac>
    <ac id="AC5">IF the §7-Q5 fork triggered (authorizer carries no usable identity): no code was written; the escalation to CTO~B via COO~B is documented in the session log, and this TO is marked blocked-pending-rescope rather than complete.</ac>
    <ac id="AC6">No emoji. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py</file>
    <file action="reference">docs/briefs/trsb-ledger-to0-identity-seeding-probe-20260518.md</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">workflow_handler.py JWT-authorizer actor binding, deployed via terraform apply -- OR, if the fork triggered, a documented escalation and no commit.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not write code against the authorizer until TO-0's brief confirms it carries usable identity. The probe-first sequencing is mandatory (PRD R2).</rule>
    <rule>Do not silently fall back to the body `user_email` if the JWT principal is absent -- that re-opens A5. Absent JWT identity is the fork condition, not a fallback.</rule>
    <rule>Do not deploy outside Terraform (CLAUDE.md Rule 1).</rule>
  </do_not>
</task_order>
