# CG-x-8 -- FWD-8 EXERCISED: the operator status read taken on a REAL MORNING reads YES with a time, and the same read taken against a night known not to have run reads NO -- both recorded, they differ, and nothing was rerun to obtain either

**TO:** `NFRA_CLDGRPH.TO-CG-D-11` (cell CG-x-8, closing pass for FWD-8) · **worker:** `0.9.0_WK_NFRA_CLDGRPH~3`
**branch:** `wk-CLDGRPH-d11` · **base:** `76c5f90155` · **worked:** 2026-09-05 13:44Z -> 14:5xZ, worktree `C:/Users/AndrewBerman/Desktop/wk-CLDGRPH-d11`

## THE HEADLINE

**The three mechanical criteria PASS by output and the order is FLIPPED.** The morning read, taken at
2026-09-05T14:01:49Z -- eleven hours and fifty-nine minutes after the 02:00Z boundary of the calendar day it
was taken on -- prints `REFRESHED LAST NIGHT: YES at 2026-09-05T02:23:22.179104+00:00`. The same read pointed
at the plant prints `REFRESHED LAST NIGHT: NO (last full: 2026-09-02T20:15:00.000000+00:00)`. They differ on
the deciding line, in the verdict token and in the time.

**The YES matches TO-CG-D-9's night exactly, and it was not read from D-9 -- it was read from the estate and
then compared.** `MORNING_READ_VINTAGE=2026-09-05T02:11:10.919000+00:00` and the built_at in the answer is
`2026-09-05T02:23:22.179104+00:00`; D-9 recorded `NIGHT_VINTAGE=2026-09-05T02:11:10.919000+00:00` and
`night_built_at=2026-09-05T02:23:22.179104+00:00` (`CG-x-2.schedule-exercised.result.md`:168,173 at this
HEAD). Same vintage, same built_at, two seats, two instruments, one night. No later full nightly has run,
so this is CG-x-2's night and not a successor's.

**THE ONE THING WORTH AN OPERATOR'S ATTENTION, and it is a strength of the answer rather than a defect:**
the pointer's CURRENT vintage this morning is `2026-09-05T12:54:31.241426+00:00`, written by
`incremental_updater` in `incremental` mode -- the served artifact has moved four vintages PAST the night.
The "did it refresh last night" answer is unaffected, because `_last_full_before_boundary` keys on a
`producer.mode == "full"` manifest whose `writer_id == "derive_runner"` landing inside `[boundary,
boundary+6h)`, not on whatever the pointer happens to name now (`graph_status_cli.py`:329-382). An operator
asking the FWD-8 question in the middle of a busy day still gets the night's answer. A naive
newest-vintage implementation would have answered with the 12:54 incremental and been wrong about the
night while looking right.

**NOTHING WAS RERUN, and that is measured on the two instruments that can see it rather than on the one the
order named.** Process table: 0 of 31 rows before the read and 0 of 28 after, for
`kuzu_nessie_load|derive_runner|projection_worker`, taken with the `grep -v grep` discipline on a snapshot
whose own rc and row count are printed -- and with a POSITIVE CONTROL returning 27 on a pattern that IS
running, so the zero is an absence and not a dead arm. Pointer: `POINTER_ETAG_BEFORE` and
`POINTER_ETAG_AFTER` are both `"4cc4f17a96e5bc5d6520a5aba7e40cf8"`, strictly equal, so no attribution arm
was needed. The plant's manifest sha256 is byte-identical before and after the missed read.

**THREE ROWS FILED, all three on the negative control the order named, none of them on the readings:**
`NFRA_CLDGRPH-W3-S3` (the `comp-find ... org/mcp/agent_telemetry` control scans ZERO files from a worktree --
the directory is gitignored -- so its "0 hits" is a NO MEASUREMENT that reads as the expected clean zero),
`NFRA_CLDGRPH-W3-S4` (a worker DOES write telemetry; the hook resolves the serial from a session-id map that
still names slot `~2`, so this worker's calls and its parent's are being written live into `~2`'s file, 1,342
rows, one session id, 100 percent `serial_source: session-id-keyed`), and `NFRA_CLDGRPH-W3-S5` (a telemetry
row carries no command text by an explicit privacy invariant, so the invocation log cannot discriminate a
read from a rerun in either direction). The substance the control was meant to establish is established --
by the process table and the pointer ETags -- and the telemetry question was answered anyway with a second
instrument: 0 rows for this serial across 160 files and 426,009 lines, with positive controls of 30,522 and
65,114 proving the scan finds serials that are present.

