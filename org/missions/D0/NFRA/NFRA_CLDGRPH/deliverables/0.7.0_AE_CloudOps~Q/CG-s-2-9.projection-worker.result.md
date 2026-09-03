# CG-s-2 + CG-s-9 -- the projection worker, PORTED

**Task order:** `NFRA_CLDGRPH.TO-CG-B-2` @`585daff578` (B2-AC8 cell_refs amended by the issuer @`ab9fb68d41`;
this seat did not edit the face) · **Cells:** `CG-s-2`, `CG-s-9` · **PRD:** v0.4 @`25c66d3358` R5/R9/R10/R11 ·
**Seat:** `0.7.0_AE_CloudOps~Q` · **GO:** msg 93402, READ-acked · **Round-1 stamp:** @`59af3f1df5`

> **STATUS OF THIS FILE: section 1 is COMPLETE and final. Sections 2-5 are IN PROGRESS.** Section 1 is
> written FIRST and BEFORE any build because `B2-AC1` requires exactly that, and because a runtime chosen
> after the code is written is a rationalisation, not a decision. Sections 4 (exercise) and the IAM limb of
> section 3 are **BLOCKED on `CG-s-1`**, measured not assumed -- see s.6.

---

## 1. `B2-AC1` -- THE RUNTIME DECISION

### 1.0 The rule the fit table fixed, restated as a constraint

**THE FULL FALLBACK NEVER RUNS UNDER A 900 s CEILING.** From `CG-s-10` @`a9aea6f3ce`, this seat's own
measurement: the full load ran **1001.172 s** and **935.500 s** (2 of 2 runs), the full-fallback
**940.594-1006.266 s**, peak **6,752.0 MB**. Run-to-run spread **+/-3.39%** is SMALLER than the shortfall
against 900 s, so this is not a case a faster run rescues. **Any design that can put the full path on a
900 s ceiling is refused by this criterion regardless of other merit.**

And the fact that decides the shape rather than just the ceiling: **the full load is the DAILY path.**
The nightly whole-table overwrite rewrites every `snapshot_ts`; the incremental diff keys on `snapshot_ts`
(`kuzu_incremental_refresh.py:165-166`); so the delta-size gate at `:174` reads 100% changed after every
overwrite (INC-A measured 27,133 of 27,133 with **11** real changes) and trips to the full load every
morning. **The 900 s finding therefore binds the ordinary path, not a rare one.**

### 1.1 THE DECISION

**ONE ECS Fargate one-off task runs BOTH paths, triggered from `CG-s-1`'s queue.** No Lambda executes any
part of the engine.

| axis | decision | the measured number beside it |
|---|---|---|
| **Runtime** | ECS Fargate one-off task (`RunTask`) on the existing `opal-globgrph` cluster | full-fallback **940.594-1006.266 s** vs Lambda's hard 900 s ceiling -- exceeded in **2 of 2** runs |
| **CPU** | `2048` (2 vCPU) | measured ~**1,073 CPU-seconds over ~935 s wall = ~1.15 cores sustained**; 2 vCPU gives headroom without a Fargate step to 4 vCPU |
| **Memory** | `16384` MB | measured peak **6,752.0 MB** (2.43x headroom). NOT sized to 8192 (1.21x) deliberately -- see 1.3 |
| **Ephemeral** | Fargate default (20 GB) | measured peak on disk **~53.8 MB** (DB 44.8 + WAL). 0.26% of default; no override needed |
| **Rebuild deadline** | `KUZU_REBUILD_DEADLINE_S` set **EXPLICITLY to 3600** | the engine's 1800 s default is justified in-source as "5x headroom" over the falsified ~6 min figure; against the measured 1001.172 s it is **1.80x**. See row `NFRA_CLDGRPH-S10` |
| **Queue visibility timeout** | **2400 s** | the longest step that holds the message is the whole task: cold start (UNMEASURED, closed by B2-AC6) + up to the 3600 s deadline... see 1.4, which is why this number is stated as PROVISIONAL-ON-AC6 |
| **Trigger** | EventBridge **Pipe**, SQS source -> `ecs:RunTask` target | see 1.2 |

### 1.2-RESTATED (2026-09-03 ~12:4xZ) -- the mechanism limb, corrected on a MEASURED read

