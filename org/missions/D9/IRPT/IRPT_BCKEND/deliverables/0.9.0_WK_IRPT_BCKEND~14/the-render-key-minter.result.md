# IRPT_BCKEND.TO-IB-rtq-1 -- THE RENDER-KEY MINTER -- result

`0.9.0_WK_IRPT_BCKEND~14`, round 17, cell `IB-rtq-1`. CONTRACTS "THE RENDER IDENTITY" items
1, 2, 3, 6, 8 (minter half), PRD v0.17 `org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md:177-262`.

## What was built

- `infra/aws/lambda/investor-reporting/_render_identity/mint.py` -- the minter module.
  `mint_render_token(bundle, private_key_pem=None, now=None) -> MintResult`. Private key
  material is loaded ONLY from an injectable source (`private_key_pem=` argument or the
  `IRPT_RENDER_JWT_PRIVATE_KEY` env var) -- never hardcoded, never read from the shared
  human-token secret. Grepping the module for the string `jwt-private-key` returns exactly
  3 matches, every one inside the render key's own name
  (`opal/auth/irpt-render-jwt-private-key`); the bare human-token secret name never
  appears.
- `deliverables/0.9.0_WK_IRPT_BCKEND~14/fixtures/irpt_render_jwt_TEST_FIXTURE_{private,public}_key.pem`
  -- the ONE throwaway 2048-bit RSA keypair, generated this round, standing in for the real
  `opal/auth/irpt-render-jwt-{private,public}-key` Secrets Manager entries (NOT created
  this round -- BOUNDS).
- `deliverables/0.9.0_WK_IRPT_BCKEND~14/test_render_mint.py` -- 14 tests, all passing.

## Claim-construction structural refusal (cell requirement (c))

