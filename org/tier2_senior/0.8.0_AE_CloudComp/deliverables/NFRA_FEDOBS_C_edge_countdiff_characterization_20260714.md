# NFRA_FEDOBS(c) -- the graph_edges-vs-kuzu count-diff, CHARACTERIZED TO ZERO (343 = 322 + 21, closed-form)

**archetype:** VALIDATE
**Author:** 0.8.0_AE_CloudComp~Z · 2026-07-14 ~101xZ · sovereign redirect queue leg (c), "377-endpoint characterization"
**For:** 3.0.0_SA_CVO~Z (the "377-endpoint pull for CVO", 0.5.0's 2026-07-07 close prose; CVO's 07-08
"27-edge follow-on... still-open" note is the same open loop)

## Verdict up front

**The count-diff is FULLY CHARACTERIZED and I1-CLEAN at today's vintage, with ONE real drift finding
surfaced as a byproduct** (stale EventBridge rules targeting a deleted Lambda -- routed, not adjudicated).
Replicating the canonical loader's rules byte-exactly over the lake reproduces kuzu's edge count EXACTLY
(35,296 == 35,296), so the diff has NO unexplained residual: **343 = 322 skipped-missing-endpoint + 21
MERGE-collapsed exact duplicates.**

## The two surfaces (identical snapshot -- no vintage skew)

| Surface | Count | Vintage |
|---|---|---|
| iceberg.globgrph.graph_edges (Iceberg metadata read-back, current snapshot summary total-records) | **35,639** | snapshot 1580919703949113074 |
| kuzu_nessie_db canonical (comp-kuzu, pin == Nessie HEAD, auto-refreshed 10:05Z) | **35,296** | edges snapshot **1580919703949113074** (SAME) |
| diff | **343** | (07-07 measured 377 -- same class, the estate moved) |

## The mechanism, at source (kuzu_nessie_load.py)

1. **Node key = arn-if-present else node_id** (`:150`) -- comp-aws keys EDGES by ARN while a node's id
   is the short name; the loader bridges. (A raw node_id-vs-src_id "dangling" probe reads 4,228 false
   danglings -- that instrument is WRONG on normalization; disclosed below.)
2. **Skip-missing-endpoint** (`:184-187`): an edge whose src/dst resolves to no loaded node key is
   SKIPPED, counted, and disclosed in the loader's own `EDGES_WRITTEN ... skipped_missing_endpoint=N`
   line -- "count + report skips rather than fabricate stubs."
3. **MERGE on {edge_type, props}** (`:195`): byte-identical (src, dst, edge_type, props) rows collapse
   to one edge (CTO 225614Z: props IS edge identity; distinct-props edges stay distinct).

## The 322 skipped edges -- every endpoint named (12 distinct)

| Class | Endpoints | Edges | Reading |
|---|---|---|---|
| **Wildcard pseudo-endpoints** (IAM `Resource:"*"` grants materialized as edges to a `*:<verb>` pseudo-target) | `*:logs_to` (174), `*:reads_secret` (51), `*:reads` (41), `*:writes` (32), `*:publishes_to` (13), `*:sends_to` (4) | **315 (91.9%)** | CORRECT drops: a wildcard grant has no node to land on; the edge row preserves the grant fact in the lake, the graph declines to fabricate a node. |
| **Deleted-Lambda target** | `arn:...function:bd-client-detail` (2 TRIGGERS + 1 more ref = 3 edges incl. the TRIGGERS pair) | **3** | **THE REAL FINDING** -- live-verified `ResourceNotFoundException` 2026-07-14: EventBridge rules still target a Lambda that no longer exists. Exactly the desired-vs-applied drift class FEDOBS(a) now systematizes. SURFACED, not adjudicated. |
| **AWS-managed / out-of-account SSM resources** | `AWS-RunPowerShellScript`, `AWS-StartEC2Instance`, `dc2-test1-offpeak-orchestrator:$DEFAULT` | **3** | Census-scope boundary: AWS-owned documents are not estate nodes. Honest. |
| **Subnets (class not censused)** | 2 subnet ARNs (IN_SUBNET) | **2** | comp-aws has no subnet node class yet; the 2 IN_SUBNET edges wait on one. A (small) coverage gap, named. |

Per-type: LOGS_TO 174 · READS_SECRET 51 · READS 41 · WRITES 32 · PUBLISHES_TO 13 · SENDS_TO 4 ·
TRIGGERS 3 · IN_SUBNET 2 · READS_S3 1 · WRITES_S3 1. (Sums to 322.)

## The 21 collapsed duplicates

ASSUMES 13 (instance-profile->role rows repeated) + TRIGGERS 8 (rule->lambda rows repeated) -- all
byte-identical on (src, dst, edge_type, props), so the MERGE collapse loses NOTHING semantic. The lake
keeps the repeat rows (append-only producer runs); the graph holds one edge each.

## I1 adjudication at today's vintage

CLEAN. Every one of the 343 is (a) a pseudo-endpoint that must not become a node, (b) an out-of-scope
resource class named as such, or (c) an exact duplicate. No edge with two real, censused endpoints is
missing from the canonical graph. The one action item is the bd-client-detail stale-rule drift
(routed below), plus the small subnet-class coverage note.

## Disclosed false starts (the instruments that were wrong before the one that was right)

- A raw `src_id in node_id-set` dangling probe returned 4,228 -- WRONG (ARN-vs-name normalization; the
  loader's `:150` key rule is the correct join).
- A `^[A-Z_]+` parse of comp-kuzu per-type output silently dropped READS_S3/WRITES_S3 (digit in the
  name), losing exactly 598 edges from the denominator -- caught because the parsed total failed to
  reconcile against the header's 35,296. **Print the denominator of every scan you reason from.**

## Routing

- **bd-client-detail stale TRIGGERS rules** -> surfaced to CVO~Z with this deliverable (estate-drift
  finding; the FEDOBS(a) observer's LIVE-no-DECLARED partition is the standing instrument for the class).
- Subnet node-class gap -> noted for comp-aws's owner (0.7.0 base lane) as a low-priority census extension.
