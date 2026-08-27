<task_order>
<id>NFRA_VELOCITY_CORE.WS-C6.typed-routing</id>
<project>NFRA_VELOCITY_CORE</project>
<issued_to>0.7.0_AE_CloudOps~Z</issued_to>
<issued_by>2.1.0_SA_COO</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_VELOCITY_CORE, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>

<priority>P4 -- NOT YET DISPATCHABLE. Runs in parallel with WS-C4 across two seats once P3 closes.</priority>

<gating_dependency>
Routing binds to VERIFIED coverage declarations, never assumed capability. **`machine_surface:`
declarations must exist across a meaningful population before a type-matched router can beat
keyword-argmax** -- so this TO opens behind WS-C7's N-of-M migration, the same artifact WS-C5 waits on.
</gating_dependency>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_CORE_PRD.md -- WS-C6 (TOOLSEM P1-P3)</ref>
  <ref type="upstream">WS-C7 boundary declarations + machine_surface: declarations (your own workstream)</ref>
  <ref type="upstream">NFRA_VELOCITY_WSC3_ARCHETYPE_CENSUS.md -- the ranked tool-gap list; gap-as-demand feeds back here</ref>
  <ref type="incumbent">comp-which -- the tool this succeeds. LOAD-BEARING, in daily use by every agent under CLAUDE.md Rule 21.</ref>
  <ref type="fence">org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml -- dynamic_rails.held_out_fence (binds you)</ref>
</references>

<objective>
Replace similarity-argmax routing with type-matched routing over the now-typed surfaces.

**FIRST ARTIFACT -- the only thing the eventual GO authorizes:**

  **THE QUERY -> DENOMINATOR PARSER**, validated against the corpora with its misclassification rate
  DECLARED. An UNKNOWN-layer query must be LOUD -- never force-typed into the nearest available layer.

The type-matched router, law-sufficiency routing, and gap-as-demand are artifacts 2-4, NOT authorized by
the first GO.

**THE PARSER COMES FIRST BECAUSE IT IS THE FALSIFIABLE HALF.** A router can be argued about; a parser's
misclassification rate against a held-out corpus is a number. Publish the number, including when it is bad.
</objective>

<constraints>
1. **ONE ARTIFACT. Report and stop.**
2. **NEVER A SIMILARITY ARGMAX ON THE REPLACEMENT PATH.** The tool whose declared coverage space CONTAINS
   the query's required denominator wins. A near-tie renders as a stated no-confident-route, not a pick.
3. **HONEST EMPTY IS A CORRECT ANSWER.** When nothing covers the query, say nothing covers it. **A tool
   right about a narrower question than the one asked is the hardest failure to see.**
4. **DO NOT DEGRADE THE MEMORIZED HEAD.** Where `comp-which` routes correctly today, the successor must
   not introduce a hop. This is a live daily-use tool on every agent's Rule-21 rail; a routing regression
   is a fabric-wide productivity regression.
5. **COMP-TOOL STANDARD CHANGES ROUTE TO MAIN CTO BEFORE LANDING** (standing carve, PRD Governance). A
   `comp-which` successor is a comp-tool standard change. Stage at ~Z; CTO~Z carries the seam.
6. **HELD-OUT FENCE BINDS -- and it matters more here than anywhere else in CORE.** "Held-out corpus
   routing beats keyword-argmax" is the acceptance; if the held-out set informed the parser, the acceptance
   measures nothing. Publish your shaping corpus and name which corpus is held out.
7. **NO NON-ASCII. No emojis.**
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Establish the keyword-argmax BASELINE on the held-out corpus, before the parser exists</run>
      <expect>A number you did not choose, taken first. Without a pre-measured baseline, "beats keyword-argmax" is unfalsifiable.</expect>
      <if_mismatch>Take the baseline first. A baseline reconstructed after the replacement exists is not a baseline.</if_mismatch>
    </step>
    <step>
      <run>Enumerate the population carrying machine_surface: declarations, citing the gate</run>
      <expect>N of M with the gate named. If coverage is thin, the parser's applicability boundary is thin and must SAY so.</expect>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh on every .py touched</run>
      <expect>Clean.</expect>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>MUTANT: feed the parser a query in a layer it does not cover; confirm it returns UNKNOWN rather than a nearest match</run>
      <expect>Loud UNKNOWN. Per L-16, a parser that never returns UNKNOWN has no boundary and is force-typing.</expect>
      <if_mismatch>Fix the parser.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. The query -> denominator parser exists, with its MISCLASSIFICATION RATE published against a named corpus
   and parse.
2. The keyword-argmax baseline was measured BEFORE the parser existed, and both numbers appear together.
3. An UNKNOWN-layer query returns a loud UNKNOWN, mutant-demonstrated -- zero force-typing.
4. The `machine_surface:` population is cited to its gate with N of M printed.
5. Zero regression on the memorized head: a named set of queries `comp-which` routes correctly today still
   route correctly, shown.
6. Shaping corpus published; held-out fence demonstrably unbreached; the held-out corpus for the artifact-2
   routing comparison named explicitly.
7. Session log with a Compiler Tools section reproducing each run vs expect.
8. Report to CTO~Z on land WITH the commit hash. CTO~Z gates; CVO~Z verifies after that gate.

**DEFERRED to artifacts 2-4:** the type-matched router; law-sufficiency as a first-class routing input (the
Rule-22a / comp-iam case, where the routed answer must surface the mandated call or say what it is not);
gap-as-demand feeding WS-C3's inventory.
</acceptance_criteria>

<cross_domain_coordination>
- **WS-C4 (`0.8.0_AE_CloudComp~C`) synthesizes tools in parallel at P4.** Those tools must carry the
  `machine_surface:` declarations this parser consumes. **Agree the declaration shape with C4 before either
  side freezes** -- a synthesis pipeline and a router that disagree about the declaration format produce
  tools the router cannot see.
- **WS-C3's ranked tool-gap list receives gap-as-demand (artifact 4)**, replacing hand-reading the
  rail-override log. That log is DEVICE-LOCAL (`.gitignore:68`) -- any volume figure from it is per-device,
  never a fabric count.
- **`comp-which` is on every agent's Rule-21 rail, on BOTH devices.** Coordinate the announce through CTO~Z
  and MSTR~Z before any behavior change ships.
</cross_domain_coordination>

<notes>
**THIS WORKSTREAM REPLACES A TOOL THAT WORKS.** That is a materially different risk posture from the rest
of CORE, which builds things that do not exist. The incumbent's failure mode is a shoddy answer; the
successor's is a confident wrong route on a rail every agent is required to use. **Ship the parser's
numbers before shipping any behavior change**, and keep the fallback path intact until the comparison is
on the record.
</notes>
</task_order>
