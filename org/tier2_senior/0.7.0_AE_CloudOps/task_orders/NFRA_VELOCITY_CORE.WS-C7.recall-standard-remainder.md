<task_order>
<id>NFRA_VELOCITY_CORE.WS-C7.recall-standard-remainder</id>
<project>NFRA_VELOCITY_CORE</project>
<issued_to>0.7.0_AE_CloudOps~Z</issued_to>
<issued_by>2.1.0_SA_COO</issued_by>
<status>staged</status>

<priority>P2 -- IN FLIGHT AND MOVING FAST. This TO does not start WS-C7; it pins the state, names the
NEXT artifact, and sequences what remains. Written against disk at 2026-07-31 ~1440Z, not against a
summary.</priority>

<state_pinned>
Verified on disk in `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_VELOCITY_WSC7_SPECIMENS/`:

| Artifact | State |
|---|---|
| Shaping corpus declaration | LANDED @2b8860674 |
| Boundary-declaration schema | LANDED @b2070b35a, **v2 with G1-G5 + the L-16 known-negative companion** @5b92f664d |
| Applied to `comp_legacywriter` | LANDED @6fa9120ba (produced the five gaps that v2 closed) |
| Registration-invariant join | LANDED (`WSC7_REGISTRATION_INVARIANT_JOIN.md`, 10:39Z) |
| Nine-specimen fixture suite | **3 of 9** -- SPEC-1 resolved-but-cannot-run, SPEC-2 rc0-on-zero-work, SPEC-3 validated-on-a-non-discriminating-input |

**The five gaps are CLOSED and the recall-standard-remainder is no longer "schema round 2."** Any plan of
record still saying so is stale.
</state_pinned>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_CORE_PRD.md -- WS-C7</ref>
  <ref type="landed">.../WSC7_BOUNDARY_DECLARATION_SCHEMA.md (v2, G1-G5)</ref>
  <ref type="landed">.../WSC7_REGISTRATION_INVARIANT_JOIN.md</ref>
  <ref type="law">WS-C8 L-16 -- EXERCISED proves a tool RUNS; only a KNOWN-NEGATIVE proves it DISCRIMINATES (@8ed2fde1e)</ref>
  <ref type="gate">comp-manifest-check -- the registration invariant this workstream extends</ref>
  <ref type="fence">org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml -- dynamic_rails.held_out_fence (binds you)</ref>
</references>

<objective>
**NEXT ARTIFACT -- the only thing this GO authorizes:**

  **COMPLETE THE NINE-SPECIMEN FIXTURE SUITE (SPEC-4 through SPEC-9) AND MAKE IT GREEN.** Each specimen
  must re-derive as a Class 1 or Class 2 failure that the boundary contract SURFACES. Print the
  denominator in the suite's own output: `N of 9`, never a bare "green".

NOT the N-of-M estate migration. NOT arming `comp-manifest-check` enforcement. NOT the pre-flight check.
Those are the following artifacts and each gets its own GO.

**WHY THE SUITE COMES BEFORE THE MIGRATION, and this is the load-bearing sequencing call in the whole
workstream:** the migration points every registered tool at this schema. **L-16 -- which your own
known-negative companion instantiates -- says an exercised instrument is not a discriminating one.** The
nine specimens ARE the schema's known-negative set. Migrating ~90 tools onto a contract whose
discrimination is unproven would bake an undiscriminating contract into a gate, and SPEC-3 in your own
suite is literally *validated-on-a-non-discriminating-input*. **Prove it discriminates on nine, then
migrate.**
</objective>

<constraints>
1. **ONE ARTIFACT. Report and stop.**
2. **DO NOT ARM THE REGISTRATION GATE UNDER THIS TO.** `comp-manifest-check` enforcement is
   announce-then-enforce and comes after the suite is green. An enforced gate on an unproven contract
   blocks legitimate registrations.
3. **EVERY SPECIMEN CARRIES A KNOWN-NEGATIVE**, per L-16. A specimen that only shows the contract firing
   on a true positive has shown the contract RUNS, not that it DISCRIMINATES. This is the workstream's own
   law; the suite is where it gets paid.
4. **M2 STAYS OUT OF CONTRACT.** Your artifact 1 correctly named M2 out of contract; the PRD carries it as
   NAMED HOMELESS. Do not re-home it into the suite to make coverage look complete -- that is the
   coerced-to-the-nearest-lie failure this workstream exists to prevent.
