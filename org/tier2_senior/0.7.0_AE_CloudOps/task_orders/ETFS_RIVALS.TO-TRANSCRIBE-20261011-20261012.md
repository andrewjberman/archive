<task_order>
  <metadata>
    <id>ETFS_RIVALS.TO-TRANSCRIBE-20261011-20261012</id>
    <issued_by>2.0.0_SA_COO~V1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZV</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
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
