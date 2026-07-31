# WS-C1 DELIVERABLE CONTRACT: THE LIFECYCLE AXIS AND THE TYPE SYSTEM

**Workstream:** NFRA_VELOCITY / CORE, WS-C1 -- rails D1/D2/D3 plus the lifecycle axis.
**Design + gate:** `1.0.0_SA_CTO~Z`. **Build:** `0.8.0_AE_CloudComp~C`. **Verify:** `3.0.0_SA_CVO~Z`.
**Status: COMPLETE** (P1, closed clause by clause).

## AUTHORITATIVE vs DERIVED

**SOURCE OF RECORD: `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml`** -- the single vocabulary
carrier, exec-locked, landed only by the gate owner.
**`docs/architecture/NFRA_VELOCITY_CORE_TYPE_DICTIONARY.md` IS DERIVED** and says so at its line 5:
*"This document is DERIVED. The YAML is authoritative; where they disagree, the YAML wins and this
file is wrong."* **This contract is derived from both.**
**That subordination clause is why a file titled CANONICAL is safe** -- it is the difference between
a rendering and a fork, and it was the gating condition on landing the dictionary at all.

## WHAT WS-C1 WAS OBLIGED TO PRODUCE, AND WHERE EACH PIECE LIVES

| Obligation | Artifact | Vintage |
|---|---|---|
| The D3 lifecycle axis in the rule bank | `NFRA_ONTOLOGY_RULE_BANK.yaml` v1.7 -> v1.8 | `@880f527cc` |
| Enforcement on the kill-list path | `org/modules/graph/comp_legacywriter.py` | `@b5854411b`, repaired `@88bf8f7bb` |
| The design spec | `../WS-C1_LIFECYCLE_DESIGN_SPEC.md` | rev 4 `@50643084b` |
| Published definitions + schemas (Andrew-direct) | `docs/architecture/NFRA_VELOCITY_CORE_TYPE_DICTIONARY.md` | landed by gate owner |
| Round 2 -- the `layer` axis ruling | `../WS-C1_ROUND2_LAYER_AXIS_RULING_20260731.md` | landed |
| The rule bank's consumer set | `../WS-C1_RULE_BANK_CONSUMER_ENUMERATION_20260731.md` | landed |
| The lifecycle-VALUE gate boundary | `../WS-C1_LIFECYCLE_VALUE_GATE_BOUNDARY_20260731.md` | `@d0fa2c55a`, amended `@3ec69a0b1` |

## WHAT IS DELIVERED

**A seven-value `lifecycle_class`** with `TRANSIENT` and `DORMANT` explicit, **per-value polarity**
(a detector must run the OPPOSITE predicate, not skip), per-value decay, and `contract_record` as a
required/optional field schema. Four typed violations. Nine licensed derivations. The held-out fence.

**`UNDECLARED` IS THE LOUD DEFAULT, AND THAT IS THE LOAD-BEARING DESIGN DECISION.** With a
claim-vs-check bound: the tool may CHECK under UNDECLARED but may not CLAIM. It emits
`ABSENT (lifecycle UNDECLARED)` and never `DEAD`.

## THE BOUNDARY THAT NOW GOVERNS THIS WORKSTREAM -- ANDREW-DIRECT

> *"It is impossible to know the Lifecycle Value of the resource without the user input pipeline you
> are building."*

**The MECHANISM is complete and continues. POPULATING per-resource VALUES is GATED** behind the Kimi
user-input pipeline, with `0.7.0_AE_CloudOps~B` as named future owner **outside CORE**. No
value-population seat is stood up.

**C1 SURVIVES THAT GATE STRUCTURALLY, NOT LUCKILY.** Live census: **438 UNDECLARED, 0 GATED, deadness
NOT ASSERTED.** Had the default been `PERMANENT`, the gate would have left the estate silently
mis-typed for its whole duration. **`contract_record.required` carries `intent_source`, so
populating-without-knowing is UNWRITABLE in the grammar** -- the gate was enforced by a required
field before it was stated.

**OPEN, ROUTED TO ANDREW, UNANSWERED:** does *populating lifecycle values* reach a value read off an
existing ratified document, or only one that must be decided?

## KNOWN GAPS, STATED RATHER THAN CLOSED

- **The rule bank cannot enumerate its own readers.** The enumeration closes the stale-reader class
  **for Python only** (28 non-`.md` files name the bank against 12 Python ones). **The
  forked-vocabulary class -- same concepts, different words -- has NO INSTRUMENT and none is claimed.**
- **`comp_debt/dormant_guard.py` runs a convergent vocabulary** -- its own `DORMANT` states and
  `revalidate_by` decay, never referencing the bank. **One vocabulary silently forked, or two with
  nothing recording the decision.** Unresolved.
- **`locality` is ratified but under-exercised** (`enum_exercised`: one of three values ever used).
- **A token cannot carry its rail.** `scope` is live in `type_tuple` and retired in `contract_record`;
  the reader-mirror must be `(section, field)`-keyed, never `field`-keyed.
