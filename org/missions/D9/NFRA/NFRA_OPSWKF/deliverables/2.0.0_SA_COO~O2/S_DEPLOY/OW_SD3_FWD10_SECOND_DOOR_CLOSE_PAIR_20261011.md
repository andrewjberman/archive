# NFRA_OPSWKF FWD-10 -- closing the second door: packet and COO half (never-widen), 2026-10-11

**Issuer:** `2.0.0_SA_COO~O2` (dell2). **Executor:** `0.7.0_AE_CloudOps~DELL2`. **CTO half owed by:** `1.0.0_SA_CTO~DELL2`.
**PRD:** v0.10 @47d579b505, FWD-10; ratified-text half SIGNED (prd-signoff.py status read 23:08Z: SIGNED, current). **Row:** NFRA_OPSWKF-D2-S11.
**Source record:** `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/NFRA_OPSWKF_SECOND_DOOR_AUTHORIZER_BYTES_AND_TRAFFIC_20261011.md` @855e7e938e.

## 1. The act (write set = ONE literal key)

| # | Key | Change | Writers of this property (counted) |
|---|---|---|---|
| K1 | HTTP API `trade-submission-api` (`w8jnzvs21g`), property `DisableExecuteApiEndpoint` | `false` -> `true`, by `aws apigatewayv2 update-api --api-id w8jnzvs21g --disable-execute-api-endpoint` | 1 today: nobody. The API is not in Terraform (`infra/aws/terraform/trade-pipeline/apigateway.tf:15-17` calls it dormant and console-only; 1 mention of its id in that file, a comment). The executor's CLI call is the only writer; no stack will revert it and none records it, so THIS packet and the ledger are the record |

**The restoring value:** `false`, by `aws apigatewayv2 update-api --api-id w8jnzvs21g --no-disable-execute-api-endpoint`.

Nothing else: no route, integration, authorizer, stage, permission, function, key, table or Terraform file is touched; nothing is
deleted. Deleting the API, its two functions and their secret is Andrew's act and is not here.

## 2. What was read first (this seat, 23:1xZ, live)

- `get-api w8jnzvs21g`: `DisableExecuteApiEndpoint` **false**; endpoint `https://w8jnzvs21g.execute-api.us-east-1.amazonaws.com`;
  CORS configured on the API itself (`AllowOrigins *`, methods incl. OPTIONS).
- **Domain mappings: none.** `get-domain-names` for the account's HTTP/WebSocket API plane returned **0 domain names**, no
  further page; so no custom domain carries this API. NOT read by this seat: the REST-API plane's custom domains
  (`apigateway get-domain-names`), which can also map an HTTP API; the executor reads it at step 2 with its count.
- **CloudFront:** a filter of `list-distributions` for an origin naming `w8jnzvs21g` returned no row. That zero carries no
  denominator from this seat; the executor repeats it printing the number of distributions scanned.
- Stage `prod`: AutoDeploy true, no access logging, no detailed metrics.
- Routes (22:1xZ): 7, none of them `$default`; so a path the API does not have matches no route and reaches no function.

## 3. Blast radius

- **After the act, the default endpoint answers no caller,** which with no custom domain is every way into this API: the
  sign-in route, and the six routes to the dashboard, submit and workflow functions.
- **Who is cut off: nobody shown.** 30 days: no request metric exists for the API; 0 invocations of its sign-in function and of
  its authorizer (controls 54,824 and 7). Before that window is NOT established (no access log). The portal's pages call the
  portal's API (`7k3ed8px20`), which this act does not touch. A caller nobody knows of, if one exists, starts failing at once;
  that is the outcome's own intent and the reason the act is reversible in one call.
- **The Lambda resource-policy statements for this API stay** (`apigateway-w8jnzvs21g` on three trade functions). They admit only
  API Gateway acting for this API, so with its endpoint disabled they admit nothing; removing them is part of the deletion, not this.
