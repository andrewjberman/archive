<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READS-Y8.f2-original-route-owner-check-laptop</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ANL</issued_to>
    <date>2026-10-12</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- read-only; no resource is changed. Four direct invokes of irpt-status, whose role holds no write permission (terraform/investor-reporting/ops/iam.tf:35, read by 0.9.0_WK_IRPT_ANLREQ~54). comp-routes: RUN -- by reading the route's rule and order of checks in `deliverables/0.9.0_WK_IRPT_ANLREQ~54/r16/ORIGINAL_ROUTE_RULE_READ.json` (read of the repository at d90edb3367, NOT of the deployed function; step 1 ties the two). comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: RUN -- by reading 2 records: the same record's section on who can invoke (any identity holding lambda:InvokeFunction on irpt-status by its identity policy; this seat did it read-only under TO-READS-Y5, irptlib.py:56-63), and the CTO's ruling that no identity is minted. Whether THIS seat still holds the grant is NOT known; step 0 says what to do if it does not.
comp-adversary: RUN -- by reading the CTO's rulings (msgs 6378, 6387, 6541) against the pair's arms; the lens: arm (b) alone cannot tell "the owner check fired" from "the record is absent", because both answer NOT_AUTHORIZED. The control on the SAME record exists to separate them. NOT seen: the deployed function, the ordinary authorizer's body (not read).
lane: the applier's own deliverables and logs; read-only on the world.
</preflight>
<proof_of_spec>
Criterion id: READS8-AC1. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/IRPT_ANLREQ.TO-READS-Y8.f2-original-route-owner-check-laptop.proof_of_spec.json`,
`to_id` the FULL id above, validated with `python .tools/proof-of-spec-check.py <instance> READS8-AC1` AFTER its commit.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R16_Y.md</decomp_doc> round 16, workstream ~Y, item 4b (arm F2): the arm and its pair are the issuer's, written on cell AR-y-165's read.
<owned_cells>AR-y-165</owned_cells>
</decomp_ref>

  <objective>
    FOUR READ-ONLY direct invokes of the deployed `irpt-status` function against ONE retained analysis request, to show whether the
    original-file route's OWNER CHECK fires: a caller who is a DIFFERENT advisor of the record's own firm is refused NOT_AUTHORIZED,
    AND a caller the rule admits for that firm is served the signed link's PRESENCE on the same record (so the refusal is not just
    "the record is absent"). Nothing is written to AWS, deleted, applied or deployed. No identity is minted and no grant is made.
  </objective>

  <context>
    Ruled by `1.0.0_SA_CTO~DELL2`: msg 6378 (three arms; callers are constructed contexts with made-up addresses on a reserved
    domain; the pair states the read was of the repository and step 1 ties the deployed function to that source first; each status
    from a parsed value), msg 6387 (a record that fits is used as it stands) and msg 6541 (YES to arm (b) live, read-only, by this
    seat, WITH an existence control on the same record: control present and (b) NOT_AUTHORIZED = the owner check fired; control
    refused = record unreachable and the pair says UNEXERCISED LIVE; no record id or address in any file or message). Arm (c), the
    owner twin, is NOT run: it needs the owner's address, which nobody is asked for.

    THE RECORD: the one named by your own file `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/F2_one_request_id.json`
    (a reserved-domain, OPAL_GLOBAL-owned request with a retained composition and original, from the call that precedes this order).
    If that file does not exist at your checkout's HEAD, STOP and report: this order is staged until it does. Read the id from that
    file at run time into memory. NEVER copy it, or any address, into a file, log or message of this order.

    THE ROUTE: `GET /api/scoped/investor-reporting/analysis/requests/{requestId}/original`, handler `irpt-status`
    (`ops/entry.py` build_owned_entry, read mode OWNED_RECORD). Its rule, read from the repository (not the deployed bytes) by
    `0.9.0_WK_IRPT_ANLREQ~54`: `deliverables/0.9.0_WK_IRPT_ANLREQ~54/r16/ORIGINAL_ROUTE_RULE_READ.json`. Read it first. In short:
    the firm fence (served.py:1207-1209, FIRM_BINDING) runs before any record is read; the owner comparison
    (`_scope/owner_reads.py:28-31`) refuses a caller who is not OPAL_GLOBAL unless the caller's firm AND principal equal the record
    owner's; the same code NOT_AUTHORIZED answers an absent record and a record owned by someone else.
  </context>

  <steps>
    0. Pre-checks, STOP and report on any miss: (i) `F2_one_request_id.json` exists at HEAD of your checkout; (ii) you hold
       `lambda:InvokeFunction` on `irpt-status` (state how you know: `iam simulate-principal-policy` on your own identity and the
       function's ARN, as TO-READS-Y5 did); (iii) no open deploy-ledger entry names `irpt-status` (read EVERY live worktree's
       `org/critical_paths/.open_deploys/` by `git worktree list --porcelain` then `git -C <wt> ls-tree -r --name-only HEAD
       org/critical_paths/.open_deploys/`; print the denominator; an open entry naming `irpt-status` is a STOP, no direct invoke
       while an apply is in flight). Record the count of open entries naming it.
    1. TIE THE DEPLOYED FUNCTION TO THE SOURCE. `aws lambda get-function-configuration --function-name irpt-status`: record
       `CodeSha256` and `LastModified`. Then say what ties that digest to a source commit (the release map's row for `irpt-status`
       or the deploy record that names the built package); if nothing ties it, write `UNTIED` in `tie.tied_to`. A missing tie does
       NOT stop the run (the arms still show the DEPLOYED function's behaviour); it is recorded, and the pair reads it.
    2. Build the four events in memory (and ONLY in memory; none is written to a file with the record's id in it). Every event:
       `routeKey` = `GET /api/scoped/investor-reporting/analysis/requests/{requestId}/original`, `pathParameters.requestId` = the
       record's id, headers `X-Contract-Version: v1`, `x-origin-verify: cloudfront`, `x-user-name: f2-probe`, and an `x-user-email`
       on the reserved domain `opal.invalid` (a different local part per arm). No body. The record's TENANT (firm) is `T`.
         - `control`: `x-firm-id: opal-capital`, `x-user-role: user`, query `selected_tenant: T`. (An INTERNAL caller the rule admits
           for firm T: `ops` reads it as OPAL_GLOBAL.) Expect `ok: true` and a download route in `data`.
         - `b` (the proof arm): `x-firm-id: T`, `x-advisor-id: f2-advisor-b` (a synthetic value, so the class is FIRM_ADVISOR),
           `x-user-role: user`, NO selector. A different advisor of the record's own firm. Expect `ok: false`,
           `status.public_reason_code` = `NOT_AUTHORIZED`.
         - `a` (the fence, a companion): `x-firm-id: F` where F is a firm code OTHER than T and one of the tenants your earlier
           counts saw, `x-advisor-id: f2-advisor-a`, `x-user-role: user`, query `selected_tenant: T`. Expect `ok: false`,
           `public_reason_code` = `FIRM_BINDING`.
         - `b_absent_id` (shows why `b` alone proves nothing): the `b` event with a well-formed id that names no record
           (`REQ-` then 24 zeros). Expect the same `NOT_AUTHORIZED` as `b`.
    3. Invoke each ONCE with `RequestResponse`, in the order `control`, `b`, `a`, `b_absent_id`. PARSE the envelope as JSON; record
       statuses from the parsed members, never from a substring. For `control` record ONLY the PRESENCE (true/false) of
       `data.download_route.url`, of `expires_at`, of `sha256` and of `byte_length`. The url, and anything after it, is NEVER
       written, printed, logged or followed: parse it into a variable, take the four booleans, drop it. For the other three record
       `ok` and `status.public_reason_code`, and the booleans (they must be false). If an arm answers anything outside its
       expectation, record what it answered (code only) and go on to the next arm; do not retry.
    3a. A LINK IN A LOG IS A STOP (CTO half, condition 2). Right after the `control` invoke and BEFORE the `b` invoke, read the
       control invoke's own CloudWatch log lines for `irpt-status` (filter on the invoke's request id). Any line carrying the signed
       link's host and a signature query (`X-Amz-` members) ENDS the run there: record `control_log_check: LINK_IN_LOG` as a finding
       with the link REDACTED (never copy it), run NO further arm, set the verdict ANOMALY, and report. If the log lines cannot be
       read, record `control_log_check: NOT_READ` with the error's code and go on. Otherwise record `CLEAN`.
    4. Write `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/F2_original_route_owner_check.json`:
       `{"read_at": "<UTC>", "tenant": "<T, the firm code>", "tie": {"code_sha256": "...", "last_modified": "...", "tied_to": "<commit
       or UNTIED>"}, "arms": {"control": {"ok": <bool>, "public_reason_code": <str or null>, "url_present": <bool>, "expires_present":
       <bool>, "sha256_present": <bool>, "byte_length_present": <bool>}, "b": {"ok": ..., "public_reason_code": ..., "url_present":
       <bool>}, "a": {...as b...}, "b_absent_id": {...as b...}}, "control_log_check": "CLEAN" | "NOT_READ" | "LINK_IN_LOG", "verdict": "OWNER_SCOPED_REFUSAL" | "UNEXERCISED_LIVE" | "ANOMALY",
       "ledger_open_entries_naming_irpt_status": <n>, "identity_arn_tail": "<the role or user name only>", "writes_made": [],
       "claim": "measured", "not_read": [...]}`. The verdict is: control `ok` with `url_present` and `b` NOT_AUTHORIZED =
       OWNER_SCOPED_REFUSAL (comparison at owner_reads.py:29-31 or the second check at owned_requests.py:176-184, NOT SEPARATED; never write "the owner check fired"); control refused = UNEXERCISED_LIVE; anything else = ANOMALY. The check refuses a verdict that does not
       follow. Before you commit, READ the file: no request id, ticket id, address, link or query string.
    5. Delete any scratch you made outside the checkout. Commit the result and the proof instance; report to the issuer citing this
       order's path, with push state. One line first as soon as step 3 ends: the verdict and the four statuses.
  </steps>

<criterion id="READS8-AC1" cell_refs="AR-y-165"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r16/reads8_check.py</invocation><expect>READS8-OK</expect></criterion>
`READS8-AC1`: the result is complete, its verdict follows from its arms by the rule of step 4, the tie is stated (a digest and a source or UNTIED), the
write list is empty, and it holds no id, address or link.

<expected_criteria>READS8-AC1</expected_criteria>

The check at the base (run by the issuer before this cut): FAIL as expected (no result file).

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~ANL/logs/
org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

  <bounds>
    - Read only: four `lambda:InvokeFunction` calls on `irpt-status`, `get-function-configuration`, `iam simulate-principal-policy`
      on your own identity. No write, no delete, no apply, no deploy, no grant, no identity or users row made, no token made.
    - No request id, address, ticket id, file content or link in any file, log or message. The control's signed link is never
      followed, printed or stored.
    - One run. A second run needs the issuer's word.
    - Flipped to `pending` by the issuer 2026-10-12 after the CTO half was signed (msg 6544, @ca36fd9c65) and its condition 1 was in place. Step 0 (i) still STOPS the run until `F2_one_request_id.json` exists.
  </bounds>
</task_order>