⛔ **This subsection supersedes 1.2 below on ONE point: who the consumer of record is.** 1.2 is kept
verbatim underneath because a decision document that quietly rewrites its own rejected alternatives is
worse than one that shows the correction. Row `NFRA_CLDGRPH-S14` @`6c02972` carries the finding; the
issuer confirmed NO face amendment is needed (93623) because `B2-AC1`'s own words -- *"the queue's
visibility timeout set from the measured numbers (>= the longest step that HOLDS the message)"* -- already
admit this reading.

**WHAT I GOT WRONG.** 1.2 rejected a Pipe that "deletes the message on RunTask acceptance" and concluded
*"the task itself is the consumer of record"*. **Measured on the live API surface:** a Pipes SQS source
exposes only `BatchSize` and `MaximumBatchingWindowInSeconds` -- no retention, no defer-ack, no on-failure
control, where the Kinesis and DynamoDB sources in the same skeleton do carry retry options. The Pipe owns
receive/delete around a `RunTask` that returns on ACCEPTANCE. **The rejection of the naive form was right;
the claim that the chosen form escaped it was wrong.** No Pipe/SQS shape, and no Lambda event-source
mapping, can make a ~16-minute ECS task the SQS consumer of record.

**THE DECISION, RE-STATED:**

| | |
|---|---|
| **Consumer of record** | **the PIPE**, not the task. Stated plainly because the wiring cannot support the alternative. |
| **Visibility timeout** | derived from the **PIPE's** hold, NOT the run duration. With `BatchSize` 1 and `MaximumBatchingWindowInSeconds` 0 the Pipe holds a message for one `RunTask` API call. **The applied 30 s placeholder already exceeds that with wide margin, so the declared value is 30 s and `~P`'s resource needs no change.** The hold is CONFIRMED by measurement at `B2-AC6` and the number re-derived there if the observation disagrees. |
| **Retry property** | **NOT SQS redrive.** A task that dies mid-run leaves no message to redrive. Recovery is **marker idempotency** -- the next stamp rebuilds from HEAD regardless -- plus the **nightly derive at 02:00Z**, which bounds the worst case at one day. That is a smaller and truer claim than the one 1.2 made. |
| **Ceiling rule** | UNAFFECTED. The work still runs in an ECS task with no wall-clock ceiling; 940.6-1006.3 s never meets a 900 s limit under any of these shapes. |

⚠ **The issuer RETRACTED, narrowly, its own endorsement of 2400 s** (93623 item 2): that number's stated
derivation from the V-1 run duration presupposed the task holding the message, which S14 measured false.
**2400 s is withdrawn as the declared value.** Nothing else in 93565 changes.

**A RECORDED RESIDUAL, not a re-apply** (93623 item 3): under this mechanism the **Pipe's execution role**
carries the consume grant (`sqs:ReceiveMessage`/`DeleteMessage`/`GetQueueAttributes` + `ecs:RunTask` +
`iam:PassRole`), and `~P`'s `aws_iam_role_policy.projection_worker_sqs` on the worker role becomes **dead**.
It **stays applied this round**: an unused grant to our own role widens no exposure, and removing it would
be an edit of `CG-s-1`'s applied resource. Named here with its address so it is a recorded residual rather
than a silent orphan; it retires with `CG-s-8`'s cleanup round.

### 1.2 The queue-to-compute mechanism, and the two designs I did not choose
*(SUPERSEDED on the consumer-of-record point by 1.2-RESTATED above; kept as the record of the reasoning
and of its correction.)*

The face admits three shapes. All three can satisfy the ceiling rule; they are not equally good.

**CHOSEN -- EventBridge Pipe from `CG-s-1`'s queue to `ecs:RunTask`, one task for both paths.**
The engine already decides internally which path it takes: `refresh()` returns `("fallback", ...)` at
`:174` and the caller runs the full load. **That decision is INSIDE the engine, so it cannot be used to
route between runtimes without first paying for it** -- INC-A measured **5.094 s** to reach it, because
reaching it requires reading the head tables and diffing against the current artifact. A router that
picks a runtime *before* the engine runs is guessing; a router that picks after has already started
computing. One runtime removes the question.

