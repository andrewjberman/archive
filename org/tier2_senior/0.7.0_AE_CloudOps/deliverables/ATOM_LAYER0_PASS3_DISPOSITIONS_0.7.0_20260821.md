# Pass-3 CODE_REDECLARATION dispositions -- 0.7.0_AE_CloudOps pod (4 rows)

**Requested by:** `4.0.0_SA_CRO` routing packet 64077 (2026-08-21T012443Z) -- characterize-not-fix, no clock.
**Assessment pin:** `f36d572be8` (CRO's `assessment_commit` = `f36d572be864e56b9175caac06b01f62fc141e2a`).
**Source read at BLOBS, not HEAD** -- `comp_aws_cli.py` @ `57788c66dc18e244ede9d9cd841f4a333cdddada`,
`comp_blast_universe.py` @ `f5b713af6d5aeda6d42a866c26fb35d21fab8fed`, both taken from CRO's own
receipts, so every line citation below carries its vintage (a `file:line` alone resolves at every
vintage, to different code).
**Fence honored:** `resolves_via` authoring is a separately gated act and is NOT bundled here. Nothing
in this deliverable adds, renames, re-homes or promotes a vocabulary value; no code was edited.

---

## THE HEADLINE, BEFORE THE ROWS

CRO's packet frames all four rows as one shape: *"the code location carries ontology vocabulary
WITHOUT a resolved authority binding -- a future two-homes risk that compounds at the next engine
edit (the R8 class)."* **That frame is true of every row and it is not the same defect in each.**
Measured, the four rows span **three distinct states that take three different remedies**:

| state | what it is | remedy | rows |
|---|---|---|---|
| **REDECLARATION** | code restates vocabulary an authority DOES carry | cite the authority home | P3R004, and the majority of P3R001/P3R002 |
| **UNGOVERNED** | code declares vocabulary NO authority carries | promote it, or declare it out-of-scope | the residual of P3R001/P3R002, half of P3R003 |
| **ALREADY-DIVERGED** | two code homes carry the same concept with DIFFERENT members | adjudicate which is canonical | P3R003 |

**A citation cannot be written for a token that has nothing to cite** -- so CITE-THE-AUTHORITY is
structurally unavailable for the UNGOVERNED members, and those rows cannot take one disposition value
honestly. That is a Rule-24 postulate (iv) state-coherence observation on the row cut, surfaced for
CRO to adjudicate as schema owner; **I am not re-cutting CRO's rows**, only reporting that one remedy
does not move all their members.

---

## P3R001 -- `concrete_graph_edge_vocabulary` (`comp_aws_cli.py`) -- **CITE-THE-AUTHORITY**, with a declared residual

**Method + denominator.** AST over the pinned blob. Edges in this file are emitted via a helper as the
**third POSITIONAL argument** -- `E(src, tgt, "ENCRYPTS_WITH")` at `:1377` -- not an `edge_type=`
kwarg. *(Stated because my first extractor keyed on the kwarg form and returned **0 against an
expected ~80**. Zero on a known-nonzero population is a retrieval failure, not an absence; the
implausible denominator is the only thing that caught it.)*

```
29 distinct edge types emitted  |  23 governed by RULE_BANK  |  6 UNGOVERNED
UNGOVERNED: FORWARDS_TO, IN_SUBNET, ON_LB, STARTS, TARGETS, USES_CERT
```

Checked against ALL THREE readable authority files (`NFRA_ONTOLOGY_RULE_BANK.yaml`,
`canon-patterns.yaml`, `SYSTEM_DEFINITIONS.yaml`) -- all six absent from every one, each file named
and read rather than assumed. Controls: bogus token `False` in all three; positive `WRITES_S3` `True`.

**DISPOSITION: CITE-THE-AUTHORITY** for the 23 governed types -- a module-level comment naming
`NFRA_ONTOLOGY_RULE_BANK.yaml` as the machine-authority, no vocabulary change. The rule bank already
declares itself *"THE single machine-authority ... never consume a copy"* (`:86`), so the citation
records an existing relationship rather than creating one.

**DECLARED RESIDUAL (needs its own row, not this disposition):** the 6 ungoverned types are the
opposite defect and take the opposite remedy. They are not redeclarations of anything.

## P3R002 -- `concrete_graph_node_type_vocabulary` (`comp_aws_cli.py`) -- **CITE-THE-AUTHORITY**, two homes, declared residual

Node types are dict literals -- `{"id": name, "type": "S3_BUCKET"}` at `:250` -- not a kwarg either.

```
37 node types emitted | 28 governed by RULE_BANK | +2 governed by canon-patterns.yaml | 7 UNGOVERNED
ADAPTER-ONLY: EC2_INSTANCE, ECS_TASK_DEFINITION
UNGOVERNED:   ACTIVITY, CODEBUILD_PROJECT, ECS_CLUSTER, EXTERNAL_ENDPOINT,
              EXTERNAL_PRINCIPAL, LB_LISTENER, TARGET_GROUP
```

**DISPOSITION: CITE-THE-AUTHORITY** for the 30 governed -- **and the citation must name TWO homes**,
because the authority for this axis is split: `RULE_BANK.node_bindings` (`:219-240`) carries 28, and
`canon-patterns.yaml` carries 2 more. A citation naming only the rule bank would be *incomplete in a
way that reads complete*. That is worth knowing independently of this row.

*(`SYSTEM_DEFINITIONS.yaml` does not carry even `S3_BUCKET` -- it is not a vocabulary authority on
this axis at all. Verified rather than assumed; I had been treating the three files as peers.)*

**DECLARED RESIDUAL:** the 7 ungoverned, same reasoning as P3R001.

## P3R003 -- `producer_edge_type_set` (`comp_blast_universe.py:453`) -- **OWNER-ADJUDICATES**

**This row is not a FUTURE two-homes risk. The second home already exists and the two homes already
DISAGREE.** Set difference computed, not eyeballed:

```
comp_blast_universe.py:453     PRODUCER_EDGE_TYPES   8 members
cli.py:647                     _WRITE_VERBS          6 members
comp-output-contracts.yaml:362 predicate             8 members  (byte-equal to the :453 set)

PRODUCER_EDGE_TYPES MINUS _WRITE_VERBS = {WRITES, PROJECTS_TO}   <- the divergence
_WRITE_VERBS MINUS PRODUCER_EDGE_TYPES = {}                       (a proper subset)
```

Both declarations carry near-identical intent comments (`:451` *"written down here, once, rather than
inferred"*; `cli.py:645` *"Kept explicit rather than inferred"*). **Two authors independently reaching
for the same discipline and landing different sets** is the R8 mechanism exactly -- and note that the
discipline itself worked: both wrote it down. What neither could do was see the other.

**Why it is consequential rather than cosmetic.** `_WRITE_VERBS` has exactly one consumer,
`cli.py:704`, and per its own comment block (`:640-643`) that is the classifier separating *"two
producers WRITING one artifact is a single-writer conflict"* from *"two scripts CALLING one helper is
ordinary reuse."* **So a shared artifact whose producing edge is plain `WRITES` falls to the
ORDINARY-REUSE side of a single-writer-conflict detector** -- `WRITES` being the most literally named
producer verb in the vocabulary. I have NOT exercised that path and do not claim a live miss; the
measured facts are that the two sets disagree and that the smaller one gates a conflict detector.

**Second finding on the same row -- the set is ALSO split on governance:**

```
governed by RULE_BANK: WRITES, WRITES_S3, PROJECTS_TO, TRIGGERS
UNGOVERNED anywhere:   SFN_INVOKES, S3_INVOKES, EVENT_INVOKES, SNS_INVOKES
```

Those four are **real, emitted edge types** -- `extract_sfn.py:153` emits `edge_type="SFN_INVOKES"`,
`extract_event_invoke.py:20` mirrors the pattern -- they simply have no authority home. The rule bank
carries generic `INVOKES` (`triggers.binds_up`) but none of the four service-specific forms.

**DISPOSITION: OWNER-ADJUDICATES.** Two independent reasons, either sufficient: (1) half the members
have nothing to cite, so a citation is unwritable for them; (2) which of the two divergent sets is
canonical is a naming call with a live consumer behind it, and it is not mine to make.
**Lane note:** this is a `~A` row and I am base -- OWNER-ADJUDICATES is the honest hand-back
regardless of seat, so no lane context was assumed on anyone's behalf.

## P3R004 -- `function_grain_node_type_set` (`comp_blast_universe.py:462`) -- **CITE-THE-AUTHORITY**

```
FUNCTION_GRAIN_TYPES = ("PipelineFunction", "Hook", "DataFetch")  3 members, 3 governed, 0 ungoverned
RULE_BANK :219-240 node_bindings -- PipelineFunction -> Transformer ; Hook, DataFetch -> Consumer
```

The cleanest row of the four: a pure redeclaration of governed vocabulary, every member present and
correctly bound. A comment citing the `node_bindings` home closes it with no vocabulary change.

**Lane note:** `~A` row, dispositioned from base because it resolves completely from source at the pin
and needed no lane context. P3R003 did need it, and is handed back accordingly.

---

## RESIDUAL / NOT DONE -- stated so nothing here reads as more closed than it is

- **No code edited, no comment landed.** These are dispositions. The citation edits for P3R001/P3R002
  are a separate act and sit in the same engine-touch as my banked comp-estate findings (63908, 63961).
- **The UNGOVERNED populations (6 edges + 7 nodes + 4 producer verbs) have no row.** They surfaced from
  characterizing CRO's rows and are reported, not filed -- filing is the registry executor's act.
- **`cli.py:704` behavior is UNEXERCISED.** The divergence is measured at source; whether it produces a
  missed conflict on live graph data is untested, and I have not claimed it does.
- **Governance was tested by word-boundary token presence**, which answers *"does an authority mention
  this token"* -- not *"is it bound on the right axis."* A token could appear in an authority file in
  an unrelated role and read as governed here. The positive/negative controls bound the instrument's
  discrimination, not its semantics.
