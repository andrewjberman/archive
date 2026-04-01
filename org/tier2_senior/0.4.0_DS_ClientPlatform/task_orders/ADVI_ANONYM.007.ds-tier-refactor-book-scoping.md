<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADVI_ANONYM-007-ds-tier-refactor</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>pending</status>
    <priority>high</priority>
    <type>feature</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Three interlocked code changes across 6 files: (1) remove 'internal' tier from
    opal_auth shared module, (2) remove tier check from pseudonymizer, add book-level
    advisor/own-client scoping, (3) update auth-handler and portal_authorizer to carry
    advisorId through the JWT/context chain. Plus schema doc updates.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_ANONYM_P3_PRD.md</ref>
    <ref type="file_1">infra/aws/lambda/shared/opal_auth/__init__.py</ref>
    <ref type="file_2">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/pseudonymizer.py</ref>
    <ref type="file_3">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</ref>
    <ref type="file_4">infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts</ref>
    <ref type="file_5">infra/aws/opalinvest_dev/lambda/auth-handler/src/jwt.ts</ref>
    <ref type="file_6">infra/aws/opalinvest_dev/lambda/auth-handler/src/types.ts</ref>
    <ref type="file_7">infra/aws/users/lambda/portal-authorizer/index.mjs</ref>
    <ref type="file_8">portal/partners/OPAL_USERS_V2_SCHEMA.md (if exists)</ref>
    <ref type="file_9">infra/aws/auth/ARCHITECTURE.md (if exists)</ref>
  </references>

  <pre_verified_facts>
    COO read all files before issuing this TO. Do not re-litigate these.

    1. opal_auth/__init__.py:57 — `return self.tier == 'internal'` (is_internal property)
       opal_auth/__init__.py:49 — `tier: str  # 'internal' | 'advisor' | 'subadvisor' | 'branch'`

    2. pseudonymizer.py — `if user_tier == 'internal': return False` at line ~59
       (inside `needs_pseudonymization` or `_should_hash` — the tier-bypass logic)

    3. lambda_function.py:1184-1185 — user_tier and user_role extracted from auth_context
       lambda_function.py:1122 — `_pseudonymize_s3_response(resp, user_tier, user_role, firm_id)` signature
       lambda_function.py:1189 — `if not allowed_firms and user_tier == 'internal':` (also needs fixing)

    4. auth-handler/db.ts:101,144 — `tier: item.tier || 'internal'` fallback (TWO locations)
       auth-handler/jwt.ts:66 — `const tier = user.tier || 'internal'` fallback
       auth-handler/types.ts:22,49 — 'internal' in type comment/docstring

    5. portal-authorizer/index.mjs:195-201 — context block. Current last field before closing:
       `role: decoded.role` (line 198). advisorId goes on line 199.
       No advisorId field exists yet in context.
  </pre_verified_facts>

  <requirements>

    <requirement id="1">
      OPAL_AUTH SHARED MODULE -- infra/aws/lambda/shared/opal_auth/__init__.py

      a) Line 57: Change `is_internal` property:
         Before: `return self.tier == 'internal'`
         After:  `return self.firm_id == 'opal-capital'`

      b) Line 49: Remove `'internal'` from the tier docstring/comment.
         Update to: `tier: str  # 'advisor' | 'subadvisor' | 'branch'`

      c) Line ~153: Update the `require_internal` docstring to say firmId=opal-capital
         instead of tier===internal. The method name can stay; behavior unchanged (it
         calls claims.is_internal which is now firm_id-based).

      Do NOT change any callers of `claims.is_internal` or `require_internal` — they
      already use the abstracted method.
    </requirement>

    <requirement id="2">
      PSEUDONYMIZER -- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/pseudonymizer.py

      Read the full file before editing. Then:

      a) Remove the tier check from `needs_pseudonymization` (or equivalent function):
         Before:
           if user_tier == 'internal':
               return False
           if user_role == 'admin':
               return False
           return True
         After:
           if user_role == 'admin':
               return False
           return True
         Remove the `user_tier` parameter from this function entirely.

      b) Add `advisor_id: str | None = None` parameter to `pseudonymize_response`:
         Before: `def pseudonymize_response(body, user_tier, user_role, firm_id)`
         After:  `def pseudonymize_response(body, user_role, firm_id, advisor_id=None)`
         (user_tier parameter also removed)

      c) Implement architect-match logic: when `advisor_id` is provided, client-level
         records where `architect == advisor_id` should NOT be hashed (own-book clients).
         The `_walk` function must propagate the `architect` value from parent objects
         down to field transforms. See PRD §3 for the `_should_hash` signature:
         ```python
         def _should_hash(user_role, advisor_id, field_architect=None):
             if user_role == 'admin':
                 return False
             if advisor_id and field_architect and field_architect == advisor_id:
                 return False
             return True
         ```

      d) Update the module docstring to reflect the new role matrix (remove internal tier).
    </requirement>

    <requirement id="3">
      LAMBDA FUNCTION -- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py

      a) Line ~1184: After `user_role = auth_context.get('role', '')`, add:
         `advisor_id = auth_context.get('advisorId', None)  # None if not set`

      b) Line ~1189: Change the internal fallback:
         Before: `if not allowed_firms and user_tier == 'internal':`
         After:  `if not allowed_firms and firm_id == 'opal-capital':`

      c) Line ~1122: Update `_pseudonymize_s3_response` signature:
         Before: `def _pseudonymize_s3_response(resp, user_tier, user_role, firm_id)`
         After:  `def _pseudonymize_s3_response(resp, user_role, firm_id, advisor_id=None)`
         Update the call to `pseudonymizer.pseudonymize_response` inside it to pass `advisor_id`.

      d) Update ALL call sites of `_pseudonymize_s3_response` throughout lambda_function.py
         to pass `advisor_id` (or omit it -- default None is fine for non-book endpoints).
         There are approximately 9 call sites from P1. Review each one.

      e) Remove `user_tier` from all call sites of `_pseudonymize_s3_response` since the
         parameter is being removed.
    </requirement>

    <requirement id="4">
      AUTH-HANDLER (TypeScript) -- infra/aws/opalinvest_dev/lambda/auth-handler/src/

      Read db.ts, jwt.ts, and types.ts before editing.

      a) db.ts:101 — `tier: item.tier || 'internal'` → `tier: item.tier || 'advisor'`
      b) db.ts:144 — same fallback fix (second occurrence)
      c) jwt.ts:66 — `const tier = user.tier || 'internal'` → `const tier = user.tier || 'advisor'`
      d) jwt.ts — Add `advisorId` to JWT payload. If the user record has `user.advisorId`,
         include it in the signed claims. Example (after the existing claims):
         `advisorId: user.advisorId || undefined`
      e) types.ts:22 — Update tier type comment to remove 'internal':
         `tier?: string;  // 'advisor' | 'subadvisor' | 'branch'`
      f) types.ts:49 — Same update in the JWT claims type comment.

      NOTE: auth-handler is TypeScript. If you are not confident in TypeScript, document
      any uncertainty in your session log and COO will route to DE for review.
      The `allowedFirmIds` logic is in `index.ts` or `handler.ts` -- search for
      `tier === 'internal'` or `allowedFirmIds = 'ALL'` and update to `firmId === 'opal-capital'`.
    </requirement>

    <requirement id="5">
      PORTAL AUTHORIZER -- infra/aws/users/lambda/portal-authorizer/index.mjs

      Line 198-199: Add advisorId to the context block immediately after `role: decoded.role`:
      ```javascript
      role: decoded.role,
      advisorId: decoded.advisorId || 'null',
      ```
      That is the ONLY change to this file.
    </requirement>

    <requirement id="6">
      DOC UPDATES

      a) If `portal/partners/OPAL_USERS_V2_SCHEMA.md` exists:
         - Remove 'internal' from the tier values list
         - Add `advisorId` field to the User Profile section (optional string)

      b) If `infra/aws/auth/ARCHITECTURE.md` exists:
         - Remove 'internal' from the tier matrix
         - Update permission resolution algorithm to show firmId=opal-capital for ALL access

      If either file does not exist, note it in your session log and skip.
    </requirement>

    <requirement id="7">
      Commit with author attribution (single commit for all changes):
      ```
      git commit --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>" \
          -m "feat(ADVI_ANONYM P3): tier refactor (internal->firmId), role-only PII gate, book scoping"
      ```
      Do NOT push. DT (.008) deploys.
      Message COO with commit hash and any findings (esp. TypeScript concerns in auth-handler).
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">opal_auth is_internal uses firm_id == 'opal-capital'.</criterion>
    <criterion id="2">pseudonymizer has no user_tier parameter. Role is the sole PII gate. advisor_id book-scoping implemented.</criterion>
    <criterion id="3">lambda_function.py extracts advisorId from auth_context. Internal fallback uses firm_id == 'opal-capital'. All _pseudonymize_s3_response call sites updated.</criterion>
    <criterion id="4">auth-handler tier fallbacks changed from 'internal' to 'advisor'. advisorId included in JWT if present on user record.</criterion>
    <criterion id="5">portal_authorizer context includes advisorId field.</criterion>
    <criterion id="6">All changes committed on CLOUD branch. Not pushed.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not change the behavior of require_internal or any callers of claims.is_internal -- they use the abstracted property which now checks firm_id. No cascading changes needed there.</constraint>
    <constraint>advisor_id book-scoping applies to partner/user only. admin users still get cleartext regardless (role check comes first in _should_hash).</constraint>
    <constraint>Do NOT modify any gold layer scripts. This is a serving-layer change only.</constraint>
    <constraint>Do NOT push to CLOUD. DT deploys all three Lambdas together after this commit.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="ADVI_ANONYM_P1_P2_verification" status="complete">
      P1 (pseudonymizer deployed) and P2 (UI indicators) both complete as of 2026-04-01.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code-commit">6 files updated on CLOUD branch</deliverable>
    <deliverable type="message">COO commit hash + any TypeScript auth-handler concerns</deliverable>
  </deliverables>
</task_order>
