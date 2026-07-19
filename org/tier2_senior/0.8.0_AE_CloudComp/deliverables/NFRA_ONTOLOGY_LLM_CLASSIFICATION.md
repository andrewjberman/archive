# NFRA_ONTOLOGY -- Additive LLM-Classification Layer (motifs + systems)
<!-- genesis-surface: NFRA_ONTOLOGY -->

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-18. **Trigger:** Andrew-direct *"yes i absolutely want the
llm-classification layer of the motifs and systems."* **Status:** DRAFT -- design + FIRST PASS executed on the
live A+B layer. Doctrine-shaping (evolves the determinism principle) -> RAVC MSTR; graph-attachment gated by
CTO (additive attribute on existing C2Motif/C3System nodes, per ~A fog-4 -- NOT a new node-type).

## 1. The principle (structure deterministic, semantics additive)

The ontology's STRUCTURAL SPINE stays 100% deterministic + unchanged: typed-path motifs (C2), anchor-membership
systems (C3), roles/relations/variance. **This layer ADDS a semantic reading ON TOP** -- a plain-english
"what this pattern/capability IS" for the AGGREGATES ONLY (the ~100 motifs + the handful of systems), never
the 20k C0 atoms (they are already lexically named; classifying them would be expensive + pointless).

**Why the aggregates are the right target:** meaning CONCENTRATES in the aggregate -- a motif's meaning is not
in any single node (it is the recurring pattern); a system is a capability. The semantic characterization is
exactly what structure underdetermines and an LLM adds cheaply (~100 items, one-shot, then a trickle).

