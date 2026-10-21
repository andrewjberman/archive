<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-PACKAGER-403.why-the-package-post-is-refused-403-token-claims-and-gateway-reason-ib2</id>
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
comp-blast: DECLARED-NOT-APPLICABLE -- READ ONLY: the secret is read in memory by the service's own reader code and only claim NAMES and times are printed; no write, no deploy, no delete, no queue action, no post. The only writes are the record file and one private temp file you create and remove. No ledger.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- your principal's existing read reach, or the step is written DENIED.
comp-adversary: RUN -- by reading your probe A_PACKAGER_PROBE.txt (A: `PackagerRefused ATTACH_REFUSED:403` for a package POST to a bogus ticket id through the resident's own port) and A_PACKAGER_CLIENTERROR.txt (R2: the ticket Lambda's log holds NO /package line, so the 403 is returned before the Lambda or by it without a path line) and the ticket service source (`infra/aws/lambda/ticket_center/lambda_function.py`: `package_ticket` admits ONE service subject, `package_principal` = `svc-irpt-packager`, firm-bound by that subject's PROFILE row `allowedFirmIds`; the service-subject token contract is sub plus userType == "service") against this cell; the lens: a printed token, header, secret value, signature, URL or email (forbidden: print claim NAMES, UTC times and the closed subject name only), a get-secret-value by you (forbidden: only the service's own reader code in memory), a second POST. NOT seen (blind): whether the 403 comes from the API authorizer or the Lambda; denominator: three reads and one closing line.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ105: why the resident's package POST is refused 403 (cell AR-y-446).
<owned_cells>AR-y-446</owned_cells>
</decomp_ref>

  <objective>
    Establish, by reads, why the ticket service side answers the resident's package POST with HTTP 403: (a) whether the packager token in the secret `opal/ticketing/svc-irpt-packager` is expired or lacks the service-subject claims, (b) what the API gateway or authorizer logged for the two refused calls (08:02:53Z run 6 READY attach, 08:58Z probe), (c) whether the packager principal's PROFILE row exists and its `allowedFirmIds`. Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the lines. GO NOW.
  </objective>

  <context>
    Load /cloud-ops first. The packager reads the secret by name, expects JSON with a non-empty string `token`, and presents `Authorization: Bearer <token>` on `POST /api/scoped/tickets/{ticketId}/package` at the api_base in the resident's `packager` binding (`api_base` host `7k3ed8px20.execute-api.us-east-1.amazonaws.com`). THE RULE: print closed words, claim NAMES, UTC times, HTTP status numbers, resource names; never a token, header value, signature, URL with a query, secret value or email.
  </context>

  <the_act>
    GO now. Each step is independent; a DENIED or ERROR on one is written and the next step runs.
    1. R1 (the token's claims): in the service's environment (as your probe A did), read the secret with the service's own reader (`resident_installed._read_secret_string`), parse the `token` as a JWT WITHOUT verifying it (base64url-decode the payload segment only) and print: the secret JSON's member NAMES; whether the token has three dot-separated parts; the payload's claim NAMES; for the claims `iat`, `nbf`, `exp` the UTC time and whether `exp` is before now; `sub` only if it equals the closed word `svc-irpt-packager` (else print `sub=<other>` without the value); `userType` and any `scope`-like claim's value only if it is a closed lower-case word of at most 16 letters. Never print the token or any other value. Line: `R1 members=<names> parts=<n> claims=<names> iat=<UTC> nbf=<UTC|-> exp=<UTC|-> expired=<yes|no|n/a> sub=<svc-irpt-packager|other> userType=<word|-> `.
    2. R2 (the gateway side): for the API with id `7k3ed8px20` read (describe only) whether it has an authorizer and which kind (name, type, identity source, no ARNs of secrets), and whether access logging is on; then, from the API's access log group or the authorizer Lambda's log group if they exist, for 2026-10-20T08:02:30Z-08:03:30Z and 08:57:30Z-08:59:30Z print the lines for the path ending `/package` as: time, HTTP status, and the closed authorizer or error reason field if present (no header or token values). If no such logs exist write `R2 NOT-FOUND` and where you looked. Line per call: `R2 <time> POST /package status=<n> reason=<CLOSED_WORD|->`.
    3. R3 (the principal's row): read the ticket service's users or profile row for the subject `svc-irpt-packager` (`aws dynamodb get-item` on the users table the ticket service uses; find the table name in `infra/aws/lambda/ticket_center/lambda_function.py` or its Terraform; consistent read) and print only: whether the row exists, its member NAMES, `userType`/`role` closed words, and the `allowedFirmIds` as the closed list of firm ids (49financial, cottonwood, inflection or ALL). Line: `R3 row=<present|absent> members=<names> userType=<word|-> allowedFirmIds=<list|->`.
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_403/A_PACKAGER_403.txt with the lines R1 to R3 (each answered, denied or `NOT-RUN <why>`) and a closing line `READS-DONE <n> of 3 answered`. Commit it. Report ONCE as in the objective. Remove the private temp file.
  </the_act>

  <bounds>
    Read only (no POST at all in this order). No get-secret-value by you, no print of any secret material, no delete, no queue action, no deploy, no IAM change. Nothing about Andrew's ticket TCK-20261017-5af976ff is read.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_403/IRPT_ANLREQ.TO-READ-PACKAGER-403.why-the-package-post-is-refused-403-token-claims-and-gateway-reason-ib2.proof_of_spec.json`.
    <criterion id="PKG403-AC1" cell_refs="AR-y-446">The record holds the answer lines and the closing line.<invocation>grep -c -E '^(R1 |R2 |R3 |READS-DONE [0-9]+ of 3 answered)' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_403/A_PACKAGER_403.txt</invocation><expect>^[4-9]$</expect></criterion>
    <criterion id="PKG403-AC2" cell_refs="AR-y-446">No line holds a token, a URL, a signature or an email address (the leak control).<invocation>grep -c -E 'eyJ[A-Za-z0-9_-]{10,}|https?://|Bearer |X-Amz-|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_403/A_PACKAGER_403.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-446 is the issuer's, as for TO-READ-PACKAGER-PROBE.
