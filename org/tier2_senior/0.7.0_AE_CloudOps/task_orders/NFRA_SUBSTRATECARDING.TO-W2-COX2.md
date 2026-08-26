<task_order>
<id>NFRA_SUBSTRATECARDING.TO-W2-COX2</id>
<project>NFRA_SUBSTRATECARDING</project>
<issued_to>0.7.0_AE_CloudOps~X</issued_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<executor_class>0.7.0_AE_CloudOps (~lane instance; SINGLE-PROJECT)</executor_class>
<status>pending</status>
<priority>P1 -- D11 wave 2, Andrew-direct full scope</priority>
<date>2026-08-26</date>
<placement>LAPTOP</placement>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/nfra-substratecarding-w2/20260826T210050Z/DECOMP.md @9e0394fedf</ref>
  <ref type="contract">org/standards/SUBSTRATE_CARD.v2.schema.json -- v2 BINDS, wave 2 is the wave boundary</ref>
  <ref type="law">CLAUDE.md Rule 28</ref>
</references>
<objective>
Produce 5 conformant substrate cards -- C3.i / comp-similar definitions -- validating against
SUBSTRATE_CARD.v2.schema.json. QUALIFY ONLY. NO deprecation verdicts (second pass).
</objective>
</task_order>

# TASK ORDER — NFRA_SUBSTRATECARDING.TO-W2-COX2

**to:** `0.7.0_AE_CloudOps~X` · **issuer:** `2.0.0_SA_COO~X` · **cut:** 2026-08-26 ~21:2xZ

⛔ **UNCERTIFIED DECOMP** — cert pending `3.0.0_SA_CVO~X`. No practical effect on this lane; a
DECOMP-INVALIDATING verdict is the issuer's act to re-decomp and re-issue.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding-w2/20260826T210050Z/DECOMP.md @9e0394fedf
Cells discharged (35, enumerated LITERALLY):
W2-aa-1, W2-aa-2, W2-aa-3, W2-aa-4, W2-aa-5, W2-aa-6, W2-aa-7, W2-as-1, W2-as-2, W2-as-3, W2-as-4,
W2-as-5, W2-as-6, W2-as-7, W2-at-1, W2-at-2, W2-at-3, W2-at-4, W2-at-5, W2-at-6, W2-at-7, W2-au-1,
W2-au-2, W2-au-3, W2-au-4, W2-au-5, W2-au-6, W2-au-7, W2-bi-1, W2-bi-2, W2-bi-3, W2-bi-4, W2-bi-5,
W2-bi-6, W2-bi-7
</decomp_ref>

<proof_of_spec>
  <criterion id="COX2-AC1" cell_refs="W2-aa-1, W2-aa-2, W2-aa-3, W2-aa-4, W2-aa-5, W2-aa-6, W2-aa-7, W2-as-1, W2-as-2, W2-as-3, W2-as-4, W2-as-5, W2-as-6, W2-as-7, W2-at-1, W2-at-2, W2-at-3, W2-at-4, W2-at-5, W2-at-6, W2-at-7, W2-au-1, W2-au-2, W2-au-3, W2-au-4, W2-au-5, W2-au-6, W2-au-7, W2-bi-1, W2-bi-2, W2-bi-3, W2-bi-4, W2-bi-5, W2-bi-6, W2-bi-7"/>
  <criterion id="COX2-AC2" cell_refs="W2-aa-2, W2-as-2, W2-at-2, W2-au-2, W2-bi-2"/>
  <criterion id="COX2-AC3" cell_refs="W2-aa-3, W2-as-3, W2-at-3, W2-au-3, W2-bi-3"/>
  <criterion id="COX2-AC4" cell_refs="W2-aa-4, W2-as-4, W2-at-4, W2-au-4, W2-bi-4"/>
  <criterion id="COX2-AC5" cell_refs="W2-aa-1, W2-aa-2, W2-aa-3, W2-aa-4, W2-aa-5, W2-aa-6, W2-aa-7, W2-as-1, W2-as-2, W2-as-3, W2-as-4, W2-as-5, W2-as-6, W2-as-7, W2-at-1, W2-at-2, W2-at-3, W2-at-4, W2-at-5, W2-at-6, W2-at-7, W2-au-1, W2-au-2, W2-au-3, W2-au-4, W2-au-5, W2-au-6, W2-au-7, W2-bi-1, W2-bi-2, W2-bi-3, W2-bi-4, W2-bi-5, W2-bi-6, W2-bi-7"/>
  <criterion id="COX2-AC6" cell_refs="W2-aa-6, W2-as-6, W2-at-6, W2-au-6, W2-bi-6"/>
  <criterion id="COX2-AC7" cell_refs="W2-aa-7, W2-as-7, W2-at-7, W2-au-7, W2-bi-7"/>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_SUBSTRATECARDING.TO-W2-COX2_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>COX2-AC1,COX2-AC2,COX2-AC3,COX2-AC4,COX2-AC5,COX2-AC6,COX2-AC7</expected_criteria>
  <alignment_denominators>criteria: 7. Cells: 35 of 35 owned by this executor, all covered. Unmapped 0; untraceable 0.</alignment_denominators>
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

