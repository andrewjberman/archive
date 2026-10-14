<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-R32.packager-secret-claims-and-door-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-14</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ ONLY order: one secret value is read in process memory to decode the CLAIMS of a token; no secret, policy, Lambda, API, table or host is changed.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called or changed; the package route is READ as a route definition of the API, never called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger. comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change is made; the IAM check is a simulate-principal-policy read.
comp-adversary: RUN -- by reading the CTO ruling (msg 7777: "read the secret ... what exists is adopted") and the door read (AR-y-335 record q1, q4) against this cell; the lens: the TOKEN or the secret JSON written to a file, a message, a log or the screen; a signature or key printed; claims decoded by a tool that sends the token elsewhere; a decode done on a shared or recorded terminal. NOT seen (blind): the portal authorizer's signing key and the token's cryptographic validity (the signature is NOT verified here); denominator: 6 result lines, one per fact.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 40, workstream ZW: the packager secret's claims, the live firm list and the live API origin the resident release binds.
<owned_cells>AR-y-337</owned_cells>
</decomp_ref>

  <objective>
    Establish, from the live estate and WITHOUT ever writing or printing the token, whether the existing secret `opal/ticketing/svc-irpt-packager` holds a token the ticket service's package door would accept in shape and time, and read three live facts the resident's bindings depend on. Change NOTHING. Write six result lines to one record file and tell 2.0.0_SA_COO~Y2 in one message.
  </objective>

  <context>
    Load /cloud-ops first. The ticket service does not authenticate; the portal authorizer verifies an RS256 JWT and passes its sub and userType, and the ticket service admits the package route only for userType `service` with sub `svc-irpt-packager` (AR-y-335 record: org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~142/r41/PACKAGER_DOOR_READ.json, q1 and q3). The resident presents the secret's JSON member `token` (opal_packager.py live_ticket_ports). The CTO ruled (msg 7777) that what exists is adopted and the applier generates a value only where none exists. The prior read (TO-READ-R31) found the secret created 2026-10-11 and never accessed; its value has not been read.
  </context>

  <the_act>
    GO. All reads are describe, get, list, query or simulate calls. Page every list.
    1. THE SECRET'S SHAPE AND CLAIMS (in process memory only). Read the secret's current value with `secretsmanager get-secret-value` INSIDE a short script whose standard output carries ONLY the fields listed below. Parse it as JSON; check for the member `token`; if the token has three dot-separated base64url parts, decode the HEADER and PAYLOAD (never the signature) in memory. The script prints NO token, NO secret JSON, NO header or payload object and NO signature byte: only the booleans and claim VALUES named in line forms 1 to 3 below. Run it so that nothing is echoed to a shared log (no `set -x`, no tracing, no output redirected into the repository), and discard the variables on exit. A decode failure is a line, not an error to retry.
    2. THE LIVE FIRM LIST. Read the ticket service Lambda's environment variable PACKAGE_ALLOWED_FIRMS (`lambda get-function-configuration` on the function infra/aws/terraform/ticket-center/main.tf names; the value is a comma list of firm slugs, not a credential) and print its items.
    3. THE LIVE API ORIGIN. Find the API Gateway (REST or HTTP) that serves POST /api/scoped/tickets/{id}/package (read the API's routes or resources; the Terraform names it, main.tf lines about 396 and 427): print its https origin (`https://<api-id>.execute-api.us-east-1.amazonaws.com`, no path) and whether the POST package route is PRESENT. Never call the route.
    4. THE RESIDENT'S IAM. Read the resident host's instance role name from infra/aws/terraform/investor-reporting/ycharts/resident.tf (about lines 160-175) and run `iam simulate-principal-policy` for `secretsmanager:GetSecretValue` on the packager secret's ARN: ALLOWED or DENIED (implicitDeny) and the role name.
    5. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r32/LIVE_STATE_R32.txt with ONE line each, in this order and form, nothing else on a line that starts with these tokens:
       `SECRET svc-irpt-packager SHAPE json_with_token|json_without_token|plain_string|empty|unreadable`
       `SECRET svc-irpt-packager CLAIMS alg=<alg|NA> sub=<sub|NA> userType=<userType|NA> iss_present=<yes|no> kid_present=<yes|no>`
       `SECRET svc-irpt-packager TIME exp=<ISO UTC|NONE> iat=<ISO UTC|NONE> state=<VALID_NOW|EXPIRED|NO_EXPIRY|NOT_A_JWT>`
       `LAMBDA ticket_api ENV PACKAGE_ALLOWED_FIRMS <comma list|UNSET>`
       `API package_route POST /api/scoped/tickets/{id}/package PRESENT|ABSENT origin=<https origin|UNREAD>`
       `IAM resident_role <role name> secretsmanager:GetSecretValue on the packager secret ALLOWED|DENIED`
       Add a free-text `NOTES` paragraph after the six lines (lines starting with another token): anything odd, each with the call that showed it. The record holds NO token, NO secret JSON, NO key and NO signature. Commit it with .tools/safe-commit.sh under your author line.
    6. Report ONCE to 2.0.0_SA_COO~Y2: "R32 read done" with the six lines (they hold no secret) and the commit.
  </the_act>

  <bounds>
    READ ONLY. No change to any secret, Lambda, API, policy, queue, table or host. The signature is NOT verified and no key is touched. The token is never written, printed, logged, committed or messaged; if you cannot guarantee that for a step, write `UNREAD <why>` on its lines instead. A denied call is a line with the reason, never a reason to widen anything.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r32/IRPT_ANLREQ.TO-READ-R32.packager-secret-claims-and-door-aq2.proof_of_spec.json`.
    <criterion id="R32R-AC1" cell_refs="AR-y-337">The record carries one line for each of the six facts, in the stated forms.<invocation>grep -c -E '^(SECRET svc-irpt-packager (SHAPE (json_with_token|json_without_token|plain_string|empty|unreadable)|CLAIMS alg=|TIME exp=)|LAMBDA ticket_api ENV PACKAGE_ALLOWED_FIRMS |API package_route POST |IAM resident_role )' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r32/LIVE_STATE_R32.txt</invocation><expect>^6$</expect></criterion>
    <criterion id="R32R-AC2" cell_refs="AR-y-337">No JWT-shaped string and no secret JSON appears anywhere in the record.<invocation>grep -c -E '[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}|"token"[[:space:]]*:' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r32/LIVE_STATE_R32.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ-ONLY order to a tier-2 applier (not a worker cell); the cell AR-y-337 is the issuer's, as for TO-READ-R31.