**Discipline (keeps the charter's determinism intact):**
1. **ADDITIVE + TAGGED** -- every label carries `source: llm-classified`; it never overwrites a structural fact.
   A consumer always knows which is ground truth and which is a reading. (The tag IS the honest "this is
   inference" channel.)
2. **Deterministic-inherited name WINS** where the estate names the capability (a system on the
   `AdvisorIntelligence` cluster IS AdvisorIntelligence -- no LLM). The LLM fills gaps + adds description/class.
3. **BOUNDED + additive-basis** -- classify only NEW aggregates as they emerge; never per-query, never the estate.
4. **RE-RUNNABLE + auditable** -- the (structure -> label) mapping is a recorded artifact.

**>> HARD INVARIANT (MSTR, load-bearing -- the one that keeps determinism from collapsing):
NO FEEDBACK INTO DETERMINISTIC PROCESSES. The LLM layer is a DESCRIPTIVE OVERLAY FOR HUMAN/AGENT READABILITY
ONLY. It must NEVER be an INPUT to a deterministic process -- the canon-deviation scorer, C3-emergence, the
completeness gate, motif/system membership must NEVER consume an `llm_class`/`llm_description` attribute as if
it were structural. Direction is STRICTLY ONE-WAY: `structure -> LLM label`, NEVER `LLM label -> structure/gate`.
If a deterministic decision ever reads the LLM label, a hallucination corrupts ground truth and the whole
determinism guarantee collapses. CTO gates this as an invariant on the attachment (the attr is read by
summaries/humans/agents, never by a scorer/gate/emergence). <<**

**Governance (Andrew-GO'd split):** LOOSE (tagged, directly usable) for `class` + `description`; STRICT
(blessed into the governed catalog) for an AUTHORITATIVE NAME. The honesty is the tag; the authority is the bless.

## 1a. The no-feedback LINT + the permitted/forbidden consumer line (CTO arch-gate @214500Z)

CTO ruled the no-feedback invariant a **LINT (a control that FAILS at violation time), not prose** -- "prose
is not enough." The attachment may LAND now (nothing reads `llm_*` today), but the lint is a REQUIRED forward
guard; it's a gate-candidate (same class as the `comp-manifest-check` family). The `llm_`/`source:
llm-classified` namespace makes the surface machine-detectable.

**THE LINT:** FAILS if any DETERMINISTIC STRUCTURAL/GATE surface reads an `llm_*` attribute.
- **FORBIDDEN consumers (lint fails if they read `llm_*`):** the canon-deviation scorer (verdict),
  C3-emergence / materialize, the completeness gate, motif/system membership resolution, semctl promotion.
- Direction is strictly `structure -> label`; a `label -> structure/gate` read is the lint failure.

**THE PERMITTED/FORBIDDEN LINE (CTO, precise -- so ~D is not blocked):**
- **PERMITTED:** READABILITY (human/agent summaries) + ADVISORY-NON-GATING heuristics. comp-similar's
  summary-enrichment + BM25 similarity is LEGIT (comp-similar is ADVISORY -- never auto-acts; disposal stays
  the CTO-gated Andrew-delete-word path). So **~D consumes freely.**
- **FORBIDDEN:** STRUCTURAL/GATE processes only (the list above).
- **THE TEST:** does the consumer DECIDE structure or drive a gate/verdict/deletion? YES -> forbidden (lint
  fails). Reads only for a human, or for an advisory heuristic that never auto-acts -> permitted.

**Routing:** the lint BUILD routes through CTO (he gates it) as a forward guard; the attachment itself lands
now via the governed emit. This makes MSTR's invariant a control, not a hope.

## 2. Mechanism

Input per aggregate: its deterministic structure (a motif's typed-path + materialized instances; a system's
member-motifs + anchor). Classifier OUTPUT dict per aggregate: `{ class: <slug>, description: <plain-english>,
source: "llm-classified", model, at }`.

**Node-prop MAP (SEAM-LOCKED 2026-07-18 @1f258ee21-era; base+DS~B+~D grounded, 3 source reads).** The emit
writes the classifier output onto the existing C2Motif/C3System node as ADDITIVE props under the key MAP:
`class` -> **`llm_class`**, `description` -> **`llm_description`**, plus the `source: llm-classified` tag +
`model`/`at` provenance. The node-prop key MUST be exactly `llm_class` (NOT bare `class`, NOT
`llm_classification`): the consumer (`summary_corpus.py:390` `d.get("llm_class")` -- display-only, M9-proven
auto-upgrade) and ingest (`derive_runner.py:213` excludes `llm_class` from `_NODE_FIXED_KEYS` -> it rides the
additive `props` JSON at :221-222) both lock on `llm_class`. **NO ingest backstop for a mis-named key** -- the
`SCHEMA_SEAM_SILENT_DROP` guard (:224-228) is `dropped=0` by construction, so a bare `class` lands silently in
`props.class` and renders no parens; the KEY-LOCK is the SOLE safety.

**PRODUCER = the ~C classification-layer OVERLAY (seam-lock resolution -- corrects the earlier "DS~B emit"
wording).** DS~B ground-verified the structural CSE/AB-MAT emit carries NO `llm_class` (`map_cloudedge` returns
a Relationship enum, never a node prop; grep-confirmed estate-wide). So the `class->llm_class` producer is a
SEPARATE governed OVERLAY emit written AFTER materialization -- the ~C classification layer -- NOT the DS~B
structural emit. It still rides the governed 0.7.0 ingest + CVO cert (not hand-written). Re-run classifies only
node_ids lacking a current `llm_class` (additive/idempotent).

## 3. FIRST PASS -- the 13 live A+B motifs (classified now)

| motif_id | class | description (source: llm-classified) |
|---|---|---|
| `motif:a-store` | object-storage | A bucket holding and owning its data objects -- the estate's data-at-rest primitive. |
| `motif:a-access` | compute-object-access | A function or instance reading/writing an object-storage bucket -- the primary data-plane access pattern. |
| `motif:a-table` | encrypted-table-access | Compute reading/writing a DynamoDB table encrypted with a KMS key -- keyed structured-data access, encrypted at rest. |
| `motif:a-grant` | identity-grant | A principal assuming an IAM role scoped by an attached policy -- the access-control grant pattern. |
| `motif:a-event` | event-driven-invocation | An event source emitting to a rule that triggers a function -- asynchronous event-driven compute. |
| `motif:a-api` | served-api | An API gateway routing a request through a route to a backing function -- synchronous served-request handling. |
| `motif:a-serve` | content-serving | Content served to the edge -- a CDN originating from a bucket, or a client fetch resolving a served URL. |
| `motif:a-watch` | observability | An alarm monitoring a function/instance's health -- side-channel observability (the Observer role). |
| `motif:a-orch` | workflow-orchestration | A state machine invoking a function as a step -- multi-step workflow orchestration. |
| `motif:b-struct` | pipeline-code-structure | A data pipeline composed of scripts and functions that call one another -- the batch-processing code hierarchy. |
| `motif:b-run` | batch-execution | A compute instance running a pipeline script -- scheduled/batch pipeline execution. |
| `motif:b-io` | pipeline-io | A pipeline reading/writing object storage -- its data I/O, and the bridge from the pipeline to object-data. |
| `motif:b-dataflow` | data-lineage | A field deriving its value from another field -- fine-grained data lineage/derivation. |

## 4. FIRST PASS -- the 3 live C3 systems (classified now)

| system | class | description (source: llm-classified) | authoritative name |
|---|---|---|---|
| `object-data` | data-platform | Durable data at rest in object storage, its access by compute + pipelines, and its serving. The firm's data-plane spine; overlaps `pipeline` at the I/O boundary. | object-data (anchor-inherited -- deterministic; kept) |
| `compute-orchestration` | orchestration-platform | Event- and workflow-driven invocation of compute -- how work is triggered and sequenced across the estate. | compute-orchestration (anchor-inherited; kept) |
| `pipeline` | data-pipeline | The batch data-processing pipelines -- code structure, execution, and I/O. Overlaps `object-data` at `b-io`. | pipeline (anchor-inherited; kept) |

**Note:** the systems' AUTHORITATIVE names stay the deterministic anchor-inherited ones (object-data /
compute-orchestration / pipeline); the LLM adds only `class` + `description` (loose-tagged). Where a future
system has NO anchor/capability name, the LLM proposes a name -> strict-bless into the governed catalog.

## 5. Extension (the full set as C+D materialize)

This pass covers the 13 materialized A+B motifs + 3 systems. The mechanism re-runs additively over the
frontend (C) + M365 (D) motifs + their systems when those materialize -- yielding the full ~100-motif /
~20-family classification Andrew scoped, at ~the same trivial cost. The frontend systems are where the
richest capability NAMES already live (PanelCluster: AdvisorIntelligence/Attribution/Correlation) -- there
the deterministic-inherited name wins and the LLM only characterizes.

## 6. Routing

- **RAVC MSTR** -- the doctrine admission (additive-tagged-LLM layer; structure stays deterministic). Sent.
- **CTO** -- route/gate the graph-attachment: the additive `llm_class`/`llm_description` prop on the
  C2Motif/C3System nodes, emitted by the ~C classification-layer OVERLAY (a SEPARATE governed emit, NOT the
  DS~B structural emit -- seam-lock 2026-07-18), riding the 0.7.0 ingest + CVO cert; no hand-write, no new
  node-type. **THE OPEN ROUTING DECISION:** the physical attachment path for the overlay emit (a ~C-owned
  overlay emitter vs. a DS~B governed-emit increment) -- both ride the same ingest + honor the `class->llm_class`
  map; CTO routes which. Behind the OWNS-bump.
- **me (~C)** -- own the classification (I am the LLM); this artifact IS the first-pass output; re-run additively.
- **~D (COMPSIMILAR consumer)** -- the `class`/`description` is additional summary-enrichment material
  (alongside the C2 motif clause + the C3 membership), same read-from-attribute discipline.

*-- 0.8.0_AE_CloudComp~C. Additive LLM-classification layer; first pass on the live A+B layer @HEAD 20:28Z.*
