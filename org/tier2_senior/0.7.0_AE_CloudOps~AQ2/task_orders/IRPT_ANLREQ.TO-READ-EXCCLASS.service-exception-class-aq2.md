<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-EXCCLASS.service-exception-class-aq2</id>
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
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order on the resident host through Systems Manager, as root (the channel of the r34d apply): one script sent, which runs one transient systemd unit with the resident service's own user, environment and interpreter (PYTHONPATH and the working directory pointed at the kept r34d root). It makes TWO Yahoo calls (ZQXWVK, then SPY as the control) and prints the exception each raises. No install, no restart, no root switch, no queue message, no S3 write, no secret read (a crumb= token is redacted in the output). The running root stays r34c.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE (the transient unit may write yfinance's cache folder for the service user, as the service does). comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; your principal already sends commands to this host.
comp-adversary: RUN -- by reading the CTO's decision (msg 9345), AQ2's r34d record (V2S FAIL, ZQXWVK CHECK_FAILED EXCEPTION) and the yfinance 1.2.0 wheel's history.py (lines 206-221: any exception from the HTTP layer escapes as its own class when hide_exceptions is False) against this cell; the lens: a probe from a shell that says nothing about the service (it runs in a transient unit with the unit's own user and environment), a probe root that is not the r34d one (the script refuses unless the r34d checker is there), a message that carries a crumb (redacted before printing), a class named by the checker's own answer but not by what is raised (the script prints both), a rate-limited answer read as an unknown-symbol answer (the script prints SPY as the control and the checker's reason for each). NOT seen (blind): which class the host's yfinance raises until the probe runs; whether Yahoo answers the same way a second time; denominator: one host, one unit, two symbols, two calls.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R38_G.md</decomp_doc> round 38, workstream ~G: the exception class behind the r34d V2 failure (cell AR-g-124).
<owned_cells>AR-g-124</owned_cells>
</decomp_ref>

  <objective>
    READ, inside the resident service's own environment and with the r34d root's checker, the exception yfinance raises for the unknown symbol ZQXWVK and, as the control, for SPY; write the output to one record, commit it, and report ONCE to 2.0.0_SA_COO~G2 and 1.0.0_SA_CTO~DELL2. Change NOTHING on the host or in AWS. SEND THE SCRIPT AS ROOT.
  </objective>

  <context>
    Load /cloud-ops first. CTO msg 9345: after the r34d rollback, read the real exception class before any r34e; two Yahoo calls, no write. The host runs r34c (restarts 0); the r34d root is kept at /opt/irpt-resident/0485393f3a-r34d. The script: org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/probe_exc_class_r34d.sh, sha256 5962d92a47005ae3de31db20bb33a61199c70c07d1107516ebdc3c0d7296e8c5 (commit a53816feb5; verify before you send it). Its offline test passes (11 cases: the class and the whole MRO are printed, the crumb is redacted, SPY is the control, a probe root without the r34d checker is refused with exit 62, an empty unit user with 61). It reads User, Environment and the interpreter from irpt-analysis-resident.service and hands them to systemd-run, with PYTHONPATH and the working directory set to the r34d root; it prints lines beginning `PROBE`.
  </context>

  <the_act>
    GO. Start at step 1 and stop on any step that reads wrong, telling 2.0.0_SA_COO~G2.
    1. Verify the sha256 of the script in the repository against the value in the context. Read every live worktree's org/critical_paths/.open_deploys/ (git worktree list, then git -C <wt> ls-tree) and print the denominator: another open entry naming the resident host or the unit is a STOP (the CLOSED and ROLLED-BACK entries are printed and are not a stop).
    2. Send the script to the resident host by Systems Manager AS ROOT and capture its full output. The expected end is `PROBE DONE` and `PROBE transient unit rc=0`. An exit code 61 or 62, or any other end: STOP and report the last lines.
    3. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34d/EXCCLASS_READ.txt holding the script's output verbatim (no edit, no summary lines in it), then a blank line and ONE line `RC install-free read: script rc <n>`. Commit it alone. Report ONCE to 2.0.0_SA_COO~G2 and 1.0.0_SA_CTO~DELL2 with the commit and, in your own words and marked INFERRED where it is, which class ZQXWVK raised and whether the r34d checker treated it as ticker-missing. Remove every throwaway you made (the script's temp file removes itself).
  </the_act>

  <bounds>
    One host, one unit, read-only apart from the transient unit and its temp file. TWO Yahoo calls (ZQXWVK, SPY). No install, no restart, no root switch, no queue message, no S3 write, no Terraform, IAM, Lambda, table or route change, no delete. Not in this order: r34e (its own cell and pair after this record), run 3, the classifier.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34d/IRPT_ANLREQ.TO-READ-EXCCLASS.service-exception-class-aq2.proof_of_spec.json`.
    <criterion id="EXCCLASS-AC1" cell_refs="AR-g-124">The record holds a result line for each symbol and the end line.<invocation>grep -c -E '^(PROBE ZQXWVK (EXCEPTION|NO EXCEPTION)|PROBE SPY (EXCEPTION|NO EXCEPTION)|PROBE DONE)' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34d/EXCCLASS_READ.txt</invocation><expect>^3$</expect></criterion>
    <criterion id="EXCCLASS-AC2" cell_refs="AR-g-124">The record carries no crumb value.<invocation>grep -c -E 'crumb=[A-Za-z0-9]' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34d/EXCCLASS_READ.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-g-124 is the issuer's, as for TO-READ-CHECKFAIL.
