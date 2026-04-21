<task_order>
  <metadata>
    <id>1.4.0_DS_CompLearns-2026-04-21-comp-learns-028-legacy-loop-decommission</id>
    <issued_by>1.1.0_SA_CTO</issued_by>
    <issued_to>1.4.0_DS_CompLearns</issued_to>
    <date>2026-04-21</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — Phase 4 exit; only runs after .027 closes green</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_RUNTIME_V1.md §3.C (Layer C rules), §13 (Phase 4), §14 (success bar)</ref>
    <ref type="code">comp/framework/run.py, comp/bin/comp-learns-run.sh, comp/framework/results_schema.py, any `results.tsv` consumers</ref>
  </references>

  <objective>
    Remove or fully quarantine the legacy evaluation loop so there is exactly one meaningful evaluation runtime in the repo. After this TO, no doc, prompt, CLI help, or test invokes `comp.framework.run`, `comp-learns-run.sh`, or reads `results.tsv` as a source of truth.

    Choose one of two paths per surface:
    - **DELETE** (preferred) — remove the file; update imports; remove tests
    - **QUARANTINE** — move to `comp/_legacy/` with a `DEPRECATED_DO_NOT_USE.md` at the root of that dir and a `DeprecationWarning` raised on import of any module inside

    DELETE is the goal. QUARANTINE is the fallback for any surface that an out-of-tree consumer still references — if any exists, call that out in the closeout rather than silently keeping legacy code at the live path.
  </objective>

  <scope>
    <files>
      <file action="inventory">(scan) any file under comp/ or docs/ that references `comp-learns-run.sh`, `comp.framework.run`, `results.tsv`, or `COMP_LEARNS_OPERATIONAL_MANDATE`</file>
      <file action="delete_or_quarantine">comp/bin/comp-learns-run.sh</file>
      <file action="delete_or_quarantine">comp/framework/run.py</file>
      <file action="delete_or_quarantine">comp/framework/results_schema.py (iff not read by live non-legacy code)</file>
      <file action="delete_or_quarantine">comp/framework/plateau.py (legacy TSV-plateau — ratchet-native plateau is in .023)</file>
      <file action="delete_or_quarantine">any results.tsv files under comp/targets/*/</file>
      <file action="modify">comp/bin/comp-learns-status (keep if needed, or merge into `comp-learns-ratchet --status`)</file>
      <file action="modify">comp/README.md + comp/OPERATING.md (remove any reference to legacy loop; point at comp-learns-ratchet)</file>
      <file action="modify">docs/architecture/COMP_LEARNS_OPERATIONAL_MANDATE.md (prepend HISTORICAL header — "superseded by COMP_LEARNS_RUNTIME_V1.md, retained for historical reference only"; no functional edits)</file>
      <file action="modify">docs/architecture/COMP_LEARNS_LOOP_ORCHESTRATOR.md (same HISTORICAL header)</file>
      <file action="create">comp/_legacy/DEPRECATED_DO_NOT_USE.md (iff any QUARANTINE path is taken)</file>
      <file action="create">org/tier2_senior/1.4.0_DS_CompLearns/deliverables/COMP_LEARNS.028_decommission_report.md</file>
    </files>
  </scope>

  <wire_contract>
    **Phase 0 — Inventory (do first, before any deletion)**:
    Run and commit output to the decommission report:
    ```
    grep -rn "comp-learns-run\.sh\|comp\.framework\.run\|from comp\.framework import run\|results\.tsv\|COMP_LEARNS_OPERATIONAL_MANDATE" \
      comp/ docs/ org/ --exclude-dir=_legacy --exclude-dir=logs
    ```
    The decommission report lists every hit with: file, line, what the reference is, and disposition (delete / quarantine / leave-as-historical-note).

    **Phase 1 — Delete preferred path**:
    For each surface in Scope:
    - If no live non-legacy code imports it → DELETE
    - If a live non-legacy surface imports it → investigate whether the import is actually exercised. If not exercised in any test or runtime path, remove the import first, then DELETE.
    - Only fall back to QUARANTINE if removal would break a live, authoritative consumer.

    **Phase 2 — Quarantine fallback (only if needed)**:
    - Move file to `comp/_legacy/<original-path-from-comp>`. Example: `comp/framework/run.py` → `comp/_legacy/framework/run.py`.
    - At the top of each quarantined `.py`:
      ```python
      import warnings
      warnings.warn(
          f"{__name__} is DEPRECATED — superseded by comp.loop.runner (comp-learns-ratchet). "
          "Retained in comp/_legacy/ for historical reference only. Scheduled for hard removal.",
          DeprecationWarning,
          stacklevel=2,
      )
      ```
    - `comp/_legacy/DEPRECATED_DO_NOT_USE.md` at the legacy dir root explains the quarantine + names the replacement surfaces + records the PRD + TO.

    **Phase 3 — Doc migration**:
    - `comp/README.md` + `comp/OPERATING.md`: replace every `comp-learns-run.sh` reference with `comp-learns-ratchet`. Update example invocations. Remove any "use bash driver for X" guidance.
    - `docs/architecture/COMP_LEARNS_OPERATIONAL_MANDATE.md` + `COMP_LEARNS_LOOP_ORCHESTRATOR.md`: prepend a one-block HISTORICAL header:
      ```markdown
      > **HISTORICAL — retained for reference only.** This document describes the v0 bash-driver loop.
      > Superseded by `docs/architecture/COMP_LEARNS_RUNTIME_V1.md` + `comp-learns-ratchet`.
      > No active work should follow the mechanics below.
      ```
      Do not edit body content — the history stays intact.
    - Scan all `org/tier2_senior/1.*_DS_CompLearns/prompt.md` + `org/tier1_exec/1.1.0_SA_CTO/prompt.md` + `2.1.0_SA_COO/prompt.md` for `comp-learns-run` references and replace with `comp-learns-ratchet`.

    **Phase 4 — Verification**:
    Re-run the inventory grep after Phases 1–3. Expected output: zero hits outside of `comp/_legacy/`, `org/*/logs/` (historical session logs — LEAVE AS-IS), and the two doc files with HISTORICAL headers. Any other hit is a miss — go back and fix.

    **Phase 5 — `comp-learns-status` disposition**:
    Two options:
    1. **Merge into runner**: delete `comp/bin/comp-learns-status`; `comp-learns-ratchet <target> --status` is the only surface.
    2. **Alias**: turn `comp-learns-status` into a 3-line shell script that execs `comp-learns-ratchet <target> --status "$@"`.
    Prefer option 1. Document choice in the decommission report.

    **Phase 6 — Success bar confirmation**:
    Verify each checkbox in PRD §14 and mark the RUNTIME_V1.md doc "realized" (edit the Status line at the top). This is the final commit of Phase 4.
  </wire_contract>

  <acceptance_criteria>
    1. **Inventory committed**: decommission report contains the full pre-deletion grep output with disposition per hit.
    2. **Zero live references post-deletion**: re-running the inventory grep returns no results under `comp/` (excluding `comp/_legacy/`) and no results under `docs/architecture/COMP_LEARNS_*.md` except the HISTORICAL-headered files and `RUNTIME_V1.md` itself (which references the legacy surfaces in context, that's fine).
    3. **No active-path imports of legacy code**: `grep -rn "from comp.framework import\|import comp.framework\|from comp._legacy" comp/ --exclude-dir=_legacy` returns no hits in live (non-test, non-legacy) modules. Tests that exercise the legacy-to-runner migration path are allowed but must be marked `@pytest.mark.legacy`.
    4. **Quarantined modules warn**: if any QUARANTINE path is used, importing any module under `comp/_legacy/` raises `DeprecationWarning`. Test: `python -W error::DeprecationWarning -c "import comp._legacy.framework.run"` fails with DeprecationWarning (proving the warning fires).
    5. **Docs migrated**: `comp/README.md` + `comp/OPERATING.md` contain no references to `comp-learns-run.sh`. Every example uses `comp-learns-ratchet`.
    6. **HISTORICAL headers in place**: `COMP_LEARNS_OPERATIONAL_MANDATE.md` + `COMP_LEARNS_LOOP_ORCHESTRATOR.md` both open with the HISTORICAL block. Body content unchanged.
    7. **Prompt files updated**: `grep -rn "comp-learns-run" org/tier2_senior/1.*_DS_CompLearns/prompt.md org/tier1_exec/*/prompt.md` returns no hits.
    8. **status surface consolidated**: exactly one of {`comp-learns-ratchet --status`, `comp-learns-status` shell alias} is the documented path. If both exist, alias points at runner.
    9. **No results.tsv files**: `find comp/targets -name "results.tsv"` returns empty.
    10. **Test suite green**: `pytest comp/ -q` passes. Any test that previously depended on the legacy loop is either deleted (if redundant with ratchet tests) or ported to use the runner.
    11. **RUNTIME_V1.md marked realized**: the top-line Status changes from "Active" to "Realized (Phase 4 complete)". Date added.
    12. **COMP_LEARNS.json updated**: project `phase` field updated to `"v1 realized"` with closeout timestamp. `prds[]` entry for `RUNTIME_V1.md` gets a `closed_at` line.
    13. **Pre-commit gate**: `.tools/ds-commit-gate.sh` passes on any `.py` edits.
  </acceptance_criteria>

  <dependencies>
    - **Hard blocked by .027** — do not decommission legacy surfaces until real-judge proving has succeeded on the new runner. If .027 fails or raises issues with the runner, Phase 4 is postponed.
  </dependencies>

  <operational_notes>
    - This is a destructive TO. Before any deletion: (a) create an annotated git tag `comp-learns-v0-final` at the pre-deletion commit, so the v0 state is recoverable; (b) `git rm` rather than `rm` so the change is tracked.
    - Historical session logs under `org/*/logs/` containing `comp-learns-run.sh` references stay as-is. They are history, not active guidance.
    - If the inventory reveals an unexpected live consumer of the legacy surface (outside comp/), escalate to 1.1.0_SA_CTO before deleting. Do NOT silently quarantine to work around an unknown dependency.
    - Removing `comp.framework.run` may cascade to unused helpers in `comp/framework/`. Deleting those is in scope — aim to leave `comp/framework/` empty or containing only files that survive as Layer-A-adjacent utilities (e.g. `branch_guard.py` if still relevant).
  </operational_notes>

  <closeout>
    - single merge commit (or tight series of commits) with `--author="1.4.0_DS_CompLearns <1.4.0_DS_CompLearns@opal.agent>"`
    - annotated git tag `comp-learns-v0-final` before the first deletion
    - annotated git tag `comp-learns-v1-realized` on the commit that edits RUNTIME_V1.md status to "Realized"
    - push with `--follow-tags`
    - MCP COMPLETE to 1.1.0_SA_CTO + 2.1.0_SA_COO with: list of deleted files, list of quarantined files (ideally empty), grep-verified inventory of remaining references, two tag shas
    - flip TO status to `complete`
    - COMP_LEARNS.json `status` → `"v1 realized"` with closeout timestamp
  </closeout>
</task_order>
