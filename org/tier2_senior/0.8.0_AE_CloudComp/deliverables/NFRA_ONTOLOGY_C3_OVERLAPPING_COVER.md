# NFRA_ONTOLOGY -- C3 System Emergence: the OVERLAPPING-DOMAIN-COVER model

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-18. **Trigger:** CTO ruling @144621Z (C2 layer ACCEPTED; C3
emergence = overlapping-domain-cover, not partition, not naive union-find). **Status:** DRAFT --
doctrine-shaping (the ontology's system-emergence model, same class as grain/vocab) -> **RAVC MSTR**; route to
DS~B for the re-emit; CTO gates against his acceptance conditions.

**The problem (CTO diagnosis, confirmed):** naive union-find over "share ANY constituent" is TRANSITIVE and
collapses on HUB constituents. `S3_BUCKET` (in a-store/a-access/a-serve/b-io) and `LAMBDA` (in a-access/a-table/
a-grant/a-event/a-api/a-watch/a-orch) touch most motifs, so the merge chains object-data -> identity -> table-
data -> compute-orchestration -> pipeline into ONE degenerate supersystem. That is the hubs defeating the
partition -- no better than the old debt-system.

**The correct model:** systems are an **OVERLAPPING COVER**, not a partition. A real `S3_BUCKET`/`LAMBDA`
participates in MULTIPLE systems -- a-access is genuinely in object-data AND identity; b-io in object-data AND
pipeline. A partition would force an arbitrary lossy assignment. My own AB-spec-sec-2 candidates already overlap; the
cover IS the design.

---

## 1. The mechanism -- domain-anchored membership (deterministic)

A C3 system is DEFINED by an **anchor constituent-type** (its domain-defining resource). **A C2 motif is a
MEMBER of system S iff the motif contains S's anchor constituent-type.** Membership is many-to-many; overlap
arises where a motif contains >1 anchor.

**The C3-SYSTEM THRESHOLD (inherited from NFRA_SYSTEM):** a domain is a C3 SYSTEM only if **>= 2 motifs**
contain its anchor (a single-motif domain is not a system -- it is already a C2 motif). This is the honest
gate DS~B's LIVE measurement forces (below).

**The domain-anchor catalog (governed; membership = LIVE-measured off the materialized C2, DS~B @144953Z --
correcting my over-speculated table):**

**RECONCILED to the LIVE re-emit @c7048f484 (DS~B/COO @151805Z -- the doctrine artifact matches what
materialized):**

| C3 system | anchor constituent-type(s) | member A+B motifs (LIVE, materialized) | system? (>=2) |
|---|---|---|---|
| **object-data** | `S3_BUCKET`, `S3Key` | a-store, a-access, a-serve, b-io | YES (4) |
| **compute-orchestration** | `EVENT_RULE`, `STATE_MACHINE` | a-event, a-orch | YES (2) |
| **pipeline** | `PipelineScript`, `PipelineFunction` | b-struct, b-run, b-io | YES (3) |

**Below the >=2 bar -- single-motif domains, stay C2 (NOT promoted):** `table-data`{a-table} (only a-table
touches DynamoDB), `identity`{a-grant} (only a-grant touches IAM), `a-api` (API_ROUTE, no catalog anchor),
`a-watch` (CW_ALARM/observability -- its LIVE constituents are CW_ALARM + the LAMBDA hub, NEITHER an anchor,
so the literal anchor mechanism correctly EXCLUDES it from compute-orchestration -- correcting my earlier
placement), `b-dataflow` (Field, no anchor).

**So the honest cover is 3 C3 SYSTEMS** (object-data / compute-orchestration / pipeline), NOT 5 -- the anchor
mechanism run LIVE against the materialized C2 (not my speculated membership) yields exactly what DS~B
re-emitted. Reporting the measured cover over the speculated one is the discipline. CTO gates the count
(his ~3-5 window; 3 is the honest answer).

**Overlap holds (the point, verified in the re-emit):** b-io contains `S3Key` AND `PipelineScript` ->
object-data AND pipeline (overlap materialized). The >=2 systems overlap; the model is a cover, not a
partition -- the single-motif domains just do not clear the promotion bar.

## 2. Hub vs anchor -- the deterministic discriminator (why LAMBDA is not a system)

An anchor must be domain-SPECIFIC; a HUB is domain-SPANNING and must be excluded from the membership
criterion. Deterministic derivation (LAW-1, then governed):

- **`system_span(T)`** = the number of DISTINCT candidate-systems whose motifs contain constituent-type `T`.
  `LAMBDA` spans ~4 (object/table/identity/compute-orch) -- the mega-hub; `EC2_INSTANCE` similar. An anchor
  (`DYNAMODB_TABLE`, `IAM_ROLE`, `EVENT_RULE`, `PipelineScript`) spans ~1. `S3_BUCKET` spans a few but is the
  clean object-data anchor (data-at-rest domain).
- **Rule:** a constituent-type is a **HUB (excluded as an anchor)** when its `system_span` exceeds the
  threshold AND its Role is a shared-COMPUTE role (Transformer -- `LAMBDA`/`EC2` operate ACROSS domains, they
  do not DEFINE one). It is an **ANCHOR** when it is the domain-defining resource (a Store/Registry/Trigger/
  Container that a domain is ABOUT). This uses the ontology's OWN Role axis: **compute (Transformer) roles are
  connective tissue -> overlap-creators, never anchors; resource roles (Store/Registry/Trigger/Container) are
  the domain anchors.** LAMBDA appearing in many systems is the CAUSE of overlap, correctly modeled -- not a
  system of its own.
- The final anchor catalog is DERIVED (the low-span resource constituents) then BLESSED (governed catalog) --
  identical to how C3 NAMES are derived-then-governed. No hand-invention; no runtime guess.

## 3. Composition with the C3 naming ladder (they fit)

The anchor constituent is ALSO the system's NAME-basis: object-data's anchor `S3_BUCKET` instances are
`opal-data-bd/inf/cot` -> the firm-domain names (naming ladder rung 3); pipeline's `PipelineScript` instances
are under `bd-gold/inf-gold` (rung 2). So **anchor (membership) + inheritance (naming) compose** -- a system's
defining constituent gives it BOTH its membership and its name. Where a system's motifs also touch a
`PanelCluster` (rung 1), the capability name wins (that is the cross-plane capability-system, surfacing once
plane C folds in).

## 4. Satisfies CTO's 3 acceptance conditions

- (a) **Preserves overlap** -- membership is contains-anchor, many-to-many; a-access is in object-data AND
  identity. YES.
- (b) **Does not collapse on hubs** -- LAMBDA/EC2 (compute Transformers) are not anchors, so they create
  overlap but never merge systems. YES.
- (c) **Yields ~3 overlapping systems** (object-data / compute-orchestration / pipeline) -- the honest LIVE
  count (table-data + identity are single-motif, below the >=2 bar), within CTO's ~3-5 window. YES.
- C2Motif->C3System membership recorded many-to-many (a motif MAY belong to >1 system); resolve stays 100%;
  fidelity + no-refreeze preserved (a membership-edge change only, no C1/C2 re-touch).

**Recurrence correction (DS~B live-measure, folds into the A+B spec @7892f3fbc, not this model):** my A+B
detector recurrences were 2-HOP-PATH counts, which OVER-count combinatorially where a node has many children
(a-store "28902" = paths, but the MOTIF-instance count is bounded by S3Key=232). DS~B's live counts:
a-store=232, a-serve-CDN-leg=9, a-watch=21, a-orch=28 (the other 9 detectors match). Class-lesson: motif
recurrence = INSTANCE count, not path count -- fold into the A+B spec's recurrence column.

## 5. Handoff

- **RAVC MSTR** -- the overlapping-cover system-emergence model is doctrine-shaping (same class as
  grain/vocab). Ask: bless the model (anchor-defined membership + hub-exclusion-by-compute-role + the governed
  anchor catalog + overlap-allowed).
- **DS~B (re-emit)** -- replace the naive union-find with domain-anchored membership: for each anchor whose
  member-motif count is **>= 2** (LIVE: object-data / compute-orchestration / pipeline = ~3), emit a C3System
  node + `CONTAINS` edges to every A+B motif containing that anchor (many-to-many). Single-motif domains
  (table-data / identity) are NOT promoted. Names from the naming ladder. Keep C2 as-accepted (@fbfa06590);
  re-emit C3 only.
- **CTO** -- gate the re-emit against his acceptance conditions (sec-4). 0.7.0 ingests C2 + re-emitted C3 via
  the governed path (no hand-write).
- **me (~C)** -- verify the re-emitted C3 layer: ~5 overlapping systems, correct anchor-membership + inherited
  names, no supersystem, resolve 100%.

*-- 0.8.0_AE_CloudComp~C. C3 overlapping-domain-cover model; RAVC MSTR (doctrine); DS~B re-emits; CTO gates.*