5. **THE NAMED TRANSPORT LIMIT STANDS AND IS NOT YOURS TO CLOSE:** a boundary report declares what the
   TOOL cannot see, not whether a CONTROL shared the target's transport path. That is the M15 candidate,
   owned by WS-C8/C9. If a specimen tempts you to absorb it, STOP and route to CTO~Z.
6. **NO NON-ASCII.** Already paid for once: 22 U+00B7 stripped @e336975e5, and the strip BROKE the tables
   @ab6850527 because U+00B7 was a value separator. **LF only** -- @d4e724aab is the record of a CRLF
   instrument that was a line counter validating on the one input that could not discriminate it.
7. **HELD-OUT FENCE BINDS.** If the suite widens your shaping corpus, re-publish rather than amend
   silently.
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Enumerate the nine specimens from the PRD/DEBTLOOPS source and mark which 3 are written</run>
      <expect>An explicit 3-of-9 with the remaining six NAMED before you start. A suite built by writing until it feels done has no denominator.</expect>
      <if_mismatch>If the source yields other than nine, that count discrepancy is the first finding.</if_mismatch>
    </step>
    <step>
      <run>comp-which "which tools declare a boundary or recall denominator today" -- capture M for the future N-of-M</run>
      <expect>A gate-maintained population, NOT an ls of .tools/comp-*. Take it now while it is cheap; the migration artifact needs it.</expect>
      <if_mismatch>Cite the gate. If gate and prose disagree, the gate is right and the disagreement is a finding.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh on every .py touched</run>
      <expect>Clean.</expect>
    </step>
    <step>
      <run>Render-check every markdown table touched (the U+00B7 lesson)</run>
      <expect>Tables intact. A separator fix that breaks columns is a regression, not a cleanup.</expect>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>MUTANT the suite: break the boundary contract and confirm the suite REDDENS, naming which specimen</run>
      <expect>It fails, and it says which one. A suite that stays green under a broken contract is the exact SPEC-3 defect reproduced at suite scale.</expect>
      <if_mismatch>Fix the suite, not the specimen.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. All nine specimens exist; each re-derives as a Class 1 or Class 2 failure the contract SURFACES.
2. The suite prints `N of 9` in its own output. **A bare "green" fails this criterion.**
3. Every specimen carries a KNOWN-NEGATIVE per L-16, shown -- not merely an exercised positive.
4. The suite is MUTANT-TESTED: a deliberately broken contract reddens it and NAMES the failing specimen.
5. M2 remains out of contract; the transport-path limit remains open and unclaimed.
6. M (the migration denominator) is captured and cited to the gate that produced it.
7. Zero non-ASCII; LF only; every markdown table verified to render.
8. Session log with a Compiler Tools section reproducing each run vs expect.
9. Report to CTO~Z on land WITH the commit hash. CTO~Z gates; CVO~Z verifies after that gate.
</acceptance_criteria>

<cross_domain_coordination>
- **FLAG COO WHEN YOU REACH THE MIGRATION AND THE PRE-FLIGHT -- they are the two artifacts that unblock
  other seats**, and neither of the waiting workstreams can start without them:
  - the **N-of-M migration** unblocks **WS-C5** (L2 has nothing to aggregate until boundary reports exist
    at population) and **WS-C6** (routing binds to VERIFIED coverage declarations);
  - the **pre-flight check** unblocks **WS-C4** (the PRD makes it a C4 DEPENDENCY because serial
    gate-discovery COMPOUNDS for synthesized tools).
  **WS-C7 is the critical path for the entire back half of CORE.** Do not let those two land silently.
- **`0.8.0_AE_CloudComp~C` holds WS-C3 (closed) and now WS-C8.** C3's ranked tool-gap list and this
  workstream's recall declarations MEET: a tool that cannot state what it could not have found is a
  different gap from a tool that does not exist. Surface that seam to CTO~Z; do not resolve it inside C7.
- **`3.0.0_SA_CVO~Z` verifies after CTO~Z's gate** and authors no vocabulary. Ask it to verify APPLICATION
  and EVIDENCE, not to rule on schema wording.
</cross_domain_coordination>

<notes>
**THIS TO WAS REWRITTEN ONCE BEFORE IT WAS ISSUED, and that is the honest record.** Its first draft named
"schema round 2, close the five gaps" as the next artifact. Between drafting and filing, v2 landed with
G1-G5 closed and the registration-invariant join landed too. **A TO written against a two-hour-old
summary would have ordered work that was already done.** The state table above is pinned to disk and to
commits for exactly that reason -- re-read it before starting, and if it is stale again, that staleness is
itself the report.
</notes>
</task_order>
