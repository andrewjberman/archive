# Task Order (ad-hoc): SCTY_PREMCP secrets-rotation runbook + JWT break-glass procedure

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-scty-premcp-secrets-runbook</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <dispatch_state>DISPATCHED 2026-07-07T18:11Z -- ~B idle, all prior work closed. Pulled from the /prd-delta dashboard's SCTY_PREMCP missing-items list (not gated on anything else in that project). Self-contained, no dependency on the in-window scty-premcp-p1-layer2-phase1-readonly-scope deploy ledger.</dispatch_state>
    <gate_note>Gates: none. Effort: doc + procedure, not a live infra change (no deploy).</gate_note>
  </metadata>

  <objective>Write a secrets-rotation runbook covering the RS256 JWT signing key, the Fernet cache key, and the Graph client secret used by the MCP gateway (SCTY_PREMCP scope) -- including a break-glass procedure for the JWT signing key specifically (what to do if it's compromised or needs emergency rotation). This item was flagged as missing in today's /prd-delta dashboard sweep and has no PRD-listed gate.</objective>

  <requirements>
    <requirement id="1">Document the current secret locations + rotation mechanism (or lack thereof) for: RS256 signing key, Fernet cache key, Graph client secret.</requirement>
    <requirement id="2">Write a step-by-step rotation runbook for routine (planned) rotation of each.</requirement>
    <requirement id="3">Write a break-glass procedure specifically for the JWT signing key -- emergency rotation path if compromised, including how existing issued tokens are invalidated/handled.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion>Runbook exists, is concrete (exact commands/console steps, not prose-only), and has been sanity-checked against how the secrets are actually currently stored/loaded (source-grounded, not assumed).</criterion>
    <criterion>Break-glass procedure specifically addresses token invalidation on emergency rotation.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="finding">/prd-delta dashboard, SCTY_PREMCP missing-items list, 2026-07-07T17:37Z</ref>
    <ref type="project">org/projects/SCTY_PREMCP.json</ref>
  </references>
</task_order>
```
