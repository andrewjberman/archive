<to_id>ADHC_GLDINC.SILVER-FIX</to_id>
<project>ADHC_GLDINC</project>
<title>SILVER-FIX — compact-realized.py:94 CLASS-N fix (A_01-provenance pattern, bd silver) + cot A_02 empirical probe rider</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (CTO ruling 1fc184f05, 135214Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>pending</status>
<priority>Low — fix-before-next-upload-run (not emergency wave); fold into COT-FIX delivery window or bd hygiene slot</priority>

<references>
  <ref type="adjudication">CTO 1fc184f05 — compact-realized.py:94 NON-BENIGN CLASS-N; lot-level dedup keep='last' over completion-order concat; gold consumer (A_03 via bd_realized_agg) survivor-independent by construction (trade_date inside dedup key, agg=max) → no served movement from defect or fix; defect surface = compact artifact consumed diagnostics-only</ref>
  <ref type="fix-template">bd oracle-fix A_01 provenance pattern (73ec87a84): provenance columns (_file_date, _intra_pos) + total-order sort before keep='last'</ref>
  <ref type="ds-sweep-citation">DS ab0cd8ba0 Phase-3 sweep: data/black_diamond/scripts/silver/compact-realized.py:94</ref>
  <ref type="a02-correction">CTO 135214Z: cot A_02 reopen condition is UNMONITORED (AST-DEDUP rule structurally silent on cross-function + sort-guarded + payload-variance); empirical probe required per monitoring-path-must-be-real discipline</ref>
</references>

<scope>
## Part 1: compact-realized.py fix (bd silver, Rule 13)

`data/black_diamond/scripts/silver/compact-realized.py:94` — fix the CLASS-N assembly shape:
- Replace completion-order append feeding bare `keep='last'` dedup with the A_01-provenance pattern: add `_file_date` + `_intra_pos` provenance columns + total-order sort on `(lot_key, _file_date, _intra_pos)` (or the script's natural dedup key + provenance) before keep='last'
- Confirm `from __future__ import annotations` as first import (Rule 15)
- bd lane only; deploy to opal-data-bd/code/silver/ via the normal DS Rule-13 cycle

Post-fix verification: first post-fix `--upload` run records compact artifact before/after + verifies A_03 (bd_realized_agg) output is byte-identical (survivor-independence is by construction, but verify empirically as the delta battery).

## Part 2: cot A_02 empirical probe (rider, read-only)

CTO correction: the cot A_02 reopen condition ("same-day fee ties with differing fee payload") is UNMONITORED — the AST-DEDUP static rule is structurally silent on payload values and cross-function dedup shape. Run a one-off probe over cot silver/transactions:

Probe: scan for same-day (trade_date) fee rows within the same account where fee_bps or fee_schedule values DIFFER across rows sharing the same dedup key. Any non-zero count = variance found → report to CTO, A_02 reopens as FIX. Zero variance across all available cot silver history = BENIGN-confirmed (report to CTO, explicitly close the condition).

Output: a simple count + one example row (if any variance). No code change, no TO needed on outcome unless CTO reopens.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change (Part 1 only)">
    <step>
      <run>comp-pipescript io data/black_diamond/scripts/silver/compact-realized.py</run>
      <expect>Consumer map for the compact artifact. Confirm A_03 (bd_realized_agg) is the only gold consumer and it feeds max-agg (survivor-independent).</expect>
      <if_mismatch>Surface any unexpected consumers to CTO+COO before proceeding.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit (Part 1)">
    <step>
      <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/silver/compact-realized.py</run>
      <expect>All checks exit 0; AST-DEDUP WARN silent on the fixed script.</expect>
      <if_mismatch>Fix is incomplete if the CLASS-N WARN still fires.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy + first upload run">
    <step>
      <run>Record compact artifact before/after; verify A_03 bd_realized_agg output byte-identical across both runs.</run>
      <expect>Byte-identical A_03 output (survivor-independence confirmed empirically); compact artifact updated cleanly.</expect>
      <if_mismatch>Any A_03 delta = unexpected; escalate to CTO+COO for never-widen review before proceeding.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **Timing:** fold into the COT-FIX delivery window (AE 0.6.0 cot A_01/A_04 fix wave, in progress). The cot A_02 probe (Part 2) is a natural rider — DS is already working cot silver/transactions data in that window.
- **No Rule 13 cross-firm:** compact-realized.py fix deploys to opal-data-bd ONLY. The Part 2 probe reads cot silver/transactions (read-only, no deploy). Cross-firm bucket refs blocked at commit.
- **Part 2 result routing:** report probe outcome to CTO + COO via MCP. If variance found, CTO adjudicates. If zero-variance, COO explicitly closes the A_02 monitoring condition.
</cross_domain_coordination>

<acceptance_criteria>
- compact-realized.py passes ds-commit-gate.sh; AST-DEDUP WARN silent post-fix.
- comp-pipescript deployed MATCH (opal-data-bd/code/silver/).
- First post-fix upload run: A_03 bd_realized_agg output byte-identical (empirical survivor-independence confirmation).
- cot A_02 probe: outcome reported to CTO+COO (variance count + example if any). Zero-variance = explicit BENIGN-close MCP to CTO+COO.
- RAVC2 to COO: Part 1 commit hash + deploy MATCH + A_03 byte-identical evidence + Part 2 probe outcome.
</acceptance_criteria>

<data_reprocess_scope>
<reprocess>compact-realized.py silver script (bd); post-fix --upload run regenerates the compact artifact. No gold reprocess needed (A_03 agg output byte-identical by construction).</reprocess>
</data_reprocess_scope>
