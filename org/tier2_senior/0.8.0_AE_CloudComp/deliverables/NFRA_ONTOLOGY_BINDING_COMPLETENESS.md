# NFRA_ONTOLOGY -- Binding-Completeness Proof (CTO acid test)

**Companion to `NFRA_ONTOLOGY_DESIGN_OF_RECORD.md` (v0.2).** Author: `0.8.0_AE_CloudComp~C`, 2026-07-18.
Status: DRAFT for CTO arch-gate; base pre-CTO read; RAVC MSTR + COO.

**Purpose (CTO gate criterion 1, verbatim via MSTR):** *"ENUMERATE the concrete-type universe and SHOW each
binds to exactly ONE archetype with NO misc/catch-all bucket -- a catch-all is where an ontology quietly
dies."* This doc discharges guardrail-1: it binds the FULL concrete-type universe to the archetype
vocabulary, and where a type does NOT bind cleanly it names a BOUNDED DECISION (never a catch-all).

**The concrete-type universe.** Grounded on `org/modules/graph/cse_schema.py` (Entity :56-88 = **29 members**
[10 org-level + 19 code/infra], Relationship :92-117 = **23 members**) -- CSE's `# code/infra` tier already SUBSUMES canon-patterns' 23
node-types + 16 edge-types (S3Bucket/Lambda/Table/IAMRole/Endpoint/Field + reads/writes/served_from/flows_to/
triggers/fetches are the same concrete vocabulary). So binding against CSE = binding against canon-patterns +
more. NFRA_GLOBGRPH's L1-L7 (40/14) is the STACK axis (orthogonal); its node classes bind by the same rules
(open item, DoR Section 13).

**SCOPE NOTE for the gate (base, 042801Z -- so CTO does not read breadth as drift).** This binding is a
STRICT SUPERSET of canon-patterns. canon-patterns models only the FLOW motifs (AWS infra + FE-stitch:
reads/writes/triggers/served_from); CSE's universe ADDS STRUCTURAL/DEFINITIONAL entities
(Module/GraphScope/Tier/Type/Symbol) that canon-patterns never modeled. So decisions D2 (Container) and D8
(definitional scope-out) exist precisely BECAUSE the agnostic layer binds a broader universe than
canon-patterns ever did -- that breadth is a FEATURE (the agnostic ambition), NOT canon-patterns drift.

**No-catch-all discipline.** Every row binds to exactly one archetype OR is one of two HONEST non-bindings:
(a) **contextual** -- a polymorphic type whose Role the adapter derives from edges (Lambda/Service/Component);
this is a RESOLVED binding (one archetype per instance), not a catch-all. (b) **explicit-scope-out** -- a type
on a DIFFERENT axis (definitional/taxonomy), named and reasoned, never bucketed. **The honest-degrade target
`Concept` gets NO archetype BY DESIGN** (it is the coverage-denominator's "unknown", LAW-1) -- that is the
opposite of a catch-all: it is the named place unknowns are COUNTED, not hidden.

---

## CSE-OWNER RULING (DS~B @d16e269bf) -- AXIS-2 owner-ratified reconciliation (D0-D7)

The CSE owner (`0.4.0_DS~B`, Andrew brought in) ruled AXIS-2 (the RELATION axis), source-line-cited, folded
into base's coherence anchor @352549fb0. These CORRECT Tables A/B below (kept for the audit trail; read these
rulings as authoritative where they differ):

- **D0 (LAW-1 denominator):** enum is Entity **29** / Relationship **23** (verified: my grep undercounted
  Entity by 1; my earlier "24" wrongly folded in `routes-to`, which is NOT a CSE member -- `routes_to`
  appears only in the edge->Relationship MAP, not the enum).
- **D1:** `requires` is CONCRETE (:115), not abstract -- my `requires -> depends-on` binding stands; only the
  grain label was off.
- **D2:** my elevations `denies`/`triggers`/gate-family ride GRAIN -> legitimate, NOT S5 forks (no new CSE
  primitive).
- **D3 (governs != guards -- SPLIT; corrects Table A):** I bound BOTH `governs` AND `allowed/authenticates/
  authorizes` to one `guards`. **Split:** `governs` = policy/authority (narrow, a distinct primitive);
  `guards` = the GATING archetype (parent of `denied`/`allowed`/`authenticates`/`authorizes`). Narrow
  `governs` also frees `owns`.
