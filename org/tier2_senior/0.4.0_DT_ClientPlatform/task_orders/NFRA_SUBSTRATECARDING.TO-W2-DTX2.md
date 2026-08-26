<task_order>
<id>NFRA_SUBSTRATECARDING.TO-W2-DTX2</id>
<project>NFRA_SUBSTRATECARDING</project>
<issued_to>0.4.0_DT_ClientPlatform~X</issued_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<executor_class>0.4.0_DT_ClientPlatform (~lane instance; SINGLE-PROJECT)</executor_class>
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
Produce 15 conformant substrate cards -- the STORES -- validating against
SUBSTRATE_CARD.v2.schema.json. QUALIFY ONLY. NO deprecation verdicts (second pass).
</objective>
</task_order>

# TASK ORDER — NFRA_SUBSTRATECARDING.TO-W2-DTX2

**to:** `0.4.0_DT_ClientPlatform~X` · **issuer:** `2.0.0_SA_COO~X` · **cut:** 2026-08-26 ~21:2xZ

⛔ **UNCERTIFIED DECOMP** — cert pending `3.0.0_SA_CVO~X`. No practical effect on this lane; a
DECOMP-INVALIDATING verdict is the issuer's act to re-decomp and re-issue.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding-w2/20260826T210050Z/DECOMP.md @9e0394fedf
Cells discharged (105, enumerated LITERALLY):
W2-bcin-1, W2-bcin-2, W2-bcin-3, W2-bcin-4, W2-bcin-5, W2-bcin-6, W2-bcin-7, W2-coth-1, W2-coth-2,
W2-coth-3, W2-coth-4, W2-coth-5, W2-coth-6, W2-coth-7, W2-hffm-1, W2-hffm-2, W2-hffm-3, W2-hffm-4,
W2-hffm-5, W2-hffm-6, W2-hffm-7, W2-jgzc-1, W2-jgzc-2, W2-jgzc-3, W2-jgzc-4, W2-jgzc-5, W2-jgzc-6,
W2-jgzc-7, W2-lqzx-1, W2-lqzx-2, W2-lqzx-3, W2-lqzx-4, W2-lqzx-5, W2-lqzx-6, W2-lqzx-7, W2-nthk-1,
W2-nthk-2, W2-nthk-3, W2-nthk-4, W2-nthk-5, W2-nthk-6, W2-nthk-7, W2-pcac-1, W2-pcac-2, W2-pcac-3,
W2-pcac-4, W2-pcac-5, W2-pcac-6, W2-pcac-7, W2-qvzv-1, W2-qvzv-2, W2-qvzv-3, W2-qvzv-4, W2-qvzv-5,
W2-qvzv-6, W2-qvzv-7, W2-rpcx-1, W2-rpcx-2, W2-rpcx-3, W2-rpcx-4, W2-rpcx-5, W2-rpcx-6, W2-rpcx-7,
W2-ugdt-1, W2-ugdt-2, W2-ugdt-3, W2-ugdt-4, W2-ugdt-5, W2-ugdt-6, W2-ugdt-7, W2-vlov-1, W2-vlov-2,
W2-vlov-3, W2-vlov-4, W2-vlov-5, W2-vlov-6, W2-vlov-7, W2-xnwo-1, W2-xnwo-2, W2-xnwo-3, W2-xnwo-4,
W2-xnwo-5, W2-xnwo-6, W2-xnwo-7, W2-xzjx-1, W2-xzjx-2, W2-xzjx-3, W2-xzjx-4, W2-xzjx-5, W2-xzjx-6,
W2-xzjx-7, W2-yjky-1, W2-yjky-2, W2-yjky-3, W2-yjky-4, W2-yjky-5, W2-yjky-6, W2-yjky-7, W2-znom-1,
W2-znom-2, W2-znom-3, W2-znom-4, W2-znom-5, W2-znom-6, W2-znom-7
</decomp_ref>

