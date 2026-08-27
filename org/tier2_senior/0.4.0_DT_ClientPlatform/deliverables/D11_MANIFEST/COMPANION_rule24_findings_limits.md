# SC-m-3 COMPANION — Rule 24 record, routed findings, C3-chain status, instrument disclosures

**Cell:** `SC-m-3` · **TO:** `NFRA_SUBSTRATECARDING.TO-W1-DTX.graph-object-manifest`
**Compiled by:** `0.4.0_DT_ClientPlatform~X` · **Compiled:** 2026-08-26T19:33Z · **Evidence vintage:** HEAD `14da312322`
**Manifest:** `graph_object_manifest.json` (39 parts, VALID against `org/standards/L0_GRAPH_SUBSTRATE_MANIFEST.schema.json`)

> **WHY THIS FILE EXISTS.** The adopted L0 schema is `additionalProperties: false` at its top level with
> exactly five keys — `schema_version`, `compiled_by`, `as_of`, `denominator`, `parts`. The Rule 24
> record, the routed findings and the instrument disclosures **cannot ride inside it**. TO s.8 permits
> the four-postulate record *"in the manifest or beside it"*; this is beside it.

---

## 1. DTX-AC3 — THE CLASSIFICATION RECORD, FOUR FIELDS, FOUR DISPOSITIONS

⛔ **TWO FIELDS, NOT ONE AXIS — AND THE SPLIT IS MEASURED, NOT ASSUMED.** The TO warned that postulate
(iii) was where Andrew's phrasing would fail, because *"authoritative vs projection"* is **standing**
and *"heavy vs light"* is **weight**. I tested it rather than assuming it.

### 1.1 `authority_role` — REUSED VERBATIM, NOT MINTED

| | |
|---|---|
| source of truth | `org/standards/SUBSTRATE_CARD.schema.json` → `properties.artifact.properties.persistence.properties.authority_role` |
| enum | `source` · `projection` · `evidence` · `reference` · `none` |
| existing record | carries its own `x-rule24` at **verdict `pass`**; adopted intent verbatim: *"tell a consumer whether editing this changes the world or gets overwritten"* |
| why reused | The build ladder puts an existing ratified term above a re-coined one, and **a vocabulary re-coined beside a ratified term is the same duplicate one layer up.** Reusing it, and saying so, is the better outcome. |

⚠ **CORRECTION OF RECORD.** TO s.4 locates this enum at `artifact.location`. **It is at
`artifact.persistence`.** I found this by reading the schema rather than citing the TO — my first probe
at `artifact.location` returned `['home','projection_of','co_resident_stores','basis','evidence','owner']`
and no `authority_role`. Recorded because a cited path that does not resolve is how a reuse claim
quietly becomes a mint.

### 1.2 `weight_class` — MINTED. Full four-postulate record.

**Values:** `heavy` (bulk-scanned or bulk-rebuilt; cost dominated by volume; not interactively
traversable) · `light` (traversable/queryable at interactive latency).

- **(i) MECE** — *declared domain:* every persisted graph-bearing object this census enumerated across
  all planes. **Exclusivity:** PASS, the two values are disjoint as defined. **Coverage:** PASS, and the
  uncovered member was **hunted rather than assumed** — the untracked JSON envelopes and the leaked
  `rebuild.tmp` set were the candidates most likely to fit neither, and both resolve to `heavy`.
- **(ii) SAME GRAIN** — the domain spans an Iceberg **table**, a file on **disk**, an **S3 object** and a
  local **cache**. *Those are not one grain.* **Remedy taken:** every part declares plane + `part_class`
  explicitly, and `weight_class` is asserted at the grain of **the persisted object** in all cases. The
  axis is not asserted across grains without that declaration. Verdict: **pass-with-declared-split**.
- **(iii) INTENT COHERENCE — THE POSTULATE THE TO FLAGGED, AND IT IS ANSWERED BY MEASUREMENT.**
  If weight and standing co-varied, one field would do. **They do not, and here are the two
  counterexamples from this census:**

  | store | weight | standing | why it breaks the bundle |
  |---|---|---|---|
  | `graph_contracts` | **LIGHT** (21 objects) | **`source`** — a governed Iceberg table | light **AND** authoritative |
  | `kuzu_nessie_db` | **HEAVY** (82,567,168 B) | **`projection`** — rebuilt by every derive | heavy **AND** a projection |

  **Conclusion: orthogonal on measured members of this domain.** Andrew's phrasing bundles standing with
  weight; this manifest ships them as **two fields**. Verdict: **pass — one field, one intent, because
  the bundle was split.**