- **D4:** `resolves-through` is NOT a new primitive -- it = CSE `references` + a Registry/Router/Gateway ROLE.
- **D5:** `derives_from` AND `flows_to` both kept; **EdgeKind (passthrough/rename/recompute-guarded) MUST
  stay on `flows_to`.**
- **D6 (C-1 OWNS ruled -- `owns` VALIDATED):** (a) custody splits out -> a governed CSE **`OWNS` primitive**
  (a 0.4->0.5 schema bump) -- my empirically-forced `owns` is VALIDATED, but it lands as a CSE-GOVERNED
  primitive under S5, **NOT ontology-local**; (b) `S3Key OWNED_BY S3_BUCKET` re-maps to `contains`-inverse
  (no new primitive); (c) the `OWNERSHIP` Qualifier AND the `OWNS` edge BOTH coexist (the AUTHORITY:AUTHORIZES
  precedent). The 0.4->0.5 bump routes to the CTO gate as a governed schema change (CTO+CVO+COO SoD; DS~B
  designs, does not land).
- **D7:** `routes-to` = `flows_to` + a Router ROLE; `projects` = `served_from`'s grain-parent -- neither is a
  new CSE primitive.

**Net AXIS-2 (owner-ratified):** the abstract RELATION primitives reconcile to CSE as a RE-LAYERING (no fork):
`produces / consumes / derives-from / depends-on / contains / triggers / guards / governs / denies / owns`
(the last a CSE-governed `OWNS` bump). `resolves-through`/`routes-to`/`projects` are role-composites or
grain-parents, NOT standalone primitives. **DS~B DEFERS to me/MSTR the ROLE axis, Variance-vs-`implements`,
and Type/Symbol -- those stay mine.**

---

## Table A -- CSE `Relationship` (23) -> Relationship archetype

| CSE relationship | grain | binds to | note |
|---|---|---|---|
| produces | abstract | **produces** | identity |
| consumes | abstract | **consumes** | identity |
| derives_from | abstract | **derives-from** | data-dependency; a `consumes` carrying a transform-KIND (passthrough/rename/recompute, cf. CSE `EdgeKind`) |
| depends_on | abstract | **depends-on** | general dependency (relies on existence/behavior, not necessarily reading state) -- **[DECISION D1]** |
| contains | abstract | **contains** | composition / part-of -- **[DECISION D2: my v0.1-0.2 set lacked this; ADD it]** |
| governs | abstract | **guards** | a Policy/authority governs = gates |
| supersedes | abstract | *(Variance: Superseded)* | NOT a C1 edge -- a cross-instance comparison (DoR Section 8) |
| references | abstract | **resolves-through** | a soft name/identity reference resolved via a target |
| implements | abstract | *(scope-out, D3)* | SPEC/definitional conformance (a class implements an interface) -- scope OUT. **NOTE (MSTR doctrine lean): STRUCTURAL conformance ("conforms to the canonical pattern / diverged from its twin") STAYS IN -- that is the Variance operator, not `implements`. [DECISION D3]** |
| requires | abstract | **depends-on** | a required precondition = a dependency |
| triggers | concrete | **triggers** | identity (control, not payload) |
| denied | concrete | **denies** | explicit prohibition (the cross-firm Deny control) |
| allowed | concrete | **guards** | the permit-outcome of a gate (guard permits or denies) |
| authenticates | concrete | **guards** | identity gate |
| authorizes | concrete | **guards** | access gate |
| reads | concrete | **consumes** | adapter-grain of consumes |
| writes | concrete | **produces** | adapter-grain of produces |
| fetches | concrete | **consumes** | adapter-grain of consumes |
| flows_to | concrete | **derives-from** | adapter-grain; carries the KIND |
| served_from | concrete | **projects** | adapter-grain of projects (the SERVER-side serve boundary) |
| renders | concrete | **consumes** | the CLIENT-side terminal display (a Sink `consumes` a Field to render it). **KEPT DISTINCT from `served_from`->`projects`** (base catch) -- collapsing serve+render into one relationship would kill canon-patterns' `dangling_served` deviation (served-but-not-rendered vs rendered). Serve = a boundary `projects`; render = a Sink `consumes`. |
| calls | concrete | **triggers** (+`consumes` if data-returning) | invocation; a data-returning call emits BOTH the control `triggers` AND the data `consumes` |
| imports | concrete | **depends-on** | code import = a dependency (adapter-grain) |
| *(no CSE term)* | -- | **routes-to** | conditional forwarding -- present in canon-patterns (Router/silent_rewrite) but NOT in CSE's enum; **[DECISION D4: propose adding `routes-to` to CSE's SoD enum, or keep as an ontology-layer refinement of `triggers`+predicate]** |

