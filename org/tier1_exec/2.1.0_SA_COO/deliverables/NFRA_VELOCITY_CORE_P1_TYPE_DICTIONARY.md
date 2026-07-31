# NFRA_VELOCITY_CORE — PHASE 1 TYPE DICTIONARY

**For:** Andrew, review. **Compiled by:** `2.1.0_SA_COO`, 2026-07-31.
**Source of record:** `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` @ `meta.version 1.8` — extracted from the
YAML itself, not from the PRD's description of it.
**Design owner:** `1.0.0_SA_CTO~Z` · **Built by:** `0.8.0_AE_CloudComp~C` · **Verified:** `3.0.0_SA_CVO~Z`.

---

## How to read this, in one paragraph

Phase 1 built a **vocabulary for talking about how things behave over time** — not a new graph, and not new
infrastructure. Before it, the estate could say *what exists* and *how it is wired*. It could not say *what
a thing's life is supposed to look like*, so every question about absence, staleness or debt collapsed into
one blunt check: **is the file there?** That check cannot tell "never created" from "deleted" from
"deliberately absent right now" from "hasn't happened yet." **Phase 1's types make those four different
answers sayable.** Everything below is vocabulary that must be **declared by a producer**; almost none of it
is populated yet, and Section 9 states exactly how little.

---

## 1. Honest provenance — what P1 *created* vs *inherited*

This distinction matters and the program's own summaries blur it. Both sets are below; the column says which.

| Landed at | What | Under |
|---|---|---|
| **v1.8** | **The LIFECYCLE axis** — `contract_record`, `lifecycle_class` (7 values), the polarity table, per-value falsifiers, typed violations, lifecycle derivations, the stopgap supersession | **NFRA_VELOCITY WS-C1 — genuinely new in Phase 1** |
| v1.8 | **`held_out_fence`** stated in the rail sections | **NFRA_VELOCITY WS-C2 acceptance clause 3 — new in Phase 1** |
| v1.7 | D-rail citation re-point (motif catalog) — no semantic change | NFRA_VELOCITY, cosmetic |
| **v1.2** | **The D1 / D2 / D3 rails themselves** | **NFRA_ONTOLOGY2 P1** — a *predecessor project* NFRA_VELOCITY absorbed and closed-as-superseded |
| pre-v1.2 | C0–C3 rails, 14 roles, 10 relations, `variance`, `completeness`, `type_tuple` | Ratified substrate, **untouched by P1** |

> **So: "the types created in Phase 1" strictly means the LIFECYCLE axis + the fence.** The D-rails were
> authored earlier under the absorbed project and were **validated** (not created) by P1's WS-C2 corpus walk.
> I give you the full D-rail vocabulary anyway, because it is the substrate the lifecycle types attach to and
> a dictionary of one without the other is unreadable — but the credit line is as above.
>
> **Verified additive:** C0–C3 + 14 roles + 10 relations + variance + completeness are **byte-identical** to
> the pinned pre-touch oracle `8f8a63200` (md5 `37e16648dc965424b75c14677927a636`). Nothing ratified was
> renamed or re-scoped.

---

## 2. THE TUPLE — the four axes every assertion must name

Any tool answer or finding declares `(rail, grain, plane, scope)`. A question is typed in the same tuple, so a
**mismatch is machine-detectable instead of a silently wrong answer**. This was the single most common failure
across the 718-finding MSBEFF corpus.

| Axis | Values | Means |
|---|---|---|
| **rail** | `C0 C1 C2 C3` · `D1 D2 D3` | Which layer the assertion answers at. C0–C3 = STRUCTURE (what exists, how wired). D1–D3 = DYNAMICS. |
| **grain** | `artifact` → `partition` → `row` → `field` | Resolution of the value, coarse → fine. **A coarser answer to a finer question is the #1 layer-mismatch defect.** `row` is declared but unpopulated. |
| **plane** | `source` `projection` `desired` `applied` `live` `mixed` `graph-cache` | **Where the value was observed.** `desired` = declared config intent (Terraform); `applied` = config as landed; `live` = runtime now. Conflating desired and applied is the Rule-22a class. |
| **scope** | `estate` `tree` `firm` `pipeline` `motif` `partition-window` `single-artifact` | **The denominator the assertion is complete OVER.** "Complete over FIRM" ≠ "complete over ESTATE". An assertion that does not name its scope has an unfalsifiable coverage claim. |

