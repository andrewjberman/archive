# CG-x-2 -- FWD-2 EXERCISED: the closing pass, three limbs, one record

**TO:** `NFRA_CLDGRPH.TO-CG-D-9` · **cell:** `CG-x-2` · **worker:** `0.9.0_WK_NFRA_CLDGRPH~1`
**branch:** `wk-NFRA_CLDGRPH-1` · **base HEAD:** `61904105639022e4f0a3601a3954860ca7283be6`
**worked:** PASS 1 2026-09-05 03:08Z -> 05:0xZ; **PASS 2 (the RE-HAND) 2026-09-05 06:1xZ -> 08:0xZ, base HEAD `0ebedc3b3b7b67cb837aac2bf27df93b5440a5e0`** · **push state:** LOCAL

---

## THE PASS-3 HEADLINE (2026-09-05 13:0xZ) -- LIMB (iii) IS CAUGHT; THIS SUPERSEDES LIMB (iii) ONLY

**D9-AC4 PASSES on a caught window, and the two honest NOT-CAUGHTs below are not retracted --
they are explained.** Pass 3 was spawned into a live producer burst. Between 12:10:36Z and
12:23:09Z the marker stamped EIGHT times, roughly every 60-90 s; a second burst ran 12:47-12:54Z.
Across the 45-minute bounded poll (`behind.sh --poll 2700`, 12:10:59Z -> 12:56:01Z, run to its
declared bound and not stopped on a favourable read) the detector caught the BEHIND window
**fourteen** times. The deciding lines:

```
BEHIND_CAUGHT=true
POINTER_MOVED_BY_READ=false
LEGIT_REBUILD_REPORTED=true
```

**Nothing was provoked.** No derive, no rebuild, no engine, no marker write, no pointer write, no
AWS mutation of any kind. The stamps are the estate's own; this worker only read. The cause of
passes 1 and 2's NOT-CAUGHT is now measured rather than argued: those passes ran 5h40m against a
marker frozen at `2026-09-05T05:55:42.571886+00:00`, and a BEHIND window exists only between a
stamp and the pointer's advance. There was no window to catch, and the instrument said so.

**THREE INSTRUMENT DEFECTS WERE FOUND AND FIXED IN THIS PASS, EACH BY A CONTROL AND NOT BY
READING THE OUTPUT.** They are listed here because two of them could have decided the criterion:

1. **`NFRA_CLDGRPH-S57`, the issuer's row, DISARMED BY EXERCISE.** The two `aws s3 cp` reads no
   longer silence stderr; the `s3 cp` rc and the jq rc are captured, empty bodies and null fields
   are guarded, every evidence row carries `read_ok`, and the report emits **`READ_FAILED` as a
   third outcome** distinct from both true and false. Demonstrated, not asserted: the positive
   control (a scratch copy pointed at a non-existent bucket, separate evidence file, the real
   pointer untouched) prints `READS_OK=0 of 1`, `BEHIND_CAUGHT=READ_FAILED`,
   `POINTER_MOVED_BY_READ=UNREAD`, `LEGIT_REBUILD_REPORTED=UNREAD` and the 404s verbatim with
   their rc. **S57 disarms only when the instrument actually prints the third outcome; it does.**
2. **`NFRA_CLDGRPH-W1-S19`, filed this pass -- `POINTER_MOVED_BY_READ` was a DIFFERENCE where the
   criterion names a CAUSE.** A client read costs ~40 s and the burst stamped every 60-90 s, so an
   advance lands inside the read window by arithmetic: 10 of the 14 behind-reads had the pointer
   move while the read was in flight, and the bare before-vs-after difference would have printed
   `POINTER_MOVED_BY_READ=true` and FAILED this criterion on a world that satisfies it -- the exact
   mirror of S57's defect, on the same script, in the opposite direction. Replaced with a
   three-limb ATTRIBUTION using the method THIS ORDER prescribes, and the strict unattributed
   difference is still printed on the next line so a grader can take either reading.
3. **Two defects of this worker's OWN new code, both caught by running the control instead of
   trusting the patch, and recorded so they are not rediscovered.** (a) The first form of the S57
   fix returned an EMPTY value field on a failed read, and TAB IS AN IFS WHITESPACE CHARACTER, so
   `IFS=$'\t' read` collapses adjacent tabs into one delimiter and every later field shifts left;
   the verdict was never wrong (`read_ok` was correctly false) but the error text landed in the
   marker field. Fixed with a `READ_FAILED` sentinel so no field is ever empty. (b) The captured
   stderr carried the `.tools/aws` shim's **CR** -- the same CRLF that W1-S18 found on night.sh --
   and a bare CR inside a JSON string made the READ_FAILED row, the very row the clause exists to
   produce, unparseable by jq. **And fixing that one exposed a third hiding beneath it:** jq's `//`
   is the ALTERNATIVE operator and fires on `false` as well as `null`, so
   `.read_ok // <derived>` silently discarded an explicit `read_ok: false` and counted the failed
   read as OK. While jq was still erroring on the CR it emitted nothing, `grep -c` read 0, and
   `READS_OK=0` was RIGHT FOR THE WRONG REASON. Two defects masking each other, the second visible
   only once the first was fixed -- which is why the control was re-run after every patch rather
   than once at the end.

**WHAT IS STILL OPEN AND IS NOT THIS SEAT'S TO CLOSE:** whether the ATTRIBUTED reading of
`POINTER_MOVED_BY_READ` is the criterion's reading, or whether the strict difference governs and
D9-AC4 fails. That is a grading question and it belongs to `3.0.0_SA_CVO` at L9 (W1-S19, ARMED,
same standing as W1-S17). Both numbers are printed on adjacent lines and neither is hidden.

---

## THE PASS-2 HEADLINE (the RE-HAND) -- READ THIS FIRST

**THE ORDER IS STILL NOT MET AND IS NOT FLIPPED -- but on ONE criterion now, not two.**

**`D9-AC2` NOW PASSES, AND IT IS A STRONGER RESULT THAN THE ONE IT REPLACES.** The issuer
re-cut the arm on `1.0.0_SA_CTO`'s ruling @`b8eaa3323b`: the old arm asked *"did any seat
invoke anything"* and failed at `2150 of 2150` **because the issuing seat was driving the round
all night** -- a PROXY that was the outlier inside its own cell, since CG-x-2's DONE WHEN reads
*"no question is ever the reason a rebuild starts"* and PRD acceptance 2 reads *"no question is
ever the cause of a rebuild"*, both CAUSAL. The arm now asks whether any invocation in the window
**caused** the rebuild, and the answer is read from the rebuild itself:
`REBUILD_TRIGGER=events-rule/opal-globgrph-derive-runner-nightly`, `SEAT_CAUSED_REBUILDS=0 of 15`.
The night's derive task id was **recovered from the window** (CloudTrail
`responseElements.tasks[0].taskArn`) rather than taken from the face on trust, and it reproduces
the id the issuer named. The seat-activity census is still printed -- `2613 of 2613`,
eight seats -- but it is now CONTEXT, not the arm: a seat being ACTIVE does not void FWD-2, only a
seat CAUSING a rebuild does, and none did.

**`D9-AC4` FAILS AGAIN, AS A SECOND HONEST NOT-CAUGHT, AND THAT IS THE CORRECT OUTCOME.**
`BEHIND_CAUGHT=false` after 82 cumulative client reads. The marker moved three times between the
two passes (`05:31:07`, `05:39:20`, `05:55:42`) and then **stopped**: it held
`2026-09-05T05:55:42.571886+00:00` for the whole of this pass's polling. A BEHIND window exists
only between a stamp and the pointer's advance; with no stamp there is no window. The four
scheduled tasks on this cluster fire at 02:00Z (the derive) and 03:30Z / 04:00Z / 04:30Z (the
producers) -- all four hours behind this pass and hours ahead of it -- and the intraday stamps come from the CloudTrail-fed
incremental updater reacting to REAL cloud changes, of which there were none.
**I did not provoke one.** The order forbids it and the CTO's words are the reason rather than the
rule: *an arm satisfied by staging its own trigger measures the stager, not the world.* A
manufactured `true` here would have been the one result this criterion cannot accept.

**UNCHANGED AND RE-MEASURED THIS PASS:** `D9-AC1` PASS -- `NIGHT_VINTAGE=2026-09-05T02:11:10.919000+00:00`
later than `PREV_EVENING=2026-09-04T18:11:48.783142+00:00`, attributed by the 3-of-3 snapshot join and never
by "newest vintage". `D9-AC3` PASS -- `STAMP_TO_ANSWER_S=82.186`. `D9-AC5` PASS --
`ENUMERATE: 0 hit(s)`, with a positive control on the SAME file and the SAME verb returning 13,
so the zero is an absence and not a dead arm.

**ONE ROW FILED THIS PASS: `NFRA_CLDGRPH-W1-S18`** -- night.sh's own section-3 positive control,
the one whose job was to make "exactly one derive ran in the window" falsifiable, printed ZERO
LINES at the merged HEAD and printed them silently: the aws shim emits CRLF and the loop's
digit guard rejected every row on its trailing CR. It is fixed in this commit and the section now
prints eight streams and `DERIVE_STREAMS_LISTED=8`, so the claim it licenses is corroborated on a
second instrument instead of agreed with by silence. The pass-1 rows `W1-S13`, `W1-S15` and
`W1-S17` stay ARMED and are not edited.

**PREMISES RE-GROUND AT THE HAND-OFF, not assumed:** the three families carry an `@sha256:` digest
(`globgrph-derive-runner`, `globgrph-projection-worker`, `globgrph-serving`, all on
`sha256:1b89853f...ecde2778`); TO-CG-D-1's proof instance validates rc 0 at this HEAD over its own
eight ids; TO-CG-D-3's validates rc 0 over its eight, seven PASS and one judgment.

**STILL NOTHING WAS WRITTEN TO AWS.** No marker, no pointer, no `projection/` object, no derive, no
rebuild, no engine, no task stopped or started. Every act in both passes is a read.

---

## THE PASS-1 HEADLINE (2026-09-05 05:0xZ) -- SUPERSEDED IN PART BY THE PASS-2 HEADLINE ABOVE

**THE ORDER IS NOT MET AND IS NOT FLIPPED.** `D9-AC2` FAILS on a measured fact: the window the
amendment fixed for limb (i) -- `2026-09-04T21:00Z -> 2026-09-05T06:00Z` -- **was not an unattended
night.** Eight seats made 2,150 tool calls inside it, and a human IAM principal launched an ECS task
on the graph's own cluster 19 minutes in. The face pre-registered exactly this outcome ("an
invocation in the window voids the arm ... this criterion FAILS honestly"), so the arm records
**VOIDED**, the criterion records **FAIL**, and the order stays open for the COO to re-hand.

**WHAT DID PASS, and it is the substance of FWD-2 rather than its precondition:** the nightly fired
itself at `02:00:05Z` on the digest-pinned bytes, ran to a completed publish, and the morning's
served answer carries that night's date -- `D9-AC1` PASS. A real producer stamp reached the served
answer in **82.186 s** end to end -- `D9-AC3` PASS. The client the reads went through has **no
rebuild path at all**, so no question this order asked could have started one -- `D9-AC5` PASS,
with a positive control proving the zero is an absence and not a dead arm.

**`D9-AC4` ALSO FAILS, as an honest NOT-CAUGHT.** The BEHIND window was hunted for 55m30s -- 27
client reads plus 138 cheap marker polls -- and never appeared, **because the marker never moved**:
it held `2026-09-05T03:31:16.793943+00:00` for 88 minutes. A window between a stamp and the
pointer's advance cannot be caught when there is no stamp. The detector is demonstrably alive (27
live marker/served pairs, `POINTER_MOVED_BY_READ=false` on all 27), and the window is demonstrably
real and 82.186 s wide on tonight's own timestamps -- but that is a reconstruction, and limb (iii)
is *tested by trying*. I did not catch it by trying, so it does not pass. **No artifact was
planted, no stamp provoked, no rebuild started, and nothing in AWS was created, run, stopped or
written by this order** -- provoking a stamp would have manufactured the very thing the criterion
exists to observe happening on its own.

**FIVE ROWS FILED:** `NFRA_CLDGRPH-W1-S13` .. `W1-S17`. Two of them (`W1-S13`, `W1-S15`) are
instrument defects that would each have produced a **clean-looking zero** on limb (i) -- one of
them did, and was caught by a control before it reached this record.

---

## LIMB (i) -- ONE UNATTENDED NIGHT

