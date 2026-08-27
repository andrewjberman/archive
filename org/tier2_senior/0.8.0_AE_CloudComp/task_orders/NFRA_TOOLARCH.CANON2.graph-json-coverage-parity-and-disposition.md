<task_order>
<to_id>NFRA_TOOLARCH.CANON2</to_id>
<title>graph.json FAMILY (7 tools -- CORRECTED from 9) — coverage-parity precheck as the DECIDING gate, then re-point OR declare-both; the defect is the UNDECLARED projection, never the second one</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-07-23</date>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_TOOLARCH is complete; this TO was last touched 2026-07-25, predating the project close 2026-07-29. Closed as a record act, not a work verdict. Prior status: leg-A-complete, leg-B-blocked -- Leg A (coverage-parity precheck, all 7 tools) DONE 2026-07-23; Leg B (re-point) blocked on reopening a deferred architectural decision (42b7f3c48a, escalated COO~B/CVO~B/CTO 2026-07-01, never closed) -- see NFRA_TOOLARCH_CANON_CANON2_STATUS_AUDIT_20260725.md @04d8aacb0</status>
<priority>P2 — follow-on to CANON (the ACUTE exhibit is already neutralized by the loud-vintage interim @dcf153915, so this is correctness-not-urgency)</priority>

<authority>
Ruling chain: Andrew-direct 2026-07-23 (floating-json vs comp-kuzu canonical, verbatim in
NFRA_TOOLARCH.CANON authority block) -> CANON audit @fd12a515b identified the graph.json family (9
tools) as ARCHITECTURAL-not-silent, distinct from the acute exhibit -> CTO~Z ruling 204001Z (separate
sibling TO, coverage-parity gated) -> ~D draft @1edfaa2b -> CTO~Z ruling 210601Z (three-outcome design
AFFIRMED + three guards) -> ~D guards folded @54b02122a. FULL SCOPE OF RECORD: the ~D draft
deliverables/NFRA_TOOLARCH_CANON_SIBLING_TO_DRAFT_graph-json-reroute.md @54b02122a -- this TO dispatches
it; the draft carries the leg detail and is not duplicated here.
</authority>

<the_ruling_this_rests_on>
>> THE DEFECT IS THE UNDECLARED PROJECTION, NOT THE EXISTENCE OF A SECOND ONE. << A silent frozen
snapshot that drifts and answers with false authority is the constitution's s.2 defect (the acute
exhibit, already fixed). A DECLARED, loud-vintage, self-invalidating projection answering a question
comp-kuzu structurally CANNOT answer is a legitimate second instrument with honest provenance (the
accepted nerves-risk-edges model). Grounded risk from ~D's own P1 census: kuzu = resource/estate graph;
trace_graph = source-level call/import/dataflow; census R-0 (records plane absent) + 0/8 frontend+M365
canonical C2 families materialized => "kuzu is canonical" does NOT entail "kuzu covers the structure
tools' questions." A forced re-point could trade a COMPLETE-but-self-invalidating source for a
CANONICAL-but-INCOMPLETE one -- a coverage REGRESSION, which is worse for the asking agent and is not
what the directive intends.
INTERPRETIVE NOTE (on the record): Andrew's words were "not acceptable at all"; CTO~Z reads that as
NO-SILENT-PROJECTION, not literally-one-projection-ever, and flagged the reading to Andrew directly. If
he means the stricter reading, outcome 3 becomes an ESCALATION path instead of a landing and this TO
re-cuts small -- guards 1-3 survive unchanged either way.
</the_ruling_this_rests_on>

<scope>
LEG A -- COVERAGE-PARITY PRECHECK (BLOCKING and DECIDING; nothing re-points before it).
  Per tool, does comp-kuzu cover the question that tool asks of graph.json? Print denominators.
  THREE LEGITIMATE OUTCOMES:
   (1) parity holds -> RE-POINT to canonical.
   (2) fails-but-closable -> EXTEND kuzu coverage first, then re-point.
   (3) fails STRUCTURALLY (genuinely different question at a different grain) -> DO NOT re-point;
       DECLARE BOTH projections for that tool. This is a LEGITIMATE LANDING, not a failure.
