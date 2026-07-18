# CSE-Owner Ruling -- NFRA_ONTOLOGY AXIS-2 abstract/concrete split + the C-1 `owns` polysemy

**Author (CSE contract owner):** `0.4.0_DS_ClientPlatform~B` -- author + SCHEMA_VERSION owner of
`org/modules/graph/cse_schema.py` (header `Author: 0.4.0_DS_ClientPlatform~B, TO: NFRA_CSE.P1`).
**For:** `0.8.0_AE_CloudComp` (base, NFRA_ONTOLOGY coordinator) coherence anchor + the CTO binding-completeness
arch-gate. **Requested:** Andrew-direct via base/coordinator, 2026-07-18 (CSE consult 071224Z).
**Governance:** RELATION-axis + Entity-tier calls + the C-1 ruling are the CSE owner's per S5
("a recognizer never forks its own primitive"). **Grounded @ `adf056d74`** -- `cse_schema.py` Entity `:56-88`,
Relationship `:92-117`, Qualifier `:134-143`, CloudEdge mapping `:295-317`.

**Scope discipline.** I rule what CSE owns: (1) the abstract/concrete TIER of CSE's own Entity+Relationship
vocabulary, (2) the four edge-case reconciliations that touch CSE primitives, (3) the C-1 `owns` polysemy.
I DEFER to NFRA_ONTOLOGY/MSTR the axes they own: the Entity->Role bindings (D5/D6/D7), the Variance operator
(D3 implements / supersedes), and the Type/Symbol taxonomy scope-out (D8). Those are the ROLE (AXIS-3) and
VARIANCE (OPERATOR) axes, not the CSE relationship vocabulary.

---

## 0. Denominator correction (LAW-1: name the coverage denominator before reasoning on it)

AST-counted @`adf056d74`: **Entity = 29 members, Relationship = 23 members.** The binding-completeness proof
(`NFRA_ONTOLOGY_BINDING_COMPLETENESS.md`) states "Entity (28) + Relationship (24)". Reconciliation:

- **Entity: actual 29, proof prose says 28.** Table B *lists* all 29 rows (10 org + 19 code/infra) and binds
  each -- so no entity is unbound; the "28" is a prose miscount. No coverage hole, but the denominator line
  should read 29.
- **Relationship: CSE enum = 23; the proof's "24" folds in `routes-to`, which is NOT a CSE member.** Table A's
  24th row is explicitly `*(no CSE term)* -> routes-to` (D4). Counting a *proposed addition* into the
  *existing-universe* denominator conflates "what CSE has" (23) with "what the ontology proposes to add"
  (routes-to). Keep them separate: **CSE Relationship universe = 23; `routes-to` is a governed-add candidate,
  not the 24th existing member.**

Total universe is 52 either way, but for a proof whose stated purpose is a correct, no-catch-all denominator,
the split-point is the thing -- so: **29 / 23, with `routes-to` outside the existing set.**

---

## 1. RELATION axis -- abstract/concrete TIER call (primary charge)

**Verdict: the source first-cut is CORRECT -- abstract block `:94-102` (9) / concrete block `:104-117` (14) --
with ONE grain correction and THREE elevations that are legitimate via GRAIN, not forks.**

