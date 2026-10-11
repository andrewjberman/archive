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
    (the executor's report goes here: per date the transcription hash, the printed enrichment exit code, and the .enrich.txt hash when written)
  </report>
</task_order>