---

## 3. D1 — VALUE / GRAIN  *(the value on an edge, and how finely it is resolved)*

**GRAIN AXIS** — ordered coarse → fine:

| Value | Definition | Live population |
|---|---|---|
| `artifact` | A whole object/table/topic as a unit | S3_BUCKET 39, DYNAMODB_TABLE 37 |
| `partition` | A dated/keyed slice of an artifact (an S3 object key) | S3Key 232 |
| `row` | A record within a partition (a DDB item, a parquet row) | **FORWARD — not a graph node. Declared, unpopulated.** |
| `field` | A column/attribute of a record | Field 4969, Prop 359 |

**EDGEKIND** — what happens to a value as it crosses an edge (ratified earlier, extended by D1):

| Value | Definition | Live |
|---|---|---|
| `passthrough` | Value crosses unchanged (identity) | 337 / 961 |
| `rename` | Same value, new name/field | 142 / 961 |
| `recompute_guarded` | Value re-derived under a guard/condition | 482 / 961 |

---

## 4. D2 — PATH / FLOW  *(the ordered hops a value takes, with direction, transform and time)*

A motif is a *shape*; a **path is a shape with direction, transform and time**.

| Component | Definition |
|---|---|
| `hops` | Ordered list of edges, each a produces / consumes / derives-from at a D1 grain |
| `direction` | Native — edges are directed |
| `transform_at_hop` | The hop's EdgeKind (D1) |
| `cadence` | **The contracted run-frequency. NOT a graph property — sourced from a D3 contract.** Forward where undeclared. |

> **The mechanical proof behind this rail:** flow-edge properties are exactly `{condition, dstField, kind,
> rename, resolution, srcField, via}` across all 961 flow edges — **there is no cadence, no vintage, no
> partition key on any of them.** So freshness *cannot* be an edge property; it is necessarily derived from
> flow + contract. That is your thesis — *"data freshness is a downstream function of flow rather than a
> separate aspect"* — established mechanically rather than asserted.

---

## 5. D3 — CONTRACT / OBLIGATION  *(what a thing is obliged to do — sourced from ABOVE it)*

**OBLIGATION TYPES:**

| Value | Definition | Violation is |
|---|---|---|
| `delivery_cadence` | The path must deliver by a contracted time | Staleness — **never a wall-clock age** |
| `completeness` | The assertion must cover a whole declared population | `Incomplete(missing=[...])` |
| `canonical_source` | A value originates from THE ONE blessed writer | Shadow-recompute / wrong-writer |
| `layer_grammar` | A layer does only its job (bronze/silver/gold) | A layer doing a later layer's job early — irreversible |

**THE BINDING LAW:** a D3 obligation is sourced from a governance level **above** the artifact (a registry, a
PRD, a law) — **never the artifact's own config.** An intent-source naming the artifact itself is the
denominator-is-its-own-configuration defect and is *rejected at declaration*.

**CONTRACT_RECORD** — what a contracted resource declares:

- **Required:** `intent_source` · `obligation` · `lifecycle_class` · `revalidate_by` · `locality`
- **Optional:** `successor` · `expiry_condition` · `cadence` · `vintage_probe` · `describes`
- **Deliberately absent:** a population/denominator scope field. **The absence is a prohibition, not a gap** —
  a record carrying its own denominator would let every subject declare its own scope, the exact defect D3
  exists to prevent.

---

## 6. ⭐ LIFECYCLE_CLASS — the centrepiece of Phase 1

