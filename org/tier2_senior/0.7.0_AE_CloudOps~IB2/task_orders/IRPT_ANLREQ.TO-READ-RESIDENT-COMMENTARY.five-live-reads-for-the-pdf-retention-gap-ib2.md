<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-RESIDENT-COMMENTARY.five-live-reads-for-the-pdf-retention-gap-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-17</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ56</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-395</owned_cells>
<decomp_context>Round 43, cell AR-y-395: five read-only live reads that close the NOT READ items of worker 292's code trace (TO-AR-y-394, record org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~292/r51/TRACE_COMMENTARY_PDF_RETENTION.md) on the CTO's ruling (msg 10630): why no commentary PDF is retained for any request.</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order: no write, no invoke, no queue receive or delete, no restart, no deploy. The reads are: a read of the resident host's installed release (by the method your r34k apply used), a read of its service journal for counts, a read of the resident service's environment KEY NAMES, a read of the commentary draft Lambda's environment KEY NAMES, and one CloudWatch GetMetricStatistics. No secret value, no message body, no client data is read or printed.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- your principal's existing reads. A DENIED read prints DENIED and the order goes on: a denial is an answer, not a stop.
comp-adversary: RUN -- by reading worker 292's trace (T3, T5, T6 NOT READ items) and the issuer's live reads (rows IRPT_ANLREQ-D2-S207, -S208) against this cell; the lens: a SQS receive-message (forbidden: it hides the message and bumps its receive count), a printed environment value, a journal excerpt that carries a request body or client text (counts and closed codes only), a count printed without its denominator (the journal window and line total travel with it), and a read of the wrong release (R1 names the release the RUNNING service loaded, not the newest tarball). NOT seen (blind): the resident host's file layout; denominator: the five reads.
</preflight>

  <objective>
    Answer five questions about the LIVE resident and the commentary draft Lambda, with counts, booleans and key names only, so the issuer can say which release retains the commentary PDF and where the chain stops. No fix, no change.
  </objective>

  <context>
    Load /cloud-ops first. Facts the issuer has already measured (read-only, 2026-10-17): in tenant 49financial the 206 artifact items hold 2 commentary DRAFTS (family ANALYSIS_COMMENTARY), 3 Overview PDFs (family YCHARTS_OPAL_REPORT, logical id request-overview-sha) and NO commentary PDF under any logical-id shape; the commentary-ready queue has no Lambda event source mapping (the resident host polls it), its DLQ holds 1 message, the draft Lambda's analysis-ready queue is mapped and empty. Worker 292's trace: the resident poll (ycharts/generate/resident_main.py:73-75, resident_worker.py:1053-1077) builds the packager at reports/resident_installed.py:449-498 and binds the commentary_ready queue at :583-584; the packager's HEAD code retains the PDF with opal_producer.produce_commentary_pdf (opal_packager.py:197-199), while the r34k base pin 0485393f had a packager calling produce_package under another logical id and no produce_commentary_pdf; the r34k record (org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/r34k/RESIDENT_R34K_BUILD.json) names pin_full_sha 1ad8bd8c1bb83ecc35d9489014a42c53812f4424 and base_pin 0485393f3ad0a7e564f4867f5e70003e2e62195b and does not say which one the tarball bindings carry.
  </context>

  <the_act>
    GO now. Start at step 1; every step is independent, so a DENIED or ERROR on one is written and the next step runs. Never print an environment value, a message body, a request body, an email address or a bucket name.
    1. R1 (which release RUNS): on the resident host, by the method your r34k apply used, read the release the running service loaded: the release or tarball identifier, its sha256, and the pin it was built at; then, on the INSTALLED copies of `opal_producer.py` and `opal_packager.py`, print booleans only: whether `def produce_commentary_pdf` is present in opal_producer.py, whether `def package_logical_id` is present in opal_producer.py, whether `produce_commentary_pdf` is named in opal_packager.py (grep -c). Line: `R1 release=<id> sha256=<64 hex> pin=<12 hex> produce_commentary_pdf=<yes|no> package_logical_id=<yes|no> packager_calls_commentary_pdf=<yes|no>` (a denied read: `R1 DENIED <what>`).
    2. R2 (what the service logged): read the resident service's journal for the last 7 days (the unit that runs ycharts/generate/resident_main.py). Print the journal window (first and last timestamp) and the total lines scanned as the denominator. Then COUNTS ONLY of these literal substrings: `IRPT_RESIDENT_READY_SIGNAL skipped=COMMENTARY_NOT_REQUESTED`, `IRPT_RESIDENT_READY_SIGNAL skipped=NO_TICKET`, `ANALYSIS_READY_SEND_FAILED`, `PackagerRefused`, and for each closed refusal code that appears after `PackagerRefused` (a code is an UPPER_SNAKE word) one count. Also the count of lines that name the request `REQ-d47252fe74634d0c5cdd8067` and the count that name `REQ-d6231c013ae90519c67d18e9` (counts, never the lines). Line: `R2 window=<first>..<last> scanned=<n> skipped_not_requested=<n> skipped_no_ticket=<n> send_failed=<n> packager_refused=<n> codes=<CODE:n,...|none> d47252fe=<n> d6231c01=<n>`.
    3. R3 (does the service poll the queue): read the resident service's environment KEY NAMES (the unit's Environment or its env file) and print, for each of `IRPT_ANALYSIS_READY_QUEUE_URL` and every name containing `COMMENTARY_READY`, whether it is set (non-empty) as a boolean, never the value. Line: `R3 resident_env <NAME>=<set|unset|absent>;...`.
    4. R4 (the drafter): `aws lambda get-function-configuration --function-name outlook-global-commentary-draft-lambda`: print the CodeSha256, LastModified, and for each of `COMMENTARY_READY_QUEUE_URL` and `KIMI_STANDING_WORD_REF` whether it is set (boolean, never the value), plus the list of all environment KEY NAMES. Line: `R4 drafter sha=<CodeSha256> modified=<UTC> COMMENTARY_READY_QUEUE_URL=<set|unset|absent> KIMI_STANDING_WORD_REF=<set|unset|absent> keys=<NAME,NAME,...>`.
    5. R5 (how long the dead letter has waited): CloudWatch `get-metric-statistics`, namespace AWS/SQS, metric ApproximateAgeOfOldestMessage, dimension QueueName=outlook-global-commentary-draft-commentary-ready-dlq, the last 24 hours, period 3600, statistic Maximum; also the main queue `outlook-global-commentary-draft-commentary-ready-queue` RedrivePolicy maxReceiveCount from get-queue-attributes (attribute RedrivePolicy). NEVER receive a message. Line: `R5 dlq_oldest_age_max_s=<n|none> datapoints=<n> maxReceiveCount=<n>`.
    6. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_reads/A_COMMENTARY_READS.txt with exactly the lines R1 to R5 (each answered, denied or `NOT-RUN <why>`) and a closing line `READS-DONE <n> of 5 answered`. Report ONCE to 2.0.0_SA_COO~Y2 with the file path and the five lines, nothing more. No ledger is needed: nothing is deployed.
  </the_act>

  <bounds>
    Reads only. No SQS receive, delete, purge or send; no restart, stop or start; no write to any table, bucket or host file; no value of any environment variable, secret or message. Journal lines are counted, never copied.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_reads/IRPT_ANLREQ.TO-READ-RESIDENT-COMMENTARY.five-live-reads-for-the-pdf-retention-gap-ib2.proof_of_spec.json`.
    <criterion id="RRC-AC1" cell_refs="AR-y-395">All five read lines and the closing line are present, each answered, denied or marked not run, never silently missing.<invocation>grep -c -E '^(R1|R2|R3|R4|R5) (release=|window=|resident_env |drafter sha=|dlq_oldest_age_max_s=|DENIED |NOT-RUN |ERROR )|^READS-DONE [0-9]+ of 5 answered$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_reads/A_COMMENTARY_READS.txt</invocation><expect>^6$</expect></criterion>
    <criterion id="RRC-AC2" cell_refs="AR-y-395">No line holds an email address, a queue or bucket URL, an access key or a bucket-style name (the leak control).<invocation>grep -c -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|https://sqs\.|arn:aws:s3:::|AKIA[0-9A-Z]{12,}|opal-data-[a-z0-9-]+' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_reads/A_COMMENTARY_READS.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-395 is the issuer's, as for TO-READ-ARMED-ROWS.