Test applied: *substrate-neutrality* -- a term is ABSTRACT (elevate to the ontology's agnostic layer) iff it
means the same thing across org/doc/code/AWS/React; CONCRETE (demote to the binding adapter) iff it only
exists within a specific substrate.

**Abstract (9) -- CONFIRMED, all pass substrate-neutrality:**
`contains, references, depends_on, produces, consumes, implements, governs, derives_from, supersedes`.

**Concrete (14) -- CONFIRMED concrete grain; each binds UP to an abstract archetype:**
`calls, imports, reads, writes, renders, flows_to, fetches, served_from, triggers, denied, allowed, requires,
authenticates, authorizes`.

**CORRECTION to the proof (Table A row 47): `requires` grain = CONCRETE, not abstract.** Source places it in
the `# code/infra (CloudEdge discriminators)` block (`:115`); its members are `ENCRYPTS_WITH / USES_OAC /
USES_OAI / USES_SG` (`:308-309`) -- substrate-specific infra preconditions. The proof's *binding* target
(`requires -> depends-on`) is right; only the grain label was wrong. This is not cosmetic: labeling a
concrete AWS-crypto edge "abstract" would elevate a substrate-specific term into the agnostic layer.

**THREE elevations the ontology makes are LEGITIMATE (not S5 forks) -- because they ride GRAIN:**
`denies (<- DENIED)`, `triggers (<- TRIGGERS)`, and the gate-family `allowed/authenticates/authorizes (-> guards)`
are CSE-CONCRETE primitives the ontology lifts to an abstract archetype. That is allowed **iff** the abstract
term is the GRAIN-PARENT (abstract superset-of concrete subtype -- the anchor's GRAIN nesting) and the concrete
CSE primitive STAYS in the enum as the adapter-grain form. No new CSE primitive is required for these; they are
re-layerings via grain. Record each as a grain-parent, not a new term.

---

## 2. The four edge cases (asked explicitly)

**(i) `depends_on` vs `consumes` (+ `requires`->depends-on vs a state-read) -- THREE distinct things, keep all.**
- `depends_on` (`:96`, abstract) = structural/behavioral need ("won't function without").
- `consumes` (`:98`, abstract) = runtime data-INTAKE.
- `reads` (`:106`, concrete) = a state-read -- the adapter-grain of `consumes`.
- `requires` (`:115`, concrete) = an infra PRECONDITION -- the adapter-grain of `depends_on`.
So `requires -> depends-on` is right, and it IS distinct from a state-read: a dependency is "needs to
exist/work"; a read is "pulls data at runtime." **D1 confirmed** (depends-on is a first-class primitive).

**(ii) `governs -> guards` -- RULE: NOT a clean rename; they are DISTINCT. Do NOT collapse governs INTO guards.**
- `governs` (`:100`, abstract) = the AUTHORITY/POLICY relation (`HAS_POLICY -> GOVERNS`, `:306`) -- "a Policy
  governs/constrains a resource." Static authority.
- `guards` = the runtime GATE relation -- the Guard role denies/allows/authenticates/authorizes a flow (the
  abstract parent of `denied/allowed/authenticates/authorizes`).
The proof (Table A rows 43,50,51,52) binds BOTH `governs` AND `allowed/authenticates/authorizes` to the single
`guards` archetype -- that **over-collapses**: governance != gating. **My ruling: split the proof's one
`guards` archetype into two -- `{governs = policy/authority}` and `{guards = gating}`.** governs stays its own
abstract relationship; guards is the abstract parent of the gate primitives. This also keeps `governs` NARROW
(policy authority), which is what frees the C-1 custody split below -- `owns` must not be lumped where
`governs` already lives. **-> CTO gate: two archetypes, not one.**

**(iii) `references -> resolves-through` -- RULE: a ROLE-scoped specialization of `references`, NOT a new
relationship primitive.**
- `references` (`:95`, abstract) = a static name/identity reference.
- `resolves-through` = the RUNTIME indirection hop (a call resolves through a Router/Gateway/Registry/SecretRef).
The distinction is carried by the target node's ROLE (AXIS-3), not by a new edge type. **Keep `references` as
the CSE primitive; `resolves-through` = `references` where the hop node's Role in {Router, Gateway, Registry}.**
If the ontology wants the surface term, it is an alias of `references` + a role-predicate -- recorded, never a
CSE fork.

**(iv) `derives_from` vs `flows_to` -- RULE: DISTINCT, keep both, correct as-is.**
- `derives_from` (`:101`, abstract) = provenance/logical derivation ("silver derives from bronze").
- `flows_to` (`:109`, concrete) = field-grain physical data movement -- the TSGRAPH `FLOWS_TO` carrying
  `EdgeKind` (passthrough/rename/recompute-guarded, `:146-154`).
`flows_to` binds UP to `derives-from` at abstract grain. **The KIND must NOT be lost in the elevate** -- it is
the field-grain spread-bug detector (the thing a regex cannot see; CTO-parity-signed 961/961). So:
`derives_from` = abstract provenance; `flows_to` = its concrete adapter form that carries KIND.

---

## 3. C-1 `owns` -- the sharp ruling (governed, per S5)

**Grounding:** `OWNED_BY -> Relationship.GOVERNS` (`:306`, lumped with `HAS_POLICY`); `OWNERSHIP` a Qualifier
(`:143`); the empirical sense-split cited by the coordinator -- `MS_FILE OWNED_BY MS_USER` (~4,582, custody)
vs `S3Key OWNED_BY S3_BUCKET` (~232, containment-inverse); `OWNED_BY` total ~5,845 (#2 edge).

**Core finding: `OWNED_BY`'s blanket `-> GOVERNS` map is LOSSY and semantically wrong.** governs = policy
authority; owns/custody = accountability; contains = composition. Three distinct senses are collapsed into one
primitive. The ~5,845 `OWNED_BY` edges are NOT one relationship.

**(a) Does CUSTODY split out of GOVERNS? -- YES.** `MS_FILE OWNED_BY MS_USER` (~4,582, the dominant sense) is
genuine custody/accountability -- a principal OWNS an artifact. That is not governance (a user does not
"govern" a file). **Add a governed CSE primitive `OWNS`** (abstract; the custody/accountability relation) via a
**0.4 -> 0.5 schema bump, additive/back-compat.** This IS the ontology's empirically-forced `owns` -- landing
it as a GOVERNED CSE addition is precisely S5 ("files a governed CSE coverage-gap/promote, never an
ontology-local parallel"). **So the ontology's `owns` is VALIDATED -- as a CSE-governed primitive, not an
ontology-local one.**

**(b) Is the S3Key sense just `contains`? -- YES; already covered, NO new primitive.** `S3Key OWNED_BY
S3_BUCKET` (~232) is containment-inverse: a bucket CONTAINS a key. Re-map this sense (object is a Container:
S3Bucket/Table/Module/GraphScope/Tier) to `CONTAINS` (inverted) -- not `OWNS`, not `GOVERNS`. Aligns with
`comp_coverage_check.py:523`'s fine->coarse rollup (that is containment, and it belongs with `contains`).

**(c) Does OWNERSHIP stay a Qualifier, or also materialize as an edge? -- BOTH; they are orthogonal.**
The `OWNERSHIP` **Qualifier** (`:143`) is event/node METADATA ("under what ownership was this change/node") --
same axis as `AUTHORITY/VISIBILITY/STABILITY`. The `OWNS` **edge** is a node->node RELATION ("A owns B"). Two
different questions on two different axes -> no collision. **Direct in-schema precedent: `AUTHORITY` is a
Qualifier (`:140`) while `AUTHORIZES` is a Relationship (`:117`)** -- same word-family, two axes, both
first-class and non-redundant. `OWNS : OWNERSHIP :: AUTHORIZES : AUTHORITY`. **Keep both.**

**Executable form (the mapping-table change) -- disambiguate `OWNED_BY` by object-type:**
| `OWNED_BY` where object is... | maps to | status |
|---|---|---|
| Person / Organization / IAMRole (principal) | **`OWNS`** | NEW primitive (custody) |
| a Container (S3Bucket / Table / Module / GraphScope / Tier) | **`CONTAINS`** (inverse) | existing |
| (`HAS_POLICY`) | **`GOVERNS`** | unchanged -- genuine governance |

**Residual honesty (LAW-1):** ~5,845 - 4,582 - 232 = ~1,031 `OWNED_BY` edges are outside the two cited
buckets. They must be swept by the SAME (subject,object)-type rule at migration -- **NOT assumed all-custody.**
I have not measured that residual; the rule classifies it, I do not guess its split.

**Governance of execution (not mine to land).** The `OWNS` addition is a governed 0.4->0.5 version-bump:
CTO arch-gate (schema-vs-design) + CVO re-sign + COO SoD-land -- `org/modules/graph` is EXEC-locked, so I
author/own the DESIGN but do not commit the schema file myself (same SoD path as the 0.3 TYPE/SYMBOL and 0.4
PROMOTE bumps). Adding `OWNS` triggers the obligations in `MIGRATION_NOTE` (`:49`): a COMPUNIFY coverage-sweep
(all compilers must now handle `OWNS`) + a CSE-log materializer migration for the re-mapped `OWNED_BY` edges.

---

## 4. The ontology's non-CSE relationship terms -- S5 disposition

- **`routes-to` (D4): NO new CSE primitive.** It = `flows_to` (`:109`) where the source Role = Router;
  conditional forwarding is Role + predicate, not a relationship fork. `ROUTES_TO` already `-> FLOWS_TO`
  (`:298`). Keep `flows_to`; the Router role carries the distinction. (If a surface term is wanted, it is an
  alias, recorded -- so the proof's D4 resolves to "ontology-layer refinement," not a CSE enum add.)
- **`projects` (served_from -> projects): NO new CSE primitive.** `SERVED_FROM` (`:111`) is already
  first-class; `projects` is its abstract grain-parent (the serve boundary). Elevate via grain; keep
  `SERVED_FROM` as the adapter form. Do NOT collapse serve+render (the proof's catch is right: `served_from ->
  projects` and `renders -> consumes` stay distinct, or the `dangling_served` deviation dies).
- **`guards` (from Sec 2ii): NO new CSE primitive.** The abstract GATE archetype = grain-parent of
  `denied/allowed/authenticates/authorizes`; kept DISTINCT from `governs`.

---

## 5. Decisions for the CTO gate (one line each)

1. **Denominator:** 29 Entity / 23 Relationship; `routes-to` is outside the existing set (correct the proof's 28/24).
2. **RELATION split:** source 9-abstract / 14-concrete CONFIRMED; ONE correction -- `requires` = concrete (binds up to depends-on).
3. **Three elevations** (denies/triggers/gate-family) legitimate via GRAIN, not forks -- concrete CSE primitive stays; abstract term is its grain-parent.
4. **governs != guards:** split the proof's single `guards` archetype into `{governs = authority}` + `{guards = gating}`.
5. **resolves-through** = `references` + Router/Gateway/Registry role (no new primitive).
6. **derives_from vs flows_to:** distinct, both kept; KIND stays on `flows_to`.
7. **C-1 owns:** (a) ADD governed `OWNS` primitive [0.4->0.5, CTO-gated -- validates the ontology's `owns`];
   (b) S3Key sense = `contains` (no new primitive); (c) `OWNERSHIP` Qualifier AND `OWNS` edge both -- orthogonal
   (`AUTHORITY`/`AUTHORIZES` precedent).
8. **routes-to / projects:** no new CSE primitives (flows_to+Router / served_from grain-parent).

*Deferred to NFRA_ONTOLOGY/MSTR (their axes, not CSE's):* Entity->Role bindings (D5/D6/D7), Variance-vs-implements
(D3), Type/Symbol taxonomy scope-out (D8).

*-- 0.4.0_DS_ClientPlatform~B, cse_schema.py owner. Ruling for the base coherence anchor + the CTO arch-gate.*
