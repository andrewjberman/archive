<!--
  Drafted by 0.3.0_DT_TradingOperations at Andrew's direction (2026-04-28),
  pending 2.0.0_SA_COO ratification. Status `draft` until COO flips to `active`
  and binds W4 into TRSB_PATHFIX.json waves.
-->
<task_order>
  <metadata>
    <id>TRSB_PATHFIX.TO-4.ae-firm-scoping-backend</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <drafted_by>0.3.0_DT_TradingOperations</drafted_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <supporting>0.3.0_DT_TradingOperations (Phase B backfill)</supporting>
    <date>2026-04-28</date>
    <status>draft</status>
    <project_code>TRSB_PATHFIX</project_code>
    <wave>W4 — FIRM-SCOPED TRADE DATA (post-portal-partner-rollout)</wave>
    <prd_ref>see context section below — no PRD update yet, follow-up scope from portal commit cbbc07c8</prd_ref>
    <effort>2-4 hours</effort>
    <gates_on>TO-1 PASS (W1 routes live); independent of TO-2 / TO-3</gates_on>
    <gates_for>None — backend hardening of frontend defense-in-depth filter</gates_for>
    <tag>trade-pipeline-v1.8.0</tag>
  </metadata>

  <context>
    Portal commits 37fc91f5 + cbbc07c8 (2026-04-28) opened Trade Submission to
    49financial + inflection partner firms. Two layers were shipped on the
    frontend:
      1. /trade-submission added to FIRM_ALLOWED_PATHS for both partner firms;
         tab list reduced to [Submit, History] for non-opal-capital firms.
      2. HistoryTab AGG view client-side-filters by initiator_email domain
         match against claims.firmId (FIRM_EMAIL_DOMAINS map: 49financial.com,
         inflectionwealthmgmt.com).

    Two backend gaps remain — this TO closes them:

    GAP 1 — submissions don't carry firmId. opal-trade-submissions items have
    initiator_email but no firmId field (verified: 30 existing items, all
    Andrew's, no firmId). Without it, the dashboard-api can't filter server-side.

    GAP 2 — trade-dashboard-api does no JWT-claim-aware filtering. dashboard_api.py
    routes by path/query params alone (lines 38-83). A determined client can hit
    /api/general/trades/submissions, /submissions/by-status, /submissions/by-date
    and observe every firm's trades regardless of UI scoping. This is a true
    data-isolation hole, not just a UX issue.

    With partners now able to log in and submit, hardening can't wait long. The
    frontend filter is defense-in-depth UX only.
  </context>

  <objective>
    Tag every trade submission with firmId at write time, backfill existing items,
    and enforce firmId-based filtering in trade-dashboard-api. opal-capital
    retains full cross-firm visibility. Partners see only their own firm's data
    even when bypassing the UI.
  </objective>

  <compiler_tools_mandate>
    <phase_1_before_write>
      - aws dynamodb describe-table --table-name opal-trade-submissions
        (capture current schema; confirm no firmId attribute exists)
      - aws dynamodb scan --table-name opal-trade-submissions --select COUNT
        (capture pre-backfill item count for reconciliation)
      - aws dynamodb scan --table-name opal-users-v2 --select COUNT
        --filter-expression "attribute_exists(firmId)"
        (verify firmId is populated on the lookup source)
      - aws apigatewayv2 get-authorizer --api-id 7k3ed8px20 --authorizer-id naqxlm
        (confirm authorizer is JWT type and JWT claims propagate to event.requestContext.authorizer.jwt.claims)
      - comp-routes behaviors (capture pre-change baseline)
    </phase_1_before_write>
    <phase_2_before_tag>
      - python -m py_compile on every edited Lambda source file (per CLAUDE.md rule 14)
      - .tools/ds-precommit-check.py + ruff check --target-version py39 on the same files
      - aws lambda get-function --function-name trade-submission-handler
        --query 'Configuration.LastModified' (verify post-deploy timestamp)
      - Same check for trade-dashboard-api
      - terraform plan in infra/aws/terraform/trade-pipeline/ (expect 0-diff after apply)
      - aws dynamodb scan --table-name opal-trade-submissions --select COUNT
        --filter-expression "attribute_exists(firmId)"
        (post-backfill: must equal pre-backfill total count)
    </phase_2_before_tag>
    <phase_3_after_tag>
      - End-to-end smoke: log in as test-regression@49financial.com,
        submit a trade via portal, verify item lands in DDB with
        firmId=49financial. Switch to andrew@opalinvest.com, verify
        AGG view in History shows BOTH the new partner trade AND the
        existing opal-capital trades. Switch back to partner, verify
        AGG view shows ONLY the partner trade (no Opal trades visible).
      - Direct API smoke: curl /api/general/trades/submissions with
        partner JWT — response must contain only firmId=49financial items
        (devtools-bypass test; this is the actual hardening goal).
      - CloudWatch: trade-dashboard-api invocation count > 0 with 200,
        no 5xx in past 5 min.
      - comp-routes behaviors (must be identical to baseline)
      - Append to org/compiler-tools-log.md
    </phase_3_after_tag>
  </compiler_tools_mandate>

  <scope>
    Three phases, sequenced. Phase B can run concurrently with Phase A deploy.

    PHASE A — submission_handler.py: tag firmId at submit time
    -----------------------------------------------------------
    File: infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py

    Add firmId lookup using opal-users-v2 email-index GSI:

        def get_user_firm_id(email):
            users_table = dynamodb.Table('opal-users-v2')
            response = users_table.query(
                IndexName='email-index',
                KeyConditionExpression=Key('email').eq(email.lower()),
                Limit=1,
            )
            items = response.get('Items', [])
            return items[0].get('firmId') if items else None

    In lambda_handler, after deriving initiator_email (line 58):
        firm_id = get_user_firm_id(initiator_email) or 'unknown'

    Add to the item dict (around line 80):
        'firmId': firm_id,

    Add `from boto3.dynamodb.conditions import Key` to imports.

    IAM: trade-submission-handler IAM role needs read access to
    opal-users-v2 (Query on GSI/email-index). Update
    infra/aws/terraform/trade-pipeline/iam.tf accordingly.

    PHASE B — backfill existing items (DT 0.3.0 supporting)
    --------------------------------------------------------
    Script: scripts/trsb_backfill_firmid.py (one-shot, idempotent)

    For each item in opal-trade-submissions where attribute_not_exists(firmId):
      1. Look up initiator_email in opal-users-v2 (email-index GSI)
      2. UpdateItem set firmId = lookup result, default 'unknown' if not found
      3. Log the (submission_id, initiator_email, firmId) triple

    Dry-run by default; --apply to write. Run AFTER Phase A deploys (so the
    Lambda is also writing firmId, no race on new items).

    Today's known data (verified 2026-04-28): all ~30 existing items have
    initiator_email = andrew@opalinvest.com → firmId = opal-capital. Backfill
    will be uniform; the script must still be table-driven for future-proofing.

    PHASE C — dashboard_api.py: filter by firmId from JWT claims
    -------------------------------------------------------------
    File: infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/dashboard_api.py

    Extract firmId from event:
        def get_caller_firm_id(event):
            claims = (
                event.get('requestContext', {})
                     .get('authorizer', {})
                     .get('jwt', {})
                     .get('claims', {})
            )
            return claims.get('firmId')

    Apply firm scoping in every aggregate handler. Pattern:
        firm_id = get_caller_firm_id(event)
        # opal-capital sees everything; partners scoped to their firm
        if firm_id and firm_id != 'opal-capital':
            items = [i for i in items if i.get('firmId') == firm_id]

    Endpoints to scope (at minimum):
      - get_pending_submissions  (line 167)
      - get_by_approver          (line 204)
      - get_by_status            (line ?)
      - get_by_date              (line ?)
      - get_recent_submissions   (default fallthrough)
      - get_submission           (single-item: 404 if firmId mismatch and caller != opal-capital)

    Endpoints already naturally scoped:
      - get_by_initiator (takes explicit email param; still gate by firmId match
        between caller and target email's firm to prevent cross-firm peek)
      - get_excel_download (gate by firmId on the underlying submission)

    PHASE D — Terraform deploy + tag
    ---------------------------------
    - Update infra/aws/terraform/trade-pipeline/iam.tf for the new
      opal-users-v2 read on trade-submission-handler
    - Run build-and-upload.sh for both Lambdas (S3-backed deployment per
      MEMORY.md)
    - terraform plan + apply in infra/aws/terraform/trade-pipeline/
    - Verify 0-diff after apply
    - git tag -a trade-pipeline-v1.8.0 + git push --follow-tags

    PHASE E (OPTIONAL, can defer) — frontend simplification
    --------------------------------------------------------
    Once backend filter is verified, the client-side isEmailFromFirm filter
    in HistoryTab is redundant (data is already firm-scoped at the API).
    Leaving it in place is fine as defense-in-depth. If removed: see
    portal/src/pages/TradeSubmission/tabs/HistoryTab.tsx:39-46 — drop the
    .filter() and the useAuth import. Skip this phase for safety; revisit
    only if the redundant filter is causing user-visible issues.

    IMPORTANT — DO NOT:
    - Backfill BEFORE Phase A deploys (race on new submissions)
    - Skip Phase A IAM update (Lambda will fail with AccessDenied on the GSI query)
    - Drop opal-capital bypass (internal users must see all firms)
    - Add firmId as a DDB GSI hash key — current scan-and-filter is fine for
      30 items growing to a few hundred; only add a GSI if scan latency
      becomes user-visible (revisit at 10k+ items)
    - Touch /api/public/trades/* legacy routes
    - Modify portal frontend in this TO (Phase E is explicitly deferred)
  </scope>

  <acceptance_criteria>
    1. trade-submission-handler writes firmId on every new submission, sourced
       from opal-users-v2.firmId via email-index GSI lookup. Verified by
       submitting a test trade as test-regression@49financial.com and reading
       the resulting DDB item.
    2. Existing 30 items in opal-trade-submissions all have firmId set after
       backfill. Pre/post counts match (no item lost or duplicated).
    3. trade-dashboard-api filters every aggregate endpoint by caller's firmId,
       with opal-capital bypass. Partner JWT cannot retrieve other firms' items
       via direct API call (curl test).
    4. opal-capital JWT continues to see every firm's items (non-regression).
    5. comp-routes behaviors output identical before and after.
    6. terraform plan reports 0-diff after apply.
    7. trade-pipeline-v1.8.0 tag applied after clean smoke test.
    8. Session log documents: backfill script invocation + counts, smoke test
       evidence (DDB items, curl JWT tests), CloudWatch metrics.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT backfill before Phase A is deployed — new submissions written between scan and write would lack firmId.</rule>
    <rule>Do NOT drop the opal-capital bypass — internal users must retain cross-firm visibility.</rule>
    <rule>Do NOT add firmId as a GSI hash key in this TO — scan-and-filter is sufficient at current scale.</rule>
    <rule>Do NOT modify the portal frontend in this TO. Phase E is explicitly deferred and out of scope here.</rule>
    <rule>Do NOT skip the IAM update — submission_handler will hit AccessDenied on opal-users-v2 GSI query without it.</rule>
    <rule>Do NOT touch /api/public/trades/* legacy routes.</rule>
    <rule>Do NOT skip py_compile + ruff gate per CLAUDE.md rule 14 before commit.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">submission_handler.py firmId-tagging patch + opal-users-v2 GSI lookup</deliverable>
    <deliverable type="code">dashboard_api.py JWT-claim-aware filter on every aggregate endpoint</deliverable>
    <deliverable type="script">scripts/trsb_backfill_firmid.py (idempotent, dry-run-default)</deliverable>
    <deliverable type="infrastructure">iam.tf update for trade-submission-handler reading opal-users-v2/email-index</deliverable>
    <deliverable type="infrastructure">terraform apply 0-diff in infra/aws/terraform/trade-pipeline/</deliverable>
    <deliverable type="document">Session log with backfill counts + smoke test evidence (DDB items, curl JWT results, CloudWatch metrics)</deliverable>
    <deliverable type="tag">trade-pipeline-v1.8.0</deliverable>
    <deliverable type="ravc">RAVC to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1-AC8 outputs + backfill report + cross-firm curl test results</deliverable>
  </deliverables>
</task_order>
