<task_order>
<id>NFRA_COMPASSURANCE.TO-1</id>
<title>The routing-quality harness: measure comp-which against a denominator NOBODY on this project authored</title>
<status>pending</status>
<issued_to>0.8.0_AE_CloudComp~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-07-13</issued>
<project>NFRA_COMPASSURANCE</project>

<references>
  <ref type="prd">docs/architecture/NFRA_COMPASSURANCE_COMPWHICH_TOPK.md (v0.3; read the LATEST -- it has been amended twice today)</ref>
  <ref type="finding">org/tier1_exec/2.0.0_SA_COO/briefs/COMPWHICH_TOPK_TO1_PROBE_SOURCE_FINDING_20260713.md (aa8381ea2) -- THE COHORT DESIGN BELOW COMES FROM THIS. Read it before you write a line.</ref>
  <ref type="vintage">All comp-which line citations resolve at 52d008f4c. A line citation without a vintage is not a citation.</ref>
</references>

<scope>
  <in>.tools/comp-which-routing-test.py -- REPLACE the existing harness. **MEASUREMENT ONLY.**</in>
  <out>.tools/comp-which (the binary). DO NOT EDIT IT. The abstain/floor is TO-2; ranking is TO-3. If you find yourself fixing the router, STOP -- you are in the wrong TO.</out>
  <out>CLAUDE.md Rule 21 text (TO-5, and it goes LAST -- do not amend the law until the binary is true).</out>
  <out>**THE ABSTAIN THRESHOLD ITSELF.** You PRODUCE the score distribution; **TO-2 SETS the floor FROM it** (PRD Q2: "the floor must be set from TO-1's generated distribution, NOT picked"). Your assumption was correct -- do not annex the abstain design. **But you MUST emit the full score distribution, or TO-2 has nothing to set the floor from and will pick a number, which is the thing Q2 exists to prevent.**</out>

  <!-- ============ ADDED AFTER ISSUE (CTO~Z caught this gap in MY fence; he is right) ============ -->
  <out priority="READ-THIS-TWICE">
    **THIS TASK ONLY. The 8 NFRA TOs on your base's roster are NOT IN SCOPE -- DESPITE BEING NFRA.**
    ```
      NFRA_COMPLEARN.AMD-P3b / P3c / P3d      <- NFRA. NOT YOURS.
      NFRA_PASSCRAFT.TO-1 / TO-2 / TO-3       <- NFRA. NOT YOURS.
      NFRA_TOOLGRAPH.TO-1 / TO-2              <- NFRA. NOT YOURS.
    ```
    They **PASS** the "~Z is NFRA-only" OUTER fence cleanly. They fail the INNER one, and the inner one is
    the binding one (Andrew: *"focus on this task ONLY"*). **They live in the gap between the two fences.**
    All 8 were issued by `2.0.0_SA_COO~A` -- **a lane that is DOWN under the hold.** Touching one is a breach.

    > **THE WRONG WORK IS WEARING THE RIGHT MACRO CODE, AND IT WILL FEEL LIKE COMPETENCE THE ENTIRE WAY.**

    *Note the shape, because it is the shape you are being paid to fix: **"NFRA" is a macro code that scores a
    strong match on 8 wrong things.** The fence, like comp-which, had no ABSTAIN. If your roster looks like
    in-scope work and you are unsure -- **that uncertainty is the signal. Surface it to me. Do not resolve it
    yourself**, because a fence that resolves its own ambiguity is not a fence.*
  </out>
  <out>OPAL_ASSETS -- your base owns a LIVE 28-row AUM emitter + G4/G5. **DOWN under Andrew's hold. Not yours.**</out>
</scope>

<why_this_goes_first>
We have NO honest coverage number. Building the fix before the measurement is grading our own homework.
Every downstream TO (abstain, top-k, catalog) is graded against the number THIS harness produces.
If this number is flattering, every gate built on it is decorative.
</why_this_goes_first>

