<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_BFIX4.TO-1</id>
    <project>ADVI_BFIX4</project>
    <title>A_03 epsilon guard + z0822229381 AQR source-data investigation (B2 fix per DS~B Hybrid C)</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>0.5-1 day</estimated_effort>
  </metadata>

  <references>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-05-04_49frecn_c1_recovery_propagation_gap_analysis.md (DS~B RAVC1 — Hybrid C recommendation §B2)</ref>
    <ref type="cto_ratify">CTO MCP 2026-05-04 — Hybrid C ratify with B2 ungated direct authorization</ref>
    <ref type="parent_project">ADVI_BFIX4 (this is TO-1; TO-2 = B1 architectural BFIX4 in B_00, awaiting Andrew)</ref>
    <ref type="adjacent">ADVI_49FRECN.003 (Fix A shipped via DS~C 99664e778; closes on detection scope only)</ref>
  </references>

  <context>
    DS~B brief (RAVC1 2026-05-04) identified two independent root causes of c1_recovered=0:
    1. D_04 detection bug (resolved by Fix A — DS~C `99664e778`)
    2. BFIX3 structural failure: bd_df pre-filter (units>0) excludes 40 RECONCILE_DROP Schwab-custodied accounts BEFORE BFIX3 can rescue them. Empirical: canonical_holdings @ 2026-04-30 contains ZERO C1 not-in-gold accounts.

    B2 is the low-risk slice of Fix B (the structural fix). Adds an epsilon guard to the UNREALIZED_DAILY injection path in A_03 to handle edge-class accounts where `abs(units) &lt; 1e-6` causes downstream artifacts. Specifically targets z0822229381 (AQR) as a known case; investigates whether other accounts in similar epsilon territory exist.

    B2 does NOT touch B_00 (that's B1, gated on Andrew). It's additive, low-risk, ship-immediately.

    CTO ratify direct quote: "B2 — ship now via DS~B, no Andrew gate. Scope: A_03 epsilon guard (`if abs(units) &lt; 1e-6: continue` in UNREALIZED_DAILY injection path) + investigate z0822229381 source-data. Risk: LOW (additive filter, doesn't touch reconcile path)."
  </context>

  <scope>
    1. **Read A_03 source** (`data/black_diamond/scripts/gold/A_03*.py`). Identify the UNREALIZED_DAILY injection path. Document the existing handling of zero/near-zero units cases (if any).

    2. **Add epsilon guard** at the appropriate point in the UNREALIZED_DAILY injection path:
       - `if abs(units) &lt; 1e-6: continue` (or equivalent — write whatever fits the local idiom)
       - Add brief inline comment: `# epsilon guard — skip near-zero unit positions to avoid divide-by-zero / phantom AUA` (or similar; keep terse)
       - Verify the guard fires for z0822229381 specifically (run script locally on a fixture if possible; or trace logically)

    3. **Investigate z0822229381 source data**:
       - Query silver/allocations and silver/transactions for z0822229381
       - Confirm: is this an AQR product specifically? Is the units-near-zero state intermittent or persistent?
       - Document findings inline in your session log (no separate brief needed unless surface area is larger than expected)

    4. **Look for similar accounts** in current allocations:
       - Scan recent silver/allocations for accounts with `abs(units) &lt; 1e-6` AND non-zero market_value
       - Are there other AQR-class or similar accounts that this guard will affect?
       - Document in session log

    5. **Pre-commit gate** (CLAUDE.md Rule 14):
       - `.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/A_03*.py`
       - py_compile + AST + ruff (target-version py39)
       - All three must exit 0

    6. **Future annotations** (CLAUDE.md Rule 15): A_03 should already have `from __future__ import annotations` per the backfill sweep. Confirm present.

    7. **Ship sequence**:
       - `.tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_B &lt;0.4.0_DS_ClientPlatform_B@opal.agent&gt;" -m "fix(A_03): epsilon guard for near-zero unit positions (BFIX4 TO-1; B2)" -- data/black_diamond/scripts/gold/A_03*.py`
       - `git push`
       - `aws s3 cp data/black_diamond/scripts/gold/A_03*.py s3://opal-data-bd/code/gold/`
       - `comp-pipescript deployed A_03` → verify MATCH

    8. **AE 0.7 chain re-run dispatch**:
       - RAVC2 to AE 0.7 with: commit ref + S3 ETag + ASK to re-dispatch chain `--from A_03 --force` on bd-gold-qa-runner
       - Note: this is QA-only run; PROD trigger comes after RAVC3 from you confirms expected outcome

    9. **Validation** (post-chain re-run):
       - Read updated `c1_recovered_accounts.json` (sidecar) — count should now include z0822229381 (if AQR rescue path was firing) PLUS z0819627441 (already counted) = 2-3
       - Read updated `out_of_scope_accounts.json` — `excluded_c1_count` should drop slightly (delta = whatever B2 newly rescues; likely 0-2 accounts)
       - Read `firm_composition.json` — total_market_value should tick up by the rescued AUA delta (small; not the full $36.3M gap — that needs B1)
       - RAVC3 to me with: SSM exit + ETag + count + AUA + investigation findings on z0822229381

    10. **Session log**: write to `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-04/advi_bfix4_to1_a03_epsilon_guard.md`
        - Pre/post code diff
        - z0822229381 source-data findings
        - Similar-accounts scan results
        - Pre-commit gate output
        - QA chain re-run SSM ID + outcome
        - Sidecar count + AUA delta
        - Compiler tools §: each `comp-` invocation + observed result
  </scope>

  <acceptance_criteria>
    1. A_03 epsilon guard applied; pre-commit gate (py_compile + AST + ruff) all 3 exit 0.
    2. `from __future__ import annotations` confirmed present.
    3. Commit + push + S3 upload + comp-pipescript deployed MATCH.
    4. AE 0.7 QA chain re-run completes; SSM exit 0.
    5. Sidecar `c1_recovered_accounts.json` count increases by B2 delta (likely 1-2 accounts) vs Fix-A-only baseline.
    6. `excluded_c1_count` drops by same delta (1-2).
    7. Firm AUA increases by rescued AUA delta (small; report exact figure).
    8. z0822229381 investigation findings documented (AQR confirmation + epsilon-state characterization).
    9. Similar-accounts scan complete; impact scope documented.
    10. Session log + RAVC3 to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      <check>comp-pipescript io A_03 — confirm UNREALIZED_DAILY injection path location + downstream consumers</check>
      <check>comp-blast A_03 — identify gold consumers downstream (D_04 + others)</check>
    </before_write>
    <before_commit>
      <check>.tools/ds-commit-gate.sh on A_03*.py edits</check>
      <check>from __future__ import annotations confirmed (CLAUDE.md Rule 15)</check>
    </before_commit>
    <after_commit>
      <check>comp-pipescript deployed A_03 → MATCH after S3 upload</check>
    </after_commit>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <scope_block>QA chain re-run from A_03 forward (`--from A_03 --force` on bd-gold-qa-runner); PROD trigger gated on RAVC3 + COO ratify post-fix outcome.</scope_block>
  </data_reprocess_scope>

  <execution_gate>
    <hard_gate>None — CTO ratified ungated direct ship 2026-05-04. Begin immediately on receipt.</hard_gate>
  </execution_gate>

  <out_of_scope>
    - B1 (BFIX4 architectural mechanism in B_00) — that's TO-2 of ADVI_BFIX4, gated on Andrew ruling.
    - .003 closure — separate concern, Fix A scope only, COO 3-step atomic close after standing-backlog update + ADVI_BFIX4 stub authoring (this commit) lands.
    - Schwab-custodied 40 RECONCILE_DROP recovery — that's B1 territory.
  </out_of_scope>
</task_order>
