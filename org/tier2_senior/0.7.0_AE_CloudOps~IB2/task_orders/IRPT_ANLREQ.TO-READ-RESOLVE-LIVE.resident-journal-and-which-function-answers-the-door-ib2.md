<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-RESOLVE-LIVE.resident-journal-and-which-function-answers-the-door-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-19</date>
    <status>complete</status><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene, CTO msg ~15:10Z): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 --><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene, CTO msg ~15:10Z): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 -->
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ69</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-409</owned_cells>
<decomp_context>Round 43, cell AR-y-409 (AMENDMENT 1 adds R3, the generation dead letter, on the CTO's msg 10782): three live read-only reads for the CTO's P0 (msg 10773: no accepted request since 2026-10-17; new PROD filings may not be accepted): the resident journal counts by the literals worker 298's trace names, and which Lambda function actually answers the API your run 3 called for the upload POST.</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order: one journal read on the resident host (counts) and AWS describe/get reads of an API's routes and integrations; no write, no restart, no queue receive, no invoke, no deploy.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- your principal's existing reads; a DENIED read prints DENIED and the order goes on.
comp-adversary: RUN -- by reading worker 298's trace (org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~298/r56/RESOLVE_PATH_TRACE.md, X3 and X6) and the issuer's CloudWatch reads (irpt-ycharts-generate invoked 1, 1 and 5 times at 09:40Z, 09:45Z and 10:30Z today and 0 times from 13:00Z to 16:20Z, errors 0) against this cell; the lens: printing a URL, a host name or an API id value into a file (names of functions only; the API is named by its config source), copying a journal line other than the closed literals, a count without its window and total, a SQS receive (forbidden). a DLQ receive that deletes or loops (forbidden: visibility-timeout 0, one call, no delete), a body copied beyond kind, request id and tenant. NOT seen (blind): the journal's unit name (you knew it); denominator: three reads.
</preflight>

  <objective>
    (AMENDMENT 1: R3 added.) Give the CTO the first numbers that explain why no request has been accepted since Oct 17: how often the resident loop polled and resolved today, and whether the API your run 3 called is served by the same Lambda function as the PROD door.
  </objective>

  <context>
    Load /cloud-ops first. The issuer's read-only reads (2026-10-19 ~16:10Z): queue irpt-generation depth 0, not visible 0, its DLQ 8 messages (oldest about 11.8 days); NORMALIZATION rows in irpt-requests: 0 in state RESOLVING in any tenant, the newest resolved row 2026-10-17T05:14Z; the Lambda irpt-ycharts-generate (the function that worker 298's trace names as the upload door) had Invocations 1 (09:40Z), 1 (09:45Z), 5 (10:30Z) today and none between 13:00Z and 16:20Z, Errors 0 all day; irpt-status and opal-ticket-api showed no invocation 14:00Z to 15:00Z either. Your run 3 posted the upload five times at about 14:28Z to 14:35Z and received RESOLVING five times.
  </context>

  <the_act>
    GO now. Each step is independent; a DENIED or ERROR on one is written and the next step runs. Never print a URL, a host name, an API id, an email, a token or a journal line outside the closed literals named below.
    1. R1 (the resident loop today): from the resident service's journal for 2026-10-19 00:00Z to now, print the window (first and last timestamp) and the total lines scanned, then COUNTS per hour (UTC hour of day) of: the lines containing `IRPT_RESIDENT_POLL handled=`, the lines containing `IRPT_RESIDENT_POLL handled=0`, the lines containing `IRPT_RESIDENT_POLL retained_for_retry`, the lines containing `IRPT_RESIDENT_RESOLVE`, and the lines containing `IRPT_RESIDENT_PACKAGE`; and for the `IRPT_RESIDENT_RESOLVE` lines the counts by their `state=<STATE> code=<CODE>` pair (closed words only). Line: `R1 window=<first>..<last> scanned=<n> polls=<h00:n,h01:n,...> handled0=<n> poll_retained=<n> resolve=<n> resolve_pairs=<STATE/CODE:n,...|none> package=<n>`.
    2. R2 (who answers the door your run 3 called): take the API you called in run 3 (named by the config source `portal-vite.config.ts-proxy-auth-target`; read your own run files for its identifier). Without printing any identifier, determine and print by NAME only: whether it is an API Gateway HTTP or REST API; the integration target of the route `POST /api/scoped/investor-reporting/analysis/inputs` (the Lambda function NAME, or `NOT FOUND`); and the same for the route `POST /api/scoped/investor-reporting/analysis`. Then print whether that function name equals `irpt-ycharts-generate`. Also print, from CloudWatch, the Invocations Sum of that function (the one named) for 14:20Z to 14:45Z today in 5-minute buckets, as `bucket:n` pairs. Line: `R2 api_kind=<http|rest|NOT FOUND> inputs_route_target=<function name|NOT FOUND> analysis_route_target=<function name|NOT FOUND> equals_irpt_ycharts_generate=<yes|no|NOT-RUN> invocations_1420_1445=<hh:mm:n,...|none>`.
    3. R3 (the generation dead letter, CTO msg 10782 item 2): the queue `irpt-generation-dlq` holds 8 messages, the oldest about 11.8 days. Read them WITHOUT consuming any: `receive-message` with `--visibility-timeout 0`, `--max-number-of-messages 10`, `--wait-time-seconds 2`, and NEVER delete, purge, redrive or send (a message that is not returned in one call is left; do not loop). From each message body parse ONLY the closed `kind` word and the `request_id` and `tenant` strings; print nothing else from a body. Then for each distinct request id print by name only whether an `analysis#<request id>#1` item exists in irpt-requests for that tenant (ConsistentRead; yes or no) and, if yes, the `ticket_id` presence as a boolean. State the age of each message (SentTimestamp to now, in days with one decimal). Line: `R3 dlq_depth_before=<n> received=<n> kinds=<KIND:n,...> request_ids=<id1,id2,...> tenants=<t:n,...> request_item_exists=<yes:n,no:n> oldest_days=<x.x> newest_days=<x.x> real_filing=<none|<ids>>` where real_filing names an id whose request item exists and carries a ticket id (a real filing), else `none`; also print `dlq_depth_after=<n>` on the same line (it must equal the before value: nothing was consumed).
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_resolve_live/A_RESOLVE_LIVE.txt with the lines R1, R2 and R3 (each answered, denied or `NOT-RUN <why>`) and a closing line `READS-DONE <n> of 3 answered`. Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the three lines, within minutes of finishing: the CTO is waiting on the first explaining number. No ledger: nothing is deployed.
  </the_act>

  <bounds>
    Reads only. No SQS delete, purge, redrive or send, and no SQS receive except the ONE visibility-timeout-0 receive of R3 on irpt-generation-dlq; no restart, stop or start; no write to any table, bucket or host file; no value of any secret. Journal lines are counted, never copied.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_resolve_live/IRPT_ANLREQ.TO-READ-RESOLVE-LIVE.resident-journal-and-which-function-answers-the-door-ib2.proof_of_spec.json`.
    <criterion id="RRL-AC1" cell_refs="AR-y-409">All three read lines and the closing line are present, each answered, denied or marked not run.<invocation>grep -c -E '^(R1 (window=|DENIED |NOT-RUN |ERROR )|R2 (api_kind=|DENIED |NOT-RUN |ERROR )|R3 (dlq_depth_before=|DENIED |NOT-RUN |ERROR ))|^READS-DONE [0-9]+ of 3 answered$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_resolve_live/A_RESOLVE_LIVE.txt</invocation><expect>^4$</expect></criterion>
    <criterion id="RRL-AC2" cell_refs="AR-y-409">No line holds a URL, an email address, an access key or a bucket-style name (the leak control).<invocation>grep -c -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|https?://|execute-api|AKIA[0-9A-Z]{12,}|opal-data-[a-z0-9-]+' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_resolve_live/A_RESOLVE_LIVE.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-409 is the issuer's, as for the earlier read orders to IB2.
