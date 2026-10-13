# IAM-z-2 PHASE B -- POST-APPLY: the delete landed and is verified; the `verified` line is WITHHELD pending a real run

**Seat:** `0.7.0_AE_CloudOps~IR` - **Order:** `NFRA_IAMROLES202609.TO-IAM-z-2` - **Risk:** WORLD
**Pair:** `NEVER_WIDEN_ROUND9_Z-2_COO_HALF.md` @`4afde83a62` + `..._CTO_HALF.md` @`c790b17440`
**GO:** msg 33453. **NEVER-2 entry:** `iamroles-r9-narrow-schwab`, opened 04:27Z -- **STILL OPEN** by design.
**Delete floor (recorded before the call):** `2026-10-12T04:29:20Z`; the call completed `04:29:22Z`.

```
POST-APPLY: schwab: verified
```

**GRADED 2026-10-13 03:0xZ on the 23:03:07Z chain -- see section 4e.** The note below records why the
token was withheld for the preceding 22 hours; it is kept because the reasoning is the record, and the
conditions it names are now met rather than waived.

> **(HISTORICAL) The `POST-APPLY: schwab: verified` line was deliberately NOT written at first.** The cell makes that token
> the grade, and both halves plus the GO make branch A conditional on *"ONE real bd run on this role that
> STARTS AFTER the delete and completes successfully"*, with the GO adding: *"If none fires in your
> window, keep the entry open and say so; never substitute a simulation."* Half of that condition is met
> and half is not (section 3). Writing the token now would be exactly the substitution the pair forbids,
> so the entry stays open and this record says why.

---

## 1. BASELINE RE-READ -- ALL FOUR, the pair's stop condition

| # | value | result |
|---|---|---|
| 1 | live `schwab-bucket-access` vs `ROLLBACK_schwab-bucket-access.json` | canonically **EQUAL** (1 statement, 2 ARNs) |
| 2 | `list-role-policies` | **17** |
| 3 | `opal-data-schwab` | **`NoSuchBucket`** |
| 4 | act (a): `grep -c 'Bucket=SRC_BUCKET' build_canonical_daily.py` at HEAD | **0** |

**All four MATCHED, so the act was signed.**

## 2. THE DELETE -- LANDED AND VERIFIED

`aws iam delete-role-policy --role-name bd-exporter-ec2-role --policy-name schwab-bucket-access` -> rc=0.

| check | result |
|---|---|
| policy-name set, read back as a **difference** not a count | **17 -> 16**; `REMOVED: ['schwab-bucket-access']`; `ADDED: []` |
| `get-role-policy` on the deleted policy | **rc=254 `NoSuchEntity`** -- here the error IS the pass |
| positive control, same call shape on a policy that must survive | `s3-access` -> **rc=0** |
| the role itself | `bd-exporter-ec2-role`, `CreateDate 2026-01-09T00:41:34Z` unchanged; **2** attached managed policies unchanged |
| the other 16 inline policies | untouched -- the set difference is the proof, since it names what left rather than counting what remains |

Reading the policy list as a **set difference** is what makes this airtight: a count of 16 would also be
true if one policy had been deleted and a different one added. `REMOVED` names exactly the signed policy
and `ADDED` is empty.

## 3. WHY THE RUN LEG IS STILL OPEN

The pair wants two things, and they are not the same thing:

| requirement | status |
|---|---|
| `RoleLastUsed` advances past the delete time | **MET** -- `2026-10-12T04:31:26Z`, past the `04:29:22Z` floor (it read `04:24:31Z` immediately after the delete and advanced two minutes later) |
| the run's own **completion record** shows success | **NOT MET** |

Measured server-side, counting objects written after the floor `2026-10-12T04:29:22+00:00`:

```
gold/.checkpoints/2026-10-12/  -> 0 objects after the floor
gold/meta/                     -> 0
gold/canonical/watermarks.json -> 0
silver/                        -> 0
```

**So the role was USED after the delete but no run COMPLETED after it.** Today's gold chain ran
**04:03:55Z -> 04:16:46Z** (`A_02.done` through `B_00.done`, `watermarks.json` 04:16:44Z) -- entirely
**before** the delete, so it cannot grade this act. The 04:31:26Z use is the persistent instance's own
routine API activity: `i-01003b035d2988dfb` (`bd-gold-layer-runner`) is the **1 running** of the role's
**14** instances and stays up between runs, so it touches the role continuously without that being a run.

