<task_order>
  <metadata>
    <id>ADHC_COMPIL.007.ae-validate-cli-hint</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-27</date>
    <status>staged</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>E stretch (v2)</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V2.md §3.3 AC4 + §4 (commit 653b0469)</prd_ref>
    <effort>0.5 weeks</effort>
    <gates_on>ADHC_COMPIL.006 COMPLETE — protocol doc must exist before CLI can point to it</gates_on>
    <optional>true</optional><!-- v2 ships when .005 + .006 complete; .007 is stretch -->
  </metadata>

  <objective>
    Add a one-line "next step" hint to comp-validate's non-zero exit output
    pointing operators to the failure-mode protocol doc. Currently when
    comp-validate fails, operators see the validation report but no guidance
    on what to do next. A single hint line eliminates most ad-hoc retry confusion.
  </objective>

  <scope>
    Modify .tools/comp-validate (or the underlying validate runner) to print
    on non-zero exit:

      Hint: see COMP_VALIDATE_PROTOCOL.md §3 for retry policy

    (Exact wording may vary — match whatever section covers retry policy in the
    .006 deliverable.)

    The hint must:
    - Only print on non-zero exit (do NOT print on clean pass)
    - Use plain ASCII (no emoji — CloudWatch/CI compatibility per CLAUDE.md)
    - Not change the exit code or any other output format
    - Be a single line, not a paragraph
  </scope>

  <acceptance_criteria>
    1. comp-validate <script> --artifact <path> (with validation error) →
       non-zero exit, existing report output unchanged, PLUS one trailing line:
       "Hint: see COMP_VALIDATE_PROTOCOL.md §3 for retry policy"
    2. comp-validate <script> --artifact <path> (clean pass) →
       exit 0, no hint line printed.
    3. COMP_VALIDATE_PROTOCOL.md §3 actually covers retry policy (coordination
       with .006 — confirm section number before hardcoding).
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT change comp-validate exit codes.</rule>
    <rule>Do NOT change comp-validate output format other than appending the hint line.</rule>
    <rule>Do NOT start before ADHC_COMPIL.006 is complete — hint must point to
    a section that exists.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">.tools/comp-validate with hint on non-zero exit</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO with: AC1+AC2 test outputs</deliverable>
  </deliverables>
</task_order>
