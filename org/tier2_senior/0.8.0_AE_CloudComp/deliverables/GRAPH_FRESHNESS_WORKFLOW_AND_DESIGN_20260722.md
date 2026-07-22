# Graph freshness: the actual workflow, and a design that follows it

**Author:** `0.8.0_AE_CloudComp` · **Date:** 2026-07-22 · **For:** Andrew (direct)
**Ask:** *"analyze the workflow here and identify how each of these is tied to what tool or function
schedule (e.g. nessie trigger, comp-aws, comp-kuzu full or inc, etc). We should design it based off
the contemplated workflow."*

Companion to `GRAPH_FRESHNESS_HEADER_PROVENANCE_20260722.md` (the four-clock finding).

---

## 1. The workflow, grounded

### WRITE path into nessie/iceberg `graph_nodes` — TWO producers, two cadences

| | Producer | Trigger | Cadence | Writes | Evidence |
|---|---|---|---|---|---|
| **A** | ECS Fargate `derive-runner` (full re-derive) | EventBridge `opal-globgrph-derive-runner-nightly` | `cron(0 2 * * ? *)` — **02:00 UTC daily** | ALL nodes, one shared `snapshot_ts` | `item2a.tf:435-445`; observed `snapshot_ts` = `2026-07-22T02:00:31Z` on 14,708 nodes |
| **B** | Lambda `opal-globgrph-incremental-updater` | CloudTrail **mutating** mgmt events → EventBridge `cloudtrail_mgmt` (`readOnly=false` minus noise) → SQS → ESM | **event-driven**, ~2-min debounce (`maximum_batching_window_in_seconds = 120`, `batch_size = 100`) | only changed nodes, each with its own `snapshot_ts` | `item2b.tf:13-27, 70-91, 175-190` |

### READ / materialize path

| | Tool | Trigger | Produces |
|---|---|---|---|
| **C** | `comp-kuzu` / `kuzu_nessie_load.py` | auto-refresh on nessie HEAD-advance (CLAUDE.md Rule 20) | local `kuzu_nessie_db`; this is the `built:` clock |

### Downstream nightly consumers of A's snapshot

`03:00Z` stitch-produce (comment: *"after the 02:00Z derive_runner_nightly snapshot"*) → `03:30Z` cse
→ `04:00Z` comp_learns → `04:30Z` fedobs.

### NOT part of the pipeline — and I had this wrong

`.fedobs_tmp/live_aws/comp_aws_derive_*.json` is **untracked local scratch**, last written
2026-07-14 by a hand-run of `comp-aws derive`. It is not a nightly product. The nightly derive-runner
writes to **nessie** (`NESSIE_URI` env on the task), not to that directory. My `comp-iam live` reads
that file, so it is currently keyed to somebody's eight-day-old local run rather than to the pipeline.

---

## 2. What the topology implies about freshness

**Freshness is a property of the ROW, not the table, because the write path is a UNION of two
cadences.** That single fact resolves the whole confusion:

> A node whose `snapshot_ts` is 02:00Z is **not stale** — it is **CURRENT**, provided path B is alive.
> It has not been re-observed because it has not CHANGED; if it had, CloudTrail would have driven an
> incremental write within ~2 minutes.

So the honest freshness claim for the graph is:

> **"Current as of the 02:00Z full derive, PLUS every CloudTrail-observed mutation since."**

That is a *strong* guarantee — considerably stronger than "17 hours old" — and the current header
states neither it nor its failure mode.

**AND THE GUARANTEE IS ENTIRELY CONDITIONAL ON PATH B BEING ALIVE.** If the incremental updater is
dead, coverage silently degrades to "up to 24h stale" while every visible signal looks unchanged.

## 3. The load-bearing gap: path B's liveness is unmeasurable from its output

The incremental cohort is **2 nodes**. That number is ambiguous between:

- **quiescent** — the estate genuinely changed twice today; the pipe is healthy; or
- **dead** — the pipe stopped and the estate has been changing unobserved.

**Node count cannot distinguish these, and node count is the only thing currently surfaced.** This is
the same shape as the day's other findings: *absence of a signal is being read as absence of the
thing*, when it is equally consistent with absence of the observer.

It is also why the current header is not merely imprecise but **anti-correlated**: the fewer nodes the
incremental writes, the closer its cohort timestamp sits to "now" per node, while the *coverage* it
provides shrinks. A dying incremental updater that writes one node a day looks maximally fresh.

## 4. Design

### D1 — Report per-COHORT vintage, never a single table-write number
```
graph_nodes:
  full-derive   14,708 nodes  observed 2026-07-22T02:00:31Z  (age 17.1h, cadence 24h)  [OK]
  incremental        2 nodes  newest   2026-07-22T14:37:22Z  (age  4.5h)               [see D3]
  => effective: current as of 02:00Z + CloudTrail mutations since
```
The existing `last-write 4.5h (< 6h cadence)` line may stay as a table fact, but it must not be the
cadence verdict.

### D2 — Evaluate the cadence check against the cohort it names
The full-derive cohort's SLA is 24h (its actual cron). Judge it against 24h and `snapshot_ts`. As
written, `< 6h cadence` on table-write **cannot fail while any incremental write is landing** — a
check that cannot report the condition it is named for.

### D3 — Assert path B's liveness from the PIPE, not from its output
Node counts conflate quiet with dead. Liveness must come from signals that exist even when nothing
changed:
- Lambda `Invocations` / `Errors` on `opal-globgrph-incremental-updater`
- SQS `NumberOfMessagesReceived` / `ApproximateAgeOfOldestMessage` on `globgrph_incremental_events`
- DLQ depth on `globgrph_incremental_dlq` (non-zero = events arriving and failing — the mode that
  looks exactly like quiescence from the node side)

Verdict shape: `incremental: HEALTHY (N invocations/24h, DLQ 0)` vs
`incremental: UNVERIFIED (no invocations in 24h — quiescent estate or dead pipe, INDISTINGUISHABLE)`.
The second is an honest UNKNOWN and must not render as OK.

### D4 — Use the nightly as the reconciliation oracle for path B
Path A re-observes everything at 02:00Z. So the 02:00 run can *measure* what path B missed: nodes
whose full-derive state differs from what incremental last wrote are exactly path B's misses. That
comparison is free (both sides already exist) and is the only self-checking signal available. Nobody
computes it today.

### D5 — `comp-iam live` reads kuzu, keyed on `snapshot_ts`
Drop the `.fedobs_tmp` JSON as the population source (it is local scratch, not pipeline output). Read
the population from kuzu — which materializes nessie and therefore carries BOTH cadences — and report
per-node observation time. The vintage gate stays; it just keys on the right clock.

### D6 — State the residual denominator honestly
kuzu carries 193 `IAM_ROLE`; live AWS has 205. The 12 absent are all `AWSServiceRoleFor*`
(AWS-managed, service-linked) — plausibly outside the `cloudtrail_mgmt` service filter and not
created by us. Whether that is a deliberate exclusion or an ingest gap is **NOT DETERMINED**, and
until it is, the live-plane denominator is "governable roles", not "all roles".

## 5. Not claimed

- Whether the 02:00Z run **succeeded** today. The rows prove a write occurred; they do not prove a
  complete or correct run. No run-status check was read.
- Why the incremental cohort is 2 (D3 is the proposal to make that answerable, not an answer).
- The correct `comp-aws derive` invocation — `--classes iam` is rejected (`unrecognized arguments`).
- Whether the `cloudtrail_mgmt` service filter covers every graph-relevant service (the rule lists
  `aws.events`, `aws.sns`, `aws.sqs`, `aws.secretsmanager`, … — the full list was not enumerated
  against the node types the graph carries).