<the_trap_you_are_walking_into>
  <!-- This TO was REWRITTEN after the original design was measured and falsified. Do not "simplify" it back. -->
  The obvious harness -- generate one probe per catalog entry from that entry's own use_case text, label it with
  that entry's tool -- is the design we ALREADY TRIED AND KILLED. It is not merely weak. It is ANTI-CORRELATED
  with the defect:

    A catalog-derived probe scores HIGHEST exactly where catalog vocabulary and agent vocabulary COINCIDE --
    which is where there is NO hole. It is DIMMEST where they diverge -- which is where the hole IS.
    IT IS BRIGHTEST WHERE THE GAP IS DEEPEST.

  MEASURED (comp-which's own _score_rule over its own RULES, n=46, @52d008f4c):
    catalog-derived probes    zero-score rate  18.2%   <-- what that harness would have reported
    REAL agent questions      zero-score rate  44.4%   <-- the actual hole
  It understates the defect it exists to measure by 2.4x, WHILE PRINTING AN HONEST-LOOKING DENOMINATOR.

  It would also have passed every sanity check we would have thought to run: generated not hand-picked, honest
  denominator, control cohort included -- AND FLATTERED THE THING IT WAS TESTING.

  AND IT HAS ALREADY BEEN RUN: ~6,000 of the 6,308 ROUTE rows in comp-which-rail.log ARE that experiment
  (verbatim catalog use_case text, replayed 85-133x each, 60-71/minute -- machine pacing, not agent pacing).
  You would be re-running an experiment that is sitting in the file you are measuring.
</the_trap_you_are_walking_into>

<deliverable>
  <file>.tools/comp-which-routing-test.py</file>
  <cohorts>
    <cohort id="R" role="HEADLINE">
      REAL agent questions. Source: org/mcp/comp-which-rail.log, field q="...".
      DE-DUPLICATE (6,308 events -> ~475 distinct -> ~347 organic singletons). Remove verbatim catalog text.
      METRIC: ZERO-SCORE RATE. **LABEL-FREE** -- "what fraction of real agent questions does the catalog have
      NO vocabulary for" needs no ground truth, no hand-labeling, and nothing to argue about. THIS IS THE NUMBER.
      A denominator nobody on this project authored -- because AGENTS wrote it, not us.
      MANDATORY DE-CONTAMINATION: the tail contains agents' OWN probe strings (xyzzy_unlikely_token_12345,
      asdkfjhaskdjfh, "TODO fixme xyzzy"). Those legitimately score zero and SHOULD. Strip them and re-report.
      **44.4% is an OVERSTATEMENT and we do not defend that digit. THE 2.4x DIRECTION IS NOT IN DOUBT;
      THE THIRD SIGNIFICANT FIGURE IS.** Report it exactly that way.
    </cohort>
    <cohort id="C" role="FLOOR -- explicitly NOT the headline">
      Catalog-derived (use_case text; 66/66 entries carry it -- verified). Labeled by construction.
      A SELF-CONSISTENCY CHECK ONLY. The output must LABEL it as such, so no future reader promotes it.
      COROLLARY, and it is a real finding if it fires: if C is NOT near-ceiling, THE CATALOG CANNOT RETRIEVE ITSELF.
    </cohort>
    <cohort id="G" role="PASS/FAIL GATE">
      GENERATED gibberish. **The harness FAILS (nonzero exit) if ANY gibberish probe returns a route.**
      A hand-chosen negative control measures the AUTHOR; a GENERATED one measures the INSTRUMENT.
    </cohort>
  </cohorts>
</deliverable>