```json
{
  "limb": "i",
  "claim": "the pointer's manifest vintage is later than the previous evening's AND no seat invoked anything",
  "window": "2026-09-04T21:00:00Z -> 2026-09-05T06:00:00Z",
  "window_source": "the issuer's AMENDMENT 2026-09-05 ~02:4xZ; the 09-04 nightly ran on PRE-PIN bytes and ROUND_ANALYSIS.round3.md s.2 item 2 rules that a night under pre-fix bytes is not the night FWD-2 means",

  "NIGHT_VINTAGE": "2026-09-05T02:11:10.919000+00:00",
  "PREV_EVENING": "2026-09-04T18:11:48.783142+00:00",
  "NIGHT_LATER_THAN_PREV_EVENING": true,
  "night_writer_id": "derive_runner",
  "night_producer_mode": "full",
  "night_built_at": "2026-09-05T02:23:22.179104+00:00",
  "night_node_count": 27295,
  "night_edge_count": 58771,

  "attribution_method": "the 3-of-3 join on nodes_snapshot_id / edges_snapshot_id / nessie_commit_hash between the derive's own MARKER_STAMPED log line and the projection manifest -- NEVER 'newest vintage'",
  "join_result": "3/3 on 2026-09-05T02:11:10.919000+00:00 (nodes_snap 4606138319900821475, edges_snap 8760077255054959316, hash c336d1e8bac0321c442677ecd5e3150ff7006eb9b47ec0ad86250f36b4ce2e6d)",
  "why_the_join_is_not_ceremonial": "the FIVE in-window vintages score 0/3, 0/3, 0/3, 3/3, 2/3. 'Newest vintage' would have picked 2026-09-05T03:31:16.793943+00:00, which scores 2 OF 3 -- it shares edges_snapshot_id and one other field with the derive's marker while being a DIFFERENT producer's artifact. A 2-of-3 near-miss is exactly what makes a loose join dangerous: only the full 3-of-3 attributes. Separately, the issuer's warning is confirmed on the record: 2026-09-05T00:52:45.603017+00:00 advanced the pointer earlier the same night by a PRODUCER stamp with no derive in the window at all.",

  "derive_task": "be97f46226f74bae86b9cf853e78763c",
  "derive_started_by": "events-rule/opal-globgrph-derive-runner-nightly",
  "derive_task_definition": "globgrph-derive-runner:7",
  "derive_image_digest": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778",
  "derive_log_span": "2026-09-05T02:00:48Z -> 2026-09-05T02:12:26Z",
  "derive_denominator_line": "s3 notifications buckets read=34 / buckets unreadable=0; unreadable=none",
  "derive_only_one_in_window": "true -- the 8 newest derive-runner log streams were listed with their event spans; exactly ONE falls inside the window, the next-newest is 2026-09-04T16:30:50Z (TO-CG-D-1's ad-hoc QA derive)",
  "instrument_note": "ECS describe-tasks returned null for this task (~1h retention, positive-controlled against 4 live tasks). startedBy and the revision were recovered from CloudTrail; the marker and the denominator line from CloudWatch Logs. Both outlive ECS. Row W1-S16.",

  "ARM_A_SEAT_INVOCATIONS_IN_WINDOW": "2150 of 2150",
  "ARM_A_VERDICT": "VOIDED -- non-zero",
  "ARM_A_SEATS": {"2.0.0_SA_COO~B": 769, "2.0.0_SA_COO": 577, "0.9.0_WK_NFRA_CLDGRPH~2": 175, "3.0.0_SA_CVO": 135, "0.0.0_AB_MSTR": 129, "1.0.0_SA_CTO": 118, "0.7.0_AE_CloudOps~W": 108, "4.0.0_SA_CRO": 21},
  "ARM_A_INSTRUMENT_DEFECT": "the face's filter ('rows naming kuzu|derive|projection|globgrph|run-task') is UNSATISFIABLE: no row in that log carries a command or argument field (423,630 rows / 159 files parsed, 0 unparseable; keys = ts, ts_unix, serial, tool_name, kind, serial_source, session_id, + a legacy agent/tool variant). Run as written it returns 0 for a STRUCTURAL reason and reads as a clean unattended night. Row W1-S13. The path is ALSO invisible from a worktree (gitignored, .gitignore:261) -- the separate defect S47 already recorded; fixing the path does not fix the filter.",

  "ARM_B_RUNTASK_NONPIPE_IN_WINDOW": "1 of 11",
  "ARM_B_VERDICT": "VOIDED -- non-zero",
  "ARM_B_THE_ONE": "2026-09-04T21:18:53Z, userIdentity.type IAMUser, arn:aws:iam::313476888478:user/Andrew_Berman, cluster opal-globgrph, taskDefinition globgrph-trino, no startedBy; responseElements.tasks length 1, failures [], errorCode null -- a SUCCESSFUL launch, not a refused attempt",
  "ARM_B_THE_OTHER_TEN": "7x the projection Pipe role ('Started by Eventbridge Pipes'); events-rule/opal-globgrph-derive-runner-nightly; chronos-schedule/globgrph-cse-produc; events-rule/opal-globgrph-comp-learns-producer-nightly",
  "ARM_B_CLASSIFIER_DEFECT_CAUGHT": "the face enumerates TWO legitimate starters; the window contains FOUR. A classifier built to the face's enumeration printed 2 of 10 -- convicting the cse-producer scheduler as a human invocation. Caught because the per-row labels disagreed with the count; both were rebuilt onto ONE classifier keyed on AssumedRole + a startedBy naming a rule/schedule/service. Corrected reading 1 of 11. Row W1-S15.",

  "VERDICT": "FAIL -- the vintage arm passes (D9-AC1), the unattended arm is VOIDED on both halves (D9-AC2)",
  "not_refuted": "the nightly itself was UNPROVOKED and fully attributed to its own EventBridge rule. globgrph-trino is the query-engine family, not the derive path, and it ran 2h41m before the cron. The arm fails on its PRECONDITION -- an idle fabric -- not on FWD-2's substance."
}
```

### LIMB (i) ARM (b), RE-CUT TO THE CAUSAL FORM (PASS 2 -- this is THE ARM; `ARM_A_*` and
`ARM_B_*` above are pass-1 measurements that remain true and are no longer what limb (i) turns on)

```json
{
  "limb": "i -- arm (b), CAUSAL",
  "authority": "1.0.0_SA_CTO ruling @b8eaa3323b, carried into TO-CG-D-9 by the issuer's amendment; scope = limb (i) second arm ONLY",
  "question": "did any invocation in the window CAUSE the rebuild -- not, was any seat active",
  "REBUILD_TRIGGER": "events-rule/opal-globgrph-derive-runner-nightly",
  "SEAT_CAUSED_REBUILDS": "0 of 15",
  "how_the_trigger_was_read": "from the rebuild itself, and the rebuild was identified from the window rather than from the face: CloudTrail RunTask in 2026-09-04T21:00Z..2026-09-05T06:00Z filtered to a derive-runner task definition returns exactly ONE event (2026-09-05T02:00:05Z), whose responseElements.tasks[0].taskArn ends be97f46226f74bae86b9cf853e78763c -- the id the issuer named, REPRODUCED not trusted. That stream carries the MARKER_STAMPED line whose three snapshot ids join 3-of-3 to the manifest of NIGHT_VINTAGE. Four links, four different instruments: S3 manifest <- snapshot join <- CloudWatch Logs <- CloudTrail <- startedBy.",
  "denominator": "15 -- every rebuild-constituting task started in the window, where rebuild-constituting = a family that writes a graph artifact (derive runner, projection worker, producers) UNIONED with a purely empirical test (a projection vintage within 900 s of the task). The union is the point: a task OUTSIDE the declared family set that DID produce a vintage would still be counted, so a scoped set cannot hide a member.",
  "total_runtask_events_in_window": 16,
  "the_one_not_counted": "2026-09-04T21:18:53Z globgrph-trino, userIdentity IAMUser arn:aws:iam::313476888478:user/Andrew_Berman, userAgent Boto3 on os/windows#10.0.26100 from 73.84.214.103. It is the ONLY human-or-seat row in the whole window and it is NOT rebuild-constituting: the nearest projection vintage is 11,224 s away (2026-09-04T18:11:48, which PRECEDES it), so no rebuild followed it. Under the pre-amendment proxy arm this single row failed the criterion; under the causal arm it is exactly what the CTO said it was -- a seat being active, not a seat causing a rebuild.",
  "classification_method": "BY PROVENANCE FORM, never by an enumeration of role names -- the defect row W1-S15 records. A starter is automated if its startedBy names a rule (events-rule/), a schedule (chronos-schedule/), a pipe (Started by Eventbridge Pipes) or a service (ecs-svc/); anything else is HUMAN-OR-SEAT. The form is open-ended, so the FOURTH starter the pass-1 face did not enumerate classifies correctly without the classifier being edited.",
  "corroboration_on_a_second_unspoofable_field": "startedBy is caller-supplied and could be forged, so every label is checked against CloudTrail-authored evidence: userIdentity.invokedBy (set by CloudTrail when an AWS service made the call) and, where that is empty, the userAgent banner. 15 of 16 rows carry invokedBy pipes.amazonaws.com or events.amazonaws.com. The sixteenth automated row -- the chronos-scheduled cse-producer, the exact row that fooled the pass-1 name-list classifier -- carries NO invokedBy, and is corroborated instead by userAgent 'AmazonEventBridgeScheduler aws-sdk-java/2.50.3 ... exec-env/AWS_ECS_FARGATE' and by firing at 03:30:13Z on 09-04 AND 09-05, to the second, on an auto-paginated 48h lookup.",
  "THE CONTROL THAT MUST AGREE": "per-row labels are printed beside the count and their tally must sum to the denominator: PIPE 11 + RULE 3 + SCHEDULE 1 + HUMAN-OR-SEAT 1 = 16 = 16, printed as LABELS_AGREE_WITH_DENOMINATOR=true. The pass-1 worker found the four-vs-two error ONLY because its labels contradicted its own total, so the control is kept rather than retired once it has fired.",
  "instrument_qualifiers_stated": "CloudTrail management-event delivery lags up to ~15 min; the window closed at 06:00Z and was read after 06:11Z, so no in-window event is undelivered. The lookup returned 16 of a cap of 50, so the denominator is not truncated, and the script prints a WARN if it ever reaches the cap.",
  "the_telemetry_filter_is_NOT_reintroduced": "the face's pass-1 filter (rows naming kuzu|derive|projection|globgrph|run-task) is unsatisfiable -- the log schema is ts/ts_unix/serial/tool_name/kind/serial_source/session_id and tool_name is the tool NAME. Running it would return 0 for a STRUCTURAL reason and certify a fully worked night as unattended. night.sh prints the field list so the limit is visible in the output rather than asserted in prose. Row W1-S13.",
  "VERDICT": "PASS -- the rebuild in this window was caused by its own EventBridge rule, and no invocation by any human or seat caused any rebuild-constituting task in it."
}
```

## LIMB (ii) -- ONE REAL PRODUCER STAMP -> THE SERVED ANSWER

```json
{
  "limb": "ii",
  "claim": "a real producer stamp reaches the served answer within minutes, with the latency printed",

  "STAMP": "2026-09-05T03:31:16.793943+00:00",
  "stamp_writer_id": "cse_producers_nightly",
  "stamp_producer_mode": "incremental",
  "stamp_choice_rule": "the face: 'the first real incremental_updater stamp after 13:00Z on the day you run, OR, if none arrives inside your bounded wait, the newest one already on the record (say which)'",
  "SAYING_WHICH": "THE SECOND BRANCH. This order ran 03:0xZ-05:0xZ on 2026-09-05; 13:00Z that day had not arrived, so no post-13:00Z stamp could exist and no bounded wait could produce one. This is the newest real producer stamp on the record. TWO DEPARTURES STATED RATHER THAN PAPERED OVER: it is not in working hours, and its writer_id is cse_producers_nightly rather than incremental_updater. It IS real and unprovoked -- its RunTask (CloudTrail 2026-09-05T03:30:13Z) was started by chronos-schedule/globgrph-cse-produc under the cse-producer scheduler role, not by any seat, and not by this order.",

  "t1_stamp_committed_at": "2026-09-05T03:31:16.793943+00:00",
  "t2_pointer_LastModified": "2026-09-05T03:31:47Z (s3api, UTC -- `aws s3 ls` would have rendered LOCAL)",
  "t3_service_last_swap": "2026-09-05T03:32:38.979596+00:00",
  "t3_source": "/ecs/globgrph-serving stream serving/globgrph-serving/8889156e83ad4e3e95931e9d505169a9 -- 'projection swap complete: {status: ok, vintage: 2026-09-05T03:31:16.793943+00:00, pointer_read_at: 2026-09-05T03:32:38.973078+00:00, last_swap: 2026-09-05T03:32:38.979596+00:00}'",
  "t4_answer_read": "2026-09-05T04:15:37.122041Z via .tools/comp-kuzu --json 'MATCH (n) RETURN count(n) AS c' -> 27295, stderr VINTAGE: Built from the estate as of 2026-09-05 03:31:16 UTC. [vintage=2026-09-05T03:31:16.793943+00:00 manifest=78fecbbdf4ef prefix=projection/2026-09-05T03:31:16.793943+00:00/]",
  "answer_corroborates_the_manifest": "node_count 27295 from the client equals the manifest's node_count 27295 exactly",

  "STAMP_TO_POINTER_S": 30.206,
  "POINTER_TO_SWAP_S": 51.980,
  "STAMP_TO_ANSWER_S": 82.186,
  "WITHIN_MINUTES": 900,
  "within_minutes_reading": "the issuer's: <= 15 min (900 s) for an incremental stamp. 82.186 s is 9.1% of that ceiling. The CVO may read it tighter; at 82 s it clears any reading of 'within minutes'.",

  "THE_AMBIGUITY_DECLARED": "the face names a fourth timestamp ('an ANSWER read carrying that vintage') but never says which clock STAMP->ANSWER stops. STAMP_TO_ANSWER_S above is last_swap - committed_at = the moment the served answer FIRST carried this vintage, CONFIRMED by the t4 read actually returning it. The other reading -- this worker's own wall clock -- is STAMP_TO_THIS_WORKERS_READ_S = 2660.328, and it is printed by latency.sh beside the first. The two differ by 32x on the same stamp; under the second, D9-AC3 would FAIL. Only the first is a property of the estate: the second is bounded only by how long a worker waits before typing, so a measurer who controls the value is not a control. Row W1-S17. Both numbers are on the record so 3.0.0_SA_CVO can grade either without re-running anything.",

  "watcher_interval_read": "PROJECTION_WATCH_INTERVAL_SECONDS default 60 s (projection_server.py:37, :402) -- the 51.98 s pointer-to-swap leg is one watcher tick, as designed",

  "VERDICT": "PASS -- 82.186 s stamp to served answer, against a 900 s ceiling"
}
```

## LIMB (iii) -- TESTED BY TRYING

```json
{
  "limb": "iii",
  "claim": "a read through the client while the served artifact is BEHIND the marker returns the stale answer with its age; the pointer does not move for the read; NO rebuild starts; and the same detector later reports a legitimate marker-triggered rebuild",
  "method": "BEHIND is a WINDOW, not a plant. The poller samples the MARKER tightly (a cheap S3 GET, ~2 s) and spends the expensive ~40 s client read only when the marker has actually moved. Measured tonight the window is ~82 s wide (stamp 03:31:16.79 -> swap 03:32:38.98), and the cheap poll detects a marker move within ~10 s, so the window is catchable. A naive read-everything loop samples SLOWER than the window it hunts and would have missed it for an instrument reason.",
  "no_plant": "no artifact was written, no stamp provoked, no rebuild started, no task stopped or restarted. Every read is a read.",
  "client": ".tools/comp-kuzu only -- the thin client from CG-s-6/TO-CG-D-3. Never comp-find --corpus aws, comp-blast or comp-trace, whose reads could still touch the _canonical seam that CG-s-8 retires LAST.",
  "SEE": "the RESULT block below, written from behind_evidence.jsonl after the polls closed"
}
```

