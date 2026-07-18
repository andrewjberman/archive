# NFRA_ONTOLOGY -- Universal Relational-Archetypal Ontology

**Design-of-record v0.1 (DRAFT for CTO arch-gate).** Author: `0.8.0_AE_CloudComp~C` (build/author lane,
LD-0310). Date: 2026-07-18. Status: **FOUNDING DRAFT -- design, not code.** Routes: CTO arch-gate
(closed-set + orthogonality ruling); COO decomposition into TOs; MSTR governs the doctrine (the
agnostic/archetypal principles as a standard). RAVC to MSTR + COO as it shapes.

> **This is the LANGUAGE, not an Opal artifact.** It must read as true of a Kafka topology, a POSIX
> filesystem, a service mesh, and our AWS estate equally. Every place a concrete Opal/AWS name appears
> below, it is an EXAMPLE of the binding adapter (Section 7), never part of the language.

---

## 0. Provenance (VERBATIM -- the phrasing IS the ruling)

Andrew-direct, MSTR terminal, 2026-07-17/18 (recorded LD-0310 `andrew_instruction_ref`; relayed to base
in the COMPSIMILAR PH2 design-of-record @72edd1eca):

> Yeah it's time for us to develop a true universal ontology for this purpose. i think systems
> ontological language should be agnostic, not opal-scoped or aws-scoped or etc, its plain english
> semantics, but designed to be relational archetypal

Separation ruling (Andrew, same window): base `0.8.0` handles the comp-similar summary MECHANICS;
NFRA_ONTOLOGY (the C3-level LANGUAGE / rule bank) is "its own thing... something we really need to go
deep on." Ownership: "we can direct NFRA_ONTOLOGY to `0.8.0_AE_CloudComp~C`."

Charter: **LD-0310** (Andrew-direct sovereign-ratified, S3). Project: `org/projects/NFRA_ONTOLOGY.json`.

---

## 1. Purpose, principles, and what this is NOT

**Purpose.** A substrate-neutral LANGUAGE for stating *what a node IS relationally* and *how nodes relate*,
so that any consumer -- a deviation scorer, a node-summary enricher, a human reading a diagram -- describes
system structure in ONE vocabulary, independent of the platform underneath.

**The three binding principles (Andrew, non-negotiable):**

1. **AGNOSTIC** -- not opal-scoped, not aws-scoped, not any-substrate-scoped. The vocabulary names
   RELATIONSHIPS, which every system has, not TYPES, which every system names differently.
2. **PLAIN-ENGLISH semantics** -- each archetype has a one-sentence human-readable definition. A person
   who has never seen the schema can read "Guard: a node a flow must pass, which may permit or deny it"
   and apply it. No typed-schema jargon in the semantics.
3. **RELATIONAL-ARCHETYPAL** -- built from universal relationship ARCHETYPES (how things relate), not
   platform types. A node's archetype is a function of its RELATIONS, never of its concrete type name.

**What this is NOT -- the OPAL_TAXONOMY boundary (CTO guardrail 2).**
Ontology answers *what a node IS relationally and how it relates* (Role / Relationship / Lineage /
Variance). Taxonomy answers *what a node is CALLED* (its name grammar, its structural naming consistency).
They **compose, they do not merge**: a well-named resource's NAME can ENCODE its ontological role
(`silver-*-sweep` names a Transformer at the silver stage), and taxonomy can lint that the name matches
the ontology -- but the two are distinct axes with distinct owners. **Nothing in this ontology names,
renames, or lints a name.** (Distinctness test, Section 9.2.)

**What this is NOT -- attributes.** Non-relational node attributes (an S3 bucket's encryption mode, a
Lambda's memory size, a table's billing mode) are NOT ontology. The ontology is closed on the RELATIONAL
axis only; attributes live in the binding adapter / taxonomy. This scope-cut is load-bearing for closure
(Section 9.1).

---

## 2. The core architectural claim -- two primitives, two derived calculi

The whole language reduces to **two primitive vocabularies and two derived calculi**, stratified by how
many nodes each archetype describes:

