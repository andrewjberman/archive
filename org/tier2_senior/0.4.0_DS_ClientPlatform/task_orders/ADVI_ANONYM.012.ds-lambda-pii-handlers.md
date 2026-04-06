# ADVI_ANONYM.012 — DS: Add Lambda Handlers for PII Endpoints

<task_order>
  <issuer>2.0.0_SA_COO</issuer>
  <issued>2026-04-02</issued>
  <agent>0.4.0_DS_ClientPlatform</agent>
  <status>staged</status>
  <priority>high</priority>
  <project>ADVI_ANONYM</project>
</task_order>

## Context

The portal currently fetches several PII-bearing gold layer files through the
S3-direct path (shared-advisor-router), which serves raw JSON with zero
pseudonymization. The pseudonymizer only runs on the Lambda path
(`opal-partners-data`). We need Lambda handlers for the PII endpoints that
currently have no Lambda handler, so DE can migrate the frontend to use them.

The Lambda already has a working pattern: `handle_advisor_book` at
`lambda_function.py:602` reads `gold/advisors/{advisor_id}/book.json` from S3
and the router at line 1266-1270 wraps it with `_pseudonymize_s3_response()`.
Follow this exact pattern for the new handlers.

## File

`infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py`

## Deliverables

### 1. Add `handle_clients_tab(bucket)` handler

Read `gold/clients_tab.json` from S3 via `serve_s3_json(bucket, key)`.
No transformation — just serve the file. Pseudonymization is applied by the
router wrapper, not inside the handler (same pattern as `handle_advisor_book`).

### 2. Add `handle_client_detail(bucket, client_key)` handler

Read `gold/clients/{client_key}.json` from S3. Sanitize `client_key` the same
way `handle_advisor_book` sanitizes `advisor_id` (alphanumeric + underscore,
no path traversal). Return via `serve_s3_json`.

### 3. Add router entries in `lambda_handler`

In the `/shared/advisor-intelligence` routing block (starting line 1215), add:

```python
elif path.endswith('/clients-tab'):
    return _pseudonymize_s3_response(
        handle_clients_tab(bucket), user_role, firm_id, advisor_id)

elif '/clients/' in path and '/detail' in path:
    client_key = extract_path_param(path, 'clients')
    return _pseudonymize_s3_response(
        handle_client_detail(bucket, client_key), user_role, firm_id, advisor_id)
```

Place these BEFORE the existing `/clients/growth` check (line 1247) so the
more specific path matches first.

### 4. Verify existing handlers already pseudonymize

Confirm these existing handlers are already wrapped with `_pseudonymize_s3_response`:
- `handle_advisor_book` (line 1269) — YES
- `handle_partner_analytics` (line 1263) — YES

No changes needed for those.

## NOT in scope

- Frontend changes (DE handles in .014)
- portal_authorizer changes (DT handles in .013)
- CloudFront behavior changes (none needed)
- Terraform deploy (DT handles after all code is committed)

## Dependencies

None. This can start immediately.

## Acceptance Criteria

- [ ] `handle_clients_tab` handler added, reads `gold/clients_tab.json`
- [ ] `handle_client_detail` handler added, reads `gold/clients/{key}.json` with input sanitization
- [ ] Both routed under `/shared/advisor-intelligence` with `_pseudonymize_s3_response` wrapper
- [ ] Existing `handle_advisor_book` pseudonymization confirmed (no change needed)
- [ ] Code committed on CLOUD branch
