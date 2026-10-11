# Four functions behind the portal authorizer: what a non-internal caller can do

Read by hand by 0.9.0_WK_NFRA_OPSWKF~7 at commit 43ec0f10ff (worktree HEAD at read time), task order NFRA_OPSWKF.TO-OW-s1.
Read: the handler source of the four functions (every file each handler imports from its own folder), the Terraform route
declarations, and `workflow_handler.py` for the trade follow-on. NOTHING WAS CALLED: no AWS, no URL, no deployed service.
Deployed bytes are never established by this record (stated once here; it applies to every section below). "Non-internal
caller" = a verified caller whose authorizer context `tier` is not `internal` (a client login, another firm's user, or a
service token with tier `service` and no firm). The record states what the code does; it rates nothing and proposes nothing.

## trade-submission-handler

routes: 1
POST /api/general/trades/submit

(Also reachable: `OPTIONS /{proxy+}` is NONE-auth but its target is the data proxy, not this function; the handler's own
OPTIONS branch is at `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:163-165`.)

non_internal_caller: CAN -- any caller whose authorizer context carries an email, whatever its tier or firm, creates a PENDING_APPROVAL trade submission row, sends the approvers-group an SES email, and may bind its own trade_request ticket; a caller with no email (e.g. a service token) gets 403.

basis:
- Route carries the CUSTOM authorizer: `infra/aws/terraform/shared-infra/apigateway-portal/routes.tf:343-350`; the integration is
  `infra/aws/terraform/shared-infra/apigateway-portal/integrations.tf:15-24`.
- The handler reads the authorizer context at `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:184-186`
  and DECIDES on exactly two things: the email is non-empty (`infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:187-190`, 403 otherwise) and a body
  `initiator_email`, if present, equals it (`infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:191-195`). `tier`, `role`, `firmRole`, `firmId`,
  `allowedFirmIds`, `userType` are never read in the handler (the only other claim read is `name`, recorded at
  `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:210`, which decides nothing).
- The trade-users table is read for the submitter (`infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:215-216`) but only to snapshot `groups` into the audit
  event; a missing row or empty groups changes nothing (`or []`, `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:216`), the row is still written.
- The write: a new item with status PENDING_APPROVAL, fund, securities, comments, attestations, optional model_securities and
  parent_submission_id all taken from the body (`infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:225-294`), stored by `put_item` at
  `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:300-319`. The fund is not checked against any list of funds the caller may use.
- With `parent_submission_id` in the body, the handler appends a SUPERSEDED_BY audit event to that existing submission by
  `update_item` (`infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:328-344`); no check that the caller initiated the predecessor.
- Email: the approvers group is looked up and `send_approval_request` sends SES mail to them
  (`infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:346-357`; SES client and `send_raw_email` at
  `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/email_utils.py:24`, `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/email_utils.py:111-121`;
  group lookup `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/email_utils.py:28-45`).
- Ticket bridge: a `ticket_id` in the body is checked for existence, type, `created_by == caller email`, fund match and
  attestations (`infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:107-123`, called at `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:198-206`), then bound with a conditional
  `update_item` (`infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:126-147`, `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:303-307`). A non-internal caller can therefore only bind
  tickets it filed itself.
- The response returns the stored submission (`infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:359-365`).
- Later refusal, step on (`infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py`): approve, reject and
  execute require a trade-users row (`infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py:230-233`, 403 "not found") and group membership
  (`infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py:154-171`; `approvers` at `infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py:287` and `infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py:358`; `executors` at
  `infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py:439`). So a submitter with no trade-users row or no groups cannot advance, approve, reject or execute its
  own or any submission; nothing in the workflow handler deletes or refuses the already-stored row, which stays
  PENDING_APPROVAL. The submission therefore is created and left pending; nothing in the code read removes it.
- Ticket fence: a submission with `origin == 'ticket'` is refused at execute with 409 before any write, S3 put or email
  (`infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py:415-426`), and the handler sets `origin` to `ticket` only on the ticket path
  (`infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:306-307`). A submission with no ticket_id has no such fence from this code.

