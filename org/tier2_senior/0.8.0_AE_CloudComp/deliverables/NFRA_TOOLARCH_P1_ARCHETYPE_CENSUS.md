# NFRA_TOOLARCH P1 -- Archetype Census: dogfooding the C0-C3 ladder on the whole estate

**Author:** `0.8.0_AE_CloudComp~D` · **Date:** 2026-07-23 · **Status:** P1 deliverable (ANALYSIS, not build)
**TO:** `NFRA_TOOLARCH.P1.archetype-census` (issued `1.0.0_SA_CTO~Z` @bfad48b9b) · **Verifies:** `3.0.0_SA_CVO~Z` · **Gates:** `1.0.0_SA_CTO~Z`
**Constitution:** `docs/doctrine/INTENT_DENOMINATOR_SYNCHRONIZATION.md` (this census IS an intent-denominator instrument)
**Charter:** Andrew-direct, `NFRA_TOOLARCH_PRD.md` s.0 -- *"use the entire system as dogfood... what are the archetypes here?"*

---

## Vintage pin (a count without its vintage is not a count -- CVO~Z tick-30 corollary)

All counts below are from **one** graph read, pinned here:

| Field | Value |
|---|---|
| DB | `infra/aws/globgrph/kuzu_nessie_db` (comp-kuzu default) |
| built | **2026-07-23T14:52:37Z** (age 3.9h at read) |
| Nessie HEAD | **current** (pin == marker HEAD) |
| nodes snapshot-id | `3752421917688589142` |
| edges snapshot-id | `2676052258466818414` |
| **denominator** | **20,398 nodes / 40,796 edges** · 58 node_types · 53 edge_types |

**Method (per the constitution s.7):** INTENT is sourced from the ratified rule bank
`org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` (the governing artifact, ABOVE the graph); DENOMINATOR is
enumerated from the live comp-kuzu graph at run time; the GAP (`INTENT \ DENOMINATOR` and its inverse) is
printed per rung, per plane. The census script is reproducible: `scratchpad/archetype_census.py` parses the
YAML programmatically -- it does NOT hand-transcribe the mapping surfaces, which is how it independently
re-derives (not re-asserts) the tick-29 boundary below. Tracked copy:
`org/tier2_senior/0.8.0_AE_CloudComp/deliverables/archetype_census.py`.

## Plane taxonomy + mass (HEAD-current; freshly confirms the 2026-07-18 motif-catalog split)

| Plane | Nodes | Mass | Character |
|---|---|---|---|
| **frontend** (React) | 11,168 | **54.8%** | dominant by mass, structurally homogeneous (type/render/containment trees) |
| **M365** (document) | 5,665 | **27.8%** | a pure custody tree (site->library->folder->file owned-by user) |
| **AWS** (cloud/IAM/serve) | 2,205 | **10.8%** | the operational core -- access/grant/event/serve/watch |
| **pipeline** (data) | 1,337 | **6.6%** | code-of-container + dataflow |
| **records** (governance) | 23 | **0.1%** | *only the ontology's OWN materialized C2/C3 nodes -- see boundary R-0* |

`Field` (4,969) and `Module` (374) are genuinely cross-plane; each is assigned to its dominant
incident-neighbour plane (Field->frontend, Module->frontend) with the pipeline-participating minority noted
as a plane-axis caveat. **The plane axis is itself under-determined for shared node types** -- the tick-29
lesson (one mapping surface under-reads) applies to the plane assignment, not only the relation mapping.

---

## C0 -- ROLE census (denominator 20,398 nodes / 58 node_types)

**10 of 14 roles occur** by the fixed node-type adapter (`node_bindings`); 18,535 nodes are role-bound:

| Role | Count | Dominant plane(s) |
|---|---|---|
| Store | 10,638 | frontend 5,328 (Prop/Field-as-store) · M365 4,614 (MS_FILE) · AWS 696 |
| Sink | 3,638 | frontend (JSXRender/JSXElement) |
| Container | 1,652 | frontend 480 · M365 1,036 (folders) · pipeline 136 |
| Transformer | 1,201 | pipeline (PipelineFunction) |
| Guard | 476 | AWS (IAM_POLICY/S3_BUCKET_POLICY/SECURITY_GROUP) |
| Gateway | 258 | AWS (API_GW/API_ROUTE/Endpoint/ServedURL/CF) |
| Trigger | 246 | AWS (EVENT_RULE/EVENT_SOURCE/SCHEDULE) |
| Registry | 212 | AWS (IAM_ROLE/INSTANCE_PROFILE) |
| Consumer | 163 | frontend (DataFetch/Hook/ReactQueryKey) |
| Observer | 51 | AWS (CW_ALARM) |

