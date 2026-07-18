# COMPSIMILAR PH2 -- Deterministic Motif Enrichment of the per-ARN Summary

**Design-of-record.** Author: 0.8.0_AE_CloudComp (base, FEED lane / design-of-record, LD-0305).
Date: 2026-07-18 ~0204Z. Status: **C2 = DESIGN (feasibility-affirmed) -> CTO arch-gate -> ~D builds.
C3 = HELD pending NFRA_ONTOLOGY (universal archetype layer, Andrew-direct 3 below).**

**What this is:** a DETERMINISTIC enrichment of the per-ARN summary CONTENT produced by
`derive_summary()` (`org/modules/graph/debtscan/summary_corpus.py:256`). It splices, into the
summary string, the canonical MOTIF CLASS + ROLE a node instantiates (C2) and the SYSTEM it is a
member of (C3). No LLM, no judgment -- every spliced token comes from a fixed catalog
(`canon-patterns.yaml`, CTO v0.1) + a pure structural position.

**Substrate (already shipped):** the `--describe` surface landed @ff21627b0 (~D) directly on
`derive_summary`. The enrichment enriches `derive_summary` itself, so BOTH `--describe` and the
later `--neighbors` similarity path inherit it. It is a PH2 CONTENT enhancement, NOT a PH1 scope
change, and it is consistent with CTO ruling-1 (corpus v1 = DERIVE-AT-SCAN): this is a
deterministic derive-at-scan enrichment from graph structure + a fixed catalog -- it is NOT the
authored `resource_summaries` overlay (that stays Phase-3).

---

## Andrew-direct provenance (VERBATIM -- the phrasing IS the ruling)

**(1) Design input, via MSTR relay (20260718T015015Z; Andrew-direct at the MSTR terminal):**

