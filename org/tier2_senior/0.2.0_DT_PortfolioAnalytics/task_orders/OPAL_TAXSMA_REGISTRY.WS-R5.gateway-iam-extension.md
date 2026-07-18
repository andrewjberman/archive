<task_order>
<to_id>OPAL_TAXSMA_REGISTRY.WS-R5</to_id>
<title>GATEWAY IAM EXTENSION — Alyssa's scoped role gains tax-producer-invoke + roster-key RW (net-new); CTO HARD plan-gate + Rule 22a; couples OPAL_TAXSMA_PT2 WS-4</title>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_to>0.2.0_DT_PortfolioAnalytics</issued_to>
<!-- DT designs the IAM; AE applies (m365-mcp-gateway infra); CTO gates. Mirrors WS-4's DT-designs/AE-applies/CTO-gates split. -->
<date>2026-07-17</date>
<status>pending</status>
<priority>P2 (Andrew-direct via CTO). Gates WS-R4 (the skill cannot invoke/enroll until this grant is live+verified). Net-new external write path -> CTO HARD plan-gate.</priority>

<authority>
Andrew-direct 2026-07-17 (brief §4 D4, §5 WS-R5). PRD §4 D4, §6. Couples OPAL_TAXSMA_PT2 WS-4 (the opal-mcp-emp-alyssa-read role + the opal-mcp-emp-* namespace-governance invariant).</authority>

<gate>
CTO HARD plan-gate + Rule 22a APPLIED+EXERCISED (same hard-withhold discipline as WS-4 — CTO does NOT confirm the onboarding grant live until the simulate + the assume-role exercise pass; SEV1/IAM). SINGLE-PURPOSE: the grant adds ONLY (i) lambda:InvokeFunction on the EXACT tax-pt2 producer ARN and (ii) s3:GetObject+PutObject on the EXACT roster key (blackdiamond/49f/_ops/taxsma_roster.json). NOT a broad invoke, NOT a broad S3 write. Rides the WS-4 opal-mcp-emp-* namespace invariant (every emp-* role stays single-employee least-privilege, gateway-trust-only).
</gate>

<scope>
Extend Alyssa's WS-4 scoped role (opal-mcp-emp-alyssa-read, currently read-only gold) with the onboarding grants:
- lambda:InvokeFunction on ONLY the tax-pt2 producer function ARN (the ad-hoc run).
- s3:GetObject + s3:PutObject on ONLY the roster key (the enroll RMW).
Nothing else. The role remains gateway-assumable-only (ExternalId), cross-firm fenced. DT designs the policy; AE applies via Terraform on the m365-mcp-gateway infra; CTO plan-gates + runs (or reviews AE's) Rule-22a live verify.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="Rule 22a live verify (post-apply, before the skill goes live)">
    <step>
      <run>simulate-principal-policy on the extended role, SEPARATE one-resource-arn calls: (a) lambda:InvokeFunction on the tax producer ARN = allowed; (b) s3:PutObject on the roster key = allowed; (c) lambda:InvokeFunction on ANOTHER function = implicitDeny; (d) s3:PutObject on a non-roster 49f key = implicitDeny; (e) s3:PutObject on opal-data-cot = explicitDeny (fence). PLUS exercise: the gateway assumes the role, enrolls a test entry + invokes the producer (succeeds); a non-entitled action AccessDenies.</run>
      <expect>Positives allowed, never-widen negatives denied, fence holds, exercise passes. comp-iam FAILS GREEN on the new (action,resource) — the live simulate + exercise are the truth.</expect>
      <if_mismatch>STOP. A widened grant (any-lambda / any-S3-write) is a REJECT. CTO hard-withholds go-live.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Couples OPAL_TAXSMA_PT2 WS-4 (extends the SAME opal-mcp-emp-alyssa-read role; the namespace-governance invariant applies). DT design -> AE apply (m365-mcp-gateway) -> CTO plan-gate + 22a. Gates WS-R4. Cross-firm fence must hold on the extended role.
</cross_domain_coordination>

<acceptance_criteria>
1. Policy design = single-purpose: invoke ONLY the tax producer, RW ONLY the roster key; no widening.
2. CTO plan-gate PASS on the design (pure-add, NEW-TERRITORY, namespace invariant honored).
3. Rule 22a APPLIED+EXERCISED evidence to CTO: positives allowed, never-widen negatives implicitDeny, cross-firm explicitDeny, assume-role exercise passes.
4. CTO go-live confirm (hard-withheld until 3 lands) before WS-R4 uses the grant.
5. Session log reproduces the simulate (separate invocations) + the exercise + observed vs expect.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/OPAL_TAXSMA_REGISTRY_PRD.md (§4 D4, §5 WS-R5, §6)</ref>
  <ref type="couples">org/tier2_senior/0.2.0_DT_PortfolioAnalytics/task_orders/OPAL_TAXSMA_PT2.WS4.gateway-scoped-entitlement.md (WS-4, the base role + namespace invariant)</ref>
  <ref type="iam-rule">CLAUDE.md Rule 22a (comp-iam fails GREEN on a new (action,resource); one --resource-arns/call; isolated controls).</ref>
</references>
</task_order>
