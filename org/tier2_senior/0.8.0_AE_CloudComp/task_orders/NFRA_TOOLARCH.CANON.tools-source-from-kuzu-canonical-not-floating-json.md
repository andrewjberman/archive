<task_order>
<to_id>NFRA_TOOLARCH.CANON</to_id>
<title>CANONICAL SOURCE — every comp-tool sources from the comp-kuzu canonical graph projection, NEVER a one-off floating json snapshot; audit + reroute, with the stale pipescript-mdpf key as the exhibit</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-07-23</date>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_TOOLARCH is complete; this TO was last touched 2026-07-25, predating the project close 2026-07-29. Closed as a record act, not a work verdict. Prior status: blocked-on-base-0.8.0 -- 4/5 acceptance criteria DONE, 5th (canonical mdpf refresh) blocked on base-owned dependency, still open as of 2026-07-25 per NFRA_TOOLARCH_CANON_CANON2_STATUS_AUDIT_20260725.md @04d8aacb0</status>
<priority>P1 — Andrew-direct; a live architecture-clarity defect that mis-scopes TOs (the MDPF key scramble tonight)</priority>

<correction date="2026-07-25" by="1.0.0_SA_CTO~Z" citing="3.0.0_SA_CVO~Z RAVC-closed reground @e449615c4, org/tier1_exec/3.0.0_SA_CVO/deliverables/cvoz_NFRA_TOOLARCH_CANON_REGROUND_20260724.md">
  This TO's original scope (below) is PARTIALLY STALE as of 2026-07-24's re-ground. Read the reground
  doc FIRST, in full, before touching this TO. Summary of what changed:
  - **comp-pipescript: KEEP, DO NOT RE-POINT.** The brief's headline claim (MDPF dataflow traced
    through comp-pipescript rides a stale 25-day projection) is REFUTED by exercise: the resolver is
    referenced ONLY inside `_estate_oos_guard()`, a routing guard, not a dataflow/data source. Both
    stale-direction failure modes are loud-or-fall-through, not silent-wrong. Do not reroute it.
  - **estate-coverage-resolver.json: FREEZE, do not regenerate.** `gen-estate-resolver.py:17`
    hardcodes a date-pinned 2026-06-15 census with NO refresh path -- regenerating stamps a fresh
    mtime over a frozen census and destroys `last_review`, the one field currently telling the truth.
    "Just regenerate it" is a trap, not a fix.
  - **comp-stitch-refresh: REMOVE from any floating-json target list.** It is the PRODUCER of
    stitch_graph.json, not a consumer of a floating artifact -- false positive in the original audit.
  - **The true out-of-kuzu set is 9 tools, not 10** (three false positives found across two audit
    passes: comp-manifest-check, comp-graph, comp-stitch-refresh).
  - **The actual live, unattended failure in this cluster** (not in this TO's original scope, and
    higher-value than the audit work below): `stitch_graph.json`'s producer has been hard-failing on
    a tripped GRAIN-SENTINEL guard for 17 days (since 07-08), backgrounded + discarded, nobody
    notified -- independently reconfirmed via NFRA_TOOLUNIFY REC-1 (`REC1_EXERCISE.md`). Look at
    `EXTERNAL_ENDPOINT: count 0 vs baseline 3` FIRST -- a count collapsing to zero smells like a
    broken extractor, not legitimate drift; the other 5 high-side trips look like real 17-day estate
    growth against a stale baseline band and are lower priority.
  **What in this TO's original scope below is UNAFFECTED:** CANON2's graph.json family (7 tools,
  DEFER + re-point-with-mutant disposition) — proceed on that as originally scoped.
</correction>

<authority>
Andrew-direct 2026-07-23 (my terminal), VERBATIM: "I notice that some of these comp-tools actually
rely on floating jsons outside of comp-kuzu canonical which is not acceptable at all... the issue with
these one-off json projections rather than relying on the canonical graph projection in kuzu is a
TOOLARCH TO." Context: COO base, doing opal-data-assets infra work, found pipescript-mdpf reporting a
STALE served key (platinum/mdpf/aggregate_aua_timeseries.json, vintage 2026-06-15, pre-revamp) while
the live renderer serves json/mdpf/global/aggregate-aua-timeseries.json -- the stale map is why the
key-path got mis-chased. ~Z gates; CVO~Z verifies. Assigned ~D (freshest census of the tool/graph
data-source landscape, P1 census just delivered).
</authority>

