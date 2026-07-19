# NFRA_ONTOLOGY -- Canonical Motif Catalog (NEXT-A: the mined C2 language)
<!-- genesis-surface: NFRA_ONTOLOGY -->

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-18. **Status:** DRAFT -- RAVC MSTR + CTO. Companion to
`NFRA_ONTOLOGY_EMPIRICAL_GRAIN_SCAN.md`. This is the "assemble every C2 + qualify C3" Andrew asked for, at
the DECIDED grain (typed multi-hop path @ recurrence >= 50). All figures comp-kuzu @2026-07-18T02:18Z (HEAD
current); denominator = 101,712 2-hop paths / 197 distinct shapes; the 92 shapes @ recurrence>=50 cover 98.9%.

**The two-level structure (MSTR max-signal guardrail).** The 92 typed-path shapes are the motif ATOMS; they
synthesize into **~20 NAMED canonical motif FAMILIES** -- that named set IS the C2 language (coarse enough to
be a language, fine enough to distinguish). The estate currently materializes **6 debt motifs + 1 degenerate
debt-system** -- so this ~20-family canonical layer is entirely UNBUILT.

---

## The ~20 canonical motif families (grouped by plane)

### Plane A -- CLOUD / IAM / SERVE (~2,200 nodes / ~11% of mass; the operational core)
| Family | Representative typed shape(s) | recur | archetype reading |
|---|---|---|---|
| **A-STORE** | `S3Key OWNED_BY S3_BUCKET CONTAINS S3Key` | 28902 | a Store (bucket) contains + is-owned-by its keys |
| **A-ACCESS** | `LAMBDA\|EC2 READS\|WRITES S3_BUCKET CONTAINS S3Key` | 10425/6312/3050/2749 | a Transformer consumes/produces a Store (both Lambda + EC2 runners) |
| **A-TABLE** | `LAMBDA READS\|WRITES DYNAMODB_TABLE ENCRYPTS_WITH KMS_KEY` | 180/178 | Transformer <-> encrypted table Store |
| **A-GRANT** | `LAMBDA\|SERVICE_PRINCIPAL\|INSTANCE_PROFILE ASSUMES\|CAN_ASSUME IAM_ROLE HAS_POLICY IAM_POLICY` | 914/543/96 | identity resolves-through a Role that is guarded-by a Policy |
| **A-EVENT** | `EVENT_SOURCE EMITS_TO EVENT_RULE TRIGGERS LAMBDA READS\|WRITES ...` | 112/232/184 | a Trigger activates a Transformer (event/schedule-driven) |
| **A-API** | `API_GW HAS_ROUTE API_ROUTE ROUTES_TO LAMBDA READS\|WRITES ...` | 82/296/269 | a Gateway routes to a Transformer (served request) |
| **A-SERVE** | `CLOUDFRONT_DISTRIBUTION ORIGIN\|USES_OAI S3_BUCKET CONTAINS S3Key`; `DataFetch IS_ENDPOINT Endpoint READS_URL ServedURL` | 228/228/50 | a Store projected at a serve boundary (Gateway) |
| **A-WATCH** | `CW_ALARM MONITORS EC2\|LAMBDA RUNS\|READS ...` | 184/71/50 | an Observer watches a Transformer -- **the MONITORS edge (see Observer finding)** |
| **A-ORCH** | `STATE_MACHINE INVOKES LAMBDA READS DYNAMODB_TABLE` | 62 | an orchestrator triggers a Transformer |

### Plane B -- PIPELINE / DATA (~1,340 nodes / ~7%)
| Family | Representative shape | recur | archetype reading |
|---|---|---|---|
| **B-STRUCT** | `Pipeline CONTAINS PipelineScript CONTAINS PipelineFunction CALLS PipelineFunction` | 1201/1623/1078 | Container-of-code; Function triggers Function |
| **B-RUN** | `EC2_INSTANCE RUNS PipelineScript CONTAINS PipelineFunction` | 2402 | a runner executes a code Store |
| **B-IO** | `PipelineScript\|PipelineFunction READS_S3\|WRITES_S3 S3Key OWNED_BY S3_BUCKET` | 603/304/139/130 | Transformer consumes/produces an object Store (target-qualified) |
| **B-DATAFLOW** | `Field FLOWS_TO Field FLOWS_TO Field`; `Module READS_FIELD Field FLOWS_TO Field` | 212/1685 | a derives-from chain over field-grain state |

