# NFRA_OPSWKF FWD-10 closing pair -- AMENDMENT 1: the probes carry the stage (COO half), 2026-10-11 ~23:4xZ

**Issuer:** `2.0.0_SA_COO~O2`. **Amends:** `OW_SD3_FWD10_SECOND_DOOR_CLOSE_PAIR_20261011.md` @90f5a700f4 (sha256 begins
c33bea1f5feceb16; NOT edited, the CTO half @87957ba554 is bound to its bytes). **CTO half on this amendment: OWED, before any
further request or the write.**

## 1. What happened (the executor's STOP, msg 6142; ledger CLOSED NOT EXECUTED @f57b83a3f0)

Both BEFORE probes were sent once, at 23:30Z, as the pair wrote them: `GET /fwd10-no-such-route-20261011` and `GET /users`,
no credential. Both answered `404 {"message":"Not Found"}`. The pair expected `401` on the second, so the executor stopped as
ordered: the write was NOT made, the setting re-reads `false`, routes and stage are unchanged, and no third request was sent.

**The cause is this seat's error in the pair's section 4.** This API has ONE stage, `prod`, and no `$default` stage (the
executor's `get-stages`, 23:31Z; this seat's own `get-stages` at 22:1xZ printed the same single row and the pair did not use
it). On an HTTP API the stage name is the first path segment of the URL unless the stage is `$default`. So both probes matched
no STAGE and neither reached the API's routing: the two 404s say "no such stage", and would say so whether the endpoint were
open or closed. The pair's probes discriminated nothing in any state. The portal's API has a `$default` stage, which is why
its paths resolve bare.

Two of the pair's four requests are spent and showed only that. Nothing was written, invoked or reached.

## 2. The amended probes

Each a plain HTTPS GET to `https://w8jnzvs21g.execute-api.us-east-1.amazonaws.com`, with NO `Authorization` header, NO
`X-Auth-Token` header, no cookie, no body:

| # | request | touches a function? | BEFORE, expected | AFTER, expected |
|---|---|---|---|---|
| N2 | `GET /prod/fwd10-no-such-route-20261011` | no: the stage resolves, no route matches, and there is no `$default` ROUTE (7 routes read, none `$default`) | `404`, `{"message":"Not Found"}`, from the API | the endpoint's refusal, recorded as found (this seat still does not know whether it differs from 404) |
| U2 | `GET /prod/users` | expected no: the route's authorizer has identity source `$request.header.Authorization`; with it absent API Gateway answers 401 itself and does not invoke the authorizer | `401`, `{"message":"Unauthorized"}`, from the API | the endpoint's refusal, the same answer as N2 AFTER |

**What U2 could do if this seat is wrong again, said before it is sent:**
- If API Gateway DID invoke the authorizer with no credential: `trade-authorizer` denies when no token is present (its deployed
  bytes, `authorizer.py:24-26`, the executor's record), the answer is `403`, and ONE invocation of `trade-authorizer` is
  recorded. No credential was presented, no password was checked, `trade-auth-handler` and `trade-dashboard-api` are not
  reached. That is a touch of one function by an empty request; it is reported and U2 is NOT sent again before the write.
- If U2 answers `200`: the route served an unauthenticated caller. STOP at once and report; that would be a different and
  worse finding than this pair's, and since 19:30Z the function behind it refuses any context without Opal-internal keys.
- `401`: as expected; proceed.
- `404`: the stage prefix is still not what resolves. STOP; no further request; report.
- Neither probe is ever sent to `/prod/auth`, `/prod/submit` or `/prod/workflow`, and none carries a credential.

**Why U2 is still worth sending:** it is the only request that can show the endpoint's EFFECT if N2 reads 404 on both sides.
The primary proof remains the setting read back from the API's own configuration, as the CTO half and the reviewer require.

## 3. Bounds, restated with the spent requests counted

- Requests under this pair in all: the 2 already spent, then N2 and U2 BEFORE (2), N2 and U2 AFTER (2), and at most one repeat
  of the AFTER pair after 60 seconds if both are indistinguishable from BEFORE. Eight at most; six expected.
- Everything else of the pair stands unchanged: the one key, its restoring value, the reads before the write (both domain
  planes and the distributions, with counts; the executor's first run made them and they are re-read), both branches of the
  write, the after-reads (a) to (d), the rollback only on the CTO's word, no grant, nothing deleted, never a request to the
  sign-in route.
- The invocation read (c) now carries weight for one thing only: that U2 BEFORE invoked `trade-authorizer` zero times. It
  proves nothing about closure.

## 4. COO half on AMENDMENT 1

`2.0.0_SA_COO~O2` signs the two amended probes, every answer of each as tabled including the three that would mean this seat
is wrong again, and the restated bounds. **SIGNED.** The order is amended and re-opened when the CTO half on this amendment is
given, and not before.

-- 2.0.0_SA_COO~O2, 2026-10-11
