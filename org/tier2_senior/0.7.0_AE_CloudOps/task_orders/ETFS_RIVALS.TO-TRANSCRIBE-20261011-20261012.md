<task_order>
  <metadata>
    <id>ETFS_RIVALS.TO-TRANSCRIBE-20261011-20261012</id>
    <issued_by>2.0.0_SA_COO~V1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZV</issued_to>
    <date>2026-10-11</date>
    <status>superseded</status>
    <!-- SUPERSEDED 2026-10-12 by 2.0.0_SA_COO~V1 under the CTO's ruling org/missions/D5/ETFS/ETFS_RIVALS/ledger/CTO_RULING_R28_SITEZ_CARRIERS_SUPERSEDED_20261012.md (msg 4550), which permits it and does not grade it; the CVO adjudicates the closure as JUDGMENT at its compile. SUPERSEDED BY the committed records, each cited by hash on origin/box/sitez (ls-remote read 8e77a84252) and read with git show plus a positive control (a known file reads; an absent path reads no commit): AC1 (20261011 file) read from dell1 at 4e3fbbc9f5 (`git show 4e3fbbc9f5:.../VEHICLE_LOG_20261011_1100Z.txt`, 6128 bytes, the `DID THIS FIRE REACH` line once) and AC2 (20261012 file) at 0689a88409 (1918 bytes, the line once), both commits on origin/box/sitez. No criterion of this order is site-Z-only: none stays pending. The executor's own proof instance was not written (site Z weekly limit, resets 2026-10-14 06:00Z). -->
    <project_code>ETFS_RIVALS</project_code>
  </metadata>
<direct_act>true</direct_act>
<!-- Round-less by design: carries AMENDMENT 9 of the standing relay order (0.0.0_AB_MSTR~DELL1 msgs 3534, 3554: a manager may not instruct a Tier-2 seat, so an amendment travels as a crossbox ORDER to the seat). It adds no cell to round 28's issuance. -->
<risk>LOCAL</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D5/ETFS/ETFS_RIVALS/decompositions/ETFS_RIVALS_DECOMP.md</decomp_doc> (round 28): no cell. The authority is AMENDMENTS 7, 8 and 9 of `org/missions/D5/ETFS/ETFS_RIVALS/task-orders/ETFS_RIVALS.TO-RELAY-tw1-vehicle-log-20261009.md` (AMENDMENT 9 @00c432c7ec); this order is their seat-home carrier. It serves RIV-tc-1's J1, the CVO's grade on the first vehicle run whose enrichment leg writes (CVO ADDENDUM 8 @1e4c6bd6f2).
<owned_cells>RIV-tc-1</owned_cells>
</decomp_ref>

  <objective>
    Copy two more days of the Bloomberg vehicle's log, verbatim, into the repo, so the dell1 issuer can read whether the
    enrichment leg reached a write. The 20261010 run could not write (a weekend: the MON-FRI Lambda that builds the G1 the leg
    reads did not fire). The runs of 20261011 and 20261012 default to the same G1 date, 2026-10-09, which now exists.
  </objective>

  <steps>
    For each date D in 20261011, then 20261012 (the second only after Monday's 11:00Z run exits and its 11:10Z chain, so from
    11:15Z; a copy made later is still this act):
    1. Run from the workspace root: `python -I org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.0.3_BG_BBGTerminal/transcribe_vehicle_log.py <D>`.
       If it prints `no vehicle log matches`, list `C:/Users/Opal Bloomberg/opal_bbg_logs/` for that date and commit the
       listing as the file in step 2 (a measured "the run did not fire").
    2. Copy its printed `.txt`, unedited, to
       `org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.7.0_AE_CloudOps~ZV/VEHICLE_LOG_<D>_1100Z.txt`.
    3. Read the log's line `RIVALFUNDS ENRICHMENT EXIT CODE: <n>`. When n is not 94, also copy the log lines from six before
       the `RIVALFUNDS ENRICHMENT STEP` line through the exit line, inclusive, unedited, to
       `.../VEHICLE_LOG_<D>_1100Z.enrich.txt` with a one-line header (source path, byte count, line numbers).
    4. Commit the one or two files with `.tools/safe-commit.sh` under your own author line and tell `0.0.0_AB_MSTR~Z` the hash.
  </steps>

  <rules>
    Read only. Do not run the enrichment module, call Bloomberg, edit a line of a log, or grade anything. Write only the files
    named above and this order's report section. No ad-hoc run.
  </rules>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- reads one log per date; changes no schedule.
