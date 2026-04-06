<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADVI_ANONYM-002-ds-pseudonymizer</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>complete</status>
    <!-- Completed 2026-04-01. Commit 3fdb9a51. pseudonymizer.py created, lambda wired at 9 PII call sites. IAM blocker documented for DT. handle_adv_drill handler not yet implemented -- wire when added. -->
    <priority>high</priority>
    <type>feature</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Implement HMAC-based pseudonymization in the opal-partners-data Lambda.
    Partner users with tier=advisor and role=user currently receive a 403 Forbidden
    from the P0 gate on all advisor-intelligence endpoints. P1 replaces that blunt block
    with graduated visibility: internal and advisor-admin users see cleartext;
    advisor-user sees hashed client names, account IDs, and relationship-level geo.
    You write the pseudonymizer module and wire it into lambda_function.py.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_ANONYM_PRD.md</ref>
    <ref type="verified_fact">infra/aws/users/lambda/portal-authorizer/index.mjs line 198: role already returned in authorizer context. No DE action needed -- role IS available to the Lambda today.</ref>
    <ref type="entry_point">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py line 1158: user_tier extracted. user_role must be added here.</ref>
  </references>

  <pre_verified_facts>
    COO verified the following before issuing this TO. Do NOT re-litigate these.

    1. portal_authorizer (deployed 2026-03-04) already returns `role` in the
       authorizer context (infra/aws/users/lambda/portal-authorizer/index.mjs line 198).
       The PRD concern about "add role to authorizer" is already resolved.

    2. lambda_function.py extracts `user_tier = auth_context.get('tier', '')` at line 1158
       but does NOT yet extract `user_role`. Your first code change is one line:
       `user_role = auth_context.get('role', '')`

    3. The deployed authorizer also computes `allowedFirmIds` correctly for advisor-user
       (single firm) and internal (ALL). firmId is in the authorizer context at line 199.

    4. The pseudonymizer key lives at `opal/pseudonym/{firmId}` in Secrets Manager.
       AE will provision these in parallel (ADVI_ANONYM.003). Your code uses lazy
       provisioning (generate + store on first request) as a fallback if AE's keys
       are not yet there.
  </pre_verified_facts>

  <scope>
    <file action="create">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/pseudonymizer.py</file>
    <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
  </scope>

  <requirements>

    <requirement id="1">
      READ lambda_function.py completely before editing. Understand every response
      path (handle_timeseries, handle_snapshots, handle_clients_*, handle_books_*,
      handle_advisor_book, etc.) before wiring the pseudonymizer. There are approximately
      20 handler functions. You must identify which ones return PII fields.
    </requirement>

    <requirement id="2">
      Create pseudonymizer.py implementing:

      ```python
      import hashlib
      import hmac
      import os
      import json
      import boto3
      import secrets

      _secrets_client = boto3.client('secretsmanager', region_name='us-east-1')
      _key_cache = {}  # {firm_id: bytes}

      def _get_firm_key(firm_id: str) -> bytes:
          """Fetch or lazily provision per-firm HMAC key from Secrets Manager."""
          if firm_id in _key_cache:
              return _key_cache[firm_id]
          secret_name = f'opal/pseudonym/{firm_id}'
          try:
              val = _secrets_client.get_secret_value(SecretId=secret_name)['SecretString']
              key = bytes.fromhex(val)
          except _secrets_client.exceptions.ResourceNotFoundException:
              # Lazy provision: generate and store
              key = secrets.token_bytes(32)
              _secrets_client.create_secret(
                  Name=secret_name,
                  SecretString=key.hex()
              )
          _key_cache[firm_id] = key
          return key

      def _hash(firm_id: str, value: str, prefix: str) -> str:
          """Compute deterministic HMAC-SHA256 8-char hex pseudonym."""
          key = _get_firm_key(firm_id)
          digest = hmac.new(key, value.encode('utf-8'), hashlib.sha256).hexdigest()
          return f'{prefix} {digest[:8]}'

      def needs_pseudonymization(user_tier: str, user_role: str) -> bool:
          """Return True if this user should see hashed PII."""
          # internal/* and advisor/admin see cleartext
          if user_tier == 'internal':
              return False
          if user_role == 'admin':
              return False
          # advisor/user (and any unknown tier/role) sees pseudonymized
          return True

      def pseudonymize_response(body: dict, user_tier: str, user_role: str, firm_id: str) -> dict:
          """Walk body and replace PII fields per the role matrix.
          Returns body unchanged if user does not need pseudonymization.
          """
          if not needs_pseudonymization(user_tier, user_role):
              return body
          return _walk(body, firm_id)

      def _walk(obj, firm_id: str):
          if isinstance(obj, dict):
              return {k: _transform_field(k, v, firm_id) for k, v in obj.items()}
          if isinstance(obj, list):
              return [_walk(item, firm_id) for item in obj]
          return obj

      def _transform_field(key: str, value, firm_id: str):
          """Apply field-level pseudonymization rules."""
          if value is None or not isinstance(value, str):
              return _walk(value, firm_id) if isinstance(value, (dict, list)) else value

          # Fields that identify a client household
          if key in ('relationship_name', 'client_name'):
              return _hash(firm_id, value, 'Client')

          # Labels in client context (ADV drill segments, client lists)
          # 'label' is also used for non-client contexts (architect names, states) --
          # pseudonymize only when inside a client/relationship-level structure.
          # The caller (lambda_function.py) must pass client-context bodies only.
          if key == 'label':
              return _hash(firm_id, value, 'Client')

          # Advisor book name (advisor full name as book title)
          if key == 'book_name':
              return _hash(firm_id, value, 'Book')

          # Account identifier
          if key == 'account_id':
              return _hash(firm_id, value, 'Acct')

          # Stable relationship key used in drill navigation
          if key in ('relationship_id', 'client_key', 'key'):
              return _hash(firm_id, value, 'id')

          # City at relationship grain -- hash when in per-client geo drill data
          # Top-level aggregate city labels are excluded by the caller
          if key in ('city', 'state'):
              return _hash(firm_id, value, 'Location')

          # Recurse into nested structures
          if isinstance(value, (dict, list)):
              return _walk(value, firm_id)

          return value
      ```

      IMPORTANT CONSTRAINTS on the pseudonymizer module:
      - Use `hmac.new`, NOT `hmac.HMAC` -- the built-in `hmac` module uses `hmac.new(key, msg, digestmod)`.
      - The `label` field is used for both client names AND non-client contexts (architect names,
        geographic aggregates). Do NOT apply the pseudonymizer to top-level `label` fields in
        snapshot or timeseries response bodies. Only apply to response bodies that are known to
        contain client-level PII. See Requirement 4 for the exact call sites.
      - `key` field (used for drill navigation) must be hashed consistently with `label` so that
        portal drill-down navigation continues to work (frontend passes `key` back as path param).
      - AUA/NNA dollar amounts (any numeric value) are NEVER hashed. Only string fields.
    </requirement>

    <requirement id="3">
      In lambda_function.py, add `user_role` extraction immediately after `user_tier` at line 1158:

      ```python
      user_tier = auth_context.get('tier', '')
      user_role = auth_context.get('role', '')       # ADD THIS LINE
      ```

      Pass `user_tier`, `user_role`, and `firm_id` to the pseudonymizer at each call site.
    </requirement>

    <requirement id="4">
      Apply pseudonymizer.pseudonymize_response() to the response BODY (before wrapping in
      cors_response or cors_response_nocache) at exactly these call sites:

      | Endpoint handler | PII present | Apply pseudonymizer? |
      |---|---|---|
      | handle_timeseries (relationship dimension) | relationship labels | YES -- only when dimension == 'relationship' |
      | handle_timeseries (city/state dimensions) | city/state labels at aggregate level | NO -- aggregate geo, not per-relationship |
      | handle_snapshots | no client names | NO |
      | handle_clients_growth | relationship names in growth entries | YES |
      | handle_clients_tax_breakdown | relationship names | YES |
      | handle_clients_tax_deferred | relationship names | YES |
      | handle_partner_analytics | top_clients list with name field | YES |
      | handle_advisor_book | client list in book | YES |
      | handle_books_relationship_* | client detail (client_name, relationship_id) | YES |
      | handle_books_account_* | account_id in account drill | YES |
      | handle_books_advisor_* | book_name in advisor book header | YES |
      | handle_adv_drill (Distribution endpoint) | clients[].label + clients[].key | YES -- only the client-segment drill data, not the top-level architect or geo segments |
      | handle_get_partners, handle_firm_*, handle_filters | no client PII | NO |

      READ each handler implementation to confirm which response dict keys contain PII
      before adding the call. Do not call pseudonymize_response on handlers that return
      no client-level PII -- unnecessary overhead.
    </requirement>

    <requirement id="5">
      All response paths that serve client-level PII (where pseudonymize_response is called)
      MUST use cors_response_nocache. Review each handler: if it currently uses cors_response
      (5-min cache) and contains client PII, change it to cors_response_nocache.
      Firm-level aggregates (firm_mix_views, firm_composition, filters) already use
      cors_response_nocache -- do not change them. Verify the remainder.
    </requirement>

    <requirement id="6">
      Grant the Lambda access to Secrets Manager by verifying the Lambda execution role
      includes `secretsmanager:GetSecretValue` and `secretsmanager:CreateSecret` for
      `opal/pseudonym/*`. Check infra/aws/terraform/partners-api/iam.tf. If the
      permission is missing, document it as a blocker in your session log (DT will
      update the Terraform). Do NOT modify iam.tf yourself.
    </requirement>

    <requirement id="7">
      Commit with author attribution:
      ```
      git commit --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>" \
          -m "feat(ADVI_ANONYM P1): pseudonymizer.py + lambda wiring for advisor-user tier"
      ```
      Do NOT push. DT will push and deploy via Terraform after verifying the build.
    </requirement>

    <requirement id="8">
      Write a session log at:
      org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/advi_anonym_p1_pseudonymizer.md
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">pseudonymizer.py exists with needs_pseudonymization(), pseudonymize_response(), _hash(), _get_firm_key() all implemented.</criterion>
    <criterion id="2">lambda_function.py extracts user_role at line ~1158 (immediately after user_tier).</criterion>
    <criterion id="3">pseudonymize_response() called on all handlers identified in Requirement 4.</criterion>
    <criterion id="4">No PII handler returns cors_response with max-age > 0. All PII paths use cors_response_nocache.</criterion>
    <criterion id="5">Lazy key provisioning: if opal/pseudonym/{firmId} secret does not exist, it is created on first request.</criterion>
    <criterion id="6">Changes committed on CLOUD branch. Not pushed.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT remove the P0 role gate from auth-validator-edge. That is DT's job, and it must happen LAST after pseudonymizer is verified end-to-end.</constraint>
    <constraint>Do NOT modify portal_authorizer. It already returns role correctly.</constraint>
    <constraint>Do NOT apply pseudonymizer to architect (advisor) names. Advisor names are employee data, not client PII.</constraint>
    <constraint>Do NOT apply pseudonymizer to aggregate-level city/state in top-level snapshot/timeseries segments. Only hash when the label is tied to a specific relationship.</constraint>
    <constraint>Do NOT modify any gold layer scripts. Pseudonymization is a serving-layer concern only.</constraint>
    <constraint>Do NOT modify iam.tf. Document missing IAM perms as blockers for DT.</constraint>
    <constraint>No emojis in any code per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="portal_authorizer_role_verification" status="complete">
      COO verified 2026-04-01: portal_authorizer deployed 2026-03-04 already returns role in context.
      No prerequisite DE deploy needed.
    </dependency>
    <dependency agent="0.7.0_AE_CloudOps" task="ADVI_ANONYM.003.ae-secrets-provisioning" status="staged">
      AE provisions Secrets Manager keys in parallel. DS lazy-provisions as fallback --
      dependency is not blocking.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code-commit">pseudonymizer.py (new) + lambda_function.py modifications on CLOUD branch</deliverable>
    <deliverable type="document">Session log with handler-by-handler PII audit results and any IAM blocker notes</deliverable>
  </deliverables>
</task_order>
