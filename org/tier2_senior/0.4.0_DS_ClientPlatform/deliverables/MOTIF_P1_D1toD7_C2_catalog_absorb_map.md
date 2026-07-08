# NFRA_MOTIF-P1 -- D1-D7 -> first C2 motif catalog: ABSORB-MAP (pre-stage, pre-P2-2)

**author:** 0.4.0_DS_ClientPlatform~A (MOTIF graph-lane, confirmed next NFRA lane) | **date:** 2026-07-07
**status:** PRE-STAGE HEAD-START -- COO~B authorized 2026-07-08T00:12Z ("consume comp-cluster CLI to pre-stage the D1-D7 absorb before P2-2's edges are live... stay event-driven, no forced work"). **NOT** a GO'd build; MOTIF-P1 build begins on COO's GO once CSE-P2 / FEDOBS-P2 / TSGRAPH-P2-2 clear.
**source (grounded, not invented):** `deliverables/tsgraph_detectors.yaml` (commit cf1c1dcde, my TSGRAPH P3-2 detector-library, CVO-certed) -- absorb, don't rebuild (MOTIF PRD S5 P1 / grounding #67).
**PRD:** `docs/architecture/NFRA_MOTIF_PRD.md` (P1 = "ABSORB the TSGRAPH detector-library D1-D7 as the frontend-class C2 motif catalog... don't rebuild").

---

## 0. The absorb principle (why a detector IS a C2 motif)

MOTIF's C2 definition (PRD S3/S4.1): a **C2 motif** is a *lossy-toward-abstraction, lossless-toward-provenance* compression of a **connected C1 subgraph**, qualified by **recurrence >= 2** (a recurrence-1 pattern is an *instance*, not a motif -- AC3 stability threshold). Each detector Dn is precisely this: it template-matches a recurring frontend architectural **idiom** over the live C1 graph; every returned row is one **instance** (a connected C1 subgraph) that decompresses to file:line lexical evidence via the node_id + props. So:

> **absorb map:** detector `Dn` -> C2 motif `motif:<idiom>`; the detector's live row-set = the motif's **instances**; `len(rows)` = the motif's **recurrence** (stability); each row's node_id+props = one instance's **decompression chain** (C1 -> C0 -> evidence).

The detector library is thus the FIRST real C2 catalog by construction -- MOTIF wires it in, it does not re-derive detection. What P2-2 gates is only **C2-in-graph** (materializing these motifs AS C2 nodes/edges in the store); the catalog DESIGN + the detector queries (comp-kuzu, HEAD-current) are available now.

---

## 1. The C2 catalog (5 motifs absorbed + 1 overlap-lens + 3 documented gaps)

