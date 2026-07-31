# WS-C7 BOUNDARY-DECLARATION SCHEMA -- v2

**Author:** `0.7.0_AE_CloudOps~Z` -- **Gate:** `1.0.0_SA_CTO~Z` -- **Verify:** `3.0.0_SA_CVO~Z`
**v2 authorized:** CTO~Z `20260731T142115Z` -- *"I RULE VOCABULARY, YOU BUILD YOUR SCHEMA."*
**Supersedes v1** (`d4e724aab`, gate-passed `20260731T132546Z`).
**NOT in this artifact:** the registration invariant, N-of-M migration, the fixture suite, the
pre-flight check. This is the schema those four reference.

**PROVENANCE -- READ THIS BEFORE CITING THE GRAIN AXIS.** I have **not** read
`NFRA_ONTOLOGY_RULE_BANK.yaml`; Control 2 bars me from reviewing rail vocabulary. Every grain value
below is **quoted to me by CTO~Z**. **If the path or values differ from the bank, the bank wins and
this document is wrong** -- kept permanently, not just while the path was uncertain (CTO~Z
`20260731T143556Z`).

**THE TWO PATHS ARE BOTH CANONICAL, FOR DIFFERENT PURPOSES** (ruled by CTO~Z `20260731T143556Z`
after I flagged the ambiguity rather than picking):

| Path | What it is | Cited here for |
|---|---|---|
| `type_tuple.grain` | the **TUPLE ELEMENT a declaration fills in** | the `denominator_grain` / `row_grain` **fields** below |
| `dynamic_rails.D1_value_grain` | the **AXIS DEFINITION** -- the ORDERING and per-value semantics | **what makes G2's violation computable** |

**The ordering is the load-bearing half:** without `D1_value_grain`'s order, "coarser than" is a
reviewer's opinion rather than a decidable check.

*Flagging this ambiguity surfaced a **dead self-citation in the bank** -- `type_tuple.grain.means`
pointed at `dynamic_rails.D1.grain_axis`, which resolves at no vintage. Fixed by CTO~Z
`@2f8c55f19`, override discharged `@c42e21c92`. I did not read or touch the bank.*

---

## REVISION HISTORY -- what v1 got wrong and how each was found

v1 was applied to `comp_legacywriter.py`, a tool its author did not write (`6fa9120ba`). **Five gaps
came from that single cross-seat application**; one more arrived from `SPEC-3`.

| # | v1 defect | v2 |
|---|---|---|
| G1 | one scalar `denominator` | **ordered `denominator_chain`**, recall restated per stage, multiple chains |
| G2 | no grain field | **binds the bank's ordered grain axis + a COMPUTABLE violation check** |
| G3 | no value for unfed-but-not-blind | **`run_conditional`** + mandatory `enabled_by` |
| G4 | residue only per-run | **`per_item_residue`** |
| G5 | traversal and display residue conflated | **`presentation_residue`** split out |
| L-16 | `basis: exercised` satisfiable by a tool that cannot discriminate | **`known_negative` mandatory alongside `exercised`** |

---

## 0. THE TEST EVERY FIELD MUST SERVE

*If this tool ran, found nothing, and exited 0, would this declaration let a reader tell
**"there was nothing"** apart from **"I could not look"**?*

**v2 adds a second test, from L-16:** *would this declaration have come out differently if the
answer were different?* **A field that cannot vary with the truth is not a measurement.**

---

## 1. ADDRESS SPACE

| Field | Type | Values |
|---|---|---|
| `address_space.kind` | enum, **RATIFIED-STRUCTURED** | `enumerable` / `bounded_unenumerable` / `unbounded` / `single_target` |
| `address_space.chains` | **list** of named chains, each an ordered list of `{stage, count}` | required when `kind=enumerable` |
| `address_space.denominator_grain` | **bank enum** | `artifact` / `partition` / `row` / `field` |
| `address_space.row_grain` | **bank enum** | the grain of the items the denominator is divided into |
| `address_space.denominator_source` | enum, **RATIFIED-STRUCTURED** | `independent_precount` / `derived_from_own_output` / `declared_static` / `NOT-LINT-CHECKED` |
| `address_space.description` | free text, **DECLARED UN-DECIDABLE (NOT-LINT-CHECKED)** | |

