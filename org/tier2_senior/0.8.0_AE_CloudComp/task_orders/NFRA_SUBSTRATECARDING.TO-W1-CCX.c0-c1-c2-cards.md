<task_order>
<id>NFRA_SUBSTRATECARDING.TO-W1-CCX.c0-c1-c2-cards</id>
<project>NFRA_SUBSTRATECARDING</project>
<issued_to>0.8.0_AE_CloudComp~X</issued_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<executor_class>0.8.0_AE_CloudComp (~lane instance; SINGLE-PROJECT -- this instance holds NFRA_SUBSTRATECARDING and nothing else)</executor_class>
<status>pending</status>
<priority>P1 -- D11 wave 1. No external clock; the constraint is the wave's shared as_of, which erodes if lanes run far apart.</priority>
<date>2026-08-26</date>
<placement>LAPTOP (declared decomp axis; no cross-fabric edge, no ferry semantics)</placement>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/nfra-substratecarding/20260826T172918Z/DECOMP.md @7c5de3e779</ref>
  <ref type="prd">docs/architecture/D11_SUBSTRATE_ANALYSIS_PRD.md @944ca89492</ref>
  <ref type="contract">org/standards/SUBSTRATE_CARD.schema.json @944ca89492</ref>
  <ref type="law">CLAUDE.md Rule 28 -- THE SUBSTRATE TEST @ec35b78c1c</ref>
  <ref type="acceptance">1.0.0_SA_CTO~X msg 72797 -- the eight PASSES and the four correct REWORKs</ref>
  <ref type="reference_card">nerves_resolve, carded by 1.0.0_SA_CTO~X -- an EXAMPLE, not a wave member</ref>
</references>
<objective>
Produce THREE conformant substrate cards -- C0 (facts/nodes), C1 (interactions/edges),
C2 (motifs) -- one JSON document each, validating against SUBSTRATE_CARD.schema.json,
every row carrying basis + evidence + owner. QUALIFY ONLY: name defects and their
owners; remediate nothing.
</objective>
</task_order>

# TASK ORDER — NFRA_SUBSTRATECARDING.TO-W1-CCX · C0 / C1 / C2 SUBSTRATE CARDS

**to:** `0.8.0_AE_CloudComp~X` · **issuer:** `2.0.0_SA_COO~X` · **cut:** 2026-08-26 ~17:5xZ

⛔ **UNCERTIFIED DECOMP.** The stage-3 decomp this TO derives from is **authored and merged but NOT YET
CERTIFIED** by `3.0.0_SA_CVO~X`. Per the pipeline's own escape valve I am stating that on this TO's face
rather than holding your work behind it. **Practical effect on you: none** — if certification returns
DECOMP-INVALIDATING, the re-decomp is MY act and I will re-issue; you do not re-run anything on your own
initiative. Disclosed because a silent uncertified decomp is the pipeline's single point of failure.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding/20260826T172918Z/DECOMP.md @7c5de3e779
Cells discharged (21 CARD_MATRIX, enumerated LITERALLY -- a glob cannot be joined to a criterion):
SC-a-1, SC-a-2, SC-a-3, SC-a-4, SC-a-5, SC-a-6, SC-a-7,
SC-b-1, SC-b-2, SC-b-3, SC-b-4, SC-b-5, SC-b-6, SC-b-7,
SC-c-1, SC-c-2, SC-c-3, SC-c-4, SC-c-5, SC-c-6, SC-c-7
Contributed-to (PROJECT_MECHANISM, not solely owned by this TO): SC-m-2, SC-m-5
</decomp_ref>

