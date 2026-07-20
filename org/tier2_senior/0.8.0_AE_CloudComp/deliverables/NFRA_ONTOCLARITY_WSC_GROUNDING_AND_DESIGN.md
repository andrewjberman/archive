# NFRA_ONTOCLARITY WS-C -- Process deterministic tie-breakers: grounding + design (for COO/CTO review)

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-20. **TO:** `NFRA_ONTOCLARITY.WS-C.process-deterministic-tie-breakers`.
Inherits WS-A (root two-layer) + WS-B (crosswalk + comp-ontolint @65612d65f). **Gate path:** COO design review ->
CTO arch-gate (the spot-8 priority ordering) -> RAVC -> CVO SEMANTIC-verify each is DETERMINISTIC (same input ->
ONE answer, EXERCISED, not reworded).

## 1. Grounding -- the 3 PROCESS fogs (brief S3d), varying resolution states

| # | Fog | Grounded current state |
|---|---|---|
| 8 | **Polymorphic-Role resolution has NO tie-breaker (the GENUINE fog -- WS-C's main work).** A node matching 2+ role derive-rules (a Lambda that GUARDS and TRANSFORMS) resolves ambiguously. | `RULE_BANK.yaml:46` says "polymorphic types resolve ONE role per instance from edges (not a fixed binding)" -- but there is NO `priority` / `precedence` / `tie-break` anywhere (grep = 0). So WHICH role wins when 2+ derive-rules match is UNDEFINED -- prose heuristics, no ordering. |
| 9 | **The 3 incorporation modes -- LARGELY RESOLVED (~A's NESTEDABSTRACT domain).** | `PLAYBOOK.md:50-67` ALREADY defines the 3 modes (CTO arch-gate 2026-07-18): `shared-version-slot` / `per-tenant-template` / `sdk-capability` + a DECISION-RULE (`:65` "external governed dependency SDK reuses -> shared-version-slot; SDK's OWN code -> sdk-capability; TENANT's own declaration -> per-tenant-template") + 2 named traps (pin-advance / vocab-vs-executable). WS-C: REFERENCE this (do not duplicate ~A's PLAYBOOK), confirm the decision-rule is deterministic. ~A is PARKED post-wave (its session wound down); no ~A coordination needed since the rule exists. |
| 10 | **C2->C3 emergence ownership -- LARGELY PINNED already.** | `RULE_BANK.yaml:123` ALREADY defers: "emergence: NFRA_SYSTEM C2->C3 union-find (>=2 connected motifs); ontology CONSUMES it, does not re-implement." `01_substrate.md:11` authors the tier-transition (the /system representation). So ownership IS asserted (NFRA_SYSTEM owns; ontology consumes) -- the residual is only that 2 artifacts describe it. WS-C: crisp the deferral so 01_substrate CITES the ownership pin, not re-authors it. |

## 2. Design (each fog DETERMINISTIC -- same input -> one answer)

### spot-8 (the substantive deliverable): a deterministic Role PRIORITY ORDERING + a machine tie-breaker
- Add a `role_priority` ordering to `RULE_BANK.yaml` (the canonical source, WS-A) so a node matching N derive-rules
  resolves to exactly ONE role deterministically -- the highest-priority matched role wins.
- GROUNDING PRINCIPLE (the arch-decision -- my rec): **specificity/distinctiveness-first.** A node IS a flow role
  (Producer/Transformer/Consumer/...) BY DEFAULT when it produces/consumes (common); it is ALSO a specific
  structural/control role (Guard interposed / Router predicate / Registry resolve / Gateway boundary / Observer
  out-of-flow / Custodian owns) only when it carries that DISTINCTIVE rarer signature. The distinctive role names
  WHAT it does; the flow position is the fallback. So specific structural/control > general flow. Proposed order
  (high->low): Custodian, Observer, Gateway, Guard, Router, Registry, Trigger, Container, Transformer, Producer,
  Consumer, Source, Store, Sink. (Exact order = CTO's arch-decision; principle = specificity-first.)
- EXERCISED (CVO deterministic bar): extend `comp-ontolint` with a `role-resolve` check -- given a synthetic node
  matching 2+ derive-rules, it returns ONE role per the ordering + a self-test seeding a polymorphic node
  (guards+transforms -> Guard, deterministically) that FIRES if the resolution is ambiguous/wrong. Same input ->
  one answer, machine-proven.

### spot-9 (confirm, ~A's domain): reference the PLAYBOOK decision-rule
- Add a one-line CITATION in the ontology docs pointing at `PLAYBOOK.md` incorporation-mode decision-rule as the
  authority (do NOT re-state the 3 modes -- cite-not-copy, same as WS-A). Confirm it's deterministic (the :65 rule
  is a clean if/else on the artifact's home). No new artifact; ~A owns the PLAYBOOK (parked).

### spot-10 (crisp the pin): 01_substrate CITES the C2->C3 ownership, RULE_BANK already defers
- RULE_BANK:123 already says "ontology CONSUMES ... does not re-implement" (the pin holds). Crisp 01_substrate:11
  to CITE that NFRA_SYSTEM (`comp_ladder.py` + `NFRA_MOTIF_P2_c3_emergence.py`) OWNS the C2->C3 transition and the
  ontology consumes it -- one authoritative owner, the other references. No re-authoring.

## 3. Open item for COO -> CTO (1 arch-decision)
1. **spot-8 Role priority ordering:** approve the SPECIFICITY-FIRST principle + the proposed high->low order (or
   CTO's grounded alternative). Everything else is confirm/crisp (no new adjudication). [My rec: specificity-first.]

## 4. Land path
COO review -> CTO on the ordering -> build (RULE_BANK role_priority + comp-ontolint role-resolve check + self-test;
spot-9/10 citations) -> CTO arch-gate + WS-2 06-gate (RULE_BANK is a _SOURCE) -> RAVC -> CVO SEMANTIC-verify
(deterministic: one answer, exercised). Then WS-D (log the clarified defs; rides WS-4) -> ONTOCLARITY 4/4.