<proof_of_spec>
  <criterion id="DTX2-AC1" cell_refs="W2-bcin-1, W2-bcin-2, W2-bcin-3, W2-bcin-4, W2-bcin-5, W2-bcin-6, W2-bcin-7, W2-coth-1, W2-coth-2, W2-coth-3, W2-coth-4, W2-coth-5, W2-coth-6, W2-coth-7, W2-hffm-1, W2-hffm-2, W2-hffm-3, W2-hffm-4, W2-hffm-5, W2-hffm-6, W2-hffm-7, W2-jgzc-1, W2-jgzc-2, W2-jgzc-3, W2-jgzc-4, W2-jgzc-5, W2-jgzc-6, W2-jgzc-7, W2-lqzx-1, W2-lqzx-2, W2-lqzx-3, W2-lqzx-4, W2-lqzx-5, W2-lqzx-6, W2-lqzx-7, W2-nthk-1, W2-nthk-2, W2-nthk-3, W2-nthk-4, W2-nthk-5, W2-nthk-6, W2-nthk-7, W2-pcac-1, W2-pcac-2, W2-pcac-3, W2-pcac-4, W2-pcac-5, W2-pcac-6, W2-pcac-7, W2-qvzv-1, W2-qvzv-2, W2-qvzv-3, W2-qvzv-4, W2-qvzv-5, W2-qvzv-6, W2-qvzv-7, W2-rpcx-1, W2-rpcx-2, W2-rpcx-3, W2-rpcx-4, W2-rpcx-5, W2-rpcx-6, W2-rpcx-7, W2-ugdt-1, W2-ugdt-2, W2-ugdt-3, W2-ugdt-4, W2-ugdt-5, W2-ugdt-6, W2-ugdt-7, W2-vlov-1, W2-vlov-2, W2-vlov-3, W2-vlov-4, W2-vlov-5, W2-vlov-6, W2-vlov-7, W2-xnwo-1, W2-xnwo-2, W2-xnwo-3, W2-xnwo-4, W2-xnwo-5, W2-xnwo-6, W2-xnwo-7, W2-xzjx-1, W2-xzjx-2, W2-xzjx-3, W2-xzjx-4, W2-xzjx-5, W2-xzjx-6, W2-xzjx-7, W2-yjky-1, W2-yjky-2, W2-yjky-3, W2-yjky-4, W2-yjky-5, W2-yjky-6, W2-yjky-7, W2-znom-1, W2-znom-2, W2-znom-3, W2-znom-4, W2-znom-5, W2-znom-6, W2-znom-7"/>
  <criterion id="DTX2-AC2" cell_refs="W2-bcin-2, W2-coth-2, W2-hffm-2, W2-jgzc-2, W2-lqzx-2, W2-nthk-2, W2-pcac-2, W2-qvzv-2, W2-rpcx-2, W2-ugdt-2, W2-vlov-2, W2-xnwo-2, W2-xzjx-2, W2-yjky-2, W2-znom-2"/>
  <criterion id="DTX2-AC3" cell_refs="W2-bcin-3, W2-coth-3, W2-hffm-3, W2-jgzc-3, W2-lqzx-3, W2-nthk-3, W2-pcac-3, W2-qvzv-3, W2-rpcx-3, W2-ugdt-3, W2-vlov-3, W2-xnwo-3, W2-xzjx-3, W2-yjky-3, W2-znom-3"/>
  <criterion id="DTX2-AC4" cell_refs="W2-bcin-4, W2-coth-4, W2-hffm-4, W2-jgzc-4, W2-lqzx-4, W2-nthk-4, W2-pcac-4, W2-qvzv-4, W2-rpcx-4, W2-ugdt-4, W2-vlov-4, W2-xnwo-4, W2-xzjx-4, W2-yjky-4, W2-znom-4"/>
  <criterion id="DTX2-AC5" cell_refs="W2-bcin-1, W2-bcin-2, W2-bcin-3, W2-bcin-4, W2-bcin-5, W2-bcin-6, W2-bcin-7, W2-coth-1, W2-coth-2, W2-coth-3, W2-coth-4, W2-coth-5, W2-coth-6, W2-coth-7, W2-hffm-1, W2-hffm-2, W2-hffm-3, W2-hffm-4, W2-hffm-5, W2-hffm-6, W2-hffm-7, W2-jgzc-1, W2-jgzc-2, W2-jgzc-3, W2-jgzc-4, W2-jgzc-5, W2-jgzc-6, W2-jgzc-7, W2-lqzx-1, W2-lqzx-2, W2-lqzx-3, W2-lqzx-4, W2-lqzx-5, W2-lqzx-6, W2-lqzx-7, W2-nthk-1, W2-nthk-2, W2-nthk-3, W2-nthk-4, W2-nthk-5, W2-nthk-6, W2-nthk-7, W2-pcac-1, W2-pcac-2, W2-pcac-3, W2-pcac-4, W2-pcac-5, W2-pcac-6, W2-pcac-7, W2-qvzv-1, W2-qvzv-2, W2-qvzv-3, W2-qvzv-4, W2-qvzv-5, W2-qvzv-6, W2-qvzv-7, W2-rpcx-1, W2-rpcx-2, W2-rpcx-3, W2-rpcx-4, W2-rpcx-5, W2-rpcx-6, W2-rpcx-7, W2-ugdt-1, W2-ugdt-2, W2-ugdt-3, W2-ugdt-4, W2-ugdt-5, W2-ugdt-6, W2-ugdt-7, W2-vlov-1, W2-vlov-2, W2-vlov-3, W2-vlov-4, W2-vlov-5, W2-vlov-6, W2-vlov-7, W2-xnwo-1, W2-xnwo-2, W2-xnwo-3, W2-xnwo-4, W2-xnwo-5, W2-xnwo-6, W2-xnwo-7, W2-xzjx-1, W2-xzjx-2, W2-xzjx-3, W2-xzjx-4, W2-xzjx-5, W2-xzjx-6, W2-xzjx-7, W2-yjky-1, W2-yjky-2, W2-yjky-3, W2-yjky-4, W2-yjky-5, W2-yjky-6, W2-yjky-7, W2-znom-1, W2-znom-2, W2-znom-3, W2-znom-4, W2-znom-5, W2-znom-6, W2-znom-7"/>
  <criterion id="DTX2-AC6" cell_refs="W2-bcin-6, W2-coth-6, W2-hffm-6, W2-jgzc-6, W2-lqzx-6, W2-nthk-6, W2-pcac-6, W2-qvzv-6, W2-rpcx-6, W2-ugdt-6, W2-vlov-6, W2-xnwo-6, W2-xzjx-6, W2-yjky-6, W2-znom-6"/>
  <criterion id="DTX2-AC7" cell_refs="W2-bcin-7, W2-coth-7, W2-hffm-7, W2-jgzc-7, W2-lqzx-7, W2-nthk-7, W2-pcac-7, W2-qvzv-7, W2-rpcx-7, W2-ugdt-7, W2-vlov-7, W2-xnwo-7, W2-xzjx-7, W2-yjky-7, W2-znom-7"/>
  <criterion id="DTX2-AC8" cell_refs="W2-bcin-1, W2-coth-1, W2-hffm-1, W2-jgzc-1, W2-lqzx-1, W2-nthk-1, W2-pcac-1, W2-qvzv-1, W2-rpcx-1, W2-ugdt-1, W2-vlov-1, W2-xnwo-1, W2-xzjx-1, W2-yjky-1, W2-znom-1"/>
  <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/NFRA_SUBSTRATECARDING.TO-W2-DTX2_PROOF_OF_SPEC.json</instance_path>
  
  <expected_criteria>DTX2-AC1,DTX2-AC2,DTX2-AC3,DTX2-AC4,DTX2-AC5,DTX2-AC6,DTX2-AC7,DTX2-AC8</expected_criteria>
  <alignment_denominators>criteria: 8. Cells: 105 of 105 owned by this executor, all covered. Unmapped 0; untraceable 0.</alignment_denominators>
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

