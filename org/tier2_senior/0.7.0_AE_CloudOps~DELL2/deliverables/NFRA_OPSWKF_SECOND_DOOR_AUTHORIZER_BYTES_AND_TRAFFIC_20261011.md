# NFRA_OPSWKF -- the second door: authorizer bytes, /auth bytes, and traffic

**Order:** `NFRA_OPSWKF.TO-READ-S4.second-door-authorizer-bytes-and-traffic-dell2.md` (cell `OW-s-5`),
read-only, for `1.0.0_SA_CTO~DELL2` to write an outcome on (its msg 5959).
**Seat:** `0.7.0_AE_CloudOps~DELL2`. **Date:** 2026-10-11.
**The API:** `trade-submission-api`, id `w8jnzvs21g`, stage `prod`, created 2026-01-06T20:33:04Z
(row `NFRA_OPSWKF-D2-S11`).
**NO call was made to that API or any route of it, and neither function was invoked.** Every answer
below is read from the DEPLOYED package or from a metric. No secret, key, token, password hash or
stored user value appears in this record: env keys, tables and fields are named, never their values.

---

## trade-authorizer

Downloaded 22:47:13Z from `get-function`'s code location into a scratch folder outside the
repository; read as text, never executed. Package 1218 bytes; **1 member**:

| member | bytes | sha256 (first 32) |
|---|---|---|
| `authorizer.py` | 2964 | `6f52eb550481c2d2a07831bd33c38154` |

**(a) What it verifies.** Not a JWT, despite the module's name and docstring: the credential is a
**two-part** string `payload_b64.signature_b64` (`authorizer.py:66-70`; three parts are rejected at
:67). The signature is **HMAC-SHA256** over the base64 payload keyed on env `JWT_SECRET` (:73-78) and
compared with `hmac.compare_digest` (:80), so the comparison is constant-time. Because the token has
no header segment, **there is no `alg` field to confuse and none is checked**. Expiry: `exp` from the
payload must be >= `time.time()` or it denies (:36-38), and `payload.get('exp', 0)` means a payload
carrying **no** `exp` is treated as expired and denied. No issuer, audience, subject or nonce is
checked. The env key is `JWT_SECRET`, which **is set on the function** (read live), so the hardcoded
fallback literal present in the deployed bytes at `:12` is **not in effect at this reading**; its
value is not reproduced here.

**(b) The context it returns to the integration -- the decisive answer.**
`allow_policy` returns `isAuthorized: true` with a context of **exactly three keys**
(`authorizer.py:101-105`), each taken from the token payload with `''` as the default:

context_keys: email, name, role

| key the releases read | present? | where its value comes from |
|---|---|---|
| `tier` | **ABSENT** | not set anywhere in the file |
| `firmId` | **ABSENT** | not set anywhere in the file |
| `email` | present | `payload.get('email', '')` (:102) |
| `role` | present | `payload.get('role', '')` (:104) |
| `userType` | **ABSENT** | not set anywhere in the file |
| `allowedFirmIds` | **ABSENT** | not set anywhere in the file |

(`name` is the third key present, `payload.get('name','')` at :103.)

**(c) On a missing or bad credential.** `deny_policy()` -> `{"isAuthorized": false}` on every failing
path: no token (:24-26), signature mismatch or undecodable payload (:31-33, via :80-82 and :92-94),
expired (:36-38), and **any** exception (:43-47). It fails closed.

**(d) Origin or source check.** **None.** No origin, referer, host or source-IP test appears in the
file. The token may arrive as `Authorization: Bearer <token>` or as an `X-Auth-Token` header (:50-60).

---

## trade-auth-handler

Downloaded 22:49:34Z the same way. Package 280997 bytes; **13 members** over **3 top-level names** --
its own code is **one file at the root**, the other **12 members are a vendored library**:

| top-level name | members | what it is |
|---|---|---|
| `auth_handler.py` | 1 | **the function's own code**, 5936 bytes, sha256 `0fc11a1b91b8d39d0406dcaaafdfcac3` |
| `bcrypt` | 5 | vendored library |
| `bcrypt-5.0.0.dist-info` | 7 | vendored library metadata (bcrypt 5.0.0) |

Only `auth_handler.py` was read; the library members were not.

**(a) What `POST /auth` accepts.** A JSON body with **`email`** (lowercased and stripped, :36) and
**`password`** (:37). Both are required or it answers 400 (:39-40). An `OPTIONS` preflight answers 200
(:27-28).

**(b) What it checks them against.** The table named by env **`USERS_TABLE`**, defaulting to
**`opal-users-v2`** (:16) -- **the same canonical users table the portal uses**. It finds the user by
the **`email-index`** GSI and then re-reads the full item by `PK`/`SK` (:92-104), **with a table
`scan` fallback** if the GSI query raises (:108-114). It requires the item's **`status`** field to
equal `active` (:49-50). The password is compared with **`bcrypt.checkpw`** against the item's
**`passwordHash`** field (:53-54, :117-131); an empty stored hash returns False (:119-120) and any
bcrypt exception returns False (:129-131). No item value was read by this seat.

