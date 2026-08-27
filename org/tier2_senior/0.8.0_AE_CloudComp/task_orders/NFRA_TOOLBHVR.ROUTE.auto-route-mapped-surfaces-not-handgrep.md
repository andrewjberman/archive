<task_order>
<to_id>NFRA_TOOLBHVR.ROUTE</to_id>
<title>AUTO-ROUTE MAPPED SURFACES — an agent asking about a surface we have ontologically mapped must be carried to the comp-tool, not left to hand-grep; strengthen the behavioral routing so infrastructure/architecture-path questions never dead-end in raw grep/aws</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~B</issued_to>
<date>2026-07-23</date>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_TOOLBHVR is complete; this TO was last touched 2026-07-23, predating the project close 2026-07-29. Closed as a record act, not a work verdict. Prior status: staged</status>
<priority>P1 — Andrew-direct; a persistent anti-pattern that causes mis-scoped TOs with incomplete data (the MDPF key scramble tonight)</priority>

<authority>
Andrew-direct 2026-07-23 (my terminal), VERBATIM: "we need better behavioral logic because CLEARLY
its not good enough if this is still happening where we have ontologically defined clear surfaces that
are not being automatically mapped to when agents are looking for information on surfaces we
extensively have mapped, aka this would be a TOOLBHVR TO." And, on the incident: "They should never be
fucking doing that given that we have tools that literally handle this." Context: COO base hand-grepped
Lambda code + `aws s3 ls` for the MDPF served-key path when comp-cache / comp-trace / pipescript /
comp-cluster trace it definitively -- and the hand-grep produced an incomplete, mis-scoped read. ~Z
gates; CVO~Z verifies. Assigned ~B (the behavioral lane; R4R6 live-arm is gated to a non-serve window,
so capacity is available now).
</authority>

<the_principle_this_enforces>
This is the constitution (INTENT_DENOMINATOR_SYNCHRONIZATION.md) on the BEHAVIORAL axis. The agent's
INTENT (find the architecture path) must be carried to the canonical DENOMINATOR (the mapped graph, via
the comp-tools). A hand-grep is intent NOT reaching the denominator -- it substitutes a private,
connection-blind raw-text denominator for the mapped one, and mis-scopes the answer. The behavioral
layer's whole job is to close that gap: intent -> the mapped surface, automatically.
</the_principle_this_enforces>

<scope>
NOW (buildable on the existing rail/HUD, does not wait on the full stack):
A. STRENGTHEN THE ROUTING for the class that failed: infrastructure / architecture / serving-PATH
   questions ("what serves this key", "which S3 key does this FE URL resolve to", "what is the full
   path from renderer to artifact", "what feeds this pipeline"). When an agent reaches for raw grep on
   Lambda/infra code or `aws s3 ls` to answer one of these, the behavioral surface (HUD nudge / rail)
   must catch it and route to the definitive tool (comp-cache for the FE leg, comp-trace / comp-routes
   for serving path, pipescript <thread> for the estate path, comp-cluster for related surfaces). The
   current rail catches SOME raw aws/grep but Andrew's verdict is it is "not good enough" -- find why
   this class slipped and close it. Print the denominator (how many infra-path raw-greps in the rail
   log went un-routed).
B. MAKE HAND-GREPPING A MAPPED SURFACE THE JUSTIFIED EXCEPTION, not the reflex. The rail already gates
   raw aws-inspection + infra-grep; extend/strengthen so a path-tracing hand-grep on a mapped surface
   is caught with a route to the tool that answers it, not just a generic nudge.

DESIGN (the full behavioral model, binds to the layers below as they land):
C. The query-type -> mapped-surface -> auto-route model is the TOOLBHVR<->TOOLSEM seam: TOOLSEM types
   the query to the surface it needs; TOOLBHVR carries the agent there. Design the routing so it plugs
   into TOOLSEM's (rail,grain,plane,scope) typing when it lands, rather than a parallel hardcoded map.
D. THE HONEST DEPENDENCY (state it, do not paper over it): agents partly hand-grep BECAUSE the mapped
   surface was STALE (tonight: pipescript-mdpf served a month-old key). A behavioral push toward a
   stale tool is worse than grep. So this TO is COMPLEMENTARY to NFRA_TOOLARCH.CANON (~D, canonical
   data sourcing): the behavioral fix routes agents to the tool; the CANON fix makes the tool current.
   Coordinate -- do not ship a routing that sends agents to a surface CANON has not yet made current;
   sequence the strengthened routing to land WITH or AFTER the surface it routes to is trustworthy.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>Read org/mcp/comp-which-rail.log for the infra-path raw-grep/aws-override class: how many path-tracing questions were hand-grepped vs routed, and WHY the rail did not catch them. Enumerate the existing behavioral surfaces (HUD hook, rail gate, comp-which) -- reuse, do not invent a new one.</run>
    <expect>The un-routed infra-path class is DERIVED from the rail log with a denominator, and the specific gap (why this class slips) is named.</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>MUTANT/EXERCISE: replay the actual COO incident shape -- a raw grep on Lambda code + `aws s3 ls` for the MDPF served-key path. The strengthened routing MUST catch it and route to comp-cache/comp-trace/pipescript, not let it through. Show before (un-routed) and after (routed) on the record.</run>
    <expect>The incident shape is caught by the new routing; a legitimate non-mapped-surface search still passes (no over-blocking -- the rail's own escape discipline).</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>Report the routing coverage delta and the TOOLSEM-seam design; state the CANON coordination (routing does not point at a surface not yet made current).</run>
    <expect>Coverage delta measured; the design plugs into TOOLSEM; the CANON sequencing stated.</expect></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
COMPLEMENTARY to NFRA_TOOLARCH.CANON (~D): route agents to the tool (this TO) + make the tool current
(CANON). Coordinate directly with ~D so the strengthened routing never points at a surface CANON has
not yet made trustworthy. Seams into TOOLSEM (query typing) -- design to plug in, do not hardcode a
parallel map. The rail/HUD is a shared surface (all agents) -- an over-aggressive route trains bypass
(the BL-1 skim-death); keep the rail's escape discipline. A behavioral-STANDARD change (rail gate
semantics) routes to main CTO per the R1R3/M3 carve; strengthening coverage within the existing rail is
yours. No main-fabric coupling.
</cross_domain_coordination>

<acceptance_criteria>
1. The un-routed infra-path raw-grep class derived from the rail log with a denominator + the gap named.
2. Strengthened routing catches the COO incident shape (mutant-proven before/after) without over-blocking legitimate non-mapped searches.
3. The TOOLBHVR<->TOOLSEM seam designed (routing plugs into query-typing, not a parallel hardcode).
4. CANON coordination stated: the routing does not point at a surface not yet made current.
5. Any rail-gate STANDARD change routed to main CTO; coverage-strengthening landed within the existing rail.
6. Session log + compiler-tools-log line.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z (family charter). Report to 1.0.0_SA_CTO~Z; standard-level rail changes to main CTO's gate.</verification>
</task_order>
