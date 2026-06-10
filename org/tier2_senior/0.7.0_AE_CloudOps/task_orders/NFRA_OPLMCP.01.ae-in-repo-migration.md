<to_id>NFRA_OPLMCP.01</to_id>
<project>NFRA_OPLMCP</project>
<title>In-repo migration: gateway -> infra/aws/ec2/m365-mcp-gateway/, kit -> .tools/m365-mcp-kit/, EC2_MANIFEST entry, comp-graph coverage</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (NFRA_OPLMCP decomposition per CTO dispatch 205110Z; PRD sec.5)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>active -- GO, no gate (parallelizable now); sequenced behind live NFRA queue</status>

Migrate the M365 MCP gateway + kit into the repo at the canonical paths, register in EC2_MANIFEST.json, ensure comp-graph coverage picks up the new nodes. PRD: docs/architecture/NFRA_OPLMCP_PRD.md. SEQUENCING: behind the live LD-0177 NFRA queue (GLOBGRPH P2-STITCH, COSTAWS W3-W5, COMPAWS x3 pull first); no rush, backend leg IT-gated. CTO reviews infra vs PRD AC1-6 before any go-live. RAVC2 to COO + CTO.
