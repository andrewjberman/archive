# OPAL_BBGTML B1 — the EXACT m365-gateway diff (proposal to CTO; nothing applied)

**From:** 0.2.0_DT_PortfolioAnalytics (sovereign delegate) — **2026-07-15**
**Rule:** the gateway is SHARED INFRA — this diff surfaces to CTO for routing BEFORE any edit
(briefing Rule 5; COO's collision-channel list names "shared API gateways" explicitly).
**Ships DARK by design:** the integration framework is fail-closed — merging the code adds
ZERO tools to the live MCP surface until `ENABLED_INTEGRATIONS` opts in (base.py doctrine).

## The change, exactly

1. **NEW** `app/integrations/opal_portal/__init__.py` (empty) +
   `app/integrations/opal_portal/integration.py` — full proposed content beside this file
   (`opal_portal_integration.py`). One mutating tool: `opal_data_refresh_upload(date, dry_run, confirm)`.
2. **EDIT** `app/integrations/registry.py` `_load_builtin_factories()` — two lines, the ycharts pattern:
   ```python
   from .opal_portal.integration import OpalPortalIntegration
   register_factory("opal_portal", OpalPortalIntegration)
   ```
3. **CONFIG** (enable step, separate from the merge): add `opal_portal` to `ENABLED_INTEGRATIONS`.
4. **SECRET** `opal/portal/svc-data-refresh` in Secrets Manager: `{"email": "<svc user>", "password": "<...>"}`.
5. **IAM** (Terraform, gateway instance role): `secretsmanager:GetSecretValue` on that secret ARN —
   verified per Rule 22a at apply (simulate-principal-policy, ONE --resource-arns, separate positive control).
6. **PROVISION** a portal service user with `userType: 'Dev'` claims (the opal-portal-authorizer +
   `validate_user_type()` gate at `infra/aws/lambda/data_refresh/lambda_function.py:89-114` requires it) —
   ADVI_PRVSYS pattern; suggest `svc-bbgtml@opalinvest.dev`.

## Governance fit (why this shape)

- `IntegrationSpec(read_only=False, min_tier="standard")` — the base.py validator REFUSES a
  read_only default on a mutating integration; Alyssa = STANDARD_EMPLOYEE tier.
- Trigger leg is **confirm-gated** (G3 pattern): `dry_run=true` stages into `pending/{uploadId}/`
  WITHOUT firing the yang-pipeline (the safe end-to-end exercise); a real send needs `confirm=true`.
- **Hybrid auth:** SharePoint locate/download rides the CALLER's delegated Graph token (Microsoft
  enforces Alyssa's own scope); only the portal API uses the service credential.
- **The gateway never unpickles** (code-execution surface; no pandas on the box). Structural checks
  only (exact names, 2–60MB). The full shape tripwire runs locally pre-send
  (`tools/bbg_pkl_tripwire.py`, exercised: 17/17 PASS on the real 07-10 vintage; key-drift mutant
  + missing-file negative controls both FAIL loud).
- **Files never ride the MCP channel** (8.5MB + 17.1MB measured): Graph download → presigned PUT,
  all server-side (OPAL_TAXSMA attachment-tools precedent).
- Egress hosts declared in-spec: the portal API GW host + graph.microsoft.com (both Opal-owned
  surfaces; no vendor egress — the Bloomberg pull never leaves the terminal machine).

## Review pins for CTO (marked in the code)

- `LOGIN_PATH = "/auth/login"` — confirm the exact portal auth route + response token field.
- `STATUS_PATH` — confirm the deployed status route shape (`handle_status(execution_id)` exists
  at lambda_function.py:718; the upload-urls/trigger routes are grounded at :264/:357).
- upload-urls response shape (`uploadId` + url list) — pinned from AWS_ENGINEER_BRIEF.md; verify
  against the deployed handler at apply time.

## Routing options (CTO's call)

(a) I apply under delegation with your arch-gate (TAXSMA precedent: 0.5.0~A deployed gateway
attachment tools); (b) route to the gateway owner lane; (c) pair review. Steps 3–6 (enable,
secret, IAM, service user) sequenced AFTER the code merge either way — the merge alone changes
nothing live.
