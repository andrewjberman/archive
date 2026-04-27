<task_order>
  <metadata>
    <id>ADHC_COMPIL.004.ae-prd-evidence-check</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-27</date>
    <status>staged</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>C stretch</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL.md §6.2.4 + §6.3 AC4 (commit 172470a8)</prd_ref>
    <effort>1 week</effort>
    <gates_on>ADHC_COMPIL.003 COMPLETE (template must exist before linter can check for §5)</gates_on>
  </metadata>

  <objective>
    Author .tools/prd-evidence-check.sh — a lint script that scans new PRDs
    in docs/architecture/ for the §5 Compiler Evidence header and at least one
    compiler-tool invocation citation. Warn-only, never block. Establishes a
    one-time coverage baseline for existing PRDs.
  </objective>

  <scope>
    .tools/prd-evidence-check.sh behavior:
    1. Accept one or more PRD file paths as arguments (or scan docs/architecture/ if no args).
    2. For each PRD file:
       a. Check for a §5 Compiler Evidence header (case-insensitive match on
          "## 5" or "# Compiler Evidence" or equivalent).
       b. Check for at least one comp-* tool invocation cited in the file body
          (comp-pipescript, comp-blast, comp-iam, comp-routes, comp-platinum,
          comp-transform, comp-validate, comp-cache, comp-pii, comp-trace,
          comp-build, comp-diff, comp-xref).
    3. Output: PASS / WARN per file. WARN if §5 missing OR no comp-* citation found.
    4. Exit 0 always (warn-only, never block commits).
    5. --baseline flag: runs against all PRDs in docs/architecture/, writes
       coverage summary to org/compiler-tools-log.md with timestamp + per-file
       PASS/WARN status.

    Run the --baseline mode once on all existing PRDs after shipping and commit
    the coverage report to org/compiler-tools-log.md.

    The script should be runnable as: prd-evidence-check.sh <file> (single PRD)
    or prd-evidence-check.sh --baseline (full scan).
  </scope>

  <acceptance_criteria>
    1. prd-evidence-check.sh exists in .tools/ and is executable.
    2. prd-evidence-check.sh <new-prd-with-section-5> → PASS
    3. prd-evidence-check.sh <new-prd-without-section-5> → WARN, exit 0
    4. prd-evidence-check.sh --baseline runs against all docs/architecture/ PRDs,
       exits 0, coverage report committed to org/compiler-tools-log.md.
    5. Script uses plain ASCII output (no emoji — CloudWatch/CI compatibility).
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT exit non-zero — warn-only is mandatory. Never block a commit.</rule>
    <rule>Do NOT start before ADHC_COMPIL.003 is complete — template must exist
    to verify the §5 pattern against.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">.tools/prd-evidence-check.sh</deliverable>
    <deliverable type="document">org/compiler-tools-log.md baseline entry (--baseline run)</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO with: AC test outputs + baseline coverage report path</deliverable>
  </deliverables>
</task_order>
