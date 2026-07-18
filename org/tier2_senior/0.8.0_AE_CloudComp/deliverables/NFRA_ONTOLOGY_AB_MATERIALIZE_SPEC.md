# NFRA_ONTOLOGY -- A+B Canonical Motif Materialization Spec (for the SoD pipeline)

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-18. **Trigger:** Andrew-direct *"materialize A+B first into the
canonical layer."* **Status:** DRAFT -- the VOCABULARY/detector spec (my lane). **The materialization RUN is
routed to the SoD pipeline (CTO arch-gate + `0.4.0_DS~B` substrate-consult + `0.7.0_AE_CloudOps` ingest + CVO
cert) -- I do NOT hand-write C2Motif/C3System nodes** (MSTR doctrine: hand-writing = a forged compression
layer, same class as a forged pipeline-complete.json).

---

## 0. The mechanism gap (surfaced per MSTR -- route the EXTENSION through CTO + DS~B)

The existing materializer `MOTIF_c2c3_materialize_spec.py` consumes `NFRA_MOTIF_P1_c2_catalog` +
`NFRA_MOTIF_P2_c3_emergence`. **The P1 catalog is the DEBT/deviation catalog (classes A1-A9)** -- so the
current semctl-c2c3-materialize is DEBT-CATALOG-COUPLED, NOT grain-parameterizable for canonical structural
motifs out of the box. **Materializing A+B canonical motifs requires EXTENDING the P1 detector catalog to
emit canonical structural motifs** (the ~13 typed-path detectors below). That extension is a CTO+DS~B SoD
build (it writes into the SoD-governed semctl layer + the C2 catalog), **not a ~C hand-patch.** This spec is
the INPUT to that build.

**Prereq already satisfied:** C2Motif/C3System are already in `NODE_TYPE_LAYER` (from the 07-08 debt
materialization), so adding canonical motifs of the SAME node_type does NOT trip the
`relabel_layers_by_node_type` fail-closed gate (`derive_runner.py:~1497`) -- no new node_type, no re-freeze
risk. (0.7.0/CVO confirm on ingest, per the existing convention.)