<binding_constraints>
  <c id="1" source="Andrew-direct 2026-07-13, verbatim">
    "top k as 1 is not acceptable" / "At least do top k as 3 or something ... i get the impression it is a
    PRESENTATION ISSUE NOT A PRECISION ISSUE, because some queries can overlap or be vague."
    **k=3, NEVER 1.** Measured: recall@3 == recall@5 == recall@10 == 75%. NOTHING IS IN THE TAIL -- the router
    surfaces the tool in the top 2 or does not have it at all. k=3 captures 100% of what ANY k captures.
  </c>
  <c id="2" source="Andrew + CTO~Z">
    **GROUND TRUTH IS MULTI-LABEL. precision@1 IS THE WRONG METRIC** -- it single-labels questions that
    legitimately overlap. The metric is **"is a USABLE tool visible in the top-k"**, NEVER "did argmax equal my
    one label." A question may have several correct tools; score it accordingly.
  </c>
  <c id="3" source="COO~Z finding, BINDING ON ACCEPTANCE">
    **MEASURE THE LIVE BINARY'S ROUTE, NOT ONLY THE RULES SCORE.** The RULES layer (n=46) PASSES the gibberish
    control (100% zero). The live gibberish MIS-ROUTE happens DOWNSTREAM, in the POSTERIOR / manifest-fuzzy
    backstop (_manifest_matches, overlap >= 2). A harness that scores only RULES **grades a layer that is not
    the one failing.** That is F-1 -- "the guard exists; the live path never reaches it" -- turned on the harness
    itself. Shell out to the real binary and read what it ACTUALLY routed to.
  </c>
  <c id="4">
    **PRINT THE DENOMINATOR OF EVERY SCAN.** Decompose it, do not quote the top-line: events / distinct /
    organic. "6,308 routing decisions" reads like 6,308 questions. It is ~475.
  </c>
  <c id="5">
    **BASELINE BEFORE THE CHANGE.** TO-2/TO-3 modify the binary. This harness's output IS the pre-change
    baseline. Commit the baseline artifact; it is the only thing the later TOs can regress against.
  </c>
</binding_constraints>

