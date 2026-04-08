# ADVI_REBORN.W5-004 -- DS: Fee Efficiency Display Clarification

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-08-reborn-w5-004-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-08</date>
    <status>complete</status>
    <project_code>ADVI_REBORN</project_code>
  </metadata>

  <objective>Clarify what fee_bps_weighted represents and decide whether to show gross client fee or advisor effective rate. Andrew flagged 90-100bps as suspiciously high for advisor-level fees.</objective>

  <context>
  Investigation finding: fee_bps_weighted = implied_annual_fee / managed_aua * 10000.
  Both numerator and denominator are multiplied by split_pct, so the split cancels out.
  The displayed value is the GROSS CLIENT FEE (what the client pays), not the advisor's
  take rate. 90-100bps is a normal range for gross advisory fees.

  The dollar commission IS correctly split-weighted (fee_bps_weighted/10000 * managed_aua
  * period_fraction), because managed_aua = account_AUA * split_pct/100.

  Key files:
  - C_08.advisor_fee_efficiency.py lines 567-570 (split weighting)
  - C_08 scorecard builder lines 199-205 (fee_bps_weighted back-derivation)
  - A_02.fee_rate_history.py line 89 (source: BD "Basis Points" = gross client fee)
  - FeeEfficiencyPanel.tsx line 93 (displays fee_bps_weighted as "Fee")

  Question from Andrew: if splits include architect+consultant+implementor+local ops+others,
  and each advisor shows 90-100bps, wouldn't the aggregate client fee be 200bps+?
  Answer: No -- the 90-100bps IS the aggregate client fee. The split cancels in the
  back-derivation. Each advisor's displayed fee is the same gross rate, not their portion.
  </context>

  <deliverables>
  1. Confirm with Andrew whether the intent is to show:
     (a) Gross client fee rate (current: 90-100bps, correct for client-facing view)
     (b) Advisor's effective rate (fee_bps * split_pct / 100, e.g., ~36-40bps for a 40% split)
  2. If (b): update C_08 to compute and output advisor_effective_bps separately
  3. Update FeeEfficiencyPanel.tsx labels to clarify what the fee represents
  4. Validate a sample of actual fee schedules from BD to confirm 90-100bps gross is realistic for 49F
  </deliverables>

  <dependencies>None -- investigation + decision task. Awaits Andrew's input on display preference.</dependencies>
</task_order>
