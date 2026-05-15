<task_order>
  <metadata>
    <id>ADVI_INFFIN.021</id>
    <slug>dsd-top-gain-positions-shape-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-14</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>IMMEDIATE — DS~D bench-clear post NMCOHT cohort bucketing fix. Andrew direct "push them along" override.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — "Top Gain Positions" structurally broken (sort criterion N/A)</priority>
    <sla>~1-2h wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.2 (CTO `23fdaac67`)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~23:0XZ image #3: "the aggregations with all n/as the alleged top positions, i think the shape is not set up for that"</ref>
    <ref type="surface">Inflection portal → AdvisorIntelligence → Books tab → Top Gain Positions table</ref>
  </references>

  <context>
    Top Gain Positions table displays Ticker + Market Value populated, but Cost Basis = N/A and Unrealized Gain = N/A for all rows (VOO, IEFA, JIJIX, FDRXX, CIVIX, SPYM, BIV, PFDE, PFOE, VO). Sort by "Top GAIN" structurally broken since gain N/A.

    Two-path resolution:
    1. Populate cost basis + unrealized gain at security grain (requires per-lot cost basis rollup to security grain)
    2. Relabel to "Top Market Value Positions" if cost-basis rollup infeasible at security grain

    Per CLAUDE.md Rule 13+14+15: DS owns the full commit→QA-deploy cycle.
  </context>

  <objective>
    Either populate cost basis + unrealized gain at security grain for Top Gain Positions (path 1) OR coordinate FE relabel to "Top Market Value Positions" + verify sort criterion matches (path 2). Decision per empirical feasibility check Phase 1.
  </objective>

  <scope>
    <files>
      <file action="readonly_reference">data/orion/scripts/gold/{top positions emitter} — current emit shape</file>
      <file action="modify_conditional">data/orion/scripts/gold/{top positions emitter} — IF path 1 feasible, augment emit with security-grain cost basis rollup</file>
      <file action="readonly_reference">portal FE TopGainPositions component — current consumer</file>
    </files>
  </scope>

  <phase id="1" when="feasibility">
    <step>
      <run>comp-pipescript io {top positions gold script} — surface current emit + FE consumer</run>
      <expect>Emit shape: tickers + market_value populated; cost_basis/unrealized_gain absent at security grain.</expect>
    </step>
    <step>
      <run>S3 inspect source lot-level data: aws s3 ls + sample read — verify per-lot cost basis available; check if rollup to security grain is feasible (lot dedupe + sum)</run>
      <expect>Feasibility decision: Path 1 (security-grain rollup feasible) OR Path 2 (infeasible at security grain → FE relabel cascade).</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>PATH 1 (if Phase 1 feasibility=YES): augment top positions gold script to emit security-grain cost_basis (sum lot-level cost basis dedupe per ticker) + unrealized_gain (market_value - cost_basis); preserve existing market_value emit</run>
      <expect>Gold script ~30-50 LOC delta; security-grain rollup emitted; sentinel _meta extended.</expect>
    </step>
    <step>
      <run>PATH 2 (if Phase 1 feasibility=NO): author dispatch note → COO for FE-relabel cascade TO INFFIN.021b (RD 0.4.2 lane); current TO closes Phase 1 only</run>
      <expect>Cascade routing clean; no orphan DS lane work.</expect>
    </step>
    <step>
      <run>PATH 1 continued: ds-commit-gate.sh: py_compile + ds-precommit-check.py + ruff py39 0.15.11</run>
      <expect>All 3 PASS.</expect>
    </step>
    <step>
      <run>PATH 1 continued: local dry-run + safe-deploy.sh + S3 upload + comp-pipescript deployed MATCH</run>
      <expect>SHA-MATCH; deploy clean.</expect>
    </step>
  </phase>

  <phase id="3" when="verify + close">
    <step>
      <run>PATH 1: SSM dispatch re-run; verify Top Gain Positions table now shows populated cost_basis + unrealized_gain per row</run>
      <expect>Top 10 rows populated; sort by unrealized_gain DESC matches "Top GAIN" semantic.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + DT 0.4 (PROD promote candidate); state which path executed</run>
      <expect>Evidence-bearing close + path attestation.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Phase 1 feasibility decision documented (Path 1 vs Path 2)
    AC2 (Path 1): Cost basis + unrealized gain populated at security grain in Top Gain Positions table
    AC2 (Path 2): Cascade TO authored for RD 0.4.2 lane (FE relabel "Top Market Value Positions")
    AC3 (Path 1): Sort criterion matches label semantically (Top GAIN = sort by unrealized_gain DESC)
    AC4 (Path 1): ds-commit-gate.sh PASS
    AC5 (Path 1): safe-deploy.sh PASS + S3 upload + comp-pipescript deployed MATCH
    AC6 (Path 1): SSM re-run + empirical verification post-deploy
    AC7: 49F regression smoke PASS (same component shared)
    AC8: No emoji per CLAUDE.md
    AC9: RAVC2 to COO + CC CTO + DT 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 comp-pipescript io; Phase 2 ds-commit-gate + safe-deploy; Phase 3 SSM dispatch.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: None.
    PARALLEL-OK: INFFIN.019 + .021 + .028 immediate dispatch siblings; RD .022-.027 staged.
    POTENTIAL CASCADE: Path 2 spawns INFFIN.021b for RD 0.4.2 lane (FE relabel).
    DS SUB-AGENT ROUTING: DS~D primary per bench-clear post NMCOHT.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_scope>Top positions emitter re-run current-date forward; no historical backfill.</reprocess_scope>
  </data_reprocess_scope>

  <deliverables>
    1. Phase 1 feasibility decision
    2. Path 1: gold script augment + deploy + empirical OR Path 2: cascade routing note
    3. RAVC2 with path attestation
  </deliverables>

  <ravc>DS~D RAVC2 to COO + CC CTO + DT 0.4 on AC1-9 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DS_ClientPlatform~D <0.4.0_DS_ClientPlatform~D@opal.agent>"`.

    **Path-conditional:** if feasibility confirms security-grain rollup infeasible, cascade routing clean — DO NOT force Path 1 if data shape doesn't support it. Per banked discipline `feedback_to_scope_none_of_above_space.md` — empirical-first.

    **49F regression:** same TopGainPositions component renders on 49F as well. Path 1 changes affect both partners (gold script shared); Path 2 FE relabel applies to both. Smoke 49F post-deploy.

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