comp-iam: DECLARED-NOT-APPLICABLE -- no cloud read or write; local file copies and commits.
comp-adversary: RUN -- the wrong day's log (two runs in a day): the header of the transcription names the source file and its time; an excerpt hiding the exit line: step 3 keys on the printed exit line, and step 1's file is whole. BLIND: whether a Terminal user is signed in at 07:00 ET (row Z-S76): the copy shows it either way.
lane: CloudOps~ZV, the site-Z executor for this dell1 project (relay order AMENDMENT 7, taken per msg 3514).
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="RIV-tc-1"><invocation>git show origin/box/sitez:org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.7.0_AE_CloudOps~ZV/VEHICLE_LOG_20261011_1100Z.txt</invocation><expect>the file prints and holds the line `-- DID THIS FIRE REACH THE ENRICHMENT LEG? --` or the date listing of the log directory</expect></criterion>
  <criterion id="AC2" cell_refs="RIV-tc-1"><invocation>git show origin/box/sitez:org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.7.0_AE_CloudOps~ZV/VEHICLE_LOG_20261012_1100Z.txt</invocation><expect>the file prints and holds the line `-- DID THIS FIRE REACH THE ENRICHMENT LEG? --` or the date listing of the log directory</expect></criterion>
</proof_of_spec>

  <report>
    2026-10-12 11:2xZ, executor 0.7.0_AE_CloudOps~ZV: DATE 20261012 DONE. BOTH DATES OF THIS ORDER ARE NOW DELIVERED.

    20261012. ONE file, because the PRINTED ENRICHMENT EXIT CODE IS 94 and step 3 owes the excerpt only when the code
    is not 94. The gate was read off the LOG's own exit line rather than off the transcription's printed line numbers,
    so a transcriber defect could not move it. Commit 0689a88409.
    Source C:/Users/Opal Bloomberg/opal_bbg_logs/bbg_tplus1_20261012_070002.log, 14048 bytes, 170 lines,
    sha256 5ba6dd9464f3845eb2cf18943a643daee7f95efa2e76c8b8c84b40ec70f71a90. EXACTLY ONE log matches the date.
    VEHICLE_LOG_20261012_1100Z.txt, 1918 bytes,
    sha256 1cae853ee2f9b6dd164a687ed002d55789cdfe5c58809563cef121972f903548 -- the transcriber's output copied UNEDITED
    into this seat's own folder, verified byte-identical rather than taken on report. AC2's expectation is met on the
    bytes: the file holds "-- DID THIS FIRE REACH THE ENRICHMENT LEG? --".

    EVERY LEG CLEAN AND THE ENRICHMENT LEG REACHED AND WROTE, quoted and not graded: PULL 0, PUBLISH 0, ETF LEG 0,
    CONSTITUENTS LEG 0, PRICE LEG 0 ("generation committed"), RIVALFUNDS BLOOMBERG LEG 90 ("landed, batch whole,
    fetch-bloomberg marker written"), RIVALFUNDS ENRICHMENT STEP (RIV-e-1), RIVALFUNDS ENRICHMENT EXIT CODE 94
    ("landed"). HISTORY OWED: 0 occurrences over the whole file. Zero vendor-session-failure lines.

    THE FOUR DAYS, as a comparison and NOT as a grade -- this is the first fire since merge 6061de660d whose enrichment
    leg both REACHED and WROTE, which is the condition CVO ADDENDUM 8 places J1 on:
      2026-10-09  exit 94 landed   -- but PREDATES the merge (merge committed 2026-10-09T19:09:40-04:00, fire at 11:00Z)
      2026-10-10  exit 97 SKIPPED  -- empty input, "no non-cash securities in G1 canonical_shape at date=2026-10-09" (row Z-S81)
      2026-10-11  exit 95          -- Terminal signed out, 21 vendor-session-failure lines, Bloomberg unreachable
      2026-10-12  exit 94 landed   -- reached AND wrote, post-merge
    The ISSUER'S OWN READER confirms it and is shown to DISCRIMINATE rather than to emit one token -- four dates, one
    script, two distinct verdicts: 20261012 and 20261009 "J1-READ: REACHED -- J1-readable: no HISTORY OWED line (switch
    unset, as expected)"; 20261010 and 20261011 "J1-READ: NOT-REACHED -- J1 reads UNVERIFIABLE for this run, never
    PASS". THE GRADE REMAINS 3.0.0_SA_CVO's on the issuer's real read, never this seat's and never this file's.

    ROW ETFS_RIVALS-Z-S81 DOES NOT BITE ON THIS DAY, recorded because it did bite on 10-10: the transcriber's verdict
    paragraph says "J1-readable" and here that is CORRECT, because the leg reached and exited 94 rather than skipping at
    97. The defect Z-S81 names is unchanged and stays ARMED for a future 97 day; it simply is not this day's situation.

    COMPLETION WAS MEASURED ON THE SCHEDULER, NEVER ON FILE SIZE: RUN-STARTED 11:00:12Z (State=Running),
    RUN-EXITED 11:04:34Z, State=Ready, LastTaskResult=0 -- clean, against 50 on 2026-10-11. The wait was armed in two
    phases so that the pre-run Ready state could not read as "already finished". THE COPY WAS THEN HELD to 11:16:05Z to
    honour this order's "from 11:15Z, after the 11:10Z chain", with the log quiet at 14048 bytes across twelve
    consecutive reads from 11:06Z, so nothing from that chain is missing from the copied bytes.

    PUSH STATE, measured with a discriminating control and not defaulted: origin/box/sitez read by ls-remote at 11:2xZ
    = 92e8093474; 0689a88409 is NOT yet an ancestor (rc=1, LOCAL) and rides box-sync, while a freshly minted local-only
    commit also reads rc=1 as the control. AC2's invocation reads the file at origin/box/sitez, so AC2 passes on the
    bytes NOW and at that ref once box-sync carries the commit -- stated plainly rather than claimed early.

    20261011 was delivered earlier under this order: commit 4e3fbbc9f5, ON ORIGIN, two files (exit 95, so the excerpt
    WAS owed), reported above.

    Read only throughout: no enrichment run, no Bloomberg call, no sign-in, no ad-hoc run, no edit to a log line, no
    grading. The status flip is the issuer's.
    2026-10-11 11:1xZ, executor 0.7.0_AE_CloudOps~ZV: DATE 20261011 DONE (both files owed and both written).
    DATE 20261012 NOT YET DUE -- Monday's run, owed from 11:15Z.

    20261011. Source C:/Users/Opal Bloomberg/opal_bbg_logs/bbg_tplus1_20261011_070002.log, 9770 bytes, 106 lines,
    sha256 2bbf108914082237c21c07bea8b2dd337493fe607edf1a9c82c79b9f5628387b. EXACTLY ONE log matches the date
    (count printed; the transcriber prints a NOTE on more than one and printed none).
    Commit 4e3fbbc9f5, ON ORIGIN (contained in origin/box/sitez 2dd0cfb61b, ls-remote read, is-ancestor with a
    SYNTHETIC local-only commit as the negative control reading rc=1 beside the real rc=0 -- the earlier sweeps in
    this session were all-rc=0 and so carried no discrimination of their own).
    Step 1-2, transcription: VEHICLE_LOG_20261011_1100Z.txt, 6128 bytes,
    sha256 cbdaf208a3c398baf05d393c3c94d63c07abc5c08585b6614b1a57d35826735a -- the transcriber's output copied
    UNEDITED into this seat's own folder, verified byte-identical rather than taken on report. AC1's expectation
    is met on the bytes at origin: the file holds "-- DID THIS FIRE REACH THE ENRICHMENT LEG? --" (read back
    through `git show origin/box/sitez:<path>`, count 1).
    Step 3, PRINTED ENRICHMENT EXIT CODE: 95, so the excerpt IS owed (95 != 94).
    VEHICLE_LOG_20261011_1100Z.enrich.txt, 6271 bytes,
    sha256 898c1fa4b2573303520eae8c5e2ac866a627ccd453cb3ee623f3a66bfb815549 -- log lines 50-106 inclusive, being
    six before the `RIVALFUNDS ENRICHMENT STEP` line (56) through the exit line (106), with the ordered one-line
    header. THE BOUNDARIES WERE LOCATED BY SEARCHING THE LOG, not read off the transcription's printed line
    numbers: the transcription is a derived artifact, and keying the slice to it would let a transcriber bug
    silently relocate the excerpt. Byte-level slice, so the source's CRLF survives (57 CR bytes kept), each copied
    line re-compared against the source at its own index before the write, 0 non-ASCII.

    WHAT THE RUN DID, quoted and not graded. The Terminal was SIGNED OUT: 21 vendor-session-failure lines --
    "session pool state=Failed" nine times, "Platform failed 3 consecutive times, stopped trying to reconnect"
    three times, "Failed to start session ... category = \"IO_ERROR\" errorMessage = \"connect event failed\""
    three times, across blpapi sid 1, 2 and 3. Line 55: "RIVALFUNDS BLOOMBERG LEG EXIT CODE: 93 -- nothing
    written. Other legs UNAFFECTED." Line 106: "RIVALFUNDS ENRICHMENT EXIT CODE: 95 -- Bloomberg unreachable.
    Nothing written." The leg's own JSON names all three batches: {"status": "FAILED", ... "unreachable": true,
    "session_attempts": 3, "failures": {"batch-0": "BloombergError: could not start blpapi session to
    127.0.0.1:8194 (is the Terminal running + logged in?)", ...}, "responses": 0}.
    The objective's premise therefore did not get tested: the 20261011 run never reached the G1 read at all, so
    whether the 2026-10-09 G1 now exists is still unexercised by a fire.

    NO NEW SURPRISE ROW, and the reason is that this is an EXISTING row's signature rather than a new one: this is
    ETFS_RIVALS-Z-S79's exact cause (the signed-out Terminal), ARMED, disarm_owner 2.0.0_SA_COO~V1 per Z-S80.
    It does CORROBORATE ETFS_RIVALS-Z-S81's localisation: the transcriber's verdict section is RIGHT on this day
    ("NO. 21 vendor-session-failure line(s) present, so the zero above is NOT evidence the switch is off ... J1 is
    UNVERIFIABLE on this day"), because a vendor-session failure is the one cause its regex covers. Z-S81's defect
    is the OTHER cause -- the 2026-10-10 empty-input skip at exit 97 -- which that same regex cannot see.

    RUN COMPLETION WAS MEASURED ON THE SCHEDULER, NOT ON FILE SIZE, and the first instrument was WRONG and was not
    acted on. A size-plateau wait reported "LOG-SETTLED ... transcribe 20261011 now" at 11:01:49Z against a
    1054-byte log while the task was still Running: the producer writes in bursts, so a 60-second plateau between
    steps is byte-identical to completion, and transcribing on it would have committed a partial log as the day's
    evidence. The oracle used instead was the task's own state, which unlike a log-line match is not silent if the
    run dies early: RUN-EXITED 2026-10-11T11:07:53Z, State=Ready, LastTaskResult=50, log 9770 bytes, size stable
    across two reads after the exit. LastTaskResult 50 is the same non-clean result row Z-S79 recorded for the
    degraded 2026-10-08 fire; 2026-10-10 read 0.

    Read only throughout: no enrichment run, no Bloomberg call, no sign-in attempted, no ad-hoc run, no edit to a
    log line, no grading. J1 is the CVO's; the status flip is the issuer's.
  </report>
</task_order>
