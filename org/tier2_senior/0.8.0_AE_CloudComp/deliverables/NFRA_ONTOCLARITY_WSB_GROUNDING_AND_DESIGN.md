# NFRA_ONTOCLARITY WS-B -- Layering crosswalk + Relation-vs-Role lint: grounding + design (for COO/CTO review)

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-19. **TO:** `NFRA_ONTOCLARITY.WS-B.layering-nesting-crosswalk-and-lint`
(COO, staged). Inherits WS-A's two-layer root fix (@f7eef81f1). **Gate path:** COO design review -> CTO arch-gate
(any "which scheme is canonical" decision) -> RAVC -> CVO SEMANTIC-verify per fog class. Load-bearing: ambiguity
GONE, not reworded; the lint must FIRE on a seeded violation (EXERCISED, not prose).

## 1. Grounding -- the 2 WS-B fogs (Phase-1 denominator, source per Rule 22)

### fog-6 LAYERING (brief S3b, high-severity): FIVE incompatible "layer/plane" numbering schemes, no crosswalk
| # | Scheme | What it numbers | Source |
|---|---|---|---|
| 1 | **C0-C3** | the COMPRESSION axis (facts->interactions->motifs->systems) | `RULE_BANK.yaml meta.layers.layer_1_cse_algebra` (WS-A); `cse_schema.py`; `01_substrate.md` |
| 2 | **the `layer` field** | the SUBSTRATE axis (aws / portal / ms / pipeline) | the graph node `layer` property; `01_substrate.md` flags "layer" OVERLOADED |
| 3 | **`semctl` (the "fifth layer exception")** | the semantic-control promotion plane | NFRA_SEMCTL / comp_honesty |
| 4 | **GLOBGRPH L1-L7** | the graph-BUILD design stages | globgrph design numbering |
| 5 | **recognizer A-B-C-D -> "Territories"** | the recognizer planes | NFRA_COMPILERKIT recognizers |
KEY INSIGHT (the disambiguation, not a reword): these are NOT incompatible numberings of the SAME thing -- they
are ORTHOGONAL AXES (compression vs substrate vs promotion vs build-stage vs recognizer-plane). The fog is that
they share the word "layer/plane" with no map saying WHICH AXIS each numbers. The crosswalk states that once.

### fog-7 NESTING (brief S3c): the Relation-vs-Role composite exception is prose, nothing enforces it
Three edges are DUAL-AXIS (a base Relation PLUS a Role); all others single-axis: `routes-to`->Router,
`resolves-through`->Registry, `projects`->Gateway (RULE_BANK.yaml `relation_composites`, e.g. `projects: {..,
role: Gateway}`). A classifier must KNOW this 3-item exception list; today it's a prose "load-bearing subtlety"
that nothing checks -> re-drifts on the next reader (Rule-20 "cannot block = not a gate", at the definitional layer).

## 2. Design

### (a) ONE crosswalk table (AC-1) -- one canonical place, inheriting WS-A's two-layer root
Home: `infra/system/01_substrate.md` (where "layer" is already flagged overloaded -- the reader's point of
confusion) as the /system representation, CITING the canonical axis-definition. The table reconciles the 5
schemes with a column per scheme + a row stating WHICH AXIS each numbers + how they relate to WS-A's two layers
(C0-C3 = layer_1 compression; the rest = substrate/build/plane axes ORTHOGONAL to the archetype layer). Consumers
reference this one table; it does not re-number anything (no new scheme -- the fix is the MAP, not a 6th scheme).
POSSIBLE ARCH-DECISION (surface to CTO): is there a SINGLE canonical layering, or is the resolution "they are
orthogonal axes, the crosswalk maps them, none is THE layer"? [My rec: orthogonal-axes + crosswalk -- there is no
one canonical "layer" because they measure different things; forcing one would be false.]

### (b) Relation-vs-Role LINT (AC-2) -- EXERCISED, not prose
A machine check (comp-tool) that reads the rule-bank's declared dual-axis exceptions (the `relation_composites`
carrying a `role:` field = exactly {routes-to->Router, resolves-through->Registry, projects->Gateway}) and
asserts the invariant: a relation yields a Role IFF it is one of those 3. It FIRES (non-zero) on a seeded
violation -- e.g. a 4th composite claiming a `role:` (over-broad), or one of the 3 dropping its role (under). Self-
test with a seeded mutant proves it fires (the exercise, not a prose claim). Home: a `.tools/comp-*` lint or an
`org/modules/graph/*.py` check reading RULE_BANK.yaml (the WS-A canonical source). WS-2 06-gate applies if it
lands under a comp-system _SOURCE path -> run comp-system + stage 06 at commit.

## 3. Open items for COO -> CTO
1. Crosswalk canonicality: orthogonal-axes-map vs one-canonical-layer? [rec: orthogonal-axes-map.]
2. Lint home + name: `.tools/comp-ontolint` (rail-registered comp-tool) vs an `org/modules/graph/` check? [rec:
   a comp-tool so it's runnable + rail-visible; NFRA_COMPREG registration is the SoD step.]

## 4. Land path
COO review -> CTO on the 2 open items -> build crosswalk (01_substrate) + lint (+ self-test seeded mutant) ->
CTO arch-gate -> RAVC -> CVO SEMANTIC-verify (layering ambiguity GONE + the lint FIRES on a seeded violation).
Feeds WS-D (log the clarified defs in system/sdk). Then WS-C (process tie-breakers).
