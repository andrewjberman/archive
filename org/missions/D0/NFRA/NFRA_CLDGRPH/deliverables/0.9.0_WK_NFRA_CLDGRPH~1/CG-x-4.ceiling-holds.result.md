# CG-x-4 -- FWD-4 CLOSING PASS: THE CEILING HOLDS BY ITSELF (and two arms of the hands-off criterion do not)

**TO** `NFRA_CLDGRPH.TO-CG-D-10` · **cell** CG-x-4 · **assignee** `0.9.0_WK_NFRA_CLDGRPH~1` ·
**branch** `wk-CLDGRPH-d10` · **base HEAD** `76c5f90155` · **read at** 2026-09-05T15:02:08Z.

> **PASS 2 (2026-09-05 ~17:3xZ) AND PASS 3 (2026-09-05 ~21:4xZ) ARE APPENDED AT THE END OF THIS
> FILE.** `D10-AC3` was RE-CUT by the issuer on `1.0.0_SA_CTO`'s ruling @`9f4a57262f` and
> re-measured in pass 2 as `HAND_ENFORCED_CEILING=1 of 3` -- FAIL, order stayed open. Pass 3 runs
> the SAME amended `D10-AC3` over a HAND-FREE cycle (`2026-09-04T21:18:54Z -> 2026-09-05T21:18:54Z`,
> re-derived by pass 3 itself, one second later than the hand-off's own timestamp for a reason
> recorded there) and measures `HAND_ENFORCED_CEILING=0 of 0`. **ALL FIVE CRITERIA NOW PASS AND THE
> ORDER FLIPS TO complete IN PASS 3.** Everything below (pass 1 and pass 2) still reproduces
> byte-identically at their own HEADs; the bar never moved a second time and no criterion was
> re-cut to make pass 3 pass.

## THE ANSWER FIRST (PASS 1)

**The ceiling holds, and it holds by itself where the ceiling is concerned.** Over the pinned
24 h cycle 2026-09-04T13:00:00Z -> 2026-09-05T13:00:00Z the oldest answer served was
**18138.643 s** old against a schedule-derived ceiling of **87191.260 s** -- 20.8% of it. The
stricter arm over *every* HTTP response in the window, including the 2887 `/health` reads that
also hand out a vintage, is **22649.197 s**, 26.0% of the ceiling. No answer in the cycle came
close to the ceiling, nothing was refused, and every vintage on the wire was written by a
producer, never by a seat.

**But `D10-AC3` FAILS ON BOTH LIMBS, and the failure is a real property of the world, not an
instrument defect.** Recorded, not argued:

| limb | expected | measured |
|---|---|---|
| `HANDS_OFF_RUNTASK` | `0 of <N>` | **`3 of 61`** |
| `WRITERS_IN_CYCLE` | `{derive_runner, incremental_updater}` | **`{cse_producers_nightly, derive_runner, incremental_updater}`** |

