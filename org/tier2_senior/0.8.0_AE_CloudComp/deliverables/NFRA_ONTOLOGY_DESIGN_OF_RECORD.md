# NFRA_ONTOLOGY -- Universal Relational-Archetypal Ontology (Design-of-Record)

**Living design-of-record. Version 0.2 (2026-07-18).** Author: `0.8.0_AE_CloudComp~C` (build/author lane,
LD-0310). Status: **DRAFT for CTO arch-gate -- design, not code.** Supersedes the founding draft
`NFRA_ONTOLOGY_UNIVERSAL_ARCHETYPE_DESIGN_v0.1_20260718.md` (@c4f893deb). Routes: base (coordinator/FEED)
synchronous pre-CTO read of the down-map -> CTO arch-gate (closed-set + orthogonality ruling) -> COO
decomposition into TOs -> MSTR governs the doctrine. RAVC MSTR + COO as it shapes.

> **This is a LANGUAGE, not an Opal artifact.** It must read as true of a Kafka topology, a POSIX
> filesystem, a service mesh, and our AWS estate equally. Every concrete Opal/AWS name below is an EXAMPLE
> of the binding adapter (Section 9), never part of the language.

**v0.2 delta vs v0.1:** (a) the whole design is re-homed ONTO the canonical NFRA_SYSTEM **C0-C3 CSE ladder**
rather than beside it (Section 3 -- the load-bearing change); (b) base's meta-principle + 3 adapter-bound
seams + 4 load-bearing specifics (A-D) folded; (c) the C3 clause gains **read-from-file governance**
(mirroring canon-patterns' `roles:`); (d) Variance re-cast as an ORTHOGONAL comparison operator, not a
compression tier; (e) the suppression relationship is corrected -- the ontology re-homes only the
UNMODELED-EDGE subset to the adapter, and does NOT merge twin-guard vs suppression vs variance;
(f) **Role binds at the C2-MOTIF-POSITION** grain, not merely local-C1 (base refinement -- the enricher's
load-bearing grain, Section 4); (g) **C3 membership CONSUMES NFRA_SYSTEM's already-materialized C3System**
detection -- I name, I do not re-detect (a determinism WIN, Section 7); (h) the division of labor is
**MSTR-doctrine-blessed** but the NFRA_SYSTEM OPERATIONAL boundary routes through COO to loop the substrate
author `0.4.0_DS~B` before CTO (Section 2/13); MSTR guardrails baked in -- G1 keep C0-C3 orthogonal to
L1-L7, G2 record `depends_on NFRA_SYSTEM`.

---

## 1. Purpose, principles, and boundaries

**Purpose.** A substrate-neutral LANGUAGE for stating *what a node IS relationally* and *how nodes relate*,
so every consumer -- a deviation scorer, a node-summary enricher, a human reading a diagram -- describes
system structure in ONE vocabulary, independent of the platform underneath.

**The three binding principles (Andrew-direct, VERBATIM, non-negotiable -- LD-0310 / memory
project_nfra_ontology_universal_agnostic_relational_archetypal):**

> "systems ontological language should be agnostic, not opal-scoped or aws-scoped or etc, its plain english
> semantics, but designed to be relational archetypal"

1. **AGNOSTIC** -- not opal-scoped, not aws-scoped, not any-substrate-scoped. The vocabulary names
   RELATIONSHIPS (which every system has), not TYPES (which every system names differently).
2. **PLAIN-ENGLISH semantics** -- each archetype has a one-sentence human-readable definition applicable by
   someone who has never seen the schema. No typed-schema jargon in the semantics.
3. **RELATIONAL-ARCHETYPAL** -- a node's archetype is a function of its RELATIONS, never of its concrete
   type name.

**Boundary 1 -- NOT taxonomy (CTO guardrail 2).** Ontology = what a node IS relationally + how it relates.
Taxonomy (OPAL_TAXONOMY) = what a node is CALLED (its name grammar). They **compose, do not merge**: a good
name ENCODES the role and taxonomy can lint name-vs-role agreement, but re-naming a node never changes its
role and re-wiring it never changes its name. Distinct axes, distinct owners; overlap governed through COO.

**Boundary 2 -- NOT attributes.** Non-relational node attributes (encryption mode, memory size, billing
mode) are NOT ontology. The ontology is closed on the RELATIONAL axis only; attributes belong to the
adapter / taxonomy. This scope-cut is load-bearing for closure (Section 11).

---

## 2. Division of labor (proposed -- route through COO; CTO arch-gates)

The estate ALREADY has the compression MECHANISM; this project supplies the agnostic VOCABULARY. Keeping
these three distinct is what prevents a parallel-invention collision (base flagged NFRA_SYSTEM overlap as a
COO-route item -- Section 13):

| Layer | Owner | Answers | Artifacts |
|---|---|---|---|
| **Compression MECHANISM** -- the C0-C3 CSE ladder + promotion + materialization | NFRA_SYSTEM / SEMCTL (COO lane) | *HOW* facts compress up to systems | `cse_schema.py`, `comp_ladder.py`, NFRA_MOTIF P1/P2, `infra/system/01_substrate.md` |
| **Archetype VOCABULARY** -- substrate-agnostic terms + plain-English semantics + assignment rules | **NFRA_ONTOLOGY (this doc, ~C)** | *WHAT* the things at each tier ARE, agnostically | this design -> the ontology rule bank (Section 14 next-step) |
| **Binding ADAPTER** -- concrete AWS types -> archetype vocabulary | CTO (owns `canon-patterns.yaml`) | *WHICH* archetype a concrete AWS thing binds to | `canon-patterns.yaml` demoted to the adapter |

**NFRA_ONTOLOGY provides the vocabulary that the C0-C3 ladder classifies INTO; canon-patterns binds AWS
types onto it; the ladder (comp_ladder.py) does the compression.**

**DOCTRINE-BLESSED (MSTR, 035139Z); the OPERATIONAL boundary still needs the substrate author's concurrence
(base, 035016Z).** MSTR source-confirmed and blessed this division at the DOCTRINE level (SEMCTL=mechanism /
NFRA_ONTOLOGY=vocabulary / canon-patterns=adapter) -- and noted the charter phrase *"the C3-level LANGUAGE"*
was speaking the estate's canonical C0-C3 algebra all along, so this is recognizing what the charter meant,
not a new design choice. What is NOT yet settled is the OPERATIONAL boundary, because the estate already has
**TWO motif notions**: NFRA_SYSTEM's **EMERGENT** motifs (mined, recurrence>=2, materialized as
C2Motif/C3System nodes in the `semctl` layer) AND canon-patterns' **CURATED** 4 CTO-authored classes. The
only non-colliding design is: **NFRA_ONTOLOGY = the NAMING/vocabulary layer that BOTH classify INTO** --
NFRA_SYSTEM stays the DETECTION mechanism (**I do NOT re-implement promotion/detection**), canon-patterns
maps AWS types up, and my archetypes name what both produce. If the vocabulary reads as a PARALLEL taxonomy
(a second motif/system definition), that is a real collision. Two operational consequences: (a) if
archetypes ever MATERIALIZE as graph nodes they must conform to / extend `cse_schema.py`'s SoD-governed,
source-enforced enum (LAW 1/2 fail-closed) -- a change touching NFRA_SYSTEM; (b) the FRACTAL/agnostic
ambition is CONSONANT with NFRA_SYSTEM (already "substrate-agnostic, recurses across scopes via the reusable
recognizer keystone", `NFRA_SEMCTL_PRD:52`) ONLY IF I build ON that keystone, not a parallel one.
**OWNERSHIP (Andrew-direct correction, relayed base 040610Z, VERBATIM):** *"this work is squarely 0.8.0
stuff... I can bring on 0.4.0_DS~B... as a consultant of sorts."* So the NFRA_ONTOLOGY<->CSE reconciliation
is **0.8.0-OWNED, in-house -- NOT a cross-project handoff and NOT a COO-gated seam.** `0.4.0_DS~B` is a
CONSULTANT I can pull in for `cse_schema.py` ground-truth, nothing more. The elemental de-fogging of this
space is being rendered by peer `0.8.0_AE~A`; I coordinate with ~A so Andrew gets ONE picture (Section 3a is
my answer to Andrew's reconcile Qs). **The only COO touch is a RECORDS update (MSTR G2): NFRA_ONTOLOGY
`depends_on` NFRA_SYSTEM/SEMCTL -- flag it for the `org/projects/NFRA_ONTOLOGY.json` edit (COO's non-gated
lane); it is not a gate.**

---

## 3. THE CORE FRAME -- the ontology populates the canonical C0-C3 CSE ladder

`infra/system/01_substrate.md` (authority: `comp_ladder.py:208`) ratifies a **C0-C3 semantic-compression
algebra** -- SUCCESSIVE SEMANTIC COMPRESSION, "up: fact -> interaction -> motif -> system":

| Tier | Canonical meaning | Deterministic promotion | Ontology supplies (this project) |
|---|---|---|---|
| **C0 FACTS** | individual objects/nodes (a function, table, bucket, endpoint), grounded in lexical evidence | -- (the ground; LAW 1 lexical-certainty) | **ROLE archetypes** -- what a fact IS relationally (a 1-node label DERIVED from its C1 edges). Section 4. |
| **C1 INTERACTIONS** | relationships/edges (calls/reads/writes/contains) | -- (the ground) | **RELATIONSHIP archetypes** -- what an edge IS. Section 5. |
| **C2 MOTIFS** | recurring shapes | recurrence **>= 2** (`NFRA_MOTIF_P1:AC3_THRESHOLD`) | **LINEAGE archetypes** -- what a motif IS, as a composition of Roles joined by Relationships. Section 6. |
| **C3 SYSTEMS** | business capabilities | a connected component of **>= 2 motifs** (union-find over shared constituents; `NFRA_MOTIF_P2_c3_emergence.py:111`) | **SYSTEM archetypes** -- what a system IS, in plain-English capability terms (the "member of <system>" clause). Section 7. |

**Two ontology constructs are NOT compression tiers:**
- **VARIANCE** is an ORTHOGONAL COMPARISON OPERATOR (Section 8): it classifies how instances of the same
  C0-fact or C2-motif relate to EACH OTHER (Twin / Fork-Shadow / ...). It applies ACROSS the ladder, so it
  is not a tier -- it is a cross-cutting classifier. This is where firm-twin/fork-shadow generalizes.
- **The adapter** (Section 9) is a binding, not a tier.

**Orthogonality to the OTHER two "layer" schemes (01_substrate.md is explicit -- do NOT conflate):**
- **C0-C3** = the SEMANTIC-COMPRESSION axis ("how abstract is this unit"). **NFRA_ONTOLOGY lives here.**
- **L1-L7 (NFRA_GLOBGRPH)** = the estate STACK axis (Portal/Network/Compute/Storage/Pipeline/IAM/External;
  40 node classes / 14 edge families, closed vocab). Every node has BOTH a C-coordinate and an L-coordinate
  (an S3 bucket is L4 AND a C0 object). **Orthogonal to us.**
- **`NODE_TYPE_LAYER`** (aws/ms/portal/semctl) = a per-node DOMAIN tag. `semctl` is where the materialized
  C2Motif/C3System nodes live. **Orthogonal to us.**

**Why this frame is right:** Andrew's charter trigger was literally *"do we have a C3 ontology bank that
deterministically explains these relationships?"* -- and NFRA_SYSTEM already DEFINES C3. The ontology is the
agnostic archetype vocabulary FOR that existing ladder, with canon-patterns as the AWS binding. Building it
beside the ladder (a parallel scheme) would be the map-vs-territory drift CTO's guardrails exist to prevent.

## 3a. Reconciliation with the CSE algebra (answer to Andrew's reconcile question)

Andrew is reconciling NFRA_ONTOLOGY against NFRA_SYSTEM's CSE schema -- they "say the same thing about C0-C3"
with a "nested versions" idea to pin. **Source-grounded on `org/modules/graph/cse_schema.py` (Entity :56-88,
Relationship :92-117):** CSE's schema is ALREADY two-tiered but FLATTENED into one enum, and the source
LABELS the two tiers --
- `Entity`: **`# org-level`** (Artifact/Component/Concept/Requirement/Constraint/Service/Policy -- ABSTRACT)
  + **`# code/infra-level (concrete)`** (Function/Module/Endpoint/Table/Lambda/S3Bucket/IAMRole/IAMStatement/
  Schedule/SecretRef/Field/ReactComponent/JSXElement/Hook).
- `Relationship`: abstract (contains/references/depends_on/produces/consumes/implements/governs/derives_from/
  supersedes) + **`# code/infra (CloudEdge discriminators)`** (calls/imports/reads/writes/renders/flows_to/
  fetches/served_from/triggers/denied/allowed/requires/authenticates/authorizes).

**So the vocabularies overlap because it IS the same vocabulary.** `produces/consumes/derives_from/supersedes/
triggers/governs` are literally in CSE. The verdict (to Andrew's three options):

**NFRA_ONTOLOGY is a REFINEMENT nested in CSE -- the LAYERED REFACTOR of CSE's own vocabulary + one new
orthogonal axis. NOT a duplicate to unify away (I adopt CSE's abstract relations verbatim -- no competing
enum), NOT orthogonal-and-coincidental.** It adds exactly three things, none a duplicate:
1. **The layer separation the charter demands.** CSE flattens Service+Lambda, produces+reads into one enum --
   so its Entity enum literally contains `LAMBDA`/`S3BUCKET` and FAILS the strict agnostic test. NFRA_ONTOLOGY
   ELEVATES CSE's `org-level` terms into the pure agnostic layer and DEMOTES its `code/infra` terms into the
   binding adapter (= canon-patterns). This refactor IS the agnostic principle (CTO gate criterion 2).
2. **The ROLE axis -- genuinely new + orthogonal.** CSE types a node by its entity-KIND (Service/Lambda/
   Function); it has NO relational-role classification. Roles (Store/Producer/Guard/...) are DERIVED from a
   node's C1 edges; a node carries BOTH a CSE entity-type AND an NFRA role (a Lambda that is a Guard).
3. **The VARIANCE calculus** generalizing CSE's flat `supersedes` into Twin/Fork-Shadow/Variant/Superseded/
   Orphan.

**"Nested versions" (Andrew's phrase) = ONE agnostic vocabulary nested THREE consistent ways:** (i) the
ABSTRACT-OVER-CONCRETE GRAIN nesting CSE's own enum already shows (`produces` [abstract] over `reads/writes/
fetches/served_from` [its concrete CloudEdge versions] -- the adapter formalizes "reads binds up to
consumes"); (ii) the COMPRESSION/ARITY nesting in the ladder (a C2 motif contains C0 nodes + C1 edges; a C3
system contains C2 motifs); (iii) the SCOPE-FRACTAL (the ladder reapplies code -> org -> any artifact class).
The charter's "describes any system" IS the scope-fractal; the archetype layering IS the grain-nesting; the
C0-C3 tiers ARE the compression-nesting.

**Consequence for closure (Section 11):** the guardrail-1 proof must now bind cleanly against CSE's 26
entities + 24 relationships (not only canon-patterns' 23+16) -- the binding-completeness table
(`NFRA_ONTOLOGY_BINDING_COMPLETENESS.md`) does exactly that, and it HONESTLY surfaces the additions the
binding forces (e.g. `contains` composition; the `depends_on`/`derives_from`/`implements` reconciliation;
non-flow entities Person/Org/Concept/Type/Symbol) rather than bucketing them into a catch-all.

---

## 4. C0 vocabulary -- ROLE archetypes (the 1-node closed set)

A Role is a plain-English label for what a C0 FACT IS in the flow, never from its concrete type. A concrete
type may be polymorphic (a Lambda is a Transformer, Guard, Router, or Trigger depending on its edges -- the
adapter decides, Section 9).

**Role binds at TWO grains (base refinement, 035016Z -- the load-bearing precision):**
- **Coarse (the archetype, this section):** the C0 label from the node's local C1 edge-neighborhood
  (`S3_BUCKET` is object-of-produces/consumes -> **Store**). This is the closed 11-set below.
- **Fine (the motif-position, C2):** the RICH role is the node's structural POSITION WITHIN a matched C2
  Lineage -- "S3 tail of SERVED_LINEAGE", "code-runner store". canon-patterns' `roles:` are motif-positions,
  not raw edge-labels; the role binds AT the C2-position (transitively C1-derived, since motifs are built
  from C1). **The enricher (Section 12) consumes the FINE grain** -- so the ontology emits both, and the
  motif-position role reads from the governed catalog exactly like the C3 membership does.

Proposed closed set (**11 roles**; CTO blesses/adjusts) -- **revised to 12 by the binding proof (+Container:
Module/GraphScope/Tier), see `NFRA_ONTOLOGY_BINDING_COMPLETENESS.md`:**

| Role | Plain-English | Structural signature (how it is DERIVED from C1) |
|---|---|---|
| **Source** | Originates data/signal from OUTSIDE the system's control. | no within-system inbound; outbound `produces`. (vendor feed, user, sensor) |
| **Store** | Holds state others read/write; transforms nothing itself. | object of `produces`/`consumes`; no outbound `derives-from`. (bucket, table, topic, file) |
| **Producer** | Writes state it did NOT derive from a within-system input. | outbound `produces`; no inbound derive-dependency. (a raw ingester) |
| **Transformer** | Reads input, DERIVES new output, writes it -- the work-doer. | inbound `consumes`/`derives-from` AND outbound `produces`. (a gold script, a stream processor) |
| **Consumer** | Reads state and acts on it; forwards or terminates. | inbound `consumes`. |
| **Sink** | Terminal consumer -- the flow ENDS here. | inbound `consumes`; no outbound. (a render, a dashboard, an archive, a human) |
| **Gateway** | The single controlled entry/exit point between a zone and outside. | sole carrier of `projects`/boundary edges for a zone. (API edge, CDN edge, mount) |
| **Guard** | A node a flow MUST PASS, which may permit or deny it. | interposed on a `consumes`/`routes-to` path; carries `guards` (+ maybe `denies`). (authorizer, validator, policy) |
| **Router** | Directs a flow to ONE OF SEVERAL destinations by a rule. | one inbound, multiple outbound `routes-to` by predicate. (edge router, load balancer, dispatch catalog) |
| **Trigger** | Activates another node on an event/schedule -- carries the GO, not the payload. | outbound `triggers`; control, not data. (schedule rule, event source, cron) |
| **Registry** | The authoritative catalog/index; others resolve identity/location THROUGH it. | object of `resolves-through`. (service registry, catalog table, DNS zone, Nessie ref-store) |

**Design notes for the gate:**
- **Store vs Registry:** a Registry is resolved-THROUGH for identity/location; a Store is read/written for
  payload. (`FP_NESSIE_INTERNAL_DDB` catalog tables are Registries, not data Stores.)
- **Producer vs Transformer:** discriminator = is the output DERIVED from a within-system input. A raw
  ingester is a Producer; a silver->gold script is a Transformer. (Adapter: bronze-writer=Producer,
  silver/gold=Transformer -- but the HARD Opal layer-invariants stay adapter-bound, Section 9/specific C.)
- **Roles are not mutually exclusive per node** (an auth-edge is a Gateway that is also a Guard); only the
  SET is closed.
- **Open (CTO):** is **Observer/Monitor** an 12th Role (a CW alarm / freshness guard OBSERVES without being
  in the flow -- `FP_CW_ALARM_IMPLICIT_MONITOR`), or a Guard-subtype that reports rather than denies? I lean
  Guard-subtype to hold the set at 11. **Ruling requested.**

---

## 5. C1 vocabulary -- RELATIONSHIP archetypes (the 2-node closed set)

A Relationship is a plain-English, DIRECTED edge label. Proposed closed set (**8**; CTO blesses/adjusts) --
**revised to 11 by the binding proof (+`depends-on`, +`contains`, +`derives-from` promoted first-class), see
`NFRA_ONTOLOGY_BINDING_COMPLETENESS.md`:**

| Relationship (A -rel-> B) | Plain-English | Notes |
|---|---|---|
| **produces** | A writes/creates state into B. | the write edge. |
| **consumes** | A reads/depends on state from B. | the read edge. `derives-from` = a consumes whose OUTPUT depends on the input; kept a SUBTYPE, not a 9th primitive, to hold the set closed (CTO may split it). |
| **triggers** | A activates B on an event/schedule -- control, not payload. | no state crosses (distinct from produces). |
| **guards** | A gates B: a flow to B must clear A. | the interposition edge. |
| **denies** | A PROHIBITS a relationship to/from B. | the NEGATIVE relationship. **An ontology must state prohibition, not only permission** -- the cross-firm Deny (`FP_CROSS_FIRM_DENY_GUARDRAIL`, 198 instances) is a `denies`, a security CONTROL; reading it as a "missing permission" is the most common adapter misread (specific A). |
| **routes-to** | A conditionally forwards a flow to B (one of several). | carries the predicate. |
| **projects** | A exposes an internal thing B at an external surface (serves/publishes). | the boundary-crossing / "served" edge. |
| **resolves-through** | A looks up identity/location of a target via B (a Registry). | the indirection edge. |

**Orthogonality correction (vs MSTR's starter set):** `supersedes` and `mirrors` were listed under
RELATIONSHIP, but they relate two instances of the SAME role -- they are VARIANCE facts, not C1 edges, and
belong on the comparison axis (Section 8). Placing them here would let one fact live on two axes (breaks
orthogonality). Moved.

---

## 6. C2 vocabulary -- LINEAGE archetypes (a GRAMMAR over Role + Relationship)

A Lineage is a C2 MOTIF (recurring shape, recurrence >= 2) expressed with ZERO new vocabulary as a canonical
composition of Role-nodes joined by Relationship-edges -- the agnostic generalization of canon-patterns'
4 pattern-classes:

| Lineage | Canonical composition | canon-patterns source |
|---|---|---|
| **Pipeline** | `Source -produces-> (Transformer -produces-> Store)* -consumes-> Sink` -- a staged derivation chain. | PIPELINE_CANON (bronze->silver->gold->served->render) |
| **Guarded-Access** | `Consumer -consumes-> Guard -guards-> Store` -- a flow that must clear a gate before it reaches state. | AUTH_CANON (route -> auth-edge -> S3) |
| **Provision** | `Producer -produces-> Store(artifact) <-consumes- Transformer/Runner` -- an artifact published, then loaded by a runtime. | DEPLOY_CANON (repo -> S3 code/ -> runner) |
| **Served-Projection** | `Store -projects-> Gateway -consumes-> ... -consumes-> Sink` -- internal thing surfaced at a boundary and rendered. | SERVED_LINEAGE_CANON (gold field -> ServedURL -> fetch -> render) |

**The axis's whole content (the general rule):** anyone can DEFINE a new Lineage as an ordered composition
of Roles and Relationships, WITHOUT extending the primitive vocabulary (a Kafka stream-join is just
`Source -produces-> Store(topic) <-consumes- Transformer(join) -produces-> Store(topic)`). Because Lineage
adds no primitives, it needs no ratification beyond the seed shapes -- the seed set is illustrative, not
closed. **Motif recurrence >= 2 (the C2 promotion threshold) is inherited from NFRA_SYSTEM, not
re-invented.**

**Deviation = a live path whose role/relationship composition diverges from its declared Lineage** (the
scorer's consumption, Section 12). canon-patterns' `deviation_classes` (layer_skip, orphan_stage,
dual_writer, missing_auth_edge, silent_rewrite_noop) all generalize to this.

**Adapter-bound seam (base's meta-principle, specific-3):** a Lineage archetype SPANS graphs -- our estate
keeps the pipeline interior (bronze->gold) in `comp-pipescript`, not as typed CloudNodes. The archetype must
span BOTH the canonical DB and pipescript; the graph-split is an adapter/measurement fact, never an
archetype limit.

---

## 7. C3 vocabulary -- SYSTEM archetypes + the governed membership catalog

A System is a C3 unit = a connected component of >= 2 motifs (NFRA_SYSTEM's `c3_emergence` threshold), named
in plain-English CAPABILITY terms. This IS the "member of <system>" clause COMPSIMILAR's C3 enrichment was
HELD waiting for.

**The WIN (base, 035016Z): the C3 membership has a canonical DETERMINISTIC SOURCE already.** NFRA_SYSTEM
already DETECTS + MATERIALIZES C3System nodes (union-find over shared motif constituents,
`NFRA_MOTIF_P2_c3_emergence.py:111`, no ML, fidelity-gated). **NFRA_ONTOLOGY does NOT re-detect systems -- it
CONSUMES NFRA_SYSTEM's C3System membership and NAMES it** from the governed catalog. So the HELD C3 clause
satisfies Andrew's determinism requirement NATIVELY, with zero new detection mechanism -- the enricher reads
`node -> its materialized C3System -> the catalogued plain-English name`.

**Governance (base's C3 contract -- load-bearing).** The system-membership label vocabulary is a **fixed,
read-from-FILE catalog**, exactly like `canon-patterns.yaml`'s `roles:` field governs C2. The enricher reads
the label set FROM the file (not a hardcoded list), so blessing a system label == editing the governed
catalog. This keeps C3 as deterministic + governed as C2. Per node/ARN the layer emits `"member of
<system>"` ONLY when the node's C2 motifs resolve into a catalogued C3 system; absent -> no clause (no
guess).

**Determinism:** the C0->C3 promotion is structural (union-find over shared motif constituents) with a fixed
threshold -- no inference (LAW 2: explicit-promotion). The system NAME comes from the governed catalog, not
from clustering-and-naming.

---

## 8. VARIANCE -- the orthogonal comparison operator (Twin / Fork-Shadow / ...)

The richest construct, and the one that UNBLOCKS COMPSIMILAR's Twin/Fork-Shadow labels. Variance classifies
how MULTIPLE instances of the same C0-fact or C2-motif relate to EACH OTHER. It is NOT a compression tier --
it applies across the ladder. Proposed set (**6**):

| Variance | Plain-English | Discriminator |
|---|---|---|
| **Canonical** | The reference instance all others are measured against. | designated, or the modal/dominant shape. |
| **Twin** | A DESIGNED parallel instance, structurally symmetric to canonical. **NOT debt.** | matches on the IDENTITY key AND a SIBLING SET exists across all values of a DECLARED variance dimension. |
| **Variant** | A legitimate FACET-difference (per-env, per-service, per-tenant). | differs ONLY along a declared dimension. |
| **Fork-Shadow** | Diverged from its twin/canonical WITHOUT a declared reason. **Advisory debt-CANDIDATE** (v2, CTO 013249Z + CVO cot adjudication): confirmed debt ONLY on a GROUNDED dimension (allowed_facets populated+cited); under `[]`+advisory a CANDIDATE pending adjudication -- can ground to debt / coverage-gap / designed-difference (cot = live NON-debt proof @1fe0f5e6f). | matches identity key but differs OFF every declared dimension (asymmetric + undeclared). |
| **Superseded** | Replaced by a newer instance but still present. | a newer instance `supersedes` it; both live. |
| **Orphan** | No canonical/twin/consumer relationship at all -- disconnected. | no variance peer AND no live consumer. |

**The load-bearing generalization (base specific-B -- elevates canon-patterns' `twin_shadow_guard`).**
canon-patterns HARD-CODES the twin dimension: "key motif-identity on `(firm, layer, logical-stage)`." The
universal layer generalizes **"firm" as a VARIANT-AXIS PARAMETER** -- a system DECLARES its variance
dimensions (firm, environment, region, tenant, service, ...). Then, keying identity on
`(variant-axis-value, layer, logical-stage)`:
- **Symmetry test:** does a SIBLING SET exist across ALL values of the declared dimension at the same
  (layer, stage)? Yes -> **Twin/Variant** (canon). One value special-cased -> **Fork-Shadow** (advisory
  debt-CANDIDATE under `[]`+advisory; confirmed debt only when the dimension is grounded -- v2, CTO 013249Z).
- **Polarity is load-bearing (base specific-B):** the guard **CLEARS** designed parallels (they are canon);
  it does **NOT** flag them. Only asymmetric+undeclared divergence is debt.

This is substrate-agnostic AND it unifies three suppression families as ONE calculus with different declared
dimensions: `DUP_BENIGN_CROSS_FIRM` = Twin on `firm`; `DUP_BENIGN_ENV_TWIN` = Variant on `env`;
`DUP_BENIGN_SERVICE_SPLIT` = Variant on `service`. (Orphan example: the CVO-confirmed real orphan
`opal-data-aaii-v2` that suppression had to UNMASK.)

**HARD adapter invariant (base specific-A -- must not dilute up):** for the `firm` dimension, firms are
BUSINESS-SEPARATED and **NEVER interchangeable/mergeable** -- cross-firm reference is IAM-denied +
gate-blocked (a CLAUDE.md NEVER-rule). The Twin archetype says "designed-parallel = canonical"; it must NOT
imply firms are fungible. The never-cross constraint lives HARD in the adapter (via the first-class `denies`
relationship), not as a soft ontology pattern.

**Determinism:** symmetric-vs-asymmetric over a declared dimension set is a pure structural comparison -- no
inference. This is exactly the deterministic Twin/Fork-Shadow verdict the COMPSIMILAR C3 clause was HELD for.

---

## 9. The binding adapter (canon-patterns.yaml demoted)

`canon-patterns.yaml` (CTO v0.1) becomes the **AWS-BINDING ADAPTER**: a table mapping concrete AWS
types/edges onto the archetype vocabulary. Two kinds of mapping:

1. **Direct** (`type -> role`): `S3_BUCKET -> Store`; `DYNAMODB_TABLE -> Store` (or Registry if a catalog);
   `SECRET -> Store`; `EVENT_RULE/EVENT_SOURCE -> Trigger`; `API_GW / ServedURL -> Gateway`;
   `IAM_POLICY(Deny) -> a denies edge`; `Field(gold) -> Store(field-grain)`; `JSXRender -> Sink`.
2. **Contextual** (`type + edge-pattern -> role`): `LAMBDA` is polymorphic -- an inbound `TRIGGERS` from an
   `API_ROUTE` + edge-fn -> **Guard/Router**; reading one data Store + writing another -> **Transformer**;
   schedule-only -> **Trigger**. This is canon-patterns' existing "role = structural position", elevated:
   **the role is a function of the C1 edge-neighborhood, decided by the adapter.**

**Edge mapping** (`edge_type -> relationship`): `WRITES/EMITS_TO -> produces`; `READS/READS_FIELD/FETCHES ->
consumes`; `FLOWS_TO -> derives-from` (carries KIND passthrough/rename/recompute); `TRIGGERS -> triggers`;
`SERVED_FROM/IS_ENDPOINT/PROJECTS_TO -> projects`; an IAM `Deny` statement -> `denies`;
`ASSUMES/CAN_ASSUME/READS_SECRET/HAS_POLICY/HAS_KEY -> resolves-through | guards` per role.

**The invisible-edge principle (base's META-PRINCIPLE -- a design pillar).** The ontology describes the
system's ACTUAL relational behavior. **A relationship the substrate/graph does not emit as an edge is an
ADAPTER COVERAGE-GAP, not an absence of the relationship.** The three canon-patterns "seams" stay in the
adapter, NEVER encoded as archetype limits:
1. **AUTH TRIGGERS-unmodeled** -- the Guard archetype is REAL; our canonical graph just lacks the TRIGGERS
   edge, so the adapter sources the role from `comp-routes` BEHAVIOR. The universal Guard is NOT
   "structurally underivable."
2. **DEPLOY bucket-grain** -- the code-runner archetype is real; our canonical DB is bucket-grain, so full
   role fidelity comes from the deploy-ledger/pipescript. Grain is estate-topology, not an archetype limit.
3. **PIPELINE interior in pipescript** -- covered in Section 6 (span both graphs).

Roughly 60% of `suppression_v1.yaml`'s 90 FP-classes are exactly this unmodeled-edge class
(`FP_LOG_GROUP_IMPLICIT_LOGS`, `FP_SECRET_RUNTIME_ACCESS`, `FP_API_LAMBDA`, `FP_LEDGE`, `FP_ECS_TRIGGER`,
`FP_EC2_SSM_INVOKED`, `FP_CW_ALARM_IMPLICIT_MONITOR`) -- under this ontology they are named gaps in ONE
adapter's edge coverage, not a hand-maintained FP list. **(Correction vs v0.1:** the ontology re-homes ONLY
this unmodeled-edge subset to the adapter. It does NOT merge the three distinct mechanisms base named in
specific-D: `twin_shadow_guard` = a CANON fact cleared by the Variance calculus (Section 8); `suppression`
= an adjudicated FP cleared by the suppression gate; the coverage-gap subset = an adapter edge-coverage
issue. Three mechanisms, kept distinct.)

**Opal layer-invariants stay adapter-bound (base specific-C).** The universal Pipeline lineage has generic
`raw -> refined -> served` stages, but the HARD CLAUDE.md rules -- bronze=RAW/immutable (17a),
silver=dedup+dtype-only/no-judgment (17), gold=business-logic, platinum=served -- are law bound to the AWS
LAYER NAMES in the adapter. They do NOT dilute into the universal layer.

---

## 10. Determinism, the CSE laws, and the coverage denominator

- **Every archetype assignment is structure-derived** -- Role from C1 edges, Relationship from the edge,
  Lineage from a motif match, System from motif-connectivity, Variance from an instance comparison. No LLM,
  no inference. Aligns with **LAW 1 (lexical-certainty-before-inference)** and **LAW 2 (explicit-promotion)**
  (`01_substrate.md`).
- **No match -> no label.** Absence is never filled (a node with no matching Role/Lineage/System/peer gets
  no clause). Mirrors COMPSIMILAR's graceful-degradation (no label -> no clause -> zero enricher rework).
- **Print the denominator.** Every classification pass reports coverage: `"N of M facts assigned a Role; K
  unclassified"`. A silent 100% is a red flag (it hides adapter coverage-gaps), not a success.

---

## 11. Closure + orthogonality (answering CTO guardrail 1)

The C0-C3 ladder is the CLOSED compression axis -- **4 tiers with deterministic, already-ratified
promotion thresholds** (recurrence>=2; connected-component>=2). The ontology supplies the closed archetype
vocabulary at each tier, plus one orthogonal operator:

- Every RELATIONAL fact is a **C0 object (a Role)**, a **C1 edge (a Relationship)**, a **C2 motif (a
  Lineage)**, a **C3 system (a System)**, or a **Variance comparison**. There is no fifth structural kind --
  the compression ladder has exactly four tiers and Variance is the single cross-tier operator.
- The two DERIVED tiers add ZERO primitives: Lineage is a GRAMMAR over Role+Relationship; System is EMERGENT
  from motif-connectivity (+ a governed naming catalog). **So the closed sets to RATIFY are: the Role set +
  the Relationship set + Variance (6) + the read-from-file C3 system-naming catalog (governed, open-per-
  system). Lineage needs no ratification (compositional).**
- **The binding-completeness proof (`NFRA_ONTOLOGY_BINDING_COMPLETENESS.md`) REVISES the primitive sets** by
  binding the full CSE + canon-patterns concrete-type universe (28 entities + 24 relationships) with ZERO
  catch-all: **Roles -> 12** (Sections 4's 11 + **Container**, forced by Module/GraphScope/Tier); **
  Relationships -> 11** (Section 5's 8 + `derives-from` promoted first-class + `depends-on` + `contains`).
  The proof caught the `contains`/Container gap and surfaced **8 bounded decisions (D1-D8) = the arch-gate
  agenda** -- each a named fork, never a catch-all.
- **No catch-all leak:** a concept that seems to need a new term is (a) a missed Role/Relationship, (b) a
  Lineage composition, (c) a System, or (d) a Variance comparison. No "misc" bucket, because there is no
  fifth arity. Non-relational attributes are OUT by the Boundary-2 scope-cut.

**Proof obligation I owe CTO (NEXT-1):** a binding-completeness table showing the Role+Relationship set binds
EVERY concrete type without a leak -- against canon-patterns' 23 node-types + 16 edge-types, and (open,
Section 13) NFRA_GLOBGRPH's fuller L1-L7 vocabulary (40 node classes / 14 edge families).

---

## 12. Consumer contracts (design FOR the consumers)

**(A) Canon-deviation scorer.** Consumes the Lineage archetypes (Section 6) + the Variance calculus
(Section 8). A deviation = a live path whose role/relationship composition diverges from its declared
Lineage, OR an instance that is a Fork-Shadow/Orphan. The scorer's `motif_outlier_semantics` becomes:
Canonical = the dominant shape; outliers = Fork-Shadow candidates; `twin_shadow_guard` = the Variance
calculus. Net: ONE universal frame instead of 4 hard-coded pattern-classes.

**(B) COMPSIMILAR node-summary C3-enrichment (the HELD clause -- my output unblocks ~D).** Per node/ARN,
deterministically, from a read-from-FILE governed catalog (Section 7):
- **Role** (C0 label) -- context adjacent to ~D's C2 motif+role clause.
- **System membership** (C3) -- `"member of <system>"`, substrate-neutral, NOT raw canon-patterns.
- **Variance verdict** -- `"canonical firm-twin of X"` / `"divergent fork-shadow (candidate -- advisory, pending adjudication)"` (advisory dim; grounded -> "(debt)") from the
  declared-dimension symmetry test.

Contract shape I will hand ~D at gate-pass (base FEEDS the walkthrough): a pure function `node -> {role,
system_membership?, variance_verdict?}` reading only the node's C1 neighborhood + declared variance
dimensions + the governed catalog -- no inference, coverage-denominatored, absent->no clause. The enricher
lights up with zero rework (graceful-degradation already shipped).

---

## 13. Open questions for CTO + coordination seams for COO

**CTO arch-gate rulings requested:**
1. **Role set size:** 11, or add Observer/Monitor as a 12th (vs. my Guard-subtype proposal)? (Section 4.)
2. **Relationship set:** 8; is `derives-from` a `consumes`-subtype (my proposal) or a distinct 9th? Bless
   `denies` as first-class (I argue yes)?
3. **supersedes/mirrors moved to Variance** -- bless the orthogonality correction? (Section 5.)
4. **Adapter authority:** does `canon-patterns.yaml` LITERALLY become the adapter (re-headed to a
   type->archetype table), or a NEW adapter file beside it? (CTO-owned-file question.)
5. **Binding target for closure:** canon-patterns' 23+16 only, or the fuller NFRA_GLOBGRPH L1-L7 (40 node
   classes / 14 edge families)? The latter is the more complete "bind every concrete type" target.

**NFRA_SYSTEM reconciliation -- 0.8.0-IN-HOUSE (Andrew-direct, NOT a COO gate).** Andrew ruled this work
"squarely 0.8.0 stuff" (Section 2); the CSE reconciliation is owned here. Three OPERATIONAL points I resolve
in-house (consulting `0.4.0_DS~B` for `cse_schema.py` ground-truth as needed; coordinating with peer `~A`'s
elemental rendering): **(1)** two motif notions coexist (NFRA_SYSTEM emergent vs canon-patterns curated) --
my vocabulary is the NAMING layer BOTH classify into, NOT a parallel detector (I do not re-implement
promotion); **(2)** if archetypes ever materialize as graph nodes they must extend `cse_schema.py`'s
SoD-governed enum -- a change I would route to the schema owner then; **(3)** build ON NFRA_SYSTEM's reusable
recognizer keystone (FRACTAL), not a parallel one. Section 3a is the reconciliation.

**COO touches (records + adjacent lanes only -- no gate on the design):**
- **Record the dependency (MSTR G2):** `org/projects/NFRA_ONTOLOGY.json` `depends_on` should add
  **NFRA_SYSTEM** (currently `[NFRA_COMPSIMILAR, NFRA_GLOBGRPH]`) -- COO's non-gated `org/projects` lane.
- **Keep C0-C3 orthogonal to L1-L7 (MSTR G1):** the archetype vocabulary is the C0-C3 axis ONLY; it must not
  absorb or collide with the NFRA_GLOBGRPH L1-L7 stack axis (every node has BOTH coordinates). Baked into
  Sections 3 + 11.
- **OPAL_TAXONOMY overlap** (naming axis) -- COO holds the overlap map; dedupe through COO.
- **Census + stale-TO reconcile (in-flight):** the census "measurement authority" handoff to ~B + my stale
  PASSCRAFT/TOOLGRAPH/COMPLEARN TOs are MSTR-routed to COO (both ACKed) -- noted here for COO's lane view.

**Proposed next steps (COO decomposition seed):**
- **NEXT-1 (me):** the **binding-completeness / down-map table** -- proves the Role+Relationship set binds
  all concrete types with no leak; discharges guardrail-1. base does a synchronous pre-CTO read of this.
- **NEXT-2 (me):** formalize the **declared-variance-dimension** mechanism + the symmetry test -- the
  COMPSIMILAR C3/Twin unblocker.
- **NEXT-3 (me, on CTO closed-set GO):** the ontology as a machine-readable rule bank (spec form) + the
  adapter down-map -- design becomes code, gated behind the arch ruling.
- **Tier-1:** COO folds this into the NFRA_ONTOLOGY PRD (`prds: []` today) + sequences; CTO arch-gates the
  closed set + the NFRA_SYSTEM division of labor; MSTR ratifies the doctrine (agnostic/archetypal principles
  as an estate standard).

---

## 14. References

- Charter: `org/tier0/ledger/LD-0310.md` (Andrew-direct sovereign, S3). Project:
  `org/projects/NFRA_ONTOLOGY.json`. Memory (canonical .claude store):
  `project_nfra_ontology_universal_agnostic_relational_archetypal.md`.
- Canonical C0-C3 CSE ladder: `infra/system/01_substrate.md` (authority `comp_ladder.py:208`); NFRA_SYSTEM
  (`docs/architecture/NFRA_SYSTEM_PRD.md`, `org/projects/NFRA_SYSTEM.json`).
- Seed substrate: `org/modules/graph/canon-patterns.yaml` (v0.1 CTO-ratified 2026-06-18);
  `org/modules/graph/debtscan/suppression_v1.yaml` (90 FP relationship-classes);
  `org/modules/graph/graph-call-manifest.yaml` (base vocab). Stack axis: NFRA_GLOBGRPH (L1-L7, 40/14).
- Consumer design-of-record: `.../deliverables/COMPSIMILAR_PH2_MOTIF_ENRICHMENT_DESIGN_20260718.md` (base).
- Superseded founding draft: `.../deliverables/NFRA_ONTOLOGY_UNIVERSAL_ARCHETYPE_DESIGN_v0.1_20260718.md`
  (@c4f893deb).

*-- 0.8.0_AE_CloudComp~C. Design-of-record v0.2, draft for CTO arch-gate. Design, not code.
base pre-CTO read of the down-map next. RAVC to MSTR + COO.*
