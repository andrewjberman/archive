<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-FWD5.live-cross-firm-s3-ib2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-17</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>65</round>
<workstream>~T</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R65_T.md</decomp_doc>
<owned_cells>AR-tz-75</owned_cells>
<decomp_context>Round 65, cell AR-tz-75: the THIRD sitting of the FWD-5 live cross-firm exercise, under the pair re-signed by the CTO (RE-SIGN 4): two principals minted on DEV, and for TWO targets (the packaged ticket and the synthetic ticket) the control run and then the firm-B run, each making 13 GET calls, then both principals removed. No write to any ticket, request or job.</decomp_context>
</decomp_ref>

  <objective>
    DRIVE, live, what the CVO's grade of FWD-5 found unproven (ADJUDICATION_v26): (a) a firm-B principal (cottonwood) against the PACKAGED ticket TCK-20261014-2965a5e0, its report and commentary PDFs and its original, with an identity entitled to the ticket (the control) served each file; (b) the five more read routes on the same request or job (`analysis/requests/{id}`, `analysis/requests`, `status/{jobId}`, `narrative/{id}`, `export/{id}`); (c) one call with no `selected_tenant`. Mint two scoped principals, run the driver's control mode and then its firm-B run for each of the two targets, remove both principals, write the four reports and the proof instance. Statuses, route names, counts and hashes only: never a body, a token, a password or an address in any file or message.
  </objective>

  <context>
    THE THIRD SITTING. The first sitting (21:13Z, folder `irpt_anlreq_fwd5/`) was a driver defect (no contract-version header); the second (folder `irpt_anlreq_fwd5_s2/`) drove the one synthetic ticket, which carries no package, and four report-side routes. Both folders STAY as they are. This sitting writes to the NEW folder `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd5_s3/` with two subfolders, `packaged/` and `synthetic/`, each holding `fwd5_control_report.json` and `fwd5_run_report.json`.
    Authority and pair (read these first, in this order): the packet `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~T2/R58_FWD5_LIVE_EXERCISE_PACKET_DRAFT_20261016.md` at commit b942ed203c, blob `6bf8cd3887` (sha256 `d53beb21...`), sections 1, 1a2, 1c, 3, 4, 7d; the CTO half `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_FWD5_LIVE_CROSS_FIRM_RUN_CTO_HALF.md`, RE-SIGN 4 (@de7f72d8c9). Binding conditions that stand: the laptop CTO's ruling XA-20261016T191116Z-4c60 (YES) with the positive control; a LEAK stops the sitting with both principals removed first and only the route name reported; localhost:5174 serves Andrew's smoke copy (`C:/dev/smoke-template-5174`): REUSE it, NEVER start, stop or restart it, print its origin and checkout identity (read without touching the server) before step 4 and after step 6 and say if it changed; the CTO will not call FWD-5 PASS (the grade is `3.0.0_SA_CVO~IRPT`'s at L9). RE-SIGN 4 adds: a control DENIED with `FIRM_BINDING` or `NOT_AUTHORIZED` on a route is a BROKEN control on that route, not past the fence: report it by route name; it grades nothing.
    The labels (packet section 1a2, easy to invert): the driver's `--firm-a` is the PRINCIPAL's own firm and `--firm-b` is the TICKET OWNER's firm. Run principal: firm-a `cottonwood`, firm-b `49financial`. Control principal: firm-a `opal-capital`, firm-b `49financial`.
    The TWO TARGETS (both tickets belong to `49financial`): PACKAGED = ticket `TCK-20261014-2965a5e0`, request `REQ-28a5ca6be3b7f438a9ca8217`, job id the same string (this request has no `irpt-jobs` row: V2 msg 9665; the job-level read is expected NOT_FOUND for the control, which is past the fence); SYNTHETIC = ticket `TCK-20261015-944c84f8`, request and job `REQ-d47252fe74634d0c5cdd8067` (the synthetic row, READY, no `hop_failure`). Base `http://localhost:5174`; run principal email `fwd5-cottonwood-r60@opal.invalid`; control principal email `fwd5-control-r60@opal.invalid`; go token = this order's id `IRPT_ANLREQ.TO-RUN-FWD5.live-cross-firm-s3-ib2`. Pins at HEAD (packet section 7d; paths under `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/`): `0.9.0_WK_IRPT_ANLREQ~219/fwd5_driver/fwd5_mint.py` = `ec8607ed57`; `0.9.0_WK_IRPT_ANLREQ~231/fwd5_driver/fwd5_driver.py` = `ba8010bb70`; `0.9.0_WK_IRPT_ANLREQ~277/fwd5_driver/test_fwd5_driver_routes.py` = `8c8a0a7c79`; `0.9.0_WK_IRPT_ANLREQ~275/fwd5_driver/test_fwd5_driver_envelope.py` = `f9eb292472`.
  </context>

  <the_act>
    0. NEVER-2 ledger read (every live worktree, `ls-tree`). Open ONE change ledger naming this order and BOTH users rows (by digest of the address, not the address): it stays OPEN until both principals read ABSENT.
    1. PRECONDITIONS, no write (STOP on any mismatch, name it): (a) `git rev-parse HEAD:<path>` of the four pinned files equals the pins above, and the packet at its path hashes to blob `6bf8cd3887`; (b) `python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~231/fwd5_driver/fwd5_driver.py --selftest` prints `FWD5-SELFTEST-OK`, and `--plan --control` prints the control line and sends nothing; (c) `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py absent` prints `R56-ABSENT-OK` (neither principal exists); (d) the server on 5174 answers a plain GET of `http://localhost:5174/` with any HTTP status (it is Andrew's: you only read; if it does not answer, STOP, do not start one); print its origin and checkout identity; (e) read-only: the synthetic job row exists under tenant `49financial`, READY, `hop_failure` ABSENT, both tickets exist, and the PACKAGED ticket carries a package (its `report_ref`, `original_ref`, `pdf_ref` and `commentary_ref` keys: key NAMES only, no values); if the packaged ticket carries no package, STOP and tell the issuer.
    2. PASSWORDS: generate two independent 32-byte random passwords (base64url) in memory, one per principal, reused for both targets; each goes ONLY to the helper or driver that needs it on STDIN as one JSON object `{"password": "..."}`; never to argv, a file, the environment, a log or a message.
    3. MINT BOTH, one `mint` each, no retry: run principal `fwd5_mint.py mint --email fwd5-cottonwood-r60@opal.invalid --firm cottonwood --allowed-firm-ids cottonwood` must print `MINT-OK READBACK-OK` and `MINT-SCOPE allowedFirmIds=cottonwood entitlement_rows=0`; control `fwd5_mint.py mint --email fwd5-control-r60@opal.invalid --firm opal-capital --allowed-firm-ids 49financial` must print `MINT-OK READBACK-OK` and `MINT-SCOPE allowedFirmIds=49financial entitlement_rows=0`. Any `MINT-REFUSED`, `READBACK-BAD` or a different scope line: go to step 7 at once (remove whatever was minted), make no request, report. Then poll (read-only, up to 120 s, 10 s apart) the `email-index` count of each address until it reads 1.
    4. TARGET PACKAGED. CONTROL RUN first, ONE run, no retry: `python <driver> --control --base http://localhost:5174 --email fwd5-control-r60@opal.invalid --ticket TCK-20261014-2965a5e0 --firm-a opal-capital --firm-b 49financial --request-id REQ-28a5ca6be3b7f438a9ca8217 --job-id REQ-28a5ca6be3b7f438a9ca8217 --out org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd5_s3/packaged/ --go IRPT_ANLREQ.TO-RUN-FWD5.live-cross-firm-s3-ib2`, password on stdin. Exit 0 is required. If the exit is 1 or 2: do NOT run the firm-B run for this target (a broken control grades nothing); go on to step 6 for this target, name the failing route. Then the FIRM-B RUN for this target, ONE run, no retry: the same command WITHOUT `--control`, with `--email fwd5-cottonwood-r60@opal.invalid --firm-a cottonwood --firm-b 49financial`, its own password on stdin. Exit 0: all 13 made calls REFUSED. Exit 1 (a LEAK): STOP the sitting, go to step 7 FIRST, then report the route name only. Exit 2 (an UNREACHED call): report which route, not a pass.
    5. TARGET SYNTHETIC: the same two runs (control first, the firm-B run only after a control exit 0) with `--ticket TCK-20261015-944c84f8 --request-id REQ-d47252fe74634d0c5cdd8067 --job-id REQ-d47252fe74634d0c5cdd8067 --out org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd5_s3/synthetic/`, everything else as in step 4. A LEAK in the first target skips this target (step 7 first).
    6. CHECKS (read-only, after the runs): `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py control`, `... report`, `... fence`; print each line verbatim in your report. A control DENIED with `FIRM_BINDING` or `NOT_AUTHORIZED` on a route is a broken control there: name the route in the report; do not retry.
    7. REMOVE BOTH principals, always, even after a refusal or a stop: `fwd5_mint.py remove --email <each>`; read `ABSENT GSI` and `ABSENT CONSISTENT` for each (the helper polls up to 300 s); then `... r56_checks.py absent` must print `R56-ABSENT-OK`. If a principal is still PRESENT after the window, say so loudly and keep the ledger OPEN (its TTL is 3 hours; do not delete by any other means).
    8. CLOSE the ledger only when step 7 reads ABSENT for both. Print the origin and checkout identity of 5174 again and say if it changed. Write the proof instance beside this order in `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/` (the root, not a subfolder) and validate it VALID with `python .tools/proof-of-spec-check.py <instance> AR75-tz-AC1,AR75-tz-AC2,AR75-tz-AC3` BEFORE you report: use phase `BUILD-GENERAL`, `controls.mutant.status` `N/A-SPEC-NAMES-NONE`, artifact `kind` `aws_resource` with `deployed_state` `DEPLOYED-VERIFIED` for the two users rows, and a `path_or_key` that does not read as a git path (the `aws:dynamodb opal-users-v2 ...` form). The instance may record AC1 or AC3 FAIL if the control or the fence did not hold: that is the honest grade. Report once; the status flip is the issuer's.
  </the_act>

  <bounds>
    - TWO users rows (the two addresses above), each minted once and removed once, in `opal-users-v2` only. The only requests are the driver's: `POST /auth/login` and GETs of the listed shapes on `http://localhost:5174`. No write to any ticket, request, job, queue, bucket, schedule, secret or other table; no Terraform; no code deploy; no change to the 5174 server or its checkout.
    - No retry of any mint, run or removal. For each target the control runs before the firm-B run; the firm-B run never runs after a failed control.
    - No password, hash, token, cookie, address or response body in any file, log or message; print route names, statuses, verdicts, codes, counts and the check lines only.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule, trigger, mapping or code moves; two users rows are written and removed within the sitting and the driver sends read-shaped GETs.
comp-iam: DECLARED-NOT-APPLICABLE -- no permission changes; the mint and removal use the applier's existing reach on `opal-users-v2` (the same helper family as the first two sittings), or the step is NOT MADE.
comp-adversary: RUN -- a false LEAK from the principal's own firm in a list body (the markers are the ticket id and `49financial`, never `cottonwood`; the flag labels are inverted, the context says which); a broken control read as a pass (each target's control exit is required before its firm-B run); a control DENIED by the fence itself read as past the fence (RE-SIGN 4: it is a broken control on that route); a principal left behind after a stop (step 7 always runs; TTL 3 hours is the backstop); the shared 5174 server stopped or restarted (forbidden; precondition d only reads it); a password in argv or a log (stdin only); sign-in failing because the email index lags (step 3 polls it); the packaged ticket carrying no package (precondition e STOPs); the packaged request having no job row (the job-level read is expected NOT_FOUND for the control).
lane: the applier's deliverables, logs, the change ledger and its sentinel.
</preflight>

<proof_of_spec>
  <criterion id="AR75-tz-AC1" cell_refs="AR-tz-75"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py fence</invocation><expect>R56-FENCE-OK</expect></criterion>
  <criterion id="AR75-tz-AC2" cell_refs="AR-tz-75"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py absent</invocation><expect>R56-ABSENT-OK</expect></criterion>
  <criterion id="AR75-tz-AC3" cell_refs="AR-tz-75"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py report</invocation><expect>R56-REPORT-OK</expect></criterion>
</proof_of_spec>
  AC1 (per target and route the fence is SHOWN, control ALLOWED and firm B REFUSED, or PAST-FENCE, control DENIED with a non-fence code and firm B REFUSED; the three file routes SHOWN on the packaged target; the no-selection call refused by absence) reads FAIL at the base (`R56-FENCE-FAIL no reports under ...`) and must read OK after step 5. AC2 is the restore control: it reads OK at the base (`R56-ABSENT-OK both principals: no PROFILE row (consistent), index count 0`) and must read OK after step 7. AC3 (both firm-B run reports: 13 REFUSED, 0 LEAK, 0 UNREACHED, 2 EXCLUDED of 15, rc 0, every report-side REFUSED carrying a fence code except the no-selection call, nothing secret) reads FAIL at the base and OK after step 5. The checker's `--self-test` reads `R56-SELFTEST-OK 16 cases`.

<expected_criteria>AR75-tz-AC1,AR75-tz-AC2,AR75-tz-AC3</expected_criteria>

  <report>
    One report to 2.0.0_SA_COO~T2 (statuses only): the precondition reads and the pin comparison; the origin and checkout identity of 5174 before and after; the mint lines of both principals (the MINT-SCOPE lines are ids only); for each target the control run's exit and its route verdicts and codes, and the firm-B run's exit and its route verdicts and codes (or "not run: control exit N"); the three check lines; the removal lines (ABSENT GSI / CONSISTENT for each) and the `absent` check; the ledger id and its state; commit hashes (read with an author filter) and the measured push state. Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
