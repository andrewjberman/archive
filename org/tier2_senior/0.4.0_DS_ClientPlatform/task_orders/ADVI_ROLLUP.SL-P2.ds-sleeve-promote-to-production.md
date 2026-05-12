<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-sl-p2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. --><!-- Unblocked 2026-05-11 by SL-P1c RAVC4 ACCEPT-WITH-NOTE (COO 12:45Z). 3-nightly shadow window CLEAN: 2026-05-01/06/07 emits, AC2/AC3 Nights 2-3 PASS, Jones $2.47M CTO-Option-A semantics. Ready for DS pickup; awaits explicit COO GO before promotion (reader-visible change). -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>SL-P2 (promote holdings_lots_shadow → production)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #9, Phase 2)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_SLEEVE_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.SL-P1.ds-sleeve-shadow-emit.md (3-night clean + Jones z0817905851 $2.31M gap closed in shadow)</ref>
  </references>

  <objective>
    Phase 2 of 4. Promote sleeve-reconstructed lots from `gold/timeseries/holdings_lots_shadow/`
    into production `gold/timeseries/holdings_lots/`. Precedence stack goes live:
    (1) silver/rps synthetic → (2) silver/unrealized sleeve (NEW) → (3) FIFO.

    Scope:
    - Merge shadow lots into production holdings_lots with precedence stack enforced.
    - Sleeve-cohort accounts now carry ULN-seeded opening lots in production.
    - All downstream consumers (B_02, C_01, C_02, C_03, C_05, D_*) see the new lots via normal reads.

    This is the promotion step — first reader-visible change. Portal surfaces update on next
    platinum refresh.
  </objective>

  <wire_contract>
    Production `gold/timeseries/holdings_lots/{date}.parquet` gains sleeve-seeded rows for the
    ~500-700 account cohort. Schema unchanged — new rows, same columns. Downstream readers see
    increased lot count on sleeve accounts; account_market_value converges to silver.
  </wire_contract>

  <acceptance_criteria>
    1. Shadow 3-night clean confirmed (SL-P1 #2 PASS).
    2. Jones z0817905851: production `account_market_value` now $2.31M higher than pre-SL-P2 (matches silver $2,396,510).
    3. Firm-wide silver-gold gap on 403 mapped-no-RPS cohort: reconciles $30M+ of the original $35-50M.
    4. Zero regression on non-sleeve accounts: `holdings_lots/{date}.parquet` diff confined to cohort rows.
    5. Downstream validation: B_02 holdings_realized / C_01 canonical_nna / D_02 summary AUA reflect the new lots correctly.
    6. `comp-validate holdings_lots --artifact /tmp/holdings_lots.parquet` exit 0.
    7. Session log Compiler Tools reproduces each `<run>` + observed + pass/fail vs. `<expect>`.
    8. Acceptance-flex pre-flag rule (CTO Rule 7).
    9. MCP COMPLETE with commit hash + Jones before/after + firm-wide gap reconciliation $.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>Verify 3-night shadow clean via gold_silver_recon manifests + Jones spot-check</run><expect>3 consecutive clean nightlies, Jones shadow account_market_value within 2% of silver.</expect><if_mismatch>STOP — need more shadow nights OR debug Jones divergence first.</if_mismatch></step>
      <step><run>comp-blast holdings_lots</run><expect>Full downstream consumer graph — B_02, C_01, C_02, C_03, C_05, D_* enumerated. Confirm promotion blast radius.</expect><if_mismatch>New consumer appeared — coordinate.</if_mismatch></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>comp-validate holdings_lots --artifact /tmp/holdings_lots.parquet</run><expect>Exit 0; sleeve-cohort rows present; non-cohort unchanged.</expect><if_mismatch>Iterate.</if_mismatch></step>
      <step><run>Non-sleeve regression: diff holdings_lots non-cohort rows pre/post</run><expect>Zero diff on non-cohort accounts.</expect><if_mismatch>Scope bled — fix.</if_mismatch></step>
      <step><run>Jones z0817905851 account_market_value post-promotion</run><expect>~$2.31M higher than pre-SL-P2 baseline; matches silver within 2%.</expect><if_mismatch>Debug before commit.</if_mismatch></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>Downstream validation: D_02 Travis book AUA reflects new lots</run><expect>AUA shift traceable to sleeve rows on his cohort accounts.</expect><if_mismatch>Coordinate with DE for FE-visible impact check.</if_mismatch></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.SL-P1" status="staged" description="shadow must have 3 clean nightlies + Jones $2.31M gap closed"/>
  </dependencies>

  <next>On commit: SLEEVE production live. COO authors SL-P3 (monitor + detection extension).</next>
</task_order>
