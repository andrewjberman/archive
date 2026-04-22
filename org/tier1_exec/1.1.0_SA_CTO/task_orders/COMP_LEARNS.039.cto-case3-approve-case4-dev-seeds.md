<task_order>
  <metadata>
    <id>1.1.0_SA_CTO-2026-04-22-comp-learns-039</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_SA_CTO</issued_to>
    <date>2026-04-22</date>
    <status>complete</status>
    <project_code>COMP_LEARNS</project_code>
  </metadata>

  <objective>
    Review and approve one Case 3 candidate from .038 SWE-bench proposals.
    Author Case 4 benchmark backlog entry (OSS historical cross-module bug, httpx or requests).
    Author 4 dev_backlog seed entries (dev-1 through dev-4) per BACKLOG_V1 §7.
  </objective>

  <gate>
    .038 complete — COO MCP with 3 bl-sweb-*.yaml candidates required before Case 3 approval.
    .037 complete — comp/backlog/benchmark/ and comp/backlog/dev/ directories must exist before
    writing new YAML entries.
  </gate>

  <deliverables>
    <deliverable>comp/backlog/benchmark/bl-sweb-{approved-id}.yaml — Case 3 approved entry (from .038 candidates)</deliverable>
    <deliverable>comp/backlog/benchmark/bl-{case4-id}.yaml — Case 4 authored entry (OSS cross-module, httpx or requests)</deliverable>
    <deliverable>comp/backlog/dev/bl-dev-1.yaml — Archetype E selector_ceiling (httpx or click)</deliverable>
    <deliverable>comp/backlog/dev/bl-dev-2.yaml — Archetype E cache_identity (httpx)</deliverable>
    <deliverable>comp/backlog/dev/bl-dev-3.yaml — Archetype A or D rapid-intake (requests or adjacent)</deliverable>
    <deliverable>comp/backlog/dev/bl-dev-4.yaml — Archetype A or B compiler-win (httpx or click); success = primary_metric KEEP under ratchet</deliverable>
  </deliverables>

  <status_notes>
    2026-04-22: Staged pending .037 + .038. Pre-drafting Case 4 and dev seeds for fast
    execution on .038 landing. COO MCP received and acked.
  </status_notes>
</task_order>
