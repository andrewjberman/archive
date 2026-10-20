<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-PACKAGER-CLIENTERROR.which-aws-call-failed-and-did-the-ready-attach-reach-the-ticket-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- READ ONLY: no write, no deploy, no delete, no upload, no queue send or receive that changes visibility, no post; the only writes are the record file and one private temp folder you create and remove. No ledger.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: RUN-AS-A-READ -- policy simulations of one role against named resources (allowed or denied and the matching statement id only); no IAM change.
comp-adversary: RUN -- by reading your receipt A_E2E6.txt (P4: retained_for_retry class=ClientError code=- at 08:04:18Z; the READY hook line at 08:02:53Z; the ticket item carried NO package member at 08:03:02Z and 08:03:17Z) and the code (`ycharts/research/opal_packager.py` handle_ready and handle_commentary_ready; `reports/resident_installed.py` make_packager; the ticket service `package_ticket`) against this cell; the lens: a printed token, URL, signature, secret value or email (forbidden), a get-secret-value (forbidden), a redrive, receive or purge of the commentary-ready queue (forbidden: the message is in its 900 s retry loop and must not be touched), a post to the ticket service (forbidden). NOT seen (blind): the journal text and the ticket Lambda's log until the steps run; denominator: three reads and one closing line.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ102: which AWS call failed in run 6's package attach and did the READY attach reach the ticket (cell AR-y-443).
<owned_cells>AR-y-443</owned_cells>
</decomp_ref>

  <objective>
    Establish, by reads, (a) what the resident's READY attach (08:02:53Z) answered and whether its POST reached the ticket service, and (b) which AWS call raised the ClientError of the commentary-time attach (08:04:18Z). Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the lines. Read only. GO NOW.
  </objective>

  <context>
    Load /cloud-ops first. Run 6 (receipt `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e6/A_E2E6.txt`, ticket TCK of the run in your state file `state_e2e6.json`, request REQ-7206be963b5d2108980885ca): U NORMALIZED with no advisor, P1 READY at 08:03:02Z (the routing fix held), P2 and P3 green at 08:04:06Z; the READY hook `IRPT_RESIDENT_PACKAGE_READY` printed at 08:02:53Z (its text was not recorded); the ticket item carried no `package` member at 08:03:02Z and 08:03:17Z; then ONE `retained_for_retry class=ClientError code=-` at 08:04:18Z. The code prints a class name only. `handle_ready` reads the acceptance record and the job (DynamoDB) and POSTs the package with `pdf_ref` and `commentary_ref` null; `handle_commentary_ready` additionally reads the commentary artifact, renders the commentary PDF, retains it through the artifacts repository (S3 and the artifact index) and POSTs the full package. THE RULE: print closed words, UPPER_SNAKE codes, HTTP status numbers, counts, times, resource NAMES and ARNs of buckets, tables and secrets; never a secret value, token, URL with a signature, email or client value.
  </context>

  <the_act>
    GO now. Each step is independent; a DENIED or ERROR on one is written and the next step runs. Never delete, post, redrive, receive, purge or send.
    1. R1 (the resident journal): from the resident service's journal between 2026-10-20T08:02:20Z and 08:06:00Z print the window and the lines scanned, then EVERY line containing `IRPT_RESIDENT_PACKAGE`, `PACKAGER`, `HOP_FAILURE`, `retained_for_retry`, `ClientError` or `Traceback`, in full (they carry closed words, class names and times only; if a line holds anything else, replace the part with `<redacted>`). Line: `R1 window=<first>..<last> scanned=<n> lines=<n>` followed by the lines themselves as `R1L <time> <line>`.
    2. R2 (the ticket service): in the CloudWatch log group of the ticket-center Lambda (find the function name from the ticket route's Terraform or the function map `infra/aws/lambda/ci/function-map/` entry named ticket_center; read only), for 08:02:20Z to 08:06:00Z print the count of requests to a path ending `/package`, and for each its HTTP status and the closed `code` of the answer if the log carries them, with the time. If the log group is absent or holds no such line, write `R2 NOT-FOUND` and where you looked. Line per request: `R2 <time> POST /package status=<n> code=<CODE|->`; a closing `R2 count=<n>`.
    3. R3 (the role's reach): from the resident host's instance profile read the role NAME; then `aws iam simulate-principal-policy` for that role on: `s3:PutObject` and `s3:GetObject` against the bucket `opal-data-irpt` keys under `irpt/49financial/state/ycharts_opal_reports/` and `irpt/49financial/state/analysis_commentaries/`; `kms:GenerateDataKey` and `kms:Decrypt` against the data key the bucket encrypts with; `dynamodb:PutItem`, `dynamodb:UpdateItem`, `dynamodb:GetItem` and `dynamodb:Query` against the table `irpt-requests`; `secretsmanager:GetSecretValue` against the secret named `opal/ticketing/svc-irpt-packager`. Print one line per action and resource: `R3 <action> <resource-name> <allowed|denied|ERROR code>` (no `get-secret-value`).
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_clienterror/A_PACKAGER_CLIENTERROR.txt with the lines R1 to R3 (each answered, denied or `NOT-RUN <why>`) and a closing line `READS-DONE <n> of 3 answered`. Commit it. Report ONCE as in the objective: the file path and the lines, nothing more. No ledger. Remove the private temp folder.
  </the_act>

  <bounds>
    Read only. No post, no upload, no delete, no redrive, no queue send, receive or purge, no `get-secret-value`, no write other than the record file and one private temp folder you create and remove; no deploy; no IAM change. Nothing about Andrew's ticket TCK-20261017-5af976ff is read.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_clienterror/IRPT_ANLREQ.TO-READ-PACKAGER-CLIENTERROR.which-aws-call-failed-and-did-the-ready-attach-reach-the-ticket-ib2.proof_of_spec.json`.
    <criterion id="PKGCE-AC1" cell_refs="AR-y-443">The record holds the answer lines and the closing line, each answered, denied or not run.<invocation>grep -c -E '^(R1 |R2 |R3 |READS-DONE [0-9]+ of 3 answered)' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_clienterror/A_PACKAGER_CLIENTERROR.txt</invocation><expect>^[4-9]|[1-9][0-9]$</expect></criterion>
    <criterion id="PKGCE-AC2" cell_refs="AR-y-443">No line holds a token, a URL, a signature or an email address (the leak control).<invocation>grep -c -E 'eyJ[A-Za-z0-9_-]{10,}|https?://|Bearer |X-Amz-|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_clienterror/A_PACKAGER_CLIENTERROR.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-443 is the issuer's, as for TO-READ-COMPOSITION-REFUSAL and TO-READ-APPL-SUGGEST.
