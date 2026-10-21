<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-DELETE-7I-DLQ-MESSAGE.one-synthetic-generation-message-by-handle-ib2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-21</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>60</round>
<workstream>~GREL5</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is ONE SQS message: the synthetic run 7I generation message (request REQ-0240fbdbf8c59e703e9fa3f0, ticket TCK-20261021-26db6ce5) in irpt-generation-dlq, deleted by its receipt handle. No purge, no redrive, no other message touched, no queue attribute change, no Terraform, no IAM change.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- the CloudOps applier's own queue access; no grant is added.
comp-adversary: RUN -- the lens: deleting a message that is not 7I's (identify it by the request id in its body, print only yes or no, never the body), a purge or redrive (forbidden), a message received from the DLQ and not returned to visibility when it is not 7I's (set its visibility to 0 at once), a delete while the message is still in the source queue (it must read in the DLQ), a second synthetic message of another run mistaken for this one. NOT seen (blind): whether the message has reached the DLQ yet (the run's journal says receives at 04:16:15Z, 04:31:15Z and 04:46:16Z, visibility 900 s, so the 5th receive is at about 05:16Z and it reaches the DLQ about 05:16Z to 05:31Z; your report said about 05:01Z to 05:16Z, so read both); denominator: the DLQ's visible plus in-flight count before and after.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R60_G.md</decomp_doc> round 60, workstream ~GREL5: the clean-up of run 7I's own synthetic message (CTO msg 11899: delete it by receipt handle, no purge, as run 7H's was deleted (msg 11829)).
<owned_cells>AR-g-181</owned_cells>
</decomp_ref>

  <objective>
    Delete exactly one SQS message, run 7I's synthetic generation message, from irpt-generation-dlq by its receipt handle, once it has arrived there. WHY: the resident refused run 7I's composition (RecipeRefused, row S249) three times; the request, job and ticket rows are deleted, so the message keeps failing and lands in the DLQ after its fifth receive. It is synthetic and no one will redrive it. THIS ORDER STARTS ONLY ON MY GO MESSAGE.
  </objective>

  <context>
    Queues (names as in your earlier reads): source `irpt-generation` (visibility 900 s, maxReceiveCount 5, redrive to `irpt-generation-dlq`). The 7I message: your row S249 and receipt irpt_anlreq_fwd10_multicomp_7i/A_E2E7I.txt (request REQ-0240fbdbf8c59e703e9fa3f0). Precedent: your 7H delete (record irpt_anlreq_7h_dlq_delete/A_DLQ_DELETE.txt, DLQ-DELETE-DONE). THE DLQ ALREADY HOLDS OLDER MESSAGES (8 to 10 visible at 04:47Z, none of them this run's): the wait trigger is the SOURCE queue (0 visible and 0 in flight) and the DLQ total growing by one, never `DLQ visible at least 1`. Use your attempt-3 method: hold every received message invisible (120 s) while all distinct DLQ messages are enumerated, test each body for the request id (yes or no, no body printed or kept), delete the one 7I message by its receipt handle, and return the others to visibility 0 together. That deviation from `return at once` is hereby authorized.
  </context>

  <the_act>
    GO only on my message. In this order, stopping at the first step that does not read as written:
    1. R0: print the date, the two queue names, and for BOTH queues the approximate visible, in-flight and delayed counts (the denominator).
    2. Wait for the message: poll the counts every few minutes until the source queue reads 0 visible and 0 in flight and the DLQ total has grown by one against R0, up to 06:00Z. If the source queue still holds it at 06:00Z, STOP and report the counts (no delete).
    3. Receive from the DLQ (batch of up to 10, wait 2 s, repeated until every distinct message has been seen once). For each message received decide `is7i` = its body contains the request id REQ-0240fbdbf8c59e703e9fa3f0 (yes or no; never print the body or an attribute value). A message that is not 7I's: hold it invisible while the enumeration runs, then change its visibility to 0 (all together) and do not touch it otherwise. Delete the 7I message by its receipt handle ONLY. If every distinct DLQ message has been seen and none is 7I's, STOP and report.
    4. C: print the DLQ and source counts after (allow a minute for the counts to settle). Expected: the DLQ holds what it held before step 3 minus nothing else (the 7I message was the extra), the source holds 0 visible and 0 in flight.
    5. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_7i_dlq_delete/A_DLQ_DELETE.txt with the lines `R0 ...`, `W waited_until=<time> dlq_visible=<n>`, `M received=<n> is7i=<n> returned=<n>`, `D deleted=1 by_receipt_handle`, `C dlq_before=<n> dlq_after=<n> source_visible=<n> source_inflight=<n>`, and the final line `DLQ-DELETE-DONE` (or `DLQ-DELETE-STOP <why>`). Report ONCE to 2.0.0_SA_COO~G2 (cc 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2).
  </the_act>

  <bounds>
    ONE message deleted, by receipt handle. No purge-queue, no redrive, no change to any queue attribute, no deletion of any message that is not 7I's (such a message goes back to visibility 0 at once). Print counts and yes/no only. Not alongside another act on these queues.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_7i_dlq_delete/IRPT_ANLREQ.TO-DELETE-7I-DLQ-MESSAGE.one-synthetic-generation-message-by-handle-ib2.proof_of_spec.json`.
    <criterion id="DLQ7I-AC1" cell_refs="AR-g-181">The record states the final line and exactly one deletion.<invocation>grep -c -E '^(DLQ-DELETE-DONE|D deleted=1 by_receipt_handle)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_7i_dlq_delete/A_DLQ_DELETE.txt</invocation><expect>^2$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a CLEAN-UP order to a tier-2 CloudOps seat on the CTO's msg 11785 (delete the synthetic message by receipt handle, no purge), not a worker cell; the cell AR-g-181 is the issuer's, as for TO-READ-RETENTION-CENSUS.