## 2. YOUR 5 SUBJECTS

| subject | named by (wave 1) | spellings |
|---|---|---|
| `ANCHOR_CATALOG + HUB_TYPES read at runtime from org/tier2_senior/0.4.0_DS_Clie` | C3.i-as-built | 1 |
| `org/modules/graph/comp_ladder.py` | C3.i-as-built | 1 |
| `org/modules/graph/debtscan/dup_scan.py` | comp-similar | 1 |
| `org/modules/graph/debtscan/summary_corpus.py` | comp-similar | 1 |
| `the two BAKED STATIC SPEC LAYERS folded by ingest_c2c3_motif_producer` | C3.i-as-built | 1 |

⛔ **These reached us as PROSE STRINGS from wave-1 `composes`/`projection_of`.** Where a subject shows
>1 spelling, wave 1 proved **no dedup heuristic can be correct** — resolve identity by reading the
thing, not the string.

## 3. ACCEPTANCE

| id | criterion |
|---|---|
| **COX2-AC1** | 5 cards exist and **all VALIDATE** against v2. Every row carries `basis` + `evidence` + `owner`. |
| **COX2-AC2** | `cadence` worked on every card. |
| **COX2-AC3** | `persistence` worked; `persisted: false` is legitimate **only if MEASURED**. |
| **COX2-AC4** | `location.home` exact, or `null` **with evidence of where you looked and the search denominator**. |
| **COX2-AC5** | ⛔ **`coverage.denominator` NON-NULL**, `"N of M"`; if genuinely uncountable, **`denominator_absent_reason` populated** (v2 makes this rejectable — use it). |
| **COX2-AC6** | `key`: `identity_space`, `key_is_stable`, `crosses_spaces`; `declared_mapping: null` **only after a hunt**. |
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

## 5. KNOWN CONTRACT GAP — `declared_opinions` IS NOT IN THE CARD SCHEMA

It exists only in the L0 manifest contract, and it is the field the canonical-materializer consumer
reads. **Record buried filters/thresholds/exclusions in `methodology.how` prose as the fallback, and
say in `evidence` that it is prose because the contract has no slot.** ⛔ **That is knowingly the F-2
shape; it is routed to `1.0.0_SA_CTO~X` and is NOT this lane's to fix.**

## 6. INSTRUMENT TRAPS — BOTH MEASURED TODAY

- ⛔ `comp-find`: **a content pattern AND `--name` in one call scans ZERO files.** Use one or the other.
  `--files`/`--band` alongside `--name` are fine. **READ THE `scanned` COUNT.**
- ⛔ `comp-keys prefix`: **truncates to 40 by DEFAULT**, total printed AFTER the rows. **Use `--all`.**
  It hides keys only, so it produces **FALSE ABSENCES** — the exact direction a `location` row rests on.

## 7. SURPRISE CHANNEL

One line to `3.0.0_SA_CVO`, cc me. **OBSERVATION never interrupts. BLOCKING routes same-turn to me.**
⛔ **A finding about a subject you are carding is the DELIVERABLE, not a surprise.**

Route to `3.0.0_SA_CVO~X` at the completion flip, cc me.
