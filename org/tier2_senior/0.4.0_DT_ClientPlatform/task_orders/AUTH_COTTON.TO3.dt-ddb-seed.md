<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>AUTH_COTTON.TO3</id>
    <project>AUTH_COTTON</project>
    <title>DDB seed — FIRM#cottonwood META + USER profile + partner row</title>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>30-60 min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/AUTH_COTTON.md</ref>
    <ref type="prd_section">§4.2 + §4.3 + §4.4 + §6 TO-3</ref>
    <ref type="gates">AUTH_COTTON.TO1 COMPLETE (opal-partner-cottonwood table must exist)</ref>
    <ref type="human_gate">Andrew password handoff — required before step 2</ref>
    <ref type="q1_assumption">domain = cottonwood.com</ref>
    <ref type="q2_assumption">mustChangePassword = false</ref>
    <ref type="q3_assumption">Scoped permissions = FIRM#cottonwood/META row in opal-users-v2</ref>
    <ref type="q5_assumption">Display name = "Cottonwood"</ref>
  </references>

  <context>
    Three DynamoDB put-item calls in order:
    1. opal-users-v2 FIRM#cottonwood / META (firm-level metadata)
    2. opal-users-v2 USER#user@cottonwood.com / PROFILE (master identity with bcrypt password)
    3. opal-partner-cottonwood email=user@cottonwood.com (partner identity, firmRole=user)

    All three with --condition-expression "attribute_not_exists(...)" to prevent overwrites.
    Step 2 gates on Andrew supplying the password out-of-band (bcrypt it locally; never
    commit plaintext to shell history or git).

    GATES: TO-1 must be complete (table exists). Andrew password must be received before step 2.
    Do NOT start this TO until COO confirms TO-1 RAVC received.
  </context>

  <scope>
    STEP 0 — PREREQUISITE CHECK:
    Verify opal-partner-cottonwood table exists:
      aws dynamodb describe-table --table-name opal-partner-cottonwood \
        --query "Table.TableStatus" --output text
    Must return ACTIVE. If not, STOP — TO-1 not complete.

    STEP 1 — Seed FIRM#cottonwood / META in opal-users-v2:
    aws dynamodb put-item \
      --table-name opal-users-v2 \
      --condition-expression "attribute_not_exists(PK)" \
      --item '{
        "PK": {"S": "FIRM#cottonwood"},
        "SK": {"S": "META"},
        "firmId": {"S": "cottonwood"},
        "name": {"S": "Cottonwood"},
        "domain": {"S": "cottonwood.com"},
        "tier": {"S": "advisor"},
        "status": {"S": "active"},
        "config": {"M": {}},
        "createdAt": {"S": "&lt;ISO8601 now&gt;"},
        "createdBy": {"S": "0.4.0_DT_ClientPlatform@opal.agent"}
      }'
    Note: No s3Bucket attribute (Cottonwood has no partner-scoped S3 bucket — intentional).

    STEP 2 — Seed USER#user@cottonwood.com / PROFILE (WAIT FOR ANDREW PASSWORD):
    Andrew provides password out-of-band. Bcrypt locally:
      python3 -c "import bcrypt; print(bcrypt.hashpw(b'&lt;PASSWORD&gt;', bcrypt.gensalt(12)).decode())"
    Then put-item:
    aws dynamodb put-item \
      --table-name opal-users-v2 \
      --condition-expression "attribute_not_exists(PK)" \
      --item '{
        "PK": {"S": "USER#user@cottonwood.com"},
        "SK": {"S": "PROFILE"},
        "email": {"S": "user@cottonwood.com"},
        "name": {"S": "Cottonwood User"},
        "firmId": {"S": "cottonwood"},
        "role": {"S": "user"},
        "tier": {"S": "advisor"},
        "passwordHash": {"S": "&lt;bcrypt_hash&gt;"},
        "password_hash": {"S": "&lt;bcrypt_hash&gt;"},
        "mustChangePassword": {"BOOL": false},
        "passwordChangedAt": {"S": "&lt;ISO8601 now&gt;"},
        "createdAt": {"S": "&lt;ISO8601 now&gt;"},
        "updatedAt": {"S": "&lt;ISO8601 now&gt;"},
        "createdBy": {"S": "0.4.0_DT_ClientPlatform"}
      }'
    CRITICAL: Confirm bcrypt hash starts with $2b$. Never write plaintext password to any file.

    STEP 3 — Seed opal-partner-cottonwood / email=user@cottonwood.com:
    aws dynamodb put-item \
      --table-name opal-partner-cottonwood \
      --condition-expression "attribute_not_exists(email)" \
      --item '{
        "email": {"S": "user@cottonwood.com"},
        "firmRole": {"S": "user"},
        "createdAt": {"S": "&lt;ISO8601 now&gt;"},
        "updatedAt": {"S": "&lt;ISO8601 now&gt;"},
        "createdBy": {"S": "0.4.0_DT_ClientPlatform"}
      }'
    Note: No advisorRole or advisorKey (Cottonwood has no ADVI access — intentional omission).
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before seed — prerequisite check">
      <step>
        <run>aws dynamodb describe-table --table-name opal-partner-cottonwood --query "Table.TableStatus" --output text</run>
        <expect>ACTIVE — TO-1 must be complete before proceeding.</expect>
        <if_mismatch>STOP. Do not seed before the table exists. Notify COO that TO-1 RAVC
        is needed before TO-3 can fire.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after all three put-items">
      <step>
        <run>aws dynamodb get-item --table-name opal-users-v2 --key '{"PK":{"S":"FIRM#cottonwood"},"SK":{"S":"META"}}' --output json</run>
        <expect>Item present with firmId=cottonwood, name=Cottonwood, domain=cottonwood.com,
        tier=advisor, status=active, config={}. No s3Bucket. No advisorRole. createdBy present.</expect>
        <if_mismatch>STOP. Row missing or malformed. Check put-item error output.</if_mismatch>
      </step>
      <step>
        <run>aws dynamodb get-item --table-name opal-users-v2 --key '{"PK":{"S":"USER#user@cottonwood.com"},"SK":{"S":"PROFILE"}}' --output json</run>
        <expect>Item present. passwordHash starts with $2b$ (bcrypt). mustChangePassword=false.
        firmId=cottonwood. role=user. tier=advisor.</expect>
        <if_mismatch>STOP. Row missing or plaintext password visible — do not proceed.
        Report to COO.</if_mismatch>
      </step>
      <step>
        <run>aws dynamodb get-item --table-name opal-partner-cottonwood --key '{"email":{"S":"user@cottonwood.com"}}' --output json</run>
        <expect>Item present. firmRole=user. No advisorRole attribute. No advisorKey attribute.</expect>
        <if_mismatch>STOP. Row missing. Verify table is ACTIVE and put-item succeeded.</if_mismatch>
      </step>
      <step>
        <run>aws dynamodb scan --table-name opal-partner-cottonwood --select COUNT --output json | python3 -c "import sys,json; d=json.load(sys.stdin); print('COUNT=', d['Count'])"</run>
        <expect>COUNT= 1</expect>
        <if_mismatch>More than 1 item — unexpected. Investigate before RAVC.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="N/A — operational seed only">
      <step>
        <run>N/A — DDB seeding is operational; no comp-* tool applies. No git commit for DDB rows.</run>
        <expect>Absence acknowledged.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      FIRM#cottonwood META row: get-item returns all documented attributes including
      firmId, name, domain, tier, status, config. No s3Bucket. Evidence: get-item JSON in log.
    </criterion>
    <criterion id="2">
      USER#user@cottonwood.com PROFILE row: get-item returns item. passwordHash starts with
      $2b$ (bcrypt 12 rounds). mustChangePassword=false. No plaintext password anywhere in
      log or git. Evidence: get-item JSON excerpt (hash truncated OK) in log.
    </criterion>
    <criterion id="3">
      opal-partner-cottonwood email=user@cottonwood.com row: get-item returns firmRole=user,
      no advisorRole, no advisorKey. Evidence: get-item JSON in log.
    </criterion>
    <criterion id="4">
      opal-partner-cottonwood scan COUNT=1 (exactly one partner row). Evidence: scan output.
    </criterion>
    <criterion id="5">
      Short DT session log entry (no commit needed) citing the three put-item invocations,
      verification commands, and outcomes. Log must NOT include plaintext password.
    </criterion>
    <criterion id="6">
      RAVC to 2.0.0_SA_COO: all three get-item confirmations + scan COUNT + explicit signal
      that TO-4 (smoke test) is now unblocked infrastructure-side.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="AUTH_COTTON.TO1" status="REQUIRED">
      opal-partner-cottonwood table must be ACTIVE before step 3 put-item.
      COO will relay GO to DT when TO-1 RAVC received.
    </dependency>
    <dependency agent="Andrew" task="password-handoff" status="REQUIRED">
      Andrew must supply the Cottonwood user password before step 2.
      COO will relay to DT when received.
    </dependency>
  </dependencies>

  <cross_domain_coordination>
    <none/>
    opal-users-v2 puts are PK/SK scoped to new keys — no collision possible.
    opal-partner-cottonwood is a new table — no existing rows to conflict.
  </cross_domain_coordination>

  <commit_identity>
    No git commit for DDB operational seed. Session log only.
    DT session log: org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-04-29/auth_cotton_to3_ddb_seed.md
  </commit_identity>

  <notes>
    DO NOT commit password hash to git. DDB operational seeds are not committed.
    If condition-expression fails (item already exists), do NOT overwrite silently —
    report to COO before any --condition-expression removal.
    Andrew assumptions (Q1/Q2/Q5): domain=cottonwood.com, mustChangePassword=false,
    name=Cottonwood. If Andrew corrects any of these, amend the put-item JSON accordingly.
    RAVC4 to COO after all 3 items verified. COO will then authorize TO-4 (smoke test).
  </notes>
</task_order>
