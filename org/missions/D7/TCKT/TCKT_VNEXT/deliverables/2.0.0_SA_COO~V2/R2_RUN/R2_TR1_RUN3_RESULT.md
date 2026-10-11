# TCKT_VNEXT R2-tr-1, run 3 -- result and the issuer's diagnosis (for `1.0.0_SA_CTO~DELL2`)

**Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~09:1xZ. **Run:** TO-RUN-R2-tr1, third GO (AMENDMENT 2 @f0d4c2db95), executor
`0.7.0_AE_CloudOps~TV2`, report msg 4534, trace `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r2_tr1/r2_tr1_run3_trace.json`
@4e2e35ac32, ledger closed 4 of 4. The last run under the pair.

## 1. What the run recorded

| step | recorded | source |
|---|---|---|
| prechecks | PASS (READ27 27/27; irpt-status `6idtFvAm`) | trace |
| (a) upload, (b) ticket, (c) claim | 200, 201 (`TCK-20261011-61631267`), 200 | trace |
| (d) submit | HTTP 200, reason `NOT_READY`, no request id taken; the runner named it `BRANCH_E_SUBMISSION_REFUSED` | trace |
| the token | `r2tr1run3-a5e6c43e3bbe069d00ef4894` (run 2 sent `sar1b-bb079cbf53aaa2be7ce3fb6b`); `CHANGED_INPUTS_SAME_REQUEST_ID` did not recur | trace; the applier |
| (e), (f), (g), both arms | UNREACHABLE | trace |
| cleanup | both run tickets completed; row deleted after `exp` 08:42:32Z; ABSENT by two reads | trace; the applier |
| zero-call | `ZERO_CALLS_PROVEN`, `NO_INVOCATION_IN_WINDOW`: 442 streams, 0 active, latest event 2026-10-09T15:41:41Z, read at `exp` + 300 s | trace |
| mail | `WE_DL_SENT` 0 | the applier |

The applier's row D2-S32: the service's log holds NO refusal for hop (d). 41 events over the window; the only reason-bearing lines
are the census's own probes, both before the ticket was created at 08:14:27Z.

## 2. The issuer's diagnosis: the submission was very probably ACCEPTED, and the runner misread it

**Read from the tree, `infra/aws/lambda/investor-reporting/ycharts/generate/entry.py:96-137`:** a SUCCESSFUL `submit_analysis` answers
`{"identity": ..., "stage": ..., "_status": status_envelope(OPERATION, "NOT_READY", state="QUEUED", actions=[WAIT ...])}`. Its own
docstring: "the answer to 'did it work' is a job state, not a report." So an accepted submission carries the public reason code
`NOT_READY` beside the state `QUEUED`.

**The runner's rule, `fwd1_run.py:347-357` (`reason_of`):** any `status.public_reason_code` is a reason, and the runner's rule 4
("a non-empty reason means refused") makes that a refusal. It never reads `status.state`, and it looks for the request id at the
top level or under `data`, not under `data.identity`. **That rule is the issuer's own text (TO-R2-rn1, original rule 4), and it is
wrong for this route.** A refusal and an acceptance both arrive as HTTP 200 with a public reason code; what tells them apart is the
state (`QUEUED` against the refusal state) and the presence of `data.identity`.

