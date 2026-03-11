```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-apiscp-007-dt-router-v7</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>ADVI_APISCP-007</thread_serial>
  </metadata>

  <objective>
    Deploy shared-advisor-router v7. Opal Capital employees have firmId='opal-capital' in
    their JWT (after AE runs migration 004). The router currently tries to route them to
    opal-data-opal-capital (which does not exist) and returns 403. Fix: when X-Firm-Id is
    'opal-capital', read the ?firm= query string parameter as the selected partner firm and
    route to opal-data-{firm}. This decouples the Opal access gate (firmId=opal-capital)
    from the firm selection (picked by the user in the portal dropdown).
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda-edge/shared-advisor-router/index.mjs</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      After the existing X-Firm-Id extraction block, add an Opal bypass check:

      if (firmId === 'opal-capital') {
        const params = new URLSearchParams(request.querystring || '');
        const selectedFirm = params.get('firm');
        if (!selectedFirm) {
          return {
            status: '400',
            statusDescription: 'Bad Request',
            headers: { 'content-type': [{ key: 'Content-Type', value: 'text/plain' }] },
            body: 'Opal user must supply ?firm= query param',
          };
        }
        firmId = selectedFirm;
        console.log('Opal routing: selectedFirm=' + selectedFirm + ' uri=' + request.uri);
      }

      This block replaces the routing firmId for Opal users only. All downstream logic
      (URI rewrite, bucket construction, domainName mutation) runs unchanged with the
      selected firmId.
    </requirement>
    <requirement id="2">
      The existing missing-firm 403 guard fires for all non-Opal cases where X-Firm-Id
      is empty or missing. Do NOT remove it. Execution order must be:
        1. OPTIONS early-return (existing)
        2. Extract X-Firm-Id (existing)
        3. If firmId === 'opal-capital': read ?firm= param, set firmId = selectedFirm (NEW)
        4. if (!firmId): return 403 (existing — fires if X-Firm-Id empty AND not opal)
        5. URI rewrite (existing)
        6. Bucket routing (existing)
    </requirement>
    <requirement id="3">
      Update the v-comment block at the top of the file with:
        v7: Opal Capital firm selection — when X-Firm-Id is 'opal-capital', read ?firm=
            query param as the routing target. Decouples Opal access gate from firm selection.
    </requirement>
    <requirement id="4">
      Deploy: zip, publish new Lambda version, update CloudFront behavior to the new
      version ARN, invalidate /api/scoped/advisor-intelligence/*, wait for Deployed status.
    </requirement>
    <requirement id="5">
      Tag: git tag shared-advisor-router-v7 on the commit. Push with --follow-tags.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      curl with X-Firm-Id: opal-capital and ?firm=bd (valid Opal user simulation) returns
      HTTP 200 application/json with firm_id: bd in body from opal-data-bd.
    </criterion>
    <criterion id="2">
      curl with X-Firm-Id: opal-capital and NO ?firm= param returns HTTP 400
      "Opal user must supply ?firm= query param".
    </criterion>
    <criterion id="3">
      curl with X-Firm-Id: bd (partner user) and ?firm=someotherfirm returns HTTP 200
      from opal-data-bd — the ?firm= param is completely ignored for partner users.
    </criterion>
    <criterion id="4">
      OPTIONS preflight still returns 204 with CORS headers (unchanged from v6).
    </criterion>
    <criterion id="5">
      git tag shared-advisor-router-v7 exists and is pushed.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      The opal bypass block must be INSIDE a strict equality check: firmId === 'opal-capital'.
      Do not use a loose check or 'includes'. A partner whose firmId happens to contain
      'opal' must not be affected.
    </constraint>
    <constraint>
      Do NOT allow ?firm= to override routing for partner users (firmId !== 'opal-capital').
      Security: a partner cannot escalate their access by sending ?firm=someotherfirm.
    </constraint>
    <constraint>
      No emoji in log statements. Use plain ASCII.
    </constraint>
    <constraint>
      Lambda version accounting: current live version is :5 (v6 code). The new publish
      will be :6 (v7 code). Confirm with aws lambda list-versions-by-function first.
    </constraint>
    <constraint>
      Dependency on AE CloudOps ADVI_APISCP.007 (DynamoDB patch) for real Opal users to
      have the correct firmId in their JWT. Router v7 can be deployed independently —
      the opal-capital check is inert until JWTs carry that value.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="ADVI_APISCP.007.opal-dynamo-patch-and-cf-cache"
      status="pending"/>
    <!-- DT can implement and deploy now. AE patch is needed for real Opal users to have
         firmId='opal-capital' in their JWT. E2E verification requires AE to complete first. -->
  </dependencies>

  <deliverables>
    <deliverable type="commit">
      shared-advisor-router v7 deployed. Lambda :6 live on CloudFront behavior.
      Tag shared-advisor-router-v7 pushed. Session log in DT logs folder.
    </deliverable>
  </deliverables>
</task_order>
```