| C2 motif | from | idiom (motif_type) | recurrence (live) | tier | AC3 stable? | absorb verdict |
|---|---|---|---|---|---|---|
| `motif:silent-display-fork` | D1 | >=2 guarded FLOWS_TO from DISTINCT sources into one `out:` display sink | **5** | gate-ready | yes (>=2) | **ABSORB** (promote-first) |
| `motif:cross-firm-asymmetry` | D2 | firm-identity-literal FLOWS_TO with a one-sided branch (trueBranch=0 XOR falseBranch=0) | **2** (4 edges) | gate-ready | yes | **ABSORB** |
| `motif:dead-component` | D4 | ReactComponent with 0 inbound INSTANTIATES | **121 raw** (FP-dense) | candidate-gen | yes | **ABSORB as CANDIDATE motif** (file-level confirm before a finding -- carries D4's 3 FP-filter classes) |
| `motif:orphan-endpoint` | D5 | Endpoint with 0 inbound FETCHES | **49** | advisory | yes | **ABSORB (advisory)** |
| `motif:render-without-null-guard` | D7 | nullable Field is a RENDERS target | **197** (478 edges) | advisory | yes | **ABSORB (advisory / WARN)** -- gate-ready only after extractor `guarded:bool` |
| `motif:hardcoded-firm-literal` | D3 | bare firm-identity literal in a branch position | 4 (overlaps D2) | advisory | yes | **ABSORB as an OVERLAP LENS** (D3 n D2 on inflection edges is expected -- different lens, not a dup); original 'bd' anchor is a REMEDIATED incident, re-anchored to the live inflection literal |
| -- D6 (prop-drill-depth) | D6 | prop threaded through N>=4 components | **0** (structural miss) | GAP | no (recurrence 0) | **DO NOT ABSORB** -- PROP_PASSES is flat one-hop (JSXElement->Prop/Field); no chain >=2 exists on this substrate. Not a motif here; route to extractor-extension (transitive PROP_DRILL edge). |
| -- D8 (any-erosion / A4) | honest_gap | `: any`/`as any` at a data boundary | n/a (not graph-modeled) | GAP | -- | **DO NOT ABSORB** -- extractor emits no AnyCast node; route to DEBTSCAN/PORTALSWEEP ESLint or extractor-extension. |
| -- D9 (hook-dep-mismatch / A7) | honest_gap | useEffect/useMemo dep-array omit/over-list | n/a (not graph-modeled) | GAP | -- | **DO NOT ABSORB** -- no HookDep edges; route to extractor-extension (Hook->{declared}/{referenced} set-diff) or react-hooks/exhaustive-deps ESLint. |

**Honest catalog size:** 5 absorbed motifs + 1 overlap-lens (D3) = the frontend-class C2 set; **3 documented gaps** (D6/D8/D9) carried as coverage-channel entries with a named extractor-extension route (NOT silently dropped -- mirrors the PRD's own honest-gap discipline + LAW-2).

---

## 2. Per-motif decompression chain (AC2/AC6 -- every motif decompresses to evidence)

Each absorbed motif node, at materialize time, carries a **decompression chain** so it PASSES `comp-ladder` `fidelity_check` (AC6) -- a motif with no intact chain is a LATENT node = build-fail. The chain is already present in the detector output:

- **silent-display-fork** -> instance = (`out:<file:line>#<field>` sink) + the >=2 (`FLOWS_TO`, recompute/guarded, condition) edges + their DISTINCT source Field node_ids. Decompress: sink -> edges -> source Fields -> each Field's CSE -> `file:line` evidence. e.g. `out:portal/src/pages/ModelPortfolios.tsx:725#spread` <- {etf_spread | index_spread on benchmarkType==='index'}.
- **cross-firm-asymmetry** -> instance = dst Field + the firm-literal FLOWS_TO edges + the (trueBranch,falseBranch) asymmetry counters. Decompress: `out:...ClientsTab.tsx:291#name` <- inflection_wealth_management edge (falseBranch=2, trueBranch=0).
- **dead-component** -> instance = the ReactComponent node_id (`rc:<file>#<Comp>`) + the ABSENCE of an INSTANTIATES in-edge (the decompression is the negative-space evidence: node exists, 0 inbound INSTANTIATES) + the mandated file-level confirmation grep. e.g. `rc:portal/src/components/MetricsRow.tsx#MetricsRow`.
- **orphan-endpoint** -> instance = Endpoint node_id + 0 inbound FETCHES + file-level caller grep. e.g. `endpoint:getDataRefreshHistory`.
- **render-without-null-guard** -> instance = nullable Field node_id + its RENDERS in-edge(s) + tsType provenance (`optional:true` / `| null`). e.g. `type:portal/src/App.tsx#NavItem#requiresAdmin`.

Every node_id is a `file:line`(+symbol) address -> the lossless-toward-provenance property holds; the compression is only lossy toward abstraction (the motif TYPE hides the N instances -- the point).

---

## 3. Pre-P2-2 vs P2-2-gated split (what this pre-stage does / does NOT do)

- **Available NOW (this pre-stage):** the catalog DESIGN above + the detector queries run live against comp-kuzu (HEAD-current). The recurrence counts + decompression chains are grounded on the current graph (provenance: nodes_snapshot 8205589666541874180 / edges_snapshot 7012385084254624612, nessie_head=current).
- **Consume until P2-2 (PRD grounding #68):** the **comp-cluster CLI** extraction (15 pages / 91 clusters, EXTRACT-complete, NOT yet graph-materialized) is the interim C2 substrate -- MOTIF-P1 reads cluster membership from the CLI, not from graph edges, until TSGRAPH-P2-2 (0.7.0_AE) materializes the cluster edges.
- **GATED on P2-2 (the GO'd build, NOT this pre-stage):** materializing these motifs AS C2 nodes/edges IN the graph + the GRAPHDEPTH CONTAINS-rollup C1->C2->C3 compression (reuse, don't rebuild -- PRD #69) + emitting C3 systems. `motif:silent-display-fork` + `motif:cross-firm-asymmetry` (both gate-ready, both firm/display-correctness idioms) are the natural first C3-system seed (a "firm-isolation-integrity" capability), but that is P2/P3 work.

## 4. On the GO (MOTIF-P1 build entry checklist -- ready to execute)
1. Re-validate the 5 detector queries HEAD-current (self-heal marker oracle; counts drift, structure holds).
2. Materialize the 5 motifs + D3 lens as C2 catalog entries, each with recurrence + decompression chain, on the P2-2 cluster-edge substrate.
3. Bind every motif node to `comp-ladder` fidelity_check (AC6); a motif that will not decompress = build-fail.
4. Route the 3 gaps (D6/D8/D9) as coverage-channel entries + extractor-extension asks (not silent).
5. Reuse GRAPHDEPTH CONTAINS-rollup for the compression; emit stable motifs as PROMOTE candidates with recurrence + FEDOBS co-occurrence + decompression chain (P3, AC5).

---

## 5. BUILD EXECUTED -- GO'd 2026-07-08T0202Z by COO~B (re-allocated to 0.4.0_DS_ClientPlatform~B)

DS~A went idle (2 respawn-requests didn't take); COO~B re-allocated MOTIF-P1 to DS~B (LIVE + free + graph-capable). The pre-stage absorb-map above is now EXECUTED as a runnable, grounded, fidelity-passing artifact.

**Deliverable:** `deliverables/NFRA_MOTIF_P1_c2_catalog.py` -- the C2 catalog absorb.
- `python NFRA_MOTIF_P1_c2_catalog.py` -> live absorb (runs each detector on comp-kuzu HEAD-current, composes each into a C2 motif `Node`, fidelity-checks each).
- `--self-test` -> 7/7 (fidelity POSITIVE + 2 NEGATIVE controls [latent motif / evidence-less C0 both FAIL the gate] + AC3 threshold + the D2 type-bug regression).
- `--ladder Dn` -> the full comp-ladder (compression up + decompression down to file:line evidence) for one motif.

**Live absorb result (HEAD-current: Nessie HEAD=current, nodes-snap 6127141211382924351, edges-snap 7012385084254624612):**

| Dn | motif | tier | recurrence | AC3 | comp-ladder fidelity (AC6) | verdict |
|---|---|---|---|---|---|---|
| D1 | silent-display-fork | gate-ready | 5 | STABLE | **PASS** | ABSORB |
| D2 | cross-firm-asymmetry | gate-ready | 2 | STABLE | **PASS** | ABSORB |
| D3 | hardcoded-firm-literal | advisory | 4 | STABLE | **PASS** | ABSORB-overlap-lens |
| D4 | dead-component | candidate-gen | 121 | STABLE | **PASS** | ABSORB-candidate |
| D5 | orphan-endpoint | advisory | 49 | STABLE | **PASS** | ABSORB-advisory |
| D7 | render-without-null-guard | advisory | 197 | STABLE | **PASS** | ABSORB-advisory |

**6/6 STABLE motifs PASS the AC6 fidelity gate** (every motif decompresses C2 -> C1 interaction -> C0 lexical fact at file:line; no LATENT node). Gaps D6/D8/D9 routed as coverage-channel entries (not dropped). Recurrence matches the certed detector empirical exactly.

### D2 TYPE-BUG (grounded HEAD-current -- Rule 22 mechanism-confirmed; re-validation earned its keep)
The pre-stage recorded D2 recurrence=2; the live re-validation returned **0 rows**. Grounded the mechanism (did NOT paper over it): the graph was rebuilt since pre-stage (nodes-snapshot `8205589666541874180` -> `6127141211382924351`); on the current build `sum(CASE WHEN ... THEN 1 ELSE 0 END)` yields a **STRING-typed** column, so the yaml D2 query's final `WHERE trueBranch = 0 OR falseBranch = 0` compares string-vs-int and silently matches nothing. **The cross-firm-asymmetry motif is genuinely LIVE** -- 2 asymmetric inflection forks (`ClientsTab.tsx:291#name` + `LeaderboardEntry#name`, both trueBranch=0/falseBranch=2), grounded via the un-filtered bucket query. **Fix = `CAST(trueBranch AS INT64) = 0`** (confirmed: recovers the 2 rows), adopted as this catalog's canonical D2 query. **ACTION: flag the fix to the detector-library owner (`tsgraph_detectors.yaml`, 0.4.0_DE_ClientPlatform).** Structure held; the detector's filter had a build-exposed type bug.

### Scope executed now vs staged (P2-2-gated / P3)
- **DONE NOW (not P2-2-gated):** catalog absorb + template-match re-validation + recurrence (AC3) + decompression chains (AC2) + comp-ladder fidelity (AC6) + gap routing. The detectors match over the EXISTING C1 edges (FLOWS_TO/RENDERS/INSTANTIATES), so this leg needs no cluster edges.
- **STAGED on MOTIF-P0 (TSGRAPH P2-2 materialize, 0.7.0_AE):** materializing the motifs AS C2 nodes + CONTAINS edges IN the store; the GRAPHDEPTH CONTAINS-rollup on live cluster edges (req#2 -- semantics applied now, engine-on-live-edges staged); C3 emergence (P2).
- **STAGED P3:** PROMOTE candidate emission with the FEDOBS co-occurrence join (`iceberg.globgrph.cse` `cse_coevolution`, in-VPC/Trino).

---
*Pre-stage authored 2026-07-07 (DS~A); BUILD EXECUTED 2026-07-08 (DS~B) -- runnable + live-grounded + AC6-fidelity-passing. No graph mutation (C2-in-graph materialization is P2-2-gated). Grounded entirely in the certed detector library + live-graph HEAD-current provenance.*