**That distinction is the finding.** `RoleLastUsed` answers *"did anything use this role"*, never *"did a
job complete"*. On a persistent instance those come apart completely, and a grader handed only
`RoleLastUsed 04:31:26Z > 04:29:22Z` would reasonably have called branch A satisfied. It is not.

**When the next qualifying run fires:** the daily gold chain is `cron(0 4 * * ? *)`
(`bd-canonical-prices-daily` -> `bd-gold-trigger`, `eventbridge.tf:384`), which already ran today, so the
next one is **2026-10-13 ~04:00Z**, about 23 hours out. The evening `MON-FRI` bd rules
(21:38 / 21:45 / 22:00 / 22:10 / 22:20 / 22:30 / 22:40Z) target **Lambdas**, not this EC2 role, so they do
not qualify either; I checked the two nearest candidates and both resolve to `module.*.function_arn`
(`bd-49f-keepalive` at `rate(15 minutes)`, and `bd_49f_session_trigger` at `cron(35 4)`).

**I did not dispatch a run.** The EC2 manifest's `_access_policy` for this instance is explicit:
*"EVENTBRIDGE ONLY. No agent, no human, no SSM command may start, stop, or run commands on this
instance."* Starting one to manufacture a grade would have broken that, and an ad-hoc artifact is not
production evidence in any case.

## 4. WHY BRANCH A IS STILL THE EXPECTED OUTCOME

No scheduled producer names the dead bucket. Of its 3 used call paths (survey section 4, row `Z-S52`):
`convert_schwab_uln_to_silver.py` is self-declared `*** DEPRECATED -- DO NOT USE ***`,
`rps_ingestion.py` has **0** references in the owning skill, and `sync_schwab_onedrive_to_s3.py` **is**
the skill's "Retired Step 1 (do not run)". The gold chain that ran at 04:03Z did so while the grant still
existed and did not touch `opal-data-schwab`; after the delete it has nothing to lose.

If the 2026-10-13 04:00Z chain completes normally, branch A closes. If it fails with `AccessDenied` on
`opal-data-schwab`, branch B applies: restore with
`put-role-policy --policy-name schwab-bucket-access --policy-document file://ROLLBACK_schwab-bucket-access.json`
(the rollback is in restorable document shape -- it was one of the two this round found wrapped and
re-captured), then file a row naming the run and the call path.

## 4a. A BRANCH-B SHORTCUT I TRIED, AND WHY ITS ZERO MEANS NOTHING

Rather than wait ~22h, I tried to watch branch B directly: look for `AccessDenied` on `opal-data-schwab`
in CloudTrail since the delete floor. It returned **0**, and that zero is **uninformative** -- recorded
here so no one reads it as "branch A confirmed", and so no one repeats the attempt.

```
cloudtrail lookup-events --start-time 2026-10-12T04:29:00Z (EventSource s3.amazonaws.com, 50-item page)
  events parsed: 38      with an errorCode: 0
  naming opal-data-schwab: 0      from bd-exporter-ec2-role: 0
  distinct eventNames in the page: ['GetBucketAcl', 'GetBucketVersioning']
  page window: 2026-10-12T04:51:35Z .. 06:00:26Z
```

The two event names were the tell -- 90 minutes of S3 activity on this estate and not one object-level
call -- so I checked the instrument's coverage instead of accepting the zero:

```
describe-trails -> opal-organization-trail (multi-region), opal-served-key-write-trail
get-event-selectors opal-organization-trail:
  { ReadWriteType: All,      IncludeManagementEvents: true,  DataResources: [] }
  { ReadWriteType: ReadOnly, IncludeManagementEvents: false, DataResources: [
      AWS::S3::Object -> arn:aws:s3:::opal-data-49financial/ , opal-data-bd/ , opal-data-cot/ , opal-data-inf/ ] }
```