**The problem it solves, stated once:** an existence check is asked a question about lifecycle that existence
cannot answer. One "absent" symbol stands for **at least four different states** — never existed / existed and
was deleted / absent right now by design / not yet occurred. **Absence is not a state; it is a set of states,
and no existence check can partition it.** Sampling harder does not help: you keep landing in troughs and
become *more confident and no more correct*.

**PRODUCER-ASSERTED, never observer-inferred.** Any implementation that infers this from key names, directory
position or observed absence has rebuilt the name-pattern stopgap with more syntax.

### The seven values, with both polarities

The two polarity columns are the deliverable. A detector must know **which predicate to run**, not merely which
rows to skip.

| Value | Meaning | ABSENT at rest | PRESENT at rest | Required falsifier fields |
|---|---|---|---|---|
| `PERMANENT` | Present from creation onward | **FINDING** (missing) | Healthy; with a cadence, healthy iff vintage advances, else FROZEN | `intent_source` |
| `TRANSIENT` | Written → consumed → deleted; oscillates | **HEALTHY** | Healthy iff dwell < `max_dwell`; **STRANDED** beyond | `consumer`, `max_dwell`, `locality` |
| `EVENT_CREATED` | Absent until a triggering occurrence; append-only after | **HEALTHY** (zero occurrences so far) | Healthy; a non-append edit is an INTEGRITY finding | `creating_event`, `event_observable`, `locality` |
| `DORMANT` | Deliberately inactive and deliberately **retained** — a rollback lever, an armed fallback | **FINDING** (a belt that vanished) | Healthy — **and zero traffic is also healthy** | `reason`, `rearm_condition`, `annotation_cite`, `revalidate_by` |
| `LEGACY` | A live successor exists; may still be READ | Per successor | Healthy to read; **a WRITE is LEGACY-WRITER** | `successor`, `intent_source` |
| `RETIRED` | Decommissioned by ruling; absence is correct and terminal | Healthy (terminal) | **FINDING** (incomplete decommission) | `retirement_ruling` |
| `UNDECLARED` | No lifecycle declared. **Today this is essentially the whole estate.** | UNKNOWN, loud | UNKNOWN, loud | — never silently resolves to PERMANENT |

> **THE NUMBER THAT JUSTIFIES THE WHOLE AXIS: absence is HEALTHY on 2 of 7 rows and presence is a FINDING on
> 2 of 7 — so a single-polarity existence detector is WRONG ON 4 OF 7 ROWS, in the direction that proposes
> deleting live infrastructure.** A skip-list *suppresses*; a type *inverts*.

**Every value carries a falsifier.** You cannot declare `TRANSIENT` to silence a detector without naming an
*exercised* consumer and a `max_dwell` bound to that consumer's cadence — which creates the STRANDED finding
that proves the declaration can still fail. `DORMANT` requires a `rearm_condition`, because **a belt nobody
can state the re-arm for is not a belt.**

**Decay:** `revalidate_by` is required on **every** declaration, and a STALE declaration never auto-promotes —
it suppresses the deletion verdict and *releases the observation*, so a silencer cannot survive its own expiry.

---

## 7. TYPED VIOLATIONS — the debt shapes, now machine-statable

| Violation | Definition |
|---|---|
| `LEGACY_WRITER` | A write whose target is LEGACY with a live successor, or whose obligation has expired |
| `CLOBBER` | Two writers at one `(key, grain)` with no adjudicating canonical-source contract |
| `TRIGGER_MISSEQUENCE` | An edge firing against the topological + temporal order |
| `SILENT_RESIDENT` | No enumerator traverses it, no predicate reacts |

*Naming note:* `SUPERSEDED` and `ORPHAN` were deliberately **not** used — both are already-occupied tokens on
the ratified variance axis with different meanings, and two definitions on one token in one file is a
prohibited shape.

---

## 8. DERIVATIONS — defined, never primitives

Each of these is **defined as a derivation** rather than stored as a fact, which is what stops them drifting:

