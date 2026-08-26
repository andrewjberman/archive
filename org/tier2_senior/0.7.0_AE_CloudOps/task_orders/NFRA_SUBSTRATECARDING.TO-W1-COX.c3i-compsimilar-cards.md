<task_order>
<id>NFRA_SUBSTRATECARDING.TO-W1-COX.c3i-compsimilar-cards</id>
<project>NFRA_SUBSTRATECARDING</project>
<issued_to>0.7.0_AE_CloudOps~X</issued_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<executor_class>0.7.0_AE_CloudOps (~lane instance; SINGLE-PROJECT -- this instance holds NFRA_SUBSTRATECARDING and nothing else)</executor_class>
<status>complete -- 14/14 cells, C3.i UNSOUND / comp-similar QUALIFIED, both cards landed @35c9a9b7ed. VERIFIED PASS by 3.0.0_SA_CVO~X @c97a0f30cc (COX-AC4 scored NEGATIVELY SATISFIED -- the wave's only actual reproducibility measurement, both control arms read at the verifier's seat). ACCEPTED by issuer 2.0.0_SA_COO~X 73325.</status>
<priority>P1 -- D11 wave 1. comp-similar is Andrew's named priority and the subject with the most unknowns.</priority>
<date>2026-08-26</date>
<placement>LAPTOP (declared decomp axis; no cross-fabric edge, no ferry semantics)</placement>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/nfra-substratecarding/20260826T172918Z/DECOMP.md @aae317509b</ref>
  <ref type="prd">docs/architecture/D11_SUBSTRATE_ANALYSIS_PRD.md @944ca89492</ref>
  <ref type="contract">org/standards/SUBSTRATE_CARD.schema.json @944ca89492</ref>
  <ref type="law">CLAUDE.md Rule 28 -- THE SUBSTRATE TEST @ec35b78c1c</ref>
  <ref type="acceptance">1.0.0_SA_CTO~X msg 72797 -- the eight PASSES and the four correct REWORKs</ref>
</references>
<objective>
Produce TWO conformant substrate cards -- C3.i AS-BUILT (the anchor-catalog baseline
the replacement must beat) and the substrate underlying comp-similar -- validating
against SUBSTRATE_CARD.schema.json, every row carrying basis + evidence + owner.
QUALIFY ONLY: name defects and their owners; remediate nothing.
</objective>
</task_order>

# TASK ORDER — NFRA_SUBSTRATECARDING.TO-W1-COX · C3.i-AS-BUILT / `comp-similar` CARDS

**to:** `0.7.0_AE_CloudOps~X` · **issuer:** `2.0.0_SA_COO~X` · **cut:** 2026-08-26 ~18:1xZ

✅ **DECOMP CERTIFIED — PASS.** `3.0.0_SA_CVO~X`, `workflows/atom_decomposition/runs/nfra-substratecarding/20260826T172918Z/CERT_20260826T1836Z_3.0.0_SA_CVO~X_ATTEMPT1.md` @`5b390a5662`. Sealed mutant FOUND (`SC-f-4.executor_class`) with three independent discriminators; seal opened and matched on all four fields. ⚠ **A cert is a FLOOR, not a laundering** — the decomp still carries `SC-m-1` PARTIAL (the reduced freeze) and two P2 findings on its face. Nothing in this TO changes.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding/20260826T172918Z/DECOMP.md @aae317509b
Cells discharged (14 CARD_MATRIX, enumerated LITERALLY -- a range is invisible to the estate harvest):
SC-d-1, SC-d-2, SC-d-3, SC-d-4, SC-d-5, SC-d-6, SC-d-7,
SC-h-1, SC-h-2, SC-h-3, SC-h-4, SC-h-5, SC-h-6, SC-h-7
Contributed-to (PROJECT_MECHANISM, not solely owned by this TO): SC-m-2, SC-m-5
</decomp_ref>

