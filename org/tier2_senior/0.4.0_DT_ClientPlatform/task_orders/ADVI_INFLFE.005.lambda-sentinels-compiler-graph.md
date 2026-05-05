<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLFE.005</id>
    <project>ADVI_INFLFE</project>
    <title>opal-partners-data Lambda response-shape sentinels + compiler graph indexer fix</title>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>pending</status><!-- Fully parallel — no gate on INFLFE.001/002/003. Begin after current AUDIT-001 render sweep + AUDIT-004 AC3 are complete. -->
    <priority>medium</priority>
    <estimated_effort>0.5-1d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/INFLEC_FE_BACKEND_WIRING.md §4 TO-5</ref>
    <ref type="compiler_evidence">comp-iam service opal-partners-data → NOT_INDEXED (AUDIT-001 matrix v4 §Compiler Tools)</ref>
    <ref type="lambda_scope">opal-partners-data Lambda — handles all firmId-routed partner API calls including Inflection L2/L3 paths; NOT bucket-swap (APIGateway-portal path)</ref>
    <ref type="adhc_compil">ADHC_COMPIL backlog item: comp-iam NOT_INDEXED for shared-infra Lambdas — DT Part B cites this</ref>
  </references>

  <context>
    Two independent parts:

    Part A — Lambda response-shape assertions. opal-partners-data Lambda currently has no
    response-shape validation for Inflection-routed calls. When envelope drift occurs (e.g.,
    getPlatinumAdvisorSummary returns an Inflection-specific shape not matching BD contract),
    the drift propagates silently to FE. Add observability-mode assertions that log schema
    mismatches to CloudWatch without failing the request. Promote to enforcement after one
    nightly clean cycle.

    Part B — Compiler graph remediation. comp-iam service opal-partners-data returns NOT_INDEXED.
    This means IAM policy changes to this Lambda are invisible to compiler tooling (comp-iam gaps
    will miss it). Fix the indexer so opal-partners-data + sibling partner Lambdas appear in
    comp-iam queries. This is a discrete ADHC_COMPIL backlog item — file commit citing it.

    Fully parallel to INFLFE.001/002/003. Begin after AUDIT-001 render sweep work completes.
  </context>

  <phase id="0" when="before any code write — scope confirmation">
    <step>
      <run>comp-iam service opal-partners-data</run>
      <expect>NOT_INDEXED (confirming Part B is needed); if it returns a service list, Part B may not be needed — document and skip</expect>
    </step>
    <step>
      <run>comp-routes behaviors | grep partners</run>
      <expect>Lists CloudFront behaviors routing to opal-partners-data; confirms which paths this Lambda handles for Inflection</expect>
    </step>
    <step>
      <run>comp-iam gaps (to understand what the NOT_INDEXED gap actually masks)</run>
      <expect>If opal-partners-data has IAM gaps not visible due to NOT_INDEXED, they surface here</expect>
    </step>
  </phase>

  <phase id="1" when="Part A — Lambda response-shape sentinels">
    <step>
      <action>Identify the Inflection-routed handler paths in opal-partners-data Lambda source. These are the firmId=inflection conditional branches (e.g., getPlatinumAdvisorSummary inflection envelope, getPlatinumClientSummary inflection path post-INFLFE.001 fix).</action>
    </step>
    <step>
      <action>Add assertInflectionEnvelope(response, expectedKeys) call at response exit for Inflection paths. Log mismatch to CloudWatch namespace Opal/InflectionSentinels. Do NOT raise HTTP 5xx — observability-mode only for v1.</action>
    </step>
    <step>
      <action>Document schema in a comment block: expected keys for each Inflection endpoint. This becomes the ground truth for INFLFE.002 FE-side sentinels to reference.</action>
    </step>
  </phase>

  <phase id="2" when="Part B — Compiler graph indexer fix">
    <step>
      <action>Identify why comp-iam service opal-partners-data returns NOT_INDEXED. Likely: the Lambda function name in the compiler graph does not match the actual Lambda name, or it's under a shared-infra module not indexed by comp-pipescript.</action>
    </step>
    <step>
      <action>Add the correct Lambda name entry to the compiler graph config so comp-iam service can resolve it. If this requires touching .comp-graph/ config: file as a single commit citing ADHC_COMPIL backlog item.</action>
    </step>
    <step>
      <run>comp-iam service opal-partners-data (re-run post-fix)</run>
      <expect>Returns service-call list (s3:GetObject, dynamodb:GetItem, etc.) — no longer NOT_INDEXED</expect>
      <if_mismatch>Fix indexer entry before closing</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="before committing Lambda changes">
    <step>
      <run>comp-iam service opal-partners-data (verify post-Part A code changes)</run>
      <expect>Service list includes all calls made by the sentinel code (cloudwatch:PutMetricData if applicable)</expect>
      <if_mismatch>Add missing IAM permission via Terraform (AE 0.7 lane) or flag as IAM gap to COO</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <none>No cross-domain coordination required. Part A modifies Lambda source only (DT app-layer scope). Part B modifies compiler graph config only. Neither touches portal/FE files. IAM Terraform changes (if needed for CloudWatch PutMetricData) go to AE 0.7 lane — flag to COO if surfaced.</none>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">Part A: Inflection-routed opal-partners-data responses have assertion logging at Lambda exit for at least getPlatinumAdvisorSummary + getPlatinumClientSummary paths</criterion>
    <criterion id="AC2">Part A: Assertions fire to CloudWatch Opal/InflectionSentinels namespace; observability-mode only (no request failures)</criterion>
    <criterion id="AC3">Part B: comp-iam service opal-partners-data returns a service list (not NOT_INDEXED) post-fix</criterion>
    <criterion id="AC4">INFLFE.002 DE can reference the Lambda-side sentinel schema doc as the ground truth for FE-side type guards</criterion>
    <criterion id="AC5">RAVC3 to COO: Lambda commit hash (Part A) + compiler graph commit hash (Part B) + comp-iam service output post-Part B + AC1-4 status</criterion>
  </acceptance_criteria>
</task_order>