- **Not narrowed by this act:** a principal with `lambda:InvokeFunction` can still invoke any of the functions directly (the
  executor's principal can; the rest of IAM is not enumerated). That is not a public door.

## 4. The proof on the deployed API: what answers, and one thing this seat is NOT sure of

PRD v0.10's read is "ONE request that touches no function and carries no credential (a route the API does not have), answered by
the API itself BEFORE the act and refused at the endpoint AFTER it".

**The caution, stated before the act rather than discovered in it:** on an HTTP API, a path with no route is answered `404
{"message":"Not Found"}` by API Gateway. This seat's recollection, NOT verified against the service today, is that an HTTP
API whose default endpoint is disabled ALSO answers `404` to every request (a REST API answers 403; an HTTP API does not). If
that is so, the PRD's read is 404 before and 404 after and shows nothing. So the pair makes TWO requests each side, records
status, the `message`, and the response header NAMES (not values) of each, and says which pair of answers discriminates:

| # | request (no credential, no body) | touches a function? | BEFORE, expected | AFTER, expected |
|---|---|---|---|---|
| N | `GET /fwd10-no-such-route-20261011` | no: no route matches, and there is no `$default` route | `404`, `Not Found`, answered by the API | the endpoint's refusal: `404` or `403` (recorded as found) |
| U | `GET /users` with NO `Authorization` header | no: the authorizer's identity source is `$request.header.Authorization`, and API Gateway answers `401` itself when the identity source is absent, without invoking the authorizer | `401`, `Unauthorized`, answered by the API | the endpoint's refusal, the same answer as N AFTER |

- **U is the discriminating read if N is 404/404:** it moves from 401 to the endpoint's refusal. That U invoked nothing is not
  taken on trust: `trade-authorizer`'s `Invocations` is read flat across the act (section 6 (c)), and if U's BEFORE answer is
  anything but `401`, STOP: do not send it again.
- **Neither request goes to `/auth`,** and no request of any kind is ever made to `/auth` by any seat. Neither carries a
  credential, a body or an `Authorization`/`X-Auth-Token` header. Four requests in all (N and U, before and after), no more.
- **The setting itself is read directly:** `get-api` reads `DisableExecuteApiEndpoint` `true` after the act. That is the
  primary proof of the write; the two requests are the proof of its effect.
- **If the PRD's wording must change** because N does not discriminate, that is the CTO's (ENDPOINT); the run records what it
  found and does not decide it.

## 5. Both branches of the act

- **`update-api` succeeds and `get-api` reads `true`:** proceed to the AFTER reads.
- **`update-api` is denied** (the executor's principal lacks `apigateway:PATCH` on this API): STOP. Nothing changed. No grant is
  added; the act goes whole to a seat that holds it (the laptop's cloud-ops seat), carried by `0.0.0_AB_MSTR~DELL2`.
- **AFTER reads show the endpoint still answering as BEFORE** (N `404 Not Found` from the API with U still `401`): the setting
  did not take effect. Re-read `get-api`; wait 60 seconds once (the service propagates); read once more; if unchanged, report.
  Do not restore: a setting that reads `true` and does nothing is reported, not toggled.
- **Anything answers 5xx, or a function's invocation count moves:** report at once.

## 6. After-reads (the executor, each printed with its time)

- **(a)** `get-api`: `DisableExecuteApiEndpoint` true; every other property of the API as BEFORE (name, endpoint, CORS, route
  selection), compared field by field; `get-routes` still 7; `get-stage` unchanged.
- **(b)** N and U AFTER, as section 4.
- **(c)** `Invocations` (AWS/Lambda, Sum, 1-minute period, from 30 minutes before the act to 10 minutes after) for
  `trade-auth-handler` and `trade-authorizer`: 0 datapoints or all zero, i.e. flat across the act; with a control in the same
  query shape that shows the metric is not blind. If the metric lags, say so and read it again at the end.
- **(d)** The portal's own door is unaffected: `get-api 7k3ed8px20` `DisableExecuteApiEndpoint` as BEFORE; no request is made
  to it.

## 7. Rollback

One call: `aws apigatewayv2 update-api --api-id w8jnzvs21g --no-disable-execute-api-endpoint`, then `get-api` reads `false`.
It re-opens the door as it stood, the sign-in route included, so it is used only on the CTO's word or if a caller Opal
depends on is shown to have broken.

## 8. Who may change it

- The executor's principal `cloudops-dell2-agent-user`: NOT measured by this seat (an HTTP API update has no dry-run); it is
  measured by the act, and a denial is a STOP (section 5). No grant is added.
- Everyone else: not enumerated. Any principal with `apigateway:PATCH` on the API can restore or re-disable it; nothing in
  Terraform holds the value.

## 9. COO half

`2.0.0_SA_COO~O2` signs the blast radius above for key K1, both branches of the write, every answer of N and U as tabled, the
caution in section 4, and the rollback. The ledger entry is the executor's, opened before the BEFORE reads and closed after (c).

**COO half -- SIGNED.** The ratified-text half of PRD v0.10 read SIGNED at 23:08Z (`prd-signoff.py status`). The
order is cut when the CTO half is given, and not before.

-- 2.0.0_SA_COO~O2, 2026-10-11
