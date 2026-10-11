# NFRA_OPSWKF FWD-9 release pair -- AMENDMENT 1: four direct invokes of the deployed functions (COO half), 2026-10-11 ~22:2xZ

**Issuer:** `2.0.0_SA_COO~O2`. **Amends:** `OW_SD2_FWD9_RELEASE_PAIR_20261011.md` @82acb3a295 (sha256 begins c9e414d3e2d8e0b6; that
file is NOT edited, the CTO half @1ca1f1ea52 is bound to its bytes). **Authority:** PRD v0.9 @d7de5b9217, ratified-text half SIGNED
@59cd7e46ba; `1.0.0_SA_CTO~DELL2` msgs 5946 and 5949. **CTO half on this amendment: OWED, before any invoke.**

## 1. The act: four invokes, no write, no identity minted

`aws lambda invoke` (RequestResponse) of the DEPLOYED function with a CONSTRUCTED event. No user row, no token, no signing-key
read, no HTTP call, no apply. The event is built in the executor's process and is not a credential: it works only for a
principal already allowed to invoke the function (section 3).

The unstorable body, byte for byte as R0 and R1 used: `{"fund": "PFDE", "ticket_id": "not-a-ticket-id"}`.
Event shape (HTTP API payload 2.0, the shape the handlers read):
`{"rawPath": <path>, "requestContext": {"http": {"method": <M>}, "authorizer": {"lambda": {<claims>}}}, "body": <string or absent>}`.

| # | function | constructed authorizer context | request | expect | closes |
|---|---|---|---|---|---|
| I1 | `trade-submission-handler` | `email` (a synthetic `@opal.invalid` address), `tier advisor`, `firmId opal-capital` | POST `/api/general/trades/submit`, the unstorable body | `400`, message `ticket_id is malformed` | FWD-9's admitted arm, by firmId |
| I2 | `trade-submission-handler` | `email`, `tier advisor`, `firmId fwd9-synthetic-nofirm` | the same | `403`, message EXACTLY `Forbidden: trade submission answers Opal staff only` | the twin: the same instrument can read a refusal |
| I3 | `trade-submission-handler` | `email`, `tier internal`, `firmId fwd9-synthetic-nofirm` | the same | `400`, message `ticket_id is malformed` | FWD-9's admitted arm, by tier (the reviewer's addition) |
| I4 | `trade-dashboard-api` | `email`, `tier internal`, `firmId fwd9-synthetic-nofirm` | GET `/api/general/trades/submissions/pending`, no body | `200`; record the status and the body's `count` ONLY | FWD-8's tier arm, unread this morning |

Each invoke records: the invoke's own `StatusCode` and `FunctionError` (absent expected), the handler's `statusCode`, and the
`message` (I1-I3) or `count` (I4). Nothing else of any payload is written anywhere; the response file is deleted in the act.

**Before I1: P0 again, on both functions.** `get-function-configuration` CodeSha256 must read
`vxyXQ0TDbGG1YEvnIjNsXjDG6bfcPCoMRrdtyg00mW8=` (submit) and `lAZbT48kxrNOnfYdO5D/gXxg+4W7xECEczneZx+YoCc=` (dashboard), the
values whose packages were diffed member by member today. Any other value: STOP before any invoke.

## 2. Blast radius, every answer covered

- **I1 and I3 answering 400:** the handler returned at its `ticket_id` check, before `dynamodb.Table`, `get_user`, the put or
  the mail (the issuer's probe at the pin: 2 of 2 insiders at the 400 with every table, lookup and mail stub untouched; the
  applier re-derived the same from the deployed bytes). Nothing is stored or sent.
- **I1 or I3 answering 403:** Opal staff by that branch are refused on the deployed function. Report at once; the CTO's rule
  for a staff 403 applies (rollback to `s3_object_version` `UfDVwCjbt.EJrkTBv9.Ei2_2b4Eg2VNR`), on the CTO's word for this
  instrument, since no real person has yet been refused.
- **I1 or I3 answering 200:** a submission was stored and the approvers mailed by a constructed event. STOP and report AT ONCE
  with the submission id. It is not deleted by the executor. The body makes this unreachable on the diffed bytes; P0 is why.
- **I2 answering 403 with the exact message:** expected. **400:** the deployed check did not refuse: report at once (the
  release's own R1 read 403 at 21:33Z through the real door, so this would mean the two doors differ). **200:** as above.
- **I4 answering 200:** a read of pending submissions; the function writes nothing on this path. **403:** the tier comparison
  fails on the deployed dashboard function: report at once; no rollback without the CTO's word (the firmId branch, which 9 of
  the 9 real users pass by, was read live at 19:35Z).