**Full denominator (every node accounted -- the census fails by construction otherwise):**
- fixed-role-bound: **18,535**
- contextual (per-instance, NOT statically bound): **977** (frontend 752, AWS 210, M365 15)
- scope-out (no role BY DESIGN, D8 type axis): **807** (frontend TypeDecl)
- unbound tail (node_type with NO adapter binding -- **C0 GAP**): **79** (AWS 56, records 23)
- **CHECK: 18,535 + 977 + 807 + 79 = 20,398 == total.**

### C0 coverage boundary

- **4 roles show 0 by the static adapter -- but they are NOT absent; they are un-static-bindable.** This is
  a **methodology boundary**, grounded, not a null result:
  - **Router** -- carried by the `routes-to` composite: **82 ROUTES_TO edges from API_ROUTE**. But API_ROUTE
    is also Gateway-bound and Gateway outranks Router in `role_priority`, so Router **resolves away on its
    only live carrier** -- effectively latent. *(A real ontology finding: Router's sole carrier is
    priority-dominated; the role may be unreachable in the current estate.)*
  - **Custodian** -- **15** (MS_USER, object of custody-sense OWNED_BY in D-CUSTODY). Contextual-resolved,
    not statically bound.
  - **Source / Producer** -- **447 distinct producing sources** (LAMBDA 177, EVENT_SOURCE 95,
    PipelineFunction 80, PipelineScript 60, EC2 32, S3_BUCKET 3), edge-derived from produces-edges. Most
    also consume -> resolve to Transformer (already counted); the pure-Source residue is EVENT_SOURCE-like.
  - **Takeaway:** the fixed adapter covers **10/14 roles**; the other 4 are reachable only by per-instance
    edge derivation / composite / contextual resolution. **A static-binding census structurally cannot count
    them.** ONTOLOGY2's dynamic rails are where these get counted honestly.
- **Unbound node_type tail (79 nodes, real C0 gap):** `EC2_INSTANCE(33), IAM_USER(4), CODEBUILD_PROJECT(4),
  ROUTE53_RECORD(3), VPC_ENDPOINT(3), ECS_TASK_DEFINITION(7), ECS_CLUSTER(1), LOAD_BALANCER(1)` +
  `C2Motif(19)/C3System(4)`. EC2_INSTANCE (a runner Transformer by every motif that uses it) has **no
  node_binding entry** -- it is role-derived only via its RUNS/READS edges. The records-plane nodes are the
  ontology's own output and carry no role.

---

## C1 -- RELATION census (denominator 40,796 edges / 53 edge_types)

**Abstract relations + composites carrying live edges:**

| Mapped target | Edges |
|---|---|
| contains | 17,704 |
| owns (OWNED_BY) | 5,880 |
| consumes | 3,543 |
| triggers | 2,057 |
| produces | 1,017 |
| guards | 990 |
| derives-from (FLOWS_TO) | 961 |
| projects (SERVED_FROM + .also PROJECTS_TO/ORIGIN/USES_OAI + IS_ENDPOINT) | 586 |
| routes-to (ROUTES_TO) | 82 |
| depends-on (USES_LAYER + ENCRYPTS_WITH) | 111 |
| non-relation TYPE axis (DECLARES/REFERENCES_TYPE/HAS_TYPE) | 2,573 |
| non-relation VARIANCE (SHARES_SOURCE) / ROLE (MONITORS) | 82 |

### C1 coverage boundary -- **reconciles CVO~Z tick-29 byte-for-byte** (independent re-derivation)

> **>> DIRECTION 1 -- LIVE BUT UNMAPPED (11 edge_types / 3,912 edges = 9.6% of live edge mass):**

