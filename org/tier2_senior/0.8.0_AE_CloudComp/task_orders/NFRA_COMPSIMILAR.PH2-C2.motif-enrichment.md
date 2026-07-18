<task_order>
<to_id>NFRA_COMPSIMILAR.PH2-C2</to_id>
<title>C2 motif enrichment of the per-ARN summary — deterministic classify_motif() splicing canonical MOTIF CLASS + ROLE into derive_summary's output (read FROM canon-patterns; no invented tokens)</title>
<issued_by>0.8.0_AE_CloudComp (base) — dispatched on Andrew-direct</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-07-18</date>
<status>pending</status>
<priority>P2. Andrew-direct GO on the build (2026-07-18). Mechanism (Part A) is UNGATED — build now. Label binding (Part B) activates on CTO landing canon-patterns roles: (graceful — see scope).</priority>

<authority>
Andrew-direct, in-session to base 2026-07-18 (VERBATIM): "C2 is fine to build, dispatch it to ~D."
Preceded by (all VERBATIM in the design-of-record @5c1d828db): (1) the PH2 motif-enrichment design input
(MSTR relay 015015Z); (2) "its a class thing yes, but if you recall, its a class that is decomposable with
full fidelity, therefore should be possible to identify c2 and c3 membership in the summary"; (3) the
NFRA_ONTOLOGY charter that HOLDS C3. CTO GO'd the C2 framing + set the binding vocab-governance (ACK
021711Z). MSTR RAVC-closed the feasibility (021349Z).
</authority>

<gate>
Part A (the mechanism) has NO gate — Andrew GO'd the build; CTO GO'd the framing. Build immediately.
Part B (the role-LABEL strings appearing in the summary) reads canon-patterns.yaml's roles: field, which is
CTO-owned and does not exist in v0.1 yet. This is NOT a build blocker: the enricher reads the field and emits
NO clause for any position lacking a blessed label (same no-guess discipline as UNKNOWN-thin), so the
mechanism ships now and the clauses light up automatically when CTO lands roles: (proposed shape @5c1d828db;
CTO confirms the exact set at your arch-gate). C3 (system membership) + the Twin/Fork-Shadow labels are OUT
OF SCOPE — held to NFRA_ONTOLOGY (do NOT build them here).
</gate>

