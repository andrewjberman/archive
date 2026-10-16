<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R18-CLOSE.close-the-part-1-test-ticket-and-read-the-notice-path-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-16</date>
    <status>complete</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>19</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R19.md</decomp_doc> (round 19): cell `R19-rl-7`, the release's after-read (the CTO's condition 1 of the combined pair); the ticket closed here is `TO-R18-RUN` PART 1's.
<owned_cells>R19-rl-7</owned_cells>
</decomp_ref>

  <objective>
    STAGED. No GO until the issuer adds a CONDITIONAL GO amendment on the signed run pair's AMENDMENT 4 (both halves). On the GO: CLAIM and then COMPLETE the part-1 meeting test ticket `TCK-20261016-9d7654eb` as one minted synthetic internal identity (the part-1 filer identity, `allowedFirmIds ["cottonwood"]`), read each transition back, delete the identity row after `exp` and read it ABSENT, and write one result file. The claim's pickup notice resolves no recipient (the contact map is empty) and logs `WE_CLIENT_NO_CONTACT`; that exercises the CTO's after-read, which the issuer runs.
  </objective>

  <context>
    Authority: the CTO's after-read condition on the combined release pair (msg 9624: zero `WE_CLIENT_SENT` AND at least one `WE_CLIENT_NO_CONTACT` since the apply end 2026-10-16T17:57:19Z), and the run pair `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md` AMENDMENT 4. Your PART 1 (`TO-R18-RUN`, msg 9806) left the meeting ticket open by design; the notice path is on CLAIM (`lambda_function.py` line 1658), not on the internal CREATE you ran.
    Model: `TO-R18-RUN` PART 1 (your script `r18_run_meeting.py`): the filer identity row (`USER#tckt-r18-filer-20261016@opal.invalid`, `PROFILE`, `firmId opal-capital`, `userType "test-filer"`, `allowedFirmIds` the LIST `["cottonwood"]`, `attribute_not_exists(PK)`), one RS256 token of at most 20 minutes (key and token in memory only, the key read reported after the fact through `0.0.0_AB_MSTR~DELL2`), the reused server on `http://localhost:5174` (Andrew's smoke copy: reuse, NEVER start, stop or restart it; the page origin printed).
  </context>

  <go>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~V2, 2026-10-16 ~20:0xZ; gate limb: none graded this modification; it names the GO, no placeholder, no path widened). CONDITIONAL GO. THE PAIR'S AMENDMENT 4 IS SIGNED BY BOTH HALVES: COO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md` (git blob `b83e173a019aa9a0078a48b126f2b52040122314`, sha256 `3c4134bd9e6807714bdfe9a54820f51d7c7f98f58fe1f2670e55984c5c6e1960`, @9f20d14148); CTO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/R18_RUN_PAIR_CTO_HALF.md` (git blob `ea18a440851b55f2ddb4f0261352152c8f83b06f`, @7b473a3455, msg 9814). Measure these two blobs, the AMENDMENT 1 CTO half (`cf7c856072d14b70122bb53afbc9259156702d66`, the origin condition) and the criterion `R18_CHECKS/r18_afterread.py` (`60ff76b6073c2c7072c1d4fdb71dddb2c5a0118e`) with `git hash-object` BEFORE the start gate; any difference is a STOP and no GO. The identity is the part-1 filer `tckt-r18-filer-20261016@opal.invalid` (it was deleted after part 1 and reads ABSENT: re-read it; PRESENT is a STOP), `allowedFirmIds ["cottonwood"]`. THE CTO'S PASS (msg 9814): the issuer's after-read prints zero `WE_CLIENT_SENT` and at least one `WE_CLIENT_NO_CONTACT` with the events scanned; ANY `WE_CLIENT_SENT` stops and is a release defect: if the claim or the complete produces one, STOP at once, do nothing further to the ticket, report it first. The reused server on 5174 is Andrew's smoke copy: NEVER start, stop or restart it. Report once to the issuer when the ticket reads completed, the row reads ABSENT and the ledger is closed; the issuer runs the after-read.
    The GO's steps are unchanged:
    1. STEP 0: open the NEVER-2 ledger entry and keep it open until the row reads ABSENT. Measure the blobs the GO names. Start gate: `TO-R18-RUN` is `complete` and its ledger closed; the ticket `TCK-20261016-9d7654eb` reads `meeting_request`, `open`, unassigned, firm `cottonwood` (any other state is a STOP); no open ledger names `opal-ticket-api`, `opal-tickets` or `opal-users-v2` in any live worktree (print the denominator); the reused server answers on `http://localhost:5174`.
    2. STEP 1: mint the identity row and its token; print the row's role set (role, userType, firmId, allowedFirmIds, entitlement rows: 0).
    3. STEP 2: as the identity, in the browser on the reused server (the Ticket Center by the sidebar link, the Open tab, the ticket listed), press Claim on that ticket only; ConsistentRead it (`status in_progress`, the assignee the identity); print the log tokens the claim produced (the issuer expects `WE_CLIENT_NO_CONTACT firm=cottonwood` and no `WE_CLIENT_SENT`). Then press Complete; ConsistentRead (`status completed`). No other ticket, button or tab.
    4. STEP 3: wait until `exp` has passed; delete the identity row; ConsistentRead ABSENT.
    5. STEP 4: write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r18_run/R18_CLOSE_RESULT.json` with `ticket`, `claim_status`, `claim_assignee`, `complete_status`, `log_tokens` (the WE_* tokens each transition produced), `identity`, `row_deleted_at`, `token_exp`, `row_absent_after`, `browser_origin`, `server_reused`, `change_ledger`. Close the ledger; write the proof instance; flip the order; report once to `2.0.0_SA_COO~V2`. The issuer runs the after-read (`R18_CHECKS/r18_afterread.py`) itself.
    If a `WE_CLIENT_SENT` token appears at any step: STOP at once, report it first, and do nothing further to the ticket.
  </go>

  <bounds>
    The blast radius is the pair's AMENDMENT 4: ONE synthetic test ticket moves open to in_progress to completed; ONE `opal-users-v2` row created and deleted. No other ticket, no S3 object, no Lambda environment change, no IAM, no Terraform, no routing window, no key, no IRPT write, no dev server started or stopped. No mail: a `WE_CLIENT_SENT` is a STOP.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R19CLOSE-AC1" cell_refs="R19-rl-7"><invocation>python -I org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_CHECKS/r18_afterread.py</invocation><expect>^AFTERREAD-OK </expect></criterion>
</proof_of_spec>
`R19CLOSE-AC1` at the issuance: FAIL as expected (`AFTERREAD-BAD ... UNEXERCISED`: zero SENT, zero NO_CONTACT since the apply end; the control window reads SENT 7, so the instrument sees the token). It reads the ticket service log read-only.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE -- no permission changes; the identity row is written and deleted with the operator's own credentials; the key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`.
comp-adversary: the control is the check's independent log read with its control window; the lens: a WE_CLIENT_SENT (a STOP), a claim or complete of another ticket, the reused server stopped or restarted (forbidden), a second identity row, a token printed.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R19-rl-7): a live run under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