| Edges | edge_type | endpoints (plane) | family |
|---|---|---|---|
| 2,447 | RENDERS | JSXRender -> Field (**frontend**) | frontend render |
| 1,382 | PROP_PASSES | JSXElement -> Field (**frontend**) | frontend prop-flow |
| 40 | NOTIFIES | CW_ALARM -> SNS_TOPIC (AWS) | AWS secondary-wiring |
| 17 | GRANTS | IAM_POLICY -> SERVICE_PRINCIPAL (AWS) | AWS secondary-wiring |
| 13 | LOGS_TO | LAMBDA -> LOG_GROUP (AWS) | AWS secondary-wiring |
| 5 | DEAD_LETTERS_TO | EVENT_RULE -> SQS_QUEUE (AWS) | AWS secondary-wiring |
| 3 | SUBSCRIBES | SNS_TOPIC -> LAMBDA (AWS) | AWS secondary-wiring |
| 2 | USES_SG | LOAD_BALANCER -> SECURITY_GROUP (AWS) | AWS secondary-wiring |
| 1 | ALIAS_TO | ROUTE53_RECORD -> LOAD_BALANCER (AWS) | AWS secondary-wiring |
| 1 | IN_VPC | LAMBDA -> SECURITY_GROUP (AWS) | AWS secondary-wiring |
| 1 | USES_OAC | CLOUDFRONT_DISTRIBUTION -> S3_BUCKET (AWS) | AWS secondary-wiring |

**The unmapped mass is TWO distinct boundaries, per plane:**
- **frontend (3,829 edges = 97.9% of the unmapped mass):** the relation axis -- 10 relations sourced from the
  cloud/pipeline planes -- has **no relation for "a render consumes a field" (RENDERS) or "an element passes
  a prop" (PROP_PASSES)**. The single largest coverage gap in the ontology is the **frontend data-flow verb
  set.** This is not a tail; it is the frontend plane's core edge vocabulary sitting off every axis.
- **AWS secondary-wiring (83 edges, 9 types):** low-volume infra-wiring (notify/grant/log/DLQ/subscribe/SG/
  alias/VPC/OAC) not yet bound up. Small mass, but 9 of the 11 unmapped types -- the **long tail of AWS
  wiring** the relation axis skipped.

> **>> DIRECTION 2 -- DECLARED BUT ZERO-LIVE in the kuzu canonical plane (9 edge_types):**

`ALLOWED, AUTHENTICATES, AUTHORIZES, DENIED` (guards/denies outcomes) · `DEPENDS_ON, REQUIRES, IMPORTS`
(the depends-on concretes) · `GOVERNS` (governs relation) · `REFERENCES` (resolves-through composite).

**Two sub-families, and the fix differs by family (caveat: one-surface denominator -- kuzu canonical only):**
- **guards/auth + governs (5):** plausibly reside in the trace/CSE planes, not the kuzu canonical projection
  -> **zero-here is NOT zero-everywhere.** Likely a **plane-visibility gap** whose fix is a stated-intent
  plane annotation (which plane each `binds_up` member lives in), per the tick-25 precedent -- NOT content.
- **depends-on concretes (DEPENDS_ON/REQUIRES/IMPORTS):** the abstract `depends-on` is carried live ONLY by
  USES_LAYER (70) + ENCRYPTS_WITH (41). **The code-import dependency plane is not in this graph at all** --
  a real absent plane, not merely an unread surface.

---

## C2 -- MOTIF census (materialized C2Motif nodes vs the ~21-family canonical target)

**19 C2Motif nodes materialized = 13 canonical (tier=canonical) + 6 debt/gate.** By recurrence:

| Canonical motif | recurrence | plane | systematized (C3)? |
|---|---|---|---|
| BStructMotif | 1,623 | pipeline | yes (pipeline) |
| **AGrantMotif** | **1,553** | AWS | **NO** |
| **BDataflowMotif** | **956** | pipeline<->frontend | **NO** |
| AAccessMotif | 742 | AWS<->pipeline | yes (object-data) |
| BIoMotif | 573 | pipeline<->AWS | yes (object-data + pipeline) |
| **ATableMotif** | **358** | AWS | **NO** |
| BRunMotif | 248 | pipeline | yes (pipeline) |
| AStoreMotif | 232 | AWS | yes (object-data) |
| AEventMotif | 112 | AWS | yes (compute-orchestration) |
| **AApiMotif** | **82** | AWS | **NO** |
| AServeMotif | 59 | AWS | yes (object-data) |
| AOrchMotif | 28 | AWS | yes (compute-orchestration) |
| **AWatchMotif** | **21** | AWS | **NO** |