**Graph-completeness, NOT promotion** (per the existing spec's own distinction): this materializes DISCOVERED
canonical structure so it is queryable in-graph. It is NOT a PROMOTE (motif -> first-class recognizer, which
is separately human-ratified + measure-gated). Keep them distinct.

---

## 1. The A+B canonical motif detectors (13 families)

Each is a typed-path detector; instances = the concrete paths matching it (recurrence from the scan
@2026-07-18T02:18Z, HEAD current; denominator = 35,613 edges / 101,712 2-hop paths). `tier: canonical`
(contrast the debt tiers gate-ready/advisory/candidate-gen).

### Plane A -- Cloud / IAM / Serve
| motif_id | detector (typed path) | recur |
|---|---|---|
| `motif:a-store` | `(S3_BUCKET)-[CONTAINS]->(S3Key)-[OWNED_BY]->(S3_BUCKET)` | 28902 |
| `motif:a-access` | `(LAMBDA\|EC2_INSTANCE)-[READS\|WRITES]->(S3_BUCKET)` | 339/267/86/50 |
| `motif:a-table` | `(LAMBDA)-[READS\|WRITES]->(DYNAMODB_TABLE)-[ENCRYPTS_WITH]->(KMS_KEY)` | 180/178 |
| `motif:a-grant` | `(LAMBDA\|SERVICE_PRINCIPAL\|INSTANCE_PROFILE)-[ASSUMES\|CAN_ASSUME]->(IAM_ROLE)-[HAS_POLICY]->(IAM_POLICY)` | 914/543/96 |
| `motif:a-event` | `(EVENT_SOURCE)-[EMITS_TO]->(EVENT_RULE)-[TRIGGERS]->(LAMBDA)` | 112 |
| `motif:a-api` | `(API_GW)-[HAS_ROUTE]->(API_ROUTE)-[ROUTES_TO]->(LAMBDA)` | 82 |
| `motif:a-serve` | `(CLOUDFRONT_DISTRIBUTION)-[ORIGIN\|USES_OAI]->(S3_BUCKET)`; `(DataFetch)-[IS_ENDPOINT]->(Endpoint)-[READS_URL]->(ServedURL)` | 228/50 |
| `motif:a-watch` | `(CW_ALARM)-[MONITORS]->(LAMBDA\|EC2_INSTANCE)` -- **the Observer motif** | 184/71/50 |
| `motif:a-orch` | `(STATE_MACHINE)-[INVOKES]->(LAMBDA)` | 62 |

### Plane B -- Pipeline / Data
| motif_id | detector (typed path) | recur |
|---|---|---|
| `motif:b-struct` | `(Pipeline)-[CONTAINS]->(PipelineScript)-[CONTAINS]->(PipelineFunction)-[CALLS]->(PipelineFunction)` | 1201/1623 |
| `motif:b-run` | `(EC2_INSTANCE)-[RUNS]->(PipelineScript)` | 248 |
| `motif:b-io` | `(PipelineScript\|PipelineFunction)-[READS_S3\|WRITES_S3]->(S3Key)-[OWNED_BY]->(S3_BUCKET)` | 304/139/130 |
| `motif:b-dataflow` | `(Field)-[FLOWS_TO]->(Field)` | 956 |

---

## 2. Candidate C3 systems (P2 emergence computes the actual union-find; these are candidates)

C3 = connected components of >= 2 A+B motifs sharing constituents (`NFRA_MOTIF_P2_c3_emergence` runs the
union-find -- I propose the candidates from shared node-types; P2 is authoritative):

| candidate system | member motifs | shared constituents |
|---|---|---|
| `system:object-data` | a-store, a-access, a-serve, b-io | S3_BUCKET, S3Key |
| `system:table-data` | a-table, a-api, a-event, a-orch | DYNAMODB_TABLE, LAMBDA |
| `system:identity` | a-grant (+ a-access via LAMBDA) | IAM_ROLE, LAMBDA |
| `system:compute-orchestration` | a-event, a-api, a-orch, a-watch, b-run | LAMBDA, EC2_INSTANCE, EVENT_RULE |
| `system:pipeline` | b-struct, b-run, b-io, b-dataflow | PipelineScript, PipelineFunction, S3Key, Field |

(These overlap -- union-find will merge/split per shared-constituent connectivity. The candidates size the
expected C3 layer: ~3-5 operational systems from the A+B planes, vs the 1 degenerate debt-system today.)

---

## 3. Materialization convention (from the existing spec -- the extension emits these records)

- C2 node: `node_id="motif:<idiom>"`, `node_type="C2Motif"`, props = `{motif_type, plane:"A"|"B",
  tier:"canonical", recurrence, n_instances, detector}` + `props.via_detectors` (lossless provenance).
- C3 node: `node_id="system:<name>"`, `node_type="C3System"`.
- CONTAINS edges: `C3System -CONTAINS-> C2Motif` (C3->C2); `C2Motif -CONTAINS-> <bare C1 instance node_id>`
  (C2->C1 -- the ladder `c1:D{n}:` discriminator STRIPPED so it resolves to the EXISTING estate store node;
  see the 07-08 comp-kuzu RAVC: c1:D{n}: form = 0 rows, stripped = resolves).
- LAW-2: every node carries its recurrence + decompression footprint (no latent node in the store).

---

## 4. Routing (the SoD pipeline -- I feed the spec, I don't run the write)

| step | owner | action |
|---|---|---|
| extend the P1 detector catalog to emit these 13 canonical motifs | **CTO (SoD arch-gate) + `0.4.0_DS~B` (P1/substrate author, consult)** | add canonical detectors to `NFRA_MOTIF_P1_c2_catalog` (or a canonical sibling); the current catalog is debt-only |
| emit the materialize JSON (nodes + CONTAINS) | `0.4.0_DS~B` (produces `motif_c2c3_materialize.json`-analog) | run the extended catalog + P2 emergence over the fresh graph |
| ingest into the semctl layer | `0.7.0_AE_CloudOps` (derive/ingest path) | same path as the debt materialize; dual-sign |
| round-trip cert | CVO | the discovered->materialized round-trip |
| the vocabulary + grain + this spec | **`0.8.0_AE_CloudComp~C` (me)** | own the detector definitions + grain; feed the pipeline; verify the materialized A+B layer against this spec (sharpest-instrument re-census) |

**RAVC:** MSTR ratifies the FINAL closed vocabulary set post-CTO-gate (not per-step -- MSTR cut the cadence).
The A+B materialization RUN is CTO/DS~B/0.7.0/CVO execution I feed + verify, not hand-write.

*-- 0.8.0_AE_CloudComp~C. A+B materialization spec; detectors from comp-kuzu @2026-07-18T02:18Z (HEAD current).*