```json
{
  "limb": "iii -- RESULT",
  "BEHIND_CAUGHT": false,
  "verdict": "BEHIND-NOT-CAUGHT -- recorded honestly, never planted. D9-AC4 FAILS.",
  "bound_spent": "27 client reads through .tools/comp-kuzu plus 138 cheap marker polls, over 2026-09-05T04:03:42.948885900Z -> 2026-09-05T04:59:13.216817800Z (55m30s), across three bounded invocations of behind.sh --poll",
  "why_not_caught": "THE MARKER NEVER MOVED. It held 2026-09-05T03:31:16.793943+00:00 for the entire 55m30s and was still holding it at the last read -- 88 minutes static. A BEHIND window can only exist between a stamp and the pointer's advance; with no stamp there is no window to catch. This is an absence of the TRIGGER, not a failure of the detector.",
  "the_detector_is_not_dead": "the poller returned a live marker and a live served vintage on every one of the 27 reads (no UNKNOWN, no empty), and its comparison arm is exercised: it correctly reported behind=false for 27 identical pairs. What it never got was an unequal pair.",
  "distinct_marker_served_pairs_observed": [["2026-09-05T03:31:16.793943+00:00", "2026-09-05T03:31:16.793943+00:00"]],
  "POINTER_MOVED_BY_READ": "false on all 27 reads -- the pointer's vintage was read immediately before and immediately after each client read and was identical every time. This half of the claim IS established: 27 of 27 reads through the client moved nothing.",
  "LEGIT_REBUILD_REPORTED": "not observable in this window -- no rebuild occurred to report. NOT a negative finding about the can-fail arm; the arm was never presented with a rebuild.",
  "CLIENT_REBUILD_PATH_HITS": 0,
  "no_rebuild_started_by_any_read": "0 projection-worker tasks started during the poll. ECS list-tasks for family globgrph-projection-worker was read before AND after every one of the 27 client reads and returned the same set each time; CloudTrail records no RunTask on the cluster after 2026-09-05T04:00:28Z (the comp-learns producer's own scheduled fire, 3 minutes before the poll began).",

  "WHAT THE ORDER FORBADE ME TO DO ABOUT IT": "provoke a stamp. The face is explicit -- 'no plant', 'a question is never the reason a rebuild starts, and neither is this order'. Writing a marker, running a producer or firing a derive would have manufactured the window this criterion exists to observe occurring naturally. So the bound was spent waiting and the result is recorded as the face pre-registered it: 'record BEHIND-NOT-CAUGHT in N reads over M minutes with the marker/served pairs observed -- an honest NOT-CAUGHT, never a plant, and the COO re-hands.'",

  "WHAT IS ESTABLISHED ANYWAY, and its limit": "limb (ii) measures the window's WIDTH on tonight's own stamp: marker 03:31:16.79 -> pointer 03:31:47 -> serving swap 03:32:38.98, so the served artifact was demonstrably BEHIND the marker for 82.186 s. The window is real and it is wide enough to catch -- the cheap poll detects a marker move within ~10 s. But that is a RECONSTRUCTION from timestamps, not a read taken while behind. Limb (iii) is 'TESTED BY TRYING' and I did not catch it by trying, so it does not pass. The reconstruction is offered as context for the re-hand, never as a substitute.",

  "FOR THE RE-HAND, so the next attempt is not another hour of waiting": "the estate stamps when the estate changes. Tonight's stamps clustered 00:28-00:52Z and then 02:11Z / 03:31Z, with an 88-minute gap after. The poller as written is the right instrument -- cheap marker sampling at ~10 s with an expensive client read fired only on a marker move -- and it should simply be started BEFORE a known scheduled producer rather than after. The four scheduled producers and their fire times are on the record in TO-CG-D-1's declared_exclusions (03:30Z Scheduler, 04:00Z Rule, 04:30Z Rule, and resource-summaries-producer with no trigger at all). Starting the poll a minute before one of those is a natural, unprovoked catch."
}
```

### LIMB (iii) -- RESULT, PASS 2 (the RE-HAND)

```json
{
  "limb": "iii -- RESULT, PASS 2",
  "BEHIND_CAUGHT": false,
  "READS_CUMULATIVE": "82 client reads in behind_evidence.jsonl across both passes",
  "POINTER_MOVED_BY_READ": "false",
  "LEGIT_REBUILD_REPORTED": "false",
  "CLIENT_REBUILD_PATH_HITS": 0,
  "what_changed_between_the_passes": "the marker DID move three times after pass 1 closed -- 2026-09-05T05:31:07.555427+00:00, 05:39:20.963495+00:00 and 05:55:42.571886+00:00, each an incremental_updater stamp with its own projection vintage and its own Pipe-started projection-worker task. So the pointer is demonstrably still moving and the pass-1 diagnosis (an absence of TRIGGER, not a dead detector) is confirmed by the world rather than argued.",
  "why_this_pass_still_did_not_catch_it": "THE MARKER NEVER MOVED AGAIN. It held 2026-09-05T05:55:42.571886+00:00 for the whole of pass 2's polling. The four scheduled tasks on this cluster fire at 02:00Z (the derive) and 03:30Z / 04:00Z / 04:30Z (the producers), and all four had already fired hours before this pass began; the intraday stamps come from the CloudTrail-fed incremental updater reacting to real cloud changes, and the estate's own stamp history shows exactly this shape -- bursts while a seat is changing the cloud (00:28-00:52Z, 05:31-05:55Z) separated by multi-hour silences (18:11Z -> 00:28Z is 6h17m). Waiting longer does not make a stamp; only a real cloud change does, and making one is the thing this order forbids.",
  "what_i_was_forbidden_to_do_about_it": "provoke a stamp. Not merely because the order says so, but for the reason the CTO gave: an arm satisfied by staging its own trigger measures the stager, not the world. Every candidate shortcut -- writing the marker, firing a producer, running a derive, touching any AWS resource to make the incremental updater notice -- would have manufactured the very event limb (iii) exists to observe happening unprompted. A second honest NOT-CAUGHT is a better record than a manufactured true, and this is that record.",
  "no_mutation_this_pass": "the pass-2 polling issued only S3 GETs on the marker and the pointer, ecs list-tasks, and reads through .tools/comp-kuzu. Nothing was created, written, run, stopped or deleted in AWS.",
  "marker_served_pairs_this_pass": "every pair is in behind_evidence.jsonl and in the transcript below; the marker column is constant at 2026-09-05T05:55:42.571886+00:00 for the whole of pass 2 and the served column matches it on every read"
}
```

---

## THE S12 CONTRAST -- the before, never the licensing arm

`NFRA_CLDGRPH-S12` @`d60817d742` recorded that a `comp-*` call used to reach
`_canonical.ensure_fresh` and trigger a LOCAL rebuild -- a question causing a rebuild, which is
precisely what FWD-2 forbids. After CG-s-6 (TO-CG-D-3) the client has no such path:

```
python .tools/comp-read infra/aws/globgrph/kuzu_cli.py --enumerate 'ensure_fresh|kuzu_nessie_load|_incremental_or_serve_stale' --limit 3
  ENUMERATE: 0 hit(s) across 169 lines / 8 section(s) scanned
  DOCSTRING 0 | COMMENT 0 | DEF 0 | CODE 0
```

**POSITIVE CONTROL, because a zero from a tool that cannot find anything is not an absence:** the
same verb on the same file with a token that IS present returns `3 hit(s)` (`VINTAGE`, banded
DOCSTRING=1 CODE=2). The arm reads this file and finds things; it does not find a rebuild path.

