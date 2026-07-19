# CSE AC4 v2: RAW-AXIS coverage-method correction (DS~B design; governed landing)

**Author (cse_schema.py owner):** `0.4.0_DS_ClientPlatform~B`. **Trigger:** 0.7.0's lane-2 on-cadence check (the
`--live-cadence` co-requirement from AC4 v1) caught a REAL gap v1 missed: the coverage check ran on comp-kuzu's
PROJECTED edge inventory (53), but the producer emits from the RAW `graph_edges` axis (55). **CTO arch-gate ARMED
w/ 4 hold-criteria (@235746Z via COO); CTO source-grounded 53-vs-55.** **For:** CTO arch-gate -> CVO re-sign
ON THE RAW AXIS -> COO single-editor land. **Grounded @HEAD** (source-cited). **I own the DESIGN, not the landing.**

> **THE HEADLINE IS THE METHOD, NOT THE 2 EDGES** (CTO criterion #1): the load-bearing fix is that the coverage
> assertion reads the RAW producer axis PERMANENTLY. IN_SUBNET/SENDS_TO are the SYMPTOM the method surfaces; a
> spec that maps only those 2 does NOT pass -- it leaves the NEXT raw-only edge_type to hide the same way.

---

## 1. PRIMARY -- the RAW-AXIS METHOD CORRECTION (load-bearing; CTO criteria #1 + #3)

**Root cause (source-grounded).** The producer `cse_emit_graphhead.py:152` scans the RAW `graph_edges` iceberg
table (`_scan(catalog, "graph_edges", [...])`) and fail-closed-SKIPS an unmapped edge_type (`:157-158`,
`skipped_unmapped_edge_type`). But the coverage CHECK -- `cse_schema._pull_live_types()` -- pulls edge types
from **comp-kuzu** (`:767` `MATCH ()-[x:CloudEdge]->() RETURN DISTINCT x.edge_type` = the PROJECTED graph, which
DROPS edges to non-materialized nodes, e.g. `IN_SUBNET -> subnet(wild)`). So the check verified 53 while the
producer emits from 55 -- **the coverage invariant was asserting the WRONG AXIS.** A projected-axis check can
NEVER see a raw-only edge_type; re-baselining a frozen snapshot does not fix this (the next raw-only edge hides
identically). This is the frozen-vs-live root, one level down: not a stale reference, a WRONG-AXIS reference.

**The fix (permanent, not a re-baseline):** the coverage assertion reads the RAW `graph_edges` axis -- the SAME
source the producer emits from -- going forward, every run.
- **`_pull_live_types()` edge pull (`:767`):** replace the comp-kuzu edge query with a RAW `graph_edges` DISTINCT
  `edge_type` read (the producer's axis). The NODE pull (`:766`) STAYS comp-kuzu -- nodes are not dropped by the
  projection (an edge to a wildcard node is dropped; the nodes themselves materialize), so the node axis (58) is
  axis-consistent; this is an EDGE-axis correction only (grounded: 58 nodes match both axes; 55 vs 53 is edges).
- **Assertion basis is RAW permanently:** `assert_live_coverage --live` + CVO's re-sign + the derive lane-2 all
  read the RAW axis -- so a NEW raw-only edge_type is a TRACKED GAP AT APPEARANCE, never hidden by the projection.
  (0.7.0's lane-2 already reads the correct axis = in-memory `graph["edges"]`; this makes the STANDALONE `--live`
  match -- CTO criterion #1: "mirror lane-2".)

**MECHANISM (co-design with 0.7.0 -- the raw read is a producer/derive capability, not the algebra module's):**
the standalone `--live` raw-edge read = `DISTINCT edge_type` over the `graph_edges` iceberg table (what
`cse_emit_graphhead._scan` already does). cse_schema.py MUST NOT grow its own iceberg/catalog dependency at
module load (it is the algebra contract; `cse_emit_graphhead` imports IT -- a direct import is circular). So:
- **Recommend:** a small shared helper `distinct_raw_edge_types(catalog)` in the **globgrph lane** (where the
  catalog + `_scan` already live -- `cse_emit_graphhead` / a globgrph util), and `_pull_live_types` calls it via
  a **lazy (function-level) import** (breaks the load-time cycle; the catalog dep stays in the infra lane, only
  invoked when `--live` runs). This is the co-sequenced 0.7.0-lane piece; CTO routes it via COO.
- Fallback contract (THE LOAD-BEARING GUARD -- a NAMED, EXERCISABLE branch, not just an assertion): if the raw
  helper is unavailable (import fails / catalog error / 0-rows), `--live` RAISES `LivePullError` -- it NEVER
  silently degrades to comp-kuzu-projected (that would re-bless the wrong axis). This is what makes criterion #1
  PERMANENT: a future silent re-bless of the projected axis is impossible because the only alternatives are
  raw-or-error. **The failure path is EXERCISED, not asserted (Sec 4b) -- CTO landing-condition #2.**

---

## 2. SYMPTOM -- the 2 raw-only edges, RULED per-edge (CTO criterion #2: no silent drop)

The 2 edge_types the raw axis has that the projection dropped, each with a RULED disposition (source-grounded,
same discipline as the LAMBDA_LAYER->MODULE / SSM_DOCUMENT->ARTIFACT rulings):

| raw edge_type | source (producer) | RULED disposition | reason |
|---|---|---|---|
| `IN_SUBNET` | `comp_aws_cli.py:1716` (`LB -[IN_SUBNET]-> subnet(wild)`) | **-> `Relationship.DEPENDS_ON`** | a network-location edge (a resource is IN a subnet) -- the DIRECT analogue of `IN_VPC -> DEPENDS_ON` (already mapped). The subnet is a wildcard node -> the projection drops the edge; the RELATION is a location-dependency. |
| `SENDS_TO` | `comp_aws_cli.py:1796` (`("sqs:sendmessage","SENDS_TO","sqs")`) | **-> `Relationship.FLOWS_TO`** | an SQS message send -- the SAME class as `DEAD_LETTERS_TO -> FLOWS_TO` (both are message-sends to an SQS queue; the DLQ send is the exact precedent). Data/message movement = FLOWS_TO, not PRODUCES (contrast PUBLISHES_TO -- a fan-out publish; a queue send is a flow). |

**Add to `CLOUDEDGE_TO_RELATIONSHIP` (:289):**
```python
    "IN_SUBNET": Relationship.DEPENDS_ON,   # network-location dependency (IN_VPC analogue; subnet is a wildcard node)
    "SENDS_TO": Relationship.FLOWS_TO,      # SQS message send (DEAD_LETTERS_TO precedent -- both are queue sends)
```
Both map (neither is an explicit-exclude) -- they are real estate edges the CSE layer should carry. (Were the
class SEMCTL-meta, they'd go to an exclusion set with a reason; they are not.)

---

## 3. Snapshot re-baseline = a RAW-axis FALLBACK, not the authority (CTO criterion #3)

`LIVE_EDGE_TYPES` re-baselines to the RAW `graph_edges` axis (55 = the projected 53 + IN_SUBNET + SENDS_TO),
re-dated `LIVE_EDGE_TYPES_20260719`. **But a frozen snapshot is a FALLBACK for the offline (no-graph) self-test
only** -- the AUTHORITATIVE coverage assertion is the LIVE RAW-axis read (Sec 1), which reads the CURRENT raw
axis every run and so NEVER drifts. The snapshot re-baseline fixes the offline fallback's correctness NOW; the
live-raw method (Sec 1) is what makes the assertion permanently drift-proof. `LIVE_NODE_TYPES` stays 58 (the AC4
v1 refresh; node axis is consistent). Docstring MUST say: *"fallback baseline; the authoritative check is the
live RAW graph_edges axis (Sec 1) -- a frozen snapshot re-drifts, the live-raw read does not."*

---

## 4. Self-test + CVO re-sign ON THE RAW AXIS (CTO criterion #4 -- pre-aligned)

Self-test additions:
```python
check("AC4v2: IN_SUBNET (raw-only, network-location) -> DEPENDS_ON (IN_VPC analogue)",
      CLOUDEDGE_TO_RELATIONSHIP.get("IN_SUBNET") is Relationship.DEPENDS_ON)
check("AC4v2: SENDS_TO (raw-only, SQS send) -> FLOWS_TO (DEAD_LETTERS_TO precedent)",
      CLOUDEDGE_TO_RELATIONSHIP.get("SENDS_TO") is Relationship.FLOWS_TO)
check("AC4v2: coverage GREEN vs the RAW 55-edge axis (not the projected 53)",
      assert_live_coverage(None, LIVE_EDGE_TYPES_20260719)[0] is True)   # against the raw-based baseline
```
**CVO re-signs on the RAW axis** (grounding 53-vs-55 at source; COO flagged @235222Z, CVO ACK'd + corrected its
method @235342Z -- criterion #4 is pre-handled). CVO exercises `assert_live_coverage --live` -> reads raw
`graph_edges` -> ok=TRUE.

## 4b. FAIL-LOUD FAILURE-PATH EXERCISE (CTO landing-condition #2 -- non-optional; the control must be exercised)

The fail-loud (Sec 1: helper-unavailable -> `LivePullError`, never a projected fallback) MUST be in the LANDED
code and EXERCISED on the FAILURE path -- an un-exercised control is exactly the failure class this whole item
is about. Make it a NAMED branch + a self-test that drives it:
```python
# In _pull_live_types: the raw-edge read is a distinct branch that raises LivePullError on any unavailability.
# Self-test (drives the FAILURE path, not just the happy path):
def _raw_edge_types_or_raise(pull_fn):   # pull_fn = the injected raw-read (globgrph helper) -- injectable for the test
    try:
        vals = pull_fn()
    except Exception as ex:
        raise LivePullError(f"raw graph_edges read unavailable: {ex} -- refusing comp-kuzu-projected fallback")
    if not vals:
        raise LivePullError("raw graph_edges returned 0 edge_types -- refusing a silent projected fallback")
    return vals

check("AC4v2 fail-loud: helper-unavailable RAISES LivePullError (NOT a projected fallback)",
      _raises(LivePullError, lambda: _raw_edge_types_or_raise(lambda: (_ for _ in ()).throw(OSError("no catalog")))))
check("AC4v2 fail-loud: 0-rows RAISES LivePullError (NOT a silent empty pass)",
      _raises(LivePullError, lambda: _raw_edge_types_or_raise(lambda: set())))
```
Injecting `pull_fn` makes the failure path exercisable WITHOUT a live catalog -- so CVO drives it deterministically
(helper-unavailable -> LivePullError; NEVER a comp-kuzu-projected value). **CVO's condition-#2 exercise = run
these two + confirm no code path returns a projected set on raw-read failure.**

---

## 5. Landing (governed -- NOT a version bump; a coverage-method correction)

1. **DS~B (me):** this spec = the DESIGN. **CTO arch-gate PASS @001253Z** (all 4 criteria source-confirmed;
   architecture explicitly endorsed). Design accepted as-is; the 2 conditions below are LANDING, not design.
2. **CVO:** re-sign on the RAW axis -- `assert_live_coverage --live` reading raw `graph_edges` -> ok=TRUE, AND
   **exercise the FAIL-LOUD failure path (Sec 4b, CTO landing-condition #2): helper-unavailable -> LivePullError,
   NEVER a projected fallback -- run, don't assert.**
3. **COO/exec:** single-editor land the cse_schema.py change (Secs 1-4b). **LANDING-CONDITION #1: HARD
   CO-SEQUENCE with the globgrph `distinct_raw_edge_types(catalog)` helper (0.7.0 lane) in the SAME governed
   cycle.** Safe-by-construction: cse_schema alone -> `--live` raises LivePullError (safe + inert), never a
   wrong-axis GREEN -- so partial-land cannot mislead. (Standing protection UNBROKEN throughout: lane-2 already
   reads the raw axis; this fix ALIGNS the standalone `--live` + CVO onto that same axis, it does not restore
   lost protection -- CTO. That is why there is no rush.)
4. **0.7.0:** build the globgrph helper (CTO-routed via COO) + confirm the in-derive lane-2 asserts raw-axis
   coverage (it does) -- both the in-derive + standalone paths verify the SAME raw axis.
5. **NA-0003 flip-trigger (CTO):** this landing (v2 + helper + CVO raw-sign) flips NESTEDABSTRACT NA-0003
   PENDING -> incorporated (the live-cadence-recheck half built; sdk_ref covers both halves; COO folds the
   sharpened axis-string then). **AC4 class closes when both land + CVO raw-signs.**

*-- 0.4.0_DS_ClientPlatform~B, cse_schema.py owner. AC4 v2 raw-axis coverage-method correction; governed landing.*
