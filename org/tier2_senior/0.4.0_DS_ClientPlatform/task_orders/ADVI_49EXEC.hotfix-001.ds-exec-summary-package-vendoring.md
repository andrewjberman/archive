<task_order>
  <metadata>
    <id>ADVI_49EXEC.hotfix-001.ds-exec-summary-package-vendoring</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-27</date>
    <status>pending</status><!-- GO: dispatched with this TO. P0 hotfix — Lambda live but broken on EventBridge fire. -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P0 hotfix — exec-summary Lambda fails on every EventBridge trigger</priority>
  </metadata>

  <context>
    DT deployed exec-summary Lambda (exec-summary-v0.1.0, TO7 COMPLETE). Lambda is live and
    EventBridge rule is wired. BUT Lambda fails on invocation with:
      Runtime.ImportModuleError: No module named 'exec_summary'

    Root cause: lambda_function.py imports from the exec_summary package
    (e.g. `from exec_summary.config import ...`). The build zip was created from
    infra/aws/lambda/exec-summary-generator/ which has the modules as flat files
    (config.py, metrics.py, etc.) but NOT as an exec_summary/ package subdirectory.

    Current state of infra/aws/lambda/exec-summary-generator/:
      config.py, lambda_function.py, metrics.py, platinum_reader.py, prompts/, validator.py
      (no exec_summary/ subdir, no __init__.py)

    Fix: create infra/aws/lambda/exec-summary-generator/exec_summary/ and copy the full
    package from data/black_diamond/scripts/exec_summary/ there. DT re-uploads + applies.
  </context>

  <objective>
    Create the exec_summary package subdirectory inside the Lambda source dir so the
    zip builder picks it up, then upload the new zip to S3. DT handles terraform apply + tag.
  </objective>

  <scope>
    Step 1 — Create package subdirectory:
      mkdir -p infra/aws/lambda/exec-summary-generator/exec_summary

    Step 2 — Copy all files from source package (preserve __init__.py):
      cp data/black_diamond/scripts/exec_summary/__init__.py infra/aws/lambda/exec-summary-generator/exec_summary/
      cp data/black_diamond/scripts/exec_summary/config.py infra/aws/lambda/exec-summary-generator/exec_summary/
      cp data/black_diamond/scripts/exec_summary/metrics.py infra/aws/lambda/exec-summary-generator/exec_summary/
      cp data/black_diamond/scripts/exec_summary/platinum_reader.py infra/aws/lambda/exec-summary-generator/exec_summary/
      cp data/black_diamond/scripts/exec_summary/validator.py infra/aws/lambda/exec-summary-generator/exec_summary/
      cp data/black_diamond/scripts/exec_summary/template_library.py infra/aws/lambda/exec-summary-generator/exec_summary/
      cp data/black_diamond/scripts/exec_summary/trigger_eval.py infra/aws/lambda/exec-summary-generator/exec_summary/
      cp -r data/black_diamond/scripts/exec_summary/prompts infra/aws/lambda/exec-summary-generator/exec_summary/prompts

    Step 3 — Pre-commit gate (mandatory per CLAUDE.md Rule 14):
      .tools/ds-commit-gate.sh infra/aws/lambda/exec-summary-generator/exec_summary/config.py \
        infra/aws/lambda/exec-summary-generator/exec_summary/platinum_reader.py \
        infra/aws/lambda/exec-summary-generator/exec_summary/validator.py \
        infra/aws/lambda/exec-summary-generator/exec_summary/metrics.py \
        infra/aws/lambda/exec-summary-generator/exec_summary/template_library.py \
        infra/aws/lambda/exec-summary-generator/exec_summary/trigger_eval.py
      All 3 checks must exit 0. If any fail: MCP COO.

    Step 4 — Commit under DS author (--only, no staging of other files):
      git commit --only --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>" \
        -m "fix(ADVI_49EXEC.hotfix-001): vendor exec_summary package into Lambda source dir" \
        -- infra/aws/lambda/exec-summary-generator/exec_summary/

    Step 5 — Build and upload new zip:
      bash infra/aws/lambda/ci/build-and-upload.sh exec-summary
      Confirm S3 upload completes (new version ID logged).

    Step 6 — RAVC4 MCP to 2.0.0_SA_COO + 0.4.0_DT_ClientPlatform with:
      - Commit hash
      - build-and-upload.sh output / new S3 version ID
      - Gate results (all 3 checks PASS)
      DT will then: terraform apply (1 change: source hash) → tag exec-summary-v0.1.1 → RAVC COO
  </scope>

  <acceptance_criteria>
    1. infra/aws/lambda/exec-summary-generator/exec_summary/__init__.py exists.
    2. All 7 modules copied: config, metrics, platinum_reader, validator, template_library, trigger_eval, __init__.
    3. ds-commit-gate.sh exits 0 on all copied .py files.
    4. Commit under DS author with --only pathspec.
    5. build-and-upload.sh exec-summary completes with new S3 version ID.
    6. RAVC4 to COO + DT with evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before commit">
      <run>.tools/ds-commit-gate.sh [all copied .py files]</run>
      <expect>py_compile + AST + ruff all exit 0. These are copies of already-gated code — should PASS.</expect>
      <if_mismatch>MCP COO immediately. Do not commit.</if_mismatch>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - DT 0.4.0: On DS RAVC4, DT runs: terraform plan (expect 1 change: source_code_hash) → apply → tag exec-summary-v0.1.1 → RAVC COO.
    - Do NOT run terraform apply yourself — that is DT scope.
    - Do NOT touch infra/aws/terraform/exec-summary/ — DS scope is Lambda source dir only.
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT modify lambda_function.py — the import structure is correct; we're adding the package it imports from.</rule>
    <rule>Do NOT run terraform apply — DT does that after DS RAVC4.</rule>
    <rule>Do NOT use git add -A or bare git commit — use git commit --only with explicit path.</rule>
  </do_not>
</task_order>