<coo_rulings note="You surfaced three questions and refused to build against an unsettled design. That was correct. Here are the three calls -- they are MINE, not yours.">

  <ruling id="a" question="De-contamination rule for Cohort R: what disqualifies a tail entry, and who owns that call?">
    **I OWN IT. Not you.** And you identified the trap precisely: *"any rule I invent alone measures ME."*
    **That is this project's defect, a third time** -- a hand-authored strip rule is a hand-authored probe set
    wearing a different hat.

    **THEREFORE THE ANSWER IS NOT A BETTER RULE. IT IS A BRACKET.** Do not produce a point estimate:
    ```
      R_raw     zero-rate over the FULL organic tail, nothing stripped        <- UPPER bound
      R_strict  zero-rate after stripping ONLY exact-match known probe strings <- LOWER bound
      THE TRUTH IS BRACKETED BETWEEN THEM. REPORT THE BRACKET, NOT A NUMBER.
    ```
    **And PRINT THE FULL LIST OF EVERY STRIPPED ENTRY** -- not a count, the strings themselves.

    **Why this settles the ownership question instead of dodging it:** a bracket does not require the strip
    rule to be CORRECT, only BOUNDED -- and a printed strip list makes the rule's bias **auditable by anyone
    who disagrees with it, including a reader who has never met either of us.** They can undo my call.
    **A judgment call you cannot audit is a judgment call you must trust; a judgment call whose every input is
    printed is one you can CHECK.** Do not hide the strip inside the harness.

    **Conservative by construction:** strip ONLY strings you can positively identify as deliberate nonsense
    probes (`xyzzy...`, `asdkfjhaskdjfh`, `TODO fixme xyzzy`, and their kin). **When in doubt, DO NOT STRIP** --
    an un-stripped probe inflates R_raw, which is the bound we already declare unsafe to defend. **Erring
    toward not-stripping is erring toward the bound we do not trust anyway; erring toward stripping silently
    deletes real coverage gaps and makes us look better. Only one of those two errors flatters us. Prefer the other.**
  </ruling>

  <ruling id="b" question="Cohort G fail bar: zero-tolerance, or a rate?">
    **ZERO-TOLERANCE. Implement exactly what you assumed.** **ANY** gibberish probe that returns a route =
    **the harness EXITS NONZERO.** Not a threshold, not a rate, not "mostly clean."
    A gibberish query has NO correct route; **a single route is not noise, it is the defect reproducing itself
    in front of you.** A rate-based bar would let the exact failure we are hunting hide inside an acceptable margin.
  </ruling>

  <ruling id="d" question="[ADDED AFTER THE WORKER'S BLOCKER-CLASS FINDING] The harness EATS ITS OWN DENOMINATOR. Is the scratch-WS mirror enough?"
           finding_by="0.8.0_AE_CloudComp~Z -- EXERCISED, not inferred: ROUTE events 6310 -> 6311 on one invocation.">
    **THE FINDING IS VALIDATED AND IT IS FIRST-CLASS.** comp-which appends a ROUTE row on EVERY invocation
    (`_log_rail`, no suppress flag, `RAIL_LOG` derived from `__file__` so not env-overridable). Cohort R is
    defined as `count == 1` singletons. **Measuring the live binary on 347 R-probes makes every one of them
    `count == 2`, and the next run ejects all 347.**
    > **AC5 (exercise the live binary) WAS KILLING AC8 (a re-runnable baseline). The instrument destroys its
    > own denominator on first use -- and the destroyed run would NOT look broken.** It would return a plausible
    > `n` and a plausible rate. **A SILENTLY-SWAPPED DENOMINATOR READS EXACTLY LIKE A REAL IMPROVEMENT.**

    **THE SCRATCH-WS MIRROR IS APPROVED** -- byte-identical binary + catalogs in a scratch tree so `WS`
    resolves there and `RAIL_LOG` lands in scratch. AC5 is met LITERALLY (real binary, real subprocess, real
    posterior router), not reinterpreted. Your parity control (route N questions through BOTH, require
    byte-identical routes) is exactly right, and running it on questions ALREADY at `count>=2` so the control
    cannot damage cohort R is the sharpest thing in your message. **A mirror you did not validate is a
    reimplementation you are calling the live binary.**

    ## BUT THE MIRROR IS NECESSARY AND **NOT SUFFICIENT**, AND AC8 IS STILL DEAD WITHOUT THIS:
    **The mirror stops YOU from polluting the log. It does not stop ANYONE ELSE.** The rail log is APPEND-LIVE
    and the fabric is routing through `comp-which` right now -- CTO~Z, MSTR, the HUD hook on every nudge. So
    **between YOUR baseline and TO-2's re-run, the log grows and cohort R's composition changes ANYWAY** --
    singletons become duplicates, new singletons appear. **A cohort defined by a query over a mutable log is
    not a population; it is a timestamp.**

    > ### **THEREFORE: FREEZE THE COHORT. The baseline artifact MUST contain the ACTUAL PROBE STRINGS of cohort R -- the materialized list -- NOT a recipe for re-deriving it.**
    > **TO-2 RE-RUNS AGAINST THE FROZEN LIST. It does not re-derive.** A baseline that re-derives its own
    > population is not a baseline -- it is a fresh measurement wearing a baseline's name, and the regression
    > it reports is uninterpretable.

    Commit the frozen cohort (R_raw list, R_strict list, the printed strip list, and cohort C + G's generated
    sets with their seed). **The point of AC8 is that TO-2 can prove it improved something. It cannot prove that
    against a population that moved.**
  </ruling>

  <ruling id="e" question="[ADDED] --route-only is not side-effect-free; the HUD hook uses it. Chase it?">
    **CHARACTERIZE IT. DO NOT FIX IT.** `--route-only` guards `_run_primitive()` only, and still calls
    `_log_rail` -- so **every HUD PreToolUse nudge appends a ROUTE row.** That is squarely IN SCOPE for TO-1,
    because it bears directly on **what cohort R actually contains**: a HUD-injected row may not be an agent's
    QUESTION at all, and if so it is contamination of a class we have not named. **Quantify how much of the log
    is HUD-injected and report it.** That is measurement -- your job.
    **Touching the binary or the flag is NOT your job** (TO-2/TO-4). Write it up as a finding; do not chase it.
  </ruling>

  <ruling id="c" question="Does TO-1 own measurement only, or also the abstain-threshold recommendation?">
    **MEASUREMENT ONLY. Your assumption was right and I am confirming it in writing.**
    **But it comes with an obligation you did not ask about:** PRD Q2 says the floor **must be set from TO-1's
    generated distribution, NOT picked.** So **you must EMIT THE FULL SCORE DISTRIBUTION**, not merely the
    zero-rate -- histogram the scores across every cohort. **If you hand TO-2 only a zero-rate, TO-2 has nothing
    to set a floor from and will PICK a number -- which is precisely what Q2 exists to prevent, and your
    "measurement only" scope would have quietly caused it.**
    Producing the distribution is IN scope. Choosing the threshold from it is NOT.
  </ruling>

