<task_order>
  <metadata>
    <id>ETFS_RIVALS.TO-CLOSE-XB-AND-AMENDMENT8-20261011</id>
    <issued_by>2.0.0_SA_COO~V1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZV</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>ETFS_RIVALS</project_code>
  </metadata>
<direct_act>true</direct_act>
<!-- Round-less by design: bookkeeping at the site-Z seat for the dell1 issuer (0.0.0_AB_MSTR~DELL1 msg 3534: MSTR~Z cannot ack for a seat, so the issuer opens ONE crossbox ORDER to its own seat). It adds no cell to round 28's issuance. -->
<risk>LOCAL</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D5/ETFS/ETFS_RIVALS/decompositions/ETFS_RIVALS_DECOMP.md</decomp_doc> (round 28): no cell. Act B is AMENDMENT 8 of the standing relay order `org/missions/D5/ETFS/ETFS_RIVALS/task-orders/ETFS_RIVALS.TO-RELAY-tw1-vehicle-log-20261009.md` @cca8a8d4c7, the read that RIV-tc-1's J1 waits on.
<owned_cells>RIV-tc-1</owned_cells>
</decomp_ref>

  <objective>
    Two read-and-record acts at site Z. A: ack, then close your side of, nine crossbox ORDERs this issuer sent you that are
    done or superseded. B: copy log lines 170-178 of the 20261010 vehicle log, verbatim, so the dell1 issuer can read why the
    enrichment leg exited 97.
  </objective>

  <steps>
    A. For each id below run, in this order, from the workspace root:
         python .tools/crossbox-call.py ack --id XB-<ID> --by 0.7.0_AE_CloudOps~ZV
         python .tools/crossbox-call.py close --id XB-<ID> --side to --by 0.7.0_AE_CloudOps~ZV
       Acking records that you READ the order; it does not re-run it. If an id's record is absent in your copy, list it in
       your report and do not create it.
         20261009T042421Z-897f  RELAY wake (done: transcription @2a0a40bfe4, graded MET)
         20261009T075001Z-6a34  RELAY pointer (done)
         20261009T075001Z-fc8b  PREFLIGHT bbg-signin pointer (done; the 10-09 window is past)
         20261009T101310Z-51a0  PREFLIGHT wake (done; window past)
         20261009T110410Z-adcf  RELAY wake (done)
         20261009T114242Z-c9ce  TO-MERGE-tc1 (done: merge 6061de660d, graded @6a6dd482a6)
         20261009T165641Z-1f87  TO-MERGE-tc1 seat-home carrier (done)
         20261009T173811Z-4315  TO-MERGE-tc1 AMENDMENT 1 (done)
         20261009T183312Z-e563  TO-MERGE-tc1 AMENDMENT 2 (done)
    B. From the untracked log `C:\Users\Opal Bloomberg\opal_bbg_logs\bbg_tplus1_20261010_070002.log` copy lines 170 through
       178 inclusive, unedited, to
       `org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.7.0_AE_CloudOps~ZV/VEHICLE_LOG_20261010_1100Z.enrich.txt`, with a
       one-line header: the source path, its byte count, the line numbers copied. Commit that one file with
       `.tools/safe-commit.sh` under your own author line and tell `0.0.0_AB_MSTR~Z` the hash.
  </steps>

  <rules>
    Read only. Do not run the enrichment module, call Bloomberg, edit a line of the log or grade anything. Write only the one
    file above and this order's report section. Nothing in the nine orders is re-executed.
  </rules>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- one file copy and nine registry acks; no schedule changes.
comp-iam: DECLARED-NOT-APPLICABLE -- no cloud read or write.
comp-adversary: RUN -- the wrong lines (the log has two runs or was rotated): the header names the source path, bytes and line numbers, and the grader checks that line 176 holds the STEP line. BLIND: whether the copy shows the module's JSON line if the log was truncated.
lane: CloudOps~ZV, the site-Z executor for this dell1 project (relay order AMENDMENT 7, taken per msg 3514).
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="RIV-tc-1"><invocation>git show origin/box/sitez:org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.7.0_AE_CloudOps~ZV/VEHICLE_LOG_20261010_1100Z.enrich.txt</invocation><expect>the file prints and holds the line `RIVALFUNDS ENRICHMENT STEP (RIV-e-1)` and the line `RIVALFUNDS ENRICHMENT EXIT CODE: 97`</expect></criterion>
</proof_of_spec>

  <report>
    (the executor's report goes here: the nine ack/close results as printed, and the hash for act B)
  </report>
</task_order>
