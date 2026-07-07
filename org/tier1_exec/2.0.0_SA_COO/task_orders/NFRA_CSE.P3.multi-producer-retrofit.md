# Task Order: NFRA_CSE P3 -- retrofit existing producers to emit CSE events (OPLMCP audit-lake agent-producer nearly free)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-cse-p3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>per-producer owners (git/agent/deploy/graph-HEAD)</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <prd_ref>docs/architecture/NFRA_CSE_PRD.md (P3)</prd_ref>
    <backfill_note>TO FILE backfilled 2026-07-07 -- the SEMCTL plane was dispatched + built via MCP + arch-gate RAVC but the durable TO records were not materialized (Andrew/CTO caught the gap 2026-07-07). This TO reflects the REAL current state. Standing-fix adopted: TO-file + MCP-dispatch, both, every time.</backfill_note>
  </metadata>

  <objective>Retrofit git/agent/deploy/graph-HEAD producers to emit CSE C0 events over the P2 log. Reuse OPLMCP .05 audit-lake as the near-free agent/MCP producer.</objective>

  <requirements>
    <requirement id="1">Each producer emits schema-valid CSEs with mandatory provenance</requirement>
    <requirement id="2">OPLMCP audit-lake agent-producer wired</requirement>
    <requirement id="3">Sequences after CSE-P2 (the log) lands</requirement>
  </requirements>
</task_order>
```
