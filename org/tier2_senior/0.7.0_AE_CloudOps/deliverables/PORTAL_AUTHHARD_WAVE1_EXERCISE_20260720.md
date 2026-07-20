# PORTAL_AUTHHARD Wave-1 -- Deploy + Exercise Report (Rule 22a)

**Executor:** 0.7.0_AE_CloudOps~B · **Lead/arch-gate:** 1.0.0_SA_CTO~B · **LD-0323** · 2026-07-20
**Deploy:** `portal-auth-v1.20.0` · source `70b2560f0` · TF `a6d4f52ed` · deploy-record `067da416e`
**Scope:** WS-1 (login-abuse throttle) + WS-2a (refresh status re-check) + WS-8 (password policy), one auth-handler build.

## Deploy (landed + verified)
- safe-apply of the CTO~B-gated saved plan: **1 added / 3 changed / 0 destroyed**; comp-tagauthz gate PASSED; 0-diff replan = "No changes." Deploy-completion ledger `20260720T1629Z_portal-authhard-wave1` **CLOSED** (3/3 legs proven). No CloudFront-distribution edit.
- Resources: `aws_dynamodb_table.portal_auth_throttle` (created) · `aws_iam_role_policy.auth_permissions` (append-only) · `aws_wafv2_web_acl.opal_cloudfront_protection` (+AuthLoginRateLimit rule) · `aws_lambda_function.auth_handler` (artifact swap, source_code_hash=eTSZUm8eVGheF4tolXuoaOQPDh0nbV7qTle+q+xpJVc=).

## EXERCISE -- account-free battery: ALL PASS (live, against opalinvest.dev)
| # | Check | Result | Evidence |
|---|---|---|---|
| EX-1 | WS-1 per-account login throttle | **PASS** | 8 wrong-pw attempts on one synthetic email -> HTTP `401,401,401,401,401,429,429,429` (5 fails then progressive-cooldown 429). Also = **runtime proof the new code is live**. |
| EX-2 | WS-1 reset/forgot INDEPENDENT limit + enumeration-safe | **PASS** | 7 `/auth/forgot-password` on a synthetic email -> `200,200,200,200,200,429,429`. Independent of the login counter; generic 200 below cap (non-existent email, no enumeration signal). |
| EX-3 | WS-1 structured forensic logs actually emitted | **PASS** | `/aws/lambda/opalinvest-auth-handler`: 6x `{"event":"login_failed","account_hash":"140c8c..","reason":"no_such_account",..}` + `{"event":"auth_throttled","key_type":"login","retry_after_sec":30,..}`. A LOG, not an alarm (no SNS). |
| EX-4 | WS-1 IAM least-privilege (Rule 22a, ONE --resource-arns/call, isolated controls) | **PASS** | simulate-principal-policy on `opalinvest-auth-lambda-role` -> throttle table: GetItem/UpdateItem/DeleteItem = **allowed**; PutItem (isolated negative control) = **implicitDeny**. |
| EX-5 | Real-user path unaffected | **PASS** | first attempt on a fresh email -> 401 (not throttled). |
| WAF | WS-1 per-IP rule LIVE (applied-state) | **PASS (present)** | `get-web-acl` -> `AuthLoginRateLimit` Block/Limit 100/Priority 2; existing `RateLimitRule` (2000/pri1) untouched. |

## WS-2a grep (CTO~B required-confirm -- CLOSED)
`portal/src/contexts/AuthContext.tsx`: `refreshToken()` (L170) throws on ANY non-ok response; every caller `.catch(()=>{})` / `catch{}` (L234, L246-247, L267-269, L441-444; comment L269 "401 interceptor will handle on next API call"). **Nothing branches on the refresh status code** -> no frontend dependency on the current 500-for-disabled. The minimal one-liner (500/indistinguishable) is correct; a future 500->403 map would be grounded-safe but is not this wave.

## EXERCISE -- account-dependent trio: ALL PASS (CTO~B GO on (a); synthetic user, verified-deleted)
Test user `authhard-wave1-test-1784565989@opal.test` (PK `USER#usr_test1784565989`), firmId `authhard-test-firm-doesnotexist` (non-existent -> empty data scope; token firmId claim confirmed = that firm), random <12 password. Atomic create->exercise->delete with a cleanup trap; lifecycle ledger `20260720T1644Z_portal-authhard-wave1-testuser` OPEN@create / CLOSED@verified-delete.

| # | Check | Result | Evidence |
|---|---|---|---|
| A1 | WS-1 counter reset-on-success | **PASS** | 4x wrong (401,401,401,401) -> 1x correct (200, clears) -> 1x wrong = **401 NOT 429** (without reset the 5th fail would 429). |
| A2 | WS-8 existing sub-12 user still logs in | **PASS** | the 11-char (direct-bcrypt-write) password logs in -> 200 (bcrypt length-opaque; no login-time check). |
| A3 | WS-2a disabled-user refresh | **PASS** | active refresh 200; **disable -> /auth/refresh -> HTTP 500 + accessToken minted: NONE**; re-enable -> refresh 200. The core WS-2a security fix, exercised. |
| A4 | WS-2a blast-containment | **PASS** | login token `firmId` claim = `authhard-test-firm-doesnotexist` (non-existent -> zero authorized firm data). |
| A5 | WS-8 set-time `<12` rejected | **PASS** | change-password 11-char newPassword -> rejected (HTTP 500; see follow-up), password unchanged. |
| A6 | WS-8 breached rejected | **PASS** | change-password `password1234` (>=12, on the breached list) -> rejected (HTTP 500), exercising the breached gate independent of the length gate. |
| A7 | WS-8 passphrase-with-spaces accepted | **PASS** | change-password `correct horse battery staple test` -> HTTP 200 accepted. |
| A8 | Test-user LIFECYCLE verified-delete | **PASS** | delete-item + post-delete consistent-read GetItem returns NO Item; independent re-confirm GONE. |

## FULL WAVE-1 ACCEPTANCE: GREEN (WS-1, WS-2a, WS-8) -- pending CVO independent re-run.

## Follow-ups (surfaced, not in Wave-1 scope)
1. **Password-policy rejection returns HTTP 500, not 400.** `validatePassword` throws a message index.ts's error-map has no branch for -> falls to the generic 500. PRE-EXISTING (the old min-8 rejection did the same); the rejection + no-password-change is correct, only the status code is poor UX. A one-line index.ts map (policy message -> 400) would fix it; deferred (touches the error contract, out of the arch-gated WS-8 scope).
2. **WS-8 breached list is a curated top-N head, not the full top-10k.** Expanding needs a one-time SecLists/Pwned-Passwords import (egress off Opal infra -> Andrew's word) or a file drop; swap `breached-passwords.ts`, no other code change.
3. **WS-1 WAF block behavioral (100-req burst) not run** against prod (login-flood tradeoff). Rule verified applied-live (get-web-acl) + EX-1 proves throttling Lambda-side. Available on CVO request.
4. **WS2a 500->403 mapping** for disabled accounts is frontend-safe (grep grounded) but deliberately not taken (keeps login()'s contract; not this wave).
