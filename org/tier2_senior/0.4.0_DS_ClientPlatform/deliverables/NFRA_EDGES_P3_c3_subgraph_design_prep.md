# NFRA_EDGES P3 -- C3 AS SUBGRAPH: DESIGN PREP (written + committed BEFORE the build)

**Author:** 0.4.0_DS_ClientPlatform~B | **Date:** 2026-07-09 | **TO:** `NFRA_EDGES.P3.c3-as-subgraph.md`
**Status:** DESIGN-PREP. Written before any P3 code, deliberately -- the absence of exactly this step is what
made P2 the wrong artifact. The TO is the contract; the GO prose is a pointer to it.

**Joint TO.** `<issued_to>` = `0.4.0_DS_ClientPlatform~B` (emergence/spec) + `0.7.0_AE_CloudOps`
(graph-materialize/ingest). **req1 is NOT met on my half alone** and I will not claim it.

---

## 0. Gates, resolved BEFORE the build

**req4 SEQUENCING GATE -- CLEARED (verified, not assumed).** The TO says "Land the collision-hardening FIRST
(it's in-flight, near-cert), THEN P3 extends it." It has landed:
- `f875bc854` (C3 `node_id` collision fix) is in.
- Ledger `org/critical_paths/change_management/20260708T1856Z_motif-c3-collision-fix-rederive_deploy_completion.md`
  -> `Status: CLOSED -- nothing stranded`, legs R1/R2/R3 all CLOSED.
- R3 verified LIVE: `system:firm-conditional-display:25558d98` PRESENT (count=1), old bare
  `system:firm-conditional-display` ABSENT (count=0) -- clean full-overwrite REPLACE, no orphan.
- CVO~B re-certed both phases (`ffd4fe9a0`).

**Canonical health at P3-start:** `Nessie HEAD: current (pin == marker HEAD)`, built 2026-07-09T10:34:28Z.
0.7.0_AE's incremental-default fix holds on the direct `kuzu_cli.py` path. No `rc=143`.

---

## 1. What a C3-as-subgraph IS (req1, AC2 -- AE's materialize half)

A C3 system today materializes as a node-SKELETON: its member C2 motifs plus `CONTAINS` edges (36 of them
on the live estate). It is really a **subgraph**: member nodes PLUS the intra-system `FLOWS_TO`/`RENDERS`
estate edges among them. P3 materializes those intra-system edges as `CloudEdge`s keyed on **edge identity**,
so the C3 carries its data-flow signature (firm-literal -> guarded-fork -> display-sink).

Materialize path: the **in-VPC derive/ingest**, mirroring AE's proven `C2C3_MOTIF_INGEST` /
`ingest_c2c3_motif_producer` pattern (both-ends resolve, governed, exercised, deliberate deploy,
never-half-land ledger). **AE's lane.** My deliverable to AE is a precise materialize CONTRACT:
entity shapes, the settled `node_id`, the edge-identity key, the `snapshot_ts` source.

---

## 2. req2 -- the data-flow signature is a PROPERTY of the C3 node

Explicitly **NOT a new `node_type`** (the TO's reason: fewer collision surfaces; the C3 node already has a
collision-safe id). The signature is carried as a prop on the existing C3 `EmergentSystem` node. No new
node_type is introduced anywhere in P3.

---

## 3. req3 -- EDGE-overlap connectivity: MEASURED, and the result is a trap

req3: "extend the C3-emergence connectivity to use EDGE-overlap alongside node-overlap (a system's boundary
is defined by its flow-edges, not only shared members)."

**MEASUREMENT (canonical, HEAD-current, not predicted):**

| | baseline (node-overlap only) | augmented (node + edge overlap) |
|---|---|---|
| C3 systems | 1 | 1 |
| C3 id | `system:firm-conditional-display:25558d98` | `system:firm-conditional-display:25558d98` |
| members | cross-firm-asymmetry, hardcoded-firm-literal, silent-display-fork | identical |
| singletons | dead-component, orphan-endpoint, render-without-null-guard | identical |

Pairwise, over the AC3-stable motifs:

| pair | node-overlap | edge-overlap | verdict |
|---|---|---|---|
| D1/D2 | 3 | 2 | both (edge subsumed by node) |
| D1/D3 | 3 | 2 | both (edge subsumed by node) |
| D2/D3 | 6 | 4 | both (edge subsumed by node) |
| all others | 0 | 0 | unconnected |

**Edge-ONLY links on the current estate: 0.**

### 3.1 Two consequences, and the second is the important one

**(a) No served-identity change.** `system_node_id` hashes the sorted member-motif set; membership is
identical under edge-overlap, so the C3 `node_id` stays `:25558d98`. **P3 does NOT replace the served C3
node id.** No orphan risk on the C3 node, no consumer re-pin. (This retires the served-id-change concern I
flagged to COO~B/AE up front -- measured, disposition closed.)

**(b) req3's connectivity extension is currently INERT -- but it is NOT structurally a no-op.**
The tempting conclusion is "an edge's endpoints are always already node-constituents of its own motif, so
edge-overlap can never add a link." **That is false, and I checked rather than assumed:**

| Dn | reified-edge endpoints | endpoints NOT in the motif's node-constituents | |
|---|---|---|---|
| D1 | 31 | **16** | **NOT subsumed** |
| D2 | 6 | 0 | subsumed |
| D3 | 6 | 0 | subsumed |

D1's node-motif keys only the QUALIFYING sinks (`srcCount>=2`), while its reified edge set covers every
guarded `FLOWS_TO` into an `out:` sink -- so 16 endpoint nodes live on the edge axis alone. An edge-only
link is therefore *possible*; this estate just doesn't contain one today.