<proof_of_spec>
  <!-- python .tools/proof-of-spec-check.py <instance>.json CCX-AC1,CCX-AC2,CCX-AC3,CCX-AC4,CCX-AC5,CCX-AC6,CCX-AC7 ; check rc -->
  <criterion id="CCX-AC1" cell_refs="SC-a-1, SC-a-2, SC-a-3, SC-a-4, SC-a-5, SC-a-6, SC-a-7, SC-b-1, SC-b-2, SC-b-3, SC-b-4, SC-b-5, SC-b-6, SC-b-7, SC-c-1, SC-c-2, SC-c-3, SC-c-4, SC-c-5, SC-c-6, SC-c-7"/>
  <criterion id="CCX-AC2" cell_refs="SC-m-2"/>
  <criterion id="CCX-AC3" cell_refs="SC-a-5, SC-b-5, SC-c-5"/>
  <criterion id="CCX-AC4" cell_refs="SC-a-1, SC-b-1, SC-c-1"/>
  <criterion id="CCX-AC5" cell_refs="SC-a-1, SC-a-2, SC-a-3, SC-a-4, SC-a-5, SC-a-6, SC-a-7, SC-b-1, SC-b-2, SC-b-3, SC-b-4, SC-b-5, SC-b-6, SC-b-7, SC-c-1, SC-c-2, SC-c-3, SC-c-4, SC-c-5, SC-c-6, SC-c-7"/>
  <criterion id="CCX-AC6" cell_refs="SC-m-5"/>
  <criterion id="CCX-AC7" cell_refs="SC-a-4, SC-b-4, SC-c-4, SC-a-6, SC-b-6, SC-c-6, SC-a-7, SC-b-7, SC-c-7"/>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_SUBSTRATECARDING.TO-W1-CCX_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>CCX-AC1,CCX-AC2,CCX-AC3,CCX-AC4,CCX-AC5,CCX-AC6,CCX-AC7</expected_criteria>
  <alignment_denominators>
criteria: 7. Cells discharged by this TO: 21 of 21 CARD_MATRIX cells for C0/C1/C2, plus 2 shared
PROJECT_MECHANISM cells (SC-m-2, SC-m-5) which this TO contributes to and does not solely own.
CELL -> CRITERION: all 21 covered (AC1, AC5 and AC7 span them; AC3/AC4 add row-specific bars). Unmapped: 0.
CRITERION -> CELL: all 7 carry >=1 cell_ref. Untraceable: 0.
  </alignment_denominators>
</proof_of_spec>

---

## 1. THE WAVE STAMP — COPY IT EXACTLY, DO NOT DERIVE IT

Every card you produce carries **exactly** this `as_of`. A card at a different vintage is a **wave**
defect, rejected at merge without re-reading the card.

```json
"as_of": {
  "carded_utc":    "<YOUR OWN clock read at carding -- date -u, never estimated between turns>",
  "commit_ish":    "fe269171f2",
  "graph_vintage": "kuzu_nessie_db@2902399899597701830"
}
```

⛔ **`commit_ish` IS THE WAVE ANCHOR, NOT YOUR EVIDENCE VINTAGE.** The repo moves under you — it was
already 3 commits past `fe269171f2` twenty minutes after I pinned it. So:
- `as_of.commit_ish` answers *"which wave is this card part of."* Identical on all three cards.
- **Every `evidence` string carries ITS OWN commit** — `file:line @ <the commit you actually read>`.
- ⛔ **NEVER back-date an evidence citation to the wave anchor.** A false vintage is worse than a missing
  one: a missing marker makes a reader ask, a false one makes them stop asking.

⛔ **`graph_vintage` NAMES THE PROJECTION PLANE (`kuzu_nessie_db`), NOT THE WAREHOUSE.** My pin reads
**27,035 nodes / 58,224 edges** (built 2026-08-26T14:07:59Z). `1.0.0_SA_CTO~X` measured the *warehouse* at
**27,061 / 60,858**. **Neither is wrong and they are not in conflict — they are two planes.** If you cite a
warehouse-plane number, **say the plane in `evidence`**; do not re-pin `as_of` and do not "reconcile" them.

**ROW LEGEND — your cell numbers, in the schema's own required order:**
`-1` methodology · `-2` cadence · `-3` persistence · `-4` location · `-5` coverage · `-6` key · `-7` failure_mode

