# Task Order: ADVI_TICKID.008 — Bond Face-Value Classifier (CONDITIONAL)

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-bond-classifier</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
  </metadata>

  <objective>
    CONDITIONAL on .007 residual: if script 05c gap remains above 0.5% after the
    account-level silver override (.007) is deployed and a gold run completes,
    implement position-level bond detection in scripts 05/05b using ETFClassifier.
    $51M gross impact from bond face-value mispricing (e.g., BNP PARIBAS: units=215K
    face value * Yahoo equity price $96.21 = $20.7M vs actual $1.84M).
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/05_build_client_performance.py</file>
      <file action="modify">data/black_diamond/scripts/gold/05b_build_account_performance.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">GATE: Only begin this work if .007 is complete, a gold run has
      executed with the silver override, and script 05c output shows residual divergence
      above 0.5%. If residual is at or below 0.5%, this TO is NOT NEEDED — mark complete
      with "not needed, target met by .007" and close.</requirement>
    <requirement id="2">If gate passes: load ETFClassifier from lib/etf_classifier.py
      (already used in 06b and 12). For each position classified as fixed_income where
      gold market_value diverges from its proportional share of silver account_market_value
      by more than 50%: replace with silver-derived value.</requirement>
    <requirement id="3">Extend ETFClassifier regex for individual bonds that may not match
      current patterns. Add coupon-rate pattern matching (\d+\.?\d*% in asset_name) and
      known bond keywords (e.g., "MATURITY", "COUPON", "FRN", "CLO").</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">BNP PARIBAS-type positions no longer show 10x overstatement</criterion>
    <criterion id="2">Fixed income positions use silver-anchored values when gold diverges significantly</criterion>
    <criterion id="3">Script 05c gap for fixed_income positions decreases</criterion>
    <criterion id="4">OR: if .007 alone meets the 0.5% target, this TO is closed as "not needed"</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>This TO shares the same code surface as .007 (scripts 05/05b). If both are needed, .008 builds on top of .007's changes — never conflicts.</constraint>
    <constraint>Do NOT begin before .007 is deployed and validated via a gold run. The gate check is mandatory.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_TICKID.007" status="complete"/>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_GLDRST.002-combined-gold-rerun" status="pending"/>
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_TICKID_PRICING_DIVERGENCE_ADDENDUM.md</ref>
  </references>

  <deliverables>
    <deliverable type="commit">Modified scripts 05/05b with bond classifier logic, OR "not needed" closure</deliverable>
  </deliverables>
</task_order>
