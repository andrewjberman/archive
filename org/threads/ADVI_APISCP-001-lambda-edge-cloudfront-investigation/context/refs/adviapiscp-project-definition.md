{
  "project_code": "ADVI_APISCP",
  "macro_code": "ADVI",
  "name": "Scoped API Multi-Partner Routing Architecture",
  "description": "Establish the canonical, compliant, multi-tenant serving architecture for /api/scoped/advisor-intelligence/* routes. Partner data must NEVER leave its origin bucket (opal-data-{firmId}). The shared-advisor-router Lambda@Edge must dynamically route to the correct S3 origin bucket per user based on the X-Firm-Id JWT claim injected by auth-validator-edge, eliminating the stale opal-data-portal-v2 copying anti-pattern permanently. Scope: Lambda@Edge firmware update, CloudFront origin config, Terraform, IAM, DynamoDB firm registry, DE endpoint documentation.",
  "prds": [
    {
      "path": "docs/architecture/ADVI_APISCP_PRD.md",
      "label": "Scoped API Multi-Partner Routing PRD",
      "date": "2026-03-10"
    }
  ],
  "status": "active",
  "phase": "Phase 1: Task orders issued to DT, DE, AE PartnerETL, AE OpalETL. No alignment thread needed -- PRD is implementation-ready.",
  "blocking": "DT Lambda@Edge v4 deploy (primary), AE audits (parallel)",
  "created": "2026-03-10",
  "pods": [
    "0.4",
    "0.5",
    "0.6"
  ],
  "pipeline": "bd-pipeline",
  "thread_counter": 0,
  "threads": []
}
