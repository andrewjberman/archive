# NFRA_VELOCITY_CORE -- TYPE DICTIONARY (CANONICAL)

**Status:** CANONICAL reference for the Phase-1 type system.
**Source of record:** `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` @ `meta.version 1.8`.
**This document is DERIVED.** The YAML is authoritative; where they disagree, the YAML wins and this file
is the defect. Regenerate from the YAML, never edit the YAML to match this.

**Design owner:** `1.0.0_SA_CTO~Z` | **Built by:** `0.8.0_AE_CloudComp~C` | **Verified:** `3.0.0_SA_CVO~Z`
**Compiled:** 2026-07-31 by `2.1.0_SA_COO` (Andrew-direct: *"a dictionary of all types created in phase 1
persisted... in a canonical doc"*).

---

## 0. SCOPE OF THIS DOCUMENT

| Section | Contains |
|---|---|
| 1 | Provenance -- which types Phase 1 created vs inherited |
| 2 | The assertion tuple (4 axes) |
| 3 | D1 -- value / grain |
| 4 | D2 -- path / flow |
| 5 | D3 -- contract / obligation |
| 6 | `contract_record` schema |
| 7 | `lifecycle_class` -- the 7 values, both polarities, required fields |
| 8 | Typed violations |
| 9 | Licensed derivations |
| 10 | The held-out fence |
| 11 | Coverage boundary |

**Not in scope:** enforcement wiring, instance populations, build history. Those live in the workstream
logs and are deliberately excluded to keep this a definitions-and-schemas reference.

---

## 1. PROVENANCE

| Landed | Types | Under |
|---|---|---|
| **v1.8** | `contract_record`, `lifecycle_class` + polarity table, typed violations, lifecycle derivations, `held_out_fence` | **NFRA_VELOCITY WS-C1 / WS-C2 -- created in Phase 1** |
| v1.2 | D1 / D2 / D3 rails | NFRA_ONTOLOGY2 (predecessor, absorbed); **validated** by Phase 1's WS-C2 corpus walk |
| pre-v1.2 | C0-C3, 14 roles, 10 relations, `variance`, `completeness`, `type_tuple` | Ratified substrate, untouched |

**Additivity verified:** C0-C3 + 14 roles + 10 relations + `variance` + `completeness` are byte-identical to
the pinned pre-touch oracle `8f8a63200` (md5 `37e16648dc965424b75c14677927a636`).

---

## 2. THE ASSERTION TUPLE

Every tool answer and every question declares `(rail, grain, plane, scope)`. A mismatch is machine-detectable
rather than a silently wrong answer.

### 2.1 `rail`
```
enum: [C0, C1, C2, C3, D1, D2, D3]
```
| Value | Layer |
|---|---|
| `C0`-`C3` | STRUCTURE -- what exists, how it is wired |
| `D1` | DYNAMICS -- value / grain |
| `D2` | DYNAMICS -- path / flow |
| `D3` | DYNAMICS -- contract / obligation |

### 2.2 `grain`
```
enum:    [artifact, partition, row, field]   # coarse -> fine
forward: [row]                               # declared, not populated
```
| Value | Definition |
|---|---|
| `artifact` | A whole object / table / topic as a unit |
| `partition` | A dated or keyed slice of an artifact (e.g. an S3 object key) |
| `row` | A record within a partition (a DDB item, a parquet row) |
| `field` | A column / attribute of a record |

*A coarser answer to a finer question is the most common layer-mismatch defect.*

### 2.3 `plane`
```
enum: [source, projection, desired, applied, live, mixed, graph-cache]
```
| Value | Definition |
|---|---|
| `source` | Code AST |
| `projection` / `graph-cache` | A vintage'd graph read -- a projection, not live |
| `desired` | Declared config INTENT (Terraform, registry) |
| `applied` | The config as landed |
| `live` | The runtime plane observed now |
| `mixed` | Spans planes |

*Conflating `desired` and `applied` is the CLAUDE.md Rule-22a class.*

### 2.4 `scope`
```
enum: [estate, tree, firm, pipeline, motif, partition-window, single-artifact]
```
The **denominator boundary** an assertion is complete OVER. "Complete over FIRM" is not "complete over
ESTATE". `tree` = a firm's whole resource tree; `partition-window` = a dated slice for a freshness assertion.
*An assertion that does not name its scope has an unfalsifiable coverage claim.*

---

## 3. D1 -- VALUE / GRAIN

**Names:** the VALUE that travels an edge and the GRAIN at which it is resolved.
**Sits between:** C0 and C1.

### 3.1 `edgekind` -- what happens to a value crossing an edge
| Value | Definition |
|---|---|
| `passthrough` | Value crosses unchanged (identity) |
| `rename` | Same value, new name or field |
| `recompute_guarded` | Value re-derived under a guard or condition |

*Serialization note: the graph emits `recompute/guarded` (slash); the ratified token is
`recompute_guarded` (underscore). Same semantic; a producer serialization form.*

---

## 4. D2 -- PATH / FLOW

**Names:** a composed DIRECTED TYPED PATH -- the ordered hops a value takes, each hop's EdgeKind, the
transform at each, and the CADENCE the path is contracted to run at.
**Sits between:** C1 and C2. *A motif is a shape; a path is a shape with direction, transform and time.*

| Component | Definition |
|---|---|
| `hops` | Ordered list of edges, each a produces / consumes / derives-from at a D1 grain |
| `direction` | Native -- edges are directed |
| `transform_at_hop` | The hop's D1 `edgekind` |
| `cadence` | The contracted run-frequency. **Not a graph property** -- sourced from a D3 contract; forward where undeclared |

**Structural fact establishing the rail:** flow-edge properties are exactly
`{condition, dstField, kind, rename, resolution, srcField, via}`. There is **no cadence, no vintage and no
partition key on any flow edge.** Therefore freshness cannot be an edge property; it is necessarily derived
from flow plus contract.

---

## 5. D3 -- CONTRACT / OBLIGATION

**Names:** the OBLIGATION a motif or system carries.
**Sits between:** C2 and C3.

### 5.1 `obligation_types`
| Value | Definition | Violation |
|---|---|---|
| `delivery_cadence` | The path must deliver by a contracted time | Staleness -- never a wall-clock age |
| `completeness` | The assertion must cover a whole declared population | `Incomplete(missing=[...])` |
| `canonical_source` | A value originates from one blessed writer | Shadow-recompute / wrong-writer |
| `layer_grammar` | A layer does only its job (bronze / silver / gold) | A layer doing a later layer's job early |

### 5.2 The binding law
```
intent_from_above:      a D3 obligation is sourced from a governance level ABOVE the artifact
                        (registry / contract / law) -- NEVER the artifact's own config.
denominator_from_below: enumerated AT RUN TIME via a D2 path at a D1 grain -- the real instances,
                        never a frozen list, never the same artifact that supplied the intent.
gap_is_the_finding:     INTENT \ DENOMINATOR, printed every run. A zero gap is SHOWN, never assumed.
```
*An `intent_source` naming the artifact itself is rejected at declaration.*

---

## 6. `contract_record` SCHEMA

The record a contracted resource or process carries. **One record, two views -- never two schemas.**

```yaml
required: [intent_source, obligation, lifecycle_class, revalidate_by, locality]
optional: [successor, expiry_condition, cadence, vintage_probe, describes]
```

| Field | Req | Definition |
|---|---|---|
| `intent_source` | yes | WHERE the obligation comes from -- a governance level above the artifact. Naming the artifact itself is rejected. |
| `obligation` | yes | Which `obligation_types` bind. **Zero obligations is not "no obligation" -- it is UNDECLARED.** |
| `lifecycle_class` | yes | Exactly one `lifecycle.enum` value. PRODUCER-ASSERTED. |
| `revalidate_by` | yes | Decay date. A STALE declaration never auto-promotes. |
| `locality` | yes | WHERE the artifact is observable. *Renamed from `scope` -- the ratified `type_tuple.scope` means the denominator an assertion is complete-over; this means where a thing is observable. Two different properties, deliberately sharing no root.* |
| `successor` | no | The live replacement (required for `LEGACY`). |
| `expiry_condition` | no | Stated condition under which the obligation lapses. Must be machine-evaluable or it is decorative. |
| `cadence` | no | Contracted run-frequency (feeds D2). |
| `vintage_probe` | no | How to read when the value last moved. |
| `describes` | no | Free text: WHAT THE SUBJECT IS. **Explicitly non-vocabulary and not lint-checked.** Exists so prose has a designated home and stays out of vocabulary slots. |

### 6.1 Deliberate absence: there is NO population/scope field
**The absence is a prohibition, not a gap.** A `contract_record` is the subject's own declaration; a
population stated on it would be sourced FROM the artifact -- the denominator-is-its-own-configuration
defect, which is the single thing D3 exists to prevent. The population comes from a governed registry,
reached via `intent_source`, i.e. from above.

---

## 7. `lifecycle_class` -- THE CORE PHASE-1 TYPE

```
field: lifecycle_class
enum:  [PERMANENT, TRANSIENT, EVENT_CREATED, DORMANT, LEGACY, RETIRED, UNDECLARED]
```

**Names:** the SHAPE of a contracted thing's life -- not its current phase.
**PRODUCER-ASSERTED, never observer-inferred.** Any implementation inferring this from key names, directory
position or observed absence has rebuilt a name-pattern stopgap with more syntax.

### 7.1 The problem it solves
An existence check is asked a question about lifecycle that existence cannot answer. One "absent" symbol
stands for at least four states: never existed | existed and was deleted | absent right now by design |
not yet occurred. **Absence is not a state; it is a set of states, and no existence check can partition it.**
Re-observation does not help -- sampling harder makes you more confident and no more correct.

### 7.2 The polarity table (the deliverable)

| Value | Meaning | ABSENT at rest | PRESENT at rest | Required fields |
|---|---|---|---|---|
| `PERMANENT` | Present from creation onward | **FINDING** (missing) | Healthy; with a cadence, healthy iff vintage advances, else FROZEN | `intent_source` |
| `TRANSIENT` | Written -> consumed -> deleted; oscillates | **HEALTHY** | Healthy iff dwell < `max_dwell`; **STRANDED** beyond | `consumer`, `max_dwell`, `locality` |
| `EVENT_CREATED` | Absent until a triggering occurrence; append-only after | **HEALTHY** (zero occurrences) | Healthy; a non-append edit is an INTEGRITY finding | `creating_event`, `event_observable`, `locality` |
| `DORMANT` | Deliberately inactive, deliberately retained -- a rollback lever, an armed fallback | **FINDING** (a belt that vanished) | Healthy. **Zero traffic at rest is also HEALTHY** | `reason`, `rearm_condition`, `annotation_cite`, `revalidate_by` |
| `LEGACY` | A live successor exists; may still be READ | Per successor | Healthy to read; **a WRITE is LEGACY-WRITER** | `successor`, `intent_source` |
| `RETIRED` | Decommissioned by ruling; absence is correct and terminal | Healthy (terminal) | **FINDING** (incomplete decommission) | `retirement_ruling` |
| `UNDECLARED` | No lifecycle declared | UNKNOWN, loud | UNKNOWN, loud | -- |

> **Absence is HEALTHY on 2 of 7 rows and presence is a FINDING on 2 of 7 -- so a single-polarity existence
> detector is WRONG ON 4 OF 7, in the direction that proposes deleting live infrastructure.**
> A skip-list suppresses; a type inverts.

### 7.3 Falsifiers -- every value must be able to fail
| Value | You cannot declare it unless |
|---|---|
| `PERMANENT` | The default-looking value is still a claim from above, never the artifact's own config |
| `TRANSIENT` | You name an **exercised** consumer and a `max_dwell` bound to that consumer's cadence -- which creates the STRANDED finding that proves the declaration can still fail |
| `EVENT_CREATED` | There is an observable for the occurrence that is independent **of the artifact** and **of the instrument** that reported it |
| `DORMANT` | You state a `rearm_condition`. *A belt nobody can state the re-arm for is not a belt.* |
| `LEGACY` | The successor is LIVE and EXERCISED -- otherwise it is a deletion wearing the wrong label |
| `RETIRED` | A retirement ruling exists. *A retirement with no ruling is an outage with paperwork.* |
| `UNDECLARED` | n/a -- the honest absence of a claim. **Never silently resolves to `PERMANENT`.** |

### 7.4 Decay
`revalidate_by` is required on **every** declaration. A STALE declaration **suppresses the deletion-class
verdict and releases the observation** -- so a silencer cannot survive its own expiry, and expiry never
becomes evidence of death. Revalidation requires at least the declaration's own predicate.

### 7.5 Token hygiene
`SUPERSEDED` and `ORPHAN` are **deliberately absent** -- both are already-occupied tokens on the ratified
`variance` axis with different definitions. Two definitions on one token in one file is prohibited. The
lifecycle value is `LEGACY`; the typed violation is `SILENT_RESIDENT`.

---

## 8. TYPED VIOLATIONS

| Violation | Definition |
|---|---|
| `LEGACY_WRITER` | A write whose target is `LEGACY` with a live successor, or whose obligation has expired |
| `CLOBBER` | Two writers at one `(key, grain)` with no adjudicating `canonical_source` contract |
| `TRIGGER_MISSEQUENCE` | An edge firing against the D2 topological + temporal order |
| `SILENT_RESIDENT` | A C-SILENT resident: no enumerator traverses it, no predicate reacts |

*Provenance: `LEGACY_WRITER`, `CLOBBER` and the zombie/silent-resident shape derive from the DEBTLOOPS
memo. `TRIGGER_MISSEQUENCE` originates in the CORE PRD -- it stands on its own merits, but nothing may
cite the memo for it.*

---

## 9. LICENSED DERIVATIONS

Each is **defined as a derivation, never stored as a primitive.**

| Property | Defined as |
|---|---|
| `freshness` | D2 path + D3 cadence + upstream vintages + trading calendar |
| `provenance` | D1 grain + D2 path walked backward |
| `staleness_vs_frozen` | Vintage advancing along the path vs the value not moving |
| `blast` | D2 forward walk at a declared grain |
| `debt` | `expired_obligation` UNION `legacy_with_live_exercised_successor` |
| `stranded` | `TRANSIENT` and observed dwell > `max_dwell` |
| `incomplete_decommission` | `RETIRED` and present at rest |
| `frozen_vs_stale` | A `PERMANENT` with a cadence: non-advancing vintage (frozen) vs advancing but behind (stale) |
| `rolling` | `PERMANENT` + a declared cadence. **A derivation, deliberately not a class.** |

---

## 10. HELD-OUT FENCE

```
ADVI_PERFORMANCE and MDPF_GLOBAL are the HELD-OUT TEST SET.
They must not shape these rails.
```
- **No surface of either** may be used as a vocabulary example; no contract may be authored to make a rail
  look expressive.
- **Every rail author must publish their shaping corpus.** An unnamed shaping corpus is indistinguishable
  from a breached one.
- **Verifiable without breaching:** check a declared shaping corpus against a schema, never against the
  fenced projects. A fence whose enforcement requires the enforcer to breach it is not a fence.
- **Binds on** the causal path into rail authorship -- not on fabric, not on seat.
- **Lifted only by** Andrew or the CVO. Not by a rail author, not by a phase close, not by the release of an
  adjacent precondition.

> **Why it is stated inside the rail sections:** a breached held-out set looks exactly like a well-fitting
> rail -- the gap reads structurally zero and the fit reads excellent. **There is no downstream signal that
> fires.** The only control is not to touch them.

---

## 11. COVERAGE BOUNDARY

1. **Declaration coverage is ZERO INSTANCES at this landing.** The vocabulary is declared here; the instance
   population is ESTATE WS-E1's registry. Every estate resource is `UNDECLARED` today.
2. **The vocabulary is PROPOSED, not final.** Its stated acceptance is the WS-C2 corpus walk; the rule bank's
   own words are *"expect the enum to change; if it does not change at all, be suspicious of the walk."*
3. **Transience is unverifiable against the graph by construction** -- a written-then-deleted marker is not a
   durable object. Falsifiable only via its exercised consumer and cadence-bound `max_dwell`.
4. **`max_dwell` is currently unsatisfiable in practice** -- no consumer declares a delivery cadence yet, so
   every `TRANSIENT` declaration renders UNKNOWN-loud.
5. **`EXERCISED` is enforced by declarer honesty and review, not by machinery** -- no exerciser exists.
6. **`expiry_condition` machine-evaluability is unenforced** -- the grammar requires it; no gate checks it.
7. **`row` grain and the partition SCHEME are forward** -- declared, unpopulated.
8. **Most obligations are not in the graph** -- D3 is contract-sourced by construction.

---

## 12. OPEN AT REVIEW

1. **Is estate-wide `UNDECLARED` acceptable as an indefinite default?** Honest, but the axis answers UNKNOWN
   for everything until WS-E1 populates it.
2. **Seven values -- right size?** The walk kept all seven and collapsed `ROLLING` into a derivation.
3. **Does `contract_record` need a scope field after all?** Five ESTATE tranche-1 values carried the ratified
   `type_tuple.scope` sense into a record with no such field. Parked and marked; unresolved whether that is
   wrong usage or a second missing field.
4. **C7's boundary-declaration schema vs this grammar.** ESTATE WS-E5 predicts a boundary field the grammar
   does not carry. Ruled split: the record may carry the OBLIGATION TO DISCLOSE, never the DISCLOSURE.
   Deliberately not landed -- nothing enters the bank on a prediction.
5. **Lifecycle VALUES are gated** on the Kimi user-input pipeline (Andrew-direct 2026-07-31). The MECHANISM
   is complete; the values cannot be populated. A completed type whose values are unobtainable is an
   integration point by definition.
