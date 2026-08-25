<to_id>NFRA_DEBTSCAN.TO-D1</to_id>
<project>NFRA_DEBTSCAN</project>
<title>D1 — P1 reachability sweeps: entry-point set + forward/backward dead-path candidates + Day-0 triage (AE scope)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (NFRA_DEBTSCAN decomposition, 180600Z 2026-06-12; per CTO PRD §9 handoff 7caee952a)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_DEBTSCAN is complete; this TO was last touched 2026-06-12, predating the project close 2026-07-09. Closed as a record act, not a work verdict. Prior status: queued — start after D8-AE Part B RAVC2 (D8-AE takes priority)</status>
<priority>P1 — first deliverable of NFRA_DEBTSCAN; unblocked (no cross-deps except Part B finish first)</priority>

<background>
NFRA_DEBTSCAN PRD §2a + §9: estate-wide reachability dead-path scanning from the unioned stitch (kuzu_stitch_db, 3,088 nodes) and Nessie-only surface (1,157 nodes / 2,150 edges, marker-CURRENT). Day-0 candidate pool: 259 isolated nodes (0 in- AND out-edges, AWS layer) + 319 LIVE-no-DECLARED (in drift census).

BINDING DOCTRINE (non-negotiable, non-waivable):
- Scanner executes ZERO mutations. Findings route to owners WITH the trace. Zero deletions/changes — verifiable from IAM posture (read-only) + run logs.
- A finding filed off a stale or UNKNOWN-VINTAGE surface is INVALID — abort filing, report the staleness instead (every filed finding must carry the provenance header per AC6).
- Dead-path candidates follow the verify-before-delete chain: _run_script sub-publisher invocation trace + name-vs-EDGE blast radius (4-layer gate: name-target-list → comp-aws graph blast-radius → saved tf-plan → post-verify).
</background>

<scope>
Phase 1 — Entry-point definition + reachability queries (QUERY-class, Kuzu-local, ms, no rebuild):
  - Define the ENTRY-POINT SET: CloudFront routes + gold dispatcher dispatch lines + EventBridge rules + cron/SSM triggers (source from comp-kuzu, both stitch and Nessie surfaces with provenance headers captured)
  - Forward sweep: entry-points → unreached = dead-path candidate
  - Backward sweep: served artifacts ← unfed = never-written/stale candidate
  - Run on BOTH surfaces: kuzu_stitch_db (3,088 nodes, pipeline+AWS+portal) AND Nessie canonical (1,157 nodes); record provenance header per run (DB, vintage, F6 marker state)
  - Record query results with provenance, NOT findings yet

Phase 2 — Suppression config before filing:
  - Populate `debtscan/suppression.yaml` from banked FP classes BEFORE first finding is filed:
    - Deny+Principal:* = guardrail not public grant (memory: reference_deny_principal_star_is_guardrail_not_public_grant.md)
    - Designed bd/cot canonical twins (bare/canonical twin-set discrimination across firms; 9-RED lesson)
    - D8 Day-0 known findings (getAUMMetrics url:(not resolved), advisor_intelligence auth:NONE FP)
    - Expected schema-check aliases
  - Seed the BenchmarkHeatmap/portal-proxy/PeersTab 2a-class instance into Day-0 backlog (AE's own Part B finding; CTO noted this belongs in TO-D1 Day-0 material)
  - Document each suppression with REASON (not just list)

Phase 3 — CVO precision sample (gate before non-ADVISORY):
  - File a SAMPLE of findings (>= 10) into ledger at org/modules/graph/debtscan/{YYYY-MM-DD}_D1_reachability_candidates.md
  - Ledger format: each finding = {family, severity, firm-scope, surface, triage, owner-lane, trace, verified-real-vs-FP}
  - Sample precision = fraction of VERIFIED-REAL findings in the sample
  - RAVC2 to COO with the ledger + sampled precision score BEFORE promoting any finding above ADVISORY status
  - CVO adjudicates precision gate (>=0.8 required for non-ADVISORY filing and critical-paths cross-filing)

Non-phase structural requirements:
  - Burn-down counter: file per-family count into a graph_metrics record at each sweep (AC3)
  - Cadence: nightly-piggyback ONLY (LD-0176) + QUERY-class ad-hoc; no manufactured derives
  - Freshness binding: every query records provenance header; refuse to file if surface is STALE or UNKNOWN-VINTAGE (AC6)
  - Cross-filing: if a gate-passed finding touches a critical-surface carve (per critical-surfaces.yaml), ALSO file in org/critical_paths/change_management/ per NFRA_GRAPHS §10.6 (AC5; no duplicate alarms)

Acceptance (D1 portion):
- AC1: first sweep produces dated ledger with >=1 CVO-verified-REAL finding
- AC2: zero mutations — verifiable from run logs + read-only IAM posture
- AC6: every filed finding carries provenance header; synthetic stale-vintage run demonstrably refuses to file
- RAVC2 to COO after Phase 3 sample submitted (CVO gates non-ADVISORY promotion)
</scope>
