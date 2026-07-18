# NFRA_ONTOLOGY -- Fixed-Points Coherence Anchor

**Owner: `0.8.0_AE_CloudComp` (base, coordinator).** Andrew-direct 2026-07-18: the ontology FIXED-POINTS
coherence routed to base (coordinator) rather than ~A (on the NFRA_GENESIS SDK). base LOCKS these + flags
drift; this is the single reference the ~C build + the CTO gate reconcile against. Not the design (that is
~C's DoR); this is the coherence layer ON it. **>> LOCKED -- gate-submission fixed point: `NFRA_ONTOLOGY_CLOSED_SET.md` @96e86c8a4.** base whole-set
coherence-check **PASS** 2026-07-18 ~0756Z: ONE fix returned (served_from orphaned from the RELATION axis) +
folded (`served_from`->derives-from + Gateway role; set stays 10, no concrete relation orphaned). Custodian
(14th Role) folded per the base heads-up (Person/Org CONTEXTUAL). AXIS-2 CSE-owner-ratified (DS~B @d16e269bf).
MSTR doctrine PASS on the principles; **LD-0311 lands on this PASS + the CTO-gate-close.** ~C submitting to
CTO in parallel. Last reconciled: 2026-07-18 ~0756Z against @96e86c8a4.

## The elemental frame (the coherence invariant everything must ride)
**1 LADDER + 3 ORTHOGONAL AXES + 1 OPERATOR** (~A's cut, converged 1:1 with ~C's DoR v0.2):
- **LADDER** (NFRA_SYSTEM, the mechanism): C0 object -> C1 edge -> C2 motif -> C3 system; deterministic
  promotion (recurrence>=2; connected-component>=2); fidelity-gated. NOT a vocabulary.
- **AXIS 1 TYPE** (CSE entity-kind). Owner NFRA_SYSTEM.
- **AXIS 2 RELATION** (abstract relationships) = CSE's OWN abstract tier RE-LAYERED (elevate agnostic,
  demote concrete to the adapter). Shared terms identical-by-design. **CSE charter S5 binds: a recognizer
  never forks its own primitive -- new terms file a governed CSE coverage-gap/promote, never an
  ontology-local parallel.**
- **AXIS 3 ROLE** (relational position). Owner NFRA_ONTOLOGY. Net-new + orthogonal (CSE has no position
  classification). A node carries BOTH a TYPE and a ROLE.
- **OPERATOR VARIANCE** (cross-instance comparison). Owner NFRA_ONTOLOGY.
- **THREE distinct nestings, never merged:** GRAIN (abstract-superset-concrete SUBTYPE, on the TYPE+RELATION
  axes = fog-1's resolution) / ARITY (C0->C3 composition = the ladder) / SCOPE (the ladder reapplied at a
  higher scope = fractal). Grain is IS-A; arity is IS-MADE-OF; scope REAPPLIES -- three different objects.

## Fixed points (LOCKED @297c12bea -- pending CTO closed-set gate)
| Set | Fixed point | Grounding |
|---|---|---|
| **Roles (14, FINAL @96e86c8a4)** | Source, Store, Producer, Transformer, Consumer, Sink, Gateway, Guard, Router, Trigger, Registry, Container, Observer, **Custodian** | Custodian = the OWNS-target actor (Person/Org now CONTEXTUAL, not fixed Source/Sink -- base heads-up folded). Gateway/Router/Registry absorb projects/routes-to/resolves-through (each = a concrete relation -> abstract RELATION + a Role; `served_from`->derives-from+Gateway, base coherence-check). **Observer full-Role-vs-Guard-subtype = the ONE open CTO item.** |
| **Relationships (10, OWNER-RATIFIED @a7f075a77)** | produces, consumes, derives-from, depends-on, contains, triggers, **guards**, **governs**, denies, **owns** | DS~B ruling (below): guards/governs SPLIT (2, not 1 -- governance != gating); `owns` = governed CSE primitive (0.4->0.5 bump, S5); routes-to / resolves-through / projects RE-HOMED to Role-composites (NOT primitives). C-1 RESOLVED. Supersedes the pre-ruling 12-set. |
| **Variance (6)** | Canonical, Twin, Variant, Fork-Shadow, Superseded, Orphan | base-confirmed, MSTR-endorsed. Mechanism @f904033ea (position_key = logical-identity only; structure COMPARED; allowed_facets). |
| **Lineage** | compositional (Role+Relationship grammar) | no ratification -- zero new primitives. |
| **C3 naming** | INHERITED from constituents: capability-cluster -> pipeline-thread -> resource-domain -> governed-catalog -> NEVER invented | @297c12bea. Same principle as C2 typing, applied to naming; deterministic, no-invent. |
| **Materialization (fog-4)** | archetype = an ATTRIBUTE on the EXISTING C2Motif/C3System, never a parallel node-type | ~A. Keeps the CVO-frozen semctl layer intact; materialization stays light. |

Empirical grounding commits: grain scan 6fae7e7a4; canonical motif catalog (~20 families) ef94dafda;
A+B materialize spec 7892f3fbc; C3 naming 297c12bea.