> THE IDEA: today's per-ARN summary is type + layer + edge-neighborhood -- and its tail degrades
> to low signal ("consumed by X; produced by Y; (+113 more)"). Enrich it DETERMINISTICALLY by
> splicing in the canonical MOTIF(s) the node instantiates + its ROLE + its SYSTEM membership. No
> LLM, no judgment -- because the motif classes are already a FIXED, NAMED catalog
> (canon-patterns.yaml: SERVED_LINEAGE_CANON, AUTH_CANON, code-runner, served-render), and a
> node's role in a motif is a pure structural position.
>
> TWO CLAUSES (Andrew's framing):
> - C2 motifs -> "instantiates <MOTIF_CLASS> as <role>" (from comp-canon-motif).
> - C3 system -> "member of <pipeline/system>" (from pipescript named-thread membership, or the
>   motif-class grouping). Andrew clarified: this goes INTO the summary string itself, not a
>   naming/community exercise -- use the fixed catalog labels, keep it deterministic.
>
> BONUS: comp-canon-motif's twin_shadow_guard keys motif-identity on (firm, layer, logical-stage)
> -- so the summary can deterministically assert "canonical firm-twin of X" vs "divergent
> fork-shadow (debt)". [...] DETERMINISM IS THE REQUIREMENT [...] If any clause would need
> inference to name, it doesn't go in the string.

**(2) Andrew-direct correction, in-session (2026-07-18, to 0.8.0_AE_CloudComp base):**

> its a class thing yes, but if you recall, its a class that is decomposable with full fidelity,
> therefore should be possible to identify c2 and c3 membership in the summary

This corrects an over-conservative first read (base had flagged "comp-canon-motif emits a
CLASS-level scorecard, not a per-node role map" as a feasibility seam). **The correction is
right and binding:** see below.

**(3) Andrew-direct charter (2026-07-17, MSTR terminal, VERBATIM; relayed 20260718T020523Z --
recorded+broadcast by MSTR under XXX.md law) -- REFRAMES the C3 clause:**

> Yeah it's time for us to develop a true universal ontology for this purpose. i think systems
> ontological language should be agnostic, not opal-scoped or aws-scoped or etc, its plain english
> semantics, but designed to be relational archetypal

Disposition (MSTR, this relay): a UNIVERSAL ARCHETYPE layer (provisionally **NFRA_ONTOLOGY**,
charter being shaped with Andrew now, routed through Tier 1) sits ABOVE `canon-patterns.yaml`;
`canon-patterns` becomes the AWS-BINDING ADAPTER mapping concrete types (S3_BUCKET, READS, bd/cot
twins) onto substrate-neutral archetypes (Store, Producer, Guard, Twin, Fork-Shadow...). **C2
(motif class + role) STANDS. C3 (system membership) is HELD** -- it should read the UNIVERSAL
layer, not raw `canon-patterns`. **DO NOT BUILD the universal layer yet (awareness only);** base
is the named likely builder (deepest in the graph/motif/ontology surfaces), pending the Tier-1
decomposition.

---

## The capability -- AFFIRMED (Andrew-direct 2)

The canon motif classes (`canon-patterns.yaml`) are defined as **structural path-shapes** --
ordered `node_type`/`edge_type` sequences (e.g. DEPLOY: `(S3_BUCKET 'code/' prefix)-[READS]->(EC2|LAMBDA|ECS runner)`;
SERVED_LINEAGE: `(Field gold)-[SERVED_FROM]->(ServedURL)-[FETCHES]->(DataFetch)-[FLOWS_TO*]->(JSXRender)`).

A structural class definition is, by construction, **decomposable to its instances with full
fidelity**: the class census IS the set of concrete matched paths (`canon-patterns.yaml`
`scorer_contract` promises exactly "per-pattern instance census -- every concrete path matched to
its motif-shape"), and every matched path names its constituent nodes and their positions. So the
projection **class -> instance -> (node, role)** is LOSSLESS. Therefore per-node **C2 (which class
+ what role)** and **C3 (which named system)** are recoverable deterministically and spliceable
into the per-ARN summary.

**The "seam" base first flagged was a build-surface detail, not a fidelity loss.** The current
`comp-canon-motif` (`canon_motif_scorer.py`) AGGREGATES that instance census up to class-level
scalars because its job is OUTLIER-scoring (dominant-motif share + the AC4 novel-candidate tail).
The per-node decomposition is the **same data read at instance grain** -- not new information.

---

## Design -- per-node motif decomposition

For each node, run the structural motif-match against the fixed catalog over the node's LOCAL
neighborhood (the SAME `{node_type, layer, in_edges, out_edges}` `derive_summary` already loads --
no new full-corpus scan for the single-ARN path), then splice:

- **C2:** `"instantiates <CLASS> as <role>"` -- CLASS from `canon-patterns.yaml` (fixed), ROLE from
  the structural position the node occupies in the matched motif (e.g. `S3 tail of
  SERVED_LINEAGE`, `store of the code-runner (DEPLOY) motif`, `served-render tail`).
- **C3 (HELD -- Andrew-direct 3):** `"member of <system>"` -- the named-thread / pipeline the node
  belongs to. The mechanism (full-fidelity from `pipescript` named-thread membership, or the lighter
  motif-class + firm/layer grouping) is decomposition-feasible TODAY, but the CLAUSE IS HELD: per
  Andrew-direct 3, C3 must read the UNIVERSAL archetype layer (NFRA_ONTOLOGY), not raw
  `canon-patterns`. Do not build C3 against `canon-patterns` in the interim. C2 does not depend on
  C3, so C2 proceeds independently.
- **Twin/shadow (bonus):** group instances by `(firm, layer, logical-stage)` across firms; a node
  with a SYMMETRIC cross-firm set is a `Twin`, an ASYMMETRIC one a `Fork-Shadow (debt)`. NOTE:
  `Twin`/`Fork-Shadow` are named in Andrew-direct 3 as UNIVERSAL ARCHETYPES -- so this bonus'
  label vocabulary should ADOPT the universal-layer terms when NFRA_ONTOLOGY lands (the
  computation -- symmetric-vs-asymmetric cross-firm set -- is unchanged; only the labels bind
  upward). Corpus-level op (needs the cross-firm set): full-fidelity in `build_corpus`, targeted
  twin-set query in the single-ARN `--describe` path. Doubles as the supersede/decommission signal
  COMPSIMILAR exists for.

**Determinism (the requirement, satisfied):** every spliced token is a fixed-catalog label
(canon class), a structural position (role), a named-thread label (pipescript), or a
firm/layer/stage node-property -- no inference. A node whose neighborhood matches NO catalog motif
gets NO C2 clause; a node in no named thread gets NO C3 clause (they are simply omitted -- never
guessed). Coverage is printed as a denominator, reusing the existing UNKNOWN-thin control:
`"N of M nodes matched >=1 motif; K unmatched (no motif clause)"`.

### BEFORE / AFTER (Andrew's example)
```
BEFORE:  S3_BUCKET 'opal-data-bd': consumed by bd-49f-fees-runner; produced by bd-49f-runner; (+113 more)
AFTER:   S3_BUCKET 'opal-data-bd': S3 tail of SERVED_LINEAGE_CANON; store of the code-runner motif
         (read by bd-49f fees/ownership/runner/session-trigger); firm-twin of opal-data-cot/inf
```

---

## Build notes -- the instance-grain sources (operational, NOT feasibility blockers)

"Decomposable with full fidelity" is realized by reading each class at INSTANCE grain from its
RIGHT surface. Each surface is modeled and deterministic; the note is about WHERE the fidelity
comes from, not WHETHER it exists:

| Class | Instance-grain source | Note |
|---|---|---|
| SERVED_LINEAGE_CANON | canonical graph (SERVED_FROM / FLOWS_TO modeled) | scored today; role = position in the served chain |
| DEPLOY_CANON (code-runner) | code/-prefix grain via deploy-ledger / pipescript; bucket-grain approximable on the canonical graph (bucket `-[READS]->` runner) | canonical DB is BUCKET-grain (no code/-prefix nodes) -- the code-prefix source gives the full-fidelity role; bucket-grain is the coarse fallback |
| PIPELINE_CANON + C3 | `comp-pipescript` named-thread membership | interior (bronze->gold) is NOT in the canonical DB; it is full-fidelity in pipescript. **C3 HELD** -- consume via the NFRA_ONTOLOGY universal layer, not raw canon-patterns (Andrew-direct 3) |
| AUTH_CANON | `comp-routes` BEHAVIOR | `TRIGGERS` to the auth-edge is UNMODELED on the canonical graph -- the auth role sources from routes behavior, not the graph edge (scorer's own note) |

Other build seams: (a) the current `canon_motif_scorer.py` emits class-aggregate scalars +
DEPLOY/PIPELINE legs are "NOT SCORED HERE" (unwired class-census legs) -- the per-node
decomposition wires them at instance grain, it does not consume the scorecard; (b) identity: the
scorer emits `node_id`, `summary_corpus` keys on `arn` -- both are CloudNode properties, so the
join is a resolvable step (one query), not free; (c) `canon-patterns.yaml` is CTO-owned -- any new
role/system vocabulary spliced into the string is a CTO canon edit (determinism + governance both
hold there).

---

## Governance constraint (CTO, BINDING -- 20260718T021711Z) + proposed role vocabulary

CTO GO'd the C2 framing (derive-at-scan structural splice, consistent with ruling-1) with a
BINDING constraint: **every role/system token spliced into the summary string MUST come from
`canon-patterns.yaml` -- the vocab is CLOSED + CTO-owned, NO token invented at splice time.** The
enricher reads the label set FROM `canon-patterns` (NOT a hardcoded list), so blessing a label ==
editing `canon-patterns`. CTO confirms the exact C2 label set at the arch-gate when ~D's build
lands.

**Implication (design-of-record):** `canon-patterns.yaml` v0.1 carries NO explicit, enumerable
role-label field today -- the roles are implicit in the motif SHAPE strings (e.g. DEPLOY's
`(S3_BUCKET 'code/' prefix)-[READS]->(runner)`). To satisfy "read the label set FROM canon-patterns",
a per-class `roles:` vocabulary must be ADDED to `canon-patterns` (a CTO-blessed addition), keyed by
structural position. **Proposed shape (base FEED -- CTO blesses/adjusts at the gate; nothing here is
canon until CTO edits the file):**

```yaml
# per pattern in canon-patterns.yaml, a new machine-readable field the enricher reads:
roles:                      # structural-position -> the canon label spliced as "<role>"
  SERVED_LINEAGE_CANON: { gold_field: "served-source", served_url: "served-url",
                          data_fetch: "fetch", jsx_render: "render-tail", s3: "S3 tail" }
  DEPLOY_CANON:         { code_prefix: "code-store", runner: "code-runner" }
  AUTH_CANON:           { route: "auth-route", edge_fn: "auth-edge", origin_s3: "auth-origin" }
  PIPELINE_CANON:       { bronze: "pipeline-bronze", silver: "pipeline-silver",
                          gold: "pipeline-gold", served_s3: "pipeline-served-store" }
```

The enricher maps a node's structural position (its `node_type` + the edge direction/neighbor
types it matches in the motif) to the role key, then reads the LABEL from this field. A position
with no canon role label -> no clause (never invented). This keeps determinism + governance AT THE
STRING, exactly as CTO required. AUTH/DEPLOY/PIPELINE roles depend on their instance-grain source
being wired (see build-notes table); the vocabulary is defined regardless.

## Handoffs

- **CTO** -- arch-gate the enrichment; canon-vocabulary owner (`canon-patterns.yaml`). Confirm the
  role/system label set is canon-blessed so every spliced token is governed.
- **~D** -- builder (COMPSIMILAR lane), layers this on the shipped `--describe` engine. base FEEDS
  the decomposition/role-mapping walkthrough on pickup.
- **COO** -- COMPSIMILAR registry row (PH2 content enhancement).
- **MSTR** -- source of relays (1) + (3); shaping the NFRA_ONTOLOGY charter with Andrew; routes
  the Tier-1 decomposition. base is the named likely NFRA_ONTOLOGY builder -- but DO NOT build yet.

**NFRA_ONTOLOGY dependency (Andrew-direct 3):** C2 (motif class + role) is independent and
proceeds. C3 (system membership) + the Twin/Fork-Shadow label vocabulary bind to the universal
archetype layer and WAIT for it. When the charter lands, `canon-patterns.yaml` is reframed as the
AWS-binding adapter beneath a substrate-neutral, plain-English, relational-archetypal ontology.
