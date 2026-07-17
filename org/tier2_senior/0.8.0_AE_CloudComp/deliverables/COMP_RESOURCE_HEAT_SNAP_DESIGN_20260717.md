# resource_heat_snap -- design (decommission research, thread 3/3)

**Author:** 0.8.0_AE_CloudComp · **Date:** 2026-07-17 · **Thread:** Andrew-direct decommission research (thread 3 of 3; comp-debris ext @f921f9e97, comp-iam-usage @bf4c846d5 delivered)
**Status:** RESEARCH / DESIGN. Adds a new SURFACE to the EXISTING `snap_store.py` framework (my TO-7 module). New Iceberg table = CTO plan-gate (NEW-TERRITORY, like `resource_summaries`); ships WITHOUT a freshness-twin (alert-suspension). Producer lands in `infra/aws/globgrph/` (AE-owned).
**Source:** `DECOMMISSION_TOOLING_ASSESSMENT_20260717.md` Part B @890e66375 · **Steer:** Andrew 2026-07-17 ("all three").

---

## 0. TL;DR -- the whole thing is COMPOSITION; the heavy parts already exist

The estate has heat for **code** (git) and **documents** (MS) and **Lambda invocation** (comp-debris), but
NOT for the **AWS-resource plane** (S3/DDB/EC2/EventBridge) -- exactly the monolith-cutover surface. This
thread closes that gap **without new machinery**, because both halves already exist:

- **The SIGNAL** is thread-1's `comp_debris_ext` adapters: they already emit, per ARN-bearing resource, a
  `(last_activity_day, band, signal_basis)` row against live AWS. That IS resource heat.
- **The WRITER** is `snap_store.py` (my TO-7 module): a `{surface}_snap` is just a SURFACES registry entry
  (4 standard cols + payload) fed by a producer that stages JSONL; the append/retry/heartbeat/delta-query
  shape is done.

So `resource_heat_snap` = **a new SURFACES entry + comp_debris_ext wired as its daily producer.** The
day-over-day delta ("this bucket went cold the week its successor went hot") becomes a first-class Trino
query -- and it is precisely the **heat-divergence axis comp-similar's `supersede` join consumes**
(CTO ruling 5: heat = BOTH data-cold AND invoke-cold, confidence-graded). **This is the thread that closes
the decommission loop.**

---

## 1. Grounding (this session)

- **`snap_store.py`** (`infra/aws/globgrph/`, author me @TO-7): SURFACES registry, each surface = 4 STANDARD
  columns (`snapshot_date` [identity partition], `computed_at`, `producer_ref`, `marker_head`) + payload.
  Stage-then-ingest (dev-box stages JSONL under `warehouse/snap_ingest/pending/{surface}/`; in-VPC sweep
  validates -> one-Nessie-commit append -> R1 twin heartbeat -> `done/`). Existing surfaces: `ms_heat_snap`,
  `code_heat_snap`, `fedobs_coverage_snap`, `fedobs_coevolution_snap`. **Adding a surface = one registry entry.**
- **`comp_debris_ext`** (thread 1, @f921f9e97): per-type adapters already produce `(arn/name, node_type, band,
  last_activity_day, dormant_days, signal_basis)` against live AWS -- validated on 254 resources.

---

## 2. The surface definition

```
resource_heat_snap payload (+ the 4 standard cols):
  arn               string  required   -- the natural key (node_id == arn for cloud resources)
  node_type         string  required   -- S3_BUCKET / DYNAMODB_TABLE / EC2_INSTANCE / EVENT_RULE / LAMBDA
  band              string  required   -- HOT / COLD-DORMANT / TOO-YOUNG / STILLBORN-OR-GUARD / UNKNOWN
  last_activity_day string  optional   -- ISO date of last activity (null if never/blind)
  dormant_days      long    optional   -- days since last activity (null unless COLD-DORMANT)
  signal_basis      string  required   -- cw-capacity / storage-delta / cw-cpu+net / cw-events / cw-invocations
```
`signal_basis` in the row is the honesty carry: a delta query can filter to the resources whose band rests
on a TRUSTED signal, and never confuse a management-event touch for usage.

## 3. The producer (daily) + the delta story
- **Producer:** `comp_debris_ext --emit-snap` -> one JSONL row per ARN-bearing resource staged under
  `pending/resource_heat_snap/{ts}.jsonl`; the in-VPC `snap_store --ingest-pending --surface resource_heat_snap`
  sweep appends it. Daily cadence (scheduled), mirroring code_heat/ms_heat.
- **The delta query (the payoff):**
  ```sql
  -- "went cold when its twin went hot": a resource whose band flipped HOT -> COLD-DORMANT,
  -- co-timed with a summary-similar resource going the other way (comp-similar supersede input).
  SELECT arn, node_type, min(snapshot_date) FILTER (WHERE band='COLD-DORMANT') AS went_cold
  FROM globgrph.resource_heat_snap
  GROUP BY arn, node_type
  HAVING bool_or(band='HOT') AND bool_or(band='COLD-DORMANT')   -- transitioned within the series
  ```
  Joined to comp-similar's summary-similar pairs, the cold member + its hot twin = the superseded pair.

## 4. Composition -- this closes the loop
```
  comp_debris_ext (thread 1)          -> the per-resource heat SIGNAL (last_activity, band, signal_basis)
  resource_heat_snap (thread 3)       -> the daily DELTA ("went cold when its twin went hot")
  comp-similar supersede (~D's build) -> the JOIN: name-cluster x summary-sim x HEAT-DIVERGENCE
                                          (ruling 5: BOTH data-cold AND invoke-cold, confidence-graded)
  comp-iam-usage (thread 2)           -> the access-plane corroboration (role went cold with the resource)
```
The three research threads + comp-similar are ONE superseded-twin detector. resource_heat_snap is the
heat-divergence axis; without a day-over-day series, "divergence" is unmeasurable (a single reading gives
coldness, never the transition). **This is why the snap sibling, not a point-in-time scan.**

## 5. Gated / boundaries
- **New Iceberg table `globgrph.resource_heat_snap` = CTO plan-gate** (NEW-TERRITORY pure-add, same class as
  `resource_summaries`). `snap_store --ensure` creates it; do NOT run until CTO reads the DDL.
- **NO freshness-twin** (alert-suspension directive, relayed 0.7.0 2026-07-17): the R1 twin heartbeat is
  WRITTEN (the key exists) but the freshness-alarm registry twin is DEFERRED until the consolidation phase
  ends -- a per-producer alarm mid-migration is exactly what Andrew suspended. (snap_store writes the
  heartbeat key regardless; the ALARM subscription is what's deferred.)
- **Lane:** the surface-registry entry + producer land in `infra/aws/globgrph/` (AE-owned, LD-0218) -- I can
  land these; the table --ensure + the Trino/Nessie side coordinate with 0.7.0 + CTO's plan-gate.
- **Advisory:** the delta feeds the identification column (comp-similar supersede -> OPAL_LCLRPO), never a
  disposal path.

## 6. Recommendation
Ship resource_heat_snap as the third surface after comp-debris-ext lands as the producer (thread 1 build) and
comp-similar's supersede mode exists to consume it (~D's Phase 2). Sequencing: thread-1 build -> this surface
-> the supersede join. Until then, `comp_debris_ext` gives the point-in-time signal; the snap sibling adds the
time axis that makes "divergence" measurable.
