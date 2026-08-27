<task_order>
<id>NFRA_PASSCRAFT.TO-3</id>
<project>NFRA_PASSCRAFT</project>
<title>P3 -- backfill the 3 COMPLETED tool-passes as ToolAudit CSEs to seed TOOLGRAPH's node set</title>
<assigned_to>0.8.0_AE_CloudComp</assigned_to>
<issued_by>2.0.0_SA_COO~A</issued_by>
<issued_date>2026-07-10</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_PASSCRAFT, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<priority>P3 -- unblocked by PASSCRAFT-TO-2 (emitter live, 1b2d5287d). Runs in PARALLEL with TOOLGRAPH-TO-2. Seeds TOOLGRAPH's node set with 3 REAL evidence-carrying tool-nodes.</priority>
<dispatch>GO 2026-07-10 by COO~A on the TO-2 landing. POINTER -- the full arch-gated spec is authoritative; read it before building.</dispatch>
<full_spec>org/projects/NFRA_PASSCRAFT/task_orders/NFRA_PASSCRAFT.TO-3.backfill-3-toolpasses.md @ 8dfcf1e75</full_spec>
<load_bearing_invariants>
  1. TRANSCRIPTION, not re-audit: transcribe each pass's ALREADY-authored verdict into the ToolAudit envelope via TO-2's emitter. NO new verdict computed (anti-harness held -- the emitter serializes, never judges).
  2. THE 3 COMPLETED PASSES (your ground-truth): comp-adapter-audit / comp-aws / comp-blast. The PRD's "comp-portal-thread" was a placeholder -- use the actually-completed 3.
  3. FIDELITY: each backfilled CSE decompresses to the original pass's cited evidence; a CSE that cannot is INVALID -- surface it as a finding (under-specified evidence_ref), do NOT fabricate.
  4. SOVEREIGN BOUNDARY: comp-blast's cache carries bd-backed nodes -- backfill the tool-PASS (names/structure only), NEVER the bd data. No bd/49F/Schwab read or target.
</load_bearing_invariants>
<diff_gate>Route diffs to 1.0.0_SA_CTO~A before landed. RAVC to 2.0.0_SA_COO~A. Hand the 3 CSEs to TOOLGRAPH-TO-1's node seed (feeds TOOLGRAPH-TO-2's Assurance plane).</diff_gate>
</task_order>
