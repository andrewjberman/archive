# NFRA_ONTOLOGY -- Fixed-Points Coherence Anchor

**Owner: `0.8.0_AE_CloudComp` (base, coordinator).** Andrew-direct 2026-07-18: the ontology FIXED-POINTS
coherence routed to base (coordinator) rather than ~A (on the NFRA_GENESIS SDK). base LOCKS these + flags
drift; this is the single reference the ~C build + the CTO gate reconcile against. Not the design (that is
~C's DoR); this is the coherence layer ON it. Last reconciled: 2026-07-18 ~0700Z against @297c12bea.

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
| **Roles (13)** | Source, Store, Producer, Transformer, Consumer, Sink, Gateway, Guard, Router, Trigger, Registry, Container, **Observer** | Observer empirically forced (~305 MONITORS edges). 12->13. |
| **Relationships (12)** | produces, consumes, derives-from, depends-on, contains, guards, denies, triggers, routes-to, projects, resolves-through, **owns** | owns empirically forced (OWNED_BY 5,845 = #2 edge). 11->12. **SEE FLAG C-1.** |
| **Variance (6)** | Canonical, Twin, Variant, Fork-Shadow, Superseded, Orphan | base-confirmed, MSTR-endorsed. Mechanism @f904033ea (position_key = logical-identity only; structure COMPARED; allowed_facets). |
| **Lineage** | compositional (Role+Relationship grammar) | no ratification -- zero new primitives. |
| **C3 naming** | INHERITED from constituents: capability-cluster -> pipeline-thread -> resource-domain -> governed-catalog -> NEVER invented | @297c12bea. Same principle as C2 typing, applied to naming; deterministic, no-invent. |
| **Materialization (fog-4)** | archetype = an ATTRIBUTE on the EXISTING C2Motif/C3System, never a parallel node-type | ~A. Keeps the CVO-frozen semctl layer intact; materialization stays light. |

Empirical grounding commits: grain scan 6fae7e7a4; canonical motif catalog (~20 families) ef94dafda;
A+B materialize spec 7892f3fbc; C3 naming 297c12bea.

## COHERENCE FLAGS (base, as coherence-keeper)
- **C-1 (owns -- reconcile before locking on AXIS 2).** `owns` is on the RELATION axis, which the S5
  resolution binds to "CSE re-layered, no fork." But CSE does NOT treat ownership as a free relationship:
  `cse_schema.py` already maps `OWNED_BY -> Relationship.GOVERNS` (coarse) AND carries `OWNERSHIP` as a
  first-class **Qualifier** (a DIFFERENT axis). So `owns` is NOT a clean coverage-gap -- it collides with
  two existing CSE treatments. Resolution options (a CTO + CSE-owner item, per S5): (i) keep OWNED_BY as
  `governs` (but ownership != governs semantically, and 5,845 edges argues it is too distinct to lump);
  (ii) split `owns` out of `governs` via a GOVERNED CSE schema bump (the honest option if it is genuinely
  distinct) AND reconcile against the `ownership` Qualifier (edge-form vs metadata-form). `owns` must NOT
  lock as an ontology-local relationship until this routes through CSE. **The empirical case for `owns` is
  strong; the AXIS/mechanism is the open question.**
- **C-2 (Observer 13th Role + owns 12th Relationship are CTO-PENDING, not settled).** Both are the
  empirical resolution of DoR open decisions -- strong justification, but they are the CTO closed-set
  ruling's to bless. Lock them as "empirically-grounded PROPOSED", not "ratified".
- **Coherent + no drift otherwise:** Roles-minus-Observer (12), Relationships-minus-owns (11), Variance (6),
  the C3 naming ladder, and fog-4 materialization all ride the elemental frame with zero shared term left
  implicit. The GRAIN/ARITY distinction (elemental precision) must survive into ~A's formal render.

## NFRA_GENESIS seam
~A's per-company adapter + the manifest's no-per-tenant-algebra-fork invariant sit on THIS seam (the
RELATION-axis re-layering). Keep coherent: a per-tenant/per-company binding is an ADAPTER instance, never a
fork of the agnostic algebra -- the same S5 discipline. Any GENESIS adapter change re-checks against this
anchor.

*-- 0.8.0_AE_CloudComp (base, coordinator). Coherence anchor; reconcile the ~C build + CTO gate against it.*
