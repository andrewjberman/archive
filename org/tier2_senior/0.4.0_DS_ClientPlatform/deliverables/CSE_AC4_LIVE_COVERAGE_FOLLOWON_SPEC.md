# CSE AC4 live-coverage fast-follow: the concrete coverage-sweep spec (DS~B design; governed landing)

**Author (cse_schema.py owner):** `0.4.0_DS_ClientPlatform~B`. **Trigger:** CVO finding on the OWNS re-sign --
`assert_live_coverage` is `ok=FALSE --live` (6 node + 1 edge live types unmapped vs the 11-day-stale embedded
snapshot). **CTO ruling:** FAST-FOLLOW, NOT ride-this-land (folding it into OWNS would conflate concerns) --
a SEPARATE governed change. **For:** CTO arch-gate -> CVO re-sign -> COO/exec single-editor land (org/modules/
graph EXEC-locked). **Grounded @`0da695451`**; live sets @HEAD nodes_snap 1276252256517924052.

**NOT a SCHEMA_VERSION bump:** this adds MAPPINGS + an exclusion set + refreshes the ground-truth snapshot. It
touches NO closed enum (Entity/Relationship unchanged) -- so it is a coverage-COMPLETENESS fix at 0.5, governed
(SoD-locked file) but not an algebra version-bump. **I own the DESIGN, not the landing.**

---

## 0. Grounding (LAW-1) -- the exact gap, live-exercised @`0da695451`

`assert_live_coverage(live_nodes=58, live_edges=53)` -> **ok=FALSE**:
- unmapped node_types (6): `C2Motif, C3System, CODEBUILD_PROJECT, LAMBDA_LAYER, SCHEDULE, SSM_DOCUMENT`
- unmapped edge_types (1): `USES_LAYER`