| Axis | Arity | Kind | What it classifies |
|---|---|---|---|
| **ROLE** | 1 node | PRIMITIVE vocabulary | what a single node IS, relationally (a label derived from its local edge-neighborhood) |
| **RELATIONSHIP** | 2 nodes | PRIMITIVE vocabulary | how one node relates to another (a directed edge label) |
| **LINEAGE** | n nodes | DERIVED calculus (a GRAMMAR over Role + Relationship) | a recurring multi-node SHAPE, expressed as a canonical composition of roles joined by relationships |
| **VARIANCE** | compare k like nodes | DERIVED calculus (a COMPARISON over same-Role nodes) | how instances of the same logical thing relate to EACH OTHER (twin / variant / fork-shadow / superseded / orphan) |

**The closure argument (answers CTO guardrail 1 -- "closed + orthogonal, no catch-all leak").**
Every RELATIONAL fact about a system is a statement about **one** node, **two** nodes, an **n-node path**,
or a **comparison of like nodes**. There is no fifth kind of relational structure. The two primitives
(Role, Relationship) are the atoms; Lineage is their canonical GRAMMAR (no new vocabulary -- it is
role-nodes joined by relationship-edges); Variance is a COMPARISON operator over same-role nodes (again no
new vocabulary -- it compares Role assignments). Because Lineage and Variance introduce **zero new
primitive terms**, the closed set to ratify is exactly **the Role set (Section 3) + the Relationship set
(Section 4)**. Everything else is grammar and comparison over those two. That is the whole "no catch-all
leak" guarantee: a concept that seems to need a new term is either (a) a Role or Relationship we missed,
(b) a Lineage = a composition, or (c) a Variance = a comparison. There is no "misc" bucket because there
is no fourth structural arity.

