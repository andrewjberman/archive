<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-PACING.door-lookup-count-per-window-ib2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-16</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order on the resident host through Systems Manager, as root: one script sent, which reads the instance metadata and runs one transient systemd unit with the resident service's own user, environment and interpreter (the running root is its working directory). It makes up to TWELVE outbound requests over about 21 minutes, each the one the upload door makes for every upload: a cookieless GET /securities/securities_info?securities=<SYMBOL> to YCharts for a known symbol (no stored session, no provider lease, no login, no secret read). No install, no restart, no root switch, no queue message, no S3 write.
comp-routes: DECLARED-NOT-APPLICABLE -- no route of ours is called. comp-cache: DECLARED-NOT-APPLICABLE.
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger; one run of the script.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; your principal already sends commands to this host.
comp-adversary: RUN -- by reading PRD v0.22 item 4 and the CRO's research (org/tier1_exec/4.0.0_SA_CRO/deliverables/RESEARCH_20261016_YCHARTS_PACING_AND_YFINANCE_FIRST.md section 2), the AQ2 read of the one cookieless lookup (clean) and the offline test of the script (11 cases) against this cell; the lens: a lookup made through the stored session (the script builds a cookieless transport per call), a lookup that collides with a live resident operation or with ~Y2's window (the caller makes sure the door is free; the script's busy guard refuses at the start when the resident handled a message in the last 60 s; exit 70), a challenged call that is repeated (each phase stops at its first challenge), a body or crumb printed (never: only status, waf action, content type, bytes and elapsed). NOT seen (blind): whether YCharts counts per window or by another rule (this read distinguishes the two), and the firewall's state when the script starts; denominator: one host, one unit, at most 12 lookups.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R45_G.md</decomp_doc> round 45, workstream ~G: the CRO's one measured read for the door's lease budget (cell AR-g-140).
<owned_cells>AR-g-140</owned_cells>
</decomp_ref>

  <objective>
    Run the paced lookup read ONCE, record its output verbatim, and report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2. Change NOTHING on the host or in AWS. SEND THE SCRIPT AS ROOT, with a command timeout of at least 3600 seconds. Do it AFTER ledger irpt-resident-r34g-20261016 reads CLOSED (the r34g apply, order IRPT_ANLREQ.TO-APPLY-R34G.resident-r34g-door-yfinance-first-ib2) and BEFORE ~Y2 starts window 4: ~Y2 starts only on your report.
  </objective>

  <context>
    Load /cloud-ops first. PRD v0.22 item 4: the door's lease should count lookups per window, with the budget set from one measured read: after a 390 s rest, six known-symbol lookups about 90 s apart, then (after the same rest) six about 5 s apart; the same cutoff index in both phases means a count per window. The script: org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/paced_lookup_probe.sh, sha256 89883f15acd542bf95237f6814042e0df99a2c85ca01c195a5f6bdf9024e031f (commit 54e7e67df7; verify before you send it). Its defaults are the read (rest 390 s, gaps 90 s and 5 s, six calls per phase); do not override them. Its lines begin `PACE`; each lookup line is `PACE PHASE <A|B> call=<n> symbol=<S> t=<time> verdict=<CLEAN|CHALLENGED|EXCEPTION> ...`; the end lines are `PACE RESULT cutoff_A=<n|none> cutoff_B=<n|none>` and `PACE VERDICT ...`. Exit codes: 61 an empty unit property, 70 the resident was busy (no lookup made). ~Y2 has said the door is free (msg 9692); window 4 waits for this read.
  </context>

  <the_act>
    GO once the r34g ledger reads CLOSED. Start at step 1 and stop on any step that reads wrong, telling 2.0.0_SA_COO~G2.
    1. Verify the script's sha256 against the value in the context. Print the r34g ledger's status (it must read CLOSED) and the resident's journal count of messages handled in the last 5 minutes (must be 0; otherwise wait two minutes, once).
    2. Send the script to the resident host by Systems Manager AS ROOT with ExecutionTimeout 3600 and capture its full output (about 21 minutes). On exit 70, wait two minutes and send it ONCE more; on a second 70, 61 or any other failure, STOP and report the last lines. Do not re-send after any lookup line has printed.
    3. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34g/PACED_READ.txt holding the script's output verbatim. Commit it alone. Report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the commit, the two PACE lines (RESULT and VERDICT) and the first challenged call's time in each phase if any, marked INFERRED where you read into it.
  </the_act>

  <bounds>
    One host, one unit, read-only apart from the transient unit and its temp file. At most TWELVE requests to YCharts's lookup route (cookieless). No install, no restart, no root switch, no queue message, no S3 write, no Terraform, IAM, Lambda, table or route change, no delete, no sign-in, no secret read. Not in this order: the lease change itself (a later release), window 4, the classifier.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34g/IRPT_ANLREQ.TO-READ-PACING.door-lookup-count-per-window-ib2.proof_of_spec.json`.
    <criterion id="PACING-AC1" cell_refs="AR-g-140">The record holds exactly one RESULT line and one VERDICT line.<invocation>grep -c -E '^PACE (RESULT cutoff_A=|VERDICT )' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34g/PACED_READ.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PACING-AC2" cell_refs="AR-g-140">The record carries no crumb value.<invocation>grep -c -E 'crumb=[A-Za-z0-9]' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34g/PACED_READ.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-g-140 is the issuer's, as for TO-READ-WAFLOOK.
