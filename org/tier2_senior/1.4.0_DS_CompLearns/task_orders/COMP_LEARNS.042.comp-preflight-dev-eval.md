<task_order>
  <metadata>
    <id>1.4.0_DS_CompLearns-2026-04-22-comp-learns-042-comp-preflight-dev-eval</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.4.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>complete <!-- commit f6f29836 pushed CLOUD 2026-04-22 by 1.4.0_DS_CompLearns --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — AUTOMATION_V1 foundation; gates .043 (wave runner) and .044 (dev loop); first automation TO</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_AUTOMATION_V1.md §4 (micro-cycle contract) + §5 (preflight checker) + §13 (TO decomposition)</ref>
    <ref type="existing_wave1_data">comp/results/pilot-wave-1/ — reference for eval-mode bundle shape (refactor.patch + test_output.txt + reasoning.md)</ref>
    <ref type="handoff_log">org/tier1_exec/1.1.0_SA_CTO/logs/2026-04-22/session13_wave2_prd_handoff.md — CTO authoritative handoff</ref>
  </references>

  <objective>
    Implement comp/bin/comp-preflight.py — the dual-mode preflight checker that gates
    DS→SC handoffs (eval mode) and DS→comp-dev-loop hand-offs (dev mode).

    Explicitly in scope:

    1. CLI interface per §5:
       ```
       comp-preflight --task <task_id> --bundle-path <path> --condition <a|b> [--mode dev|eval]
       ```
       Default mode: `eval`. Exits 0 on pass, exits 1 on failure. Structured JSON to stdout
       in both cases (format per §5 diagnostic output).

    2. Checks that run in BOTH modes:
       - CHECK 1: task packet present + valid (comp/tasks/{task_id}/packet.yaml exists,
         required fields populated, schema_version matches current)
       - CHECK 2: candidate bundle complete
         - eval mode: refactor.patch (or changes.patch) + test_output.txt + reasoning.md present
         - dev mode: changes.patch + result.json present, both non-empty; result.json must
           include baseline_commit, compiler_sha, target_version, mutation_type,
           intervention_tag, validation_level. Any extra files beyond those two: EXIT 1.

    3. Checks dev mode ONLY:
       - CHECK 2b: worktree HEAD coherence (SOFT — logs WARNING, does NOT block). DS
         worktree HEAD should match either task packet's baseline_commit OR an explicitly
         recorded branch head. Mismatch is non-blocking but appears in diagnostic output
         under "warnings".

    4. Checks eval mode ONLY (skipped in dev mode):
       - CHECK 3: scoring manifest computed + pinned — manifest_hash computable from
         baseline_commit + task_packet_id + scorer_prompt_version + checklist_version +
         judge_mode + harness_exposure_profile + allowed_artifacts + schema_version.
         Matches expected or logs new anchor.
       - CHECK 4: scorer doctrine version pinned — SC prompt hash + checklist hash match
         pinned values. Mismatch: EXIT 1 (doctrine drift).
       - CHECK 5: clean scorer worktree provisioned — scorer worktree seeded from
         baseline_commit, no uncommitted changes, candidate bundle not embedded in worktree
         source tree.
       - CHECK 6: allowed artifacts surface clean — scorer input contains only packet.yaml
         + bundle (diff + test_output.txt); reasoning.md explicitly absent from scorer
         input surface; no DS session logs, no prior verdict files, no other task artifacts.
       - CHECK 7: budget compliance (SOFT — logs, does not block). If bundle metadata
         includes wall_clock_sec + token_count, verify within packet budget; overrun logs
         WARNING in diagnostic output.

    5. Diagnostic output format per §5 — structured JSON to stdout:
       ```json
       {
         "pass": bool,
         "mode": "dev"|"eval",
         "task_id": str,
         "condition": "a"|"b",
         "timestamp": "ISO8601",
         "checks": {<check_name>: "PASS"|"FAIL"|"SKIP", ...},
         "failure_reason": str|null,
         "warnings": [str, ...]
       }
       ```
       SKIP is used for eval-only checks in dev mode.

    6. Unit tests at comp/tests/test_preflight.py covering:
       - Eval mode: valid bundle → exit 0, all 7 checks PASS (with budget=WARNING accepted)
       - Eval mode: missing reasoning.md → exit 1, failure_reason populated
       - Eval mode: scorer worktree has uncommitted change → exit 1 at CHECK 5
       - Eval mode: reasoning.md leaked into scorer input surface → exit 1 at CHECK 6
       - Dev mode: valid micro-cycle → exit 0, CHECKs 3-7 all SKIP
       - Dev mode: result.json missing required field (e.g. compiler_sha) → exit 1 at CHECK 2
       - Dev mode: extra file in bundle (e.g. test_output.txt present but not required) → exit 1 at CHECK 2 (strict: only 2 files)
       - Dev mode: worktree HEAD mismatch → exit 0 with WARNING in diagnostic (soft gate)
       - Common: invalid task_id → exit 1 at CHECK 1
       - Both modes: diagnostic JSON structure valid

    7. Fixtures under comp/tests/fixtures/preflight/ — reuse pilot-wave-1 bundle data where
       possible; construct minimal synthetic fixtures for dev-mode cases.

    Explicitly out of scope:
    - Running SC (comp-preflight only validates the pre-handoff state; it does not invoke SC)
    - Wave orchestration (.043 is the wave runner — preflight is one step in that loop)
    - Dev loop iteration (.044 is comp-dev-loop — preflight is called by it per iteration)
    - Manifest hash computation library (if needed, add a minimal helper; do NOT build a
      full manifest-infra subsystem — keep scope tight to what CHECK 3 + CHECK 4 require)
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-build && pytest comp/ -q</run>
        <expect>Rebuild clean; all existing tests PASS.</expect>
        <if_mismatch>Rebase on current CLOUD or fix any pre-existing red before starting.</if_mismatch>
      </step>
      <step>
        <run>ls comp/bin/</run>
        <expect>Lists existing comp/bin/ scripts (e.g. any prior runners). Confirms comp/bin/ exists as the landing directory for CLI tooling; if absent, this TO creates it.</expect>
        <if_mismatch>If comp/bin/ does not exist, create it with __init__.py. Note the creation in commit message.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile comp/bin/comp-preflight.py</run>
        <expect>Exit 0 — no syntax errors.</expect>
        <if_mismatch>STOP. Fix syntax before proceeding.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/bin/comp-preflight.py comp/tests/test_preflight.py</run>
        <expect>Exit 0 — py_compile clean + AST undefined-name scanner clean.</expect>
        <if_mismatch>STOP. Resolve each flagged issue (missing import, typo, rename miss). Do NOT commit until clean.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/tests/test_preflight.py -v</run>
        <expect>All test_preflight cases PASS — coverage includes both modes and all failure paths enumerated in §5.</expect>
        <if_mismatch>STOP. Debug and fix. Do NOT commit a partially passing test file.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>Full comp/ suite GREEN. No regressions.</expect>
        <if_mismatch>STOP. Investigate and fix before commit.</if_mismatch>
      </step>
      <step>
        <run>python comp/bin/comp-preflight.py --task task-001-httpx-netrc-host-authority --bundle-path comp/results/pilot-wave-1/bundles/task-001-ds-1.3.0-condition_a-run-1 --condition a --mode eval</run>
        <expect>Exit 0 (or exit 1 with pre-wave-1 missing reasoning/manifest — whichever is real). JSON to stdout parses clean. Document the exact observed output in session log.</expect>
        <if_mismatch>If wave-1 bundle fails preflight for a reason not caught by your tests, add a test case for it. This is the "dry-run against wave 1 data" gate from .043 but applied here at module level.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-build</run>
        <expect>Rebuild succeeds post-commit. No stale-cache warnings.</expect>
        <if_mismatch>Surface to COO — likely concurrent edit. Re-run pytest comp/ -q to confirm no regression.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/tests/test_preflight.py -v --tb=short</run>
        <expect>Still GREEN. Confirms post-commit state.</expect>
        <if_mismatch>Investigate — uncommitted local state must have influenced earlier runs. Fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>.043 (comp-wave-runner, 1.3.0_DS) calls comp-preflight.py in its per-event loop; stable CLI + exit code + stdout JSON schema is the contract. .044 (comp-dev-loop, 1.1.0_DS) also calls comp-preflight.py in --mode dev on every iteration. Do NOT change the CLI contract after ship — breakage cascades to both. If the implementation reveals the §5 spec is underspecified, flag to COO before diverging.</note>
    <shared_artifacts>comp/bin/comp-preflight.py (read by .043 + .044 via subprocess); diagnostic JSON schema (consumed by both); comp/tests/fixtures/preflight/ (may be reused by .043 dry-run fixtures)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/bin/comp-preflight.py implements the §5 CLI with --mode dev|eval (default eval).
    2. All 7 checks + CHECK 2b implemented per §5; eval-only checks SKIP cleanly in dev mode.
    3. Diagnostic JSON to stdout matches §5 format in both pass and fail paths.
    4. comp/tests/test_preflight.py covers the enumerated unit test cases; all PASS.
    5. pytest comp/ -q GREEN end-to-end (no regressions).
    6. Dry-run against wave-1 bundle documented in session log (exit code + JSON observed).
    7. Commit under --author=1.4.0_DS_CompLearns@opal.agent with --only pathspec scoped to comp/bin/comp-preflight.py + comp/tests/test_preflight.py (+ fixtures if added).
    8. Pushed to CLOUD.
    9. Session log at org/tier2_senior/1.4.0_DS_CompLearns/logs/2026-04-22/ with Compiler Tools section documenting every mandate run.
    10. MCP COMPLETE to 2.1.0_SA_COO with commit sha — unblocks .043 + .044 GO.
  </acceptance_criteria>

  <dependencies>
    - No blocking upstream. Execute immediately on GO receipt.
    - Blocks: .043 (wave runner calls preflight); .044 (dev loop calls preflight); .045 (Stage 2 activation review dry-runs preflight).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb. Confirm pwd.
    - Ds-commit-gate.sh on comp-preflight.py + test_preflight.py before commit — this is the universal rule for every Python edit (CLAUDE.md Rule 14).
    - If manifest_hash computation requires hashing a scorer prompt file and the canonical location is uncertain: per §5 CHECK 4, it is the SC prompt file hash — resolve to the actual SC prompt path (likely org/tier2_senior/2.1.0_SC_CompLearns/prompt.md or deliverables/sc-prompt-*.md). If ambiguous, MCP COO for arbitration; do not invent.
    - reasoning.md exclusion (CHECK 6) is mechanically enforced — scorer input surface is the directory/tarball provisioned TO SC, NOT the raw bundle path. If .043 wave runner handles provisioning, CHECK 6 verifies the provisioned surface, not the source bundle.
    - If §5 ambiguity arises during implementation: single clarification MCP to COO, do NOT make a unilateral call on semantic contract.
    - No emojis in any stdout / log output (CLAUDE.md Code Quality).
  </operational_notes>

  <closeout>
    On completion:
    - commit with --only --author="1.4.0_DS_CompLearns &lt;1.4.0_DS_CompLearns@opal.agent&gt;" -- comp/bin/comp-preflight.py comp/tests/test_preflight.py [fixtures]
    - push to CLOUD
    - flip TO status to complete with commit ref
    - MCP COMPLETE to 2.1.0_SA_COO with commit sha — this authorizes .043 + .044 GO
    - session log with Compiler Tools section reproducing each mandate <run>
  </closeout>
</task_order>
