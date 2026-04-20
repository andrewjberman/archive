<task_order>
  <header>
    <id>ADHC_ROUTER.T4</id>
    <project>ADHC_ROUTER</project>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_at>2026-04-15</issued_at>
    <status>complete</status><!-- COO flip 2026-04-16 per ADHC_ROUTER Phase 1 closeout. ~D shipped 3c921e08 — ADHC_ROUTER.T4 + comp-validate pass-through dispatch (proposal E partial). -->
    <authorizing_directive>Andrew 2026-04-15 — corpus-driven compiler regression testing.</authorizing_directive>
  </header>

  <scope>
    Stress-test the silver-scope path of `comp-pipescript deployed` (shipped with AE CloudOps TO) AND dotted-path `comp-platinum reverse` (0324142a) against the WP-11 3-bond scoped-overrides + CN-P0 nna_atomic canonical schema work you completed today. Both were silver-layer or canonical-convergence work that hit multiple tool gaps at authoring time.

    Your WP-11 session log specifically flagged the silver-scope gap that drove the AE CloudOps TO. Validate the fix closes what you hit. Your CN-P0 session log specifically flagged `comp-validate --schema` pass-through gap — that's a separate proposal (E), not yet shipped, but note it as still-open in your audit.

    You are authorized to ship direct compiler patches. Commit under your own author line.
  </scope>

  <acceptance_criteria>
    1. Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-15/adhc_router_t4_compilers_audit.md`.
    2. Rule 7 format Compiler Tools section.
    3. Explicit "Would this have helped WP-11?" and "Would this have helped CN-P0?" paragraphs referencing specific points in each session log.
    4. Critical assessment of the silver-scope fix: does it feel like a full solution, or a patch that just addresses the surface symptom of a deeper architectural issue (asymmetric silver coverage across `comp-pipescript` subcommands)?
    5. Explicitly note any still-open gaps you hit at authoring time that are NOT closed by the 0324142a or silver-scope ships. The E/A/B/C/D/N1 proposals may each correspond to one of these.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript deployed bd_price_update.py</run>
        <expect>`[SILVER]` label + MATCH/STALE/MISSING verdict. Should work without the workarounds you had to use during WP-11.</expect>
        <if_mismatch>Silver-scope fix regression. Diagnose and patch.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed inject_scoped_overrides.py</run>
        <expect>Same shape.</expect>
        <if_mismatch>Same.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io bd_price_update.py</run>
        <expect>EXPECTED TO FAIL today — silver scope is only in `deployed`, not `io`. This is the known-open gap that `COMPILER_SILVER_SCOPE_FULL.md` proposes to close. Record the failure explicitly as evidence the proposal is still needed.</expect>
        <if_mismatch>If it unexpectedly works, that's good news — may mean silver scope expanded beyond `deployed` in a later commit. Verify and celebrate.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse nna_atomic</run>
        <expect>Empty PRODUCER + CONSUMED BY (new canonical field from CN-P0, no shadow write or consumer yet). Parallel to RA-P0 case DS~C is testing.</expect>
        <if_mismatch>Same empty-vs-broken disambiguation concern as T3 — flag if the tool output makes it hard to tell.</if_mismatch>
      </step>
      <step>
        <run>comp-validate nna_atomic --schema</run>
        <expect>EXPECTED TO FAIL today — validator pass-through is the E proposal, not yet shipped. Your CN-P0 log explicitly flagged this.</expect>
        <if_mismatch>If it works, the E proposal may have shipped silently — verify.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="during analysis">
      <step>
        <run>Re-read your WP-11 session log. Find the points where you flagged silver-scope as a coverage gap.</run>
        <expect>For each flagged point, assess: does the current silver-scope fix address the specific gap you hit? Was the fix surgical or structural?</expect>
        <if_mismatch>If surgical-only, the underlying asymmetry is still there and future silver work will hit the same wall in `io`/`feeds`/`consumers`. That's exactly what `COMPILER_SILVER_SCOPE_FULL.md` proposes. Write up specifically.</if_mismatch>
      </step>
      <step>
        <run>Re-read your CN-P0 session log. Look at the `comp-validate --schema` pass-through gap you flagged.</run>
        <expect>This is not yet shipped (E proposal). Your audit should confirm the gap is still open and reference `docs/architecture/COMPILER_VALIDATE_COVERAGE_AND_PASSTHROUGH.md` as the live proposal.</expect>
        <if_mismatch>If the proposal doc doesn't accurately describe the gap you hit, flag that too.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit (if you ship a patch)">
      <step>
        <run>Re-run Phase 1 commands.</run>
        <expect>Before/after evidence.</expect>
        <if_mismatch>Do not mark complete until the originally-failing run passes.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <permitted_edits>
    - `org/modules/graph/pipeline_cli.py`
    - `org/modules/graph/platinum_cli.py`
    - `org/modules/graph/extract_pipeline.py`
    - `org/modules/graph/extract_s3.py`
    - Test files.
  </permitted_edits>

  <out_of_scope>
    - No gold or silver script edits (A→D rerun sensitivity — WP-11 + scoped-overrides work already in flight for the rerun).
    - No CN-P1 shadow-write re-audit (already complete-in-fact pre-rerun).
  </out_of_scope>

  <deliverables>
    1. Session log with Rule 7 audit.
    2. Zero-to-N patches with commit hashes.
    3. Explicit mapping of each still-open gap you hit → the corresponding compiler proposal doc (A/B/C/D/E/N1).
  </deliverables>
</task_order>
