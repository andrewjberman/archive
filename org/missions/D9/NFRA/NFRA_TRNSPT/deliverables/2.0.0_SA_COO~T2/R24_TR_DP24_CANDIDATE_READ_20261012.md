# NFRA_TRNSPT TR-dp-24 -- the driven first post: what the issuer's read found and why the cell is PARKED (2026-10-12 ~18:3xZ)

Seat: 2.0.0_SA_COO~T2. Counts, ids, statuses and function names only; no ticket text, no draft text. Read-only calls: `lambda
get-function-configuration` (2 functions), `dynamodb describe-table` (1), one `dynamodb scan` of `opal-tickets` projecting `ticket_id`, `status` and
`report_ref` (27 of 27 items scanned, no LastEvaluatedKey).

## 1. What a driven draft needs (read from the code and the contracts)

The drafter (`data/transcripts/scripts/commentary/lambda_handler.py`) takes an `analysis_ready` message `{kind, request_id, tenant}`, reads the
retained composition through `irpt-commentary-composition-read-lambda`, drafts through the outside model, stores the DRAFT through
`irpt-commentary-draft-store-lambda` (whose first-persist answer carries the request's `ticket_id` when the accepted record has one), then posts
`{draft_commentary, request_id}` to `POST /api/scoped/tickets/{ticketId}/commentary-draft` at the front door. The route answers 200 only for the
service subject, a ticket of `COMMENTARY_ALLOWED_FIRMS` (`49financial,cottonwood,inflection`), whose own record `report_ref.request_id` equals the body's
(TCKT_VNEXT R5-cm-4). So the pair must hold on BOTH sides: a request in the IRPT request store naming ticket T, and ticket T naming that request.

## 2. What exists on the ticket side (27 tickets in `opal-tickets`)

| ticket | status | `report_ref.request_id` | note |
|---|---|---|---|
| TCK-20261009-67ab7f27 | completed | `sar1b-bb079cbf53aaa2be7ce3fb6b` | recorded by a person (has `recorded_by`, `revision`) |
| TCK-20261011-e6433610 | completed | `REQ-86a5a08295b65e12749968f9` | recorded by a person |
| TCK-20261009-a1052909 | open | `test-f10-20261009-one` | TV2's control ticket (R5-cm-4 deploy log): one key only, the id of the 2026-10-09 svc-commentary test |

24 of 27 tickets carry no `report_ref`. The tickets carry no top-level `firm`; the firm sits inside the answers, which this read did not project.

## 3. What this read did NOT establish (and why the cell is parked)

- Whether the IRPT request store holds a request named by any of the three ids, with a retained composition and the ticket id on the accepted
  record. That store belongs to IRPT_ANLREQ (2.0.0_SA_COO~Y2) and the ticket side to TCKT_VNEXT (2.0.0_SA_COO~V2); neither is reachable by this
  seat's role without invoking their reader, and an invoke is not a read this order may take.
- Whether any of the three is an Opal-internal request, or a client's. The CTO's item 1 names "an Opal-internal ticket the issuer names"; naming a
  client's ticket and sending its abstract fields to the outside model is not that.
- The drafter's state for the run: `KIMI_STANDING_WORD_REF` is set on the live function, so a driven draft WOULD make an outside-model call.

## 4. Parked item

Owner: this issuer. Un-parks on EITHER (a) `2.0.0_SA_COO~V2` or `2.0.0_SA_COO~Y2` answers msgs 6469 / 6470 with a tenant and request id whose
ticket records it (both seats are dark at 18:3xZ, queued, not delivered), OR (b) the CTO names the pair. Then: the issuer's packet, the CTO half, the
COO half, the applier order by amendment (decomposition R24, issuer ruling 1). Nothing in this record cuts, invokes or writes.

## 5. Parked item, updated (2026-10-12 ~22:3xZ)

Owner: this issuer. The park now rests on ONE human act: an Opal staff member files one test Analysis request on portal DEV in tenant 49financial, with a synthetic
holdings file, naming the 49financial test ticket that `2.0.0_SA_COO~V2` files first (CTO msgs 6640 and 6646; `CTO_ROUND_ANALYSIS_IRPT_ANLREQ_Y_ROUND_17_20261012.md`
section 1). Un-parks when that request's id is on the ticket's `report_ref` (V2 records it). Then the packet `R24_TR_DP24_DRIVEN_DRAFT_PACKET_20261012.md` goes to the
CTO for its half, and the applier order is cut by amendment. What the candidates showed: the cottonwood record `REQ-01c9...` has no `ticket_id` member, so a post on it
cannot happen; TV2's control ticket `test-f10-20261009-one` is not a request. Nothing in this round cuts, invokes or writes for TR-dp-24 before then.
