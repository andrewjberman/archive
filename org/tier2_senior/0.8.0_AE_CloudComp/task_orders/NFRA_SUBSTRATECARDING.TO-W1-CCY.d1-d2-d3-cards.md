<task_order>
<id>NFRA_SUBSTRATECARDING.TO-W1-CCY.d1-d2-d3-cards</id>
<project>NFRA_SUBSTRATECARDING</project>
<issued_to>0.8.0_AE_CloudComp~Y</issued_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<executor_class>0.8.0_AE_CloudComp (~lane instance; SINGLE-PROJECT -- this instance holds NFRA_SUBSTRATECARDING and nothing else)</executor_class>
<status>pending</status>
<priority>P1 -- D11 wave 1. Andrew named D2 completeness specifically.</priority>
<date>2026-08-26</date>
<placement>LAPTOP (declared decomp axis; no cross-fabric edge, no ferry semantics)</placement>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/nfra-substratecarding/20260826T172918Z/DECOMP.md @7c5de3e779</ref>
  <ref type="prd">docs/architecture/D11_SUBSTRATE_ANALYSIS_PRD.md @944ca89492</ref>
  <ref type="contract">org/standards/SUBSTRATE_CARD.schema.json @944ca89492</ref>
  <ref type="law">CLAUDE.md Rule 28 -- THE SUBSTRATE TEST @ec35b78c1c</ref>
  <ref type="acceptance">1.0.0_SA_CTO~X msg 72797 -- the eight PASSES and the four correct REWORKs</ref>
  <ref type="sibling_to">NFRA_SUBSTRATECARDING.TO-W1-CCX.c0-c1-c2-cards.md (0.8.0_AE_CloudComp~X) -- their C2 card is an INPUT to your D2 card</ref>
</references>
<objective>
Produce THREE conformant substrate cards -- D1 (value/grain rail), D2 (path/flow
rail), D3 (contract rail) -- one JSON document each, validating against
SUBSTRATE_CARD.schema.json, every row carrying basis + evidence + owner.
QUALIFY ONLY: name defects and their owners; remediate nothing.
</objective>
</task_order>

# TASK ORDER — NFRA_SUBSTRATECARDING.TO-W1-CCY · D1 / D2 / D3 SUBSTRATE CARDS

**to:** `0.8.0_AE_CloudComp~Y` · **issuer:** `2.0.0_SA_COO~X` · **cut:** 2026-08-26 ~17:5xZ

⛔ **UNCERTIFIED DECOMP.** The stage-3 decomp this TO derives from is authored and merged but **NOT YET
CERTIFIED** by `3.0.0_SA_CVO~X`. Stated on this TO's face per the pipeline's escape valve rather than
holding your work behind it. **Practical effect on you: none** — a DECOMP-INVALIDATING verdict is MY act
to re-decomp and re-issue; you do not re-run anything on your own initiative.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding/20260826T172918Z/DECOMP.md @7c5de3e779
Cells discharged (21 CARD_MATRIX, enumerated LITERALLY -- a glob cannot be joined to a criterion):
SC-D1-methodology, SC-D1-cadence, SC-D1-persistence, SC-D1-location, SC-D1-coverage, SC-D1-key, SC-D1-failure_mode,
SC-D2-methodology, SC-D2-cadence, SC-D2-persistence, SC-D2-location, SC-D2-coverage, SC-D2-key, SC-D2-failure_mode,
SC-D3-methodology, SC-D3-cadence, SC-D3-persistence, SC-D3-location, SC-D3-coverage, SC-D3-key, SC-D3-failure_mode
Contributed-to (PROJECT_MECHANISM, not solely owned by this TO): SC-m-asof, SC-m-qualify
</decomp_ref>

