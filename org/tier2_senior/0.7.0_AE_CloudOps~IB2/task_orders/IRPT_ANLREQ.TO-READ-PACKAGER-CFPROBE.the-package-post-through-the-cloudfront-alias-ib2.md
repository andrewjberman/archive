<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-PACKAGER-CFPROBE.the-package-post-through-the-cloudfront-alias-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>complete</status><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene, CTO msg ~15:10Z): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 -->
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- ONE authenticated package POST as the packager principal to a ticket id that does not exist, sent through the CloudFront alias of the portal (the ticket service answers not-found and writes nothing), plus a read of the authorizer's log lines. No other write, no deploy, no delete, no queue action. The only writes are the record file and one private temp file you create and remove. No ledger.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the probe runs as the host role as it is.
comp-adversary: RUN -- by reading your A_PACKAGER_403.txt (the direct host is refused ORIGIN_VERIFICATION_FAILED; the token is valid) and the CTO ruling (msg 11292: route through CloudFront, the authorizer unchanged, the origin secret never handed to the resident) against this cell; the lens: a printed secret, token, header, URL with a query or email (forbidden: print the exception class, the closed message, an HTTP status and a closed reason word only), a real ticket id (use the bogus id below only), a second POST, any change to the resident's bindings (the probe overrides api_base IN MEMORY only). NOT seen (blind): the edge function's own log (it is in other regions); denominator: one probe, one log read, one claim read and one closing line.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ110: the package POST through the CloudFront alias (cell AR-y-451).
<owned_cells>AR-y-451</owned_cells>
</decomp_ref>

  <objective>
    Print what the ticket service side answers to ONE package POST to a ticket id that does not exist when the packager's own code sends it through the portal's CloudFront alias instead of the direct API Gateway host, and the authorizer's reason for it. Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the lines. THIS ORDER STARTS ONLY ON MY GO MESSAGE (never alongside another IB2 act: the IAM grant order must be closed first).
  </objective>

  <context>
    Load /cloud-ops first. The CTO ruled (msg 11292) that the packager calls the ticket service through the same CloudFront route the portal uses, and that the authorizer is not changed. The alias is `https://opalinvest.dev` (the CloudFront distribution's own alias; behaviour `/api/scoped/tickets/*` allows POST, adds the origin header at the origin, and runs the viewer-request edge function). Cell AR-y-449 reads the sources offline; this order is the live proof. An answer of not-found (HTTP 404 from the ticket service) means the request passed the edge, the origin gate and the token check; 401 or 403 means it did not.
  </context>

  <the_act>
    GO only on my message. The two steps are independent. Never print a secret, token, header, URL or email.
    1. PROBE A2. Send a small python3 script to the resident host by Systems Manager AS ROOT, run with the service's own environment and interpreter in the way your earlier probe entered it, with the install root `/opt/irpt-resident/0485393f3a-r34m`:
```
import json, sys, boto3
root = "/opt/irpt-resident/0485393f3a-r34m"
sys.path[:0] = [root + "/ycharts/research", root + "/reports", root + "/ycharts/generate", root + "/intake", root]
import opal_packager
import resident_installed as ri
cfg = dict(json.load(open(root + "/reports/resident_bindings.json"))["packager"])
cfg["api_base"] = "https://opalinvest.dev"
sm = boto3.client("secretsmanager", region_name="us-east-1")
ports = opal_packager.live_ticket_ports(cfg, read_secret=ri._read_secret_string(sm), http=ri._packager_http)
payload = {"report_ref": "x", "pdf_ref": None, "original_ref": "x", "commentary_ref": None,
           "firm": "49financial", "request_id": "REQ-" + "0" * 24, "request_revision": 1}
try:
    print("A2_RETURNED", type(ports["attach"]("TCK-20261020-00000000", payload)).__name__)
except Exception as exc:
    print("A2_EXC", type(exc).__name__, str(exc)[:80])
```
    (Adjust only the import path lines if needed; the override is in memory and nothing is written to the host.) Note the UTC second of the call. Line: `A2 <A2_RETURNED type|A2_EXC class closed-message> at <HH:MM:SSZ>`. If the script cannot run, write `A2 NOT-RUN <why>`.
    2. LOG. For the API `7k3ed8px20`, read the authorizer log group `/aws/lambda/opal-portal-authorizer` for the 60 seconds around the call's time and print, for the line(s) that belong to a path ending `/package` or to the call's second, only: time and the closed reason or decision word (no header or token value). Line: `R2 <time> reason=<CLOSED_WORD|ADMITTED|->` or `R2 NOT-FOUND <where you looked>`.
    3. TOKEN. In the same run as step 1, parse the packager token's payload WITHOUT verifying it (as your TO-READ-PACKAGER-403 R1 did) and print only whether the claim `iss` equals the closed word `opal-portal-auth` and the claim `aud` equals the closed word `opal-portal-api` (else the word `other`; never the value). Line: `T iss=<opal-portal-auth|other> aud=<opal-portal-api|other>`.
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_cfprobe/A_PACKAGER_CFPROBE.txt with the lines A2, R2 and T (each answered or `NOT-RUN <why>`) and a closing line `PROBES-DONE <n> of 3 answered`. Commit it. Report ONCE as in the objective. Remove the private temp file.
  </the_act>

  <bounds>
    Exactly one package POST (to the bogus ticket id) and one log read. No other call, no purge, redrive or send, no delete, no `get-secret-value` by you, no IAM, Terraform or binding change, no deploy. Nothing about Andrew's ticket TCK-20261017-5af976ff is read.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_cfprobe/IRPT_ANLREQ.TO-READ-PACKAGER-CFPROBE.the-package-post-through-the-cloudfront-alias-ib2.proof_of_spec.json`.
    <criterion id="PKGCF-AC1" cell_refs="AR-y-451">The record holds the three answer lines and the closing line.<invocation>grep -c -E '^(A2 |R2 |T iss=|PROBES-DONE [0-9]+ of 3 answered)' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_cfprobe/A_PACKAGER_CFPROBE.txt</invocation><expect>^4$</expect></criterion>
    <criterion id="PKGCF-AC2" cell_refs="AR-y-451">No line holds a token, a URL, a signature or an email address (the leak control).<invocation>grep -c -E 'eyJ[A-Za-z0-9_-]{10,}|https?://|Bearer |X-Amz-|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_cfprobe/A_PACKAGER_CFPROBE.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-451 is the issuer's, as for TO-READ-PACKAGER-PROBE.