**NOTHING IN THE REAL WORLD WAS TOUCHED.** No schedule stopped, no rule disabled, no marker written, no
pointer moved, no derive/rebuild/engine run, no AWS mutation, no S3 write. Every AWS call in this pass is a
`head-object` or a `get-object`. The night that did not run is a LOCAL FIXTURE, and whether that fixture
stands for a real missed night is D11-AC4, which is `3.0.0_SA_CVO`'s to grade and is recorded below with no
verdict.

## THE RECORD

```json
{
  "morning_wall_clock": "2026-09-05T14:01:49Z",
  "morning_read": "REFRESHED LAST NIGHT: YES at 2026-09-05T02:23:22.179104+00:00",
  "morning_read_vintage": "2026-09-05T02:11:10.919000+00:00",
  "morning_read_boundary": "2026-09-05T02:00:00+00:00 (+6h window; checked 1 manifest)",
  "morning_is_a_real_morning": "the read was taken at 14:01:49Z on 2026-09-05, 11h59m AFTER that calendar day's own 02:00Z nightly boundary, with the wall clock printed by the script itself (date -u +%FT%TZ); the boundary is not the worker's opinion -- graph_status_cli.py:60-61 derives it from cron(0 2 * * ? *) at infra/aws/terraform/globgrph/item2a.tf:439",
  "night_vintage_from_D9": "2026-09-05T02:11:10.919000+00:00, built_at 2026-09-05T02:23:22.179104+00:00, writer_id derive_runner, mode full, joined 3 of 3 on nodes_snapshot_id / edges_snapshot_id / nessie_commit_hash -- org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/CG-x-2.schedule-exercised.result.md:102,168,173,178 at HEAD 76c5f90155",
  "morning_read_matches_D9_night": "YES, exactly and on both fields: the morning answer's built_at 2026-09-05T02:23:22.179104+00:00 == D-9's night_built_at, and the vintage it names 2026-09-05T02:11:10.919000+00:00 == D-9's NIGHT_VINTAGE. It is CG-x-2's own night and not a later one: no second full/derive_runner manifest exists in the 02:00-08:00Z window (checked_manifests=1, and the tool returns on the FIRST full it finds scanning the window ascending, so the count of 1 means the window held exactly one candidate vintage at or after the boundary that it needed to open).",
  "missed_read": "REFRESHED LAST NIGHT: NO (last full: 2026-09-02T20:15:00.000000+00:00)",
  "missed_read_vintage": "2026-09-02T20:00:00.000000+00:00",
  "the_two_readings_differ": "on the verdict token (YES vs NO), on the clause shape (`at <time>` vs `(last full: <time>)`) and on the time itself (2026-09-05T02:23:22.179104+00:00 vs 2026-09-02T20:15:00.000000+00:00). Same tool, same code path, same boundary (2026-09-05T02:00:00+00:00 in both), one environment variable different.",
  "plant_description": "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/plant/ -- a pointer+manifest pair committed with TO-CG-D-4 and NOT re-planted by this order. current.json names vintage 2026-09-02T20:00:00.000000+00:00 with manifest_sha256 a46a35809dab2e63c57210023bf145275145c19ef946bf4fd75a77473f11d4bf; the manifest under that vintage carries 14 fields in a real manifest's shape (age_line, artifact{expected_publish_set_size_band_bytes, files, format, total_size_bytes}, built_at, committed_at, edge_count, edges_skipped_missing_endpoint, edges_snapshot_id, nessie_commit_hash, node_count, nodes_snapshot_id, producer{engine, engine_version, mode, source_commit}, schema_version, vintage, writer_id), writer_id derive_runner, producer.mode full, built_at 2026-09-02T20:15:00.000000+00:00. It is 'known not to have run' BY CONSTRUCTION: its newest full vintage predates today's 02:00Z boundary by 2 days 6 hours, so no manifest exists in the window and the tool takes the did-not-run branch.",
  "plant_sha256_verified_before_and_after": "a46a35809dab2e63c57210023bf145275145c19ef946bf4fd75a77473f11d4bf both times -- and the pointer's CLAIMED manifest_sha256 equals the manifest's ACTUAL sha256, which is what makes the answer a NO rather than an UNVERIFIABLE: _read_manifest_verified refuses on a mismatch and _projection_rows would then print 'REFRESHED LAST NIGHT: UNVERIFIABLE (...)' (graph_status_cli.py:282-296, 400-427)",
  "procs_before_after": "0 / 0 for pattern 'kuzu_nessie_load|derive_runner|projection_worker', over ps -ef snapshots of 31 and 28 rows (the denominator), taken with grep -v grep on a snapshot captured into a variable. POSITIVE CONTROL on the same probe, same run: 27 matches for pattern 'bash', so the probe returns non-zero when the truth is non-zero. THE TRAP, measured rather than asserted: a bare `ps -ef | grep -c -E '<pattern>'` typed at an interactive shell returned 2 against this same pattern while the truth was 0 -- the wrapper shell's own command line carries the pattern text and ps -ef renders full argv, so the probe counted itself; the disciplined form returned 0 in the same second.",
  "pointer_etags": "before \"4cc4f17a96e5bc5d6520a5aba7e40cf8\", after \"4cc4f17a96e5bc5d6520a5aba7e40cf8\", strictly equal -> POINTER_ETAG_STRICT_DIFFERS=false and POINTER_MOVED_ACROSS_READS=false with no attribution arm required. Both reads printed their rc (0) and their raw bytes; the shim's trailing CR was stripped explicitly (the raw od -c dump in the transcript shows the CRLF the shim emits).",
  "telemetry_rows_for_serial": 0,
  "telemetry_rows_for_serial_provenance": "MEASURED, but NOT by the invocation the order names -- see rows NFRA_CLDGRPH-W3-S3 and W3-S4. The named invocation scans 0 files from a worktree because org/mcp/agent_telemetry/ is gitignored (.gitignore:261). This 0 is from an in-process byte scan of all 160 files in C:/Users/AndrewBerman/Desktop/ajb_workspace/org/mcp/agent_telemetry, denominator 426,009 lines, positive controls 30,522 hits for 0.0.0_AB_MSTR and 65,114 for 2.0.0_SA_COO. It is a true zero FOR THE STRING and it is NOT evidence that this worker wrote no telemetry: 1,342 rows of this session's acts exist under the sibling name 0.9.0_WK_NFRA_CLDGRPH~2 (W3-S4).",
  "nothing_was_rerun_evidence": "(i) process table 0/31 and 0/28 with a live positive control; (ii) pointer ETag identical across the read; (iii) the plant's bytes identical across the missed read; (iv) the tool itself has no rebuild path -- comp-graph status is a pull read and graph_status_cli.py's status command performs only S3/local GETs (the status row for the projection literally prints rebuild: 'none -- the estate refreshes itself (FWD-2)'); (v) the invocation log, offered by the cell as A negative control, is NOT counted here because it cannot discriminate -- W3-S5.",
  "rows_filed": ["NFRA_CLDGRPH-W3-S3", "NFRA_CLDGRPH-W3-S4", "NFRA_CLDGRPH-W3-S5"],
  "real_world_writes": "NONE. No schedule/rule touched, no live pointer or marker written, no derive/rebuild/engine invoked, no AWS mutation, no S3 write. AWS verbs used in this pass: s3api head-object (x2 per morning run), and boto3 GetObject/ListObjectsV2 inside the status tool."
}
```

