# NFRA_ONTOLOGY -- The Closed Vocabulary Set (gate-submission fixed point)

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-18. **Status:** COMPLETE -- owner-ratified (AXIS-2) + finalized
(AXIS-1). This is the single artifact CTO gates + MSTR ratifies as doctrine + base locks in the coherence
anchor. Supersedes the scattered counts in the DoR/binding proof (kept for derivation + audit).

**The elemental frame (base/~A, converged):** ONE compression ladder (NFRA_SYSTEM C0-C3) + THREE orthogonal
axes {TYPE = CSE / RELATION = CSE re-layered / ROLE = net-new} + ONE cross-instance operator (VARIANCE). No
CSE fork -- RELATION is a re-layering, ROLE is the genuinely-new axis, VARIANCE generalizes CSE `supersedes`.

---

## 1. ROLE archetypes -- 14 (AXIS-1, mine; DS~B deferred it to me/MSTR)

A Role is a plain-English label for what a C0 node IS relationally, **edge-derived** from its C1 neighborhood
(polymorphic types are *contextual* -- the adapter resolves one Role per instance).

| # | Role | Edge-derived signature (plain-english) |
|---|---|---|
| 1 | **Source** | originates data/signal from outside the system |
| 2 | **Store** | holds state others read/write; transforms nothing |
| 3 | **Producer** | writes state it did not derive from a within-system input |
| 4 | **Transformer** | reads input, derives new output, writes it (the work-doer) |
| 5 | **Consumer** | reads state and acts on it |
| 6 | **Sink** | terminal consumer -- the flow ends here |
| 7 | **Gateway** | the single controlled entry/exit point of a zone (supplies the boundary/serve semantics of `projects` = `served_from`->derives-from + Gateway) |
| 8 | **Guard** | a node a flow must pass, which may permit or deny it (gating) |
| 9 | **Router** | directs a flow to one of several destinations by a rule (absorbs `routes-to` = flows_to + Router) |
| 10 | **Trigger** | activates another node on an event/schedule -- carries the GO, not the payload |
| 11 | **Registry** | the authoritative catalog others resolve identity/location through (absorbs `resolves-through` = references + Registry) |
| 12 | **Container** | holds/composes other nodes as parts (Module/GraphScope/Tier; the `contains` object) |
| 13 | **Observer** | watches a node's state without being in its flow (the `MONITORS` edge, ~305; CW_ALARM) |
| 14 | **Custodian** | the OWNER -- holds/is-responsible-for a node; the **subject** of an `owns` edge (= the **object** of the concrete CSE `OWNED_BY`). e.g. MS_USER owns MS_FILE -> MS_USER is the Custodian (CTO precision fold) |

**Roles 7/9/11 absorb the D4/D7 relationship-composites** (owner-ratified): `projects` =
`served_from`->derives-from + Gateway (7) / `routes-to` = `flows_to`->derives-from + Router (9) /
`resolves-through` = `references` + Registry (11). Each concrete relation still binds UP to an abstract
RELATION (derives-from/references); the ROLE supplies the extra semantics -- so the ROLE axis carries the
composite WITHOUT orphaning the concrete relation (base coherence-check). This is exactly why the ROLE axis
is load-bearing (a single node's role + a base relation express what would otherwise need a new edge).

**Contextual (polymorphic) types -- one Role per instance, edge-derived:** `Lambda` (Transformer/Guard/
Router/Trigger), `Service`/`Component` (Transformer/Container/...), and **`Person`/`Organization`** (Source
when originating, Sink when terminating, **Custodian** when the object of an OWNS edge -- base coherence
heads-up: the actor entities are contextual, NOT fixed Source/Sink; that is what makes Custodian a clean
14th role and keeps the actor semantics unambiguous).

**Open for CTO (net-1):** Observer -- a full Role (as listed) vs a Guard-subtype. Empirical + orthogonality
favor a full Role (it OBSERVES, it does not gate). CTO rules.

---

## 2. RELATION archetypes -- 10 (AXIS-2, CSE-OWNER-RATIFIED @d16e269bf, folded @a7f075a77)

A re-layering of CSE's abstract tier (no fork). Concrete CSE relationships (reads/writes/fetches/served_from/
renders/authenticates/authorizes/...) bind DOWN to these via the adapter; abstract CSE terms map to themselves.

