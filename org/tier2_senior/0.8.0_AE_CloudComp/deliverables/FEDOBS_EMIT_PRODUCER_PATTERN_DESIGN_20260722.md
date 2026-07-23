# fedobs_emit must follow the graph-producer pattern — design

**Author:** `0.8.0_AE_CloudComp` · **Date:** 2026-07-22 · **For:** Andrew (direct)

## Andrew-direct, VERBATIM (recorded same turn per `org/XXX.md`; NOT broadcast — his standing
## no-Tier-1-contact instruction is still in force, the CVO release was scoped to that handoff)

> "That should have the exact same pattern as all the other graph functions. Scheduled full write at
> night, incremental write function in cloud and local as needed."

## 1. The gap, grounded

Every other graph producer has both halves. The findings emitter has neither.

| producer | nightly full | cloud incremental | local incremental |
|---|---|---|---|
| `graph_nodes` / `graph_edges` | ECS `derive-runner`, `cron(0 2 * * ? *)` | Lambda `incremental-updater`, CloudTrail→SQS, 120s | `kuzu_incremental_refresh.py` (+ full fallback) |
| `cse` | `cse_producer.tf`, `cron(30 3 * * ? *)` | — | — |
| `comp_learns` | `comp_learns_producer.tf`, `cron(0 4 * * ? *)` | — | — |
| `fedobs_signals` (`fedobs_observe.py`) | `fedobs_producer.tf`, `cron(30 4 * * ? *)` | — | — |
| **`fedobs_obs_findings` (`fedobs_emit.py`)** | **NONE** | **NONE** | **NONE** |

**The two fedobs halves are independent, which I verified rather than assumed.** `fedobs_observe.py`
reads `CSE_TABLE = "iceberg.globgrph.cse"` (`:48`) and writes `fedobs_signals/observations/`. It never
reads the findings table. So the findings parquet is not stale *because* something upstream is stale —
**it is an orphaned producer with no trigger of any kind.**

Measured consequence — the whole federated findings table is frozen, written in two manual batches:

```
observer=LIVE-AWS     2026-07-14T10:17:51Z     <- emitted from the 8-day-stale local derive
observer=GRAPHS-D8    2026-07-07T12:32:21Z
observer=DEBTSCAN     2026-07-07T12:32:09Z
observer=COMPDRIFT    2026-07-07T12:31:54Z
observer=PIPESCRIPT   2026-07-07T12:32:30Z
```

Trino federates this in place (`fedobs_glue.tf`) alongside `iceberg.globgrph.graph_nodes`. So a
correlation joining findings against a graph refreshed 17h ago is joining it against findings frozen
for **15 days**, and nothing in the join says so.

## 2. What the pattern maps to

**A — NIGHTLY FULL EMIT (the direct analogue, and the piece that closes the freeze).**
An ECS Fargate task running `fedobs_emit.py --observers <all>` on a cron, slotted AFTER the observers
it reads. Ordering matters and the chain already declares it: 02:00 derive → 03:00 stitch → 03:30 cse
→ 04:00 comp_learns → 04:30 fedobs_signals. The findings emit belongs at **05:00Z**, after every
observer it adapts has refreshed. Task role `fedobs_emitter_task` ALREADY EXISTS (`fedobs.tf:37`) with
the AC2 Deny-on-truth policy — it was built for exactly this and is currently only borrowed by the
signals producer. **The infra is 90% present; what is missing is a rule and a task-def.**

**B — CLOUD INCREMENTAL. This is where the analogy stops being mechanical, and I am not going to
pretend otherwise.**
`graph_nodes`' incremental works because AWS emits a CloudTrail event when the *observed thing*
changes. **There is no equivalent event for "an observer produced a new finding."** The five adapters
read heterogeneous surfaces (D8 ledger JSON, debtscan ledgers, compdrift rows, pipescript output,
the live-AWS derive JSON) that change on their own schedules and mostly are not S3 objects.

Three candidate triggers, none of which I am picking unilaterally:
1. **S3 event per observer artifact** — clean for the observers whose output lands in S3; useless for
   the repo-resident ones.
