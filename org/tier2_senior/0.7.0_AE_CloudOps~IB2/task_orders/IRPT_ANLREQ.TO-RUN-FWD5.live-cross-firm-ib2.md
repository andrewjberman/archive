<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-FWD5.live-cross-firm-ib2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-16</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>61</round>
<workstream>~T</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R61_T.md</decomp_doc>
<owned_cells>AR-tz-71</owned_cells>
<decomp_context>Round 61, cell AR-tz-71: the FWD-5 live cross-firm exercise with its POSITIVE CONTROL, under the re-signed pair: mint two synthetic principals on DEV, run the driver's control mode and then its firm-B run against the one synthetic ticket of 49financial, remove both principals. No write to any ticket, request or job.</decomp_context>
</decomp_ref>

  <objective>
    Show, live, that a firm-B principal (cottonwood) is REFUSED on every call for firm A's one synthetic ticket while an identity entitled to that ticket (the control) reads ALLOWED on the same list, so each REFUSED is the fence and not a broken route. Mint two scoped principals, run `fwd5_driver.py --control` and then `fwd5_driver.py`, remove both principals, write the two reports and the proof instance. Statuses, route names, counts and hashes only: never a body, a token, a password or an address in any file or message.
  </objective>

  <context>
    Authority and pair (read these first, in this order): the packet `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~T2/R58_FWD5_LIVE_EXERCISE_PACKET_DRAFT_20261016.md` at commit 9666f7bf14, blob `57052520eb` (sha256 `0a0bec98...`), sections 1, 1a2, 1c, 3, 4, 7, 7b; the CTO half `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_FWD5_LIVE_CROSS_FIRM_RUN_CTO_HALF.md`, section RE-SIGN 2 (@e1062579f2), which covers both branches (control broken grades nothing and S134 stays ARMED; a LEAK stops the sitting whatever the control reads, both principals removed first). The laptop CTO's ruling XA-20261016T191116Z-4c60 (YES) carries; its binding condition is the positive control (CTO msg 9804). The CTO's condition 1 (msg 9779): localhost:5174 serves Andrew's smoke copy (`C:/dev/smoke-template-5174`); this run REUSES that server and NEVER starts, stops or restarts it; if the driver needs a checkout it does not carry, STOP and tell the issuer (who asks the CTO).
    The labels (packet section 1a2, easy to invert): the driver's `--firm-a` is the PRINCIPAL's own firm and `--firm-b` is the TICKET OWNER's firm. Run principal: firm-a `cottonwood`, firm-b `49financial`. Control principal: firm-a `opal-capital`, firm-b `49financial`.
    Fixed inputs: ticket `TCK-20261015-944c84f8`; request and job `REQ-d47252fe74634d0c5cdd8067` (tenant `49financial`; the synthetic row, READY, no `hop_failure` since t56); base `http://localhost:5174`; run principal email `fwd5-cottonwood-r60@opal.invalid`; control principal email `fwd5-control-r60@opal.invalid`; go token = this order's id `IRPT_ANLREQ.TO-RUN-FWD5.live-cross-firm-ib2`; out dir `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd5/`. Pins at HEAD (packet sections 7 and 7b; paths under `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/`): `0.9.0_WK_IRPT_ANLREQ~219/fwd5_driver/fwd5_mint.py` = `ec8607ed57`; `.../test_cross_firm_mint.py` = `4c9f115d4e`; `0.9.0_WK_IRPT_ANLREQ~231/fwd5_driver/fwd5_driver.py` = `06206f2864`; `0.9.0_WK_IRPT_ANLREQ~272/fwd5_driver/test_fwd5_driver_control.py` = `2186cd2731`.
  </context>

  <the_act>
    0. NEVER-2 ledger read (every live worktree, `ls-tree`). Open ONE change ledger naming this order and BOTH users rows (by digest of the address, not the address): it stays OPEN until both principals read ABSENT.
    1. PRECONDITIONS, no write (STOP on any mismatch, name it): (a) `git rev-parse HEAD:<path>` of the four pinned files equals the pins above, and the packet at its path hashes to blob `57052520eb`; (b) `python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~231/fwd5_driver/fwd5_driver.py --selftest` prints `FWD5-SELFTEST-OK`, and the same with `--plan --control` prints the control line and sends nothing; (c) `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py absent` prints `R56-ABSENT-OK` (neither principal exists); (d) the server on 5174 answers a plain GET of `http://localhost:5174/` with any HTTP status (it is Andrew's: you only read; if it does not answer, STOP, do not start one); (e) read-only: the job row `REQ-d47252fe74634d0c5cdd8067` under tenant `49financial` exists, state READY, `hop_failure` ABSENT, and the ticket `TCK-20261015-944c84f8` exists (no write; any `report_ref` attribute already on it is fine and is reported).
    2. PASSWORDS: generate two independent 32-byte random passwords (base64url) in memory, one per principal; each goes ONLY to the helper or driver that needs it on STDIN as one JSON object `{"password": "..."}`; never to argv, a file, the environment, a log or a message.
    3. MINT BOTH, one `mint` each, no retry: run principal `fwd5_mint.py mint --email fwd5-cottonwood-r60@opal.invalid --firm cottonwood --allowed-firm-ids cottonwood` must print `MINT-OK READBACK-OK` and `MINT-SCOPE allowedFirmIds=cottonwood entitlement_rows=0`; control `fwd5_mint.py mint --email fwd5-control-r60@opal.invalid --firm opal-capital --allowed-firm-ids 49financial` must print `MINT-OK READBACK-OK` and `MINT-SCOPE allowedFirmIds=49financial entitlement_rows=0`. Any `MINT-REFUSED`, `READBACK-BAD` or a different scope line: go to step 7 at once (remove whatever was minted), make no request, report. Then poll (read-only, up to 120 s, 10 s apart) the `email-index` count of each address until it reads 1.
    4. CONTROL RUN first, ONE run, no retry: `python <driver> --control --base http://localhost:5174 --email fwd5-control-r60@opal.invalid --ticket TCK-20261015-944c84f8 --firm-a opal-capital --firm-b 49financial --request-id REQ-d47252fe74634d0c5cdd8067 --job-id REQ-d47252fe74634d0c5cdd8067 --out org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd5/ --go IRPT_ANLREQ.TO-RUN-FWD5.live-cross-firm-ib2`, password on stdin. Exit 0 is required (ticket-read and ticket-list ALLOWED). If the exit is 1 or 2: do NOT run step 5 (a broken control grades nothing); go to step 7.
    5. FIRM-B RUN, ONE run, no retry: the same command WITHOUT `--control`, with `--email fwd5-cottonwood-r60@opal.invalid --firm-a cottonwood --firm-b 49financial`, its own password on stdin. Read the exit: 0 all 7 made calls REFUSED; 1 a LEAK: STOP the sitting, go to step 7 FIRST, then report the route name only; 2 an UNREACHED call: report which route, not a pass.
    6. CHECKS (read-only, after step 5): `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py control`, `... report`, `... fence`; print each line verbatim in your report.
    7. REMOVE BOTH principals, always, even after a refusal or a stop: `fwd5_mint.py remove --email <each>`; read `ABSENT GSI` and `ABSENT CONSISTENT` for each (the helper polls up to 300 s); then `... r56_checks.py absent` must print `R56-ABSENT-OK`. If a principal is still PRESENT after the window, say so loudly and keep the ledger OPEN (its TTL is 3 hours; do not delete by any other means).
    8. CLOSE the ledger only when step 7 reads ABSENT for both. Write the proof instance beside this order in `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/` (the root, not a subfolder) and validate it VALID with `python .tools/proof-of-spec-check.py <instance> AR71-tz-AC1,AR71-tz-AC2,AR71-tz-AC3` BEFORE you report: use phase `BUILD-GENERAL`, `controls.mutant.status` `N/A-SPEC-NAMES-NONE`, artifact `kind` `aws_resource` with `deployed_state` `DEPLOYED-VERIFIED` for the two users rows, and a `path_or_key` that does not read as a git path (the `aws:dynamodb opal-users-v2 ...` form). The instance may record AC1 FAIL if the control or the fence did not hold: that is the honest grade. Report once; the status flip is the issuer's.
  </the_act>

  <bounds>
    - TWO users rows (the two addresses above), each minted once and removed once, in `opal-users-v2` only. The only requests are the driver's: `POST /auth/login` and GETs of the listed shapes on `http://localhost:5174`. No write to any ticket, request, job, queue, bucket, schedule, secret or other table; no Terraform; no code deploy; no change to the 5174 server or its checkout.
    - No retry of any mint, run or removal. The control runs before the firm-B run; the firm-B run never runs after a failed control.
    - No password, hash, token, cookie, address or response body in any file, log or message; print route names, statuses, verdicts, counts and the check lines only.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule, trigger, mapping or code moves; two users rows are written and removed within the sitting and the driver sends read-shaped GETs.
comp-iam: DECLARED-NOT-APPLICABLE -- no permission changes; the mint and removal use the applier's existing reach on `opal-users-v2` (the same helper family as TO-RUN-AR-v33's mint), or the step is NOT MADE.
comp-adversary: RUN -- a false LEAK from the principal's own firm in a list body (the markers are the ticket id and `49financial`, never `cottonwood`: the flag labels are inverted, step 5 says which); a broken control read as a pass (step 4's exit is required before step 5); a principal left behind after a stop (step 7 always runs; TTL 3 hours is the backstop); the shared 5174 server stopped or restarted (forbidden; precondition d only reads it); a password in argv or a log (stdin only); sign-in failing because the email index lags (step 3 polls the index before the runs); a ticket-list entry shape the control does not recognize (the control reads DENIED, exits 1, nothing is graded, both principals are removed: the safe failure).
lane: the applier's deliverables, logs, the change ledger and its sentinel.
</preflight>