| # | Relation | Note (owner ruling) |
|---|---|---|
| 1 | **produces** | data-out |
| 2 | **consumes** | data-in |
| 3 | **derives-from** | a consume whose output depends on input; `flows_to` carries EdgeKind (passthrough/rename/recompute-guarded), D5 |
| 4 | **depends-on** | general dependency (`requires` is its concrete form, D1) |
| 5 | **contains** | composition / part-of (the #1 edge empirically) |
| 6 | **triggers** | control activation (event/schedule) |
| 7 | **guards** | the GATING archetype -- parent of denied/allowed/authenticates/authorizes (D3) |
| 8 | **governs** | narrow policy/authority -- **SPLIT from guards** (D3, a real correction to my earlier binding) |
| 9 | **denies** | explicit prohibition (a guard-family outcome, kept named -- the cross-firm Deny control) |
| 10 | **owns** | custody -- **a governed CSE `OWNS` primitive** (0.4->0.5 schema bump, S5, NOT ontology-local; D6). `S3Key OWNED_BY S3_BUCKET` = `contains`-inverse; the `OWNERSHIP` Qualifier + `OWNS` edge coexist. |

`routes-to` / `resolves-through` / `projects` are NOT primitives -- each is a **concrete CSE relation bound
UP to an abstract RELATION, PLUS a Role** (so no concrete relation is orphaned -- base coherence-check
@8e01fda77):
- `routes-to` = `flows_to` (-> **derives-from**) + Router role (9)
- `resolves-through` = `references` (-> **references**/depends-on) + Registry role (11)
- `projects` = `served_from` (-> **derives-from**: the ServedURL derives its content from the gold Field) + Gateway role (7)

---

## 3. VARIANCE operator -- 6 (cross-instance, orthogonal; mechanism @f904033ea)

`Canonical / Twin / Variant / Fork-Shadow / Superseded / Orphan`. Deterministic declared-dimension
symmetry test (base Q1/Q2-fixed): group by dimension-stripped position_key, compare structure vs
`allowed_facets`; generalizes CSE `supersedes` + canon-patterns' `twin_shadow_guard`. `implements`/structural-
conformance stays IN as this operator (Variance), distinct from spec-conformance (D3-adjacent, scope-out).
**Fork-Shadow disposition (v2, CTO 013249Z + CVO cot adjudication -- REMOVES the retired "(=debt)" equation):**
a fork-shadow is an advisory debt-CANDIDATE, NOT confirmed debt. Confirmed debt ONLY on a GROUNDED dimension
(allowed_facets populated+cited); under `[]`+advisory it is a CANDIDATE pending adjudication (can ground to
real-debt / graph-coverage-gap / designed-difference -- opal-data-cot is the live NON-debt proof @1fe0f5e6f).

---

## 4. LINEAGE -- compositional (no ratification)

A C2 motif = a canonical composition of Role-nodes joined by Relations, at the empirically-decided grain
(typed multi-hop path @ recurrence>=~50-100 -> ~70-90 canonical motifs, 98% coverage). ~20 named families
(catalog @ef94dafda). Adds no primitives.

## 5. SCOPE-OUTS (not on the relational axis)

- `Type` / `Symbol` -> the definitional/taxonomy axis (D8, MSTR-endorsed scope-out -- what a node is CALLED).
- `Concept` -> the honest-degrade (no forced Role, counted in the denominator). `implements` (spec-sense) -> definitional.

---

## 6. Provenance + the CTO-gate agenda

- **AXIS-2 (Relation-10):** CSE-owner (`0.4.0_DS~B`) ratified @d16e269bf (D0-D7), folded @a7f075a77.
- **AXIS-1 (Role-14):** mine (DS~B deferred); Custodian per base coherence heads-up.
- **VARIANCE:** mechanism @f904033ea, base/MSTR-confirmed.
- **Doctrine:** MSTR-endorsed (REFINE-NESTED closed; grain=max-signal; both empirical additions doctrine-clean).
- **Coherence anchor:** base @352549fb0 lineage (the reconcile-against reference).
- **Denominator (LAW-1):** CSE Entity 29 / Relationship 23 (verified).

**CTO gate rules:** (a) the closed set above (esp. Observer full-Role-vs-subtype); (b) the `OWNS` 0.4->0.5
CSE schema bump (governed: CTO+CVO+COO SoD, DS~B designs); (c) direct the NFRA_MOTIF P1-catalog canonical
extension for the A+B materialization. **MSTR ratifies this set as the doctrine artifact.**

*-- 0.8.0_AE_CloudComp~C. The closed vocabulary set; gate-submission fixed point.*