## CRITERIA, EACH WITH ITS INVOCATION AND ITS DECIDING LINE

| id | verdict | invocation (run under `timeout 120`) | deciding output | denominator |
|---|---|---|---|---|
| D11-AC1 | **PASS** | `bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/morning.sh \| grep -E '^MORNING_READ='` | `MORNING_READ=REFRESHED LAST NIGHT: YES at 2026-09-05T02:23:22.179104+00:00` | 1 of 1 morning read, script rc 0, taken 2026-09-05T14:01:49Z after that day's 02:00Z boundary |
| D11-AC2 | **PASS** | `bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/missed.sh \| grep -E '^MISSED_READ='` | `MISSED_READ=REFRESHED LAST NIGHT: NO (last full: 2026-09-02T20:15:00.000000+00:00)` | 1 of 1 missed-night read, script rc 0, same code path, one env var different |
| D11-AC3 | **PASS** | `bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/morning.sh \| grep -E '^(PROCS\|POINTER_MOVED_ACROSS_READS)='` | `PROCS=0` then `POINTER_MOVED_ACROSS_READS=false` | procs 0 of 31 / 0 of 28 ps rows with a 27-match positive control; pointer 2 of 2 ETag reads at rc 0 and equal |
| D11-AC4 | **RECORDED, NO VERDICT** (`judgment="true"`) | a reading act | the reading is below | graded by `3.0.0_SA_CVO` at L9 |

