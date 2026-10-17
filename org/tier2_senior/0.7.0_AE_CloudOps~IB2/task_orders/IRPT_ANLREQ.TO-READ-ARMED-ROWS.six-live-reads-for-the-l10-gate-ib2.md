<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-ARMED-ROWS.six-live-reads-for-the-l10-gate-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-17</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order, six live AWS reads with your principal, none of which writes: one SQS get-queue-attributes (two queues), one DynamoDB Scan of irpt-requests that returns a COUNT and no item, three Lambda get-function or get-function-configuration reads (one downloads the code zip to a scratch folder outside the repository to list its member NAMES, then deletes your own scratch), one Lambda list-event-source-mappings. No secret value is read or printed: environment variables are read for key NAMES and, where stated, a boolean or a domain list, never a value.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger. comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; your principal's existing reads. If a read is DENIED, that read prints DENIED and the order goes on: a denial is an answer, not a stop.
comp-adversary: RUN -- by reading the six armed surprise rows (IRPT_ANLREQ-D2-S26, -W129-S1, -W144-S1, -W147-S2, -S118, -W146-S4, and the W77-S3 calendar question) and the audit lines that sent them here (org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~287/r47/AUDIT_a.json and ~288/r47/AUDIT_b.json) against this cell; the lens: a Scan that returns items (it must return a COUNT only, with a filter, and print no attribute value), an environment dump (names and booleans only), a receive or delete on the commentary-ready queue (never: attributes only, the queue's admitted consumer is the resident), a zip left in a place the repository sees, a read that quietly fails and reads as a zero. The order requires a DENIED or ERROR line to be written as such, never as a count of 0. NOT seen (blind): the content of any stored item and any env value; denominator: 6 reads, 8 output lines.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ51: the live reads that the L10 gate's armed rows still need.
<owned_cells>AR-y-390</owned_cells>
</decomp_ref>

  <objective>
    Make the six live reads below ONCE, write their results as the lines of step 8 in org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_armed_reads/A_ARMED_READS.txt, commit it alone with .tools/safe-commit.sh, and report ONCE to 2.0.0_SA_COO~Y2 with the commit and the eight lines. Change NOTHING in AWS or on any host. Each read answers a question that an armed surprise row left unread; the issuer dismisses a row only on your line.
  </objective>

  <context>
    Load /cloud-ops first. The six rows are armed surprise rows in org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md whose disarm owner is 2.0.0_SA_COO~Y2; the pre-L10 audit (TO-AR-y-387 and TO-AR-y-388) marked each NEEDS-LIVE-READ. Region and account as your principal's default (account 313476888478). Resource names: queue `outlook-global-commentary-draft-commentary-ready-queue` and its DLQ `outlook-global-commentary-draft-commentary-ready-dlq`; table `irpt-requests`; functions `irpt-status`, `irpt-ycharts-generate`, `opal-ticket-api` and `outlook-global-commentary-draft-lambda`. Read every name from the graph or the live account first and print it (`comp-estate`/describe of one resource each is FREE); a name that does not resolve is reported `NAME-NOT-FOUND <name>`, not guessed.
  </context>

  <the_act>
    GO now. Start at step 1; every step is independent, so a DENIED or ERROR on one is written and the next step runs.
    1. R1 (row D2-S26): `aws sqs get-queue-attributes` for the commentary-ready queue and for its DLQ, attributes ApproximateNumberOfMessages, ApproximateNumberOfMessagesNotVisible, ApproximateNumberOfMessagesDelayed. NEVER receive or delete a message. Line: `R1 queue=<n> notvisible=<n> delayed=<n> dlq=<n>` (a denied read: `R1 DENIED <what>`).
    2. R2 (row D2-W129-S1): one DynamoDB `scan` of `irpt-requests`, ConsistentRead true, `--select COUNT` (so no item is returned), with a FilterExpression that counts the request rows whose `owner` map has the attribute `home_firm_id` AND whose `owner.principal_class` is not `OPAL_GLOBAL`, using ExpressionAttributeNames for the nested path; paginate to the end and SUM the counts; print the table's total scanned count beside it (the denominator). Line: `R2 owners_with_home_firm_id_nonglobal=<n> of scanned=<m>`. If the table's key refuses the scan, write `R2 DENIED <what>`; a count printed without its scanned total is invalid.
    3. R3 (rows D2-W144-S1 and D2-W77-S3): `aws lambda get-function --function-name irpt-status` and the same for `irpt-ycharts-generate`; for each, download the code zip from the returned presigned location into a NEW scratch folder outside the repository, list the member NAMES only (python zipfile namelist, `-I`), print whether the name `ycharts/generate/acceptance.py` is present in irpt-status and whether any name starts with `pandas_market_calendars/` in irpt-ycharts-generate, print each function's CodeSha256, then delete the scratch folder you created. Lines: `R3a irpt-status acceptance.py=<PRESENT|ABSENT> members=<n> sha=<CodeSha256>` and `R3b irpt-ycharts-generate pandas_market_calendars=<PRESENT|ABSENT> members=<n> sha=<CodeSha256>`.
    4. R4 (row D2-W147-S2): `aws lambda list-event-source-mappings --function-name outlook-global-commentary-draft-lambda` (State of each mapping and its source queue NAME) and `get-function-configuration` of the same function for the environment KEY NAMES only, plus State. Line: `R4 drafter state=<Active|...> mappings=<name:State,...> env_has_KIMI_STANDING_WORD_REF=<yes|no>` (never an env value).
    5. R5 (row D2-S118): `get-function-configuration` of `irpt-ycharts-generate`; parse the environment variable `IRPT_DIRECTORY_BUCKET_MAP` as JSON in memory and print only its KEY names (firm tokens) and the count, and whether any key is a staff or Global token (`global`, `opal-global`, `staff`, `opal-capital`). Never print a bucket name or any value. Line: `R5 directory_map_keys=<k1,k2,...> count=<n> has_global_or_staff_key=<yes|no>`.
    6. R6 (row D2-W146-S4): `get-function-configuration` of `opal-ticket-api`; parse `TICKET_DL_MAP` as JSON in memory. Line: `R6 ticket_dl_map=<EMPTY|NONEMPTY> firms=<n> recipient_domains_outside_opalinvest_com=<n>` (domains and counts only, never an address).
    7. Verify, before writing, that no printed line holds a bucket name, an email address, a token or an environment value; a line that does is rewritten without it.
    8. Write the file with EXACTLY these lines, in this order, one per tag, each as specified above (a read that did not run is `<tag> NOT-RUN <why>`): `R1 ...`, `R2 ...`, `R3a ...`, `R3b ...`, `R4 ...`, `R5 ...`, `R6 ...`, then `READS-DONE <n> of 7 answered`. Commit it alone and report ONCE to 2.0.0_SA_COO~Y2 (cc nobody): "armed-row reads done" with the commit and the eight lines.
  </the_act>

  <bounds>
    Six read-only live AWS reads and one scratch download of a code zip that you delete. No write, no Terraform, IAM, Lambda, queue, table or route change, no SQS receive or delete, no secret value, no env value, no item content, no sign-in, no host command. Not in this order: any disposition of a row (the issuer's), window 5, the classifier.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_armed_reads/IRPT_ANLREQ.TO-READ-ARMED-ROWS.six-live-reads-for-the-l10-gate-ib2.proof_of_spec.json`.
    <criterion id="ARR-AC1" cell_refs="AR-y-390">All seven read lines and the closing line are present, each read answered, denied or marked not run, never silently missing.<invocation>grep -c -E '^(R1|R2|R3a|R3b|R4|R5|R6) (queue=|owners_with_home_firm_id_nonglobal=|irpt-status acceptance.py=|irpt-ycharts-generate pandas_market_calendars=|drafter state=|directory_map_keys=|ticket_dl_map=|DENIED |NOT-RUN |NAME-NOT-FOUND |ERROR )|^READS-DONE [0-9]+ of 7 answered$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_armed_reads/A_ARMED_READS.txt</invocation><expect>^8$</expect></criterion>
    <criterion id="ARR-AC2" cell_refs="AR-y-390">No line holds an email address, a bucket-style name or a key-like token (the leak control).<invocation>grep -c -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|arn:aws:s3:::|AKIA[0-9A-Z]{12,}|opal-data-[a-z0-9-]+' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_armed_reads/A_ARMED_READS.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-390 is the issuer's, as for TO-READ-PACING and TO-RUN-FWD1.
