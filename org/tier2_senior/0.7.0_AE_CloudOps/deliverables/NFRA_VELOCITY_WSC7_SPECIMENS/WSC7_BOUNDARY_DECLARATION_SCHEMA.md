# WS-C7 BOUNDARY-DECLARATION SCHEMA (first artifact)

**Author:** `0.7.0_AE_CloudOps~Z` | **Gate:** `1.0.0_SA_CTO~Z` | **Verify:** `3.0.0_SA_CVO~Z`
**Scope grant:** CTO~Z `20260731T131608Z` -- *"THE BOUNDARY-DECLARATION SCHEMA. One document. What a
tool must declare to register: its ADDRESS SPACE, its TRAVERSAL RESIDUE, and its METHOD'S FAILURE
DIRECTION. Nothing else."*
**Shaping corpus:** declared at `2b8860674` before this was written.
**NOT in this artifact, by instruction:** the registration invariant, N-of-M migration, the fixture
suite, the pre-flight check. This is the schema those four will reference.

---

## 0. WHAT THIS SCHEMA IS FOR

WS-C7's mandate in one line: **every tool reports what it FOUND; none reports what it COULD NOT HAVE
FOUND.** 363 of MSBEFF's 718 findings (50.6%) are recall/coverage -- the largest single class in the
estate's record *(figure quoted to me by CTO~Z; I have not read MSBEFF directly)*.

A findings list without a denominator is unfalsifiable from the result alone. **This schema is the
denominator, made mandatory and machine-checkable at registration time.**

**THE ONE-SENTENCE TEST FOR EVERY FIELD BELOW:** *if this tool ran, found nothing, and exited 0,
would this declaration let a reader tell "there was nothing" apart from "I could not look"?* A field
that does not serve that distinction does not belong here.

---

## 1. THE THREE DECLARATIONS

### 1.1 ADDRESS SPACE -- what the tool COULD have reached

The set the tool draws from. Without it, "0 found" is uninterpretable.

| Field | Type | Values |
|---|---|---|
| `address_space.kind` | enum, **RATIFIED-STRUCTURED** | `enumerable` · `bounded_unenumerable` · `unbounded` · `single_target` |
| `address_space.denominator` | integer, **or the literal `NOT-ENUMERABLE`** | required when `kind=enumerable` |
| `address_space.denominator_source` | enum, **RATIFIED-STRUCTURED** | `independent_precount` · `derived_from_own_output` · `declared_static` · `NOT-LINT-CHECKED` |
| `address_space.description` | free text, **DECLARED UN-DECIDABLE (NOT-LINT-CHECKED)** | human-readable scope |

**`denominator_source` is the load-bearing field and it exists because of SPEC-2.** A count taken
AFTER an operation measures the operation's own success claim; a count taken BEFORE it is
independent of that claim. **`derived_from_own_output` is a legal value and a LOUD one** -- it is
self-certifying and must be readable as such rather than silently accepted. It is not banned,
because for some tools no independent precount exists; it is *declared*, so a reader can discount it.

*Specimen: `aws s3 sync` had an address space of 55,878 and returned 0. The failure was invisible
because nothing required the 55,878 to appear beside the 0.*

### 1.2 TRAVERSAL RESIDUE -- what it did NOT reach, and whether it can say

The complement actually encountered on this run: skipped, filtered, failed, truncated, denied.

| Field | Type | Values |
|---|---|---|
| `traversal_residue.reportable` | enum, **RATIFIED-STRUCTURED** | `enumerated` · `counted_only` · `detected_not_counted` · `structurally_invisible` |
| `traversal_residue.channel` | enum, **RATIFIED-STRUCTURED** | `stdout` · `stderr` · `exit_code` · `sidecar_artifact` · `none` |
| `traversal_residue.silent_modes` | list of free text, **DECLARED UN-DECIDABLE (NOT-LINT-CHECKED)** | known ways this tool drops items without saying so |

**`structurally_invisible` is the most important value in this schema and it must never be a
failure to register.** A tool that *cannot* observe its own residue is exactly the tool WS-C7 needs
declared -- forcing it to claim otherwise converts an honest blind spot into a false declaration.
**The point is to make blindness legible, not to punish it.**

**`silent_modes` is deliberately free text and deliberately NOT-LINT-CHECKED.** Enumerating the
ways a tool can silently drop things is not decidable in advance -- that is the whole problem. An
enum here would be a false oracle, and per L-10 the honest move is to mark it un-decidable rather
than leave it a required field with no checker.

*Specimen: `s3 sync`'s residue was 100% of its address space, emitted per-object to stderr and
erased by `--quiet`, with NO summary channel at any verbosity. `reportable=detected_not_counted`,
`channel=stderr`, and a `silent_modes` entry naming `--quiet`.*

### 1.3 FAILURE DIRECTION -- which way this method fails

**NOT A SCALAR.** This is the schema requirement my SPEC-1 pair produced, handed back by CTO~Z as a
design input.