Four rows carry the findings: `NFRA_CLDGRPH-W1-S20` (the third writer), `NFRA_CLDGRPH-W1-S21`
(the three hand RunTasks, and why no admissible window at this HEAD can avoid them),
`NFRA_CLDGRPH-W1-S22` (an uncovered member of the hands-off domain -- a control-plane
`ecs:UpdateService` replaced the serving task *inside* the cycle, which neither census member
can see, and which also contradicts this order's status-block premise of one continuous task),
and `NFRA_CLDGRPH-W1-S23` (the ceiling's `+60` term under-allows the interval it must cover --
measured 113.490 s, verdict unaffected).

**THE ORDER DOES NOT FLIP.** A FAIL row leaves it open; a VALID proof instance is not a met order.

## WHAT WAS MEASURED, AND WITH WHAT GRAIN

**The cycle is PINNED, not rolling:** `2026-09-04T13:00:00Z -> 2026-09-05T13:00:00Z`. 24 h exactly,
containing exactly one 02:00Z boundary and the nightly's swap, with both ends in the past at the
cut so the window is CLOSED and no event in it is still arriving. A rolling `now - 24 h` would hand
the L9 grader a different population than this record reports.

**"The service's own log" spans TWO streams, not one.** `serving/globgrph-serving/c18ee8b40e...`
(the task this order's status block names) ends at epoch-ms 1788539258092 = 2026-09-04T16:27:38Z;
`serving/globgrph-serving/8889156e83ad...` begins at 1788539209370 = 2026-09-04T16:26:49Z and is
still serving. Both are inside the cycle. This is why the timeline reads BOTH vintage-setting log
lines: the watcher's `projection swap complete` (`projection_server.py:406`) **and** startup's
`initial verified projection open read-only` (`:514`). A startup install returns `"started"`, never
`"swapped"` (`:327`), so it emits **no swap line** -- a swaps-only timeline would have silently lost
the served vintage across the replacement and mis-aged every answer after it.

**How an answer is aged.** The access line carries no vintage -- `log_message` emits
`LOG.info("http " + format_string, *args)` and nothing more (`:499-500`) -- so each answer is PLACED
against the timeline: the served vintage at instant *t* is the vintage of the last vintage-setting
event at or before *t*, and age = *t* - vintage. The effective-from instant used is the **CloudWatch
event timestamp**, which is emitted *after* `install()` returns and is therefore >= the true swap
instant; that holds the old vintage active slightly longer than it really was, making **every age an
UPPER BOUND**. `UNPLACED_ANSWERS=0 of 3151` is the coverage claim, and it is a measured zero: the
seed (the vintage already being served at CYCLE_START, `2026-09-04T12:48:00.440101+00:00`, set by the
swap at 2026-09-04T12:49:24Z) was fetched by a 24 h lookback *before* the window precisely so that
the cycle's first answers are placeable rather than dropped.

**`ANSWERS_IN_CYCLE=261`** counts `POST /cypher` responses with status 200 -- the answers actually
handed out. The window held 264 `POST /cypher` lines in total; the other 3 are HTTP 500s (Kuzu parser
exceptions on malformed statements, visible in the transcript) which hand an error, not an answer.
The 2887 `GET /health` responses are excluded from the graded number and included in the stricter
supplementary arm, so the graded population cannot be the flattering cut.

**The ceiling belongs to the schedule, and every term is read rather than assumed:**

```
CEILING_S = 86400            the schedule's own period, cron(0 2 * * ? *)
          + 731.260104       the nightly chain's OWN duration, built_at - vintage from ITS manifest
          +    60            PROJECTION_WATCH_INTERVAL_SECONDS, the pointer-to-swap lag ceiling
          = 87191.260104 s
```

The nightly is identified by its **own properties**, never by "newest" and never by a typed date: the
one vintage served in the cycle whose manifest carries `producer.mode == "full"` **and**
`writer_id == "derive_runner"` and whose swap landed in the 02:00-04:00Z band.
`NIGHTLY_CANDIDATES=1` -- and had that set not been exactly one, `cycle_census.py` refuses to pick
and prints `AMBIGUOUS_OR_ABSENT` rather than breaking the tie silently.

## THE CONTROL (`D10-AC4`)

`python -m pytest infra/aws/globgrph/tests/test_projection_server.py -q -k "backward or refus"` ->
**`3 passed, 4 deselected in 0.23s`**, rc 0. The three selected, named so the count carries its grain:
`SwapTests::test_backward_test_seam_refuses_without_loading_or_moving` (the order's cited seam --
a planted backward pointer body, `LOADER_CALLS=0`, served vintage unchanged),
`ContractReaderTests::test_refuses_artifact_sha_mismatch`, and
`RequestTests::test_refuses_multiple_statements`. The plant is the reader's own in-process seam; no
S3 object was planted and nothing on the live plane was written.

The live corroborant: `REFUSALS_IN_CYCLE=0` over the window. That zero is a **measured absence, not a
dead arm** -- the same filter instrument on the same log and the same window returned 264 `POST
/cypher` lines and 38 swap lines, which is the positive control printed beside it.

## THE THREE HAZARDS THIS ORDER'S SIBLINGS PAID FOR

1. **S57, `2>/dev/null` on a verdict read.** No stderr redirection appears anywhere in `cycle.sh`,
   `cycle_ages.py` or `cycle_census.py`. Every read captures its rc, prints it, and a non-zero rc
   writes a `READ_FAILED` sentinel instead of falling through to a number. The summary block refuses
   to print at all (`exit 3`) if any value fails to lift from its helper, so a failed read can never
   surface as a measurement.
2. **W1-S18, a control whose failure mode is silence.** Every `.tools/aws` read is passed through
   `tr -d '\r'`; every census prints its denominator (`pages=`, `events=`, `RUNTASK_EVENTS_FETCHED`,
   `DISTINCT_VINTAGES_TO_READ`, `MANIFEST_READS_OK=39 of 39`), so an instrument that printed nothing
   would be visible as a zero denominator rather than as a clean pass.
3. **W1-S19, a bare before-vs-after difference.** **No arm of this order compares a before to an
   after.** Every number is a single read of a durable record -- a CLOSED CloudWatch window,
   immutable per-vintage S3 manifests, CloudTrail after its delivery lag -- taken after the window
   shut. Nothing this script does can perturb what it measures, so no change needs attributing.
   The RunTask census nonetheless attributes every event by **provenance form** (never by a list of
   role names -- the defect W1-S15 recorded) and prints every per-row label beside the count, with
   `RUNTASK_LABEL_SUM=61 ... AGREE` as the arithmetic check that the labels and the total agree.

**Two instruments, not one, on the graded numbers.** `cycle.sh` was run first in a fully SERIAL form
(1m48s) and then in the concurrent form committed here (1m06s / 0m50s / 1m16s across the three graded
invocations). Both forms returned `OLDEST_AGE_SERVED_S=18138.643`, `CEILING_S=87191.260`,
`ANSWERS_IN_CYCLE=261`, `SWAPS_IN_CYCLE=38` identically. The serial form was replaced because a
criterion that spends 90% of its `timeout 120` bound is one slow API call away from recording rc 124
instead of a measurement -- not because its answer differed.

**The manifest cache is disclosed, not hidden.** A `_build_manifest.json` is immutable for a given
vintage key, so a cached rc=0 row is the same bytes a live read returns; a cached FAILURE is never
reused. The run prints `MANIFEST_CACHE_HITS` and `MANIFEST_LIVE_READS` on every pass. All 39 rows in
`manifest_writer_cache.tsv` were read live by this worker at 2026-09-05 ~14:2xZ, rc 0 on 39 of 39.

## `D10-AC5` -- THE READING ACT (judgment; NO verdict; `3.0.0_SA_CVO` grades this at L9)

**On the ceiling's definition against FWD-4's "the ceiling belongs to the schedule, not to a person".**
Every term of `86400 + chain + 60` is read from a non-human artifact: the period from the EventBridge
rule's own `schedule_expression`, the chain duration from the nightly build's own manifest, the lag
bound from the server's own environment default echoed back by the running process's startup line.
No term is a number a person chose for this measurement, which is the property the endpoint asks for.
Two things about it are worth the grader's attention rather than this worker's assertion. First, the
chain term is measured from **this** cycle's nightly (731.260 s); it is a per-cycle quantity, so the
ceiling is strictly a *per-cycle* ceiling and not a constant of the system -- a slower nightly raises
its own ceiling, which is arguably the wrong direction for a bound and is the one place where the
definition flatters the world. The measured margin is wide enough (20.8%) that no plausible chain
duration changes the verdict, but the shape of the definition is the CVO's to rule on, not the
margin. Second -- and this one is measured, not stylistic -- **the `+60` term is the only allowance
the formula makes for everything between `built_at` and the swap, and that interval exceeded 60 s
twice in this very cycle**: 69.051 s (built_at 2026-09-04T13:09:17.943199+00:00 -> swap event
2026-09-04T13:10:26.994Z) and 113.490 s (built_at 2026-09-05T12:53:40.918503+00:00 -> swap event
2026-09-05T12:55:34.409Z), 2 of 38 swaps, against a minimum of 4.889 s. The install itself is not
the cost -- `pointer_read_at -> last_swap` is 0.007 s in both cases; the excess sits between the
build finishing and the server first SEEING the pointer, i.e. the producer's artifact-upload and
pointer-flip time, which the ceiling's derivation does not name at all and which the 60 s poll
does not start until. Substituting the observed maximum gives 86400 + 731.260 + 113.490 =
87244.750 s, and `WITHIN_CEILING` stays `true` on a measured 18138.643 s -- so the verdict is
untouched and only the definition is at issue. Filed as `NFRA_CLDGRPH-W1-S23`.

**On the log method's coverage.** `UNPLACED_ANSWERS=0 of 3151` -- every HTTP line in the window was
placed against the timeline, so no answer was excluded from the ceiling test. The seam that could
have produced unplaceable answers, and did not, is the task replacement at 16:26:49Z: had the
timeline been built from swap lines alone, the 261 answers would have been aged against a vintage
that stopped being current at that instant. The residual coverage limit is that the access line
records neither the vintage nor the response body, so an answer's age is *inferred* from the timeline
rather than *read* from the answer -- the two can only diverge if a swap completed between an
answer's `manager.query()` lease and the swap's log line, a sub-second window on a 3151-line
population. The `age_line`/`vintage` fields the server puts in every `POST /cypher` **response body**
would make the age directly readable, and they are not logged.

**On what the FAIL does and does not touch.** The two failing limbs are about *who was on the
cluster*, not about *how old any answer was*. The ceiling arm and the control arm are independent of
both, and both pass. Whether "nobody enforcing the ceiling by hand" is contradicted by three hand
RunTasks none of which touched the pointer, and by a third `writer_id` that is a scheduled nightly
producer, is exactly the grading question the three rows put to the CVO -- and it is not this
worker's to answer.

## THE RECORD

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-D-10",
  "cell": "CG-x-4",
  "fwd": "FWD-4",
  "worker": "0.9.0_WK_NFRA_CLDGRPH~1",
  "read_at": "2026-09-05T15:02:08Z",
  "repo_head": "76c5f90155fcfc1b22278678bce89dbe711ac73d",
  "graded_keys": {
    "CYCLE_START": "2026-09-04T13:00:00Z",
    "CYCLE_END": "2026-09-05T13:00:00Z",
    "ANSWERS_IN_CYCLE": 261,
    "SWAPS_IN_CYCLE": 38,
    "NIGHTLY_SWAP_AT": "2026-09-05T02:23:34Z",
    "OLDEST_AGE_SERVED_S": 18138.643,
    "CEILING_S": 87191.26,
    "WITHIN_CEILING": "true",
    "HANDS_OFF_RUNTASK": "3 of 61",
    "WRITERS_IN_CYCLE": "{cse_producers_nightly, derive_runner, incremental_updater}"
  },
  "ceiling_arithmetic": {
    "claim": "measured",
    "cron_period_s": 86400,
    "cron": "cron(0 2 * * ? *)",
    "cron_at": "infra/aws/terraform/globgrph/item2a.tf:438-443",
    "chain_s": 731.260104,
    "chain_from": "the cycle's nightly manifest s3://opal-313476888478-globgrph/projection/2026-09-05T02:11:10.919000+00:00/_build_manifest.json: built_at 2026-09-05T02:23:22.179104+00:00 minus vintage 2026-09-05T02:11:10.919000+00:00",
    "watcher_interval_s": 60,
    "watcher_from": "projection_server.py:36 PROJECTION_WATCH_INTERVAL_SECONDS, corroborated by the process's own startup line 'pointer watcher interval 60.0 seconds'",
    "ceiling_s": 87191.260104
  },
  "top5_oldest_answers": [
    {
      "age_s": 18138.643,
      "answered_at": "2026-09-04T23:14:07.426000Z",
      "served_vintage": "2026-09-04T18:11:48.783142+00:00"
    },
    {
      "age_s": 18130.814,
      "answered_at": "2026-09-04T23:13:59.597000Z",
      "served_vintage": "2026-09-04T18:11:48.783142+00:00"
    },
    {
      "age_s": 15972.629,
      "answered_at": "2026-09-04T22:38:01.412000Z",
      "served_vintage": "2026-09-04T18:11:48.783142+00:00"
    },
    {
      "age_s": 15805.89,
      "answered_at": "2026-09-05T10:19:08.461000Z",
      "served_vintage": "2026-09-05T05:55:42.571886+00:00"
    },
    {
      "age_s": 15796.385,
      "answered_at": "2026-09-05T10:18:58.956000Z",
      "served_vintage": "2026-09-05T05:55:42.571886+00:00"
    }
  ],
  "swap_timeline": [
    {
      "at": "2026-09-04T13:00:00Z",
      "vintage": "2026-09-04T12:48:00.440101+00:00",
      "kind": "SEED (already serving at CYCLE_START)"
    },
    {
      "at": "2026-09-04T13:10:26.994000Z",
      "vintage": "2026-09-04T12:55:59.236365+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-04T14:39:33.573000Z",
      "vintage": "2026-09-04T14:38:47.159054+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-04T14:41:34.566000Z",
      "vintage": "2026-09-04T14:41:04.219993+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-04T14:44:35.569000Z",
      "vintage": "2026-09-04T14:43:18.370316+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-04T14:46:36.523000Z",
      "vintage": "2026-09-04T14:45:21.329463+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-04T16:26:49.370000Z",
      "vintage": "2026-09-04T14:45:21.329463+00:00",
      "kind": "startup-install"
    },
    {
      "at": "2026-09-04T16:51:51.981000Z",
      "vintage": "2026-09-04T16:38:39.485910+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-04T18:12:58.963000Z",
      "vintage": "2026-09-04T18:11:48.783142+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T00:29:24.051000Z",
      "vintage": "2026-09-05T00:28:21.155513+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T00:37:25.347000Z",
      "vintage": "2026-09-05T00:36:33.532742+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T00:54:27.185000Z",
      "vintage": "2026-09-05T00:52:45.603017+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T02:23:34.061000Z",
      "vintage": "2026-09-05T02:11:10.919000+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T03:32:39.012000Z",
      "vintage": "2026-09-05T03:31:16.793943+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T05:31:47.151000Z",
      "vintage": "2026-09-05T05:31:07.555427+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T05:39:48.760000Z",
      "vintage": "2026-09-05T05:39:20.963495+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T05:57:50.573000Z",
      "vintage": "2026-09-05T05:55:42.571886+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T11:39:12.577000Z",
      "vintage": "2026-09-05T11:37:57.355159+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:02:14.820000Z",
      "vintage": "2026-09-05T12:01:37.379252+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:03:15.669000Z",
      "vintage": "2026-09-05T12:02:49.821182+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:05:16.583000Z",
      "vintage": "2026-09-05T12:04:14.956045+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:06:17.478000Z",
      "vintage": "2026-09-05T12:05:11.879345+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:07:18.616000Z",
      "vintage": "2026-09-05T12:06:22.416021+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:08:19.447000Z",
      "vintage": "2026-09-05T12:07:48.890292+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:09:20.279000Z",
      "vintage": "2026-09-05T12:08:32.676281+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:10:21.154000Z",
      "vintage": "2026-09-05T12:09:12.462130+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:11:22.055000Z",
      "vintage": "2026-09-05T12:10:36.884158+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:12:22.947000Z",
      "vintage": "2026-09-05T12:11:27.375244+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:13:23.809000Z",
      "vintage": "2026-09-05T12:12:05.739979+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:14:24.710000Z",
      "vintage": "2026-09-05T12:13:33.832979+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:15:25.662000Z",
      "vintage": "2026-09-05T12:14:56.469712+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:17:26.571000Z",
      "vintage": "2026-09-05T12:16:58.855158+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:19:27.477000Z",
      "vintage": "2026-09-05T12:19:10.768569+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:22:28.465000Z",
      "vintage": "2026-09-05T12:21:25.739594+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:24:29.364000Z",
      "vintage": "2026-09-05T12:23:09.662217+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:48:31.585000Z",
      "vintage": "2026-09-05T12:47:37.329883+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:51:32.476000Z",
      "vintage": "2026-09-05T12:50:45.008597+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:53:33.463000Z",
      "vintage": "2026-09-05T12:52:19.817312+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:55:34.409000Z",
      "vintage": "2026-09-05T12:53:04.983210+00:00",
      "kind": "swap"
    },
    {
      "at": "2026-09-05T12:56:35.269000Z",
      "vintage": "2026-09-05T12:54:31.241426+00:00",
      "kind": "swap"
    }
  ],
  "verdicts": {
    "D10-AC1": "PASS-by-output",
    "D10-AC2": "PASS-by-output",
    "D10-AC3": "FAIL-by-output (BOTH limbs)",
    "D10-AC4": "PASS-by-output",
    "D10-AC5": "RECORDED (judgment=true; no verdict; 3.0.0_SA_CVO grades at L9)"
  },
  "rows_filed": [
    "NFRA_CLDGRPH-W1-S20",
    "NFRA_CLDGRPH-W1-S21",
    "NFRA_CLDGRPH-W1-S22",
    "NFRA_CLDGRPH-W1-S23"
  ],
  "ceiling_third_term_check": {
    "claim": "measured",
    "what_the_plus60_must_cover": "built_at -> swap log event",
    "n": 38,
    "min_s": 4.889,
    "max_s": 113.49,
    "over_60s": 2,
    "the_two": [
      {
        "built_at": "2026-09-04T13:09:17.943199+00:00",
        "pointer_read_at": "2026-09-04T13:10:26.950195+00:00",
        "swap_event": "2026-09-04T13:10:26.994Z",
        "built_to_swap_s": 69.051,
        "install_s": 0.007
      },
      {
        "built_at": "2026-09-05T12:53:40.918503+00:00",
        "pointer_read_at": "2026-09-05T12:55:34.372692+00:00",
        "swap_event": "2026-09-05T12:55:34.409Z",
        "built_to_swap_s": 113.49,
        "install_s": 0.007
      }
    ],
    "corrected_ceiling_s": 87244.75,
    "within_ceiling_still": "true",
    "row": "NFRA_CLDGRPH-W1-S23"
  },
  "hand_runtasks": [
    {
      "at": "2026-09-04T13:41:39Z",
      "startedBy": "EMPTY",
      "identity": "IAMUser arn:aws:iam::313476888478:user/Andrew_Berman",
      "taskDefinition": "globgrph-trino",
      "sourceIP": "73.84.214.103"
    },
    {
      "at": "2026-09-04T16:30:15Z",
      "startedBy": "wk-cldgrph-1-cgs15",
      "identity": "IAMUser arn:aws:iam::313476888478:user/Andrew_Berman",
      "taskDefinition": "globgrph-derive-runner:7",
      "sourceIP": "73.84.214.103"
    },
    {
      "at": "2026-09-04T21:18:53Z",
      "startedBy": "EMPTY",
      "identity": "IAMUser arn:aws:iam::313476888478:user/Andrew_Berman",
      "taskDefinition": "globgrph-trino",
      "sourceIP": "73.84.214.103"
    }
  ],
  "runtask_labels": {
    "PIPE": 54,
    "SCHEDULER_EVENTS_RULE": 3,
    "SCHEDULER_CHRONOS": 1,
    "HAND": 3,
    "sum": 61,
    "denominator": 61,
    "agree": true
  }
}
```

## TRANSCRIPT -- `bash cycle.sh` in full, rc 0, 2026-09-05T15:02:08Z

```
=== TO-CG-D-10 / CG-x-4 -- FWD-4: THE CEILING HOLDS BY ITSELF
READ_AT=2026-09-05T15:02:08Z
REPO_HEAD=76c5f90155fcfc1b22278678bce89dbe711ac73d
WINDOW_MS=1788526800000 -> 1788613200000   (pinned, closed, 24h)

--- 1. THE SERVED-VINTAGE TIMELINE (the service's own log)
The access line carries NO vintage (projection_server.py:499-500), so an answer is placed
against this timeline.  BOTH vintage-setting lines are read: the watcher's swap (:406) AND
startup's 'open read-only' (:514) -- startup's install returns "started", never "swapped",
so a swaps-only timeline SILENTLY LOSES the served vintage across a task replacement.
  TIMELINE_IN_WINDOW: rc=0  pages=1  events=39

--- 1b. THE SEED: the vintage already being served at CYCLE_START (24h lookback before it)
Without this the first answers of the cycle are UNPLACEABLE and would be silently dropped.
  TIMELINE_SEED_LOOKBACK: rc=0  pages=1  events=37

--- 1c. STREAMS THE WINDOW SPANS (a timeline crossing a task replacement must say so)
  stream serving/globgrph-serving/8889156e83ad4e3e95931e9d505169a9  first=1788539209370 last=1788616637989
  stream serving/globgrph-serving/c18ee8b40e4a4bf3993f8f78cc2f98a6  first=1788460959874 last=1788539258092
  STREAMS_TOTAL_IN_GROUP=2   (read rc=0)

--- 2. THE ANSWERS (every http line in the window; POST /cypher is the served answer)
  HTTP_IN_WINDOW: rc=0  pages=1  events=3151

--- 2b. THE REFUSAL CENSUS (the seam that keeps a stale artifact off the wire)
  REFUSALS: rc=0  pages=1  events=0

--- 4. HANDS OFF, limb (i): every RunTask in the cycle, paginated to a real denominator
  RUNTASK_PAGES=2  RUNTASK_EVENTS_FETCHED=61  (read rc=0)
  INSTRUMENT QUALIFIER: CloudTrail management-event delivery lags up to ~15 min; this window
    closed at 2026-09-05T13:00:00Z and is read after it, so no in-window event is undelivered.

--- 4b. HANDS OFF, limb (ii): CloudTrail on the POINTER KEY itself (projection/current.json)
  POINTER_KEY_EVENTS=0 (read rc=0)
  POINTER_TRAIL_COVERAGE=UNKNOWN -- S3 DATA events are not enabled on this trail, so a
    zero here CANNOT distinguish 'nobody wrote the pointer' from 'the trail does not see
    object writes at all'.  The order anticipates exactly this and routes the question to
    the manifests' writer_id instead (WRITERS_IN_CYCLE), a PRODUCER-side record that is
    not subject to this gap.

--- 4c. AN UNCOVERED MEMBER OF THE HANDS-OFF DOMAIN, printed because the census cannot see it
The order's hands-off definition enumerates two members: RunTask and a pointer PutObject.
A control-plane ecs:UpdateService is NEITHER, yet it replaces the SERVING task inside the
cycle -- and a task replacement re-seats the served vintage from whatever the pointer then
says.  A hands-off claim that cannot see it is scoped narrower than its own sentence.
  UPDATESERVICE 2026-09-04T16:26:11Z | identity=IAMUser/arn:aws:iam::313476888478:user/Andrew_Berman | service=arn:aws:ecs:us-east-1:313476888478:service/opal-globgrph/globgrph-serving | taskDefinition=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-serving:2

  SEED_SET_AT_MS=1788526164556  SEED_VINTAGE=2026-09-04T12:48:00.440101+00:00
  swap-complete lines inside the window: 38
  POSITIVE CONTROL for the CloudWatch filter instrument -- it must find something before any
    zero of its counts as an absence: 'POST /cypher' lines = 264, swap lines = 38.
  REFUSALS_IN_CYCLE=0 (the read returned rc=0, so this is a MEASURED absence and not a
    dead arm -- the same instrument on the same window returned the two non-zero counts above)

--- 3. THE WRITER CENSUS -- every vintage served in the cycle, from ITS OWN manifest
  DISTINCT_VINTAGES_TO_READ=39
  MANIFEST_CACHE_HITS=39  MANIFEST_LIVE_READS=0  (cache: /c/Users/AndrewBerman/Desktop/wk-CLDGRPH-d10/org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/manifest_writer_cache.tsv)

--- 5. THE AGE JOIN
TIMELINE_RAW_LINES=40  TIMELINE_EVENTS_PARSED=40
HTTP_RAW_LINES=3151  HTTP_LINES_PARSED=3151
PLACEMENT_METHOD=last-vintage-setting-event-at-or-before-answer (event ts => UPPER BOUND age)
UNPLACED_ANSWERS=0 of 3151
  http_status 200 = 3148
  http_status 500 = 3
  route GET/health = 2887
  route POST/cypher = 264
SERVED_POST_CYPHER_200=261
TOP5_OLDEST_ANSWERS (age_s | answered_at | served_vintage):
  18138.643 | 2026-09-04T23:14:07.426000Z | 2026-09-04T18:11:48.783142+00:00
  18130.814 | 2026-09-04T23:13:59.597000Z | 2026-09-04T18:11:48.783142+00:00
  15972.629 | 2026-09-04T22:38:01.412000Z | 2026-09-04T18:11:48.783142+00:00
  15805.890 | 2026-09-05T10:19:08.461000Z | 2026-09-05T05:55:42.571886+00:00
  15796.385 | 2026-09-05T10:18:58.956000Z | 2026-09-05T05:55:42.571886+00:00
OLDEST_AGE_CANDIDATE=18138.643
WIDER_BOUND_OLDEST_AGE_ANY_HTTP_S=22649.197
  cycle_ages.py rc=0

--- 6. THE CEILING, THE WRITERS, THE RUNTASK LABELS
VINTAGES_SERVED_IN_CYCLE=39 distinct (incl. the seed served at CYCLE_START)
MANIFEST_READS_OK=39 of 39
  writer cse_producers_nightly = 1 vintage(s)
  writer derive_runner = 3 vintage(s)
  writer incremental_updater = 35 vintage(s)
WRITERS_VALUE={cse_producers_nightly, derive_runner, incremental_updater}
NIGHTLY_CANDIDATES=1 (full + derive_runner + swap in the 02:00-04:00Z band)
  2026-09-05T02:23:34Z | vintage 2026-09-05T02:11:10.919000+00:00 | built_at 2026-09-05T02:23:22.179104+00:00
CEILING_ARITHMETIC: 86400 (cron period) + 731.260104 (built_at 2026-09-05T02:23:22.179104+00:00 - vintage 2026-09-05T02:11:10.919000+00:00) + 60 (watcher interval) = 87191.260104
NIGHTLY_SWAP_AT_VALUE=2026-09-05T02:23:34Z
CHAIN_S_VALUE=731.260
CEILING_S_VALUE=87191.260
RUNTASK_EVENTS_CLASSIFIED=61
  label HAND = 3
  label PIPE = 54
  label SCHEDULER_CHRONOS = 1
  label SCHEDULER_EVENTS_RULE = 3
RUNTASK_LABEL_SUM=61 (must equal RUNTASK_EVENTS_CLASSIFIED=61): AGREE
  HAND_ROW 2026-09-04T21:18:53Z | startedBy='' | invokedBy=- | identity=IAMUser/arn:aws:iam::313476888478:user/Andrew_Berman
  HAND_ROW 2026-09-04T16:30:15Z | startedBy='wk-cldgrph-1-cgs15' | invokedBy=- | identity=IAMUser/arn:aws:iam::313476888478:user/Andrew_Berman
  HAND_ROW 2026-09-04T13:41:39Z | startedBy='' | invokedBy=- | identity=IAMUser/arn:aws:iam::313476888478:user/Andrew_Berman
RUNTASK_HAND_VALUE=3
RUNTASK_TOTAL_VALUE=61
  cycle_census.py rc=0

=============================== CG-x-4 SUMMARY ===============================
CYCLE_START=2026-09-04T13:00:00Z
CYCLE_END=2026-09-05T13:00:00Z
ANSWERS_IN_CYCLE=261
SWAPS_IN_CYCLE=38
NIGHTLY_SWAP_AT=2026-09-05T02:23:34Z
OLDEST_AGE_SERVED_S=18138.643
CEILING_S=87191.260
WITHIN_CEILING=true
HANDS_OFF_RUNTASK=3 of 61
WRITERS_IN_CYCLE={cse_producers_nightly, derive_runner, incremental_updater}
==============================================================================
SUPPLEMENTARY (never graded; printed so the graded numbers carry their frame):
  CEILING_CHAIN_S=731.260  (the nightly's own built_at - vintage, from ITS manifest)
  UNPLACED=0 of 3151  (answers the timeline could not place; a zero IS the coverage claim)
  STRICTER_ARM_ALL_HTTP_OLDEST_S=22649.197 -> within ceiling: true
    (every http response incl. /health, which also hands out a vintage; a WIDER population
     than the graded one, printed so the graded number cannot be the flattering cut)
  EXTRA_UPDATESERVICE_IN_CYCLE=1  (an uncovered member of the hands-off domain -- see 4c)
```

## TRANSCRIPT -- the four graded invocations, each under `timeout 120`

Re-run to capture verbatim; every value reproduces the run above, which is what a PINNED closed
window is for. `D10-AC4` rc was read UNPIPED in its own call.

```
$ timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/cycle.sh | grep -E '^(OLDEST_AGE_SERVED_S|CEILING_S|WITHIN_CEILING)='
OLDEST_AGE_SERVED_S=18138.643
CEILING_S=87191.260
WITHIN_CEILING=true
rc=0 (grep; the bounded run did not time out -- see the values above)

$ timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/cycle.sh | grep -E '^(ANSWERS_IN_CYCLE|SWAPS_IN_CYCLE|NIGHTLY_SWAP_AT)='
ANSWERS_IN_CYCLE=261
SWAPS_IN_CYCLE=38
NIGHTLY_SWAP_AT=2026-09-05T02:23:34Z
rc=0 (grep)

$ timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/cycle.sh | grep -E '^(HANDS_OFF_RUNTASK|WRITERS_IN_CYCLE)='
HANDS_OFF_RUNTASK=3 of 61
WRITERS_IN_CYCLE={cse_producers_nightly, derive_runner, incremental_updater}
rc=0 (grep) -- the CRITERION nonetheless FAILS: expect wants '0 of N' and the two-name writer set

$ timeout 120 python -m pytest infra/aws/globgrph/tests/test_projection_server.py -q -k "backward or refus"
...                                                                      [100%]
3 passed, 4 deselected in 0.48s
pytest rc=0 (read UNPIPED in a prior call; see the report body)

-- the three selected, named so the count carries its grain (--collect-only):
infra/aws/globgrph/tests/test_projection_server.py::ContractReaderTests::test_refuses_artifact_sha_mismatch
infra/aws/globgrph/tests/test_projection_server.py::SwapTests::test_backward_test_seam_refuses_without_loading_or_moving
infra/aws/globgrph/tests/test_projection_server.py::RequestTests::test_refuses_multiple_statements

3/7 tests collected (4 deselected) in 0.25s
```

---

# PASS 2 -- D10-AC3 RE-CUT, RE-MEASURED, AND STILL FAILING (on a better question)

**TO** `NFRA_CLDGRPH.TO-CG-D-10` · **cell** CG-x-4 · **assignee** `0.9.0_WK_NFRA_CLDGRPH~1` ·
**branch** `wk-CLDGRPH-d10b` · **base HEAD** `497ffff69c` · **read at** 2026-09-05T17:1xZ ·
**scope** D10-AC3 ONLY, per the amendment dated 2026-09-05 ~16:4xZ on `1.0.0_SA_CTO`'s ruling
@`9f4a57262f`. FWD-4 is not amended, CG-x-4 is not amended, and D10-AC1/AC2/AC4/AC5 are untouched.

## THE ANSWER FIRST

**`HAND_ENFORCED_CEILING=1 of 3`. D10-AC3 FAILS AGAIN, AND THE ORDER STAYS OPEN.** The amendment
diagnosed the pass-1 instrument correctly -- the old `<expect>` counted hand-STARTED RunTasks when
the cell asks about hands ENFORCING -- and its new test is the right one. The world does not clear
the new bar either. Of the three hand-started tasks in the cycle, **two are excused by their own
bytes and one is not**:

| hand task | what it ran | artifact | effect on served freshness |
|---|---|---|---|
| 2026-09-04T13:41:39Z `globgrph-trino` | one read-only `SELECT ... GROUP BY` on the statement API | none | **NONE** -- no vintage committed in its 57.7 s window |
| 2026-09-04T16:30:15Z `globgrph-derive-runner:7`, `startedBy=wk-cldgrph-1-cgs15` | the derive-runner entrypoint; committed the graph tables at 16:38:39.485910Z | **vintage `2026-09-04T16:38:39.485910+00:00`, served from 16:51:51Z** | **FRESHER -- 20 of 261 answers, by up to 6798.156 s** |
| 2026-09-04T21:18:53Z `globgrph-trino` | the same read-only `SELECT` | none | **NONE** -- no vintage committed in its 49.8 s window |

**This is not a criterion defect and it does not ask for another re-cut.** The amendment's worked
example asserts the `wk-cldgrph-1-cgs15` task is *"a digest-pinned rebuild for a DIFFERENT cell and
not ceiling enforcement"*. That is true of its **purpose** and false of its **effect**, and the
amendment's own operative sentence forbids reading the effect from anything but the task and the
artifact it produced. Row `NFRA_CLDGRPH-W1-S25` carries the divergence. The face is explicit that a
criterion which fails because the world is what it is *"FAILS honestly and the order stays open"*,
and that no reading may be reached for because it passes -- so none was.

**Every number pass 1 measured is carried unchanged and none is lost**, which the ruling requires:

| carried | pass 1 | pass 2 | bar? |
|---|---|---|---|
| `OLDEST_AGE_SERVED_S` / `CEILING_S` / `WITHIN_CEILING` | 18138.643 / 87191.260 / true | **identical** | D10-AC1, PASS |
| `ANSWERS_IN_CYCLE` / `SWAPS_IN_CYCLE` / `NIGHTLY_SWAP_AT` | 261 / 38 / 2026-09-05T02:23:34Z | **identical** | D10-AC2, PASS |
| `HANDS_OFF_RUNTASK` | `3 of 61` | **`3 of 61`** | no longer the bar; evidence |
| `WRITERS_IN_CYCLE` | `{cse_producers_nightly, derive_runner, incremental_updater}` | **identical, every member named** | no longer the bar; evidence |
| RunTask per-row labels | `PIPE 54 / EVENTS_RULE 3 / CHRONOS 1 / HAND 3` = 61 | **identical, label-sum control AGREE** | the readability control, kept |
| `UNPLACED_ANSWERS` | `0 of 3151` | **identical** | the coverage claim |
| the control | `3 passed, 4 deselected` | **identical** | D10-AC4, PASS |

## THE WINDOW: THE SAME PINNED CYCLE, AND THE FLATTERING CUT NAMED AND REFUSED

**`2026-09-04T13:00:00Z -> 2026-09-05T13:00:00Z`, unchanged from pass 1.** The face leaves the window
to this worker and asks it to say which and why. Three reasons, in order of weight:

1. **It is the cycle the other four criteria describe.** Re-cutting D10-AC3's window would leave
   AC1, AC2 and AC5 reporting a different population than AC3, and the L9 grader would be reading
   five criteria about four cycles. Every number in the table above reproduces byte-identically
   because the population did not move.
2. **It is CLOSED and it is defensible**: 24 h exactly, both ends in the past at the cut, exactly one
   02:00Z boundary and the nightly's swap inside it.
3. **The alternative is a flattering cut, and it is named here so the refusal is auditable.** The
   latest *admissible* closed 24 h window at this cut is `2026-09-04T16:48Z -> 2026-09-05T16:48Z`.
   It excludes the 16:30:15Z RunTask by 18 minutes -- so the criterion, which counts hand-started
   tasks *in the cycle*, would print **`HAND_ENFORCED_CEILING=0 of 2` and PASS** -- while still
   containing the 16:51:51Z swap to that task's artifact and the answers it freshened. The window
   would move the RunTask out of the denominator without moving its EFFECT out of the window, which
   is the one thing the amended criterion measures. Declined.

## THE METHOD: EFFECT, READ FROM THE ARTIFACT, THEN COMPUTED AS A COUNTERFACTUAL

**Step 1 -- open every hand-started task** (`cycle.sh` section 4d). Its own log stream gives the
window; CloudTrail's `requestParameters` gives the container command verbatim. Neither is an
inference about the task, and neither is the fact that a hand started it.

**Step 2 -- attribute a served vintage to a task, on BOTH limbs or neither** (`cycle_hand_effect.py`):

- **CONTAINMENT.** The vintage instant falls inside the task's own execution window. A vintage is
  the **source-warehouse commit instant**, not a build time: the manifest carries the same value
  three times (`vintage`, `committed_at`, `source_vintage.{nodes,edges}_metadata_last_modified`), so
  "the source data was committed while this task was running" is read from the artifact.
- **FAMILY CONSISTENCY.** The manifest's `(writer_id, mode)` is a form that task's family produces.

Containment alone convicts any task that merely overlapped somebody else's commit; family
consistency alone convicts every derive-runner that ever ran. **A family with no declared form, an
unreadable manifest, or an unreadable/empty task window FAILS CLOSED** -- it attributes *everything*
to the task rather than nothing, because the cheap bug here is a window that collapses to zero width
and silently excuses every hand.

**Step 3 -- compute the effect, do not argue it.** Remove every timeline entry serving an attributed
vintage and re-age all 261 answers; the previous vintage simply stays served for longer, which is
what would have happened had the task never run. The task made a served answer fresher iff some
answer's age **strictly increases**. *Stated limit:* a later incremental build is assumed to keep its
own vintage, because a vintage is the source commit instant and does not depend on which projection
the incremental was layered onto -- so ages after the next non-attributed swap are unchanged by
construction and the measured effect is bounded to the interval between the two swaps.

## THE ZERO IS CONTROLLED BEFORE IT IS SPENT

`HAND_ENFORCED_CEILING` is a count of absences on two of three tasks, so the arm is proven able to
fire first, on a producer nobody's hand started:

> `CONTROL 2026-09-05T02:00:05Z (events-rule/opal-globgrph-derive-runner-nightly): removing its
> vintage would have aged 30 answer(s), max +4705.316 s, over 2026-09-05T02:55:09Z .. 03:32:29Z`
> `EFFECT_POSITIVE_CONTROL=FIRED`

The identical chain shape from a **scheduled** derive-runner (RunTask 02:00:05Z -> warehouse commit
02:11:10.919Z -> pipe-started projection worker 02:11:13Z -> swap 02:23:34Z) fires the counterfactual.
So `EFFECT=NONE` on the two trino tasks is a **measured absence**, not a dead instrument. The script
returns non-zero and refuses to print a count at all if the control does not fire.

## THE CHAIN THAT COUNTS, ON FOUR PLANES THAT DO NOT SHARE A PRODUCER

1. **Control plane** -- CloudTrail `RunTask` 2026-09-04T16:30:15Z, `globgrph-derive-runner:7`,
   `startedBy=wk-cldgrph-1-cgs15`, `userIdentity=IAMUser/Andrew_Berman`, task
   `4a1baae562c8496983eb068146ae33d5`.
2. **The task's own log** -- `/ecs/globgrph/derive-runner`, stream
   `derive-runner/derive-runner/4a1baae5...`: first event `1788539450256` = 16:30:50Z, last
   `1788539984914` = 16:39:44Z (paged to exhaustion: the next forward token returns 0 events), ending
   `OK: DERIVE_RUNNER_COMPLETE date=20260904 batch_ts=1788539433147`.
3. **The artifact** -- `projection/2026-09-04T16:38:39.485910+00:00/_build_manifest.json`:
   `writer_id=derive_runner`, `producer.mode=full`, `built_at=2026-09-04T16:51:03.403904+00:00`, and
   `source_vintage.nodes_metadata_last_modified == edges_metadata_last_modified ==
   2026-09-04T16:38:39.485910+00:00` -- **inside the task's own window**.
4. **The service's own log** -- `projection swap complete` at 2026-09-04T16:51:51Z carrying that
   vintage; the next swap is 2026-09-04T18:12:58Z (vintage 18:11:48.783142Z).

The 61-event RunTask census contains exactly **two** derive-runner runs: this one and the nightly.
Nothing else in the cycle could have produced a `mode=full` vintage at that instant.

## WHAT THE ARM NOW SAYS ABOUT FWD-4, WITHOUT GRADING IT

The **ceiling** held by itself: 18138.643 s against 87191.260 s, 20.8% of budget. **Removing the hand
act does not move that number at all** -- the counterfactual oldest is *identical*, 18138.643 s,
because the oldest answer of the cycle lies outside the interval the hand act touched. The 20 answers
it did touch would have reached at most **12197.572 s**, 14.0% of the ceiling. So the hand did not
rescue the ceiling and did not even bear on the arm that measures it; it moved *freshness* for 81
minutes, which is a different property and is exactly the one the amended criterion asks about. Whether FWD-4's acceptance -- *"no one is
handed an answer older than the last scheduled refresh"* -- is about the ceiling holding or about no
person moving freshness is a reading of the endpoint, and that reading is `3.0.0_SA_CVO`'s at L9 and
`1.0.0_SA_CTO`'s in the PRD. It is not this worker's, and no verdict on it is offered here.

## ROWS FILED THIS PASS (channel: 96 rows at base -> 98; counted by PARSING every fenced block)

- **`NFRA_CLDGRPH-W1-S24`** -- `.tools/jq.exe` emits CRLF too. Row W1-S18 recorded that hazard for
  `.tools/aws` and `cycle.sh`'s control is scoped to the aws shim; jq is a second carrier and the
  scoped control could not see it. It bit this pass's own new code and **failed closed**
  (`NO_LOG_CONFIG` on 4 of 4 tasks) rather than returning a wrong count -- had the join failed open,
  `HAND_ENFORCED_CEILING` would have read `0 of 3` with no visible defect at all. Fixed in the
  instance; ARMED on the uncensused population, `disarm_owner 2.0.0_SA_COO~A`.
- **`NFRA_CLDGRPH-W1-S25`** -- the amendment's worked example is contradicted by the artifact: the
  CG-s-15 rebuild's output WAS served. ARMED, `disarm_owner 2.0.0_SA_COO~A`.

W1-S20..W1-S23 stand exactly as written and none was edited.

## THE PASS-2 KEY=VALUE SET

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-D-10",
  "cell": "CG-x-4",
  "pass": 2,
  "scope": "D10-AC3 only (amended 2026-09-05 ~16:4xZ on ruling 9f4a57262f)",
  "base_head": "497ffff69c",
  "CYCLE_START": "2026-09-04T13:00:00Z",
  "CYCLE_END": "2026-09-05T13:00:00Z",
  "cycle_unchanged_from_pass_1": true,
  "HAND_ENFORCED_CEILING": "1 of 3",
  "HANDS_OFF_RUNTASK": "3 of 61",
  "WRITERS_IN_CYCLE": "{cse_producers_nightly, derive_runner, incremental_updater}",
  "ANSWERS_IN_CYCLE": 261,
  "SWAPS_IN_CYCLE": 38,
  "NIGHTLY_SWAP_AT": "2026-09-05T02:23:34Z",
  "OLDEST_AGE_SERVED_S": 18138.643,
  "OLDEST_AGE_SERVED_S_COUNTERFACTUAL_NO_HAND": 18138.643,
  "OLDEST_AGE_SERVED_S_COUNTERFACTUAL_NOTE": "identical to the measured value: the cycle's oldest answer is outside the interval the hand act touched",
  "MAX_AGE_AMONG_HAND_AFFECTED_ANSWERS_COUNTERFACTUAL_S": 12197.572,
  "CEILING_S": 87191.260,
  "WITHIN_CEILING": true,
  "UNPLACED_ANSWERS": "0 of 3151",
  "runtask_labels": {"PIPE": 54, "SCHEDULER_EVENTS_RULE": 3, "SCHEDULER_CHRONOS": 1, "HAND": 3, "sum": 61, "label_sum_control": "AGREE"},
  "positive_control": {"task": "events-rule/opal-globgrph-derive-runner-nightly", "at": "2026-09-05T02:00:05Z", "answers_aged_by_removal": 30, "max_delta_s": 4705.316, "verdict": "FIRED"},
  "hand_tasks": [
    {"at": "2026-09-04T13:41:39Z", "family": "globgrph-trino", "task": "540a18975358499dbe8afd783ad8381f", "own_window_s": 57.7, "ran": "read-only SELECT on the Trino statement API", "attributed_vintages": 0, "effect": "NONE"},
    {"at": "2026-09-04T16:30:15Z", "family": "globgrph-derive-runner", "started_by": "wk-cldgrph-1-cgs15", "task": "4a1baae562c8496983eb068146ae33d5", "own_window_s": 569.9, "ran": "the derive-runner image entrypoint (no command override)", "attributed_vintages": 1, "vintage": "2026-09-04T16:38:39.485910+00:00", "served_from": "2026-09-04T16:51:51Z", "served_until": "2026-09-04T18:12:58Z", "answers_made_fresher": 20, "max_delta_s": 6798.156, "affected_span": "2026-09-04T16:57:07Z .. 2026-09-04T18:08:38Z", "effect": "FRESHER"},
    {"at": "2026-09-04T21:18:53Z", "family": "globgrph-trino", "task": "cc317e333c004f2d8a0ff2e07883f4ef", "own_window_s": 49.8, "ran": "read-only SELECT on the Trino statement API", "attributed_vintages": 0, "effect": "NONE"}
  ],
  "criteria": {"D10-AC1": "PASS", "D10-AC2": "PASS", "D10-AC3": "FAIL", "D10-AC4": "PASS", "D10-AC5": "UNVERIFIABLE-BY-INSTRUMENT (3.0.0_SA_CVO)"},
  "order_flipped": false,
  "rows_filed": ["NFRA_CLDGRPH-W1-S24", "NFRA_CLDGRPH-W1-S25"]
}
```

## THE GRADED INVOCATIONS, PASS 2, VERBATIM

```
$ timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/cycle.sh | grep -E '^(HAND_ENFORCED_CEILING|HANDS_OFF_RUNTASK|WRITERS_IN_CYCLE)='
HAND_ENFORCED_CEILING=1 of 3
HANDS_OFF_RUNTASK=3 of 61
WRITERS_IN_CYCLE={cse_producers_nightly, derive_runner, incremental_updater}
PIPELINE_RC=0
  -- the pipeline's rc is grep's, not the script's; cycle.sh's OWN rc read UNPIPED is 0 (70 s
     against the order's 120 s bound).  D10-AC3 FAILS: <expect> requires HAND_ENFORCED_CEILING=0
     of [0-9]+ and the measured value is 1 of 3.  Denominator: 3 hand-started tasks of 61 RunTask
     events, each one opened and read individually above.

$ timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/cycle.sh | grep -E '^(OLDEST_AGE_SERVED_S|CEILING_S|WITHIN_CEILING)='
OLDEST_AGE_SERVED_S=18138.643
CEILING_S=87191.260
WITHIN_CEILING=true
PIPELINE_RC=0
  -- D10-AC1 PASSES.  Denominator: 261 placed answers, 0 unplaced of 3151 http lines.

$ timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/cycle.sh | grep -E '^(ANSWERS_IN_CYCLE|SWAPS_IN_CYCLE|NIGHTLY_SWAP_AT)='
ANSWERS_IN_CYCLE=261
SWAPS_IN_CYCLE=38
NIGHTLY_SWAP_AT=2026-09-05T02:23:34Z
PIPELINE_RC=0
  -- D10-AC2 PASSES.  Denominator: 39 vintage-setting log events in the window plus the seed.

$ timeout 120 python -m pytest infra/aws/globgrph/tests/test_projection_server.py -q -k "backward or refus"
...                                                                      [100%]
3 passed, 4 deselected in 0.50s
RC=0
  -- D10-AC4 PASSES, rc read UNPIPED.  Denominator: 3 selected of 7 collected.
```

## THE PASS-2 RUN IN FULL (`cycle.sh`, unpiped, rc 0, 70 s)

```
=== TO-CG-D-10 / CG-x-4 -- FWD-4: THE CEILING HOLDS BY ITSELF
READ_AT=2026-09-05T17:30:26Z
REPO_HEAD=497ffff69c44612fec7ca0df918bb3d39d67536e
WINDOW_MS=1788526800000 -> 1788613200000   (pinned, closed, 24h)

--- 1. THE SERVED-VINTAGE TIMELINE (the service's own log)
The access line carries NO vintage (projection_server.py:499-500), so an answer is placed
against this timeline.  BOTH vintage-setting lines are read: the watcher's swap (:406) AND
startup's 'open read-only' (:514) -- startup's install returns "started", never "swapped",
so a swaps-only timeline SILENTLY LOSES the served vintage across a task replacement.
  TIMELINE_IN_WINDOW: rc=0  pages=1  events=39

--- 1b. THE SEED: the vintage already being served at CYCLE_START (24h lookback before it)
Without this the first answers of the cycle are UNPLACEABLE and would be silently dropped.
  TIMELINE_SEED_LOOKBACK: rc=0  pages=1  events=37

--- 1c. STREAMS THE WINDOW SPANS (a timeline crossing a task replacement must say so)
  stream serving/globgrph-serving/8889156e83ad4e3e95931e9d505169a9  first=1788539209370 last=1788624467986
  stream serving/globgrph-serving/c18ee8b40e4a4bf3993f8f78cc2f98a6  first=1788460959874 last=1788539258092
  STREAMS_TOTAL_IN_GROUP=2   (read rc=0)

--- 2. THE ANSWERS (every http line in the window; POST /cypher is the served answer)
  HTTP_IN_WINDOW: rc=0  pages=1  events=3151

--- 2b. THE REFUSAL CENSUS (the seam that keeps a stale artifact off the wire)
  REFUSALS: rc=0  pages=1  events=0

--- 4. HANDS OFF, limb (i): every RunTask in the cycle, paginated to a real denominator
  RUNTASK_PAGES=2  RUNTASK_EVENTS_FETCHED=61  (read rc=0)
  INSTRUMENT QUALIFIER: CloudTrail management-event delivery lags up to ~15 min; this window
    closed at 2026-09-05T13:00:00Z and is read after it, so no in-window event is undelivered.

--- 4b. HANDS OFF, limb (ii): CloudTrail on the POINTER KEY itself (projection/current.json)
  POINTER_KEY_EVENTS=0 (read rc=0)
  POINTER_TRAIL_COVERAGE=UNKNOWN -- S3 DATA events are not enabled on this trail, so a
    zero here CANNOT distinguish 'nobody wrote the pointer' from 'the trail does not see
    object writes at all'.  The order anticipates exactly this and routes the question to
    the manifests' writer_id instead (WRITERS_IN_CYCLE), a PRODUCER-side record that is
    not subject to this gap.

--- 4c. AN UNCOVERED MEMBER OF THE HANDS-OFF DOMAIN, printed because the census cannot see it
The order's hands-off definition enumerates two members: RunTask and a pointer PutObject.
A control-plane ecs:UpdateService is NEITHER, yet it replaces the SERVING task inside the
cycle -- and a task replacement re-seats the served vintage from whatever the pointer then
says.  A hands-off claim that cannot see it is scoped narrower than its own sentence.
  UPDATESERVICE 2026-09-04T16:26:11Z | identity=IAMUser/arn:aws:iam::313476888478:user/Andrew_Berman | service=arn:aws:ecs:us-east-1:313476888478:service/opal-globgrph/globgrph-serving | taskDefinition=arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-serving:2

  SEED_SET_AT_MS=1788526164556  SEED_VINTAGE=2026-09-04T12:48:00.440101+00:00
  swap-complete lines inside the window: 38
  POSITIVE CONTROL for the CloudWatch filter instrument -- it must find something before any
    zero of its counts as an absence: 'POST /cypher' lines = 264, swap lines = 38.
  REFUSALS_IN_CYCLE=0 (the read returned rc=0, so this is a MEASURED absence and not a
    dead arm -- the same instrument on the same window returned the two non-zero counts above)

--- 3. THE WRITER CENSUS -- every vintage served in the cycle, from ITS OWN manifest
  DISTINCT_VINTAGES_TO_READ=39
  MANIFEST_CACHE_HITS=39  MANIFEST_LIVE_READS=0  (cache: /c/Users/AndrewBerman/Desktop/wk-CLDGRPH-d10b/org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/manifest_writer_cache.tsv)

--- 4d. EACH HAND-STARTED TASK OPENED: its own execution window and its own command
  TASKS_TO_OPEN=4  (every HAND task in the cycle, PLUS the
    scheduled nightly derive-runner, opened ONLY to serve as the positive control: the
    counterfactual arm must be shown to FIRE before any hand task's zero is believed)
  WINDOWS_FROM_CACHE=0  WINDOWS_FETCHED_LIVE=4  WINDOWS_TOTAL=4
  (a READ_FAILED / EMPTY_STREAM / NO_LOG_CONFIG row is kept AS A FAILURE so the attribution
   join fails CLOSED on that task rather than quietly excusing it)
    window be97f46226f74bae86b9cf853e78763c rc=0 first_ms=1788573648761 last_ms=1788574346404
    window cc317e333c004f2d8a0ff2e07883f4ef rc=0 first_ms=1788556777165 last_ms=1788556782765
    window 4a1baae562c8496983eb068146ae33d5 rc=0 first_ms=1788539450256 last_ms=1788539984914
    window 540a18975358499dbe8afd783ad8381f rc=0 first_ms=1788529350477 last_ms=1788529356701
  THE COMMAND EACH HAND TASK RAN (verbatim from CloudTrail's own requestParameters):
    2026-09-04T21:18:53Z | globgrph-trino | cmd=B=http://trino.opal-globgrph.local:8080; q(){ echo "@@CHQ@@ $1"; r=$(curl -s -XPOST "$B/v1/statement" -H 'X-Trino-User: comp-heat' --data "$1"); echo "$r"; n=$(echo "$r" | grep -o '"nextUri":"[^"]*"' | head -1 | sed 's/.*"nextUri":"//;s/"$//'); i=0; while [ -n "$n" ] && [ $i -lt 90 ]; do i=$((i+1)); r=$(curl -s "$n"); echo "$r"; n=$(echo "$r" | grep -o '"nex
    2026-09-04T16:30:15Z | globgrph-derive-runner:7 | cmd=(none -- the image entrypoint runs)
    2026-09-04T13:41:39Z | globgrph-trino | cmd=B=http://trino.opal-globgrph.local:8080; q(){ echo "@@CHQ@@ $1"; r=$(curl -s -XPOST "$B/v1/statement" -H 'X-Trino-User: comp-heat' --data "$1"); echo "$r"; n=$(echo "$r" | grep -o '"nextUri":"[^"]*"' | head -1 | sed 's/.*"nextUri":"//;s/"$//'); i=0; while [ -n "$n" ] && [ $i -lt 90 ]; do i=$((i+1)); r=$(curl -s "$n"); echo "$r"; n=$(echo "$r" | grep -o '"nex

--- 5. THE AGE JOIN
TIMELINE_RAW_LINES=40  TIMELINE_EVENTS_PARSED=40
HTTP_RAW_LINES=3151  HTTP_LINES_PARSED=3151
PLACEMENT_METHOD=last-vintage-setting-event-at-or-before-answer (event ts => UPPER BOUND age)
UNPLACED_ANSWERS=0 of 3151
  http_status 200 = 3148
  http_status 500 = 3
  route GET/health = 2887
  route POST/cypher = 264
SERVED_POST_CYPHER_200=261
TOP5_OLDEST_ANSWERS (age_s | answered_at | served_vintage):
  18138.643 | 2026-09-04T23:14:07.426000Z | 2026-09-04T18:11:48.783142+00:00
  18130.814 | 2026-09-04T23:13:59.597000Z | 2026-09-04T18:11:48.783142+00:00
  15972.629 | 2026-09-04T22:38:01.412000Z | 2026-09-04T18:11:48.783142+00:00
  15805.890 | 2026-09-05T10:19:08.461000Z | 2026-09-05T05:55:42.571886+00:00
  15796.385 | 2026-09-05T10:18:58.956000Z | 2026-09-05T05:55:42.571886+00:00
OLDEST_AGE_CANDIDATE=18138.643
WIDER_BOUND_OLDEST_AGE_ANY_HTTP_S=22649.197
  cycle_ages.py rc=0

--- 6. THE CEILING, THE WRITERS, THE RUNTASK LABELS
VINTAGES_SERVED_IN_CYCLE=39 distinct (incl. the seed served at CYCLE_START)
MANIFEST_READS_OK=39 of 39
  writer cse_producers_nightly = 1 vintage(s)
  writer derive_runner = 3 vintage(s)
  writer incremental_updater = 35 vintage(s)
WRITERS_VALUE={cse_producers_nightly, derive_runner, incremental_updater}
NIGHTLY_CANDIDATES=1 (full + derive_runner + swap in the 02:00-04:00Z band)
  2026-09-05T02:23:34Z | vintage 2026-09-05T02:11:10.919000+00:00 | built_at 2026-09-05T02:23:22.179104+00:00
CEILING_ARITHMETIC: 86400 (cron period) + 731.260104 (built_at 2026-09-05T02:23:22.179104+00:00 - vintage 2026-09-05T02:11:10.919000+00:00) + 60 (watcher interval) = 87191.260104
NIGHTLY_SWAP_AT_VALUE=2026-09-05T02:23:34Z
CHAIN_S_VALUE=731.260
CEILING_S_VALUE=87191.260
RUNTASK_EVENTS_CLASSIFIED=61
  label HAND = 3
  label PIPE = 54
  label SCHEDULER_CHRONOS = 1
  label SCHEDULER_EVENTS_RULE = 3
RUNTASK_LABEL_SUM=61 (must equal RUNTASK_EVENTS_CLASSIFIED=61): AGREE
  HAND_ROW 2026-09-04T21:18:53Z | startedBy='' | invokedBy=- | identity=IAMUser/arn:aws:iam::313476888478:user/Andrew_Berman
  HAND_ROW 2026-09-04T16:30:15Z | startedBy='wk-cldgrph-1-cgs15' | invokedBy=- | identity=IAMUser/arn:aws:iam::313476888478:user/Andrew_Berman
  HAND_ROW 2026-09-04T13:41:39Z | startedBy='' | invokedBy=- | identity=IAMUser/arn:aws:iam::313476888478:user/Andrew_Berman
RUNTASK_HAND_VALUE=3
RUNTASK_TOTAL_VALUE=61
  cycle_census.py rc=0

--- 6b. D10-AC3 AS AMENDED: DID ANY HAND-STARTED TASK MAKE A SERVED ANSWER FRESHER?
Not 'was a hand involved' (it was, 3 times, and that count is still printed below) but
whether the ARTIFACT a hand-started task produced was SERVED and displaced an older one.
The effect is COMPUTED as a counterfactual re-ageing, and the arm is proven able to fire
on a SCHEDULED producer before any hand task's zero is spent as an absence.
EFFECT_BASE: answers=261  timeline_entries=40  unplaced=0
EFFECT_POSITIVE_CONTROL -- the counterfactual arm must FIRE on a SCHEDULED producer
  before any per-task zero below is spent as an absence.  Control: the cycle's own
  nightly derive-runner, started by an EventBridge rule, not by a hand.
    own-log window 2026-09-05T02:00:05Z .. 2026-09-05T02:12:26Z (task ran 741.4 s past its RunTask call)
    ATTRIBUTED 2026-09-05T02:11:10.919000+00:00 (contained AND writer_id=derive_runner mode=full is family globgrph-derive-runner's form)
    CONTROL 2026-09-05T02:00:05Z (events-rule/opal-globgrph-derive-runner-nightly): removing its vintage would have aged 30 answer(s), max +4705.316 s, over 2026-09-05T02:55:09Z .. 2026-09-05T03:32:29Z
EFFECT_POSITIVE_CONTROL=FIRED -- the arm can detect a freshening effect, so a per-task
  zero below is a MEASURED absence and not a dead instrument.

HAND_TASKS_IN_CYCLE=3 (the denominator N; every one is examined below)
  HAND_TASK 2026-09-04T13:41:39Z | family=globgrph-trino | startedBy=(empty) | task=540a18975358499dbe8afd783ad8381f
      own-log window 2026-09-04T13:41:39Z .. 2026-09-04T13:42:36Z (task ran 57.7 s past its RunTask call)
      NO served vintage was committed inside this task's own window
      EFFECT=NONE -- produced no vintage that was served; it did not enforce the
      ceiling and it does not void the arm.
  HAND_TASK 2026-09-04T16:30:15Z | family=globgrph-derive-runner | startedBy=wk-cldgrph-1-cgs15 | task=4a1baae562c8496983eb068146ae33d5
      own-log window 2026-09-04T16:30:15Z .. 2026-09-04T16:39:44Z (task ran 569.9 s past its RunTask call)
      ATTRIBUTED 2026-09-04T16:38:39.485910+00:00 (contained AND writer_id=derive_runner mode=full is family globgrph-derive-runner's form)
      EFFECT=FRESHER -- 20 served answer(s) were fresher than the schedule alone
      would have made them, by up to 6798.156 s, over 2026-09-04T16:57:07Z .. 2026-09-04T18:08:38Z
      THIS COUNTS: a hand made a served answer fresher.
  HAND_TASK 2026-09-04T21:18:53Z | family=globgrph-trino | startedBy=(empty) | task=cc317e333c004f2d8a0ff2e07883f4ef
      own-log window 2026-09-04T21:18:53Z .. 2026-09-04T21:19:42Z (task ran 49.8 s past its RunTask call)
      NO served vintage was committed inside this task's own window
      EFFECT=NONE -- produced no vintage that was served; it did not enforce the
      ceiling and it does not void the arm.
HAND_ENFORCED_VALUE=1
HAND_DENOM_VALUE=3
  cycle_hand_effect.py rc=0

=============================== CG-x-4 SUMMARY ===============================
CYCLE_START=2026-09-04T13:00:00Z
CYCLE_END=2026-09-05T13:00:00Z
ANSWERS_IN_CYCLE=261
SWAPS_IN_CYCLE=38
NIGHTLY_SWAP_AT=2026-09-05T02:23:34Z
OLDEST_AGE_SERVED_S=18138.643
CEILING_S=87191.260
WITHIN_CEILING=true
HAND_ENFORCED_CEILING=1 of 3
HANDS_OFF_RUNTASK=3 of 61
WRITERS_IN_CYCLE={cse_producers_nightly, derive_runner, incremental_updater}
==============================================================================
  (HANDS_OFF_RUNTASK and WRITERS_IN_CYCLE are CARRIED UNCHANGED from the pass-1
   instrument.  They are no longer the bar -- HAND_ENFORCED_CEILING is -- but the
   ruling requires that no number the failing instrument measured is lost.)
SUPPLEMENTARY (never graded; printed so the graded numbers carry their frame):
  CEILING_CHAIN_S=731.260  (the nightly's own built_at - vintage, from ITS manifest)
  UNPLACED=0 of 3151  (answers the timeline could not place; a zero IS the coverage claim)
  STRICTER_ARM_ALL_HTTP_OLDEST_S=22649.197 -> within ceiling: true
    (every http response incl. /health, which also hands out a vintage; a WIDER population
     than the graded one, printed so the graded number cannot be the flattering cut)
  EXTRA_UPDATESERVICE_IN_CYCLE=1  (an uncovered member of the hands-off domain -- see 4c)
```

# PASS 3 -- A HAND-FREE CYCLE, ALL FIVE CRITERIA PASS, THE ORDER FLIPS

**TO** `NFRA_CLDGRPH.TO-CG-D-10` · **cell** CG-x-4 · **assignee** `0.9.0_WK_NFRA_CLDGRPH~1` ·
**branch** `wk-cldgrph-1-d10p3` · **base HEAD** `b46a1632a779ce9aa0d21d78cca0f98918fbb5f7` · **read at**
2026-09-05T21:45:26Z · **scope**: the SAME amended `D10-AC3`, re-measured over a cycle in which
nobody's RunTask ran at all -- not "0 of N enforced", but `HAND_ENFORCED_CEILING=0 of 0`. No
criterion is re-cut a second time; the `<expect>` blocks are byte-identical to pass 2's.

## THE ANSWER FIRST

**ALL FIVE CRITERIA PASS. `D10-AC1`, `D10-AC2`, `D10-AC3` and `D10-AC4` are PASS-by-output; `D10-AC5`
is a recorded reading, no verdict, per its `judgment="true"` grading. THE ORDER FLIPS TO `complete`
IN THIS PASS.**

| criterion | measured | verdict |
|---|---|---|
| `D10-AC1` | `OLDEST_AGE_SERVED_S=27049.418`, `CEILING_S=87191.260`, `WITHIN_CEILING=true` | PASS |
| `D10-AC2` | `ANSWERS_IN_CYCLE=212`, `SWAPS_IN_CYCLE=31`, `NIGHTLY_SWAP_AT=2026-09-05T02:23:34Z` | PASS |
| `D10-AC3` | `HAND_ENFORCED_CEILING=0 of 0`, `HANDS_OFF_RUNTASK=0 of 51`, `WRITERS_IN_CYCLE={cse_producers_nightly, derive_runner, incremental_updater}` | PASS |
| `D10-AC4` | `3 passed, 4 deselected in 0.22s` | PASS |
| `D10-AC5` | recorded below | judgment, no verdict |

**Why `0 of 0` is a measured clean result and not a hollow control.** Zero hand-started RunTasks fell
inside this cycle at all, so the amended criterion's own denominator is zero. The discriminating
instrument is proven live regardless: `cycle_hand_effect.py`'s positive control runs the SAME
counterfactual re-ageing against the cycle's own SCHEDULED nightly derive-runner BEFORE any zero is
reported, and it fires -- removing that vintage ages 30 answers by up to 4705.316 s. The arm that
would have caught a hand-enforced freshening is shown able to fire in this exact window; there was
simply nothing for it to catch, and that absence is a property of the cycle, not of the instrument.

## THE WINDOW: RE-DERIVED, NOT COPIED, AND CORRECTED BY ONE SECOND

The hand-off named `CYCLE_START = 2026-09-04T21:18:53Z` (the last hand RunTask's own eventTime) and
`CYCLE_END = 2026-09-05T21:18:53Z`, and required both re-derived from artifacts rather than taken on
word. Re-deriving turned up a boundary defect the hand-off's own number would have carried:

- **CloudTrail's `--start-time` is INCLUSIVE at the second.** `cloudtrail lookup-events
  --lookup-attributes AttributeKey=EventName,AttributeValue=RunTask --start-time
  2026-09-04T21:18:53Z --end-time 2026-09-04T21:19:10Z` still returns the hand RunTask at exactly
  that instant (task `cc317e333c004f2d8a0ff2e07883f4ef`, family `globgrph-trino`, IAMUser
  `Andrew_Berman`). The identical call with `--start-time 2026-09-04T21:18:54Z` returns zero events.
  Using the hand-off's own number verbatim would have left the very RunTask the window exists to
  exclude sitting inside it, printing `HANDS_OFF_RUNTASK=1 of 52` instead of `0 of 51`.
- **CYCLE_START is therefore `2026-09-04T21:18:54Z`**, one second later than the hand-off's number,
  and **CYCLE_END is `2026-09-05T21:18:54Z`**, exactly 24 h later. Filed as `NFRA_CLDGRPH-W1-S26`.
- **Condition (i), independently re-verified:** a RunTask census `2026-09-03T00:00:00Z ->
  2026-09-05T21:29:21Z` (144 events, 3 pages) labelled every row by provenance form -- `PIPE 119`,
  `SCHEDULER_EVENTS_RULE 9`, `SCHEDULER_CHRONOS 3`, `HAND 13` -- and the LAST hand-labelled event is
  the same `2026-09-04T21:18:53Z`; nothing HAND-labelled falls after it through the census read.
- **Condition (ii), independently re-verified:** the swap timeline `2026-09-04T13:00Z -> now` (39
  events) shows the seed vintage held at window-open, `2026-09-04T18:11:48.783142+00:00`
  (`writer_id incremental_updater`, swapped in at `2026-09-04T18:12:58.963Z`, well before
  `CYCLE_START`), and every one of the 31 in-window vintages is `incremental_updater` /
  `derive_runner` (the nightly, `SCHEDULER_EVENTS_RULE`) / `cse_producers_nightly` -- none
  attributable to a HAND task under `cycle_hand_effect.py`'s containment-and-family rule at either
  candidate boundary. The `2026-09-04T16:30:15Z` hand rebuild that pass 2 found effective (vintage
  `2026-09-04T16:38:39.485910+00:00`, served `16:51:51Z -> 18:12:58Z`) is entirely OUTSIDE this
  window, on the correct side by 2 h 46 min.
- **The remaining hand RunTask** (`2026-09-04T21:18:53Z`, one second before `CYCLE_START`) is a
  read-only Trino `SELECT ... GROUP BY ch.heat_band` against `iceberg.globgrph.graph_nodes` /
  `code_heat.globgrph.code_heat`, verbatim from its own `containerOverrides[0].command` -- no write,
  no vintage, already opened by pass 2 for the sibling task at `13:41:39Z` and re-confirmed here for
  this one. It would attribute zero served vintages under the attribution rule regardless of which
  side of the boundary it fell on; only the printed denominator moved.

## THE CEILING'S DEFINITION AGAINST FWD-4, AND THE METHOD'S COVERAGE (D10-AC5, a reading, no verdict)

**The ceiling's arithmetic, every term read rather than assumed:**

```
CEILING_S = 86400              the schedule's own period, cron(0 2 * * ? *), item2a.tf:439
          +   731.260104       the nightly chain's OWN duration, built_at - vintage, from ITS
                                manifest (2026-09-05T02:23:22.179104Z - 2026-09-05T02:11:10.919000Z)
          +    60               PROJECTION_WATCH_INTERVAL_SECONDS, the pointer-to-swap lag ceiling
          = 87191.260104 s
```

Against FWD-4's endpoint, *"There is a ceiling on how old any answer can be, and the ceiling belongs
to the schedule, not to a person"*: every term above is a property of the SCHEDULE (the cron period)
or of the SCHEDULED chain's own record (its manifest's `built_at`, the watcher's fixed poll interval)
-- none is a property of any person or any hand act. The measured oldest answer this cycle,
27049.418 s, is 31.0% of that ceiling; the cycle's own nightly (the one instance that sets `CHAIN_S`)
is the only vintage-producing event this arm treats as authoritative for the arithmetic, and it is
`SCHEDULER_EVENTS_RULE`-started, never HAND.

**The log method's coverage, stated so the reading is auditable.** The access line
(`projection_server.py:499-500`, `LOG.info("http " + format_string, *args)`) carries no vintage, so
every answer is PLACED against the swap/startup timeline rather than read directly, and the
CloudWatch event timestamp (emitted after `install()` returns) makes every placed age an UPPER
BOUND, never an understatement. Coverage this pass: `UNPLACED_ANSWERS=0 of 3092` -- every `POST
/cypher` and `GET /health` line in the window found a vintage-setting event at or before it,
because the SEED (the 24 h lookback before `CYCLE_START`) supplies the vintage already being served
at window-open. Nothing in this cycle required falling back to `/health`'s own `last_swap`/`vintage`
pairs as a coverage patch -- the timeline method alone placed 100% of the 3092 http lines in the
window (212 `POST /cypher` answers, 2880 `GET /health` reads, all HTTP 200, zero refusals).

## THE GRADED INVOCATIONS, PASS 3, VERBATIM

```
$ timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/cycle.sh | grep -E '^(OLDEST_AGE_SERVED_S|CEILING_S|WITHIN_CEILING)='
OLDEST_AGE_SERVED_S=27049.418
CEILING_S=87191.260
WITHIN_CEILING=true
rc=0
  -- D10-AC1 PASSES.  Denominator: 212 placed answers, 0 unplaced of 3092 http lines.

$ timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/cycle.sh | grep -E '^(ANSWERS_IN_CYCLE|SWAPS_IN_CYCLE|NIGHTLY_SWAP_AT)='
ANSWERS_IN_CYCLE=212
SWAPS_IN_CYCLE=31
NIGHTLY_SWAP_AT=2026-09-05T02:23:34Z
rc=0
  -- D10-AC2 PASSES.  Denominator: 32 vintage-setting log events in the window (31 swaps plus the seed).

$ timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/cycle.sh | grep -E '^(HAND_ENFORCED_CEILING|HANDS_OFF_RUNTASK|WRITERS_IN_CYCLE)='
HAND_ENFORCED_CEILING=0 of 0
HANDS_OFF_RUNTASK=0 of 51
WRITERS_IN_CYCLE={cse_producers_nightly, derive_runner, incremental_updater}
rc=0
  -- D10-AC3 PASSES.  Denominator: 0 hand-started tasks of 51 RunTask events in the window; the
     positive control (the cycle's own scheduled nightly) fires before this zero is spent.

$ timeout 120 python -m pytest infra/aws/globgrph/tests/test_projection_server.py -q -k "backward or refus"
...                                                                      [100%]
3 passed, 4 deselected in 0.22s
RC=0
  -- D10-AC4 PASSES, rc read UNPIPED.  Denominator: 3 selected of 7 collected.
```

**`cycle.sh`'s own rc, read UNPIPED** (a pipeline's rc is its last command's, never the script's):

```
$ timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/cycle.sh > /tmp/out.txt 2>&1; echo "RC=$?"
RC=0
```

## THE PASS-3 RUN IN FULL (`cycle.sh`, unpiped, rc 0)

```
=== TO-CG-D-10 / CG-x-4 -- FWD-4: THE CEILING HOLDS BY ITSELF
READ_AT=2026-09-05T21:45:26Z
REPO_HEAD=b46a1632a779ce9aa0d21d78cca0f98918fbb5f7
WINDOW_MS=1788556734000 -> 1788643134000   (pinned, closed, 24h)

--- 1. THE SERVED-VINTAGE TIMELINE (the service's own log)
The access line carries NO vintage (projection_server.py:499-500), so an answer is placed
against this timeline.  BOTH vintage-setting lines are read: the watcher's swap (:406) AND
startup's 'open read-only' (:514) -- startup's install returns "started", never "swapped",
so a swaps-only timeline SILENTLY LOSES the served vintage across a task replacement.
  TIMELINE_IN_WINDOW: rc=0  pages=1  events=31

--- 1b. THE SEED: the vintage already being served at CYCLE_START (24h lookback before it)
Without this the first answers of the cycle are UNPLACEABLE and would be silently dropped.
  TIMELINE_SEED_LOOKBACK: rc=0  pages=1  events=42

--- 1c. STREAMS THE WINDOW SPANS (a timeline crossing a task replacement must say so)
  stream serving/globgrph-serving/8889156e83ad4e3e95931e9d505169a9  first=1788539209370 last=1788640127988
  STREAMS_TOTAL_IN_GROUP=2   (read rc=0)

--- 2. THE ANSWERS (every http line in the window; POST /cypher is the served answer)
  HTTP_IN_WINDOW: rc=0  pages=1  events=3092

--- 2b. THE REFUSAL CENSUS (the seam that keeps a stale artifact off the wire)
  REFUSALS: rc=0  pages=1  events=0

--- 4. HANDS OFF, limb (i): every RunTask in the cycle, paginated to a real denominator
  RUNTASK_PAGES=2  RUNTASK_EVENTS_FETCHED=51  (read rc=0)
  INSTRUMENT QUALIFIER: CloudTrail management-event delivery lags up to ~15 min; this window
    closed at 2026-09-05T21:18:54Z and is read after it, so no in-window event is undelivered.

--- 4b. HANDS OFF, limb (ii): CloudTrail on the POINTER KEY itself (projection/current.json)
  POINTER_KEY_EVENTS=0 (read rc=0)
  POINTER_TRAIL_COVERAGE=UNKNOWN -- S3 DATA events are not enabled on this trail, so a
    zero here CANNOT distinguish 'nobody wrote the pointer' from 'the trail does not see
    object writes at all'.  The order anticipates exactly this and routes the question to
    the manifests' writer_id instead (WRITERS_IN_CYCLE), a PRODUCER-side record that is
    not subject to this gap.

--- 4c. AN UNCOVERED MEMBER OF THE HANDS-OFF DOMAIN, printed because the census cannot see it
The order's hands-off definition enumerates two members: RunTask and a pointer PutObject.
A control-plane ecs:UpdateService is NEITHER, yet it replaces the SERVING task inside the
cycle -- and a task replacement re-seats the served vintage from whatever the pointer then
says.  A hands-off claim that cannot see it is scoped narrower than its own sentence.

  SEED_SET_AT_MS=1788545578963  SEED_VINTAGE=2026-09-04T18:11:48.783142+00:00
  swap-complete lines inside the window: 31
  POSITIVE CONTROL for the CloudWatch filter instrument -- it must find something before any
    zero of its counts as an absence: 'POST /cypher' lines = 212, swap lines = 31.
  REFUSALS_IN_CYCLE=0 (the read returned rc=0, so this is a MEASURED absence and not a
    dead arm -- the same instrument on the same window returned the two non-zero counts above)

--- 3. THE WRITER CENSUS -- every vintage served in the cycle, from ITS OWN manifest
  DISTINCT_VINTAGES_TO_READ=32
  MANIFEST_CACHE_HITS=32  MANIFEST_LIVE_READS=0  (cache: manifest_writer_cache.tsv)

--- 4d. EACH HAND-STARTED TASK OPENED: its own execution window and its own command
  TASKS_TO_OPEN=1  (every HAND task in the cycle, PLUS the
    scheduled nightly derive-runner, opened ONLY to serve as the positive control: the
    counterfactual arm must be shown to FIRE before any hand task's zero is believed)
  WINDOWS_FROM_CACHE=1  WINDOWS_FETCHED_LIVE=0  WINDOWS_TOTAL=1
  (a READ_FAILED / EMPTY_STREAM / NO_LOG_CONFIG row is kept AS A FAILURE so the attribution
   join fails CLOSED on that task rather than quietly excusing it)
    window be97f46226f74bae86b9cf853e78763c rc=0 first_ms=1788573648761 last_ms=1788574346404
  THE COMMAND EACH HAND TASK RAN (verbatim from CloudTrail's own requestParameters):
    (this task is the cycle's own SCHEDULED nightly derive-runner, opened only as the positive
    control; it is not HAND-labelled and carries no command line here -- see section 6b)

--- 5. THE AGE JOIN
TIMELINE_RAW_LINES=32  TIMELINE_EVENTS_PARSED=32
HTTP_RAW_LINES=3092  HTTP_LINES_PARSED=3092
PLACEMENT_METHOD=last-vintage-setting-event-at-or-before-answer (event ts => UPPER BOUND age)
UNPLACED_ANSWERS=0 of 3092
  http_status 200 = 3092
  route GET/health = 2880
  route POST/cypher = 212
SERVED_POST_CYPHER_200=212
TOP5_OLDEST_ANSWERS (age_s | answered_at | served_vintage):
  27049.418 | 2026-09-05T20:25:20.659000Z | 2026-09-05T12:54:31.241426+00:00
  27044.574 | 2026-09-05T20:25:15.815000Z | 2026-09-05T12:54:31.241426+00:00
  18138.643 | 2026-09-04T23:14:07.426000Z | 2026-09-04T18:11:48.783142+00:00
  18130.814 | 2026-09-04T23:13:59.597000Z | 2026-09-04T18:11:48.783142+00:00
  15972.629 | 2026-09-04T22:38:01.412000Z | 2026-09-04T18:11:48.783142+00:00
OLDEST_AGE_CANDIDATE=27049.418
WIDER_BOUND_OLDEST_AGE_ANY_HTTP_S=30256.807
  cycle_ages.py rc=0

--- 6. THE CEILING, THE WRITERS, THE RUNTASK LABELS
VINTAGES_SERVED_IN_CYCLE=32 distinct (incl. the seed served at CYCLE_START)
MANIFEST_READS_OK=32 of 32
  writer cse_producers_nightly = 1 vintage(s)
  writer derive_runner = 1 vintage(s)
  writer incremental_updater = 30 vintage(s)
WRITERS_VALUE={cse_producers_nightly, derive_runner, incremental_updater}
NIGHTLY_CANDIDATES=1 (full + derive_runner + swap in the 02:00-04:00Z band)
  2026-09-05T02:23:34Z | vintage 2026-09-05T02:11:10.919000+00:00 | built_at 2026-09-05T02:23:22.179104+00:00
CEILING_ARITHMETIC: 86400 (cron period) + 731.260104 (built_at 2026-09-05T02:23:22.179104+00:00 - vintage 2026-09-05T02:11:10.919000+00:00) + 60 (watcher interval) = 87191.260104
NIGHTLY_SWAP_AT_VALUE=2026-09-05T02:23:34Z
CHAIN_S_VALUE=731.260
CEILING_S_VALUE=87191.260
RUNTASK_EVENTS_CLASSIFIED=51
  label PIPE = 47
  label SCHEDULER_CHRONOS = 1
  label SCHEDULER_EVENTS_RULE = 3
RUNTASK_LABEL_SUM=51 (must equal RUNTASK_EVENTS_CLASSIFIED=51): AGREE
RUNTASK_HAND_VALUE=0
RUNTASK_TOTAL_VALUE=51
  cycle_census.py rc=0

--- 6b. D10-AC3 AS AMENDED: DID ANY HAND-STARTED TASK MAKE A SERVED ANSWER FRESHER?
Not 'was a hand involved' (it was, 3 times, and that count is still printed below) but
whether the ARTIFACT a hand-started task produced was SERVED and displaced an older one.
The effect is COMPUTED as a counterfactual re-ageing, and the arm is proven able to fire
on a SCHEDULED producer before any hand task's zero is spent as an absence.
EFFECT_BASE: answers=212  timeline_entries=32  unplaced=0
EFFECT_POSITIVE_CONTROL -- the counterfactual arm must FIRE on a SCHEDULED producer
  before any per-task zero below is spent as an absence.  Control: the cycle's own
  nightly derive-runner, started by an EventBridge rule, not by a hand.
    own-log window 2026-09-05T02:00:05Z .. 2026-09-05T02:12:26Z (task ran 741.4 s past its RunTask call)
    ATTRIBUTED 2026-09-05T02:11:10.919000+00:00 (contained AND writer_id=derive_runner mode=full is family globgrph-derive-runner's form)
    CONTROL 2026-09-05T02:00:05Z (events-rule/opal-globgrph-derive-runner-nightly): removing its vintage would have aged 30 answer(s), max +4705.316 s, over 2026-09-05T02:55:09Z .. 2026-09-05T03:32:29Z
EFFECT_POSITIVE_CONTROL=FIRED -- the arm can detect a freshening effect, so a per-task
  zero below is a MEASURED absence and not a dead instrument.

HAND_TASKS_IN_CYCLE=0 (the denominator N; every one is examined below)
HAND_ENFORCED_VALUE=0
HAND_DENOM_VALUE=0
  cycle_hand_effect.py rc=0

=============================== CG-x-4 SUMMARY ===============================
CYCLE_START=2026-09-04T21:18:54Z
CYCLE_END=2026-09-05T21:18:54Z
ANSWERS_IN_CYCLE=212
SWAPS_IN_CYCLE=31
NIGHTLY_SWAP_AT=2026-09-05T02:23:34Z
OLDEST_AGE_SERVED_S=27049.418
CEILING_S=87191.260
WITHIN_CEILING=true
HAND_ENFORCED_CEILING=0 of 0
HANDS_OFF_RUNTASK=0 of 51
WRITERS_IN_CYCLE={cse_producers_nightly, derive_runner, incremental_updater}
==============================================================================
  (HANDS_OFF_RUNTASK and WRITERS_IN_CYCLE are CARRIED UNCHANGED from the pass-1
   instrument.  They are no longer the bar -- HAND_ENFORCED_CEILING is -- but the
   ruling requires that no number the failing instrument measured is lost.)
SUPPLEMENTARY (never graded; printed so the graded numbers carry their frame):
  CEILING_CHAIN_S=731.260  (the nightly's own built_at - vintage, from ITS manifest)
  UNPLACED=0 of 3092  (answers the timeline could not place; a zero IS the coverage claim)
  STRICTER_ARM_ALL_HTTP_OLDEST_S=30256.807 -> within ceiling: true
    (every http response incl. /health, which also hands out a vintage; a WIDER population
     than the graded one, printed so the graded number cannot be the flattering cut)
  EXTRA_UPDATESERVICE_IN_CYCLE=0  (an uncovered member of the hands-off domain -- see 4c)
```

## THE SWAP TIMELINE, PASS 3 WINDOW, AND THE TOP-5 OLDEST ANSWERS (JSON)

```json
{
  "cycle_start": "2026-09-04T21:18:54Z",
  "cycle_end": "2026-09-05T21:18:54Z",
  "ANSWERS_IN_CYCLE": 212,
  "SWAPS_IN_CYCLE": 31,
  "NIGHTLY_SWAP_AT": "2026-09-05T02:23:34Z",
  "OLDEST_AGE_SERVED_S": 27049.418,
  "CEILING_S": 87191.260104,
  "WITHIN_CEILING": true,
  "HAND_ENFORCED_CEILING": "0 of 0",
  "HANDS_OFF_RUNTASK": "0 of 51",
  "WRITERS_IN_CYCLE": ["cse_producers_nightly", "derive_runner", "incremental_updater"],
  "CEILING_CHAIN_S": 731.260104,
  "UNPLACED_ANSWERS": "0 of 3092",
  "STRICTER_ARM_ALL_HTTP_OLDEST_S": 30256.807,
  "STRICTER_ARM_WITHIN_CEILING": true,
  "EXTRA_UPDATESERVICE_IN_CYCLE": 0,
  "REFUSALS_IN_CYCLE": 0,
  "RUNTASK_LABELS": {"PIPE": 47, "SCHEDULER_CHRONOS": 1, "SCHEDULER_EVENTS_RULE": 3, "HAND": 0, "sum": 51},
  "swap_timeline": [
    {"at": "2026-09-04T21:18:54Z", "vintage": "2026-09-04T18:11:48.783142+00:00", "note": "SEED (already serving at CYCLE_START)"},
    {"at": "2026-09-05T00:29:24.051000Z", "vintage": "2026-09-05T00:28:21.155513+00:00"},
    {"at": "2026-09-05T00:37:25.347000Z", "vintage": "2026-09-05T00:36:33.532742+00:00"},
    {"at": "2026-09-05T00:54:27.185000Z", "vintage": "2026-09-05T00:52:45.603017+00:00"},
    {"at": "2026-09-05T02:23:34.061000Z", "vintage": "2026-09-05T02:11:10.919000+00:00"},
    {"at": "2026-09-05T03:32:39.012000Z", "vintage": "2026-09-05T03:31:16.793943+00:00"},
    {"at": "2026-09-05T05:31:47.151000Z", "vintage": "2026-09-05T05:31:07.555427+00:00"},
    {"at": "2026-09-05T05:39:48.760000Z", "vintage": "2026-09-05T05:39:20.963495+00:00"},
    {"at": "2026-09-05T05:57:50.573000Z", "vintage": "2026-09-05T05:55:42.571886+00:00"},
    {"at": "2026-09-05T11:39:12.577000Z", "vintage": "2026-09-05T11:37:57.355159+00:00"},
    {"at": "2026-09-05T12:02:14.820000Z", "vintage": "2026-09-05T12:01:37.379252+00:00"},
    {"at": "2026-09-05T12:03:15.669000Z", "vintage": "2026-09-05T12:02:49.821182+00:00"},
    {"at": "2026-09-05T12:05:16.583000Z", "vintage": "2026-09-05T12:04:14.956045+00:00"},
    {"at": "2026-09-05T12:06:17.478000Z", "vintage": "2026-09-05T12:05:11.879345+00:00"},
    {"at": "2026-09-05T12:07:18.616000Z", "vintage": "2026-09-05T12:06:22.416021+00:00"},
    {"at": "2026-09-05T12:08:19.447000Z", "vintage": "2026-09-05T12:07:48.890292+00:00"},
    {"at": "2026-09-05T12:09:20.279000Z", "vintage": "2026-09-05T12:08:32.676281+00:00"},
    {"at": "2026-09-05T12:10:21.154000Z", "vintage": "2026-09-05T12:09:12.462130+00:00"},
    {"at": "2026-09-05T12:11:22.055000Z", "vintage": "2026-09-05T12:10:36.884158+00:00"},
    {"at": "2026-09-05T12:12:22.947000Z", "vintage": "2026-09-05T12:11:27.375244+00:00"},
    {"at": "2026-09-05T12:13:23.809000Z", "vintage": "2026-09-05T12:12:05.739979+00:00"},
    {"at": "2026-09-05T12:14:24.710000Z", "vintage": "2026-09-05T12:13:33.832979+00:00"},
    {"at": "2026-09-05T12:15:25.662000Z", "vintage": "2026-09-05T12:14:56.469712+00:00"},
    {"at": "2026-09-05T12:17:26.571000Z", "vintage": "2026-09-05T12:16:58.855158+00:00"},
    {"at": "2026-09-05T12:19:27.477000Z", "vintage": "2026-09-05T12:19:10.768569+00:00"},
    {"at": "2026-09-05T12:22:28.465000Z", "vintage": "2026-09-05T12:21:25.739594+00:00"},
    {"at": "2026-09-05T12:24:29.364000Z", "vintage": "2026-09-05T12:23:09.662217+00:00"},
    {"at": "2026-09-05T12:48:31.585000Z", "vintage": "2026-09-05T12:47:37.329883+00:00"},
    {"at": "2026-09-05T12:51:32.476000Z", "vintage": "2026-09-05T12:50:45.008597+00:00"},
    {"at": "2026-09-05T12:53:33.463000Z", "vintage": "2026-09-05T12:52:19.817312+00:00"},
    {"at": "2026-09-05T12:55:34.409000Z", "vintage": "2026-09-05T12:53:04.983210+00:00"},
    {"at": "2026-09-05T12:56:35.269000Z", "vintage": "2026-09-05T12:54:31.241426+00:00"}
  ],
  "top5_oldest_answers": [
    {"age_s": 27049.418, "answered_at": "2026-09-05T20:25:20.659000Z", "served_vintage": "2026-09-05T12:54:31.241426+00:00"},
    {"age_s": 27044.574, "answered_at": "2026-09-05T20:25:15.815000Z", "served_vintage": "2026-09-05T12:54:31.241426+00:00"},
    {"age_s": 18138.643, "answered_at": "2026-09-04T23:14:07.426000Z", "served_vintage": "2026-09-04T18:11:48.783142+00:00"},
    {"age_s": 18130.814, "answered_at": "2026-09-04T23:13:59.597000Z", "served_vintage": "2026-09-04T18:11:48.783142+00:00"},
    {"age_s": 15972.629, "answered_at": "2026-09-04T22:38:01.412000Z", "served_vintage": "2026-09-04T18:11:48.783142+00:00"}
  ],
  "criteria": {"D10-AC1": "PASS", "D10-AC2": "PASS", "D10-AC3": "PASS", "D10-AC4": "PASS", "D10-AC5": "UNVERIFIABLE-BY-INSTRUMENT (3.0.0_SA_CVO)"},
  "order_flipped": true,
  "rows_filed": ["NFRA_CLDGRPH-W1-S26"]
}
```

## THE CONTROL, PASS 3, QUOTED WHOLE

```
$ timeout 120 python -m pytest infra/aws/globgrph/tests/test_projection_server.py -q -k "backward or refus"
...                                                                      [100%]
3 passed, 4 deselected in 0.22s
```

**THE ORDER FLIPS.** `NFRA_CLDGRPH.TO-CG-D-10.close-fwd4-ceiling-holds.md`'s `<status>` moves to
`complete` in the same commit as this record and the proof instance, per the flip rule: the checker
returns rc 0 and every mechanical criterion is PASS-by-output.
