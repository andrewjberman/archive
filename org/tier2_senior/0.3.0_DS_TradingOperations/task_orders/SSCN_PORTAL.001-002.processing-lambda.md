# Task Order: SSCN — Processing Lambda (Python)

```xml
<task_order>
  <metadata>
    <id>0.3.0_DE_TradingOperations-2026-03-05-sscn-processing-lambda</id>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.3.0_DS_TradingOperations</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <thread_serial>SSCN_PORTAL-001</thread_serial>
    <thread_ref>org/tier2_senior/0.3.0_DS_TradingOperations/threads/SSCN_PORTAL-001-pattern-0-security-scanner-data-architec_0.3.0_DE_TradingOperations+0.5.0_AE_OpalETL.md</thread_ref>
  </metadata>

  <objective>
    Write the Python source for the SSCN processing Lambda. This Lambda is triggered by an S3
    ObjectCreated event when the monthly FactSet Excel is uploaded, reads the file, computes
    per-factor percentiles using the V0 canonical logic, and writes static JSON artifacts to
    opal-data-portal-v2 for each of the 6 universes plus the shared factor metadata.
    All decisions were locked in SSCN_PORTAL-001. This task order is implementation only.
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/opal_security_scanner_processor/lambda_function.py</file>
      <file action="create">infra/aws/lambda/opal_security_scanner_processor/requirements.txt</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      SOURCE REFERENCE (read before writing):
      - docs/architecture/SSCN_DATA_CONTRACT.md (authoritative contract; all field names, null
        semantics, S3 key structure, and compute split are here)
      - docs/architecture/security-scanner-source/source_headers_20251028.json (confirmed column
        names from actual Excel header row 4)
      - V0 script (available in thread context): quick_update_weights.py --
        calculate_percentiles_with_sign() is the canonical percentile logic to mirror

      Key finding from header snapshot: actual export has 284 scoring factor columns, NOT 255
      as PRD states. Lambda must iterate dynamically over present columns, not a fixed list.
    </requirement>
    <requirement id="2">
      LAMBDA ENTRY POINT (lambda_handler):
      Triggered by S3 ObjectCreated event. Extract bucket + key from event record.
      Key pattern: security_scanner/uploads/{asOf}/Screening_DIVZ_IDVZ_{asOf}.xlsx
      Extract asOf from the key path (do not parse from filename; parse from the path segment).
      Read the Excel from S3 into a bytes buffer and load with pd.read_excel(buffer, header=4).
    </requirement>
    <requirement id="3">
      FACTOR METADATA OUTPUT (factor_metadata.json):
      Source: XLSM Tab 3 "3-Factor Data". This is static (not regenerated monthly from the
      FactSet Excel — the FactSet Excel is the data file, not the factor registry).

      For Phase 0, DS should produce this JSON from the XLSM audit artifacts already available
      in docs/architecture/security-scanner-source/. If a machine-readable factor registry
      does not yet exist there, create it as a checked-in JSON file:
        docs/architecture/security-scanner-source/factor_metadata_registry.json
      and have the Lambda read it from S3 (copied there as a deployment artifact) or inline it
      as a package constant if small enough.

      Output key (both paths):
        json/security_scanner/{asOf}/factor_metadata.json
        json/security_scanner/latest/factor_metadata.json

      Shape per SSCN_DATA_CONTRACT.md Section 4, Endpoint 1:
        {
          "asOf": "YYYY-MM-DD",
          "factors": [
            {
              "code": string,
              "name": string,
              "category": string,
              "relationship": "Positive" | "Inverse",
              "ic": number,
              "coveragePct": number,
              "autocorrelationPct": number,
              "assetClass": string,
              "systematic": "Yes" | "No"
            }
          ]
        }
    </requirement>
    <requirement id="4">
      UNIVERSE PROCESSING (universe_data.json + scanner_data.json):
      For each universe in UNIVERSE_OPTIONS:
        sp500 / wt_ivv, r1000 / wt_iwb, r1000v / wt_iwd,
        acwx / wt_acwx, eafe / wt_efa, eafev / wt_efv

      1. Filter: df_universe = df[df[universe_col] > 0].copy()
      2. Identify scoring factor columns: all columns present in df.columns that are NOT in
         the identity, universe, or admin column sets (use source_headers_20251028.json as
         the reference for non-scoring columns to exclude).
      3. For scanner_data: compute percentiles per factor:
           factor_values = pd.to_numeric(df_universe[code], errors='coerce')
           if relationship == 'Inverse': factor_values = -factor_values
           percentiles = factor_values.rank(pct=True, method='average') * 100
         Relationship mapping comes from factor_metadata_registry.json.
         Emit pctls[code] = null where factor_values is NaN.
      4. Build output rows per SSCN_DATA_CONTRACT.md Section 5 interfaces:
         universe_data.json row: ticker, name, mktVal, country, sector, industryGroup,
           universeWeight, values (Record[code, number|null])
         scanner_data.json row: same identity fields, values, pctls (Record[code, number|null])
      5. Identity field mapping (V0 anchors from source_headers_20251028.json):
           ticker         <- 'ticker'
           name           <- 'factset_entity_proper_name' if present, else 'name'
           mktVal         <- 'mkt_val'
           country        <- 'country_name'
           sector         <- 'sector_name'
           industryGroup  <- 'indgrp_name'
           universeWeight <- df[universe_col]
      6. Write JSON to S3 for both {asOf}/ and latest/ paths.
    </requirement>
    <requirement id="5">
      NULL SEMANTICS (per SSCN_DATA_CONTRACT.md Section 7):
      - Missing raw value: emit null in values[code] (not 0, not omit)
      - Missing percentile: emit null in pctls[code]
      - Python NaN must be serialized as JSON null (use default=lambda x: None if isinstance(x, float) and math.isnan(x) in json.dumps, or use pandas .where(pd.notna(x), None) before building the dict)
      Do NOT emit NaN into the JSON payload — browsers cannot parse NaN as JSON.
    </requirement>
    <requirement id="6">
      S3 OUTPUT (per SSCN_DATA_CONTRACT.md Section 3):
      Bucket: opal-data-portal-v2
      For each universe, write:
        json/security_scanner/{asOf}/factor_metadata.json          (once, not per universe)
        json/security_scanner/{asOf}/universes/{uId}/universe_data.json
        json/security_scanner/{asOf}/universes/{uId}/scanner_data.json
        json/security_scanner/latest/factor_metadata.json          (overwrite)
        json/security_scanner/latest/universes/{uId}/universe_data.json  (overwrite)
        json/security_scanner/latest/universes/{uId}/scanner_data.json   (overwrite)
      Where uId is the portal-friendly ID (sp500, r1000, r1000v, acwx, eafe, eafev).
      Content-Type: application/json. No Content-Encoding (Phase 0 = no gzip).
    </requirement>
    <requirement id="7">
      REQUIREMENTS FILE:
      infra/aws/lambda/opal_security_scanner_processor/requirements.txt must list:
        pandas
        openpyxl
      (numpy if needed; boto3 is provided by the Lambda runtime and must NOT be listed)
      This file is what AE uses to build the security-scanner-deps Lambda Layer.
    </requirement>
    <requirement id="8">
      ERROR HANDLING:
      - If the uploaded key does not match the expected pattern, log and raise immediately.
      - If a universe column is not found in df.columns, skip that universe and log a warning
        (do not fail the entire run).
      - If factor_metadata_registry.json is missing or malformed, fail fast and raise.
      No emojis in log output (CloudWatch log constraint per CLAUDE.md).
      Use plain ASCII prefixes: INFO:, WARN:, ERROR:
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">lambda_function.py exists at infra/aws/lambda/opal_security_scanner_processor/lambda_function.py.</criterion>
    <criterion id="2">requirements.txt lists pandas and openpyxl (no boto3).</criterion>
    <criterion id="3">percentile logic mirrors calculate_percentiles_with_sign(): coerce numeric, negate Inverse factors, rank(pct=True, method='average') * 100.</criterion>
    <criterion id="4">NaN is serialized as JSON null (not Python NaN or "NaN" string).</criterion>
    <criterion id="5">Both {asOf}/ and latest/ S3 keys are written per the contract.</criterion>
    <criterion id="6">All 284 factor columns are iterated dynamically (no hardcoded list of 255 or any fixed count).</criterion>
    <criterion id="7">universe_data.json and scanner_data.json shapes match SSCN_DATA_CONTRACT.md Section 5 interfaces exactly (camelCase JSON keys).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT use aws lambda update-function-code or any direct deployment method. Source code only — AE deploys via Terraform (SSCN_PORTAL.001-002.terraform-infra.md).</constraint>
    <constraint>Do NOT write code directly on EC2 or in the AWS console. All code lives in this repo.</constraint>
    <constraint>camelCase for all JSON output field names (mktVal, coveragePct, industryGroup, etc.) — this was DE's convention established in SSCN_PORTAL-001 turn 3. Do not use snake_case in JSON output.</constraint>
    <constraint>Do not hardcode the factor count as 255. Use 284 (actual) or iterate dynamically.</constraint>
    <constraint>No emojis anywhere in the source file (CloudWatch log constraint).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.5.0_AE_OpalETL" task="SSCN_PORTAL.001-002.terraform-infra.md" status="pending">
      AE deploys this Lambda via Terraform after DS delivers the source code.
      DS signals completion by committing the source file and updating this task order status to complete.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">infra/aws/lambda/opal_security_scanner_processor/lambda_function.py committed to CLOUD branch</deliverable>
    <deliverable type="commit">infra/aws/lambda/opal_security_scanner_processor/requirements.txt committed to CLOUD branch</deliverable>
    <deliverable type="log">Session log at org/tier2_senior/0.3.0_DS_TradingOperations/logs/2026-03-05/ (or next session date)</deliverable>
  </deliverables>
</task_order>
```