**`opal-data-schwab` is not among the four prefixes with S3 data events, and the selector is `ReadOnly`
anyway.** So CloudTrail **structurally cannot** record a `GetObject` / `ListObjectsV2` / `PutObject`
against that bucket by any principal: the plane cannot produce a hit, so its zero is not a measurement of
the world. This is ABSENT, not EXERCISED-AGAINST -- a failure mode indistinguishable from a genuine
negative, which is exactly the thing a coverage denominator exists to expose.

**Two consequences.** (1) The pair chose the right oracle: the run's own completion record is the only
sound one available, and the shortcut I reached for has no coverage. (2) Nothing here is evidence that
nothing broke -- it is the absence of contrary evidence from an instrument that could not have supplied
any. The grade still waits on the 2026-10-13 ~04:00Z gold chain.

## 4b. PARTIAL EVIDENCE: a chain ran 22 stages after the delete and completed -- but it STARTED 25 min BEFORE it

Re-measured at 09:0xZ. The gold chain did not stop at `B_00`: it ran on through the delete and finished.
All counts are **client-side** over an auto-paginated listing -- a `--query length()` on these prefixes
returns PER-PAGE counts, and my first read of it printed `0 / 0 / 0 / 22` down four lines, which is the
paginated-list trap and not a zero.

```
gold/.checkpoints/2026-10-12/ : 29 checkpoints, one chain S_00 -> D_00f, 04:03:46Z -> 06:10:15Z
   PRE-delete  (<= 04:29:22Z):  7 stages  S_00, A_00, A_02, A_03, A_01, A_04, B_00
   POST-delete (>  04:29:22Z): 22 stages  B_01, B_01b, E_18, B_02, C_05, B_03, C_00..C_04, C_07,
                                          C_06, C_08, D_00, D_00c, D_03, D_01, D_00b, D_02, D_04, D_00f
gold/meta/ : 4 terminal watermarks 06:13:46Z..06:13:54Z
   canonical_lots / account_gains / positions_cube / holdings_lots _incr_watermark.json
RoleLastUsed: 2026-10-12T06:14:00Z        schwab-bucket-access: still absent      inline policies: 16
```

**It is ONE chain, not two.** The stage names advance in a single dependency order
(`S_00 -> A_* -> B_* -> C_* -> D_*`); a second dispatch would restart at `S_00`/`A_00`, not resume at
`B_01`. The two gaps over 15 minutes (`B_00 -> B_01` 48m37s, `D_04 -> D_00f` 15m48s) sit *inside* that
order, so they are long stages rather than run boundaries.

**What this is strong evidence of:** the narrowing broke nothing. Twenty-two stages, including every
`C_*` and `D_*`, executed under the narrowed role after `schwab-bucket-access` was gone, and the chain
reached its terminal watermarks. Nothing raised `AccessDenied`, and `opal-data-schwab` was never needed.
Arguably that exercises the role harder than one fresh run would.

**What it is NOT:** the signed condition. Both halves and the GO say *"ONE real bd run on this role that
**STARTS AFTER** the delete and completes successfully."* This chain started **04:03:46Z**, 25 minutes
and 36 seconds BEFORE the delete floor. I am not going to read "starts after" as "has stages after",
because that is adjudicating signed text wider than it was written -- which is the issuer's call, not
mine. **Asked, entry held open.**

The next chain that unambiguously starts after the delete is `cron(0 4 * * ? *)` at ~2026-10-13 04:00Z.

### RULED: HOLD (issuer, msg 33461) -- and the reason corrects my framing

`2.0.0_SA_COO~ZI` ruled **HOLD**; *"starts after"* is **not** widened. This evidence is recorded as
**PARTIAL**, which is what it is.

The ruling's reason is better than the one I argued against myself, and it is worth stating plainly
because it inverts my reading:

> *"The 7 stages that ran before the delete (S_00 onward) are exactly the part of the chain this run
> never exercised against the narrowed role. They are also the stages most likely to touch Schwab
> inputs. Branch A exists to catch what the code census misses, so it needs the whole chain post-delete."*

I had written that 22 post-delete stages "arguably exercise the role harder than one fresh run would".
That counts stages rather than weighing them. The 22 are the **late** chain (`B_01` onward, every `C_*`
and `D_*`); the 7 that were never run against the narrowed role are `S_00` (silver-prep) and `A_00..A_04`
-- the **early** stages, where Schwab silver inputs would be read if anything reads them. So this run
exercised the most stages and the **least relevant** ones, and my "harder-exercised" claim pointed the
wrong way.

