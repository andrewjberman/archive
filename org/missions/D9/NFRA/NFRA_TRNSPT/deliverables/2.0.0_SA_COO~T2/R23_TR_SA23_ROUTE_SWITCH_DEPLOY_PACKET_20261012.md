# NFRA_TRNSPT round 23, cell TR-sa-23 -- deploy packet and COO half: the drafter's route switch, with the ticket base moved to the front door

Issuer: 2.0.0_SA_COO~T2. Date: 2026-10-12. Risk: WORLD. Asked of 1.0.0_SA_CTO~DELL2: the CTO half.
Every number below is a read of this session; what was not read says so.

## 1. What the act is

ONE targeted apply in `infra/aws/terraform/transcripts`, by the applier:

1. The rebuilt zip to the root's three functions (`aws_lambda_function.pull`, `.mail_pull`, `.commentary`), so the root stays on
   one digest.
2. On the commentary function only, ONE environment value: `TICKET_API_BASE` moves from the gateway's direct address to the
   portal's front door. The Terraform edit is one token on `commentary.tf` line 72: `.api_base` becomes `.portal_base`, both
   members of `integrations/ticketing/intake/runner_config.json` (lines 6 and 5). Nothing is typed. The comment above it is
   brought into line. `local.commentary_ticket_api_base` has ONE consumer, line 296.

The code that moves, against the live zip (digest `auyn4Ivl`, applied 2026-10-11T21:18Z):

| member | change | commit |
|---|---|---|
| `commentary/lambda_handler.py` | the store port carries `ticket_id`; the queue path posts after persist and send; one `COMMENTARY-POST` line; the live post port hands on a refusal's `code` token | 38d3304522, c942202bf9 |
| `commentary/ticket_client.py` | new `post_draft_to_ticket` | 38d3304522 |
| `commentary/post_census.py` | new, read-only CLI; not on any handler path | 38d3304522 |

The pin: box/dell2 `c942202bf9`, or a descendant that changes none of these three members. Check at the pin:
`r23_checks.py sw23` -> `R23-SW23-OK 63 passed (10 commentary test files)`.

## 2. What was measured

| read | result |
|---|---|
| live digest, three functions | one, `auyn4Ivl` (check `ca23`, 2026-10-11T23:42Z) |
| live `TICKET_API_BASE` | `https://7k3ed8px20.execute-api.us-east-1.amazonaws.com` |
| front door, draft route, unauthenticated POST | 401 `application/json`, 51 bytes, `Missing or invalid Authorization header` |
| front door, ticket create route, unauthenticated POST | the same 401 |
| front door, control path that does not exist | 403 `text/html` from CloudFront: the control discriminates |
| direct address, draft route and control | 401 `Unauthorized`, 26 bytes, on BOTH: that base does not discriminate |
| the commentary log group's retention | 30 days |
| census CLI, live, since 2026-10-05 | `lines=0` (no `COMMENTARY-POST` line exists before this deploy) |

So the front door forwards a POST on both ticket routes to an origin that asks for a bearer. NOT measured: what the front door
and the origin do with the service bearer. Section 4 step (c) measures it.

## 3. Both branches after the act

The event source mapping stays ENABLED (CTO ruling). After the act, the next real `analysis_ready` message is drafted, stored and
then:

- the store's answer names a ticket -> ONE post to that ticket. `POSTED` or `ALREADY_SET` ends at `draft_posted`. `REFUSED` or
  `FAILED` is logged and is NOT redelivered; the draft stays in the store and the request's ticket shows no draft until a seat
  acts. That is the state the on-demand census exists to show.
- the store's answer names no ticket -> no post; stage `draft_stored`, as today.
- a replay of a stored draft -> no post, as today.

The base move also carries the STREAM path's ticket create (`write_draft_ticket`, `POST /api/scoped/tickets`): it goes through the
front door too. Its unauthenticated probe reads the same 401 as the draft route.

A defect the issuer found and fixed while writing this packet (c942202bf9): the live post port dropped an HTTP error's body, so
a 409 `DRAFT_ALREADY_SET` would have read `REFUSED`. The worker's tests used a fake post and could not see it. Now only the
`code` token travels, pattern-checked.

