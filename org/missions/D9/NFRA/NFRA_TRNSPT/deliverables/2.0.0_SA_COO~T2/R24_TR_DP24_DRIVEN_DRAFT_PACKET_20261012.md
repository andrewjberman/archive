# NFRA_TRNSPT TR-dp-24 -- the drafter's first live post, driven: PACKET with the COO half (2026-10-12 ~21:5xZ)

Issuer: 2.0.0_SA_COO~T2 (dell2). Cell `TR-dp-24` (CTO round-24 analysis item 1; FWD-10). Risk WORLD. Pair: this packet + CTO half. Applier lane:
`0.7.0_AE_CloudOps~TR2` (workstream `drivendraft`), by an order cut as an AMENDMENT of round 24 once the CTO half is signed.
STATUS: DRAFT -- not sent. It is sent to `1.0.0_SA_CTO~DELL2` when the precondition in section 2 reads met. Ids, statuses and counts only; no text.

**UPDATE 2026-10-14 ~12:3xZ (2.0.0_SA_COO~T2), CTO round-25 analysis @14c6836730 section 1 (msg 7599):** the cell moves to IRPT_ANLREQ workstream T (PRD ADDENDUM 2). Its TRIGGER is the O1 ticket that
IRPT_ANLREQ's partner-advisor run files (pivot packet O2), NOT the staff filing in 49financial described in section 2 below; ticket `TCK-20261012-c546fead` and the
filing are no longer the trigger. Three consequences, none yet applied to the text below: (a) section 2 items 1 and 2 are read against the O1 request id and the ticket id that
`2.0.0_SA_COO~Y2` reports, printed by the applier from the ticket's `report_ref` at step 0 as before; (b) the ORGANIC arm goes first: the commentary function's event source mapping on
`outlook-global-commentary-draft-analysis-ready-queue` is Enabled (live read 2026-10-14 12:2xZ, last modified 2026-10-11T01:26:42-04:00, batch 1), so the line in section 1 saying the queue is
"bound to nothing today" is STALE; `post_census.py --live --since 2026-10-14T00:00:00Z` reads `lines=0 with_ticket=0 posted=0 unposted=0 no_ticket=0`. The organic arm sends only when the resident reads the request record with a non-empty `ticket_id` AND `commentary_requested` exactly `True`
(`resident_worker.py:235-242`; the submission accepts the field as an optional JSON boolean, `submission.py:81-83`); otherwise the resident logs
`IRPT_RESIDENT_READY_SIGNAL skipped=COMMENTARY_NOT_REQUESTED <request_id>` and nothing reaches the queue (queue live read 2026-10-14 13:2xZ: 0 visible, 0 in flight). The driven invoke is cut only if the organic arm
has not posted for the O1 request once the READY event has had time to arrive, and the wait is set when the pair is cut; (c) the pair (this packet + CTO half) is unchanged otherwise. The model stays Kimi K3
(`ANDREW_DIRECT_20261013_211xZ_COMMENTARY_MODEL_KIMI_K3_NOW_OPENAI_LATER.md`).

## 1. What moves (the whole write set)

ONE direct invoke of `outlook-global-commentary-draft-lambda` with ONE SQS-shaped record for ONE request. It is the queue path of
`commentary/lambda_handler.py` run by hand; the organic first draft (the analysis-ready queue, bound to nothing today) stays the negative arm.

| write | where | note |
|---|---|---|
| one outside-model call | Moonshot (`KIMI_API_URL`) | the standing C-KIMI word (call `dell2-20261009T015641Z-1889`); a fixed instruction plus the abstract fields; closed-list values only (round 23 TR-cl-23); no theme, no free text, no precedent text today |
| one stored DRAFT | `irpt-commentary-draft-store-lambda` `put` for (tenant, request id) | the store reads the accepted record at persist; its answer carries `ticket_id` only when the record names one |
| one `commentary_ready` message | the function's commentary-ready queue | `{tenant, request_id}`; nothing consumes it today (no packager is bound) |
| one draft on ONE ticket | `POST {front door}/api/scoped/tickets/{ticketId}/commentary-draft` | the ticket the request's record names; the route admits only the service subject, a firm in `COMMENTARY_ALLOWED_FIRMS`, and a ticket whose `report_ref.request_id` equals the body's |
| log lines | the function's log group | one `COMMENTARY-POST request_id=<id> outcome=<token> status=<n> code=<token>` |

NOT moved: code, configuration, IAM, schedules, queues, the mapping, any other ticket or request. No delete follows (a delete is a human act).

## 2. Precondition (items 1 and 2 are read first by the applier; any miss is STOP before the invoke. Items 3 and 4 cannot be read from dell2 and are read by the run itself: a miss ends before the model call, see the branch table)

