<task_order>
<id>NFRA_SUBSTRATECARDING.TO-W2-CCX2</id>
<project>NFRA_SUBSTRATECARDING</project>
<issued_to>0.8.0_AE_CloudComp~X</issued_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<executor_class>0.8.0_AE_CloudComp (~lane instance; SINGLE-PROJECT)</executor_class>
<status>complete -- CUT SHORT AT THE DELIVERED BOUNDARY on Andrew-direct 00:15Z + 00:4xZ. 6 of 11 subjects DELIVERED and standing; 5 subjects (35 cells) closed SCOPE-SUPERSEDED, NOT abandoned -- the wave was re-aimed at materializers, the work was not found wanting. Nothing delivered is withdrawn, re-litigated or back-dated. ISSUER 2.0.0_SA_COO~X.</status>
<priority>P1 -- D11 wave 2, Andrew-direct full scope</priority>
<date>2026-08-26</date>
<placement>LAPTOP</placement>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/nfra-substratecarding-w2/20260826T210050Z/DECOMP.md @7969fd40ca</ref>
  <ref type="contract">org/standards/SUBSTRATE_CARD.v2.schema.json -- v2 BINDS, wave 2 is the wave boundary</ref>
  <ref type="law">CLAUDE.md Rule 28</ref>
</references>
<objective>
Produce 11 conformant substrate cards -- c-rung definitions -- validating against
SUBSTRATE_CARD.v2.schema.json. QUALIFY ONLY. NO deprecation verdicts (second pass).
</objective>
</task_order>

# TASK ORDER — NFRA_SUBSTRATECARDING.TO-W2-CCX2

**to:** `0.8.0_AE_CloudComp~X` · **issuer:** `2.0.0_SA_COO~X` · **cut:** 2026-08-26 ~21:2xZ

✅ **DECOMP CERTIFIED** — `3.0.0_SA_CVO~X`, ATTEMPT 4 PASS, record `5168510a28` over packet
`7969fd40ca`. Mutant `W2-jlsi-5.card_grain` found on three discriminators and the seal closed
CRYPTOGRAPHICALLY (commitment recomputed from the certifier's own found values, byte-equal, no
reveal round). The DECOMP face is now GENERATED from the rectangle — `build_decomp_face.py
--check` exits 1 on drift — so the id space this TO cites cannot silently diverge again.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding-w2/20260826T210050Z/DECOMP.md @7969fd40ca
Cells discharged (77, enumerated LITERALLY):
W2-fwhj-1, W2-fwhj-2, W2-fwhj-3, W2-fwhj-4, W2-fwhj-5, W2-fwhj-6, W2-fwhj-7, W2-gfwb-1, W2-gfwb-2,
W2-gfwb-3, W2-gfwb-4, W2-gfwb-5, W2-gfwb-6, W2-gfwb-7, W2-hzfk-1, W2-hzfk-2, W2-hzfk-3, W2-hzfk-4,
W2-hzfk-5, W2-hzfk-6, W2-hzfk-7, W2-idsf-1, W2-idsf-2, W2-idsf-3, W2-idsf-4, W2-idsf-5, W2-idsf-6,
W2-idsf-7, W2-kibc-1, W2-kibc-2, W2-kibc-3, W2-kibc-4, W2-kibc-5, W2-kibc-6, W2-kibc-7, W2-nccg-1,
W2-nccg-2, W2-nccg-3, W2-nccg-4, W2-nccg-5, W2-nccg-6, W2-nccg-7, W2-pzkj-1, W2-pzkj-2, W2-pzkj-3,
W2-pzkj-4, W2-pzkj-5, W2-pzkj-6, W2-pzkj-7, W2-rjvs-1, W2-rjvs-2, W2-rjvs-3, W2-rjvs-4, W2-rjvs-5,
W2-rjvs-6, W2-rjvs-7, W2-uyan-1, W2-uyan-2, W2-uyan-3, W2-uyan-4, W2-uyan-5, W2-uyan-6, W2-uyan-7,
W2-wmzh-1, W2-wmzh-2, W2-wmzh-3, W2-wmzh-4, W2-wmzh-5, W2-wmzh-6, W2-wmzh-7, W2-yoyi-1, W2-yoyi-2,
W2-yoyi-3, W2-yoyi-4, W2-yoyi-5, W2-yoyi-6, W2-yoyi-7
</decomp_ref>

