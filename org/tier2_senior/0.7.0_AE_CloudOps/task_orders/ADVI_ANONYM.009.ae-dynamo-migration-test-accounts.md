<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADVI_ANONYM-009-ae-dynamo</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-01</date>
    <status>pending</status>
    <priority>high</priority>
    <type>infrastructure</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Three DynamoDB operations on opal-users-v2: (1) batch update 12 opal-capital users
    from tier:internal to tier:advisor, (2) create FIRM#mockadv record, (3) create 3
    new test user accounts. Can run in parallel with DS .007 code changes.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_ANONYM_P3_PRD.md -- §4 MockADV Firm, §5 Test Accounts</ref>
    <ref type="table">DynamoDB: opal-users-v2 (us-east-1)</ref>
  </references>

  <requirements>

    <requirement id="1">
      TIER MIGRATION: Batch update all opal-capital users from tier:'internal' to tier:'advisor'.

      First, scan to find all affected users:
      ```bash
      aws dynamodb scan \
        --table-name opal-users-v2 \
        --filter-expression "firmId = :fid" \
        --expression-attribute-values '{":fid":{"S":"opal-capital"}}' \
        --projection-expression "PK,SK,tier,email" \
        --output json
      ```

      For each user record with tier='internal', update to tier='advisor':
      ```bash
      aws dynamodb update-item \
        --table-name opal-users-v2 \
        --key '{"PK":{"S":"USER#{pk}"},"SK":{"S":"PROFILE"}}' \
        --update-expression "SET tier = :t" \
        --expression-attribute-values '{":t":{"S":"advisor"}}'
      ```

      Log the count and email of each user updated. Expected: ~12 users.
      Verify: re-scan after update -- no records should show tier='internal'.
    </requirement>

    <requirement id="2">
      CREATE FIRM#mockadv:
      ```bash
      aws dynamodb put-item \
        --table-name opal-users-v2 \
        --item '{
          "PK":         {"S":"FIRM#mockadv"},
          "SK":         {"S":"META"},
          "firmId":     {"S":"mockadv"},
          "name":       {"S":"MockADV"},
          "tier":       {"S":"advisor"},
          "s3Bucket":   {"S":"opal-data-bd"},
          "domain":     {"S":"mockadv.test"},
          "status":     {"S":"active"},
          "config":     {"M":{}},
          "createdAt":  {"S":"2026-04-01T00:00:00Z"},
          "createdBy":  {"S":"andrew@opalinvest.com"}
        }'
      ```
      Note: `parentFirmId` is omitted (null equivalent in DynamoDB).
      Verify: `aws dynamodb get-item --table-name opal-users-v2 --key '{"PK":{"S":"FIRM#mockadv"},"SK":{"S":"META"}}'`
    </requirement>

    <requirement id="3">
      CREATE 3 TEST USER ACCOUNTS.

      You must first determine the correct PK format for user records by reading an
      existing user: `aws dynamodb get-item --table-name opal-users-v2 --key '{"PK":{"S":"USER#andrew@opalinvest.com"},"SK":{"S":"PROFILE"}}'`
      (or scan for a known user to confirm the PK pattern).

      Account 1 -- Opal User (non-admin internal):
      ```json
      {
        "PK": "USER#user@opalinvest.com",
        "SK": "PROFILE",
        "email": "user@opalinvest.com",
        "name": "Opal User",
        "tier": "advisor",
        "role": "user",
        "firmId": "opal-capital",
        "status": "active"
      }
      ```

      Account 2 -- Travis Penfield (49F admin):
      ```json
      {
        "PK": "USER#travis.penfield@49financial.com",
        "SK": "PROFILE",
        "email": "travis.penfield@49financial.com",
        "name": "Travis Penfield",
        "tier": "advisor",
        "role": "admin",
        "firmId": "49financial",
        "status": "active"
      }
      ```

      Account 3 -- Chase Bertrand (49F user, book scoping):
      ```json
      {
        "PK": "USER#chase.bertrand@49financial.com",
        "SK": "PROFILE",
        "email": "chase.bertrand@49financial.com",
        "name": "Chase Bertrand",
        "tier": "advisor",
        "role": "user",
        "firmId": "49financial",
        "advisorId": "Chase Bertrand",
        "status": "active"
      }
      ```

      IMPORTANT: `advisorId: "Chase Bertrand"` must match exactly the `architect` field
      value in the gold data (case-sensitive). Confirm the architect name string used in
      gold data before writing -- if it differs, flag in session log.

      Verify each account: get-item to confirm the record exists with correct fields.
    </requirement>

    <requirement id="4">
      VERIFY test account auth flow (optional but recommended):
      - Check that andrew@opalinvest.com still has tier=advisor (unchanged by migration).
      - Confirm FIRM#mockadv is visible in the firm list query used by the portal.
    </requirement>

    <requirement id="5">
      Write session log:
      org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-01/advi_anonym_p3_dynamo_migration.md

      Include: count of users migrated, MockADV firm created, 3 test accounts created,
      Chase Bertrand advisorId value confirmed against gold data.
    </requirement>

    <requirement id="6">
      Message COO (2.0.0_SA_COO) when done with:
      - Count of opal-capital users migrated
      - Chase Bertrand advisorId value (confirm exact string from gold data)
      - Any anomalies
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">All opal-capital users have tier=advisor (0 users with tier=internal remaining).</criterion>
    <criterion id="2">FIRM#mockadv record exists in opal-users-v2 with s3Bucket=opal-data-bd.</criterion>
    <criterion id="3">3 test accounts created with correct tier/role/firmId/advisorId fields.</criterion>
    <criterion id="4">Chase Bertrand advisorId matches architect field in gold data.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>DO NOT update andrew@opalinvest.com -- his record may already have tier=advisor or a different structure. Scan confirms; skip if already correct.</constraint>
    <constraint>MockADV s3Bucket MUST be opal-data-bd (not a new bucket). No data copy needed.</constraint>
    <constraint>This migration is safe at any time relative to the Lambda deploy (firmId=opal-capital is unchanged). No downtime window needed.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ANONYM.007" status="pending">
      AE can run in parallel with DS. DynamoDB migration is safe regardless of Lambda deploy order.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="data">DynamoDB: 12 users migrated, MockADV firm created, 3 test accounts</deliverable>
    <deliverable type="message">COO completion message with migration count + Chase advisorId confirmed</deliverable>
  </deliverables>
</task_order>
