<to_id>NFRA_OPLMCP.02</to_id>
<project>NFRA_OPLMCP</project>
<title>Backend integration: IT app-reg intake (5 values) -> Secrets Manager, flip MOCK_GRAPH=0, first live /me + /outlook calls</title>
<assigned_to>0.7.0_AE_CloudOps (+Andrew/IT)</assigned_to>
<issued_by>2.0.0_SA_COO (NFRA_OPLMCP decomposition per CTO dispatch 205110Z; PRD sec.5)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>complete -- 2026-06-23 (0.7.0_AE_CloudOps~B): backend GO-LIVE done. IT app-regs delivered (5 values in Secrets Manager: m365-login/m365-graph + m365-fernet created). STEP-A secrets+IAM (EC2 replaced i-01d75->i-07dccb1615503ac99 for AMI+public-IP, gw_golive scoped policy) -> STEP-B code-deploy MOCK_GRAPH=0 + /health={ok:true} -> STEP-C listener 503->authenticate-oidc GO-LIVE VERIFIED (curl https://mcp.opalinvest.dev/ = 302->Entra not 503; TG healthy; TF 0-diff). tag m365-mcp-gateway-v1.2.0; commit e17ffac4d; ledger oplmcp02-golive-cutover CLOSED (3 legs proven); RAVC2 CTO+COO. AC2 (/me+/outlook live + per-user-scope, synthetic mailboxes) = CVO cert gate (separate). CTO-GO'd plan + 2 rulings.</status>

On IT app-reg delivery: load the 5 values into Secrets Manager, flip MOCK_GRAPH=0, verify first live Graph calls (/me + /outlook). PRD: docs/architecture/NFRA_OPLMCP_PRD.md. SEQUENCING: behind the live LD-0177 NFRA queue (GLOBGRPH P2-STITCH, COSTAWS W3-W5, COMPAWS x3 pull first); no rush, backend leg IT-gated. CTO reviews infra vs PRD AC1-6 before any go-live. RAVC2 to COO + CTO.
