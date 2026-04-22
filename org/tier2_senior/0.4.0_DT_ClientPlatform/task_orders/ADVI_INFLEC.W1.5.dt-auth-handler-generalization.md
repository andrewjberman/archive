<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w1.5-auth-handler</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <co_owner>0.7.0_AE_CloudOps</co_owner>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Generalize `opalinvest-auth-handler` Lambda's `getPartnerIdentity()` so it derives the partner table name from the caller's `firmId` (`opal-partner-${firmId}`), eliminating the hardcoded `PARTNER_TABLE_49FIN` constant in `db.ts`. Also update the auth-handler IAM policy to grant `dynamodb:GetItem` on `arn:aws:dynamodb:*:*:table/opal-partner-*` (wildcard, validated against §4.2 row 2). Build + deploy via standard Lambda protocol. Regression-guarded by W5.9 (49F users still work end-to-end after deploy).
  </objective>

  <context>
    ADVI_INFLEC PRD v1.2 §4.2 row 2 + ONBOARDING.md §5 Step 3. Current code hardcodes `PARTNER_TABLE_49FIN = "opal-partner-49financial"` in `infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts`. `getPartnerIdentity(email, firmId)` currently ignores `firmId` and hits the 49F table. After generalization, any user whose firmId maps to an existing `opal-partner-{firmId}` table Just Works — no per-partner code changes for future firms.

    **Two-partner constraint at go-live:** Inflection is the second partner. Approach "generalize now" is per CTO recommendation in PRD §4.2 (explicit "Recommendation: generalize now"). Adding a switch statement per partner is a banned anti-pattern.

    **IAM scoping decision:** PRD flags "wildcard opal-partner-* OR explicit opal-partner-inflection". Wildcard is mandated — every future partner onboarding becomes a one-TO data-plane write without iam.tf edits. If AE prefers explicit listing for security, escalate to CTO before deviating.

    **Critical prerequisite:** W1.4 table MUST exist before deploy. Otherwise the deploy succeeds but Inflection login silently 500s on missing-table. Sequence enforced by cross_domain_coordination.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>cat infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts | grep -n "PARTNER_TABLE_49FIN\|getPartnerIdentity\|opal-partner"</run>
    <expect>Hardcoded constant at top of file. `getPartnerIdentity(email, firmId)` signature — confirm firmId is already a parameter even if currently unused.</expect>
    <if_mismatch>If `firmId` is not already a parameter, refactor call sites as part of this TO. Flag in session log.</if_mismatch>

    <run>cat infra/aws/terraform/portal-auth/iam.tf | grep -A 10 -B 2 "opal-partner"</run>
    <expect>Existing policy with arn:aws:dynamodb:*:*:table/opal-partner-49financial (or opal-partner-*). Confirm current scope.</expect>

    <run>comp-iam service opalinvest-auth-handler</run>
    <expect>No MISSING permissions currently. After iam.tf change, re-run — expect MISSING count unchanged or improved (wildcard broader).</expect>

    <run>aws dynamodb describe-table --table-name opal-partner-inflection</run>
    <expect>ACTIVE status (W1.4 prerequisite satisfied). If ERROR ResourceNotFoundException, W1.4 has not shipped — BLOCK.</expect>

    Phase 2 (during implementation):
    <run>grep -rn "PARTNER_TABLE_49FIN\|opal-partner-49financial" infra/aws/opalinvest_dev/lambda/auth-handler/src/</run>
    <expect>Only db.ts hits. All removed after edit.</expect>

    <run>bash infra/aws/lambda/ci/build-nodejs-lambda.sh portal-auth opalinvest-auth-handler</run>
    <expect>Build succeeds; auth-handler.zip uploaded to s3://opal-313476888478-lambda-artifacts/portal-auth/auth-handler.zip (path per build-and-upload convention). SHA logged.</expect>

    <run>.tools/terraform.exe plan (from portal-auth/)</run>
    <expect>1 iam_policy change (wildcard grant) + 1 lambda_function code hash update; nothing else.</expect>

    Phase 3 (after deploy):
    <run>comp-iam service opalinvest-auth-handler</run>
    <expect>No MISSING permissions; wildcard in effect.</expect>

    <run>comp-iam gaps</run>
    <expect>No regressions elsewhere.</expect>

    Integration test (both partners):
    1. 49F user login → auth-handler reads opal-partner-49financial → JWT carries correct advisor claims. `curl` smoke or Cognito invoke.
    2. Inflection user login (if test row provisioned) → auth-handler reads opal-partner-inflection → JWT carries correct claims.
    3. User with firmId=opal-capital (internal) → auth-handler bypasses partner table lookup (per ONBOARDING.md §2 Step 1 note). No table lookup attempted.

    <run>comp-blast opalinvest-auth-handler</run>
    <expect>Blast radius unchanged vs Phase 1.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `opalinvest-auth-handler` Lambda (portal-auth Terraform workspace).
    also_in_to: W1.4 (opal-partner-inflection table creation — MUST precede deploy).
    last_write_owner: 0.4.0_DT_ClientPlatform on code; 0.7.0_AE_CloudOps on iam.tf + TF apply.
    required_action: "HARD SEQUENCE: W1.4 apply → W1.5 code edit → W1.5 iam.tf edit → build + deploy → test 49F regression (W5.9 kickoff). If W1.5 deploys before W1.4, Inflection login fails silently (ResourceNotFoundException caught as generic 500). 49F never regresses because `opal-partner-49financial` always exists — but test to confirm."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `PARTNER_TABLE_49FIN` constant removed from `db.ts`.
    2. `getPartnerIdentity(email, firmId)` resolves table name as `opal-partner-${firmId}`.
    3. `portal-auth/iam.tf` grants `dynamodb:GetItem` on `arn:aws:dynamodb:*:*:table/opal-partner-*`.
    4. `comp-iam service opalinvest-auth-handler` shows no MISSING permissions post-deploy.
    5. 49F user login integration test: JWT carries correct advisorKey + advisorRole + firmRole. No regression.
    6. Internal user (firmId=opal-capital) login: no partner-table read attempted (log confirms). No regression.
    7. Inflection user login (if at least one row provisioned in opal-partner-inflection): JWT carries correct claims. If no row yet, this test deferred to W5.6 and documented.
    8. Tag `portal-auth-v{next}` pushed per CLAUDE.md Rule 6 (`git tag -l "portal-auth-v*" | sort -V | tail -5` for increment).
    9. Source map `infra/aws/lambda/ci/lambda-source-map.json` updated.
    10. Session log at `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-04-{NN}/advi_inflec_w1_5_auth_handler.md` with code diff, iam.tf diff, build SHA, deploy tag, integration test output, comp-iam runs.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts</file>
      <file action="modify">infra/aws/terraform/portal-auth/iam.tf</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="reference">infra/aws/users/ONBOARDING.md §5 Step 3</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">BLOCK on W1.4: `aws dynamodb describe-table --table-name opal-partner-inflection` must return ACTIVE before deploy. Log pre-check in session log.</requirement>
    <requirement id="2">IAM scope = wildcard `opal-partner-*` — not per-partner listing. If AE prefers explicit list, escalate to CTO first.</requirement>
    <requirement id="3">Generalization must preserve existing 49F behavior byte-for-byte (same table read, same field set, same JWT claim injection). W5.9 regression test is a hard gate.</requirement>
    <requirement id="4">Build via `bash infra/aws/lambda/ci/build-nodejs-lambda.sh portal-auth opalinvest-auth-handler`. No manual zip + upload.</requirement>
    <requirement id="5">Deploy via Terraform. NO `aws lambda update-function-code`. CLAUDE.md Rule 1.</requirement>
    <requirement id="6">Integration test 49F login BEFORE signaling W5.9 off to DT. If 49F regresses, revert the Lambda (prior version via Terraform) and escalate to CTO + COO immediately.</requirement>
    <requirement id="7">Structured logging on missing-table error path — if `opal-partner-${firmId}` doesn't exist, log `partner_table_missing` with `firmId`, return 401/empty (not 500). Prevents silent drift.</requirement>
    <requirement id="8">Commit before apply per CLAUDE.md Rule 2. Tag after deploy per Rule 6.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">`db.ts` generalized + `portal-auth/iam.tf` wildcard grant + source map update. Author 0.4.0_DT_ClientPlatform (code) + 0.7.0_AE_CloudOps (iam.tf — separate commit if pod preference).</deliverable>
    <deliverable type="tag">`portal-auth-v{next}` — with `--follow-tags`.</deliverable>
    <deliverable type="test">Integration test matrix (49F + Inflection + internal user) logged.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT deploy before W1.4 applies. Verify table ACTIVE.</rule>
    <rule>Do NOT skip 49F regression test.</rule>
    <rule>Do NOT hardcode another partner constant (e.g. PARTNER_TABLE_INFLECTION). Generalize — don't branch.</rule>
    <rule>Do NOT use `aws lambda update-function-code`.</rule>
    <rule>Do NOT weaken IAM — wildcard is intended scope, not defense-in-depth.</rule>
    <rule>Do NOT silently 500 on missing-table. Log + return 401.</rule>
  </do_not>
</task_order>
