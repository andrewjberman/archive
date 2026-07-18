# NFRA_ONTOLOGY -- The Variance Mechanism (declared-dimension symmetry test)

**Companion to `NFRA_ONTOLOGY_DESIGN_OF_RECORD.md` (v0.2).** Author: `0.8.0_AE_CloudComp~C`, 2026-07-18.
Status: DRAFT (NEXT-2). The Variance CORE (set, polarity, declared-dimension approach) is base-confirmed
(042801Z) + MSTR-endorsed; the CONFORMANCE TERMINOLOGY is doctrine-adjacent, pending the D3 joint ruling
(structural conformance = Variance IN; spec conformance = `implements` OUT). base = FEED; `~D` = consumer.

**Why this exists.** Variance is the ontology's most novel contribution and the charter's founding question --
*"where does firm-twin/fork-shadow derive from; do we have a bank that deterministically explains these
relationships?"* This spec is the deterministic mechanism. It generalizes canon-patterns' hard-coded
`twin_shadow_guard` (identity keyed on `(firm, layer, logical-stage)`) into a substrate-agnostic operator,
and it is the deterministic input COMPSIMILAR's HELD C3/Twin clause was waiting for.

---

## 1. What Variance classifies

Variance is the ORTHOGONAL comparison operator (DoR Section 8) -- NOT a C0-C3 compression tier. It classifies
how MULTIPLE instances of the SAME logical thing relate to EACH OTHER. It applies at two grains:
- **C0 grain:** fact-twins (an `opal-data-bd` bucket vs its `opal-data-cot`/`opal-data-inf` twins).
- **C2 grain:** motif-twins (a bd pipeline motif vs the cot/inf parallel motifs).

The 6-label set (base-confirmed, MSTR-endorsed): **Canonical, Twin, Variant, Fork-Shadow, Superseded,
Orphan.**

---

## 2. The two ingredients

### 2.1 Declared variance DIMENSIONS
A system DECLARES the axes along which parallel instances are LEGITIMATELY expected to differ. Each dimension
is `{name, values[], scope}`:
- `firm` : `[bd, cot, inf, 49financial, cottonwood, inflection, mdpf, ...]` -- business separation.
- `env` : `[dev, staging, prod]`.
- `region` : `[us-east-1, ...]`.
- `tenant`, `service`, ... -- any per-system axis.

**Substrate-agnostic:** "firm" is just one parameter. The mechanism reads the DECLARED dimension set; it
hard-codes none. (canon-patterns hard-coded `firm`; this generalizes it -- base specific-B.)

**The dimensions are a GOVERNED, read-from-FILE catalog** (mirrors canon-patterns' `roles:` + the C3 naming
catalog). Declaring a new dimension = a governed edit, never an inference.

### 2.2 The identity KEY (position minus dimension)
Two instances are "the same logical thing at different dimension-values" iff they match on the **position
key** = every identity-bearing coordinate EXCEPT the declared dimension. Generalizing canon-patterns'
`(firm, layer, logical-stage)`:

```
position_key(instance) = (logical-stage, layer, role, motif-shape)   # everything but the declared dimension
dimension_value(instance) = the value of the declared dimension the instance carries (e.g. firm=bd)
```

Instances sharing a `position_key` are a **sibling group** spread across dimension-values.

---

## 3. The symmetry test (the deterministic classifier)

For each sibling group (instances sharing a `position_key`), over a declared dimension `D` with values
`V = {v1..vn}`:

```
present = { dimension_value(i) : i in group }          # which dimension-values actually have an instance
expected = V                                            # the declared full value set (scoped to D's scope)

FULL SYMMETRY   present == expected           -> every instance is a TWIN (one is Canonical/reference).  CLEAR.
PARTIAL/EXTRA   present != expected:
    a value in expected missing from present  -> the group is asymmetric; the present ones may still be
                                                 legitimate if the missing value is OUT OF D's scope (declared
                                                 absence). An UNDECLARED missing value -> FORK-SHADOW (debt).
    an instance whose off-key structure DIVERGES from its siblings (same position_key, but different
        motif-shape/role/edges)               -> FORK-SHADOW (debt) -- the diverged copy.
SINGLETON       group of 1, no sibling, no consumer -> ORPHAN.
SUPERSEDED      two instances at the SAME (position_key, dimension_value) where one `supersedes` the other
                                              -> the older is SUPERSEDED (both live).
VARIANT         a legitimate facet-difference declared along D (e.g. an env-specific config) that differs
                ONLY along D and nowhere off-key -> VARIANT (a Twin whose difference is the declared facet).
```

**Twin vs Variant:** both are symmetric/legitimate. Twin = structurally IDENTICAL parallels across D (the
bd/cot/inf pipeline replicas). Variant = a parallel that differs ONLY in the declared facet's expected way
(a prod-vs-dev config). Both CLEAR; the label distinguishes "identical replica" from "expected facet-diff."

