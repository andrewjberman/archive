<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-CHECKFAIL.served-checker-check-failed-aq2</id>
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
comp-blast: DECLARED-NOT-APPLICABLE -- a READ ONLY order on the resident host through Systems Manager (the channel of releases 32, 34 and the yfinance library): systemctl show, journalctl, reads of named /proc files and directory listings. No write, no install, no restart, no network call, no vendor call, no secret read, no queue message.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; your principal already sends commands to this host.
comp-adversary: RUN -- by reading the CTO's ruling (msg 9283), AQ2's own V2 output (ssm_v2_r34c_out.txt: SPY KEPT from a SHELL) and intake/yfinance_check.py against this cell; the lens: a journal window cut by the wrong timezone (the order requires --utc and prints the first and last line times and the line count of the window), a /proc environment read that prints a secret (the order prints ONLY the eleven named variables), a journal excerpt that carries a customer holding (the order prints only lines matching the exception filter and never a holdings row), a missing exception line read as proof the exception does not exist (the order says plainly when the journal carries no exception text for the window: the checker keeps only a reason code), a sandbox property read from the wrong unit (the unit is irpt-analysis-resident.service and the order prints its MainPID). NOT seen (blind): the unit's real sandbox and the journal's content until steps 1-5; denominator: one unit, one process, one window.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R35_G.md</decomp_doc> round 35, workstream ~G: the read that names the exception behind the served checker's TICKER_CHECK_FAILED (cell AR-g-120).
<owned_cells>AR-g-120</owned_cells>
</decomp_ref>

  <objective>
    READ the resident unit's sandbox, its process environment, the yfinance cache folders, the import-path wiring and the probe-window journal (10:15-10:40Z, 2026-10-16), write ONE record, commit it, and report ONCE to 2.0.0_SA_COO~G2. Change NOTHING on the host or in AWS and make NO vendor call.
  </objective>

  <context>
    Load /cloud-ops first. CTO msg 9283: run 3 is on HOLD; the served door checker returned TICKER_CHECK_FAILED in the probe window while V2 passed from a shell. The hypotheses to test first: (1) the service's import path or environment lacks pydeps; (2) yfinance's cache directory is not writable for the service user; (3) the service's network egress differs from the shell's. Code facts: intake/yfinance_check.py lets CheckerUnavailable (yfinance not importable) propagate and turns every other per-symbol exception into CHECK_FAILED with only a reason code (EXCEPTION, TIMEOUT, PUSHBACK, ERROR_FRAME), so the exception text may not be in the journal; say so if it is not. The unit is irpt-analysis-resident.service; the running root is /opt/irpt-resident/0485393f3a-r34c (r34c, MainPID 1096215 at its close; read the current one). Send each script as root or ec2-user, whichever can read the journal; both are read-only here.
  </context>

  <the_act>
    GO. Start at step 1 and stop on any step that reads wrong, telling 2.0.0_SA_COO~G2. Write each section to org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/CHECKFAIL_READ.txt under a line `SECTION <NAME>` (NAME one of UNIT, SANDBOX, PROCENV, CACHE, PYPATH, JOURNAL, in that order).
    1. UNIT: `systemctl show irpt-analysis-resident.service -p MainPID -p User -p Group -p ActiveEnterTimestamp -p NRestarts -p WorkingDirectory -p ExecStart`; print the rc of each.
    2. SANDBOX: `systemctl show irpt-analysis-resident.service -p Environment -p EnvironmentFiles -p ProtectHome -p ProtectSystem -p PrivateTmp -p PrivateNetwork -p ReadWritePaths -p ReadOnlyPaths -p InaccessiblePaths -p IPAddressAllow -p IPAddressDeny -p RestrictAddressFamilies -p NoNewPrivileges -p DynamicUser`. If an EnvironmentFiles path is named, print its NAMES only (cut each line at the first `=`), never a value.
    3. PROCENV: for the MainPID read /proc/<pid>/environ (tr '\0' '\n') and print ONLY these eleven variables with their values: HOME, USER, LOGNAME, PYTHONPATH, XDG_CACHE_HOME, TMPDIR, PATH, HTTP_PROXY, HTTPS_PROXY, NO_PROXY, YF_CACHE_DIR; print `ABSENT` for one that is not set. Also print `ls -ld` of the process's cwd (/proc/<pid>/cwd).
    4. CACHE: for the unit's User and the HOME read in step 3 (else getent passwd): `ls -ld <HOME> <HOME>/.cache <HOME>/.cache/py-yfinance` and `sudo -u <User> test -w` of each (print yes or no, or `ABSENT`); the same for $XDG_CACHE_HOME and $TMPDIR if set; and `df -Pk <HOME> /tmp | tail -2`.
    5. PYPATH: in the running root, print the lines (with line numbers) that name `pydeps` in ycharts/session/resident_session.py, ycharts/generate/resident_worker.py and the resident's launcher script that ExecStart names (grep -n pydeps; print `none` for a file with no match); and `ls -ld /opt/investor-reporting-ycharts/pydeps` with `test -r` as the User. THEN the journal: `journalctl -u irpt-analysis-resident.service --utc --since '2026-10-16 10:15:00' --until '2026-10-16 10:40:00' --no-pager`; first print the window's line count, its first and last line times; then print ONLY lines (with 2 lines of context) matching -i -E 'Traceback|Error|Exception|yfinance|checker|CHECK_FAILED|CheckerUnavailable|ErrorFrame|permission|sqlite|peewee|cache|timeout|429|403|curl|ssl|resolve|network'; never print a line naming a holding row, a file's contents or a customer name; cut a matching line at 400 characters. Write that under `SECTION JOURNAL`. If nothing matches, write `NO_MATCH window_lines=<n>`.
    6. Commit the record in one commit (the file only) and report ONCE to 2.0.0_SA_COO~G2 with the commit and, in your own words, which of the three hypotheses the record supports or refutes and what it cannot tell (the exception text, if the journal carries none).
  </the_act>

  <bounds>
    One host, one unit, read-only. No install, no pip, no import of any package, no restart, no queue message, no network call, no vendor call, no secret value (names only for an environment file), no holding or customer text in the record. Not in this order: the fix (its own pair), run 3, the classifier, the Lambdas.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/IRPT_ANLREQ.TO-READ-CHECKFAIL.served-checker-check-failed-aq2.proof_of_spec.json`.
    <criterion id="CHECKFAIL-AC1" cell_refs="AR-g-120">The record carries the six sections, each once.<invocation>grep -c -E '^SECTION (UNIT|SANDBOX|PROCENV|CACHE|PYPATH|JOURNAL)$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/CHECKFAIL_READ.txt</invocation><expect>^6$</expect></criterion>
    <criterion id="CHECKFAIL-AC2" cell_refs="AR-g-120">The process environment section prints only the eleven named variables (no other NAME=value line).<invocation>awk '/^SECTION PROCENV$/{f=1;next} /^SECTION /{f=0} f' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/CHECKFAIL_READ.txt | grep -c -E '^[A-Z_]+=' | grep -E '^([0-9]|1[01])$'</invocation><expect>^([0-9]|1[01])$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-g-120 is the issuer's, as for TO-READ-HOSTLIB.
