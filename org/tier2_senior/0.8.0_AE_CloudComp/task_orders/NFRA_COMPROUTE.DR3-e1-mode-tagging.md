# TASK ORDER -- NFRA_COMPROUTE.DR3 (E1 fix: manifest mode:query|rebuild tagging)

<issued_to>0.8.0_AE_CloudComp~B</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_COMPROUTE is complete; this TO was last touched 2026-07-01, predating the project close 2026-07-19. Closed as a record act, not a work verdict. Prior status: dispatched</status>
<priority>HIGH -- Andrew-direct default-router. This IS the E1 fix (your validation finding), formalized. CTO BLESSED the hard mode-gate (132556Z). Small + load-bearing: ~E's Stage-A pre-filter reads YOUR tag.</priority>
<date>2026-07-01</date>

## Context
Your E1 finding (report 4e9f0258d): comp-which routes a read question to comp-aws DERIVE (8-min rebuild) because comp_route.py ignores the manifest's mode:query|rebuild tag. CTO BLESSED the HARD mode-gate: a read/navigate/explore intent hard-EXCLUDES mode:rebuild tools (a read routed to a write is a CATEGORY ERROR). This TO delivers the TAG that ~E's Stage-A pre-filter (DR1) consumes -- the concrete E1 fix. (Separate from your E3 comp-drift fix + the addendum re-verify, both already in flight.)

## Objective
Tag every comp-tool in the capability manifest with mode:query|rebuild, grounded in each tool's ACTION-CLASS, so the router can hard-exclude rebuild tools from read intents.

## Scope
1. **mode tag on the manifest:** every comp-tool gets mode: query | rebuild, GROUNDED in its actual action-class (Rule-22 -- read the tool, don't guess): mode:rebuild = writes/mutates/expensive-derive (comp-aws-derive = the 8-min rebuild; any tool whose primary act is a DERIVE/BUILD/WRITE); mode:query = instant read surfaces (comp-kuzu head/state read, comp-grep, comp-glob, comp-blast/trace/xref read-path, etc.). Where a tool has BOTH a query + a rebuild path, tag the ROUTE-TARGET action (the read surface = query; the derive subcommand = rebuild).
2. **Interface align:** the tag schema/location coordinated with ~C (comp-which reads it) + ~E (Stage-A pre-filter reads it). One tag source, both consume.
3. **E1 repro closes:** "what lambdas read bucket X" (+ the other read-question repros in your report) now route to a READ surface (comp-kuzu / query-mode), NOT comp-aws-derive. Reposition comp-kuzu as the instant head/state check (Andrew's framing).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>ground each tool's action-class from source/manifest (not memory) -- which tools DERIVE/WRITE vs READ; confirm the manifest's EXISTING mode field (your report says it exists) or where to add it</run>
    <expect>Every comp-tool classifiable query|rebuild from its actual behavior; the tag field located.</expect>
    <if_mismatch>If a tool's action-class is genuinely dual/ambiguous, tag the route-target action + note it for ~E's pre-filter; do not guess a mode.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>the E1 repro through a mode-aware route (with ~E's pre-filter or a stub): the read question returns a mode:query surface, 0 mode:rebuild; ds-gate + non-ASCII</run>
    <expect>Read intent -> query surface (comp-kuzu etc.); comp-aws-derive EXCLUDED from the read answer. E1 closed.</expect>
    <if_mismatch>STOP. If a read still reaches a rebuild tool, the tag or the pre-filter wiring is wrong -- reconcile with ~E.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~E: Stage-A mode pre-filter (DR1) consumes your tag. Align the tag schema.
- 0.8.0_AE_CloudComp~C: comp-which surface (DR2) reads the tag for routing. Coordinate the mode-tag integration.
- 1.0.0_SA_CTO: BLESSED the hard mode-gate (132556Z). RAVC.
</cross_domain_coordination>

<acceptance_criteria>
1. Manifest mode-tagged query|rebuild for every comp-tool, GROUNDED per-tool action-class (no guess); comp-aws-derive = rebuild; comp-kuzu/grep/glob = query.
2. E1 repro closed: the read question routes to a READ surface, 0 mode:rebuild tools in the read answer (verified with ~E's pre-filter).
3. Tag schema aligned with ~E (pre-filter) + ~C (surface). RAVC COO~B + CC CTO + ~E + ~C.
</acceptance_criteria>

## Note
Small but load-bearing -- your tag is the E1 mode-gate's data. Ground each mode from the tool's real action-class (Rule-22), especially the dual query/rebuild tools. This closes E1, the naturalness HIGH you found.
