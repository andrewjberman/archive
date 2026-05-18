<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.029a</id>
    <slug>dsc-safe-json-serialize</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <coordinates_with>0.7.0_AE_CloudOps (downstream .029b comp-validate gold-nan)</coordinates_with>
    <date>2026-05-14</date>
    <status>done</status>
    <!-- GT correction 2026-05-18 (2.0.0_SA_COO): status was stale at `staged`. Work shipped by DS~C in commit e0f51a147 — data/orion/scripts/gold/lib/safe_json_serialize.py (117 lines) + test_safe_json_serialize.py (189 lines) + INF_D_00c + INF_D_04 reference migrations. .029b (which gates on this per PRD §15.5) correctly showed `done`; .029a was shipped-ahead-of-status, not skipped. This was COMPIL_V4's sole open closure gate per CTO §16 retrospective. -->
    <dispatch_held>false</dispatch_held>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P1 — Wave 2 cross-pod hygiene; .029b AE 0.7 follow-on gates on this</priority>
    <sla>~4-6 hours wall per PRD §15.4 sizing (4 modules: shared util + 1-2 reference migrations + tests)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-029 Part A</ref>
    <ref type="anchor_commit">DS~C `de2286d67` 2026-05-14 — `_strip_nan` + `allow_nan=False` discipline at `_write_json_s3` boundary in INF_D_00c.portal_leaderboard.py</ref>
    <ref type="cross_link">Downstream: `.029b ae-gold-nan-audit` (AE 0.7) gates on this util being canonical at `data/orion/scripts/gold/lib/safe_json_serialize.py`. INFFIN.014 (`a731e8461` DS~C 2026-05-14) reuses the same pattern empirically.</ref>
    <ref type="memory">DS~C banking-worthy: cross-script audit candidate already noted in DS~C session log</ref>
  </references>

  <context>
    Multiple gold scripts emit JSON via `_write_json_s3()`-class helpers. `pd.mean()/.median()` on filtered Series can return NaN → `json.dumps(...)` emits literal `NaN` token (which is NOT valid JSON) → portal JSON.parse fail → cascading UI errors.

    DS~C empirically discovered + fixed this in INF_D_00c via `_strip_nan(obj)` recursive helper + `allow_nan=False` tripwire at write boundary (`de2286d67`). Pattern is liftable: every gold-script JSON-write boundary benefits from the same defense-in-depth.

    **Two-part TO** (this is Part A — DS authoring):
    - Part A: lift `_strip_nan()` + `allow_nan=False` discipline to `data/orion/scripts/gold/lib/safe_json_serialize.py`. Single import + single call swap pattern for migration. Reference migration on 1-2 existing scripts (INF_D_00c original + INFFIN.014 INF_D_04 already use the pattern inline — opportunistic refactor to consume shared util).
    - Part B (`.029b`, AE 0.7): cross-script audit `comp-validate gold-nan` enumerates every gold-script JSON-emit boundary; flags compliance per file.
  </context>

  <objective>
    Land `data/orion/scripts/gold/lib/safe_json_serialize.py` shared util with:
    - `safe_json_dumps(obj, **kwargs)` — wraps `json.dumps` with auto `_strip_nan` + `allow_nan=False` defense-in-depth
    - `strip_nan(obj)` — recursive NaN/Inf/-Inf stripper (handles dict/list/tuple)
    - Type hints + JSDoc + tests
    - Opportunistic migration on 1-2 existing call sites (INF_D_00c + INFFIN.014's INF_D_04 are candidates; migration is single-LOC import + replace).

    No forced backfill across all ~15-20 gold-script JSON-emit sites. Migration is opportunistic per-script during normal maintenance.
  </objective>

  <scope>
    <files>
      <file action="create">data/orion/scripts/gold/lib/safe_json_serialize.py</file>
      <file action="create">data/orion/scripts/gold/lib/tests/test_safe_json_serialize.py</file>
      <file action="modify">data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py (reference migration: replace inline `_strip_nan` with shared import)</file>
      <file action="modify">data/orion/scripts/gold/INF_D_04.client_portal_summary.py (reference migration if it has inline NaN handling per INFFIN.014 context)</file>
      <file action="readonly_reference">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-029</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>grep -rn "_strip_nan\|allow_nan=False" data/orion/scripts/gold/ | head -20</run>
      <expect>≥2 inline implementations enumerated (INF_D_00c.portal_leaderboard.py from de2286d67 + possible INFFIN.014 sites in INF_D_04).</expect>
      <if_mismatch>If 0 hits, base implementation hasn't been committed; verify de2286d67 is on origin.</if_mismatch>
    </step>
    <step>
      <run>grep -rn "json.dumps\|json\.dump" data/orion/scripts/gold/ | head -30</run>
      <expect>~15-20 candidate JSON-emit sites enumerated (anchor for migration scope + .029b audit baseline).</expect>
      <if_mismatch>If significantly different count, surface — informs .029b audit scope.</if_mismatch>
    </step>
    <step>
      <run>ds-commit-gate.sh on a stub safe_json_serialize.py</run>
      <expect>Three gates PASS (py_compile + ds-precommit-check.py + ruff py39).</expect>
      <if_mismatch>Fix gate failures before writing real util.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>python -m pytest data/orion/scripts/gold/lib/tests/test_safe_json_serialize.py -v</run>
      <expect>All tests PASS: leaf NaN → null; nested NaN + Inf in dicts/lists at various depths → all null; allow_nan=False raises on unstripped NaN (tripwire live).</expect>
      <if_mismatch>STOP. Fix util semantics; defense-in-depth must work both ways (strip + tripwire).</if_mismatch>
    </step>
    <step>
      <run>ds-commit-gate.sh on the new util + tests + migrated scripts</run>
      <expect>9/9 PASS (3 per file × ≥3 files).</expect>
      <if_mismatch>STOP per CLAUDE.md Rule 14.</if_mismatch>
    </step>
    <step>
      <run>aws s3 head-object spot-check on `s3://opal-data-inf/code/gold/lib/safe_json_serialize.py` post safe-deploy.sh</run>
      <expect>S3 mirror matches commit SHA via comp-pipescript deployed gate.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>grep -rn "from .lib.safe_json_serialize\|import safe_json_serialize" data/orion/scripts/gold/</run>
      <expect>≥2 reference migrations confirmed (INF_D_00c + INFFIN.014's INF_D_04 candidate).</expect>
    </step>
    <step>
      <run>Signal AE 0.7 — .029b dispatch unblock (this util at canonical path enables their audit tool)</run>
      <expect>MCP sent + AE 0.7 acknowledges receipt of canonical path.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `data/orion/scripts/gold/lib/safe_json_serialize.py` ships with `safe_json_dumps()` + `strip_nan()` exported.
    AC2: Tests cover: leaf NaN, nested NaN/Inf, negative tripwire (allow_nan=False raises), edge cases (dict/list/tuple).
    AC3: ≥2 reference migrations on existing scripts (INF_D_00c + INF_D_04 or alternates).
    AC4: ds-commit-gate.sh PASS (py_compile + ds-precommit-check.py + ruff py39 + `from __future__ import annotations` per Rule 15).
    AC5: safe-deploy.sh SHA-MATCH on S3.
    AC6: AE 0.7 .029b dispatch-unblock signal sent.
    AC7: Session log + RAVC2 MCP to COO + CC AE 0.7.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: grep existing inline implementations + json.dumps consumers + ds-commit-gate stub
    Phase 2: pytest util + ds-commit-gate 9/9 + safe-deploy SHA-MATCH
    Phase 3: migrate-site grep verify + AE 0.7 unblock signal
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: none — foundational lib + reference migrations.

    DOWNSTREAM BLOCKING: `.029b comp-validate gold-nan` (AE 0.7) gates on this util being at canonical path. Send AE 0.7 unblock signal post-RAVC2.

    PARALLEL-OK: Wave 1 .027 + .028 (AE lane, different tools).

    NO PORTAL CHANGES.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Lib code + opportunistic reference migrations. Migrated scripts retain identical runtime behavior; util wrapping is transparent. No silver/bronze re-emit; no Lambda redeploy; no chain re-fire. Future migrations (~13-18 remaining gold-script JSON-emit sites) are opportunistic per-script — no forced backfill per AC2 framing.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `safe_json_serialize.py` shared util
    2. `test_safe_json_serialize.py` test suite (≥6 tests covering happy + edge + tripwire)
    3. ≥2 reference migrations (INF_D_00c + INF_D_04 candidates)
    4. safe-deploy.sh + S3 SHA-MATCH evidence
    5. AE 0.7 .029b dispatch unblock signal
    6. Session log + RAVC2 to COO
  </deliverables>

  <ravc>
    DS~C RAVC2 to COO + CC AE 0.7 on AC1-7 PASS. COO ratifies + signals AE 0.7 .029b dispatch unblocked.
  </ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>"` per protocol.

    **Compiler context:**
    ```
    SERIAL=0.4.0_DS_ClientPlatform~C
    TO_ID=ADHC_COMPIL_V4.029a
    ```

    **Migration policy** (PRD §15.4 AC2 framing): opportunistic only. No forced backfill. Future agents migrate per-script during normal maintenance touches.
  </notes>
</task_order>
