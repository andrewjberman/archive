<to_id>NFRA_OPLMCP.02</to_id>
<project>NFRA_OPLMCP</project>
<title>Backend integration: IT app-reg intake (5 values) -> Secrets Manager, flip MOCK_GRAPH=0, first live /me + /outlook calls</title>
<assigned_to>0.7.0_AE_CloudOps (+Andrew/IT)</assigned_to>
<issued_by>2.0.0_SA_COO (NFRA_OPLMCP decomposition per CTO dispatch 205110Z; PRD sec.5)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>pending -- HARD GATE: IT must complete 2 Entra app registrations (Andrew owns the IT call); intake the 5 values then flip</status>

On IT app-reg delivery: load the 5 values into Secrets Manager, flip MOCK_GRAPH=0, verify first live Graph calls (/me + /outlook). PRD: docs/architecture/NFRA_OPLMCP_PRD.md. SEQUENCING: behind the live LD-0177 NFRA queue (GLOBGRPH P2-STITCH, COSTAWS W3-W5, COMPAWS x3 pull first); no rush, backend leg IT-gated. CTO reviews infra vs PRD AC1-6 before any go-live. RAVC2 to COO + CTO.
