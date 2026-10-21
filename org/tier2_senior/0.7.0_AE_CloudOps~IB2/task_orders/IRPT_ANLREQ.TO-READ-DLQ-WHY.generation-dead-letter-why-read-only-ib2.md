<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-DLQ-WHY.generation-dead-letter-why-read-only-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-19</date>
    <status>complete</status><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene, CTO msg ~15:10Z): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 -->
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- READ ONLY: no write, no deploy, no delete, no redrive, no purge, no send; the dead-letter queue is read with a zero visibility timeout and never consumed; nothing is created. No ledger: nothing is deployed.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- your principal's existing read reach, or the step is written DENIED.
comp-adversary: RUN -- by reading the CTO's ruling (msg 10793: "the DLQ holds REQ-8966d24f, a real Cottonwood staff request from 10-08 with no ticket. Read why it failed and propose its redrive or its closure, as its own cell"), your own earlier read A_RESOLVE_LIVE.txt (R3 and N4: 8 messages, 4 received, two request ids) against this cell; the lens: a receive that hides a message from the resident (visibility timeout 0 only), a delete or redrive (forbidden), a log line that leaks a URL, email, token or client value (only closed words are printed), a loop of receives (one call only), an apply running alongside (none: this order is read-only and may run while the run-4 order waits). NOT seen (blind): the four dead-letter messages one receive did not return; denominator: three reads and one closing line.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ79: why the generation dead letter holds a real Cottonwood staff request, read-only (cell AR-y-420).
<owned_cells>AR-y-420</owned_cells>
</decomp_ref>

  <objective>
    Answer, by reads only, WHY the real Cottonwood staff request REQ-8966d24ffefa1c28269ef26c (accepted 2026-10-08T21:10Z, no ticket) is in `irpt-generation-dlq`, and whether the queue's other messages are at risk of expiring, so the issuer can propose a redrive or a closure. Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the lines. This order is READ ONLY and may run at any time outside the weekday 11:30Z-14:15Z band; it does not wait for the run-4 order.
  </objective>

  <context>
    Load /cloud-ops first. Your own read `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_resolve_live/A_RESOLVE_LIVE.txt` (R3, N4) found: `irpt-generation-dlq` depth 8; one zero-timeout receive returned 4 messages, kind `analysis_generate`, two requests: REQ-8966d24ffefa1c28269ef26c (tenant cottonwood, owner a non-synthetic Opal-Global staff principal, no ticket id, accepted 2026-10-08T21:10Z) and REQ-4b5155ac2ea9467ab771b414 (tenant 49financial, a synthetic FWD-1 staff request with a ticket id, accepted 2026-10-09T14:59Z). The first is a real staff request that never produced a report and was never shown to its filer (no ticket). The CTO wants the cause and a redrive-or-closure proposal; the issuer writes the proposal from your lines. THE RULE FOR EVERY STEP: print closed words, counts, ages and key NAMES only; never print a URL, a host name, an API id, an email, a token, a signature or a journal or log line beyond the closed literals named below.
  </context>

  <the_act>
    GO now. Each step is independent; a DENIED or ERROR on one is written and the next step runs. Never delete, purge, redrive, send, or receive with a non-zero visibility timeout.
    1. R1 (the two requests' own rows): for each of the two request ids above (with their tenants) read, with ConsistentRead, the job row in `irpt-jobs` (key: tenant and job = the request id) and the request item in `irpt-requests` (key: tenant and `request_revision` = `analysis#<request id>#1`). Print by NAME and closed words only: whether each exists; the job's `state`; the closed failure or attention code the job row carries (the member that names it, and its value if it is an UPPER_SNAKE code); the number of attempts if the row carries one; its last-updated time (UTC to the minute); whether the request item carries a `ticket_id` (boolean), a `commentary_ref` (boolean), and its acceptance time. Line: `R1 <request id first 12 chars> tenant=<t> job=<exists|absent> state=<STATE|none> code=<CODE|none> attempts=<n|none> updated=<UTC|none> item=<exists|absent> ticket=<yes|no> acceptedAt=<UTC|none>` (one line per request).
    2. R2 (the queue itself): `get-queue-attributes` of `irpt-generation-dlq` (ApproximateNumberOfMessages, MessageRetentionPeriod in days, and, from its source queue, which queue names this one as dead letter via `list-dead-letter-source-queues`) and of the source queue (its `RedrivePolicy` maxReceiveCount, its VisibilityTimeout, its ApproximateNumberOfMessages and ApproximateNumberOfMessagesNotVisible), plus ONE `receive-message` on the dead-letter queue with `--visibility-timeout 0 --max-number-of-messages 10 --wait-time-seconds 2` asking for the attributes `SentTimestamp` and `ApproximateReceiveCount` only (never read or print a body beyond the closed `kind` word, the `request_id` and the `tenant`): print, per received message, its age in days (one decimal) from `SentTimestamp`, its `ApproximateReceiveCount`, and its request id's first 12 characters, then the oldest age and the number of days of retention LEFT for the oldest (retention minus age; a negative or tiny value is the finding: the messages expire). Line: `R2 dlq_depth=<n> retention_days=<n> source=<name|NOT FOUND> max_receive=<n> source_visibility_s=<n> source_depth=<n> source_not_visible=<n> received=<n> ages_days=<a,b,...> receive_counts=<a,b,...> oldest_retention_left_days=<x>`.
    3. R3 (why it failed, from retained logs): for the FIRST request id only, count and print the closed words of every retained log line that names it: (a) the resident service's journal (`journalctl` for the resident unit, as in your earlier reads): lines containing the request id, with the window scanned (first and last timestamp) and the total lines scanned; (b) the CloudWatch log groups of the generation Lambda `irpt-ycharts-generate` and of the resident-side group if one exists, for 2026-10-08 20:00Z to 2026-10-09 23:00Z, filtered by the request id: the count of matching events and, for at most 20 of them, ONLY the leading closed literal (a word matching `^[A-Z][A-Z0-9_]+`) and the second token if it is an UPPER_SNAKE code; also print each group's retention setting and whether the earliest retained event is before or after 2026-10-08T21:00Z (if the logs are gone, say `LOGS-NOT-RETAINED`). Line: `R3 journal_window=<first>..<last> scanned=<n> journal_hits=<n> cw_groups=<name:retention_days:earliest_before_21z=<yes|no>,...> cw_hits=<n> literals=<LITERAL:n,...|none>`.
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_dlq_read/A_DLQ_WHY.txt with the lines R1 (two lines), R2 and R3 (each answered, denied or `NOT-RUN <why>`) and a closing line `READS-DONE <n> of 3 answered`. Commit it. Report ONCE as in the objective: the file path and the lines, nothing more. No ledger.
  </the_act>

  <bounds>
    Read only. No write to any table, queue, bucket or log; no delete; no redrive; no purge; no send; ONE receive call with visibility timeout 0; no deploy; no Terraform; no IAM change. Nothing about Andrew's ticket TCK-20261017-5af976ff or any client object beyond the two request ids is read.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_dlq_read/IRPT_ANLREQ.TO-READ-DLQ-WHY.generation-dead-letter-why-read-only-ib2.proof_of_spec.json`.
    <criterion id="DLQW-AC1" cell_refs="AR-y-420">The record holds the four answer lines (R1 twice, R2, R3) and the closing line, each answered, denied or not run.<invocation>grep -c -E '^(R1 |R2 |R3 |READS-DONE [0-9]+ of 3 answered)' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_dlq_read/A_DLQ_WHY.txt</invocation><expect>^5$</expect></criterion>
    <criterion id="DLQW-AC2" cell_refs="AR-y-420">No line holds a token, a URL, a signature or an email address (the leak control).<invocation>grep -c -E 'eyJ[A-Za-z0-9_-]{10,}|https?://|Bearer |X-Amz-|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_dlq_read/A_DLQ_WHY.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-420 is the issuer's, as for TO-READ-RESOLVE-LIVE.