### THE CAN-FAIL PROOF -- every arm shown returning the OTHER answer

A control whose failure mode is silence licenses the arm above it (row `NFRA_CLDGRPH-W1-S18`), so each arm
was exercised on an input that must produce the opposite result. `bash morning.sh --selftest`, verbatim:

- `SELFTEST_COMPARATOR_SAME=false` / `SELFTEST_COMPARATOR_DIFF=true` -- the SAME pure function that produces
  `POINTER_MOVED_ACROSS_READS` returns `true` when fed two different ETags. The false in the criterion is a
  measurement, not a constant.
- `SELFTEST_PROCS_POSITIVE_CONTROL=24` on pattern `bash`, `ps_rows=29` -- the proc probe returns non-zero on
  a pattern that IS running.
- **D11-AC2 IS ITSELF THE CAN-FAIL ARM FOR THE READ:** the same binary, the same code path, produces `NO`
  where the morning produces `YES`. The status tool is not wedged on one answer.
- **AND A THIRD OUTCOME EXISTS AND IS NOT BEING PRODUCED HERE:** the tool has an `UNVERIFIABLE` branch
  (`graph_status_cli.py`:485-486, taken when the boundary scan cannot list or read a manifest, and :419
  when the straddle read of the pointer/manifest fails). Both readings avoided it -- one over S3 with `read_method: boto3`, one over the
  fixture with `read_method: local-file` -- so neither YES nor NO here is an error state wearing a verdict's
  clothes.

### D11-AC4 -- the reading (a reading act; NO verdict; `3.0.0_SA_CVO` grades this at L9)

PRD acceptance 8 says: *"'Did it refresh last night' is a read, not a rerun. An operator gets a plain yes or
no with a time, and a missed night looks different from a completed one."*

**On "a plain yes or no with a time":** delivered on both arms, in one line each, with the time in both.
The YES carries the built_at of the full nightly; the NO carries the built_at of the newest full BEFORE the
boundary, which is the operationally useful number (how far back the last real refresh was) rather than a
bare negative. The word "plain" is met in the deciding line; an operator running `comp-graph status` also
gets 40 lines of surrounding context, and the FWD-8 answer is one of them, labelled.

**On "a missed night looks different from a completed one":** they differ in three independent places, not
one -- token, clause shape, and time. That matters because a single-token difference could be produced by a
stringly-typed default.

**On whether the plant stands for "a night known not to have run", which is the question the issuer put:**
what I can say from measurement, and where the reading has to be someone else's.

1. **The plant exercises the SAME code path a real miss would.** `_last_full_before_boundary` computes the
   boundary from the wall clock, lists vintages, finds none inside `[boundary, boundary+6h)`, then walks
   backwards for the newest `full` and returns `ran: False`. The plant reaches that branch by having no
   in-window vintage at all. A real missed night reaches the same branch the same way -- an empty window --
   and the intervening incrementals a real estate would carry do not change the branch, because the window
   scan requires `producer.mode == "full"` AND `writer_id == "derive_runner"` and an incremental fails both.
   **The limit of that claim, stated:** a real miss would have a non-empty window of incremental vintages to
   scan and reject (up to `_MAX_WINDOW_GETS` = 12 manifest GETs); the plant's window is empty, so the
   REJECTION half of the window scan is not exercised by this fixture. What is exercised is the branch that
   produces the answer.
2. **The plant is realistic on shape, not merely on verdict.** 14 fields, the same field names and nesting
   as the live manifest read minutes earlier over S3 (compare the two `projection.current` blocks in the
   transcripts: identical field list, differing only in values), `IN-BAND` band status, `writer_id`
   `derive_runner`, `producer.mode` `full`. Its `manifest_sha256` verifies, so it passes the straddle
   contract rather than short-circuiting it.
3. **The counterfactual the issuer names is the real constraint and I did not test around it.** A real miss
   cannot be obtained without a production change -- disabling `events-rule/opal-globgrph-derive-runner-nightly`
   or stopping a task -- which is a NEVER on this order's face and outside any worker's lane. I did not do
   it and I do not think it should be done to satisfy a criterion.
