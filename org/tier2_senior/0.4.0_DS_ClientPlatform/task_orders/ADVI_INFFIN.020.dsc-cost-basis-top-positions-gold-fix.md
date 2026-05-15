<task_order>
  <metadata>
    <id>ADVI_INFFIN.020</id>
    <slug>dsc-cost-basis-top-positions-gold-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-15</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>Cascade from ADVI_INFFIN.019 RAVC2 (08e9e4301). All 4 root causes empirically confirmed.</dispatch_unblock_condition>
    <completed_at>2026-05-15T01:56Z</completed_at>
    <completed_commit>9e5d5359d</completed_commit>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Andrew dashboard tomorrow gate; CBBY $1.31B vs $27M semantic error + Top Gain Positions N/A</priority>
    <sla>~2-3h wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="investigation">ADVI_INFFIN.019 RAVC2 (08e9e4301) — 4 root causes; brief: docs/briefs/data-scientist-inflection-cost-basis-investigation-20260514.md</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 walkthrough image #8: cost_basis values + capital gains visible on Books tab</ref>
    <ref type="script_a">data/orion/scripts/gold/INF_D_02.client_portal_summary.py — CBBY + Top Gain Positions logic</ref>
    <ref type="script_b">data/orion/scripts/gold/INF_D_00.portal_leaderboard.py — firm-level aggregation of same metrics</ref>
    <ref type="account_gains_source">data/orion/scripts/gold/INF_B_03.account_gains.py output — (date, account_id, ticker) with cost_basis + unrealized_gain + asset_name + term</ref>
    <ref type="canonical_lots_source">gold/canonical_lots — per-lot cost basis for current holdings only (disposed lots excluded)</ref>
    <ref type="ae_chain_coord">AE 0.6.1 — chain re-fire needed after gold script ship (INF_D_02 + INF_D_00 run)</ref>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.6a-d (CTO 23fdaac67)</ref>
  </references>

  <context>
    INFFIN.019 empirically confirmed 4 root causes. This TO ships Fix A + Fix B + Fix D. Fix C (label rename) is FE-only — routed to RD 0.4.2 separately.

    Fix A — CBBY SOURCE ERROR (highest priority):
    Current: INF_D_02 `_aggregate_cost_basis_by_year` sums trans_amount for ALL Buy Exchange (type 10) + Income Reinvested (type 14) transactions (621,643 rows, $1.548B total). INCLUDES positions already sold. Result: $1.31B vs AUA $203M.
    Correct source: canonical_lots — per-lot cost basis for CURRENT holdings only (disposed lots excluded). Expected CBBY post-fix: ~$27M (matching AUA-scale correctly).

    Fix B — TOP GAIN POSITIONS SOURCE ERROR:
    Current: Top positions sourced from bronze buy transactions — wrong table, wrong grain, silent account_id format mismatch causes N/A on cost_basis.
    Correct source: gold/account_gains/{date}.parquet (INF_B_03 output) — per-(account_id, ticker) with cost_basis + unrealized_gain + asset_name + term. Sort by unrealized_gain DESC (not market value).

    Fix D — STALE ARTIFACT HOUSEKEEPING (low priority, bundle):
    platinum/firm/snapshots/aua_by_tax_status.json has data:[] (dead/stale). INF_D_00 emit should remove or tombstone this artifact.

    49F SCOPE NOTE: DS~C INFFIN.019 flagged that INF_D_02 CBBY pattern also appears in 49F's D_02 equivalent. Phase 0 includes a grep/comp-pipescript io check to confirm whether 49F D_02 shares the same bug. If shared code: Fix A scope includes 49F D_02. If separate: flag to 49F DS lane TO.
  </context>

  <objective>
    Fix INF_D_02 + INF_D_00 gold scripts: (A) CBBY from canonical_lots for current holdings only, (B) Top Gain Positions from account_gains parquet sorted by unrealized_gain DESC, (D) remove stale aua_by_tax_status emit. Ship + chain re-fire via AE 0.6.1.
  </objective>

  <scope>
    <files>
      <file action="modify">data/orion/scripts/gold/INF_D_02.client_portal_summary.py — Fix A + Fix B + 49F scope check</file>
      <file action="modify">data/orion/scripts/gold/INF_D_00.portal_leaderboard.py — Fix A aggregate + Fix D stale artifact</file>
      <file action="readonly_reference">data/orion/scripts/gold/INF_B_03.account_gains.py — output schema for Fix B source</file>
      <file action="readonly_reference">gold/canonical_lots — schema for Fix A source</file>
    </files>
  </scope>

  <phase id="0" when="before write — I/O surface + 49F scope check">
    <step>
      <run>comp-pipescript io INF_D_02 — confirm: CBBY logic location, Top Positions logic location, canonical_lots read path availability, account_gains read path availability.</run>
      <expect>Column gap check clean. CBBY + Top Positions source identified. canonical_lots + account_gains S3 paths confirmed accessible.</expect>
    </step>
    <step>
      <run>comp-pipescript io INF_D_00 — confirm: firm-level CBBY aggregation path. Locate aua_by_tax_status emit for Fix D.</run>
      <expect>INF_D_00 I/O surface mapped. aua_by_tax_status emit location identified.</expect>
    </step>
    <step>
      <run>grep "cost_basis_by_year\|aggregate_cost_basis\|trans_amount" data/orion/scripts/gold/ -r --include="*.py" | grep -v INF_D_02 | grep -v INF_D_00 — identify if 49F D_02 or other scripts share the pattern.</run>
      <expect>49F scope confirmed or ruled out. If 49F D_02 shares pattern: Fix A applies to both scripts in Phase 1.</expect>
      <if_mismatch>If 49F D_02 shares bug: include in Fix A scope this TO. If separate 49F script: flag scope to 49F DS lane + note in RAVC2.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="implementation">
    <step>
      <run>INF_D_02 Fix A: Replace `_aggregate_cost_basis_by_year` source from buy-transaction bronze sweep to canonical_lots join. canonical_lots provides per-lot cost_basis for current holdings (disposed lots absent by construction). Sort key: (year, account_id). Preserve existing column names in output so downstream platinum shape is unchanged.</run>
      <expect>CBBY values drop from $1.31B range to ~$27M AUA-scale range. Shape preserved.</expect>
    </step>
    <step>
      <run>INF_D_02 Fix B: Replace Top Gain Positions source from buy-transaction bronze to INF_B_03 account_gains parquet (date-partitioned). account_id join key type-match (INT64 → INT64, per coerce_silver_ids convention). Sort by unrealized_gain DESC. Cap at top 10. Emit: account_id, ticker, cost_basis, unrealized_gain, asset_name, term.</run>
      <expect>Top Gain Positions populates with real unrealized_gain values. cost_basis no longer N/A. Sort by gain not market value.</expect>
    </step>
    <step>
      <run>INF_D_00 Fix A: Update firm-level CBBY aggregation to read from INF_D_02 canonical_lots-sourced CBBY (or directly from canonical_lots at firm-level). Ensure aggregate math is consistent with D_02 fix.</run>
      <expect>Firm-level CBBY consistent with client-level.</expect>
    </step>
    <step>
      <run>INF_D_00 Fix D: Remove or tombstone aua_by_tax_status.json emit (data:[] is dead). If removal: delete emit block. If tombstone: emit with deprecation marker. Prefer removal if no downstream consumer.</run>
      <expect>Stale artifact no longer emitted or explicitly tombstoned. comp-pipescript io confirms no platinum consumer of this key.</expect>
    </step>
    <step>
      <run>ds-commit-gate.sh INF_D_02 INF_D_00 — py_compile + AST + ruff py39.</run>
      <expect>3-gate PASS on both scripts.</expect>
      <if_mismatch>Fix before committing. Do not advance to deploy with a failing gate.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="validation">
    <step>
      <run>Sample validation: read current S3 platinum clients_tab.json for 3 accounts. Verify Fix A: per-year CBBY values are now AUA-scale (~$27M total range). Verify Fix B: top gain positions have cost_basis values (not N/A) and are sorted by unrealized_gain DESC.</run>
      <expect>CBBY values AUA-scale. Top positions populated and sorted correctly.</expect>
    </step>
    <step>
      <run>49F regression: if Fix A applied to 49F D_02, verify 49F platinum Books tab CBBY is also corrected and within expected AUA range for 49F firm.</run>
      <expect>49F regression clean or explicitly scoped out with flag to DS lane.</expect>
    </step>
  </phase>

  <phase id="3" when="commit + deploy + chain re-fire">
    <step>
      <run>safe-commit.sh --author "0.4.0_DS_ClientPlatform~C &lt;0.4.0_DS_ClientPlatform~C@opal.agent&gt;" -m "fix(INFFIN.020): CBBY source → canonical_lots + Top Gain Positions → account_gains + aua_by_tax_status housekeeping" -- data/orion/scripts/gold/INF_D_02.client_portal_summary.py data/orion/scripts/gold/INF_D_00.portal_leaderboard.py</run>
      <expect>Commit clean. No contamination.</expect>
    </step>
    <step>
      <run>safe-deploy.sh — push to CLOUD + S3 upload + comp-pipescript deployed MATCH for INF_D_02 + INF_D_00.</run>
      <expect>SHA-MATCH on both scripts. Deploy clean.</expect>
    </step>
    <step>
      <run>Notify AE 0.6.1 via MCP: "INFFIN.020 Fix A+B shipped (commit SHA). INF_D_02 + INF_D_00 updated. Chain re-fire needed — INF_D_02 run on today's date to materialize CBBY fix + Top Positions fix to platinum." Include commit SHA + deployed confirmation in the message.</run>
      <expect>AE 0.6.1 receives chain re-fire signal. They coordinate the --single INF_D_02 + INF_D_00 dispatch.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + AE 0.6.1 with: commit SHA, safe-deploy MATCH evidence, before/after CBBY value comparison (S3 artifact sample), Top Positions fix evidence, 49F scope ruling.</run>
      <expect>Evidence-bearing RAVC2. Andrew dashboard gate: tomorrow.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: INF_D_02 CBBY sources from canonical_lots (current holdings only — disposed lots excluded)
    AC2: CBBY values are AUA-scale (~$27M range for Inflection) — not historical-aggregate inflated ($1.31B)
    AC3: Top Gain Positions sources from account_gains parquet (INF_B_03 output)
    AC4: Top Gain Positions sorted by unrealized_gain DESC (not market value)
    AC5: Top Gain Positions cost_basis and unrealized_gain fields populated (not N/A)
    AC6: Top Gain Positions includes asset_name + term per INF_B_03 emit
    AC7: INF_D_00 firm-level CBBY consistent with INF_D_02 client-level after Fix A
    AC8: aua_by_tax_status.json emit removed or tombstoned (stale artifact)
    AC9: 49F scope: Fix A applied to 49F D_02 if shared code confirmed; else flagged to 49F DS lane in RAVC2
    AC10: ds-commit-gate.sh 3-gate PASS on INF_D_02 + INF_D_00
    AC11: from __future__ import annotations preserved as first import per Rule 15
    AC12: safe-deploy.sh PASS + comp-pipescript deployed MATCH on both scripts
    AC13: AE 0.6.1 notified for chain re-fire via MCP
    AC14: No emoji per CLAUDE.md
    AC15: RAVC2 to COO + CC CTO + AE 0.6.1 with evidence
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 0 comp-pipescript io x2 + grep 49F check; Phase 1 ds-commit-gate.sh x2; Phase 2 comp-pipescript deployed x2.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: INFFIN.019 RAVC2 complete (08e9e4301). DS~C executes Fix A+B+D.
    FE LANE: Fix C (Capital Gains TTM label rename → "Unrealized P&L Change (TTM)") is RD 0.4.2 — dispatched separately.
    AE CHAIN: AE 0.6.1 CC on RAVC2; chain re-fire needed to materialize D_02 + D_00 platinum output.
    49F SCOPE: Confirm or rule out at Phase 0 step 3 (grep sweep). If 49F D_02 shares pattern: scope in. If separate: flag to 49F DS lane.
    DT: No portal change from DS side. RD Fix C label change will bump portal — DT will handle that submodule bump.
    ANDREW DASHBOARD: Tomorrow gate. Ship tonight.
  </cross_domain_coordination>

  <data_reprocess_scope>
    INF_D_02 + INF_D_00 re-run for today's date only. canonical_lots and account_gains partitions already on S3 (from daily chain). No silver/bronze re-emit. No Lambda redeploy. AE 0.6.1 coordinates the gold script re-fire.
  </data_reprocess_scope>

  <deliverables>
    1. INF_D_02 Fix A (CBBY → canonical_lots) + Fix B (Top Positions → account_gains)
    2. INF_D_00 Fix A (firm-level CBBY) + Fix D (stale artifact housekeeping)
    3. 49F scope ruling (include or flag)
    4. ds-commit-gate.sh PASS evidence (both scripts)
    5. safe-deploy.sh + comp-pipescript deployed MATCH
    6. AE 0.6.1 chain re-fire notification
    7. RAVC2 with before/after CBBY values + Top Positions evidence
  </deliverables>

  <ravc>DS~C RAVC2 to COO + CC CTO + AE 0.6.1 on AC1-15 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DS_ClientPlatform~C &lt;0.4.0_DS_ClientPlatform~C@opal.agent&gt;"`.

    **Fix A source mechanics:** canonical_lots is a gold artifact produced by a separate script. Confirm the S3 path and partition key for today's date before writing the join. Use the same date-partition pattern as other gold scripts (e.g., `s3://opal-data-inf/gold/canonical_lots/{date}/`). If canonical_lots schema differs from expected, adjust — the key invariant is: only CURRENT holdings, not disposed lots.

    **Fix B source mechanics:** account_gains parquet at `s3://opal-data-inf/gold/account_gains/{date}/` (INF_B_03 output). Schema: (date, account_id, ticker, cost_basis, unrealized_gain, asset_name, term). Join on account_id (INT64). Sort by unrealized_gain DESC. Cap at top 10 per account.

    **Fix D — comp-pipescript io check first:** Before removing aua_by_tax_status.json emit, confirm no platinum consumer via comp-pipescript io INF_D_00. If consumer found: DO NOT remove, escalate to COO. If no consumer (data:[] confirmed dead): remove the emit block.

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