- **(iv) STATE COHERENCE** — Does one remedy move every value together? **NO, and naming which do not
  move is mandatory.** `weight_class` moves only if a store is re-engineered (compacted, re-homed,
  re-formed) — a *build* act. `authority_role` **does not move on a rebuild at all**; the schema's own
  record says *a projection promoted to source is a governance act, not a refresh.* So a cadence fix
  moves **neither**, and a re-home moves `weight_class` without touching `authority_role`. **That
  non-co-movement is precisely why they are two fields.**

### 1.3 `materializer_standing` — ADOPTED, and adoption is an authoring act

From `org/standards/L0_GRAPH_SUBSTRATE_MANIFEST.schema.json` (`1.0.0_SA_CTO~X`).
Enum: `canonical` · `historical_in_use` · `superseded` · `unknown`. Applied to the materializer-bearing
parts only.

⛔ **WHY IT IS CARRIED ALONGSIDE THE CURRENCY CLAIM RATHER THAN INSTEAD OF IT.** They answer different
questions — currency asks *is this the most-updated script*, standing asks *what role does it play now*
— and **standing has a value currency cannot express: `historical_in_use`.** Without it, a frozen July
artifact that today's derive actually consumes must be recorded as either *current* (false) or
*superseded* (false).

⛔ **`historical_in_use` IS THE MOST DANGEROUS STANDING IN THE SCHEMA BECAUSE IT WORKS.** A frozen
artifact silently feeding today's derive breaks nothing and alarms nobody — **neither a staleness check
(it is in use) nor a liveness check (it works) can find it.** Measured live on
`motif_c2c3_materialize{,_ab}.json`: today's derive logged `specs=3`, the two frozen July class specs
**plus** the live composition (`1.0.0_SA_CTO~X` 73215 Q2, cited not re-derived).

Four postulates: **(i)** MECE over *materializers of a graph layer*, `unknown` closing the population
honestly · **(ii)** every value at the grain of **a materializer**, never mixed with its output ·
**(iii)** single intent — role in the *current* pipeline, deliberately not bundled with currency ·
**(iv)** values do **not** move together and **the remedies differ**: `superseded` → retire;
`historical_in_use` → **a MIGRATION, because its consumer must change first and no act on the artifact
alone can remedy it**; `unknown` → a measurement, not a fix.

### 1.4 `temporal_claim` — ADOPTED **WITHOUT** A FOUR-POSTULATE RECORD, AND SAYING SO IS THE POINT

Enum: `current_state` · `point_in_time` · `timeless` · `unknown`.

⛔ **THE RECORD IS ABSENT AND IT IS ROUTED, NOT SUPPLIED BY ME.** `2.0.0_SA_COO~X` measured the gap
(73225 §3) and ruled explicitly: **use the field, state that it was adopted without the record, and do
not author the record yourself** — *"you would be authoring a taxonomy for another seat's contract, and
the enum's owner is the one who can say what domain it partitions."* Routed to `1.0.0_SA_CTO~X` as the
schema's owner; a record landed at `54b9d6f37d` after my adoption.

**Why the field earns its place anyway:** it makes a violation *expressible*. A part claiming
`current_state` while measurably stale is a **testable** contradiction — which is exactly what
`resource_summaries` (39d), `graph_contracts` (71d), `.comp-graph/graph.json` (20d) and
`kuzu_nessie_db.s3` (20d against a **declared daily** cadence) now are on the manifest's face.

⛔ **THE FAILURE MODE OF THIS FIELD, WHICH I FLAG BECAUSE IT TAKES ONE WORD TO TRIGGER:** a part whose
**claim** and **vintage** disagree has two remedies — *refresh the part*, or *downgrade the claim* —
and **choosing the second to make the violation disappear is laundering.** A field designed to catch
stale parts can be turned into a way to hide them.

---

## 2. THE SEMANTIC-DEFECT AXIS — UNMEASURED ESTATE-WIDE, AND THAT IS THE HONEST ANSWER

**Andrew, verbatim (1907Z):** *"not legacy shit that may have weird deprecated opinionation, filtering,
questionable definitions and resolution, etc"*

⛔ **THIS IS A SEMANTIC CLASS, NOT A VINTAGE CLASS.** A materializer can have run **this morning** and
still encode a deprecated opinion. **Every freshness instrument this estate holds — mtime, snapshot id,
per-table last-write, the wave `as_of`, the `comp-kuzu` provenance header — is structurally blind to
it.** A methodology row resting on *"the generator ran recently"* is **not responsive** to what he asked.

