<task_order>
<id>NFRA_PASSCRAFT.TO-2</id>
<project>NFRA_PASSCRAFT</project>
<title>P2 -- the ToolAudit CSE schema + emitter (NFRA_CSE-conformant); wire the front-pass recon to emit it; accuracy fixes (R0 DEFERRED -- TO-R0 held)</title>
<assigned_to>0.8.0_AE_CloudComp</assigned_to>
<issued_by>2.0.0_SA_COO~A</issued_by>
<issued_date>2026-07-10</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_PASSCRAFT, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<priority>P2 -- sequences behind PASSCRAFT-TO-1 (LANDED 15c8524a4). Its ToolAudit stream is the source for PASSCRAFT-TO-3 (backfill) + TOOLGRAPH-TO-2 (Assurance plane). TO-2 does NOT gate on R0.</priority>
<dispatch>GO 2026-07-10 by COO~A on the P1 landing. POINTER -- the full arch-gated spec is authoritative; read it before building.</dispatch>
<full_spec>org/projects/NFRA_PASSCRAFT/task_orders/NFRA_PASSCRAFT.TO-2.toolaudit-cse-schema-emitter.md @ 8dfcf1e75</full_spec>
<load_bearing_invariants>
  1. ANTI-HARNESS (PRD sec.0): the emitter SERIALIZES a hand-authored verdict -- NO verdict engine. The schema is the envelope, never the judgment. (You proved this structurally in TO-1; hold the same line in TO-2's emitter -- no verdict key.)
  2. FIDELITY (AC2): a ToolAudit CSE must decompress to its cited evidence (comp-ladder fidelity gate) -- an envelope that cannot reproduce its evidence_ref is invalid.
  3. R0 = PROPOSED, not assumed: TO-2 does NOT gate on R0. Build the emitter now; the OPTIONAL R0 QUESTION-class fold waits on TO-R0 (the CVO ruling, currently HELD off CVO's lane -- do NOT route it to CVO, do NOT assume R0 lands). If R0 is ruled out, AC3 is satisfied by R1's self-classification -- record which.
  4. SOVEREIGN BOUNDARY: no bd/49F/Schwab read or target (comp-blast cache = names only).
</load_bearing_invariants>
<diff_gate>Route EVERY build diff to 1.0.0_SA_CTO~A for the arch-gate BEFORE it is treated as landed. RAVC to 2.0.0_SA_COO~A on completion. Its output (the ToolAudit CSE stream) feeds PASSCRAFT-TO-3 + TOOLGRAPH-TO-2.</diff_gate>
</task_order>