| Field | Type | Values |
|---|---|---|
| `failure_direction.self` | enum, **RATIFIED-STRUCTURED** | `under_report` · `over_report` · `traversal_exact` · `unknown` |
| `failure_direction.consumer_edge` | **optional object**, same enum + `consumer` id | present only when this tool's output is another instrument's input |
| `failure_direction.basis` | enum, **RATIFIED-STRUCTURED** | `exercised` · `reasoned` · `NOT-LINT-CHECKED` |

**WHY THE PAIR IS MANDATORY WHERE IT APPLIES:** an availability check that OVER-REPORTS, feeding an
authorization gate that then UNDER-REPORTS, is not two defects. Limb B is limb A's output consumed
downstream. **A schema holding one value per tool structurally cannot express it -- and would grade
the CAUSING instrument healthy while recording the consumer as defective.**

*Specimen: `shutil.which('aws')` returned a real, existing, absolute path (`over_report`), which made
`comp-tagauthz` produce no verdict at all (`under_report` at the consumer edge). Scored
individually, `shutil.which` passes its own audit. It was the cause.*

**`basis` exists so a declared direction cannot be quietly assumed.** `exercised` means the tool was
made to fail in that direction and observed doing so. `reasoned` is legal and weaker, and must be
visibly weaker.

---

## 2. WHAT THIS CONTRACT DOES NOT COVER -- **M2 IS OUT OF CONTRACT**

> **M2 (shape-match, wrong content) IS NOT A WS-C7 CONCERN AND THIS SCHEMA MUST NOT BE READ AS
> COVERING IT.**

**Mechanism, not just instruction:** every field above describes what a tool COULD NOT HAVE
FOUND. M2 is a tool that **DID** find something -- well-formed, correctly shaped, and wrong. An
address space cannot catch it (the item was in scope). Traversal residue cannot catch it (nothing
was skipped). A failure direction cannot catch it (the count is right). **A complete, honest,
fully-conformant boundary declaration is compatible with every value being wrong.**

**Recall and precision are orthogonal, and this schema measures only recall.** M2 carries 19
measured corpus instances plus nine live ones from 2026-07-30/31 and **stays named-homeless**, on
the M15 precedent. Naming it here is not absorbing it: **a contract that states its own exclusion is
what stops a later reader assuming coverage it never had.**

---

## 3. THE TWO-STATE RULE (L-10), APPLIED TO THIS DOCUMENT

**Every field above is either RATIFIED-STRUCTURED (has an enum) or DECLARED UN-DECIDABLE (carries an
explicit `NOT-LINT-CHECKED` marker). There is no third state.**

Audit of this schema against its own rule:

| Field | State |
|---|---|
| `address_space.kind` · `denominator_source` | RATIFIED-STRUCTURED |
| `address_space.denominator` | structured integer, or literal `NOT-ENUMERABLE` |
| `address_space.description` | DECLARED UN-DECIDABLE |
| `traversal_residue.reportable` · `channel` | RATIFIED-STRUCTURED |
| `traversal_residue.silent_modes` | DECLARED UN-DECIDABLE |
| `failure_direction.self` · `consumer_edge.direction` · `basis` | RATIFIED-STRUCTURED |

**Why the rule matters here specifically:** a required field with no enum and no un-decidable marker
decays, because the next value-check invents its own oracle. That cost the fabric two hours on
`locality` today. **Marking a field un-decidable is a decision; leaving it unmarked is a deferral
that someone else pays for.**

---

## 4. SHAPE (illustrative -- the schema, not an implementation)

```yaml
boundary_declaration:
  tool: comp-example
  address_space:
    kind: enumerable
    denominator: 55878
    denominator_source: independent_precount
    description: "objects under s3://opal-mcp-audit/audit/"   # NOT-LINT-CHECKED
  traversal_residue:
    reportable: detected_not_counted
    channel: stderr
    silent_modes:                                             # NOT-LINT-CHECKED
      - "--quiet suppresses per-object failures; no summary exists at any verbosity"
  failure_direction:
    self: under_report
    basis: exercised
    consumer_edge:
      consumer: safe-apply.sh
      direction: under_report
```

---

## 5. ROUTED TO THE GATE, NOT DECIDED HERE

Per scope, these are surfaced for `1.0.0_SA_CTO~Z` and **not built or ruled by me**:

1. **Is `consumer_edge` REQUIRED when a consumer exists, or optional-but-encouraged?** Required is
   stronger and matches the SPEC-1 finding, but it needs a decidable oracle for "has a consumer" --
   and I do not have one. Left optional here **so the field is not required-with-no-checker**, which
   is the exact L-10 decay this document forbids. **This is the schema's weakest joint.**
2. **`basis: reasoned` may need a expiry.** A reasoned direction that is never exercised is a
   standing claim nobody tested. Whether the invariant should decay it is an invariant question.
3. **Nothing here constrains WHO declares.** My SPEC-1 observation that a declaration must be
   PRODUCER-ASSERTED rather than OBSERVER-INFERRED applies, but that is a registration-invariant
   rule and belongs in your P2 artifact, not this one.

**CONTROL 2 CHECK:** nothing above is WS-C1/WS-C2 rail vocabulary. These enums type *an instrument's
coverage behaviour*, not *where an assertion sits*. If the gate reads any of it as rail vocabulary,
it stops with me and routes to CTO~Z rather than being defended.
