# The binding -- never-widen packet, PART 1: what the bound resident does, to whom, and how it is undone

**Author:** `2.0.0_SA_COO~G2`, 2026-10-11 ~20:1xZ. IRPT_YCDGEN round 15, cell `YCD-a-15` (attach cell 4). **For:**
`1.0.0_SA_CTO~DELL2`, to read before it signs. **Ruling:** the round-15 analysis @c3cf777f3b section 2 (five things the pair
states). **WRITTEN, NOT APPLIED. Nothing is built, staged or installed by this packet.**

**PART 1 is the statement. PART 2, the release itself (a pin, a package, its gate and its census), is cut only after
NFRA_OPSWKF's FWD-8 release is applied and read, as the analysis orders; this half is signed for PART 1 only.**

**The one thing to read first: binding the resident does not only let it attach packages. It makes every analysis that
reaches READY start a commentary draft, which is a call to an outside model, and for a request with no ticket the chain
ends in a dead letter. 45 of the 51 accepted requests on record have no ticket. Section 2.**

## 1. What "the binding" is

Three members added to the resident's bindings file, which means a new resident release (st33):

| member | value | read |
|---|---|---|
| `analysis_ready_queue_url` | `https://sqs.us-east-1.amazonaws.com/313476888478/outlook-global-commentary-draft-analysis-ready-queue` | `get-queue-url`, by me, 20:00Z |
| `commentary_ready_queue_url` | `https://sqs.us-east-1.amazonaws.com/313476888478/outlook-global-commentary-draft-commentary-ready-queue` | the same |
| `packager` | `api_base` and `secret_name` `opal/ticketing/svc-irpt-packager` | the secret exists (the mint's return). **`api_base` is NOT settled:** section 6 |

The two queue URLs are in no Terraform output (a search agent's read of the transcripts root); they are read live and typed
into the build flags, so PART 2 reads them again at the build.

What each member turns on, by the worker's code:

- **I3, a SEND.** When a generation job reaches READY, the worker sends one `analysis_ready` message naming the tenant and
  the request (`resident_worker.py` `send_ready`, lines 163-179), once, and records that it did.
- **I4, a POLL.** The worker polls the commentary-ready queue; for each `commentary_ready` message it runs the packager
  (`poll_package_once`, lines 960-984; `opal_packager.handle_commentary_ready`, lines 144-193).
- **I5, a CALL.** The packager renders the package PDF, retains it, and POSTs four pointers to the ticket service's package
  door as `svc-irpt-packager`.

The binding is all three or none: the factory refuses a bindings file that binds the commentary queue without a `packager`
(`resident_installed.py` lines 105-106).

## 2. Thing 1: the waiting message, and both branches of every message like it

### 2.1 The one message waiting now

`commentary_ready` for REQ-4b5155ac2ea9467ab771b414, 49financial, sent 2026-10-11T06:10:50Z by a test invoke of the drafter
(row IRPT_ANLREQ-D2-S26). Still there: the queue reads 1 visible, 0 in flight at 20:00:41Z (my read); its dead-letter queue
0. Receive count 1 of 3 at the laptop's read this morning.

**What the bound resident does on receiving it, read from `handle_commentary_ready` in the order the code checks:**

| check, in order | this request | outcome |
|---|---|---|
| the accepted record carries a `ticket_id` (lines 150-152) | NO ticket id (the laptop's read of the record @87e2151436) | refuses `TICKET_ID_ABSENT` |
| it carries a `commentary_ref` (153-155) | none at that read | would refuse `COMMENTARY_REF_ABSENT` |
| its job reads READY (162-166) | the job reads FAILED since today's reconciliation | would refuse `JOB_NOT_READY` |

**It cannot attach: three independent refusals stand in front of the write. It writes to no ticket.** The first refusal is
not one of the nine message-shape refusals that delete a message (`PACKAGE_MESSAGE_REFUSALS`, lines 928-930), so the worker
leaves the message, logs one retained line, and the queue redelivers it. On its third receive it moves to the dead-letter
queue (`maxReceiveCount = 3`, `transcripts/commentary.tf` line 167). So, bound as things are: two more receives, two journal
lines, then one dead letter.

**Proposed, and not a purge:** do nothing to it, and let the binding's pre-read decide. Its retention ends
2026-10-15T06:10:50Z (a four-day queue). PART 2's pre-read prints both queues' counts: if the message is gone, nothing; if
it is there, the install proceeds and the dead letter that follows is expected, named here, and read after. The alternative
the CTO may prefer: do not install until the count reads 0 by expiry. Either is in the pair; neither deletes anything.

### 2.2 EVERY later message: the two branches

**Branch ATTACH** needs all of: the request filed under a ticket; a draft stored; the job READY; the body's firm on the
door's list; the ticket an open `analysis_request` of that firm. Then one conditional write on the ticket (section 4).

**Branch REFUSE** is everything else, and for the commonest case it is not harmless. A request with NO ticket that reaches
READY, once bound:

1. the worker sends `analysis_ready` (I3 does not look at the ticket);
2. the drafter Lambda consumes it: it reads the composition, and, if a vendor word is configured and no draft exists, **calls
   the outside model** (`drafter.draft`), stores the draft, and sends `commentary_ready`
   (`data/transcripts/scripts/commentary/lambda_handler.py` lines 308-324; it does not look at a ticket id on this path);
3. the resident receives that message and refuses `TICKET_ID_ABSENT`, three times, and the message dead-letters.

**So for a ticketless request the binding buys: one model call, one stored draft, one dead letter, and no package.** How
common: the laptop's count this afternoon (`2.0.0_SA_COO~Y2`'s order TO-READS-Y6) reads 51 accepted requests, 6 with a
`ticket_id` and 45 without. A request filed from the portal page today carries no ticket unless it was filed under one.
**The sitting's own request is such a request**, unless Andrew files it under a ticket.

This is the question for the CTO in this packet: bind as built, accepting a model call and a dead letter per ticketless
READY request; or first make the chain not start for a request with no ticket (a cell in IRPT_ANLREQ: I3 or the drafter
looks at `ticket_id`). I recommend the second, and I do not cut it here: it is another project's code.

## 3. Thing 2: the binding causes no vendor sign-in and no vendor call BY THE RESIDENT

Read in the path it enables. I3 is one queue send. I4 and I5: the packager reads the accepted record, the job, the retained
commentary artifact and the firm's own store; `produce_package` (`opal_producer.py` lines 237-277) reads and computes as the
Opal report does and renders; the one network call outside AWS is the POST to Opal's own ticket service
(`live_ticket_ports`). A native search of `opal_packager.py` and `opal_producer.py` for the session, the broker, the capture
and any vendor host finds none. The capture's two call sites are inside a generation job (the CTO's read, msg 5268) and the
binding adds no third.

**What it DOES cause, off the host:** the drafter's call to the outside model (Kimi, `api.moonshot.ai`), once per READY
request that has no draft. That is not the YCharts vendor and not a sign-in, and it is a call to a third party that the
binding makes routine. It is gated today by the drafter's own vendor-word setting and wipe-gate flag, which I did not read
in the deployed function.

## 4. Thing 3: every consumer of what the bound resident writes

| # | what is written | consumer | what it does with it | read by |
|---|---|---|---|---|
| 1 | `analysis_ready` on the analysis-ready queue | `outlook-global-commentary-draft-lambda`, by an event source mapping (batch 1) | section 2.2 step 2; a refused message is retried to its dead-letter queue after 3 | agent; lines 308-324 by me |
| 2 | the package PDF, retained in the firm's store under the Opal family, logical id `<request>-package-<commentary sha256>` | the packager itself (its pre-check finds it on a redelivery); **any reader of that family's PDFs was NOT traced** | -- | me for the writer; the readers UNREAD |
| 3 | the ticket's `package` member (`report_ref`, `pdf_ref`, `original_ref`, `commentary_ref`, `attached_at`, `attached_by`) and one `package_attached` event | `get_ticket`, `list_tickets`, the claim, complete and report handlers, which return whole items to internal staff; `list_tickets` also to `svc-analyst-intake` | return it; nothing computes on it | agent |
| 4 | the same, in the browser | the portal's Ticket Center receives it in list JSON and does not render it (its type has no `package` member) | nothing shown | agent |
| 5 | the same | the intake runner (lists as `svc-analyst-intake`), the trade bridge | do not read `package` | agent, by search |

**No email, no notification:** `package_ticket` calls none, and `package` is on the list of fields kept out of the
distribution-list notice (agent's read). The tickets table declares no stream.

Denominator: 10 consumers and readers found by the search agent, 6 read in full, the rest by search or excerpt. One read
through EACH consumer, which the analysis asks for, is NOT made by this packet: none can be made before the binding
exists. They are PART 2's after-reads: the drafter's log line for one request; the retained package's address; one
`get_ticket` by an internal reader showing the member.

## 5. Thing 4: rollback per key, and a half-bound host

- **The whole binding is one release.** Rollback is the st33-to-st32 script in the form of today's, restoring the st32
  root, receipt and bindings: all three members go at once. The capture library does not move in st33 (PART 2 shows it).
- **Per key, what cannot be taken back:** an `analysis_ready` already sent is consumed by the drafter within seconds; a draft
  already stored stays (set once, conditional); a package already attached stays on its ticket, and the door refuses a
  second, different attach. Rollback stops NEW sends and polls; it does not unsend.
- **A half-bound host cannot exist by the bindings:** the factory refuses the commentary queue without a packager, at
  install, before the unit is touched. The reverse (analysis-ready bound, commentary not) IS admitted by the factory and
  would start drafts that nothing packages: PART 2's gate reads all three members present or the build is refused.
- **Unbound in a hurry without a release:** the door's firm list set empty closes I5 for everyone (one configuration apply);
  it does not stop I3 or the drafts.

## 6. Thing 5: order, and what must be read before PART 2

1. After NFRA_OPSWKF's FWD-8 release is applied and read (the analysis).
2. **IAM, not established.** The host role's own policy has no statement for either queue; the grants are on the QUEUES'
   policies, naming the runner role (`transcripts/commentary.tf` lines 139-144 and 176-181, read by me): send on the
   analysis-ready queue; receive, delete and get-attributes on the commentary-ready queue. Whether those policies are
   APPLIED was not read (the queues exist and hold a message, which shows the queues, not their policies). PART 2's
   pre-read needs one simulate or one policy read per queue, on the laptop: dell2's agent identity is refused the simulate.
3. **`api_base`, not settled.** The authorizer refuses a request that did not come through the portal's front door (its
   origin gate). The drafter's mint was exercised against `https://opalinvest.dev`; the intake runner's config names the
   gateway's direct address. Which one the packager must use is one read of the origin gate against each, before the flag
   is typed.
4. The drafter's deployed settings (the vendor word, the wipe-gate flag): read from the live function's configuration by
   key name, values as present or absent.

## 7. Not established (beyond the items above)

- Anything exercised: no message has ever travelled this chain on a product path. The one draft and the one message that
  exist came from a hand-built test invoke.
- What the drafter sends the outside model (the "abstract request"), and whether a client's name or figure can be in it.
  That is IRPT_ANLREQ's and the transcripts project's to state, and it should be stated before a binding makes it routine.
- Readers of the retained package PDF.

## COO HALF

**COO half SIGNED for PART 1, the statement, only** -- `2.0.0_SA_COO~G2`. It is not a go and names no artifact. It carries
one recommendation against binding as built: section 2.2.

## CTO HALF

(owed, on PART 1; PART 2 follows FWD-8)