4. **What a grader may reasonably hold against the fixture, said by the seat that built the reading:** the
   plant proves the CODE answers NO when no full nightly landed in the window; it does not prove the ESTATE
   would present that NO to an operator during a real miss, because in a real miss the pointer would also
   be stale, the incrementals may or may not still be running, and the reader would be talking to S3 rather
   than to a local directory (`read_method: local-file` in the NO transcript is the visible tell that the
   arm ran against a fixture, and it is printed rather than hidden). The strongest honest statement is:
   the DECISION FUNCTION is exercised on a night that did not run; the DELIVERY PATH for that answer under
   a real miss is inferred from the shared code, not observed.
5. **On the other half of the criterion -- whether the morning read's time matches D-9's night:** it does,
   exactly, on both the vintage and the built_at, and the match was made by comparing two independently
   produced numbers rather than by carrying D-9's forward. This is the half I would rate strongest.

## TRANSCRIPTS

### morning.sh -- the real morning read, verbatim (2026-09-05T14:01:49Z)

Run under `timeout 120`, script rc 0. The primary transcript.

```text
==============================================================================
MORNING READ -- TO-CG-D-11 / CG-x-8 / 0.9.0_WK_NFRA_CLDGRPH~3
READS ONLY: HEAD/GET on S3, one status read, one process snapshot. Nothing rerun.
==============================================================================
WALL_CLOCK_UTC=2026-09-05T14:01:49Z
NIGHTLY_BOUNDARY_HOUR=02:00Z  (graph_status_cli.py:60, cron(0 2 * * ? *))
MORNING_TEST=the read is taken AFTER today's 02:00Z boundary on the calendar day it runs

--- POINTER ETAG BEFORE (rc printed; a failed read says so and is never a number) ---
  etag_read[before] rc=0
  etag_read[before] raw_bytes=0000000   "   4   c   c   4   f   1   7   a   9   6   e   5   b   c   5 0000020   d   6   5   2   0   a   5   a   b   a   7   e   4   0   c   f 
  etag_read[before] stderr=<empty>
  etag_read[before] value="4cc4f17a96e5bc5d6520a5aba7e40cf8"

--- PROCESS TABLE BEFORE (grep -v grep discipline; denominator printed) ---
  pattern='kuzu_nessie_load|derive_runner|projection_worker'  matches=0  ps_rows(denominator)=31

--- POSITIVE CONTROL: the proc probe can return NON-ZERO (a zero is an absence, not a dead arm) ---
  pattern='bash'  matches=27  ps_rows(denominator)=30

--- THE READ: bash .tools/comp-graph status (whole output, verbatim) ---
COMP-GRAPH STATUS  (query-vs-rebuild freshness)
  contract: org/modules/graph/graph-call-manifest.yaml

LOCAL TRACE LAYER (.comp-graph/)
  graph                MISSING      absent             no-TTL    trace graph (comp-trace/comp-blast/comp-diff/comp-xref)  (build: comp-build)
                       predicate: content-SHA drift per indexed node (no TTL on the default path)
                       evaluated: no cached graph -- run comp-build
  baseline             MISSING      absent             no-TTL    xref baseline snapshot (comp-xref)  (build: comp-xref --save)
  platinum.*           MISSING      absent             TTL 300s  comp-platinum caches (per-firm, keyed by --firm)  (build: comp-platinum page <C> --firm <F>)

CLOUD / CROSS-LAYER (projection/current.json, straddle-verified)
  projection.current   PRESENT      built 65m ago      no-TTL    cloud Kuzu projection (projection/current.json, straddle-verified)
                       vintage: 2026-09-05T12:54:31.241426+00:00
                       age_line: Built from the estate as of 2026-09-05 12:54:31 UTC.
                       built_at: 2026-09-05T12:55:56.746109+00:00
                       nessie_commit_hash: 4e7af7e55f82661fb41bbf73825466bdd50d94da5fb6edeefbe842ac8fcd1c76
                       nodes_snapshot_id: 8664091868311394101
                       edges_snapshot_id: 8760077255054959316
                       writer_id: incremental_updater
                       producer.mode: incremental
                       producer.source_commit: 5644fee152600506259a8869f7067e89c8e6c0f2
                       node_count: 27292
                       edge_count: 58771
                       edges_skipped_missing_endpoint: 386
                       artifact_bytes: 34832384
                       band_status: NO-BAND
                       read_method: boto3
  projection.last_night YES          present            no-TTL    REFRESHED LAST NIGHT: YES at 2026-09-05T02:23:22.179104+00:00
                       evaluated: boundary 2026-09-05T02:00:00+00:00 (+6h window); checked 1 manifest(s)
                       boundary: 2026-09-05T02:00:00+00:00
                       checked_manifests: 1
                       vintage: 2026-09-05T02:11:10.919000+00:00

FRESHNESS CONTRACT (3 states):
  (default)  serve the cache iff that tool's freshness PREDICATE says fresh
  --check    REPORT staleness, never rebuild.   0 = fresh | 2 = stale | 1 = tool error
  --force    always re-derive
  --fresh    DEPRECATED no-op alias of default (warns; removed next cycle) -- the
             NFRA_GRAPHUNI P2/D2 head-pin made default honor the fingerprint and
             collapsed FRESH into DEFAULT. Proven no-op, with a control.

POPULATION (derived from each tool's actual capability, not a token list):
  contract tools  (warm cached read + rebuild; default/--check/--force):
     comp-trace, comp-blast, comp-diff, comp-xref, comp-platinum, comp-system
  rebuild+probe verb (no warm cached read -- its DEFAULT is the rebuild; --check probes):
     comp-build
  pure producers  (always re-derive; no cached query path -- --force/--fresh collapse):
     comp-aws derive, comp-stitch-refresh
  query-only      (no rebuild path of its own; cannot own a --force):
     comp-kuzu
  status_rc=0
  status_stderr=

--- PROCESS TABLE AFTER ---
  pattern='kuzu_nessie_load|derive_runner|projection_worker'  matches=0  ps_rows(denominator)=28

--- POINTER ETAG AFTER ---
  etag_read[after] rc=0
  etag_read[after] raw_bytes=0000000   "   4   c   c   4   f   1   7   a   9   6   e   5   b   c   5 0000020   d   6   5   2   0   a   5   a   b   a   7   e   4   0   c   f 
  etag_read[after] stderr=<empty>
  etag_read[after] value="4cc4f17a96e5bc5d6520a5aba7e40cf8"

==============================================================================
MORNING_READ=REFRESHED LAST NIGHT: YES at 2026-09-05T02:23:22.179104+00:00
MORNING_READ_VINTAGE=2026-09-05T02:11:10.919000+00:00
MORNING_READ_BOUNDARY=2026-09-05T02:00:00+00:00
STATUS_RC=0
PROCS_BEFORE=0
PROCS_AFTER=0
PROCS_POSITIVE_CONTROL=27  (the probe is alive; a zero above is an absence)
PS_ROWS_DENOMINATOR=31/28
PROCS=0
POINTER_ETAG_BEFORE="4cc4f17a96e5bc5d6520a5aba7e40cf8"
POINTER_ETAG_AFTER="4cc4f17a96e5bc5d6520a5aba7e40cf8"
POINTER_ETAG_STRICT_DIFFERS=false
POINTER_MOVEMENT_ATTRIBUTION=n/a -- the pair is identical, so there is no movement to attribute
POINTER_REREAD=not needed -- the pair was stable on the first reading
POINTER_MOVED_ACROSS_READS=false
==============================================================================
```