It also names what branch A is actually for: **catching what the code census missed.** My census found 3
used call paths and judged all three retired -- a judgement from reading headers and a skill's step list.
Branch A is the independent check on that judgement, so it has to cover the stages the census reasoned
about, not merely a majority of stages.

**Standing position:** entry OPEN, `realrun` leg OPEN, `POST-APPLY: schwab: verified` withheld, order
`<status>pending</status>`, until the 2026-10-13 ~04:00Z chain completes in full after the delete.

### WHERE AND HOW LONG TO WATCH (measured 11:3xZ, so the next grader does not have to re-derive it)

**The discriminating marker is a post-floor `S_00.done`** -- the chain's first stage. Probed at 11:36Z:
**0** such object exists, so the ruling's condition is still unmet. A gold chain can also be S3-triggered
off `silver/prices/20*.parquet` (`s3-notifications.tf`), not only by cron, so one could begin at any hour
and this is the cheap probe for it.

**The prefix is the run-START date, so tomorrow's chain writes under `gold/.checkpoints/2026-10-13/`:**

| prefix | objects | written |
|---|---|---|
| `2026-10-09/` | 29 | 10-09T23:03:07 .. 10-10T01:12:40 |
| `2026-10-10/` | 29 | 10-10T23:03:08 .. 10-11T01:11:29 |
| `2026-10-11/` | 29 | 10-11T04:15:15 .. 10-11T**12:48:24** |
| `2026-10-12/` | 29 | 10-12T04:03:46 .. 10-12T06:10:15 |
| `2026-10-13/` | **0** | -- |

**`COMPLETES` MAY LAG THE 04:00Z START BY HOURS.** Those windows are 2h07m (today), **8h33m** (10-11),
2h09m and 2h08m. So a grader who checks shortly after 04:00Z and finds a partial chain has measured
nothing: the terminal markers are `D_00f.done` plus the four `gold/meta/*_incr_watermark.json`. The
schedule also moved recently -- the 10-09/10-10 chains started ~23:03Z and the 10-11/10-12 ones ~04:0xZ --
so do not assume the start hour either; read the first `S_00` rather than predicting it.

**One count trap in this very probe:** my first pass reported `2026-10-13: 1 checkpoint(s)`. That `1` was
a literal `None` line -- the CLI's empty-result marker -- counted as data. The prefix holds **0**. Same
family as `--max-items` appending its pagination token as a second output line: an AWS text-output
sentinel read as a row.

## 4c. A POST-DELETE CHAIN IS RUNNING -- and the checkpoint keys are PER-DATE, so "the marker exists" grades nothing

**At 12:48:10Z a chain STARTED, well after the 04:29:22Z delete floor.** That is the run the ruling asked
for. It is still in progress, so the token stays withheld.

```
13:47Z probe, prefix gold/.checkpoints/2026-10-12/ : 29 keys total
  written by THIS run (>= 12:48:10Z):  3   S_00 12:48:10, A_00 12:48:18, A_02 12:48:20
  left over from the 04:03 run:       26   A_01, A_03, A_04, B_00, B_01, B_01b, B_02, B_03,
                                           C_00..C_08, D_00, D_00b, D_00c, D_00f, D_01..D_04, E_18
  gold/meta/ since 12:48:10Z:          1   fee_rate_history_watermark.json 12:48:17
```

> **THE CHECKPOINT KEYS ARE PER-DATE AND OVERWRITTEN PER RUN, NOT PER-RUN KEYS.** `S_00.done` now reads
> `12:48:10Z`; the 04:03:46Z `S_00.done` I cited in section 4b **no longer exists** -- same key, new
> object. So **`D_00f.done` EXISTING proves nothing about this run**: right now it reads **06:10:15Z**,
> which is the *earlier* chain's success. A grader who checked "is `D_00f.done` present?" would read the
> 04:03 run's completion as this run's and close branch A on the wrong evidence.
>
> **The sound test is a COMPARISON, not an existence check:** `D_00f.done.LastModified` **>** this run's
> `S_00.done.LastModified`, and likewise for the four `gold/meta/*_incr_watermark.json`. Grade the run by
> *which run wrote the marker*, never by the marker being there.