The CTO's rulings (`CTO_DELL2_RELAUNCH_THREE_ASKS_READ_AND_RULED_20261012.md` section 7, AMENDED @cccdb9ed92; then `CTO_ROUND_ANALYSIS_IRPT_ANLREQ_Y_ROUND_17_20261012.md`
section 1, msg 6641 ruling (A), CTO msg 6646): ONE synthetic request in tenant **49financial**, filed by ONE Opal staff member through the Analysis form on portal DEV with a
synthetic holdings file, naming ONE test ticket `2.0.0_SA_COO~V2` files FIRST in 49financial: `TCK-20261012-c546fead` (open, 49financial, created by `svc-commentary`, no draft, no `report_ref`; V2 msg 6651, record `R14_TEST_TICKET_20261012.json` @1bd49086ab). No synthetic 49financial advisor exists and none is minted (a users row
and partner profile for a fixture, and a constructed no-row filer, are both REFUSED). The filing is an act only a person can do: it is on Andrew's list. The earlier
cottonwood ticket `TCK-20261012-13cd3a1d` is NOT used and stays open as a test ticket (its close is Andrew's act). The act is TR-dp-24's ONLY once all four hold:
1. the request exists, an accepted record in 49financial whose id is `REQ-<24 hex>` and whose record carries `ticket_id` = the 49financial test ticket's id (Y2);
2. the ticket's `report_ref.request_id` equals that id (V2 records it);
3. the composition is retained and readable through `irpt-commentary-composition-read-lambda` (a read by an identity that holds the grant);
4. no stored DRAFT exists for the pair (`get_ref` answers none), so the run reaches the model.
The request id is NEVER typed into this packet or the order: the applier reads it from the ticket's `report_ref` at step 0 and prints it beside the ticket id.

## 3. Steps (the applier's order; read-only unless marked WRITE)

0. Read the 49financial test ticket (status, firm, `report_ref.request_id`, draft present yes/no); the live digest of the function (must be the root's one digest, today `xC1GDXXp`)
   and `TICKET_API_BASE` (the front door). Print them. A mismatch is STOP.
1. Build the record body with the repo's own keys module: `keys.queue_message("analysis_ready", {"tenant": "49financial", "request_id": <read>})`, ASCII bytes,
   and print the body's length and sha256 (the handler admits only the byte-equal rebuild).
2. WRITE, once: `lambda invoke` of the function, `RequestResponse`, payload `{"Records":[{"eventSource":"aws:sqs","messageId":"dp24-1","body":<the body>}]}`.
   Record the invoke time T0 (`date -u`). No retry on any outcome.
3. Read the response: `results[0].stage` and `failed`. Read the function's log since T0: the `COMMENTARY-POST` line, with the `REPORT` line beside it.
4. Run `python data/transcripts/scripts/commentary/post_census.py --live --since <T0>`: the expected line is `posted=1 unposted=0`.
5. Read the ticket again: a draft is present, its model field and length only. Read the commentary-ready queue's approximate message count (attributes only).

## 4. Branches (each outcome read from the response, not predicted)

| `results[0].stage` | log `outcome` | meaning | next |
|---|---|---|---|
| `draft_posted` | `POSTED` (200) | PASS: the first live post | report; ledger closes |
| `draft_posted` | `ALREADY_SET` (409 `DRAFT_ALREADY_SET`) | the ticket already held a draft: not a pass | report; STOP |
| `draft_post_refused` | `REFUSED` (status, code token) | the route refused (403 pair mismatch, 400, ...) | report status and code; no retry; DRAFT stays stored |
| `draft_post_failed` | `FAILED` | transport | report; no retry |
| `draft_stored` | `NO_TICKET` | the record names no ticket: precondition 1 was mis-read | report; STOP |
| `draft_exists` / `no_vendor_word` | -- | no model call ran | report; STOP |
| `failed` non-empty | -- | composition refused or an error class | report the closed reason; STOP |

Only `draft_posted` with `POSTED` on `status=200`, `post_census` `posted=1 unposted=0`, and the ticket reading a draft present together are the pass.

## 5. Rollback and bounds

There is no rollback of the model call, the stored draft, the queue message or the ticket draft; the CTO's ruling allows the act on a synthetic request and
ticket with these as its write set and forbids deletes. A failure leaves the stored DRAFT (a replay answers `draft_exists`, so a second run cannot repost: the
repost, if wanted, is a new request, under a new ruling). The applier opens a ledger entry in `org/critical_paths/change_management/` before step 2 and closes it
after step 5, listing the keys above as the write set.

## 6. COO half (this issuer)

GIVEN, on these bounds: the write set in section 1 and no other; one invoke; no retry; the precondition read before the invoke; the pass defined in section 4.
Issuer's live reads before sending to the CTO: precondition items 1 and 2 (the ticket's `report_ref`), the function's digest and base. Not read: item 3 (the grant
is the reader's) and item 4 (an invoke of the store).