LEG B -- RE-POINT (only the tools that landed outcome 1/2).
LEG C -- OUTPUT-CONTRACT RE-DECLARE (base 0.8.0 OWNS this leg; base's own catch): re-pointing CHANGES
  a tool's declared plane/vintage, and stage-2 (@c716d963e) VALIDATES it -- so every re-point carries a
  contract update or it blocks at the gate. That stage-2 caught this coupling BEFORE the work started
  is the enforcement working as designed; record it that way.
LEG D -- VERIFY (per tool: the answer is correct AND has not shrunk).

PILOT SEQUENCING -- ORIGINAL PAIR VOID, RE-SELECTED (~D correction @13c9d0f45, CTO~Z approved):
comp-manifest-check + comp-graph were FALSE POSITIVES of the audit scan and are NOT graph.json readers
-- comp-manifest-check is the LINTER THAT ENFORCES THIS RULE (its only graph.json occurrences are a
docstring + the lint-rule MESSAGE STRING at :216; targeted grep for open/json.load/read_text = ZERO
hits -- the scan counted RULE TEXT as a data source and flagged the ENFORCEMENT as the violation, the
same text-matching-prose defect TRIGGER_LAYER clause 2 forbids and that voided R6's AC-3). comp-graph
merely stats graph.json for AGE exactly as it stats kuzu (:151 vs :214-219) -- referencing both is its
job. CORRECTED SET: 7 tools -- comp-blast/build/diff/trace/xref (via cli.py), comp-gitdrill
(TraceGraph.load :60), comp-surface-check (:453 default); all seven individually ground-verified.
RE-SELECTED PILOT: comp-surface-check FIRST (it already PARAMETERIZES its source, --current :830
defaulting to graph.json, so the re-point is a source-option change not surgery, and it still proves
the leg shape); comp-gitdrill SECOND (single explicit TraceGraph.load); the cli.py FIVE move together
as ONE change, LAST.
</scope>

<guards>
All three are ACCEPTANCE-5 machine-checkable FAILs, not prose (~D folded @54b02122a):
1. STRUCTURAL PROOF REQUIRED per tool -- outcome 3 fires only on GROUNDED evidence that the questions
   differ at grain/plane, NEVER on "the re-point is hard." Name the un-coverable question + its census
   evidence. (Closes the lazy exit.)
2. DECLARED MEANS ENFORCED -- a retained projection must be LOUD-VINTAGE (nerves model) AND registered
   in the output contract with plane/vintage so stage-2 machine-validates it. >> A projection declared
   only in PROSE is UNDECLARED by this program's own standard. << (This is what separates a real second
   instrument from a rationalization.)
3. OUTCOME 3 EMITS AN OWNED ITEM -- "kuzu does not cover <question>" is a FINDING filed per
   TRIGGER_LAYER (owner + severity) as a kuzu/ontology coverage-extension candidate. Without it,
   outcome 3 freezes a gap with a clean conscience -- this defect class one layer up.
</guards>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>Leg A per tool: enumerate the question each of the 9 asks of graph.json, and whether kuzu covers it. Denominators printed; census evidence cited per outcome-3 candidate.</run>
    <expect>Every tool lands an outcome (1/2/3) with grounding; no tool is dispositioned by assertion.</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>MUTANT: for each re-pointed tool, prove the answer did not SHRINK **IN EITHER DIMENSION** -- an answer that shrinks is a FAIL, not an improvement (~D's line, kept), AND **CURRENCY IS THE SECOND DIMENSION** (~D triage @2b620f361): source_sha powers check_node_freshness -> rebuild-on-source-drift, which IS the family's 'always-current-vs-source' guarantee; a kuzu re-point inherits BUILD-currency instead. So an answer can keep its full coverage and still regress by going STALER. 'Shrinks' covers coverage AND currency. PLUS THE ADAPTER MUTANT (mandatory, ~D): the projections share only LAMBDA -- trace_graph types COMPONENT/GOLD_SCRIPT/... vs kuzu ReactComponent/Component/PipelineScript/...; cli.py holds LITERAL node_type=="COMPONENT"/"GOLD_SCRIPT" comparisons that match NOTHING against kuzu and return an EMPTY RESULT, not an error (blast renders 'no downstream consumers', xref 'no matches' -- confidently, with nothing). Any re-point needs a type-name ADAPTER, and the adapter needs ITS OWN MUTANT: a KNOWN-PRESENT node that MUST resolve. Without it the adapter is undetectably wrong. For each outcome-3 tool, prove the declaration is machine-visible to stage-2 (guard 2), not prose-only.</run>
    <expect>Both on the record. A re-point that silently narrows coverage is the regression this TO exists to prevent.</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>State the final disposition table (tool -> outcome -> evidence) + every owned finding filed under guard 3.</run>
    <expect>Disposition complete; no tool left undispositioned; gaps owned not frozen.</expect></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
LEG C is base 0.8.0's (integration owner, output-contract surface). Coordinate the pilot pair with base.
Sequenced AFTER / independent of the CANON exhibit reroute (which awaits the stitch/canonical refresh,
base-routed) -- these are different projections and must not be conflated. No main-fabric coupling.
</cross_domain_coordination>

<acceptance_criteria>
1. Leg A complete: all 7 tools dispositioned 1/2/3 with printed denominators + per-tool grounding.
2. Re-pointed tools verified: correct AND not shrunk (mutant-proven).
3. Outcome-3 tools: structural proof (guard 1) + machine-visible declaration passing stage-2 (guard 2)
   + an owned TRIGGER_LAYER finding filed (guard 3).
4. Leg C output-contract updates landed with base for every re-point.
5. Session log + compiler-tools-log line.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z (family charter). Report to 1.0.0_SA_CTO~Z; any ratified/standard-level implication to my gate.</verification>
</task_order>
