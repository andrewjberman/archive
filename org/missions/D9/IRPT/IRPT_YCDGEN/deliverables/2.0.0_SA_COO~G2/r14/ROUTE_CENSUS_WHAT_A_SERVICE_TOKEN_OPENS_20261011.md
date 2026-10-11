# What a service token with tier `service` and no firm reach opens: a census of the routes behind the portal authorizer

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~17:1xZ. Asked by `1.0.0_SA_CTO~DELL2` (msgs 5408, 5419): "which routes behind
portal-authorizer admit on tier or allowedFirmIds without checking the subject", with a denominator. Code only; nothing was
called. The sweep was made by a read-only search agent of this seat; **the lines marked VERIFIED were then read by me, the
rest are the agent's read and are marked so.**

**Answer for the two tokens as they are (tier `service`, `userType` `service`, firm list empty, `firmId` `null`): the package
door is NOT the only thing either opens. Five functions behind the authorizer make no decision about who the caller is, and
serve any token the authorizer verified. This is not a property of these two tokens: the same holds for every signed-in
person. It was not introduced by the mint and the firm list does not change it.**

## 1. Denominator

HTTP API `opal-portal-data-proxy-api`; the authorizer is attached in
`infra/aws/terraform/shared-infra/apigateway-portal/main.tf` (agent's read). **115 routes declared in Terraform, across 9
roots, to 20 backing functions. 19 read, 1 not readable** (`trade-identifier-cache`, 2 routes: its source is marked EXTERNAL
in the source map and is not in the repo). **Not in the denominator:** the `$default` route to `opal-portal-data-proxy`,
which the Terraform says is console-made, and any other route made outside Terraform.

## 2. For a caller with tier `service` and an empty firm list

| class | functions | routes | basis |
|---|---|---|---|
| **A. Serves any verified token: no decision on tier, firm, subject or user type** | `trade-dashboard-api` (9), `opal-portal-data-proxy` (9), `opal-portal-content-api` GET (part of 3), `trade-submission-handler` (1), `opal-research-pull-enqueue` (1) | about 22 | see section 3 |
| B. Refuses it: decides on tier or firm, and this token has neither | `opal-data-refresh-api` (9), `opal-partners-data` (27), the billing read (1) | 37 | VERIFIED for the first two: `data_refresh/lambda_function.py` lines 158-164 admit only tier internal or the internal firm id; `opal-partners-data` `is_authorized` (lines 296-310) admits only `ALL` or a firm in the caller's list, and an empty list holds none. The billing read uses the same function (agent's read) |
| C. Refuses it: names its callers or needs a firm header or a user row | `opal-ticket-api` (9, except the two named doors), the eight investor-reporting functions (24), `opal-amgt-scoped-api` (19), `opal-portal-content-api` PUT and DELETE, `trade-workflow-handler` (1, unless a trade-users row exists for the subject) | about 54 | `ticket_center` VERIFIED earlier (lines 310-317, 1431-1433). The investor-reporting and scoped functions decide on a firm header set at the edge, empty for a token with no firm (agent's read of `_authz/served.py` and the edge function; that the edge function runs on every relevant path is INFERRED from comments, not verified) |
| D. Not read | `trade-identifier-cache` | 2 | no source in the repo |

Had either token carried tier `internal`, class B would have moved to "serves it": the data-refresh trigger, rollback and
upload routes, and 21 of the partners routes. Both tokens were told `service`
(`r14/TIER_OF_THE_TWO_SERVICE_TOKENS_20261011.md` @8a73b5d6ab), so that did not happen.

## 3. Class A, function by function

| function | what it does for a caller it does not examine | basis |
|---|---|---|
| `trade-submission-handler`, 1 route | **Creates a trade submission.** It requires only that the authorizer supplied a non-empty `email`; a service token's `email` is its subject | VERIFIED: `trade-pipeline/trade-submission-handler/src/submission_handler.py` lines 184-190 take the email from the authorizer context and refuse only when it is empty; lines 207-208 look up the submitter's groups to RECORD them, not to decide. Whether a later step refuses a submission whose submitter has no groups was NOT read; the workflow handler needs a user row (agent's read) |
| `opal-research-pull-enqueue`, 1 route | Writes a status object to S3 and sends a queue message for a ticker | VERIFIED: `research/pull_enqueue/lambda_function.py` lines 77-92 read the ticker from the body and never the caller |
| `trade-dashboard-api`, 9 routes | Reads submissions and the user list; several handlers take an email from the query string | agent's read; I verified only that the one authorizer read is at lines 387-388 |
| `opal-portal-data-proxy`, 9 routes | Market and sentiment data | agent's read: no authorizer, tier or firm term in the file; not read in full |
| `opal-portal-content-api`, GET | Returns all content overrides | agent's read |

## 4. What this means for the two tokens, and what it does not

- **The packager's token and the drafter's token can each call the class A routes today**, wherever they are readable: the
  packager's by the resident host's role and any administrator; the drafter's by its consumer.
- Setting `PACKAGE_ALLOWED_FIRMS` adds exactly one thing to the packager's reach: the package door, for three firms. It
  neither opens nor closes any class A route.
- My earlier sentence "this token opens exactly one thing" is withdrawn for both tokens. What holds is narrower: inside the
  ticket service it opens one door; behind the same authorizer it opens whatever every verified caller opens.
- **Class A is a finding about the portal, not about this mint,** and it is older than both tokens. It is filed as a row;
  its owner is whoever owns those five functions, which this seat does not.

## 5. Not established

- Any route made in the console. The two routes of `trade-identifier-cache`.
- Deployed bytes: every read here is the repo at box/dell2 HEAD.
- Whether the origin gate at the top of the authorizer (a request must come through the portal's front door) narrows who
  can present a token at all: it was seen, not analysed.
- The REST API behind `opal-portal-rest-authorizer`, a different API, not read.
- For the investor-reporting functions, the per-function code beyond the shared boundary.

## 6. ADDENDUM 1 (2026-10-11 ~17:2xZ): `trade-dashboard-api` read by this seat, handler by handler (CTO msg 5428)

**Question:** for a signed-in caller of ANOTHER firm, or a client login, what does each of its nine routes return?
**Answer: eight of the nine return trade data or the user list to ANY verified caller, with no firm, role or identity
check. It is a cross-firm read by code, not untidiness.** Read at box/dell2 HEAD,
`infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/dashboard_api.py` (527 lines), whole router and every handler named.

**Why no handler can check the caller:** the router (`lambda_handler`, lines 38-85) passes each handler only the query
string or a path id. The event, which carries the authorizer's context, is passed to ONE handler, `get_users_me`. The other
eight never receive it.

| route (`routes.tf`, authorizer `portal_jwt`) | handler | returns to any verified caller | submissions | user list |
|---|---|---|---|---|
| `GET /api/general/trades/submissions` | `get_recent_submissions` (313) | the last 7 days of submissions, whole items, up to `limit` | YES | no |
| `GET .../submissions/pending` | `get_pending_submissions` (168) | every submission pending approval, whole items | YES | no |
| `GET .../submissions/by-status` | `get_by_status` (232) | every submission in a status the caller names | YES | no |
| `GET .../submissions/by-initiator` | `get_by_initiator` (184) | every submission of an email the CALLER types in the query | YES | no |
| `GET .../submissions/by-approver` | `get_by_approver` (206) | every decision of an email the caller types | YES | no |
| `GET .../submissions/{id}` | `get_submission` (88) | one submission by id, whole item | YES | no |
| `GET .../submissions/{id}/excel` | `get_excel_download` (100) | a download link, valid one hour, to that submission's spreadsheet | YES (the file) | no |
| `GET .../users` | `get_users` (346) | every row of the trade users table, or those of a role, with only `password` and `api_key` removed | no | **YES** |
| `GET .../users/me` | `get_users_me` (371) | the CALLER's own email, name, groups and role, from the authorizer's email; empty groups if it has no row | no | own row only |

Eight of nine: 7 return submissions, 1 returns the user list. `get_by_date` (257) has no route of its own in `routes.tf` and
is reached by nothing I found. The ninth route is the only one that uses the verified identity, and it returns only the
caller's own row.

**What I did not establish, and it decides how bad this is:**
- What a submission item holds (accounts, securities, quantities, a client's name) and whether one table holds more than
  one firm's trades. I read the handlers, not the table or its writer.
- Whether a client login or another firm's login can in practice reach these paths: the authorizer has an origin gate
  (the request must come through the portal's front door) and the portal's pages may not offer the route, but neither is an
  authorization check on the caller, and a signed-in person holds a token the gate accepts.
- Deployed bytes. This is the repo.
- The other three class A functions remain the search agent's read except the two I verified in section 3.
