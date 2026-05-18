<task_order>
  <metadata>
    <id>TRSB_LEDGER.010a</id>
    <slug>ae-remove-public-workflow-route</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 -- P0 EXPEDITE. INTERRUPT TO-1 to land this, then resume TO-1. Authored on the CTO~B architecture ruling 2026-05-18 (TRSB_LEDGER public-route exposure). Does NOT wait behind the TO-1 -> TO-2 serial queue.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P0 -- EXPEDITE, same-hour. A live unauthenticated approve/reject/EXECUTE path on a financial trade system. Indefensible; no legacy surface ever needs unauthenticated *workflow*.</priority>
    <sla>Same-hour. Small isolated routes.tf delete + terraform apply.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md -- §9 "Legacy unauthenticated trade surface" (CTO~B amending to v0.2).</prd>
    <finding>TO-0 probe brief docs/briefs/trsb-ledger-to0-identity-seeding-probe-20260518.md §3 -- the /api/public/trades/* NONE-auth route family.</finding>
    <ruling>CTO~B 2026-05-18: there is NO legitimate unauthenticated trade surface. TIER 0 -- remove POST /api/public/trades/workflow NOW, expedited, ahead of the serial queue. The rest of the family + the legacy opal-trade-form-ui distribution = TRSB_LEDGER.010 (Tier 1, same-day, Andrew-supersession-gated).</ruling>
  </references>

  <objective>
    Remove the `POST /api/public/trades/workflow` route -- the unauthenticated (`authorization_type = NONE`) route that reaches `trade-workflow-handler` and lets any caller submit / approve / reject / EXECUTE a trade with no authentication. This is the single most severe item in the TRSB_LEDGER finding set; it ships ahead of everything else.
  </objective>

  <context>
    TO-0 found that `infra/aws/terraform/shared-infra/apigateway-portal/routes.tf` defines a parallel `/api/public/trades/*` route family with `authorization_type = NONE`, wired to the SAME Lambda integrations as the authenticated `/api/general/trades/*` twins. `POST /api/public/trades/workflow` points at the same integration (`i_xkuchu9`) as `POST /api/general/trades/workflow` -- so `trade-workflow-handler` (approve/reject/execute) is reachable with no auth.

    CTO~B ruling: the `workflow` route goes NOW, regardless of the legacy `opal-trade-form-ui` form's fate -- a standalone submission form would only ever POST `submit` + GET `identifiers`; it never needs `workflow`. The remaining public routes + the legacy form retirement are TRSB_LEDGER.010 (gated on an Andrew supersession confirm); this TO is NOT gated on that.

    CRITICAL: the integration `i_xkuchu9` is SHARED with the authenticated `/api/general/trades/workflow` route. This TO removes ONLY the public ROUTE resource -- it MUST NOT delete or alter the shared integration, or the authenticated route breaks.
  </context>

  <scope>
    <step>Phase 1 -- Direct read `infra/aws/terraform/shared-infra/apigateway-portal/routes.tf`. Identify the `aws_apigatewayv2_route` resource for `POST /api/public/trades/workflow`. Confirm its integration target is shared with the `/api/general/trades/workflow` route (do not touch the integration).</step>
    <step>Phase 2 -- Remove ONLY the `POST /api/public/trades/workflow` route resource from routes.tf. Leave the shared integration and the authenticated `/api/general/trades/workflow` route intact. Leave the other `/api/public/trades/*` routes for TRSB_LEDGER.010.</step>
    <step>Phase 3 -- terraform plan: must show exactly one route resource destroyed, nothing else. terraform apply. Commit per CLAUDE.md Rules 1-6 + tag. Smoke: `POST /api/public/trades/workflow` returns 404/403 (route gone); `POST /api/general/trades/workflow` still works (authenticated path intact).</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read: infra/aws/terraform/shared-infra/apigateway-portal/routes.tf -- the POST /api/public/trades/workflow route + its integration ref</run>
        <expect>The public workflow route is a distinct `aws_apigatewayv2_route` whose integration target is the SAME integration id used by the /api/general/trades/workflow route. comp-routes N/A (trade pipeline uninstrumented, PRD §5).</expect>
        <if_mismatch>If the public route has its OWN dedicated integration (not shared), remove that integration too -- but verify first; do not delete a shared integration.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/terraform.exe plan</run>
        <expect>Exactly one resource destroyed: the POST /api/public/trades/workflow route. No integration destroyed (it is shared). No other route, no Lambda, no other resource touched.</expect>
        <if_mismatch>If the plan destroys an integration or any /api/general/ route, STOP -- do not apply. The shared integration must survive.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Smoke: curl POST /api/public/trades/workflow ; curl POST /api/general/trades/workflow (authenticated)</run>
        <expect>The public route returns 404/403 (gone). The authenticated /api/general/trades/workflow route still resolves and reaches the handler.</expect>
        <if_mismatch>If the authenticated route broke, the shared integration was disturbed -- roll back and re-isolate the change.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Route-removal only -- no data, no Lambda source, no S3, no schema change. Removes an attack surface; touches no stored data.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/terraform/shared-infra/apigateway-portal/routes.tf
    also_in_to: TRSB_LEDGER.010 (removes the REMAINING /api/public/trades/* routes from the same file)
    last_write_owner: 0.7.0_AE_CloudOps owns both 010a and 010. 010a lands first (P0); 010 edits the same file afterward. No cross-agent contention.
    required_action: Land 010a, then resume TO-1. TO-10 (the rest) follows once Andrew confirms legacy-form supersession.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The `POST /api/public/trades/workflow` route resource is removed from routes.tf. The shared integration and the authenticated `/api/general/trades/workflow` route are intact.</ac>
    <ac id="AC2">terraform plan shows exactly one route destroyed and nothing else; terraform apply succeeds with a 0-diff-after plan.</ac>
    <ac id="AC3">Smoke: `POST /api/public/trades/workflow` no longer resolves; `POST /api/general/trades/workflow` still works.</ac>
    <ac id="AC4">Deployed via terraform apply; pipeline git tag applied. No emoji. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B (CC 1.0.0_SA_CTO~B -- CTO~B asked to be flagged on this apply).</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/terraform/shared-infra/apigateway-portal/routes.tf</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">routes.tf -- POST /api/public/trades/workflow route removed, deployed via terraform apply, tag applied.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B, CC 1.0.0_SA_CTO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not delete the shared integration -- only the public ROUTE resource. The authenticated /api/general/trades/workflow route depends on that integration.</rule>
    <rule>Do not remove the other /api/public/trades/* routes here -- that is TRSB_LEDGER.010. This TO is scoped to the workflow route ONLY so it can ship same-hour.</rule>
    <rule>Do not deploy outside Terraform (CLAUDE.md Rule 1).</rule>
  </do_not>
</task_order>
