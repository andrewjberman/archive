<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <id>2.0.0_SA_COO-2026-04-24-adhc-ownpth-002-ds-hook-script-impl</id>
  <project>ADHC_OWNPTH</project>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_to>0.4.0_DS_ClientPlatform</issued_to>
  <issued_date>2026-04-24</issued_date>
  <status>staged</status><!-- STAGED: gates on ADHC_OWNPTH.001 (CTO .owned-paths.yaml) completion -->

  <title>ADHC_OWNPTH TO 2 — Hook script + validator implementation (DS tooling lane)</title>

  <references>
    <ref type="prd">docs/architecture/ADHC_OWNPTH.md</ref>
    <ref type="yaml">`.owned-paths.yaml` (repo root — TO 1 output; read before coding)</ref>
  </references>

  <context>
    TO 1 (1.0.0_SA_CTO) produces `.owned-paths.yaml` at repo root. TO 2 implements the hook
    script that reads that YAML and enforces lane ownership at commit time. DS owns the
    `.tools/` lane (established precedent: comp-* tools, ds-commit-gate.sh, etc.). DS is
    authoring this hook because it is Python+bash tooling, not because it is a data script.

    Hook behavior per PRD §6.2: reads `GIT_AUTHOR_NAME` from env, extracts agent serial,
    reads staged file list via `git diff --cached --name-only`, resolves each file to a lane
    via YAML, checks if author is in permitted_agents. Phase 1 (OWNED_PATHS_MODE=warn):
    EXIT 0 with WARN banner + audit log. Phase 2 (OWNED_PATHS_MODE=block): EXIT 1 with
    ERROR banner. --author-override LANE escape hatch honored in both phases.
  </context>

  <scope>
    Implement two files:

    1. `.tools/owned-paths-validate.py` (Python 3.9+, stdlib only — no pip deps)
       - Parses `.owned-paths.yaml` (via `yaml.safe_load`)
       - Implements longest-match-wins path glob resolution (fnmatch or pathlib)
       - Exposes `resolve_lane(path: str) -> str | None` and `check_agent(agent: str, path: str, lanes: dict) -> bool`
       - CLI mode: `owned-paths-validate.py .owned-paths.yaml` → exit 0 if YAML parses + all lane refs resolve; exit 1 with error list otherwise
       - Must begin with `from __future__ import annotations` (CLAUDE.md rule 15)

    2. `.tools/git-hooks/owned-paths-check.sh` (bash)
       - Reads `GIT_AUTHOR_NAME` env var; extracts agent serial (strip email portion)
       - Calls `git diff --cached --name-only` to get staged file list
       - Invokes `owned-paths-validate.py` for resolution
       - Per-file: calls resolve_lane; checks agent in permitted_agents for that lane
       - Aggregates violations; if any:
           OWNED_PATHS_MODE=warn  (default Phase 1): print WARN banner to stderr; append to
             org/git-author-override-audit.log; EXIT 0
           OWNED_PATHS_MODE=block (Phase 2): print ERROR banner to stderr; EXIT 1
       - --author-override LANE: if GIT_COMMIT_AUTHOR_OVERRIDE is set in env, skip
           lane check for that commit; append OVERRIDE entry to audit log; EXIT 0
       - Audit log line format:
           {ISO8601} {PASS|WARN|BLOCK|OVERRIDE}  {agent_serial}  {N_files}  ({detail})
       - Handles edge cases: no staged files (exit 0), YAML not found (WARN + exit 0 in
           warn mode; ERROR + exit 1 in block mode), GIT_AUTHOR_NAME not set (WARN only)

    3. `tests/owned_paths_check_test.py` (stdlib unittest)
       - Positive: AE 0.7.0 commits to infra/aws/ → PASS (in CLOUD_OPS_OR_ETL lane)
       - Negative warn: AE 0.7.0 commits to org/tier1_exec/1.0.0_SA_CTO/ → WARN (exit 0)
       - Negative block: same as above with OWNED_PATHS_MODE=block → exit 1
       - Override: AE 0.7.0 commits to org/ with GIT_COMMIT_AUTHOR_OVERRIDE=ANY_EXEC → PASS + audit log entry
       - Canary: reproduce incident #4 pre-fix state — stage 50 files under
           org/tier1_exec/1.1.0_SA_CTO/ with author 0.7.0_AE_CloudOps → violation list
           cites all 50 files

    Do NOT modify `.owned-paths.yaml` (TO 1 scope).
    Do NOT wire `.git/hooks/pre-commit` (TO 3 scope).
  </scope>

  <dependencies>
    <dependency agent="1.0.0_SA_CTO" task="ADHC_OWNPTH.001" status="staged"
                required=".owned-paths.yaml must exist at repo root before DS codes against its schema. Read the YAML before writing any path-resolution logic."/>
  </dependencies>

  <data_reprocess_scope>
    <no_reprocess_needed>
      This TO produces tooling files only (.tools/ + tests/). No data scripts modified.
      No silver/bronze/gold reprocess required.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat .owned-paths.yaml | python3 -c "import yaml,sys; d=yaml.safe_load(sys.stdin); print('lanes:', list(d.get('lanes',{}).keys())[:10])"</run>
        <expect>TO 1 must be complete. Prints first 10 lane names. If .owned-paths.yaml not found, STOP — TO 1 is not done yet.</expect>
        <if_mismatch>STOP. Do not implement the hook until .owned-paths.yaml exists and parses.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile .tools/owned-paths-validate.py</run>
        <expect>Exit 0. No syntax errors.</expect>
        <if_mismatch>STOP. Fix syntax before committing.</if_mismatch>
      </step>
      <step>
        <run>bash -n .tools/git-hooks/owned-paths-check.sh</run>
        <expect>Exit 0. No bash syntax errors.</expect>
        <if_mismatch>STOP. Fix bash syntax before committing.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh .tools/owned-paths-validate.py</run>
        <expect>Exit 0. py_compile + AST scan + ruff check all pass.</expect>
        <if_mismatch>STOP. Fix all gate failures before committing.</if_mismatch>
      </step>
      <step>
        <run>python -m pytest tests/owned_paths_check_test.py -v (or python -m unittest tests/owned_paths_check_test.py)</run>
        <expect>All tests pass: positive, negative-warn, negative-block, override, canary.</expect>
        <if_mismatch>STOP. Fix test failures before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>.tools/owned-paths-validate.py .owned-paths.yaml</run>
        <expect>Exit 0. All lane refs resolve; YAML valid.</expect>
        <if_mismatch>Surface to 2.0.0_SA_COO. YAML may need adjustment before TO 3 wiring.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. `.tools/owned-paths-validate.py` exists; stdlib only; begins with `from __future__ import annotations`.
    2. `.tools/git-hooks/owned-paths-check.sh` exists; reads YAML via validate.py; phase-controlled via OWNED_PATHS_MODE.
    3. `--author-override` escape hatch implemented; appends OVERRIDE line to audit log.
    4. Audit log format matches PRD §6.3 exactly (ISO8601 + PASS/WARN/BLOCK/OVERRIDE + agent + N_files + detail).
    5. All 5 unit tests pass (positive, negative-warn, negative-block, override, canary).
    6. Canary test explicitly reproduces incident #4: 50 files under org/tier1_exec/1.1.0_SA_CTO/ + AE 0.7.0 author → violation list.
    7. ds-commit-gate.sh exit 0 on owned-paths-validate.py.
    8. `bash -n` exit 0 on owned-paths-check.sh.
    9. `.tools/owned-paths-validate.py .owned-paths.yaml` exit 0 post-commit.
    10. Session log includes compiler tools section with all runs + explicit pass/fail.
    11. MCP COO with commit hash + canary test output on completion.
  </acceptance_criteria>

  <evidence>
    <!-- To be filled by DS on completion -->
  </evidence>
</task_order>