**`1.0.0_SA_CTO~X` (73215 Q3) and `2.0.0_SA_COO~X` (73208 ruling 2) converged independently:** no
instrument in this estate discriminates it; **`UNMEASURED` is the correct answer; do not invent a proxy.**

⛔ **THE REFRAME THAT MATTERS — THE REMEDY IS A CONTRACT, NOT A SCANNER.** `1.0.0_SA_CTO~X`'s framing:

> *"The defect is not 'wrong opinion'. It is 'opinion that cannot be found.'"*
> `ANCHOR_CATALOG = {...}` — content may be wrong, but it is a **visible dict. Reviewable.**
> filtering inside a loop — content may be fine and **nobody can ever tell. Unreviewable.**

Hence `generation.declared_opinions` in the L0 schema, with **`null` a legal and LOUD value** meaning
*the opinions are buried and this part is unreviewable on the semantic axis* — **which is itself the
finding.** In this manifest, `declared_opinions` is `null` on **39 of 39 parts**. That is not a blank;
it is a measured statement that **no part of this graph substrate declares its opinions.**

⛔ **AND WHY PER-PART SILENCE MUST NOT READ AS CLEAN.** Per `0.8.0_AE_CloudComp~X` (73195), where this
class *has* been caught it was caught **incidentally** — C2's vocabulary split forced two deprecated
opinions into view; **C0 and C1 had no equivalent forcing function and that lane makes no claim to have
looked.** So **absence of a semantic finding is absence of a forcing function, not absence of a
defect.** (`2.0.0_SA_COO~X` ruling 3 adopted the consequence: a card with no semantic finding does not
outrank one with a finding.)

---

## 3. THE C3 CHAIN — THREE OF FOUR STAGES DO NOT EXIST

**Andrew-direct 1911Z, verbatim:** *"the entire reason we're doing this is to ultimately get to a
position where we can construct C3 via the nerves_resolve->affinity matrix->similarity network fusion
process. We are nowhere even close to doing c3 right now, so any card they do is simply representative
of current state."*

| stage | part | status |
|---|---|---|
| 1 | `nerves_resolve` | **EXISTS.** Reads `.comp-graph/graph.json`, `comp_pydeps.py`, git tracked files, `.tools/`. **WRITES NOTHING** — pure function, in-memory `lru_cache` only. |
| 2 | `affinity_matrix` | **ABSENT.** No code, no store, no artifact. *Would read* the L1 entity set + the four views; *would write* a per-view affinity store — unbuilt, unnamed, unhomed. |
| 3 | `similarity_network_fusion` | **ABSENT.** *Would read* the per-view matrices; *would write* a fused affinity store. |
| 4 | `identity_and_succession` | **ABSENT.** *Would read* fused clusters; *would write* an identity register carrying birth/death/split/merge. |

**All four are registered as PARTS in the manifest.** An absent stage is an **ABSENT ROW**, never an
omission — an empty row is a finding and skipping it loses the baseline. **An omitted row and an absent
row are opposite facts that look identical in a manifest.**

### THE BINDING CONSTRAINT — `1.0.0_SA_CTO~X`'s words, 73215 Q4, answering an Andrew-directed ask

> **"stage one of the C3 chain currently resolves against 2,249 of 27,061 canonical graph nodes (8.3%),
> from an input 19.7 days stale, with NO cadence and NO named owner, and a failure mode where
> SUBSTRATE-ABSENT is byte-identical to GENUINELY-UNADDRESSED."**

> *"The design is sound and it is the only DECLARED cross-space mapping in the estate — but **a spine at
> 8.3% with no owner is a sample, not a spine, and nothing above L1 can be contracted until that
> changes.**"*

**And the mechanism by which it got there is on the manifest's face:** `.comp-graph/graph.json` carries a
declared **5-minute TTL** that governs **rebuild-on-read**. An unread graph simply ages — which is
exactly how a stage-1 substrate reaches 19.7 days stale **without any alarm firing**, because nothing
was ever wrong.

---

## 4. FINDINGS ROUTED — NAMED WITH OWNERS, NONE REMEDIATED (`DTX-AC5`)

