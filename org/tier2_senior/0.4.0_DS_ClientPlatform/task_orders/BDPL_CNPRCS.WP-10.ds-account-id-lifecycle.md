<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-bdpl-cnprcs-wp10</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. --><!-- ~B assigned 2026-04-15. Flips pending on WP-3 tag cut. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W2</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 2)</ref>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-10)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-14_asset_dim_and_canonical_prices_refactor.md (§WP-10)</ref>
  </references>

  <objective>
    Account-ID lifecycle + canonical account-state-transition table.
    **NOT** cash-as-position (folded into WP-5 per CTO decision) and **NOT** gold↔silver
    recon harness (split into WP-10b).

    Build `gold/canonical/account_lifecycle/{date}.parquet` — one row per
    (account_id, effective_date, state_transition) capturing open/close/rename/merge events
    across silver/account_team + silver/allocations + silver/transactions.

    Purpose: every gold script joining on account_id gets a stable history it can query
    as "what was this account's state on this date" — kills the slow drift where current
    join logic silently swallows closed-but-not-deleted accounts or miscounts reopened
    ones.
  </objective>

  <wire_contract>
    gold/canonical/account_lifecycle/{date}.parquet
      columns: account_id, effective_date, state ('open'|'closed'|'reopened'|'merged'|'renamed'),
               prior_state, transition_reason (enum), source_event (silver path + row offset)

    Consumers (D_00/D_00b/D_00c/D_01/D_02/D_04/C_01/C_05/C_08) join on
    `(account_id, as_of_date)` → latest lifecycle row ≤ as_of_date. Existing joins get
    a lifecycle filter; no schema-breaking change to consumers.
  </wire_contract>

  <acceptance_criteria>
    1. account_lifecycle parquet produced nightly, covers full historical window.
    2. Invariant: every account_id appearing in silver/transactions has ≥1 lifecycle row with state='open' before its earliest transaction date.
    3. Spot-check: accounts known to have closed + reopened (DS identifies 3-5 cases from prior briefs) show correct state_transition timeline.
    4. No consumer break: `comp-blast account_id` downstream readers unchanged; update to consumers is additive.
    5. `comp-validate account_lifecycle --artifact /tmp/account_lifecycle.parquet` exits 0.
    6. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    7. MCP COMPLETE to COO with commit hash + 3-5 spot-check examples.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io on every gold script joining on account_id (D_00, D_00b, D_00c, D_01, D_02, D_04, C_01, C_05, C_08)</run>
        <expect>Enumerated join patterns per script. Record in session log for consumer cutover planning.</expect>
        <if_mismatch>New consumer discovered — extend consumer list + flag to COO.</if_mismatch>
      </step>
      <step>
        <run>comp-blast account_id</run>
        <expect>Full downstream consumer graph enumerated and matches Phase 1 script list.</expect>
        <if_mismatch>Coordinate with COO on graph surprises.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>comp-validate account_lifecycle --artifact /tmp/account_lifecycle.parquet</run>
        <expect>Exit 0; all 3 invariants hold (open-before-tx, state sequence legal, source_event resolvable).</expect>
        <if_mismatch>Iterate until validator clean.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast account_lifecycle</run>
        <expect>Consumer set matches Phase 1 enumeration; no surprise readers.</expect>
        <if_mismatch>Surface to COO; likely a mid-flight consumer commit.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="BDPL_CNPRCS.WP-3" status="staged" description="silver/transactions needs CUSIP backfill first so lifecycle state_transitions can cite asset-flow evidence"/>
  </dependencies>

  <next>
    Parallel to WP-10b (recon harness). Feeds every downstream WP-4..WP-9 consumer.
  </next>
</task_order>