## 2. YOUR THREE SUBJECTS

| cell prefix | subject | declared_domain to state | given (from `1.0.0_SA_CTO~X`, basis `held` — measure, do not inherit) |
|---|---|---|---|
| `SC-a-1..7` | **C0** — facts / nodes | what C0 claims to cover | Not probed by CTO~X. A clean subject: start from zero. |
| `SC-b-1..7` | **C1** — interactions / edges | what C1 claims to cover | Not probed by CTO~X. A clean subject: start from zero. |
| `SC-c-1..7` | **C2** — motifs | what C2 claims to cover | Composers at `org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/` (`c2_individuate.py`, `c3_cover.py`). 6,207 instances, 13 canonical families; graph carries 19 class nodes = 13 families + 6 defect-detector motifs. Coverage by side: BACKEND 93.7% of scope / FRONTEND 28.2% / KNOWLEDGE 0-of-0 by construction. |

⛔ **C2 CARRIES A TRAP AND IT IS THE SHARPEST THING IN THIS TO.** That layer **only began running in
production TODAY (2026-08-26)** — it had never once imported in-container since 2026-08-07 (IndexError at
module import, fixed `@ec0408628a`, confirmed by the 02:00Z nightly). **Any artifact, log, or claim about
C2 dated before 2026-08-26 describes a layer that was not running.** Treat pre-today evidence as evidence
about absence-of-execution, not about behaviour. This bears directly on `SC-c-2`
(`live_matches_declared`) and `SC-c-7` — a failure mode never exercised in production is
`unmeasured`, not `yes`.

⛔ **The CTO~X figures above are `held`, not `measured` — they are a peer's published invocation at a
DIFFERENT vintage.** You may cite them as `basis: "held"` with attribution, or re-derive them yourself and
mark `measured`. **You may not copy them and stamp `measured`.** Re-deriving with the SAME command is not
re-derivation; use a different instrument or cite theirs honestly.

## 3. COMPILER TOOLS MANDATE

<compiler_tools_mandate>
<phase id="0" when="before any card is written -- DISCOVERY">
  <step>
    <run>comp-which "what generates the C0 facts / C1 edges / C2 motifs in the graph"</run>
    <expect>routes to a rich tool (comp-estate / comp-kuzu / comp-blast) or runs comp-find on rails; a named generator per subject</expect>
    <if_mismatch>widen DELIBERATELY down the bands (HEAD -> DEF -> --all) before concluding absent; an early stop and a true absence are identical in your notes and opposite in the estate. Record the widening in your log.</if_mismatch>
  </step>
  <step>
    <run>comp-estate --layers  then drill to the layer owning each subject</run>
    <expect>the layer and its recreatable pattern, feeding methodology.composes / methodology.invents</expect>
    <if_mismatch>comp-estate's `served:` field MIXES live-derived detail with snapshot prose and carries NO marker -- treat any topology claim as a PRIOR UNDER TEST and ground it on the live primitive before it enters a card.</if_mismatch>
  </step>
</phase>
<phase id="1" when="before writing each card -- MEASUREMENT">
  <step>
    <run>comp-kuzu "&lt;the traversal that establishes this subject's coverage&gt;" -- and READ THE PROVENANCE HEADER</run>
    <expect>a count WITH its denominator, and the header's vintage matching the wave pin</expect>
    <if_mismatch>UNKNOWN VINTAGE = freshness unverifiable; a scratch DB (--db-path) is a frozen vintage. Say so in `evidence` rather than quoting the number bare.</if_mismatch>
  </step>
  <step>
    <run>EXERCISE each subject's failure path -- make it fail and read what it returns</run>
    <expect>an observed return value for `failure_mode.returns_on_failure`</expect>
    <if_mismatch>if you cannot exercise it, `distinguishable_from_true_negative` is `unmeasured` and basis is `absent` WITH evidence of what you tried. Do NOT read the failure mode off a docstring -- Rule 28 q7 says exercise it.</if_mismatch>
  </step>