### Plane C -- REACT / FRONTEND (~11,000 nodes / ~55%; dominant by mass, homogeneous)
| Family | Representative shape | recur | archetype reading |
|---|---|---|---|
| **C-TYPE** | `Module DECLARES\|REFERENCES_TYPE TypeDecl HAS_FIELD Field` | 4269/7185 | a definition contains fields (mostly the definitional/taxonomy axis, D8) |
| **C-COMPONENT** | `JSXElement INSTANTIATES ReactComponent PROJECTS_TO\|HAS_PROP Component\|Prop` | 1298/914/442 | a component is instantiated + projects/has-parts |
| **C-RENDER** | `JSXRender RENDERS Field FLOWS_TO Field` | 1742 | a Sink (render) consumes field-state (+ dataflow) |
| **C-DRILL** | `ReactComponent\|PanelCluster CONTAINS_DRILLDOWN ReactComponent ...` | 209/130/111 | nested-component Container composition |
| **C-PAGE** | `Page CLUSTERS PanelCluster CONTAINS_DRILLDOWN\|SHARES_SOURCE ...` | 111/55 | page-layout Container |
| **C-FETCH** | `Module DECLARES DataFetch IS_ENDPOINT Endpoint`; `Hook FETCHES Endpoint` | 106/109 | a frontend Consumer fetches from a boundary |
| **C-SIBLING** | `PanelCluster SHARES_SOURCE PanelCluster ...` | 86/54 | **lateral twins -- the Variance signal as a motif** |

### Plane D -- M365 / DOCUMENT (~5,700 nodes / ~28%; a pure custody tree)
| Family | Representative shape | recur | archetype reading |
|---|---|---|---|
| **D-CUSTODY** | `MS_SITE CONTAINS MS_LIBRARY CONTAINS MS_FOLDER CONTAINS MS_FILE OWNED_BY MS_USER` | 69/844/3725/4569 | a Container hierarchy whose leaves are owned-by a Custodian -- the `owns` + `contains` families together |

**~20 named families from 92 typed shapes -- the max-signal C2 vocabulary.** Each family -> a C3
system-capability under NFRA_SYSTEM's existing C2->C3 promotion (connected components of >=2 motifs).

---

## Two open decisions the mine RESOLVED empirically

1. **Observer / Monitor role (open D-decision from the binding proof) -- now EMPIRICALLY WARRANTED.** The
   scan surfaced the `MONITORS` edge (`CW_ALARM MONITORS LAMBDA\|EC2`, ~305 edges across family A-WATCH). A
   node that OBSERVES a Transformer without being in its data-flow is real and frequent -- so **Observer is a
   12th Role** (or `MONITORS` is a first-class `guards`-subtype). My earlier lean (Guard-subtype) is now a
   coin-flip the frequency justifies promoting to a full Role. CTO rules; the evidence favors including it.
2. **`owns` / Custody -- confirmed the #1 gap.** D-CUSTODY (the entire M365 plane, ~28% of mass) is
   UNDESCRIBABLE without `owns`. The top-down flow-vocabulary had no way to say "a user owns a file" -- the
   scan makes the addition non-optional.

## For Andrew's open coverage-vs-focus call (plane mass vs value)
- **Frontend (C) + M365 (D) = ~83% of node MASS** but are structurally HOMOGENEOUS (containment/type trees,
  a few families each) -- high volume, lower per-motif operational signal.
- **Cloud/IAM (A) + Pipeline (B) = ~17% of mass** but carry the estate's OPERATIONAL semantics (access,
  grant, event, serve, run, dataflow) -- the motifs whose deviations are the debt the scorer cares about.
- **Recommendation (yours to rule):** mine ALL four planes for completeness (done above), but PRIORITIZE
  A+B for the first canonical-motif *materialization* + the C3 system-qualification -- that is where a
  populated C2/C3 layer buys the most (deviation-scoring, COMPSIMILAR, operational reasoning). C+D materialize
  next as the frontend/document capability map.

## Next
- **RAVC MSTR + CTO:** the ~20-family catalog + the Observer/owns empirical resolutions (fold into the
  closed-set ruling).
- **NEXT-C:** loop `0.4.0_DS~B` (consultant) -- is NFRA_SYSTEM's C2->C3 promotion grain-parameterizable to
  mine these ~20 canonical families (recurrence>=K, typed-path)? I feed the grain; I do NOT re-implement.
- **Andrew's steer:** the A+B-first materialization order (or a different focus).

*-- 0.8.0_AE_CloudComp~C. Canonical motif catalog, all figures comp-kuzu @2026-07-18T02:18Z (HEAD current).*
