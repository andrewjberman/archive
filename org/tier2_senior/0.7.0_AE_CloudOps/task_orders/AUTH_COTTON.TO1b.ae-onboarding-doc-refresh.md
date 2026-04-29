<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>AUTH_COTTON.TO1b</id>
    <project>AUTH_COTTON</project>
    <title>ONBOARDING.md §5 Step 3 doc-drift refresh — post-Inflection auth handler generalization</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>pending</status>
    <priority>medium</priority>
    <estimated_effort>15-30 min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/AUTH_COTTON.md</ref>
    <ref type="prd_section">§4.6 + §6 TO-1b</ref>
    <ref type="target_file">infra/aws/users/ONBOARDING.md</ref>
    <ref type="verify_file">infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts</ref>
  </references>

  <context>
    ONBOARDING.md was last touched 2026-04-15, BEFORE the Inflection onboarding (2026-04-21).
    §5 Step 3 currently references "auth handler has opal-partner-49financial as a hardcoded
    constant" — but Inflection (opal-partner-inflection) was successfully onboarded post that
    writing, proving the auth handler now resolves table name dynamically from user.firmId.

    This TO refreshes the runbook to reflect reality so the next partner onboarding works
    from accurate docs. It is doc-only; no runtime impact.

    CRITICAL CHECK: Before editing, read infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts
    to confirm the generalization assumption. If still hardcoded (unexpected), STOP and escalate
    to CTO — this invalidates the entire AUTH_COTTON architecture assumption.
  </context>

  <scope>
    1. Read infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts
       - Locate getPartnerIdentity() or equivalent function
       - Confirm table name is resolved from user.firmId (NOT hardcoded to "opal-partner-49financial")
       - Note exact line range that proves generalization

    2. Read infra/aws/users/ONBOARDING.md §5 (find the Step 3 reference)
       - Identify the specific text that says "hardcoded constant" or similar

    3. Edit ONBOARDING.md §5 Step 3:
       - Replace "hardcoded constant" / outdated language with:
         "auth handler resolves partner table name dynamically from user.firmId
         (e.g., firmId=cottonwood → opal-partner-cottonwood). No auth handler
         code change is needed for new partners — adding a new partner table via
         Terraform and a user row in opal-users-v2 is sufficient."
       - Cite the db.ts line range that confirms this in the edit or adjacent comment

    4. Verify no other §5 steps contain stale 49F-specific hardcoded references.

    Commit doc change.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write — code read">
      <step>
        <run>Read infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts (full file or
        grep for getPartnerIdentity, firmId, opal-partner)</run>
        <expect>Table name is resolved from user.firmId or firmId variable, NOT hardcoded
        string "opal-partner-49financial". Line range confirms dynamic resolution.</expect>
        <if_mismatch>STOP. If still hardcoded to 49financial, do NOT edit ONBOARDING.md
        (the drift description would be wrong). Report to COO immediately — this is a
        blocker for the entire AUTH_COTTON project architecture.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Read infra/aws/users/ONBOARDING.md post-edit §5</run>
        <expect>No more "hardcoded constant" language. Step 3 accurately describes dynamic
        table name resolution. No contradictions with any other ONBOARDING.md sections.</expect>
        <if_mismatch>Fix contradictions before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="N/A — doc only">
      <step>
        <run>N/A — no comp-* tool covers documentation drift checks.</run>
        <expect>Absence acknowledged.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      db.ts read confirms dynamic table name resolution. Evidence: file path + line number
      in session log showing the firmId-based resolution.
    </criterion>
    <criterion id="2">
      ONBOARDING.md §5 Step 3 no longer says "hardcoded constant". Replacement text
      reflects current dynamic resolution with db.ts citation.
      Evidence: diff in session log.
    </criterion>
    <criterion id="3">
      No other ONBOARDING.md §5 steps contain stale 49F-only hardcoded references
      (full §5 scan). Evidence: noted in session log.
    </criterion>
    <criterion id="4">
      Commit via safe-commit.sh with correct author identity.
      Evidence: commit hash in session log.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="none" status="none"/>
    Parallelizable with TO-1 (can ride-along in same commit or separate small commit).
    No gates. Independent of TO-2, TO-3, TO-4.
  </dependencies>

  <cross_domain_coordination>
    <none/>
    ONBOARDING.md is not touched by any other active project.
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh --author "0.7.0_AE_CloudOps &lt;0.7.0_AE_CloudOps@opal.agent&gt;" \
      -m "docs(AUTH_COTTON.TO1b): refresh ONBOARDING.md §5 Step 3 — post-Inflection dynamic table resolution" \
      -- infra/aws/users/ONBOARDING.md
  </commit_identity>

  <notes>
    If db.ts read shows a more complex pattern (e.g., table name pulled from env var or
    config map rather than direct firmId interpolation), document the actual mechanism
    in ONBOARDING.md rather than the assumed one. The key message is: auth handler
    requires no code change for new partners.
  </notes>
</task_order>