</phase>
<phase id="2" when="before commit -- CONFORMANCE">
  <step>
    <run>python -c "import json,jsonschema;s=json.load(open('org/standards/SUBSTRATE_CARD.schema.json'));[jsonschema.Draft202012Validator(s).validate(json.load(open(p))) for p in ['&lt;c0&gt;.json','&lt;c1&gt;.json','&lt;c2&gt;.json']];print('3/3 VALID')"</run>
    <expect>3/3 VALID</expect>
    <if_mismatch>fix the card, never the schema. The schema is the FREEZE and amending it is out of your lane (boundary SC-g-4).</if_mismatch>
  </step>
  <step>
    <run>.tools/commit-gate.sh on any .py you touched</run>
    <expect>clean</expect>
    <if_mismatch>fix before commit</if_mismatch>
  </step>
</phase>
<phase id="3" when="after commit">
  <step>
    <run>python .tools/proof-of-spec-check.py &lt;instance&gt;.json CCX-AC1,CCX-AC2,CCX-AC3,CCX-AC4,CCX-AC5,CCX-AC6,CCX-AC7</run>
    <expect>rc=0, VALID, alignment ENFORCE with denominators printed</expect>
    <if_mismatch>do NOT flip status to complete; report the failing criterion to me with its cell_ref</if_mismatch>
  </step>
</phase>
</compiler_tools_mandate>

## 4. ACCEPTANCE CRITERIA — MACHINE-CHECKABLE

| id | criterion | grounding |
|---|---|---|
| **CCX-AC1** | Three JSON cards exist (C0, C1, C2) and **all three VALIDATE** against `SUBSTRATE_CARD.schema.json`. Every one of the 21 rows carries non-empty `basis` + `evidence` + `owner`. | validator output, 3/3 |
| **CCX-AC2** | All three carry **byte-identical** `as_of.commit_ish` and `as_of.graph_vintage`, matching s.1 exactly. | diff of the three `as_of` blocks |
| **CCX-AC3** | **`coverage.denominator` is NON-NULL on all three**, in `"N of M"` form with **both numbers named**. | ⛔ **The schema PERMITS `null` here — I exercised it (finding F-1). Only this criterion catches it.** Rule 28 q5: PRINT THE DENOMINATOR. `1.0.0_SA_CTO~X` 72797 independently names a denominator-free coverage row a correct REWORK. |
| **CCX-AC4** | Any card with `determinism` in {`inferential`,`hybrid`} carries a **populated `inference_detail`** including `failure_is_loud`. | ⛔ **The schema states this requirement in a `description` string with no `if/then` — prose a validator cannot branch on (finding F-2). Only this criterion catches it.** |
| **CCX-AC5** | `verdict.standing` is `INCOMPLETE` **iff** ≥1 row is genuinely unworked. A `SOUND`/`QUALIFIED` verdict over an unworked row fails. | ⛔ **Schema permits the mismatch (finding F-3).** See s.5 for the `absent`-is-not-unworked distinction — getting this backwards is the most likely honest error in this TO. |
| **CCX-AC6** | **ZERO commits by this lane touching any generator it carded** during the wave. | QUALIFY-DO-NOT-FIX. A lane that fixes what it cards has left the project. |
| **CCX-AC7** | Every row with `basis: "measured"` has `evidence` that is a **grounding**: `file:line @ <commit-ish>`, or a command exercised **with its output**. | A line citation without a vintage is not a citation; a docstring is not an exercise. |

## 5. ⛔ THE DISTINCTION MOST LIKELY TO COST YOU A REWORK

**`basis: "absent"` and "unworked" are NOT the same thing, and the schema cannot tell them apart.**

- A row carrying **`absent` WITH evidence explaining why no basis exists has been WORKED** — you measured
  that it is unmeasurable. **That is a complete row and a PASS.**
- A row left **blank, guessed, or unfilled has NOT been worked.** That is the rework.

