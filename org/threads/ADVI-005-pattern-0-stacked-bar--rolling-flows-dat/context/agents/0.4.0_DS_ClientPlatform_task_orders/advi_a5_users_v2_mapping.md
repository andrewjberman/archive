# Task Order: Stream A5 — opal-users-v2 Advisor Identity Investigation

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-advi-a5-users-v2-mapping</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Investigate the opal-users-v2 DynamoDB table schema and determine whether a mapping
    from JWT user identity to advisor identity in the gold layer currently exists.
    This is the linchpin for Books tab access gating — an advisor landing on their own
    book requires resolving JWT userId to the correct architect name in the gold data.
    Start this in your first activation session — no thread dependency.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
  </references>

  <requirements>
    <requirement id="A5.1">
      Investigate the opal-users-v2 DynamoDB table (read-only — do not write):
        - What is the partition key and sort key structure?
        - What fields identify an advisor? (userId, email, advisorId, firmId, etc.)
        - Does any field directly match a key used in the gold layer
          (accounts_dimension_latest.architect or rel_architect_lookup.parquet)?
      Use AWS CLI or boto3 describe-table + scan/query to inspect schema and sample records.
    </requirement>
    <requirement id="A5.2">
      Determine which of the three mapping scenarios applies:
        (a) Direct field match — a field in opal-users-v2 directly maps to
            accounts_dimension_latest.architect or rel_architect_lookup.parquet key.
            Name the field pair.
        (b) Email-based lookup — JWT email claim can be cross-referenced against
            an email field in the gold layer. Name both fields.
        (c) No existing mapping — no field in opal-users-v2 currently connects to
            the gold layer's advisor identifier. New data registration step required.
    </requirement>
    <requirement id="A5.3">
      Document your findings in your session log:
        - Table schema (PK/SK, key attributes)
        - Scenario determination (a), (b), or (c)
        - If (a) or (b): name the specific field pair and confirm with a sample value
        - If (c): flag as a BLOCKER to COO and CTO before any Books auth work proceeds.
          The Books tab advisor identity resolution cannot be implemented until this gap
          is closed. Provide a recommendation for how the mapping should be established
          (e.g., admin registration step, email normalization approach).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">opal-users-v2 schema documented in session log: PK/SK and key identity fields named.</criterion>
    <criterion id="2">Mapping scenario (a), (b), or (c) determined and documented with specific field names or blocker flag.</criterion>
    <criterion id="3">If (c): COO and CTO notified via session log next steps before any auth implementation proceeds.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read-only investigation — do not write to opal-users-v2 or any DynamoDB table.</constraint>
    <constraint>Do not assume the mapping exists. Confirm with actual table contents before concluding (a) or (b).</constraint>
    <constraint>Do NOT use emojis in any script, query, or log output. Plain ASCII only.</constraint>
    <constraint>Commit session log with: git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">Session log with opal-users-v2 schema and mapping scenario finding</deliverable>
  </deliverables>
</task_order>
```