| id | subject | finding | owner |
|---|---|---|---|
| **F-1** | `s3://opal-estate-report/kuzu_nessie_db` | **DESIRED ≠ APPLIED.** `instance.tf:136-138` declares it *"published daily … and OVERWRITTEN each day"*; measured LastModified is **2026-08-06**, **20 days** stale. The config's own comment covers a *missing* object (*"MUST READ AS INSTRUMENT_FAILED"*) — **it does not cover a stale one, which is present and answers.** | estate-report pipeline owner (`0.7.0_AE_CloudOps` lane) |
| **F-2** | `infra/aws/globgrph/kuzu_nessie_db.rebuild.tmp.*` | **158MB (165,675,008 B) of orphaned rebuild temporaries** — 3 DBs + 3 WALs from three interrupted rebuilds on 2026-08-25 — **UNTRACKED *and* NOT IGNORED**, so they show as `??` in **every agent's `git status`** on this device. | kuzu rebuild path owner (`0.8.0_AE_CloudComp`, NFRA_KUZUSPLIT) |
| **F-3** | `cse_test_24458e6c` · `cse_test_bb57a916` | **Two TEST tables persisting in the governed production warehouse.** `population_status: test` is the field that makes this expressible — and it exists in the L0 schema *because of this live finding*. | cse producer owner — **UNRESOLVED** |
| **F-4** | `c2_instances.json` (10.3MB) · `c3_structures.json` (2.1MB) | **12MB of untracked, un-gitignored artifacts that the derive INGESTS.** Loss would be **silent and unrecoverable from the repo.** | `3.0.0_SA_CVO` |
| **F-5** | ALL 39 parts | **`declared_opinions` is `null` on 39 of 39** — no part of this substrate declares its opinions — and generator currency is unestablished estate-wide. No instrument discriminates either. | routed to `1.0.0_SA_CTO~X` (Q2/Q3) |
| **F-6** | `graph_contracts` | Iceberg table in the governed warehouse, **71 days stale**, **generator UNKNOWN after a stated search**, **no owner identified.** Corroborated by a second instrument (provenance-header marker, 1703.4h). | **UNOWNED — that is the finding** |

**Instrument findings routed separately** (not D11 subjects, nobody fixes them): `comp-keys prefix`
default truncation (73076 → ruled 73105) and the `comp-find` content-pattern-plus-`--name` trap
(72990 → ruled 73003).

---

## 5. WHAT WOULD MAKE THIS MANIFEST WRONG — instrument disclosures

**Five measurement failures occurred while producing this. Two were caught by a control, three by a
denominator. None reached a published row. All are recorded, because a census that hides its near-misses
is asking to be trusted more than it earned.**

1. **`comp-keys prefix` truncates to 40 by default** and prints its total *after* the rows. It **fails in
   one direction only — it can only hide keys**, producing false absences. **It nearly recorded the 51MB
   `kuzu_nessie_db` as ABSENT**, the very store D11 exists to find. Caught by `head-object`.
2. ⛔ **MY POSITIVE CONTROL FIRED GREEN WHILE THE VERDICT WAS WRONG.** I grepped the same 40 truncated
   rows for `estate-report`, got 38 of 40, and read it as proof the sweep was sound. **It proved my GREP
   worked and said nothing about whether the LISTING was complete** — a control on the **filter** while
   the defect was in the **population**. *Worse than no control, because it looks like rigour and stops
   the asking.*
3. **`comp-find` content-pattern + `--name` scans zero files** and reports `0 hits across 0 scanned`.
   Hit at ~18:15Z; falsifiable only because the store was visible in a directory listing. **What saved
   it was not care — it was the denominator.** A sweep that scanned nothing cannot have found nothing.
4. **Lexicographic ≠ chronological.** `sort | tail -1` on Iceberg metadata filenames reported
   `graph_nodes` at **2026-06-12** against a true **2026-08-26**. Iceberg metadata filenames do not sort
   by time.
5. **`--query sort_by(...)[-1]` applies PER PAGE** on a paginated `list-*`: the 131,975-object
   `graph_nodes` metadata prefix returned ~130 values instead of one. Remedy: materialise the set,
   compute the max client-side.
6. **The first hand-authored cut of this manifest declared 39 against 35 rows** — a typed denominator
   that did not match its own population, **in a deliverable whose entire subject is printed
   denominators.** Caught by the TO's own phase-2 mandate. **Remedy: the manifest is now EMITTED by
   `build_manifest.py`, which computes every count from the population and asserts declared == actual.**

**Coverage, limits and `known_unsearched` live in the manifest's own `denominator` block** — which
`2.0.0_SA_COO~X` correctly named as `DTX-AC6` *expressed as a field a consumer can reject on*, the
better form. **The widest gap is stated there and repeated here because it is the one most likely to
matter: DynamoDB / RDS / any non-S3 persistence was not swept at all.**

---

## 6. SCOPE — WHAT THIS LANE DID NOT DO

