<task_order>
<to_id>NFRA_TOOLARCH.P1</to_id>
<title>ARCHETYPE CENSUS — dogfood the C0-C3 ladder on the whole estate: which motif families actually recur, per plane, with denominators; state the ontology's own honest coverage boundary</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-07-23</date>
<status>complete</status>
<priority>P1 — TOOLARCH mechanical layer; parallelizable NOW (runs on the ratified C-ladder; P2 pattern inventory waits on ONTOLOGY2 rails)</priority>

<authority>
Andrew-direct 2026-07-23 (NFRA_TOOLARCH charter, verbatim in docs/architecture/NFRA_TOOLARCH_PRD.md
s.0: "use the entire system as dogfood and say, what are the archetypes here?"). ~Z holds TO-authoring
+ direct dispatch for this batch. Constitution: docs/doctrine/INTENT_DENOMINATOR_SYNCHRONIZATION.md.
~Z gates; CVO~Z verifies.
</authority>

<scope>
ANALYSIS, NOT tool-building. Use the EXISTING ratified C0-C3 ladder as the classifier (do not wait for
the ONTOLOGY2 rails -- this census runs on the static rungs; the dynamic-rail typing is P2). Produce an
archetype census of Opal itself:
  A. C0 -- the fact/role distribution: which of the 14 ROLES actually occur, at what frequency, per plane
     (AWS / pipeline / frontend / M365 / records).
  B. C1 -- the relation distribution: which of the 10 RELATIONS (+ composites) carry the live edges.
  C. C2 -- the MOTIF families: which of the ~20 canonical families actually recur, at what recurrence,
     per plane. This is the heart of the census -- the archetypes the estate is MADE of.
  D. C3 -- the SYSTEM distribution: the union-find systems and their motif composition.
EVERY count prints its denominator (population scanned, source per count) -- the census IS an
intent-denominator instrument; a count without its denominator fails by construction.

START FROM THE KNOWN GAP, not a clean slate: CVO~Z's tick-29 census already found 11 live edge types on
NO axis (RENDERS 2447, PROP_PASSES 1382 + 9 wiring types) and 9 declared-but-zero-live-in-plane. That is
the ontology's FIRST honest coverage boundary. The archetype census must state, per plane, where the
C0-C3 ladder does NOT yet cover the live estate -- that boundary is the deliverable's most valuable half
(it is the demand signal for the ONTOLOGY2 rails and the TOOLARCH pattern inventory).

OUT OF SCOPE (P2, waits on ~C's rails): the PATTERN INVENTORY (pattern -> archetype -> instantiating
tools -> gaps) needs the (rail, grain, plane) type system to type a pattern. Do not attempt it here;
name it as the sequenced follow-on.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-kuzu census queries (node_type x role, edge_type x relation, motif-family recurrence, system union-find) at pin==HEAD; read the canonical motif catalog + NFRA_ONTOLOGY_RULE_BANK.yaml</run>
    <expect>Every census axis derived from the live graph with its denominator + vintage printed. Pin the graph vintage (a count without its vintage is not a count -- CVO~Z tick-30 corollary).</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>Coverage-boundary pass: reconcile the census against the tick-29 uncovered-edge set; enumerate per plane where the ladder does not cover the live estate. Cross-check with a SECOND surface where feasible (the tick-29 lesson: one mapping surface under-reads).</run>
    <expect>The uncovered set is derived, not asserted; stated per plane with denominators.</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>Rank the recurring archetypes by frequency x plane-spread; identify the top motif families that a generalized tool would serve.</run>
    <expect>A ranked archetype table feeding TOOLARCH P2 (the pattern inventory) + ONTOLOGY2 (the rail demand).</expect></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Read-only census over the shared graph -- no build conflict with the parallel tool builds (~A R2, ~B
R4R6, base R5). Consumes CVO~Z's tick-29 output; its coverage-boundary deliverable feeds ONTOLOGY2 P1
(~C) as demand signal -- coordinate so the rail authoring and the census reference one uncovered-edge
set, not two. Output to docs/architecture/ (archetype census doc) or the TOOLARCH deliverables folder.
No main-fabric coupling.
</cross_domain_coordination>

<acceptance_criteria>
1. C0/C1/C2/C3 distributions censused per plane, every count with its denominator + graph vintage pinned.
2. The ontology's coverage boundary stated per plane (where the ladder does not cover the live estate),
   derived from + reconciled against the tick-29 uncovered set.
3. A ranked archetype table (recurring motif families x plane-spread) feeding P2 + ONTOLOGY2.
4. P2 pattern inventory named as the sequenced follow-on (blocked on ~C's rails), not attempted here.
5. Session log + compiler-tools-log line.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z (family charter). Report to 1.0.0_SA_CTO~Z.</verification>
</task_order>