<proof_of_spec>
  <!-- python .tools/proof-of-spec-check.py <instance>.json COX-AC1,COX-AC2,COX-AC3,COX-AC4,COX-AC5,COX-AC6,COX-AC7 ; check rc -->
  <criterion id="COX-AC1" cell_refs="SC-d-1, SC-d-2, SC-d-3, SC-d-4, SC-d-5, SC-d-6, SC-d-7, SC-h-1, SC-h-2, SC-h-3, SC-h-4, SC-h-5, SC-h-6, SC-h-7"/>
  <criterion id="COX-AC2" cell_refs="SC-m-2"/>
  <criterion id="COX-AC3" cell_refs="SC-d-5, SC-h-5"/>
  <criterion id="COX-AC4" cell_refs="SC-h-1, SC-d-1"/>
  <criterion id="COX-AC5" cell_refs="SC-d-1, SC-d-2, SC-d-3, SC-d-4, SC-d-5, SC-d-6, SC-d-7, SC-h-1, SC-h-2, SC-h-3, SC-h-4, SC-h-5, SC-h-6, SC-h-7"/>
  <criterion id="COX-AC6" cell_refs="SC-m-5"/>
  <criterion id="COX-AC7" cell_refs="SC-d-6, SC-h-6"/>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_SUBSTRATECARDING.TO-W1-COX_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>COX-AC1,COX-AC2,COX-AC3,COX-AC4,COX-AC5,COX-AC6,COX-AC7</expected_criteria>
  <alignment_denominators>
criteria: 7. Cells discharged: 14 of 14 CARD_MATRIX cells for C3i + comp-similar, plus 2 shared
PROJECT_MECHANISM cells (SC-m-2, SC-m-5) contributed to, not solely owned.
CELL -> CRITERION: all 14 covered (AC1 and AC5 span them; AC3/AC4/AC7 add row-specific bars). Unmapped: 0.
CRITERION -> CELL: all 7 carry >=1 cell_ref. Untraceable: 0.
  </alignment_denominators>
</proof_of_spec>

---

**ROW LEGEND — your cell numbers, in the schema's own required order:**
`-1` methodology · `-2` cadence · `-3` persistence · `-4` location · `-5` coverage · `-6` key · `-7` failure_mode
**SURFACES:** `d` = C3.i-as-built · `h` = whatever underlies `comp-similar`

## 1. THE WAVE STAMP — COPY IT EXACTLY, DO NOT DERIVE IT

```json
"as_of": {
  "carded_utc":    "<YOUR OWN clock read at carding -- date -u, never estimated between turns>",
  "commit_ish":    "fe269171f2",
  "graph_vintage": "kuzu_nessie_db@2902399899597701830"
}
```

⛔ **`commit_ish` IS THE WAVE ANCHOR, NOT YOUR EVIDENCE VINTAGE.** **Every `evidence` string carries ITS OWN
commit.** Never back-date a citation to the anchor — a false vintage is worse than a missing one, because a
missing marker makes a reader ask and a false one makes them stop asking.

⛔ **`graph_vintage` NAMES THE PROJECTION PLANE** (`kuzu_nessie_db`, 27,035 nodes / 58,224 edges), **NOT THE
WAREHOUSE** (which `1.0.0_SA_CTO~X` measured at 27,061 / 60,858). Two planes, two vintages, **neither wrong**.
Say the plane in `evidence`; do not reconcile them and do not re-pin `as_of`.

## 2. SUBJECT `d` — C3.i AS-BUILT

**Carded as the BASELINE the replacement must beat.** Andrew's end goal is *"a mechanical process around the
materialization and tracking of c3.i"* — this card is the *before* picture that process has to improve on.

**Given by `1.0.0_SA_CTO~X` (basis `held` — a peer's published invocation at a DIFFERENT vintage; cite with
attribution or re-derive with a DIFFERENT instrument, but do NOT copy and stamp `measured`):**

| | |
|---|---|
| id spaces | **THREE, with no declared mapping**: `sys-<business-name>` (14) · `system:<domain>:<hash>` (4) · composer domain-keyed (1,257) |
| generation | **SEVEN hand-listed AWS node types** (`ANCHOR_CATALOG`) |
| identity | `sha1(anchor_node_id)` → **`key_is_stable: unstable`** |
| sides | **BACKEND-only.** FRONTEND/KNOWLEDGE structurally zero — 28 cross-side edges estate-wide, all converging on one dead-end node |

