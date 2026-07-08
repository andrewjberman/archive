# Task Order: NFRA_CSE P3 -- retrofit existing producers to emit CSE events (OPLMCP audit-lake agent-producer nearly free)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-cse-p3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS~B (DS-side: per-producer CSE emission-contract spec, now -- unblocked by CSE-P2 close) + 0.5.0_AE_OpalETL (producer-wiring: graph-HEAD-advance emitter + OPLMCP audit-lake agent/deploy integration, sequenced AFTER FEDOBS-P3)</issued_to>
    <date>2026-07-07</date>
    <status>complete -- CLOSED 2026-07-08 (NFRA drive, COO~B). CVO AC5 exercise-verify PASS (dc7e5de1d): 4 producers live-emitting valid CSEs into the C0 log (git 6 genesis + graph_head + deploy + agent = 84 records, 4 source partitions), each fail-closed-validated @0.3, honest-range confidence (typed-HIGH where lexically-certain, Concept-LOW where not), and the AGENT producer REDACTION-SAFE BY CONSTRUCTION (all 15 agent CSEs metadata-only, ZERO MCP args body, scoped to the 3-tool metadata-safe allowlist). DS-side emission-contract spec (dabb7240e, DS~B) + AE producer-wiring (cse_emit_graphhead/deploy/agent.py, 0.5.0, S3-bootstrap no derive-rebuild) both CVO-certed. Follow-ons non-blocking: graph_head --full (~55k substantive full-graph stream) + scheduled emitters + 377-endpoint characterization.</status>
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