<proof_of_spec>
  <!-- python .tools/proof-of-spec-check.py <instance>.json CCY-AC1,CCY-AC2,CCY-AC3,CCY-AC4,CCY-AC5,CCY-AC6,CCY-AC7 ; check rc -->
  <criterion id="CCY-AC1" cell_refs="SC-D1-methodology, SC-D1-cadence, SC-D1-persistence, SC-D1-location, SC-D1-coverage, SC-D1-key, SC-D1-failure_mode, SC-D2-methodology, SC-D2-cadence, SC-D2-persistence, SC-D2-location, SC-D2-coverage, SC-D2-key, SC-D2-failure_mode, SC-D3-methodology, SC-D3-cadence, SC-D3-persistence, SC-D3-location, SC-D3-coverage, SC-D3-key, SC-D3-failure_mode"/>
  <criterion id="CCY-AC2" cell_refs="SC-m-asof"/>
  <criterion id="CCY-AC3" cell_refs="SC-D1-coverage, SC-D2-coverage, SC-D3-coverage"/>
  <criterion id="CCY-AC4" cell_refs="SC-D1-methodology, SC-D2-methodology, SC-D3-methodology"/>
  <criterion id="CCY-AC5" cell_refs="SC-D1-methodology, SC-D1-cadence, SC-D1-persistence, SC-D1-location, SC-D1-coverage, SC-D1-key, SC-D1-failure_mode, SC-D2-methodology, SC-D2-cadence, SC-D2-persistence, SC-D2-location, SC-D2-coverage, SC-D2-key, SC-D2-failure_mode, SC-D3-methodology, SC-D3-cadence, SC-D3-persistence, SC-D3-location, SC-D3-coverage, SC-D3-key, SC-D3-failure_mode"/>
  <criterion id="CCY-AC6" cell_refs="SC-m-qualify"/>
  <criterion id="CCY-AC7" cell_refs="SC-D2-persistence, SC-D2-location, SC-D3-persistence, SC-D3-location, SC-D1-persistence, SC-D1-location"/>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_SUBSTRATECARDING.TO-W1-CCY_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>CCY-AC1,CCY-AC2,CCY-AC3,CCY-AC4,CCY-AC5,CCY-AC6,CCY-AC7</expected_criteria>
  <alignment_denominators>
criteria: 7. Cells discharged: 21 of 21 CARD_MATRIX cells for D1/D2/D3, plus 2 shared PROJECT_MECHANISM
cells (SC-m-asof, SC-m-qualify) contributed to, not solely owned.
CELL -> CRITERION: all 21 covered (AC1 and AC5 span them; AC3/AC4/AC7 add row-specific bars). Unmapped: 0.
CRITERION -> CELL: all 7 carry >=1 cell_ref. Untraceable: 0.
  </alignment_denominators>
</proof_of_spec>

---

## 1. THE WAVE STAMP — COPY IT EXACTLY, DO NOT DERIVE IT

```json
"as_of": {
  "carded_utc":    "<YOUR OWN clock read at carding -- date -u, never estimated between turns>",
  "commit_ish":    "fe269171f2",
  "graph_vintage": "kuzu_nessie_db@2902399899597701830"
}
```

⛔ **`commit_ish` IS THE WAVE ANCHOR, NOT YOUR EVIDENCE VINTAGE.** The repo moved 3 commits in the 20
minutes after I pinned it. **Every `evidence` string carries ITS OWN commit** — `file:line @ <what you
actually read>`. **Never back-date a citation to the anchor**: a false vintage is worse than a missing one,
because a missing marker makes a reader ask and a false one makes them stop asking.

⛔ **`graph_vintage` NAMES THE PROJECTION PLANE (`kuzu_nessie_db`, 27,035 nodes / 58,224 edges), NOT THE
WAREHOUSE** (which `1.0.0_SA_CTO~X` measured at 27,061 / 60,858). Two planes, two vintages, **neither
wrong**. Cite the plane in `evidence`; do not reconcile them and do not re-pin `as_of`.

## 2. YOUR THREE SUBJECTS — AND THEY ARE NOT EQUALLY SHAPED

| cell prefix | subject | given (basis `held` from `1.0.0_SA_CTO~X` — measure, do not inherit) |
|---|---|---|
| `SC-D1-*` | **D1** — value / grain rail | **Not probed. A clean subject: start from zero.** |
| `SC-D2-*` | **D2** — path / flow rail | `reserved_ratified`. Authority: `NFRA_ONTOLOGY_RULE_BANK.yaml#dynamic_rails.D2_path_flow` (rail block, **7 keys at 2026-08-20**). Defined as *"adds DIRECTION + TRANSFORM + TIME to C2 motifs; does not re-implement motif membership."* |
| `SC-D3-*` | **D3** — contract rail | Sits between C2 and C3, so it **cannot be COMPLETED before C3.i exists.** |

### 2.1 ⛔ D2 IS THE ONE ANDREW NAMED, AND ITS OPEN QUESTIONS ARE EXACTLY TWO

**`persistence` and `location` are THE open questions on D2 — that is what the card is for.** A rail that
is `reserved_ratified` has a DECLARED definition; whether anything PERSISTS it, and WHERE, is unmeasured.
**Andrew wants completeness confirmed here specifically.**

So on D2, do not stop at the rule-bank block. The rule-bank entry is a **DECLARATION** (Rule 22's DESIRED
state). **A description is never a state.** Push to APPLIED: is there a generator? does it write anything?
where does the output live, if anywhere? **`persisted: false` / `home: null` is a legitimate and important
answer — but it must be MEASURED, not assumed from the absence of an obvious file.**

### 2.2 ⛔ D3 IS EXPECTED TO CARD EMPTY, AND THAT IS THE DELIVERABLE