## 2. YOUR 15 SUBJECTS

⛔ **AMENDED 22:2xZ — 6 SUBJECT(S) ADDED.** The original derivation read `composes` +
`projection_of` and **NEVER READ `location.co_resident_stores`** — a THIRD card field naming stores.
`0.4.0_DT_ClientPlatform~X` measured it (4 of 4 positive controls firing). **Your existing cell ids are
UNCHANGED** — ids derive from the subject string, so an addition moves nothing. Added here:
- `.comp-graph/graph.json`
- `infra/system/ontology/SYSTEM_DEFINITIONS.yaml`
- `org/modules/graph/nerves-edges.json and nerves-risk-edges.json`
- `org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c2_instances.j`
- `org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c3_structures.`
- `s3://opal-estate-report/kuzu_nessie_db`

| subject | named by (wave 1) | spellings |
|---|---|---|
| `.comp-graph/graph.json` | wave-1 co_resident_stores | 1 |
| `comp-heat` | comp-similar | 1 |
| `data/firm_registry.json` | D3_contract_obligation | 1 |
| `infra/system/ontology/SYSTEM_DEFINITIONS.yaml` | wave-1 co_resident_stores | 1 |
| `kuzu_nessie_db` | D1_value_grain, D2_path_flow, comp-similar | 3 |
| `org/modules/graph/keep-dormant.yaml` | D3_contract_obligation | 2 |
| `org/modules/graph/nerves-edges.json and nerves-risk-edges.json` | wave-1 co_resident_stores | 1 |
| `org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/` | C3.i-as-built | 1 |
| `org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c2_instances` | wave-1 co_resident_stores | 1 |
| `org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c3_structure` | wave-1 co_resident_stores | 1 |
| `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/motif_c2c3_materialize.j` | C2 | 2 |
| `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/motif_c2c3_materialize_a` | C2 | 2 |
| `s3://opal-313476888478-globgrph/warehouse/globgrph/graph_edges_6629328d-a582-4` | C3.i-as-built, comp-similar | 1 |
| `s3://opal-313476888478-globgrph/warehouse/globgrph/graph_nodes_4c6c23bd-fffa-4` | C3.i-as-built, comp-similar | 1 |
| `s3://opal-estate-report/kuzu_nessie_db` | wave-1 co_resident_stores | 1 |

