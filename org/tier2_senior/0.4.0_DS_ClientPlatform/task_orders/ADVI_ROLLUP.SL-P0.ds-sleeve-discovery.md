<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-sl-p0</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to><!-- Base lane per CTO Q2 ACK 2026-04-15 — saturation on ~A/~B/~C/~D; base is the dedicated SLEEVE lane -->
    <date>2026-04-15</date>
    <status>complete</status><!-- Closed 2026-04-15 PM. Path 3 + Path 1 escalation. Cohort 598 in band. Memo docs/architecture/ADVI_SLEEVE_P0_DECISION.md. Session log sleeve_p0_discovery.md. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>SL-P0 (discovery + quantity-source pick)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #9)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_SLEEVE_PLAN.md (authoritative scope)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-15_post_presentation_master_summary.md (§9)</ref>
    <ref type="precedent">B_01 existing RPS synthetic lot injection (pattern to extend for ULN/sleeve path)</ref>
  </references>

  <objective>
    Phase 0 of 4. Discovery + cohort sizing + quantity-source decision for sleeve reconstruction.
    Blocks all subsequent phases (P1 shadow emit, P2 promote, P3 monitor) — SL-P1..P3 cannot start
    until THIS TO commits a quantity-source decision memo.

    Problem: BD sub-custody sleeve accounts (PCRA Trust, SWTC TTEE, similar retirement vehicles)
    land in `silver/allocations` + `silver/unrealized` but never fire Transfer In transactions,
    so gold's FIFO replay never opens lots. Diagnostic case: Jones z0817905851 silver $2,396,510
    vs gold $82,423 = $2.31M missing.

    Firm-wide: ~$35-50M actionable silver-gold under-reconstruction in 403 mapped-no-RPS cohort
    plus ~44 gold-exceeds-silver accounts.

    Scope of THIS TO (P0):
    1. **Cohort detection:** conservative multi-signal classifier on (account_type + account_registration_type
       + account_number prefix + portfolio_group). Output: `sleeve_cohort_{date}.parquet` with
       account_id + sleeve_confidence + detection_signal flags. First-cut cohort sizing (expect ~500-700 accounts).
    2. **Quantity-source pick (MANDATORY — blocks P1..P3):** Choose between 3 candidates, document
       in `docs/architecture/ADVI_SLEEVE_P0_DECISION.md`:

       - **Path 1 (preferred):** BD adds Units column to unrealized export. Requires BD push-back check
         with AE — if ingestion can retrieve from BD's UGL source. Record AE coordination transcript in memo.
       - **Path 2 (fallback):** Pull quantity from adjacent BD feed (ULT = Taxable Unrealized, or positions API).
         Requires investigation of BD feed ecosystem; record findings.
       - **Path 3 (final fallback):** Apportion `account_market_value` across ULN lots by cost-basis weight.
         Breaks on rebalanced sleeves — document accuracy analysis.

    3. **Decision memo commits the chosen path** with rationale, expected accuracy, and rollback plan if
       initial cohort execution reveals a cliff failure.

    4. **No shadow write yet.** No production code change. NO precedence-stack wiring (that's P1).
  </objective>

  <wire_contract>
    Intermediate artifact: `sleeve_cohort_{date}.parquet` (P0 discovery output)
      account_id, sleeve_confidence (0.0-1.0), signals (list of which detections matched),
      account_market_value, estimated_sleeve_lot_count

    Decision memo at `docs/architecture/ADVI_SLEEVE_P0_DECISION.md`:
      - Chosen path (Units | ULT | apportion)
      - Rationale with evidence
      - Expected quantity accuracy (% of positions correctly quantified)
      - Rollback trigger criteria
      - AE coordination notes (path 1 only)
  </wire_contract>

  <acceptance_criteria>
    1. `sleeve_cohort_{date}.parquet` produced; cohort size in expected band (500-700 accounts).
    2. Jones z0817905851 classified as sleeve with sleeve_confidence ≥ 0.9 (spot-check anchor).
    3. Quantity-source decision memo at `docs/architecture/ADVI_SLEEVE_P0_DECISION.md`, explicit choice documented.
    4. If Path 1 chosen: AE coordination transcript in memo confirming BD feed path feasibility.
    5. If Path 3 chosen: accuracy analysis committed showing expected error bounds on rebalanced sleeves.
    6. `comp-validate sleeve_cohort --artifact /tmp/sleeve_cohort.parquet` exits 0.
    7. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    8. MCP COMPLETE to COO with commit hash + decision + cohort size.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io B_01</run>
        <expect>READS includes silver/rps + silver/transactions; WRITES includes gold/timeseries/holdings_lots. Confirms B_01 is the precedence-stack extension point for P1 ULN override.</expect>
        <if_mismatch>If B_01 I/O has drifted, update plan doc reference before writing cohort detector.</if_mismatch>
      </step>
      <step>
        <run>comp-blast silver/unrealized</run>
        <expect>No current gold consumers (confirmed 2026-04-15 pre-flight). silver/unrealized is produced but unused by gold — the gap SLEEVE addresses.</expect>
        <if_mismatch>If a gold consumer now exists, document and decide whether to extend or rewrite.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io silver/unrealized</run>
        <expect>Columns include open_date, unit_cost, asset_id, cusip; quantity IS MISSING (the P0 decision point).</expect>
        <if_mismatch>If quantity is present, Path 1 is already satisfied — choose Path 1 and skip ULT/apportion investigation.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io holdings_lots</run>
        <expect>Current FIFO replay logic visible; precedence with RPS synthetic lots documented. Confirms P1 can extend same pattern.</expect>
        <if_mismatch>Coordinate with DS core on holdings_lots refactor history.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>comp-validate sleeve_cohort --artifact /tmp/sleeve_cohort.parquet</run>
        <expect>Exit 0; cohort size within 500-700 band; sleeve_confidence distribution reasonable.</expect>
        <if_mismatch>Tune classifier thresholds; iterate on detection signals.</if_mismatch>
      </step>
      <step>
        <run>Spot-check Jones z0817905851 in cohort artifact</run>
        <expect>sleeve_confidence ≥ 0.9, at least 2 detection signals matched.</expect>
        <if_mismatch>Debug classifier — this is the anchor case.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>Read back the decision memo from git and confirm all 3 decision-gate fields populated (path, rationale, rollback)</run>
        <expect>Memo is complete and unambiguous — SL-P1 can reference a single decision value.</expect>
        <if_mismatch>Iterate on memo — a vague decision blocks P1 authorship.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. P0 is discovery; independent of W2 BD pipeline work.
  </dependencies>

  <next>
    On P0 commit: signal COO with decision value (Units | ULT | apportion). COO authors SL-P1..P3
    with first acceptance line "SL-P0 decision memo committed and decision = {value}" per CTO directive.
  </next>
</task_order>