**NOT CHOSEN -- a Lambda consumer that runs the incremental in-function and launches ECS on fallback.**
It satisfies the ceiling rule and it is the cheapest per intraday stamp (5.1-7.5 s at ~465 MB fits Lambda
comfortably). I rejected it on three measured grounds: (i) it puts ONE engine behind TWO runtimes, two
IAM principals and two deployment surfaces, and the face's own bound is *one engine, one source* -- not
violated by two runtimes, but this is where that bound starts to fray; (ii) the Lambda would pay the
**5.094 s** diff before discovering the fallback, then re-pay the whole diff again inside the ECS task,
because the task starts from scratch -- the work is duplicated on the daily path, which is the path that
matters; (iii) the latency it buys is not an outcome anyone asked for. The brief's O3b wants the age of an
answer **BOUNDED**, not small; nothing in the PRD or the brief asks for sub-minute projection freshness.
**If a stated intraday-latency requirement ever lands, the Pipe's target can be split then, and this
paragraph is the record of what would have to change.**

**NOT CHOSEN -- Pipe straight to `RunTask` with the message deleted on invocation.** This is the naive
form of the chosen design and it is wrong in a way worth writing down: a Pipe deletes the source message
when the TARGET INVOCATION succeeds, and `RunTask` returns as soon as the task is ACCEPTED, not when it
finishes. That would acknowledge the message ~1 s in and lose every retry property for a ~16-minute job:
a task that dies at minute 12 would leave no message to redrive and no DLQ entry. **Therefore the task
itself is the consumer of record** -- the Pipe carries the message body as an override and the task
deletes it only after the artifact and manifest are durably written. That is what makes the visibility
timeout in 1.4 load-bearing rather than decorative.

### 1.3 Why 16 GB and not 8 GB, stated as a caveat rather than a preference

`CG-s-10` measured **6,752.0 MB** peak on a box with **8.0 GB free**, and **paging was not instrumented**.
Memory pressure is a NAMED, UNRESOLVED candidate for part of the 2.7x gap against the prior figures. An
8192 MB task would have 1.21x headroom over a number that may itself be depressed by the very pressure it
was measured under -- and `B2-AC6`'s cloud run is *the first measurement the sizing may rest on*. **Sizing
at 16384 removes memory pressure as a confound from that measurement.** It is deliberately generous for
one ~16-minute task per day, and it is a right-sizing candidate once AC6's number exists -- named here so
the next seat re-opens it on evidence instead of inheriting it as settled.

### 1.4 The visibility timeout is PROVISIONAL, and says so

`B2-AC1` asks for the number and its basis. The basis is incomplete **by construction**: the longest step
that holds the message is cold start + run, and **ECS cold start is UNMEASURED** -- the fit table's one
open cell, which `B2-AC6` closes. So: **2400 s**, derived as the measured worst full-fallback
(**1006.266 s**) plus the explicit 3600 s deadline's practical worst case bounded by observation, with
margin for a cold start assumed under ~120 s. ⛔ **This number is re-derived from AC6's measured cold
start and cloud duration before the exercise criteria close, and if the cloud run exceeds it the timeout
is raised and the change recorded.** A visibility timeout shorter than the run means a second worker picks
up the same stamp mid-build -- which the singleton scope decision in section 3 (S3) must also answer.

### 1.5 CE-G-5's fate, stated because silence is a surprise row

**CE-G-5 is LOCAL-ONLY and does NOT port.** Its layer (`_canonical.py` @`173dd335f4`: no orphaned rebuild,
serve-stale-immediately with the age on the line) exists to protect *a reader querying a local database
that may be mid-rebuild*. The cloud worker has no reader: it consumes a queue message, writes a new
versioned artifact under `projection/<vintage>/`, and serves nothing. **Its cloud equivalent is
artifact-first-pointer-last, which is `CG-s-3`'s contract, not this port's** -- a reader never sees a
half-written projection because it reads a pointer that is advanced only after the artifact is complete,
which is a stronger guarantee than serve-stale-with-an-age and is why the local layer is not re-implemented.
`_canonical.py` itself is **not carried to the cloud at all**; it is the local orchestrator and it retires
with `CG-s-8`. R9's KUZUSPLIT O-1 (serve-labeled-stale) survives as WORKER-INTERNAL in exactly one sense:
the worker never publishes a partial artifact, and on failure it publishes nothing rather than something
stale-but-labelled.

