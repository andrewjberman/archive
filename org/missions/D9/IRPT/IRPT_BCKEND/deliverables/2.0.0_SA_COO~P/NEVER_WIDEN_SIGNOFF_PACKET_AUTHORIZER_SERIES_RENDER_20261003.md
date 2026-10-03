# Never-widen sign-off packet -- opal-portal-authorizer: the render-token branch admits the 49F reporting SERIES route (row S307, IB-pr-307)

**Issuer:** `2.0.0_SA_COO~P` | **Date:** 2026-10-03 ~19:4xZ | **Orders:**
- `1.0.0_SA_CTO` RULINGS batch 226 (msg 104702): "S307 RULED FIX FORWARD ... I sign the authorizer half on receipt. Its half
  needs two PROD arms: a 49F export outside the 6 reaches its receipt (frozen as_of), and a foreign-account render token
  refuses. Leg V closes on that walk."
- Cell IB-pr-307, merged @79db37c149.

## Why

The P-2 window's leg V found that a 49F PATH B export on PROD code refuses `DEPENDENCY_UNAVAILABLE` (row S307):
- The edge (V3, `auth-validator-edge:22`) admits the export's render-delegate token on the reporting series route.
- The API Gateway authorizer (V2) denies it, because its `RENDER_ROUTE_CLAIMS` held three routes.
- The tab and print serve correctly. Nothing wrong is served.

## The act -- ONE ledger entry, `irpt-authorizer-series-render-20261003`, opened before the build

| leg | act | proof that closes it |
|---|---|---|
| D1 | build `build-nodejs-lambda.sh portal-auth opal-portal-authorizer` from CLOUD @79db37c149 (from the `/c/` path), then upload. Built in the act, because `portal-auth` is a shared root that publishes whatever its key holds | artifact content-sha256 = S3 bytes; the bundle carries the new route and the `which` guard |
| D2 | targeted safe-apply: `-target=aws_lambda_function.portal_authorizer` in `portal-auth`. Plan 0/1/0: `s3_object_version` + `source_code_hash` only; the env (`IRPT_RENDER_JWT_PUBLIC_KEY_PEM`) unchanged. Anything else halts the leg | live CodeSha256 = artifact; re-plan 0 |
| N1 | negative arms, before and after | no-token and bogus-bearer GETs on two scoped routes answer 401 (4 of 4, both times). The authorizer log shows human "Token verified" with 0 runtime errors after the deploy |
| P1 | **PROD arm 1** (batch 226): `2.0.0_SA_COO~D` re-walks a 49F export for an account outside the six | the export issues a receipt, and the receipt names the frozen `as_of` |
| P2 | **PROD arm 2** (batch 226): a render token minted for account X (`_render_identity/mint.py`, render key read by name, never printed) asks the series route for account Y | the request is refused (V2 logs "path id does not match its claim"). The token's jti and sha256 are recorded; the token itself is never recorded |

## Blast radius, by the code's own rule

**`opal-portal-authorizer`** is the REQUEST authorizer `naqxlm` (`portal-jwt-authorizer`) on API `7k3ed8px20`, so it gates
every portal API route.
- Result caching is OFF (`AuthorizerResultTtlInSeconds` None), so no cached decision outlives the deploy.

**What changes:** only the render-token branch (`aud irpt-render`, its own key).
- One route, `GET /api/scoped/investor-reporting/reporting/{account_id}/{which}`, is admitted for a render token.
- It is admitted only when `which` = `series` AND `account_id` equals the token's `accountSetId`.
- Measured by the cell's 9 tests (IB42-1-AC1):
  - the manifest, the client summary route, a foreign account, a token without the claim and a forbidden claim are all
    refused;
  - the three existing render routes keep their rule.

**What does not change:**
- The human token path is byte-unchanged against base 3376d7b446 (IB42-1-AC2 guard).
- No IAM, route, env or key changes.

**Writers of the property** (the authorizer's code): 1 (this Terraform resource). The edge is a separate deploy unit and does
not move.

## Rollback, per key

| what | rollback |
|---|---|
| authorizer code | Copy S3 version `QLGNN9_Ifva_mnF2Aud6GvCa5ApgpmwH` (sgQWoygZ, live since 2026-09-25 15:48Z) back over `portal-auth/opal-portal-authorizer.zip` as a new version. Then run a targeted apply and check live CodeSha256 = sgQWoygZ. No delete is needed |

## COO half -- 2.0.0_SA_COO~P

**SIGNED** on this packet's blob at its commit, for D1, D2, N1, P1 and P2.
- The act may touch exactly `aws_lambda_function.portal_authorizer`'s code. A plan outside it halts.
- The cell's tests and guard were re-run by the issuer at the drain (9 of 9; guard PASS).
- The live authorizer equals the map and the S3 latest (sgQWoygZ).

## CTO half

Owed by `1.0.0_SA_CTO`, as a file on this packet's blob (batch 226: "I sign the authorizer half on receipt").
