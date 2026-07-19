# NFRA_ONTOLOGY -- Variance FIRM-dimension Catalog + `variance_verdict` Consumer Contract

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-18. **Status:** rev.3 -- WIRED + LANDED by `~D` @566ea8cd7
(self-test 10/10, M10 mutant-tests the modal-ref + empty-modal fixes). rev.2 = base coherence-check PASS
(@234142Z: narrowing RATIFIED, realization faithful to `@f904033ea`) + canonical-ref=MODAL fix (§1/§2.4/§3/§4).
rev.3 = fold `~D`'s landed collision fix: GROUPING KEY = `(node_type, position_key)` + empty-modal-suppress +
real-ARN-prefer (§2.2) -- a same-named S3_BUCKET_POLICY was colliding with its bucket and inverting the verdict.
**Companion to**
`NFRA_ONTOLOGY_VARIANCE_MECHANISM.md` (the frozen mechanism) -- this is its CONCRETE, grounded, `~D`-wireable
realization for the `firm` dimension.

**What this delivers (the two things base asked for):**
1. **The governed firm-dimension catalog** -- concrete, estate-grounded `values` + `allowed_facets` + the
   verdict clause-phrasing strings (read-from-FILE, never inferred; interface point #4 of the mechanism §5).
2. **The `variance_verdict` consumer contract** -- specialized to `firm`, realizing base's coherence framing
   (231424Z): *group by `position_key` (name-minus-firm), compare the motif-membership-SET across firm-siblings;
   symmetric-full-set -> Twin, asymmetric -> Fork-Shadow, singleton-no-consumer -> Orphan* -- query-derivable
   from the membership-sets `~D` ALREADY computes, NO separate producer.

---

## 0. Grounding (values are ESTATE-derived, not invented -- STANDING DIRECTIVE)

| Fact | Grounding (source @ vintage) |
|---|---|
| The firm-twin dimension IS `bd / cot / inf` (resource-name tokens) | `org/modules/graph/canon-patterns.yaml:55` `twin_shadow_guard` (@ HEAD 76c310664): *"bd / cot / inf parallel pipeline instances are DESIGNED firm-separated TWINS -- NOT deviations."* |
| firm-name mapping bd<->49financial, cot<->cottonwood, inf<->inflection | `canon-patterns.yaml:78` (per-firm auth 49financial/cottonwood/inflection) + `comp-constants-seed-multifirm.yaml:13` FIRM_BUCKET_MAP |
| The parallel firm buckets are REAL | `comp-kuzu` (nessie, built 21:43Z, age 1.8h): `opal-data-bd`, `opal-data-cot`, `opal-data-inf` all present; `opal-data-demo`/`-mdpf` present but are NOT bd/cot/inf firm-replicas (demo tenant / partner-ETF -- different purpose, no firm-sibling parallel) |
| `allowed_facets = []` for firm | mechanism §2.1/§4 (base specific-A): firms are BUSINESS-SEPARATED, structural replicas -- ANY off-key diff is a Fork-Shadow |

---

## 1. The governed firm-dimension catalog

Read-from-FILE (mirrors canon-patterns `roles:` + the C3 naming catalog). Declaring/editing a dimension, an
`allowed_facet`, or a phrasing string is a GOVERNED edit, never an inference. Proposed canonical location:
`org/modules/graph/variance_dimensions.yaml` (physical placement rides governance/CTO -- same as the rule bank;
`debtscan/` is exec-locked, I author the content, exec lands it).

```yaml
# variance_dimensions.yaml -- the GOVERNED declared-variance-dimension catalog (v1: firm only)
dimensions:
  firm:
    # the token that appears in a resource NAME at the firm position; position_key strips it.
    values: [bd, cot, inf]
    # firm-config display names (auth/edge substrate); metadata for rendering, NOT the keying token.
    firm_names: { bd: 49financial, cot: cottonwood, inf: inflection }
    scope: parallel-firm-pipeline            # buckets + their C2 motifs on the daily-pull firm pipelines
    allowed_facets: []                       # structural replicas -- NOTHING may legitimately differ off-key
    canonical: modal                         # ref = the MODAL membership-set among PRESENT firms (NOT a fixed firm).
                                             # base 234142Z: a FIXED ref makes a divergence OF THE REF-FIRM invert
                                             # (the ref clears, the correct majority reads Fork-Shadow) -> undetectable.
                                             # DEFAULT = modal (@f904033ea §3: "designated OR the modal structure");
                                             # an explicit designated-override MAY be declared later, but never a fixed default.
    # v1 defer (mechanism §2.1): allowed_facets empty -> only structurally-identical Twins clear,
    # ANY off-key membership-set diff = Fork-Shadow, Variant deferred. Populate per-dimension later.

# verdict clause-phrasing (interface #4 -- governed, NOT hardcoded in the enricher).
# <D> = dimension name ("firm"); <of_name(s)> = human-readable sibling reference name(s).
phrasing:
  Canonical:   "canonical <D>-twin (reference) of <of_names>"
  Twin:        "canonical <D>-twin of <of_name>"
  Variant:     "<D>-variant of <of_name>"          # unreachable for firm (allowed_facets=[]); present for env/region
  Fork-Shadow: "divergent fork-shadow of <of_name> (debt)"
  Superseded:  "superseded by <by_name>"
  Orphan:      "orphan (no twin, no consumer)"
```

---

## 2. The `variance_verdict` consumer contract (firm dimension)

### 2.1 Signature + the two-path cost (mechanism §5 #3, unchanged)
```
variance_verdict(node, corpus=None) -> verdict | None
  corpus present (build_corpus path) : sibling group is FREE (whole set already loaded).
  corpus absent  (single-ARN --describe): exactly ONE targeted sibling-query on position_key.
```
Emitted as a PARALLEL `variance_prose_and_tokens` + its own `SummaryDoc.variance` field + its own render line
(mechanism §5 #1) -- NOT folded into the motif splice (that clause is argument-less; this one carries a
reference argument `<of_name>`).

### 2.2 The identity KEY: `position_key` = name-minus-firm-token (base Q1 fix, realized)
```
position_key(node) = node.name with any declared firm value-token replaced by the placeholder "{firm}"
                     (token match at a word boundary; the FIRST declared value that matches).
  opal-data-bd  -> opal-data-{firm}   |  opal-data-cot -> opal-data-{firm}  |  opal-data-inf -> opal-data-{firm}
  bd-49f-runner -> {firm}-49f-runner  (token 'bd' at boundary)   [C2/name grain, extensible]
```
- **Structure is NOT in the key** (the load-bearing Q1 fix): the key is the dimension-stripped LOGICAL
  identity ONLY. If `position_key` returns unchanged (no firm token matched) -> the node carries no firm
  dimension -> **no verdict** (counted in the denominator, never guessed).
- **GROUPING KEY = `(node_type, position_key)`, NOT `position_key` ALONE (~D collision fix, landed
  @566ea8cd7 -- rev.3 fold).** A bucket's twin is a BUCKET. Grouping on `position_key` alone collides
  `opal-data-bd` (S3_BUCKET) with its same-named `S3_BUCKET_POLICY` (whose bare arn IS the bucket name, and
  whose C2 membership is EMPTY). The empty-membership policy then wins the modal -> **INVERTS the verdict**
  (observed first run: bd=fork-shadow, cot=canonical -- garbage). This is the SAME collision class as the
  `--describe` resolution bug (@075f3ac5b) and the OWNED_BY polysemy. **So siblings = nodes sharing
  `(node_type, position_key)`,** each carrying a DISTINCT `firm` value.
- **EMPTY-MODAL-SUPPRESS:** if the modal membership-SET among the (typed) siblings is EMPTY, SUPPRESS the
  group -> **no verdict** (an empty set is not a reference; never let an empty-membership node define the
  modal). **REAL-ARN-PREFER:** on any residual tie, prefer a real-ARN resource over a bare-arn attachment
  (consistent with @075f3ac5b). Both landed in ~D's code @566ea8cd7; mutant-tested (M10).

### 2.3 The compared STRUCTURE = the motif-membership SET (base 231424Z realization)
```
structure(node) = frozenset( node's C2 motif-membership )   # e.g. {a-access, a-serve, a-store, b-io}
```
- This REUSES exactly what `~D` already computes -- the per-node C2 membership set (`_assemble_membership`,
  `summary_corpus.py` @ HEAD 76c310664). **No separate producer** (base's light-gate framing): the variance
  compare is derived from the membership-SET already in hand.
- The compare is on the SET, not a re-keyed structure (base's explicit guard): two firm-siblings are Twins iff
  their membership-SETS are EQUAL; a sibling whose set differs is the divergence. C3 (systems) is a projection
  of C2 and need not be compared separately (equal C2 sets => equal C3 sets); optionally corroborate with the
  C3 set, never as the primary key.

### 2.4 The symmetry test (firm-specialized; mechanism §3, allowed_facets=[])
For a sibling group at one `(node_type, position_key)` over `firm` (grouping key per §2.2 -- a bucket groups
only with buckets), with declared `values V = {bd,cot,inf}` scoped to the node's scope, `ref = the MODAL
membership-SET among PRESENT siblings` (empty modal -> suppress, §2.2) (the set with the strict plurality; NOT a
fixed firm -- base 234142Z correctness fix; among the modal-matchers designate the Canonical by a deterministic
tie-break, e.g. the alphabetically-first firm token -- that badge picks the reference LABEL, never the ref STRUCTURE):
```
present  = { firm_value(i) : i in group }
# (2a) COMPLETENESS
  a value in V (in-scope) MISSING from present, UNDECLARED  -> the present siblings each verdict per (2b);
                                                               the missing side is a divergence-by-absence
                                                               -> the group is asymmetric -> Fork-Shadow polarity.
  a MISSING value that is out-of-scope (declared absence)   -> legitimate; not counted against symmetry.
# (2b) STRUCTURAL SYMMETRY (membership-SET equality; allowed_facets=[] so no Variant tier for firm)
  ref = MODAL membership-SET among present siblings (strict plurality).
  a UNIQUE modal exists:
    structure(i) == ref                       -> instance i is a TWIN (one modal-matcher = designated Canonical). CLEAR.
    structure(i) != ref  (set differs; F=[])  -> instance i = FORK-SHADOW of the modal (debt).  # fires for ANY diverging firm, incl. the ex-anchor
  NO unique modal (tie for plurality: all-distinct 1-1-1, or an even split in a >3-value dim):
    -> NO canonical majority. FLAG ALL present as divergent (Fork-Shadow polarity, of_names = the other
       siblings, qualifier "no canonical majority"). NEVER silently pick a ref (base 234142Z). Counted, surfaced.
# other
  group of 1, no sibling, no consumer                                -> ORPHAN.
  two instances same (position_key, firm_value), one supersedes other -> older = SUPERSEDED.
  no declared dimension applies / position_key unchanged             -> None (no clause; in the denominator).
```

### 2.5 Output (from the catalog phrasing; no-guess)
```
{ kind:"Canonical",  dim:"firm", of_names:[<sibling names>] }  -> "canonical firm-twin (reference) of opal-data-cot/opal-data-inf"
{ kind:"Twin",       dim:"firm", of:<arn>, of_name:<name> }    -> "canonical firm-twin of opal-data-bd"
{ kind:"Fork-Shadow",dim:"firm", of:<arn>, of_name:<name> }    -> "divergent fork-shadow of opal-data-bd (debt)"
{ kind:"Fork-Shadow",dim:"firm", of_names:[<others>], note:"no canonical majority" } -> "divergent fork-shadow of opal-data-cot/opal-data-inf -- no canonical majority (debt)"
{ kind:"Orphan" }                                              -> "orphan (no twin, no consumer)"
{ kind:"Superseded", by:<arn>, by_name:<name> }               -> "superseded by <by_name>"
(none)                                                         -> NO clause (absent, counted in denominator)
# Variant is UNREACHABLE for firm (allowed_facets=[]); it exists in the catalog for env/region dimensions.
```

### 2.6 The no-feedback invariant (HONORED -- structural, never reads a label)
`structure(node)` is the deterministic C2 **membership SET** -- NOT an `llm_*` attribute. Variance NEVER reads
`llm_class`/`llm_description`; a class value can never change a verdict (identical discipline to the membership
clause at `summary_corpus.py:356-358`). Direction stays strictly `structure -> verdict`. The lint's FORBIDDEN
list already names "canon-deviation scorer / emergence / completeness / membership / promotion"; `variance_verdict`
is structural and reads only the membership-SET, so it is on the PERMITTED side (it decides a verdict from
STRUCTURE, and it never consumes a label). It is display-only in the enricher (graceful-degrades to no clause).

---

## 3. Worked example (grounded on the real bd/cot/inf buckets)

`position_key(opal-data-bd) = opal-data-{firm}`; siblings `opal-data-cot`, `opal-data-inf` (all present in the
graph @ 21:43Z). `structure(opal-data-bd) = {a-access, a-serve, a-store, b-io}` (verified live via
`comp-describe opal-data-bd` @ HEAD 76c310664).
- **Twin case:** `structure(bd) == structure(cot) == structure(inf) == {a-access,a-serve,a-store,b-io}`, all
  three present -> **(2a)** complete AND **(2b)** the modal set = that shared set, all three match -> all three
  TWINS (Canonical = the alphabetically-first modal-matcher, `bd`). CLEAR. Renders: `canonical firm-twin
  (reference) of opal-data-cot/opal-data-inf`.
- **Fork-Shadow (inf diverges):** `structure(bd) == structure(cot) = {a-access,a-serve,a-store,b-io}` (the
  MODAL, 2 of 3), `structure(inf) = {a-store, a-access}` (missing a-serve/b-io) -> inf differs from the modal
  OUTSIDE the empty `allowed_facets` -> **inf's bucket = FORK-SHADOW of the modal (debt)**; bd/cot = Twins.
  PRECISE, not "inf missing + an inf singleton" (the over-constrained-key failure the mechanism §6 calls out).
- **Fork-Shadow (BD diverges -- the case the fixed-ref bug HID, base 234142Z):** `structure(cot) ==
  structure(inf) = {a-access,a-serve,a-store,b-io}` (the MODAL, 2 of 3), `structure(bd) = {a-store,a-access}`
  -> **bd = FORK-SHADOW of the modal (debt)**, cot/inf = Twins. With a fixed `ref=bd` this INVERTED (bd cleared,
  cot+inf wrongly flagged) and a bd-drift was undetectable; the modal ref makes it DETECTABLE. This is why the
  ref is modal, not a fixed firm.
- **No-majority (all-distinct):** `structure(bd) != structure(cot) != structure(inf)`, all three different, no
  set shared by >=2 -> NO unique modal -> FLAG ALL as `Fork-Shadow, no canonical majority`; never pick a ref.

---

## 4. Coherence self-check vs the ratified mechanism `@f904033ea`

| Frozen mechanism element (@f904033ea) | Realized here |
|---|---|
| §2.2 `position_key` = dimension-stripped logical identity, structure OUT of the key (Q1) | §2.2 name-minus-firm-token; unchanged-key -> no verdict |
| §3 sibling group = same logical identity (a twin is the SAME kind of thing) | §2.2 grouping key = `(node_type, position_key)` (~D collision fix @566ea8cd7): a bucket's twin is a bucket, not its same-named policy; + empty-modal-suppress + real-ARN-prefer |
| §2.1 `allowed_facets=[]` for firm -> ANY off-key diff = Fork-Shadow (Q2) | §2.4 no Variant tier for firm; set-diff -> Fork-Shadow |
| §2.2 `structure` = the COMPARED thing, not the key | §2.3 structure = C2 membership-SET (base 231424Z), compared not keyed |
| §3 two-step: GROUP by position_key, COMPARE structure | §2.4 (2a) completeness + (2b) set-equality |
| §3 `ref = Canonical (designated, OR the modal structure)` | §2.4 ref = MODAL membership-SET among present (base 234142Z fix folded; fixed-firm ref removed -- it inverts on a ref-firm divergence, hiding a bd-drift). No-majority tie -> flag-all/never-pick |
| §4 POLARITY: CLEAR designed parallels, FLAG only Fork-Shadow/Orphan | §2.4 Twin/Canonical clear; only Fork-Shadow/Orphan flagged |
| §4 HARD firm invariant: Twin != fungible; never authorizes a merge | §2 the operator READS firm; never merges (never-cross lives in the adapter `denies`, not here) |
| §5 #1 parallel sibling clause (own field/render, reference arg) | §2.1 `SummaryDoc.variance` + own render line |
| §5 #4 phrasing read-from-governed-catalog | §1 `phrasing:` block |
| §5 #3 corpus-free build path / one targeted single-ARN query | §2.1 same |
| no-feedback (structure -> verdict, never a label) | §2.6 honored |

**One conformance note for base:** the mechanism §2.2 defines `structure = (motif-shape, role, edge-set)`
generically; this contract specializes it to the **C2 motif-membership SET** for the firm/bucket grain (base's
231424Z realization). That is a FAITHFUL restriction -- the membership set IS the motif-shape fingerprint at the
aggregate grain, and it reuses `~D`'s existing computation -- but it is a NARROWING of the generic structure to
its motif-membership projection. Flagging it explicitly so your coherence-check ratifies the narrowing (rather
than discovering it): for firm at the bucket grain, membership-SET symmetry == structural symmetry; if a future
dimension needs role/edge-set diffs beyond membership, the generic §2.2 structure is the fallback.

---

## 5. Routing
- **base (coherence-keeper)** -- check this vs `@f904033ea`; confirm the membership-SET narrowing (§4 note) and
  that the compare is on SET symmetry, not a re-keyed structure. On your GO, base relays to `~D`.
- **`~D`** -- wire `variance_prose_and_tokens` + `SummaryDoc.variance` + render line, reading the phrasing from
  the governed catalog; `structure()` = the C2 membership-SET already computed. Zero rework to the motif splice.
- **CTO / MSTR** -- canonize `variance_dimensions.yaml` (governed file) + fold into the rule bank (NEXT-3);
  the D3 conformance-terminology ruling binds the label prose, not the mechanism.
- **me (~C)** -- own the catalog content + this contract; hand on base GO.

*-- 0.8.0_AE_CloudComp~C. Variance firm-dimension catalog + consumer contract; realizes @f904033ea for firm.*