<proof_of_spec>
  <criterion id="CCX2-AC1" cell_refs="W2-fwhj-1, W2-fwhj-2, W2-fwhj-3, W2-fwhj-4, W2-fwhj-5, W2-fwhj-6, W2-fwhj-7, W2-gfwb-1, W2-gfwb-2, W2-gfwb-3, W2-gfwb-4, W2-gfwb-5, W2-gfwb-6, W2-gfwb-7, W2-hzfk-1, W2-hzfk-2, W2-hzfk-3, W2-hzfk-4, W2-hzfk-5, W2-hzfk-6, W2-hzfk-7, W2-idsf-1, W2-idsf-2, W2-idsf-3, W2-idsf-4, W2-idsf-5, W2-idsf-6, W2-idsf-7, W2-kibc-1, W2-kibc-2, W2-kibc-3, W2-kibc-4, W2-kibc-5, W2-kibc-6, W2-kibc-7, W2-nccg-1, W2-nccg-2, W2-nccg-3, W2-nccg-4, W2-nccg-5, W2-nccg-6, W2-nccg-7, W2-pzkj-1, W2-pzkj-2, W2-pzkj-3, W2-pzkj-4, W2-pzkj-5, W2-pzkj-6, W2-pzkj-7, W2-rjvs-1, W2-rjvs-2, W2-rjvs-3, W2-rjvs-4, W2-rjvs-5, W2-rjvs-6, W2-rjvs-7, W2-uyan-1, W2-uyan-2, W2-uyan-3, W2-uyan-4, W2-uyan-5, W2-uyan-6, W2-uyan-7, W2-wmzh-1, W2-wmzh-2, W2-wmzh-3, W2-wmzh-4, W2-wmzh-5, W2-wmzh-6, W2-wmzh-7, W2-yoyi-1, W2-yoyi-2, W2-yoyi-3, W2-yoyi-4, W2-yoyi-5, W2-yoyi-6, W2-yoyi-7"/>
  <criterion id="CCX2-AC2" cell_refs="W2-fwhj-2, W2-gfwb-2, W2-hzfk-2, W2-idsf-2, W2-kibc-2, W2-nccg-2, W2-pzkj-2, W2-rjvs-2, W2-uyan-2, W2-wmzh-2, W2-yoyi-2"/>
  <criterion id="CCX2-AC3" cell_refs="W2-fwhj-3, W2-gfwb-3, W2-hzfk-3, W2-idsf-3, W2-kibc-3, W2-nccg-3, W2-pzkj-3, W2-rjvs-3, W2-uyan-3, W2-wmzh-3, W2-yoyi-3"/>
  <criterion id="CCX2-AC4" cell_refs="W2-fwhj-4, W2-gfwb-4, W2-hzfk-4, W2-idsf-4, W2-kibc-4, W2-nccg-4, W2-pzkj-4, W2-rjvs-4, W2-uyan-4, W2-wmzh-4, W2-yoyi-4"/>
  <criterion id="CCX2-AC5" cell_refs="W2-fwhj-1, W2-fwhj-2, W2-fwhj-3, W2-fwhj-4, W2-fwhj-5, W2-fwhj-6, W2-fwhj-7, W2-gfwb-1, W2-gfwb-2, W2-gfwb-3, W2-gfwb-4, W2-gfwb-5, W2-gfwb-6, W2-gfwb-7, W2-hzfk-1, W2-hzfk-2, W2-hzfk-3, W2-hzfk-4, W2-hzfk-5, W2-hzfk-6, W2-hzfk-7, W2-idsf-1, W2-idsf-2, W2-idsf-3, W2-idsf-4, W2-idsf-5, W2-idsf-6, W2-idsf-7, W2-kibc-1, W2-kibc-2, W2-kibc-3, W2-kibc-4, W2-kibc-5, W2-kibc-6, W2-kibc-7, W2-nccg-1, W2-nccg-2, W2-nccg-3, W2-nccg-4, W2-nccg-5, W2-nccg-6, W2-nccg-7, W2-pzkj-1, W2-pzkj-2, W2-pzkj-3, W2-pzkj-4, W2-pzkj-5, W2-pzkj-6, W2-pzkj-7, W2-rjvs-1, W2-rjvs-2, W2-rjvs-3, W2-rjvs-4, W2-rjvs-5, W2-rjvs-6, W2-rjvs-7, W2-uyan-1, W2-uyan-2, W2-uyan-3, W2-uyan-4, W2-uyan-5, W2-uyan-6, W2-uyan-7, W2-wmzh-1, W2-wmzh-2, W2-wmzh-3, W2-wmzh-4, W2-wmzh-5, W2-wmzh-6, W2-wmzh-7, W2-yoyi-1, W2-yoyi-2, W2-yoyi-3, W2-yoyi-4, W2-yoyi-5, W2-yoyi-6, W2-yoyi-7"/>
  <criterion id="CCX2-AC6" cell_refs="W2-fwhj-6, W2-gfwb-6, W2-hzfk-6, W2-idsf-6, W2-kibc-6, W2-nccg-6, W2-pzkj-6, W2-rjvs-6, W2-uyan-6, W2-wmzh-6, W2-yoyi-6"/>
  <criterion id="CCX2-AC7" cell_refs="W2-fwhj-7, W2-gfwb-7, W2-hzfk-7, W2-idsf-7, W2-kibc-7, W2-nccg-7, W2-pzkj-7, W2-rjvs-7, W2-uyan-7, W2-wmzh-7, W2-yoyi-7"/>
  <criterion id="CCX2-AC8" cell_refs="W2-fwhj-1, W2-gfwb-1, W2-hzfk-1, W2-idsf-1, W2-kibc-1, W2-nccg-1, W2-pzkj-1, W2-rjvs-1, W2-uyan-1, W2-wmzh-1, W2-yoyi-1"/>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_SUBSTRATECARDING.TO-W2-CCX2_PROOF_OF_SPEC.json</instance_path>
  
  <expected_criteria>CCX2-AC1,CCX2-AC2,CCX2-AC3,CCX2-AC4,CCX2-AC5,CCX2-AC6,CCX2-AC7,CCX2-AC8</expected_criteria>
  <alignment_denominators>criteria: 8. Cells: 77 of 77 owned by this executor, all covered. Unmapped 0; untraceable 0.</alignment_denominators>
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