| Debt/gate motif | recurrence | tier | plane |
|---|---|---|---|
| RenderWithoutNullGuard | 197 | advisory | frontend |
| DeadComponent | 121 | candidate-gen | frontend |
| OrphanEndpoint | 49 | advisory | AWS-serve |
| SilentDisplayFork | 5 | gate-ready | frontend |
| HardcodedFirmLiteral | 4 | advisory | pipeline |
| CrossFirmAsymmetry | 2 | gate-ready | pipeline |

### C2 coverage boundary -- **the headline gap**

The 2026-07-18 motif catalog names **~21 canonical families across 4 planes: 9 A + 4 B + 7 C + 1 D.**

- **MATERIALIZED: all 13 A+B families** (the operational core, ~17% of node mass). This is newer than the
  catalog, which recorded the canonical layer as "entirely UNBUILT" -- the A+B-first materialization the
  catalog recommended has landed.
- **NOT MATERIALIZED: the 8 C+D canonical families** -- C-TYPE, C-COMPONENT, C-RENDER, C-DRILL, C-PAGE,
  C-FETCH, C-SIBLING (frontend) + D-CUSTODY (M365). **~83% of node mass (frontend + M365) has ZERO
  canonical-motif materialization.** The only C2 nodes touching those planes are the 4 debt motifs
  (RenderWithoutNullGuard/DeadComponent/SilentDisplayFork on a handful of ReactComponents). Coverage of the
  C2 rung is **13/21 families = 62%, and 0% of the two highest-mass planes.**
- This is the same boundary as C1 Direction-1 seen one rung up: the frontend plane is under-covered at
  BOTH the relation axis (RENDERS/PROP_PASSES unmapped) AND the motif layer (no C family materialized). **The
  frontend is the estate's largest plane and its least-described.**

---

## C3 -- SYSTEM census (union-find over connected motifs)

**4 C3System nodes; 11 of 19 motifs systematized (12 membership edges):**

| System | motifs |
|---|---|
| object-data | AStoreMotif, AAccessMotif, AServeMotif, BIoMotif |
| pipeline | BStructMotif, BRunMotif, BIoMotif |
| compute-orchestration | AEventMotif, AOrchMotif |
| EmergentSystem (degenerate) | HardcodedFirmLiteral, SilentDisplayFork, CrossFirmAsymmetry |

### C3 coverage boundary

- **8 of 19 motifs are UNSYSTEMATIZED:** `AGrantMotif(1553), BDataflowMotif(956), ATableMotif(358),
  AApiMotif(82), AWatchMotif(21)` + 3 debt (`DeadComponent, OrphanEndpoint, RenderWithoutNullGuard`).
- **The sharpest C3 gap: the two highest-recurrence canonical motifs after BStruct -- AGrantMotif (1,553)
  and BDataflowMotif (956) -- sit in NO system.** The IAM-grant archetype (the single most-recurrent
  operational motif) and the field-dataflow archetype (the derives-from backbone) are un-composed at C3. A
  union-find that omits its two heaviest motifs is under-covering exactly where operational reasoning needs
  it most.
- **No frontend or M365 C3 system exists** (consistent with C2: no C/D motif to compose). The C3 names are
  anchor-type categories (object-data / compute-orchestration / pipeline), not the aspirational
  capability-cluster names (rungs 1-3 of the c3_naming_ladder remain UNWIRED per the rule bank's own
  honesty note).

---

## Coverage boundary, stated per plane (acceptance criterion 2)