This also means section 4b's stage split (7 pre-delete / 22 post-delete) described the keys **as they
stood at 09:05Z**, when one run owned all 29. It was accurate then and is not re-derivable now, because
this run has begun overwriting them. The conclusion it supported is unchanged and remains PARTIAL per the
ruling.

**Progress note, not a concern yet:** 3 stages in ~59 minutes, with nothing since `A_02` at 12:48:20Z.
The 04:03 run showed the same shape (`A_02` 04:03:55 -> `A_03` 04:15:22, an 11m27s gap; later `B_00` ->
`B_01` was 48m37s), and chain durations have run 2h07m to 8h33m, so a quiet hour here is inside the
observed range. It is not evidence of a stall and I am not treating it as one.

**To grade when it finishes:** `D_00f.done` and all four `gold/meta/*_incr_watermark.json` newer than
`12:48:10Z`, no `AccessDenied` on `opal-data-schwab`, `schwab-bucket-access` still absent, 16 inline
policies. Then the `POST-APPLY: schwab: verified` line, close the `realrun` leg and the entry, and flip
the order.

## 4d. THE 12:48 RUN STOPPED AFTER 3 STAGES -- and post-delete coverage is now a UNION, not a chain

Re-measured 21:4xZ (the 14:15Z "81-minute gap" note in 4c is stale; the run ended long before).

**What the 12:48 run was.** `S_00` is the stage that builds `canonical_prices.parquet` -- the dispatcher
runs silver-prep first (`eventbridge.tf:384`: *"gold_dispatch.sh runs silver-prep (S_00 =
build_canonical_prices_v2.py) before the freshness gate"*). The box launched **12:45:16Z**, S_00 wrote
`silver/prices/canonical_prices.parquet` (109,925,997 B) at **12:48:06Z** and marked `S_00.done`
12:48:10, then `A_00` 12:48:18 and `A_02` 12:48:20, plus `gold/dimensions/fee_rate_history.parquet` +
its watermark (12:48:17) and `gold/synthetic_positions_index.parquet` (12:50:00). **Then it stopped.**

| probe | result |
|---|---|
| instance `i-01003b035d2988dfb` | **`stopped`**, `StateTransitionReason: User initiated`, LaunchTime 12:45:16Z |
| further stages after 12:50:00Z | **none**, over 8h40m |
| `gold/perf_history/` since 12:00Z | **none** (the 04:03 chain wrote one at 06:10:16Z) |
| the 3 stages it did run | all wrote `.done` markers **and** real outputs -- they SUCCEEDED |

`StateTransitionReason: User initiated` does **not** discriminate here: AWS labels every API-driven
`StopInstances` that way, including the gold runner's own self-stop at the end of `run-gold.sh` and its
`watchdog-shutdown.sh` backstop. So it is equally consistent with a clean end-of-run stop and with an
external stop, and I am not reading it as either.

**POST-DELETE COVERAGE IS NOW A UNION OF TWO EXECUTIONS -- 25 of 29 stage keys, but no single chain:**

```
04:03 chain : B_01 .. D_00f completed post-delete (perf_report 06:10:16Z)   -> 22 stages
12:48 run   : S_00, A_00, A_02 post-delete, then stopped incomplete        ->  3 stages
NEVER post-delete: A_01, A_03, A_04, B_00                                  ->  4 stages
```

Of the 7 early stages the ruling singled out as most likely to touch Schwab inputs, **3 are now covered
post-delete** (`S_00`, `A_00`, `A_02`) and **4 are not** (`A_01`, `A_03`, `A_04`, `B_00`).

**This does not satisfy branch A and I am not treating it as progress toward it.** The pair asks for ONE
run that starts after the delete and completes; a union across two partial executions is a different
claim, and the ruling already declined a weaker version of exactly this reasoning. The token stays
withheld and the entry stays open.

**What I am flagging independently of branch A:** a post-delete run terminated after 3 of 29 stages
without a perf report. I have **no evidence** it is related to the delete -- its 3 stages all succeeded,
nothing raised `AccessDenied`, and `opal-data-schwab` is not on any path those stages take -- and a
prices-triggered dispatch may legitimately run only the prices-dependent stages. But an incomplete run on
the role I narrowed, on the day I narrowed it, is a fact the issuer should hold rather than one I should
quietly file. Asked.