| Property | Defined as |
|---|---|
| **freshness** | D2 path + D3 cadence + upstream vintages + trading calendar — never a wall-clock mtime |
| **provenance** | D1 grain + D2 path walked backward |
| **staleness vs frozen** | Vintage advancing along the path vs the value not moving |
| **blast** | D2 forward walk at a declared grain |
| **debt** | Expired obligation ∪ LEGACY-with-live-exercised-successor |
| **stranded** | TRANSIENT with dwell > `max_dwell` — **not statable by any current instrument in either direction** |
| **incomplete decommission** | RETIRED and present at rest |
| **rolling** | PERMANENT + a declared cadence — **a derivation, deliberately not a class** |

---

## 9. ⚠ WHAT IS NOT TYPED — the honest coverage boundary

**This section is the one I would read most carefully.** The vocabulary is real; the population is near zero.

1. **LIFECYCLE COVERAGE AT THIS LANDING IS ZERO INSTANCES.** The vocabulary is declared; the instance registry
   is ESTATE WS-E1's and does not exist yet. **Every estate resource is UNDECLARED today.** Reading this
   dictionary as though the estate were typed would be a serious misread.
2. **The vocabulary is PROPOSED, NOT VALIDATED as final** — it was fitted to a declared corpus and tested by
   the WS-C2 walk. The rule bank's own words: *"expect the enum to change; if it does not change at all, be
   suspicious of the walk."*
3. **TRANSIENCE IS UNVERIFIABLE AGAINST THE GRAPH BY CONSTRUCTION** — a written-then-deleted marker is not a
   durable object, so no graph read can confirm a TRANSIENT declaration. A real asymmetry, not a gap to close.
4. **`max_dwell` is currently UNSATISFIABLE in practice** — no consumer declares a delivery cadence yet, so
   every TRANSIENT declaration renders UNKNOWN-loud today. Correct failure direction, but **the axis ships
   INERT for the marker population** and the old name-pattern stopgap stays load-bearing.
5. **"EXERCISED" is enforced by honesty and review, not by machinery** — no exerciser exists yet.
6. **`expiry_condition` machine-evaluability is unenforced** — the grammar requires it, no gate checks it.
7. **`row` grain and the partition SCHEME are forward** — declared, not populated.
8. **Most obligations are not in the graph at all** — D3 is contract-sourced by construction.

---

## 10. THE HELD-OUT FENCE — the one control protecting the whole test

**`ADVI_PERFORMANCE` and `MDPF_GLOBAL` are the held-out test set. They must not shape these rails.**

Why it is stated *inside* the rail sections rather than in a design document: so a future author cannot
innocently breach it.

> **Why it is the most dangerous item to get wrong:** if the rails are shaped using them, the only real test of
> this framework is destroyed **and nothing reports it.** A breached held-out set looks *exactly* like a
> well-fitting rail — the gap reads structurally zero and the fit reads excellent. **There is no downstream
> signal that fires.** The only control is not to touch them.

Every rail author must **publish their shaping corpus**, because an unnamed one is indistinguishable from a
breached one. Liftable only by you or the CVO — not by a rail author, not by a phase close.

---

## 11. What I would want you to decide or push back on

1. **Is `UNDECLARED` acceptable as the estate-wide default indefinitely?** It is honest, but it means the axis
   currently answers UNKNOWN for everything. The population comes from ESTATE WS-E1.
2. **Seven values — right size?** The walk kept all seven and collapsed `ROLLING` into a derivation. If any
   value looks like it is carrying two ideas, now is the cheap moment to say so.
3. **`DORMANT` cites `keep-dormant.yaml` as its intent source and does not copy it.** That registry's seven
   live entries currently use a weaker citation form than this axis requires; the divergence is disclosed
   rather than silently inherited, and the registry fix is on its own path.
4. **The lifecycle VALUE population is gated pending the Kimi user-input pipeline** (your 2026-07-31 direct).
   The mechanism continues; nothing here populates values.
