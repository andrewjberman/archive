<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-04-15-comp-pipescript-deployed-silver</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to><!-- Redirected from CTO to AE CloudOps 2026-04-15 per CTO MCP 16:35 UTC. CTO authored historical commits but tooling maintenance lane is owned by AE CloudOps per MEMORY.md; CTO in oversight mode this session. Subprocess env-isolation gap folded into scope as optional. -->
    <date>2026-04-15</date>
    <status>complete</status>
    <project_code>ad-hoc</project_code>
    <priority>Unblocks WP-11 Phase 2 audit — should land ≤ 1 hour</priority>
  </metadata>

  <references>
    <ref type="trigger">MCP 0.4.0_DS_ClientPlatform~D 20260415T162911Z — reported `comp-pipescript deployed` scans gold/ only, misses silver-layer enforcer scripts</ref>
    <ref type="cto_direction">MCP 1.0.0_SA_CTO 20260415T163052Z — comp-tools enhancement, NOT silver-TO addendum; unblocks WP-11 structural auditability</ref>
    <ref type="blocked_TO">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/BDPL_CNPRCS.WP-11.ds-scoped-price-overrides.md (Phase 2 step on `comp-pipescript deployed` currently unauditable for silver-layer scripts)</ref>
  </references>

  <objective>
    Extend `comp-pipescript deployed` (implemented in `org/modules/graph/pipeline_cli.py`) to scan
    `s3://opal-data-bd/code/silver/` in addition to `code/gold/`. Silver-layer daily-enforcer scripts
    (`bd_price_update.py`, `inject_scoped_overrides.py`, etc.) that gate canonical prices currently
    return "Unknown script" or are silently skipped — making MATCH/STALE/MISSING signals misleading
    for silver-dependent work packages.

    Output labels results by layer:
      `[GOLD] D_04.client_portal_summary.py: MATCH`
      `[SILVER] bd_price_update.py: STALE`
      `[SILVER] inject_scoped_overrides.py: MATCH`

    Update `org/modules/graph/comp-tools.yaml` doc entry for `comp-pipescript deployed` to reflect
    expanded scope. Note: silver-layer boundary is ambiguous (some scripts in `scripts/silver/`
    deploy to `code/silver/`; the tool must either read a manifest of known silver scripts OR
    fall back to a directory-level scan).

    **Optional scope (fold in if convenient, surfaced by CTO 2026-04-15):** subprocess env isolation —
    tool spawns `aws` by bare name; subprocess loses PATH; "aws CLI not found" on some shells.
    Candidate fix: resolve `aws` via `shutil.which` at call site OR pass full env to subprocess.
    Small lift, same script.
  </objective>

  <wire_contract>
    No new output format — same MATCH/STALE/MISSING enum. Only addition: `[GOLD]` vs `[SILVER]`
    prefix so agents can distinguish layers. Existing gold-only invocations continue to return
    correct labels with `[GOLD]` prefix (non-breaking additive change).
  </wire_contract>

  <acceptance_criteria>
    1. `comp-pipescript deployed bd_price_update.py` returns meaningful MATCH/STALE/MISSING with `[SILVER]` label (currently: "Unknown script" or silent skip).
    2. `comp-pipescript deployed inject_scoped_overrides.py` — same.
    3. Existing `comp-pipescript deployed D_04` continues to return correct MATCH/STALE/MISSING with `[GOLD]` prefix (regression).
    4. `org/modules/graph/comp-tools.yaml` updated: `deployed` subcommand notes expanded scope.
    5. `org/compiler-tools-log.md` gains one entry documenting the enhancement trigger + result.
    6. Session log Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    7. MCP COMPLETE to COO with commit hash + regression evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>git blame .tools/comp-pipescript | head -5</run>
        <expect>Last author identified (current blame: CTO for pipeline_cli.py). Confirm editing the right file.</expect>
        <if_mismatch>STOP. Verify file path and delegation target.</if_mismatch>
      </step>
      <step>
        <run>grep -n "code/gold" org/modules/graph/pipeline_cli.py</run>
        <expect>Find S3 prefix usage; confirm only gold/ is scanned in the `deployed` path.</expect>
        <if_mismatch>If silver/ already present in scan scope, this TO is moot — close with a note.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>comp-pipescript deployed bd_price_update.py</run>
        <expect>Returns MATCH/STALE/MISSING with `[SILVER]` label — not "Unknown script" and not silent skip.</expect>
        <if_mismatch>STOP. Fix the layer-detection / silver-manifest logic before commit.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed D_04</run>
        <expect>Returns MATCH/STALE/MISSING with `[GOLD]` label (regression — existing behavior preserved).</expect>
        <if_mismatch>STOP. Gold-layer detection broke; revert approach.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed inject_scoped_overrides.py</run>
        <expect>Meaningful `[SILVER]` status on the second WP-11 target.</expect>
        <if_mismatch>Surface to COO + DS ~D; may indicate silver script not yet uploaded.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. Standalone tooling fix.
  </dependencies>

  <next>
    On commit: COO logs the enhancement to `org/compiler-tools-log.md`. DS ~D re-runs WP-11 Phase 2
    `comp-pipescript deployed` steps to close the audit trail retroactively.
  </next>
</task_order>