<the_principle_this_enforces>
This IS the constitution (docs/doctrine/INTENT_DENOMINATOR_SYNCHRONIZATION.md) applied to the tools'
OWN DATA SOURCING. A tool whose data source is a frozen floating-json snapshot has a DENOMINATOR that
is its own configuration -- drifted from the canonical graph (the authority from above) -- exactly the
s.2 defect. comp-kuzu is the single canonical projection (the one denominator); every tool must read
IT, so a tool's answer is never staler than the graph. A per-tool json snapshot is a private
denominator that silently diverges (the pipescript-mdpf underscore-vs-hyphen, month-stale, is the
exhibit).
</the_principle_this_enforces>

<scope>
A. AUDIT (census -- your strength): enumerate every comp-tool that reads a FLOATING JSON (a committed
   or generated .json snapshot) as a data source for graph/path/architecture questions, vs reading the
   comp-kuzu canonical projection. Print the denominator (N tools audited, K reading floating jsons,
   which json each). The pipescript-mdpf thread is the confirmed exhibit; find the rest -- do not stop
   at the one Andrew named (a hand-listed set is the frozen-enumeration defect one layer over).
B. REROUTE (the fix): for each tool reading a floating json, reroute it to source from comp-kuzu
   canonical (or state, with grounding, why a given json is a legitimate non-graph artifact -- e.g. a
   deliberate frozen fixture -- which must then be LOUD about its vintage, not silently authoritative).
   Coordinate any shared-surface / heavy build with base 0.8.0 (integration owner).
C. THE STALE-GRAPH HALF (the exhibit's immediate cause): the pipescript-mdpf thread maps the PRE-revamp
   key. Determine whether that is (i) the tool reading a stale json, or (ii) the canonical graph itself
   stale on the mdpf thread (needs the json/mdpf/global/* keys + the gold-append/portal-overwrite
   two-write reflected). Fix per the finding: reroute (i) and/or refresh the canonical thread (ii). The
   acceptance is that the tool returns the CURRENT served key from canonical, not the month-old one.
D. RELATED COVERAGE GAP (name it, scope decision yours + mine): comp-routes cannot trace a CloudFront
   static /json/* rewrite (only Lambda routes), so no comp-tool gives the full frontend->S3 path for
   MDPF. This is a distinct comp-routes coverage gap COO surfaced. Name it as a sibling item; propose
   whether it folds here or becomes its own TO (my ruling on your recommendation).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>Audit the tool data-source landscape: for each comp-tool, does it read comp-kuzu canonical or a floating json? Use comp-toolgraph / comp-manifest / reading the tool sources. Print the denominator.</run>
    <expect>The floating-json set is DERIVED (every tool checked), not the one Andrew named + a guess.</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>MUTANT / EXHIBIT: after the reroute, pipescript-mdpf (or the fixed tool) MUST return the CURRENT served key (json/mdpf/global/aggregate-aua-timeseries.json), NOT the stale platinum underscore key. Show before (stale) and after (canonical-current) on the record.</run>
    <expect>The exhibit defect is fixed and demonstrated; a re-run reads canonical, not the snapshot.</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>State the residual: any json legitimately kept as a non-graph source (with its loud-vintage justification), and the comp-routes CloudFront-rewrite gap disposition.</run>
    <expect>Residuals named, not silently left.</expect></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Reroute touches tool sources -- coordinate any shared-surface change with base 0.8.0 (integration
owner) and the comp-kuzu refresh model (NFRA_KUZUSPLIT: comp-kuzu-full/inc). If the canonical mdpf
thread needs refreshing, that is graph-derive work -- coordinate with the graph-refresh owner, do not
hand-edit the canonical projection. No main-fabric coupling; the mdpf key TRUTH is DE/COO's (read it,
do not re-rule it).
</cross_domain_coordination>

<acceptance_criteria>
1. Floating-json audit: denominator printed, the full set derived (not hand-listed), each tool's json named.
2. Every floating-json tool rerouted to comp-kuzu canonical OR its json justified as a loud-vintage fixture.
3. Exhibit fixed: the mdpf-key tool returns the CURRENT canonical served key, before/after on the record.
4. comp-routes CloudFront-rewrite coverage gap named with a fold-or-separate recommendation.
5. Session log + compiler-tools-log line.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z (family charter). Report to 1.0.0_SA_CTO~Z; design decisions (reroute-vs-justify, comp-routes fold) to my gate.</verification>
</task_order>
