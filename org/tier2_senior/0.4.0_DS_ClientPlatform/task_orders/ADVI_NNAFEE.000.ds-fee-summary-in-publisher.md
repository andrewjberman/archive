# ADVI_NNAFEE.000 — DS: Add fee_summary to book.json and client_detail.json

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-nnafee-000-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <project_code>ADVI_NNAFEE</project_code>
    <priority>high</priority>
    <phase>0</phase>
  </metadata>

  <objective>
    Add a `fee_summary` block to the publisher scripts that produce `book.json`
    (per-advisor) and `client_detail.json` (per-relationship). Without this, the
    L2 and L3 fee panels have no data.
  </objective>

  <context>
    Gold script C_08 (`data/black_diamond/scripts/gold/C_08.advisor_fee_efficiency.py`)
    already produces `gold/canonical/advisor_fee_detail/{date}.parquet` with per-advisor,
    per-account, per-role, per-date fee data.

    The publisher scripts that build book.json and client_detail.json need to read
    from this parquet, aggregate, and embed the fee_summary block.
  </context>

  <references>
    <ref type="prd">docs/architecture/ADVI_NNAFEE_FEE_EFFICIENCY_VIEWS.md</ref>
  </references>

  <scope>
    <files>
      <file action="modify">Publisher script for book.json (per-advisor endpoint)</file>
      <file action="modify">Publisher script for client_detail.json (per-relationship endpoint)</file>
      <file action="read">data/black_diamond/scripts/gold/C_08.advisor_fee_efficiency.py</file>
      <file action="read">gold/canonical/advisor_fee_detail/ parquet files</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Add `fee_summary` block to AdvisorBookResponse (book.json):
```json
"fee_summary": {
  "weighted_avg_fee_bps": 42.3,
  "annual_implied_revenue": 520000,
  "by_role": [
    { "role": "architect", "aua": 85000000, "fee_bps": 55.2, "pct_of_book": 0.68 },
    { "role": "implementor", "aua": 25000000, "fee_bps": 28.1, "pct_of_book": 0.20 }
  ]
}
```
    </requirement>
    <requirement id="2">Add `fee_summary` block to BooksClientDetailResponse (client_detail.json):
```json
"fee_summary": {
  "weighted_avg_fee_bps": 38.5,
  "annual_implied_revenue": 42100,
  "by_account": [
    { "account_id": "***1234", "fee_bps": 52, "aua": 1200000 },
    { "account_id": "***5678", "fee_bps": 35, "aua": 800000 }
  ]
}
```
    </requirement>
    <requirement id="3">Read fee data from `gold/canonical/advisor_fee_detail/` parquet. Aggregate by role for L2, by account for L3.</requirement>
    <requirement id="4">Commit after implementation. Verify the JSON output is correct by spot-checking a few advisors.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">book.json contains fee_summary with by_role array for every advisor with fee data</criterion>
    <criterion id="2">client_detail.json contains fee_summary with by_account array for every relationship</criterion>
    <criterion id="3">Advisors without fee data get fee_summary: null (not missing key)</criterion>
    <criterion id="4">Values match C_08 output when spot-checked</criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency>None — this is Phase 0, the first task in the chain</dependency>
  </dependencies>

  <commit_pattern>feat(NNAFEE): add fee_summary to book.json and client_detail.json publishers</commit_pattern>
</task_order>