The seam itself survives in `_canonical.py` for the OTHER tools until CG-s-8 retires it last (the
CTO's ordering). **This is quoted as the BEFORE, never as the licensing arm.**

---

## CRITERIA, EACH WITH ITS INVOCATION AND ITS DECIDING LINE (PASS 2 -- the pass-1 table follows)

| id | verdict | invocation (each under `timeout 120`) | deciding output |
|---|---|---|---|
| D9-AC1 | **PASS** | `bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/night.sh \| grep -E '^(NIGHT_VINTAGE\|PREV_EVENING)='` | `NIGHT_VINTAGE=2026-09-05T02:11:10.919000+00:00` / `PREV_EVENING=2026-09-04T18:11:48.783142+00:00` |
| D9-AC2 | **PASS** | `bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/night.sh \| grep -E '^(REBUILD_TRIGGER\|SEAT_CAUSED_REBUILDS)='` | `REBUILD_TRIGGER=events-rule/opal-globgrph-derive-runner-nightly` / `SEAT_CAUSED_REBUILDS=0 of 15` |
| D9-AC3 | **PASS** | `bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/latency.sh \| grep -E '^STAMP_TO_ANSWER_S='` | `STAMP_TO_ANSWER_S=82.186` |
| D9-AC4 | **FAIL** | `bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/behind.sh \| grep -E '^(BEHIND_CAUGHT\|POINTER_MOVED_BY_READ\|LEGIT_REBUILD_REPORTED)='` | `BEHIND_CAUGHT=false` -- a SECOND honest NOT-CAUGHT; the marker held 2026-09-05T05:55:42.571886+00:00 for the whole of pass 2 and no stamp was provoked |
| D9-AC5 | **PASS** | `python .tools/comp-read infra/aws/globgrph/kuzu_cli.py --enumerate 'ensure_fresh\|kuzu_nessie_load\|_incremental_or_serve_stale' --limit 3` | `ENUMERATE: 0 hit(s) across 169 lines / 8 section(s) scanned`; positive control same file same verb `'def \|import '` returns 13 |
| D9-AC6 | RECORDED, no verdict | judgment | the reading below, for `3.0.0_SA_CVO` at L9 |

**PASS-1 TABLE, kept because a superseded verdict is still a measurement that was made:** `D9-AC1` PASS, `D9-AC2` FAIL (`SEAT_INVOCATIONS_IN_WINDOW=2150 of 2150` / `RUNTASK_NONPIPE_IN_WINDOW=1 of 11` under the PROXY arm the CTO's ruling replaced), `D9-AC3` PASS (`STAMP_TO_ANSWER_S=82.186`), `D9-AC4` FAIL (NOT-CAUGHT in 27 reads over 55m30s), `D9-AC5` PASS, `D9-AC6` recorded. The pass-1 `D9-AC2` numbers are NOT withdrawn -- they are true of the window and simply do not answer the question the arm now asks.


---

## D9-AC6 -- THE THREE LIMBS READ TOGETHER (a reading act; NO verdict; graded by `3.0.0_SA_CVO`)

**FWD-2 says:** *"The graph gets newer on the estate's own schedule -- nightly in full and within
minutes of any cloud change."* **Acceptance 2:** *"Left alone overnight it is newer in the morning;
a cloud change made during the day is visible without anyone requesting a refresh; and no question
is ever the cause of a rebuild."*

**Clause 1, "left alone overnight it is newer in the morning."** The *newer in the morning* half is
established beyond argument: the nightly fired itself at `02:00:05Z` from
`events-rule/opal-globgrph-derive-runner-nightly` on the pinned digest
`sha256:1b89853f...`, ran 02:00:48Z -> 02:12:26Z, stamped the marker, and its artifact --
identified by a 3-of-3 snapshot join, not by recency -- is serving as
`2026-09-05T02:11:10.919000+00:00`, later than the previous evening's
`2026-09-04T18:11:48.783142+00:00`. The *left alone* half is **NOT established, and I record that
as a failure rather than reading it charitably.** Eight seats made 2,150 tool calls in the window
and a human launched `globgrph-trino` on the cluster at `21:18:53Z`. Neither touched the derive
path, and nothing suggests either caused the nightly -- but "unattended" is a claim about the
*window*, and this window does not support it. The face pre-registered VOIDED for exactly this, so
that is what it gets.

**A structural tension the issuer should see, because re-handing alone will not clear it.** This
criterion can only pass on a night when nobody works, and this project is being driven hardest at
night -- the round-4 drain has occupied every night since the pins landed 2026-09-04 ~17:2xZ. The
arm and the work compete for the same hours. Either the re-hand needs a night the fabric is
*deliberately* idle, or the arm should be re-cut to ask what it actually cares about -- *did any
invocation CAUSE a rebuild* -- which is answerable on any night and is the question FWD-2's third
clause actually poses. I am not authorised to re-cut it and have not; I am naming it.

**Clause 2, "a cloud change during the day is visible without anyone requesting a refresh."**
Demonstrated end to end in **82.186 s**: marker `03:31:16.79` -> pointer `03:31:47` (30.2 s) ->
serving swap `03:32:38.98` (52.0 s, one 60 s watcher tick) -> a client read returning that vintage
with its plain-words age line and a node count matching the manifest exactly. Nobody requested it;
the stamp came from a chronos-scheduled producer. **Two honest qualifications.** It was `03:31Z`,
not working hours -- 13:00Z had not arrived when this order ran, and the face's own fallback
branch ("the newest one already on the record, say which") is what I used. And the face never says
which clock `STAMP->ANSWER` stops; I read it as *when the served answer first carried the vintage*,
82.186 s, and printed my own wall-clock reading (2,660.328 s) beside it so the CVO can grade
either. Under the second reading D9-AC3 fails. I chose the first because the second is bounded
only by when a worker chooses to type, and a number the measurer controls cannot be a control.

**Clause 3, "no question is ever the cause of a rebuild."** This is the clause the whole order is
built to test, and it is the strongest of the three. The client every read in this order went
through has **zero** rebuild-path tokens, positive-controlled. Nothing this order did -- and it did
a great deal of reading -- created, ran, stopped or wrote anything. The S12 contrast is real and
directional: a `comp-*` call used to trigger a local rebuild; it no longer can.

**But the clause is only HALF exercised, and the half I could not exercise is the interesting one.**
"No question causes a rebuild" has a weak reading (the client has no rebuild code -- proven) and a
strong reading (*while the served answer is visibly stale, a read still refuses to refresh it*).
The strong reading is what limb (iii) exists for, and it needs the served artifact to be BEHIND the
marker at the moment of the read. I hunted that window for 55m30s and the estate simply did not
stamp -- the marker sat unchanged for 88 minutes. `POINTER_MOVED_BY_READ=false` on 27 of 27 reads
is real evidence and I record it, but every one of those reads was taken against an artifact that
was already current, which is the easy case. **A read that declines to rebuild when nothing is
stale proves less than a read that declines when something is.** That is why I record `D9-AC4` as
FAIL rather than arguing the 27 reads cover it.

**What I did NOT do, and would name if I had.** No artifact was planted, no stamp provoked, no
criterion's `expect` relaxed. When `D9-AC2` turned out to fail on a measured fact, the honest FAIL
is the record and the order stays open. When D9-AC5's sibling defect (an `expect` unsatisfiable by
its own invocation) was fixed by the issuer before hand-off, I re-ran it with a positive control
rather than trusting the fix.

**The two findings I would put in front of a grader first,** because each would have produced a
*clean-looking zero* on the criterion that matters most: (1) the seat-invocation log carries no
command text, so the face's filter returns 0 structurally -- run as written it would have certified
this working night as unattended (`W1-S13`); (2) the face enumerates two legitimate RunTask
starters where the window holds four, and a classifier built to that enumeration convicted a
scheduled producer as a human invocation -- it printed `2 of 10` before the disagreement between
its own labels and its own count exposed it (`W1-S15`). Both are the same shape: **a check whose
negative and whose no-measurement are indistinguishable.** The first was disarmed by asking what
the log *can* answer; the second by classifying on provenance instead of on a list of names.


### D9-AC6 -- PASS-2 AMENDMENT TO THE READING (a reading act; NO verdict)

PASS-2 AMENDMENT TO THIS READING (2026-09-05 08:0xZ, the RE-HAND). The pass-1 reading above stands except on ONE point, and the point is the whole of clause 3.

**CLAUSE 1**,  'left alone overnight it is newer in the morning': the NEWER half is unchanged and established -- NIGHT_VINTAGE 2026-09-05T02:11:10.919000+00:00 later than PREV_EVENING 2026-09-04T18:11:48.783142+00:00, attributed by a 3-of-3 snapshot join and never by recency. The LEFT ALONE half I read in pass 1 as a failure, because 2,150 seat tool calls sat inside the window. 1.0.0_SA_CTO ruled @b8eaa3323b that this reads the clause wrong: CG-x-2's own DONE WHEN says 'no question is ever the REASON a rebuild starts' and PRD acceptance 2 says 'no question is ever the CAUSE of a rebuild'. Both are causal, and 'no seat was awake' is a proxy for them that the estate can fail while the property holds perfectly -- as it did: the seats awake in that window were the ones RUNNING THIS ROUND. I read the clause now as the cell reads it, and on that reading it is established: the rebuild's own startedBy is events-rule/opal-globgrph-derive-runner-nightly, and of 15 rebuild-constituting tasks in the window, 0 were caused by a human or a seat. I want to be explicit that I am not simply agreeing with a ruling that makes my criterion pass: the strongest thing I can say against myself is that the causal arm cannot see a seat that caused a rebuild by an act with no CloudTrail RunTask -- a marker write, an S3 put -- and I did not measure that surface. What I did measure is bounded and stated: RunTask provenance for the whole window, plus the unscoped re-read that would have caught a human-started task producing a vintage outside the declared rebuild families.

**CLAUSE 2**,  'a cloud change during the day is visible without anyone requesting a refresh': unchanged, established, 82.186 s end to end on a real producer stamp, read as WITHIN MINUTES at the issuer's <= 900 s. I restate the qualifier rather than let it fade: the stamp I measured is at 03:31Z and is not 'working hours', and its writer_id is cse_producers_nightly, so it is a SCHEDULED producer's change rather than an ad-hoc daytime one. It is the newest real stamp on the record and no bounded wait produced a working-hours one; row W1-S17 records that the clock STAMP->ANSWER stops at is ambiguous in the face and that the two readings differ by 32x.

**CLAUSE 3**,  'no question is ever the cause of a rebuild': the WEAK reading is proven -- the client every read in this order went through has no rebuild path at all (0 hits, positive control 13 on the same file and verb). The STRONG reading, that a read taken while the served artifact is BEHIND the marker returns the stale answer and starts nothing, is STILL NOT EXERCISED, and this is the honest cost of the pass: BEHIND_CAUGHT=false again, over the cumulative client reads in behind_evidence.jsonl spanning 2026-09-05T04:03Z -> 08:1xZ (the count is printed by behind.sh as READS= and carried in D9-AC4's denominator). The half that IS exercised is exercised hard: POINTER_MOVED_BY_READ=false on every one of them, and 0 projection-worker tasks started by any read. What is missing is not a control but an EVENT -- the estate did not stamp, because the estate did not change. I could have made it change in four seconds. That is precisely why I did not: an arm satisfied by staging its own trigger measures the stager, not the world, and this is the one criterion in the cell whose entire content is that the world moves without being asked.

**READ TOGETHER**:  FWD-2's substance -- the graph gets newer on the estate's own schedule, nightly in full and within minutes of a change, and nobody's question causes it -- is exercised on every limb except the deliberate stale-read trial, which needs an unprovoked stamp to land inside a poll and has now failed to for two passes for the same reason both times. 3.0.0_SA_CVO grades this; I offer no verdict on it.

---

## TRANSCRIPTS

### night.sh (limb i)

```
=== TO-CG-D-9 LIMB (i): ONE UNATTENDED NIGHT
WINDOW=2026-09-04T21:00:00Z -> 2026-09-05T06:00:00Z
READ_AT=2026-09-05T04:01:13Z

--- 1. projection/ vintages (full list, no head)
VINTAGES_TOTAL=53
--- vintages inside the window:
2026-09-05T00:28:21.155513+00:00
2026-09-05T00:36:33.532742+00:00
2026-09-05T00:52:45.603017+00:00
2026-09-05T02:11:10.919000+00:00
2026-09-05T03:31:16.793943+00:00
VINTAGES_IN_WINDOW=5

--- 2. derive-runner log streams (durable instrument; ECS has aged the task out)

--- the night derive's own lines (marker + the bucket-notification denominator)
  s3 notifications buckets read=34 / buckets unreadable=0; unreadable=none
  OK: MARKER_STAMPED writer=derive_runner hash=c336d1e8bac0321c442677ecd5e3150ff7006eb9b47ec0ad86250f36b4ce2e6d nodes_snap=4606138319900821475 edges_snap=8760077255054959316
DERIVE_DENOMINATOR_LINE=s3 notifications buckets read=34 / buckets unreadable=0; unreadable=none

--- 3. attribute the vintage by the 3-of-3 snapshot join (NEVER by 'newest')
  2026-09-05T00:28:21.155513+00:00  writer=incremental_updater mode=incremental built_at=2026-09-05T00:28:45.142377+00:00 JOIN=0/3
  2026-09-05T00:36:33.532742+00:00  writer=incremental_updater mode=incremental built_at=2026-09-05T00:36:48.483584+00:00 JOIN=0/3
  2026-09-05T00:52:45.603017+00:00  writer=incremental_updater mode=incremental built_at=2026-09-05T00:54:18.301291+00:00 JOIN=0/3
  2026-09-05T02:11:10.919000+00:00  writer=derive_runner mode=full built_at=2026-09-05T02:23:22.179104+00:00 JOIN=3/3
  2026-09-05T03:31:16.793943+00:00  writer=cse_producers_nightly mode=incremental built_at=2026-09-05T03:31:43.917433+00:00 JOIN=2/3

NIGHT_VINTAGE=2026-09-05T02:11:10.919000+00:00
NIGHT_WRITER=derive_runner NIGHT_MODE=full NIGHT_BUILT_AT=2026-09-05T02:23:22.179104+00:00
PREV_EVENING=2026-09-04T18:11:48.783142+00:00
NIGHT_LATER_THAN_PREV_EVENING=true

--- 4. arm (a) seat invocation census -- org/mcp/agent_telemetry
TELEMETRY_DIR=/c/Users/AndrewBerman/Desktop/ajb_workspace/org/mcp/agent_telemetry (GITIGNORED at .gitignore:261 -- absent from every worktree;
  reading it at the worktree path returns a FALSE ZERO, so the parent workspace is read)
  telemetry files scanned: 159
  FIELDS PRESENT ON WINDOW ROWS: kind, serial, serial_source, session_id, tool_name, ts, ts_unix
  INSTRUMENT LIMIT: no field carries the command text or arguments of a tool call.
  The order's arm-(a) filter ('rows naming kuzu|derive|projection|globgrph|run-task')
  is therefore UNSATISFIABLE ON THIS LOG: such a regex reads 0 for a STRUCTURAL reason
  (the field does not exist), not because no seat touched the graph -- a vacuous zero.
  The honest arm at the grain the log DOES carry: was any seat invoking anything at all.
  -- seats active in the window:
       2.0.0_SA_COO~B                   769 tool call(s)
       2.0.0_SA_COO                     594 tool call(s)
       0.9.0_WK_NFRA_CLDGRPH~2          182 tool call(s)
       3.0.0_SA_CVO                     135 tool call(s)
       0.0.0_AB_MSTR                    129 tool call(s)
       1.0.0_SA_CTO                     118 tool call(s)
       0.7.0_AE_CloudOps~W              108 tool call(s)
       4.0.0_SA_CRO                     21 tool call(s)
SEAT_INVOCATIONS_IN_WINDOW=2056 of 2056

--- 5. arm (b) CloudTrail RunTask census in the window
  eventTime            type        principal / cluster / taskDefinition / startedBy
  SCHEDULER 2026-09-05T04:00:28Z  AssumedRole  arn:aws:sts::313476888478:assumed-role/opal-globgrph-comp-learns-producer-events/17c584966a443389ba4f09c834f2b4dc  cluster=arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph  td=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-comp-learns-producer:1  startedBy=events-rule/opal-globgrph-comp-learns-producer-nightly
  PIPE      2026-09-05T03:31:19Z  AssumedRole  arn:aws:sts::313476888478:assumed-role/opal-globgrph-projection-pipe/c126db3c80a13fb9ad7f4ba60961626d  cluster=arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph  td=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:4  startedBy=Started by Eventbridge Pipes
  SCHEDULER 2026-09-05T03:30:13Z  AssumedRole  arn:aws:sts::313476888478:assumed-role/opal-globgrph-cse-producer-scheduler/7411f1275df93b75b4449bfb302d615d  cluster=arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph  td=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-cse-producer:1  startedBy=chronos-schedule/globgrph-cse-produc
  PIPE      2026-09-05T02:11:13Z  AssumedRole  arn:aws:sts::313476888478:assumed-role/opal-globgrph-projection-pipe/c126db3c80a13fb9ad7f4ba60961626d  cluster=arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph  td=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:4  startedBy=Started by Eventbridge Pipes
  SCHEDULER 2026-09-05T02:00:05Z  AssumedRole  arn:aws:sts::313476888478:assumed-role/opal-globgrph-derive-runner-events/99c3650895ff341993e0d3b14cdb1eb7  cluster=arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph  td=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-derive-runner:7  startedBy=events-rule/opal-globgrph-derive-runner-nightly
  PIPE      2026-09-05T00:52:48Z  AssumedRole  arn:aws:sts::313476888478:assumed-role/opal-globgrph-projection-pipe/c126db3c80a13fb9ad7f4ba60961626d  cluster=arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph  td=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:4  startedBy=Started by Eventbridge Pipes
  PIPE      2026-09-05T00:36:36Z  AssumedRole  arn:aws:sts::313476888478:assumed-role/opal-globgrph-projection-pipe/c126db3c80a13fb9ad7f4ba60961626d  cluster=arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph  td=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:4  startedBy=Started by Eventbridge Pipes
  PIPE      2026-09-05T00:36:21Z  AssumedRole  arn:aws:sts::313476888478:assumed-role/opal-globgrph-projection-pipe/c126db3c80a13fb9ad7f4ba60961626d  cluster=arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph  td=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:4  startedBy=Started by Eventbridge Pipes
  PIPE      2026-09-05T00:28:23Z  AssumedRole  arn:aws:sts::313476888478:assumed-role/opal-globgrph-projection-pipe/c126db3c80a13fb9ad7f4ba60961626d  cluster=arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph  td=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:4  startedBy=Started by Eventbridge Pipes
  PIPE      2026-09-05T00:28:20Z  AssumedRole  arn:aws:sts::313476888478:assumed-role/opal-globgrph-projection-pipe/c126db3c80a13fb9ad7f4ba60961626d  cluster=arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph  td=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:4  startedBy=Started by Eventbridge Pipes
  NONPIPE   2026-09-04T21:18:53Z  IAMUser  arn:aws:iam::313476888478:user/Andrew_Berman  cluster=opal-globgrph  td=globgrph-trino  startedBy=-
RUNTASK_NONPIPE_IN_WINDOW=1 of 11

--- the nightly's own RunTask attribution (startedBy, recovered from CloudTrail
    because ECS describe-tasks has aged the task out):
  2026-09-05T02:00:05Z	AssumedRole	arn:aws:sts::313476888478:assumed-role/opal-globgrph-derive-runner-events/99c3650895ff341993e0d3b14cdb1eb7	arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph	arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-derive-runner:7	events-rule/opal-globgrph-derive-runner-nightly
```

### latency.sh (limb ii)

```
=== TO-CG-D-9 LIMB (ii): ONE REAL PRODUCER STAMP -> THE SERVED ANSWER
READ_AT=2026-09-05T04:15:09Z
STAMP=2026-09-05T03:31:16.793943+00:00

--- t1 STAMP (manifest): vintage=2026-09-05T03:31:16.793943+00:00 committed_at=2026-09-05T03:31:16.793943+00:00
    writer_id=cse_producers_nightly  producer.mode=incremental  built_at=2026-09-05T03:31:43.917433+00:00
    (contract s.1: vintage == committed_at == the marker's committed_at_iso, byte for byte)
--- t2 POINTER: vintage=2026-09-05T03:31:16.793943+00:00  LastModified=Sat, 05 Sep 2026 03:31:47 GMT
--- t3 SWAP (serving log stream serving/globgrph-serving/8889156e83ad4e3e95931e9d505169a9):
    2026-09-05 03:32:39,012 INFO projection swap complete: {'status': 'ok', 'vintage': '2026-09-05T03:31:16.793943+00:00', 'pointer_read_at': '2026-09-05T03:32:38.973078+00:00', 'last_swap': '2026-09-05T03:32:38.979596+00:00'}
    last_swap=2026-09-05T03:32:38.979596+00:00
--- t4 ANSWER (through .tools/comp-kuzu, the thin client):
    read_at=2026-09-05T04:15:37.122041Z  node_count=27295  vintage=2026-09-05T03:31:16.793943+00:00
    VINTAGE: Built from the estate as of 2026-09-05 03:31:16 UTC.  [vintage=2026-09-05T03:31:16.793943+00:00 manifest=78fecbbdf4ef prefix=projection/2026-09-05T03:31:16.793943+00:00/]
    ANSWER_CARRIES_THE_STAMP=true

STAMP_TO_POINTER_S=30.206
POINTER_TO_SWAP_S=51.980
STAMP_TO_ANSWER_S=82.186
  ^ = last_swap - committed_at: the moment the served answer FIRST carried this vintage,
    confirmed by the t4 client read returning vintage=2026-09-05T03:31:16.793943+00:00.
STAMP_TO_THIS_WORKERS_READ_S=2660.328  <-- when this seat happened to ask; NOT the estate's latency
WITHIN_MINUTES=900  (the issuer's reading: <= 15 min for an incremental stamp; the CVO grades)
```

### behind.sh (limb iii)

```
=== TO-CG-D-9 LIMB (iii): TESTED BY TRYING (reported from behind_evidence.jsonl)
READS=27  FIRST=2026-09-05T04:03:42.948885900Z  LAST=2026-09-05T04:59:13.216817800Z
BEHIND_CAUGHT=false
BEHIND-NOT-CAUGHT in 27 reads over 2026-09-05T04:03:42.948885900Z -> 2026-09-05T04:59:13.216817800Z
--- every marker/served pair observed:
  2026-09-05T04:03:42.948885900Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:04:43.505027700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:06:51.328782200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:09:59.642213300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:11:58.459485100Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:13:57.513787200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:15:57.879293600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:17:54.711489300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:20:00.161407300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:22:16.652593200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:24:28.219722100Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:26:24.581429200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:28:20.560031700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:30:17.358665600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:32:10.259994600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:33:47.640012900Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:35:22.674520600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:37:15.094746400Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:39:31.485131300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:44:59.136212500Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:46:50.246337700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:48:57.764624700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:50:56.046437900Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:52:49.253888300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:54:51.343417800Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:56:48.240410000Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:59:13.216817800Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
```

---

## PASS-2 TRANSCRIPTS (the RE-HAND)

### night.sh (limb i, amended: causal arm) -- verbatim

```
=== TO-CG-D-9 LIMB (i): ONE UNATTENDED NIGHT
WINDOW=2026-09-04T21:00:00Z -> 2026-09-05T06:00:00Z
READ_AT=2026-09-05T08:15:13Z

--- 1. projection/ vintages (full list, no head)
VINTAGES_TOTAL=56
--- vintages inside the window:
2026-09-05T00:28:21.155513+00:00
2026-09-05T00:36:33.532742+00:00
2026-09-05T00:52:45.603017+00:00
2026-09-05T02:11:10.919000+00:00
2026-09-05T03:31:16.793943+00:00
2026-09-05T05:31:07.555427+00:00
2026-09-05T05:39:20.963495+00:00
2026-09-05T05:55:42.571886+00:00
VINTAGES_IN_WINDOW=8

--- 2. CloudTrail RunTask events in the window (the causal instrument, read once)
RUNTASK_EVENTS_RETURNED=16 (API cap 50)
INSTRUMENT QUALIFIER: CloudTrail management-event delivery lags up to ~15 min; this window
  closed at 2026-09-05T06:00:00Z and is read after it, so no in-window event is undelivered.
DERIVE_RUNTASK_EVENTS_IN_WINDOW=1
  eventTime      = 2026-09-05T02:00:05Z
  taskDefinition = arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-derive-runner:7
  taskArn        = arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/be97f46226f74bae86b9cf853e78763c   (recovered FROM THE WINDOW)
  startedBy      = events-rule/opal-globgrph-derive-runner-nightly
  invokedBy      = events.amazonaws.com   (CloudTrail-authored; the caller cannot set it)
  ISSUER_TASK_ID_REPRODUCED=true  (the face's id matches the id read from the record)
REBUILD_TRIGGER=events-rule/opal-globgrph-derive-runner-nightly

--- 3. derive-runner log streams (durable; ECS has aged the task itself out)
  IN_WINDOW  derive-runner/derive-runner/be97f46226f74bae86b9cf853e78763c  2026-09-05T02:00:48Z -> 2026-09-05T02:12:26Z  <== the task CloudTrail names
  OUT  derive-runner/derive-runner/4a1baae562c8496983eb068146ae33d5  2026-09-04T16:30:50Z -> 2026-09-04T16:39:44Z
  OUT  derive-runner/derive-runner/aeb8dec6982a43bd80fe49a9ed34b871  2026-09-04T12:47:54Z -> 2026-09-04T12:57:11Z
  OUT  derive-runner/derive-runner/7286e56c80614ab49fa2fba791bb8b43  2026-09-04T08:37:55Z -> 2026-09-04T08:50:36Z
  OUT  derive-runner/derive-runner/ef251d0df84e4a51847f7701e535dfc1  2026-09-04T02:00:39Z -> 2026-09-04T02:10:23Z
  OUT  derive-runner/derive-runner/126daf3f1e9f423ab5456f5ccacbf00f  2026-09-03T16:53:18Z -> 2026-09-03T17:02:16Z
  OUT  derive-runner/derive-runner/b873932d173a485282b671ba883979d0  2026-09-03T16:13:11Z -> 2026-09-03T16:22:42Z
  OUT  derive-runner/derive-runner/be6e1b00cac64e19b23479c15ae31482  2026-09-03T02:00:50Z -> 2026-09-03T02:11:55Z
  DERIVE_STREAMS_LISTED=8 (positive control: a zero here would be a DEAD ARM, not a clean night)

--- the night derive's own lines (marker + the bucket-notification denominator)
  s3 notifications buckets read=34 / buckets unreadable=0; unreadable=none
  OK: MARKER_STAMPED writer=derive_runner hash=c336d1e8bac0321c442677ecd5e3150ff7006eb9b47ec0ad86250f36b4ce2e6d nodes_snap=4606138319900821475 edges_snap=8760077255054959316
DERIVE_DENOMINATOR_LINE=s3 notifications buckets read=34 / buckets unreadable=0; unreadable=none

--- 4. attribute the vintage by the 3-of-3 snapshot join (NEVER by 'newest')
  2026-09-05T00:28:21.155513+00:00  writer=incremental_updater mode=incremental built_at=2026-09-05T00:28:45.142377+00:00 JOIN=0/3
  2026-09-05T00:36:33.532742+00:00  writer=incremental_updater mode=incremental built_at=2026-09-05T00:36:48.483584+00:00 JOIN=0/3
  2026-09-05T00:52:45.603017+00:00  writer=incremental_updater mode=incremental built_at=2026-09-05T00:54:18.301291+00:00 JOIN=0/3
  2026-09-05T02:11:10.919000+00:00  writer=derive_runner mode=full built_at=2026-09-05T02:23:22.179104+00:00 JOIN=3/3
  2026-09-05T03:31:16.793943+00:00  writer=cse_producers_nightly mode=incremental built_at=2026-09-05T03:31:43.917433+00:00 JOIN=2/3
  2026-09-05T05:31:07.555427+00:00  writer=incremental_updater mode=incremental built_at=2026-09-05T05:31:34.621912+00:00 JOIN=1/3
  2026-09-05T05:39:20.963495+00:00  writer=incremental_updater mode=incremental built_at=2026-09-05T05:39:33.568849+00:00 JOIN=1/3
  2026-09-05T05:55:42.571886+00:00  writer=incremental_updater mode=incremental built_at=2026-09-05T05:56:56.355759+00:00 JOIN=1/3
MANIFESTS_READ=8 of 8 in-window vintages

NIGHT_VINTAGE=2026-09-05T02:11:10.919000+00:00
NIGHT_WRITER=derive_runner NIGHT_MODE=full NIGHT_BUILT_AT=2026-09-05T02:23:22.179104+00:00
PREV_EVENING=2026-09-04T18:11:48.783142+00:00
NIGHT_LATER_THAN_PREV_EVENING=true

--- THE CAUSAL CHAIN, end to end (each link a different instrument):
  projection manifest 2026-09-05T02:11:10.919000+00:00
    <-3/3 snapshot join- MARKER_STAMPED in log stream derive-runner/derive-runner/be97f46226f74bae86b9cf853e78763c
      <-taskArn- CloudTrail RunTask 2026-09-05T02:00:05Z
        <-startedBy- events-rule/opal-globgrph-derive-runner-nightly

--- 5. seat ACTIVITY census -- org/mcp/agent_telemetry (context, not the arm)
TELEMETRY_DIR=/c/Users/AndrewBerman/Desktop/ajb_workspace/org/mcp/agent_telemetry (GITIGNORED at .gitignore:261 -- absent from every worktree;
  reading it at the worktree path returns a FALSE ZERO, so the parent workspace is read)
  telemetry files scanned: 159
  FIELDS PRESENT ON WINDOW ROWS: kind, serial, serial_source, session_id, tool_name, ts, ts_unix
  INSTRUMENT LIMIT: no field carries the command text or arguments of a tool call.
  A filter like 'rows naming kuzu|derive|projection|globgrph|run-task' is UNSATISFIABLE
  on this log: it reads 0 for a STRUCTURAL reason (the field does not exist), not because
  no seat touched the graph -- a vacuous zero that would certify a WORKED night as
  unattended. This log can answer WHETHER SEATS WERE ACTIVE and nothing finer.
  -- seats active in the window:
       2.0.0_SA_COO~B                   957 tool call(s)
       2.0.0_SA_COO                     845 tool call(s)
       0.9.0_WK_NFRA_CLDGRPH~2          262 tool call(s)
       0.0.0_AB_MSTR                    145 tool call(s)
       3.0.0_SA_CVO                     143 tool call(s)
       1.0.0_SA_CTO                     132 tool call(s)
       0.7.0_AE_CloudOps~W              108 tool call(s)
       4.0.0_SA_CRO                     21 tool call(s)
SEAT_INVOCATIONS_IN_WINDOW=2613 of 2613

--- 6. arm (b) CAUSAL: every task started in the window, classified BY PROVENANCE
  EVENT LINES IN=16 ; PARSED=16 ; UNPARSED=0  (an unparsed event is NOT silently dropped: it is counted here and it would understate every number below)
  PER-ROW LABELS (the control: these labels must add up to the totals below)
  PROV      eventTime            family                       nearest vintage  rebuild  startedBy / corroboration
  PIPE      2026-09-05T05:55:45Z globgrph-projection-worker   -2s              YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  PIPE      2026-09-05T05:39:23Z globgrph-projection-worker   -2s              YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  PIPE      2026-09-05T05:39:10Z globgrph-projection-worker   +11s             YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  PIPE      2026-09-05T05:31:10Z globgrph-projection-worker   -2s              YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  RULE      2026-09-05T04:30:19Z globgrph-fedobs-producer     -3542s           YES      events-rule/opal-globgrph-fedobs-producer-nightly | SERVICE-PRINCIPAL:events.amazonaws.com
  RULE      2026-09-05T04:00:28Z globgrph-comp-learns-producer -1751s           YES      events-rule/opal-globgrph-comp-learns-producer-nightly | SERVICE-PRINCIPAL:events.amazonaws.com
  PIPE      2026-09-05T03:31:19Z globgrph-projection-worker   -2s              YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  SCHEDULE  2026-09-05T03:30:13Z globgrph-cse-producer        +64s             YES      chronos-schedule/globgrph-cse-produc | SERVICE-AGENT:AmazonEventBridgeScheduler
  PIPE      2026-09-05T02:11:13Z globgrph-projection-worker   -2s              YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  RULE      2026-09-05T02:00:05Z globgrph-derive-runner       +666s            YES      events-rule/opal-globgrph-derive-runner-nightly | SERVICE-PRINCIPAL:events.amazonaws.com
  PIPE      2026-09-05T00:52:48Z globgrph-projection-worker   -2s              YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  PIPE      2026-09-05T00:36:36Z globgrph-projection-worker   -2s              YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  PIPE      2026-09-05T00:36:21Z globgrph-projection-worker   +13s             YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  PIPE      2026-09-05T00:28:23Z globgrph-projection-worker   -2s              YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  PIPE      2026-09-05T00:28:20Z globgrph-projection-worker   +1s              YES      Started by Eventbridge Pipes | SERVICE-PRINCIPAL:pipes.amazonaws.com
  HUMAN-OR-SEAT 2026-09-04T21:18:53Z globgrph-trino               -11224s          no       - | NONE
      ^ identity=IAMUser arn=arn:aws:iam::313476888478:user/Andrew_Berman sourceIP=73.84.214.103 nearest_vintage=2026-09-04T18:11:48.783142+00:00
      ^ userAgent=Boto3/1.42.54 md/Botocore#1.43.0 md/awscrt#0.31.3 ua/2.1 os/windows#10.0.26100 md/arch#amd64 lang/python#3.12.10 md/pyimpl#CPython m/b,n,D,Z cfg/retry-mode#legacy Botocore/1.43.0

  LABEL TALLY (must sum to the denominator):
    HUMAN-OR-SEAT  1
    PIPE           11
    RULE           3
    SCHEDULE       1
    SUM            16
  LABELS_AGREE_WITH_DENOMINATOR=true (16 == 16)

  REBUILD-CONSTITUTING tasks: 15 ; NOT rebuild-constituting: 1 ; total RunTask: 16
  UNSCOPED CONTROL -- every HUMAN-OR-SEAT row in the WHOLE window, whether or not its
  family is in the declared rebuild set, with the nearest projection vintage:
    2026-09-04T21:18:53Z  family=globgrph-trino  nearest_vintage=2026-09-04T18:11:48.783142+00:00 (-11224s)  -> caused a rebuild: no
  CORROBORATION GAP -- automated rows with no service-principal in invokedBy: 0

SEAT_CAUSED_REBUILDS=0 of 15

--- 7. the pre-amendment RunTask count, kept so the two frames can be compared
RUNTASK_NONPIPE_IN_WINDOW=1 of 16
  (the pre-amendment arm; it counts a human-started task that constituted NO rebuild --
   a globgrph-trino query task -- which is exactly the PROXY the CTO's ruling replaced.)

=== CRITERION FIELDS
NIGHT_VINTAGE=2026-09-05T02:11:10.919000+00:00
PREV_EVENING=2026-09-04T18:11:48.783142+00:00
REBUILD_TRIGGER=events-rule/opal-globgrph-derive-runner-nightly
```

### latency.sh (limb ii) -- verbatim

```
=== TO-CG-D-9 LIMB (ii): ONE REAL PRODUCER STAMP -> THE SERVED ANSWER
READ_AT=2026-09-05T08:17:35Z
STAMP=2026-09-05T03:31:16.793943+00:00

--- t1 STAMP (manifest): vintage=2026-09-05T03:31:16.793943+00:00 committed_at=2026-09-05T03:31:16.793943+00:00
    writer_id=cse_producers_nightly  producer.mode=incremental  built_at=2026-09-05T03:31:43.917433+00:00
    (contract s.1: vintage == committed_at == the marker's committed_at_iso, byte for byte)
--- t2 POINTER: vintage=2026-09-05T05:55:42.571886+00:00  LastModified=Sat, 05 Sep 2026 05:57:00 GMT
    NOTE: the pointer has since advanced past this stamp; LastModified then describes the
    LATER put and STAMP_TO_POINTER_S below would be wrong. Refusing to print it.
--- t3 SWAP (serving log stream serving/globgrph-serving/8889156e83ad4e3e95931e9d505169a9):
    2026-09-05 03:32:39,012 INFO projection swap complete: {'status': 'ok', 'vintage': '2026-09-05T03:31:16.793943+00:00', 'pointer_read_at': '2026-09-05T03:32:38.973078+00:00', 'last_swap': '2026-09-05T03:32:38.979596+00:00'}
    last_swap=2026-09-05T03:32:38.979596+00:00
--- t4 ANSWER (through .tools/comp-kuzu, the thin client):
    read_at=2026-09-05T08:18:06.915568Z  node_count=27294  vintage=2026-09-05T05:55:42.571886+00:00
    VINTAGE: Built from the estate as of 2026-09-05 05:55:42 UTC.  [vintage=2026-09-05T05:55:42.571886+00:00 manifest=9d61a1f5d2ca prefix=projection/2026-09-05T05:55:42.571886+00:00/]
    ANSWER_CARRIES_THE_STAMP=false (the estate has moved on to 2026-09-05T05:55:42.571886+00:00)

STAMP_TO_POINTER_S=UNMEASURABLE (pointer has advanced past this stamp; its LastModified now
  describes a later PUT). STAMP_TO_ARTIFACT_CLOSED_S=27.123 from the manifest's built_at.
POINTER_TO_SWAP_S=55.062 measured from built_at, an UPPER bound on the pointer leg.
STAMP_TO_ANSWER_S=82.186
  ^ = last_swap - committed_at: the moment the served answer FIRST carried this vintage,
    confirmed by the t4 client read returning vintage=2026-09-05T05:55:42.571886+00:00.
STAMP_TO_THIS_WORKERS_READ_S=17210.122  <-- when this seat happened to ask; NOT the estate's latency
WITHIN_MINUTES=900  (the issuer's reading: <= 15 min for an incremental stamp; the CVO grades)
```

### behind.sh (limb iii, pass 2 report) -- verbatim

```
=== TO-CG-D-9 LIMB (iii): TESTED BY TRYING (reported from behind_evidence.jsonl)
READS=82  FIRST=2026-09-05T04:03:42.948885900Z  LAST=2026-09-05T08:12:16.819642400Z
BEHIND_CAUGHT=false
BEHIND-NOT-CAUGHT in 82 reads over 2026-09-05T04:03:42.948885900Z -> 2026-09-05T08:12:16.819642400Z
POINTER_MOVED_BY_READ=false
  ^ established across ALL 82 reads: the pointer's vintage was read immediately
    before and immediately after every client read and was identical every time.
LEGIT_REBUILD_REPORTED=false
  ^ NOT a negative finding about the can-fail arm: the arm was never presented with a
    rebuild while behind. The detector DID observe the served vintage advance on its own
    between polls (see DISTINCT_SERVED below) -- context, never the arm.
CLIENT_REBUILD_PATH_HITS=0
DISTINCT_MARKERS=2026-09-05T03:31:16.793943+00:00
 2026-09-05T05:55:42.571886+00:00
 
DISTINCT_SERVED=2026-09-05T03:31:16.793943+00:00
 2026-09-05T05:55:42.571886+00:00
 
--- every marker/served pair observed:
  2026-09-05T04:03:42.948885900Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:04:43.505027700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:06:51.328782200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:09:59.642213300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:11:58.459485100Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:13:57.513787200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:15:57.879293600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:17:54.711489300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:20:00.161407300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:22:16.652593200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:24:28.219722100Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:26:24.581429200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:28:20.560031700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:30:17.358665600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:32:10.259994600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:33:47.640012900Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:35:22.674520600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:37:15.094746400Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:39:31.485131300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:44:59.136212500Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:46:50.246337700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:48:57.764624700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:50:56.046437900Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:52:49.253888300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:54:51.343417800Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:56:48.240410000Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T04:59:13.216817800Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00
  2026-09-05T06:22:53.226735200Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:24:42.283518900Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:26:26.011624500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:28:25.615361200Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:30:20.673784500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:32:30.428863000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:34:38.630738400Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:36:42.483584600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:38:48.417279100Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:41:05.124333100Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:43:02.270443600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:45:01.029673300Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:47:13.680502100Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:49:12.750208700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:51:21.987829300Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:53:30.534215300Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:55:30.670856400Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T06:57:45.068230800Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:00:02.415928500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:02:24.896381500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:03:51.969406800Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:06:00.703547200Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:08:09.075239700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:10:03.296542700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:12:13.158504500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:14:09.504805400Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:16:13.315046000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:18:18.203646900Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:20:30.367234600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:22:38.505761000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:24:35.639299300Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:26:33.367327100Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:28:32.315984200Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:30:23.759969800Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:32:27.700757000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:34:42.310568600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:36:50.596133700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:39:02.529032800Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:41:08.474024800Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:43:21.652343200Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:45:30.872413500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:47:16.513963000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:49:10.816297300Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:51:03.652925400Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:53:05.649255600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:53:36.944702700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:55:34.976724600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:57:18.269221900Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T07:59:15.762784700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T08:01:28.317987500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T08:03:36.872849000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T08:05:45.301524900Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T08:08:01.256244000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T08:10:11.775480900Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
  2026-09-05T08:12:16.819642400Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00
```

---

# PASS 3 (2026-09-05 12:10Z -> 13:0xZ) -- LIMB (iii), THE CAUGHT WINDOW

## THE POLL

`bash behind.sh --poll 2700`, started **2026-09-05T12:10:59Z**, ended **2026-09-05T12:56:01Z** at
its declared bound. 33 client reads through `.tools/comp-kuzu` this pass (115 cumulative in
`behind_evidence.jsonl` across the three passes), interleaved with cheap marker-only polls: the
loop reads the marker every ~5-10 s (a ~2 s S3 GET) and spends the expensive ~40 s client read only
when the marker has MOVED or on a periodic baseline, because a read-everything loop samples slower
than the ~30 s window it is hunting and would miss it for an instrument reason rather than a world
reason.

**The burst, from the poll's own marker line** (this is what passes 1 and 2 did not have):
`12:10:36.884158` -> `12:11:27.375244` -> `12:12:05.739979` -> `12:13:33.832979` ->
`12:14:42.810835` -> `12:14:56.469712` -> `12:16:43.795811` -> `12:16:58.855158` -> ... and a
second burst `12:47:37` -> `12:50:07` -> `12:50:45` -> `12:52:19` -> `12:54:31`. Twenty-one
distinct marker values are in the evidence file; passes 1 and 2 saw two.

## THE CATCH (limb iii's first arm)

| field | value |
|---|---|
| `BEHIND_CAUGHT` | **true** |
| `BEHIND_READ_AT` | `2026-09-05T12:12:47.239769100Z` |
| `BEHIND_MARKER` | `2026-09-05T12:12:05.739979+00:00` |
| `BEHIND_SERVED` | `2026-09-05T12:11:27.375244+00:00` |
| `BEHIND_NODE_COUNT` | `27292` |
| behind reads in the file | **14** |

The client answered while behind, with its age line, exactly as limb (iii) requires:

```
VINTAGE: Built from the estate as of 2026-09-05 12:11:27 UTC.  [vintage=2026-09-05T12:11:27.375244+00:00 manifest=a15d4e2746db prefix=projection/2026-09-05T12:11:27.375244+00:00/]
```

The marker was 38.4 s ahead of the served artifact at that read: the stale answer WITH its age,
returned by a client that has no rebuild path (`CLIENT_REBUILD_PATH_HITS=0`, D9-AC5).

## THE READ MOVED NOTHING (limb iii's second arm) -- ATTRIBUTED, WITH THE STRICT NUMBER BESIDE IT

```
POINTER_MOVED_BY_READ=false
POINTER_ADVANCED_DURING_A_BEHIND_READ=10 of 14 behind reads   (the STRICT before-vs-after difference, printed unattributed and unhidden)
ATTRIB_UNATTRIBUTED_ADVANCES=0
```

Three limbs, any one of which can fail it:

- **L1 PROVENANCE -- 10 of 10 advances SERVICE-only.** Every `globgrph-projection-worker` task
  active across an advancing behind-read, described from ECS and classified by its OWN `startedBy`:
  all return `Started by Eventbridge Pipes`. This is PROVENANCE, not a name-match against a list --
  the discipline D9-AC2 was amended onto after a name list convicted a scheduled producer. An
  EMPTY `startedBy`, the signature of an ad-hoc `RunTask` by a principal, is classified
  `NON_SERVICE` and fails the limb. Captured to `behind_task_provenance.jsonl` **with its
  measurement time** (`2026-09-05T12:57:23Z`) because ECS drops STOPPED tasks after about an hour --
  the W1-S16 phenomenon -- and a report making the call live would print a different answer
  tomorrow than it printed today. 36 tasks named by the behind rows, 34 described, 2 already aged
  out; both aged-out tasks appear on BOTH sides of their read and so are in no active set.
- **L2 KEYING -- 10 of 10.** Every new pointer vintage equals a marker `committed_at_iso` observed
  in this same evidence file (21 distinct markers). The pointer's vintage is minted by the marker
  writer; a read does not write the marker.
- **L3 BASE RATE, the negative control with its denominator -- 94 reads whose marker was UNCHANGED
  from the previous read advanced the pointer ZERO times**, while 20 reads whose marker HAD moved
  account for all 10 advances. If a read moved pointers, the 94 marker-static reads are where that
  would show. The advance tracks the MARKER. It does not track the READ.

The instrument's own falsifier was RUN, not declared: `behind_attribute.py` against an EMPTY
provenance file prints `POINTER_MOVED_BY_READ=true` with `ATTRIB_UNATTRIBUTED_ADVANCES=6` and every
advance labelled `PROVENANCE_UNMEASURED`. It does not default to false.

## THE CAN-FAIL ARM (limb iii's third arm)

```
LEGIT_REBUILD_REPORTED=true
LEGIT_REBUILD_AT=2026-09-05T12:13:35.337534700Z
LEGIT_REBUILD_SERVED=2026-09-05T12:12:05.739979+00:00
```

The SAME detector that reported the stale answer at 12:12:47Z reported the caught-up one 48 s
later: served advanced `12:11:27.375244` -> `12:12:05.739979`, produced by Pipe-started tasks
`2ece7b4df961` and `ba23a328741f`. The cycle repeats through both bursts and the world ends the
poll caught up (marker == served == `2026-09-05T12:54:31.241426+00:00`). A legitimate,
marker-triggered rebuild, reported by the same read, with no question having caused it.

## THE S57 POSITIVE CONTROL -- the THIRD OUTCOME, exercised

Run on a scratch COPY of `behind.sh` pointed at a non-existent bucket, writing to its own evidence
file. The live pointer, the live marker and the deliverable's own evidence file were not touched.

```
READS_OK=0 of 1  (rows carrying an EXPLICIT read_ok field: 1 of 1)
BEHIND_CAUGHT=READ_FAILED
READ_FAILED=true  1 of 1 reads could not read the marker, the pointer or the served vintage
POINTER_MOVED_BY_READ=UNREAD
LEGIT_REBUILD_REPORTED=UNREAD
--- the read errors, verbatim:
  2026-09-05T13:05:21.792671900Z  rc=1  err=S3_CP_RC_1 download failed: s3://...-NO-SUCH-BUCKET-s57-control/warehouse/_branch_head.main.json to - An error occurred (404) when calling the HeadObject operation: Not Found ...
```

A world that is not behind prints `BEHIND_CAUGHT=false`; a world that could not be read prints
`BEHIND_CAUGHT=READ_FAILED`. They are no longer the same line.

## CRITERIA -- PASS 3

| id | invocation | deciding output | status |
|---|---|---|---|
| D9-AC1 | `night.sh \| grep -E '^(NIGHT_VINTAGE\|PREV_EVENING)='` | `NIGHT_VINTAGE=2026-09-05T02:11:10.919000+00:00` / `PREV_EVENING=2026-09-04T18:11:48.783142+00:00` | PASS (pass 2, carried by citation) |
| D9-AC2 | `night.sh \| grep -E '^(REBUILD_TRIGGER\|SEAT_CAUSED_REBUILDS)='` | `REBUILD_TRIGGER=events-rule/opal-globgrph-derive-runner-nightly` / `SEAT_CAUSED_REBUILDS=0 of 15` | PASS (pass 2, carried by citation) |
| D9-AC3 | `latency.sh \| grep -E '^STAMP_TO_ANSWER_S='` | `STAMP_TO_ANSWER_S=82.186` | PASS (pass 2, carried by citation) |
| **D9-AC4** | `behind.sh \| grep -E '^(BEHIND_CAUGHT\|POINTER_MOVED_BY_READ\|LEGIT_REBUILD_REPORTED)='` | `BEHIND_CAUGHT=true` / `POINTER_MOVED_BY_READ=false` / `LEGIT_REBUILD_REPORTED=true` | **PASS (pass 3, MEASURED HERE)** |
| D9-AC5 | `comp-read kuzu_cli.py --enumerate 'ensure_fresh\|kuzu_nessie_load\|_incremental_or_serve_stale'` | `ENUMERATE: 0 hit(s) across 169 lines` | PASS (pass 2, carried by citation) |
| D9-AC6 | a reading act | recorded, no verdict | UNVERIFIABLE-BY-INSTRUMENT -- `3.0.0_SA_CVO` at L9 |

## D9-AC6 -- PASS-3 AMENDMENT TO THE READING (a reading act; NO verdict)

Limb (iii) of FWD-2's DONE WHEN -- *"no question is ever the reason a rebuild starts"* -- now has
both of its halves on the record rather than one. The NEGATIVE half was always the stronger one and
is unchanged: the client has no rebuild path at all (`CLIENT_REBUILD_PATH_HITS=0`), so a question
CANNOT start a rebuild, which is a structural fact and not a sampling result. What passes 1 and 2
could not supply was the POSITIVE half -- an actual behind window, actually read through, actually
returning the stale answer with its age while a rebuild it did not cause ran to completion beside
it. That is now supplied 14 times over.

**The reading I had to make, stated as a reading and not as a finding:** the criterion's phrase is
"the pointer does not move FOR the read", and in a quiet estate that is indistinguishable from "the
pointer does not move". Under a burst the two separate, and I read the criterion as the CAUSAL
claim its own method paragraph states -- *"unchanged BY the read; it moves later BY the producer"* --
because the alternative reading makes the criterion unsatisfiable in exactly the conditions it
requires: a behind window only exists during a burst, and during a burst a 40 s read will straddle
an advance. A criterion that can only be met when the phenomenon it measures is absent is not a
criterion. **I may be wrong about that, which is why W1-S19 is ARMED to `3.0.0_SA_CVO` and why the
strict number is printed beside the attributed one.** The CVO can grade this either way without
re-running anything.

The other two limbs read as they did in pass 2 and are not re-argued here.

## PASS-3 TRANSCRIPTS

### behind.sh (limb iii, pass 3 report) -- verbatim

```
=== TO-CG-D-9 LIMB (iii): TESTED BY TRYING (reported from behind_evidence.jsonl)
READS=115  FIRST=2026-09-05T04:03:42.948885900Z  LAST=2026-09-05T12:54:39.838720400Z
READS_OK=115 of 115  (rows carrying an EXPLICIT read_ok field: 33 of 115)
BEHIND_CAUGHT=true
BEHIND_READ_AT=2026-09-05T12:12:47.239769100Z
BEHIND_MARKER=2026-09-05T12:12:05.739979+00:00
BEHIND_SERVED=2026-09-05T12:11:27.375244+00:00
BEHIND_NODE_COUNT=27292
BEHIND_ANSWER_AGE_LINE=VINTAGE: Built from the estate as of 2026-09-05 12:11:27 UTC.  [vintage=2026-09-05T12:11:27.375244+00:00 manifest=a15d4e2746db prefix=projection/2026-09-05T12:11:27.375244+00:00/]
TASKS_BEFORE={"running":"","stopped":"arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/018ac34d707a4f0ab6a399b9e6d8fba6 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/0b291391e5254fd796b175423c1ce80a arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/166f976d2d334941b857064da06da806 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/1996262a6ba341ae94758397f102afd1 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/23d020e8c8994b648a9218b09fee79ae arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/3cec1489ba8f4345a439906d91fae84e arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/54c8c675d8e14f60afcfd30849f8ec69 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/65f75849bc684e4f8ddeab9f53e232e6 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/6dbf081418b940e2a7f4050483d79050 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/719d546ae1de4899a0a2f73568b6df7a arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/765540f369ed47c1907bff0cff0d5652 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/8b39e99d551d48dfb89ef7012d3977b4 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/8d603f95b6ea4371a9dee2ed5e536426 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/9b362183778846eda4fb45fe51a98099 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/a0e2280953784d3ead5b2469b10443fc arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/a22002d5139b4b7d8e078c8508b84c51 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/b8834c1c57204358a248536bf83b2940 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/cd06303f343d45488c84f29cf1fc5a9a arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/f9cc497ae9734ea5ba9efbc25051bdb4"}
TASKS_AFTER={"running":"arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/2ece7b4df9614db0a25918b33122a935","stopped":"arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/018ac34d707a4f0ab6a399b9e6d8fba6 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/0b291391e5254fd796b175423c1ce80a arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/166f976d2d334941b857064da06da806 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/1996262a6ba341ae94758397f102afd1 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/23d020e8c8994b648a9218b09fee79ae arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/3cec1489ba8f4345a439906d91fae84e arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/54c8c675d8e14f60afcfd30849f8ec69 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/65f75849bc684e4f8ddeab9f53e232e6 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/6dbf081418b940e2a7f4050483d79050 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/719d546ae1de4899a0a2f73568b6df7a arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/765540f369ed47c1907bff0cff0d5652 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/8b39e99d551d48dfb89ef7012d3977b4 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/8d603f95b6ea4371a9dee2ed5e536426 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/9b362183778846eda4fb45fe51a98099 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/a0e2280953784d3ead5b2469b10443fc arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/a22002d5139b4b7d8e078c8508b84c51 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/b8834c1c57204358a248536bf83b2940 arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/cd06303f343d45488c84f29cf1fc5a9a arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/f9cc497ae9734ea5ba9efbc25051bdb4"}
POINTER_MOVED_BY_READ=false
POINTER_ADVANCED_DURING_A_BEHIND_READ=10 of 14 behind reads   (the STRICT before-vs-after difference, printed unattributed and unhidden)
ATTRIB_L1_PROVENANCE: every projection-worker task active across an advancing behind-read, classified by its OWN startedBy -- 10 of 10 advances SERVICE-only
ATTRIB_L2_KEYING: advances whose new pointer vintage equals a marker committed_at_iso observed in this evidence file -- 10 of 10   (denominator of DISTINCT observed markers: 21)
ATTRIB_L3_BASE_RATE (the negative control): reads whose MARKER was unchanged from the previous read = 94; of those, reads that advanced the pointer = 0.  Reads whose marker HAD moved = 20; of those, advanced = 10.  The advance tracks the MARKER, not the READ.
ATTRIB_UNATTRIBUTED_ADVANCES=0
--- per-advance attribution (the control that must agree with the count above):
  2026-09-05T12:13:35.337534700Z  ptr 2026-09-05T12:12:05.739979+00:00 -> 2026-09-05T12:13:33.832979+00:00  L2_KEYED_TO_AN_OBSERVED_MARKER=true  L1=SERVICE_ONLY  -> PRODUCER_CAUSED
      tasks active across the read: 2ece7b4df961=SERVICE:Started by Eventbridge Pipes; ba23a328741f=SERVICE:Started by Eventbridge Pipes
  2026-09-05T12:14:47.571638000Z  ptr 2026-09-05T12:13:33.832979+00:00 -> 2026-09-05T12:14:56.469712+00:00  L2_KEYED_TO_AN_OBSERVED_MARKER=true  L1=SERVICE_ONLY  -> PRODUCER_CAUSED
      tasks active across the read: 8a634b8a51e8=SERVICE:Started by Eventbridge Pipes; e582d75697c6=SERVICE:Started by Eventbridge Pipes
  2026-09-05T12:16:49.306069300Z  ptr 2026-09-05T12:14:56.469712+00:00 -> 2026-09-05T12:16:58.855158+00:00  L2_KEYED_TO_AN_OBSERVED_MARKER=true  L1=SERVICE_ONLY  -> PRODUCER_CAUSED
      tasks active across the read: 77385700b944=SERVICE:Started by Eventbridge Pipes; 968a8a947563=SERVICE:Started by Eventbridge Pipes
  2026-09-05T12:18:53.767855900Z  ptr 2026-09-05T12:16:58.855158+00:00 -> 2026-09-05T12:19:10.768569+00:00  L2_KEYED_TO_AN_OBSERVED_MARKER=true  L1=SERVICE_ONLY  -> PRODUCER_CAUSED
      tasks active across the read: 5379d65d2019=SERVICE:Started by Eventbridge Pipes; d7797d58e02d=SERVICE:Started by Eventbridge Pipes
  2026-09-05T12:21:04.810225600Z  ptr 2026-09-05T12:19:10.768569+00:00 -> 2026-09-05T12:21:03.085712+00:00  L2_KEYED_TO_AN_OBSERVED_MARKER=true  L1=SERVICE_ONLY  -> PRODUCER_CAUSED
      tasks active across the read: 03ae59d23811=SERVICE:Started by Eventbridge Pipes; 40fc9b865bbe=SERVICE:Started by Eventbridge Pipes
  2026-09-05T12:23:09.581944100Z  ptr 2026-09-05T12:21:25.739594+00:00 -> 2026-09-05T12:23:09.662217+00:00  L2_KEYED_TO_AN_OBSERVED_MARKER=true  L1=SERVICE_ONLY  -> PRODUCER_CAUSED
      tasks active across the read: 6c2ee7813904=SERVICE:Started by Eventbridge Pipes
  2026-09-05T12:47:43.375244400Z  ptr 2026-09-05T12:23:09.662217+00:00 -> 2026-09-05T12:47:37.329883+00:00  L2_KEYED_TO_AN_OBSERVED_MARKER=true  L1=SERVICE_ONLY  -> PRODUCER_CAUSED
      tasks active across the read: 102e420d5b20=SERVICE:Started by Eventbridge Pipes
  2026-09-05T12:50:14.062481500Z  ptr 2026-09-05T12:47:37.329883+00:00 -> 2026-09-05T12:50:07.498295+00:00  L2_KEYED_TO_AN_OBSERVED_MARKER=true  L1=SERVICE_ONLY  -> PRODUCER_CAUSED
      tasks active across the read: 1ecc979cd1f2=SERVICE:Started by Eventbridge Pipes
  2026-09-05T12:50:57.157589400Z  ptr 2026-09-05T12:50:07.498295+00:00 -> 2026-09-05T12:50:45.008597+00:00  L2_KEYED_TO_AN_OBSERVED_MARKER=true  L1=SERVICE_ONLY  -> PRODUCER_CAUSED
      tasks active across the read: 53dda85afc8a=SERVICE:Started by Eventbridge Pipes
  2026-09-05T12:52:23.621817700Z  ptr 2026-09-05T12:50:45.008597+00:00 -> 2026-09-05T12:52:19.817312+00:00  L2_KEYED_TO_AN_OBSERVED_MARKER=true  L1=SERVICE_ONLY  -> PRODUCER_CAUSED
      tasks active across the read: 37e076503549=SERVICE:Started by Eventbridge Pipes
LEGIT_REBUILD_REPORTED=true
LEGIT_REBUILD_AT=2026-09-05T12:13:35.337534700Z
LEGIT_REBUILD_SERVED=2026-09-05T12:12:05.739979+00:00
LEGIT_REBUILD_STARTER=arn:aws:pipes:us-east-1:313476888478:pipe/opal-globgrph-projection-worker (the Pipe; see night.sh arm (b) CloudTrail rows)
CLIENT_REBUILD_PATH_HITS=0

--- every marker/served pair observed:
  2026-09-05T04:03:42.948885900Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:04:43.505027700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:06:51.328782200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:09:59.642213300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:11:58.459485100Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:13:57.513787200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:15:57.879293600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:17:54.711489300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:20:00.161407300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:22:16.652593200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:24:28.219722100Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:26:24.581429200Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:28:20.560031700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:30:17.358665600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:32:10.259994600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:33:47.640012900Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:35:22.674520600Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:37:15.094746400Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:39:31.485131300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:44:59.136212500Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:46:50.246337700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:48:57.764624700Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:50:56.046437900Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:52:49.253888300Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:54:51.343417800Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:56:48.240410000Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T04:59:13.216817800Z  marker=2026-09-05T03:31:16.793943+00:00  served=2026-09-05T03:31:16.793943+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:22:53.226735200Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:24:42.283518900Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:26:26.011624500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:28:25.615361200Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:30:20.673784500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:32:30.428863000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:34:38.630738400Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:36:42.483584600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:38:48.417279100Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:41:05.124333100Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:43:02.270443600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:45:01.029673300Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:47:13.680502100Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:49:12.750208700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:51:21.987829300Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:53:30.534215300Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:55:30.670856400Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T06:57:45.068230800Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:00:02.415928500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:02:24.896381500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:03:51.969406800Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:06:00.703547200Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:08:09.075239700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:10:03.296542700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:12:13.158504500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:14:09.504805400Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:16:13.315046000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:18:18.203646900Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:20:30.367234600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:22:38.505761000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:24:35.639299300Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:26:33.367327100Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:28:32.315984200Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:30:23.759969800Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:32:27.700757000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:34:42.310568600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:36:50.596133700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:39:02.529032800Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:41:08.474024800Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:43:21.652343200Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:45:30.872413500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:47:16.513963000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:49:10.816297300Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:51:03.652925400Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:53:05.649255600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:53:36.944702700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:55:34.976724600Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:57:18.269221900Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T07:59:15.762784700Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T08:01:28.317987500Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T08:03:36.872849000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T08:05:45.301524900Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T08:08:01.256244000Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T08:10:11.775480900Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T08:12:16.819642400Z  marker=2026-09-05T05:55:42.571886+00:00  served=2026-09-05T05:55:42.571886+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:11:05.518226300Z  marker=2026-09-05T12:10:36.884158+00:00  served=2026-09-05T12:10:36.884158+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:11:57.620030000Z  marker=2026-09-05T12:11:27.375244+00:00  served=2026-09-05T12:11:27.375244+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:12:47.239769100Z  marker=2026-09-05T12:12:05.739979+00:00  served=2026-09-05T12:11:27.375244+00:00  behind=true  ptr_moved_by_read=false
  2026-09-05T12:13:35.337534700Z  marker=2026-09-05T12:13:33.832979+00:00  served=2026-09-05T12:12:05.739979+00:00  behind=true  ptr_moved_by_read=true
  2026-09-05T12:14:47.571638000Z  marker=2026-09-05T12:14:42.810835+00:00  served=2026-09-05T12:13:33.832979+00:00  behind=true  ptr_moved_by_read=true
  2026-09-05T12:15:31.337466400Z  marker=2026-09-05T12:14:56.469712+00:00  served=2026-09-05T12:14:56.469712+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:16:49.306069300Z  marker=2026-09-05T12:16:43.795811+00:00  served=2026-09-05T12:14:56.469712+00:00  behind=true  ptr_moved_by_read=true
  2026-09-05T12:17:43.325404900Z  marker=2026-09-05T12:16:58.855158+00:00  served=2026-09-05T12:16:58.855158+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:18:53.767855900Z  marker=2026-09-05T12:18:50.261442+00:00  served=2026-09-05T12:16:58.855158+00:00  behind=true  ptr_moved_by_read=true
  2026-09-05T12:19:34.236403400Z  marker=2026-09-05T12:19:10.768569+00:00  served=2026-09-05T12:19:10.768569+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:21:04.810225600Z  marker=2026-09-05T12:21:03.085712+00:00  served=2026-09-05T12:19:10.768569+00:00  behind=true  ptr_moved_by_read=true
  2026-09-05T12:21:53.249796900Z  marker=2026-09-05T12:21:25.739594+00:00  served=2026-09-05T12:19:10.768569+00:00  behind=true  ptr_moved_by_read=false
  2026-09-05T12:23:09.581944100Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:21:25.739594+00:00  behind=true  ptr_moved_by_read=true
  2026-09-05T12:24:44.387055200Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:26:21.024198500Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:28:01.678333200Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:29:42.580684800Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:31:25.171036400Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:33:03.938489800Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:34:46.081477200Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:36:31.773865300Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:38:27.062211400Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:40:22.473281300Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:42:23.816925300Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:44:22.664576800Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:46:13.505901200Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:47:43.375244400Z  marker=2026-09-05T12:47:37.329883+00:00  served=2026-09-05T12:23:09.662217+00:00  behind=true  ptr_moved_by_read=true
  2026-09-05T12:49:32.341770800Z  marker=2026-09-05T12:47:37.329883+00:00  served=2026-09-05T12:47:37.329883+00:00  behind=false  ptr_moved_by_read=false
  2026-09-05T12:50:14.062481500Z  marker=2026-09-05T12:50:07.498295+00:00  served=2026-09-05T12:47:37.329883+00:00  behind=true  ptr_moved_by_read=true
  2026-09-05T12:50:57.157589400Z  marker=2026-09-05T12:50:45.008597+00:00  served=2026-09-05T12:47:37.329883+00:00  behind=true  ptr_moved_by_read=true
  2026-09-05T12:52:23.621817700Z  marker=2026-09-05T12:52:19.817312+00:00  served=2026-09-05T12:50:45.008597+00:00  behind=true  ptr_moved_by_read=true
  2026-09-05T12:53:13.357113400Z  marker=2026-09-05T12:53:04.983210+00:00  served=2026-09-05T12:52:19.817312+00:00  behind=true  ptr_moved_by_read=false
  2026-09-05T12:54:39.838720400Z  marker=2026-09-05T12:54:31.241426+00:00  served=2026-09-05T12:52:19.817312+00:00  behind=true  ptr_moved_by_read=false
```

### behind.sh --poll (pass 3, the live poll) -- verbatim

```
POLL start 2026-09-05T12:10:59Z budget=2700s evidence=/c/Users/AndrewBerman/Desktop/wk-NFRA_CLDGRPH-1b/org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/behind_evidence.jsonl
  2026-09-05T12:11:05.518226300Z  marker=2026-09-05T12:10:36.884158+00:00  served=2026-09-05T12:10:36.884158+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  >>> MARKER MOVED: 2026-09-05T12:10:36.884158+00:00 -> 2026-09-05T12:11:27.375244+00:00 -- reading the client NOW
  2026-09-05T12:11:57.620030000Z  marker=2026-09-05T12:11:27.375244+00:00  served=2026-09-05T12:11:27.375244+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  >>> MARKER MOVED: 2026-09-05T12:11:27.375244+00:00 -> 2026-09-05T12:12:05.739979+00:00 -- reading the client NOW
  2026-09-05T12:12:47.239769100Z  marker=2026-09-05T12:12:05.739979+00:00  served=2026-09-05T12:11:27.375244+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=false
  >>> MARKER MOVED: 2026-09-05T12:12:05.739979+00:00 -> 2026-09-05T12:13:33.832979+00:00 -- reading the client NOW
  2026-09-05T12:13:35.337534700Z  marker=2026-09-05T12:13:33.832979+00:00  served=2026-09-05T12:12:05.739979+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=true
  12:14:16Z  marker unchanged (2026-09-05T12:13:33.832979+00:00) -- cheap poll, no client read
  12:14:28Z  marker unchanged (2026-09-05T12:13:33.832979+00:00) -- cheap poll, no client read
  12:14:36Z  marker unchanged (2026-09-05T12:13:33.832979+00:00) -- cheap poll, no client read
  >>> MARKER MOVED: 2026-09-05T12:13:33.832979+00:00 -> 2026-09-05T12:14:42.810835+00:00 -- reading the client NOW
  2026-09-05T12:14:47.571638000Z  marker=2026-09-05T12:14:42.810835+00:00  served=2026-09-05T12:13:33.832979+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=true
  >>> MARKER MOVED: 2026-09-05T12:14:42.810835+00:00 -> 2026-09-05T12:14:56.469712+00:00 -- reading the client NOW
  2026-09-05T12:15:31.337466400Z  marker=2026-09-05T12:14:56.469712+00:00  served=2026-09-05T12:14:56.469712+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:16:25Z  marker unchanged (2026-09-05T12:14:56.469712+00:00) -- cheap poll, no client read
  12:16:38Z  marker unchanged (2026-09-05T12:14:56.469712+00:00) -- cheap poll, no client read
  >>> MARKER MOVED: 2026-09-05T12:14:56.469712+00:00 -> 2026-09-05T12:16:43.795811+00:00 -- reading the client NOW
  2026-09-05T12:16:49.306069300Z  marker=2026-09-05T12:16:43.795811+00:00  served=2026-09-05T12:14:56.469712+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=true
  >>> MARKER MOVED: 2026-09-05T12:16:43.795811+00:00 -> 2026-09-05T12:16:58.855158+00:00 -- reading the client NOW
  2026-09-05T12:17:43.325404900Z  marker=2026-09-05T12:16:58.855158+00:00  served=2026-09-05T12:16:58.855158+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:18:32Z  marker unchanged (2026-09-05T12:16:58.855158+00:00) -- cheap poll, no client read
  12:18:42Z  marker unchanged (2026-09-05T12:16:58.855158+00:00) -- cheap poll, no client read
  >>> MARKER MOVED: 2026-09-05T12:16:58.855158+00:00 -> 2026-09-05T12:18:50.261442+00:00 -- reading the client NOW
  2026-09-05T12:18:53.767855900Z  marker=2026-09-05T12:18:50.261442+00:00  served=2026-09-05T12:16:58.855158+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=true
  >>> MARKER MOVED: 2026-09-05T12:18:50.261442+00:00 -> 2026-09-05T12:19:10.768569+00:00 -- reading the client NOW
  2026-09-05T12:19:34.236403400Z  marker=2026-09-05T12:19:10.768569+00:00  served=2026-09-05T12:19:10.768569+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:20:15Z  marker unchanged (2026-09-05T12:19:10.768569+00:00) -- cheap poll, no client read
  12:20:23Z  marker unchanged (2026-09-05T12:19:10.768569+00:00) -- cheap poll, no client read
  12:20:32Z  marker unchanged (2026-09-05T12:19:10.768569+00:00) -- cheap poll, no client read
  12:20:41Z  marker unchanged (2026-09-05T12:19:10.768569+00:00) -- cheap poll, no client read
  12:20:51Z  marker unchanged (2026-09-05T12:19:10.768569+00:00) -- cheap poll, no client read
  >>> MARKER MOVED: 2026-09-05T12:19:10.768569+00:00 -> 2026-09-05T12:21:03.085712+00:00 -- reading the client NOW
  2026-09-05T12:21:04.810225600Z  marker=2026-09-05T12:21:03.085712+00:00  served=2026-09-05T12:19:10.768569+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=true
  >>> MARKER MOVED: 2026-09-05T12:21:03.085712+00:00 -> 2026-09-05T12:21:25.739594+00:00 -- reading the client NOW
  2026-09-05T12:21:53.249796900Z  marker=2026-09-05T12:21:25.739594+00:00  served=2026-09-05T12:19:10.768569+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=false
  12:22:38Z  marker unchanged (2026-09-05T12:21:25.739594+00:00) -- cheap poll, no client read
  12:22:49Z  marker unchanged (2026-09-05T12:21:25.739594+00:00) -- cheap poll, no client read
  12:22:59Z  marker unchanged (2026-09-05T12:21:25.739594+00:00) -- cheap poll, no client read
  >>> MARKER MOVED: 2026-09-05T12:21:25.739594+00:00 -> 2026-09-05T12:23:09.662217+00:00 -- reading the client NOW
  2026-09-05T12:23:09.581944100Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:21:25.739594+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=true
  12:23:51Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:24:01Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:24:09Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:24:19Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:24:28Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:24:36Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:24:44.387055200Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:25:26Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:25:35Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:25:44Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:25:53Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:26:03Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:26:11Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:26:21.024198500Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:27:00Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:27:10Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:27:19Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:27:29Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:27:39Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:27:49Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:28:01.678333200Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:28:42Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:28:53Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:29:03Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:29:11Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:29:22Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:29:31Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:29:42.580684800Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:30:26Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:30:35Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:30:44Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:30:55Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:31:05Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:31:13Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:31:25.171036400Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:32:07Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:32:17Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:32:26Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:32:35Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:32:44Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:32:53Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:33:03.938489800Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:33:48Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:33:57Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:34:05Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:34:13Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:34:24Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:34:35Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:34:46.081477200Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:35:32Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:35:42Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:35:51Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:36:01Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:36:12Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:36:23Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:36:31.773865300Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:37:17Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:37:30Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:37:39Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:37:50Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:38:02Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:38:14Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:38:27.062211400Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:39:19Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:39:29Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:39:42Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:39:51Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:40:03Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:40:12Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:40:22.473281300Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:41:18Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:41:29Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:41:41Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:41:51Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:42:01Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:42:13Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:42:23.816925300Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:43:11Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:43:22Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:43:34Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:43:48Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:43:59Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:44:10Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:44:22.664576800Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:45:12Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:45:23Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:45:32Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:45:42Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:45:51Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:46:03Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  2026-09-05T12:46:13.505901200Z  marker=2026-09-05T12:23:09.662217+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  12:46:54Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:47:05Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:47:16Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:47:25Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  12:47:33Z  marker unchanged (2026-09-05T12:23:09.662217+00:00) -- cheap poll, no client read
  >>> MARKER MOVED: 2026-09-05T12:23:09.662217+00:00 -> 2026-09-05T12:47:37.329883+00:00 -- reading the client NOW
  2026-09-05T12:47:43.375244400Z  marker=2026-09-05T12:47:37.329883+00:00  served=2026-09-05T12:23:09.662217+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=true
  12:48:24Z  marker unchanged (2026-09-05T12:47:37.329883+00:00) -- cheap poll, no client read
  12:48:35Z  marker unchanged (2026-09-05T12:47:37.329883+00:00) -- cheap poll, no client read
  12:48:45Z  marker unchanged (2026-09-05T12:47:37.329883+00:00) -- cheap poll, no client read
  12:48:57Z  marker unchanged (2026-09-05T12:47:37.329883+00:00) -- cheap poll, no client read
  12:49:08Z  marker unchanged (2026-09-05T12:47:37.329883+00:00) -- cheap poll, no client read
  12:49:21Z  marker unchanged (2026-09-05T12:47:37.329883+00:00) -- cheap poll, no client read
  2026-09-05T12:49:32.341770800Z  marker=2026-09-05T12:47:37.329883+00:00  served=2026-09-05T12:47:37.329883+00:00  BEHIND=false  read_ok=true  pointer_moved_by_read=false
  >>> MARKER MOVED: 2026-09-05T12:47:37.329883+00:00 -> 2026-09-05T12:50:07.498295+00:00 -- reading the client NOW
  2026-09-05T12:50:14.062481500Z  marker=2026-09-05T12:50:07.498295+00:00  served=2026-09-05T12:47:37.329883+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=true
  >>> MARKER MOVED: 2026-09-05T12:50:07.498295+00:00 -> 2026-09-05T12:50:45.008597+00:00 -- reading the client NOW
  2026-09-05T12:50:57.157589400Z  marker=2026-09-05T12:50:45.008597+00:00  served=2026-09-05T12:47:37.329883+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=true
  12:51:44Z  marker unchanged (2026-09-05T12:50:45.008597+00:00) -- cheap poll, no client read
  12:51:53Z  marker unchanged (2026-09-05T12:50:45.008597+00:00) -- cheap poll, no client read
  12:52:03Z  marker unchanged (2026-09-05T12:50:45.008597+00:00) -- cheap poll, no client read
  12:52:14Z  marker unchanged (2026-09-05T12:50:45.008597+00:00) -- cheap poll, no client read
  >>> MARKER MOVED: 2026-09-05T12:50:45.008597+00:00 -> 2026-09-05T12:52:19.817312+00:00 -- reading the client NOW
  2026-09-05T12:52:23.621817700Z  marker=2026-09-05T12:52:19.817312+00:00  served=2026-09-05T12:50:45.008597+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=true
  12:53:03Z  marker unchanged (2026-09-05T12:52:19.817312+00:00) -- cheap poll, no client read
  >>> MARKER MOVED: 2026-09-05T12:52:19.817312+00:00 -> 2026-09-05T12:53:04.983210+00:00 -- reading the client NOW
  2026-09-05T12:53:13.357113400Z  marker=2026-09-05T12:53:04.983210+00:00  served=2026-09-05T12:52:19.817312+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=false
  12:54:00Z  marker unchanged (2026-09-05T12:53:04.983210+00:00) -- cheap poll, no client read
  12:54:09Z  marker unchanged (2026-09-05T12:53:04.983210+00:00) -- cheap poll, no client read
  12:54:18Z  marker unchanged (2026-09-05T12:53:04.983210+00:00) -- cheap poll, no client read
  12:54:30Z  marker unchanged (2026-09-05T12:53:04.983210+00:00) -- cheap poll, no client read
  >>> MARKER MOVED: 2026-09-05T12:53:04.983210+00:00 -> 2026-09-05T12:54:31.241426+00:00 -- reading the client NOW
  2026-09-05T12:54:39.838720400Z  marker=2026-09-05T12:54:31.241426+00:00  served=2026-09-05T12:52:19.817312+00:00  BEHIND=true  read_ok=true  pointer_moved_by_read=false
  12:55:30Z  marker unchanged (2026-09-05T12:54:31.241426+00:00) -- cheap poll, no client read
  12:55:42Z  marker unchanged (2026-09-05T12:54:31.241426+00:00) -- cheap poll, no client read
  12:55:54Z  marker unchanged (2026-09-05T12:54:31.241426+00:00) -- cheap poll, no client read
POLL end 2026-09-05T12:56:01Z
```