⛔ **C3.i IS EXPECTED TO CARD `UNSOUND`, AND THAT IS THE CARD WORKING** (`1.0.0_SA_CTO~X` 72797 case 2).
An unstable key, ~11% coverage and three unmapped id spaces are exactly what a baseline card should surface.
**Do not soften the verdict to look constructive.** A SOUND card about an UNSOUND subject is two different
objects and the schema keeps them apart on purpose.

⛔ **`SC-d-6` (key) IS THE HIGHEST-VALUE CELL ON THIS SUBJECT.** Three id spaces with nothing declaring the
mapping is the estate's most repeated defect — six instances measured in one day. Set `crosses_spaces`
honestly and put the absence of a mapping in `declared_mapping: null` **with evidence of where you looked
for one.**

⛔ **The KNOWLEDGE-side zero is structural, NOT a coverage gap you should hunt.** Already measured.
Reproducing it is not a finding; misreporting it as an incomplete sweep would be.

## 3. SUBJECT `h` — WHATEVER UNDERLIES `comp-similar` · **ANDREW'S PRIORITY**

**The subject with the most unknowns, and the one that most needs the TRUST grain.**

| | |
|---|---|
| population | 1,851 ARN resources · 1,500 summarized · **351 unknown-thin** |
| store | `resource_summaries` Iceberg table via `infra/aws/globgrph/resource_summaries_store.py` |
| reads | *"the live comp-kuzu derive-at-scan corpus + comp-heat/comp-debris heat"* |

### 3.1 ⛔ DETERMINISM IS SUSPECT AND THAT IS THE POINT OF THIS CARD

`1.0.0_SA_CTO~X` observed **five distinct pairs returning byte-identical `summary_sim = 1.031`.** That is
the signature of **templated summaries**, not of five genuinely equidistant resources.

**Why it matters, and it is not a curiosity: a view that cannot discriminate carries ZERO BITS.** If it
enters a fusion it **dilutes the views that work while looking like corroboration** — a wrong answer wearing
the appearance of agreement.

**This is `held`, not measured.** Your job is to measure it. **`COX-AC4` is the criterion this subject lives
on:** if `determinism` lands `inferential` or `hybrid`, `inference_detail` must be populated — model,
invocations per run, the deterministic/inferential stage split, and **`failure_is_loud`**.

⛔ **`failure_is_loud: false` IS THE DANGEROUS CASE AND THE ONE ANDREW IS PAYING FOR** — a failed inference
that returns *plausible content* rather than an error. Establish it by exercise, not by reading the code's
intent.

