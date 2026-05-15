<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.027</id>
    <slug>ae-postmerge-cols</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-14</date>
    <status>done</status>
    <dispatch_held>false</dispatch_held>
    <completed>2026-05-14</completed>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P1 — Wave 1 highest empirical leverage; retroactive validates against today's INF_D_00c bug-shadows cascade</priority>
    <sla>~1 day wall per PRD §15.4 sizing</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-027 + §15.1 anchor table</ref>
    <ref type="anchor_commit">DS~A INF_D_00c fix #2 `11ca5f36f` (advisor_key suffix-collision; bug-shadows 2nd surface 2026-05-14)</ref>
    <ref type="project_json">org/projects/ADHC_COMPIL_V4.json (extend Phase 1 scope to include v0.5 candidates)</ref>
    <ref type="authority">CTO PRD v0.5 ship `826043eb4` 2026-05-14 + Andrew kickoff approval</ref>
    <ref type="cross_link">Wave 1 sibling: .028 shadow-detect. Both retroactive-validatable against fd11a33c2/de2286d67/11ca5f36f cascade. Underlying compiler graph: ADHC_COMPIL_V4.020 extended graph (already shipped).</ref>
  </references>

  <context>
    `pd.DataFrame.merge()` produces suffix-collided columns (`_x`/`_y`) when both sides have same-name columns. Subsequent `dropna(subset=['advisor_key'])` or other column-existence-dependent ops KeyError because the post-merge frame has `advisor_key_x` / `advisor_key_y` but not bare `advisor_key`. Compiler doesn't currently model dataframe-column-existence post-merge.

    Empirical anchor: DS~A `11ca5f36f` shipped at 14:12Z 2026-05-14 — 8-line fix dropping `iw.advisor_key` pre-merge so `account_team.advisor_key` survives bare. This was bug-shadows surface #2 in the same function (`_aggregate_gro_per_advisor_window`) after `fd11a33c2` dtype fix. Pre-commit `comp-pipescript postmerge-cols INF_D_00c` would have flagged the merge call site as "post-merge column `advisor_key` ambiguous; expect `_x`/`_y` suffix".
  </context>

  <objective>
    Land `comp-pipescript postmerge-cols <script>` subcommand. For every `merge()` call site in the script, output expected post-merge column set vs. accessed columns. Flag mismatches (suffix-collision risks + KeyError risks). Optional `--strict` mode errors on any unverified post-merge column access. Per-script manifest persists under `org/modules/graph/postmerge-cols/{script_id}.yaml` for cross-tool consumption.
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/comp-pipescript (add `postmerge-cols` subcommand)</file>
      <file action="create">org/modules/graph/postmerge-cols/ (new manifest directory)</file>
      <file action="readonly_reference">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-027</file>
      <file action="readonly_reference">data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py (anchor empirical)</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript --help | head -30</run>
      <expect>Existing subcommands listed; no `postmerge-cols` entry — confirms NEW subcommand (per PRD §15.3).</expect>
      <if_mismatch>If `postmerge-cols` already exists, surface to COO — likely concurrent author.</if_mismatch>
    </step>
    <step>
      <run>grep -n "merge(" data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py | head -10</run>
      <expect>~3-5 merge() call sites enumerated for retroactive validation baseline.</expect>
      <if_mismatch>If 0 matches, anchor commit may have been reverted; verify git log + 11ca5f36f present.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io INF_D_00c</run>
      <expect>READS includes account_team + client_perf (both have `advisor_key` per the bug-shadows root cause).</expect>
      <if_mismatch>If column overlap not in io output, comp-pipescript io needs upstream extension first.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>comp-pipescript postmerge-cols INF_D_00c</run>
      <expect>Per-merge-site table with left-cols + right-cols + suffix-collision-flag + downstream-access-list. ≥1 collision flagged for `_aggregate_gro_per_advisor_window` (the anchor).</expect>
      <if_mismatch>STOP. Tool must detect the empirical anchor before shipping.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript postmerge-cols INF_D_00c --strict</run>
      <expect>Exit 1 on uncovered access; output points at specific line numbers.</expect>
      <if_mismatch>--strict mode behavior incorrect; fix before ship.</if_mismatch>
    </step>
    <step>
      <run>cat org/modules/graph/postmerge-cols/INF_D_00c.yaml</run>
      <expect>Generated manifest exists; lists call sites + post-merge column manifest.</expect>
      <if_mismatch>Manifest persistence missing; required per AC2.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>Retroactive validation: comp-pipescript postmerge-cols INF_D_00c at PRE-`11ca5f36f` checkout (commit `fd11a33c2`)</run>
      <expect>Tool flags the bug that 11ca5f36f fixed. This IS the corpus signal.</expect>
      <if_mismatch>Tool missed the empirical anchor; iterate detection logic.</if_mismatch>
    </step>
    <step>
      <run>comp-blast comp-pipescript</run>
      <expect>No new consumers appeared during write.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `comp-pipescript postmerge-cols INF_D_00c` detects `advisor_key` suffix-collision in `_aggregate_gro_per_advisor_window` pre-`11ca5f36f` (retroactive validation of empirical anchor).
    AC2: Per-script post-merge column manifest persists under `org/modules/graph/postmerge-cols/{script_id}.yaml`.
    AC3: `--strict` mode exits 1 on uncovered post-merge column access.
    AC4: Tool runs on ≥3 other gold scripts (INF_B_00, INF_C_00, INF_C_01) without crash; baseline manifest emitted for each.
    AC5: Session log Compiler Tools section reproduces Phase 1/2/3 runs with observed result vs expect.
    AC6: MCP RAVC2 to COO with empirical-anchor retroactive-validation evidence (Phase 3 step 1 output).
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript --help` baseline + `grep merge(` + `comp-pipescript io INF_D_00c`
    Phase 2: `comp-pipescript postmerge-cols INF_D_00c` (new) + `--strict` mode + manifest emit verify
    Phase 3: retroactive validation against `fd11a33c2` checkout + `comp-blast comp-pipescript` post-commit
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: ADHC_COMPIL_V4 Phase 1 extended graph (`.020`) — already shipped.

    PARALLEL-OK: Wave 1 sibling .028 shadow-detect (same anchor incident; different detection layer).

    COORDINATES WITH: future v0.5 tools (.026 comp-types index, .031 comp-adapter-audit) share TS/Python AST machinery; setup learnings can transfer.

    NO PORTAL / NO DATA-LAYER changes.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Compiler-tool development. No script changes; no S3 emits; no Lambda redeploys.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `comp-pipescript postmerge-cols` subcommand
    2. `org/modules/graph/postmerge-cols/` manifest directory + per-script yaml files (≥4: INF_D_00c, INF_B_00, INF_C_00, INF_C_01)
    3. Retroactive-validation evidence on `fd11a33c2` checkout
    4. Session log + RAVC2 MCP to COO
  </deliverables>

  <ravc>
    AE 0.7 RAVC2 to COO on AC1-6 PASS. COO ratifies + signals Wave 1 sibling .028 dispatch unblocked (parallel) + Wave 2/3/4 in sequence.
  </ravc>

  <notes>
    **Empirical anchor priority:** the retroactive validation against `fd11a33c2` IS the corpus signal. If the tool can't detect a known-bug-fixed-yesterday-in-this-exact-pattern, it doesn't deliver value. AC1 is load-bearing.

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.

    **Compiler context:**
    ```
    SERIAL=0.7.0_AE_CloudOps
    TO_ID=ADHC_COMPIL_V4.027
    ```
  </notes>
</task_order>
