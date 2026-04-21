<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.5-user-provisioning</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Provision the first Inflection portal users per `infra/aws/users/ONBOARDING.md §2` runbook. Two writes per user: (1) `opal-users-v2 USER#email` row with `firmId=inflection`, (2) `opal-partner-inflection` row with advisorKey + advisorRole + firmRole. At minimum: one user with `firmRole=admin` for BooksTab + leaderboard drill access.
  </objective>

  <context>
    PRD §9 W5.5 + ONBOARDING.md §2. Blocked on W1.4 (opal-partner-inflection table exists) + W1.5 (auth-handler can resolve the table). User list: Andrew to provide actual Inflection user emails + names + advisorKeys (matching Inflection advisor slugs in gold layer). If no real Inflection users yet, provision a test user for smoke testing only — clearly labeled as test.

    PRD §10 Q13 (domain gating: auto-allow @inflectionwealthmgmt.com vs explicit provisioning) is OPEN. Use explicit provisioning now (conservative); domain auto-allow can be added later if Andrew resolves Q13.
  </context>

  <compiler_tools_mandate>
    Phase 3:
    <run>aws dynamodb get-item --table-name opal-partner-inflection --key '{"email":{"S":"$EMAIL"}}'</run>
    <expect>Row returns with advisorKey, advisorRole, firmRole populated.</expect>
    <run>aws dynamodb get-item --table-name opal-users-v2 --key '{"PK":{"S":"USER#$EMAIL"},"SK":{"S":"PROFILE"}}'</run>
    <expect>Row returns with firmId=inflection, role=user.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W1.4 (table) + W1.5 (auth-handler generalization). Check both before starting."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. At least one opal-users-v2 USER row with firmId=inflection.
    2. Corresponding opal-partner-inflection row with advisorKey matching an I_D00c leaderboard advisorKey.
    3. At least one user has firmRole=admin.
    4. `--condition-expression "attribute_not_exists(PK)"` used on all writes.
    5. Session log with get-item verify output.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">DynamoDB opal-users-v2 (data write)</file>
      <file action="modify">DynamoDB opal-partner-inflection (data write)</file>
      <file action="reference">infra/aws/users/ONBOARDING.md §2</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">ONBOARDING.md §2 two-write order: opal-users-v2 first, then opal-partner-inflection.</requirement>
    <requirement id="2">role=user always (R2 — never admin in master table).</requirement>
    <requirement id="3">advisorKey must snake_case-match gold layer slug from I_D00c leaderboard output.</requirement>
    <requirement id="4">Blocked on W1.4 + W1.5.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with put-item + get-item output.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT set role=admin in opal-users-v2 (R2). firmRole=admin in opal-partner-inflection is fine.</rule>
    <rule>Do NOT guess advisorKey — confirm from I_D00c output or Andrew.</rule>
    <rule>Do NOT skip condition-expression.</rule>
  </do_not>
</task_order>
