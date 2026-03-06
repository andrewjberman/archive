# Auth Architecture — Opal Portal

**Owner:** 0.5.0_AE_OpalETL
**Date:** 2026-03-06
**Status:** Complete
**Source:** Derived from audit of auth-handler, portal-authorizer, api-client, db.ts, jwt.ts, and ADVI J1/J2/J3 task orders.

---

## 1. Stack Summary

| Component | Implementation |
|---|---|
| Identity store | DynamoDB `opal-users-v2` |
| Partner identity | DynamoDB `opal-partner-49financial` |
| Auth Lambda | `opalinvest-auth-handler` (Node.js/TypeScript) |
| Token type | Custom JWT, RS256 asymmetric |
| Key storage | Secrets Manager `opal/auth/jwt-private-key` + `opal/auth/jwt-public-key` |
| Password hashing | bcryptjs, 12 rounds |
| Access token TTL | 15 minutes |
| Refresh token TTL | 7 days (HttpOnly cookie) |
| Terraform module | `infra/aws/terraform/portal-auth/` |
| Auth API endpoint | `https://7k3ed8px20.execute-api.us-east-1.amazonaws.com` (separate API Gateway) |

**Not Cognito.** All identity, password hashing, and token signing is implemented in-house.

---

## 2. DynamoDB: opal-users-v2

### Key Schema

| Record type | PK | SK |
|---|---|---|
| User profile | `USER#usr_xxxx` | `PROFILE` |
| Firm membership | `FIRM#firmId` | `MEMBER#userId` |
| Firm metadata | `FIRM#firmId` | `META` |

### GSIs

| GSI Name | Hash Key | Use Case |
|---|---|---|
| `email-index` | `email` | Login lookup by email |
| `firmId-index` | `firmId` | List users in a firm |

### User Record Fields

| Field | Type | Notes |
|---|---|---|
| `email` | String | Login identifier, GSI key |
| `password_hash` | String | bcrypt 12-round hash |
| `name` | String | Display name |
| `role` | String | `admin` or `user` |
| `tier` | String | `internal` or `advisor` |
| `firmId` | String | e.g., `opal-capital`, `49financial` |
| `regionId` | String | Optional region |
| `officeId` | String | Optional office |
| `userType` | String? | `Dev` = superadmin; absent for normal users |
| `allowedPages` | String[] | Page-level access gates (e.g., `advisor-intelligence`) |
| `allowedTabs` | Record | Per-page tab access gates |

### Firm Hierarchy

Firms have a `parentFirmId` field on their META record. The portal-authorizer
recursively scans `FIRM#*/META` records to build descendant sets for admin scoping.

---

## 3. DynamoDB: opal-partner-49financial

Created by ADVI-J1 (AE CloudOps, shared-infra-v1.3.0).

### Key Schema

| PK | Notes |
|---|---|
| `email` | Simple partition key — no sort key |

### GSI

| GSI Name | Hash Key |
|---|---|
| `ByAdvisorRole` | `advisorRole` |

### Fields

| Field | Type | Notes |
|---|---|---|
| `email` | String | PK; matches `opal-users-v2` email |
| `advisorKey` | String | BD gold layer advisor slug (e.g., `arch_jane_smith`) |
| `advisorName` | String | Display name |
| `advisorRole` | String | `architect`, `implementor`, `admin`, or `viewer` |
| `createdAt` | String | ISO timestamp |
| `createdBy` | String | Admin who created the record |

### Purpose

Bridge between portal users (opal-users-v2) and BD gold layer advisor identity.
Populated manually at advisor onboarding. Read by auth-handler at login/refresh
for users whose `allowedPages` includes `advisor-intelligence`.

---

## 4. JWT Structure

### Token Types

| Type | TTL | Transport | Algorithm |
|---|---|---|---|
| Access token | 15 min | `Authorization: Bearer` header, localStorage | RS256 |
| Refresh token | 7 days | HttpOnly cookie `refresh_token` | RS256 |

### Access Token Claims (AccessTokenPayload)

| Claim | Type | Notes |
|---|---|---|
| `sub` | string | User email |
| `name` | string | Display name |
| `role` | string | `admin` or `user` |
| `tier` | string | `internal` or `advisor` |
| `firmId` | string | Firm identifier |
| `regionId` | string | Region |
| `officeId` | string | Office |
| `userType` | string? | `Dev` = superadmin bypass |
| `allowedPages` | string[] | Page-level access list |
| `allowedTabs` | Record | Tab-level access per page |
| `advisorKey` | string? | ADVI J2: advisor slug from partner table |
| `advisorName` | string? | ADVI J2: advisor display name |
| `advisorRole` | string? | ADVI J2: advisor role from partner table |
| `iss` | string | `opal-portal-auth` |
| `aud` | string | `opal-portal-api` |

