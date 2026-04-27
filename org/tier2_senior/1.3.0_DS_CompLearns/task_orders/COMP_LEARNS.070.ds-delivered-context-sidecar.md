<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-070-ds-delivered-context-sidecar</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Stage 3 ship-blocker R-DS-1 (parallel with .071/.072/.073)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §6 — Per-question per-condition delivered-context audit (R-DS-1)</ref>
    <ref type="prd_section">§6.3 — Sidecar schema; §6.4 — Auditability use cases (PATTERN C diagnosis, attribution claims, format failure forensics)</ref>
    <ref type="runner">comp/loop/runner.py — context delivery path; f5095ac0 path fix is the prior DS touch-point</ref>
    <ref type="scorecard">comp/bench/scorecard.py — schema at lines 133-160; two new fields required</ref>
    <ref type="cvo_ruling">CVO R-DS-1 (§6.2) — sidecar not scorecard-bloat; scorecard carries stable reference only</ref>
    <ref type="cvo_ruling_r_cto_3">CVO R-CTO-3 — PATTERN C diagnosis hampered by absence of direct delivered-context evidence; ship-blocker for Stage 3</ref>
    <ref type="pytest_baseline">458 tests passing (comp/ --ignore=comp/targets) — do not regress</ref>
  </references>

  <objective>
    Wire the runner to emit a per-question, per-condition delivered-context sidecar artifact on every scored run.
    The scorecard carries a stable reference to the sidecar manifest (not the blobs themselves).

    ## Context

    Click PATTERN C diagnosis required circumstantial inference about what context the selector delivered
    to the judge per question. Stage 3 makes this directly auditable. For every scored run, the runner
    must capture the exact compressed context string delivered to the judge for each (question, condition)
    pair and write it to a sidecar directory. A manifest.json ties the blobs together with SHA-256 hashes.
    The scorecard gains two new fields pointing to the manifest.

    This is a pure instrumentation change — it does not alter scoring logic, champion selection, or
    the ratchet decision path. The sidecar is write-only during a run; consumers (SC audit, CTO diagnosis)
    read it post-hoc.

    ## Phase 0 — Pre-implementation baseline gate

    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&1 | tail -3
    # Expect: 458 passed (or more). Zero failures.
    ```

    If tests fail before you touch anything, MCP COO immediately.

    ## Phase 1 — Runner changes (comp/loop/runner.py)

    After the context compression step and before the judge call, capture the delivered context string
    for each (question_id, condition) pair. Write it to:

    ```
    comp/results/<target>/<run_id>/delivered_context/<question_id>_<condition>.txt
    ```

    Where:
    - `<target>` = the target identifier (e.g., `dev-click-001`, `sphinx`)
    - `<run_id>` = a stable identifier for this ratchet run (use iteration number + timestamp, or the
      existing run identifier if one exists in the runner)
    - `<question_id>` = the question id string (e.g., `q01`, `q03`)
    - `<condition>` = the condition label (e.g., `C1`, `C2`, `C3`, `C4`)

    Directory creation: ensure the `delivered_context/` directory is created before writes.
    If the delivered context is empty (C1 unaided — no compiler context), write an empty file
    with a comment line `# C1 unaided -- no compiler context delivered`.

    After all questions for the run are scored, write the manifest:

    ```
    comp/results/<target>/<run_id>/delivered_context/manifest.json
    ```

    Manifest schema:
    ```json
    {
      "schema_version": 1,
      "run_id": "<run_id>",
      "target": "<target>",
      "compiler_content_sha": "<sha256[:8] of compiler.py>",
      "conditions": ["C1", "C2", "C3", "C4"],
      "question_ids": ["q01", "q02", ...],
      "blob_hashes": {
        "q01_C1": "<sha256 hex of q01_C1.txt>",
        "q01_C2": "<sha256 hex of q01_C2.txt>",
        ...
      }
    }
    ```

    Each value in `blob_hashes` is the SHA-256 hex digest of the corresponding `.txt` file content.
    Use `hashlib.sha256(content.encode()).hexdigest()` (or bytes if content is already bytes).

    ## Phase 2 — Scorecard changes (comp/bench/scorecard.py)

    Add two new optional fields to the scorecard JSON output (after the existing cost/provenance fields):

    ```json
    "delivered_context_ref": "comp/results/<target>/<run_id>/delivered_context/manifest.json",
    "delivered_context_manifest_sha": "<sha256 hex of manifest.json>"
    ```

    The `delivered_context_manifest_sha` is the SHA-256 of the manifest.json file content, computed
    after the manifest is written. This ensures end-to-end content addressing: any post-hoc edit to
    either a blob or the manifest is detectable from the scorecard.

    If the runner did not emit a sidecar (e.g., dry-run or non-standard mode), these fields may be
    omitted or set to null — do not make them required-or-error.

    ## Phase 3 — Pre-commit gate

    Run the commit gate on both changed files:
    ```bash
    .tools/ds-commit-gate.sh comp/loop/runner.py comp/bench/scorecard.py
    ```
    All three checks (py_compile + ds-precommit-check + ruff) must exit 0 for each file.

    Run the full test suite:
    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=short 2>&1 | tail -5
    ```
    458+ passed, 0 failed.

    ## Phase 4 — Smoke-test with dev-click-001

    Run one ratchet iteration against dev-click-001 with judge=mock (no API cost) to verify
    sidecar files are written:
    ```bash
    python comp/bin/comp-learns-ratchet click --judge mock --max-iter 1
    ls comp/results/dev-click-001/*/delivered_context/ 2>/dev/null | head -20
    python3 -c "import json; m=json.load(open(sorted(__import__('glob').glob('comp/results/dev-click-001/*/delivered_context/manifest.json'))[-1])); print('blobs:', len(m['blob_hashes']), 'manifest_sha set:', bool(m.get('compiler_content_sha')))"
    ```

    Verify: blob files present for each (question, condition) pair; manifest.json written; hashes non-empty.

    If dev-click-001 runs under the `click` target name, adjust the path accordingly. Check
    comp/targets/dev-click-001/ or comp/targets/click/ for how the runner resolves the target name.

    ## Phase 5 — Commit and push

    ```bash
    git commit --only \
      --author="1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>" \
      -m "feat(COMP_LEARNS.070): delivered-context sidecar (R-DS-1) -- per-Q per-condition blob + manifest + scorecard ref" \
      -- comp/loop/runner.py \
         comp/bench/scorecard.py
    git push origin CLOUD
    ```

    ## Phase 6 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Sidecar path format confirmed (sample path from smoke test)
    - manifest.json schema version
    - Scorecard fields added (delivered_context_ref, delivered_context_manifest_sha)
    - Test count (must be 458+)
    - Whether any edge case was found (e.g., C1 empty-context handling)
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&amp;1 | tail -3</run>
        <expect>458 passed (or more). Zero failures.</expect>
        <if_mismatch>STOP. Report failure count to COO before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh comp/loop/runner.py comp/bench/scorecard.py</run>
        <expect>All 3 checks exit 0 for each file (py_compile + ds-precommit-check + ruff).</expect>
        <if_mismatch>STOP. Fix flagged issue. Do not commit until gate exits 0.</if_mismatch>
      </step>
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=short 2>&amp;1 | tail -5</run>
        <expect>458+ passed, 0 failed.</expect>
        <if_mismatch>STOP. Fix regression before committing.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .071 (pilot machinery), .072 (SC pre-screen), .073 (COO packet schema).
      No shared artifact writes with those TOs.
      .075 (sphinx pre-screen execution) does NOT gate on this TO — pre-screen uses existing runner.
      Primary metric scoring runs in Stage 3 gate on this TO being complete.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/loop/runner.py emits per-question per-condition delivered-context .txt files to comp/results/&lt;target&gt;/&lt;run_id&gt;/delivered_context/ on every scored run.
    2. manifest.json written at end of run with schema_version=1, blob_hashes dict covering all (Q, condition) pairs.
    3. Each blob_hash value is the SHA-256 hex of the corresponding file content.
    4. comp/bench/scorecard.py adds delivered_context_ref and delivered_context_manifest_sha fields (null-safe if no sidecar).
    5. delivered_context_manifest_sha is SHA-256 of manifest.json content.
    6. ds-commit-gate.sh exits 0 on both runner.py and scorecard.py.
    7. pytest comp/ --ignore=comp/targets passes 458+ tests, 0 failures.
    8. Smoke test confirms sidecar files present for dev-click-001 mock run.
    9. Committed --only --author=1.3.0_DS_CompLearns. Pushed to CLOUD.
    10. MCP 2.1.0_SA_COO with commit sha + sidecar path format + test count.
  </acceptance_criteria>

  <dependencies>
    - No gates. Parallelizable with .071/.072/.073.
    - .075 (sphinx pre-screen execution) does NOT require this TO — pre-screen predates 4-condition scoring.
    - Stage 3 primary case dispatch (post-.076) requires this TO complete.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis in code or logs.
    - from __future__ import annotations not required for runner.py / scorecard.py, but run pre-commit gate.
    - Do NOT alter scoring logic, champion selection, or ratchet decision paths.
    - Do NOT add sidecar fields to the champion.json — sidecar is run-scoped, not champion-scoped.
    - C1 unaided produces empty context by design — handle gracefully (empty file with comment line is acceptable).
    - run_id should be deterministic and stable for a given ratchet run so that a re-run of the same
      iteration produces the same sidecar path. Using iteration number + date suffix is acceptable.
      Check how the runner currently identifies runs and follow that convention.
    - ANTHROPIC_API_KEY is not needed for Phase 4 smoke test (--judge mock).
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO with commit sha + sidecar format + test count
    - session log
  </closeout>
</task_order>