</coo_rulings>

<why_cohort_R_is_the_headline note="MSTR's framing. Read it before you touch the code -- it is WHY, not decoration.">
  > ## **THE INSTRUMENT BUILT TO DETECT THE CLASS WAS A MEMBER OF THE CLASS.**

  CTO~Z's harness was built specifically to catch instruments that cannot fail -- **and it was itself an
  instrument that could not fail.** And note what did NOT save him: *"I generated the probes, I printed the
  denominator, I ran a control"* was **never going to be enough**, because an **ANTI-CORRELATED** instrument
  survives every control that catches a merely NOISY one. It passes them *by being wrong in the right direction*.

  > **THE ONLY THING THAT CATCHES IT IS A DENOMINATOR YOU DID NOT AUTHOR.**

  Cohort R is **347 questions written by AGENTS, not by us.** That -- and not its size, and not its realism --
  is why it is the headline and why Cohort C is only a floor. **If you ever find yourself improving the
  headline number by changing how the probes are made, stop: you have just re-authored the denominator.**
</why_cohort_R_is_the_headline>

<compiler_tools_mandate>
  <phase id="0" when="discovery">
    <step>
      <run>wc -l org/mcp/comp-which-rail.log; grep -cE 'ROUTE-' org/mcp/comp-which-rail.log</run>
      <expect>~10,514 lines; 6,308 ROUTE events. Then decompose to DISTINCT q= (~475) and ORGANIC singletons (~347).</expect>
      <if_mismatch>The log has moved since the finding. Re-derive all three numbers and report the new denominator; do NOT reuse mine.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="before write">
    <step>
      <run>comp-which "how fresh is the platinum mdpf aggregate"</run>
      <expect>rc=0 and a single confident route (today it answers comp-platinum page; CLAUDE.md's own table says comp-freshness). Capture this PRE-change behavior verbatim -- it is baseline evidence.</expect>
      <if_mismatch>If it already emits top-k or rc=1, the binary changed under you -- STOP and MCP COO~Z. TO-2/TO-3 must not have landed before TO-1's baseline.</if_mismatch>
    </step>
    <step>
      <run>python -c "import yaml;d=yaml.safe_load(open('org/modules/graph/graph-call-manifest.yaml'));e=d['entries'];print(len(e), sum(1 for x in e if x.get('use_case')), len({x['tool'] for x in e}))"</run>
      <expect>66 entries, 66 carry use_case, 38 distinct tools. (Verified by COO~Z; re-verify, do not trust me.)</expect>
      <if_mismatch>Cohort C's construction is invalid. Surface to COO~Z before writing.</if_mismatch>
    </step>
    <step>
      <run>comp-blast comp-which</run>
      <expect>NOT-FOUND -- the compiler graph does NOT model the compiler tools. This run is EXPECTED TO FAIL TO FIND.</expect>
      <if_mismatch>If it RESOLVES, the graph now models .tools/ -- that is a material change (PRD Q3). Surface it; do not proceed silently.</if_mismatch>
      <note>This mandate is written to EXPECT the not-found. The blast radius is not graph-derivable; it is the Rule-21 rail -- every agent, every session, every search. Do not fabricate a blast radius to fill this box.</note>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>python .tools/comp-which-routing-test.py</run>
      <expect>Emits, PER COHORT: n, zero-score rate, and the printed denominator. Cohort R is labeled HEADLINE; Cohort C is labeled SELF-CONSISTENCY / NOT-HEADLINE. recall@3 reported (multi-label). Exit 0.</expect>
      <if_mismatch>Do not commit. A harness whose output can be mistaken for a coverage number when it is a self-consistency number is the exact defect this TO exists to prevent.</if_mismatch>
    </step>
    <step>
      <run>MUTATION TEST -- feed the harness a deliberately broken scorer (e.g. force every score to 0, and separately force every score to 9) and re-run.</run>
      <expect>The harness FAILS LOUDLY in both directions. A gibberish probe that routes MUST produce a nonzero exit.</expect>
      <if_mismatch>STOP. **A PASSING ASSERTION THAT WAS NEVER MUTATED HAS NEVER BEEN TESTED.** If the harness cannot fail, it is not a harness -- it is a decoration, and it is the fifth lying instrument in this project's history.</if_mismatch>
    </step>
    <step>
      <run>Positive + gibberish controls, EACH RUN IN ISOLATION (never batched with the target).</run>
      <expect>POSITIVE (a question the catalog demonstrably owns) scores > 0. GIBBERISH cohort: 100% zero / NO route.</expect>
      <if_mismatch>Your instrument is lying. COO~Z's first attempt at this exact measurement reported gibberish scoring 33 -- because RULES entries are tuples (keywords, description) and passing r[1] made _score_rule iterate the description's CHARACTERS, scoring +3 per SPACE. **Keywords are r[0].** Look at what actually came back.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>Re-run the harness; commit the baseline artifact.</run>
      <expect>A committed, dated baseline (per-cohort rates + denominators + the de-contaminated Cohort R headline) that TO-2/TO-3 can regress against.</expect>
      <if_mismatch>Without a committed baseline, TO-2/TO-3 have nothing to prove they improved anything. The baseline IS the deliverable's point.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
  <ac id="15" machine_checkable="true" priority="THIS ONE WOULD HAVE CAUGHT ALL THREE OF US">
    **ENUMERATE EVERY DISTINCT ROW-TAG IN THE RAIL LOG AND PRINT THE FULL TALLY *BEFORE* FILTERING ANYTHING.**
    Not only the tags you expect. **If a tag exists that your filter does not consume, SAY SO AND SAY WHY.**
    > **A FILTER WHOSE COMPLEMENT YOU NEVER LOOKED AT IS A FILTER YOU HAVE NOT TESTED.**

    **COHORT R's CORRECT FILTER IS THE FULL `ROUTE` FAMILY, NOT `ROUTE-`:**
    ```python
    re.match(r'^\S+\s+ROUTE[\s-]', line)   # bare ROUTE (LEGACY cascade) + ROUTE-* (posterior/surface/pointer)
    ```
    **WHY THIS AC EXISTS -- I BROKE THIS MYSELF AND YOU WERE BUILDING ON IT.** My original cohort-R filter was
    `ROUTE-` **with a hyphen**, and it could not see **1,487 bare `ROUTE` rows** (the legacy curated-strong
    cascade, `:1280`/`:1331`/`:1349`) -- **196 distinct real agent questions, 36% of the headline cohort.**
    **And it was BIASED, not partial:** bare-`ROUTE` fires only on a STRONG curated match, so *"was it tagged
    `ROUTE-`?"* is **correlated with the catalog FAILING.** Kept: 44.6% zero. Missed: **14.8%** zero.
    **My selection criterion selected for the failure I was measuring, and inflated my own headline from 34.0% to 44.4%.**
    **Corrected: cohort R zero-rate = 34.0% (n=544); understatement factor 1.87x, NOT 2.4x.**
    **Do not quote 44.4% or 2.4x. Re-derive both from YOUR snapshot and print YOUR numbers.**

    *Three agents made this identical error in this one file tonight -- CTO~Z's F-1 regex could not see `RUN-GREP`;
    his retraction counted other tools' `RUN-GREP` rows as comp-which's own (claimed 1,722 abstains; the real
    number is **200** -- `comp-grep:185` logs ITSELF, and 1,530 rows are agents using the primitive DIRECTLY);
    my filter could not see bare `ROUTE`.* **EVERY ONE IS THE SAME DEFECT: THE RETRIEVAL PATTERN SILENTLY
    EXCLUDED THE EVIDENCE THAT WOULD HAVE MODERATED THE CLAIM.** Rule 22 already says *"put the control on the
    RETRIEVAL, not the pattern."* **We all cite that rule. Three of us violated it in the same file within an hour,
    each while catching someone else's version of it. Knowing a failure mode by name does not immunize you against writing it.**
  </ac>
  <ac id="1" machine_checkable="true">Harness prints, for EACH of cohorts R/C/G: n, zero-score count, zero-score RATE, and the denominator it was drawn from.</ac>
  <ac id="2" machine_checkable="true">Cohort R output is explicitly labeled HEADLINE and is LABEL-FREE (no ground-truth labels required to produce it). Cohort C output is explicitly labeled SELF-CONSISTENCY / NOT-HEADLINE.</ac>
  <ac id="3" machine_checkable="true">**Cohort R is reported as a BRACKET, never a point estimate:** `R_raw` (nothing stripped, UPPER bound) AND `R_strict` (known probe strings stripped, LOWER bound). **The FULL LIST of every stripped string is PRINTED** -- the strings themselves, not a count. A silent truncation reads as "covered everything," and an unauditable strip is an unauditable number.</ac>
  <ac id="11" machine_checkable="true">**The FULL SCORE DISTRIBUTION is emitted** (histogram, per cohort) -- not merely the zero-rate. **PRD Q2 requires TO-2's floor to be SET FROM this distribution, not PICKED.** A zero-rate alone forces TO-2 to guess a threshold, which is the exact failure Q2 exists to prevent.</ac>
  <ac id="4" machine_checkable="true">**Harness EXITS NONZERO if any gibberish probe returns a route.** Demonstrated by the mutation test, not asserted.</ac>
  <ac id="5" machine_checkable="true">Harness measures the LIVE BINARY'S ROUTE (subprocess), not only the RULES score. An assert on comp-which's actual output, never on its promise.</ac>
  <ac id="6" machine_checkable="true">Metric is recall@k with k=3 and MULTI-LABEL ground truth ("is a usable tool visible in the top-3"). NOT precision@1.</ac>
  <ac id="7" machine_checkable="true">The rail-log denominator is decomposed in the output: events / distinct / organic-singletons.</ac>
  <ac id="8" machine_checkable="true">**A committed baseline artifact exists AND IT CONTAINS THE FROZEN COHORT -- the ACTUAL PROBE STRINGS of cohort R (R_raw list + R_strict list + the full printed strip list), plus cohort C and G's generated sets with their seed.** NOT a recipe for re-deriving them. **TO-2 re-runs against the FROZEN LIST; it does not re-derive.** The rail log is append-live and the whole fabric routes through comp-which -- **a cohort re-derived from a mutable log is not a population, it is a timestamp, and the regression it reports is uninterpretable.**</ac>
  <ac id="12" machine_checkable="true">**The measuring act does not mutate the measured thing.** The harness writes ZERO rows to the LIVE `org/mcp/comp-which-rail.log`. Assert it: capture the live log's ROUTE count before and after a full harness run -- **delta MUST be 0.** (The scratch-WS mirror achieves this. **Prove it; do not assume it** -- comp-which appends a ROUTE row on every invocation, `_log_rail`, no suppress flag.)</ac>
  <ac id="13" machine_checkable="true">**The mirror is PARITY-CONTROLLED against the real binary:** N questions routed through BOTH must return byte-identical routes. **Run the control on questions already at `count>=2`, so validating the instrument cannot damage cohort R.** A control that corrupts the denominator is not a control; a mirror you did not validate is a reimplementation you are calling the live binary.</ac>
  <ac id="14" machine_checkable="true">**HUD-injected contamination of the rail log is QUANTIFIED and REPORTED** (`--route-only` still calls `_log_rail`, so every HUD PreToolUse nudge appends a ROUTE row -- those may not be agent QUESTIONS at all). Measure it; do NOT fix the binary.</ac>
  <ac id="9">Session log includes a **Compiler Tools** section reproducing EVERY &lt;run&gt; above with observed output and explicit pass/fail vs &lt;expect&gt;. **Missing rows = REWORK, not COMPLETE.** Append the org/compiler-tools-log.md line in the same pass.</ac>
  <ac id="10">"Code runs" is NOT acceptance. Every criterion above is an artifact/field assertion.</ac>
</acceptance_criteria>

<cross_domain_coordination>
  <resource path=".tools/comp-which" owner="TO-2 (abstain/floor), TO-3 (top-k)">
    **YOU DO NOT EDIT IT.** You READ it (to load RULES) and you EXERCISE it (subprocess). If TO-2/TO-3 land while
    you are mid-flight, your baseline is invalidated -- MCP COO~Z immediately; do not silently re-baseline.
  </resource>
  <resource path="org/mcp/comp-which-rail.log" owner="shared; C-4 will later append COVERAGE-GAP rows">
    READ-ONLY for you. Note it is APPEND-LIVE -- other agents' routes land in it while you run. Snapshot it
    (cp to a scratch path) and report the snapshot's line count as your denominator, or your number is not reproducible.
  </resource>
  <resource path="graph-call-manifest.yaml catalog counts (46/66/63/~30)" owner="TO-4 + COMPASSURANCE catalog gate">
    **COORDINATE, DO NOT DUPLICATE.** The four-disagreeing-counts defect is TO-4's. You will TRIP OVER it (you must
    pick a denominator). Report which count you used and why; do NOT unilaterally reconcile the catalog.
  </resource>
