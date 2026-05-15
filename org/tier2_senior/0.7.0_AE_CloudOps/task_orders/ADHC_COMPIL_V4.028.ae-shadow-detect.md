<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.028</id>
    <slug>ae-shadow-detect</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-14</date>
    <status>done</status>
    <dispatch_held>false</dispatch_held>
    <completed>2026-05-14</completed>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P1 — Wave 1 highest empirical leverage; named-pattern detection for bug-shadows cascade class</priority>
    <sla>~2-3 days wall per PRD §15.4 sizing (higher because pattern-detection requires AST + git-log integration)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-028 + §15.1 anchor table</ref>
    <ref type="anchor_commits">3 sequential INF_D_00c fixes 2026-05-14: dtype `fd11a33c2` → NaN `de2286d67` → suffix-collision `11ca5f36f` (compounded bug-shadows pattern in same function)</ref>
    <ref type="memory">`memory/feedback_bug_shadows.md` C.2 framing — fix #1 unmasks fix #2 unmasks fix #3 in cascade</ref>
    <ref type="cross_link">Wave 1 sibling .027 postmerge-cols (same anchor incident; different detection layer — .027 catches per-merge collision; .028 detects cascade pattern across multiple sequential fixes).</ref>
  </references>

  <context>
    Bug-shadows pattern (per memory `feedback_bug_shadows.md` C.2): fix #1 resolves visible failure; new failure surfaces in same function next run; fix #2 resolves it; fix #3 cascade. Each fix is independently correct but the cascade burns wall time + compounds diagnostic effort.

    Today's empirical: INF_D_00c `_aggregate_gro_per_advisor_window` had **3 sequential fixes** within 1h45m (dtype `fd11a33c2` → NaN `de2286d67` → suffix-collision `11ca5f36f`). Each cleared the visible symptom + unmasked the next bug downstream. Compiler can detect the shape: fix site is downstream of a recently-failed assertion in same function; pre-fix-#1 the chain breaks at #1; post-fix-#1 it breaks at #2; etc.

    `comp-pipescript shadow-detect <function-name>` enumerates the "post-condition lock-in chain" of subsequent ops that depend on an assertion (`dropna(subset=...)` / `astype()` / `merge()` etc.). Flags sites where a single line's correctness gates subsequent ops. With `--recent-failures 7d`, cross-references recent commits touching the named function; identifies if subsequent fixes hit deeper sites.
  </context>

  <objective>
    Land `comp-pipescript shadow-detect <function>` subcommand. Two modes:
    - Static: enumerate the post-condition lock-in chain in a named function (no git history needed).
    - History-cross-referenced (`--recent-failures 7d`): cross-reference recent commits touching the function; detect cascade pattern.

    Output suitable for CTO post-mortem corpus banking (named pattern + commit citations).
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/comp-pipescript (add `shadow-detect` subcommand)</file>
      <file action="create">org/modules/graph/shadow-detect/{script_id}.{function}.yaml (new per-function lock-in chain manifest)</file>
      <file action="readonly_reference">data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py (anchor)</file>
      <file action="readonly_reference">memory/feedback_bug_shadows.md (corpus pattern documentation)</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>git log --all --oneline --since="2 days ago" --grep="INF_D_00c\|advisor_key\|household_id" | head -10</run>
      <expect>3 cumulative fixes enumerated: fd11a33c2 + de2286d67 + 11ca5f36f.</expect>
      <if_mismatch>If commits not present, anchor corpus needs alternate source.</if_mismatch>
    </step>
    <step>
      <run>grep -n "dropna\|astype\|merge\|\.fillna\|\.subset" data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py | head -20</run>
      <expect>~10-20 assertion-class call sites enumerated; this IS the lock-in chain surface.</expect>
      <if_mismatch>If 0 hits, function may have been refactored; check current state.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>comp-pipescript shadow-detect _aggregate_gro_per_advisor_window</run>
      <expect>Static output: enumerated lock-in chain through `dropna(subset=['advisor_key'])` + merge() + astype() ops; ≥3 chain links.</expect>
      <if_mismatch>STOP. Static mode must detect anchor pattern before shipping.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript shadow-detect _aggregate_gro_per_advisor_window --recent-failures 7d</run>
      <expect>Cross-referenced commit list: fd11a33c2 + de2286d67 + 11ca5f36f present; cascade pattern flagged with depth indicator (1st, 2nd, 3rd fix).</expect>
      <if_mismatch>--recent-failures cross-reference not landing; fix git-log integration before ship.</if_mismatch>
    </step>
    <step>
      <run>cat org/modules/graph/shadow-detect/INF_D_00c._aggregate_gro_per_advisor_window.yaml</run>
      <expect>Manifest persists; structured for post-mortem corpus banking (named pattern + chain links + commit citations).</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>comp-pipescript shadow-detect _aggregate_gro_per_advisor_window --recent-failures 7d at PRE-`fd11a33c2` checkout</run>
      <expect>Tool flags the lock-in chain BEFORE fix #1 lands. (would have surfaced "fix site downstream of dropna subset; check column-existence post-merge")</expect>
      <if_mismatch>Pattern detection missed anchor; iterate.</if_mismatch>
    </step>
    <step>
      <run>Run on ≥2 other functions with sequential-fix patterns (CTO post-mortem corpus or git log mining)</run>
      <expect>Tool surfaces lock-in chains across other functions; no false-positive crashes.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Static mode `shadow-detect _aggregate_gro_per_advisor_window` returns the lock-in chain in <5s.
    AC2: `--recent-failures 7d` cross-references the 3 INF_D_00c commits + flags cascade pattern.
    AC3: Retroactive validation at `fd11a33c2` checkout detects the chain that 11ca5f36f's fix lives in.
    AC4: Output suitable for CTO post-mortem corpus banking (structured yaml with pattern name + chain + citations).
    AC5: Tested on ≥2 other functions; no crashes.
    AC6: Session log + MCP RAVC2 to COO with empirical-anchor retroactive evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: git log enumeration + grep assertion sites
    Phase 2: shadow-detect static + --recent-failures + manifest persist
    Phase 3: retroactive validation on `fd11a33c2` checkout + ≥2 other function tests
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: extended graph (`.020`); git-log read access (universal).

    PARALLEL-OK: .027 postmerge-cols (Wave 1 sibling).

    COORDINATES WITH: future `.031 comp-adapter-audit` shares AST+git integration setup.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Compiler-tool development; no script / S3 / Lambda touch.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `comp-pipescript shadow-detect` subcommand (static + history modes)
    2. `org/modules/graph/shadow-detect/` manifest directory + ≥3 per-function yaml files
    3. Retroactive-validation evidence at `fd11a33c2` checkout
    4. Session log + RAVC2 MCP
  </deliverables>

  <ravc>AE 0.7 RAVC2 to COO on AC1-6 PASS.</ravc>

  <notes>
    **AC3 is load-bearing:** if the tool can't detect the bug-shadows chain in retrospect on a known-cascade corpus, it doesn't deliver value.

    **CTO post-mortem corpus banking** — your manifest output (named pattern + commit citations) should be directly absorbable into the upcoming SHARED.006 post-mortem doc + future corpus-quality references. Banking by-design.

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.
  </notes>
</task_order>
