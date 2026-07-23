<task_order>
<to_id>NFRA_TOOLARCH.ROUTES</to_id>
<title>comp-routes trace — CONSULT THE REWRITE TABLE IT ALREADY HAS, and DISCLOSE a catch-all fall-through; today trace is UNDISCRIMINATING for the static-rewrite class and answers authoritatively anyway</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~A</issued_to>
<date>2026-07-23</date>
<status>staged</status>
<priority>P1 — small fix, HIGH leverage: it is the blocker on ~B's TOOLBHVR.ROUTE flipping from "no coverage" to a real route, and it closes a live false-authority defect</title></priority>

<authority>
Andrew-direct lineage: the MDPF key-scramble ("you guys should be using comp-cache comp-cluster
comp-trace... to track these paths definitively so we have 100% clarity"); main CTO routed the
CF-static-rewrite gap as a co-equal buildout item (via MSTR 195623Z). SCOPE CORRECTED DOWNWARD by
~D's positive control + ~B's phase-1: this is NOT a capability build -- the table already exists and
`trace` simply never consults it. ~Z gates; CVO~Z verifies. Assigned ~A (just shipped comp-dataflow,
warm on the tool-build path).
</authority>

<the_defect_grounded>
TWO findings, both measured, not asserted:
1. UNDISCRIMINATING (the serious one -- ~D's positive control): `comp-routes trace <url>` falls through
   to the catch-all CloudFront `/*` behavior and returns `Origin: S3-opalinvest-portal` for ANY path --
   a path WITH a known rewrite rule returns BYTE-IDENTICAL output to one without. **An instrument that
   returns the same answer for every input is not an instrument** (CONTROLS_OVER_CARE) -- and because
   the output READS AUTHORITATIVE, it is worse than silence: an agent trusting it gets a false
   resolution. This is the same false-authority class as the stale-key exhibit, in a different tool.
2. THE FIX IS ALREADY HALF-BUILT: `comp-routes rewrites` ALREADY holds the correct table INCLUDING
   `/api/general/json/ -> json/` (the MDPF hop). `trace` just never consults it. So the missing
   capability is a WIRING, not a build.
CONSEQUENCE TODAY (~B's phase-1, 18,014 rail events): there is currently NO tool that resolves a
concrete URL to its S3 key for the static-rewrite class -- which is why ~B's TOOLBHVR.ROUTE is shipping
an honest "no coverage" message instead of a route. This TO turns that into a real route.
</the_defect_grounded>

<scope>
A. WIRE `trace` TO THE `rewrites` TABLE: when tracing a URL/path, consult the rewrite table BEFORE
   falling through to the catch-all, so `/api/general/json/mdpf/global/aggregate-aua-timeseries.json`
   resolves through `/api/general/json/ -> json/` to its actual S3 key. Reuse the existing table --
   do NOT re-derive or hand-copy it (a second copy is the frozen-enumeration class).
B. DISCLOSE THE FALL-THROUGH (the honesty limb, required even where A cannot resolve): when trace
   answers from the catch-all `/*` rather than a matched rule, the output must SAY SO -- e.g.
   "MATCHED: catch-all /* (no specific behavior matched this path) -- this is a DEFAULT, not a
   resolution." An undiscriminating answer must announce that it is undiscriminating. Same pattern as
   the loud-vintage disclosure ~D landed on pipescript; always-on, no suppress flag.
C. CARRY THE R1R3 OUTPUT CONTRACT: coverage line + plane/vintage. State plainly what trace can and
   cannot resolve (Lambda routes vs CF static rewrites vs un-modelled paths).
OUT OF SCOPE: a general CF-behavior modelling capability. If A+B do not fully close the class, NAME the
residual as a capability candidate -- do not silently expand into a build.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>Read comp-routes' rewrites-table source + the trace path; confirm ~D's positive control yourself (trace a path WITH a known rewrite and one WITHOUT -- if the outputs are byte-identical, the defect is reproduced).</run>
    <expect>The undiscriminating behavior REPRODUCED first-hand (never taken on report), with both outputs on the record.</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>THE DISCRIMINATION MUTANT (this is the acceptance): after the wiring, a path WITH a rewrite and a path WITHOUT must return DIFFERENT, CORRECT answers -- the MDPF path must resolve to its real S3 key (json/mdpf/global/aggregate-aua-timeseries.json), and an unmatched path must render the catch-all DISCLOSED. Byte-identical outputs = FAIL.</run>
    <expect>Before/after on the record. The tool that could not discriminate now does, and where it still cannot, it says so.</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>Notify ~B (TOOLBHVR.ROUTE) that the class is now routable so it flips its no-coverage message to a real route; state any residual the class still cannot resolve.</run>
    <expect>~B unblocked or told precisely what remains uncovered.</expect></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
UNBLOCKS ~B (TOOLBHVR.ROUTE) -- ~B's routing is designed to flip from honest-no-coverage to a real
route the moment this lands; notify it directly. Register/declare through base 0.8.0's output-contract
surface (stage-2 validates plane/vintage). The MDPF key TRUTH is DE/COO's -- resolve to it, do not
re-rule it. No main-fabric coupling; read-only tool change.
</cross_domain_coordination>

<acceptance_criteria>
1. The undiscriminating defect REPRODUCED first-hand in phase 1 (both byte-identical outputs shown).
2. Discrimination mutant PASSES: rewrite-path vs non-rewrite-path return different + correct answers;
   the MDPF path resolves to its real S3 key.
3. Catch-all fall-through DISCLOSED always-on (no suppress flag); an undiscriminating answer says so.
4. R1R3 output contract carried (coverage + plane/vintage), stage-2 clean.
5. ~B notified; residual named if the class is not fully closed.
6. Session log + compiler-tools-log line.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z (family charter). Report to 1.0.0_SA_CTO~Z.</verification>
</task_order>