<scope>
  1. classify_motif(node, in_edges, out_edges) — a per-node DETERMINISTIC structural matcher over the SAME
     local neighborhood derive_summary already loads (summary_corpus.py:256). Match the node's structural
     position (its node_type + the edge directions/neighbor types it occupies) against the canon-patterns.yaml
     motif shapes; return the matched (CLASS, role-key). NO new full-corpus scan on the single-ARN path (keep
     the 2-query --describe cost). NO call into canon_motif_scorer.py (that is a class-CENSUS tool answering a
     different question — you are decomposing to node grain, which is lossless per the scorer_contract's
     per-pattern instance census, Andrew-direct-2).
  2. LABEL BINDING (governed): read the role LABEL from canon-patterns.yaml's per-class roles: field (a new
     CTO-owned field; proposed shape @5c1d828db). READ FROM THE FILE — do NOT hardcode a label dict. A matched
     position whose canon role label is absent -> emit NO clause (never invent a token). Blessing a label ==
     a CTO edit to canon-patterns.
  3. SPLICE: extend derive_summary's prose (and, where it aids similarity, the tokens) with
     "instantiates <CLASS> as <role>" for each matched+labeled position. Because this enriches derive_summary's
     OUTPUT, it lands in the shipped --describe surface (@ff21627b0) with ZERO surface change, and later flows
     into --neighbors the same way.
  4. COVERAGE: extend the coverage denominator (reuse the UNKNOWN-thin control) — "N of M nodes matched >=1
     motif; K unmatched (no motif clause)".
  Instance-grain sourcing (build-notes @5c1d828db): SERVED_LINEAGE from the canonical graph (SERVED_FROM/
  FLOWS_TO modeled) is the FIRST class to land — its roles are structurally derivable today. DEPLOY
  (code-runner) is bucket-grain on the canonical DB (code/-prefix grain needs deploy-ledger/pipescript);
  AUTH's defining TRIGGERS edge is unmodeled (sources from comp-routes behavior). Land SERVED_LINEAGE first;
  the others follow as their instance-grain source is wired — each gated only by that source, not by feasibility.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>read summary_corpus.py (derive_summary:256 + SummaryDoc + coverage) and canon-patterns.yaml; comp-manifest-check (baseline)</run>
      <expect>the enrichment slots into derive_summary's existing SummaryDoc/prose path (no new executable expected — it enriches an existing engine); manifest baseline green so any registration delta is visible.</expect>
      <if_mismatch>STOP. If a new registered surface IS needed, follow the COMPCLOSE invariant (tools_index co-land = exec/COO SoD) before committing a new comp-*.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>summary_corpus.py --self-test WITH a NEW DETERMINISM MUTANT: assert that a structural position whose role label is NOT in canon-patterns roles: produces NO spliced token (the no-invented-token control), and that a blessed label DOES splice.</run>
      <expect>self-test PASS including the new mutant. A build that could splice a token absent from canon-patterns FAILS the mutant — that is the discriminating determinism/governance test, not a vacuous pass.</expect>
      <if_mismatch>STOP. The no-invented-token control is the binding governance guarantee (CTO 021711Z) — fix before commit.</if_mismatch>
    </step>
    <step>
      <run>EXERCISE --describe against a live ARN with a known motif (e.g. an opal-data-* served bucket — Andrew's opal-data-bd example) after canon-patterns roles: is blessed; or, pre-blessing, confirm graceful no-clause.</run>
      <expect>the motif clause ("instantiates <CLASS> as <role>") renders in --describe output with zero surface change once roles: is blessed; pre-blessing, no clause + no error (graceful degrade).</expect>
      <if_mismatch>STOP. A clause off an unblessed/guessed label, or a crash on an absent roles: field, is a defect.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
canon-patterns.yaml is CTO-OWNED — you READ it (roles: field), you do NOT edit it; CTO blesses/lands the
roles: vocabulary (Part B). Coordinate with CTO (base is relaying the proposed shape @5c1d828db + that roles:
is now on the build critical path). Composes with NFRA_COMPSIMILAR.PH2 (the supersede-mode engine, also ~D):
both touch summary_corpus.py — sequence your edits so the motif enrichment and the BM25/--supersede engine do
not collide in the module (MCP each other / land in coordinated commits). C3 (system membership) + Twin/
Fork-Shadow are HELD to NFRA_ONTOLOGY — do not build them here. base FEEDS the (class,role)-mapping
walkthrough on pickup.
</cross_domain_coordination>

<acceptance_criteria>
1. classify_motif deterministically maps a node's structural position -> (CLASS, role-key); role LABEL is READ
   FROM canon-patterns roles: (not hardcoded); a position with no canon label -> NO clause (machine-checkable
   via the self-test determinism mutant).
2. self-test PASS incl. the new no-invented-token mutant (a splice of an off-canon token -> self-test RED).
3. derive_summary prose carries "instantiates <CLASS> as <role>" for matched+labeled positions; --describe
   renders it with zero surface change (exercised against a live ARN once roles: is blessed; graceful
   no-clause pre-blessing).
4. Coverage denominator prints N matched >=1 motif / K unmatched.
5. C3 (system membership) + Twin/Fork-Shadow labels are NOT present (held to NFRA_ONTOLOGY).
6. Session log reproduces each mandate run (observed vs expect) + the compiler-tools line.
SERVED_LINEAGE lands first (structurally derivable today); DEPLOY/AUTH/PIPELINE roles follow as their
instance-grain source is wired.
</acceptance_criteria>

<references>
  <ref type="design">org/tier2_senior/0.8.0_AE_CloudComp/deliverables/COMPSIMILAR_PH2_MOTIF_ENRICHMENT_DESIGN_20260718.md @5c1d828db (spec, feasibility, proposed roles: vocabulary)</ref>
  <ref type="engine">org/modules/graph/debtscan/summary_corpus.py:256 (derive_summary — the enrichment point); --describe shipped @ff21627b0</ref>
  <ref type="canon">org/modules/graph/canon-patterns.yaml (CTO-owned; the roles: field to read)</ref>
  <ref type="prd">docs/architecture/NFRA_COMPSIMILAR_PRD.md</ref>
  <ref type="gate">CTO C2 framing-GO + vocab-governance ACK 20260718T021711Z</ref>
  <ref type="held">C3 + Twin/Fork-Shadow -> NFRA_ONTOLOGY (Andrew-direct 3, awaiting charter-shape)</ref>
</references>
</task_order>
