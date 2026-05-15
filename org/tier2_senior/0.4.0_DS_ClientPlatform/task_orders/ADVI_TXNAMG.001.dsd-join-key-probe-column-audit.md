<task_order>
  <metadata>
    <id>ADVI_TXNAMG.001</id>
    <slug>dsd-join-key-probe-column-audit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-15</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_TXNAMG</project_code>
    <priority>P1 — gates TO-3 (the amalgamating writer); read-only investigation, no ship risk; runs immediately and in parallel with TO-2.</priority>
    <sla>~4-5h wall. Read-only — no commit/deploy cycle.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_TXNAMG.md (PRD v0.1, commit e7fecbf93) — §4.2 column-correspondence audit, §4.5 join-key probe, §6 TO-1.</prd>
    <evidence>docs/briefs/inf-infinc006-cto-validation-20260515.md (58777ee94); docs/briefs/inf-infinc006-topology-coo-packet-20260515.md (428f053dd + 7cb7a7657).</evidence>
  </references>

  <context>
    silver/transactions/{date}.parquet has two live daily writers (PRD §2). ADVI_TXNAMG consolidates to ONE canonical writer by amalgamation: convert_transactions_to_silver.py (REST spine) left-joins every Custom-Report-unique column onto the REST spine by Orion transaction id. Before that writer (TO-3) can be built, three facts must be empirically nailed: (1) the join key, (2) which Custom-Report columns are genuinely unique vs aliases of REST columns, (3) whether the historical backfill-era Custom-Report CSVs share the daily schema. This TO produces all three. It is read-only — no code ships here.
  </context>

  <objective>
    Deliver an evidence-bearing brief that gives TO-3 a definitive, no-ambiguity join spec: the join key, the exact set of Custom-Report-unique columns to carry, and a historical/daily schema-parity verdict.
  </objective>

  <scope>
    <item>(a) JOIN-KEY PROBE (PRD §4.5). Pull REST (bronze/transactions/) + Custom-Report (bronze/orion-api/{date}/transactions.csv) for one shared window. Intersect id sets. Confirm REST `id` is the same identifier as Custom-Report 28198 `Transaction ID`, and that it maps to `id` — NOT `orderId` or `tradeOrderId`. State the match rate and any non-joining rows.</item>
    <item>(b) COLUMN-CORRESPONDENCE AUDIT (PRD §4.2). For every column in the Custom-Report silver schema, classify as: ALIAS of a REST column (e.g. units≡noUnits, trans_amount≡transAmount, type_desc≡trans_type_desc, nav_price≡navPrice, account_id≡accountId) → NOT joined (REST already carries it); or GENUINELY ABSENT from REST (current_account_value, current_cash_value, managed_account, created_date, edited_date, activity_category, account_lname, rep_name, ... — confirm empirically) → carried by the join. Resolve ambiguous cases (account_code vs accountNumber, trade_status vs status, tran_notes vs notes, download_symbol vs ticker, reg_type) by value inspection on overlap rows. OUTPUT: the definitive join column set.</item>
    <item>(c) HISTORICAL SCHEMA-PARITY. The ~2026-05-08–11 backfill-era bronze/orion-api/*/transactions.csv files were bulk-written months of data in one pass; a backfill run can drift Custom Report 28198 versions vs the daily files. Confirm the backfill-era CSVs carry the SAME column set as the recent daily CSVs. If they differ, document the per-era column delta so TO-3 can reconcile.</item>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Join-key verdict: REST `id` ≡ Custom-Report `Transaction ID` confirmed (or refuted with the correct key named), with empirical match rate on a shared window.</ac>
    <ac id="AC2">Definitive Custom-Report-unique join column set — an explicit list, every Custom-Report silver column classified alias-vs-carry, ambiguous cases resolved by value inspection.</ac>
    <ac id="AC3">Historical/daily schema-parity verdict — backfill-era CSVs confirmed same-schema as daily, OR the per-era delta documented.</ac>
    <ac id="AC4">Deliverable is a brief (docs/briefs/) — investigation output, NOT a code ship.</ac>
    <ac id="AC5">Do NOT re-gate the carried columns on "find a consumer" — Andrew's directive carries all genuinely-unique columns for forward use regardless of current consumption (PRD §1).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1: grep + value-inspection probe (boto3/pandas on bronze partitions). Phase 2/3: n/a — read-only investigation, no code commit, no deploy. comp graph does not model manual_api/ pull scripts or the silver/transactions artifact (PRD §5.2 coverage gap) — empirical S3 probes are the sanctioned authoritative basis.</compiler_tools_mandate>

  <cross_domain_coordination>
    Read-only — TO-1 writes no artifact, so no write-collision with any active TO. It READS bronze/transactions/ + bronze/orion-api/*/transactions.csv (shared keys, read-only). TO-1's output (the join column set + key) is the INPUT contract for TO-3 (ADVI_TXNAMG.003, same receiver DS~D) — TO-3 is dispatch_held until this TO's brief is delivered. Runs in parallel with TO-2 (ADVI_TXNAMG.002, DS~B) — no overlap (TO-2 touches gold consumer scripts; TO-1 touches no code).
  </cross_domain_coordination>

  <deliverables>
    <item>Brief at docs/briefs/ — join-key verdict + definitive join column set + schema-parity verdict.</item>
    <item>RAVC2 to COO + CC CTO with the brief path and the three verdicts.</item>
    <item>Session log with Compiler Tools section.</item>
  </deliverables>

  <ravc>DS~D RAVC2 to COO + CC CTO on AC1-5. The join column set + key are the gating input for TO-3 — COO releases TO-3's dispatch_held on validated receipt.</ravc>

  <notes>
    Investigation TO — the bar is empirical evidence, not "code runs." PRD §4.2 lists candidate alias/carry classifications; treat them as starting hypotheses to confirm, not as the answer. The DS~D INFINC.006 Phase-0 probe artifacts (inf_006_phase0_probe.py / inf_006_phase0_result.json) already characterized the REST 31-col bronze schema — reuse that. INFINC.006 stays HELD; this TO does not touch it.
  </notes>
</task_order>