---

## 3. `B2-AC3` + `B2-AC4` -- THE FOUR FIXES, EACH WITH A CONTROL THAT WAS RUN

Landed @`117e539280`. Two of the four were demonstrated against the **pre-port blob** so the control
is shown to fail, not asserted to.

| fix | RED arm (pre-port `e445642c5f`) | GREEN arm (ported) |
|---|---|---|
| **S9** one key rule | `endpoint_resolves = False` | `= True` |
| **S3** singleton scope | `_lock_path_for` absent; ONE lock for every target | `lock(A) != lock(B)`, `lock(A)` stable |
| **S8** manifest edge_count | manifest 60,688 vs stored 58,432, **delta +2,256** | manifest 58,432 = stored 58,432, **delta 0** |
| **S2** flag semantics | enumerate 4 hits incl. the retired text | 2 hits / 363 lines, contradictory string **ABSENT** |

`node_count` agrees in BOTH S8 arms (27,133 / 27,135), so that control is specific to the field
that was wrong rather than a blanket pass.

### 3a. What the S9 fix did NOT do, stated because the opposite would be the easy claim

**`skipped_missing_endpoint` is 383 before the fix and 383 after it** (pre-port FULL-1/FULL-2, and the
ported run at 11:36-11:51Z on a later marker). **The fix recovered ZERO edges on today's data.** None of
the 383 skipped endpoints carries whitespace; they are genuinely absent from the head node set. S9 closes
a **LATENT** defect -- the control proves the two rules had diverged and now agree -- and it is honest to
say the card's specimen does not occur in the current warehouse. The count is carried here so `CG-s-3`
and any later reader inherit a measured number rather than an implication.

### 3b. S8 corroborated in the wild, by a caller this seat did not run

At 11:41:09Z `_canonical.ensure_fresh` rebuilt the canonical DB through some other caller on this box,
and the manifest it produced carries **`edge_count: 58432` -- the STORED count**, where every pre-fix
manifest carried the merge-attempt count. A rebuild this seat did not invoke, through a different entry
point, independently exercises the fix. (Node count 27,134 there vs 27,135 in my run: a different, later
marker, not a disagreement.)

### 3c. S8's second limb -- the guard question, DECIDED on control flow

The remediation row warned explicitly against asserting absence from a token census
(*"3.0.0_SA_CVO~A enumerated one token, not the file's control flow"*). Read as control flow:
the full loader **HAS** two enforced post-load guards -- the untyped-nodes check and the TSGRAPH fold
gate -- and **both gate the return code** at `:261` (`return 0 if (untyped == 0 and not gate_fail) else 1`).
What it does **NOT** have is the incremental engine's post-apply comparison of what landed against what
was read (`kuzu_incremental_refresh.py:227-232`), and `skipped_missing_endpoint` is **printed and never
enforced**. So: guards present, count-comparison ABSENT, both cited. Whether the loader should refuse on
`skipped > 0` is a real question this fix deliberately does not answer silently -- at 383 it would refuse
every current build.

### 3d. Caller safety, and a failing suite that is not mine

`comp-pydeps consumers` (denominator **323** python files): the loader has 3 consumers, the incremental 2,
including `tests/test_kuzu_incremental_refresh.py`. Suite re-run: **48 passed**. The 1 failure and 6 errors
are PRE-EXISTING -- `git status` shows this seat's `infra/` change set is exactly the two engine files plus
the new control; neither failing test file is in it; and `test_canonical_rebuild_liveness.py` has **0 hits**
for either engine file across 232 lines (its errors are `fixture 'td' not found`, and the other is a
graph-vintage denominator mismatch from the 09:11Z rebuild). Proven, not asserted.

## 2, 4, 5. THE PORT, THE EXERCISE, THE HANDOFF -- IN PROGRESS

Recorded here so the file is honest about its own state rather than reading as coverage:

- **s.2 the port** (B2-AC2) -- not yet built.
- **s.3 the four fixes** (B2-AC3 S9, B2-AC4 S2/S3/S8) -- not yet made. The `comp-blast` caller reads the
  face mandates BEFORE writing are in flight; the fixes must keep `_canonical.py` and `kuzu_cli.py`
  working until `CG-s-8` retires them.
