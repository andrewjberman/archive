<task_order>
  <metadata>
    <id>TRSB_LEDGER.008</id>
    <slug>ae-trade-groups-me-endpoint</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO~B decomposition of TRSB_LEDGER PRD v0.1). Phase 3 (backend half) -- Andrew Q2/Q4 RESOLVED so Phase 3 is unblocked; CTO~B pre-decided the endpoint shape (dedicated endpoint, not a JWT claim), so this TO has no hard architectural gate. Sequenced after TO-5 on the AE 0.7.0 serial backend lane. References TO-0's trade-users seeding finding.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P2 -- Phase 3. Enables TO-8b portal role-aware gating (fixes A4).</priority>
    <sla>1d wall -- a single read endpoint.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.A A4 (portal gates on firm, not role); section 6 TO-8; section 7 Q4 deferred (TO-7 dropped -- Andrew manages trade-users directly).</prd>
    <ruling>CTO~B 2026-05-18: TO-8's surfacing mechanism is a DEDICATED endpoint `/api/general/trades/users/me`, NOT a JWT auth claim. Reasoning: a trade-subsystem claim pollutes the portal-wide auth token; group membership lives in `trade-users` (separate from `opal-users`) and a claim would force the auth Lambda to cross-read it on the hot path; a baked claim is stale 8-12min until token refresh, but Andrew managing the executors list directly (Q4 deferral) needs add/remove to reflect on next page load. A queried endpoint does that; a claim does not.</ruling>
  </references>

  <objective>
    Add a dedicated `/api/general/trades/users/me` endpoint to `trade-dashboard-api` that returns the calling user's `trade-users` record -- specifically their `groups` list -- so the portal can gate the Execution and Approvals tabs on actual group membership instead of firm identity (the A4 fix, completed by TO-8b on the portal side).
  </objective>

  <context>
    A4: `TradeSubmission.tsx` shows the Approvals and Execution tabs to any internal (`claims.firmId === 'opal-capital'`) user -- there is no check that the user is an executor. Every internal user sees the Execute button. Backend enforcement (TO-1) is the real gate, but the FE should not present actions the user cannot take.

    For the portal to gate correctly it must know the caller's trade-groups. Per CTO~B's ruling this is a dedicated endpoint, not an auth claim. `trade-dashboard-api/src/dashboard_api.py` already has a `get_users` handler -- adding a `/users/me` handler that returns the caller's own record is trivial and consistent.

    Identity: the endpoint identifies the caller from the API Gateway JWT authorizer context (consistent with TO-2's actor-identity binding). TO-0's brief reports what the authorizer carries -- reference it. TO-0 also reports whether existing trade-users rows have populated `groups` lists; if a caller's row has no groups, the endpoint returns an empty groups list (the portal then shows no privileged tabs -- correct fail-closed behavior).

    File: infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/dashboard_api.py + apigateway.tf route wiring.
  </context>

  <scope>
    <step>Phase 1 -- Reference TO-0's brief for the authorizer claim path + the trade-users groups-population finding. Direct read dashboard_api.py get_users + apigateway.tf route definitions.</step>
    <step>Phase 2 -- Add a `/api/general/trades/users/me` GET handler to dashboard_api.py: identify the caller from the JWT authorizer context, look up their `trade-users` row, return `{ email, name, groups, role }` (groups is the field the portal needs; role included for display). If the caller has no trade-users row or an empty groups list, return groups as an empty list (fail-closed).</step>
    <step>Phase 2 -- Wire the route in apigateway.tf under the existing trade JWT authorizer. Confirm iam.tf already grants `dynamodb:GetItem/Query` on trade-users (it does -- PRD §2.C).</step>
    <step>Phase 3 -- Deploy via terraform apply (CLAUDE.md Rules 1-6). Smoke the endpoint.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read: dashboard_api.py get_users handler + apigateway.tf trade routes; read TO-0 brief for the authorizer claim path</run>
        <expect>get_users exists and is the consistency template; the trade routes share one JWT authorizer; TO-0 confirms the authorizer claim path for caller identity. comp-routes N/A (uninstrumented, PRD §5).</expect>
        <if_mismatch>If TO-0 found the authorizer carries no usable identity, this endpoint cannot identify the caller -- STOP and flag COO~B; it shares the §7-Q5 fork with TO-2.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Direct read: iam.tf -- dynamodb GetItem/Query grant on trade-users</run>
        <expect>Already granted (PRD §2.C, iam.tf ~line 59). No IAM change. comp-iam N/A (uninstrumented).</expect>
        <if_mismatch>If the grant is absent, STOP and flag COO~B -- an iam.tf change escalates the TO.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Deployed-endpoint smoke: GET /api/general/trades/users/me as an authenticated user</run>
        <expect>200 with the caller's `{ email, name, groups, role }`. The `groups` value matches that user's trade-users row. A user with no trade-users row gets an empty groups list, not a 500.</expect>
        <if_mismatch>If the endpoint returns another user's record or 500s on a missing row, do not mark complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>New read-only endpoint -- no data write, no schema change, no silver/bronze script, no reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/dashboard_api.py; infra/aws/terraform/trade-pipeline/apigateway.tf
    also_in_to: TRSB_LEDGER.005 (dashboard_api.py -- get_by_approver GSI cutover)
    last_write_owner: 0.7.0_AE_CloudOps owns both TO-5 and TO-8 -- same serial lane, TO-8 after TO-5. No cross-agent contention. apigateway.tf is not touched by any other TRSB TO.
    required_action: TO-8 follows TO-5 in-lane; pull latest dashboard_api.py before writing.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">A `/api/general/trades/users/me` GET endpoint exists, wired under the trade JWT authorizer, returning the caller's `{ email, name, groups, role }`.</ac>
    <ac id="AC2">The caller is identified from the JWT authorizer context -- a caller cannot retrieve another user's record.</ac>
    <ac id="AC3">A caller with no trade-users row or an empty groups list gets an empty `groups` list (fail-closed), not an error.</ac>
    <ac id="AC4">Deployed-endpoint smoke passes. Deployed via terraform apply (0-diff plan); pipeline tag applied.</ac>
    <ac id="AC5">No emoji. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B. The endpoint contract (path, response shape) is reported to TO-8b's owner (RD 0.3.2) so the portal can consume it.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/dashboard_api.py</file>
    <file action="modify">infra/aws/terraform/trade-pipeline/apigateway.tf</file>
    <file action="reference">infra/aws/terraform/trade-pipeline/iam.tf</file>
    <file action="reference">docs/briefs/trsb-ledger-to0-identity-seeding-probe-20260518.md</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">dashboard_api.py /users/me endpoint + apigateway.tf route, deployed via terraform apply (0-diff plan), pipeline tag applied.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section + the endpoint contract for TO-8b. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not implement trade-group surfacing as a JWT auth claim -- CTO~B locked the dedicated-endpoint shape. A claim is explicitly rejected.</rule>
    <rule>Do not let the endpoint return a record for any email other than the JWT-authenticated caller.</rule>
    <rule>Do not 500 on a caller with no trade-users row -- fail closed with an empty groups list.</rule>
    <rule>Do not deploy outside Terraform (CLAUDE.md Rule 1).</rule>
  </do_not>
</task_order>