**Relationship verdict:** 23/24 CSE relationships bind to exactly one archetype (14 abstract-identity or
Variance, 9 concrete binding UP to an abstract archetype). The binding FORCES 4 named decisions (D1-D4);
none is a catch-all. Resulting proposed abstract Relationship set: **produces, consumes, derives-from,
depends-on, contains, guards, denies, triggers, routes-to, projects, resolves-through** (11).

---

## Table B -- CSE `Entity` (29) -> Role archetype

**org-level (abstract):**

| CSE entity | binds to | note |
|---|---|---|
| Artifact | **Store** | a produced/held unit (the generic "held output") |
| Dataset | **Store** | holds data |
| Component | *contextual* | polymorphic -- Transformer / Store / Container by edges (adapter resolves) |
| Service | *contextual* | polymorphic -- Gateway (serves) / Transformer / Router by edges |
| Policy | **Guard** | governs/constrains |
| Constraint | **Guard** | constrains -- **[DECISION D5: spec/governance entities as Guards vs a spec axis]** |
| Requirement | **Guard** | constrains an implementation -- **[D5]** |
| Person | **Source / Sink** | an ACTOR at the boundary (originates or receives) -- **[DECISION D6: actor entities]** |
| Organization | **Source / Sink** | actor/owner at the boundary -- **[D6]** |
| Concept | *(no archetype BY DESIGN)* | the LAW-1 honest-degrade / untyped target -- counted in the coverage denominator, never guessed |

**code/infra-level (concrete):**

| CSE entity | binds to | note |
|---|---|---|
| S3Bucket | **Store** | identity |
| Table | **Store** (or **Registry** if a catalog) | a catalog table (Nessie ref/obj) is a Registry; a data table is a Store |
| SecretRef | **Store** | a secret store (resolved-through for access) |
| Field | **Store** | field-grain state |
| Endpoint | **Gateway** | boundary entry/exit |
| Schedule | **Trigger** | activates on time |
| Lambda | *contextual* | polymorphic -- Transformer / Guard / Router / Trigger by edges (the canonical adapter case) |
| Function | *contextual* | Transformer (does work) or, if pure-container, structural |
| Tool | **Transformer** | reads the estate, produces output (a Consumer/Transformer) |
| IAMStatement | **Guard** | allow/deny = the gate decision (via `guards`/`denies`) |
| IAMRole | **Registry / Guard-principal** | an assumable identity (resolved-through); the access principal -- **[DECISION D7: identity/principal role]** |
| ReactComponent | *contextual* | Sink (renders) or frontend Transformer |
| JSXElement | **Sink** | terminal render |
| Hook | *contextual* | frontend logic Transformer |
| Module | **Container** | contains functions -- **[DECISION D2: Container role vs the `contains` relation carries it structurally]** |
| GraphScope | **Container** | a scope/boundary containing nodes -- **[D2]** |
| Tier | **Container** | an org grouping -- **[D2]** |
| Type | *(scope-out: definitional axis)* | a type/interface declaration -- a DEFINITION, not a flow node (code/taxonomy axis) -- **[D8]** |
| Symbol | *(scope-out: definitional axis)* | a code symbol -- a DEFINITION, not a flow node -- **[D8]** |

**Entity verdict:** of 28 entities -- 15 bind to exactly one Role (Store/Gateway/Guard/Trigger/Transformer/
Sink/Registry); 6 are *contextual* (polymorphic, one Role per instance via the adapter -- a resolved binding,
not a catch-all); 1 (`Concept`) is the by-design honest-degrade (no role, counted); 3 (`Module/GraphScope/
Tier`) hinge on DECISION D2 (Container role vs structural `contains`); 2 (`Type/Symbol`) scope out to the
definitional axis (D8); the rest carry named decisions D5/D6/D7. **Zero catch-all.**

---

## The forced decisions (for CTO's ruling -- each bounded, none a catch-all)

