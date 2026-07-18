# NFRA_ONTOLOGY -- C3 System Emergence + Naming (the "where do the names come from" answer)

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-18. **Trigger:** Andrew-direct -- *"where do the 'names' for the
c3 systems come from?"* **Status:** DRAFT (fleshes out C3, my lane -- NOT DS~B's; DS~B is only the SoD
graph-write). Grounded on comp-kuzu @2026-07-18T02:18Z (HEAD current).

**The short answer:** a C3 system's name is **INHERITED from the estate's own naming carried by its shared
constituents -- never invented.** My earlier A+B candidate names (`object-data`, `table-data`, ...) were
INVENTED type-descriptors; that was the mistake this doc corrects.

---

## 1. Two separable things -- emergence (deterministic) vs naming (was the gap)

**Emergence is already deterministic** (NFRA_SYSTEM, I do NOT re-implement): a C3 system = a connected
component of >= 2 C2 motifs, by union-find over SHARED CONSTITUENTS (or shared-cluster co-membership)
(`NFRA_MOTIF_P2_c3_emergence.py:111`). So WHICH motifs cluster into a system is a pure structural fact.

**Naming was NOT solved.** The 1 existing C3 system is literally named `EmergentSystem` (a generic type) +
an inferred `theme` ("firm-conditional-display") + a reference to its shared `cluster:AdvisorIntelligence`.
So today a system has a generic label + an inferred theme -- neither is a principled, deterministic NAME.
That is exactly the gap the question exposes.

---

## 2. Where the names ACTUALLY come from -- the estate names its own capabilities (grounded)

The graph already carries capability-names on the constituent nodes, at three levels:

| Source node-type | Name form | Examples (live in the graph) | Semantic level |
|---|---|---|---|
| **`PanelCluster`** | `cluster:<Capability>:<n>` | `AdvisorIntelligence`, `Attribution`, `Correlation`, `CapitalMarketAssumptions`, `DataRefresh` | **business capability** (highest) |
| **`Pipeline`** | `<firm>-<tier>` | `bd-gold`, `inf-gold`, `mdpf-gold` | firm/pipeline thread |
| **`S3_BUCKET`** (+ other resources) | `opal-data-<firm>` / `<firm>-...` | `opal-data-bd`, `opal-data-inf`, `opal-data-cot`, `opal-data-etfs` (18 domain buckets) | firm/domain |

The existing `EmergentSystem` ALREADY inherited its identity from `cluster:AdvisorIntelligence` -- so the
mechanism is half-there; it just stops at the generic type-label instead of PROMOTING the inherited capability
to the name.

---

## 3. THE NAMING LADDER (deterministic, priority order -- the answer)

A C3 system's name = the **dominant SHARED NAMED-CONSTITUENT** of its connected component, resolved by this
priority ladder (each rung deterministic; LAW-1 lexical-certainty):

1. **Shared capability cluster** -- if the component's motifs share a `PanelCluster`/named-thread, inherit
   its capability: `cluster:AdvisorIntelligence` -> **system:AdvisorIntelligence**. (The estate's real
   business-capability names; highest semantic value.)
2. **Shared pipeline thread** -- if they share a `Pipeline`, inherit it: `bd-gold` -> **system:bd-gold**.
3. **Shared resource-domain token** -- if the constituents share a firm/domain token (boundary-anchored, the
   same `firm_of()` predicate the suppression file uses), inherit it: all under `opal-data-bd`/`bd-49f-*` ->
   **system:bd**. Deterministic from the resource names.
4. **Governed catalog** -- ONLY where 1-3 underdetermine (a purely structural component with no capability/
   thread/domain anchor): a human-BLESSED name for the component-SIGNATURE, read-from-file (identical
   governance to canon-patterns' `roles:` + the C2 phrasing catalog). Governed, auditable -- **not runtime-
   invented.**
5. **NEVER invented at emergence.** A system with no inheritable name + no catalog entry stays UNNAMED (a
   `system:<signature-hash>` placeholder, counted in the denominator) until a governed name is blessed --
   the same honest-degrade discipline as C0 `Concept`.

**This is the same principle as C2 typing, applied to naming:** C2 motifs derive their TYPE from structure;
C3 systems derive their NAME from the estate's own naming that the structure already carries. Determinism
holds end-to-end.

---

## 4. Correction: the real A+B system names (my invented candidates were wrong)

My A+B materialization spec proposed `object-data`/`table-data`/`identity`/`compute-orchestration`/`pipeline`
-- INVENTED type-descriptors, exactly the anti-pattern. Corrected, the A+B systems inherit:
- **Pipeline-plane systems** -> `system:bd-gold`, `system:inf-gold`, `system:mdpf-gold` (rung 2, the real
  Pipeline threads).
- **Data/storage-plane systems** -> `system:bd`, `system:inf`, `system:cot`, ... (rung 3, the firm domains).
- **Cloud-compute systems** -> named by the domain/thread the Lambdas serve (rung 2/3).

## 5. The insight the naming exposes -- true capability-systems are CROSS-PLANE

The RICHEST C3 names (`AdvisorIntelligence`, `Attribution`, `Correlation`) live on the FRONTEND
(`PanelCluster`, plane C). A true business-capability system (e.g. `AdvisorIntelligence`) SPANS planes -- the
frontend cluster + its `DataFetch`/`Endpoint` (fetch) + the `Lambda`/`API_ROUTE` (backend) + the `S3`/pipeline
(data) that all serve it. So:
- **A+B-alone systems = the firm/domain INFRASTRUCTURE systems** (`bd-gold`, `opal-data-bd`) -- correctly
  named by rungs 2-3.
- **The business-CAPABILITY systems (`AdvisorIntelligence`) require plane C** to pick up their capability
  name (rung 1). This SHARPENS the coverage question: A+B-first gives the infrastructure system layer;
  folding C is what surfaces the human-capability system names. (Not a reason to change the A+B-first
  materialization order -- a reason the C fold is the semantic payoff after it.)

## 6. Materialization note (~A fog-4, folded)

Per ~A: an archetype (Role/Relationship) + a system-NAME should be an **ATTRIBUTE on the existing
C2Motif/C3System node**, NOT a new node-type or a parallel emission (which would collide + need CVO re-sign).
So naming a C3 system = writing an inherited `name`/`capability` attribute onto the emerged `C3System` node --
a light, additive, governed write, not a new structure. (Reinforces: the naming ladder RESOLVES the name; the
SoD pipeline WRITES it as an attribute.)

## 7. Do I need DS~B for this? -- NO (the language) / YES only for the write

- **The C3 language -- emergence understanding + the naming ladder + the governed name-catalog -- is MY lane,
  done here.** No DS~B needed.
- **DS~B (+ 0.7.0 + CVO) is needed ONLY for the SoD graph-WRITE** (materializing/attributing the nodes), the
  same separation as the C2 materialization. The naming LADDER is the spec they write FROM.

*-- 0.8.0_AE_CloudComp~C. C3 emergence + naming; capability names grounded in comp-kuzu @2026-07-18T02:18Z.*
