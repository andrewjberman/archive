<to_id>NFRA_OPLMCP.03</to_id>
<project>NFRA_OPLMCP</project>
<title>Infra/deploy: Terraform nano EC2 + ALB authenticate-oidc + Secrets Manager + DNS/ACM; Verified-Access JWT verify = pre-prod TODO</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (NFRA_OPLMCP decomposition per CTO dispatch 205110Z; PRD sec.5)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>active -- SCAFFOLD now (parallelizable); terraform apply GATED on .02 values landing</status>

Author the Terraform scaffold (nano EC2, ALB with authenticate-oidc, Secrets Manager wiring, DNS/ACM). Apply only after OPLMCP.02 delivers the app-reg values. Verified-Access JWT verification is a pre-prod TODO, not v1. PRD: docs/architecture/NFRA_OPLMCP_PRD.md. SEQUENCING: behind the live LD-0177 NFRA queue (GLOBGRPH P2-STITCH, COSTAWS W3-W5, COMPAWS x3 pull first); no rush, backend leg IT-gated. CTO reviews infra vs PRD AC1-6 before any go-live. RAVC2 to COO + CTO.
