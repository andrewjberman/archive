# comp-debris extension past Lambda -- design (research, decommission lane)

**Author:** 0.8.0_AE_CloudComp · **Date:** 2026-07-17 · **Thread:** Andrew-direct decommission research (thread 1 of 3; comp-iam expansion + resource_heat_snap queued)
**Status:** RESEARCH / DESIGN. No tool built, no resource touched. Extends `comp_debris.py` (author 1.0.0_SA_CTO~Z) from Lambda-only to the AWS-resource plane. Building lands at `org/modules/graph/` (ANY_EXEC lane) -> a build lane / CTO, separately staffed.
**Source:** `DECOMMISSION_TOOLING_ASSESSMENT_20260717.md` @890e66375 (rec #1, highest-leverage) · **Steer:** Andrew 2026-07-17 ("all of those but start with the lambda for comp-debris").

---

## 0. TL;DR -- the finding that shapes the extension

The band architecture (`HOT / COLD-DORMANT / TOO-YOUNG / STILLBORN-OR-GUARD / UNKNOWN`) and the three
binding refinements are **resource-type-AGNOSTIC and reusable verbatim.** The extension is NOT a rewrite --
it is a set of per-type **activity adapters**, each returning `(last_activity_day, created_day, read_ok,
signal_basis)`, feeding the EXISTING `classify()`. What changes is the SIGNAL, never the band logic.

Two grounded findings drive the design:
1. **CloudTrail is NOT a universal "last-used" source** (Andrew named it; the ground truth is narrower).
   The org trail captures **management events universally** (a "last-configured" touch for every resource)
   but **data events only for S3 reads on `opal-data-bd` + `opal-data-inf`** (2 of 38 buckets) plus served
   writes. So per-type USAGE must come from **CloudWatch service metrics**, with CloudTrail management events
   as the universal cross-confirm and data events only where enabled.
2. **S3 coldness is TWO-DIMENSIONAL** (write vs read). Read-activity is BLIND on 36/38 buckets; but
   **write-coldness is FREE and always-on** via the daily `BucketSizeBytes` / `NumberOfObjects` storage-metric
   delta -- and **write-cold IS the supersession tell** (an old bucket stops being written when its successor
   takes over). So the monolith-cutover detection this whole lane exists for is achievable on S3 with a
   free, always-on signal -- no data-event enablement needed.

---

## 1. Grounding (live, this session -- 2026-07-17)

- **Trails** (`describe-trails`):
  - `opal-organization-trail` (multi-region): management events = **ALL** (read+write); data events =
    `AWS::S3::Object` **ReadOnly** on `arn:aws:s3:::opal-data-bd/` + `arn:aws:s3:::opal-data-inf/` ONLY.
  - `opal-served-key-write-trail` (advanced selector `served-firm-header-writes-only`): S3 **writes**
    (readOnly=false) on `opal-data-{inf,bd,cot}/platinum/firm/` served prefixes.
  - => NO Lambda-invoke / DynamoDB-item / EC2 / EventBridge data events anywhere; management events universal.
  - Full management-event history lives in `s3://opal-cloudtrail-logs-313476888478` (Athena-queryable past
    the ~90d console horizon) -- the source for a "last-mgmt-touch" older than 90d.
- **S3 request metrics** (`list-bucket-metrics-configurations` on inf/assets/bd): **NONE configured.**
  Only always-on **Storage metrics** exist (`list-metrics AWS/S3`): `NumberOfObjects`, `BucketSizeBytes`
  (daily). No `GetRequests`/`PutRequests` usage metric on any sampled bucket.
- **Existing `comp_debris.py`** (Lambda-only): `classify()` + `BANDS` + `_HELD_RX` + `build_ledger`; reap
  rank = `COLD-DORMANT` only (dormancy AFTER activity); the 3 refinements are the self-test mutants.
- **`dup_scan.py`** already carries a DynamoDB `ConsumedReadCapacityUnits` metric-window path
  (`metric_reads_sum` / `windowed_dead_verdict`) -- reuse it for the DDB adapter.

---

## 2. The signal-adapter table (per resource type -- the whole design in one table)

| Type | USAGE signal (last-used) | Creation ts | Availability | Notes |
|---|---|---|---|---|
| `LAMBDA` | CW `AWS/Lambda Invocations` | `LastModified` | default-on | v1 (existing) -- unchanged |
| `DYNAMODB_TABLE` | CW `ConsumedRead`+`WriteCapacityUnits` | `describe_table.CreationDateTime` | default-on | mirror Lambda; reuse dup_scan metric path |
| `EC2_INSTANCE` | CW `CPUUtilization` + `NetworkIn` (idle = both ~0) | `describe_instances.LaunchTime` | default-on (5-min basic) | **idle != stopped** -- a running-idle box IS the cost |
| `EVENT_RULE` | CW `AWS/Events Invocations`/`TriggeredRules` per `RuleName` | CloudTrail `PutRule` / graph `snapshot_ts` | default-on | never-triggered = cold wiring |
| `S3_BUCKET` (write) | daily `BucketSizeBytes`/`NumberOfObjects` delta (flat = no writes) | `list_buckets.CreationDate` | **always-on, FREE** | write-cold = the supersession tell |
| `S3_BUCKET` (read) | CloudTrail data events (bd+inf only) / server logs | -- | **absent on 36/38** | read-UNKNOWN -> BLIND band, never "cold" |
| (universal cross-confirm) | CloudTrail **management** events (last-configured) | -- | universal (Athena on trail bucket) | "last operator touch", NOT usage |

---

## 3. Architecture -- one `classify()`, N adapters (minimal change)

- **Unchanged (the invariants live here):** `classify()`, `BANDS`, `_HELD_RX`, `build_ledger`, `_render`.
  Rename the one field `last_invoked_day` -> `last_activity_day` (behavior identical) so it reads
  type-agnostically.
- **New:** `activity_adapter(resource) -> {read, last_activity_day, created_day, signal_basis}` per type
  (`debris_lambda` [existing logic], `debris_ddb`, `debris_ec2`, `debris_events`, `debris_s3`). Each adapter
  owns ONLY its signal; the band verdict stays central.
- **CLI:** `comp-debris [--types lambda,s3,ddb,ec2,events] [--days N] [--hot-days N]` (default: all types),
  one unified ledger, per-row `signal_basis`. `--self-test` gains one band-mutant per new type.

---

## 4. The honesty rules the extension MUST carry (the anti-false-outage spine)

The extension multiplies the surface where a blind read looks like a corpse. Five controls, each a
generalization of an existing refinement -- these are the reason to build it carefully, not fast:

1. **PER-DIMENSION UNKNOWN** (refinement 2, generalized): S3 read-activity is BLIND on 36 buckets. The row
   NEVER collapses to "cold" -- it carries `signal_basis` + a `READ-UNKNOWN` flag. A bucket write-cold but
   read-unknown is NOT a standalone reap candidate.
2. **SIGNAL BASIS PRINTED PER ROW** (the print-the-denominator discipline, Rule 22 / memory verify-law 6+10):
   every row states what signal its band rests on (`cw-invocations` / `cw-capacity` / `cw-cpu+net` /
   `storage-delta` / `cloudtrail-data` / `mgmt-only`). A human must never mistake a management-event touch
   for usage. This is the single most important addition -- the heterogeneous signal is the honesty.
3. **NEVER-ACTIVE != COLD, per type** (refinement 1): the TOO-YOUNG vs STILLBORN-OR-GUARD split needs a
   creation ts for EVERY type -- grounded: each has one (`LaunchTime`/`CreationDateTime`/`CreationDate`/
   `LastModified`). No type ships without it.
4. **HOLD-AWARE** (refinement 3): `_HELD_RX` on name, across all types (unchanged).
5. **T-1 / TRADING-CALENDAR (NEVER#1 -- the biggest new false-outage risk):** a data bucket write-cold over
   a weekend + market holiday is the CORRECT T-1 state, NOT cold. The window + hot-days MUST count TRADING
   days (via `lib/trading_calendar.py`) for pipeline buckets -- else a Monday sweep false-alarms every data
   bucket, which is exactly the mdpf/OPAL_ASSETS false-outage class. This is non-negotiable for the S3/data
   extension; the Lambda v1 never touched data buckets so it dodged this -- the extension cannot.
6. **CADENCE-AWARE WINDOWING for scheduled resources (DISCOVERED by the prototype live run 2026-07-17):** a
   scheduled `EVENT_RULE`/`SCHEDULE` must be judged HOT/COLD against its OWN cadence (`ScheduleExpression`
   rate/cron), NEVER a flat window -- else every monthly/weekly rule false-alarms as COLD-DORMANT. Live proof:
   `fred-ingestion-monthly-late` flagged cold at 23d is a MONTHLY rule = HEALTHY; `bd-49f-fees-runner-daily`
   at 21d is a DAILY runner = a REAL finding. The cadence is the discriminator. This is control #5 (the
   trading-calendar) generalized to the schedule axis -- the STILLBORN-OR-GUARD refinement, one level up, on
   time. The adapter reads the schedule expression and computes "cold" as "missed >= K cadence-periods."

---

## 5. Cost / rate (the sweep must stay cheap)

- **`GetMetricData` batches up to 500 metric queries per call** -> ONE batched call per type, not
  `get_metric_statistics` per resource. ~549 prime resources -> a handful of calls total.
- S3 storage-delta: 2 datapoints/bucket (window start/end); 38 buckets in one batched `GetMetricData`.
- CloudTrail management-event history via Athena runs ONLY on the STILLBORN-OR-GUARD tail (cross-confirm the
  "old + never-invoked" rows), never the flood -- same "expensive leg on the cold tail only" discipline as
  dup_scan's `graph_dead_confirm`.

---

## 6. How the three threads compose (this feeds the other two)

- **-> resource_heat_snap (thread 3):** each adapter's `(last_activity_day, signal_basis)` snapshotted
  daily (reuse `snap_store.py`) makes "went cold the week its twin went hot" a first-class Trino delta query.
- **-> comp-similar `supersede` (CTO ruling 5: heat = BOTH data-cold AND invoke-cold, confidence-graded):**
  S3 write-cold (storage-delta) = the data-cold axis; the CW metric signals = the invoke-cold axis. This
  extension IS the heat source the supersede join consumes. both-cold = HIGH; one-cold = MEDIUM-surfaced.
- **-> comp-iam expansion (thread 2):** the access-plane "last-used" (RoleLastUsed / Access Advisor) is the
  same coldness idea on the identity plane -- a fourth adapter class, one plane over.

---

## 7. Boundaries

- **ADVISORY, never deletes** (unchanged). Confirmation pass (comp-heat / comp-dups / comp-deadgrant /
  comp-trigger / comp-similar) stays SEPARATE, on the cold tail -- not machinery inside comp-debris.
- **Read-only:** `list_functions` / `list_buckets` / `describe_table` / `describe_instances` / `list_rules`
  + `GetMetricData` + (cold-tail only) Athena on the trail bucket. **No data-event enablement** (costly;
  out of scope -- the design uses the signals that already exist).
- **Lane:** the build lands under `org/modules/graph/` (ANY_EXEC = CTO/COO/CVO) -> a build lane / CTO. This
  doc is the design of record; building is separately staffed (same split as comp-similar -> ~D).

## 8. Open questions for the gate
- EC2 idle threshold: what CPUUtilization + NetworkIn floor over what window = "idle" (a runner between
  scheduled jobs is idle-but-not-dead)? Needs a purpose-review band like STILLBORN-OR-GUARD, not a reap.
- S3 read-blindness: RESOLVED (Andrew-direct 2026-07-17) -- accept UNKNOWN-read for now; do NOT enable
  CloudTrail S3 data events on `opal-data-assets`. Write-cold via the free storage-delta is the supersession
  signal; read-coldness deferred (write-cold + read-unknown stays advisory, never a standalone reap).
- Trading-calendar scope: which buckets are "pipeline/T-1" (calendar-counted) vs ops buckets (wall-clock ok)?
  Likely reuse the same held/pipeline classification the freshness frontier uses.