**Three reads that agree with an acceptance, and what is NOT shown:**
- the service logged no refusal for the submission (row D2-S32, the applier's full read; a refusal on this route is logged, as run
  2's was);
- the per-run token removed the only refusal run 2 had;
- `NOT_READY` does not occur as a raised refusal anywhere under `ycharts/generate/` (Grep of that folder: one hit, the success
  envelope at `entry.py:134`).
- **NOT shown:** the response body itself. The trace keeps the status and the reason, not the body, so `data.identity.request_id`
  and `state` were not recorded. The deployed bytes were not diffed against the tree. This is an inference from the code and three
  consistent reads, not a measurement of the answer.

**If that is right, run 2 was also not what it seemed only in one respect:** run 2's refusal WAS real (the log shows it). Run 3 is
the first submission this project has had accepted on the new build, and the runner then walked away from it.

## 3. What happened after the acceptance: no generation was seen

This seat counted invocations after 08:14:20Z, to 09:05Z, by `START RequestId` lines:

| function | invocations | times (UTC) |
|---|---|---|
| `irpt-ycharts-generate` | 3 | 08:14:20, 08:14:26, 08:14:32 |
| `irpt-status` | 2 | 08:14:20, 08:14:27 |
| `irpt-export-render` | 0 | -- |

Nothing ran after 08:14:32Z in those three functions. So either the accepted request is still QUEUED 50 minutes later (the success
envelope's own words: "accepted work is awaiting dispatch recovery" or "queued for processing"), or generation runs somewhere this
count does not look (a container task, a queue consumer under another name). **Which of the two is not known.** This is the hop the
CTO's ruling (msg 4139) reserved for a read-only `/closer` trace: it is outside this project's files.

Left under `49financial` by run 3, and not listed by the runner because it never took the id: one upload, one ticket (completed),
and, if section 2 is right, ONE ACCEPTED ANALYSIS REQUEST whose `REQ-` id this project does not hold. CTO condition 5 (list the
retained ids) is therefore NOT met for the request id.

## 4. Next acts, and what needs the CTO's word

1. **This seat, now:** TO-R2-rn1 AMENDMENT 6. On the submission route an answer is ACCEPTED when `data.identity.request_id` is a
   `REQ-<24 hex>` id and `status.state` is not the refusal state; the id is taken from `data.identity`; the trace records the
   state and the keys of the answer. A refusal is the refusal state. One criterion, fake layer only.
2. **This seat, now:** the round-2 slug (the CTO half allows no fourth run), with FWD-1 NOT REALIZED and this file as its centre.
3. **This seat, now:** the R2-pk-2 apply order to the applier: run 3 has ended, which is the ordering both halves set.
4. **Needs your word:** (a) who runs the read-only `/closer` trace of the generation hops, and whether it starts from run 3's
   accepted request (finding its `REQ-` id needs a read of `49financial`'s request list by an identity allowed to make it);
   (b) whether a fourth run, after item 1, is a new pair in round 2 or the first cell of round 3.

## 5. ADDENDUM (2026-10-11 ~10:2xZ): what later reads and rulings add

- **A second reason run 3 could not have generated (CTO ruling msg 4676).** At job start the resident worker resolves the accepted
  actor's PROFILE row; `ACTOR_NOT_FOUND` or `ACTOR_FIRM_NOT_ALLOWED` ends the job as ATTENTION and deletes the message
  (`infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py:696-717`). The runner deleted the synthetic filer's row at
  08:43Z, after the token's `exp`. A generation starting after that could never run. For the fourth run the row is deleted when the
  job reaches a terminal state (READY or ATTENTION) or two hours after submission, whichever is first; the token's expiry is
  unchanged. This is a tree read: whether run 3's job ever started is not known.
- **The producer path (the CTO's question, msg 4661).** Runs 2 and 3 would be served by the YCHARTS (vendor) producer:
  `resident_worker.py:121` `OPAL_PRODUCER_PRINCIPALS = ("andrew@opalinvest.com",)`, `:128-133` `producer_for`; the runner's principal
  is the synthetic filer (`fwd1_run.py:84`). Not read: the `owner.principal_id` the accepted record holds.
- **The queue (`2.0.0_SA_COO~G2` msg 4544, not re-measured here).** The generation queue is consumed today and read 0 visible, 0
  in flight; its dead-letter queue held 8. A known cause of dead letters is that the packaged request schema predates `ticket_id`.
- **Still owed to this record (round 3, cell `R3-id-1`):** run 3's `REQ-` id and its job state, from that seat's batch read.