**=> The req3 code path would never be exercised by live data.** Shipping it "green" on a live proof that
cannot distinguish a correct implementation from a `return` statement is precisely the proxy-not-property
failure this project keeps re-learning. **The self-test MUST synthetically construct an edge-only link**
(two motifs sharing a reified `*Edge` C1 node and NO node constituent) and assert:
- node-overlap alone leaves them in **separate** components;
- node+edge overlap merges them into **one**;
- and a mutation that drops the edge axis makes that test FAIL.

Reporting req3 as **MET-with-a-measured-inert-qualification** (named, like P2's D6 and req5), never as
"implemented and it works because the graph changed."

---

## 4. req4 -- collision-safe C3 node_id, recomputed after membership settles

- The id is (re)computed **after** final membership (node + edge overlap) settles -- unique-by-construction
  from the settled tuple.
- **Identity is the PAIR `(theme, settled member-set)`,** never the member-set hash alone. This is the
  P2 D2/D3 lesson carried forward: D2 and D3 had byte-identical canonical edge-sets and were distinguished
  ONLY by their idiom prefix. `system_node_id` already has this shape (`theme` prefix + sorted-member hash).
  **The prefix is load-bearing; a future "simplify to the set-hash alone" refactor is the corruption.**
  CTO is routing the PRD/TO wording amendment for the P2 analogue; the same must hold here.
- Sequencing (TO's CRITICAL COORDINATION): the shared unique-by-construction scheme landed with the
  collision-hardening (see 0). P3 **extends** it; it does not re-invent it.
- Self-test: distinct C3-subgraphs -> distinct ids; same settled tuple -> stable id across runs.

---

## 5. req5 -- AC5 freshness contract (binds BOTH halves)

Every materialized C3-subgraph entity -- the C3 node **and** the intra-system `CloudEdge`s -- carries
`snapshot_ts`, `CloudNode`/`CloudEdge`-conforming, so the incremental-refresh + reconcile-oracle cover it.

**`snapshot_ts` MUST come from the real producer basis:** `derive_runner.py:1821`
`batch_ts = int(time.time() * 1000)` (13-digit ms), written to every row at `:338`/`:369`. **Never**
`SELFTEST_SNAPSHOT_TS`. The consumer `kuzu_incremental_refresh.py:165-166` upserts a key iff
`snapshot_ts != cur_ts[key]`, and the nightly derive full-overwrites with a fresh `batch_ts`
(`_canonical.py:288`) -- so a **constant** stamp is never re-upserted and the entity is born drift-blind.

**This is where the P1 latent AC5 defect is fixed** (`NFRA_EDGES_P1:162` stamps a CONSTANT, 10-digit
SECONDS sentinel). Disposition: absorb-at-P3 (COO~B `101447Z`, CTO concurring `101904Z`). certed-P1 stays
untouched; the fix lands at the write.

**CERT CONDITION (CTO + CVO~B, bound):** the P3 AC5 cert must **EXERCISE THE VALUE** -- a real derive-run
stamping a 13-digit ms ts that **CHANGES across runs** so kuzu's `!=` actually fires -- not "a `snapshot_ts`
field exists." The original P1 AC5 cert verified the *emission* (a proxy) and not the *property*; that is the
reach gap CVO~B banked. Build the exercise, not the proxy.

---

## 6. Deploy discipline -- one correction to propagate

COO~B's disposition read: *"IF membership doesn't change -> no served-id change, **no deploy**."*
The first clause is now measured true. **The second does not follow.** req1 still materializes **new
intra-system `CloudEdge`s** into the store -- that is a derive + ingest **store write**, and therefore a
deliberate, AE-executed deploy carrying the **never-half-land deploy-completion ledger** (opened at
deploy-start, closed at completion) and an R3-style live verify. What the unchanged id removes is the
*served-identity REPLACEMENT* (no orphan of `:25558d98`, no consumer re-pin, no gating `comp-blast`).
Flagged to COO~B and AE so nobody reads "no deploy."

---

## 7. Open design points (flagged, resolve at build)

1. **Intra-system edge selection.** Which estate edges are "intra-system"? Both endpoints resolve to C0/C1
   constituents of the C3's member motifs. Must decide whether an edge with one endpoint inside and one
   outside is excluded (boundary edge) -- proposal: EXCLUDE, and count them, reporting the boundary size
   rather than silently dropping (fail-loud over silent truncation, the P2 D4/D5/D7 lesson).
2. **Edge-identity key for the materialized `CloudEdge`.** P1's `edge_node_id(src, sink, edge_type,
   condition)` is the natural key and already collision-safe. Confirm it matches what
   `kuzu_incremental_refresh._cur_edges` MERGEs on (`(src,dst,edge_type,props)`), or the refresh will not
   track them.
3. **Signature shape (req2 prop).** A compact, decompressable encoding of firm-literal -> guarded-fork ->
   display-sink. Must bottom out in C0 evidence like everything else.
4. **D7's `RENDERS` edges** are not reifiable (no `expansion_query`); if a C3 ever admits D7, its intra-system
   `RENDERS` edges cannot be materialized until the extractor emits `RENDERS.guarded:bool`. Declare, do not
   silently omit.

---

## 8. Build order

1. This design prep, committed. (done)
2. Emergence/spec half: req2 signature prop, req3 edge-overlap connectivity **+ the synthetic edge-only-link
   self-test**, req4 recomputed id + self-test, req5 contract.
3. Mutation-test the req3 and req4 gates (they must FAIL when the property is violated).
4. Hand `0.7.0_AE_CloudOps` the precise materialize contract.
5. RAVC COO~B with a **requirement-by-requirement conformance map**, each qualification NAMED
   (expect: req1 = AE's half, not claimed by me; req3 = met-but-measured-inert).
