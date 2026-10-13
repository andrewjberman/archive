<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-Z6-R4.svc-intake-remint-backlog-read-then-pin</id>
    <issued_by>2.0.0_SA_COO~ZB</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZT</issued_to>
    <date>2026-10-13</date>
    <status>pending -- issued 2026-10-13 ~20:5xZ, Z6 repairs issuance (CTO ruling @61e3067f5c disposition 4 as amended by CTO msg 33741); queue position 2 of 2 on this lane, after TO-Z6-R5; GATED on the never-widen pair's CTO half</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>WORLD</risk>
# pipeline-override: flat project with no tree home (OPAL_BBGTML, org/projects/OPAL_BBGTML.json); one cell of the Z6 repairs issuance ruled by 1.0.0_SA_CTO~Z @61e3067f5c + msg 33741; the order is the LD-0529 carrier to a Tier-2 seat

  <objective>
    The D7 ticket intake (Scheduled Task OPAL_D7_ticket_intake, every 5 minutes) has not completed a pass since 2026-09-03 for
    two stacked reasons: its gateway identity pin can never match (exit 2), and behind it, its portal fetch token expired on
    2026-09-19 (HTTP 403). Re-mint the fetch token, read the backlog, and land the pin only if the first good pass would post nothing.
  </objective>

  <context>
    THE SPEC IS THE NEVER-WIDEN PAIR. COO half:
    org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/NEVER_WIDEN_PAIR_SVC_ANALYST_INTAKE_REMINT_COO_HALF.md. Read it in full; where
    this order and the pair differ, the pair wins. Its header names the CTO half. If the header does not name a COMMITTED CTO
    half file carrying a SIGNED line, STOP before step 1 and report "BLOCKED-ON-CTO-HALF". That is the gate, not a formality.
    Row OPAL_BBGTML-Z-S14 (org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md) records the measurements; this cell disarms it.
    LIVE PRODUCTION: integrations/ticketing/intake/runner_config.json is read by the runner every 5 minutes FROM THE SHARED
    WORKING TREE; saving it IS the deploy, bound by bar A5-A7 (exercise in the SAME act, in this tree, or revert first).
    The pass posts into the CLIENT ticket channel. A post into that channel that the backlog read did not license is the one
    outcome this order exists to prevent.
    Precedent mint script (method only; the subject, secret and write differ): 
    org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/pk_mint/mint_packager.py.
  </context>

  <the_act>
    Follow the pair's section 3, steps 1-3, in order, as ONE act:
    1. RE-MINT. Write org/tier2_senior/0.7.0_AE_CloudOps~ZT/deliverables/r4_remint.py: without --go it does the before-read only
       (the versions table must still read AWSCURRENT 77bf1488-d32c-4e17-96b6-18bf9b2d7638); with --go it mints per the pair's
       section 2 and calls put-secret-value on opal/ticketing/svc-analyst-intake; with --readback it decodes the stored token
       WITHOUT verifying, prints claim NAMES and the iss/aud/sub/userType/name values, exp-iat in days, the new VersionId, and
       does one GET {api_base}/api/scoped/tickets?status=open&amp;limit=1 printing only the HTTP status. The token and the signing
       key are never printed, logged or written to disk.
    2. BACKLOG READ: AC2.
    3. THE PIN, by the pair's branches:
       - BACKLOG: ZERO -> open the ledger entry
         python .tools/deploy_ledger.py open --slug opal-bbgtml-z6-r4-intake-pin-20261013 --title "OPAL_BBGTML Z6 R4: intake gateway pin -> oid" --author 0.7.0_AE_CloudOps~ZT --leg "L1|git|runner_config.json line 11 in the shared working tree|commit hash" --leg "L2|verify|AC3 + the next scheduled pass|runner.log lines"
         set line 11 to "identity": "517aa5ee-b4d0-425a-b493-5a22ff77ac4f" (nothing else), run AC3 in the same act, then read the
         next scheduled pass in %USERPROFILE%/opal_ticket_intake/runner.log (expect "intake pass exit 0", buzzed=0), close the entry.
       - BACKLOG: N (rc 1) -> do NOT touch runner_config.json. Stop and report N and the cursor. The call is Andrew's.
       - UNKNOWN (rc 3) after the re-mint -> do NOT touch the pin; roll the secret back per the pair's section 4; file a row.
  </the_act>

  <bounds>
    - Writes: ONE new version of opal/ticketing/svc-analyst-intake, and on BRANCH ZERO only, line 11 of runner_config.json.
      Nothing else: no create-secret, no delete-secret, no IAM, no other secret, no change to opal/auth/jwt-*.
    - Never run the runner without --dry-run. Never send to Teams. Never print a ticket's text into a committed file: the
      backlog read prints counts only, keep it that way.
    - The claim set is the 08-20 set exactly (pair section 2). Adding any claim is a widening and is refused.
    - A surprise is a row in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md (disarm_owner 2.0.0_SA_COO~ZB); keep working.
  </bounds>

  <paths>
    integrations/ticketing/intake/runner_config.json
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~ZT/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~ZT/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~ZT/task_orders/
    org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="Z6-R4"><invocation>python org/tier2_senior/0.7.0_AE_CloudOps~ZT/deliverables/r4_remint.py --readback; echo "exit=$?"</invocation><expect>after the --go run: claim names exactly aud, exp, iat, iss, name, nbf, sub, userType; iss opal-portal-auth, aud opal-portal-api, sub svc-analyst-intake, userType service, name "Opal Analyst Intake (service)"; exp-iat = 30 days; a VersionId other than 77bf1488-d32c-4e17-96b6-18bf9b2d7638 now AWSCURRENT; the one fetch answers HTTP 200; exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="Z6-R4"><invocation>python org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/z6_checks/r4_backlog_read.py; echo "exit=$?"</invocation><expect>a number, not UNKNOWN: either "BACKLOG: ZERO" with exit=0, or "BACKLOG: N" with exit=1; the cursor line and the fetched denominator printed. (Before the re-mint it read FETCH_FAILED 403, exit=3 -- the control.)</expect></criterion>
  <criterion id="AC3" cell_refs="Z6-R4"><invocation>python -m integrations.ticketing.intake.runner --dry-run 2>&amp;1 | grep -E "IDENTITY-FAIL|FETCH_FAILED|INTAKE PASS|REFUSED"; echo "exit=${PIPESTATUS[0]}"</invocation><expect>BRANCH ZERO only, run from the repo root in the same act as the pin edit: an "INTAKE PASS" summary line with buzzed=0, no IDENTITY-FAIL and no FETCH_FAILED line, exit=0 (6 is a sweep fault: a row, not a rollback). On BRANCH N this criterion is recorded NOT-RUN with the reason "backlog N, the call is Andrew's".</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE as a deliverable file under org/tier2_senior/0.7.0_AE_CloudOps~ZT/deliverables/ and in your final message: each
    criterion's output, the branch taken, the new VersionId, the rotate_by date, the ledger slug and close state (branch zero),
    the next scheduled pass's runner.log lines, and push state as a measured value. Leave the status flip to the issuer.
  </report>
</task_order>