Refresh token includes `type: 'refresh'` claim (validates it's not an access token being used as refresh).

---

## 5. Auth Handler Routes

Lambda: `opalinvest-auth-handler`
API Gateway: `https://7k3ed8px20.execute-api.us-east-1.amazonaws.com`
Source: `infra/aws/opalinvest_dev/lambda/auth-handler/src/`

| Method | Path | Description |
|---|---|---|
| POST | `/auth/login` | bcrypt verify + JWT issue |
| POST | `/auth/refresh` | Refresh token → new access token |
| POST | `/auth/logout` | Clear refresh cookie |
| POST | `/auth/forgot-password` | Password reset flow |
| POST | `/auth/reset-password` | Apply reset token |
| GET | `/auth/me` | Return current user from JWT |
| POST | `/auth/change-password` | Authenticated password change |
| POST | `/auth/admin/users` | Admin CRUD: create/list/delete/force-reset |

### Login Flow

1. GSI lookup on `email-index` → get user record
2. `bcrypt.compare(password, user.password_hash)` (12 rounds — ~150ms)
3. `updateLastLogin(userId)`
4. If `user.allowedPages?.includes('advisor-intelligence')`:
   - `getPartnerIdentity(email)` from `opal-partner-49financial`
   - Errors are caught and logged — login does NOT fail on partner table errors
5. `generateAccessToken(user, partnerIdentity?)` → 15-min RS256 JWT
6. `generateRefreshToken(user)` → 7-day RS256 JWT, set as HttpOnly cookie
7. Return `{ accessToken, user: { email, name, role, tier, ... } }`

### Refresh Flow

1. Extract `refresh_token` from HttpOnly cookie (NOT from body/header)
2. `verifyRefreshToken(token)` → decode and verify RS256 signature + `type: 'refresh'`
3. `getUser(sub)` → re-read user from DynamoDB (picks up any permission changes)
4. `getPartnerIdentity(email)` if needed
5. `generateAccessToken(user, partnerIdentity?)` → new 15-min access token
6. Return `{ accessToken }` (refresh token is NOT rotated)

### Graceful Degradation (Partner Identity)

If `opal-partner-49financial` has no record for the email → JWT omits
`advisorKey`, `advisorName`, `advisorRole` entirely. User can log in and
access all non-advisor-scoped pages normally. Partner table errors also
degrade gracefully — not thrown as 401/403.

---

## 6. Portal Authorizer

Lambda: `opal-portal-authorizer`
Source: `infra/aws/users/lambda/portal-authorizer/index.mjs`
Response format: HTTP API v2 simple response `{ isAuthorized, context }`

Attached to: API Gateway HTTP API routes for `/api/scoped/*` and `/api/private/*`

### Flow

1. Extract `Authorization: Bearer {token}` from request headers
2. Verify RS256 signature using `opal/auth/jwt-public-key` (cached in Lambda memory)
3. `computeAllowedFirms(decoded)`:
   - `tier=internal` OR `userType=Dev` → `'ALL'`
   - `tier=advisor AND role=admin` → own firmId + all descendants (recursive Scan)
   - `tier=advisor AND role=user` → own firmId only
4. Attach context to request:

```
email, name, tier, role, firmId, officeId, regionId, userType,
allowedFirmIds (string: 'ALL' or comma-separated),
allowedPages (JSON stringified string[]),
allowedTabs (JSON stringified Record),
advisorKey (string or 'null'),
advisorName (string or 'null'),
advisorRole (string or 'null')
```

Downstream scoped Lambdas read via:
```
event.requestContext.authorizer.advisorKey
event.requestContext.authorizer.allowedFirmIds
```

### Firm Hierarchy (recursive descent)

`getAllDescendants(firmId)`: Scans `opal-users-v2` for `SK=META AND parentFirmId=firmId`,
then recursively descends. Builds full set of descendant firmIds for admin-scoped
multi-tenant data access.

---

## 7. API Route Architecture

Three route families served from the same CloudFront distribution:

| Path prefix | Handler Lambda | Auth gate |
|---|---|---|
| `/auth/*` | `opalinvest-auth-handler` | None (public) |
| `/api/general/*` | `opal-portal-data-proxy` | JWT validation via auth-validator-edge (CloudFront function) |
| `/api/scoped/*` | `opal-data-refresh-api` | Lambda Authorizer (opal-portal-authorizer) |
| `/api/private/*` | `opal-data-refresh-api` | Lambda Authorizer (opal-portal-authorizer) |

### Client API Config (portal/src/api/api-client.ts)

```
API_BASE_URL  = VITE_PORTAL_API_URL ?? ''            // CloudFront same-origin
AUTH_API_BASE = VITE_AUTH_API_URL   ?? 'https://7k3ed8px20.execute-api.us-east-1.amazonaws.com'
```

Auth API calls go directly to the auth Lambda's API Gateway (bypassing CloudFront).
All other API calls go through CloudFront (same-origin in production, Vite proxy in dev).

### 401 Refresh Mutex

`api-client.ts` implements a single-mutex refresh pattern:
- `isRefreshing`: boolean flag
- `refreshPromise`: shared Promise

When a 401 is received:
1. If not refreshing: start `POST /auth/refresh`, store promise
2. If refreshing: await the shared promise
3. On success: update localStorage token, retry original request
4. On failure: clear localStorage → redirect to `/login`

Prevents parallel refresh storms when multiple concurrent requests all 401
at the same time (e.g., after token expiry between polling intervals).

---

## 8. ADVI Partner Identity Stream (J1/J2/J3)

These task orders wired advisor identity from the BD gold layer into the JWT:

| Task | Owner | Deliverable | Tag |
|---|---|---|---|
| J1: Create opal-partner-49financial table | 0.7.0_AE_CloudOps | DynamoDB table + IAM on auth role | `shared-infra-v1.3.0` |
| J2: auth-handler reads partner table | 0.4.0_DT_ClientPlatform | advisorKey/Name/Role injected into JWT at login/refresh | `portal-auth-v1.1.0` |
| J3: portal-authorizer passes claims | 0.4.0_DT_ClientPlatform | advisorKey/Name/Role in Lambda requestContext | `portal-auth-v1.2.0` |

**J4** (Books tab auth gating, DE + RD scope) is unblocked by J3 completion.
It uses `advisorKey` from requestContext to scope S3 path, and `advisorRole`
to determine L1/L2/viewer render tier.

---

## 9. Data Refresh + SSCN Pipeline Endpoints

The `opal-data-refresh-api` Lambda (other Terraform module, AE-owned) serves two pipeline families:

### Yang DataRefresh Flow

| Step | Endpoint | Notes |
|---|---|---|
| 1 | POST `/api/scoped/data-refresh/upload-urls` | Presigned S3 PUT URLs for `data-refresh/pending/{uploadId}/` |
| 2 | PUT (direct to S3) | Client uploads files to presigned URLs |
| 3 | POST `/api/scoped/data-refresh/trigger` | Lambda auto-generates manifest, copies to `uploads/`, triggers Step Functions |
| 4 | GET `/api/scoped/data-refresh/status/{id}` | Poll Step Functions execution |
| 5 | GET `/api/scoped/data-refresh/history` | List past executions |
| 6 | POST `/api/scoped/data-refresh/rollback` | Restore prior execution (version-based or re-processing) |

**Recognized file types for auto-manifest generation:**

| Type key | Pattern |
|---|---|
| `data_pkl` | `data*.pkl` |
| `model_pkl` | `model*.pkl` |
| `cma_excel` | `*cma*.xlsx` |
| `peer_excel` | `*peer*.xlsx` |
| `attribution_excel` | `*attribution*.xlsx` |
| `saa_excel` | `*saa*.xlsx` |
| `regression_csv` | `*regression*.csv` |

### SSCN (Security Scanner) Flow

| Step | Endpoint | Notes |
|---|---|---|
| 1 | POST `/api/scoped/security-scanner/upload-url` | Presigned PUT URL to `security_scanner/uploads/{asOf}/Screening_DIVZ_IDVZ_{asOf}.xlsx` |
| 2 | PUT (direct to S3) | Client uploads FactSet Excel |
| 3 | (automatic) | S3 event → `opal-security-scanner-processor` Lambda |
| 4 | GET `/api/scoped/security-scanner/factors` | Factor metadata (284 factors, asOf date) |
| 5 | GET `/api/scoped/security-scanner/universe/{id}/data` | Security-level universe data |
| 6 | GET `/api/scoped/security-scanner/universe/{id}/scanner` | Percentile scores per factor |

SSCN files do NOT go through the DataRefresh/Yang pipeline. The two flows use
separate S3 prefixes and separate trigger Lambdas.

---

## 10. Security Notes

- `userType: 'Dev'` in JWT = superadmin bypass. Grants ALL firm access in authorizer
  and unrestricted access in data-refresh Lambda.
- All `/api/scoped/*` routes require valid JWT — the Lambda Authorizer blocks unauthorized
  requests before they reach the handler Lambda.
- SSCN presign URLs expire in 15 minutes (shorter than DataRefresh 1-hour URLs).
- Refresh token is stored in HttpOnly cookie — not accessible to JavaScript.
  Access token in localStorage is accessible but short-lived (15min).
- The data-refresh Lambda has a development fallback (Method 3 in `validate_user_type`)
  that allows unauthenticated access if no authorizer context is present. This should
  only occur in local/direct invocation testing — API Gateway enforces the Lambda
  Authorizer before the Lambda is invoked.
