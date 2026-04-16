<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-sl-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>pending</status><!-- picked up 2026-04-16; SL-P0 hard gate cleared via commit 2db02ebc + decision memo (Path 3 apportion + Path 1 escalation, 598 cohort) -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>SL-P1 (shadow emit to holdings_lots_shadow/)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #9, Phase 1)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_SLEEVE_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.SL-P0.ds-sleeve-discovery.md — decision memo at docs/architecture/ADVI_SLEEVE_P0_DECISION.md is the hard gate</ref>
    <ref type="precedent">B_01 RPS synthetic lot injection (existing pattern to extend for ULN/sleeve path)</ref>
  </references>

  <objective>
    Phase 1 of 4. Shadow-emit sleeve-reconstructed lots to `gold/timeseries/holdings_lots_shadow/{date}.parquet`
    using the quantity-source path ratified in SL-P0's decision memo.

    Scope:
    - Read SL-P0 output `sleeve_cohort_{date}.parquet` to identify target accounts (sleeve_confidence threshold TBD in P0 memo).
    - Seed opening lots from `silver/unrealized` using the chosen quantity source (Units | ULT | apportion).
    - Apply incremental silver/transactions on top (standard FIFO after opening state).
    - Emit as SHADOW at `holdings_lots_shadow/` — NOT at `holdings_lots/`. No reader impact.
    - Precedence stack documented in commit: (1) silver/rps synthetic, (2) silver/unrealized sleeve, (3) FIFO.

    Diagnostic check: Jones z0817905851 shadow reconstruction should close $2.31M silver-gold gap
    (silver $2,396,510 vs gold $82,423).

    NO promotion to production `holdings_lots/` — that's P2.
  </objective>

  <wire_contract>
    New shadow output at `gold/timeseries/holdings_lots_shadow/{date}.parquet`. Same schema as
    production holdings_lots for drop-in parity. Zero change to production holdings_lots or any
    reader downstream. Rollback = delete shadow artifact.
  </wire_contract>

  <acceptance_criteria>
    1. **SL-P0 decision memo committed and decision = (Units | ULT | apportion).** [HARD GATE — verify the memo file exists + decision field populated before any code change.]
    2. `gold/timeseries/holdings_lots_shadow/{date}.parquet` produced nightly for sleeve cohort accounts only.
    3. Jones z0817905851 shadow reconstruction: account_market_value within 2% of silver `$2,396,510` (allowing for timing + cost-basis-weight edge cases).
    4. Firm-wide shadow coverage: ~$30M+ of the ~$35-50M silver-gold gap reconciled on the 403 mapped-no-RPS cohort.
    5. Zero-byte diff on production `holdings_lots/{date}.parquet` and all downstream consumers.
    6. `comp-validate holdings_lots_shadow --artifact /tmp/holdings_lots_shadow.parquet` exit 0.
    7. Session log Compiler Tools reproduces each `<run>` + observed + pass/fail vs. `<expect>`.
    8. Acceptance-flex pre-flag rule (CTO Rule 7).
    9. MCP COMPLETE to COO with commit hash + Jones spot-check + firm-wide coverage $ + decision-path citation.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat docs/architecture/ADVI_SLEEVE_P0_DECISION.md | grep -i 'decision\|path'</run>
        <expect>Decision value explicitly: Units | ULT | apportion. Memo present + committed.</expect>
        <if_mismatch>HARD STOP — SL-P0 not complete. Do not proceed.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io B_01</run>
        <expect>B_01's RPS synthetic pattern identifiable for extension to ULN/sleeve path.</expect>
        <if_mismatch>Pattern drifted — re-read B_01.</if_mismatch>
      </step>
      <step>
        <run>comp-blast silver/unrealized</run>
        <expect>Still no gold consumers (SLEEVE is the first). No surprise reader.</expect>
        <if_mismatch>If a gold consumer now reads silver/unrealized, coordinate before producing shadow.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>comp-validate holdings_lots_shadow --artifact /tmp/holdings_lots_shadow.parquet</run>
        <expect>Exit 0; schema parity with production holdings_lots; cohort-size reasonable.</expect>
        <if_mismatch>Iterate.</if_mismatch>
      </step>
      <step>
        <run>Diff gold/timeseries/holdings_lots/{date}.parquet pre/post commit</run>
        <expect>Zero-byte diff. Shadow is additive only.</expect>
        <if_mismatch>STOP — scope bled into production.</if_mismatch>
      </step>
      <step>
        <run>Spot-check Jones z0817905851 in shadow output</run>
        <expect>account_market_value within 2% of silver $2,396,510.</expect>
        <if_mismatch>Debug lot-seeding logic before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast holdings_lots_shadow</run>
        <expect>No consumers yet (shadow only).</expect>
        <if_mismatch>Rogue reader imported early — coordinate before P2 cutover.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.SL-P0" status="complete" evidence="2db02ebc" description="HARD GATE cleared: SL-P0 sleeve discovery complete, Path 3 + Path 1 escalation, 598 cohort, decision memo shipped"/>
  </dependencies>

  <next>
    On commit: COO authors SL-P2 (promote shadow → production) with staged dep on 3 clean nightlies + Jones verification.
  </next>
</task_order>