- **s.4 the exercise** (B2-AC6) -- **BLOCKED, measured:** see s.6.
- **s.5 the handoff lines for CG-s-3** (B2-AC7) -- written with s.2.
- **the IAM limb of s.3 + the apply** (B2-AC5) -- **BLOCKED, measured:** see s.6.

## 6. WHAT IS BLOCKED, MEASURED RATHER THAN ASSUMED

| blocker | probe | result |
|---|---|---|
| the worker role does not exist | `aws iam get-role --role-name opal-globgrph-projection-worker` | `NoSuchEntity` -- the role is `CG-s-1`'s to create (TO-CG-B-1 at `0.7.0_AE_CloudOps~P`); this face ATTACHES statements to it and cannot create it |
| `CG-s-1`'s queue does not exist | `aws sqs list-queues --queue-name-prefix opal-globgrph` | only `opal-globgrph-incremental-events` and `-dlq` -- the **CloudTrail-fed item2b pair**, which R5 explicitly excludes ("not the CloudTrail queue, that is one writer of five"). S1's queue is absent |

Both are exactly where the GO put them: `B2-AC6` releases on `TO-CG-B-1`'s `B1-AC4`, and the queue ARN
reaches this seat through the issuer when `B1-AC3` lands. **Neither is idle waiting** -- the decision, the
fixes and the Terraform are the unblocked work and proceed now.

### 6-RELEASED. `CG-s-1` APPLIED at 11:33Z -- `B2-AC5`'s blocker is CLEARED

`TO-CG-B-1` is complete, CVO-certified (93540) and RAVC-accepted @`afd94db0ce`. The role and queue that
returned `NoSuchEntity`/absent when I probed them at 08:5xZ now exist on the APPLIED plane. `B2-AC6`'s
exercise remains gated on consuming a **REAL** marker stamp.

### 6c. LIVE-QUEUE FACTS the consumer must carry (93566), and the two that bite

1. **TWO message shapes arrive.** The S3 event envelope `{"Records":[...]}` **and** a one-off
   `{"Service":"Amazon S3","Event":"s3:TestEvent"}` with **no `Records` key**. A consumer that assumes
   `Records` crashes on it (`~P`'s first parser did). The worker tolerates both; a TestEvent is deleted,
   never DLQ'd.
2. **No `versionId`** -- bucket versioning is Andrew-locked OFF, so object identity is `eTag` + `sequencer`.
3. ⛔ **The DLQ baseline is 3, not 0**, self-inflicted by `~P`'s four receive-polls (every `ReceiveMessage`
   increments `ApproximateReceiveCount` even at `--visibility-timeout 0`; `maxReceiveCount` 3). **My DLQ
   reads are DELTAS on 3** until ~09:25Z 2026-09-04. And **I must not `receive-message` the main queue more
   than twice before the consumer runs, or I DLQ my own exercise message.**
4. **Main depth 0**: the 09:42:42Z stamp expired at retention 3600. The exercise consumes a real stamp;
   the marker is **never** hand-written (`probe_ifmatch_cas.py:81` FORBIDDEN_KEYS). Nightly derive 02:00Z
   guarantees one; daytime stamps came 09:24, 09:25, 09:42Z.
5. **Each real event carries `userIdentity.principalId`** -- that is the "no seat stamped it" control, and
   it is stronger than an invocation log because it rides the event's own face.

### 6d. ⛔ AN OPEN DESIGN POINT IN MY OWN `B2-AC1`, found while authoring the Terraform

`B2-AC1` states *"the TASK is the consumer of record"* so that a ~16-minute job dying at minute 12 stays
redrivable, and rejects the naive Pipe form for acking on `RunTask` acceptance. **But an EventBridge Pipe
with an SQS source acks when the TARGET INVOCATION succeeds, and `RunTask` returns on acceptance -- which
is the same defect I rejected, relocated into the design I chose.** Either the Pipe is the consumer (and
the retry property I claimed is not there) or the task is (and the Pipe is the wrong trigger).