<proof_of_spec>
  <criterion id="AR71-tz-AC1" cell_refs="AR-tz-71"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py fence</invocation><expect>R56-FENCE-OK</expect></criterion>
  <criterion id="AR71-tz-AC2" cell_refs="AR-tz-71"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py absent</invocation><expect>R56-ABSENT-OK</expect></criterion>
  <criterion id="AR71-tz-AC3" cell_refs="AR-tz-71"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py report</invocation><expect>R56-REPORT-OK</expect></criterion>
</proof_of_spec>
  AC1 (the fence is SHOWN on `ticket-read` and `ticket-list`: control ALLOWED and firm-B REFUSED, both reports well formed) reads FAIL at the base (`R56-FENCE-FAIL no report at ...`) and must read OK after step 5. AC2 is the restore control: it reads OK at the base (`R56-ABSENT-OK both principals: no PROFILE row (consistent), index count 0`) and must read OK after step 7. AC3 (the firm-B run report: 7 REFUSED, 0 LEAK, 0 UNREACHED, 2 EXCLUDED of 9, rc 0, nothing secret) reads FAIL at the base and OK after step 5. The checker's `--self-test` reads `R56-SELFTEST-OK`.

<expected_criteria>AR71-tz-AC1,AR71-tz-AC2,AR71-tz-AC3</expected_criteria>

  <report>
    One report to 2.0.0_SA_COO~T2 (statuses only): the precondition reads and the pin comparison; the mint lines of both principals (the MINT-SCOPE lines are ids only); the control run's exit and its route verdicts; the firm-B run's exit and its route verdicts (or "not run: control exit N"); the three check lines; the removal lines (ABSENT GSI / CONSISTENT for each) and the `absent` check; the ledger id and its state; commit hashes (read with an author filter) and the measured push state. Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
