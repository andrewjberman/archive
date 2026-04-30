<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.003</id>
    <project>ADVI_INFLEC</project>
    <title>Fix NNA pipeline truncation — INF_C_01.canonical_nna.py cuts off at 2021Q1</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status><!-- closure: 650332e58 (INF_C_01 coverage diagnostics shipped; root cause = deployment gap not code); flipped 2026-04-30 by COO ground-truth reconciliation -->
    <priority>high</priority>
    <estimated_effort>1-2h</estimated_effort>
  </metadata>

  <references>
    <ref type="diagnostic_brief">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ADVI_INFLEC_DIAGNOSTIC_BRIEF_20260429.md §C5 + C10</ref>
    <ref type="target_script">data/orion/scripts/gold/INF_C_01.canonical_nna.py</ref>
    <ref type="symptom">timeseries_overview.nna.quarterly = 4 rows (2020Q2–2021Q1 only); all post-2021 NNA = 0</ref>
  </references>

  <context>
    timeseries_overview.nna.quarterly has only 4 rows (2020Q2 through 2021Q1).
    Every period 2021Q2 through 2026Q2 has NNA = 0.0 in growth_decomposition.
    dashboard.json.ytd.nna = 0.0.
    NNA metrics in partner_analytics are all 0.0.

    DS~A confirmed April TRN silver is current (watermark 2026-04-28). So transaction
    data exists. The truncation is in the NNA CALCULATION, not data absence.

    INF_C_01.canonical_nna.py is the canonical NNA computation script. The bug is either:
    A. A date filter that hard-caps NNA computation to before 2021-XX
    B. A client/account ID join that breaks for accounts onboarded after 2021
    C. A transaction type filter that excludes certain inflow/outflow categories
    D. A NULL/NaN accumulation that silently zeros out flows

    This TO investigates and fixes INF_C_01.
  </context>

  <scope>
    STEP 1 — Read INF_C_01.canonical_nna.py in full.
    Identify: date range parameters, transaction type filters, join keys, aggregation logic.

    STEP 2 — Inspect silver/transactions/ data for post-2021 flows:
    Load silver/transactions/ (or s3 equivalent) filtered to Inflection rep_ids {3,11,12}.
    Check: are there inflow/outflow transactions post 2021-Q1? What are their transaction types?
    Quantify: sum of inflows/outflows by year 2021-2026.

    STEP 3 — Identify the break:
    If transactions exist but NNA = 0: the bug is in the computation (date filter, join failure, etc.).
    If transactions DON'T exist post 2021: the silver/transactions pipeline has its own truncation
    (escalate to COO — may require AE bronze/silver investigation, separate from this fix).

    STEP 4 — Fix the identified bug:
    Most likely: fix the date range or join key in INF_C_01 to cover all available periods.
    Add a diagnostic log: print(f"NNA computation: {n_transactions} transactions, date_range={min_date}..{max_date}")
    to make future debugging easier.

    STEP 5 — Pre-commit gate + S3 upload:
    .tools/ds-commit-gate.sh INF_C_01.canonical_nna.py
    aws s3 cp to s3://opal-data-inf/code/gold/INF_C_01.canonical_nna.py
    comp-pipescript deployed INF_C_01 → MATCH

    STEP 6 — Re-run:
    Dispatch INF_C_01 on EC2 for a test run (can be standalone, does not need full chain).
    Verify: timeseries output has NNA rows through 2026Q2; non-zero values for recent periods.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_C_01</run>
        <expect>READS includes silver/transactions (or equivalent NNA source). WRITES includes
        nna-related artifacts. Any COLUMN GAPS in NNA fields documented.</expect>
        <if_mismatch>If READS don't include transactions, the NNA source is wrong — document in RAVC.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_C_01.canonical_nna.py</run>
        <expect>Exit 0. All three checks pass.</expect>
        <if_mismatch>STOP. Fix gate failures first.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after S3 upload">
      <step>
        <run>comp-pipescript deployed INF_C_01</run>
        <expect>MATCH</expect>
        <if_mismatch>Re-upload. Do not signal re-run until MATCH confirmed.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      Root cause identified and documented in session log.
      Evidence: code excerpt showing the bug + fix.
    </criterion>
    <criterion id="2">
      After re-run: timeseries NNA has rows from 2020 through at minimum 2025Q4 (non-zero).
      Evidence: python parse of NNA artifact showing recent non-zero periods.
    </criterion>
    <criterion id="3">
      .tools/ds-commit-gate.sh exit 0. comp-pipescript deployed MATCH.
    </criterion>
    <criterion id="4">
      RAVC to 2.0.0_SA_COO: root cause, fix, commit hash, NNA verification snippet.
      If silver/transactions doesn't have post-2021 data: escalate immediately with evidence
      — do NOT attempt a workaround. COO will route AE investigation.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="none" status="independent"/>
    Parallelizable with DIAGFIX.001, .002, .004, .005.
  </dependencies>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_A &lt;0.4.0_DS_ClientPlatform_A@opal.agent&gt;" \
      -m "fix(ADVI_INFLEC.DIAGFIX.003): INF_C_01 NNA pipeline truncation — restore post-2021 flows" \
      -- data/orion/scripts/gold/INF_C_01.canonical_nna.py
  </commit_identity>
</task_order>