**Determinism (Andrew's standing requirement, inherited from COMPSIMILAR).** Every archetype assignment is
DERIVED FROM STRUCTURE -- a node's role from its edge-neighborhood, a relationship from the edge, a lineage
from a path match, a variance from an instance comparison. No inference, no LLM. A node whose structure
matches no archetype gets NO label (never guessed); coverage is always printed as a denominator
(Section 8).

---

## 3. ROLE archetypes (PRIMITIVE -- the closed 1-node set)

A Role is a plain-English label for what a node IS in the flow, **derived from its local edge-neighborhood**
(inbound/outbound relationship pattern), never from its concrete type. A concrete type may be polymorphic
(a Lambda is a Transformer, a Guard, a Router, or a Trigger depending on its edges -- Section 7).

Proposed closed set (**11 roles**; CTO blesses/adjusts the final set at the gate):

| Role | Plain-English definition | Structural signature (how it is DERIVED) |
|---|---|---|
| **Source** | Originates data or signal from OUTSIDE the system's control. | inbound: none within-system; outbound: `produces`. (a vendor feed, a user, a sensor, an upstream API) |
| **Store** | Holds state that others read or write; performs no transformation itself. | is the object of `produces`/`consumes`; does not itself `derives-from`. (a bucket, a table, a topic, a file) |
| **Producer** | Writes/creates state into a Store or a downstream node; does not derive it from a within-system input. | outbound `produces`; no inbound `derives-from` dependency. |
| **Transformer** | Reads input, DERIVES new output from it, writes the output -- the work-doing node. | inbound `consumes`/`derives-from` AND outbound `produces`. (a gold script, a stream processor, a compiler) |
| **Consumer** | Reads state and acts on it; forwards or terminates. | inbound `consumes`; may or may not forward. |
| **Sink** | Terminal consumer -- the flow ENDS here. | inbound `consumes`; outbound: none. (a render, a dashboard, an archive, a human) |
| **Gateway** | The single controlled entry/exit point between a zone and the outside. | the sole node carrying `projects`/cross-boundary edges for a zone. (an API edge, a CDN edge, a mount point) |
| **Guard** | A node a flow MUST PASS, which may permit or deny it. | interposed on a `consumes`/`routes-to` path; carries `guards` (and may carry `denies`). (an authorizer, a validator, a policy, a firewall rule) |
| **Router** | Directs a flow to ONE OF SEVERAL destinations by a rule. | one inbound flow, multiple outbound `routes-to` by predicate. (an edge router, a load balancer, a dispatch catalog) |
| **Trigger** | Activates another node on an event or schedule -- carries the "GO", not the payload. | outbound `triggers`; carries control, not data. (a schedule rule, an event source, a cron) |
| **Registry** | The authoritative catalog/index of what exists; others resolve identity/location THROUGH it. | is the object of `resolves-through`. (a service registry, a catalog table, a DNS zone, a Nessie ref-store) |

**Design notes for the gate:**
- **Store vs Registry:** both hold state, but a Registry is resolved-THROUGH for identity/location (others
  ask it "where/what is X"); a Store is read/written for payload. The suppression file's
  `FP_NESSIE_INTERNAL_DDB` (catalog ref/obj tables) is a Registry, not a data Store -- the distinction is
  real and load-bearing.
- **Guard vs Gateway vs Router:** a Gateway is a POSITION (the boundary crossing); a Guard is a DECISION
  (permit/deny); a Router is a CHOICE (which of N). One concrete node can hold two roles (an auth-edge is a
  Gateway that is also a Guard) -- roles are not mutually exclusive per node, only the SET is closed.
- **Producer vs Transformer:** the discriminator is whether the output is DERIVED from a within-system
  input. A Source-fed ingester that only lands raw bytes is a Producer; a script that reads silver and
  writes gold is a Transformer. (This maps cleanly to bronze=Producer-of-raw, silver/gold=Transformer.)
- **Candidate for the gate: Monitor / Observer.** A CloudWatch alarm, a freshness guard, a health check
  OBSERVES a node without being in its flow (`FP_CW_ALARM_IMPLICIT_MONITOR`). Is "Observer" an 12th Role,
  or is it a Guard whose `guards` edge is advisory rather than blocking? I lean **Guard-subtype** (an
  Observer is a Guard that reports rather than denies) to keep the set at 11 -- **CTO ruling requested.**

---

## 4. RELATIONSHIP archetypes (PRIMITIVE -- the closed 2-node set)

A Relationship is a plain-English, DIRECTED edge label for how one node relates to another. Proposed closed
set (**8 relationships**; CTO blesses/adjusts):

| Relationship | Plain-English (A -rel-> B) | Notes |
|---|---|---|
| **produces** | A writes/creates state into B. | the data-out edge (write). |
| **consumes** | A reads/depends on state from B. | the data-in edge (read). `derives-from` is a consumes whose OUTPUT depends on the input -- a transform dependency (kept as a consumes SUBTYPE, not a separate primitive, to hold the set closed). |
| **triggers** | A activates B on an event/schedule -- control, not payload. | the "GO" edge. Distinct from produces: no state crosses. |
| **guards** | A gates B: a flow to B must clear A. | the interposition edge (auth-before-read, validate-before-write). |
| **denies** | A PROHIBITS a relationship to/from B. | the NEGATIVE relationship. **An ontology must represent prohibition, not only permission** -- the cross-firm Deny guardrail (`FP_CROSS_FIRM_DENY_GUARDRAIL`, 198 instances) is a `denies`, a security CONTROL, and reading it as a "missing permission" is the single most common adapter misread. |
| **routes-to** | A conditionally forwards a flow to B (one of several). | the choice edge; carries the predicate. |
| **projects** | A exposes an internal thing B at an external surface (serves/publishes). | the boundary-crossing edge; the "served" edge. |
| **resolves-through** | A looks up identity/location of a target via B (a Registry). | the indirection edge. |

**Moved OFF this axis (an orthogonality correction to the starter set).** MSTR's starter register listed
`supersedes` and `mirrors` under RELATIONSHIP. On inspection they are **VARIANCE facts, not base
relationships**: both relate two instances of the SAME role (a Producer and its replacement; a Producer and
its twin). They belong on the cross-instance axis (Section 6), not the 2-node edge axis. Keeping them here
would break orthogonality (the same fact expressible on two axes). This is the kind of refinement the
two-primitive closure is meant to force.

---

## 5. LINEAGE archetypes (DERIVED -- a GRAMMAR over Role + Relationship)

A Lineage is a RECURRING multi-node shape, expressed with ZERO new vocabulary as a canonical composition of
Role-nodes joined by Relationship-edges. This is the generalization of canon-patterns' 4 pattern-classes:

| Lineage archetype | Canonical composition (roles + relationships) | canon-patterns.yaml source |
|---|---|---|
| **Pipeline** | `Source -produces-> (Transformer -produces-> Store)* -consumes-> Sink` -- a staged derivation chain. | PIPELINE_CANON (bronze->silver->gold->served->render) |
| **Guarded-Access** | `Consumer -consumes-> Guard -guards-> Store` -- a flow that must clear a gate before it reaches state. | AUTH_CANON (route -> auth-edge -> S3) |
| **Provision** (deploy) | `Producer -produces-> Store(artifact) <-consumes- Transformer/Runner` -- an artifact is published to a store, then a runtime loads it. | DEPLOY_CANON (repo -> S3 code/ -> runner) |
| **Served-Projection** | `Store -projects-> Gateway -consumes-> ... -consumes-> Sink` -- an internal thing surfaced at a boundary and rendered. | SERVED_LINEAGE_CANON (gold field -> ServedURL -> fetch -> render) |

**The general rule (this is the axis's whole content):** a Lineage archetype is DEFINABLE by anyone as an
ordered composition of Roles and Relationships. New systems declare new Lineages WITHOUT extending the
primitive vocabulary -- a Kafka "stream-join" lineage is just `Source -produces-> Store(topic)
<-consumes- Transformer(join) -produces-> Store(topic)`. Because Lineage adds no primitives, it needs no
separate ratification beyond the four seed shapes above; the seed set is illustrative, not closed.

**Deviation = a live path that does not match its declared Lineage** (this is what the canon-deviation
scorer consumes -- Section 10). canon-patterns' `deviation_classes` (layer_skip, orphan_stage, dual_writer,
missing_auth_edge, silent_rewrite_noop, ...) all generalize to: *a concrete path whose role/relationship
composition diverges from the canonical Lineage shape.*

---

## 6. VARIANCE archetypes (DERIVED -- a COMPARISON over same-Role instances)

The richest axis, and the one that UNBLOCKS COMPSIMILAR C3 + the Twin/Fork-Shadow labels. Variance
classifies how MULTIPLE instances of the same logical thing relate to EACH OTHER. Proposed set
(**6 variances**):

| Variance | Plain-English | The discriminator |
|---|---|---|
| **Canonical** | The reference instance -- the shape all others are measured against. | designated (or the modal/dominant shape). |
| **Twin** | A DESIGNED parallel instance, structurally symmetric to the canonical. NOT debt. | matches the canonical on the IDENTITY key AND differs only along a DECLARED variance dimension. |
| **Variant** | A legitimate FACET-difference of the same logical thing (per-env, per-service, per-tenant copy). | differs ONLY along a declared dimension; symmetric where the dimension does not apply. |
| **Fork-Shadow** | An instance that DIVERGED from its twin/canonical WITHOUT a declared reason. **This IS debt.** | matches on identity key but differs OFF-key (asymmetric + undeclared). |
| **Superseded** | An instance REPLACED by a newer one but still present (should be archived/removed). | a newer instance `supersedes` it; both live. |
| **Orphan** | An instance with NO canonical/twin/consumer relationship at all -- disconnected. | no variance peer AND no live consumer. |

**The load-bearing generalization (this elevates canon-patterns' `twin_shadow_guard`).**
canon-patterns HARD-CODES the twin dimension: "key motif-identity on `(firm, layer, logical-stage)`." The
universal layer generalizes it: **a system DECLARES its VARIANCE DIMENSIONS** (firm, environment, region,
tenant, service, ...); then:

- instances that match on the identity key and differ **ON a declared dimension** are **Twin/Variant** (fine);
- instances that match on the identity key but differ **OFF every declared dimension** are **Fork-Shadow**
  (debt -- the 29-file inf bare-vs-INF_ shadow, the 9-RED bd-cot fork);
- an instance with **no peer and no consumer** is an **Orphan** (the CVO-confirmed `opal-data-aaii-v2` real
  orphan the suppression file had to UNMASK).

This is substrate-agnostic: "firm" becomes just one possible declared dimension. The same calculus
distinguishes dev/staging/prod copies (`DUP_BENIGN_ENV_TWIN` -> Variant on the `env` dimension), per-service
IAM splits (`DUP_BENIGN_SERVICE_SPLIT` -> Variant on the `service` dimension), and cross-firm parallels
(`DUP_BENIGN_CROSS_FIRM` -> Twin on the `firm` dimension) -- all three suppression families are ONE
variance calculus with different declared dimensions.

**Determinism holds:** symmetric-vs-asymmetric over a declared dimension set is a pure structural
comparison -- no inference. This is exactly the deterministic Twin/Fork-Shadow label COMPSIMILAR's C3 clause
was HELD waiting for.

---

## 7. The layering + the binding adapter (canon-patterns.yaml demoted)

**Architecture (LD-0310):** the universal archetype layer (Sections 3-6) sits ABOVE; the CTO-ratified
`canon-patterns.yaml` (v0.1) becomes the **AWS-BINDING ADAPTER** -- a table that maps concrete AWS
types/edges onto the substrate-neutral archetypes.

**The adapter has two kinds of mappings:**
1. **Direct** (`type -> role`): `S3_BUCKET -> Store`, `DYNAMODB_TABLE -> Store` (or Registry if a catalog),
   `SECRET -> Store`, `EVENT_RULE/EVENT_SOURCE -> Trigger`, `SNS_TOPIC/SQS_QUEUE -> Store(queue) or Trigger`,
   `API_GW -> Gateway`, `ServedURL -> Gateway`, `IAM_POLICY(Deny) -> Guard via denies`, `Field(gold) ->
   Store(field-grain)`, `JSXRender -> Sink`.
2. **Contextual** (`type + edge-pattern -> role`): `LAMBDA` is polymorphic --
   `LAMBDA` with inbound `TRIGGERS` from an `API_ROUTE` + outbound `READS` to `S3` as an edge-fn -> **Guard**
   or **Router**; `LAMBDA` reading a data Store and writing another -> **Transformer**; `LAMBDA` only
   triggered on schedule -> **Trigger/Transformer**. This is canon-patterns' existing "role = structural
   position" principle, elevated: **the role is a function of the edge-neighborhood, decided by the adapter.**

**Edge mapping** (`edge_type -> relationship`): `WRITES/EMITS_TO -> produces`; `READS/READS_FIELD/FETCHES ->
consumes`; `FLOWS_TO -> derives-from` (carries KIND: passthrough/rename/recompute); `TRIGGERS -> triggers`;
`SERVED_FROM/IS_ENDPOINT -> projects`; `PROJECTS_TO -> projects`; an IAM `Deny` statement -> `denies`;
`ASSUMES/CAN_ASSUME/READS_SECRET/HAS_POLICY/HAS_KEY -> resolves-through` or `guards` per role.

**The invisible-edge principle (this is a DESIGN pillar, and it validates the whole approach against the
suppression file).** The ontology describes the system's ACTUAL relational behavior. **A relationship that
the substrate/graph does not emit as an edge is an ADAPTER COVERAGE-GAP, not an absence of the
relationship.** Roughly 60% of `suppression_v1.yaml`'s 90 FP-classes are exactly this: the edge is real but
unmodeled --
`FP_LOG_GROUP_IMPLICIT_LOGS`, `FP_SECRET_RUNTIME_ACCESS`, `FP_API_LAMBDA` (API_GW->Lambda invoke absent),
`FP_LEDGE` (CloudFront->edge trigger absent), `FP_ECS_TRIGGER`, `FP_EC2_SSM_INVOKED`,
`FP_CW_ALARM_IMPLICIT_MONITOR`. Under this ontology these are NOT false positives to hand-suppress one by
one -- they are **named gaps in the adapter's edge coverage**. The ontology asserts "an API-invoked Lambda
`consumes` a `triggers` from its Gateway" as a SEMANTIC truth; the adapter's job is to emit that edge (or
declare it a known gap). This turns a 90-entry hand-maintained FP list into a coverage checklist for ONE
adapter. (Whether the ontology SUBSUMES suppression, or merely informs it, is an open question for CTO --
Section 11.)

---

## 8. Determinism + the coverage-denominator discipline

Inherited verbatim from Andrew's COMPSIMILAR determinism requirement and CLAUDE.md's controls doctrine:

- **Every archetype assignment is structure-derived.** No inference, no LLM, no guessing.
- **No match -> no label.** A node whose neighborhood matches no Role gets no Role clause; a path matching
  no Lineage gets none; an instance with no peer gets no Variance beyond Orphan. Absence is never filled.
- **Print the denominator.** Every classification pass reports coverage as `"N of M nodes assigned a Role;
  K unclassified"`, reusing COMPSIMILAR's existing UNKNOWN-thin control. A silent 100% is a red flag, not a
  success -- an unclassified tail is the honest signal of adapter coverage-gaps (Section 7).

---

## 9. Answering the two CTO guardrails

### 9.1 CLOSED + orthogonal, no catch-all leak (guardrail 1)
The closure argument (Section 2): relational structure has exactly four arities (1 / 2 / n / compare), the
two DERIVED axes add zero primitives, so **the only closed set to ratify is the Role set + the Relationship
set**. A concept that appears to need a new term resolves to (a) a missed Role/Relationship, (b) a Lineage
composition, or (c) a Variance comparison -- there is no fourth structural kind, hence no "misc" bucket. The
attribute scope-cut (Section 1) keeps non-relational facts OUT, so the ontology is closed on the relational
axis without pretending to describe everything. **The proof obligation I owe CTO:** demonstrate that the
proposed Role+Relationship set binds EVERY one of canon-patterns' 23 node-types + 16 edge-types with no leak
(a binding-completeness table -- Section 11 next-step).

### 9.2 DISTINCT from OPAL_TAXONOMY (guardrail 2)
Two-axis test: **ontology = what a node IS relationally + how it relates** (Role/Relationship/Lineage/
Variance, derived from STRUCTURE); **taxonomy = what a node is CALLED** (its name grammar, derived from the
NAME string). A node has BOTH a role (ontology) and a name (taxonomy); a good name ENCODES the role, and
taxonomy can lint name-vs-role agreement -- but neither axis defines the other. They compose (taxonomy can
carry an ontology term in a name segment), they never merge (renaming a node does not change its role;
re-wiring it does). Overlap governance runs through COO (the OPAL_TAXONOMY overlap map).

---

## 10. Consumer contracts (design FOR the consumers)

**(A) Canon-deviation scorer.** Consumes: Lineage archetypes + their canonical compositions (Section 5) and
the Variance calculus (Section 6). A deviation is a live path whose role/relationship composition diverges
from its declared Lineage, OR an instance that is a Fork-Shadow/Orphan. The scorer's existing
`motif_outlier_semantics` (dominant-vs-outlier) becomes: the Canonical variance IS the dominant shape;
outliers are Fork-Shadow candidates. The `twin_shadow_guard` becomes the Variance calculus. Net: the scorer
reads ONE universal frame instead of 4 hard-coded pattern-classes.

**(B) COMPSIMILAR node-summary C3-enrichment (the HELD clause -- my output unblocks ~D).** The C3 clause
"member of `<system>`" and the Twin/Fork-Shadow labels were HELD (Andrew-direct 3) pending this layer. My
layer emits, per node, deterministically:
- its **Role** (spliceable as C2-adjacent context: "Store", "Guard", ...);
- its **Lineage membership** (the C3 "member of `<Pipeline/Guarded-Access/...>`" clause -- a substrate-
  neutral system-membership, NOT raw canon-patterns);
- its **Variance label** ("Canonical firm-twin of X" / "divergent Fork-Shadow (debt)") from the declared-
  dimension comparison.

Contract shape I will define for ~D at gate-pass (base FEEDS the walkthrough): a pure function
`node -> {role, lineage_membership[], variance_label?}` reading only the node's structural neighborhood +
the declared variance dimensions -- no inference, coverage-denominatored. This is exactly the deterministic
input ~D's enricher was waiting for; it lights up with zero enricher rework (graceful-degradation design
already shipped: no label -> no clause).

