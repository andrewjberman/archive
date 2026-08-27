<task_order>
<id>NFRA_SUBSTRATECARDING.TO-W2-COX2</id>
<project>NFRA_SUBSTRATECARDING</project>
<issued_to>0.7.0_AE_CloudOps~X</issued_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<executor_class>0.7.0_AE_CloudOps (~lane instance; SINGLE-PROJECT)</executor_class>
<status>complete -- 7 subjects / 49 cells, 7/7 cards VALID against v2, landed @03b900a109. All 8 criteria PASS with denominators printed per criterion. VERIFIED PASS by 3.0.0_SA_CVO~X @a7650cb78a against the CERTIFIED decomp @5168510a28 (alignment 8/8 + 49/49 + 49/49; floor census 25 measured / 19 inferred / 4 absent / 1 held matching the lane's own disclosure exactly). Verdicts 5 QUALIFIED + 2 UNSOUND. decomp_ref repinned to the certified vintage @c8b192d364, lane-verified before applying. ACCEPTED by issuer 2.0.0_SA_COO~X 74054.</status>
<priority>P1 -- D11 wave 2, Andrew-direct full scope</priority>
<date>2026-08-26</date>
<placement>LAPTOP</placement>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/nfra-substratecarding-w2/20260826T210050Z/DECOMP.md @7969fd40ca</ref>
  <ref type="contract">org/standards/SUBSTRATE_CARD.v2.schema.json -- v2 BINDS, wave 2 is the wave boundary</ref>
  <ref type="law">CLAUDE.md Rule 28</ref>
</references>
<objective>
Produce 7 conformant substrate cards -- C3.i / comp-similar definitions -- validating against
SUBSTRATE_CARD.v2.schema.json. QUALIFY ONLY. NO deprecation verdicts (second pass).
</objective>
</task_order>

# TASK ORDER — NFRA_SUBSTRATECARDING.TO-W2-COX2

**to:** `0.7.0_AE_CloudOps~X` · **issuer:** `2.0.0_SA_COO~X` · **cut:** 2026-08-26 ~21:2xZ

✅ **DECOMP CERTIFIED** — `3.0.0_SA_CVO~X`, ATTEMPT 4 PASS, record `5168510a28` over packet
`7969fd40ca`. Mutant `W2-jlsi-5.card_grain` found on three discriminators and the seal closed
CRYPTOGRAPHICALLY (commitment recomputed from the certifier's own found values, byte-equal, no
reveal round). The DECOMP face is now GENERATED from the rectangle — `build_decomp_face.py
--check` exits 1 on drift — so the id space this TO cites cannot silently diverge again.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding-w2/20260826T210050Z/DECOMP.md @7969fd40ca
Cells discharged (49, enumerated LITERALLY):
W2-cadn-1, W2-cadn-2, W2-cadn-3, W2-cadn-4, W2-cadn-5, W2-cadn-6, W2-cadn-7, W2-dmjw-1, W2-dmjw-2,
W2-dmjw-3, W2-dmjw-4, W2-dmjw-5, W2-dmjw-6, W2-dmjw-7, W2-dxyo-1, W2-dxyo-2, W2-dxyo-3, W2-dxyo-4,
W2-dxyo-5, W2-dxyo-6, W2-dxyo-7, W2-mrns-1, W2-mrns-2, W2-mrns-3, W2-mrns-4, W2-mrns-5, W2-mrns-6,
W2-mrns-7, W2-snuw-1, W2-snuw-2, W2-snuw-3, W2-snuw-4, W2-snuw-5, W2-snuw-6, W2-snuw-7, W2-svdr-1,
W2-svdr-2, W2-svdr-3, W2-svdr-4, W2-svdr-5, W2-svdr-6, W2-svdr-7, W2-widb-1, W2-widb-2, W2-widb-3,
W2-widb-4, W2-widb-5, W2-widb-6, W2-widb-7
</decomp_ref>

<proof_of_spec>
  <criterion id="COX2-AC1" cell_refs="W2-cadn-1, W2-cadn-2, W2-cadn-3, W2-cadn-4, W2-cadn-5, W2-cadn-6, W2-cadn-7, W2-dmjw-1, W2-dmjw-2, W2-dmjw-3, W2-dmjw-4, W2-dmjw-5, W2-dmjw-6, W2-dmjw-7, W2-dxyo-1, W2-dxyo-2, W2-dxyo-3, W2-dxyo-4, W2-dxyo-5, W2-dxyo-6, W2-dxyo-7, W2-mrns-1, W2-mrns-2, W2-mrns-3, W2-mrns-4, W2-mrns-5, W2-mrns-6, W2-mrns-7, W2-snuw-1, W2-snuw-2, W2-snuw-3, W2-snuw-4, W2-snuw-5, W2-snuw-6, W2-snuw-7, W2-svdr-1, W2-svdr-2, W2-svdr-3, W2-svdr-4, W2-svdr-5, W2-svdr-6, W2-svdr-7, W2-widb-1, W2-widb-2, W2-widb-3, W2-widb-4, W2-widb-5, W2-widb-6, W2-widb-7"/>
  <criterion id="COX2-AC2" cell_refs="W2-cadn-2, W2-dmjw-2, W2-dxyo-2, W2-mrns-2, W2-snuw-2, W2-svdr-2, W2-widb-2"/>
  <criterion id="COX2-AC3" cell_refs="W2-cadn-3, W2-dmjw-3, W2-dxyo-3, W2-mrns-3, W2-snuw-3, W2-svdr-3, W2-widb-3"/>
  <criterion id="COX2-AC4" cell_refs="W2-cadn-4, W2-dmjw-4, W2-dxyo-4, W2-mrns-4, W2-snuw-4, W2-svdr-4, W2-widb-4"/>
  <criterion id="COX2-AC5" cell_refs="W2-cadn-1, W2-cadn-2, W2-cadn-3, W2-cadn-4, W2-cadn-5, W2-cadn-6, W2-cadn-7, W2-dmjw-1, W2-dmjw-2, W2-dmjw-3, W2-dmjw-4, W2-dmjw-5, W2-dmjw-6, W2-dmjw-7, W2-dxyo-1, W2-dxyo-2, W2-dxyo-3, W2-dxyo-4, W2-dxyo-5, W2-dxyo-6, W2-dxyo-7, W2-mrns-1, W2-mrns-2, W2-mrns-3, W2-mrns-4, W2-mrns-5, W2-mrns-6, W2-mrns-7, W2-snuw-1, W2-snuw-2, W2-snuw-3, W2-snuw-4, W2-snuw-5, W2-snuw-6, W2-snuw-7, W2-svdr-1, W2-svdr-2, W2-svdr-3, W2-svdr-4, W2-svdr-5, W2-svdr-6, W2-svdr-7, W2-widb-1, W2-widb-2, W2-widb-3, W2-widb-4, W2-widb-5, W2-widb-6, W2-widb-7"/>
  <criterion id="COX2-AC6" cell_refs="W2-cadn-6, W2-dmjw-6, W2-dxyo-6, W2-mrns-6, W2-snuw-6, W2-svdr-6, W2-widb-6"/>
  <criterion id="COX2-AC7" cell_refs="W2-cadn-7, W2-dmjw-7, W2-dxyo-7, W2-mrns-7, W2-snuw-7, W2-svdr-7, W2-widb-7"/>
  <criterion id="COX2-AC8" cell_refs="W2-cadn-1, W2-dmjw-1, W2-dxyo-1, W2-mrns-1, W2-snuw-1, W2-svdr-1, W2-widb-1"/>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_SUBSTRATECARDING.TO-W2-COX2_PROOF_OF_SPEC.json</instance_path>
  
  <expected_criteria>COX2-AC1,COX2-AC2,COX2-AC3,COX2-AC4,COX2-AC5,COX2-AC6,COX2-AC7,COX2-AC8</expected_criteria>
  <alignment_denominators>criteria: 8. Cells: 49 of 49 owned by this executor, all covered. Unmapped 0; untraceable 0.</alignment_denominators>
</proof_of_spec>

---

**ROW LEGEND:** `-1` methodology · `-2` cadence · `-3` persistence · `-4` location · `-5` coverage · `-6` key · `-7` failure_mode

## 1. THE WAVE-2 STAMP — COPY IT, AND IT IS **NOT** WAVE 1's

```json
"as_of": { "carded_utc": "<YOUR clock read>", "commit_ish": "100e7ea130", "graph_vintage": "kuzu_nessie_db@2902399899597701830" }
```
⛔ **`100e7ea130` is the WAVE-2 anchor. Wave 1's `fe269171f2` on a wave-2 card is a WAVE defect.**
⛔ Every `evidence` string carries **its own** commit. Never back-date to the anchor.
⚠ `graph_vintage` is unchanged from wave 1 because the projection **has not rebuilt** (built 14:07:59Z,
re-read 21:19Z, identical). **A measured fact, not a copied value.**

## 2. YOUR 7 SUBJECTS  — ⛔ **SUBJECT SET IS FROZEN as of 22:5xZ**

**FROZEN ON A MEASUREMENT, not an assertion:** `head_resolution_map.json` accounts for **55 of 55** raw heads
from the three wave-1 store fields. **Reopening requires a BLOCKING surprise naming a head that map does not
account for** — a measurement anyone can run, not a suspicion.

| subject | provenance |
|---|---|
| `.tools/comp-debris` | dropped_recovery |
| `ANCHOR_CATALOG + HUB_TYPES read at runtime from org/tier2_senior/0.4.0_DS_Cl` | head_43 |
| `org/modules/graph/comp_ladder.py` | head_43 |
| `org/modules/graph/debtscan/dup_scan.py` | head_43 |
| `org/modules/graph/debtscan/summary_corpus.py` | head_43 |
| `s3://opal-313476888478-globgrph/warehouse/globgrph/resource_summaries_b38ddc` | co_resident_addition |
| `the two BAKED STATIC SPEC LAYERS folded by ingest_c2c3_motif_producer` | head_43 |

⛔ **These reached us as PROSE STRINGS.** Resolve identity by reading the thing, not the string.

## 3. ACCEPTANCE

| id | criterion |
|---|---|
| **COX2-AC1** | 7 cards exist and **all VALIDATE** against v2. Every row carries `basis` + `evidence` + `owner`. *(count corrected 5 -> 7 from the CERTIFIED rectangle @5168510a28; the TO was cut before the subject set's final amendments and only this PROSE lagged. The machine-readable `cell_refs` were verified complete against the rectangle BEFORE this edit, so no obligation changed -- this is the count catching up to the spec, not a spec change.)* |
| **COX2-AC2** | `cadence` worked on every card. |
| **COX2-AC3** | `persistence` worked; `persisted: false` is legitimate **only if MEASURED**. |
| **COX2-AC4** | `location.home` exact, or `null` **with evidence of where you looked and the search denominator**. |
| **COX2-AC5** | ⛔ **`coverage.denominator` NON-NULL**, `"N of M"`; if genuinely uncountable, **`denominator_absent_reason` populated** (v2 makes this rejectable — use it). |
| **COX2-AC6** | `key`: `identity_space`, `key_is_stable`, `crosses_spaces`; `declared_mapping: null` **only after a hunt**. |
| **COX2-AC8** | ⛔ **`declared_opinions` POPULATED on every card** — an enumerated array, or `null` WITH the reason in `evidence`. **Omitting the key passes the schema and FAILS this TO** (s.5). |
| **COX2-AC7** | `failure_mode` **EXERCISED**, never read off a docstring. |

⛔ **AND BINDING ON EVERY ROW: `basis_by_field` IS POPULATED WHEREVER A ROW'S PROVENANCE IS MIXED.**
Wave 1 measured **23 of 56 rows (41%)** claiming `basis: measured` while holding a sub-claim the lane
never exercised — the split surviving only as prose. **v2 added `basis_by_field` because of that
measurement. This wave is the corpus that tests whether the fix is livable.**

## 4. ⛔ NO DEPRECATION VERDICTS. NONE.

Andrew-direct: the deprecation tag is a **SECOND PASS, AFTER carding**. **Zero cards carry a
deprecation verdict at first delivery.** A lane that decides a subject is doomed while carding it
**cards it differently** — less searching on a store it expects thrown away. **The tag must not leak
backwards into the measurement it derives from.** If a subject looks obviously dead, **card it fully
and say nothing about its fate.**

## 5. ⛔ CONTRACT GAP **CLOSED MID-WAVE** — `declared_opinions` NOW EXISTS. POPULATE IT.

**SUPERSEDES the "record it in prose" instruction this TO shipped with.** `1.0.0_SA_CTO~X` landed it
@`9660f526d8` at `process.methodology.declared_opinions` — an array of **every filter, threshold,
exclusion, cutoff and definitional choice this subject's producer makes, ENUMERATED.**

⛔ **`null` IS A LEGAL AND LOUD VALUE MEANING "THE OPINIONS ARE BURIED AND THIS SUBJECT IS UNREVIEWABLE
ON THE SEMANTIC AXIS." That is itself the finding — it is not a blank.**

⚠ **AND IT IS OPTIONAL IN THE SCHEMA, BY DESIGN — I EXERCISED IT: a card omitting the field entirely
VALIDATES** (positive control fired: a card missing `trust` was REJECTED, so that pass is real).
`1.0.0_SA_CTO~X` made it optional deliberately **because this wave was already dispatched against a
contract without it**, and making it required mid-round would retroactively invalidate lanes already
working. **That is the correct call and it means THE TO CARRIES THE BINDING, NOT THE VALIDATOR:**

> ⛔ **THIS TO REQUIRES `declared_opinions` ON EVERY CARD — an enumerated array, or `null` WITH the
> reason stated in `evidence`. A card that omits the key passes the schema and FAILS this TO.**

**Why it is worth a mid-wave amendment:** it is the ONLY remedy for the semantic axis — *"the defect is
not 'wrong opinion', it is 'opinion that cannot be found'"* — and **it is the single field the
canonical-materializer consumer reads.** A visible `ANCHOR_CATALOG = {...}` is reviewable even when its
content is wrong; a filter buried in a loop is not, **and no freshness instrument we hold can see it.**

⚠ **`materializer_standing` is now REQUIRED in `methodology`** (`canonical | historical_in_use |
superseded | unknown`). ⛔ **`historical_in_use` is the most dangerous standing in the schema — it
WORKS, therefore nothing surfaces it.** `unknown` is honest; do not upgrade it because something ran
recently.


## 6. INSTRUMENT TRAPS — BOTH MEASURED TODAY

- ⛔ `comp-find`: **a content pattern AND `--name` in one call scans ZERO files.** Use one or the other.
  `--files`/`--band` alongside `--name` are fine. **READ THE `scanned` COUNT.**
- ⛔ `comp-keys prefix`: **truncates to 40 by DEFAULT**, total printed AFTER the rows. **Use `--all`.**
  It hides keys only, so it produces **FALSE ABSENCES** — the exact direction a `location` row rests on.

## 7. SURPRISE CHANNEL

One line to `3.0.0_SA_CVO`, cc me. **OBSERVATION never interrupts. BLOCKING routes same-turn to me.**
⛔ **A finding about a subject you are carding is the DELIVERABLE, not a surprise.**

Route to `3.0.0_SA_CVO~X` at the completion flip, cc me.
