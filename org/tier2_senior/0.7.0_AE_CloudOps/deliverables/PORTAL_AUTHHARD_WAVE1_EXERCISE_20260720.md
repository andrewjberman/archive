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

## REMAINING -- account-dependent (need a provisioned test account)
- WS-1 counter reset-on-success (a correct login clears the counter).
- WS-2a disabled-user `/auth/refresh` -> **HTTP 500 + NO token minted**; active-user refresh still 200.
- WS-8 set-time: `<12` rejected, passphrase-with-spaces accepted, breached-list entry rejected; **existing sub-12 user still logs in** (no lockout).
- WS-1 WAF *block* behavioral (100-req burst): rule verified live-present; full block-exercise available but not run against prod (login-flood tradeoff).

Blocked on a test-account decision (see RAVC). WAF-block-burst optional on CTO~B/CVO request.
