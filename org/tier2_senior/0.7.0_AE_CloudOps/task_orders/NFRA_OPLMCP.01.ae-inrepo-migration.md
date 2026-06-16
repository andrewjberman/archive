<to_id>NFRA_OPLMCP.01</to_id>
<project>NFRA_OPLMCP</project>
<title>OPLMCP.01 — In-repo migration: gateway code + Terraform + comp-graph coverage (AE scope)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (NFRA_OPLMCP sub-stream decomposition, 181700Z 2026-06-12; per CTO PRD §OPLMCP sub-streams 7caee952-era)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete -- in-repo migration DONE (orig 8b0e7d241 + ~B re-sync 2026-06-16 66a9a353b/a2fe54360/0c767fa8c, AE~B RAVC2). NB DUPLICATE to_id: 2 .01 files (inrepo + in-repo); both reconciled complete. [recon 2026-06-16 COO]</status>
<priority>P2 — first OPLMCP sub-stream; unblocks OPLMCP.02 backend integration + OPLMCP.03 TF infra</priority>

<background>
NFRA_OPLMCP front-end leg is proven (device -> gateway, mock backend): MCP Streamable HTTP, 13 Graph tools, access-layer identity propagation, KILL_SWITCH/blocklist verified. Gateway code + local Lokka kit currently live on Andrew's machine only (not in-repo). CTO ruling (ws-charter): bring in-repo under NFRA_OPLMCP governance per CLAUDE.md Rules 7-12 (Terraform-owns-EC2-infra, EC2_MANIFEST.json registration, S3-artifact deploy via safe-ec2-deploy.sh, audit->lake governance is the repo's strength).

OPLMCP.02 (backend integration, blocked on IT app-reg provisioning) + OPLMCP.03 (Terraform nano EC2 infra) both depend on OPLMCP.01 migration landing first.
</background>

<scope>
1. GATEWAY CODE MIGRATION:
   - Move/copy the m365-mcp-gateway/ codebase into `infra/aws/ec2/m365-mcp-gateway/` in the repo
   - Verify it follows S3-artifact deploy pattern (safe-ec2-deploy.sh workflow per Rule 12)
   - Register in EC2_MANIFEST.json (name, deploy-script path, S3-artifact path, service owner)

2. LOKKA MCP KIT VERSION:
   - Move local Lokka kit into `.tools/m365-mcp-kit/` (versioned in repo, not machine-local)
   - Document usage in .tools/m365-mcp-kit/README-install.md or inline in the kit

3. COMP-GRAPH COVERAGE:
   - Add the m365-mcp-gateway EC2 instance and its Lambda/S3/route dependencies to the comp-graph (comp-aws derive or manual node registration in the appropriate graph YAML)
   - Ensure comp-blast + comp-iam can reach the gateway instance
   - Run comp-iam service m365-mcp-gateway to verify IAM gaps after registration

4. PRE-CHANGE GATES (Rule 20):
   - comp-kuzu "MATCH (n) WHERE n.name CONTAINS 'm365' RETURN n" — confirm 0 nodes before migration (expected; confirms clean slate)
   - comp-blast m365-mcp-gateway after migration — confirm blast radius is bounded
   - comp-iam gaps after migration — flag any missing permissions for Secrets Manager reads (the OPLMCP.02 backend will need SM access)

5. NOT IN SCOPE for OPLMCP.01:
   - Terraform EC2 + ALB infra (OPLMCP.03 scope)
   - IT app-reg intake + MOCK_GRAPH=0 flip (OPLMCP.02 scope, gated on IT provisioning)
   - Verified-Access JWT signature-verify (pre-prod TODO, OPLMCP.03+)
   - Tool surface expansion beyond the current 13 Graph tools (OPLMCP.04)
   - Claude-Enterprise data-terms governance (OPLMCP.05)

Acceptance:
- gateway code in infra/aws/ec2/m365-mcp-gateway/ and EC2_MANIFEST.json registered
- Lokka kit in .tools/m365-mcp-kit/
- comp-graph: m365-mcp-gateway node present (comp-aws + comp-blast reachable)
- comp-iam: no MISSING permissions found at migration-time (Secrets Manager access noted for OPLMCP.02 prep)
- RAVC2 to COO when complete
</scope>
