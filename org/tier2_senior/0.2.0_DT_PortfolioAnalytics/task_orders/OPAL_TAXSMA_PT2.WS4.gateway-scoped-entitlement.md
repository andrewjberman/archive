<task_order>
<to_id>OPAL_TAXSMA_PT2.WS4</to_id>
<title>GATEWAY ENTITLEMENT — email→scoped-ARN layer + Alyssa's gold-prefix-ONLY read role (net-new external read into the monolith; CTO hard plan-gate + Rule 22a live verify + never-widen single-prefix)</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.2.0_DT_PortfolioAnalytics</issued_to>
<!-- Lane: 0.2.0_DT authored the design (TAXSMA_PT2_SCOPED_TABLE_IAM_ASSESSMENT) + CTO named DT lead on WS-4.
     The gateway IAM apply is AE-executed (m365-mcp-gateway is AE/CloudOps infra) — DT designs, AE applies,
     CTO gates. -->
<date>2026-07-17</date>
<!-- PARKED 2026-07-20 by 0.2.0_DT per CTO sequence call 201850Z: MDPF_REVAMP is sole focus. Resume-trigger = MDPF parity+swap complete OR Andrew word (OR immediately if urgent -> flag CTO). Clean-park: the gateway-IAM apply STAYS HELD (not half-landed), pick-up-ready; on resume the 22a applied+exercised evidence routes to CTO as the SEV1 gate. -->
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project OPAL_TAXSMA_PT2, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
<priority>P2 (Andrew-direct via CTO 205620Z). GATE: CTO hard plan-gate (net-new external-read grant) + WS-3 gold prefix exists (the verify target). Parallel to the data chain; the read path (WS-6) needs it.</priority>

<authority>
PRD §6 WS-4 + DT's design (org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/TAXSMA_PT2_SCOPED_TABLE_IAM_ASSESSMENT_20260717.md).
Andrew-direct arch (MEMORY: per-employee scoped IAM, email→scoped-IAM-ARN assume-role via the MCP gateway).
</authority>

<gate>
** CTO HARD PLAN-GATE (his, non-negotiable): WS-4's gateway scoped-IAM is a NET-NEW external-read grant into
   opal-data-assets — the gateway has ZERO reach today. It goes through CTO's plan-gate + Rule 22a live verify
   + never-widen single-prefix. Do NOT apply the IAM until CTO reads the plan. **
Also gated on WS-3 (the gold dim_taxsma_report prefix must exist for the verify's positive control).
</gate>

<scope>
The email→scoped-ARN entitlement layer + Alyssa's gold-prefix-ONLY read role: read-only on ONLY the gold
`blackdiamond/49f/gold/dim_taxsma_report/` prefix (PII-free by construction — the PII boundary is silver→gold,
so a gold-only grant is the security-correct single-prefix PII-free read). email→scoped-IAM-ARN assume-role
through the MCP gateway. NEVER-WIDEN single-prefix — the grant reaches exactly the gold prefix, nothing else.
</scope>

<compiler_tools_mandate>
  <phase id="2" when="before apply — the Rule 22a live verify (CTO gate evidence)">
    <step>
      <run>aws iam simulate-principal-policy --policy-source-arn &lt;Alyssa gateway role&gt; --action-names s3:GetObject --resource-arns &lt;exact gold dim_taxsma_report prefix key&gt; (ONE --resource-arns; positive control)</run>
      <expect>ALLOWED on the gold prefix. comp-iam is NECESSARY-NOT-SUFFICIENT (models action not (action,resource)) — the live simulate on the exact key is the truth (Rule 22a).</expect>
      <if_mismatch>STOP. Fix the grant scope before apply.</if_mismatch>
    </step>
    <step>
      <run>SEPARATE invocation — simulate the SAME role against a DIFFERENT prefix (e.g. any silver/bronze key): --resource-arns &lt;a non-gold key&gt;</run>
      <expect>implicitDeny (or explicit deny) on EVERY non-gold prefix — the never-widen control. Run this as a SEPARATE call from the positive control (2+ ARNs in one call poisons held ones to implicitDeny; a batched control is corrupted by its own presence — Rule 22a).</expect>
      <if_mismatch>STOP. A role that reaches beyond the gold prefix is a widen — do not apply; re-scope.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
CTO plan-gate + apply is AE-executed (m365-mcp-gateway infra). Feeds WS-6 (the /tax-pt2 read path uses Alyssa's
scoped role end-to-end). Depends on WS-3 (gold prefix exists). The owned-domain allowlist / SES-sender rules do
not apply (this is an IAM read grant, not a sending identity). No alarm leg.
</cross_domain_coordination>

<acceptance_criteria>
1. CTO plan-gate PASSED on the net-new grant (his read of the plan diff).
2. Rule 22a live verify: ALLOWED on the exact gold prefix + implicitDeny on a non-gold prefix — the two controls
   run as SEPARATE invocations, both reproduced in the session log.
3. email→scoped-ARN assume-role through the gateway works end-to-end for Alyssa's identity (exercised, not config-read).
4. never-widen single-prefix confirmed; session log reproduces each mandate run + observed vs expect.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/OPAL_TAXSMA_PT2_PRD.md (§6 WS-4)</ref>
  <ref type="design">org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/TAXSMA_PT2_SCOPED_TABLE_IAM_ASSESSMENT_20260717.md</ref>
  <ref type="rule">CLAUDE.md Rule 22a (comp-iam fails GREEN; one --resource-arns; controls separate)</ref>
</references>
</task_order>
