<task_order>
<id>NFRA_VELOCITY_CORE.WS-C4.stability-grader-and-synthesis</id>
<project>NFRA_VELOCITY_CORE</project>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.1.0_SA_COO</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_VELOCITY_CORE, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>

<priority>P4 -- NOT YET DISPATCHABLE. Runs in parallel with WS-C6 across two seats once P3 closes.</priority>

<gating_dependency>
**THE PRD MAKES WS-C7's PRE-FLIGHT CHECK A WS-C4 DEPENDENCY, not a nicety** -- the registration chain is
six gates deep, each revealing itself only after the previous passes (five serial discoveries, about 40
minutes, on ONE tool), and **serial discovery COMPOUNDS for synthesized tools, which is this workstream's
entire output.** This TO opens when WS-C7's pre-flight artifact lands. Synthesizing tools into an
undiscovered gate chain is how a synthesis pipeline produces tools that cannot register.
</gating_dependency>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_CORE_PRD.md -- WS-C4 (TOOLARCH s3/P3/P4)</ref>
  <ref type="upstream">org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_VELOCITY_WSC3_ARCHETYPE_CENSUS.md @29b5ccacc -- the ranked tool-gap list is this workstream's queue</ref>
  <ref type="upstream">WS-C7 pre-flight check + shell-reachability gate (0.7.0_AE_CloudOps~Z)</ref>
  <ref type="law">WS-C8 L-16 -- EXERCISED proves a tool RUNS; only a KNOWN-NEGATIVE proves it DISCRIMINATES</ref>
  <ref type="fence">org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml -- dynamic_rails.held_out_fence (binds you)</ref>
</references>

<objective>
Grade every pattern BEFORE choosing its extraction mechanism, then synthesize from the graded set.

**FIRST ARTIFACT -- the only thing the eventual GO authorizes:**

  **THE FIVE-AXIS STABILITY GRADER, VALIDATED ON BOTH NAMED CASES.** Axes: GOVERNANCE (law, convention or
  accident?), CHURN (how often has the shape changed?), POPULATION (enumerable? registry-bounded?),
  VIOLATION (do live exceptions exist today?), BLAST (what breaks silently if the shape drifts?).
  **It must grade the S3 key grammar as STABLE-BY-LAW and vendor filenames as UNSTABLE. Both, or the
  grader is wrong** -- that is the PRD's acceptance, not a suggestion.

Tool synthesis is artifact 2 and is NOT authorized by the first GO.

**BRITTLENESS IS A PROPERTY OF THE TARGET, NOT OF REGEX.** A grader scoring the extraction technique
instead of the thing being extracted has inverted the workstream.
</objective>

<constraints>
1. **ONE ARTIFACT. Report and stop.**
2. **A PATTERN EXTRACTOR WHOSE GOVERNING LAW IS NOT CITED IS UNREGISTRABLE.** STABLE-BY-LAW requires
   governed + low churn + bounded + zero live violations, and the extractor must cite the law it depends
   on so a law change fails the tool LOUDLY. Anything less -> structural extraction (AST / graph /
   live-primitive), or the tool is not built.
3. **NO EXCEPTION CARVED FOR GENERATED TOOLS.** Same registration invariant, same mutant requirements, same
   boundary declaration as hand-built. A synthesis pipeline exempting its own output from the standard is
   a factory for unverifiable tools.
4. **THE VALIDATION CASES ARE A CONTROL, NOT A DEMO. Grade both BEFORE tuning.** A grader tuned until the
   two known cases come out right has been fitted to them, and the acceptance would then measure your
   tuning rather than the grader.
5. **HELD-OUT FENCE BINDS.** Publish your shaping corpus.
6. **NO NON-ASCII. No emojis.**
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-which "what governs the S3 key grammar" and the equivalent for vendor filenames</run>
      <expect>For the S3 grammar: a NAMED law/standard/gate. For vendor filenames: nothing, or convention only. If the S3 grammar turns out ungoverned, that INVERTS the validation case and IS the finding -- report it, do not pick a different case.</expect>
      <if_mismatch>Report the delta. Do not substitute a case that makes the grader look right.</if_mismatch>
    </step>
    <step>
      <run>CHURN axis: git history of the declaration AND of the instances, both cases, window stated</run>
      <expect>A measured churn rate over a NAMED window. "Low churn" with no window is not a measurement.</expect>
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
      <run>MUTANT the grader: inject a live violation into the known-stable case and confirm the grade DROPS off STABLE-BY-LAW</run>
      <expect>The grade moves. Per L-16, a grader that returns STABLE-BY-LAW under an injected live violation cannot fail and is not a control.</expect>
      <if_mismatch>Fix the grader.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. The five-axis grader exists and each axis is computed from a NAMED instrument, not judged.
2. S3 key grammar grades STABLE-BY-LAW; vendor filenames grade UNSTABLE. Both, shown, with the axis values
   that produced each grade.
3. Grades were taken BEFORE any tuning, and the pre-tuning result is on the record even if it was wrong.
4. The grader is MUTANT-TESTED: an injected live violation drops the grade off STABLE-BY-LAW.
5. CHURN carries a stated measurement window; POPULATION cites the registry or states it is unbounded.
6. Shaping corpus published; held-out fence demonstrably unbreached.
7. Session log with a Compiler Tools section reproducing each run vs expect.
8. Report to CTO~Z on land WITH the commit hash. CTO~Z gates; CVO~Z verifies after that gate.

**DEFERRED to artifact 2:** >=1 tool synthesized end-to-end through registration + mutants.
</acceptance_criteria>

<cross_domain_coordination>
- **WS-C3's ranked tool-gap list (LANDED @29b5ccacc) is this workstream's input queue** -- but read WS-C3's
  own section-4 impeachment before trusting the compression ratio: it measures **CATALOGUE CURATION**, not
  tool redundancy, because the pattern count came from two ratified catalogues (12 + 4) rather than an
  independent enumeration of observed motifs. **WS-C3 item 3 carries that residual UNOWNED.** If this
  workstream needs the redundancy reading, the independent enumeration is a prerequisite -- surface it to
  CTO~Z rather than reusing a published ratio for a purpose its own author explicitly disclaimed.
- **WS-C6 (typed routing) runs in parallel at P4 on a different seat.** Synthesized tools must carry
  `machine_surface:` declarations C6 consumes. **Agree the declaration shape with C6 BEFORE synthesis.**
- **WS-C7's registration invariant binds every synthesized tool.** No carve-out.
</cross_domain_coordination>

<notes>
**THE VALIDATION CASES ARE THE WHOLE POINT OF ARTIFACT 1.** The PRD says both must grade correctly "or the
grader is wrong" -- a rare, cheap, genuine control: a known-stable and a known-unstable target chosen
before the instrument existed. **Run it once, honestly, before tuning anything.** An instrument validated
only after adjustment has measured its author.
</notes>
</task_order>