### missed.sh -- the night known not to have run, verbatim (2026-09-05T14:02:56Z)

Run under `timeout 120`, script rc 0. `read_method: local-file` is the printed tell that this arm ran against the plant and not against S3.

```text
==============================================================================
MISSED-NIGHT READ -- TO-CG-D-11 / CG-x-8 / 0.9.0_WK_NFRA_CLDGRPH~3
The SAME read, the SAME code path, pointed at the PLANT. Nothing in the real world
was stopped, disabled, provoked or rerun to obtain this reading.
==============================================================================
WALL_CLOCK_UTC=2026-09-05T14:02:56Z
COMP_GRAPH_POINTER_URI=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/plant/current.json

--- THE PLANT, READ BACK BEFORE IT IS USED (a fixture is evidence only if it is the one named) ---
  plant pointer bytes:
{"artifact_prefix":"projection/2026-09-02T20:00:00.000000+00:00/","manifest_key":"projection/2026-09-02T20:00:00.000000+00:00/_build_manifest.json","manifest_sha256":"a46a35809dab2e63c57210023bf145275145c19ef946bf4fd75a77473f11d4bf","schema_version":1,"vintage":"2026-09-02T20:00:00.000000+00:00"}
  plant tree:
2026-09-02T20_00_00.000000+00_00
current.json
  plant vintage dirs:
2026-09-02T20_00_00.000000+00_00
  plant manifest path=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/plant/2026-09-02T20_00_00.000000+00_00/_build_manifest.json
  plant manifest sha256(actual)=a46a35809dab2e63c57210023bf145275145c19ef946bf4fd75a77473f11d4bf
  plant pointer manifest_sha256(claimed)=a46a35809dab2e63c57210023bf145275145c19ef946bf4fd75a77473f11d4bf
  (they must match or the straddle read refuses and the answer would be UNVERIFIABLE,
   not NO -- so this equality is what makes the NO an ANSWER rather than an error)
  plant manifest fields:
    vintage=2026-09-02T20:00:00.000000+00:00
    built_at=2026-09-02T20:15:00.000000+00:00
    writer_id=derive_runner
    producer.mode=full
    schema_version=1
    field_count=14

--- PROCESS TABLE BEFORE (grep -v grep; denominator printed) ---
  pattern='kuzu_nessie_load|derive_runner|projection_worker'  matches=0  ps_rows(denominator)=30
  POSITIVE CONTROL pattern='bash'  matches=30 (probe alive)

--- THE READ: COMP_GRAPH_POINTER_URI=<plant> bash .tools/comp-graph status (verbatim) ---
COMP-GRAPH STATUS  (query-vs-rebuild freshness)
  contract: org/modules/graph/graph-call-manifest.yaml

LOCAL TRACE LAYER (.comp-graph/)
  graph                MISSING      absent             no-TTL    trace graph (comp-trace/comp-blast/comp-diff/comp-xref)  (build: comp-build)
                       predicate: content-SHA drift per indexed node (no TTL on the default path)
                       evaluated: no cached graph -- run comp-build
  baseline             MISSING      absent             no-TTL    xref baseline snapshot (comp-xref)  (build: comp-xref --save)
  platinum.*           MISSING      absent             TTL 300s  comp-platinum caches (per-firm, keyed by --firm)  (build: comp-platinum page <C> --firm <F>)

CLOUD / CROSS-LAYER (projection/current.json, straddle-verified)
  projection.current   PRESENT      built 2d ago       no-TTL    cloud Kuzu projection (projection/current.json, straddle-verified)
                       vintage: 2026-09-02T20:00:00.000000+00:00
                       age_line: Built from the estate as of 2026-09-02 20:00:00 UTC.
                       built_at: 2026-09-02T20:15:00.000000+00:00
                       nessie_commit_hash: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
                       nodes_snapshot_id: 1111111111111111111
                       edges_snapshot_id: 2222222222222222222
                       writer_id: derive_runner
                       producer.mode: full
                       producer.source_commit: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
                       node_count: 27000
                       edge_count: 58000
                       edges_skipped_missing_endpoint: 400
                       artifact_bytes: 47000000
                       band_status: IN-BAND
                       read_method: local-file
  projection.last_night NO           present            no-TTL    REFRESHED LAST NIGHT: NO (last full: 2026-09-02T20:15:00.000000+00:00)
                       evaluated: boundary 2026-09-05T02:00:00+00:00 (+6h window); checked 1 manifest(s)
                       boundary: 2026-09-05T02:00:00+00:00
                       checked_manifests: 1
                       vintage: 2026-09-02T20:00:00.000000+00:00

FRESHNESS CONTRACT (3 states):
  (default)  serve the cache iff that tool's freshness PREDICATE says fresh
  --check    REPORT staleness, never rebuild.   0 = fresh | 2 = stale | 1 = tool error
  --force    always re-derive
  --fresh    DEPRECATED no-op alias of default (warns; removed next cycle) -- the
             NFRA_GRAPHUNI P2/D2 head-pin made default honor the fingerprint and
             collapsed FRESH into DEFAULT. Proven no-op, with a control.

POPULATION (derived from each tool's actual capability, not a token list):
  contract tools  (warm cached read + rebuild; default/--check/--force):
     comp-trace, comp-blast, comp-diff, comp-xref, comp-platinum, comp-system
  rebuild+probe verb (no warm cached read -- its DEFAULT is the rebuild; --check probes):
     comp-build
  pure producers  (always re-derive; no cached query path -- --force/--fresh collapse):
     comp-aws derive, comp-stitch-refresh
  query-only      (no rebuild path of its own; cannot own a --force):
     comp-kuzu
  status_rc=0
  status_stderr=

--- PROCESS TABLE AFTER ---
  pattern='kuzu_nessie_load|derive_runner|projection_worker'  matches=0  ps_rows(denominator)=33

--- THE PLANT AFTER THE READ: the fixture is unchanged, so the read wrote nothing ---
  plant manifest sha256(after)=a46a35809dab2e63c57210023bf145275145c19ef946bf4fd75a77473f11d4bf
  plant pointer sha256(after)=c180b67c7dff36eea01bd34cfc837058d5a28f0b3d82c416da7065adbaf3211f

==============================================================================
MISSED_READ=REFRESHED LAST NIGHT: NO (last full: 2026-09-02T20:15:00.000000+00:00)
MISSED_READ_VINTAGE=2026-09-02T20:00:00.000000+00:00
MISSED_READ_BOUNDARY=2026-09-05T02:00:00+00:00
MISSED_STATUS_RC=0
MISSED_PROCS_BEFORE=0
MISSED_PROCS_AFTER=0
PS_ROWS_DENOMINATOR=30/33
==============================================================================
```