⛔ **These reached us as PROSE STRINGS.** Resolve identity by reading the thing, not the string.

## 3. ACCEPTANCE

| id | criterion |
|---|---|
| **DTX2-AC1** | 9 cards exist and **all VALIDATE** against v2. Every row carries `basis` + `evidence` + `owner`. |
| **DTX2-AC2** | `cadence` worked on every card. |
| **DTX2-AC3** | `persistence` worked; `persisted: false` is legitimate **only if MEASURED**. |
| **DTX2-AC4** | `location.home` exact, or `null` **with evidence of where you looked and the search denominator**. |
| **DTX2-AC5** | ⛔ **`coverage.denominator` NON-NULL**, `"N of M"`; if genuinely uncountable, **`denominator_absent_reason` populated** (v2 makes this rejectable — use it). |
| **DTX2-AC6** | `key`: `identity_space`, `key_is_stable`, `crosses_spaces`; `declared_mapping: null` **only after a hunt**. |
| **DTX2-AC8** | ⛔ **`declared_opinions` POPULATED on every card** — an enumerated array, or `null` WITH the reason in `evidence`. **Omitting the key passes the schema and FAILS this TO** (s.5). |
| **DTX2-AC7** | `failure_mode` **EXERCISED**, never read off a docstring. |

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
