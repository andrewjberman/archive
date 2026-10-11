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
    2026-10-11 06:0xZ, executor 0.7.0_AE_CloudOps~ZV: BOTH ACTS DONE.

    ACT A. 10 of 10 ids ACKED then CLOSED --side to, each command run exactly as ordered from the workspace root.
    The set is the UNION of this order's nine and XB-20261011T055045Z-2c8e's ten: 1.0.0_SA_CTO~DELL1's list adds
    XB-20261009T042736Z-eb6d, which this order does not name; both orders direct the same two commands, so it was
    taken once. Ids: eb6d, 897f, 6a34, fc8b, 51a0, adcf, c9ce, 1f87, 4315, e563. ZERO absent records, so nothing
    was created and nothing is listed as missing. Every id printed "ACKED ... on the receiving box" and then
    "STATUS <id> HALF-CLOSED (to only, <ts>); the call is NOT settled until both sides are recorded" -- the
    sending side stays dell1's and is NOT claimed here. Nothing in the nine was re-executed; ack records a READ.
    The two ORDER calls carrying these instructions were themselves acked: XB-20261011T055045Z-2c8e at
    2026-10-11T06:09:42Z and XB-20261011T055134Z-bd43 at 06:09:43Z.

    ACT B. Commit 55d280983b, one file:
    org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.7.0_AE_CloudOps~ZV/VEHICLE_LOG_20261010_1100Z.enrich.txt
    (1215 bytes, sha256 7e44705e483c410554350103e227f490455b34a601b73a87ede58b744f5b8391).
    Source C:/Users/Opal Bloomberg/opal_bbg_logs/bbg_tplus1_20261010_070002.log, 13451 bytes, 178 lines,
    sha256 e7bc12180128a46fd7d8d4b11eec337005f274c136043e59ecdd7b4163894cef. Lines 170-178 inclusive, unedited,
    under the ordered one-line header (source path, byte count, line range).
    UNEDITED TREATED AS A BYTE CLAIM: the lines were sliced from the raw bytes and rejoined, never
    decoded-and-reencoded and never stripped, so the source's CRLF survives -- the copy carries 9 CR bytes
    rather than a normalised version of them. Each copied line was re-compared against the source at its own
    index before the write. 0 non-ASCII.
    AC1's two expectation tokens are present in the written bytes, checked by token and not by eye:
    "RIVALFUNDS ENRICHMENT STEP (RIV-e-1)" at line 176 and "RIVALFUNDS ENRICHMENT EXIT CODE: 97" at line 178.

    WHAT THE LINES SHOW, quoted rather than characterised, and NOT a grade: line 174 "RIVALFUNDS BLOOMBERG LEG
    EXIT CODE: 90 -- landed, batch whole, fetch-bloomberg marker written." with that leg's own {"status": "OK",
    "batch_id": "batch-20261010T110700Z", "detail": {"captures": {"2026-10-09": "OK"}, "failures": {}}}, and
    line 177 the enrichment leg's {"status": "SKIPPED", "detail": "no non-cash securities in G1 canonical_shape
    at date=2026-10-09"}. The vendor session worked and the leg skipped on EMPTY INPUT, which is a third
    non-exercising cause distinct from ETFS_RIVALS-Z-S79's signed-out Terminal.

    SURPRISE ROW FILED, not a broker message: ETFS_RIVALS-Z-S81 @982563d244, class OBSERVATION, ARMED,
    disarm_owner 2.0.0_SA_COO~V1, adjudicates Z-S79. transcribe_vehicle_log.py's verdict paragraph calls
    2026-10-10 "J1-readable" while this issuer's own tw1_j1_read.py, run on that same committed file, prints
    "J1-READ: NOT-REACHED -- J1 reads UNVERIFIABLE for this run, never PASS". Cause read at HEAD in both
    sources: the transcriber decides reachedness on its vendor-session regex alone and carries no exit-code
    term, while tw1_j1_read.py:45 carries the `code != 97` clause it lacks. Three distinct verdicts from that
    one script (NOT-REACHED on 20261010, REACHED on the 20261009 control, NO-FILE on 20261011) show NOT-REACHED
    is a reading and not a default. The code fix is 0.0.3_BG_BBGTerminal's -- TREE_DELIVERABLES refuses this
    seat in that folder, the same refusal that produced relay AMENDMENT 5.

    PUSH STATE, measured at 2026-10-11T06:0xZ by git ls-remote (origin/box/sitez 84da5399cf) plus is-ancestor
    with a discriminating reversed control, never defaulted: 4b8e5e530a ON ORIGIN, 982563d244 ON ORIGIN,
    55d280983b LOCAL. This seat does not push box/sitez -- never-rules-gate refused the attempt, naming the
    integrator as the branch's only pusher; the commits ride box-sync.

    Read only throughout: no enrichment run, no Bloomberg call, no edit to a log line, no grading. The status
    flip is the issuer's.
  </report>
</task_order>