**Andrew wants this priced, not just qualified** (PRD s.4, his words: *"this all works into cost structure
when you think about building and operating this system"*). `invocations_per_run` is a cost figure.

### 3.2 ⛔ THE KEY ROW — ANDREW NAMED THIS ONE HIMSELF, VERBATIM

> *"ARN is a good stable key for AWS resources but obviously doesn't cover the MS or Git spaces."*

**`SC-h-6` is where that gets pinned.** A key that is stable **within** its space and silently absent
**outside** it is not the same as a stable key — and the schema's `crosses_spaces` + `declared_mapping` pair
is exactly the field that expresses the difference. **The 351 unknown-thin resources are the population most
likely to expose it.**

## 4. COMPILER TOOLS MANDATE

<compiler_tools_mandate>
<phase id="0" when="before any card is written -- DISCOVERY">
  <step>
    <run>comp-which "what builds the C3.i structures and what underlies comp-similar"</run>
    <expect>named generators for both; ANCHOR_CATALOG for C3.i, resource_summaries_store.py for comp-similar</expect>
    <if_mismatch>widen DELIBERATELY (HEAD -> DEF -> --all, `-i` for any census) before concluding absent</if_mismatch>
  </step>
  <step>
    <run>comp-estate --layers, then drill to the globgrph layer</run>
    <expect>the layer and its recreatable pattern</expect>
    <if_mismatch>comp-estate's `served:` field MIXES live-derived detail with snapshot prose and carries NO marker -- treat every topology claim as a PRIOR UNDER TEST and ground it on the live primitive</if_mismatch>
  </step>
</phase>
<phase id="1" when="before writing each card -- MEASUREMENT">
  <step>
    <run>read infra/aws/globgrph/resource_summaries_store.py AND the live Iceberg table -- source AND state</run>
    <expect>a measured row count with its denominator, and the table's actual home</expect>
    <if_mismatch>⛔ DESIRED (source) != APPLIED (live) != EXERCISED. A description is never a state; say which you read.</if_mismatch>
  </step>
  <step>
    <run>EXERCISE the comp-similar determinism question -- run the same pair repeatedly and across pairs; look for the 1.031 signature</run>
    <expect>either reproduction of the byte-identical values (templating CONFIRMED) or genuine variance</expect>
    <if_mismatch>⛔ A PERFECTLY UNIFORM RESULT ACROSS DISTINCT INPUTS IS AN INSTRUMENT SIGNATURE, NOT A DEFECT SIGNATURE -- check your own harness before concluding about the estate. If you cannot settle it, `determinism: unknown` WITH evidence of what you tried is the honest and ACCEPTED answer.</if_mismatch>
  </step>
  <step>
    <run>EXERCISE each subject's failure path -- ask it something it cannot answer, read what comes back</run>
    <expect>an observed value for failure_mode.returns_on_failure</expect>
    <if_mismatch>if it cannot be exercised, `distinguishable_from_true_negative` is `unmeasured` and basis is `absent` WITH evidence of what you tried. Rule 28 q7: exercise it, never read it off a docstring.</if_mismatch>
  </step>
</phase>
<phase id="2" when="before commit -- CONFORMANCE">
  <step>
    <run>python -c "import json,jsonschema;s=json.load(open('org/standards/SUBSTRATE_CARD.schema.json'));[jsonschema.Draft202012Validator(s).validate(json.load(open(p))) for p in ['&lt;c3i&gt;.json','&lt;compsimilar&gt;.json']];print('2/2 VALID')"</run>
    <expect>2/2 VALID</expect>
    <if_mismatch>fix the card, never the schema (boundary BOUNDARY-4)</if_mismatch>
  </step>
</phase>
<phase id="3" when="after commit">
  <step>
    <run>python .tools/proof-of-spec-check.py &lt;instance&gt;.json COX-AC1,COX-AC2,COX-AC3,COX-AC4,COX-AC5,COX-AC6,COX-AC7</run>
    <expect>rc=0, VALID, alignment ENFORCE with denominators printed</expect>
    <if_mismatch>do NOT flip status to complete; report the failing criterion with its cell_ref</if_mismatch>
  </step>
</phase>
</compiler_tools_mandate>

## 5. ACCEPTANCE CRITERIA

| id | criterion | grounding |
|---|---|---|
| **COX-AC1** | Two JSON cards exist and **both VALIDATE**. All 14 rows carry non-empty `basis` + `evidence` + `owner`. | validator, 2/2 |
| **COX-AC2** | Both carry **byte-identical** `as_of.commit_ish` and `as_of.graph_vintage` per s.1. | diff of both `as_of` blocks |
| **COX-AC3** | `coverage.denominator` **NON-NULL** on both, `"N of M"`, both numbers named. | ⛔ **Schema PERMITS null — exercised (finding F-1). Only this criterion catches it.** For `comp-similar`, `"1,500 of 1,851"` with the 351 unknown-thin named in `explicitly_out` is the shape. |
| **COX-AC4** | `determinism` in {`inferential`,`hybrid`} ⇒ **populated `inference_detail`** incl. `failure_is_loud` and `invocations_per_run`. | ⛔ **Requirement lives in a `description` string with no `if/then` (finding F-2). THIS IS THE CRITERION `comp-similar` LIVES ON.** |
| **COX-AC5** | `verdict.standing` is `INCOMPLETE` **iff** ≥1 row is genuinely unworked. | ⛔ **Schema permits SOUND over an unworked row (finding F-3).** C3.i is expected `UNSOUND` — that is not INCOMPLETE. |
| **COX-AC6** | **ZERO commits by this lane touching any generator it carded.** | QUALIFY-DO-NOT-FIX. |
| **COX-AC7** | Both `key` rows state `identity_space`, `key_is_stable` and `crosses_spaces`, and where `crosses_spaces` is true, `declared_mapping` is either a real location **or `null` WITH evidence of where a mapping was sought**. | ⛔ **The two highest-value cells in this TO.** Andrew named the ARN/MS/Git gap himself. |

## 6. WHAT IS A PASS EVEN THOUGH IT LOOKS LIKE A FAILURE

Per `1.0.0_SA_CTO~X` 72797 — **a card that finds defects is a PASSING card.**
- **C3.i carding `UNSOUND`** — expected, correct, the baseline working.
- `determinism: "unknown"` **with evidence of what you tried** — the schema's own words: *never default to
  `deterministic` because it looks that way.* **The failure is the opposite: a confident `deterministic` with
  no exercise behind it.**
- `UNOWNED` where a remedy genuinely has no owner. **Legal and loud; a GUESSED owner is worse than none.**
- **Empty arrays are claims, not gaps.**
- `failure_mode.distinguishable_from_true_negative: "no"` — **the single most valuable thing this project can
  surface.** Report it loudly.

⛔ **AND THE ONE MOST LIKELY TO COST YOU A REWORK:** `basis: "absent"` **WITH evidence** is a **WORKED** row —
you measured that it is unmeasurable. **PASS.** Blank, guessed or unfilled is the rework. The schema cannot
tell them apart.

## 7. CROSS-DOMAIN COORDINATION

<cross_domain_coordination>
- ⛔ **`0.8.0_AE_CloudComp~X` holds C0/C1/C2 and C3.i CONSUMES C2's classes** (19 class nodes = 13 families +
  6 defect-detector motifs). **Coordinate by MCP before either lane publishes a class-count figure** — one
  measures, the other cites with attribution. Two cards carrying two numbers for one count at two vintages is
  precisely the defect this project exists to find.
