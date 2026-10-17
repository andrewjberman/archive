<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-PACKAGER-RETAINED.one-live-read-of-the-retained-for-retry-lines-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-17</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ58</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-397</owned_cells>
<decomp_context>Round 43, cell AR-y-397: one read-only live read of the resident journal's `retained_for_retry` lines, the closed-code log the poll prints when the packager raises and leaves the commentary-ready message in its queue (ycharts/generate/resident_main.py:67-79 and 32-35), because the corrected reads of AR-y-396 show: both queue URLs and the packager are bound, 0 package outcomes in 7 days, and the commentary-ready queue saw 2 sends, 4 receives and 0 deletes (three receives on 2026-10-14, then the dead letter).</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order: one journal read on the resident host; no write, no restart, no queue receive, no deploy.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- your principal's existing read; a DENIED read prints DENIED.
comp-adversary: RUN -- by reading resident_main.py:32-35 and :67-79 against the journal: the line format is closed (`IRPT_RESIDENT_PACKAGE retained_for_retry class=<ClassName> code=<UPPER_SNAKE or ->` and `IRPT_RESIDENT_POLL retained_for_retry class=... code=...`), and carries no exception text; the lens: copying any other journal line (forbidden), a count without its window and total, the wrong literal (the earlier `PackagerRefused` and `IRPT_RESIDENT_PACKAGE outcome=` counts read 0 and are not the log of a raise). NOT seen (blind): the journal's unit name (your earlier reads knew it); denominator: one read.
</preflight>

  <objective>
    Print the closed-code reason the packager raised on each commentary-ready message it polled, so the issuer can say which refusal stops the chain before the PDF is retained.
  </objective>

  <context>
    Load /cloud-ops first. Your reads of 2026-10-17 (msgs 10639 and the A_RESIDENT_PACKAGER.txt file) show the running resident is release irpt-resident-0485393f3a-r34k at pin 1ad8bd8c1bb8, both queue URLs and `packager` are set in its bindings with matching queue names, 29,928 journal lines in the 7-day window, 0 `IRPT_RESIDENT_PACKAGE outcome=` lines, and the commentary-ready queue's sums: sent 1 on 10-10 and 1 on 10-14, received 1 on 10-10 and 3 on 10-14, deleted 0. A raise from the packager that is not a message-shape refusal or an ATTACHED outcome leaves the message in the queue and prints a `retained_for_retry` line (ycharts/generate/resident_worker.py:1020-1023, 1066-1074; resident_main.py:75-79).
  </context>

  <the_act>
    GO now. Never print a journal line other than the lines this step names; never print a value, a request id, a URL or a message body.
    1. R1: from the resident service's journal for the last 8 days (the same unit as before), print the window (first and last timestamp) and the total lines scanned, then COUNTS of the lines that begin (after the journal timestamp and host fields) with `IRPT_RESIDENT_PACKAGE retained_for_retry` and of the lines that begin with `IRPT_RESIDENT_POLL retained_for_retry`, then EVERY `IRPT_RESIDENT_PACKAGE retained_for_retry` line in full as `<UTC timestamp to the minute> class=<ClassName> code=<CODE|->` (at most 40; if more, print the first 20 and the last 20 and the total). Line group: `R1 window=<first>..<last> scanned=<n> package_retained=<n> poll_retained=<n>` followed by one line `R1L <UTC to the minute> class=<ClassName> code=<CODE|->` per package line.
    2. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_retained/A_PACKAGER_RETAINED.txt with the R1 line, the R1L lines, and a closing line `READS-DONE 1 of 1 answered` (or `R1 DENIED <what>` / `R1 NOT-RUN <why>` and `READS-DONE 0 of 1 answered`). Report ONCE to 2.0.0_SA_COO~Y2 with the file path and the R1 line plus the R1L lines. No ledger: nothing is deployed.
  </the_act>

  <bounds>
    Reads only. No SQS receive, delete, purge or send; no restart, stop or start; no write to any table, bucket or host file. Only the closed `retained_for_retry` lines are printed from the journal; everything else is counted.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_retained/IRPT_ANLREQ.TO-READ-PACKAGER-RETAINED.one-live-read-of-the-retained-for-retry-lines-ib2.proof_of_spec.json`.
    <criterion id="RPR-AC1" cell_refs="AR-y-397">The R1 line and the closing line are present, answered, denied or marked not run.<invocation>grep -c -E '^R1 (window=|DENIED |NOT-RUN |ERROR )|^READS-DONE [0-9]+ of 1 answered$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_retained/A_PACKAGER_RETAINED.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="RPR-AC2" cell_refs="AR-y-397">Every other line is a closed R1L line or one of the two above (the leak control): no line outside those forms.<invocation>grep -c -v -E '^R1 (window=|DENIED |NOT-RUN |ERROR )|^R1L [0-9T:-]+Z? class=[A-Za-z_]+ code=([A-Z][A-Z0-9_]*|-)$|^READS-DONE [0-9]+ of 1 answered$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_retained/A_PACKAGER_RETAINED.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-397 is the issuer's, as for AR-y-395 and AR-y-396.
