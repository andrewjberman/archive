<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-05-24-demov1-006-mechanism-class-change</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-24</date>
    <status>complete</status>
    <reconcile_2026_06_01>DONE (~D lane) -- Path B structured-PII-tagging shipped by 0.4.0_DS_ClientPlatform~D Phases 1-3 (115af15f8/50176a86e/7e9969a5d); COO already flagged work-shipped-2026-05-24-but-TO-pending (19fdf2155). ~D-issued; flipped as queue-hygiene per COO reconcile-direction. (was: pending)</reconcile_2026_06_01>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_DEMOV1</project_code>
    <priority>P1 -- LD-0030 mechanism-class change for DEMOV1.004 leak-detection. Durable follow-on per attempt-13 SUCCESS sequencing (NOT immediate supersession; reserved branch for attempt-13 failure no longer fires).</priority>
    <sla>~4-8h wall (architectural primitive implementation + regression-test fixture + full transform re-run + R5 PII scan validation).</sla>
    <!-- GO ON AUTHOR by 2.0.0_SA_COO base 2026-05-24T03:35Z UTC. CVO LD-0029 priority-
         consult CORROBORATE Path B verdict (commit 293649cc0) ratified via LD-0026
         backstop. MSTR LD-0030 charter (b58751842) supersedes LD-0029; routes
         materialization via COO with M-1 + FN-1 baked.

         Original sequencing: DS~C picks up post-attempt-13 (success or final-fail
         empirical anchor); NOT blocking attempt-13.

         REASSIGNMENT 2026-05-24T21:5xZ (ws COO): attempt-13 SUCCESS empirically
         settled (DS~C close-out commit 469df551f + ws COO RAVC2-Accept commit
         f93f52969 + ws CVO CORROBORATE AC5 verdict commit 95e2b366e). Per LD-0030
         attempt-13-SUCCESS branch + LD-0021 staging materialization: issued_to
         changes from 0.4.0_DS_ClientPlatform~C to 0.4.0_DS_ClientPlatform~D.
         Rationale: Path B is mechanism-class-change (substring-scan -> structural-
         disjointness-at-build-time); fresh ~D context-baggage-free is cleaner than
         ~C's 13-attempt substring-scan muscle memory; ~C's close-out + monitor logs
         (paired in 469df551f) are the SPAWN-WITH-DIRECTION orient bundle for ~D's
         first cycle. MSTR LD-0050 covers DS~D demand-justified spawn at CY-0088
         per SS-0002 §7 step 14 materialization. -->
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_DEMOV1.md (v0.1.3)</prd>
    <ld_charter>org/tier0/ledger/LD-0030.md (MSTR materialization charter; supersedes LD-0029)</ld_charter>
    <cvo_corroborate_verdict>commit 293649cc0 -- CVO LD-0029 priority-consult verdict CORROBORATE Path B</cvo_corroborate_verdict>
    <iteration_history>commits 9e02fc35d (couple-component guard) + defcab3cb (shared-surname couple c1) + dbf170b32 (_embeds_real substring guard) + DS~C session logs attempts 6-13</iteration_history>
    <target_code>data/demo/scripts/transform/fake_identities.py + adjacent pseudonymizer modules</target_code>
    <r5_scan>PII-leak scan (ruling R5) per ADVI_DEMOV1.004 acceptance gate</r5_scan>
  </references>

  <objective>
    Change DEMOV1 leak-detection mechanism class from POST-HOC SUBSTRING-SCAN to STRUCTURED-PII-TAGGING-AT-PSEUDONYMIZER-BUILD-TIME. Substring-scan + variants are post-hoc fragment containment checks (12 attempts iterating since DEMOV1.004 GO; multiple failure modes uncovered each attempt). Structured tagging at build time prevents the failure class by construction -- knowing all real names upfront (DS factory already pre-seeds via 9e02fc35d + defcab3cb) enables a structural disjointness guarantee at the moment of fake generation, eliminating the need to retroactively detect leaks. End-state: every fake identity generated is provably-disjoint from the real-identity set at generation time; the R5 PII scan becomes a verify-not-detect step.
  </objective>

  <context>
    DEMOV1.004 transform iteration history: 12 attempts (post-attempt-9 launched 2026-05-23T~07:25Z UTC; attempt-13 still in flight as of this TO). Each iteration found a new leak class (austin_thompson substring leak; sam_owens couple-component; Powell/Winslow/Clarke shared-surname; attempt-12 diagnostic exposes; attempt-13 _embeds_real substring guard). Pattern: post-hoc substring scan is structurally insufficient -- each fix addresses one failure mode but allows the next failure mode to surface on the next run. CY-0052 META trend banked the rediagnose-iteration class as candidate for mechanism-class rethink; LD-0029 architectural-fork surfaced to Andrew; Andrew direct-routed to CVO; CVO CORROBORATE Path B mechanism-class change.

    PATH B PRIMITIVE (M-1, verbatim from CVO):
      "Structured-PII-tagging-at-pseudonymizer-build-time. Reasoning: substring-scan + variants are post-hoc fragment containment checks; structured tagging at build time prevents the failure class by construction (knowing all real names upfront -- DS factory already pre-seeds -- enables structural disjointness guarantee)."

    KEY OBSERVATION: the pseudonymizer ALREADY pre-seeds real names (per 9e02fc35d + defcab3cb iteration). Path B leverages this same data STRUCTURALLY rather than as substring-scan input. The disjointness guarantee at generation time is the architectural difference.

    REGRESSION-TEST REQUIREMENT (FN-1, verbatim from CVO):
      "Whatever Path B primitive ships MUST validate against full known-leaker set (austin_thompson + sam_owens + Powell/Winslow/Clarke + attempt-12 exposes + attempt-13 catches)."

    Iteratively-grown set going forward -- any future leak discovery adds to the regression-test fixture.

    SEQUENCING (RESOLVED 2026-05-24): attempt-13 SUCCESS empirically settled (R5 PII scan: leak_count=0 over 22,260 objects scanned vs 9,665 real z-IDs + 3,291 real literals; AC5 reconciliation cent-perfect; DS~C close-out commit 469df551f; ws COO RAVC2-Accept commit f93f52969; ws CVO CORROBORATE on AC5 method commit 95e2b366e). Per attempt-13-SUCCESS branch: this TO is the DURABLE-FOLLOW-ON for any future demo-data refresh (per Q2 snapshot-only ruling, future refresh = manual rebuild + Andrew direction; Path B is the rebuild's leak-detection primitive). NOT immediate supersession of the existing demo snapshot. DS~D picks up this TO post-CY-0088 spawn per LD-0021 staging materialization.

    ORIENT BUNDLE FOR DS~D (SPAWN-WITH-DIRECTION fast-orient inputs):
      - DS~C close-out log: org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-24/advi_demov1_004_attempt13_close~C.md (commit 469df551f) -- full AC1-8 evidence + reconciliation method + mechanism-class observation
      - DS~C monitor log: org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-24/advi_demov1_004_attempt13_monitor~C.md (paired in 469df551f) -- Phase-1/2 compiler-tools mandates + mid-run state
      - ws COO RAVC2-Accept MCP: filesystem inbox archive 20260524T213658Z_2.0.0_SA_COO__RAVC2-ACCEPT__ADVI_DEMOV1.004_attempt-1.md
      - CVO AC5 verdict log: org/tier1_exec/3.0.0_SA_CVO/logs/2026-05-24/cvo_loop_2141Z_ADVI_DEMOV1_004_AC5_disjointness_verdict.md (commit 95e2b366e) -- includes FN-1 per-slice coverage characterization + FN-2 2D-pattern as load-bearing insight + FN-3 common-name collision false-negative bound; potentially informative for Path B regression-test fixture design
  </context>

  <scope>
    <in_scope>
      DELIVERABLE A -- PATH B PRIMITIVE IMPLEMENTATION.
        - Edit `data/demo/scripts/transform/fake_identities.py` + adjacent pseudonymizer modules.
        - Implement structured-PII-tagging-at-build-time: at the moment of fake identity generation, ensure the generated identity is provably-disjoint from the real-identity set. Mechanism: pre-build a structured index of all real-name fragments (full names + first names + last names + couple-components + shared-surname-cohorts + any other fragment class known to leak), then generate fakes that are structurally guaranteed not to overlap any fragment.
        - Specific data-structure choice: DS~C decides (could be trie, set-of-tuples, hash-based exclusion, or similar). Document the choice + reasoning in session log.
        - Integration point: the disjointness check fires AT generation time (before the fake is returned), not POST-HOC after generation. This is the architectural inversion vs substring-scan.

      DELIVERABLE B -- FN-1 REGRESSION-TEST FIXTURE.
        - Build a discrete test fixture covering the full known-leaker set:
          * austin_thompson (attempt-9 leak class)
          * sam_owens (attempt-10 couple-component class)
          * Powell, Winslow, Clarke (attempt-11 shared-surname cohort)
          * attempt-12 exposes (per DS~C's diagnostic HARD ERROR commit c61d4da6e)
          * attempt-13 catches (per dbf170b32 _embeds_real guard outputs)
        - Invocation point: pre-transform-run hook OR explicit test target (DS~C decides where it lives most naturally in the test harness). Should run automatically before any --apply mode dispatch.
        - Future-proof: fixture is iteratively-grown -- if future leak surfaces, append to fixture; new Path B primitive runs MUST pass against the growing set.

      DELIVERABLE C -- TRANSFORM RE-RUN UNDER PATH B.
        - Once Path B primitive + regression-test ship + pass: dispatch a fresh transform run (attempt-N+1 if you're tracking the iteration counter, or "Path B run #1" if cleaner naming).
        - Full 22,260-object scope; ~12h+ wall per CY-0051 baseline (Path B doesn't necessarily speed up the transform; it just structurally prevents leaks).
        - R5 PII scan post-transform: should be a VERIFY-NOT-DETECT step -- ideally finds zero leaks because the build-time disjointness guarantee made them structurally impossible.

      DELIVERABLE D -- RAVC2 to COO + CC CVO + cite LD-0030 charter.
        - All ACs evidenced; regression-test fixture passes; R5 scan result; session log with the data-structure-choice reasoning.
    </in_scope>
    <out_of_scope>
      - VALFIN.012 Phase B materialization (separate workstream; gated on .010 ship; DS~D lane).
      - DS Base 24h-window force-kill question (separate Andrew/MSTR decision).
      - LD-0018 F2 (a) Andrew product-strategy deferral (separate product question).
      - Modifying any non-demo-pipeline pseudonymizer (this is DEMOV1-scope only).
      - Speeding up the transform's runtime (Path B is correctness, not speed).
      - Changing the R5 scan itself (it remains the closure gate; Path B just makes it find zero).
    </out_of_scope>
  </scope>

  <cross_domain_coordination>
    Lead: 0.4.0_DS_ClientPlatform~D (durable-follow-on owner per LD-0021 staging materialization + LD-0030 attempt-13-SUCCESS sequencing). DS~D's lane authority for this work derives from SS-0002 §7 step 14 + MSTR LD-0050 demand-justified spawn at CY-0088. Iteration history (12-attempt substring-scan series) lives in DS~C's close-out + monitor logs cited in &lt;context&gt; ORIENT BUNDLE; DS~D consumes that history as orient input, not as muscle memory.
    Sub-forks within Path B implementation route under LD-0026 backstop: surface to COO → Andrew 1-cycle SLA → CVO/CTO if silent.
    No cross-lane coordination needed for primary implementation. DS~C standby cycle 1 (per ws COO recommendation MCP 21:46Z; reassess CY-0089 for LD-0036 step-2 stand-down) -- if DS~D needs iteration-history clarification beyond what the close-out + monitor logs surface, MCP DS~C directly OR route through ws COO.
    CC AE~C on RAVC2 (instance teardown coordination per existing demo-static-snapshot design once R5 scan clean) -- AE~C cross-domain thread on EC2 write-role grant closed at .004 close-out (20260524T213744Z); .006's transform re-run reuses the same demo-transform-runner IAM + EC2 infra unless DS~D surfaces a new mechanism-class need.
    CC CVO on RAVC2 -- they'll re-verify the regression-test fixture (FN-1) + R5 scan and ratify LD-0030 closed. CVO has prior context via the AC5 disjointness verdict (commit 95e2b366e) which is conceptually adjacent (haystack + corpus 2D-coverage pattern shares the structural-knowledge-of-corpus framing with Path B build-time disjointness).
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before write (design)">
      <step>
        <run>(read CVO LD-0029 verdict file + LD-0030 ledger entry; review iteration history commits 9e02fc35d / defcab3cb / dbf170b32 / c61d4da6e)</run>
        <expect>Have CVO's Path B reasoning + iteration history's known-leaker set in hand before designing the structured-tagging primitive.</expect>
        <if_mismatch>STOP. Without CVO reasoning, the primitive choice might miss the architectural inversion CVO is specifying.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit (implementation)">
      <step>
        <run>.tools/ds-commit-gate.sh data/demo/scripts/transform/fake_identities.py [+ adjacent files]</run>
        <expect>Exit 0 -- py_compile + AST + ruff all PASS on the Path B primitive.</expect>
        <if_mismatch>STOP. Investigate gate failure before commit.</if_mismatch>
      </step>
      <step>
        <run>(run regression-test fixture on the new Path B primitive locally)</run>
        <expect>All known-leaker entries PASS the disjointness check (i.e., the primitive structurally prevents each documented leak class).</expect>
        <if_mismatch>STOP. Primitive doesn't yet structurally prevent the documented leak class. Iterate.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit (transform re-run)">
      <step>
        <run>.tools/safe-deploy.sh + SSM dispatch transform run under Path B</run>
        <expect>Cycle clean; transform runs end-to-end.</expect>
        <if_mismatch>STOP. Investigate deployed-vs-committed drift OR substantive runtime issue.</if_mismatch>
      </step>
      <step>
        <run>R5 PII-leak scan post-transform on opal-data-demo/platinum/**</run>
        <expect>Zero leaks found (Path B's disjointness guarantee makes leaks structurally impossible; R5 scan is verify-not-detect).</expect>
        <if_mismatch>STOP. If R5 finds leaks under Path B, the structural-tagging didn't cover a fragment class; surface to COO with the missed-class for the next iteration round (this would be a sub-fork triggering LD-0026 backstop if architectural).</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <ac id="AC1">Path B primitive implemented: at fake generation time, output is provably-disjoint from real-identity fragment set via structured (not substring-scan) check. Data-structure choice + reasoning documented in session log.</ac>
    <ac id="AC2">FN-1 regression-test fixture exists + invocation point identified + passes against full known-leaker set (austin_thompson + sam_owens + Powell/Winslow/Clarke + attempt-12 exposes + attempt-13 catches).</ac>
    <ac id="AC3">Transform re-run under Path B completes end-to-end on full 22,260-object scope.</ac>
    <ac id="AC4">R5 PII-leak scan post-transform finds ZERO leaks (Path B's structural disjointness guarantee).</ac>
    <ac id="AC5">Substring-scan / `_embeds_real` / couple-component-guard / shared-surname-guard primitives either deleted or retained as defense-in-depth-not-primary per DS~C's design call (document choice in session log).</ac>
    <ac id="AC6">Session log + Compiler Tools section reproduces every &lt;run&gt; with observed output + pass/fail vs. &lt;expect&gt;.</ac>
    <ac id="AC7">RAVC2 to COO + CC CVO + CC AE~C; cites LD-0030 charter + regression-test fixture path + R5 scan exit code.</ac>
  </acceptance_criteria>

  <not_authorized>
    - Substring-scan primitive as the PRIMARY mechanism (Path B explicitly supersedes it; substring-scan can survive as defense-in-depth-not-primary per AC5).
    - Speeding up the transform's runtime (Path B is correctness, not speed; if the speed question matters separately, route to COO for a different TO).
    - Acceptance flex on AC4 (R5 scan zero-leaks) -- if Path B's disjointness guarantee doesn't hold, the primitive needs iteration not acceptance.
    - Acceptance flex on AC2 (regression-test full known-leaker set) -- the fixture's completeness IS the empirical guarantee.
    - Touching non-DEMOV1 pseudonymizer code -- scope-creep guard.
  </not_authorized>
</task_order>
