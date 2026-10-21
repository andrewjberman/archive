<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-DELETE-7H-DLQ-MESSAGE.one-synthetic-generation-message-by-handle-ib2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-21</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>60</round>
<workstream>~GREL4</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is ONE SQS message: the synthetic run 7H generation message (request REQ-e90c581652f6c90d3e33af23, ticket TCK-20261021-c553ca50) in irpt-generation-dlq, deleted by its receipt handle. No purge, no redrive, no other message touched, no queue attribute change, no Terraform, no IAM change.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- the CloudOps applier's own queue access; no grant is added.
comp-adversary: RUN -- the lens: deleting a message that is not 7H's (identify it by the request id in its body, print only yes or no, never the body), a purge or redrive (forbidden), a message received from the DLQ and not returned to visibility when it is not 7H's (set its visibility to 0 at once), a delete while the message is still in the source queue (it must read in the DLQ), a second synthetic message of another run mistaken for this one. NOT seen (blind): whether the message has reached the DLQ yet (the run's journal says 3 of 5 receives by 02:41Z, visibility 900 s, so about 03:11Z to 03:26Z); denominator: the DLQ's visible plus in-flight count before and after.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R60_G.md</decomp_doc> round 60, workstream ~GREL4: the clean-up of run 7H's own synthetic message (CTO msg 11785: delete it by receipt handle, no purge, as 2.0.0_SA_COO~Y2 did for S243).
<owned_cells>AR-g-180</owned_cells>
</decomp_ref>

  <objective>
    Delete exactly one SQS message, run 7H's synthetic generation message, from irpt-generation-dlq by its receipt handle, once it has arrived there. WHY: the resident refused run 7H's composition (CLOSED_COMPOSITION_REQUIRED, row S245) three times; the request, job and ticket rows are deleted, so the message keeps failing and lands in the DLQ after its fifth receive. It is synthetic and no one will redrive it. THIS ORDER STARTS ONLY ON MY GO MESSAGE.
  </objective>

  <context>
    Queues (names as in your earlier reads): source `irpt-generation` (visibility 900 s, maxReceiveCount 5, redrive to `irpt-generation-dlq`). The 7H message: your row S245 and receipt irpt_anlreq_fwd10_multicomp_7h/A_E2E7H.txt (request REQ-e90c581652f6c90d3e33af23). Y2's precedent: row S243 (two older synthetic messages deleted by receipt handle, DLQ left empty).
  </context>

  <the_act>
    GO only on my message. In this order, stopping at the first step that does not read as written:
    1. R0: print the date, the two queue names, and for BOTH queues the approximate visible, in-flight and delayed counts (the denominator).
    2. Wait for the message: poll the DLQ counts every few minutes until the DLQ visible count is at least 1 or the source queue reads 0 visible and 0 in flight, up to 04:00Z. If the source queue still holds it at 04:00Z, STOP and report the counts (no delete).
    3. Receive from the DLQ (batch of up to 10, wait 2 s). For each message received decide `is7h` = its body contains the request id REQ-e90c581652f6c90d3e33af23 (yes or no; never print the body or an attribute value). A message that is not 7H's: change its visibility to 0 at once and do not touch it. Delete the 7H message by its receipt handle ONLY. If the DLQ holds no 7H message after two receives, STOP and report.
    4. C: print the DLQ and source counts after (allow a minute for the counts to settle). Expected: the DLQ holds what it held before step 3 minus nothing else (the 7H message was the extra), the source holds 0 visible and 0 in flight.
    5. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_7h_dlq_delete/A_DLQ_DELETE.txt with the lines `R0 ...`, `W waited_until=<time> dlq_visible=<n>`, `M received=<n> is7h=<n> returned=<n>`, `D deleted=1 by_receipt_handle`, `C dlq_before=<n> dlq_after=<n> source_visible=<n> source_inflight=<n>`, and the final line `DLQ-DELETE-DONE` (or `DLQ-DELETE-STOP <why>`). Report ONCE to 2.0.0_SA_COO~G2 (cc 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2).
  </the_act>

  <bounds>
    ONE message deleted, by receipt handle. No purge-queue, no redrive, no change to any queue attribute, no deletion of any message that is not 7H's (such a message goes back to visibility 0 at once). Print counts and yes/no only. Not alongside another act on these queues.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_7h_dlq_delete/IRPT_ANLREQ.TO-DELETE-7H-DLQ-MESSAGE.one-synthetic-generation-message-by-handle-ib2.proof_of_spec.json`.
    <criterion id="DLQ7H-AC1" cell_refs="AR-g-180">The record states the final line and exactly one deletion.<invocation>grep -c -E '^(DLQ-DELETE-DONE|D deleted=1 by_receipt_handle)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_7h_dlq_delete/A_DLQ_DELETE.txt</invocation><expect>^2$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a CLEAN-UP order to a tier-2 CloudOps seat on the CTO's msg 11785 (delete the synthetic message by receipt handle, no purge), not a worker cell; the cell AR-g-180 is the issuer's, as for TO-READ-RETENTION-CENSUS.