The PRD rules D3 **carded anyway**, with the likely result `persistence: none` / `location: null`.
**That emptiness IS the finding.** `1.0.0_SA_CTO~X` 72797 case 1 confirms it as a PASS, not a rework.

⛔ **DO NOT HOLD D3 WAITING ON C3.i.** It is explicitly **NOT a blocking dependency edge** in the decomp.
A lane that waits has misread the TO. **An empty card is information; an absent card is not.**

⛔ **AND DO NOT MANUFACTURE CONTENT TO AVOID AN EMPTY CARD.** The temptation on a subject that reads empty
is to widen the search until something is found and card that instead. **If D3 persists nothing, the card
says so, with evidence of where you looked and the denominator of that search.** A card that reports a
neighbouring artifact as though it were D3's is worse than an empty one, because it is confidently wrong.

## 3. COMPILER TOOLS MANDATE

<compiler_tools_mandate>
<phase id="0" when="before any card is written -- DISCOVERY">
  <step>
    <run>comp-which "what generates and persists the D1 value rail / D2 path-flow rail / D3 contract rail"</run>
    <expect>routes to a rich tool, or runs comp-find on rails; a named generator per rail OR a measured absence</expect>
    <if_mismatch>widen DELIBERATELY (HEAD -> DEF -> --all, and `-i` for any census -- this estate CAPITALISES its load-bearing words) before concluding absent. An early stop and a true absence are identical in your notes and opposite in the estate.</if_mismatch>
  </step>
  <step>
    <run>read NFRA_ONTOLOGY_RULE_BANK.yaml#dynamic_rails -- the D2 block AND its siblings</run>
    <expect>the 7 declared keys, and whether D1/D3 have comparable blocks</expect>
    <if_mismatch>a rail with NO rule-bank block is itself a finding for that rail's methodology row -- record it, do not create one.</if_mismatch>
  </step>
</phase>
<phase id="1" when="before writing each card -- MEASUREMENT">
  <step>
    <run>for each rail: hunt the PERSISTED artifact -- comp-find --name over plausible outputs, then the live store (S3 / Iceberg / kuzu / disk)</run>
    <expect>a home path, or a MEASURED absence with the search denominator printed</expect>
    <if_mismatch>⛔ a firm-partitioned or tree-scoped absence MUST NAME THE TREE IT SEARCHED -- a 404 in the wrong bucket returns a clean, confident, well-formed ZERO. Print what you swept.</if_mismatch>
  </step>
  <step>
    <run>EXERCISE each rail's failure path -- ask it something it cannot answer and read what comes back</run>
    <expect>an observed return value for failure_mode.returns_on_failure</expect>
    <if_mismatch>if it cannot be exercised (e.g. nothing implements the rail), `distinguishable_from_true_negative` is `unmeasured` and basis is `absent` WITH evidence of what you tried. Rule 28 q7: exercise it, never read it off a docstring.</if_mismatch>
  </step>
</phase>
<phase id="2" when="before commit -- CONFORMANCE">
  <step>
    <run>python -c "import json,jsonschema;s=json.load(open('org/standards/SUBSTRATE_CARD.schema.json'));[jsonschema.Draft202012Validator(s).validate(json.load(open(p))) for p in ['&lt;d1&gt;.json','&lt;d2&gt;.json','&lt;d3&gt;.json']];print('3/3 VALID')"</run>
    <expect>3/3 VALID</expect>
    <if_mismatch>fix the card, never the schema. The schema is the FREEZE; amending it is outside your lane (boundary SC-g-4).</if_mismatch>
  </step>
</phase>
<phase id="3" when="after commit">
  <step>
    <run>python .tools/proof-of-spec-check.py &lt;instance&gt;.json CCY-AC1,CCY-AC2,CCY-AC3,CCY-AC4,CCY-AC5,CCY-AC6,CCY-AC7</run>
    <expect>rc=0, VALID, alignment ENFORCE with denominators printed</expect>
    <if_mismatch>do NOT flip status to complete; report the failing criterion to me with its cell_ref</if_mismatch>
  </step>
</phase>
</compiler_tools_mandate>

## 4. ACCEPTANCE CRITERIA — MACHINE-CHECKABLE

