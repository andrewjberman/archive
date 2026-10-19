<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-DLQ-INVENTORY.every-dead-letter-message-id-firm-date-count-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-19</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- READ ONLY: the dead-letter queue is read with a zero visibility timeout and never consumed; no delete, purge, redrive or send; nothing is written except the record file.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- your principal's existing read reach, or the step is written DENIED.
comp-adversary: RUN -- by reading the CTO ruling (msg 11081 item 1: record every message's request id, firm, filed date and receive count; ids and counts only, nothing from the body; zero visibility; consume nothing) and your read A_DLQ_WHY.txt (8 messages; one receive returned 4) against this cell; the lens: a receive that hides a message from the resident (zero visibility only), a body field leaked (only the closed kind word, request id and tenant are parsed), a receive loop that never ends (a hard cap of 8 receives), a message missed because one receive samples a subset (repeated receives until the distinct set stops growing), a delete or redrive (forbidden). NOT seen (blind): a message that is invisible because another consumer holds it; denominator: the queue's reported depth, and the number of distinct messages seen.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ80: the dead-letter inventory (cell AR-y-421).
<owned_cells>AR-y-421</owned_cells>
</decomp_ref>

  <objective>
    Record, for EVERY message in `irpt-generation-dlq`, its request id, tenant (firm), filed date and receive count, so the CTO's redrive decision (by 2026-10-22 12:00Z) is made on the whole set. Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the table. Read only; no ledger. Do this BEFORE the run-4 order (it takes minutes).
  </objective>

  <context>
    Load /cloud-ops first. Your read `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_dlq_read/A_DLQ_WHY.txt` found the queue's depth 8 and one receive returning 4, two distinct requests. An SQS receive samples a subset of the queue's servers; with long polling (a wait of 20 s) and repeated receives the whole set is returned. THE RULE: print ids, tenants, dates, counts and ages only; never a body beyond the closed `kind` word, the `request_id` and the `tenant`; never a URL, email, token or signature.
  </context>

  <the_act>
    GO now. Never delete, purge, redrive or send. Every receive uses `--visibility-timeout 0`.
    1. Print the queue's `ApproximateNumberOfMessages` and `ApproximateNumberOfMessagesNotVisible` (the denominator).
    2. Receive repeatedly (`--max-number-of-messages 10 --wait-time-seconds 20`, attributes `SentTimestamp` and `ApproximateReceiveCount`), at most 8 receives, stopping at the first receive that returns no message not already seen or when the distinct messages seen reach the queue's depth. Identify a message by its `MessageId` (held in memory only, never printed in full: print its first 8 characters). Parse the closed `kind` word, the `request_id` and the `tenant` from each body.
    3. For each DISTINCT message print one row: `M <MessageId first 8> kind=<KIND> request=<request id> tenant=<tenant> sent=<UTC date from SentTimestamp, yyyy-mm-dd hh:mm> age_days=<one decimal> receive_count=<n>`. Then, for each distinct request id (the same request may appear in more than one message), print one row: `Q <request id> tenant=<tenant> messages=<n> accepted=<UTC from the request item's acceptance time if you read it, else NOT-READ> ticket=<yes|no|NOT-READ>` where the request item (irpt-requests, key tenant and `analysis#<request id>#1`, ConsistentRead) is read for the acceptance time and the presence of `ticket_id` (a boolean) only.
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_dlq_inventory/A_DLQ_INVENTORY.txt with the rows M and Q, a line `COUNTS depth=<n> distinct_messages=<n> distinct_requests=<n> receives=<n>` and a closing line `INVENTORY-DONE complete=<yes|no>` (yes only when the distinct messages equal the depth read in step 1, otherwise no with the shortfall named). Commit it and report ONCE.
  </the_act>

  <bounds>
    Read only. No write to any table, queue, bucket or log other than the record file; no delete; no redrive; no purge; no send; at most 8 receives with visibility timeout 0; no deploy; no IAM change. Nothing about Andrew's ticket TCK-20261017-5af976ff is read.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_dlq_inventory/IRPT_ANLREQ.TO-READ-DLQ-INVENTORY.every-dead-letter-message-id-firm-date-count-ib2.proof_of_spec.json`.
    <criterion id="DLQI-AC1" cell_refs="AR-y-421">The record holds the counts line and the closing line.<invocation>grep -c -E '^(COUNTS depth=[0-9]+ distinct_messages=[0-9]+ distinct_requests=[0-9]+ receives=[0-9]+|INVENTORY-DONE complete=(yes|no))' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_dlq_inventory/A_DLQ_INVENTORY.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="DLQI-AC2" cell_refs="AR-y-421">No line holds a token, a URL, a signature or an email address (the leak control).<invocation>grep -c -E 'eyJ[A-Za-z0-9_-]{10,}|https?://|Bearer |X-Amz-|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_dlq_inventory/A_DLQ_INVENTORY.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-421 is the issuer's, as for TO-READ-DLQ-WHY.