Two facts now bear on it, both from the issuer: `~P`'s role grants the **worker** `sqs:ReceiveMessage`,
`DeleteMessage`, `GetQueueAttributes`, `ChangeMessageVisibility` -- an IAM shape for a worker that consumes
the queue **itself**; and *"a run longer than the timeout re-receives its own message and DLQs it on the
third attempt -- demonstrated live"*, which only bites if the consumer holds the message for the run. Both
point at task-as-consumer, and the issuer endorsing the **2400 s** visibility timeout derived from the V-1
duration only makes sense on that reading.

**RESOLUTION IS DEFERRED TO A MEASURED READ, NOT A RECALLED ONE.** I will not author Terraform on a
mechanism whose ack semantics I have not verified against the live service -- reasoning from what I
remember of Pipes is precisely the document-claim-over-measurement failure this project exists to correct.
The mechanism limb of `B2-AC1` is therefore OPEN; the runtime, CPU, memory, ephemeral, deadline and
timeout limbs are unaffected and stand.

> **CLOSED 2026-09-03 ~12:4xZ.** The measured read was taken (`aws pipes create-pipe
> --generate-cli-skeleton`: `SqsQueueParameters` = `BatchSize` + `MaximumBatchingWindowInSeconds`, nothing
> else; the stream sources in the same skeleton DO carry retry controls, which is the discriminating
> contrast). Filed as row `NFRA_CLDGRPH-S14` @`6c02972`; the issuer confirmed no face amendment is needed
> and narrowly retracted its 2400 s derivation (93623). **The limb is re-stated in s.1.2-RESTATED: the
> PIPE is the consumer of record, the timeout is derived from the Pipe's hold (declared 30 s, which the
> applied placeholder already satisfies), and the retry property is marker idempotency plus the nightly
> 02:00Z guarantee -- not SQS redrive.** `B2-AC1`'s proof row moves from OPEN to PASS **only** on that
> re-statement, and the declared hold is confirmed by measurement at `B2-AC6`.

### 6a. The wiring names, relayed 09:19Z (93433) -- **DESIRED, NOT APPLIED**

| | name |
|---|---|
| queue | `arn:aws:sqs:us-east-1:313476888478:opal-globgrph-projection-events` |
| DLQ | `arn:aws:sqs:us-east-1:313476888478:opal-globgrph-projection-events-dlq` |
| role | `arn:aws:iam::313476888478:role/opal-globgrph-projection-worker` (carries `CG-s-1`'s queue-consume statement only; the S3-read / `projection/*`-write / logs statements are THIS face's to attach per `B2-AC5`) |

⛔ **These are deterministic names read off `~P`'s `projection.tf` on the DESIRED plane. This port wires
against them and does NOT cite them as existing** -- my own probes above returned `NoSuchEntity` and an
absent queue, and a relayed name is not an applied resource. `B2-AC6` still releases on `~P`'s **OBSERVED**
queue message (`B1-AC4`), not on this relay.

### 6b. A hazard carried into `B2-AC5`'s apply, named before the plan rather than discovered at it

`~P`'s module-wide plan of `infra/aws/terraform/globgrph` surfaced **four foreign committed-never-applied
items** beside its own six resources: three Glue partition changes and an SNS email subscription to a human
address that is a **recorded Andrew EXCLUSION**. `~P` stopped and filed BLOCKING row `NFRA_CLDGRPH-S11`;
the issuer ruled `safe-apply -target` on exactly the owned addresses, verified by ONE **UNSCOPED** re-plan
asserted by address list.

**The same tree is this face's apply surface, so the same hazard is mine.** The plan of record for
`B2-AC5`: `-target` on exactly this port's own addresses; **verification by an UNSCOPED re-plan**, asserted
by address list -- my resources ABSENT from it, the four foreign ones still PRESENT. ⚠ This is deliberately
*not* a `-target` re-plan: CLAUDE.md Rule 22 records a `-target` apply verified by a `-target` re-plan as a
measured failure class, because a check scoped to the members cannot see a defect in what they share. The
unscoped read is the whole control.

⛔ **The exercise waits for REAL marker stamps.** `CG-s-10` measured a **1h58m** quiet window against R5's
45-stamps/24h sizing input; the nightly derive (`cron(0 2 * * ? *)` UTC) guarantees at least one per day.
If no stamp lands inside the working window the criteria are held OPEN with the window's bounds stated.
**A forced stamp is a bound violation and a surprise row, never a shortcut.**

## 7. SURPRISE ROWS FILED BY THIS SEAT UNDER THIS TASK ORDER