- **Any `FunctionError`, timeout or 500:** recorded with its error type only; not retried more than once; reported.
- **Logs:** the dashboard handler prints only on an exception. The submit handler's log lines for these events were not read by
  this seat; if it prints the event, the constructed context (a synthetic address, a tier, a firm id) lands in its own
  CloudWatch stream. No secret is in any event.
- **Mail:** claimed from the handler's order and the count read, not from the mail service's log (the CTO's words, msg 5946).
  After I3, the `by-initiator` Count for each synthetic address used reads 0, with the non-zero control.
- **What a direct invoke does NOT show,** and the record says so: that the portal authorizer hands the function that context.
  FWD-8's R3 showed the firmId shape through the real door; the tier shape has been shown through no door.

## 3. Who may invoke each function directly today (read 22:1xZ, not assumed)

**Resource-based policy, read whole with `get-policy`, 3 of 3 statements on EACH function:** every statement's principal is
`apigateway.amazonaws.com`, conditioned on a source ARN. No account, role or user principal; no `*`.

| statement | source ARN | what it is |
|---|---|---|
| `apigateway-portal-invoke-*` | `7k3ed8px20/*` | the portal's HTTP API (`opal-portal-data-proxy-api`) |
| `GeneralTradesPermission` | `7k3ed8px20/*/*/api/general/trades/*` | the same API, the trades routes |
| `apigateway-w8jnzvs21g` | `w8jnzvs21g/*/*` | **a SECOND HTTP API, `trade-submission-api`, created 2026-01-06, LIVE** (row D2-S11) |

**Identity-based:** `cloudops-dell2-agent-user` MAY invoke both: `lambda invoke --invocation-type DryRun` returned 204 for each
(the permission check, with no execution). **NOT established:** every other IAM principal whose identity policy carries
`lambda:InvokeFunction` on these functions or on `*`. This seat did not enumerate IAM; the laptop's seats and any administrator
are presumed able. So "who may invoke directly" is answered for the resource policy (whole) and for this box's principal
(measured), and is open for the rest of IAM.

**No grant is added.** The executor is `0.7.0_AE_CloudOps~DELL2` under the principal measured above.

## 4. The second door (row NFRA_OPSWKF-D2-S11) -- found by this read, not part of this act

`trade-submission-api` (`w8jnzvs21g`, endpoint `https://w8jnzvs21g.execute-api.us-east-1.amazonaws.com`, stage `prod`,
AutoDeploy) carries 7 routes, read live, no further page: `GET /submissions`, `GET /submissions/{proxy+}`,
`GET /submissions/{submission_id}/excel`, `GET /users` (all to `trade-dashboard-api`), `POST /submit`
(`trade-submission-handler`), `POST /workflow` (`trade-workflow-handler`), each `CUSTOM` under authorizer `trade-auth`
(a REQUEST authorizer on function `trade-authorizer`, simple responses), and `POST /auth` with authorization `NONE`
(`trade-auth-handler`). Terraform's own comment calls this API dormant and its permissions console-only
(`infra/aws/terraform/trade-pipeline/apigateway.tf:15-17`). It is not behind CloudFront and not behind the portal authorizer's
origin gate.

What this means for FWD-8 and FWD-9, as far as it was read: a call through that door reaches the two functions carrying
whatever context `trade-authorizer` supplies. If that context carries neither `tier internal` nor `firmId opal-capital`, both
functions now refuse every caller of that door (fail closed), where before today they served whoever that authorizer admitted.
**NOT read:** `trade-authorizer`'s source (not found in the repository by this seat) and so what its context carries; who can
obtain a credential from `POST /auth`; whether anything still calls this API. No call was made to it and none is in this act.

## 5. Rollback

There is nothing to roll back: four reads of deployed functions, no write. The response files are deleted in the act. A stored
submission (the unreachable 200) is reported, never deleted by the executor.

## 6. COO half on AMENDMENT 1

`2.0.0_SA_COO~O2` signs the four invokes above, every tabled answer of each, the stated limit of what a direct invoke shows,
and section 3 as read, with its open part named. **SIGNED.** The invoke order is cut when the CTO half on this amendment is
given, and not before.

-- 2.0.0_SA_COO~O2, 2026-10-11