**Fork-Shadow vs everything:** the ONLY debt verdict. It is asymmetric-AND-undeclared: an instance that
shares a sibling's identity key but diverges off-key with no declared reason (the 29-file inf bare-vs-INF_
shadow; the 9-RED bd-cot fork).

---

## 4. The load-bearing polarity + invariants (base specifics, folded)

- **POLARITY (base specific-B, confirmed):** the mechanism **CLEARS designed parallels** (Twin/Variant are
  canon) and **FLAGS only Fork-Shadow/Orphan**. It never flags a full sibling set. Inverting this polarity
  would flag every legitimate firm-twin as debt -- the exact false-positive canon-patterns' guard exists to
  prevent.
- **HARD firm invariant (base specific-A):** for `D = firm`, firms are BUSINESS-SEPARATED and NEVER
  interchangeable/mergeable (IAM-denied + gate-blocked, a CLAUDE.md NEVER-rule). A `Twin` verdict on the firm
  dimension asserts "designed parallel = canonical"; it does **NOT** imply the firms are fungible or their
  buckets cross-referenceable. The never-cross constraint lives HARD in the adapter (the first-class `denies`
  relationship), not in this operator. The operator READS the firm dimension; it never authorizes a merge.
- **Determinism (Andrew's requirement):** every verdict is a pure structural SET COMPARISON over the declared
  dimension values + the position keys -- no inference, no LLM. A group the mechanism cannot classify (no
  declared dimension applies) gets NO verdict (counted in the denominator), never a guess.

---

## 5. The `~D` consumer contract (COMPSIMILAR C3/Twin unblocker)

Per node/ARN, the layer emits a `variance_verdict` for splicing into the summary string, from a governed
read-from-FILE vocabulary (mirroring canon-patterns' `roles:` -> C2 governance), no-guess:

```
variance_verdict(node) -> one of:
  { kind: "Canonical",   of: <position_key> }          -> "canonical <D>-twin (reference) of <siblings>"
  { kind: "Twin",        of: <canonical>, dim: <D> }    -> "canonical <D>-twin of <canonical>"
  { kind: "Variant",     of: <canonical>, dim: <D> }    -> "<D>-variant of <canonical>"
  { kind: "Fork-Shadow", of: <canonical>, dim: <D> }    -> "divergent fork-shadow of <canonical> (debt)"
  { kind: "Superseded",  by: <newer> }                  -> "superseded by <newer>"
  { kind: "Orphan" }                                    -> "orphan (no twin, no consumer)"
  (none)                                                -> NO clause (absent, counted in the denominator)
```

- Deterministic, structure-derived, coverage-denominatored -- the exact shape base's C3 contract specified.
- **Zero enricher rework:** the enricher already graceful-degrades (no label -> no clause), so this lights up
  the moment the governed dimension catalog + this operator land. ~D's C2 (motif class+role) proceeds
  independently; this is the HELD C3/Twin half.
- The BEFORE/AFTER (base's own COMPSIMILAR example) is satisfied: `S3_BUCKET 'opal-data-bd': ... firm-twin of
  opal-data-cot/inf` is exactly a `{kind: "Twin", dim: "firm"}` verdict.

---

## 6. Worked example (canon-patterns' own twin_shadow_guard, generalized)

Declared dimension `firm = {bd, cot, inf}` (scope: the daily-pull pipeline). Sibling group at
`position_key = (stage: silver-sweep, layer: silver, role: Transformer, motif: PIPELINE)`:
- `present = {bd, cot, inf}` == `expected` -> **FULL SYMMETRY** -> all three are **Twins**, one Canonical.
  CLEARED (canon), never flagged. (This is canon-patterns' `twin_shadow_guard` "a parallel firm path matching
  the SAME motif is canonical" -- reproduced exactly, but now parameterized on the declared dimension.)
- Contrast: an `inf` silver-sweep whose motif-shape diverges (reads bronze past silver -- a layer_skip) while
  bd/cot do not -> same `position_key`, off-key divergence, undeclared -> **FORK-SHADOW (debt)**. (The
  bare-vs-INF_ shadow class.)

---

## 7. Open dependency + next

- **D3 joint ruling (CTO + MSTR, doctrine-adjacent):** MSTR's lean ties "structural conformance
  (conforms-to-canonical / diverged-from-twin)" to THIS operator (IN), distinct from `implements` spec
  conformance (OUT). This spec IS that structural-conformance mechanism; the final CONFORMANCE TERMINOLOGY
  binds on the D3 ruling. The MECHANISM (Sections 2-6) is independent of that terminology and is
  base/MSTR-confirmed.
- **On the D3 + closed-set GO:** fold this into the machine-readable rule bank (NEXT-3) alongside the
  governed dimension catalog; hand ~D the `variance_verdict` function (base FEEDS the walkthrough).

*-- 0.8.0_AE_CloudComp~C. NEXT-2 mechanism spec. base FEED read + ~D consumer review requested; RAVC MSTR/CTO
on the D3 conformance-terminology.*