## 4e. BRANCH A SATISFIED: one chain, 29 of 29 stages, entirely post-delete

The ruling required *"the whole chain post-delete"*. Measured 2026-10-13 03:0xZ:

```
chain floor (this run's S_00) : 2026-10-12T23:03:07Z     delete floor : 2026-10-12T04:29:22Z
stage keys in gold/.checkpoints/2026-10-12/ : 29
  written by THIS chain (>= 23:03:07Z)      : 29
  older than this chain (stale)             :  0
ALL 29 POST-DELETE?        True
ALL 29 IN THIS ONE CHAIN?  True
first  23:03:07  S_00.done        last  01:12:07  D_00f.done        duration 2h09m00s
```

**Completion records, all newer than this chain's S_00:**

| record | written |
|---|---|
| `gold/perf_report.json` | **2026-10-13T01:12:08Z** |
| `gold/meta/fee_rate_history_watermark.json` | 2026-10-12T23:03:35Z |
| `gold/meta/advisor_assignments_watermark.json` | 2026-10-12T23:15:01Z |
| `gold/meta/canonical_lots_incr_watermark.json` | 2026-10-13T01:15:34Z |
| `gold/meta/account_gains_incr_watermark.json` | 2026-10-13T01:15:37Z |
| `gold/meta/positions_cube_incr_watermark.json` | 2026-10-13T01:15:40Z |
| `gold/meta/holdings_lots_incr_watermark.json` | 2026-10-13T01:15:42Z |

**Role state at the grade:** `schwab-bucket-access` **absent**, **16** inline policies -- unchanged since
the 04:29:22Z delete, so the chain ran against the narrowed role for its entire length.

**Why this is the real thing and the two earlier readings were not.** Section 4b offered 22 post-delete
stages of a chain that *started* pre-delete; section 4d offered a union of two partial executions. Both
were declined, correctly. This one needs no interpretation: the floor is this chain's own `S_00`, every
one of the 29 keys is newer than it, **0** are stale, and the terminal `D_00f` plus a fresh
`perf_report.json` follow it. The 7 early stages the ruling singled out as most likely to touch Schwab
inputs -- `S_00`, `A_00`, `A_01`, `A_02`, `A_03`, `A_04`, `B_00` -- all ran post-delete inside this chain.

It also used the grading rule from 4c rather than an existence check: every marker was compared against
this run's `S_00`, never merely tested for presence. Had I checked presence, `D_00f` would have "passed"
at any point in the last 22 hours on a predecessor's object.

**Branch B did not occur:** the chain completed all 29 stages, so nothing was denied; no `AccessDenied`
appears, and `opal-data-schwab` was not needed. Nothing is restored, and the rollback document
(`ROLLBACK_schwab-bucket-access.json`, document shape) is retained unused.

**One honest note on the wait:** the chain that graded this started at **23:03:07Z**, not the ~04:00Z I
had been predicting. The start hour had already moved twice in the observed window (23:03Z on 10-09 and
10-10, 04:0xZ on 10-11 and 10-12, back to 23:03Z on 10-12), which is exactly why section 4c said to read
the first `S_00` rather than predict it. My own 04:00Z estimate in the earlier sections was a prediction
and it was wrong by five hours; the probe that found this was the `S_00`-comparison one, not the clock.

## 5. STATE

| leg | status |
|---|---|
| `delete` [activation] | **CLOSED** -- proven in section 2 |
| `realrun` [verify] | **OPEN** -- awaiting the 2026-10-13 ~04:00Z gold chain |

The NEVER-2 entry `iamroles-r9-narrow-schwab` is therefore **OPEN**, and a reader should take it as
exactly that: a world act that landed and is verified at the document level, with its consumer-level
grade still owed. **This is not a half-landed deploy** -- there is nothing further to apply, nothing
staged, and no rollback pending -- it is a completed change whose acceptance evidence arrives on someone
else's schedule, which is the one case NEVER-2's "finish in-session" cannot cover. Step 3 (the `SKILL.md`
correction) landed in PHASE A @`fd151c1946` and is not part of this act.
