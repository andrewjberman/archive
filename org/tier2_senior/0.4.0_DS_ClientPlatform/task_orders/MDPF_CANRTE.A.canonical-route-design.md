<task_order>
<to_id>MDPF_CANRTE.A.canonical-route-design</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-04</date>
<status>complete -- CLOSED 2026-08-05 ~2350Z (2.0.0_SA_COO). Phase A design COMPLETE @ab2d2f167 (verified: commit exists, matches title). Superseded by execution: Phase B is now EXECUTING per org/projects/MDPF_CANRTE.json. Surfaced by 0.4.0_DS_ClientPlatform's backlog triage.</status>
<priority>P0 (Andrew-direct at YOUR terminal ~06:00Z @f9952d616f -- "Your next task for tomorrow"; program GO ~13:07Z @ff160d0b5; seating gate discharged by TIGHT SCOPE @86f52bdfb)</priority>

<title>MDPF_CANRTE Phase A -- canonical per-firm route DESIGN: one route, one grammar, fork recommendations with evidence (design-only; no serve-path or deployed-script contact)</title>

<context>
Andrew's words are the spec (verbatim @f9952d616f, your own record): "this process should be
exactly the same for every single firm, going through exactly the same steps in exactly the same
way... Your next task for tomorrow is going to be simplifying these to a canonical route for all
firms."

GOVERNING ARTIFACT: docs/architecture/MDPF_CANONICAL_ROUTE_SCOPE.md (TIGHT SCOPE v0.1,
@86f52bdfb) -- READ IT FIRST AND WHOLE. This TO is deliberately thinner than the scope doc; on
any perceived conflict, the scope doc wins and you surface the conflict rather than adjudicate.

THE WALLS (carried verbatim from the scope + CTO 131710Z -- each is a hard boundary):
- ETFS-CANON SEAM: fork F-1 (49f DDB custody detour) is ADJACENT to the ETFS canon question
  (which DynamoDB table / S3 location is canonical -- a SEPARATE Andrew P0 at 0.7.0) and MUST
  NOT adjudicate it -- your F-1 recommendation names its boundary with ETFS CANON explicitly,
  or the fork escalates.
- DOWNSTREAM TAIL UNTOUCHED: spine.json -> aum_metrics -> accrual bridge -> platinum is already
  uniform -- out of scope entirely.
- NO SERVE-PATH OR DEPLOYED-SCRIPT CONTACT until Phase C is ratified. Phase A is DESIGN-ONLY:
  your deliverable is a document, not a code change. Zero commits under data/.
- TODAY'S MDPF_GLOBAL EXECUTION RUNS INDEPENDENTLY (09:00/10:00 ET checkpoint loads, gate cut,
  Leg B, emitter bundle) -- the canon-route work neither waits on it nor touches it.
