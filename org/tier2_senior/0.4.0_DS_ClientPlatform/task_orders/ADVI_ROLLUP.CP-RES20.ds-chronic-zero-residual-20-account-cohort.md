<task_order>
  <metadata>
    <id>ADVI_ROLLUP.CP-RES20</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by><!-- self-authored per Andrew 2026-04-22 directive, relayed via COO 20260422T194240Z -->
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>complete</status>
    <completed_date>2026-04-22</completed_date>
    <path_selected>C</path_selected>
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P3 — tail-end MV recovery, not gate-critical</priority>
    <predecessors>
      <predecessor id="ADVI_ROLLUP.CP-VETO-AUTH" status="complete" closeout_date="2026-04-22"/>
      <predecessor id="ADVI_ROLLUP.CP-DS1" status="complete" closeout_date="2026-04-21"/>
    </predecessors>
  </metadata>

  <context>
    After CP-DS1 PIVOT 2 + PIVOT 5 + silver-cap shipped and CP-VETO-AUTH was superseded
    (472-cohort reduced to 0 via existing pivots), a small residual cohort remains.

    Cohort (measured 2026-04-22 against gold/timeseries/holdings_lots/2026-04-20.parquet +
    silver/allocations/2026-04-15.parquet):
      - 20 accounts
      - All alloc_billable with alloc_noncash > $1,000
      - gold_mv = $0 (chronic-zero in gold output)
      - ZERO silver/unrealized rows for any of these accounts
      - Aggregate alloc_noncash missing: $6,013,161

    Top misses:
      z0820721041 — $2,000,000
      z0820721031 — $1,750,000
      z0814308771 — $519,815
      z0814292981 — $469,032
      z0814308781 — $298,973
      z0820682621 — $181,562
      z0820930841 — $166,276
      z0814317801 — $152,358
      z0820682641 — $149,961
      z0820682611 —  $60,392

    These accounts are distinct from the 472 CP-MAP cohort (which HAVE silver/unrealized
    rows but lack Schwab-RPS mapping). The CP-RES20 cohort has NEITHER silver/unrealized
    NOR Schwab-RPS visibility — they are silver-invisible at the custody-feed level. The
    only MV signal we have for them is silver/allocations' per-account market_value field,
    which is portfolio-aggregated (not lot-level).
  </context>

  <objective>
    Recover the $6,013,161 aggregate gold MV gap for the 20-account residual cohort, OR
    document a closed-form reason why a subset cannot be recovered.

    Two candidate authority paths (DS to select + justify in Phase 1):

      Path A — silver/allocations account-level stub:
        Emit a single "synthetic account stub" lot per cohort account to
        gold/holdings_lots with:
          - units = 1
          - price = account_market_value - cash_market_value (from silver/allocations)
          - asset_name = 'SILVER_ALLOC_STUB' (or similar sentinel)
          - is_open = True
          - price_quality = 'allocation_stub'
        Pro: simple, covers MV at account grain.
        Con: distorts lot-level semantics (no real cost basis, no term, no acquisition_date).
        Downstream: need to flag price_quality='allocation_stub' for lot-level consumers to
        filter out (B_01b classify, C_02 canonical_lots, C_05 client_tax_liability).

      Path B — silver/positions (if it has data for these accounts):
        Load silver/positions_cube or silver/daily_positions and check coverage for the
        20-account cohort. If present, build proper lot-level records.
        Pro: preserves lot semantics.
        Con: silver/daily_positions is stale (last updated 2026-02-02 per S3 ls);
        silver/positions_cube may be more current. Need to verify.

      Path C — document silver-invisibility and exclude:
        If neither silver/allocations stub nor silver/positions can produce defensible
        lot records, document the cohort as silver-invisible and file a feed-expansion
        TO (CP-MASTERFEED-like, for the AE pod to pursue with Schwab/BD data team).
        The $6M gap stays as a known residual, within the 2% Gate 2 band.
  </objective>

  <wire_contract>
    If Path A or B selected: gold/timeseries/holdings_lots/{date}.parquet gains rows for
    the 20 cohort accounts, aggregate MV matches silver/allocations non-cash within 1%.
    Firm non-cash gold MV shifts from $1,660,263,546 toward $1,666,276,707 (estimated
    recovery).

    If Path C selected: no code change; deliverable is the feed-expansion follow-on TO +
    documentation of residual.
  </wire_contract>

  <acceptance_criteria>
    1. Authority path (A / B / C) selected with justification in session log.
    2. If A or B: code change shipped + py_compile exit 0 + ds-commit-gate exit 0.
    3. If A or B: QA run against bd-gold-qa-runner; verify cohort MV emits correctly.
    4. Regression-free on the other 6,523 alloc_billable accounts (firm non-cash gold MV
       does not change by more than $500 outside the cohort — tight regression budget
       given the small scope).
    5. comp-validate B_01 exit 0; comp-pipescript deployed MATCH.
    6. MCP COMPLETE to COO with: path selected, MV recovered (or $0 with C),
       residual chronic count, commit hash.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 — pre-write (authority selection):
      <run>aws s3 ls s3://opal-data-bd/silver/positions_cube/ | tail -5</run>
      <expect>At least one partition dated within 7 days of 2026-04-20, with non-zero size</expect>
      <if_mismatch>silver/positions_cube is stale — eliminate Path B; choose A or C</if_mismatch>

      <run>python -c "import pandas as pd; df = pd.read_parquet('s3://opal-data-bd/silver/positions_cube/{latest}.parquet'); print([a for a in ['z0820721041','z0820721031','z0814308771','z0814292981','z0814308781'] if a in set(df['account_id'].unique())])"</run>
      <expect>At least 3 of 5 top-miss accounts present in silver/positions_cube</expect>
      <if_mismatch>silver/positions_cube lacks cohort coverage — eliminate Path B; choose A or C</if_mismatch>

      <run>comp-blast B_01.holdings_lots.py</run>
      <expect>List of downstream consumers (B_01b, C_02, C_03, C_05, C_06, C_07) confirmed; no new consumers added since CP-DS1</expect>
      <if_mismatch>New consumer = review impact before writing stub emission</if_mismatch>

      <run>comp-platinum reverse price_quality</run>
      <expect>Enumerate current price_quality values downstream consumers expect</expect>
      <if_mismatch>'allocation_stub' collision or missing downstream branch = add filter</if_mismatch>

    Phase 2 — pre-commit:
      <run>python -m py_compile data/black_diamond/scripts/gold/B_01.holdings_lots.py</run>
      <expect>exit 0</expect>
      <if_mismatch>syntax error — fix before commit</if_mismatch>

      <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/B_01.holdings_lots.py</run>
      <expect>exit 0 (py_compile + AST undefined-name scanner)</expect>
      <if_mismatch>undefined name / rename propagation miss — fix before commit</if_mismatch>

    Phase 3 — post-QA:
      <run>comp-pipescript deployed B_01</run>
      <expect>MATCH</expect>
      <if_mismatch>STALE — S3 upload missing or mid-deploy</if_mismatch>

      <run>comp-validate B_01 --artifact /tmp/holdings_lots_2026-04-20.parquet</run>
      <expect>exit 0; cohort MV recovery reported</expect>
      <if_mismatch>validation failure — investigate before MCP COMPLETE</if_mismatch>
  </compiler_tools_mandate>

  <dependencies>
    <dependency task="ADVI_ROLLUP.CP-DS1" status="complete"/>
    <dependency task="ADVI_ROLLUP.CP-VETO-AUTH" status="complete"/>
    <dependency task="silver/positions_cube freshness"
      description="Path B viability gate — if stale, Path B eliminated"/>
  </dependencies>

  <risk>
    Path A stub emission distorts lot-level downstream consumers unless cleanly flagged.
    B_01b (classify_new_securities) may attempt to classify 'SILVER_ALLOC_STUB' as a new
    security — MUST filter by price_quality before DynamoDB write. C_02 (canonical_lots)
    must filter stubs before FIFO cost-basis logic.

    Path C leaves the $6M gap as a known residual. Firm non-cash at $1,660,263,546 is
    -0.004% vs $1,660,325,207 target — already well inside Gate 2 band. A "no-op close"
    is defensible but must document the feed-expansion follow-on for visibility.

    Small MV budget ($6M / $1.66B = 0.36%) does not justify a high-risk emission path.
    Bias toward Path C unless Path B proves trivially available.
  </risk>

  <next>
    On complete: firm non-cash gold MV either +$6M (Path A/B) or documented residual
    (Path C). ADVI_ROLLUP non-cash recon fully closed to the feed-boundary level. Any
    remaining gap is a feed-expansion scope for the partner-ETL pod, not a gold-script
    scope.
  </next>
</task_order>