Two classes: (a) `C2Motif/C3System` are SEMCTL META-nodes (the compression-layer C2/C3 nodes materialized by
this session's AB-MAT -- NOT estate resources; they are ABOUT the estate); (b) the rest are REAL estate
resources/edges that need a mapping. **A silent None on the meta-nodes is NOT "intentionally excluded"** -- the
exclusion must be EXPLICIT (CVO's + my point).

---

## 1. Part 1 -- EXPLICIT semctl-meta exclusion (not silent-None)

**Add (cse_schema.py, near the maps):**
```python
# SEMCTL META-node types: the C2/C3 COMPRESSION-LAYER nodes (motifs/systems materialized by the semctl
# layer, e.g. AB-MAT 2026-07-18) -- they describe the estate, they are NOT estate resources, so they carry
# NO algebra Entity BY DESIGN (an Entity is an estate noun). EXPLICITLY excluded from the coverage requirement
# -- a named exclusion, never a silent None (the honest form: "counted as intentionally-excluded", not "missing").
SEMCTL_META_NODE_TYPES: frozenset = frozenset({"C2Motif", "C3System"})
```

**Wire it into the two coverage checks** so meta-nodes do NOT count as unmapped:
```python
# assert_live_coverage (:~528) and coverage_sweep (:~512):
#   BEFORE: un_n = sorted(t for t in ln if t not in CLOUDNODE_TYPE_TO_ENTITY)
#   AFTER:
un_n = sorted(t for t in ln if t not in CLOUDNODE_TYPE_TO_ENTITY and t not in SEMCTL_META_NODE_TYPES)
```
(Both call sites -- coverage_sweep's `observed_node_types` diff + assert_live_coverage's `ln` diff.)

---

## 2. Part 2 -- MAP the 4 real estate types + the 1 edge

**CLOUDNODE_TYPE_TO_ENTITY (:251) -- add 4 (reuse EXISTING Entities; no enum change):**
```python
    "SCHEDULE": Entity.SCHEDULE,          # a schedule IS a Schedule (Entity.SCHEDULE exists; EVENT_RULE also
    #                                       maps here -- SCHEDULE the node_type was simply never added).
    "CODEBUILD_PROJECT": Entity.SERVICE,  # a CI/build service (same class as ECS_*/API_GW/STATE_MACHINE -> SERVICE).
    "LAMBDA_LAYER": Entity.MODULE,        # a reusable, versioned code/dependency package functions USES_LAYER
    #                                       (= a shared code MODULE; precedent PipelineScript/Module -> MODULE).
    "SSM_DOCUMENT": Entity.ARTIFACT,      # a stored automation/command/runbook DOCUMENT (a held/produced unit,
    #                                       like MS_FILE -> ARTIFACT). It is a definition, not a running service.
```
**CTO-RULED @224227Z (taxonomy, CTO's lane -- both my primary proposals confirmed):**
- `LAMBDA_LAYER` -> **Entity.MODULE** (RULED): a reusable shared-code/dep package functions DEPEND ON (the
  `USES_LAYER->REQUIRES` edge reinforces "a function REQUIRES the module"). MODULE over ARTIFACT -- the semantic
  role is "a reusable dependency"; ARTIFACT would flatten it to a deployable-zip and lose the dependency semantics.
- `SSM_DOCUMENT` -> **Entity.ARTIFACT** (RULED): a stored, DECLARATIVE automation/runbook DEFINITION (like
  MS_FILE / a CloudFormation template). NOT FUNCTION -- the document doesn't DO work; it's a stored spec the SSM
  SERVICE executes (document = definition, SSM = executor). ARTIFACT is the stored definitional unit.
- `SCHEDULE`->SCHEDULE (identity), `CODEBUILD_PROJECT`->SERVICE (managed build service), `USES_LAYER`->REQUIRES
  (the USES_* dependency family) -- unambiguous, approved.

**CLOUDEDGE_TO_RELATIONSHIP (:289) -- add 1:**
```python
    "USES_LAYER": Relationship.REQUIRES,  # a function REQUIRES its layer -- the USES_* dependency family
    #                                       (USES_OAC/USES_OAI/USES_SG all -> REQUIRES).
```

---

## 3. Part 3 -- REFRESH the stale ground-truth snapshot (58 / 53)

The embedded `LIVE_NODE_TYPES_20260707` (54) / `LIVE_EDGE_TYPES_20260707` are 11 days stale. Refresh to the
LIVE set @HEAD (58 node / 53 edge, pulled @`0da695451`) and RE-DATE the constants (keep the old name as an
alias or replace the references in `assert_live_coverage`/`_self_test`):
- `LIVE_NODE_TYPES_20260718` = the 58 live types (adds C2Motif, C3System, CODEBUILD_PROJECT, LAMBDA_LAYER,
  SCHEDULE, SSM_DOCUMENT vs the 54; note MS_GROUP/MS_DRIVE_ONEDRIVE stay MAPPED but are not live -- over-coverage
  is fine, the snapshot is the LIVE set).
- `LIVE_EDGE_TYPES_20260718` = the 53 live types (adds USES_LAYER + reconciles any drift).
- Update the self-test's `LIVE_NODE_TYPES_20260707` references (checks 9/10) to the new constants.

**Post-fix, `assert_live_coverage --live` -> ok=TRUE** (meta-nodes excluded; the 4 types + USES_LAYER mapped;
snapshot current). CVO exercises this live at re-sign.

---

## 3b. THE DURABLE FIX -- `--live-cadence` wiring is a CO-REQUIREMENT (CTO arch note @224227Z)

Refreshing the FROZEN snapshot to today is a **POINT fix** -- a re-frozen snapshot RE-DRIFTS in ~11 days, the
IDENTICAL root cause. So the durability half is **not optional:** `assert_live_coverage --live` must be wired
into the derive/CI path **on a cadence**, so a NEW live node/edge type is a **TRACKED GAP AT APPEARANCE**, never
another silent 11-day drift. (Session doctrine, 4th instance: *check LIVE at run-time, never a frozen reference*
-- same class as the materialize denominator, the OWNS census-guard, and the emit-vs-ingest applied re-verify.)

**LANE SPLIT:** my snapshot-refresh (Part 3) unfreezes the CURRENT drift = **my lane (this spec)**. The
`--live-cadence` derive/CI wiring = **0.7.0/AE lane** (CTO-routed via COO), co-sequenced. **Both land, or the fix
is temporary.** This spec's Part 3 is a necessary-not-sufficient half; it must NOT land alone as if it closed the
class. The cadence's cadence + exact CI hook are the 0.7.0/AE design; my Part-3 refresh is what it re-baselines against.

---

## 4. Self-test additions (gate the fix)

```python
check("AC4: SEMCTL meta-nodes explicitly EXCLUDED (not silent-None)",
      "C2Motif" in SEMCTL_META_NODE_TYPES and "C3System" in SEMCTL_META_NODE_TYPES)
check("AC4: the 4 estate types now map to an Entity",
      all(t in CLOUDNODE_TYPE_TO_ENTITY for t in
          ("SCHEDULE", "CODEBUILD_PROJECT", "LAMBDA_LAYER", "SSM_DOCUMENT")))
check("AC4: USES_LAYER maps to REQUIRES",
      CLOUDEDGE_TO_RELATIONSHIP.get("USES_LAYER") is Relationship.REQUIRES)
check("AC4: live coverage GREEN with meta excluded + new mappings + refreshed snapshot",
      assert_live_coverage()[0] is True)   # against the refreshed embedded snapshot
```
(The 58/53 numbers in checks 9/10 update to match the refreshed snapshot.)

---

## 5. Landing (governed -- same cycle as OWNS, NOT a version bump)

1. **DS~B (me):** this concrete spec = the DESIGN.
2. **CTO:** arch-gate **CLOSED / GO @224227Z** -- 2 Entity calls RULED (MODULE / ARTIFACT), Part 1 + Part 3
   approved, `--live-cadence` made a CO-REQUIREMENT (Sec 3b).
3. **CVO:** re-sign -- exercise `assert_live_coverage --live` -> ok=TRUE + the self-test additions on the live graph.
4. **COO/exec:** single-editor land the cse_schema.py change (Parts 1-3 + Sec 4). No co-migration seam (a
   coverage/mapping completeness change, not a shared-resolver semantics change) -- but CVO confirms nothing
   consumed the meta-nodes as estate Entities. **CO-SEQUENCE with the 0.7.0/AE `--live-cadence` derive/CI wiring
   (Sec 3b, CTO-routed via COO): both land, or the fix is temporary.**
5. **~C:** (optional) confirm the semctl-meta exclusion is consistent with the ontology's node-type view.

*-- 0.4.0_DS_ClientPlatform~B, cse_schema.py owner. AC4 live-coverage fast-follow; governed landing.*
