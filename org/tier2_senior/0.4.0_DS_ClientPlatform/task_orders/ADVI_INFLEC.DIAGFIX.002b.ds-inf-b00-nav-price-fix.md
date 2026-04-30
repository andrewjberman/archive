<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.002b</id>
    <project>ADVI_INFLEC</project>
    <title>INF_B_00 holdings pricing fix — nav_price "last seen wins" overwrites valid price with 0</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status><!-- closure: 127fe2a17 (INF_B_00 nav_price last-seen-wins guard + post-loop diagnostic; 40.2% market_value=$0 root cause fixed); flipped 2026-04-30 by COO ground-truth reconciliation -->
    <priority>high</priority>
    <estimated_effort>1-2h</estimated_effort>
  </metadata>

  <references>
    <ref type="root_cause_source">DIAGFIX.001 RAVC (AE 0.6.1 20260429T204910Z) — Option D confirmed</ref>
    <ref type="target_script">data/orion/scripts/gold/INF_B_00.canonical_holdings.py</ref>
    <ref type="symptom">3,738/9,295 holdings rows (40.2%) have nav_price=0.0 -> market_value=$0; 666/782 accounts partially zeroed</ref>
    <ref type="affected_tickers">HTRB(501 rows), VO(321), VB(318), USRT(312), VOO(297), FXAIX(148)</ref>
    <ref type="immediate_fix">DIAGFIX.002a handles Option 1 (aum_snapshot AUA swap for partner_analytics) — this TO handles Option 2 (holdings root cause)</ref>
  </references>

  <context>
    INF_B_00.canonical_holdings.py reconstructs position snapshots from the Orion TRN feed
    using a "last seen wins" approach for nav_price. Many TRN rows are non-trade events
    (advisory fee payments, journals, income distributions) with nav_price=0. When the LAST
    transaction for an (account, ticker) pair is a non-trade event, the position's nav_price
    is set to 0, making market_value = units * 0.0 = $0.

    This affects 40.2% of holdings rows (3,738/9,295) and 85.2% of accounts (666/782).

    The fix is simple: only update nav_price when the incoming value is positive (> 0).
    This restores correct market values for HTRB, VO, VB, USRT, VOO, FXAIX and all other
    affected tickers.

    After the fix, holdings.market_value.sum() should significantly increase from $89.6M.
    There may be a residual gap vs. aum_snapshot $182.6M due to TRN reconstruction coverage
    (not all positions may have TRN history). Document the post-fix sum in the RAVC.

    This is the root cause fix. DIAGFIX.002a (Option 1) handles the immediate display fix
    (aum_snapshot swap for partner_analytics) and is independent/parallel.
  </context>

  <scope>
    STEP 1 — Read INF_B_00 in full.
    Locate the nav_price update logic — the "last seen wins" loop that sets:
      pos_meta[key]['nav_price'] = nav  (unconditional overwrite)
    Confirm this is the pattern.

    STEP 2 — Apply the fix:
    Change the unconditional update to a guarded write:
      if nav is not None and nav > 0:
          pos_meta[key]['nav_price'] = nav
    Preserve all other logic unchanged.
    Add a diagnostic log line immediately after the loop completes:
      zeroed = sum(1 for v in pos_meta.values() if v.get('nav_price', 0) == 0)
      total = len(pos_meta)
      print(f"INFO: INF_B_00 nav_price guard — {total} positions, {zeroed} still-zero after fix")
    This makes future debugging easy.

    STEP 3 — Pre-commit gate:
    comp-pipescript io INF_B_00 (confirm WRITES gold/canonical/holdings*.parquet)
    .tools/ds-commit-gate.sh data/orion/scripts/gold/INF_B_00.canonical_holdings.py
    aws s3 cp to s3://opal-data-inf/code/gold/INF_B_00.canonical_holdings.py
    comp-pipescript deployed INF_B_00 — MATCH

    STEP 4 — Re-run + verify:
    Dispatch INF_B_00 via SSM on EC2 i-0ed5afded2ebd4ed4.
    After completion, verify:
      holdings.market_value.sum() — expect significantly higher than $89.6M
      Fraction of rows with nav_price=0 — expect < 5% (from 40.2% baseline)
      The diagnostic print: "still-zero after fix" count
    Document pre/post values in session log.

    ESCALATION: If post-fix sum < $130M despite the nav_price fix, flag to COO —
    there may be a second gap (positions entirely absent from TRN feed, or units=0 rows).
    Do NOT attempt a workaround; COO will route investigation.

    STEP 5 — Downstream chain note (for RAVC):
    After INF_B_00 fix, downstream scripts will produce updated outputs on next chain run:
      - INF_D_07.concentration_risk.py — may populate from DIAGFIX.004 fix + better holdings
      - INF_D_09.canonical_performance.py — uses holdings as input
    COO will decide whether to trigger downstream re-runs after reviewing post-fix sum.
    Do NOT trigger downstream runs unless explicitly instructed by COO.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_B_00</run>
        <expect>READS: silver/transactions (or equivalent TRN source). WRITES: gold/canonical/holdings*.parquet.
        Confirm nav_price column is in the output schema.</expect>
        <if_mismatch>If READS don't include transactions, the data source is unexpected — document in RAVC before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_B_00.canonical_holdings.py</run>
        <expect>Exit 0. py_compile + AST + ruff all pass.</expect>
        <if_mismatch>STOP. Fix gate failures first.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after S3 upload">
      <step>
        <run>comp-pipescript deployed INF_B_00</run>
        <expect>MATCH.</expect>
        <if_mismatch>Re-upload. Do not dispatch re-run until MATCH confirmed.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      After re-run: holdings.market_value.sum() > $130M (from $89.6M baseline).
      Fraction of rows with nav_price=0 < 5% (from 40.2% baseline).
      Evidence: python parse of holdings parquet + diagnostic log output in session log.
    </criterion>
    <criterion id="2">
      ds-commit-gate.sh exit 0. comp-pipescript deployed MATCH.
    </criterion>
    <criterion id="3">
      RAVC to 2.0.0_SA_COO: pre/post holdings sum, remaining zero-nav count, commit hash.
      Escalation with evidence if post-fix sum < $130M.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.6.1_AE_PartnerETL" status="complete">DIAGFIX.001 RAVC — root cause confirmed</dependency>
    Parallel with DIAGFIX.002a, DIAGFIX.003, DIAGFIX.004.
    DIAGFIX.002a (Option 1) is NOT gated on this fix and runs independently.
    This fix enables concentration_risk and position-level display accuracy downstream.
  </dependencies>

  <cross_domain_coordination>
    <none/>
    Option 1 (aum_snapshot swap for partner_analytics) already dispatched as DIAGFIX.002a.
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_A &lt;0.4.0_DS_ClientPlatform_A@opal.agent&gt;" \
      -m "fix(ADVI_INFLEC.DIAGFIX.002b): INF_B_00 nav_price last-seen-wins — guard update to nav &gt; 0 only" \
      -- data/orion/scripts/gold/INF_B_00.canonical_holdings.py
  </commit_identity>
</task_order>