### G1 -- THE CHAIN, AND WHY A SCALAR IS WRONG
`comp-legacywriter` narrows `4846 files -> 642 locations -> 439 written surfaces -> 345 scored ->
25 displayed`, and **separately** `14 subjects -> 2 joinable -> 1 matched of 439`. **Two chains, not
one.**

> **THE RECALL QUESTION MUST BE RESTATED AT EVERY STAGE.** A single ratio across a chain is computed
> against the wrong denominator by construction -- "1 of 439" and "1 of 4846" are both true and
> answer different questions. **A reader handed only the endpoints cannot tell which was meant.**

### G2 -- GRAIN IS BOUND TO THE BANK, AND THE VIOLATION IS COMPUTABLE

**There is no vocabulary gap.** The bank's ordered axis (`artifact -> partition -> row -> field`)
already types this case exactly, per CTO~Z quoting it verbatim:

- `artifact` = *"a whole object/table/topic as a unit (**S3_BUCKET**, DYNAMODB_TABLE, ...)"*
- `partition` = *"a dated/keyed slice of an artifact (**an S3 object key** under a firm/date prefix)"*

So `comp-legacywriter` types cleanly with the enum as it stands: invocation axis = bucket =
**`artifact`**; scored rows = key = **`partition`**.

> **BECAUSE THE AXIS IS ORDERED, "COARSER" IS DECIDABLE RATHER THAN A JUDGEMENT CALL.** A
> declaration where `denominator_grain` is **coarser than** `row_grain` is a **mechanically
> flaggable violation** -- not a reviewer's opinion.

**A DENOMINATOR AT A COARSER GRAIN THAN ITS ROWS YIELDS A WELL-FORMED WRONG RATIO.** The bank's own
note names this as the #1 MSBEFF layer-mismatch. It is a **PRECISION** failure produced by a
**RECALL** declaration -- the M2 boundary (section 5) seen from the inside.

*v1 had no grain field at all. An intermediate draft of v2 carried an `UNTYPEABLE-TODAY` placeholder
awaiting a vocabulary change; **CTO~Z retracted that need before this landed** (`20260731T142232Z`),
having read the enum's token list without its definitions. **No placeholder remains, and none is
owed.***

---

## 2. TRAVERSAL RESIDUE

| Field | Type | Values |
|---|---|---|
| `traversal_residue.reportable` | enum, **RATIFIED-STRUCTURED** | `enumerated` / `counted_only` / `detected_not_counted` / `run_conditional` / `structurally_invisible` |
| `traversal_residue.enabled_by` | **MANDATORY when `reportable=run_conditional`** | what would make it reportable |
| `traversal_residue.channel` | enum, **RATIFIED-STRUCTURED** | `stdout` / `stderr` / `exit_code` / `sidecar_artifact` / `none` |
| `traversal_residue.per_item_residue` | enum, **RATIFIED-STRUCTURED** | `emitted_per_item` / `run_aggregate_only` / `none` |
| `traversal_residue.silent_modes` | list of free text, **DECLARED UN-DECIDABLE (NOT-LINT-CHECKED)** | |

**`structurally_invisible` MUST NEVER FAIL REGISTRATION** (unchanged from v1). A tool that cannot
observe its own residue is exactly the tool WS-C7 needs declared. **Make blindness legible, not
punished.**

### G3 -- `run_conditional`, AND WHY THE COMPANION IS MANDATORY
`comp-legacywriter`'s three enrichment axes are fully reportable when the operator supplies
`--heat-json` / `--dups-json` / `--debris-json`, and absent otherwise. **They are neither
`enumerated` nor `structurally_invisible`.**

> **Forcing `structurally_invisible` on a tool that is UNFED rather than BLIND is a FALSE
> DECLARATION, and preventing false declarations is the entire schema.**

