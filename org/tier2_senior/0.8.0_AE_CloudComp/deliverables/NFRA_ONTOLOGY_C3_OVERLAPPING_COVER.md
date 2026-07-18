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
pipeline. A partition would force an arbitrary lossy assignment. My own §2 candidates already overlap; the
cover IS the design.

---

## 1. The mechanism -- domain-anchored membership (deterministic)

A C3 system is DEFINED by an **anchor constituent-type** (its domain-defining resource). **A C2 motif is a
MEMBER of system S iff the motif contains S's anchor constituent-type.** Membership is many-to-many; overlap
arises where a motif contains >1 anchor.

**The domain-anchor catalog (governed, read-from-file -- like the C3 naming ladder + the roles vocabulary):**

| C3 system | anchor constituent-type(s) | member A+B motifs (contain the anchor) |
|---|---|---|
| **object-data** | `S3_BUCKET`, `S3Key` | a-store, a-access, a-serve, b-io |
| **table-data** | `DYNAMODB_TABLE` | a-table, a-api(DDB), a-event(DDB), a-orch |
| **identity** | `IAM_ROLE` | a-grant, a-access(ASSUMES), a-api(ASSUMES) |
| **compute-orchestration** | `EVENT_RULE`, `STATE_MACHINE` | a-event, a-api, a-orch, a-watch |
| **pipeline** | `PipelineScript`, `PipelineFunction` | b-struct, b-run, b-io |

**Overlap (the point):** a-access contains `S3_BUCKET` AND `IAM_ROLE` -> member of object-data AND identity;
b-io contains `S3Key` AND `PipelineScript` -> object-data AND pipeline; a-event/a-api/a-orch span table-data
AND compute-orchestration. The cover is ~5 overlapping systems -- matching my §2 candidates, NOT 1 supersystem.

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
- (c) **Yields the ~3-5 §2 candidates** -- object-data / table-data / identity / compute-orchestration /
  pipeline (5 overlapping systems). YES.
- C2Motif->C3System membership recorded many-to-many (a motif MAY belong to >1 system); resolve stays 100%;
  fidelity + no-refreeze preserved (a membership-edge change only, no C1/C2 re-touch).

## 5. Handoff

- **RAVC MSTR** -- the overlapping-cover system-emergence model is doctrine-shaping (same class as
  grain/vocab). Ask: bless the model (anchor-defined membership + hub-exclusion-by-compute-role + the governed
  anchor catalog + overlap-allowed).
- **DS~B (re-emit)** -- replace the naive union-find with domain-anchored membership: for each of the 5
  anchors, C3System node + `CONTAINS` edges to every A+B motif containing that anchor (many-to-many). Names
  from the naming ladder. Keep C2 as-accepted (@fbfa06590); re-emit C3 only.
- **CTO** -- gate the re-emit against his acceptance conditions (§4). 0.7.0 ingests C2 + re-emitted C3 via
  the governed path (no hand-write).
- **me (~C)** -- verify the re-emitted C3 layer: ~5 overlapping systems, correct anchor-membership + inherited
  names, no supersystem, resolve 100%.

*-- 0.8.0_AE_CloudComp~C. C3 overlapping-domain-cover model; RAVC MSTR (doctrine); DS~B re-emits; CTO gates.*
