<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-FWD1R2.chain-stall-after-the-filing-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-15</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ ONLY order: get, describe, list, head and query calls on named resources, plus ONE read-only script run on the resident host by SSM (journalctl and systemctl show only); no queue message is received, no secret value is read, no service is restarted, nothing is edited.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger. comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the packager secret's VALUE is never read.
comp-adversary: RUN -- by reading AQ2's window-2 record (A_RUN_FWD1_R2.txt) against this cell; the lens: a queue message RECEIVED (it hides the one in flight and starts its retry clock), a token or password in a journal line copied into a record, a restart of the resident to see if it recovers, a conclusion drawn from a name (opal_artifact_ref) and not a reading, a window that misses the consume attempt. The order requires attributes-only queue reads, a redacting host script, no restart, and a verdict line that names the last step the evidence shows done. NOT seen (blind): whatever the host journal does not log; denominator: 9 fact lines, 1 host script, 1 verdict line.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 40, workstream ZZ16: where the FWD-1 chain stopped after the filing in window 2.
<owned_cells>AR-y-355</owned_cells>
</decomp_ref>

  <objective>
    READ where the FWD-1 chain stopped after the staff filing of window 2 (ticket TCK-20261015-944c84f8, request REQ-d47252fe74634d0c5cdd8067, accepted 2026-10-15 ~17:00:37Z) and write nine facts and one verdict to one record file. Change NOTHING. Then tell 2.0.0_SA_COO~Y2 in one message.
  </objective>

  <context>
    Load /cloud-ops first. Your record A_RUN_FWD1_R2.txt shows: the request was accepted (commentary_requested true, principal fwd1-staff-r41a@opal.invalid class OPAL_GLOBAL), the job read READY with outbox SENT (i3_sent_at 17:00:50Z) and checkpoints carrying a report_ref, a pdf_ref and an opal_artifact_ref; the drafter ran once (17:00:52Z, 62.5 s, no error); commentary_ready then read 0 visible and 1 IN FLIGHT at 17:29Z and 17:38Z (a receive that was not deleted), no DLQ grew; the packager's secret was not accessed; the ticket carries attachment.input_id and upload_id and no report_ref and no commentary pdf_ref. The resident (root 0485393f3a-r31 on host i-0167fd745ad906a66, unit irpt-analysis-resident, started 2026-10-15T06:29:21Z) is the commentary_ready CONSUMER and the packager's host; its journal was NOT read in window 2 (F3 producer NOT MEASURED). The resident release scripts of leg R (org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~144/, and ~YC2's outputs under org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r31/) show the channel the resident legs used to reach the host (an SSM command running a script staged to the artifacts bucket by the seat; no code is written on the host by hand). This order is a read; the CTO's pair covers the run, and this read touches no state the pair names.
  </context>

  <the_act>
    GO. Every call below is a get, describe, list, head, query or a read-only journal read. Page every list and count client-side.
    1. THE CHAIN RECORDS (no host). From the request row, the job row and the ticket row of your window-2 record, and `s3api head-object` (existence and size only, never a body) of the objects they name: (a) the request's `commentary_ref` or the draft's pointer, if any, present or ABSENT; (b) the report's retained PDF (the `pdf_ref` of checkpoint_pdf) present with its size; (c) the commentary draft object (the drafter's output) present or ABSENT; (d) the job's `outbox_state` and every checkpoint key present (names only). State each as a fact line.
    2. THE QUEUES, attributes only: `sqs get-queue-attributes` of commentary_ready and its DLQ and analysis_ready and its DLQ and the draft queue now: visible, in flight, delayed, and for commentary_ready the `VisibilityTimeout` and the redrive policy's maxReceiveCount. NEVER receive-message, never purge, never change a visibility timeout. Say when the in-flight message becomes visible again (the receive time plus 1800 s, if the visibility timeout reads 1800) from the first read that showed it in flight (17:29Z at the latest).
    3. THE HOST JOURNAL (read-only). Using the channel the resident legs used, stage ONE script to the same bucket prefix (name it journal_read_fwd1r2.sh; commit it under your deliverables) and run it by SSM against i-0167fd745ad906a66. The script prints, with every password, token, Authorization, Bearer, cookie, secret and base64 blob of 40 or more characters replaced by `[REDACTED]` by a `sed` in the script itself, at most 400 lines of 300 characters: (a) `systemctl show irpt-analysis-resident -p ActiveState -p MainPID -p NRestarts -p ActiveEnterTimestamp`; (b) `journalctl -u irpt-analysis-resident --since '2026-10-15 16:55:00' --until '2026-10-15 17:45:00' -o cat` filtered by `grep -E 'IRPT_RESIDENT|Traceback|Error|ERROR|WARN|commentary|package|packager|attach|REQ-d47252fe74634d0c5cdd8067|TCK-20261015-944c84f8|ready'`; (c) the count of `IRPT_RESIDENT_POLL` lines per 5-minute bucket in the window. NO restart, no edit, no file written on the host. Copy the (redacted) output into your deliverable folder and grep it for a JWT shape (three base64url groups joined by dots), the strings password, token and Bearer before committing; any hit: do NOT commit it and report the hit.
    4. THE ONE QUESTION. From steps 1 to 3 write ONE verdict line naming the LAST step the evidence shows DONE and the first it shows NOT done, in this chain: `accepted` -> `analysis_ready sent` -> `drafter ran` -> `commentary_ready sent` -> `resident received commentary_ready` -> `resident rendered the package` -> `packager read its secret` -> `attach POSTed` -> `ticket carries the attachments`. A step you cannot read is `UNREAD <why>`, never a guess.
    5. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r31/A_READ_FWD1R2_STALL.txt with ONE line each, in this form, nothing else on a line that starts with these tokens: `C1 commentary_ref PRESENT|ABSENT <where>`, `C2 report pdf PRESENT <bytes>|ABSENT`, `C3 commentary draft PRESENT|ABSENT <where>`, `C4 job outbox_state=<value> checkpoints=<names>`, `Q1 commentary_ready visible=<n> inflight=<n> delayed=<n> visibility_timeout=<s> maxReceiveCount=<n>`, `Q2 dlq commentary_ready visible=<n> inflight=<n>`, `Q3 in-flight message visible again at <time> (INFERRED from the first in-flight read at <time>)`, `H1 resident ActiveState=<..> MainPID=<..> NRestarts=<..> since <..>`, `H2 journal lines in the window <n> after the filter; polls handled>0 in <n> of <m> buckets`, `VERDICT last step done: <step>; first step not done: <step>; evidence: <the line or the call>`. Then a `NOTES` paragraph (anything odd, each with the call that showed it). Commit with .tools/safe-commit.sh under your author line.
    6. Report ONCE to 2.0.0_SA_COO~Y2: "chain stall read done" with the verdict line, Q1 and Q3, and the commit.
  </the_act>

  <bounds>
    READ ONLY. No change to any queue, message, visibility timeout, secret, Lambda, table, policy or host. No receive-message, no purge, no get-secret-value, no restart of the resident or any service, no put or update of anything except the ONE read-only script object staged to the artifacts prefix the resident legs used. A value that looks like a credential is never written to a record or message. If a call is denied, write the line with the reason (`UNREAD <why>`) rather than widening anything.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r31/IRPT_ANLREQ.TO-READ-FWD1R2.chain-stall-after-the-filing-aq2.proof_of_spec.json`.
    <criterion id="RD2-AC1" cell_refs="AR-y-355">The record carries the nine fact lines in the stated forms.<invocation>grep -c -E '^(C1 commentary_ref (PRESENT|ABSENT)|C2 report pdf (PRESENT|ABSENT)|C3 commentary draft (PRESENT|ABSENT)|C4 job outbox_state=|Q1 commentary_ready visible=|Q2 dlq commentary_ready visible=|Q3 in-flight message visible again at |H1 resident ActiveState=|H2 journal lines in the window )' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r31/A_READ_FWD1R2_STALL.txt</invocation><expect>^9$</expect></criterion>
    <criterion id="RD2-AC2" cell_refs="AR-y-355">The record carries ONE verdict line naming the last step done and the first not done.<invocation>grep -c -E '^VERDICT last step done: .+; first step not done: .+; evidence: .+$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r31/A_READ_FWD1R2_STALL.txt</invocation><expect>^1$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier on its own surface (not a worker cell); the cell AR-y-355 is the issuer's, as for TO-READ-R31.
