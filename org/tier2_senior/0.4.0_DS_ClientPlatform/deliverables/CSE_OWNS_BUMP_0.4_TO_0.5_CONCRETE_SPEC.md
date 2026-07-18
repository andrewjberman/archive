# CSE Schema-Bump 0.4 -> 0.5: the concrete OWNS spec (DS~B design; governed landing)

**Author (cse_schema.py owner):** `0.4.0_DS_ClientPlatform~B`. **For:** CTO arch-gate -> CVO re-sign -> COO/exec
single-editor land (org/modules/graph EXEC-locked; same governed cycle as 0.3 TYPE/SYMBOL, 0.4 PROMOTE).
**Authorization:** CTO greenlight @213523Z (both gates lifted: A+B materialization APPLIED-closed; binding-
completeness ratified LD-0311 @086238604, incl. my AXIS-2 reconciliation @d16e269bf). **Requirement half:**
~C's `NFRA_ONTOLOGY_OWNS_BUMP_REQUIREMENT.md` @fdd4a5e00 (R1-R4). **Grounded @`1db09432c`**; live OWNED_BY
distribution @HEAD nodes_snap 1276252256517924052.

**I own the DESIGN, not the landing.** This spec is precise enough to land near-verbatim after the arch-gate.

---

## 0. Grounding (LAW-1) -- the OWNED_BY polysemy, live-measured