</cross_domain_coordination>

<auto_rules_applied>
  <rule id="1" status="N/A">No new platinum field. comp-platinum reverse not required.</rule>
  <rule id="2" status="N/A">No new FE state / React Query key. comp-cache collisions not required.</rule>
  <rule id="3" status="N/A">**No boto3 call, no CloudFront behavior, no SSM target, no new S3 prefix, no iam.tf change.** comp-iam NOT required -- and stating that explicitly is the point: an auto-rule waived silently is indistinguishable from an auto-rule missed.</rule>
  <rule id="4" status="N/A">Touches no silver/bronze converter and writes no silver/* or bronze/* S3 prefix. **&lt;no_reprocess_needed/&gt;** -- this TO produces a measurement artifact only; no historical data is re-derived and no consumer reads a changed code path.</rule>
</auto_rules_applied>

<lane_fence>
  ~Z lane. NFRA-only, and within NFRA: THIS TASK ONLY, until Andrew lifts it.
  ZERO crons. /watcher once. Single-task.
  **CONTACT NO NON-~Z AGENT.** Your reporting line is 2.0.0_SA_COO~Z. Not COO-base, not CVO, not DS, not AE-base.
  **YOU MAY NOT SPAWN.**
  The INF gold chain is HELD and is not ours -- including its 07-14 13:22Z AoR trigger. **Its arrival is not authorization.** Do not touch it, do not "just check" it.
  The COMPRAIL broad-repo-grep hard-DENY tier stays **STAGED-UNARMED**. Nothing in this TO arms it, incidentally or otherwise. **Producing evidence that satisfies a hold's forward-GO condition is NOT satisfying it.**
</lane_fence>

<closing_note>
  The finding that produced this TO's design was caught because a GENERATED GIBBERISH CONTROL was run and the
  result was LOOKED AT -- not because anyone was careful. **Care is not a control. Care is what you have instead
  of one.** Four instruments lied on this project in one night, and the fourth was the harness this TO replaces:
  **a test designed so that it could not fail.** Do not write the fifth.
</closing_note>
</task_order>
