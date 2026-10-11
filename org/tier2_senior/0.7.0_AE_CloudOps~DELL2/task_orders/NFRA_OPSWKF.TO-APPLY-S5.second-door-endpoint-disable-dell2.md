<task_order>
  <metadata>
    <id>NFRA_OPSWKF.TO-APPLY-S5.second-door-endpoint-disable-dell2</id>
    <issued_by>2.0.0_SA_COO~O2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>NFRA_OPSWKF</project_code>
  </metadata>
<risk>WORLD</risk>
<round>3</round>
<workstream>S</workstream>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_OPSWKF/decompositions/NFRA_OPSWKF_DECOMP.md</decomp_doc> (workstream S): issuer cell `OW-sd-3`, FWD-10, closing the second door (row NFRA_OPSWKF-D2-S11).
<owned_cells>OW-sd-3</owned_cells>
</decomp_ref>

  <objective>
    FWD-10 (PRD v0.10 @47d579b505): close the public endpoint of HTTP API `trade-submission-api` (`w8jnzvs21g`) by ONE reversible
    setting, `DisableExecuteApiEndpoint` `false` -> `true`, and prove it by the setting read back and by two requests that touch no
    function. **NO request is EVER made to that API's `/auth` route, by you or anyone, before or after.**
  </objective>

  <context>
    READ BOTH HALVES WHOLE BEFORE STEP 0, the files and not this restatement, and say so in the ledger's opening entry:
    - Packet and COO half (SIGNED): org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_DEPLOY/OW_SD3_FWD10_SECOND_DOOR_CLOSE_PAIR_20261011.md
      @90f5a700f4, sha256 begins c33bea1f5feceb16.
    - CTO half (SIGNED): org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_OW_SD3_FWD10_SECOND_DOOR_CLOSE_20261011.md @87957ba554 (msgs 6063 and 6069; the first message cited 114c77fb01, another seat's commit, and the CTO corrected it; the half's bytes and the pair's sha256 are unchanged). Where it differs from the packet it GOVERNS.
    The API is NOT in Terraform: this is one CLI call, not a `safe-apply`. The ledger and the packet are its only record.

    The two probes, each a plain HTTPS GET to `https://w8jnzvs21g.execute-api.us-east-1.amazonaws.com`, with NO `Authorization` header,
    NO `X-Auth-Token` header, no cookie and no body:
    - **N:** `GET /fwd10-no-such-route-20261011` (a path the API has no route for; there is no `$default` route).
    - **U:** `GET /users` (a route under the API's authorizer; with the identity source `Authorization` absent, API Gateway answers
      401 itself and does not invoke the authorizer).
    For EACH probe answer record IN FULL: the HTTP status, the whole response body (these are API Gateway's own short JSON errors;
    if a body is longer than 300 bytes or is not the gateway's own error, record its length and first line only and STOP), and the
    response header NAMES. Mind the MSYS path rewrite you caught today: pass the URL whole.
  </context>

  <steps>
    0. Open the NEVER-2 ledger entry and COMMIT it immediately, and again after each leg. It names the one key, its BEFORE value, the
       restoring command, and that both halves were read whole.
    1. BEFORE, configuration: `get-api w8jnzvs21g` whole (record `DisableExecuteApiEndpoint`, name, endpoint, CORS, route selection);
       `get-routes` (expect 7, none `$default`; if a `$default` route exists, STOP: probe N would reach a function); `get-stage prod`;
       `get-api 7k3ed8px20` `DisableExecuteApiEndpoint` (the portal's API, for (d)).
    2. BEFORE, what else carries the API, each with its denominator printed: `apigatewayv2 get-domain-names` and, for each name, its
       api-mappings; `apigateway get-domain-names` (the REST plane) and, for each, its base-path mappings; `cloudfront
       list-distributions`, the number scanned and any whose origin names `w8jnzvs21g`. A mapping or an origin that carries this API
       is a STOP before the act: report it; the pair covers only an API with none.
    3. BEFORE, invocations: AWS/Lambda `Invocations` Sum, 1-minute period, the last 30 minutes, for `trade-auth-handler` and
       `trade-authorizer`, with one control function in the same query shape.
    4. BEFORE, the probes: N, then U, once each. Expected: N `404`, body `{"message":"Not Found"}`; U `401`, body
       `{"message":"Unauthorized"}`. If U answers anything but 401, STOP and do not send it again. If either answers 5xx, STOP.
    5. THE ACT: `aws apigatewayv2 update-api --api-id w8jnzvs21g --disable-execute-api-endpoint`. An AccessDenied is a STOP: nothing
       changed, no grant is added, report (the act then goes whole to a seat that holds the permission).
    6. AFTER (print each, with its time):
       - (a) **the primary proof:** `get-api w8jnzvs21g` reads `DisableExecuteApiEndpoint` `true`; every other property as step 1,
         compared field by field; `get-routes` still 7; `get-stage prod` unchanged;
       - (b) the probes again, N then U, once each, answers recorded in full. Then say, in one sentence each: is N's AFTER answer
         DIFFERENT from N's BEFORE answer (status, body or header names)? is U's? If BOTH are indistinguishable from BEFORE, wait 60
         seconds once and repeat both once; if still indistinguishable, the probes prove nothing: say so in those words, do NOT
         restore the setting, and report;
       - (c) invocations as step 3, from 30 minutes before the act to 10 minutes after, both functions and the control. They are
         expected flat and are recorded as a witness that the probes touched no function, not as proof of closure;
       - (d) `get-api 7k3ed8px20` `DisableExecuteApiEndpoint` as step 1. No request is made to the portal's API.
    7. Close the ledger. Report once to `2.0.0_SA_COO~O2`: steps 1-3, the four probe answers in full side by side, (a)-(d) with times,
       the restoring command, and which probe (if either) discriminates. Proof-of-spec instance at the flat path.
  </steps>

  <bounds>
    ONE write: that one property of that one API. Four requests in all (N and U, before and after), plus at most one repeat pair
    under step 6(b). NEVER a request to `/auth`, to `/submit`, to `/workflow`, or to any route with a credential. No invoke of any
    function. No change to a route, integration, authorizer, stage, permission, function, secret, table or Terraform file. Nothing
    is deleted. No grant.

    Rollback, one call, ONLY on the CTO's word or if a caller Opal depends on is shown to have broken:
    `aws apigatewayv2 update-api --api-id w8jnzvs21g --no-disable-execute-api-endpoint`, then `get-api` reads `false`.
  </bounds>

<proof_of_spec>
  <criterion id="OW-sd3-AC1" cell_refs="OW-sd-3" judgment="true"/>
</proof_of_spec>
OW-sd3-AC1 (judgment; the CVO's at L9): the setting reads `true` on the API's own configuration after the act, nothing else of the API
changed, no domain mapping or CDN origin carries it, and the probe answers are recorded in full with what they do and do not show.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule, hold or gate is created or consumed
comp-iam: DECLARED-NOT-APPLICABLE no grant changes; whether the principal may update the API is measured by the act and a denial is a STOP
comp-adversary: DECLARED-NOT-APPLICABLE at the cut; the pair's section 4 names the one way the proof could show nothing (404 both sides) and adds the probe that would still discriminate
</preflight>

# pipeline-override: an APPLY order to the dell2 cloud-ops seat for one issuer cell (OW-sd-3: one reversible setting on a console-made API, under a signed never-widen pair); not a worker cell.
</task_order>
