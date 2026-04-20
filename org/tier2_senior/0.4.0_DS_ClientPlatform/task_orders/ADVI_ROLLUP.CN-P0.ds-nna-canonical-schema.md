<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-cn-p0</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- COMPLETE 2026-04-15 — commit 93b70620 by ~D. Deliverables: docs/data/nna_atomic_schema.md, docs/data/nna_atomic_consumer_enumeration.md, data/black_diamond/scripts/validators/validate_nna_atomic.py. Column list RATIFIED per acceptance #7; further additions require CN-P0a addendum. Unblocks CN-P1 shadow write (paired RA-P1 co-ship in single DS commit). -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>CN-P0 (schema + tests)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #8)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_CANNNA_PLAN.md (authoritative scope)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-15_post_presentation_master_summary.md (§8)</ref>
    <ref type="supersedes">GEO 3-way NNA point fix (item #4) — CANNNA eliminates schism class structurally, per PRD §Risks #3</ref>
    <ref type="cross_domain">ADVI_ROLLUP.RA-P0 + RA-P1 — paired structural convergence (ROLEAUA + CANNNA co-ship shadow artifacts in single D_02 pre-pass commit at P1)</ref>
  </references>

  <objective>
    Phase 0 of 6. Schema design + invariant tests for the canonical `gold/canonical/nna_atomic/{date}.parquet`
    table that will supersede 10 scripts × ~25 aggregation sites with three semantically distinct
    "NNA" concepts:

      - `nna_txn` — C_01 at (date, account_id), the only physically-grounded number
      - `nna = cum_inflows - cum_outflows` — D_00/D_00b/D_00c derived
      - `period_nna = end.nna - start.nna` — D_01 period-differenced on relationship-grain cum columns

    Three concepts × inconsistent dedup (account vs relationship vs state-city) × inconsistent
    EXCLUDE_NAMES filters = Travis three-way on AdvisorPublicProfile, TX three-way on
    Snapshot-GEO-NNA, and 8 other latent schisms.

    Scope of THIS TO (P0 only):
    - Freeze the table schema: one row per `(date, account_id)` with daily + cumulative flows
      plus SCD PIT attribution keys (relationship / architect / implementor / consultant / local_ops /
      additional_advisor / office / state / country / city / tax_status / billable / is_excluded / is_ghost).
    - Write the 5 invariants from plan doc as a standalone validator script
      (`comp-validate nna_atomic` wiring).
    - Enumerate all 12 current aggregation sites across C_01 / D_00 / D_00b / D_00c / D_01 / D_02
      with file:line citations + per-site concept/dedup/filter delta analysis.
    - NO production code change. NO shadow write yet. Zero reader impact.

    P1 (shadow write in C_01, co-ships with RA-P1 in single D_02 pre-pass commit) comes next.
  </objective>

  <wire_contract>
    gold/canonical/nna_atomic/{date}.parquet (P0 produces schema spec + validator only, no data yet):

    | Column | Type | Notes |
    |---|---|---|
    | date | DATE | partition key |
    | account_id | STRING | primary key |
    | daily_inflow | FLOAT | transaction-based |
    | daily_outflow | FLOAT | transaction-based |
    | nna_txn | FLOAT | = daily_inflow - daily_outflow (invariant 1) |
    | cum_inflow | FLOAT | running total |
    | cum_outflow | FLOAT | running total |
    | cum_nna | FLOAT | = cum_inflow - cum_outflow (invariant 2) |
    | relationship | STRING | SCD PIT attribution |
    | architect / implementor / consultant / local_ops / additional_advisor | STRING | role slots |
    | office / state / country / city | STRING | geo attribution |
    | tax_status / billable | ENUM | fee-bucket partition (invariant 5) |
    | is_excluded / is_ghost | BOOL | filter flags |

    Invariants (from plan doc, enforced via validator):
      1. `nna_txn == daily_inflow - daily_outflow` within $0.01 per row
      2. `cum_nna == cum_inflow - cum_outflow` within $0.01 per row
      3. Timeline consistency: `cum_flows[t] == cum_flows[t-1] + daily_flows[t]` per account
      4. Cross-cohort additivity: `sum_{account} daily_inflow` at a date equals firm daily_inflow
      5. Fee-partition preservation: `billable + non_billable == total` per (date, group)

    Final column list confirmed by CTO at P0 review; may adjust before P1 shadow write.
  </wire_contract>

  <acceptance_criteria>
    1. Schema spec committed as `docs/data/nna_atomic_schema.md`.
    2. Invariant validator at `data/black_diamond/scripts/validators/validate_nna_atomic.py` implementing all 5 invariants.
    3. Consumer enumeration memo committed: file:line citations for all ~25 current aggregation sites across the 10 scripts + per-site concept / dedup / filter delta analysis.
    4. Cross-domain coordination block acknowledges RA-P1 as co-ship partner (same D_02 pre-pass commit).
    5. `comp-validate nna_atomic --schema` exits 0.
    6. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    7. **Column list RATIFIED at P0.** No further column additions permitted without a `CN-P0a` addendum TO (CTO lock 2026-04-15). This prevents P1 shadow-write moving-target and protects consumer-reverse work.
    8. MCP COMPLETE to COO with commit hash + memo path + validator pointer.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-blast C_01; comp-blast D_00; comp-blast D_00b; comp-blast D_00c; comp-blast D_01; comp-blast D_02</run>
        <expect>All 6 scripts return downstream graphs; confirm 12 aggregation sites + 3 NNA concepts per plan doc. Record blast outputs per site in P0 memo.</expect>
        <if_mismatch>If aggregation site count drifted from 12 or 3 NNA concepts changed, update plan doc reference in P0 memo before schema write.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse nna_atomic</run>
        <expect>Empty — nna_atomic is a NEW platinum field (CTO auto-rule Phase 1 hit). No existing producer or consumer.</expect>
        <if_mismatch>If any existing reference found, investigate — likely rogue earlier prototype.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>comp-validate nna_atomic --schema</run>
        <expect>Validator script syntax clean; invariant count matches plan doc (5 invariants).</expect>
        <if_mismatch>Fix validator wiring.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile data/black_diamond/scripts/validators/validate_nna_atomic.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast nna_atomic_schema_doc</run>
        <expect>No consumers yet — schema doc is reference only until P1 produces data.</expect>
        <if_mismatch>If an agent is already importing schema, coordinate before they ship on un-validated data.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~B" task="BDPL_CNPRCS.WP-10b" status="pending" description="~B is executing WP-10b (gold↔silver recon harness) first; CN-P0 queues behind its completion to avoid same-agent overlap"/>
  </dependencies>

  <cross_domain_coordination>
    RA-P1 co-ships with CN-P1 in a single DS commit (CTO directive 2026-04-15). Both produce
    shadow artifacts in the D_02 pre-pass. Do not commit CN-P1 alone. CN-P0 and RA-P0 can commit
    independently; they feed the shared P1.
  </cross_domain_coordination>

  <next>
    On P0 complete: ~B signals COO. COO issues CN-P1 TO paired with RA-P1 authored simultaneously.
  </next>
</task_order>