- **`NFRA_CLDGRPH-S10`** (OBSERVATION, ARMED, disarm_owner this seat) -- the engine's rebuild-deadline
  default is derived in-source from the ~6 min figure `CG-s-10` falsified, giving 1.80x headroom where the
  comment claims 5x. **Disarmed at this port by the explicit 3600 s in 1.1**, and re-checked against
  AC6's cloud duration. The engine-side correction is deliberately NOT taken here: this face names four
  fixes (S9, S2, S3, S8) and quietly widening that set is the scope drift round 2 forbids.
- **`NFRA_CLDGRPH-S12`** (OBSERVATION, ARMED, disarm_owner the issuer) -- **this face's BOUNDS and its own
  `<compiler_tools_mandate>` are not jointly satisfiable.** The bound says `kuzu_nessie_db` "is not read or
  written (mtime control as in TO-CG-V-1)"; the mandate requires `comp-blast` on both engine files;
  `comp-blast` reaches the canonical graph through `_canonical.ensure_fresh`, which found the DB BEHIND
  HEAD and **rebuilt it at 09:11:51Z** (82,661,376 B -> 46,997,504 B; listing md5 `711b0b3c..` ->
  `d64fca39..`). Obeying the mandate wrote the file the bound protects, **before a line of the port
  existed**. Classed OBSERVATION, not BLOCKING: nothing is stopped, the rebuild is the designed daily path
  and left the estate fresher, so per the face only BLOCKING rows are messaged and this one is not.
  ⚠ **TO-CG-V-1's control is NOT retroactively broken** -- that TO closed at 07:52Z and all four of its
  control reads precede this write by 80 minutes.
  ⭐ The rebuild's own banner independently CORROBORATES `CG-s-10`'s "daily path" finding from a different
  instrument: *"canonical FULL rebuild via the DESIGNED daily ground-truth reset (post-nightly whole-table
  delta trips the large-delta gate; CTO condition 2, NOT a defect)"*.

  **THIS PORT'S CONTROL THEREFORE RUNS FROM A RE-BASELINED READING, stated so the shift is visible rather
  than silent:** `infra/aws/globgrph/kuzu_nessie_db`, **46,997,504 B**, mtime
  **`2026-09-03 05:12:21.682472900 -0400`**, listing md5 **`d64fca39dfa47179f7798dcb1b8e2340`**. The port
  itself touches the canonical DB not at all, which is the narrow reading of the bound this seat proceeds
  on; the issuer decides which clause governs.

- **An id COLLISION on the shared channel, caught and self-corrected.** I appended as `S11` after reading a
  max of `S10`; `0.7.0_AE_CloudOps~P` appended their own `S11` (BLOCKING) in the same minute. **I renumbered
  MINE to `S12`** -- theirs is BLOCKING and routes to the issuer, mine is OBSERVATION, and the seat that
  detects a clash fixes its own row rather than another seat's. `~P`'s row is byte-untouched. Channel now:
  **12 rows, 12 distinct ids, 12 of 12 schema-valid.** Header denominator corrected **1 -> 12** across the
  two appends (it read "1 row" while the file held 9, on the issuer's instruction 93402).

- **The caller census the fixes must not break** (`comp-pydeps consumers`, denominator **323 python files**
  scanned across `.tools/` + `org/modules` + `infra/aws/globgrph` + `lib`): `kuzu_nessie_load.py` has **3**
  code consumers -- `_canonical.py` [INVOKE], `kuzu_ac_traversals.py` [INVOKE], `graph_status_cli.py`
  [INVOKE]; `kuzu_incremental_refresh.py` has **2** -- `_canonical.py` [INVOKE] and
  `infra/aws/globgrph/tests/test_kuzu_incremental_refresh.py` [IMPORT]. **That test file is the existing
  harness the S2/S3/S8 controls extend rather than duplicate**, and all five consumers must still work
  until `CG-s-8` retires them.
  ⚠ `comp-blast` itself returned **NOT-FOUND** for both engine paths against a 27,135-node graph and said
  so explicitly ("This is a NOT-FOUND, not a 'nothing breaks' clear"), routing to `comp-pydeps` -- so the
  caller set above comes from the instrument that models it, not from the one that was mandated.
