<to_id>NFRA_OPLMCP.07</to_id>
<project>NFRA_OPLMCP</project>
<title>OPLMCP.07 graph-onboarding -- bring the m365-mcp-gateway server + AWS architecture onto the comp-* graph (close the STEP-A comp-iam coverage-gap)</title>
<assigned_to>0.7.0_AE_CloudOps (OPLMCP lane -- ~B or base; knows the gateway resources from .02/.03)</assigned_to>
<consult>comp-iam / comp-aws tool-owner (cross-tool REVIEW + COMMIT-THROUGH, owned-paths convention)</consult>
<verify>3.0.0_SA_CVO (coverage-verify + TO-5 (i)-gap close)</verify>
<issued_by>2.0.0_SA_COO (charter per CTO 174037Z; Andrew-direct "bring opalmcp server + architecture onto the graph"; PRD S5)</issued_by>
<issued_date>2026-06-23</issued_date>
<status>complete</status>
<!-- CLOSED 2026-06-24: AC1 (comp-iam resolves gateway) + AC2 (comp-aws 4 ALB derive-classes, 692142c9d) + AC3 (pipescript m365-mcp thread) + AC4 (CVO coverage-verify PASS 132813Z -> TO-5(i) coverage-gap CLOSED). Manual-IAM-review/rail-checked path for the gateway RETIRED (graph-native). Post-close hardening (non-blocking, tracked): CVO per-class oracle-cert for the 4 ALB classes. -->
<!-- GATED: POST-.02-GO-LIVE. Model the FINAL architecture -- the new EC2 instance-id (STEP-A replace), the OIDC listener config, the final go-live IAM all settle at go-live; modeling the in-flight state = stale. NON-BLOCKING on the .02 cutover (the STEP-A manual-IAM-review + rail-checked override carry .02). Formalizes the (i) coverage-gap ~B surfaced at STEP-A (comp-iam "No service matching" for m365-mcp-gateway). -->

<objective>
Bring the FULL OPLMCP architecture onto the comp-* graph so it's graph-backed -- the rail covers it NATIVELY, retiring the manual-IAM-review + rail-checked-override path for the gateway's IAM. Andrew-direct. SPEC-OF-RECORD: PRD Addendum A (docs/architecture/NFRA_OPLMCP_PRD.md) -- decompose against it. PRINCIPLE (Addendum A): a permanent estate service is "done" ONLY when the comp-* graph RESOLVES it -- graph-onboarding is definition-of-done, not afterthought (OPLMCP first; estate-wide generalization = CTO follow-on).
</objective>

<the_work>
1. comp-iam: model m365-mcp-gateway (the role + the gw_golive policy + SSM-core) so `comp-iam service m365-mcp-gateway` RESOLVES (currently "No service matching" = the STEP-A coverage-gap). Closes the gap directly.
2. comp-aws: model the OPLMCP AWS resources + edges -- ALB / target-group / listener / EC2 gateway / SG / Route53 ALIAS / the 3 SM secrets (opal/mcp/m365-login + m365-graph + Fernet) -- so the blast-radius/edge graph covers it (the destructive-op pre-gate basis).
3. pipescript / estate-graph: confirm the gateway resolves as its named property (EC2_MANIFEST carries the .03 + the .02-replace instance entry; verify comp-graph picks it up).
</the_work>

<compiler_tools_mandate>
comp-which-first; the model additions are cross-tool (comp-iam/comp-aws are not the OPLMCP lane's owned tools) -> author-by-OPLMCP-lane, REVIEW + COMMIT-THROUGH the comp-iam/comp-aws tool-owner (owned-paths convention). ds/safe-commit gates as applicable.
</compiler_tools_mandate>

<acceptance_criteria>
1. `comp-iam service m365-mcp-gateway` RESOLVES (role + gw_golive policy + SSM-core modeled); the manual-IAM-review / rail-checked path for the gateway IAM is RETIRED.
2. comp-aws covers the OPLMCP resources + edges (ALB/TG/listener/EC2/SG/Route53/3-SM-secrets) -- blast-radius graph resolves.
3. The gateway resolves as a named property in pipescript / estate-graph.
4. CVO verifies: comp-iam / comp-aws / comp-which ALL resolve the gateway post-onboarding -> the (i) coverage-gap CLOSES in the TO-5 telemetry.
5. Cross-tool review+commit-through the tool-owner; CVO verifies. GATED post-.02-go-live (model the FINAL settled architecture). RAVC2 COO + CVO.
</acceptance_criteria>
