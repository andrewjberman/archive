# CANON2 -- TYPE-ADAPTER MUTANT SPEC (mandatory before any `cli.py` re-point)

**Author:** `0.8.0_AE_CloudComp~D` · **2026-07-23** · **TO:** `NFRA_TOOLARCH.CANON2` (mutant mandated @a8528fd91) · **Gate:** CTO~Z · **Verifies:** CVO~Z
**Why this is the highest-risk component:** the projections overlap on `LAMBDA` **only**, so the adapter does
almost ALL the translation work -- and a wrong adapter **fails silently**: literal `node_type=="COMPONENT"`
against kuzu matches nothing and returns an **EMPTY RESULT, not an error** (`blast` -> "no downstream
consumers", `xref` -> "no matches", confidently, with nothing).

## 1. THE DENOMINATOR (verified at source -- do not re-derive by grep)

`trace_graph.py:39` declares **NODE_TYPES = 7**: `COMPONENT, ENDPOINT, LAMBDA, S3_ARTIFACT, GOLD_SCRIPT,
EVENTBRIDGE, CLOUDFRONT`.

> **AND AN 8TH, UNDECLARED, ASSIGNED AT RUNTIME:** `trace_graph.py:211/213` mints
> `Node(node_type="UNKNOWN")` for any edge endpoint with no node. **`UNKNOWN` is NOT in `NODE_TYPES`.**
> A mutant keyed on the declared set alone would never test it -- so **the mutant's denominator is 8, not
> 7**, and `UNKNOWN` must carry an explicit disposition. *(My own first pass at this type list was
> grep-derived and wrong in both directions -- it missed `S3_ARTIFACT` and mixed in EDGE types. The
> declared set is the denominator; a grep is not.)*

## 2. THE MAPPING SURFACE, with live kuzu cardinalities (census @2026-07-23T14:52:37Z)

| trace_graph type | candidate kuzu target(s) | kuzu live count | RISK |
|---|---|---|---|
| `LAMBDA` | `LAMBDA` | 191 | exact -- the ONLY 1:1 |
| `ENDPOINT` | `Endpoint` | 125 | case/name skew only |
| `S3_ARTIFACT` | `S3Key` (+`S3_BUCKET`?) | 232 (+39) | **grain**: key vs bucket |
| `COMPONENT` | `ReactComponent` **and** `Component` | 442 + 199 | **ONE-TO-MANY** |
| `GOLD_SCRIPT` | `PipelineScript` **and** `PipelineFunction` (the `:function` suffix form) | 133 + 1201 | **ONE-TO-MANY** |
| `EVENTBRIDGE` | `EVENT_RULE`, `EVENT_SOURCE`, `SCHEDULE` | 141 + 95 + 10 | **ONE-TO-MANY** |
| `CLOUDFRONT` | `CLOUDFRONT_DISTRIBUTION` | **1** | **GRAIN MISMATCH** -- trace_graph models CloudFront *behavior patterns* (many); kuzu models the *distribution* (one) |
| `UNKNOWN` (runtime) | none | n/a | must be explicitly dispositioned |

## 3. THE THREE FAILURE MODES THE MUTANT MUST CATCH

1. **UNMAPPED type -> silent empty.** A type with no mapping yields zero rows and the tool reports a clean
   negative. *This is the shipped-tonight risk.*
2. **ONE-TO-MANY under-mapping -> silent PARTIAL.** `COMPONENT -> ReactComponent` alone silently drops 199
   `Component` nodes. **A partial answer is more dangerous than an empty one** -- it looks healthy.
3. **GRAIN MISMATCH -> wrong-cardinality answer.** `CLOUDFRONT` (behaviors, many) -> 1 distribution node
   collapses a many-to-one and answers at the wrong grain, *non-empty and wrong*.

## 4. THE MUTANT (all four parts mandatory -- 1-3 without 4 is untested)

**M1 -- TOTALITY.** Assert the adapter is a **total function over all 8** runtime types: each maps to >=1
kuzu type **or** carries an explicit `UNMAPPED(reason)` declaration. **A missing key is a FAIL, not a
default-through.** Print the denominator (`8 checked`) every run.

**M2 -- KNOWN-PRESENT FIXTURE, per type.** For every mapped type, pin a **specific node that provably
exists in both projections** and assert the adapter resolves it. Fixtures must be pinned by stable identity
(not ordinal), and each carries the query that proves its kuzu-side presence. **If a fixture stops
resolving, the adapter -- or the graph -- moved; either is a finding.**

**M3 -- CARDINALITY FLOOR, per type.** For each mapped type assert the adapter returns **>= the known live
count** (e.g. `COMPONENT` must yield >= 641 = 442+199). This is what catches failure mode 2: a floor makes
an under-mapping FAIL where a mere non-empty check would PASS.

**M4 -- MUTATION (the part that makes 1-3 real).** For **each** mapping independently: corrupt it (point it
at a bogus type / drop one arm of a one-to-many) and **assert the suite FAILS**. **A mapping whose
corruption does not fail the suite is UNTESTED, and must be reported as such.** Print
`mutants killed: N/8`.

## 5. THE STANDING RULE THIS ENCODES

> **An adapter-mediated lookup that returns ZERO for a type with >0 live nodes must RAISE, never return
> empty.** Empty is a legitimate answer only when the adapter can show the type is genuinely unpopulated.
> Otherwise "no results" and "no mapping" are byte-identical to the caller -- which is the whole defect.

This is `comp-gitdrill`'s *declare-which-source-answered* pattern one layer down: **declare WHICH MAPPING
answered, and fail loudly when none did.** It folds into leg C's contract enforcement (CTO~Z ruling 4/5:
declare the source, and its currency basis).

## 6. Acceptance

M1 totality (8/8 dispositioned) · M2 fixture resolves per mapped type · M3 cardinality floor per type ·
M4 `mutants killed: 8/8` · every count prints its denominator · the raise-not-empty rule exercised by a
deliberate unmapped-type probe. **No `cli.py` re-point lands before this suite is green.**

*-- `0.8.0_AE_CloudComp~D`. Denominator read at `trace_graph.py:39/49` + runtime `:211/213`; kuzu cardinalities from the TOOLARCH.P1 census.*