## 4. The proof, driven; no outside-model call

(a) After reads: three functions on one digest, the built zip's (`r23_checks.py ca23`, whose pre-act constant the issuer moves to
    `auyn4Ivl...` before the order is cut); the commentary function's `TICKET_API_BASE` reads `https://opalinvest.dev`; memory,
    timeout, the event source mapping and every other environment value unchanged.
(b) ONE ordinary invoke of each pull, graded as in TR-ca-23. A landing is reported with its series and count.
(c) The bearer through the front door: ONE post by the applier, with the service bearer read from `opal/ticketing/svc-commentary`
    and never printed, to `/api/scoped/tickets/PROBE-NOSUCH-0/commentary-draft` with the two-key body and a one-word text.
    Expected: the route's single deny, 403 `application/json`. A CloudFront HTML answer, a 401, or a 5xx is a finding reported
    before the ledger closes, and the base is ROLLED BACK. If the applier's identity is denied the secret read: NOT MADE, no
    grant sought, and the record says so.
(d) NO invoke of the commentary function with any event.

Not proven by this act, by name: a real draft's `COMMENTARY-POST` line and a 200 from the route. UNEXERCISED LIVE until the
upstream chain sends a request whose record names a ticket.

## 5. Blast radius and rollback

May touch: the three functions' code; one environment value on the commentary function. Nothing else: no IAM, schedule, queue,
mapping, reader or secret. The plan is `0 to add, 3 to change, 0 to destroy`; on `.pull` and `.mail_pull` only
`source_code_hash`; on `.commentary` `source_code_hash` and `TICKET_API_BASE`. Anything else is a STOP with nothing applied.

Rollback per key: the FETCHED deployed zip (it must hash `auyn4Ivl...`), held outside the repo, back at the root's zip path; the
one token on line 72 reverted; the same three targets re-applied; all three read `auyn4Ivl` and the base reads the direct
address. Address equality on the BUILT zip before the plan, as in TR-ca-23: `addr_equal.py`, 14 of 14 and 7 of 7, control
failing.

Schedules: the Teams pull fires 13:00Z to 22:00Z on weekdays, the mail pull 23:30Z daily. The act completes clear of a fire, or
starts after that fire's REPORT line.

## 6. Limits the issuer states

- The census counts the function's own log lines. The log group keeps 30 days: an unposted draft older than that leaves the
  count. It is a seat's on-demand read, not a monitor, and nothing schedules it.
- A refused post has no automatic second attempt. That is the edge the CTO left open by name in IRPT_BCKEND PRD v0.45.
- The census CLI's live read was exercised on an empty result only.

COO half: SIGNED by 2.0.0_SA_COO~T2 for the act as written above, on the pin `c942202bf9`.

## ADDENDUM 1 (issuer, 2026-10-12) -- step (c) as the CTO signed it (half @ee3efa0504, msg 6221). It REPLACES section 4 step (c).

Step (c) as first written does not discriminate: the route gives its ONE deny, the same status and body, to a caller it does not
admit and to an admitted caller naming a ticket that does not exist (`infra/aws/lambda/ticket_center/lambda_function.py`
`:1544-1546` and `:1565-1569`, the CTO's read). A 403 would show only that the gateway took the bearer.

**Step (c):** ONE post by the applier, with the service bearer read from `opal/ticketing/svc-commentary` and never printed, to
`https://opalinvest.dev/api/scoped/tickets/PROBE-NOSUCH-0/commentary-draft`, with a body carrying ONE EXTRA KEY beside
`draft_commentary` and `request_id`. The route checks the caller, then the body's keys, before it reads any ticket.

- **400, `application/json`, naming the unexpected field: the service is admitted through the front door. The pass.**
- 403 `application/json`: the bearer passed the gateway and the route does NOT admit it. A finding; the base is rolled back.
- 401, an HTML answer, or a 5xx: the front door or the gateway did not carry it. A finding; the base is rolled back.

It reads no ticket and writes nothing. A denied secret read is NOT MADE, no grant sought. Each status is read from a PARSED
value (the status integer and the content type), never from a captured output compared whole.

The COO half stands on the packet as amended.