- json/mdpf/* teardown stays PARKED; the hyphenated account-distribution.json is the LIVE
  SERVED portal bell (4-way name collision -- match full bucket + key before citing anything
  near that name).
</context>

<scope>
Phase A (now): the canonical-route DESIGN --
1. One feeder-shape ruling per leg class, one path grammar, one naming rule (aum_metrics vs
   aum-metrics and the split builder homes die here, on paper first).
2. Disposition EVERY divergence: the four census divergences from your @f9952d616f distillation
   (49f DDB custody detour · cottonwood-only tabular gold dim · inflection direct-silver spine
   leg · naming/grammar residue) PLUS candidate #5 from the scope's own io run (SS6): the
   cross-firm hardcoded read -- gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json
   inside the nominally-49f builder [INFERRED from the io manifest; YOUR Phase-A adjudication
   confirms or refutes it at source].
3. Fork RECOMMENDATIONS with evidence (CTO rules; sovereign-class residue to Andrew):
   F-1 DDB-walk vs retired (with the explicit ETFS-CANON boundary statement) ·
   F-2 dim-for-all vs spine-direct · F-3 Model-B one firm-parameterized builder vs per-firm
   scripts.
4. The TWO BANKED CONSTRAINTS ride every recommendation: C-1 the 49f Andrew-canonical custody
   ruling gets an EXPLICIT generalize-or-supersede disposition (never silently dropped); C-2 a
   Model-B recommendation carries the comp-pipescript cross-tree blindness fix in its scope
   line (no canon route the drift instrument cannot see) -- C-2 coordination with the graph
   stream routes THROUGH CTO per anti-chatter, never directly.
5. WRITES ENUMERATED BY SOURCE READ for every builder in the route: the extractor reports
   "WRITES: none detected" on dynamic keys -- treat that as UNKNOWN, never zero; your design
   states each builder's writes from reading its source, cited file:line @ commit.
Phase B (migration-plan design, same seat, NO new seating) begins ONLY after CTO's fork rulings
land -- sequenced cutover, parity gates (DELTA=0 class), serve-freeze windows, rollback. Do not
start B on your own clock; the fork rulings are the gate.
0.2.0_DS_PortfolioAnalytics is a NAMED CONSULT (fold owner) -- a coordination touch on the fold
seams, not a seat; keep it scoped.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before design">
    <step>
      <run>comp-pipescript io &lt;each spine builder in the route&gt; --pipeline mdpf   (one run per builder; the scope's own run on dim_mdpf_aggregate_aua_timeseries is your format reference)</run>
      <expect>READS/WRITES manifest captured per builder. Where the tool cannot see (assets-tree gaps, dynamic keys -- the C-2 blindness), you hand-derive from source and CITE AS HAND-DERIVED file:line @ commit -- never present a tool gap as an empty result.</expect>
      <if_mismatch>A builder the tool cannot address at all is ITSELF Phase-A evidence for C-2 -- record the exact rc + invocation, hand-derive, continue.</if_mismatch>
    </step>
    <step>
      <run>comp-estate mdpf   (read the provenance header before trusting thread names)</run>
      <expect>The mdpf thread's producers->served->frontend chain as the tool sees it; discrepancies vs your census are design inputs, not blockers.</expect>
      <if_mismatch>UNKNOWN VINTAGE header = freshness unverifiable -- refresh or mark the read as such in the design doc.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before submitting the design">
    <step>
      <run>self-audit: every causal claim and every divergence disposition in the doc carries file:line @ commit-ish (Rule 22 -- a causal claim without grounding is INFERRED and cannot authorize a fork recommendation)</run>
      <expect>Zero ungrounded dispositions; candidate #5 explicitly CONFIRMED or REFUTED at source; every INFERRED remainder labeled INFERRED.</expect>
      <if_mismatch>STOP. Ground it or label it -- an ungrounded fork rec gets refused at CTO's desk and costs the round-trip.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after submitting">
    <step>
      <run>deliver the design doc path + fork recs to COO + CTO (program triangle only -- no broadcast); flip this TO's status per protocol</run>
      <expect>CTO has what he needs to rule F-1/F-2/F-3 without a follow-up evidence request.</expect>
      <if_mismatch>REWORK per CTO's redline; the fork rulings are Phase B's gate, so evidence gaps here stall the whole program.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Anti-chatter is a WALL (scope SS7): all program traffic runs COO &lt;-&gt; CTO &lt;-&gt; you. 0.2.0_DS
consult touches are scoped to the fold seams. Cross-stream needs (e.g. C-2's comp-pipescript
fix, which lives in the CVO/graph stream) route THROUGH CTO on a real dependency only. Your own
in-flight MDPF_GLOBAL work (EMIT-2 residual, T4.A residue, scheduled-advance reads) is the
OTHER stream at your own seat -- keep the artifacts separate; canon-route design cites census
evidence, it does not fold live-execution state.
</cross_domain_coordination>

<acceptance_criteria>
Scope SS5 is the program-level bar; this TO's Phase-A slice:
1. Design doc: ONE canonical route (leg classes, one path grammar, one naming rule); all FIVE
   divergence candidates dispositioned with source citations; writes-by-source-read table per
   builder (extractor-blind writes named as such).
2. F-1/F-2/F-3 recommendations, each evidence-grounded; F-1 carries the explicit ETFS-CANON
   boundary statement; C-1 disposition explicit; C-2 rider present on any Model-B rec.
3. Zero code changes, zero serve-path contact, zero data/ commits -- design only.
Plus: session log includes a Compiler Tools section reproducing every <run> with observed
output and explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="scope">docs/architecture/MDPF_CANONICAL_ROUTE_SCOPE.md @86f52bdfb (GOVERNING -- read whole, it wins conflicts)</ref>
  <ref type="authority">Andrew-direct @f9952d616f (your record, the spec) + program GO @ff160d0b5 (CTO terminal)</ref>
  <ref type="census">your divergence census + distillation @f9952d616f</ref>
  <ref type="project">org/projects/MDPF_CANRTE.json (registered @86f52bdfb)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
