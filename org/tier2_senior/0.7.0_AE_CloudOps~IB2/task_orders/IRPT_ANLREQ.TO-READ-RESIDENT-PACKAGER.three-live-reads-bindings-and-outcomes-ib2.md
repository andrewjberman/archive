<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-RESIDENT-PACKAGER.three-live-reads-bindings-and-outcomes-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-17</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ57</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-396</owned_cells>
<decomp_context>Round 43, cell AR-y-396: three read-only live reads that replace the two reads of TO-READ-RESIDENT-COMMENTARY (AR-y-395) that read the wrong thing: R3 read the service UNIT environment, but the resident sets its queue environment in-process from its BINDINGS file (reports/resident_installed.py:571-584), and R2 counted `PackagerRefused`, but the poll prints terminal results as `IRPT_RESIDENT_PACKAGE outcome=<code>` (ycharts/generate/resident_worker.py:1075).</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order: no write, no restart, no queue receive or delete, no deploy. Reads: the installed bindings file's KEY NAMES and two booleans, the resident journal for counts, one comparison of two queue names printed as a boolean.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- your principal's existing reads; a DENIED read prints DENIED and the order goes on.
comp-adversary: RUN -- by reading IB2's A_COMMENTARY_READS.txt (R1 to R5) against resident_installed.py:571-596 and resident_worker.py:1053-1077; the lens: printing a queue URL or any binding value (forbidden: names and booleans only), a SQS receive (forbidden), a journal line copied (counts and closed codes only), a count without its window and total, the wrong literal again. NOT seen (blind): the bindings file's path (the r34k apply knew it); denominator: three reads.
</preflight>

  <objective>
    Settle whether the RUNNING resident is bound to the analysis_ready and commentary_ready queues, and what it did with the messages it polled, so the issuer can say where the chain between a drafted request and a retained commentary PDF stops. Reads only.
  </objective>

  <context>
    Load /cloud-ops first. Your first read order returned (msg 10639): the running release is irpt-resident-0485393f3a-r34k at pin 1ad8bd8c1bb8 and its installed producer has `produce_commentary_pdf` (so the code is there); 29,932 journal lines over 7 days; one `skipped=COMMENTARY_NOT_REQUESTED` line for Andrew's request; the commentary-ready dead letter holds 1 message aged 173,328 s (about 48 h) with maxReceiveCount 3; the drafter Lambda has its queue and model settings set. This order closes what that read could not see.
  </context>

  <the_act>
    GO now. Each step is independent; a DENIED or ERROR is written and the next step runs. Never print a binding VALUE, a queue URL, a message body, a request body or an email address.
    1. R1 (the bindings the resident loaded): open the INSTALLED bindings file the running service reads (the file `reports/resident_installed.py` loads as `BINDINGS_NAME`; find it by the method your r34k apply used). Print the TOP-LEVEL KEY NAMES in sorted order, and for each of `analysis_ready_queue_url`, `commentary_ready_queue_url` and `packager` print `set` (non-empty) or `unset` or `absent`, never the value. Then print `queue_names_match=<yes|no|NOT-RUN>`: whether the queue NAME (the last path segment only, compared inside your shell, not printed) of the bound `commentary_ready_queue_url` equals `outlook-global-commentary-draft-commentary-ready-queue`, and the same for `analysis_ready_queue_url` against `outlook-global-commentary-draft-analysis-ready-queue`. Line: `R1 keys=<a,b,...> analysis_ready_queue_url=<set|unset|absent> commentary_ready_queue_url=<set|unset|absent> packager=<set|unset|absent> commentary_queue_name_match=<yes|no> analysis_queue_name_match=<yes|no>`.
    2. R2 (what the packager poll did): from the same 7-day journal window as before, COUNTS ONLY of these literals: `IRPT_RESIDENT_PACKAGE outcome=` in total and per closed outcome code (an UPPER_SNAKE word after `outcome=`, one count each), `ANALYSIS_READY_QUEUE_UNSET`, `IRPT_RESIDENT_READY_SIGNAL` in total, and the count of lines naming `REQ-d47252fe74634d0c5cdd8067`. Print the window and the total lines scanned. Line: `R2 window=<first>..<last> scanned=<n> package_outcomes=<n> outcome_codes=<CODE:n,...|none> ready_queue_unset=<n> ready_signals=<n> d47252fe=<n>`.
    3. R3 (the dead letter's cause class, without touching the message): CloudWatch `get-metric-statistics`, namespace AWS/SQS, dimension QueueName=outlook-global-commentary-draft-commentary-ready-queue, metrics NumberOfMessagesReceived and NumberOfMessagesSent and NumberOfMessagesDeleted, statistic Sum, the last 7 days, period 86400 (one datapoint per day; print the three sums per day). NEVER receive a message. Line: `R3 sent=<d1:n,d2:n,...> received=<...> deleted=<...>`.
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_resident_packager/A_RESIDENT_PACKAGER.txt with exactly the lines R1 to R3 (each answered, denied or `NOT-RUN <why>`) and a closing line `READS-DONE <n> of 3 answered`. Report ONCE to 2.0.0_SA_COO~Y2 with the file path and the three lines. No ledger: nothing is deployed.
  </the_act>

  <bounds>
    Reads only. No SQS receive, delete, purge or send; no restart, stop or start; no write to any table, bucket or host file; no value of any binding, environment variable, secret or message. Journal lines are counted, never copied.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_resident_packager/IRPT_ANLREQ.TO-READ-RESIDENT-PACKAGER.three-live-reads-bindings-and-outcomes-ib2.proof_of_spec.json`.
    <criterion id="RRP-AC1" cell_refs="AR-y-396">All three read lines and the closing line are present, each answered, denied or marked not run.<invocation>grep -c -E '^(R1|R2|R3) (keys=|window=|sent=|DENIED |NOT-RUN |ERROR )|^READS-DONE [0-9]+ of 3 answered$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_resident_packager/A_RESIDENT_PACKAGER.txt</invocation><expect>^4$</expect></criterion>
    <criterion id="RRP-AC2" cell_refs="AR-y-396">No line holds an email address, a queue or bucket URL, an access key or a bucket-style name (the leak control).<invocation>grep -c -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|https://sqs\.|arn:aws:s3:::|AKIA[0-9A-Z]{12,}|opal-data-[a-z0-9-]+' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_resident_packager/A_RESIDENT_PACKAGER.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-396 is the issuer's, as for TO-READ-RESIDENT-COMMENTARY.