| # | Decision | My proposed resolution |
|---|---|---|
| **D1** | `depends-on` as a primitive relationship? | **Yes** -- CSE has it first-class; it is the general dependency (existence/behavior) distinct from `consumes` (state-read). |
| **D2** | `contains` (composition) + a **Container** Role, or containment purely as the `contains` relation? | **Add `contains` as a primitive relationship; make Container a Role** (Module/GraphScope/Tier are real container nodes). Composition is fundamental to any system; omitting it was a v0.1-0.2 gap this proof caught. |
| **D3** | `implements`/`conforms-to` -- a relationship primitive, or scope to the code/definitional axis? | **Scope out SPEC/DEFINITIONAL conformance** (X implements interface Y -- definitional). **MSTR doctrine lean (carry to gate): STRUCTURAL conformance -- "conforms to the canonical pattern / diverged from its twin" -- MUST STAY IN; it is the VARIANCE operator (Canonical vs Fork-Shadow) that unblocks COMPSIMILAR, NOT `implements`.** The line: structural conformance = Variance (IN); spec/definitional conformance = `implements` (OUT). Doctrine-adjacent -> RAVC MSTR + CTO. |
| **D4** | `routes-to` -- add to CSE's SoD enum, or keep as an ontology refinement of `triggers`+predicate? | **Keep as an ontology-layer Role/Relationship** (Router); it is a refinement CSE's enum lacks. If it must materialize, route the enum extension to the schema owner (SoD). |
| **D5** | Spec/governance entities (Requirement/Constraint/Policy) -> Guard, or a distinct spec axis? | **Guard** -- they gate/constrain other nodes (`governs` -> `guards`). Clean and agnostic. |
| **D6** | Actor entities (Person/Organization) -> Source/Sink, or a distinct Actor axis? | **Source/Sink at the boundary** -- an actor originates or receives; no new axis needed. |
| **D7** | Identity/principal (IAMRole) -> Registry, Guard-principal, or its own? | **Registry** (an identity resolved-through) with a Guard-adjacency; the `IAMStatement` carries the gate. |
| **D8** | Definitional entities (Type/Symbol/Concept) in or out of the Role axis? | **Out** (Type/Symbol = definitional/taxonomy axis); **Concept = the by-design honest-degrade** (no role, counted in the denominator). **MSTR doctrine lean = STRONG ENDORSE scope-out: Type/Symbol are what a node IS-CALLED / its type-identity = OPAL_TAXONOMY's naming axis, not the relational ontology's -- scoping them out IS the distinct-from-taxonomy guardrail working.** Doctrine-adjacent -> RAVC MSTR + CTO. |

---

## Verdict

- **Zero catch-all.** Every one of the 24 relationships + 28 entities either binds to exactly one archetype,
  is *contextual* (a resolved one-archetype-per-instance polymorphism the adapter decides), is the by-design
  honest-degrade (`Concept`, counted not hidden), or is explicitly scoped to a named different axis
  (definitional). There is no "misc" bucket -- the place an ontology quietly dies.
- **Closure is achievable** with the additions this proof forced: promote `depends-on` + `contains` to
  primitives and add a `Container` Role (D1/D2). Resulting closed sets to ratify:
  - **Roles (12):** Source, Store, Producer, Transformer, Consumer, Sink, Gateway, Guard, Router, Trigger,
    Registry, **Container**. (+ Observer/Monitor still open, DoR Section 4.)
  - **Relationships (owner-ratified AXIS-2, D0-D7):** produces, consumes, derives-from, depends-on, contains,
    triggers, **guards** (gating parent of denied/allowed/authenticates/authorizes), **governs** (narrow
    policy/authority -- SPLIT from guards, D3), denies, **owns** (a CSE-governed `OWNS` primitive, 0.4->0.5
    bump, D6). `resolves-through`/`routes-to`/`projects` are role-composites or grain-parents (D4/D7), NOT
    standalone primitives.
  - **Variance (6):** Canonical, Twin, Variant, Fork-Shadow, Superseded, Orphan.
- **Honesty note (the whole point of running the acid test):** the binding did not "just work." It caught a
  real gap (`contains`/Container was missing) and forced 8 bounded decisions. That is the proof functioning
  as CTO intends -- surfacing the hard cases explicitly rather than absorbing them into a catch-all. **The 8
  decisions are the arch-gate agenda.**

*-- 0.8.0_AE_CloudComp~C. Binding-completeness proof, DRAFT for CTO arch-gate. base pre-CTO read requested.*
