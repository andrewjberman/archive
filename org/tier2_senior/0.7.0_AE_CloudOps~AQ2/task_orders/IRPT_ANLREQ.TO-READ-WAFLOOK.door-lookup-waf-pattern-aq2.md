<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-WAFLOOK.door-lookup-waf-pattern-aq2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-16</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order on the resident host through Systems Manager, as root: one script sent, which reads the journal and the instance metadata and runs one transient systemd unit with the resident service's own user, environment and interpreter (the running root is its working directory). It makes ONE outbound request, the one the upload door makes for every upload: a cookieless GET /securities/securities_info?securities=ZQXWVK to YCharts (no stored session, no provider lease, no login, no secret read). No install, no restart, no root switch, no queue message, no S3 write. The running root stays r34e. The four uploads' finding rows are READ only.
comp-routes: DECLARED-NOT-APPLICABLE -- no route of ours is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; your principal already sends commands to this host.
comp-adversary: RUN -- by reading the CTO's decisions (msgs 9422, 9429), AQ2's SET 2 record, the issuer's erratum (the door's lookup is sessionless: resident_session.py 120-131, operation_lease.py 298-317, transport.py 487-504) and the offline test of the script (11 cases) against this cell; the lens: a lookup made through the stored session (the script builds a cookieless transport and prints the jar size, which must be 0), a lookup that collides with a live resident operation (the busy guard refuses while the resident handled a message in the last 60 s; exit 70), a body or crumb printed (the first 200 characters only, crumb= redacted), a single lookup repeated (the script makes exactly one), a read of the four rows that prints a holding. NOT seen (blind): whether the challenge persists now, and what the WAF keys on; denominator: one host, one unit, one lookup, one journal window, four rows.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R41_G.md</decomp_doc> round 41, workstream ~G: the pattern behind the WAF challenge on the upload door's lookup (cell AR-g-128).
<owned_cells>AR-g-128</owned_cells>
</decomp_ref>

  <objective>
    READ the journal lines, the host's address and the four uploads' finding rows, and make ONE cookieless lookup the door's own way; write one record, commit it, and report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2. Change NOTHING on the host or in AWS. SEND THE SCRIPT AS ROOT.
  </objective>

  <context>
    Load /cloud-ops first. FWD-1 run 3 SET 2 (your record A_SET2_JOURNAL_R3.txt): ZQXWVK's resolve was challenged (PROVIDER_READ_UNAVAILABLE:WAF_CHALLENGE) on all four receives while four earlier resolves answered. The CTO's decision (msgs 9422 and 9429): you read the journal lines and the four rows; then ONE cookieless lookup, made the door's own way, to see whether the challenge persists. The door's lookup is SESSIONLESS by design (CTO rulings batch 72 item 12): no cookie, nothing from the stored session. The script: org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/waf_lookup_probe.sh, sha256 0022c326ceba53f972db20db6aafa8281f5ac1ab30c89f18928f97b18c420e11 (commit 14d8b8e9dc; verify before you send it). Its defaults: journal window 2026-10-16 13:36:00 to 13:45:00 UTC, symbol ZQXWVK. Its lines begin `WAF`; the lookup's lines begin `WAF LOOKUP`; exit codes: 61 an empty unit property, 70 the resident was busy (no lookup made), 2 the lookup raised.
  </context>

  <the_act>
    GO. Start at step 1 and stop on any step that reads wrong, telling 2.0.0_SA_COO~G2.
    1. Verify the script's sha256 against the value in the context. Read every live worktree's org/critical_paths/.open_deploys/ (git worktree list, then git -C <wt> ls-tree) and print the denominator: another open entry naming the resident host or the unit is a STOP; your own held run-3 ledger irpt-fwd1-run3-20261016 is printed and is NOT a stop (it writes nothing to the host until its window).
    2. Send the script to the resident host by Systems Manager AS ROOT and capture its full output. On exit 70 (busy), wait two minutes and send it ONCE more; on a second 70, 61 or any other failure, STOP and report the last lines. The lookup is made exactly once: do not re-send after a lookup line has printed.
    3. THE FOUR ROWS: with your existing read path for the uploads' NORMALIZATION rows, read the four finding rows of the SET 2 uploads that ended READY (their upload ids are in your OBJECTS_WRITTEN_FWD1_R3.txt; ZQXWVK's row too, which ended NEEDS_CORRECTION RESOLVE_RETRY_EXHAUSTED). Print for each: the symbol, the row state and the finding codes with their actions. No holding value, no amount, no file content.
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_fwd1_r3/WAFLOOK_READ.txt holding the script's output verbatim, a blank line, then the five row lines (`ROW <symbol> <state> <codes and actions>`). Commit it alone. Report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the commit and, in your own words and marked INFERRED where it is: whether the lookup answered clean (status 200, no WAF action, JSON) or was challenged, the host's public address, what the journal lines show about the session, and what the four rows answered.
  </the_act>

  <bounds>
    One host, one unit, read-only apart from the transient unit and its temp file. ONE request to YCharts's lookup route (cookieless). No install, no restart, no root switch, no queue message, no S3 write, no Terraform, IAM, Lambda, table or route change, no delete, no sign-in, no secret read. Not in this order: the resident change, SET 3, run 3, the classifier.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_fwd1_r3/IRPT_ANLREQ.TO-READ-WAFLOOK.door-lookup-waf-pattern-aq2.proof_of_spec.json`.
    <criterion id="WAFLOOK-AC1" cell_refs="AR-g-128">The record holds exactly one lookup result line (answered or raised) and the five row lines.<invocation>grep -c -E '^(WAF LOOKUP status=|WAF LOOKUP EXCEPTION|ROW [A-Z0-9^.:_-]+ )' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_fwd1_r3/WAFLOOK_READ.txt</invocation><expect>^6$</expect></criterion>
    <criterion id="WAFLOOK-AC2" cell_refs="AR-g-128">The record carries no crumb value.<invocation>grep -c -E 'crumb=[A-Za-z0-9]' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_fwd1_r3/WAFLOOK_READ.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-g-128 is the issuer's, as for TO-READ-EXCCLASS.
