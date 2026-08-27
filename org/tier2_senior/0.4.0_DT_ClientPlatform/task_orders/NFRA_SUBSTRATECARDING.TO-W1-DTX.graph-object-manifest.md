<task_order>
<id>NFRA_SUBSTRATECARDING.TO-W1-DTX.graph-object-manifest</id>
<project>NFRA_SUBSTRATECARDING</project>
<issued_to>0.4.0_DT_ClientPlatform~X</issued_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<executor_class>0.4.0_DT_ClientPlatform (~lane instance; SINGLE-PROJECT -- this instance holds NFRA_SUBSTRATECARDING and nothing else)</executor_class>
<status>complete -- SC-m-3 COMPLETE, both phases. Phase A 39 parts @e0eff1d908+@6e9ee3b28b; phase B reconcile @b97814abfb on the OBSERVED trigger (8/8 cards committed, measured). All 6 criteria PASS, dispositions asserted in code to sum to 42. VERIFIED PASS by 3.0.0_SA_CVO~X (phase A @26b4d6cea3). ACCEPTED by issuer 2.0.0_SA_COO~X 73479.</status>
<priority>P1 -- D11 wave 1. Andrew named this deliverable directly and called its absence "very concerning".</priority>
<date>2026-08-26</date>
<placement>LAPTOP (declared decomp axis; no cross-fabric edge, no ferry semantics)</placement>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/nfra-substratecarding/20260826T172918Z/DECOMP.md @aae317509b</ref>
  <ref type="prd">docs/architecture/D11_SUBSTRATE_ANALYSIS_PRD.md @944ca89492 -- the STANDING DELIVERABLE section</ref>
  <ref type="contract">org/standards/SUBSTRATE_CARD.schema.json @944ca89492 -- artifact.location.projection_of is your INPUT</ref>
  <ref type="law">CLAUDE.md Rule 24 -- TAXONOMY LAW (binds the manifest's classification axis) · Rule 28</ref>
</references>
<objective>
Produce THE GRAPH-OBJECT MANIFEST: a machine-readable JSON enumerating what graph
stores exist, where each lives, which are heavy/authoritative vs light/traversable
projections, and each TAGGED TO ITS GENERATOR -- assembled from the projection_of
lineage every wave-1 card carries. QUALIFY ONLY: name defects and owners; fix nothing.
</objective>
</task_order>

# TASK ORDER — NFRA_SUBSTRATECARDING.TO-W1-DTX · THE GRAPH-OBJECT MANIFEST

**to:** `0.4.0_DT_ClientPlatform~X` · **issuer:** `2.0.0_SA_COO~X` · **cut:** 2026-08-26 ~18:1xZ

✅ **DECOMP CERTIFIED — PASS.** `3.0.0_SA_CVO~X`, `workflows/atom_decomposition/runs/nfra-substratecarding/20260826T172918Z/CERT_20260826T1836Z_3.0.0_SA_CVO~X_ATTEMPT1.md` @`5b390a5662`. Sealed mutant FOUND (`SC-f-4.executor_class`) with three independent discriminators; seal opened and matched on all four fields. ⚠ **A cert is a FLOOR, not a laundering** — the decomp still carries `SC-m-1` PARTIAL (the reduced freeze) and two P2 findings on its face. Nothing in this TO changes.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding/20260826T172918Z/DECOMP.md @aae317509b
Cell discharged (PROJECT_MECHANISM, grain = project): SC-m-3
Reads-from (not owned by this TO -- the other lanes produce them): SC-a-4, SC-b-4, SC-c-4, SC-d-4,
SC-e-4, SC-f-4, SC-g-4, SC-h-4
Contributed-to: SC-m-5
</decomp_ref>

<proof_of_spec>
  <!-- python .tools/proof-of-spec-check.py <instance>.json DTX-AC1,DTX-AC2,DTX-AC3,DTX-AC4,DTX-AC5,DTX-AC6 ; check rc -->
  <criterion id="DTX-AC1" cell_refs="SC-m-3"/>
  <criterion id="DTX-AC2" cell_refs="SC-m-3"/>
  <criterion id="DTX-AC3" cell_refs="SC-m-3"/>
  <criterion id="DTX-AC4" cell_refs="SC-m-3, SC-a-4, SC-b-4, SC-c-4, SC-d-4, SC-e-4, SC-f-4, SC-g-4, SC-h-4"/>
  <criterion id="DTX-AC5" cell_refs="SC-m-5"/>
  <criterion id="DTX-AC6" cell_refs="SC-m-3"/>
  <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/NFRA_SUBSTRATECARDING.TO-W1-DTX_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>DTX-AC1,DTX-AC2,DTX-AC3,DTX-AC4,DTX-AC5,DTX-AC6</expected_criteria>
  <alignment_denominators>
criteria: 6. Cells OWNED: 1 (SC-m-3). Cells READ (produced by other lanes, cited so the reconcile is
traceable): 8 location cells, one per wave-1 subject. Contributed-to: SC-m-5.
CELL -> CRITERION: SC-m-3 covered by 5 criteria; the 8 read-cells covered by AC4. Unmapped: 0.
CRITERION -> CELL: all 6 carry >=1 cell_ref. Untraceable: 0.
  </alignment_denominators>
</proof_of_spec>

---

## 1. THE AUTHORITY — ANDREW, VERBATIM

> *"something that is very concerning to me is not having a clear manifest of 'what' graph objects exist and
> where involved in this process … all of that needs to be pinned down as well in a manifest json deliverable
> that we build out and tag to the relevant generators."*

**His mental model — Nessie/Iceberg heavy and authoritative, kuzu light and traversable — is right and
INCOMPLETE.** The manifest's job is to make the complete picture legible, including the stores that fit
neither half of that split.

## 2. ⛔ THE SHAPE OF THIS TO: TWO PHASES, AND PHASE A STARTS NOW

**This TO is NOT blocked on the other lanes.** It has a dependency, and the dependency is on ONE of its two
phases only.

| phase | what | when |
|---|---|---|
| **A — CENSUS** | Independently enumerate the graph stores that exist: where each lives, what writes it, what reads it. | **NOW. Nothing gates it.** |
| **B — RECONCILE** | Join phase A against every wave-1 card's `artifact.location.projection_of`, and close the gap in **both directions**. | **Observed trigger: the LAST wave-1 card MERGED.** Not a date, not "when the lanes finish." |

⛔ **PHASE A IS NOT A WAIT — IT IS THE INDEPENDENT INSTRUMENT.** If the manifest were assembled only from
what the cards happen to name, **it could never discover a store no card mentions** — and a store nobody
names is exactly the thing Andrew called concerning. **Phase A is what makes the reconcile a MEASUREMENT
rather than a transcription.**

## 3. THE STARTING LIST — AND IT IS EXPLICITLY *NOT* A CENSUS

`1.0.0_SA_CTO~X` supplied these as stores they **tripped over**, stated openly as a starting list and not a
complete enumeration:

```
Iceberg/Nessie   graph_nodes (27,061) · graph_edges (60,858) · resource_summaries · cse_*
kuzu_nessie_db   the canonical projection -- LAGGED 20,800 vs 27,061 when measured
.comp-graph/graph.json                     2,249 nodes, 19.7d stale, feeds nerves_resolve
nerves-edges.json / nerves-risk-edges.json 1,832 danger nodes, feeds comp-pulse
estate-coverage-resolver.json
motif_c2c3_materialize{,_ab}.json          baked July class specs
s3://opal-estate-report/ kuzu_nessie_db    a SECOND 51MB kuzu db, 2026-08-06
c2_instances.json / c3_structures.json     UNTRACKED composer outputs in the harness dir
```

⛔ **TREAT EVERY ROW AS A PRIOR UNDER TEST, INCLUDING THE COUNTS.** Those figures are `held` at CTO~X's
vintage. **My own wave pin reads the kuzu projection at 27,035 nodes / 58,224 edges** — different numbers
from the same store, because a different plane at a different moment. **Two readings, neither wrong.** Your
manifest must record **which plane and which vintage** each figure came from, or it will read as a
contradiction to the next person.

⛔ **A STARTING LIST THAT GOES UNCHALLENGED BECOMES A CENSUS BY DEFAULT.** The single most valuable thing
this TO can produce is **a store that is on nobody's list.** Hunt deliberately.

## 4. ⛔ THE CLASSIFICATION AXIS IS A SCHEMA-ENUMERATION ACT — RULE 24 BINDS YOU

The manifest must say which stores are **heavy/authoritative** and which are **light/traversable
projections**. **That is minting a classification axis, and CLAUDE.md Rule 24 binds every such act —
including adopting one authored elsewhere.**

**Your manifest ships WITH its four-postulate record** or it is not a conforming deliverable:

| postulate | what you must state |
|---|---|
| **(i) MECE** | Values mutually exclusive AND collectively exhaustive **over the declared domain — name the domain, then hunt the uncovered member.** ⚠ Andrew's two-value split (heavy/light) is a starting point, not a proven partition: **an untracked JSON in a harness dir is neither, and a SECOND copy of a kuzu db in S3 tests it hard.** |
| **(ii) SAME GRAIN** | Every value at one grain. A *table* and a *file on disk* and an *S3 prefix* may not be the same grain — if they are not, say so and split the axis. |
| **(iii) INTENT COHERENCE** | One axis, one intent. ⚠ **"authoritative vs projection" (standing) and "heavy vs light" (weight/traversability) are TWO INTENTS** and Andrew's phrasing bundles them. A store can be light AND authoritative. **If they do not co-vary, that is a two-field split, not one axis.** |
| **(iv) STATE COHERENCE** | Ask whether ONE remedy moves every value together. **If building the obvious instrument delivers some values and structurally cannot deliver others, NAME WHICH VALUES DO NOT MOVE.** |

**The card schema's own `authority_role` enum (`source`/`projection`/`evidence`/`reference`/`none`) already
exists and already carries a Rule-24 record.** ⛔ **Check it before minting anything new** — the build ladder
says an existing ratified term beats a re-coined one, and a vocabulary re-coined beside a ratified term is
the same duplicate one layer up. **Reusing it, and saying you reused it, is a better outcome than a new axis.**

## 5. COMPILER TOOLS MANDATE

<compiler_tools_mandate>
<phase id="0" when="PHASE A -- before the manifest is written">
  <step>
    <run>comp-which "what graph stores exist and what writes each one"</run>
    <expect>routes to comp-estate/comp-kuzu/comp-blast, or runs comp-find on rails</expect>
    <if_mismatch>widen DELIBERATELY (HEAD -> DEF -> --all; `-i` for ANY census -- this estate CAPITALISES its load-bearing words and a case-sensitive sweep drops precisely the rulings)</if_mismatch>
  </step>
  <step>
    <run>comp-estate --layers  +  comp-blast on each named generator</run>
    <expect>generator -> store edges, and the readers on the other side</expect>
    <if_mismatch>a store with no discoverable generator IS A FINDING -- record it as generator UNKNOWN with evidence of the search, never omit the row</if_mismatch>
  </step>
  <step>
    <run>comp-kuzu provenance header on every kuzu read</run>
    <expect>snapshot ids + built-time + per-table vintage</expect>
    <if_mismatch>UNKNOWN VINTAGE = freshness unverifiable; a scratch DB (--db-path) is a FROZEN vintage. Record the vintage beside every count.</if_mismatch>
  </step>
</phase>
<phase id="1" when="PHASE B -- on the observed trigger (last wave-1 card merged)">
  <step>
    <run>join every card's artifact.location.projection_of + co_resident_stores against the phase-A census</run>
    <expect>BOTH denominators printed: stores-in-cards-not-in-census, and census-stores-no-card-names</expect>
    <if_mismatch>⛔ a one-directional reconcile is not a reconcile. BOTH residues are findings and BOTH get owners.</if_mismatch>
  </step>
</phase>
<phase id="2" when="before commit">
  <step>
    <run>python -c "import json;d=json.load(open('&lt;manifest&gt;.json'));print(len(d['stores']),'stores')" ; plus your own schema/self-test if you author one</run>
    <expect>parses; counts match the reconcile table</expect>
    <if_mismatch>fix before commit</if_mismatch>
  </step>
  <step>
    <run>.tools/commit-gate.sh on any .py you touched</run>
    <expect>clean</expect>
    <if_mismatch>fix before commit</if_mismatch>
  </step>
</phase>
<phase id="3" when="after commit">
  <step>
    <run>python .tools/proof-of-spec-check.py &lt;instance&gt;.json DTX-AC1,DTX-AC2,DTX-AC3,DTX-AC4,DTX-AC5,DTX-AC6</run>
    <expect>rc=0, VALID, alignment ENFORCE with denominators printed</expect>
    <if_mismatch>do NOT flip to complete; report the failing criterion with its cell_ref</if_mismatch>
  </step>
</phase>
</compiler_tools_mandate>

## 6. ACCEPTANCE CRITERIA

| id | criterion | grounding |
|---|---|---|
| **DTX-AC1** | A machine-readable manifest JSON exists. **Every store carries: exact location, form, what WRITES it, what READS it, and its vintage-at-observation with the plane named.** | the file, parsed |
| **DTX-AC2** | **Every store is TAGGED TO ITS GENERATOR** — Andrew's explicit words. A store whose generator could not be found is recorded **`generator: UNKNOWN` with evidence of the search**, never omitted. | ⛔ **An omitted row and an unowned row are opposite facts that look identical in a manifest.** |
| **DTX-AC3** | The classification axis ships **WITH its Rule 24 four-postulate record** (i–iv), and states whether it REUSES the card schema's `authority_role` or mints new values — with the reason. | CLAUDE.md Rule 24. **Adoption is an authoring act.** |
| **DTX-AC4** | **The reconcile prints BOTH denominators**: stores named in cards but absent from the census, and census stores no card names. **Both residues carry owners.** | ⛔ **A residual bucket is a claim, not a remainder.** "Total minus the part I measured" is not a measurement of the label you give it — itemise until the parts sum, or call it UNATTRIBUTED. |
| **DTX-AC5** | **ZERO commits by this lane touching any store or generator it manifests.** | QUALIFY-DO-NOT-FIX. A lane that fixes what it catalogues has left the project. |
| **DTX-AC6** | The manifest **states its own coverage and its own limits** — what universe it swept, what it could not reach, and that the CTO~X starting list was a starting list. | **A manifest that does not state its own coverage becomes a census by default the moment someone cites it.** |

## 7. CROSS-DOMAIN COORDINATION

<cross_domain_coordination>
- **All four card lanes feed this TO.** `0.8.0_AE_CloudComp~X` (C0/C1/C2), `0.8.0_AE_CloudComp~Y` (D1/D2/D3),
  `0.7.0_AE_CloudOps~X` (C3.i + `comp-similar`). Their `location.projection_of` arrays are your phase-B input.
  **Do not chase them for it** — the trigger is the merge, and phase A does not wait.
- ⚠ **`0.7.0_AE_CloudOps~X`'s subjects touch `resource_summaries` and the kuzu corpus directly** — the two
  stores most likely to appear in both their card and your manifest. **Coordinate before either publishes a
  row count**, so one measures and the other cites with attribution.
- ⛔ **`org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/` holds the UNTRACKED composer
  outputs** (`c2_instances.json`, `c3_structures.json`) — that tree is **READ-ONLY** for you; it belongs to
  CVO. An untracked output IS a manifest row and IS a finding; it is not yours to track or move.
- **No shared write path with any other lane.** Your deliverable is a new file in your own tree.
</cross_domain_coordination>

## 8. DELIVERABLES

1. `graph_object_manifest.json` — suggested home
   `org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/graph_object_manifest.json`.
2. The Rule 24 four-postulate record for the classification axis (in the manifest or beside it).
3. The proof-of-spec instance at the `<instance_path>` above.
4. A session log with a **mandatory `## Compiler Tools` section** — every `<run>`, observed result, pass/fail
   vs `<expect>`. **Blank and "N/A" are not acceptable.**
5. **Route to `3.0.0_SA_CVO~X`** at the completion flip, cc me. **Verification lane, not an approval gate.**

⛔ **PHASE A IS REPORTABLE ON ITS OWN.** Send me the census when it is done rather than holding everything to
the phase-B trigger. **Status is CELL-level** — a partially complete `SC-m-3` must be expressible, or the
record lies to the next seat in whichever direction it happens to lag.

## 9. SURPRISE CHANNEL

Spec is **FROZEN** mid-round. Only legal off-spec act is to **SURFACE**: one line by MCP to `3.0.0_SA_CVO`,
cc me. **OBSERVATION never interrupts — one line, keep working.** **BLOCKING routes same-turn to me.**

⛔ **A store you did not expect to find is NOT a surprise — it is the deliverable.** Put it in the manifest.
