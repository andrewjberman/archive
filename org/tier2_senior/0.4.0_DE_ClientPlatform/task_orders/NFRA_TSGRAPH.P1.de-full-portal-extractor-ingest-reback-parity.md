<to_id>NFRA_TSGRAPH.P1</to_id>
<project>NFRA_TSGRAPH</project>
<title>P1 — full-portal semantic extractor + Nessie ingestion + RE-BACK comp-types/comp-transform under a HARD parity-gate (no rip-and-replace)</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<consult>0.7.0_AE_CloudOps (Nessie INGESTION leg = reuse the inc-2b CodeBuild+emit pattern; NO schema change, string discriminators on CloudNode/CloudEdge — its globgrph platform)</consult>
<parity_gate_reviewer>1.0.0_SA_CTO (close-reviews the per-tool parity results = the cutover gate)</parity_gate_reviewer>
<issued_by>2.0.0_SA_COO (CTO P1-decompose direction 194141Z; formal PRD v0.1 31a0b0e92 = docs/architecture/NFRA_TSGRAPH_PRD.md, decision-complete)</issued_by>
<issued_date>2026-06-17</issued_date>
<status>active</status>
<priority>HIGH — Andrew-direct lineage (the "expand graphing into the TS" ask). P0 GO'd + measured (7.2s cold / 12.5ms incremental fits the derive); P1 makes it real. Build-primary ts-morph, SCIP deferred (P0 verdict).</priority>

<context>
P0 spike GO (c8871dd52 code + f73437cae report, CTO+COO accepted): a ts-morph TS-Compiler-API extractor resolves real symbols/types (regex baseline empirically fails the same slice), proves the field-grain stitch end-to-end (a renamed field through a ternary-gated adapter), emits on the real CloudNode/CloudEdge schema, fixes the D8 key-space class, measured-affordable. Formal PRD v0.1 decision-complete. P1 = scale it to the full portal + re-back the regex tools on it WITHOUT regressions.
</context>

<deliverable>
PRD §6 shape (DE-proposed + CTO-endorsed), 3 legs in sequence:
LEG A — FULL-PORTAL INCREMENTAL EXTRACTOR (DE-primary): the ts-morph semantic walk over the whole portal (not one slice), incremental (changed files + dependents, mirroring the trace 5-min cache + nightly derive). Emit the §3 node/edge schema for the full portal.
LEG B — NESSIE INGESTION (AE-consult, 0.7.0): wire the extractor's producer JSON into the platform via the inc-2b CodeBuild->S3->derive pattern. NO schema change — string discriminators on the existing CloudNode/CloudEdge (the P0 contract). The semantic graph goes LIVE + queryable via comp-kuzu (with the provenance header + HEAD-oracle freshness, F5 law).
LEG C — RE-BACK comp-types + comp-transform on the semantic graph, under a HARD PARITY-GATE (gated on Leg B live): tool-by-tool, equivalence-or-BETTER vs the regex tools BEFORE any cutover (the GLDINC incremental-vs-oracle discipline — NO rip-and-replace). The NNA-attribution chain is the P1 STRESS-TEST (the dual-attribution fork + recompute + inference classes — exactly the hard case the semantic graph should illuminate; it was excluded from P0 as in-flux).
</deliverable>

<acceptance_criteria>
(PRD §8, machine-checkable — CTO authored these as the cutover gate)
AC1 PARITY: 0 regressions, a PER-TOOL parity report (comp-types + comp-transform on the semantic graph == or BETTER than the regex tool on the same inputs) BEFORE cutover. Equivalence-or-better is the bar; any regression blocks the cutover for that tool.
AC2 FINE-LINEAGE: gold-field -> RENDERS path resolves end-to-end OR is recorded-unresolved (visible). The field-grain lineage (the P0 spine, now full-portal).
AC3 NO-SILENT-UNKNOWN (HARD INVARIANT): every unresolvable (dynamic URL/key, as-cast, HOC) is marked unresolved + VISIBLE in coverage, NEVER a false edge (the platform law + the P0 discipline).
AC4 INTEGRATION + KUZU SCALE-WATCH: the full-portal graph loads into Nessie->Kuzu + stitches to cloud/trace (DataFetch->Lambda->gold->S3 joins); watch the index/query scale (P0 measured 7.2s cold / 12.5ms incremental — confirm at full-portal volume, flag if it degrades).
AC5 NNA DIVERGENCE VISIBLE: the NNA-attribution dual-source divergence (D_00f vs D_00c) surfaces as a FORKED FLOWS_TO in the semantic graph (the stress-test — proves the graph illuminates the exact bug-class ADVI_NNAATTR is fixing).
</acceptance_criteria>

<sequencing>
Leg A (extractor) -> Leg B (ingestion, AE-consult) -> Leg C (re-back + parity-gate, gated on B live). RAVC2 at the PARITY-GATE (Leg C) -> CTO close-reviews the per-tool parity results = the cutover decision. Intermediate RAVC2 on Leg A+B (graph live) is fine for a checkpoint. NO cutover of a re-backed tool until its AC1 parity passes + CTO signs.
</sequencing>

<lane_note>
DE-primary (the ts-morph extractor + the re-back = the hard TS/semantic work; you own the substrate). 0.7.0_AE consult for the Nessie ingestion (the inc-2b CodeBuild+emit pattern, its platform — commit-through-owner if you touch derive code; your tsgraph_spike/ lane is granted for the extractor). CTO parity-gate-reviews the cutover (Leg C). Your P0 code is committed (c8871dd52) under the org/modules/graph/tsgraph_spike/** = DE lane (e0b2f555e); P1 extends it. RAVC2 to COO (CC CTO).
</lane_note>