**(c) What it issues on success.** A **two-part HMAC token**, `payload_b64.signature_b64` (:154) --
the same shape the authorizer validates. Signature: **HMAC-SHA256** over the base64 payload keyed on
env **`JWT_SECRET`** (:147-152). Claims: **`email`, `name`, `role`, `exp`, `iat`** (:136-142) -- and
**no `tier`, `firmId`, `userType` or `allowedFirmIds`**. Lifetime: **`TOKEN_EXPIRY_HOURS` hours**,
default **24** (:18, :140); that env key is **not set** on the function (read live), so 24 hours
applies. **The signing key is this function's own HMAC secret, named `JWT_SECRET`; it is NOT the
portal's signing key** -- the portal signs RS256 with the secret `opal/auth/jwt-private-key`, a
private key, whereas this is a symmetric HMAC shared secret, a different algorithm and different key
material. Separately worth the CTO's eye: the **response body** returns `tier` and `firmId` to the
caller (:69-76) although the **token** carries neither.

**(d) Rate limit, lockout or origin check.** **None of the three.** No attempt counter, no lockout, no
backoff and no origin test appear in the file; CORS is `Access-Control-Allow-Origin: '*'` (:185). On
success it does **write** `lastLogin` and `updatedAt` on that user's own row (:165-174).

**(e) Env key NAMES** (read live, names only): **`JWT_SECRET`, `USERS_TABLE`**. The code also reads
`TOKEN_EXPIRY_HOURS` (:18), which is not set, so its default stands.

---

## What the three functions answer through this API today

A reading of code and context keys. **Nothing was called.**

- **`trade-dashboard-api` -- REFUSES every caller of this door.** FWD-8's check admits only
  `tier` exactly `internal` **or** `firmId` exactly `opal-capital`, and the authorizer supplies
  neither key (`authorizer.py:101-105`), so both comparisons fail on absent values and the function
  answers 403 before serving anything.
- **`trade-submission-handler` -- REFUSES every caller of this door**, for the same reason: FWD-9's
  `_require_internal` reads those two keys out of the authorizer context before the body is parsed.
- **`trade-workflow-handler` -- unchanged by this project**, so it receives the same three-key context
  (`email`, `name`, `role`) and decides by its own rule, which OW-s-1's record gives as a
  `trade-users` row plus a group. That rule was not re-read here, so whatever it admitted before today
  it still admits.

So today's two releases make this door **fail closed** for the two functions they changed, and leave
the third exactly as it was.

---

## Traffic, 30 days

Window 2026-09-11T22:53:39Z to 2026-10-11T22:53:39Z, daily `Sum`. The `list-metrics` denominator was
printed **first**, so "no datapoints" can be told from "no such metric".

- `list-metrics` AWS/ApiGateway `Count`, `ApiId=w8jnzvs21g`: **0 metric rows**.
  The same call for the portal API `7k3ed8px20`: **2 metric rows** (`ApiId` alone, and
  `ApiId`+`Stage=$default`).
- `get-metric-statistics` for `w8jnzvs21g`: **0 datapoints** with `ApiId` alone, and **0 datapoints**
  with `ApiId`+`Stage=prod`.

requests_30d: NO-METRIC

control_portal_api_30d: 54824  (31 datapoints, so the query shape and window do find traffic)

- AWS/Lambda `Invocations`, `Sum`, same window: **`trade-authorizer` 0** (0 datapoints) and
  **`trade-auth-handler` 0** (0 datapoints). Control in the same namespace and shape:
  `trade-submission-handler` reads **7** over 2 datapoints, so the Lambda metric is not blind.
- **Access logging: not enabled.** `get-stage` returns `AccessLogSettings: null` (with
  `AutoDeploy: true`, last deployment `1opl8h`), so there is no access log to point at. **No log line
  was read.**

Three independent measures therefore agree that nothing has called this door in 30 days, and each has
a control that would have shown traffic if there were any.

---

## not_established

- **Whether the API was ever called before this window.** CloudWatch metric retention bounds the
  question; `0 metric rows` means no metric exists today, not that none ever did. The absence of stage
  access logging means there is no second record to check.
- **Who holds a credential `POST /auth` would accept.** No item of `opal-users-v2` was read -- no
  count of rows carrying a `passwordHash`, no `status` census, nothing. The route accepts any
  `active` user of the canonical table whose bcrypt hash matches, and how many that is was not
  measured.
- **Whether the two `JWT_SECRET` values are the same.** The authorizer and the handler each read an
  env key of that name; neither value was read, so that they agree is inferred from the token shapes
  matching, never measured. Nor was either secret's strength, age or rotation examined.
- **Whether the authorizer's hardcoded fallback is reachable.** Its env key is set at this reading, so
  the literal at `:12` is not in effect now; nothing in the bytes prevents it applying if that key
  were ever unset.
- **`trade-workflow-handler`'s own rule.** Not re-read here; taken from OW-s-1's record.
- **Authorizer result caching on the API.** Not read, so how long an `isAuthorized` decision might be
  reused is unknown.
- **Anything outside this account's CloudWatch.** A WAF, VPC flow log or CDN record was not consulted.
- **The source of either function.** The source map marks both EXTERNAL with no files, and neither was
  found in the repository, so the deployed package is the only text there is -- these readings cannot
  be compared against a committed original.

Nothing above is a rating or a proposed fix: the outcome is `1.0.0_SA_CTO~DELL2`'s to write.
