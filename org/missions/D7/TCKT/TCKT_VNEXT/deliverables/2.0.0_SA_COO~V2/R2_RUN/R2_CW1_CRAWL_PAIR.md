# TCKT_VNEXT R2-cw-1 -- one-ticket browser crawl: never-widen pair, COO half

**Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~03:5xZ. **Authority:** Andrew, "crawl that instead" (row 15 of
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261010_133xZ_FIFTEEN_OPEN_ITEMS_ANSWERED.md`, open call
`dell2-20261009T022719Z-fbb1`); CTO round-2 analysis @bbba700c22 section 4 item 4; CTO ruling msg 3990 ("(a) a signed pair for a
one-ticket crawl identity on dell2 ... the round-1 v2.2 shape, narrowed"). Cell `R2-cw-1` of `decompositions/TCKT_VNEXT_DECOMP_R2.md`.
The shape it narrows: `R1_RUN/TV_R1_SEAT_ARM_PLAN_AND_PAIR.md` v2.2 with COO-half AMENDMENTS 1-2.

## 1. The ticket, measured 2026-10-11 ~03:5xZ (ConsistentRead of `opal-tickets`, status fields only)

| field | value |
|---|---|
| `ticket_id` | `TCK-20261009-a1052909` |
| `status` / `assignee` | `open` / null |
| `ticket_type` / `source` | `analysis_request` / `portal` |
| `created_by` / `requester.email` | `svc-commentary` / the literal string `svc-commentary` (not an address) |
| `requester.firm` | `cottonwood` |
| `title` | `[TEST TCKT_VNEXT F10] svc-commentary positive arm` |
| `report_ref.request_id` | `test-f10-20261009-one` (a test value; it opens nothing) |

It is the F10 leg-M test ticket, written by the service principal. It holds no client's request.

## 2. The identity (synthetic, internal tier, minted for this cell only)

- **Row:** `opal-users-v2` `PK USER#tckt-r2-crawler-20261011@opal.invalid`, `SK PROFILE`; `firmId opal-capital`, `status active`,
  `userType "test-filer"`, `name "TCKT_VNEXT R2 one-ticket crawler"`, `allowedFirmIds` the LIST `["cottonwood"]`. Written with
  `attribute_not_exists(PK)` and read back PRESENT with ConsistentRead before the token is minted.
- **Token:** ONE RS256 token, the CURRENT signing slot, `sub` = that address, `iss opal-portal-auth`, `aud opal-portal-api`,
  `firmId opal-capital`, `tier internal`, `role user`, `userType "test-filer"`. `exp` = the run's length + 5 minutes, and never more
  than 20 minutes after `iat`. Held in memory and in the one browser context only; never written to a file, a log or a trace. The
  key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`.
- **Why the LIST is `cottonwood`:** the ticket's `requester.firm` is `cottonwood`, and the SA-k-1 clamp returns 404 on GET, CLAIM and
  COMPLETE for a ticket outside the caller's list. `cottonwood` is a client firm. The identity can therefore LIST and GET cottonwood
  tickets for the token's life; section 4 bounds what is recorded.

## 3. The act (executor: a `0.7.0_AE_CloudOps` lane seat on dell2; this seat holds no key)

0. Open the NEVER-2 ledger entry FIRST. Read every live worktree's `.open_deploys/` (`git worktree list --porcelain`, then
   `ls-tree` per tree), union them, print the per-tree denominator; an open entry naming `opal-ticket-api` or `opal-tickets` is a STOP.
1. Re-read the ticket (ConsistentRead). Proceed only if it reads `status open`, `assignee` null, `created_by svc-commentary`. Any
   other state is a STOP: the ticket is left as found and nothing is minted.
2. Write the row, read it back, mint the token.
3. **One-firm proof before any write:** with the token, `GET /api/scoped/tickets` returns only tickets whose `requester.firm` is
   `cottonwood`; `GET` of one `49financial` ticket id (`TCK-20261009-67ab7f27`) is 404; ONE data-refresh route is refused. Anything
   else is a STOP.
4. **The crawl, in a browser on portal DEV:** open the Ticket Center board signed in as the identity, find the row
   `TCK-20261009-a1052909`, press the board's own claim control, then its complete control. No API call replaces a click: the two
   writes are made by the page. Before each click the ticket is re-read and its prior `status` and `assignee` printed.
5. **The board read:** reload the board and read the ticket's row; then ConsistentRead the item: `status completed`, `assignee` the
   identity's address.
6. **Zero-call read with a positive control:** over `iat`..`exp`, count the identity's address in the data-refresh Lambda's log
   group, printing the streams searched (a count of 0 streams searched is VOID, as round 1's was); the positive control is the same
   filter over `/aws/lambda/opal-ticket-api`, which must find the identity's CLAIM and COMPLETE.
7. **Removal, same sitting, v2.2's method:** wait until the token's `exp` has passed, then delete the row and read it back ABSENT with
   ConsistentRead. The proof prints the `exp`, the later delete time and the absent read. The ledger closes only after this.

**The two writes this identity may make:** `POST /api/scoped/tickets/TCK-20261009-a1052909/claim` and
`POST /api/scoped/tickets/TCK-20261009-a1052909/complete`. No other ticket, no other route, no CREATE, no REPORT, no PACKAGE, no IRPT
write, no upload. Sign-in plumbing the page itself performs (a token refresh, a telemetry beacon) is not a write of the identity and is
named in the trace if it occurs.

## 4. Blast radius (what the act may touch, and the rollback per key)

| key | what may change | rollback |
|---|---|---|
| `opal-tickets` item `TCK-20261009-a1052909` | `status open -> in_progress -> completed`; `assignee` null -> the identity's address; two `events` rows appended | prior values are printed before each write. A ticket has no un-claim route: a claim that lands and a complete that is refused leaves the ticket `in_progress` under the synthetic assignee, and this seat then routes one DynamoDB-level reset to the CTO as its own pair. It is a test ticket, so the residue harms no client |
| `opal-users-v2` row `USER#tckt-r2-crawler-20261011@opal.invalid` | created, then deleted after `exp` | delete + ConsistentRead ABSENT |
| SES, one attempt | CLAIM calls `notify_client_isolated(..., "pickup")` (`lambda_function.py:1038`, called from `claim_ticket`), which sends to `requester.email`. Here that is the string `svc-commentary`, not an address, so SES refuses it and the handler logs `WE_CLIENT_SEND_FAILED`; the claim still succeeds. **No mail reaches any person.** Read from the code and the item, not exercised | none needed; the trace records the `WE_CLIENT_*` token the claim logged. If it logs `WE_CLIENT_SENT`, that is a surprise row and a STOP before COMPLETE |
| cottonwood tickets, READ only | the board lists cottonwood tickets to the identity for the token's life | nothing is recorded but this one ticket's row: no screenshot of the whole board, no other ticket's id, title or content in any file |
| data-refresh | in the radius; expected zero calls | step 6 proves zero with a positive control; `userType test-filer` on an internal principal is admitted by that gate (row D2-S17), which is why it is named here |
| IRPT read surfaces | the token is narrowed to `cottonwood` by the `served.py` clamp; the crawl opens no IRPT page | none; any IRPT request in the browser's network log is recorded and is a surprise row |

No IAM, code, route or Terraform change. No client figures in any tracked file.

**Both branches.** (A) The board reads the ticket `completed`: open call `-fbb1` closes on that read. (B) A write is refused, or any
STOP fires: the ticket is left as found (or `in_progress`, as the first row above says), the row is removed after `exp`, and the
refusal is recorded with its status and reason.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11, for the blast radius in section 4 and both branches. No run is staged until the CTO half matches this
text and a run order cites both pins.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2` (msg 3990: "I sign or refuse the same turn").
