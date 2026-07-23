<task_order>
<to_id>NFRA_ONTOLOGY2.P1</to_id>
<title>THE RAILS — author D1 (value/grain), D2 (path/flow), D3 (contract/obligation) as ADDITIVE rule-bank sections between the ratified C0-C3 rungs; fold in the PSTMRT P2 completeness-axis amendment</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<date>2026-07-23</date>
<status>pending</status>
<!-- ~C 2026-07-23 ~19:2xZ: AUTHORED + validated + routed to CTO~Z for arch-gate co-canonize.
     D1/D2/D3 rails + completeness axis + type_tuple + c1_frontend_adapter fork-resolution (11/11
     additive, 0 new-vocab) authored in NFRA_ONTOLOGY_RULE_BANK.yaml (v1.1->1.2) + variance_dimensions.yaml
     (+registry_binding). Acceptance EXERCISED: summary_corpus.py zero-diff (self-test+build+isolation
     control), comp-ontolint PASS, strictly-additive diff. Package: deliverables/NFRA_ONTOLOGY2_P1/
     ARCH_GATE_PACKAGE.md + ontology2_p1_authored.patch. Files are exec-locked (ANY_EXEC) -> CTO~Z
     co-canonizes (staged live OR apply patch). Status stays pending until canonized + CVO~Z-verified. -->

<priority>P0 — THE CRITICAL PATH of NFRA_TOOLSTACK. Every layer above the mechanical (TOOLSEM, TOOLBHVR, TOOLARCH P2) blocks on the rail vocabulary this TO produces.</priority>

<authority>
Andrew-direct 2026-07-23 (NFRA_ONTOLOGY2 charter, verbatim in docs/architecture/NFRA_ONTOLOGY2_PRD.md
s.0; the constitutional layer of the NFRA_TOOLSTACK program). ~Z holds TO-authoring + direct dispatch
for this batch (Andrew-direct "write the TOs and just deliver them direct"). Constitution:
docs/doctrine/INTENT_DENOMINATOR_SYNCHRONIZATION.md. You are the rule-bank CONTENT lane; ~Z gates;
CVO~Z verifies.
</authority>

<scope>
Author three ADDITIVE dynamic-rail sections in org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml, each
interleaved between the existing static rungs. Design of record: NFRA_ONTOLOGY2_PRD.md s.2.

D1 -- VALUE / GRAIN (between C0 and C1): WHAT travels an edge and at what grain (artifact / partition /
   row / field). SEED TO EXTEND, not invent: derives-from already carries
   EdgeKind(passthrough|rename|recompute_guarded) -- the ratified embryonic value semantic. Name the
   grain axis; state which existing edge types carry which grain; cite the graph evidence.

D2 -- PATH / FLOW (between C1 and C2): a DIRECTED, typed PATH -- the ordered hops a value takes, each
   hop's EdgeKind, the transform at each, and the CADENCE the path runs at. SEED: C2 motifs are already
   "typed multi-hop paths @ recurrence"; D2 adds direction + transform + time to that topology.

D3 -- CONTRACT / OBLIGATION (between C2 and C3): what a motif PROMISES vs what it does -- cadence,
   completeness-over-a-scope, canonical-source, layer-grammar. SEED: PSTMRT's completeness axis +
   TRIGGER_LAYER doctrine are proto-D3 obligations; the MDPF delivery-cadence contract is a written one.

Each rail section MUST carry: (1) its vocabulary; (2) the GRAPH EVIDENCE that populates it (a rail that
cannot be derived from the existing graph + declared contracts is speculation -- ship the measurement
with the rail); (3) its honest COVERAGE BOUNDARY (what it cannot yet see -- the R1 discipline applied to
the ontology itself); (4) the derivations it licenses (freshness=D2+D3+vintages+calendar;
provenance=D1+D2 backward; blast=D2 forward at grain).

FOLD-IN -- PSTMRT P2 (designed in NFRA_PSTMRT_PRD.md s.3, co-owned with you): the rule-bank COMPLETENESS
axis section + variance_dimensions.yaml registry_binding to data/firm_registry.json. It is a D3-class
obligation (complete-over a scope), so it lands naturally in this rail work. The normalization CVO~Z
corroborated (parity asserts aliases UNION firm_id; three mapping surfaces need one read) is part of it.
</scope>

<hard_constraints>
- ADDITIVE ONLY. The ratified C0-C3 ladder, the 14 ROLES, the 10 RELATIONS, and the variance operator
  are RATIFIED and UNTOUCHED. Any change that renames or re-scopes ratified vocabulary is OUT OF SCOPE
  and routes to the ratification chain via ~Z -- not authored here.
- No LLM semantics. Deterministic structure first; any LLM label is orthogonal + one-way (ontology law).
- The rails must be DERIVABLE from the existing graph. If a rail element cannot be populated from live
  graph evidence, mark it a declared-but-unpopulated FORWARD element (the tick-25 stated-intent pattern)
  -- loud, not silent.
</hard_constraints>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-kuzu to enumerate the live edge-kind distribution + the tick-29 uncovered-edge set (11 unmapped + 9 zero-live-in-plane); read NFRA_ONTOLOGY_RULE_BANK.yaml meta + the derives-from EdgeKind seed</run>
    <expect>Each rail's populating evidence is enumerated from the live graph with denominators printed; the tick-29 gap is the starting coverage boundary, not a clean slate.</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>Additivity proof: diff the ratified sections (C0-C3 / 14 roles / 10 relations / variance) pre vs post -- must be BYTE-IDENTICAL. The live consumer summary_corpus.py must run zero-diff on the current estate after the amendment.</run>
    <expect>Ratified vocab byte-unchanged; summary_corpus.py zero-diff exercised, both on the record.</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>Demonstrate ONE derivation end to end: pick freshness or provenance and show it computed as a D-rail derivation over a real pipeline, with its coverage boundary stated.</run>
    <expect>A worked derivation proving the rails license the queries the PRD claims; blind spots named.</expect></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Rule-bank content is co-canonized (CTO/MSTR per its header); ~Z gates the design, ratified-vocab
changes route to the ratification chain. Shares data/firm_registry.json (read-only; v1 frozen-additive,
~Z gate) for the completeness fold-in. The D-rail vocabulary is the type system TOOLSEM + the R1/R3
coverage declarations are written in -- coordinate the (rail, grain, plane, scope) tuple shape with the
R1R3 output-contract surface (base 0.8.0 owns comp-output-contracts.yaml). No main-fabric coupling.
</cross_domain_coordination>

<acceptance_criteria>
1. D1/D2/D3 authored as additive rule-bank sections, each with vocabulary + populating graph evidence +
   coverage boundary + licensed derivations.
2. Additivity proven: ratified sections byte-identical; summary_corpus.py zero-diff on current estate.
3. PSTMRT P2 completeness axis + variance registry_binding landed with the normalization note.
4. One worked derivation (freshness or provenance) demonstrated with its coverage boundary stated.
5. Forward-declared (unpopulated) rail elements marked LOUD, never silently omitted.
6. Session log + compiler-tools-log line. Route the design to ~Z for the gate before canonization.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z (family charter). Design gate: 1.0.0_SA_CTO~Z BEFORE canonization.</verification>
</task_order>