---

## 11. Open questions for CTO's arch-gate + proposed next steps

**Open design questions (CTO ruling requested):**
1. **Role set size:** 11 as proposed, or does CTO want Observer/Monitor as a 12th (vs. my Guard-subtype
   proposal)? (Section 3 note.)
2. **Relationship set:** 8 as proposed; is `derives-from` a `consumes`-subtype (my proposal, holds the set
   smaller) or a distinct 9th primitive? Is `denies` blessed as a first-class primitive (I argue yes -- an
   ontology must state prohibition)?
3. **supersedes/mirrors moved to Variance** (Section 4) -- bless the orthogonality correction?
4. **Adapter authority:** does `canon-patterns.yaml` LITERALLY become the adapter file (re-headed +
   restructured to a type->archetype table), or does a NEW adapter file sit beside it and reference it? This
   is a CTO-owned-file question (canon-patterns is CTO's).
5. **Ontology vs suppression (Section 7):** does the universal layer SUBSUME `suppression_v1.yaml`'s
   coverage-gap classes (they become adapter edge-coverage gaps), or stay separate with the ontology only
   informing them? (Affects NFRA_DEBTSCAN.)

**Proposed next steps (COO decomposition seed):**
- **NEXT-1 (me):** the **binding-completeness table** -- prove the Role+Relationship set binds all 23
  node-types + 16 edge-types + the 90 suppression relationship-classes with NO leak (discharges the
  guardrail-1 proof obligation). This is the strongest possible input to CTO's closed-set ruling.
- **NEXT-2 (me):** formalize the **declared-variance-dimension** mechanism (how a system declares its
  dimensions; how the twin/fork-shadow/variant discriminator reads them) -- the COMPSIMILAR C3 unblocker.
- **NEXT-3 (me, on CTO closed-set GO):** the ontology as a machine-readable rule bank (the `.yaml`/spec
  form) + the adapter down-map -- this is where "design" becomes "code", gated behind the arch ruling.
- **Tier-1:** COO folds this into the NFRA_ONTOLOGY PRD (`prds: []` today) + sequences; CTO arch-gates the
  closed set; MSTR ratifies the doctrine (the agnostic/archetypal principles as an estate standard).

---

## 12. References

- Charter: `org/tier0/ledger/LD-0310.md` (Andrew-direct sovereign, S3). Project:
  `org/projects/NFRA_ONTOLOGY.json`.
- Seed substrate: `org/modules/graph/canon-patterns.yaml` (v0.1 CTO-ratified 2026-06-18);
  `org/modules/graph/debtscan/suppression_v1.yaml` (90 FP relationship-classes);
  `org/modules/graph/graph-call-manifest.yaml` (base node/edge vocab).
- Consumer design-of-record: `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/COMPSIMILAR_PH2_MOTIF_ENRICHMENT_DESIGN_20260718.md`
  (base) -- the C2/C3 split, the HELD C3 clause, the `roles:` vocabulary proposal.
- Related: LD-0299 (wave), OPAL_TAXONOMY (naming axis -- composes, does not merge).

*-- 0.8.0_AE_CloudComp~C, founding draft for CTO arch-gate. Design, not code. RAVC to MSTR + COO.*