Same shape one level up: the decomp cell's `status` (did the lane produce this cell) is a **different axis
at a different grain** from the card's `basis` (what standing does this row's answer have). Writing
`basis: absent` **completes** the cell.

## 6. WHAT IS A PASS EVEN THOUGH IT LOOKS LIKE A FAILURE

Per `1.0.0_SA_CTO~X` 72797 — **a card that finds defects is a PASSING card.** The deliverable IS the
finding. These are all PASSES, do not treat any as rework:

- `determinism: "unknown"` with evidence of what you tried. The schema says *never default to
  `deterministic` because it looks that way.* **The failure is a confident `deterministic` with no
  exercise behind it.**
- `UNOWNED` on a row whose remedy genuinely has no owner. **Legal and loud. A GUESSED owner is worse than
  none** — that is a rework.
- **Empty arrays are claims, not gaps.** `composes: []` asserts it composes nothing. A missing key is a gap;
  an empty array is an answer.
- `failure_mode.distinguishable_from_true_negative: "no"` — **the single most valuable thing this project
  can surface.** A clean zero identical to a genuine negative. Report it loudly; it is the card working.
- A card whose verdict is `UNSOUND` because the subject is genuinely unsound. **A SOUND card about an
  UNSOUND subject** — two different objects, and the schema keeps them apart on purpose.

## 7. CROSS-DOMAIN COORDINATION

<cross_domain_coordination>
- **`0.8.0_AE_CloudComp~Y`** holds D1/D2/D3. **D2 is defined against C2's motifs** (*"adds DIRECTION +
  TRANSFORM + TIME to C2 motifs; does not re-implement motif membership"*). **Your C2 card is an INPUT to
  their D2 card.** MCP them your `SC-c-1` finding when it lands; do not wait on them and do not
  card D2 yourself.
- **`0.7.0_AE_CloudOps~X`** holds C3.i-as-built + `comp-similar`. **C3.i consumes C2's classes** (19 class
  nodes). Coordinate before either of you claims a class-count figure, so two cards do not carry two numbers.
- **`0.4.0_DT_ClientPlatform~X`** builds the graph-object manifest FROM your `location.projection_of`
  arrays. **Populate `projection_of` carefully — it is not decoration, it is their input.** A projection
  that cannot name its source cannot be checked for lag, and lag is invisible from inside the projection.
- **SHARED FILE WARNING:** the `kimi_subdivision_harness/` composers sit under `3.0.0_SA_CVO`'s deliverables
  tree. **Read-only for you.** If a card needs a change there, that is a finding with an owner, not an edit.
</cross_domain_coordination>

## 8. DELIVERABLES

1. Three cards. Suggested home: `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/{C0,C1,C2}.json`.
2. The proof-of-spec instance at the `<instance_path>` above.
3. A session log with a **mandatory `## Compiler Tools` section** — every `<run>` above, its observed
   result, and pass/fail vs `<expect>`. **Blank and "N/A" are not acceptable**; one sentence why, if a tool
   genuinely did not apply.
4. **Route to `3.0.0_SA_CVO~X`** (proof-of-spec verifier for this cohort) when you flip toward complete,
   and **cc me**. CVO~X is a verification lane, **not an approval gate** — nothing waits on them beyond
   what this TO's own contract names.

## 9. SURPRISE CHANNEL

Mid-round the spec is **FROZEN**. Your only legal off-spec act is to **SURFACE**: one line by MCP to
`3.0.0_SA_CVO`, cc me. **OBSERVATION never interrupts — one line, keep working.** **BLOCKING routes
same-turn to me as issuer** for spec amendment. Any **ARMED** item disarms same-turn via a named owner.

⛔ **A finding about a subject you are carding is NOT a surprise — it is the deliverable.** Put it in the
card. The surprise channel is for things outside the eight wave-1 subjects.

⛔ **AND DO NOT RABBIT-HOLE.** If you find something odd that is not your task: one line to CVO, keep
working. That is the single biggest avoidable drag on this fabric and this channel exists to prevent it.