| Plane | C0 (role) | C1 (relation) | C2 (motif) | C3 (system) |
|---|---|---|---|---|
| **AWS** | covered (10 roles) + EC2/IAM_USER/etc. unbound tail (56 nodes) | secondary-wiring tail unmapped (9 types, 83 edges) | 9/9 A families materialized | 3 systems; AGrant/ATable/AApi/AWatch unsystematized |
| **pipeline** | covered (Transformer/Container) | fully mapped | 4/4 B families materialized | BStruct/BRun/BIo systematized; **BDataflow unsystematized** |
| **frontend** | covered (Store/Sink/Container/Consumer) | **RENDERS+PROP_PASSES unmapped (3,829 edges -- the #1 gap)** | **0/7 C families materialized** | **no frontend C3 system** |
| **M365** | covered (Store/Container) + **Custodian only contextual** | fully mapped (owns/contains) | **0/1 D family (D-CUSTODY) materialized** | **no M365 C3 system** |
| **records** (R-0) | **ENTIRELY ABSENT** -- the graph has NO representation of the governance/records plane (TOs, ledgers, memory, commits) except the 23 nodes the ontology materialized about ITSELF | n/a | n/a | n/a |

**R-0 is the whole-plane boundary the tick-29 edge-census could not see (it is edge-typed; an absent plane
has no edges to count).** The estate's own decision-record substrate -- the thing every agent reasons from
-- is off the graph entirely. Whether it SHOULD be modeled is a charter question for ONTOLOGY2/ARCHTOOL, not
this census; but the boundary is stated.

---

## Ranked archetype table (acceptance criterion 3 -- frequency x plane-spread -> tool demand)

Ranked for "which archetype a generalized tool would serve most," by recurrence weighted for cross-plane
spread and *un-systematized* status (an un-composed heavy motif is the strongest demand signal):

| Rank | Archetype | recurrence | plane-spread | signal to P2 / ONTOLOGY2 |
|---|---|---|---|---|
| 1 | **AGrantMotif** (identity->role->policy) | 1,553 | AWS | heaviest motif, **unsystematized** -> a generalized IAM-grant/coverage tool |
| 2 | **BStructMotif** (container-of-code) | 1,623 | pipeline | heaviest overall, systematized -> pipeline-structure tooling exists to generalize |
| 3 | **BDataflowMotif** (derives-from chain) | 956 | pipeline<->frontend | **cross-plane + unsystematized** -> a field-lineage tool spanning the pipeline/frontend seam |
| 4 | **RENDERS/PROP_PASSES** (frontend flow) | 3,829 edges | frontend | **unmapped at C1 entirely** -> the frontend needs its own relation verbs before any tool |
| 5 | **AAccessMotif / BIoMotif** (transformer<->store) | 742 / 573 | AWS<->pipeline | cross-plane, systematized -> access-pattern tooling to generalize |
| 6 | **ATableMotif** (table access) | 358 | AWS | unsystematized -> DynamoDB-access tool demand |
| 7 | **D-CUSTODY** (owns/contains tree) | ~5,700 nodes | M365 | 28% of mass, **0 motif materialized** -> a custody-tree tool for the whole document plane |

The compression the PRD predicts is already visible: **53 edge types + 58 node types reduce to ~13 recurring
operational archetypes**, and the tool-demand concentrates in **~6 of them** -- exactly the "far smaller than
the tool count" the charter expects P2 to confirm.

---

## P2 -- named as the sequenced follow-on (acceptance criterion 4; OUT OF SCOPE here)

The **PATTERN INVENTORY** (pattern -> archetype -> instantiating tools -> gaps) is **P2, blocked on ~C's
ONTOLOGY2 rails.** It needs the `(rail, grain, plane)` type system to type a pattern (a pattern is a
recurring `(archetype, question)` pair, and "question" is grained by D1/D2/D3). This census produces the
**demand side** -- the archetypes and their coverage boundary; P2 maps the estate's ~83 tools + 718 MSBEFF
findings + 187 override intents onto them. **Not attempted here.**

**Coordination (single uncovered set, per the TO):** the uncovered edge/plane set this census states
(C1 Direction-1 = 11 types/3,912 edges; C1 Direction-2 = 9 declared-zero-live; C2 = 8 unmaterialized C+D
families; C3 = 8 unsystematized motifs; R-0 = absent records plane) is the **one demand-signal set** for
`0.8.0_AE_CloudComp~C`'s ONTOLOGY2 rail authoring. ~C and this census reference this set, not two.

---

## Acceptance-criteria check

1. C0/C1/C2/C3 censused per plane, every count with denominator + vintage pinned -- **done** (vintage in header; denominators printed per rung).
2. Coverage boundary stated per plane, derived from + reconciled against tick-29 -- **done** (Direction-1/2 reproduce tick-29 byte-for-byte via independent re-derivation; per-plane table + R-0).
3. Ranked archetype table -- **done** (frequency x plane-spread x systematized-status).
4. P2 pattern inventory named as sequenced follow-on, blocked on ~C rails, not attempted -- **done.**
5. Session log + compiler-tools-log line -- pending (this session's log).

*-- `0.8.0_AE_CloudComp~D`, archetype census, all counts comp-kuzu @2026-07-23T14:52:37Z (Nessie HEAD current). Reproducible: `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/archetype_census.py`.*
