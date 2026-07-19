# NFRA_ONTOLOGY -- The Variance Mechanism (declared-dimension symmetry test)

**Companion to `NFRA_ONTOLOGY_DESIGN_OF_RECORD.md` (v0.2).** Author: `0.8.0_AE_CloudComp~C`, 2026-07-18.
Status: **rev.3 -- v2 DISPOSITION co-change (CTO 013249Z + CVO cot adjudication): a firm fork-shadow under
[]+advisory is a CANDIDATE, NOT confirmed debt (corrects the ratified @f904033ea "Fork-Shadow=debt" model at
:100/:112/:155; cot = the live NON-debt proof @1fe0f5e6f). The verdict KIND is unchanged; only the disposition
claim is corrected. HOLD re-land until CTO+MSTR co-sign the mechanism ruling.** rev.2 -- base Q1/Q2 fix + ~D's
4 interface asks folded (044024Z / 043855Z). The
Variance polarity + hard-firm-invariant are base-confirmed; the CORE was corrected per base's review (Q1: keep
structure OUT of the identity key so Fork-Shadow fires; Q2: `allowed_facets` makes Variant deterministic). The
CONFORMANCE TERMINOLOGY is doctrine-adjacent, pending the D3 joint ruling (structural conformance = Variance
IN; spec conformance = `implements` OUT). base = FEED; `~D` = consumer (contract shape confirmed-fit).

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
is `{name, values[], scope, allowed_facets[]}`:
- `firm` : values `[bd, cot, inf, 49financial, cottonwood, inflection, mdpf, ...]`, allowed_facets `[]`
  (structural replicas -- NOTHING may legitimately differ off-key; business separation).
- `env` : values `[dev, staging, prod]`, allowed_facets `[memory_size, replica_count, endpoint_host]`
  (a per-env config may legitimately differ ONLY in these).
- `region` : values `[us-east-1, ...]`, allowed_facets `[...]`.
- `tenant`, `service`, ... -- any per-system axis.