`role` and `tier` are literal constants in `_build_claims` ("renderer" / "render"); there
is no parameter, no bundle field and no branch that can set either to anything else.
`firmRole` and `userType` are never assigned anywhere in the module. Belt-and-braces: if a
caller's bundle carries `role`, `firmRole`, `tier` or `userType` at all, `mint_render_token`
raises `RenderMintRefused` before ever reaching the signing step (see
`_refuse_admin_bypass_keys`), and a second defensive check after claim construction
(`mint_render_token`'s post-`_build_claims` guard) refuses to sign if those values were
ever produced. The chosen arm is REFUSAL, not silent stripping.

## Test run (exact criterion invocation)

```
cd deliverables/0.9.0_WK_IRPT_BCKEND~14 && py -3.12 -m pytest test_render_mint.py -v
```

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\AndrewBerman\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\tmp\wk-irpt-17-14
configfile: pytest.ini
plugins: anyio-4.12.1, langsmith-0.7.17, asyncio-1.3.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 14 items

test_render_mint.py::test_claim_shape_and_values PASSED                  [  7%]
test_render_mint.py::test_exp_minus_iat_within_five_minutes PASSED       [ 14%]
test_render_mint.py::test_jti_unique_across_two_mints PASSED             [ 21%]
test_render_mint.py::test_sub_equals_render_prefix_plus_jti PASSED       [ 28%]
test_render_mint.py::test_decoding_with_wrong_key_fails PASSED           [ 35%]
test_render_mint.py::test_expired_token_fails_decode PASSED              [ 42%]
test_render_mint.py::test_admin_bypass_claims_are_refused[role-admin] PASSED [ 50%]
test_render_mint.py::test_admin_bypass_claims_are_refused[firmRole-admin] PASSED [ 57%]
test_render_mint.py::test_admin_bypass_claims_are_refused[tier-internal] PASSED [ 64%]
test_render_mint.py::test_admin_bypass_claims_are_refused[userType-Dev] PASSED [ 71%]
test_render_mint.py::test_no_admin_bypass_claim_ever_appears_when_bundle_is_clean PASSED [ 78%]
test_render_mint.py::test_missing_bundle_field_is_refused PASSED         [ 85%]
test_render_mint.py::test_no_private_key_source_raises PASSED            [ 92%]
test_render_mint.py::test_private_key_from_env_var PASSED                [100%]

============================== warnings summary ===============================
(6 DeprecationWarning lines from python-jose's own jwt.py:281/:311 -- jose's internal use
of datetime.utcnow(), not this module's code -- 12 warnings total, 0 failures)
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================= 14 passed, 12 warnings in 0.44s =======================
```

`rc=0`. Every arm cell requirement (e) names appears by function name above: claim shape
(`test_claim_shape_and_values`, `test_exp_minus_iat_within_five_minutes`,
`test_jti_unique_across_two_mints`, `test_sub_equals_render_prefix_plus_jti`), the
wrong-key-fails assertion (`test_decoding_with_wrong_key_fails`), the expiry assertion
(`test_expired_token_fails_decode`), and the admin-bypass-claim-refusal assertion
(`test_admin_bypass_claims_are_refused`, all 4 parametrized cases, plus the positive-half
check `test_no_admin_bypass_claim_ever_appears_when_bundle_is_clean`).

## One concrete minted token and its decoded claim set

Minted from a synthetic bundle
(`firm_id=49financial, bundle_id=bundle-test-0001, revision=r7, account_set_id=acct-set-42,
job_id=job-9931, report_id=report-555, delegator_subject=advisor:alice@49financial.example`)
with the fixture private key, decoded with the fixture public key
(`jose.jwt.decode(..., issuer='opal-irpt-render', audience='irpt-render', algorithms=['RS256'])`):

```
TOKEN:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGFsLWlycHQtcmVuZGVyIiwiYXVkIjoiaXJwdC1yZW5kZXIiLCJpYXQiOjE3OTAwODUxNDQsIm5iZiI6MTc5MDA4NTE0NCwiZXhwIjoxNzkwMDg1NDQ0LCJqdGkiOiJyZW5kZXItZDRhNTM4NTY1MmQ0NDM1MmIyYjA0ODhiNjc1NWIwZTIiLCJyb2xlIjoicmVuZGVyZXIiLCJ0aWVyIjoicmVuZGVyIiwiZmlybUlkIjoiNDlmaW5hbmNpYWwiLCJidW5kbGUiOiJidW5kbGUtdGVzdC0wMDAxIiwicmV2aXNpb24iOiJyNyIsImFjY291bnRTZXRJZCI6ImFjY3Qtc2V0LTQyIiwiam9iSWQiOiJqb2ItOTkzMSIsInJlcG9ydElkIjoicmVwb3J0LTU1NSIsInN1YiI6InJlbmRlcjpyZW5kZXItZDRhNTM4NTY1MmQ0NDM1MmIyYjA0ODhiNjc1NWIwZTIiLCJkZWxlZ2F0b3IiOiJhZHZpc29yOmFsaWNlQDQ5ZmluYW5jaWFsLmV4YW1wbGUifQ.VKAXr9i16t7bymh0xAlZdykow0OSQ_g_dNsjxhuv5FobRYHxPuIXvuJCoN8_aWbXeU_--eca1rSi9gWV39ahsEmIJ7M4-Iu8l8aXCifyLz4O4sDOCn6TjTJg1VUf33mlqA0RjH0v5wRj2R2lrrNWp4fRUTwAn8g_cs_chRdemOLc3nmD7YGBdU1f8q5fctXnVrHu7RHZAH0pEI6F2deivCIyI52OoaQC642Z_b-iAFKIpGIzByBkw_WUpPKNdS3tTlO_mi5BqFT-mvN6oJY-2sNnumRxCwj5S-G_qShmqbOMdgx0VFU1OqNLql6XEhK29aws0VB9kEf4G0G0JGr9Lw

DECODED CLAIMS:
{
  "accountSetId": "acct-set-42",
  "aud": "irpt-render",
  "bundle": "bundle-test-0001",
  "delegator": "advisor:alice@49financial.example",
  "exp": 1790085444,
  "firmId": "49financial",
  "iat": 1790085144,
  "iss": "opal-irpt-render",
  "jobId": "job-9931",
  "jti": "render-d4a5385652d44352b2b0488b6755b0e2",
  "nbf": 1790085144,
  "reportId": "report-555",
  "revision": "r7",
  "role": "renderer",
  "sub": "render:render-d4a5385652d44352b2b0488b6755b0e2",
  "tier": "render"
}
```

`exp - iat = 300` (exactly the 5-minute ceiling); `nbf == iat` (0s of minter-introduced
skew, within the 60s verifier leeway PRD item 2 allows); `sub == "render:" + jti`; `role`
`renderer`, `tier` `render`; no `firmRole`, no `userType`, no `role admin`, no `tier
internal` anywhere in the claim set.

## BOUNDS observed

No Secrets Manager entry, no SSM parameter, no AWS API call, no Lambda deploy, no
Terraform change. No edit to `infra/aws/lambda/shared/opal_auth/`. No edit to
`_scope/resolve.py`, `_authz/enforce.py`, `portal-authorizer/index.mjs` or
`auth-validator-edge/index.mjs`. No wiring into B14's real export job call graph --
`mint_render_token` is a standalone, tested module only.

## Environment note (filed as a surprise row, see IRPT_BCKEND-W14-S1)

`python-jose[cryptography]==3.3.0` is confirmed an existing estate dependency (declared in
`infra/aws/lambda/opal_pm_upload_urls/requirements.txt`,
`infra/aws/lambda/opal_pm_snapshot_handler/requirements.txt` and
`infra/aws/lambda/portfolio_optimization_loader/requirements.txt`) but was NOT installed
in this worktree's local `py -3.12` interpreter before this round -- it was installed via
`py -3.12 -m pip install "python-jose[cryptography]==3.3.0"` (a pre-existing estate pin,
not a new dependency) so the criterion's own invocation could run.
