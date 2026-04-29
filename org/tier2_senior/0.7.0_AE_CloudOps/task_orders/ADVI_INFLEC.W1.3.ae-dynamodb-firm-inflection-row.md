<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w1.3-firm-row</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- Verified 2026-04-29: FIRM#inflection row exists in opal-users-v2 with SK=META (not METADATA per existing precedent), s3Bucket=opal-data-inf, written 2026-04-21 by 0.7.0_AE_CloudOps. -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Insert `PK=FIRM#inflection, SK=METADATA` row in `opal-users-v2` DynamoDB, wiring the firmId → s3Bucket lookup that `opal-partners-data` Lambda uses at request time. This is the single data-plane write that activates Inflection data serving through the existing multi-tenant serving layer — zero Lambda code changes required (PRD §3.1).
  </objective>

  <context>
    ADVI_INFLEC PRD v1.2 §3.2 + §4.2 row 8. Existing precedent: `FIRM#mockadv → s3Bucket=opal-data-bd`. Inflection row mirrors that shape:

    ```
    PK: FIRM#inflection
    SK: METADATA
    s3Bucket: opal-data-inf
    firmName: Inflection Wealth Management
    firmTier: primary
    allowedDimensions: [<TBD; default match 49F list>]
    ```

    Depends on W1.1 (bucket `opal-data-inf` exists). Should precede or be concurrent with W1.4 (partner-inflection table) + W1.6/W1.7 (FIRM_BUCKET_MAP edge updates). Row is data-only; no Lambda code change.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>aws dynamodb get-item --table-name opal-users-v2 --key '{"PK":{"S":"FIRM#49financial"},"SK":{"S":"METADATA"}}'</run>
    <expect>Existing 49F FIRM row — copy schema structure. Attributes: s3Bucket, firmName, firmTier, allowedDimensions (if present).</expect>
    <if_mismatch>Row missing means 49F was provisioned differently; fall back to FIRM#mockadv pattern (§3.2).</if_mismatch>

    <run>aws dynamodb get-item --table-name opal-users-v2 --key '{"PK":{"S":"FIRM#mockadv"},"SK":{"S":"METADATA"}}'</run>
    <expect>Existing mockadv FIRM row — attribute template.</expect>

    Phase 2 (during implementation):
    <run>aws dynamodb put-item --table-name opal-users-v2 --item file://.tmp.json --condition-expression "attribute_not_exists(PK)"</run>
    <expect>Write succeeds; ConditionCheck passes (row not yet present).</expect>
    <if_mismatch>If ConditionCheck fails, a FIRM#inflection row already exists — diff current attrs vs target and update-item instead of put-item.</if_mismatch>

    Phase 3 (after write):
    <run>aws dynamodb get-item --table-name opal-users-v2 --key '{"PK":{"S":"FIRM#inflection"},"SK":{"S":"METADATA"}}'</run>
    <expect>Row returns with s3Bucket=opal-data-inf, firmName=Inflection Wealth Management, all expected attrs.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `opal-users-v2` DynamoDB. Only new row write; no schema change; no cross-agent contention.
    last_write_owner: 0.7.0_AE_CloudOps.
    required_action: "W1.1 (bucket exists) must complete first. Otherwise a race exists where opal-partners-data resolves firmId=inflection → s3Bucket=opal-data-inf → bucket doesn't exist → 500."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Row `PK=FIRM#inflection, SK=METADATA` exists with s3Bucket=opal-data-inf, firmName=Inflection Wealth Management.
    2. Row matches 49F FIRM row's attribute shape.
    3. `aws dynamodb scan opal-users-v2 --filter-expression "begins_with(PK, :p)" --expression-attribute-values '{":p":{"S":"FIRM#"}}' --query 'Items[*].PK.S'` returns {FIRM#49financial, FIRM#inflection, FIRM#mockadv, FIRM#opal-capital} (or superset).
    4. Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-{NN}/advi_inflec_w1_3_firm_row.md` with put-item cmd, get-item verify, and 49F/mockadv reference rows for audit.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="reference">infra/aws/users/ONBOARDING.md (runbook guide)</file>
      <file action="modify">DynamoDB opal-users-v2 (data-only write)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Mirror 49F FIRM row attribute shape exactly. Deviation without justification is a QA failure.</requirement>
    <requirement id="2">Use `--condition-expression "attribute_not_exists(PK)"` — do not blind-overwrite.</requirement>
    <requirement id="3">No schema change on opal-users-v2 — row add only.</requirement>
    <requirement id="4">Do NOT provision any user rows in this TO — user rows ship in W5.5.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with put-item + get-item output.</deliverable>
    <deliverable type="commit">(Optional) if captured as Terraform `aws_dynamodb_table_item` resource in shared-infra workspace; otherwise data-only and tracked in session log only.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT skip the condition-expression.</rule>
    <rule>Do NOT write any USER# rows in this TO — those are W5.5.</rule>
    <rule>Do NOT invent attribute names — mirror 49F FIRM row.</rule>
  </do_not>
</task_order>