`OWNED_BY` = 5,845 edges (the #2 relationship). Object-type distribution @HEAD (comp-kuzu, exact, no residual):

| OWNED_BY object type | count | sense | maps to |
|---|---|---|---|
| `MS_USER` | 5,613 | CUSTODY (an actor holds the artifact) | **OWNS** (new) |
| `S3_BUCKET` | 232 | CONTAINMENT-INVERSE (the bucket contains the key) | **CONTAINS** (existing, no new primitive) |

Exactly two object types; the split is clean and target-typed. Custody is the dominant + primary sense (96%).

---

## 1. R1 -- add the governed `Relationship.OWNS` primitive

**Change (cse_schema.py, class Relationship, the ABSTRACT block):** add after `SUPERSEDES` (`:102`) -- OWNS is
the abstract custody relation (my AXIS-2 ruling: agnostic tier, ratified LD-0311 D6), so it belongs with the
abstract relationships, NOT the code/infra block.

```python
    SUPERSEDES = "supersedes"
    OWNS = "owns"                      # 0.5: the governed CUSTODY/stewardship relation -- "A holds / is-
    #                                    responsible-for B" (an actor OWNS a resource). The C-1 custody sense
    #                                    of OWNED_BY, split out of the NARROWED governs (D3/D6, LD-0311). NOT
    #                                    governance (policy/authority stays GOVERNS); NOT containment (the
    #                                    S3Key sense is CONTAINS). Abstract tier (agnostic).
```

**Validator: NO change needed.** `_REL_VALUES = frozenset(r.value for r in Relationship)` (`:182`) is
enum-derived, so `"owns"` auto-joins the accepted set (identical to how PROMOTE auto-extended `_PRODUCER_VALUES`
at 0.3->0.4). `validate()` S3.2 (`:382`) accepts it with no edit.

---

## 2. R2 + R3 -- re-map OWNED_BY OUT of GOVERNS, target-typed

**R2 -- change the flat default (cse_schema.py `:306`):**
```python
    # BEFORE: "OWNED_BY": Relationship.GOVERNS, "HAS_POLICY": Relationship.GOVERNS,
    # AFTER:
    "OWNED_BY": Relationship.OWNS, "HAS_POLICY": Relationship.GOVERNS,
```
The flat default is now OWNS (custody, the dominant 5,613 sense). `HAS_POLICY` stays GOVERNS (governance is now
NARROW -- policy/authority only, per the D3 govern!=guards split @d16e269bf). This frees custody from GOVERNS.

**R3 -- add the target-typed resolver + the container set (cse_schema.py, beside `map_cloudnode` `:345`):**
```python
# Live-grounded (OWNED_BY object distribution @HEAD): the two OWNED_BY object classes. Extensible via the same
# governed bump if a new object type appears (a coverage-gap, caught by the census in Sec 4a, reconciled, not guessed).
_OWNED_BY_CONTAINER_TYPES: frozenset = frozenset({"S3_BUCKET"})   # containment-inverse -> CONTAINS
_OWNED_BY_ACTOR_TYPES: frozenset = frozenset({"MS_USER"})          # custody -> OWNS


def map_cloudedge(edge_type: str, dst_node_type: str = "") -> "Relationship":
    """AC3 (edge): resolve a CloudEdge to its algebra Relationship. TARGET-TYPED for the polysemous OWNED_BY
    (0.5, R3): object is a CONTAINER (S3_BUCKET) -> CONTAINS (containment-inverse, the fine->coarse rollup;
    NO new primitive); else (object is an actor, e.g. MS_USER) -> OWNS (custody). All other edges resolve by
    the flat CLOUDEDGE_TO_RELATIONSHIP map. Returns None on a coverage gap (caller fail-closes).
    THE SANCTIONED EDGE RESOLVER -- a direct CLOUDEDGE_TO_RELATIONSHIP.get('OWNED_BY') returns only the custody
    DEFAULT (it lacks the object type); container disambiguation REQUIRES this function (see Sec 5 co-migration)."""
    if edge_type == "OWNED_BY":
        if dst_node_type in _OWNED_BY_CONTAINER_TYPES:
            return Relationship.CONTAINS   # containment-inverse: the OBJECT (bucket) is the container
        return Relationship.OWNS           # custody (default; actor object -- MS_USER, 5613/5845)
    return CLOUDEDGE_TO_RELATIONSHIP.get(edge_type)
```

**Direction note (containment-inverse):** `S3Key OWNED_BY S3_BUCKET` -> CONTAINS means the OBJECT (bucket) is the
CONTAINER and the SUBJECT (key) is the contained -- i.e. canonical `CONTAINS` reads `S3_BUCKET -> S3Key`, the
INVERSE of the OWNED_BY src/dst. Direction lives in the CSE transformation edges (subject/object), not the
Relationship type; a consumer materializing canonical containment swaps src/dst for this sense. This matches
`comp_coverage_check.py:523`'s existing fine->coarse (contained->container) rollup read of OWNED_BY.

---

## 3. R4 -- OWNERSHIP Qualifier and OWNS edge COEXIST (no change; document)

`Qualifier.OWNERSHIP` (`:143`) STAYS. The `OWNS` Relationship is added ALONGSIDE it. They are orthogonal axes:
`OWNERSHIP` = a per-node metadata attribute ("under what ownership was this node/change"); `OWNS` = a node->node
relation ("A owns B"). A node CAN carry an OWNERSHIP qualifier AND be the object of an OWNS edge. Exact in-schema
precedent: `Qualifier.AUTHORITY` (`:140`) + `Relationship.AUTHORIZES` (`:117`) already coexist -- same
word-family, two axes. `OWNS : OWNERSHIP :: AUTHORIZES : AUTHORITY`. **Do NOT collapse them.** No code change.

---

## 4. Version bump + migration

**SCHEMA_VERSION (`:42`): `"0.4"` -> `"0.5"`.** Append to the version-comment block:
```python
# 0.4->0.5 (CTO-arch-gated + CVO-re-signed 2026-07-18, LD-0311 downstream): +Relationship.OWNS (the governed
# CUSTODY primitive) + OWNED_BY target-typed disambiguation (custody->OWNS / containment-inverse->CONTAINS via
# map_cloudedge); freed by the D3 narrow-governs split (@d16e269bf). Additive enum-extend (back-compat: the
# validator auto-accepts via _REL_VALUES); the OWNED_BY re-map is a CSE-log materializer migration.
```

**Migration obligations (per MIGRATION_NOTE `:49` -- a re-map = version-bump + a CSE-log materializer migration):**
- **CSE-log materializer migration:** existing OWNED_BY-custody CSEs that recorded `GOVERNS` re-map to `OWNS`.
  The ontology rule bank @967f23fe1 already anticipates this (`relations.owns.binds_up:[OWNED_BY]` re-points
  GOVERNS->OWNS on land) -- coordinate the re-derive so the rule-bank re-point + this bump land in one window.
- **Coverage-sweep: UNAFFECTED.** `OWNED_BY` was already in `CLOUDEDGE_TO_RELATIONSHIP` and stays; no new
  edge_type is introduced (the change is the mapped-TO value + a resolver). `coverage_sweep`/`assert_live_coverage`
  (membership checks) do not trip. No COMPUNIFY new-edge sweep needed (contrast an enum-ADD of a new edge type).

---

## 4a. Forward denominator-guard (CTO arch-gate condition @215258Z; folds the semctl denominator discipline)

The two-case disambiguation is EXHAUSTIVE **today** (OWNED_BY objects = exactly {MS_USER, S3_BUCKET} @HEAD). The
risk is FORWARD: a NEW OWNED_BY object type -- especially a new CONTAINER -- would `map_cloudedge`-DEFAULT to OWNS
(custody), silently mis-classifying it. Same class as the materialize denominator + the auto-classifier: make it
VISIBLE, never silently defaulted. Add a batch census (mirrors `coverage_sweep`'s pattern):

```python
def owned_by_object_census(owned_by_object_types) -> tuple:
    """Forward denominator-guard (semctl contract): given the LIVE OWNED_BY object node_types (one re-derive),
    return (ok, unknown_object_types). An object type in neither _OWNED_BY_ACTOR_TYPES nor
    _OWNED_BY_CONTAINER_TYPES currently DEFAULTS to OWNS via map_cloudedge -- which is WRONG for a new CONTAINER.
    Surface it for a governed whitelist-bump (add to the container set, or affirm custody), NEVER silently
    default. Print the distribution on each re-derive so a new object type is seen, not absorbed."""
    known = _OWNED_BY_ACTOR_TYPES | _OWNED_BY_CONTAINER_TYPES
    unknown = sorted(set(owned_by_object_types) - known)
    return (not unknown, unknown)
```

The re-derive / CSE-emit path calls this once per pass on the live OWNED_BY object set, prints
`OWNED_BY objects: {type: count}`, and a non-empty `unknown` is a tracked coverage-gap (a governed bump), never a
silent OWNS-default. **Additive; does not touch R1-R4.** CTO flagged it non-blocking for this land -- folded here
so the guard lands WITH the resolver it guards (map_cloudedge is new this bump); ride-this-land vs fast-follow is
CTO/COO's call. This is an ADDITIVE amendment post the gated @66a30da7c -- R1-R4 UNCHANGED (only Sec 4a + 2
self-test checks added), so it does not re-open the arch-gate.

---

## 5. **CO-MIGRATION REQUIRED (the seam this bump opens) -- BINDING ON THE LAND (CTO @215258Z: atomic set, one window)**

`map_cloudedge` is the new sanctioned resolver, but a live consumer still resolves OWNED_BY by DIRECT `.get()`:

- **`infra/aws/globgrph/cse_emit_graphhead.py:102`** -- `rel = cs.CLOUDEDGE_TO_RELATIONSHIP.get(edge_type)`.
  After this bump it returns OWNS for every OWNED_BY (correct for the 5,613 custody edges) but **MISSES the
  container disambiguation** -- the 232 `S3Key OWNED_BY S3_BUCKET` edges would emit as OWNS, not CONTAINS.
  **REQUIRED:** migrate this call site to `cs.map_cloudedge(edge_type, dst_node_type)` (it has the CloudEdge,
  so it has the dst node_type). This is an infra/globgrph change = **AE/0.7.0 lane**, co-sequenced with the land.
- My own verification tools (`NFRA_CSE_P2_ac4_fullgraph_parity.py:203`, `NFRA_CSE_P2_coverage_sweep.py:150`)
  also `.get()` directly -- lower stakes (coverage/parity, not emission), but I update them to `map_cloudedge`
  in the same window for consistency (my deliverables lane, self-committed).
- The staged draft copy `deliverables/NFRA_CSE_P1_cse_schema.py` is a PRE-canonical staging artifact (superseded
  by org/modules/graph/cse_schema.py); it does NOT land -- flag for deletion or a no-land marker (housekeeping).

**Pre-land check for CTO/COO:** a fresh estate sweep (`comp-grep "CLOUDEDGE_TO_RELATIONSHIP" `) for any OTHER
direct-`.get('OWNED_BY')` resolver expecting GOVERNS. My @1db09432c sweep found the above; re-run at land-time.

---

## 6. Self-test additions (gate the bump -- the exercised control)

Add to `_self_test` (mirroring the collision-safe / negative-control discipline already in the module):
```python
# OWNS bump (0.5)
check("OWNS on-enum (validator auto-accepts)", "owns" in _REL_VALUES)
check("R2: OWNED_BY flat default re-mapped OUT of GOVERNS onto OWNS",
      CLOUDEDGE_TO_RELATIONSHIP["OWNED_BY"] is Relationship.OWNS)
check("R2: HAS_POLICY stays GOVERNS (governance stays narrow, not swept into OWNS)",
      CLOUDEDGE_TO_RELATIONSHIP["HAS_POLICY"] is Relationship.GOVERNS)
check("R3: OWNED_BY -> MS_USER (actor) resolves OWNS (custody)",
      map_cloudedge("OWNED_BY", "MS_USER") is Relationship.OWNS)
check("R3: OWNED_BY -> S3_BUCKET (container) resolves CONTAINS (containment-inverse, no new primitive)",
      map_cloudedge("OWNED_BY", "S3_BUCKET") is Relationship.CONTAINS)
check("R3: OWNED_BY with no object type falls back to the custody DEFAULT (OWNS)",
      map_cloudedge("OWNED_BY", "") is Relationship.OWNS)
check("R3: a non-polysemous edge still resolves by the flat map",
      map_cloudedge("HAS_POLICY", "") is Relationship.GOVERNS)
check("R4: OWNERSHIP Qualifier + OWNS Relationship COEXIST (AUTHORITY:AUTHORIZES precedent)",
      "ownership" in _QUAL_VALUES and "owns" in _REL_VALUES
      and "authority" in _QUAL_VALUES and "authorizes" in _REL_VALUES)
# forward denominator-guard (Sec 4a)
check("4a: census FLAGS an unknown OWNED_BY object type (not silently defaulted to OWNS)",
      owned_by_object_census({"MS_USER", "S3_BUCKET", "SOME_NEW_CONTAINER"}) == (False, ["SOME_NEW_CONTAINER"]))
check("4a: census PASSES the known object set (MS_USER actor + S3_BUCKET container)",
      owned_by_object_census({"MS_USER", "S3_BUCKET"}) == (True, []))
```

---

## 7. Landing path (governed) -- an ATOMIC CO-MIGRATION SET, one window (CTO arch-gate @215258Z: GO; NO partial land)

1. **DS~B (me):** this concrete spec = the DESIGN. (I do NOT edit org/modules/graph/cse_schema.py -- EXEC-locked.)
2. **CTO:** arch-gate CLOSED / GO @215258Z (R1-R4 grounded/correct; co-migration made BINDING; + the Sec-4a guard).
3. **CVO:** re-sign -- exercise the 9 self-test checks + the OWNED_BY re-map parity on the LIVE graph
   (custody->OWNS, S3Key->CONTAINS, HAS_POLICY->GOVERNS). CVO's live exercise, not a config read.
4. **The atomic land set (ONE window, COO-coordinated -- a schema bump without its consumers repointed is the
   half-migration trap):**
   a. cse_schema.py bump (Sec 1-4a) -- **COO/exec single-editor**.
   b. `cse_emit_graphhead.py:102` flat `.get()` -> `map_cloudedge` -- **AE/0.7.0**. CRITICAL: this is the
      graph-head EMITTER; if left on flat `.get()` the LIVE graph gets the 232 S3Key edges as OWNS not CONTAINS.
   c. my P2 parity/coverage tools (`NFRA_CSE_P2_ac4_fullgraph_parity.py:203`, `NFRA_CSE_P2_coverage_sweep.py:150`)
      -> `map_cloudedge` -- **me (~B), same window**, self-committed.
   d. rule-bank @967f23fe1 GOVERNS->OWNS re-point -- **~C, same window**.
   e. **PRE-LAND ESTATE SWEEP RE-RUN** (`comp-grep CLOUDEDGE_TO_RELATIONSHIP` + any flat OWNED_BY resolution) at
      land-time -- the co-migration set must be COMPLETE (multi-call-site predicate-coverage; Rule 20). COO runs
      `comp-blast` on the OWNED_BY consumers when authoring the wave.
   f. HOUSEKEEPING: delete / no-land-mark the staged pre-canonical `deliverables/NFRA_CSE_P1_cse_schema.py`.
5. **~C:** verify post-land -- `owns`/Custodian bind to the OWNS edge + both OWNED_BY senses resolve correctly.

*-- 0.4.0_DS_ClientPlatform~B, cse_schema.py owner. Concrete OWNS 0.4->0.5 bump; governed landing.*
