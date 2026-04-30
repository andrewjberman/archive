<task_order>
  <metadata>
    <id>ADHC_COMPIL.009.ae-validate-windows-path-translator</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-30</date>
    <status>complete</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>F.2 (v3)</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V3.md §4.2</prd_ref>
    <effort>1 day</effort>
    <gates_on>None</gates_on>
    <bundle_recommendation>Bundle with .008 + .010 — same AE owner, same release window, common .tools/ file-set.</bundle_recommendation>
  </metadata>

  <objective>
    Stop forcing every DS agent to retry every `comp-validate` command because
    POSIX `/tmp/...` paths don't resolve under Windows Python. 8+ FAIL→retry
    pairs in the past two weeks (PRD §2.2 #2, log lines 663–666, 937, 941,
    1117, 1425, 1445, 1534, 1623). Pure friction; agents already know to retry
    with `C:/tmp/`, but the tool should translate transparently.
  </objective>

  <scope>
    Modify .tools/comp-validate (Python entry) to translate POSIX paths to
    Windows paths in the `--artifact` argument handler, before opening the
    file:

    1. Detect Windows host: `platform.system() == 'Windows'`. Note that
       `sitecustomize.py` mocks `platform.system` to return `'Windows'` per
       the AWS-hang fix (MEMORY.md "AWS CLI Hang Fixes (Windows) — Fix 2").
       The detection works against the mocked value.
    2. If argument starts with `/tmp/`: rewrite to `C:/tmp/`
    3. If argument starts with `/c/` (MSYS2 form): rewrite to `C:/`
    4. If neither original nor translated path exists, error message MUST
       show BOTH the original and translated paths so the operator can debug
       which step failed.

    Apply the same translation to JSON and parquet artifacts (the parquet
    reader path also opens the file directly; both paths need the
    translation). Single helper function called from both code paths.

    Linux/macOS hosts: NO translation. Pass paths through unchanged. The
    detection is gated on Windows specifically.
  </scope>

  <acceptance_criteria>
    1. On Windows: `comp-validate <id> --artifact /tmp/x.json` works
       identically to `comp-validate <id> --artifact C:/tmp/x.json` — same
       exit code, same stdout.
    2. On Windows: `comp-validate <id> --artifact /c/Users/AndrewBerman/AppData/Local/Temp/x.json`
       works identically to the Windows-absolute form
       `C:/Users/AndrewBerman/AppData/Local/Temp/x.json`.
    3. On Windows: parquet artifacts under `/tmp/role_aua_sample.parquet`
       (the form that FAILed at log line 1473) work after translation.
    4. On Windows: when neither original nor translated path exists, error
       output contains both the input path AND the rewritten path on
       separate lines.
    5. Linux/macOS spot-check: `comp-validate <id> --artifact /tmp/x.json`
       behavior unchanged (no rewriting; standard POSIX resolution).
       Verifiable on the AE 0.7 host or a Linux runner if available; if no
       Linux host accessible, document a unit-test mock that confirms the
       Windows-only branch.
    6. Test fixture: 3 representative validate configs (D_04, cohort_a_summary,
       nna_atomic) × 4 path forms (POSIX `/tmp/`, MSYS `/c/`, Windows
       relative `tmp/`, Windows absolute `C:/...`) = 12 cases on Windows;
       all PASS where the file exists, all show dual-path error otherwise.
    7. Append one row per AC to `org/compiler-tools-log.md`.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT translate paths on Linux/macOS hosts — POSIX is correct there. Translation is Windows-only.</rule>
    <rule>Do NOT silently swallow the translation step — always emit both the original and translated path in error output, so operators don't get confused about which was attempted.</rule>
    <rule>Do NOT modify `comp-validate` exit codes or output format beyond the error-message dual-path additions.</rule>
    <rule>Do NOT introduce a `--no-translate` flag — the goal is transparent fix, not a knob.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">.tools/comp-validate with Windows POSIX-path translation</deliverable>
    <deliverable type="code">Test fixture covering 12 Windows cases + Linux mock</deliverable>
    <deliverable type="document">Session log with AC1–AC7 verification output (stdout diffs for AC1–AC3)</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO with: AC1–AC3 stdout-diff PASS, AC4 dual-path error excerpt, AC5 Linux confirmation method, fixture pass count</deliverable>
  </deliverables>

  <compiler_tools_mandate>
    Phase 1 (before write):
    - Direct read of .tools/comp-validate to locate the artifact-opening code
      paths (both JSON and parquet readers)
    - Verify MEMORY.md "AWS CLI Hang Fixes" and confirm `platform.system()`
      returns `'Windows'` from the mocked sitecustomize.py

    Phase 2 (before commit):
    - Run the 12 Windows fixture cases; capture exit codes + stdout
    - Run one validate against a real artifact path (e.g.
      `/tmp/cohort_a_summary.json` after first uploading via `aws s3 cp` from
      a current gold artifact) end-to-end to confirm the translation works
      against a live config

    Phase 3 (after commit):
    - Append one row per AC to `org/compiler-tools-log.md`
    - Confirm in next session window that `--artifact /tmp/...` FAIL→retry
      pattern drops to zero
  </compiler_tools_mandate>
</task_order>
