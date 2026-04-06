# ADVI_ANONYM.013 — DT: portal_authorizer advisorId Passthrough

<task_order>
  <issuer>2.0.0_SA_COO</issuer>
  <issued>2026-04-02</issued>
  <agent>0.4.0_DT_ClientPlatform</agent>
  <status>staged</status>
  <priority>high</priority>
  <project>ADVI_ANONYM</project>
</task_order>

## Context

The pseudonymizer in the partners-api Lambda supports book-scoping: when a
user has an `advisorId`, their own clients appear in cleartext while other
advisors' clients are hashed. This is the design for partner `role=user`
accounts like chase@49financial.

The Lambda reads `advisorId` from auth context at `lambda_function.py:1186`:
```python
advisor_id = auth_context.get('advisorId', None)
```

But `portal_authorizer` (`infra/aws/lambda/portal_authorizer/index.mjs:93-101`)
never includes `advisorId` in the context it returns to API Gateway:

```javascript
const context = {
  email: decoded.sub,
  name: decoded.name || '',
  tier: decoded.tier,
  role: decoded.role,
  firmId: decoded.firmId || 'null',
  officeId: decoded.officeId || 'null',
  regionId: decoded.regionId || 'null'
};
```

The JWT already contains `advisorId` (minted by auth-handler at `jwt.ts:80`).
It just needs to be passed through.

## File

`infra/aws/lambda/portal_authorizer/index.mjs`

## Deliverable

Add `advisorId` to the context object at line 93-101:

```javascript
const context = {
  email: decoded.sub,
  name: decoded.name || '',
  tier: decoded.tier,
  role: decoded.role,
  firmId: decoded.firmId || 'null',
  officeId: decoded.officeId || 'null',
  regionId: decoded.regionId || 'null',
  advisorId: decoded.advisorId || 'null'
};
```

**Also fix the 'null' string pattern:** Currently `firmId`, `officeId`,
`regionId` all fall back to the string `'null'` instead of empty string or
omitting the field. The Lambda receives `advisor_id = 'null'` (a truthy string)
which never matches any architect field — so it degrades to full pseudonymization
rather than book-scoped. Use empty string `''` as fallback for `advisorId`
(and optionally clean up the others to match, but `advisorId` is the critical one):

```javascript
advisorId: decoded.advisorId || ''
```

## Deploy

After committing, this requires a Terraform deploy of the portal-auth pipeline:
- `bash infra/aws/lambda/ci/build-and-upload.sh portal-auth portal_authorizer`
- `.tools/terraform.exe -chdir=infra/aws/terraform/portal-auth plan`
- `.tools/terraform.exe -chdir=infra/aws/terraform/portal-auth apply`
- Verify 0-diff
- Tag: `portal-auth-v1.6.0`

## Dependencies

None. This can start immediately (independent of .012).

## Acceptance Criteria

- [ ] `advisorId` added to portal_authorizer context object
- [ ] Fallback is empty string `''`, not `'null'`
- [ ] Code committed on CLOUD branch
- [ ] Terraform deploy: portal-auth-v1.6.0 at 0-diff
