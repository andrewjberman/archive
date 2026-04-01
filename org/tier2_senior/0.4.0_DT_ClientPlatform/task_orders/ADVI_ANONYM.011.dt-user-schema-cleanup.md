<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-01-ADVI_ANONYM-011-dt-user-schema-cleanup</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>complete</status>
    <!-- Completed 2026-04-01. Commit ec9ff6e2. portal-auth-v1.5.0. partner lookup gate changed to firmId, status check wired, 5 deprecated fields removed from types/db/jwt. NOTE: login broken 18:29-18:34 due to handler path mismatch (dist/index.handler vs index.mjs at zip root). COO hotfix applied handler=index.handler. Req 6 data migration deferred to AE. -->
    <priority>high</priority>
    <type>refactor</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Clean up opal-users-v2 schema: remove deprecated fields (tier, regionId,
    officeId, allowedPages, allowedTabs), move allowedPages/allowedTabs to
    partner-specific table, gate partner identity lookup on firmId instead of
    allowedPages, and wire the status field into login to enable account
    disable/suspend.
  </objective>

  <context>
    Andrew confirmed the following architectural decisions (2026-04-01):

    1. opal-users-v2 is identity + auth ONLY. Partner-specific scoping fields
       (allowedPages, allowedTabs, advisorKey, advisorName, advisorRole) belong
       in the partner-specific table (opal-partner-49financial).

    2. tier is deprecated. Internal access is now firmId=opal-capital (P3 commit
       a067e0fb). The subadvisor/branch hierarchy is unused -- every partner is
       a flat firm with admin/user roles.

    3. regionId and officeId are unused placeholders. Remove them.

    4. status field exists on user records but nothing checks it. Wire it into
       the login flow so suspended/inactive users are blocked.

    5. The partner table lookup in auth.ts is currently gated on
       user.allowedPages?.includes('advisor-intelligence'). Since allowedPages
       is moving to the partner table, the gate must change to firmId-based:
       if (user.firmId && user.firmId !== 'opal-capital') { ... }
  </context>

  <requirements>

    <requirement id="1">
      AUTH-HANDLER auth.ts -- Change partner identity lookup gate:

      Before:
        if (user.allowedPages?.includes('advisor-intelligence')) {
          partnerIdentity = await getPartnerIdentity(user.email);
        }

      After:
        if (user.firmId && user.firmId !== 'opal-capital') {
          partnerIdentity = await getPartnerIdentity(user.email);
        }

      This applies in BOTH the login function (~line 58) and the refresh
      token function (~line 104). Search for all getPartnerIdentity calls.
    </requirement>

    <requirement id="2">
      AUTH-HANDLER auth.ts -- Wire status check into login:

      After password verification and before token generation, add:
        if (user.status !== 'active') {
          throw new Error('Account disabled');
        }
    </requirement>

    <requirement id="3">
      AUTH-HANDLER db.ts -- Remove deprecated fields from getUser return mapping:
      - Remove: tier, regionId, officeId, allowedPages, allowedTabs
      - Keep: email, password_hash, name, role, firmId, userType, status,
              must_change_password, created_at, created_by, last_login,
              password_changed_at, updatedAt, reset_token, reset_token_expires,
              userId, PK

      Also remove from createUser:
      - Remove: tier (line 144), regionId (line 146), officeId (line 147)
      - Keep status (already hardcoded 'active')
    </requirement>

    <requirement id="4">
      AUTH-HANDLER types.ts -- Remove from User interface:
      - tier
      - regionId
      - officeId
      - allowedPages
      - allowedTabs

      Remove from AccessTokenPayload interface:
      - allowedPages
      - allowedTabs
      (tier can stay in JWT for now as a vestigial field -- removing from
      JWT is a separate breaking change that affects portal-authorizer)
    </requirement>

    <requirement id="5">
      AUTH-HANDLER jwt.ts -- Remove from generateAccessToken payload:
      - allowedPages spread
      - allowedTabs spread

      Remove the const declarations for allowedPages and allowedTabs.
    </requirement>

    <requirement id="6">
      PARTNER TABLE -- Migrate allowedPages and allowedTabs to
      opal-partner-49financial. Add these fields to the partner table records
      for any users that currently have them set in opal-users-v2. The
      getPartnerIdentity return type should include these fields so the JWT
      can still carry them (sourced from partner table instead of user table).
    </requirement>

    <requirement id="7">
      DOCUMENTATION -- Update:
      - portal/partners/OPAL_USERS_V2_SCHEMA.md (remove deprecated fields,
        update User Profile table)
      - infra/aws/auth/ARCHITECTURE.md (remove tier references if any remain)
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Login rejects users with status !== 'active'.</criterion>
    <criterion id="2">Partner identity lookup fires for any non-opal-capital firmId.</criterion>
    <criterion id="3">tier, regionId, officeId removed from User interface and db operations.</criterion>
    <criterion id="4">allowedPages/allowedTabs sourced from partner table, not user table.</criterion>
    <criterion id="5">Existing 49F users' allowedPages/allowedTabs migrated to partner table.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT remove status from the schema -- it is being wired in, not deprecated.</constraint>
    <constraint>Do NOT remove tier from JWT/AccessTokenPayload yet -- portal-authorizer still references it. That is a separate task.</constraint>
    <constraint>Do NOT modify opal-users-v2 DynamoDB records directly. The old fields can remain on existing records as dead data -- the code just stops reading them.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ANONYM.007" status="complete">
      P3 tier refactor (commit a067e0fb) -- tier is already unused in pseudonymizer and Lambda.
    </dependency>
  </dependencies>
</task_order>
