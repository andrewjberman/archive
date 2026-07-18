# OWNS 0.4->0.5 CSE Schema-Bump -- Archetype Requirement (ontology half; DS~B implements)

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-18. **Status:** DRAFT -- the ONTOLOGY-REQUIREMENT half (my lane).
**DS~B (cse_schema.py owner) writes the concrete bump** from this requirement. CTO GO @140753Z.
**SEQUENCING (CTO guardrail):** DS~B is fired NOW on the higher-priority P1-catalog canonical-extension (the
A+B materialization trigger); **this OWNS-bump folds BEHIND that** for DS~B (no concurrent cse_schema.py-adjacent
edits -- module/attention collision). I supply the requirement anytime; DS~B designs after the P1-extension
emit hands off. **Landing = governed cycle:** CTO arch-gate (of the concrete spec) -> CVO re-sign ->
COO/exec single-editor land (org/modules/graph EXEC-locked; same path as 0.3 TYPE/SYMBOL, 0.4 PROMOTE). NOT
gated by LD-0311 (a downstream governed change).

---

## 1. What the ontology requires (the archetype half)

The ratified vocabulary (LD-0311) carries **`owns`** as a first-class RELATION and **Custodian** as a Role.
CSE currently has NO clean home for custody (`cse_schema.py:306` maps `OWNED_BY -> Relationship.GOVERNS`,
lumped with `HAS_POLICY`). The bump must give custody its own primitive so the ontology's `owns`/Custodian
bind to a real CSE edge -- NOT to overloaded `GOVERNS`.

**Requirement R1 -- add a governed `OWNS` Relationship primitive.** A new `cse_schema.Relationship.OWNS =
"owns"` enum member. Semantics (plain-english, for the enum docstring): *A holds / is-responsible-for B* --
the custody/stewardship relation (an actor OWNS a resource). Version 0.4 -> 0.5 (additive, enum-extend).

**Requirement R2 -- re-map `OWNED_BY` custody sense OUT of GOVERNS, onto OWNS.** The edge->Relationship map
(`:306`) must move the CUSTODY sense of `OWNED_BY` from `GOVERNS` to `OWNS`. This is FREED by the D3
narrow-governs split (already owner-ratified @d16e269bf): `governs` = narrow policy/authority only, so custody
no longer belongs there.

**Requirement R3 -- disambiguate `OWNED_BY`'s polysemy (target-typed).** `OWNED_BY` is polysemous (the root of
the C-1 collision):
- `MS_FILE OWNED_BY MS_USER` (4582), `MS_FOLDER OWNED_BY MS_USER` (1031) -> **custody** -> `OWNS` (target is a
  Person/Organization/actor).
- `S3Key OWNED_BY S3_BUCKET` (232) -> **containment-inverse** -> `contains` (target is a Container; NO new
  primitive -- this is the fine->coarse rollup `comp_coverage_check.py:523` already uses).
So the map is TARGET-TYPE-CONDITIONED: `OWNED_BY -> OWNS` when the object is an actor entity; `OWNED_BY ->
CONTAINS`(inverse) when the object is a container. DS~B chooses the mechanism (a conditioned map entry, or a
resolve-time disambiguation) -- the REQUIREMENT is that both senses resolve correctly, not one lumped.

**Requirement R4 -- the `OWNERSHIP` Qualifier and the `OWNS` edge COEXIST.** `cse_schema.py:143` carries
`Qualifier.OWNERSHIP` (a per-node attribute axis). It stays; the `OWNS` edge (a relation axis) is added
alongside -- the two are orthogonal (a node CAN carry an ownership Qualifier AND be the object of an OWNS
edge), exactly the `AUTHORITY`:`AUTHORIZES` precedent (a Qualifier + a Relationship naming related concepts).
Do NOT collapse them.

## 2. The ontology bindings this unblocks (what consumes OWNS)

- **Relation `owns`** (rule bank `relations.owns.binds_up: [OWNED_BY]`, custody sense) -> the CSE `OWNS`
  edge. (The rule bank @967f23fe1 already anticipates this; it re-points from GOVERNS to OWNS on land.)
- **Role `Custodian`** (14th) = the OWNER = the **subject** of `owns` (= object of `OWNED_BY`); edge-derived,
  contextual for Person/Organization/MS_USER.
- **The M365/custody plane** (D-CUSTODY, ~28% of node mass) becomes describable -- currently undescribable
  without custody.

## 3. Denominator / grounding (LAW-1)

- `OWNED_BY` = 5,845 edges = the #2 relationship in the graph (comp-kuzu @2026-07-18T02:18Z). Custody sense:
  `MS_FILE/MS_FOLDER OWNED_BY MS_USER` = 5,613; containment-inverse: `S3Key OWNED_BY S3_BUCKET` = 232.
- CSE-owner ruling: D6 @d16e269bf (owns VALIDATED as a governed CSE primitive, S5, not ontology-local).

## 4. Handoff

- **DS~B:** own the concrete cse_schema.py bump (the enum add + the target-conditioned edge-map + the version
  0.4->0.5 + any validator update) from R1-R4. Sequence BEHIND the P1-extension. Ping me if a requirement is
  ambiguous.
- **CTO:** arch-gate the concrete spec; route the governed landing cycle (CTO gate -> CVO re-sign -> COO/exec
  single-editor land).
- **me (~C):** this requirement; verify post-land that `owns`/`Custodian` bind to the new OWNS edge (the rule
  bank re-point) + the two OWNED_BY senses resolve correctly.

*-- 0.8.0_AE_CloudComp~C. OWNS-bump archetype requirement; DS~B implements the concrete cse_schema.py change.*
