<task_order>
  <metadata>
    <id>TRSB_PATHFIX.TO-1.ae-api-gateway-route-fix</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-27</date>
    <status>complete</status><!-- Verified 2026-04-29: all 12 /api/general/trades/* routes present with CUSTOM+naqxlm. Tag trade-pipeline-v1.6.0 already applied. Work executed in prior AE session; TO status was stale. -->
    <project_code>TRSB_PATHFIX</project_code>
    <wave>W1 — USER-FACING UNBLOCK (same-session)</wave>
    <prd_ref>docs/architecture/TRSB_PATHFIX_PRD.md §3 W1 (2026-04-27)</prd_ref>
    <effort>30-60 min</effort>
    <gates_on>None — ship now</gates_on>
    <gates_for>TRSB_PATHFIX.TO-2 + TO-3 (W2/W3 can ship after W1)</gates_for>
    <tag>trade-pipeline-v1.6.0</tag>
  </metadata>

  <objective>
    Add 12 API Gateway routes under /api/general/trades/* to HTTP API 7k3ed8px20.
    The portal hard-codes /api/general/trades/* (16 call sites in
    portal/src/api/endpoints/trade-submission.ts:192-414). That prefix hits CloudFront
    behavior /api/general/trades/* → API GW 7k3ed8px20, but the API GW has NO routes under
    that prefix — all trade routes live at /api/public/trades/*. Every trade UI call returns
    404 → CF's 404→/index.html mask → client gets HTML → JSON.parse crash
    ("Unexpected token '<'"). All four tabs (Submit, Approvals, Execution, History) broken.
  </objective>

  <compiler_tools_mandate>
    <phase_1_before_write>
      - aws apigatewayv2 get-routes --api-id 7k3ed8px20 (capture full route list pre-change)
      - aws apigatewayv2 get-integrations --api-id 7k3ed8px20 (confirm integration IDs:
        ehdnz7g=trade-submission-handler, mvrx5ci=trade-identifier-cache,
        x3p4wrq=trade-dashboard-api, xkuchu9=trade-workflow-handler)
      - aws apigatewayv2 get-authorizer --api-id 7k3ed8px20 --authorizer-id naqxlm
        (confirm JWT authorizer healthy — same one used by /api/scoped/*)
      - comp-routes behaviors (verify CF behavior /api/general/trades/* is unchanged before
        and after — no CF edits in this TO)
    </phase_1_before_write>
    <phase_2_before_tag>
      - aws apigatewayv2 get-routes --api-id 7k3ed8px20 | grep 'general/trades'
        (expect 12 new routes, ALL with AuthorizationType: CUSTOM, AuthorizerId: naqxlm)
      - aws lambda get-policy --function-name trade-submission-handler (verify new
        aws_lambda_permission arn:aws:execute-api source-arn covers /api/general/trades/*)
      - Same check for trade-workflow-handler, trade-dashboard-api, trade-identifier-cache
      - aws apigatewayv2 get-stage --api-id 7k3ed8px20 --stage-name '$default'
        (verify last-deployed timestamp is post-route-add)
    </phase_2_before_tag>
    <phase_3_after_tag>
      - Browser smoke: Submit tab POST /api/general/trades/submit returns 200 + JSON
        {submission_id: ...}; submission appears in DDB opal-trade-submissions;
        renders in Approvals tab.
      - CloudWatch: trade-submission-handler invocation count > 0 with 200 on
        /api/general/trades/submit in past 5 min.
      - comp-routes behaviors (same baseline as phase 1 — no change expected)
      - Append to org/compiler-tools-log.md
    </phase_3_after_tag>
  </compiler_tools_mandate>

  <scope>
    Add 12 routes to API GW 7k3ed8px20 via AWS CLI (Terraform for this API GW is out of
    scope until TRSB_TFIMPT.W3 ships shared-infra/apigateway-portal/ import). Document
    every create-route invocation in session log so they can be replayed into TF later.

    ROUTES TO ADD (all with AuthorizationType=CUSTOM, AuthorizerId=naqxlm):

    Integration ehdnz7g (trade-submission-handler):
      POST /api/general/trades/submit

    Integration xkuchu9 (trade-workflow-handler):
      POST /api/general/trades/workflow

    Integration x3p4wrq (trade-dashboard-api):
      GET  /api/general/trades/users
      GET  /api/general/trades/submissions
      GET  /api/general/trades/submissions/pending
      GET  /api/general/trades/submissions/by-status
      GET  /api/general/trades/submissions/by-initiator
      GET  /api/general/trades/submissions/{id}
      GET  /api/general/trades/submissions/{id}/excel
      GET  /api/general/trades/submissions/by-approver  ← NEW (no /api/public equivalent;
           dashboard_api.py:56-57 already routes /submissions/by-approver)

    Integration mvrx5ci (trade-identifier-cache):
      GET  /api/general/trades/identifiers/search
      POST /api/general/trades/identifiers/batch

    LAMBDA PERMISSIONS: for each route add aws_lambda_permission with
    SourceArn = arn:aws:execute-api:{region}:{account}:7k3ed8px20/*/*/api/general/trades/*
    covering each of the 4 trade Lambda functions.

    IMPORTANT — DO NOT:
    - Change CloudFront (behavior /api/general/trades/* already correct)
    - Change portal frontend (call sites are correct, the drift was API GW side)
    - Change any existing /api/public/trades/* routes (leave them as-is; may have consumers)
    - Set AuthorizationType: NONE on any new route (current /api/public/trades/* are NONE —
      do not propagate that defense gap; all new routes must be CUSTOM+naqxlm)
    - Terraform apply anything in this wave (pre-TF state; AWS CLI only per PRD §3)

    LAMBDA CODE: No changes needed. trade-dashboard-api routes by path substring
    (dashboard_api.py:52-77) — the new /api/general/ prefix will hit the same handlers.
  </scope>

  <acceptance_criteria>
    1. aws apigatewayv2 get-routes --api-id 7k3ed8px20 returns 12 new routes under
       /api/general/trades/*, all with AuthorizationType: CUSTOM, AuthorizerId: naqxlm.
    2. Browser: Submit tab POST returns 200 + JSON (no HTML response, no JSON.parse error).
       New submission appears in DDB opal-trade-submissions + renders in Approvals tab.
    3. All 4 tabs (Submit, Approvals, Execution, History) load without JSON.parse errors.
    4. aws lambda get-policy on all 4 trade Lambdas shows source-arn covering new routes.
    5. comp-routes behaviors output identical before and after (no CF change).
    6. Session log documents exact aws apigatewayv2 create-route invocations for TF replay.
    7. trade-pipeline-v1.6.0 tag applied after clean smoke test.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT modify CloudFront. The behavior /api/general/trades/* already points to
    API GW 7k3ed8px20 correctly — changing it is high blast radius.</rule>
    <rule>Do NOT modify portal frontend. The /api/general/trades/* call sites are correct.</rule>
    <rule>Do NOT touch /api/public/trades/* routes. Leave them; may have consumers.</rule>
    <rule>Do NOT use AuthorizationType: NONE. All new routes must be CUSTOM+naqxlm.</rule>
    <rule>Do NOT run terraform apply in W1. Document CLI invocations for future TF replay.</rule>
    <rule>Do NOT touch Lambda code in W1. Routing by path-substring already works.</rule>
    <rule>Do NOT ship W2/W3 before W1 smoke test passes.</rule>
  </do_not>

  <deliverables>
    <deliverable type="infrastructure">12 new API GW routes under /api/general/trades/* on
    7k3ed8px20, all CUSTOM+naqxlm, Lambda permissions updated</deliverable>
    <deliverable type="document">Session log with exact create-route CLI invocations + smoke
    test evidence (CloudWatch + browser screenshots)</deliverable>
    <deliverable type="tag">trade-pipeline-v1.6.0</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1-AC5 outputs
    + routes list + CloudWatch trace</deliverable>
  </deliverables>
</task_order>