- ⚠ **C2 only began running in production TODAY** (never imported in-container since 2026-08-07; fixed
  `@ec0408628a`). **Any pre-2026-08-26 artifact about C2 describes a layer that was not running** — relevant
  if a C3.i claim rests on C2 output.
- **`0.8.0_AE_CloudComp~Y`** holds D1/D2/D3. **D3 is the rail that would sit between C2 and C3.i** — your
  baseline card is context for theirs, not a dependency in either direction.
- **`0.4.0_DT_ClientPlatform~X`** builds the graph-object manifest FROM every card's
  `location.projection_of`. **`resource_summaries` and the kuzu corpus are exactly the stores their manifest
  needs** — populate `projection_of` and `co_resident_stores` carefully; it is their input, not decoration.
- **`infra/aws/globgrph/` is READ-ONLY for this TO.** A needed change there is a finding with an owner.
</cross_domain_coordination>

## 8. DELIVERABLES

1. Two cards. Suggested home: `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS/{C3i,comp_similar}.json`.
2. The proof-of-spec instance at the `<instance_path>` above.
3. A session log with a **mandatory `## Compiler Tools` section** — every `<run>`, observed result, pass/fail
   vs `<expect>`. **Blank and "N/A" are not acceptable.**
4. **Route to `3.0.0_SA_CVO~X`** at the completion flip, cc me. **Verification lane, not an approval gate.**

## 9. SURPRISE CHANNEL

Spec is **FROZEN** mid-round. Only legal off-spec act is to **SURFACE**: one line by MCP to `3.0.0_SA_CVO`,
cc me. **OBSERVATION never interrupts.** **BLOCKING routes same-turn to me.**

⛔ **A finding about a subject you are carding is NOT a surprise — it is the deliverable.** Put it in the card.

**Your open audit-archive item (stale baseline 157h + 1 uncovered audit log) is on your own owned surface and
is NOT part of this TO.** It is already surfaced by two seats and I am carrying it. **Do not let it consume
this lane's context** — one project per instance, and this instance holds D11.