not_established: whether the authorizer ever issues an empty `email` for a service token (the handler's 403 depends on it);
whether SES sending limits or the approvers group size in the live table bound the email volume; whether any
non-code control (WAF, CloudFront behaviour) narrows who reaches the route; deployed bytes.

## opal-research-pull-enqueue

routes: 1
POST /api/private/research/pull

non_internal_caller: CAN -- any caller the authorizer verifies can post a ticker and make the function overwrite packs/<ticker>/status.json in the harvest bucket with state REQUESTED and put a pull request on the SQS queue the box-side consumer drains; the handler reads no caller claim at all.

basis:
- Route carries the CUSTOM authorizer: `infra/aws/terraform/harvest/api-gateway.tf:104-110`; integration `infra/aws/terraform/harvest/api-gateway.tf:95-102`.
- The handler never reads `requestContext.authorizer`. The only reference to `requestContext` is a shape test that the event
  looks like an API Gateway proxy event (`infra/aws/lambda/research/pull_enqueue/lambda_function.py:51`); the payload is the
  JSON body (`infra/aws/lambda/research/pull_enqueue/lambda_function.py:47-66`). Nothing is decided on who the caller is.
- Decision made on the body only: a non-empty string `ticker` or 400 (`infra/aws/lambda/research/pull_enqueue/lambda_function.py:63-66`, `infra/aws/lambda/research/pull_enqueue/lambda_function.py:78-80`).
- Write 1: `put_object` of `packs/<security_key>/status.json` with state REQUESTED
  (`infra/aws/lambda/research/pull_enqueue/lambda_function.py:82-98`); `security_key` is the ticker with surrounding space stripped and inner spaces turned to
  underscores, nothing else sanitised (`infra/aws/lambda/research/pull_enqueue/lambda_function.py:39-40`). The module docstring says this write deliberately
  overwrites an existing status object (`infra/aws/lambda/research/pull_enqueue/lambda_function.py:20-22`).
- Write 2: `send_message` to the queue with ticker, key and time (`infra/aws/lambda/research/pull_enqueue/lambda_function.py:100-105`). The docstring names the box-side
  consumer that drains it (`infra/aws/lambda/research/pull_enqueue/lambda_function.py:16-17`); what the consumer then does (a Bloomberg pull) is outside this file and
  is not read here.
- Returns 202 with the key and time (`infra/aws/lambda/research/pull_enqueue/lambda_function.py:108`). No read of data is returned.
- Terraform sets the bucket and queue the function writes to (`infra/aws/terraform/harvest/api-gateway.tf:84-88`).

not_established: what the box consumer does with a message (its source was not in this cell's list), whether it validates the
ticker; whether the queue or the bucket carries any deployed-side limit; deployed bytes (the Terraform comment at
`infra/aws/terraform/harvest/api-gateway.tf:77-83` itself says deployed bytes differ from source on one variable).

## opal-portal-data-proxy

routes: 11
GET /metadata/yang
GET /v1/health/data-availability
GET /v1/market/rsi
GET /v1/market/rsi/details
GET /v1/metadata/yang
GET /v1/sentiment/fear-greed
GET /v1/sentiment/fear-greed/details
GET /v1/sentiment/keywords
POST /v1/sentiment/keyword-intelligence
OPTIONS /{proxy+}   (authorization NONE)
$default   (console-only catch-all, not in Terraform; its authorization setting is not in the repository)

non_internal_caller: CAN -- any caller the authorizer verifies reads every dataset the proxy serves (market, AUM, positioning/model holdings, valuation, macro, news, sentiment) because the handler never reads the caller context, and POST keyword-intelligence only reads cached or stored data and spends no OpenAI quota.

basis:
- Ten routes are declared in Terraform at `infra/aws/terraform/shared-infra/apigateway-portal/routes.tf:246-316`,
  `infra/aws/terraform/shared-infra/apigateway-portal/routes.tf:326-332` (OPTIONS, authorization_type NONE) and
  `infra/aws/terraform/shared-infra/apigateway-portal/routes.tf:409-416`; the first nine carry the CUSTOM authorizer.
  The integration `s7ntfz4` and the `$default` catch-all route `khcd4f1` are console-only
  (`infra/aws/terraform/shared-infra/apigateway-portal/integrations.tf:41-44`). The count of 11 includes `$default`.
- The handler never reads the authorizer context. Its only reads of the event are method, path, path parameters, query string,
  body and headers (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2097-2104`, `infra/aws/lambda/portal_data_proxy/lambda_function.py:2378`);
  `session_tracker.py` reads headers, query string and request id only
  (`infra/aws/lambda/portal_data_proxy/session_tracker.py:90-121`). A search of both files for `authorizer`, `firmId`, `tier`
  and `claims` finds no match in the handler code.
- Router: one chain of `if method and path` branches, each handed nothing about the caller
  (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2138-2390`); an unknown path returns 404 with a route list (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2396-2444`). Because the
  router matches on the path after stripping `/prod` and `/v1` (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2110-2113`), every branch below is
  reachable through the `$default` route as well as the declared ones, if `$default` carries the authorizer (not
  established).
- What is served, all from S3 JSON or DynamoDB tables, none filtered by caller: market metrics and tickers
  (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2145-2174`), AUM summary, flows, timeseries, metrics, account distribution and non-model assets
  (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2180-2204`), peer performance (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2211-2212`), positioning data, attribution, allocation
  summary and the model holdings from the pickle (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2227-2244`), valuation, correlations, macro, factor tilts,
  capital market assumptions, returns (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2251-2321`), articles, trending topics and sentiment
  (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2328-2371`). Buckets and tables are named at `infra/aws/lambda/portal_data_proxy/lambda_function.py:92-106`.
- POST keyword-intelligence: body keyword only (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2376-2387`); handler reads the intelligence table
  (`infra/aws/lambda/portal_data_proxy/lambda_function.py:1469-1500`), S3 keyword metadata and the articles table (`infra/aws/lambda/portal_data_proxy/lambda_function.py:1508-1618`), then returns the
  cached result or the "evolving" card; the source states no OpenAI call is made at request time
  (`infra/aws/lambda/portal_data_proxy/lambda_function.py:1661-1675`). `_get_openai_api_key` exists (`infra/aws/lambda/portal_data_proxy/lambda_function.py:1380-1398`) but this route does not call it
  on any path read.
- Writes: the handler has no `put_item`, `put_object`, `update_item` or `delete_*` call (search of the file finds none). The one
  side effect is the session tracker's CloudWatch `put_metric_data`
  (`infra/aws/lambda/portal_data_proxy/session_tracker.py:221-250`), and the handler prints the whole event, including the
  authorizer context, to the log (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2094`). Warm ping `?warm=1` returns at once
  (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2120-2131`). OPTIONS returns 200 with no data (`infra/aws/lambda/portal_data_proxy/lambda_function.py:2097-2099`).

not_established: whether `$default` (khcd4f1) carries the authorizer, and what other routes the console holds against the
integration; whether the authorizer itself refuses some tiers on some paths before the handler (the authorizer is outside this
cell); whether the pickle/model reader at `get_model_data` (`infra/aws/lambda/portal_data_proxy/lambda_function.py:1837`) was read in full for any write (it was
not traced line by line; the file search for write calls found none); deployed bytes.

## opal-portal-content-api

routes: 3
GET /api/scoped/portal-content
PUT /api/scoped/portal-content/{surfaceId}
DELETE /api/scoped/portal-content/{surfaceId}

non_internal_caller: PARTLY -- GET returns every stored content override to any verified caller with no claim check, while PUT and DELETE refuse unless the context firmId equals opal-capital (tier is never read, so the test is the firm, not the tier).

basis:
- All three routes carry the CUSTOM authorizer: `infra/aws/terraform/portal-content/main.tf:148-163`.
- Router: method and path only (`infra/aws/lambda/portal_content/lambda_function.py:158-177`). GET with no tail goes to
  `get_all_overrides()` (`infra/aws/lambda/portal_content/lambda_function.py:170-171`), which is handed no event, so it cannot read the caller. It scans the whole
  table and returns each override's body, `updated_at` and `updated_by` (`infra/aws/lambda/portal_content/lambda_function.py:84-98`). `updated_by` is the editor's
  email (`infra/aws/lambda/portal_content/lambda_function.py:133`).
- PUT and DELETE are handed the event (`infra/aws/lambda/portal_content/lambda_function.py:172-176`). Claims are read at `infra/aws/lambda/portal_content/lambda_function.py:66-73`
  (`email`, `userType`, `firmId`; the default for a missing firmId is `unknown`). The single decision is
  `actor.get("firmId") == INTERNAL_FIRM_ID` (`infra/aws/lambda/portal_content/lambda_function.py:76-79`, constant from the environment with default
  `opal-capital` at `infra/aws/lambda/portal_content/lambda_function.py:43`). On a false result both return 403 (`infra/aws/lambda/portal_content/lambda_function.py:102-104`,
  `infra/aws/lambda/portal_content/lambda_function.py:144-146`) before any table access. `tier`, `role`, `firmRole` and `allowedFirmIds` are not read.
- For a caller that does pass: PUT validates the surface id and a body up to 8192 bytes, then `put_item` with the previous bodies
  kept (`infra/aws/lambda/portal_content/lambda_function.py:105-139`); DELETE removes the row (`infra/aws/lambda/portal_content/lambda_function.py:147-153`).
- A non-internal caller whose firmId is not `opal-capital` therefore cannot write or delete; it can read all overrides.

not_established: whether the authorizer can issue `firmId` equal to `opal-capital` to a caller whose `tier` is not `internal`
(the handler decides on firmId alone, so the answer depends on how the authorizer fills that claim; the authorizer is outside
this cell); the deployed value of `INTERNAL_FIRM_ID`; deployed bytes.

## What is the same and what differs

| function | reads data | writes or creates a record | spends money or quota | none |
|---|---|---|---|---|
| trade-submission-handler | returns the stored submission it just made; reads the trade-users row and (ticket path) the caller's own ticket | yes: new PENDING_APPROVAL submission; ticket link; SUPERSEDED_BY event on a named predecessor | yes: SES email to the approvers group per submission | no |
| opal-research-pull-enqueue | no | yes: overwrites packs/<key>/status.json; queue message | yes, by consumer design: queue message drained by the box-side pull consumer (consumer not read) | no |
| opal-portal-data-proxy | yes: all served datasets, no caller filter | no (a CloudWatch metric and a full-event log line only) | no (no OpenAI call on any path read) | no |
| opal-portal-content-api | yes (GET: all overrides, no claim check) | PUT and DELETE only for firmId equal to opal-capital; refused otherwise | no | no |

Same in all four: none of the four handlers reads `tier`; the data proxy and the enqueue function read no caller claim at all; the
trade submission handler decides on email only; the content API decides on firmId only, and only on its two write verbs.