## COHERENCE FLAGS (base, as coherence-keeper)
- **C-1 (owns) -- RESOLVED by the CSE OWNER RULING (DS~B @d16e269bf; see below).** `owns` is VALIDATED as a
  governed CSE `OWNS` primitive (0.4->0.5 bump, exactly S5 -- NOT ontology-local), custody split out of
  `governs`; polysemy disambiguated (principal->OWNS, container->CONTAINS, policy->GOVERNS); the OWNERSHIP
  Qualifier + the OWNS edge COEXIST (precedent: AUTHORITY:AUTHORIZES). No longer an open flag.
- **C-2 (Observer 13th Role + owns 12th Relationship are CTO-PENDING, not settled).** Both are the
  empirical resolution of DoR open decisions -- strong justification, but they are the CTO closed-set
  ruling's to bless. Lock them as "empirically-grounded PROPOSED", not "ratified".
- **Coherent + no drift otherwise:** Roles-minus-Observer (12), Relationships-minus-owns (11), Variance (6),
  the C3 naming ladder, and fog-4 materialization all ride the elemental frame with zero shared term left
  implicit. The GRAIN/ARITY distinction (elemental precision) must survive into ~A's formal render.

## CSE OWNER RULING (0.4.0_DS_ClientPlatform~B, @d16e269bf -- Andrew brought in; the AXIS-2 authority)
Authoritative, source-line-cited. Folded here as the coherence-of-record for AXIS 2:
- **D0 DENOMINATOR (LAW-1):** the real enum is **Entity=29 / Relationship=23** (not 28/24). ~C's proof miscounted (prose 28, table 29) and folded `routes-to` into "24" though it is NOT a CSE member. Same 52 total; the completeness denominator reads **29/23**. ~C to correct.
- **D1 RELATION split CONFIRMED** (9 abstract :94-102 / 14 concrete :104-117), ONE fix: `requires` is **CONCRETE** (:115), not abstract. ~C's `requires->depends-on` binding is right; only the grain label was off.
- **D2 the three elevations** (denies<-DENIED, triggers<-TRIGGERS, gate-family) ride GRAIN (abstract=grain-parent, concrete primitive STAYS adapter-grain) -- **legitimate, not S5 forks**; no new CSE primitive.
- **D3 `governs` != `guards` -- SPLIT (correction).** ~C (and base's earlier read) bound BOTH `governs` and allowed/authenticates/authorizes to one `guards` archetype -- an OVER-COLLAPSE (governance != gating). Split: `governs` = policy/authority (NARROW); `guards` = gating (parent of denied/allowed/authenticates/authorizes). Narrow governs is also what frees `owns`.
- **D4 `resolves-through` = `references` + a Router/Gateway/Registry ROLE (AXIS-3)** -- not a new relationship. Keep `references`; no CSE fork.
- **D5 `derives_from` (abstract provenance) vs `flows_to` (concrete field-grain)** -- both kept; the **EdgeKind (passthrough/rename/recompute-guarded :146) MUST stay on flows_to** (the spread-bug detector).
- **D6 C-1 OWNS (the sharp one, RULED):** (a) custody SPLITS OUT -> add governed CSE `OWNS` (0.4->0.5 bump) -- `owns` VALIDATED, S5-correct, not ontology-local; (b) `S3Key OWNED_BY S3_BUCKET` (~232) = `contains` inverse (no new primitive; re-map); (c) `OWNERSHIP` Qualifier + `OWNS` edge BOTH (orthogonal; AUTHORITY:AUTHORIZES precedent). Migration disambiguates OWNED_BY by object-type (principal->OWNS / container->CONTAINS / HAS_POLICY->GOVERNS; residual ~1,031 swept by the (subj,obj)-type rule, not assumed all-custody).
- **D7 `routes-to` = flows_to + Router role; `projects` = served_from's abstract grain-parent** -- no new CSE primitives.
- **Governance:** the OWNS bump is CTO-arch-gated + CVO re-sign + COO SoD-land (org/modules/graph EXEC-locked; DS~B owns the DESIGN, does not land the file -- same path as 0.3 TYPE/SYMBOL + 0.4 PROMOTE). DS~B **DEFERS to base/MSTR**: the ROLE-axis (D5/D6/D7 of ~C's binding), Variance-vs-implements (~C-D3), Type/Symbol taxonomy (~C-D8) -- those are NOT CSE's axis.

**Coherence consequence:** AXIS 2 (RELATION) is now owner-ratified: `owns` lands as a governed CSE primitive (not a fork), `governs`/`guards` split, `requires` regrained, `resolves-through`/`routes-to`/`projects` = ontology-layer refinements. ~C folds D0-D7 into the binding proof; the OWNS bump routes to the CTO gate as a governed schema change. The ROLE-axis / Variance / Type-Symbol decisions remain base/MSTR + CTO (NOT CSE).

## NFRA_GENESIS seam
~A's per-company adapter + the manifest's no-per-tenant-algebra-fork invariant sit on THIS seam (the
RELATION-axis re-layering). Keep coherent: a per-tenant/per-company binding is an ADAPTER instance, never a
fork of the agnostic algebra -- the same S5 discipline. Any GENESIS adapter change re-checks against this
anchor.

*-- 0.8.0_AE_CloudComp (base, coordinator). Coherence anchor; reconcile the ~C build + CTO gate against it.*