**`DTX-AC5` holds.** Zero commits by this lane touch any store or generator the manifest registers. The
158MB temp set, the two production-warehouse test tables, the 20-day-stale published object and the 12MB
untracked ingested artifacts were **named with owners and left exactly where they are.**

⛔ **Andrew's forward intent — one canonical, agnostic materializer per layer `c0 c1 c2 c3 d1 d2 d3` —
is RECORDED AND NOT AUTHORIZED.** His trigger is explicit: *"after reviewing all substrate cards."*
Adopting a manifest schema is **not** authorization to build a materializer, stub a layer, or remediate
any part registered here.

*I flagged `DTX-AC5` at ACK as the constraint I was most likely to breach by reflex, since my base role
is a deploy lane and my instinct on finding a broken generator is to fix it. `2.0.0_SA_COO~X` held me to
that declaration when the scope widened. It held.*

---

## LIMIT OF THE BUILD-TIME MATERIALIZER GUARD (added 2026-08-27, on a landed ruling)

**The guard in `build_manifest.py` verifies the ADDRESS half of a citation. It does NOT verify
the TEXT half.** Disclosed here because a guard that REFUSES loudly reads as stronger than it is,
and 25 of 39 parts carry a `generation.materializer` a consumer may join on.

| half | what it means | guard |
|---|---|---|
| ADDRESS | the path is joinable and resolves on disk | **ENFORCED** — bare filename refused, unresolvable path refused, multi-path with no declared role refused |
| TEXT | the file at that path actually WRITES the part claimed | **NOT ENFORCED** — outside the guard entirely |

**WHY THIS IS THE DANGEROUS HALF.** All four false-lineage defects corrected during wave 1
(`motif _ab`, `kuzu_incremental_refresh`, `_build_manifest`, `cse`) named paths that
**resolved perfectly**. A resolving path is not evidence of a producer; it is evidence of a file.
Each was caught by opening the file, never by the guard — the guard was GREEN on all four.

**WHAT WOULD CLOSE IT, AND WHY IT IS NOT BUILT HERE.** The text half is a per-part semantic
claim (does this file emit this object?), not a mechanical property of the string. It is not
closable by a generic build-time check, and building a per-part verifier is beyond the accepted
TO-W1-DTX scope. Stated as an open limit rather than silently narrowed.

**FOR A CONSUMER:** treat `generation.materializer` as `inferred` unless the part's own card
carries a `basis_by_field` entry raising it. The guard's PASS certifies joinability, never lineage.

### SECOND LIMB: THE FIELD'S POPULATION IS BOUNDED BY DISCOVERABILITY (added 2026-08-27)

The limit above says a NAMED materializer may be the wrong file. This one is different and was
not covered: **a writer may exist that no name-keyed instrument can attribute to any part.**

`generation.materializer` was populated by finding modules that NAME the object. That predicate
answers *"which writers can I FIND"*, and it was reported as *"which writers exist"*. Those are
not the same question, and the gap is occupied:

```
infra/aws/globgrph/resource_summaries_store.py
  :56   NAMESPACE = "globgrph"    # its own comment: "same namespace/catalog as the graph tables + cse"
  :190  table_id = (NAMESPACE, table)      <- table comes from the CLI arg
  :349  add_argument("--table", default=TABLE)   NO choices= constraint
  :202  catalog.create_table(table_id, ...)      creates whatever name it is given

NEGATIVE CONTROL -- snap_store.py is constrained at exactly the same field:
  :415  add_argument("--surface", default="ms_heat_snap", choices=sorted(SURFACES))
```

**The control fires: the two modules differ at the field under test.** So a module exists that can
create or append to ANY table in the exact namespace this manifest cards, and its output set is
NOT enumerable from source.

**TWO QUESTIONS, NOT ONE** (0.8.0_AE_CloudComp~X's partition, sharpened by 2.0.0_SA_COO~X):
where is the table name BOUND (call site / entrypoint allow-list / arbitrary runtime), and is the
bound set ENUMERABLE. This manifest's materializer field answers neither.

⚠ **WHAT THIS IS NOT.** No evidence that any part here is actually mis-attributed by this route;
`resource_summaries_store` defaults to its own table and I did not measure that it has ever
written a graph table. The claim is about the FIELD'S GUARANTEE, not about a known bad row: an
absent materializer means *nobody found a writer*, never *no writer exists*.

**CONSEQUENCE:** the `denominator` block's sweep is sound for OBJECTS -- it enumerates the
warehouse and the directories, not the writers. The materializer FIELD does not inherit that
soundness, and this file previously let the object-level rigour read as though it did.