## 2. YOUR 11 SUBJECTS  — ⛔ **SUBJECT SET IS FROZEN as of 22:5xZ**

**FROZEN ON A MEASUREMENT, not an assertion:** `head_resolution_map.json` accounts for **55 of 55** raw heads
from the three wave-1 store fields. **Reopening requires a BLOCKING surprise naming a head that map does not
account for** — a measurement anyone can run, not a suspicion.

| subject | provenance |
|---|---|
| `NFRA_ONTOLOGY_RULE_BANK.yaml#c1_frontend_adapter` | head_43 |
| `NFRA_ONTOLOGY_RULE_BANK.yaml#node_bindings` | head_43 |
| `NFRA_ONTOLOGY_RULE_BANK.yaml#non_relation_edges` | head_43 |
| `NFRA_ONTOLOGY_RULE_BANK.yaml#relation_composites` | head_43 |
| `NFRA_ONTOLOGY_RULE_BANK.yaml#relations` | head_43 |
| `NFRA_ONTOLOGY_RULE_BANK.yaml#roles` | head_43 |
| `live AWS estate` | head_43 |
| `org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c2_individ` | head_43 |
| `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/MOTIF_c2c3_materialize` | head_43 |
| `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_ONTOLOGY_RULE_BANK.yam` | co_resident_addition |
| `repo source tree` | head_43 |

⛔ **These reached us as PROSE STRINGS.** Resolve identity by reading the thing, not the string.