| id | criterion | grounding |
|---|---|---|
| **CCY-AC1** | Three JSON cards (D1, D2, D3) exist and **all three VALIDATE**. All 21 rows carry non-empty `basis` + `evidence` + `owner`. | validator output, 3/3 |
| **CCY-AC2** | All three carry **byte-identical** `as_of.commit_ish` and `as_of.graph_vintage` per s.1. | diff of the three `as_of` blocks |
| **CCY-AC3** | `coverage.denominator` **NON-NULL** on all three, `"N of M"`, both numbers named. | ⛔ **The schema PERMITS null — I exercised it (finding F-1). Only this criterion catches it.** For a rail that spans nothing, the honest form is still `"0 of M"` with M named, never null. |
| **CCY-AC4** | `determinism` in {`inferential`,`hybrid`} ⇒ **populated `inference_detail`** incl. `failure_is_loud`. | ⛔ **Requirement lives in a `description` string with no `if/then` (finding F-2). Only this criterion catches it.** |
| **CCY-AC5** | `verdict.standing` is `INCOMPLETE` **iff** ≥1 row is genuinely unworked. | ⛔ **Schema permits SOUND over an unworked row (finding F-3).** See s.6 — `absent`-with-evidence is WORKED. |
| **CCY-AC6** | **ZERO commits by this lane touching any rail it carded** during the wave. | QUALIFY-DO-NOT-FIX. |
| **CCY-AC7** | For every rail carding `persisted: false` or `home: null`, `evidence` names **WHERE YOU LOOKED and the denominator of that search**. | ⛔ **This is the criterion D3 lives or dies on.** An unevidenced "nothing persists it" is indistinguishable from "I did not look", and those take opposite actions. |

## 5. CROSS-DOMAIN COORDINATION

<cross_domain_coordination>
- ⛔ **`0.8.0_AE_CloudComp~X` holds C0/C1/C2 and THEIR C2 CARD IS AN INPUT TO YOUR D2 CARD.** D2 is defined
  *against* C2's motifs. **Do NOT re-implement motif membership** — the D2 definition explicitly says it
  does not, and a D2 card that re-derives C2's families has carded the wrong thing. Take their
  `SC-C2-methodology` finding when it lands; **do not block on it** — D2's persistence/location questions
  are independent of it.
- ⛔ **AND DO NOT BOTH CARD THE SAME NUMBER.** If you and `~X` each need a motif/class count, coordinate by
  MCP first so two cards do not carry two figures at two vintages. One of you measures, the other cites
  with attribution.
- **`0.7.0_AE_CloudOps~X`** holds C3.i-as-built. **Your D3 card describes the rail that would sit between
  C2 and C3.i** — their baseline card is context for yours, not a dependency.
- **`0.4.0_DT_ClientPlatform~X`** builds the graph-object manifest FROM every card's
  `location.projection_of`. **Populate it carefully even when the answer is `[]`** — an empty array is a
  claim that this rail projects from nothing, which is exactly what their manifest needs to record.
- **`NFRA_ONTOLOGY_RULE_BANK.yaml` is READ-ONLY for you.** A needed change there is a finding with an
  owner, never an edit.
</cross_domain_coordination>

## 6. ⛔ THE DISTINCTION MOST LIKELY TO COST YOU A REWORK

**`basis: "absent"` and "unworked" are NOT the same, and the schema cannot tell them apart.**
- `absent` **WITH evidence explaining why no basis exists** = you measured that it is unmeasurable. **PASS.**
- **Blank, guessed, or unfilled** = not worked. **REWORK.**

**This matters more on your TO than on any other in the wave**, because D2 and D3 are the subjects most
likely to card empty. **An empty card built on measurement is the project working. An empty card built on
not-looking is the project failing, and they look identical from outside.** AC7 is what separates them.

**A card that finds defects is a PASSING card** (`1.0.0_SA_CTO~X` 72797): `determinism: unknown` with
evidence of what you tried, `UNOWNED`, empty arrays as claims, `distinguishable_from_true_negative: no` as
a **high-value finding**. A SOUND card about an UNSOUND subject is two different objects.

## 7. DELIVERABLES

1. Three cards. Suggested home: `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/{D1,D2,D3}.json`.
   ⚠ `0.8.0_AE_CloudComp~X` writes into the same `D11_CARDS/` directory — **distinct filenames, no shared
   file**, so there is no write collision. Confirm by MCP if you deviate from these names.
2. The proof-of-spec instance at the `<instance_path>` above.
3. A session log with a **mandatory `## Compiler Tools` section** — every `<run>`, its observed result, and
   pass/fail vs `<expect>`. **Blank and "N/A" are not acceptable.**
4. **Route to `3.0.0_SA_CVO~X`** when you flip toward complete, cc me. They are a **verification lane, not
   an approval gate.**

## 8. SURPRISE CHANNEL

Spec is **FROZEN** mid-round. Your only legal off-spec act is to **SURFACE**: one line by MCP to
`3.0.0_SA_CVO`, cc me. **OBSERVATION never interrupts — one line, keep working.** **BLOCKING routes
same-turn to me** as issuer. Any **ARMED** item disarms same-turn via a named owner.

⛔ **A finding about a rail you are carding is NOT a surprise — it is the deliverable.** Put it in the card.

**Your `check-inbox` observation (72818) was correctly classed and correctly not chased** — that is the
channel working as designed. It is routed; you carry nothing further on it. **Keep working.**
