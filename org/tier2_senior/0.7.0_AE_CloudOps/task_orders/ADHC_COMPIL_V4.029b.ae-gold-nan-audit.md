<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.029b</id>
    <slug>ae-gold-nan-audit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-14</date>
    <status>done</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>.029a DS~C RAVC2 PASS — `safe_json_serialize.py` at canonical path `data/orion/scripts/gold/lib/safe_json_serialize.py` with S3-deployed SHA-MATCH</dispatch_unblock_condition>
    <completed>2026-05-14</completed>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P1 — Wave 2 follow-on to .029a; closes ADHC_GOLDNAN cross-script discipline pattern</priority>
    <sla>~1-1.5 days wall per PRD §15.4 sizing</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-029 Part B</ref>
    <ref type="upstream_dep">.029a DS~C `safe_json_serialize.py` shared util at canonical path</ref>
    <ref type="cross_link">Wave 2 sibling: .029a (DS~C lead, foundational lib). Cross-pod ADHC_GOLDNAN closure pattern.</ref>
  </references>

  <context>
    Cross-script audit tool for gold-script JSON-emit boundaries. Lists every gold script with `json.dumps` / `_write_json_s3` / similar boundary; flags compliance per file:
    - PASS: imports + uses `safe_json_serialize` shared util (post-migration state)
    - INLINE: has inline `_strip_nan` / `allow_nan=False` (pre-migration; opportunistic-refactor candidate)
    - NEITHER: no NaN handling at JSON boundary (silent-drift risk; flag for follow-up)

    Output: per-script pass/fail matrix; lift-vs-inline-fix recommendation per file.
  </context>

  <objective>
    Land `comp-validate gold-nan` subcommand. Walks `data/orion/scripts/gold/**/*.py` for JSON-emit boundaries; classifies each per the 3-state above; emits per-script + chain-wide report.
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/comp-validate (add `gold-nan` subcommand)</file>
      <file action="create">org/modules/graph/gold-nan/{script_id}.yaml (per-script compliance manifest)</file>
      <file action="create">org/modules/graph/gold-nan/REPORT.md (chain-wide rollup)</file>
      <file action="readonly_reference">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-029 Part B</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>head -object check on `s3://opal-data-inf/code/gold/lib/safe_json_serialize.py`</run>
      <expect>S3 mirror present + DS~C SHA-MATCHED per .029a RAVC2.</expect>
      <if_mismatch>.029a hasn't shipped or S3 sync failed; STOP and surface to COO.</if_mismatch>
    </step>
    <step>
      <run>grep -rn "json.dumps\|json\.dump\|_write_json_s3" data/orion/scripts/gold/ | wc -l</run>
      <expect>~15-20 JSON-emit boundary call sites (matches .029a Phase 1 baseline).</expect>
      <if_mismatch>If significant drift from .029a's count, surface — possible concurrent gold-script work.</if_mismatch>
    </step>
    <step>
      <run>comp-validate --help</run>
      <expect>Existing subcommands; no `gold-nan` entry (new subcommand per PRD §15.3).</expect>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>comp-validate gold-nan</run>
      <expect>Per-script 3-state classification: PASS / INLINE / NEITHER. INF_D_00c.portal_leaderboard.py = PASS post-.029a migration. INF_D_04.client_portal_summary.py = PASS or INLINE depending on .029a migration scope.</expect>
      <if_mismatch>STOP. Tool must correctly classify the known-state anchors before ship.</if_mismatch>
    </step>
    <step>
      <run>cat org/modules/graph/gold-nan/REPORT.md</run>
      <expect>Chain-wide rollup: total scripts, % PASS, % INLINE (opportunistic-refactor candidates), % NEITHER (silent-drift risk follow-up).</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>comp-validate gold-nan --strict</run>
      <expect>Exit 1 on any NEITHER classification; exit 0 if all scripts at PASS or INLINE.</expect>
      <if_mismatch>--strict mode incorrect; fix before declaring done.</if_mismatch>
    </step>
    <step>
      <run>Surface report to COO + CTO + DS~C</run>
      <expect>Per-script matrix + NEITHER candidates (if any) flagged for follow-up TOs.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `comp-validate gold-nan` enumerates all gold-script JSON-emit boundaries (≥15 scripts).
    AC2: 3-state classification correct on anchor scripts (INF_D_00c = PASS post-.029a; reference migration confirms).
    AC3: Per-script yaml + chain-wide REPORT.md persisted.
    AC4: `--strict` mode exits 1 on NEITHER classifications.
    AC5: Identified NEITHER-class scripts surfaced to COO for follow-up TO authoring.
    AC6: Session log + MCP RAVC2 to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: S3 head-object on .029a util + grep JSON-emit baseline + comp-validate --help
    Phase 2: comp-validate gold-nan + REPORT verify
    Phase 3: --strict mode + report surface
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: .029a SHIPPED + S3-deployed.

    POTENTIAL FOLLOW-ON: NEITHER-class scripts may need DS sub-TOs to add NaN handling (opportunistic; non-urgent).

    NO PORTAL / NO DATA-LAYER changes.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Compiler-tool development.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `comp-validate gold-nan` subcommand
    2. `org/modules/graph/gold-nan/{script_id}.yaml` per-script manifests
    3. `org/modules/graph/gold-nan/REPORT.md` chain-wide rollup
    4. Session log + RAVC2 to COO with NEITHER-class candidate routing
  </deliverables>

  <ravc>AE 0.7 RAVC2 to COO on AC1-6 PASS; COO routes any NEITHER-class follow-ups to DS lanes.</ravc>

  <notes>
    **Cross-pod choreography:** .029a (DS~C) ships first; .029b (this TO; AE 0.7) ships second. Don't pre-empt .029a's RAVC2.

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.
  </notes>
</task_order>