## 3. ACCEPTANCE

| id | criterion |
|---|---|
| **CCX2-AC1** | 11 cards exist and **all VALIDATE** against v2. Every row carries `basis` + `evidence` + `owner`. *(count corrected 10 -> 11 from the CERTIFIED rectangle @5168510a28; the TO was cut before the subject set's final amendments and only this PROSE lagged. The machine-readable `cell_refs` were verified complete against the rectangle BEFORE this edit, so no obligation changed -- this is the count catching up to the spec, not a spec change.)* |
| **CCX2-AC2** | `cadence` worked on every card. |
| **CCX2-AC3** | `persistence` worked; `persisted: false` is legitimate **only if MEASURED**. |
| **CCX2-AC4** | `location.home` exact, or `null` **with evidence of where you looked and the search denominator**. |
| **CCX2-AC5** | ⛔ **`coverage.denominator` NON-NULL**, `"N of M"`; if genuinely uncountable, **`denominator_absent_reason` populated** (v2 makes this rejectable — use it). |
| **CCX2-AC6** | `key`: `identity_space`, `key_is_stable`, `crosses_spaces`; `declared_mapping: null` **only after a hunt**. |
| **CCX2-AC8** | ⛔ **`declared_opinions` POPULATED on every card** — an enumerated array, or `null` WITH the reason in `evidence`. **Omitting the key passes the schema and FAILS this TO** (s.5). |
| **CCX2-AC7** | `failure_mode` **EXERCISED**, never read off a docstring. |

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

---

## ⛔ SCOPE CUT — Andrew-direct 2026-08-27 00:15Z + 00:4xZ

**VERBATIM, the operative words (typos his, preserved — the phrasing is the ruling):**

> *"the whole pioint of this is not to hit random phrases and concepts, it was to hit the actual
> things that are resolvable crucial dependencies for materializers and ontological functions"*", 
> *"i think we need to go surgical mode here, pivot, we need to find the materializers that actualy matter"*

**DELIVERED AND STANDING — 6 of 11 subjects.** Verified or verifiable against the
CERTIFIED decomp `@5168510a28`. **A scope re-aim does not reach backwards.**

**SCOPE-SUPERSEDED — 5 subjects / 35 cells.** ⛔ **NOT abandoned.** The two read
identically from a status field and take OPPOSITE wave-3 actions: superseded work is answered by
the re-aimed wave; abandoned work gets re-attempted as-is.

- `live AWS estate`
- `org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c2_individuate.py`
- `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/MOTIF_c2c3_materialize_spec.py`
- `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_ONTOLOGY_RULE_BANK.yaml`
- `repo source tree`

**WHY THESE AND NOT THE OTHERS:** the wave-2 subject set was derived by harvesting `composes` /
`projection_of` / `co_resident_stores` out of wave-1 card fields. Those fields hold artifact
references AND prose descriptions — **one field, two grains, Rule 24(ii) violated at the SOURCE** —
so the harvest faithfully returned a mixed-grain population. **The method was executed correctly and
the population was wrong, and the population is the issuer's.** Measured: 10 of 44 subjects resolve
to no openable artifact (`resolvability_assessment.json` @`322c41bbb4`).

**PROOF-OF-SPEC INSTANCE: NONE OWED — issuer ruling 2026-08-27 ~01:1xZ.** The TO's 7 criteria span
this lane's full declared cell set, part of which is now SCOPE-SUPERSEDED. An instance over the
ORIGINAL set would assert criteria over cells that no longer exist (a false claim); a RE-SCOPED
instance would be a different instrument wearing the specified instrument's name, so a later reader
comparing this lane's "passed proof-of-spec" against another's would be comparing two different
tests. **The absent instance is a PROPERTY OF THE CUT, not a gap.** This lane is DELIVERED-UNVERIFIED
at TO level and CARD-CONFORMANT at card level (`3.0.0_SA_CVO~X` card-level battery: v2 schema 0
errors, as_of uniform on the wave-2 anchor, all rows carry basis+evidence+owner, forward_disposition
absent). An honest absence beats a green from a substituted instrument.
