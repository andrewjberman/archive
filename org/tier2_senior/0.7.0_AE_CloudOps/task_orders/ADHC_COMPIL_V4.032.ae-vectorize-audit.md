<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.032</id>
    <slug>ae-vectorize-audit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-14</date>
    <status>active</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED — Wave 3 RAVC2 received (890f8d2fe). Wave 4 dispatched 2026-05-15. Empirical anchor: DS~B `a4a4fd0b2` cash_drag 553s→<30s corpus signal.</dispatch_unblock_condition>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P1 — Wave 4 cross-script hygiene; pandas vectorization opportunity detection</priority>
    <sla>~1.5-2 days wall per PRD §15.4 sizing</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-032</ref>
    <ref type="anchor_commit">DS~B INF_D_06.cash_drag `a4a4fd0b2` 2026-05-14 — vectorize groupby across partitions + per-account time-weighted mean (553s → target <30s)</ref>
    <ref type="ds_corpus">DS~B detection-rules brief: AST scan + runtime telemetry parse (FutureWarning clusters) + wall-time outliers (>5× median step)</ref>
    <ref type="cross_link">Wave 4 sibling: .025 skipgate + .030 stale-marker. Compounds with ADVI_INFINC Phase 2-6 (script-internal vectorize-audit BEFORE chain-level Pattern A skip-gate per DS~B's framing).</ref>
  </references>

  <context>
    Pattern A scripts use per-partition Python loops (`for date in dates: ...`) where vectorized pandas groupby would compress 10-100x. Hard to detect manually; pre-vectorization profiles look "fine" until a single script dominates chain wall.

    DS~B today empirically vectorized INF_D_06.cash_drag: 553s wall (~9.2 min) for a step that should take <30s. Outer Python loop wrapping partition-scoped + per-account groupby-apply → single vectorized concat + groupby on full frame. 18× speedup target.

    **DS~B's banked detection rules (from session 3 RAVC):**
    1. AST scan: `.groupby(...).apply(lambda...)` invocation inside `for`/`while`/ThreadPoolExecutor.submit body → flag
    2. Runtime telemetry parse: chain-runner logs for `FutureWarning: ` mentions tied to pandas groupby; cluster by script + line number
    3. Wall-time outliers: any gold-d step > 5× median step wall flagged for vectorize-audit investigation
  </context>

  <objective>
    Land `comp-perf vectorize-audit <script>` subcommand. Detects via DS~B's 3-rule corpus. Emits candidate refactor sketch per flagged site. `--chain inf` chain-wide audit; rank by wall-time impact (cross-reference `gold_prof.py` telemetry).
  </objective>

  <scope>
    <files>
      <file action="create">.tools/comp-perf (new binary OR subcommand under .tools/comp-pipescript)</file>
      <file action="create">org/modules/graph/vectorize-audit/{script_id}.yaml (per-script vectorize candidates)</file>
      <file action="readonly_reference">data/orion/scripts/gold/INF_D_06.cash_drag.py (anchor — both pre + post-`a4a4fd0b2`)</file>
      <file action="readonly_reference">data/orion/scripts/gold/gold_prof.py (telemetry shipping per PRD)</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>git log --all --oneline --since="3 days ago" --grep="cash_drag\|vectorize" | head -5</run>
      <expect>`a4a4fd0b2` DS~B vectorization ship enumerated.</expect>
    </step>
    <step>
      <run>git show --stat a4a4fd0b2 | head -20</run>
      <expect>Pre/post diff visible for AST-pattern training.</expect>
    </step>
    <step>
      <run>aws s3 ls s3://opal-data-inf/gold/logs/ | grep -E "20260514.*\.log" | head -5</run>
      <expect>Chain-runner logs available for runtime-telemetry-parse rule.</expect>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>comp-perf vectorize-audit INF_D_06.cash_drag at PRE-`a4a4fd0b2` checkout</run>
      <expect>Flag the outer-loop groupby-apply pattern that 553s came from. Refactor sketch points at vectorized groupby alternative.</expect>
      <if_mismatch>STOP. AC1 load-bearing.</if_mismatch>
    </step>
    <step>
      <run>comp-perf vectorize-audit INF_D_06.cash_drag at POST-`a4a4fd0b2`</run>
      <expect>0 flags (the fix already applied).</expect>
    </step>
    <step>
      <run>comp-perf vectorize-audit --chain inf</run>
      <expect>Chain-wide ranking by wall-time impact × opportunity score. Top candidates surfaced for follow-up.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>Test on ≥3 other Pattern A scripts; surface vectorize opportunities</run>
      <expect>No crashes; opportunities flagged.</expect>
    </step>
    <step>
      <run>Surface top-N candidates to COO for follow-up DS routing</run>
      <expect>Output suitable for direct routing to DS lanes per ADVI_INFINC Phase 2-6 sequencing.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Detects INF_D_06.cash_drag pre-vectorize pattern from `a4a4fd0b2~1` (would have surfaced 553s opportunity before manual perf P0).
    AC2: Output ranked by `gold_prof.py` wall-time × identified opportunity score.
    AC3: `--chain inf` mode functional + cross-references runtime telemetry.
    AC4: 0 false-positives on post-`a4a4fd0b2` state.
    AC5: Tested on ≥3 other Pattern A scripts.
    AC6: Top-N candidates surfaced for follow-up routing.
    AC7: Session log + RAVC2 MCP to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: git log anchor + diff training + S3 log availability
    Phase 2: vectorize-audit at PRE checkout + POST checkout + --chain inf
    Phase 3: cross-script tests + follow-up routing
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: Wave 1+2+3 RAVC2; DS~B `a4a4fd0b2` AE chain wall-time RAVC2 (gives perf-impact baseline).

    DOWNSTREAM CONSUMERS: ADVI_INFINC Phase 2-6 PRE-flight check per DS~B's "script-internal vectorize before chain-level skip-gate" framing. Banking this as Phase-0-sub-check standard.

    NO PORTAL CHANGES.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Compiler-tool development.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `comp-perf vectorize-audit` subcommand
    2. Per-script yaml + top-N chain-wide ranking
    3. Retroactive validation on `a4a4fd0b2~1` checkout
    4. Session log + RAVC2
  </deliverables>

  <ravc>AE 0.7 RAVC2 to COO on AC1-7 PASS.</ravc>

  <notes>
    **AC1 load-bearing:** retroactive validation on `a4a4fd0b2~1` IS the value signal.

    **DS~B's Phase-0-sub-check framing**: before applying chain-level Pattern A skip-gate per ADVI_INFINC TO, run vectorize-audit on that script first. Compounding savings.

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.
  </notes>
</task_order>
