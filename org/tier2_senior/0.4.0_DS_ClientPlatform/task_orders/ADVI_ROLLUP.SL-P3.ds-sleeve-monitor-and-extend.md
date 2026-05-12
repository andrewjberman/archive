<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-sl-p3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. --><!-- Dep: SL-P2 in production + 1 week stable operation -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>SL-P3 (monitor + detection extension — terminal)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #9, Phase 3 — terminal)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_SLEEVE_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.SL-P2.ds-sleeve-promote-to-production.md (must be live + 1 week stable)</ref>
  </references>

  <objective>
    Phase 3 of 4 (terminal; PRD numbers this as terminal — SL is P0..P3 = 4 phases total).
    Monitor SL-P2 production behavior + extend sleeve detection to additional cohorts.

    Scope:
    - **Monitor (week-1 post-SL-P2):** nightly sleeve account count + firm-wide silver-gold delta
      trend; flag drift if cohort grows or silver-gold gap widens.
    - **Extend detection:** evaluate ~44 gold-exceeds-silver accounts (opposite direction — gold
      has lots silver doesn't). Some may be legitimate reversals; some may be detection-miss sleeves
      that our classifier mistakenly excluded. Decide inclusion/exclusion per account.
    - **Document edge cases:** any production issues observed (lot reconciliation failures, ULN
      quantity-path accuracy outliers, Jones-style anchor cases that diverge) logged to
      `docs/data/sleeve_production_monitor.md`.
    - **SLEEVE wave close:** final reconciliation memo showing before/after firm-wide silver-gold
      gap reduction + any unresolved outlier accounts.
  </objective>

  <wire_contract>
    Production monitor only. No schema change. Detection-extension logic updates live in the classifier
    module introduced in SL-P0.
  </wire_contract>

  <acceptance_criteria>
    1. Week-1 production monitor report committed to `docs/data/sleeve_production_monitor.md` with daily cohort size + silver-gold delta trend.
    2. ~44 gold-exceeds-silver cohort evaluated; per-account inclusion/exclusion decision documented.
    3. Firm-wide silver-gold gap reduction vs pre-SL-P2: at least 60% of the original $35-50M gap closed.
    4. Any production outliers (non-Jones cases with >5% silver-gold divergence in the sleeve cohort) flagged with root cause.
    5. Final SLEEVE wave closure memo at `docs/data/sleeve_wave_closure.md` — reconciliation numbers + decision log + followup backlog.
    6. `comp-validate holdings_lots --artifact /tmp/holdings_lots.parquet` exit 0 for the week.
    7. Session log Compiler Tools reproduces each `<run>` + observed + pass/fail vs. `<expect>`.
    8. Acceptance-flex pre-flag rule (CTO Rule 7).
    9. MCP COMPLETE with both memo paths + reconciliation summary. **SLEEVE wave TERMINAL.**
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>Review 1-week sleeve_cohort + silver-gold recon harness manifests post-SL-P2</run><expect>Daily cohort size stable ±5%, firm-wide silver-gold gap trending toward reduction target.</expect><if_mismatch>STOP — investigate cohort churn or reconciliation regression before proceeding.</if_mismatch></step>
      <step><run>comp-pipescript io on the sleeve classifier module</run><expect>Classifier still references same silver inputs (account_type, registration_type, account_number prefix, portfolio_group).</expect><if_mismatch>Classifier drifted — scope broken; escalate.</if_mismatch></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>Gold-exceeds-silver cohort evaluation: 44-account review matrix</run><expect>Each account decision-logged with rationale (include | exclude | needs-BD-coordination).</expect><if_mismatch>Incomplete evaluation — complete review before ship.</if_mismatch></step>
      <step><run>Firm-wide gap reconciliation calc</run><expect>≥60% of original $35-50M gap closed.</expect><if_mismatch>Target miss — document cause; MCP heads-up to CTO per Rule 7 before ship.</if_mismatch></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>comp-blast holdings_lots</run><expect>Consumer set stable; no new rogue readers introduced during monitor window.</expect><if_mismatch>Coordinate.</if_mismatch></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.SL-P2" status="staged" description="production live + 1-week stable operation"/>
  </dependencies>

  <next>On commit: SLEEVE wave COMPLETE. ADVI_ROLLUP Wave 4 all three structural convergences TERMINAL (RA + CN + SL). COO marks W4 success criteria met per PRD.</next>
</task_order>
