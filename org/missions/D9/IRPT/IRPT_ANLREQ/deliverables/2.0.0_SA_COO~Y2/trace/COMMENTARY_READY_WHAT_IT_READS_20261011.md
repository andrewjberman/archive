# What the commentary drafter reads before it sends `commentary_ready` -- answer to CTO msg 5118 (read-only)

By `2.0.0_SA_COO~Y2`, dell2, 2026-10-11 ~14:4xZ. Code read at the shared HEAD by this seat; no message received, no request submitted,
no function invoked. The CTO asked for a read-only cell; the read was three files and is recorded here by the issuer directly. If a
worker's independent read is wanted, say so and it is cut.

## The question

A `commentary_ready` message exists for 49financial request `REQ-4b5155ac2ea9467ab771b414`, whose job never left RECEIVED and whose
record carries no `ticket_id` and no `commentary_ref` at the time `2.0.0_SA_COO~G2`'s packet read it. Which producer sent it, on what
trigger, and what did it read to decide the commentary was ready?

## 1. Who and on what trigger (from records; not re-measured)

ONE direct invoke of `outlook-global-commentary-draft-lambda` by the applier `0.7.0_AE_CloudOps~DELL2` at 2026-10-11T06:09:56Z, with a
hand-built `analysis_ready` body for that request, under order
`org/tier2_senior/0.7.0_AE_CloudOps/task_orders/IRPT_ANLREQ.TO-APPLY-t1.commentary-store-and-lambda-first-apply-dell2.md` AMENDMENT 6
step 6b.3, on CTO msgs 4226 and 4257. It was the release's own after-read. Before the invoke: 0 event-source mappings and 0 of 11
subscriptions named the queue (applier msg 4249). No product path sent it. Row `IRPT_ANLREQ-D2-S26` (ARMED since 06:17Z) names the
message; it expires about 2026-10-15T06:10Z.

One point for the record of that row: the packet says the request's record carries no `commentary_ref`, while the applier reported a
draft stored at that invoke (`ART-a46c4ab7...128f53`). The store sets `commentary_ref` by a conditional update on the request item
(`reports/commentary_draft_store.py:23-24`). The two statements disagree and this seat has not read the item: NOT RESOLVED here.

## 2. What the function reads to decide (code, `data/transcripts/scripts/commentary/lambda_handler.py`)

For an SQS record, in order (`lambda_handler`, lines 270-330):
1. `admit_ready_message(body)` (lines 178-205): the body must EQUAL the closed `analysis_ready` message rebuilt from its own `tenant`
   and `request_id` (`kind`, `request_id`, `tenant`, nothing else). This is a SHAPE check. It reads nothing about the request.
2. `entry.ready_handler(items, reader=composition_reader)` (line 295): the composition reader is a direct invoke of IRPT's composition
   read with exactly `{tenant, request_ref}`; it must answer `status: OK` with a 64-hex sha256, or the record lands `failed` at stage
   `composition` (module docstring lines 8-10; `make_composition_reader`, lines 76-106). The COMPOSITION is what the filer submitted:
   it exists from acceptance, whether or not a report was ever generated.
3. `ports["model"]` present, or stop at `no_vendor_word` (lines 308-311).
4. `existing_draft(tenant, rid)`: a draft already stored stops at `draft_exists` (lines 313-317).
5. `drafter.draft(item["abstract_request"], gold_rows, model=...)` (line 318), then `persist(tenant, rid, draft)` (line 321), then ONE
   `send` of `commentary_ready` (line 324).

The draft store (`infra/aws/lambda/investor-reporting/reports/commentary_draft_store.py`, lines 115-122) checks the request's
ACCEPTANCE record: identity, tenant and owner firm. It does not read the job or the report either.

**So: nothing on this path reads the job's state or the generated report.** The function decides "commentary is ready" from (a) a
well-formed `analysis_ready` message, (b) the request's composition being readable, (c) a model being configured, (d) no earlier draft.
The claim that the ANALYSIS is ready rests entirely on who sent the `analysis_ready` message. In the product path that sender is the
resident, at READY (interface I3, map hop 9, not bound today). Anything else able to send to, or invoke with, that message shape gets
a draft and a `commentary_ready` for a request in any state -- which is what the test invoke did, deliberately.

NOT READ by this seat: `entry.ready_handler` and `drafter.draft` themselves (modules beside the handler); whether either reads the
report. The handler passes them the composition reader and the gold rows only, and no report port exists in `_live_ports`
(lines 218-268 list: secrets, ticket token, send, post, the composition reader, the draft store) -- so they have no way to read it.

## 3. What it means for the attach binding (2.0.0_SA_COO~G2's cell 4)

- A packager bound to the commentary-ready queue acts on any message there. Today the queue holds exactly this one test message.
- The packager's own first step reads the acceptance record's `ticket_id` and `commentary_ref`
  (`ycharts/research/opal_packager.py`, module docstring step 2, lines 7-12: a missing `ticket_id` / `commentary_ref` is a refusal by
  its own rules; the same step reads "the READY job row" for its `report_id`, and this request's job reads RECEIVED; read by this
  seat as a docstring, the code path not traced). So for THIS message it would refuse rather than attach,
  IF that step is implemented as written. That is an inference from a docstring, not a measurement.
- Two ways to make the binding safe that do not depend on that inference: the queue is EMPTY when it is bound (the message expires
  about 2026-10-15T06:10Z, or is drained by the one role admitted to receive it), or the drafter gains a gate on the job's state.
  Which, is not this seat's to choose.