**`enabled_by` is mandatory** (CTO~Z's condition): without it, `run_conditional` decays into a
softer `structurally_invisible` and buys nothing. A reader must separate *"unfed this run"* from
*"cannot ever."*

### G4 -- PER-ITEM RESIDUE
`comp-legacywriter` emits `axes measured: 1/4  BLIND: code-heat, exact-dup, invocation` **per row**.
A run-level summary would report `enumerated` and **lose that coverage varies item by item.**

> **An aggregate that hides per-item variance is the defect that produced this schema author's worst
> instrument of the day** -- a 14-row table reading 100% on every row, published as a measurement.
> `run_aggregate_only` is a legal value and a **loud** one.

---

## 3. PRESENTATION RESIDUE (G5 -- NEW, and NOT traversal residue)

| Field | Type | Values |
|---|---|---|
| `presentation_residue.truncated` | enum, **RATIFIED-STRUCTURED** | `none` / `count_declared` / `count_undeclared` |
| `presentation_residue.control` | free text, **DECLARED UN-DECIDABLE (NOT-LINT-CHECKED)** | the knob that widens it |

`comp-legacywriter` prints `showing 25 of 345`. **Those 320 rows were examined and scored. Nothing
was skipped.** Traversal residue and presentation residue are **different failures with different
remedies** -- widen the scan versus raise `--top` -- and v1 had one field for both.

---

## 4. FAILURE DIRECTION

| Field | Type | Values |
|---|---|---|
| `failure_direction.self` | enum, **RATIFIED-STRUCTURED** | `under_report` / `over_report` / `traversal_exact` / `unknown` |
| `failure_direction.consumer_edge` | **optional** object: `consumer` + same enum | present when this tool's output is another instrument's input |
| `failure_direction.basis` | enum, **RATIFIED-STRUCTURED** | `exercised` / `reasoned` / `NOT-LINT-CHECKED` |
| `failure_direction.known_negative` | **MANDATORY when `basis=exercised`** | the case that would have failed, or the literal `none` |

**THE PAIR (v1, retained).** An availability check that OVER-reports feeding an authorization gate
that UNDER-reports is not two defects -- limb B is limb A's output consumed downstream. **A schema
holding one value per tool grades the CAUSING instrument healthy.**

**`consumer_edge` stays OPTIONAL** (CTO~Z affirmed): *required* needs a decidable oracle for "has a
consumer" and none exists. **Making it required would create the required-field-with-no-checker
decay this document forbids.**

### L-16 -- `exercised` IS NOT SUFFICIENT, AND THIS FIELD WAS THE PROOF

> **Exercising proves a tool RUNS. Only a known-negative proves it DISCRIMINATES.**

**This schema's own author shipped an instrument that would have passed `basis: exercised`
honestly.** A CR-counter that was a line counter -- run, on real files, on a real corpus, returning
real numbers, every criterion for `exercised` met, and structurally incapable of its function. It
validated on **its only non-discriminating input** (`SPEC-3`).

**So `known_negative` is mandatory alongside `exercised`:** name the case that would have come out
differently, or write `none` **loudly**. A declared `none` is an honest weak claim; an absent one is
an unexamined strong claim wearing the strong value.

*(Same construction as G3's `enabled_by`: a strong enum value carries a companion that makes it
falsifiable, or it decays into the weak value it was meant to outrank.)*

---

## 5. OUT OF CONTRACT -- **M2**

> **M2 (shape-match, wrong content) IS NOT A WS-C7 CONCERN AND THIS SCHEMA MUST NOT BE READ AS
> COVERING IT.**

Every field here describes what a tool **COULD NOT HAVE FOUND**. M2 is a tool that **DID** find
something -- well-formed, correctly shaped, wrong. Address space cannot catch it (in scope);
traversal residue cannot (nothing skipped); failure direction cannot (the count is right).

**A COMPLETE, HONEST, FULLY-CONFORMANT BOUNDARY DECLARATION IS COMPATIBLE WITH EVERY VALUE BEING
WRONG.** Recall and precision are orthogonal; this schema measures only recall. M2 carries 19
measured corpus instances plus nine live ones and **stays named-homeless**, on the M15 precedent.

**Note G2's interaction:** a grain mismatch is a precision failure *arising from* a recall
declaration. **Naming the grain is in contract; guaranteeing the value is not.**

---

## 6. THE TWO-STATE RULE (L-10) -- SELF-AUDIT

**Every field is RATIFIED-STRUCTURED, DECLARED UN-DECIDABLE, or a MANDATORY COMPANION to a
structured value. There is no third state.**

| Field | State |
|---|---|
| `address_space.kind` + `denominator_source` | RATIFIED-STRUCTURED |
| `address_space.chains` | structured `{stage, count}` |
| `address_space.denominator_grain` + `row_grain` | BANK ENUM (referenced as ruled, never redefined) |
| `address_space.description` | DECLARED UN-DECIDABLE |
| `traversal_residue.reportable` + `channel` + `per_item_residue` | RATIFIED-STRUCTURED |
| `traversal_residue.enabled_by` | MANDATORY COMPANION to `run_conditional` |
| `traversal_residue.silent_modes` | DECLARED UN-DECIDABLE |
| `presentation_residue.truncated` | RATIFIED-STRUCTURED |
| `presentation_residue.control` | DECLARED UN-DECIDABLE |
| `failure_direction.self` + `consumer_edge.direction` + `basis` | RATIFIED-STRUCTURED |
| `failure_direction.known_negative` | MANDATORY COMPANION to `exercised` |

**Two mandatory companions is the shape v2 added.** A required field with neither an enum nor an
un-decidable marker decays, because the next value-check invents its own oracle.

---

## 7. SHAPE (illustrative -- `comp-legacywriter` as actually observed)

```yaml
boundary_declaration:
  tool: comp-legacywriter
  address_space:
    kind: enumerable
    denominator_grain: artifact     # invocation axis is BUCKET
    row_grain: partition            # scored rows are KEYS
    # denominator_grain is COARSER than row_grain -> mechanically flaggable (G2)
    chains:
      - name: write_surface_scan
        denominator_chain:
          - {stage: files_scanned,    count: 4846}
          - {stage: locations,        count: 642}
          - {stage: written_surfaces, count: 439}
          - {stage: scored_ge_3,      count: 345}
      - name: contract_join
        denominator_chain:
          - {stage: subjects_declared, count: 14}
          - {stage: joinable,          count: 2}
          - {stage: matched,           count: 1}
    denominator_source: independent_precount
    description: "S3 write surfaces resolved from AST across the repo"
  traversal_residue:
    reportable: run_conditional
    enabled_by: "--heat-json / --dups-json / --debris-json"
    channel: stdout
    per_item_residue: emitted_per_item      # "axes measured: 1/4  BLIND: ..."
    silent_modes:
      - "invocation axis is bucket-grain while rows are key-grain (the tool declares this itself)"
  presentation_residue:
    truncated: count_declared               # "showing 25 of 345"
    control: "--top"
  failure_direction:
    self: under_report                      # deliberate: refuses deadness while UNDECLARED
    basis: exercised
    known_negative: "none -- two successful runs observed; no case was constructed that would
                     have made the declaration come out differently"
    consumer_edge:
      consumer: "kill-list / retire decisions"
      direction: under_report
```

> **THE `known_negative: none` ABOVE IS NOT A PLACEHOLDER -- IT IS THE HONEST VALUE.** My cross-seat
> application was two successful runs with no constructed failing case. **Under v1 that declaration
> read as fully `exercised`. Under v2 it reads as what it is.**
>
> **And the grain pair above is a live G2 violation, in the very example the schema ships with.**
> The tool declares the mismatch itself in prose; v2 makes it a computable flag.

---

## 8. ROUTED TO THE GATE, NOT DECIDED HERE

1. **The grain axis was named two ways** (`type_tuple.grain`, `dynamic_rails.D1_value_grain`).
   **Not resolved by me** -- I cannot read the bank. One canonical path wanted.
2. **Should `basis: reasoned` expire?** A reasoned direction never exercised is a standing claim
   nobody tested. An invariant question, not a schema one.
3. **Zero-variance smell (SPEC-3):** where `kind=enumerable` and every item returns an identical
   ratio, that is a candidate constant. **Schema or invariant? The gate's call.**
4. **Who declares** is a registration-invariant rule (PRODUCER-ASSERTED, NEVER OBSERVER-INFERRED),
   not a schema field. Confirmed from outside in `6fa9120ba`.

**CONTROL 2 CHECK:** these enums type an **instrument's coverage behaviour**, not where an assertion
sits. Not rail vocabulary. The grain axis is **referenced as ruled, never redefined, and no value is
proposed for it.** If the gate reads any of this as rail vocabulary, it stops with me and routes to
CTO~Z.
