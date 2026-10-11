# IB149-1 -- which member says commentary is asked for, and who reads the accepted record

Order IRPT_BCKEND.TO-IB-pr-453, worker 0.9.0_WK_IRPT_BCKEND~309, read at 0bdd920114. A code and contract read: no AWS call, no network call, no vendor request, no product file edited, no contract change proposed. The full record is `IB149-1_commentary_asked_member.json`; paths below are under `infra/aws/lambda/investor-reporting/` (IR) unless written otherwise. Each sentence ends with its claim.

## What starts a draft today

1. The worker does NOT send `analysis_ready` only when a ticket id is present. `mark_ready` (IR/ycharts/generate/resident_worker.py:319-329) writes READY, copies `ticket_id` into the receipt if the record has one, and then calls `signal_ready` on every path; `send_ready` (:163-186) sends unless the queue-url environment variable is empty (measured). The offline test `test_ready_signal.py test_b` asserts that a job with no ticket still sends once, and it passed here, opal and vendor builds (measured). The order's premise differs from the code; this is row IRPT_BCKEND-D2-W309-S1.
2. The receiver (data/transcripts/scripts/commentary/lambda_handler.py:178-327) accepts only the byte-exact closed message, builds its item from tenant and request id alone, reads the composition (which needs the job to read READY, IR/reports/commentary_composition.py:146), and drafts if a model is configured and no draft exists. It reads no ticket id and no commentary member (measured).

## Does a submission say commentary is asked for

3. No (`NOT_TOLD`, measured). The request body is a closed set (IR/ycharts/generate/submission.py:14-16, refused at :51-52; schema `AnalysisSubmissionRequest.schema.json` additionalProperties false). The nearest member is `ticket_id`, which says only "filed under a ticket"; commentary could be inferred from it, and nothing on the send path does so.

## Does the ticket say it

4. Yes (`TOLD_BY_A_MEMBER`, measured). `answers.add_commentary`, a boolean on an `analysis_request` ticket, is declared at infra/aws/lambda/ticket_center/lambda_function.py:108 and validated at :711-713. True means a commentary was asked for; false or omitted means a report only. The declared default False is metadata: no code applies it, so an unsent answer is simply missing (measured).
5. No code in the IRPT tree reads it. Its only reader in the repo is the commentary drafter's own check on a ticket it writes (data/transcripts/scripts/commentary/ticket_client.py:104). The ticket contract is that code; no schema file or TCKT PRD text names it (measured).

## The accepted record

6. It is the immutable JSON attribute `record` of the item `analysis#<request_id>#1` in the irpt-requests table, written once by `DynamoAcceptance.accept` (IR/ycharts/generate/acceptance.py:113-131). Members today: identity (six fields), owner, browser_sha256, composition_ref, accepted_at, acting_principal_id, and ticket_id only when the submission carried one (measured).
7. A replayed submit returns the prior record unchanged (:108-110, :135-139), so any member added to the writer later is absent on every record accepted earlier and stays absent (measured).
8. `commentary_ref` is NOT a member of the record. The draft store sets it later as a separate attribute of the same item (IR/reports/commentary_draft_store.py:213-219), and `DynamoAcceptance.get` returns only `record` (acceptance.py:68-71). The packager reads `record.get("commentary_ref")` (IR/ycharts/research/opal_packager.py:153) from that same `get`; the code says it would never see it, but no live read was made (inferred; row W309-S2).
9. No file declares the stored record. The nearest are `OwnedAnalysisRequest.schema.json` (the public read projection, closed) and the code-level closed set `IDENTITY_FIELDS` (IR/ops/owned_requests.py:19, applied at :186 to the identity sub-object only). So "forbids additional members" is null for the record itself (measured as an absence). In code, no reader found refuses an unknown top-level member; a member added inside `identity` would be refused by every `_validate` caller (measured).

## Could acceptance read the fact without a ticket read

10. No (`answer` false, measured). At acceptance.py:90-121 the writer holds the owner, the validated submission (closed set, `ticket_id` as an id only), the composition ref, two revisions and the acting principal. It has no ticket body, no ticket port and no ticket import. Only a read of the ticket's `answers.add_commentary` would tell it, and the CTO has ruled the worker and drafter get no ticket read.

## Readers of the accepted record

11. 50 readers in 35 reader files of the 45 files naming the record (35 readers, 1 writer `acceptance.py`, 9 neither), found by listing every file naming `DynamoAcceptance`, `analysis#`, `.acceptance` or the record's name, then placing each by reading its lines (measured). By kind: worker 5, publication 3, authority 3, request_api 4, status_api 6, drafter 2, packager 2, research 1, acceptance_store 4, test 20 (one per test file).
12. Unknown top-level members are ignored by every production reader; they read named members only. The one strict reader is `OwnedRequestReader._validate`, strict on the identity sub-object. Whole-record equality appears only in `_final` (two reads of the same store). The only production reader of `ticket_id` is `mark_ready` (absent: the receipt omits it and the send still happens), `_require_ticket` (absent: nothing happens) and the packager (absent: `TICKET_ID_ABSENT`). `test_resident_worker.py:794-799` shows unknown flags on the record change nothing end to end. No page in this repo reads the record: the served response is `{identity, accepted_at}` only (IR/ops/owned_requests.py:243).

## Not established

The deployed queue binding and the live commentary Lambda configuration (no AWS call); the portal (its submodule is empty in this worktree); whether live tickets carry `add_commentary`; the live behaviour of S2; org-tree scripts that read the same table. Rows filed: IRPT_BCKEND-D2-W309-S1, -S2, -S3.