### morning.sh --selftest -- the can-fail proof, verbatim

Each arm fed an input that must produce the OTHER answer. `SELFTEST_BARE_GREP_TRAP=0` here is itself worth reading: inside a script the pattern lives in a variable, so the harness shell's own command line does not carry it and the bare form happens to agree; typed at an interactive shell against the same estate the bare form returned 2 against a truth of 0. The trap is real and whether it fires depends on how the probe is invoked, which is why the disciplined form is used unconditionally.

```text
== SELFTEST: the can-fail proof. A control whose failure mode is silence licenses the
== arm above it (row W1-S18). These arms are shown returning the OTHER answer.
SELFTEST_COMPARATOR_SAME=false   (expect false)
SELFTEST_COMPARATOR_DIFF=true   (expect true)
SELFTEST_PROCS_POSITIVE_CONTROL=24  pattern='bash'  ps_rows=29
== the proc probe is ALIVE: it returns non-zero on a pattern that IS running, so a zero
== on the engine pattern is an ABSENCE and not a dead arm.
SELFTEST_BARE_GREP_TRAP=0   (the trap: counts the grep itself)
SELFTEST_DISCIPLINED=0   (grep -v grep)
SELFTEST_CR_STRIP_RAW=0000000   "   4   c   c   4   f   1   7   a   9   6   e   5   b   c   5
```