**`allowed_facets` (base Q2, 044024Z -- required for a DETERMINISTIC Variant).** A dimension `{name, values,
scope}` alone cannot tell a legitimate env-Variant (env changed the memory size, EXPECTED) from a Fork-Shadow
(memory changed with no declared reason). So the dimension MUST declare WHICH facets it may legitimately
alter. Then: an off-key difference WITHIN `allowed_facets` = **Variant** (legitimate); OUTSIDE = **Fork-Shadow**
(debt). For `firm`, `allowed_facets = []` -- firm replicas are structurally identical, so ANY off-key diff is
a Fork-Shadow (this is exactly canon-patterns' firm-twin intent). **v1 defer option (base):** ship with
`allowed_facets` unpopulated -> only structurally-identical Twins clear, ANY off-key diff = Fork-Shadow, and
Variant is deferred; populate `allowed_facets` per-dimension later. Either way Variant stays deterministic.

**Substrate-agnostic:** "firm" is just one parameter. The mechanism reads the DECLARED dimension set; it
hard-codes none. (canon-patterns hard-coded `firm`; this generalizes it -- base specific-B.)

**The dimensions are a GOVERNED, read-from-FILE catalog** (mirrors canon-patterns' `roles:` + the C3 naming
catalog). Declaring a new dimension (or an `allowed_facet`) = a governed edit, never an inference.

### 2.2 The identity KEY vs the compared STRUCTURE (base Q1 fix -- load-bearing)
Two instances are "the same logical thing at different dimension-values" iff they match on the **position
key** = the LOGICAL IDENTITY with the declared dimension STRIPPED. **Structure (motif-shape/role/edges) is
NOT in the key -- it is what the symmetry test COMPARES.**

```
position_key(instance)  = (logical-stage, layer, normalized-logical-identity)   # dimension-stripped; NO structure
dimension_value(instance) = the value of the declared dimension the instance carries (e.g. firm=bd)
structure(instance)     = (motif-shape, role, edge-set)                          # the COMPARED thing, NOT the key
```

**Why structure must be OUT of the key (the bug base caught):** canon-patterns keys on `(firm, layer,
logical-stage)` -- NO motif/role -- and treats "matching the SAME motif" as the COMPARISON and "DIVERGED from
its twin" as the fork-shadow. If motif-shape/role were IN the key, two instances that DIVERGE in structure
would have DIFFERENT keys, land in different sibling groups, and the diverged-copy Fork-Shadow clause could
NEVER FIRE (self-contradictory dead code). Keying on logical identity ALONE and comparing structure SEPARATELY
is what makes "inf's stage-N is a fork-shadow of bd/cot" a precise verdict instead of the weak "inf missing +
an inf singleton."

Instances sharing a `position_key` are a **sibling group** spread across dimension-values; the symmetry test
(Section 3) then compares their `structure`.

---

## 3. The symmetry test (the deterministic classifier)

TWO steps -- (1) GROUP by `position_key` (logical identity), (2) COMPARE `structure` across the dimension.
For each sibling group over a declared dimension `D` with values `V = {v1..vn}` and `allowed_facets F`:

```
present  = { dimension_value(i) : i in group }         # which dimension-values actually have an instance
expected = V (scoped to D's scope)                     # the declared full value set
ref      = the Canonical instance (designated, or the modal structure)

# (2a) COMPLETENESS -- is the sibling set present across all expected values?
present == expected                        -> complete. proceed to (2b).
a value in expected MISSING from present   -> asymmetric. legitimate IF the value is out-of-scope (declared
                                              absence); an UNDECLARED gap -> FORK-SHADOW (the missing side is a
                                              divergence-by-absence).

# (2b) STRUCTURAL SYMMETRY -- compare each instance's structure() to ref:
structure(i) == structure(ref) for all i   -> TWIN group (all structurally identical; ref = Canonical).  CLEAR.
structure(i) differs from ref ONLY in facets within F  -> instance i is a VARIANT (legitimate facet-diff).  CLEAR.
structure(i) differs from ref OUTSIDE F (or F is empty) -> instance i is a FORK-SHADOW -- the diverged copy.
   # DISPOSITION (v2, CTO 013249Z + CVO cot adjudication): a fork-shadow is CONFIRMED DEBT only on a GROUNDED
   # dimension (allowed_facets populated+cited); under []+advisory it is a CANDIDATE (pending adjudication),
   # NOT confirmed debt -- it can ground out to debt / graph-coverage-gap / designed-difference.

# other verdicts:
SINGLETON  group of 1, no sibling, no consumer                    -> ORPHAN.
SUPERSEDED two instances at the SAME (position_key, dim_value), one `supersedes` the other -> older = SUPERSEDED.
```

**Twin vs Variant (now deterministic via `allowed_facets`, base Q2):** Twin = structure IDENTICAL to ref
(bd/cot/inf replicas). Variant = structure differs from ref ONLY within the dimension's declared
`allowed_facets` (a dev/prod config differing only in memory_size). Both CLEAR. The `allowed_facets` set is
what makes the Twin/Variant/Fork-Shadow line a pure structural test, not a judgment.

**Fork-Shadow -- the only debt-CANDIDATE verdict (NOT confirmed debt under advisory).** It fires two ways, both
well-defined against the logical-identity key: (a) an instance whose STRUCTURE diverges from its siblings
OUTSIDE the allowed facets (the 29-file inf bare-vs-INF_ shadow; the 9-RED bd-cot fork); (b) an UNDECLARED
missing side of an expected sibling set. **DISPOSITION (v2, CTO 013249Z + CVO cot adjudication -- corrects the
earlier "ONLY debt verdict"):** a firm fork-shadow under `[]`+advisory is a CANDIDATE pending adjudication, NOT
confirmed debt -- it can ground out to real-debt / graph-coverage-gap / designed-legit-difference. **cot is the
LIVE PROOF: opal-data-cot was a firm fork-shadow that grounded to a 0.7.0-derive coverage-GAP = NON-debt
(@1fe0f5e6f).** Only a fork-shadow on a GROUNDED dimension (allowed_facets populated+cited) is confirmed debt.
The verdict KIND (Fork-Shadow = the structural divergence) is unchanged; only the DISPOSITION claim is corrected.

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
- **Determinism (Andrew's requirement):** every verdict is a pure structural comparison -- group by
  `position_key` (logical identity), then compare `structure` across the dimension values against the declared
  `allowed_facets`. No inference, no LLM. A group the mechanism cannot classify (no declared dimension applies)
  gets NO verdict (counted in the denominator), never a guess.

---

## 5. The `~D` consumer contract (COMPSIMILAR C3/Twin unblocker)

Per node/ARN, the layer emits a `variance_verdict`, from a governed read-from-FILE vocabulary, no-guess.
**Conformed to ~D's LANDED enricher (`summary_corpus.py` @4c57b963a, review 043855Z) -- 4 interface points:**

**(#1) SIBLING enrichment, NOT a fold into the motif splice.** ~D's motif clause is argument-LESS
("instantiates <CLASS> as <label>"); the variance clause carries a REFERENCE ARGUMENT ("... of <canonical>").
So it wires as a PARALLEL `variance_prose_and_tokens` + its own `SummaryDoc.variance` field + its own render
line -- NOT through `motif_prose_and_tokens`.

**(#2) Return human-readable reference NAMES inline** (splice stays a PURE format, no second lookup in the
enricher). **(#4) Both the `kind` enum AND the clause-PHRASING strings are read-from-the-governed-catalog**
(blessing phrasing == a governed edit, identical to `roles:`):

```
variance_verdict(node, corpus?) -> one of:   # phrasing strings are FROM the governed catalog, not hardcoded
  { kind:"Canonical",  dim:<D>, of_names:[<sibling names>] } -> "canonical <D>-twin (reference) of <of_names>"
  { kind:"Twin",       dim:<D>, of:<arn>, of_name:<name> }   -> "canonical <D>-twin of <of_name>"
  { kind:"Variant",    dim:<D>, of:<arn>, of_name:<name> }   -> "<D>-variant of <of_name>"
  { kind:"Fork-Shadow",dim:<D>, of:<arn>, of_name:<name> }   -> "divergent fork-shadow of <of_name> <disposition>"
      # <disposition> from fork_shadow_disposition (v2, CTO 013249Z): advisory (allowed_facets=[]) -> "(candidate -- advisory, pending adjudication)"; grounded -> "(debt)"
  { kind:"Superseded", by:<arn>, by_name:<name> }            -> "superseded by <by_name>"
  { kind:"Orphan" }                                          -> "orphan (no twin, no consumer)"
  (none)                                                     -> NO clause (absent, counted in the denominator)
```

**(#3) Two-path cost (confirmed expected):** variance needs the SIBLING GROUP (cross-instance by
`position_key`), NOT in the single-ARN local neighborhood. `variance_verdict` accepts the `corpus` when
available -- FREE in `build_corpus` (whole set loaded); on the single-ARN `--describe` path it does exactly
ONE targeted sibling-query.

- Deterministic, structure-derived, coverage-denominatored -- the discipline base's C3 contract specified.
- **Zero enricher rework:** graceful-degrades (no verdict -> no clause); lights up when the operator + the
  governed catalog land. ~D's C2 (motif class+role) proceeds independently -- this is the HELD C3/Twin half.
- The BEFORE/AFTER (base's example) is satisfied: `S3_BUCKET 'opal-data-bd': ... canonical firm-twin of
  opal-data-cot/inf` = `{kind:"Twin", dim:"firm", of_name:"opal-data-cot"}` with `of_names` rendered.

---

## 6. Worked example (canon-patterns' own twin_shadow_guard, generalized)

Declared dimension `firm = {bd, cot, inf}`, `allowed_facets = []` (scope: the daily-pull pipeline). Sibling
group keyed on LOGICAL identity (structure is NOT in the key):
`position_key = (stage: silver-sweep, layer: silver, logical-identity: "daily-silver-sweep")`.
- **Canonical case:** all three of bd/cot/inf carry an instance at this key; `structure(bd) == structure(cot)
  == structure(inf)` -> **(2a)** complete AND **(2b)** structurally identical -> all three are **Twins**, one
  Canonical, CLEARED. (canon-patterns' `twin_shadow_guard` "a parallel firm path matching the SAME motif is
  canonical" -- reproduced, now parameterized on the declared dimension.)
- **Fork-Shadow case (now fires correctly -- the bug base caught):** bd/cot/inf all carry an instance at the
  SAME `position_key` (so they ARE one sibling group -- structure is NOT in the key), but `structure(inf)`
  diverges from `structure(bd/cot)` (inf reads bronze past silver -- a layer_skip) and `allowed_facets` is
  empty -> **(2b)** inf's structure differs OUTSIDE the allowed facets -> **inf's silver-sweep = FORK-SHADOW of
  bd/cot (debt)**. A precise verdict -- NOT the weak "inf missing + an inf singleton" the over-constrained key
  would have produced. (The bare-vs-INF_ shadow class.)

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
