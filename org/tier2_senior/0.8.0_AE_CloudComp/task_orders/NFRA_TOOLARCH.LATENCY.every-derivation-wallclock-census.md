<task_order>
<to_id>NFRA_TOOLARCH.LATENCY</to_id>
<title>LATENCY CENSUS — run EVERY derivation of EVERY comp-tool, record output + wall-clock, and classify what is instantaneous / heavy-but-fixable / heavy-by-necessity; the FAST half of the mechanical layer has never been measured</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~B</issued_to>
<date>2026-07-23</date>
<status>staged</status>
<priority>P1 — Andrew-direct; closes the unmeasured half of the mechanical layer</priority>

<authority>
Andrew-direct 2026-07-23 (my terminal), VERBATIM: "actually running every single derivation of every
comp-tool and recording outputs somewhere as well as marking wall-clock on each. We want to be able to
know what items are actually big jobs, because we want to try and scope and organize these things in a
manner where they are relatively instantaneous on time unless its literally something like a comp-kuzu
full where theres nothing that can be done about it."
WHY IT MATTERS TO THE PROGRAM: Andrew's original mechanical framing (NFRA_MSBEFF s.0) was "how the
tools get their data and it has to be FAST and reliable." The audit measured RELIABLE (~0.87% true
failure) and COVERAGE (the top defect class) -- but LATENCY was never measured at all. This is the
unmeasured half of the layer. ~Z gates; CVO~Z verifies. Assigned ~B (just closed ROUTE; demonstrated
census discipline on 18,014 rail events and, critically, the SAFETY instinct this job needs).
</authority>

<safety_design_read_this_first>
RUNNING EVERY DERIVATION IS NOT A SAFE DEFAULT. Before any execution:
1. CLASSIFY EVERY DERIVATION read-only vs MUTATING/EXPENSIVE **from source**, and record the
   classification. NEVER execute a derivation classified mutating as part of the census -- record it
   as NOT-RUN with its reason and (where known) a documented expected cost. Mutating/expensive
   includes: anything that rebuilds a graph or index, writes/derives artifacts, deploys, invokes,
   triggers, or mutates AWS/DDB/S3 state.
2. AWS-TOUCHING derivations: read-only AWS calls are permitted but SEQUENCE AWAY from the live
   main-fabric serve window; if any is rate-limit-sensitive or costly, record it NOT-RUN rather than
   risk it. Nothing in this census may perturb a live pipeline.
3. TIMEBOX each run (name the ceiling, e.g. 120s) and record a TIMEOUT as a first-class result -- a
   derivation that exceeds the box IS the finding, not an error to retry into.
4. Run in an ISOLATED worktree where any derivation could touch tree state (the two-axis isolation
   mandate from the R4R6 incident: own worktree AND no shared-hook wiring).
IF IN DOUBT ON A DERIVATION, DO NOT RUN IT -- record it as NOT-RUN with the reason. An unrun
derivation that is honestly recorded is a finding; a fired mutation is an incident.
</safety_design_read_this_first>

<scope>
A. ENUMERATE the derivation surface FROM THE REGISTRY at run time (tools_index / entries /
   subcommands), never a hand-list -- print the denominator (N tools x M derivations). A hand-listed
   surface is the frozen-enumeration class this program exists to close.
B. RUN every read-only derivation (per the safety design). RECORD PER DERIVATION, durably:
   tool · derivation/subcommand · wall-clock ms · exit code + its contracted class (PASS/VERDICT/
   REFUSE/FAIL per comp_output_contract) · output size · output digest · the output itself (or a
   bounded capture + path to the full artifact) · run vintage · host/context.
   Artifact home: a structured file (jsonl preferred -- it is re-derivable and diffable) in the
   deliverables tree; state the path in your report.
C. CLASSIFY each derivation into a latency band and, for everything above "fast", a DISPOSITION:
     INSTANTANEOUS / FAST / SLOW / HEAVY, and for SLOW+HEAVY:
       - HEAVY-BY-NECESSITY (irreducible: a full graph build, a full-estate scan) -> name WHY it is
         irreducible, with the mechanism, not an assertion.
       - HEAVY-BUT-FIXABLE -> name the suspected cost driver (re-derives-per-call, no cache, scans a
         whole tree to answer a scoped question, shells out N times, re-reads a large artifact).
   Andrew's bar is the ruling: these should be RELATIVELY INSTANTANEOUS unless irreducibly heavy.
D. RANK the fixable ones by (frequency-of-use x latency) -- the rail/telemetry gives real usage counts,
   so an expensive tool nobody calls ranks below a moderate one called constantly. Deliver the ranked
   optimization candidate list; do NOT build the optimizations in this TO.
E. FLAG (do not build): latency class is a natural addition to the declared output contract -- an agent
   could know the cost BEFORE invoking. Recommend or reject with reasoning; the contract is a STANDARD
   surface so any change routes to main CTO via me.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>Enumerate the derivation surface from the registry; classify read-only vs mutating/expensive FROM SOURCE; print both denominators (N derivations enumerated, K classified mutating and excluded).</run>
    <expect>The surface is DERIVED not hand-listed, and the excluded set is explicit with per-item reasons -- an unrun derivation is recorded, never silently skipped.</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>Execute the census per the safety design. Include a TIMING SANITY CONTROL: re-run a sample of derivations and report variance -- a single-shot wall-clock is a sample, not a measurement, and a number without its variance invites false precision.</run>
    <expect>Per-derivation records complete incl. TIMEOUT/NOT-RUN as first-class results; sample variance reported so the bands are honest.</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>Deliver the ranked fixable-candidate list + the heavy-by-necessity set with mechanisms; state the coverage denominator (of N derivations, R run, K excluded, T timed out).</run>
    <expect>Every derivation dispositioned; nothing silently absent from the census.</expect></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Registry/derivation surface is base 0.8.0's (integration owner) -- coordinate the enumeration source.
Any AWS-touching read sequences away from the live main-fabric serve. Isolated worktree per the R4R6
two-axis isolation mandate. The optimization BUILDS are a follow-on TO, not this one. Output-contract
latency-class (scope E) is a STANDARD change -> routes to main CTO via me if recommended.
</cross_domain_coordination>

<acceptance_criteria>
1. Derivation surface enumerated FROM the registry with printed denominator; mutating/expensive set
   excluded WITH per-item reasons (no silent skips).
2. Per-derivation records durable + structured: wall-clock, contracted result class, output digest,
   output capture, vintage. TIMEOUT and NOT-RUN are first-class recorded outcomes.
3. Timing sanity control: sampled re-runs with reported variance (no single-shot numbers presented as
   measurements).
4. Latency bands assigned; every SLOW/HEAVY item dispositioned heavy-by-NECESSITY (mechanism named) or
   heavy-but-FIXABLE (cost driver named).
5. Ranked optimization candidates by frequency x latency, using real usage counts from telemetry.
6. Scope-E recommendation stated (latency in the output contract: yes/no + reasoning).
7. ZERO mutations, zero pipeline perturbation -- state how verified.
8. Session log + compiler-tools-log line.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z (family charter). Report to 1.0.0_SA_CTO~Z.</verification>
</task_order>