### the D11-AC1 / D11-AC2 / D11-AC3 criterion invocations, verbatim (2026-09-05T14:39:03Z)

Each run under `timeout 120`; script rc and grep rc printed beside each deciding line. Taken 37 minutes after the primary transcript and IDENTICAL on every deciding line -- five runs of morning.sh across the pass, same answer, same ETag pair, PROCS=0 every time.

```text
wall clock: 2026-09-05T14:39:03Z
=== D11-AC1  invocation: bash .../morning.sh | grep -E '^MORNING_READ=' (under timeout 120) ===
script_rc=0
MORNING_READ=REFRESHED LAST NIGHT: YES at 2026-09-05T02:23:22.179104+00:00
grep_rc=0

=== D11-AC2  invocation: bash .../missed.sh | grep -E '^MISSED_READ=' (under timeout 120) ===
script_rc=0
MISSED_READ=REFRESHED LAST NIGHT: NO (last full: 2026-09-02T20:15:00.000000+00:00)
grep_rc=0

=== D11-AC3  invocation: bash .../morning.sh | grep -E '^(PROCS|POINTER_MOVED_ACROSS_READS)=' (under timeout 120) ===
script_rc=0
PROCS=0
POINTER_MOVED_ACROSS_READS=false
grep_rc=0

=== the pointer-stability context of the AC3 run (strict + attribution) ===
POINTER_ETAG_BEFORE="4cc4f17a96e5bc5d6520a5aba7e40cf8"
POINTER_ETAG_AFTER="4cc4f17a96e5bc5d6520a5aba7e40cf8"
POINTER_ETAG_STRICT_DIFFERS=false
POINTER_MOVEMENT_ATTRIBUTION=n/a -- the pair is identical, so there is no movement to attribute
POINTER_REREAD=not needed -- the pair was stable on the first reading
POINTER_MOVED_ACROSS_READS=false
```

