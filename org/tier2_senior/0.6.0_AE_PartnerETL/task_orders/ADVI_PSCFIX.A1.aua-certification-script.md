# Task Order: ADVI_PSCFIX A1 — AUA Certification Script

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-11-advi-pscfix-a1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-11</date>
    <status>pending</status>
  </metadata>

  <objective>
    Write and wire 05d_write_aua_certification.py in the BD EC2 gold runner.
    This script runs daily after 05c_validate_aua_vs_silver.py and produces
    gold/aua_certification/{today}.json — the certified_aua figure that the
    bd-portal-publisher Lambda uses to override total_aua fields across all
    publisher outputs.
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/ec2/bd_pipeline/scripts/05d_write_aua_certification.py</file>
      <file action="modify">infra/aws/ec2/bd_pipeline/run_gold.sh (or equivalent EC2 runner entrypoint)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Script logic (exactly as specified in PRD):
      1. Check if silver/allocations/{today}.parquet exists in S3. If not: log
         "SKIP: no silver allocation for {date}" and exit 0 (non-blocking).
      2. Load the parquet. Exclude liability account types from AUA total:
         CreditCard, Mortgage, Loans, Insurance, TermLife, Annuity.
         Sum account_market_value -> certified_aua.
      3. Load gold/client_performance.parquet. Filter to date == today.
         Sum total_aua -> gold_aua.
      4. Write gold/aua_certification/{today}.json to S3 with this exact shape:
         {
           "date": "YYYY-MM-DD",
           "certified_aua": 1599225407.0,
           "gold_aua": 1604943633.0,
           "gap_abs": -5718226.0,
           "gap_pct": -0.003563,
           "liability_types_excluded": {
             "CreditCard": {"count": N, "mv": 0.0},
             "Mortgage":   {"count": N, "mv": 0.0},
             "Loans":      {"count": N, "mv": 0.0},
             "Insurance":  {"count": N, "mv": 0.0},
             "TermLife":   {"count": N, "mv": 0.0},
             "Annuity":    {"count": N, "mv": 0.0}
           }
         }
         gap_abs = certified_aua - gold_aua
         gap_pct = gap_abs / gold_aua (negative means gold runs hot)
    </requirement>

    <requirement id="2">
      Non-blocking: if the script errors for any reason (missing columns,
      S3 error, parquet schema mismatch), log the error and exit 0.
      The pipeline must continue regardless. The publisher falls back to
      gold-derived totals when the certification JSON is absent.
    </requirement>

    <requirement id="3">
      Wire into the EC2 runner so that 05d runs after 05c and before the
      publisher Lambda is invoked. Confirm the sequence in run_gold.sh
      (or equivalent entrypoint). The script must be uploaded to S3 per
      the EC2 code deployment standard (repo -> S3 -> EC2 pulls).
    </requirement>

    <requirement id="4">
      No emojis in log output. Use plain ASCII prefixes: OK:, SKIP:, WARN:, ERROR:.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Script runs on EC2, silver parquet exists: gold/aua_certification/{today}.json
      appears in S3 with all required fields. certified_aua differs from gold_aua
      by the expected gap.
    </criterion>
    <criterion id="2">
      Script runs on EC2, silver parquet absent: exits 0, logs "SKIP:", no JSON written,
      pipeline continues.
    </criterion>
    <criterion id="3">
      Script errors: exits 0, logs "ERROR:", pipeline continues. No runner crash.
    </criterion>
    <criterion id="4">
      05d appears in the EC2 runner sequence after 05c and before publisher invocation.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Deploy via S3 artifact model — never write script directly on EC2.
    Repo -> S3 -> EC2 pulls. See EC2_CODE_DEPLOYMENT_STANDARD.md.</constraint>
    <constraint>No emojis in any output or log strings.</constraint>
    <constraint>This script is non-blocking. Exit 0 on all error paths.</constraint>
    <constraint>Do not modify 05c_validate_aua_vs_silver.py or any upstream scripts.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">05d_write_aua_certification.py written, uploaded to S3, wired in EC2 runner</deliverable>
    <deliverable type="verify">gold/aua_certification/{date}.json confirmed in S3 after next pipeline run</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_PSCFIX_PRD.md — Deliverable 2: Silver AUA Certification</ref>
  </references>
</task_order>
```