2. **Chain off each producer's completion** — the derive/cse/comp_learns tasks already run on a
   schedule; each could emit a completion event the findings emitter subscribes to. Closest to the
   existing pattern and reuses the EventBridge fabric already there.
3. **Per-observer partition re-emit on demand** — `fedobs_emit --observers live_aws` already supports
   exactly this. It is the *local* incremental in all but name.

**The honest statement: the nightly full is a straightforward port; the incremental needs a trigger
that does not exist yet, and inventing one silently would be the worse error.** Note also that a
findings emit is CHEAP and the whole table is small (7.8 KB for LIVE-AWS) — so unlike `graph_nodes`,
where a 55K-row reload cost 356s and the incremental existed to avoid it, **the incremental here buys
freshness, not time.** That changes which trigger is worth building.

**C — LOCAL INCREMENTAL.** Already exists in substance: `fedobs_emit.py --observers <one>` re-emits a
single partition. What it lacks is the vintage discipline the rest of the estate now has — it should
refuse to publish a partition whose source observation is older than a TTL, exactly as
`comp-iam refresh-census`/`live` now do, rather than silently republishing a stale finding.

## 3. What the existing design already gets right, and must not be lost

`fedobs_emit` carries `vintage` = *"when the observer saw it (honest-vintage: a stale finding is not
correlated as current)"*, and `adapt_live_aws` uses the derive file's mtime. So the 2026-07-14
LIVE-AWS partition is stamped with its true observation time — **the staleness travels with the data
instead of being laundered.** Scheduling must not replace that with a write-time stamp; that would be
the same container-clock-vs-data-clock error the graph freshness header just had.

## 4. Sequencing / gates — what I have NOT done

- **No Terraform written and nothing applied.** A new EventBridge rule + task-def is an infra apply;
  applies are CTO-gated (`safe-apply`, HALTGT) and the fabric is under Andrew's restart hold.
- The B-trigger decision is an architecture call and is listed above as options, not a choice.
- **NOT verified:** who reads `fedobs_obs_findings` today besides `comp-fedobs`, and whether any live
  consumer is currently reasoning off the frozen table. That determines whether this is a freshness
  improvement or an active-correctness issue, and it is the first thing I would check next.

---

## AMENDMENT 2026-07-23 — code_heat is the SECOND INSTANCE of this pattern gap

CVO~Z SYSPARITY tick-4 (025720Z) surfaced comp-learns-status computing over a 144.3h-stale
code_heat binding. Grounded 0.8.0 (0259Z): the producer (infra/aws/globgrph/code_heat_emit.py,
DEV-BOX-RESIDENT by TO-2 ruling) has **NO scheduler anywhere** — no EventBridge rule, no
task-def, no local cron (a 07-08 rail-log override searched for exactly that and found none).
Last hand-run landed 2026-07-16T03:40:45Z (s3api, explicit Z). NEVER-SCHEDULED, not stalled.

**So Andrew's ruled pattern ("Scheduled full write at night, incremental write function in cloud
and local as needed", @79c42337e verbatim) now has TWO instances waiting on the same
architecture decision:**

| Producer | Last write | Consumer harmed |
|---|---|---|
| fedobs_emit (4 observers) | 07-07 (LIVE-AWS limb 07-14) | ad-hoc Trino correlation queries (no scheduled reader — consumer question CLOSED @45f5814d1) |
| code_heat_emit | 07-16T03:40:45Z | comp-learns-status DEMAND/GAP/COST views (build-next decisions) + the GRAPHFEED code_heat_snap sibling |

One decision covers both; the nightly-full trigger choice (the 3 options in this doc) should be
made once and instantiated per-producer. code_heat's dev-box residency (git-history-shaped)
constrains its option set: the nightly full write must run WHERE the git history lives, which
makes the "local scheduled task + cloud incremental" split the natural fit for it specifically.
Heal-on-read (the item-6 danger-map mechanism) is NOT the right shape here — a refresh needs the
dev box, so a cloud/commit-path consumer cannot self-heal it.
