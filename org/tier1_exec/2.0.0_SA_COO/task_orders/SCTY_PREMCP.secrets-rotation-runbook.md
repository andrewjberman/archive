# Task Order (ad-hoc): SCTY_PREMCP secrets-rotation runbook + JWT break-glass procedure

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-scty-premcp-secrets-runbook</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <dispatch_state>DISPATCHED 2026-07-07T18:11Z -- ~B idle, all prior work closed. Pulled from the /prd-delta dashboard's SCTY_PREMCP missing-items list (not gated on anything else in that project). Self-contained, no dependency on the in-window scty-premcp-p1-layer2-phase1-readonly-scope deploy ledger. CLOSED 2026-07-07T18:45Z.</dispatch_state>
    <gate_note>Gates: none. Effort: doc + procedure, not a live infra change (no deploy).</gate_note>
  </metadata>

  <objective>Write a secrets-rotation runbook covering the RS256 JWT signing key, the Fernet cache key, and the Graph client secret used by the MCP gateway (SCTY_PREMCP scope) -- including a break-glass procedure for the JWT signing key specifically (what to do if it's compromised or needs emergency rotation). This item was flagged as missing in today's /prd-delta dashboard sweep and has no PRD-listed gate.</objective>

  <requirements>
    <requirement id="1" status="met">Documented all 3 secret locations (Secrets Manager IDs + JSON/plain shape) + the rotation mechanism (NONE automated -- deploy-time-fetch only, confirmed via secrets-iam.tf's own comment + deploy-to-ec2.sh source).</requirement>
    <requirement id="2" status="met">Step-by-step routine rotation for each of the 3, all sharing the same mechanical path (update secret -> re-run the canonical safe-ec2-deploy.sh wrapper, which already re-fetches on every run).</requirement>
    <requirement id="3" status="met">Break-glass for the JWT signing key: source-grounded the single-in-memory-key/no-JWKS-multi-kid mechanism (oauth_as.py) -- rotation+restart IS the token-invalidation mechanism, atomic and total. Documented the faster surgical revocation.py kill-path as the FIRST response for a single-user compromise. Includes exercise-based verification (JWKS kid actually changed + a pre-rotation token actually fails), not a config-read close.</requirement>
  </requirements>

  <closure_evidence>
    docs/runbooks/m365-gateway-secrets-rotation.md, commit 465a9ba7f. Session log:
    org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-07-07/scty_premcp_secrets_rotation_runbook.md
    (0b572929c). Two inaccuracies caught + fixed before commit (canonical deploy wrapper vs
    direct script; revoke-user's actual CLI argv shape) -- verified against source, not assumed
    correct on first draft.
  </closure_evidence>

  <references>
    <ref type="finding">/prd-delta dashboard, SCTY_PREMCP missing-items list, 2026-07-07T17:37Z</ref>
    <ref type="project">org/projects/SCTY_PREMCP.json</ref>
  </references>
</task_order>
```
