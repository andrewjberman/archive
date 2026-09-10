# CG-s-36 -- THE `STORED_IN` RETIREMENT AS ITS OWN CELL: THE DECISION, AND WHAT FORCED IT

**TO:** `NFRA_CLDGRPH.TO-CG-H-1` | **cell:** CG-s-36 (decomp v0.11 s.1a) | **worker:**
`0.9.0_WK_NFRA_CLDGRPH~1` | **worktree:** `C:/tmp/wk-cldgrph-8-1` | **branch:** `wk-cldgrph-8-1`
| **HEAD at measurement:** `3f99d48f49` | **push state:** LOCAL.

---

## THE ANSWER, FIRST

**`STORED_IN` IS NOT RETIRED. `BRANCH=NOT_RETIRED`, and that is a decision, not a silence.**

The order made both branches passes and asked for a decision a reader can check. Three
independent measurements force this one, and **each would force it alone**:

1. **The reader set is NON-EMPTY** -- 15 consumer files over a 29,973-file repository
   denominator, after every named subtraction. The order's own rule: NON-EMPTY => DO NOT RETIRE.
2. **2 of those 15 lie OUTSIDE this order's `<paths>`**, in the sibling slot's folder that slot
   is working in right now. A RETIRE branch would have been **half-landed by construction** --
   the single forbidden outcome -- and a worker never widens its own grant. (Row W1-S46.)
3. **Condition 2 is blocked, and worse than round 7 recorded.** The retirement *as ruled* is a
   **re-point** onto `OWNED_BY`, and a re-point breaks a control that landed in this worktree one
   commit ago. (Row W1-S47.)

**The third is the finding this cell adds**, so it is stated plainly before the evidence:
`derive_stitch.py` drops every `STORED_IN` arriving in the archived snapshot **unconditionally**,
and the licence for that is written in its own comment -- *"STORED_IN is this producer's OWN edge
type (nothing else in the estate writes one), so a STORED_IN arriving in the snapshot is by
construction a previous cycle's output"*. **The unconditional drop is sound only because the type
is sole-written.** `OWNED_BY` is not sole-written. Re-point the emit and the fold starts deleting
other producers' live edges every cycle, silently.

---

## 1. THE TWO CENSUSES, THEIR DENOMINATORS, AND THEIR TREE

`timeout 120 python .../h1_reader_census.py` -> rc 0. Capture: `h1_ac1_output.txt`.

| | value | what it is |
|---|---|---|
| `TREE_READ` | **WORKTREE** | `C:/tmp/wk-cldgrph-8-1`, git dir `.git/worktrees/wk-cldgrph-8-1` |
| `TREE_POSITIVE_CONTROL` | **FIRED** | `h1_tree_control.marker` exists only on this branch and **both** instruments found it |
| `REPOSITORY_DENOMINATOR` | **29,973 file(s)** | 31,425 tracked + 37 untracked-not-ignored, minus a 1,489-file named floor |
| `MANIFEST_DENOMINATOR` | **78 tool(s)** | `graph-call-manifest.yaml` `tools_index`; 128 entries; **78 of 78 resolved to a file, 0 unresolved** |
| `REPOSITORY_CONSUMERS` | **15** | 13 in-grant, **2 out-of-grant** |
| `MANIFEST_CONSUMERS` | **0** | over the resolved 78 |
| `DOMAIN_DELTA` | **15** | |
| `CLASSIFIER_CONTROL` | **4 of 4** | READ / WRITE / FIXTURE / PROSE, one planted line each |

**THE TREE CLAUSE, AND WHY IT STILL EARNED ITS COST AFTER THE FIX LANDED.** The hazard was that
`comp-find` invoked from a linked worktree scanned the **main** tree and returned a well-formed
zero with a real denominator, with nothing in the output naming the tree. The fix is present here
-- `.tools/_comprail.py` resolves `cwd=os.getcwd()` under a docstring naming the worktree case --
and the issuer's face records that it first tested this with `merge-base --is-ancestor` and got a
correct NO to a question nobody asked, because the fix reached `CLOUD` under a different hash
(row S115). The control is kept anyway, and it is not ceremonial: **the fix is a property of the
checkout you are standing in, and the worker is the only one who can see that from where it
stands.** Both instruments were required to find the marker -- the native `git` enumeration *and*
the comp-rail -- so the rail's corpus root is measured rather than assumed. It cost one file.

**WHAT THE DENOMINATOR EXCLUDES, tested per segment rather than asserted.** A shared verdict over
the whole floor would certify each segment by the other segment's argument, so each was measured:

- `__pycache__/` -- 1,464 files, **0 of them carry the literal**. (A `.pyc` embeds its module's
  string constants, so this was a real possibility, and when one does carry the literal it is a
  compiled copy of a `.py` the census already reads.)
- `.scratch/` -- 25 files, **10 carry the literal, all ten named in the capture**, all of them
  this project's own untracked scratch working files (this cell's row-append and instance-build
  helpers, the predecessor's, and some captures). Worker scratch is not a consumer surface.
- gitignored arm -- 32 files, counted and excluded, never entered the union.

**THE SUBTRACTION, written as the printed denominator minus each named exclusion** (Rule 24(i)):
START 94 files carrying a word-boundary `STORED_IN`; MINUS 75 whose every occurrence is PROSE;
MINUS 4 that are this cell's own `h1_*` artifacts; **= 15**. Nothing else is subtracted -- **in particular
no prior round's deliverable and no test**, because for a retirement question a fixture that
constructs the edge IS a consumer of the vocabulary.

> **A NOTE ON 15 vs ROUND 7's 7, so the two are not read as a contradiction.** They are different
> subtractions, both honest. Round 7 additionally dropped prior-round deliverables as "this
> order's own artifacts"; this census drops only prose and its own `h1_*` files. Neither number
> is wrong; what matters is that **each is printed with the subtractions that produced it**. The
> comparison that carries the finding is not 15-vs-7, it is **15-vs-0**.

---

## 2. THE DOMAIN FALSIFIER: THE DECLARED DOMAIN AND THE CLAIM'S POPULATION ARE DISJOINT

`timeout 120 python .../h1_domain_falsifier.py` -> rc 0. Capture: `h1_ac2_output.txt`.

```
CORPUS_FILES_SWEPT=29973
UNSCOPED_DENOMINATOR=94          <- the claim's population: files carrying the term
DOMAIN_HOLDS=0 of 94
MEMBERS_OUTSIDE_DOMAIN=94
SUBTRACTION_VERDICT=VOID
FALSIFIER_CONTROL=FIRED          <- both arms: a held population -> VALID, one member out -> VOID
```

**`DOMAIN_HOLDS=0 of 94` is the strongest form this finding could take.** The declared domain does
not merely *miss some* members of the claim's population -- **it holds none of them.** The
manifest's 78 tools resolve to 101 files, and **not one** of those files is among the 94 that
carry the term. The domain and the population are **disjoint sets**.

> **THE TWO SWEEP DENOMINATORS MOVE BETWEEN RUNS AND THAT IS CORRECT, SO IT IS DISCLOSED RATHER
> THAN SMOOTHED.** Across this cell's runs `REPOSITORY_DENOMINATOR` went 29,963 -> 29,964 ->
> 29,971 -> 29,973 and `UNSCOPED_DENOMINATOR` 88 -> 92 -> 94, for one known reason: **this cell
> was itself adding untracked files to the corpus it was sweeping.** A live-tree census whose
> denominator did *not* move under that condition would be reading a stale or a wrong tree. Every
> graded value was invariant across all runs -- `MANIFEST_CONSUMERS=0`, `REPOSITORY_CONSUMERS=15`,
> `DOMAIN_DELTA=15`, `DOMAIN_HOLDS=0`, `SUBTRACTION_VERDICT=VOID`, `BRANCH=NOT_RETIRED` -- because
> a consumer is decided by content, not by corpus size. The figures quoted here are the FINAL
> capture's, and the instance's numbers are lifted from that capture rather than retyped.

So the census the CTO's condition 1 specified was not a slightly-too-narrow reading of the
retirement question. **It was a census of a different population entirely**, which happened to
return a number that could be read as an answer. Rule 24(i) as amended @`b3bc1d7511` says a
denominator certifies the SWEEP and never the SET, and that the failure mode is a green: *a wrong
domain returning NON-EMPTY gets argued with; returning EMPTY it gets ACTED ON.* Here it returned
empty.

**The falsifier is a separate script from the census on purpose, and the reason is mechanical:
the falsifier must be able to fail while the census succeeds.** Its control exercises the verdict
function on **both** branches inside the run, because a falsifier that has only ever produced the
answer it produced today is a promise rather than a control.

---

## 3. THE BRANCH, AND THE THREE THINGS THAT FORCED IT

`timeout 120 bash .../h1_branch.sh` -> rc 0. Capture: `h1_ac3_output.txt`.

### BLOCKER 1 -- the reader set is non-empty: 15 consumers, each with its line

Named in full in the capture (15 of 15, with line numbers and classification). The production
surfaces among them: `derive_runner.py:2275`
(`STITCH_EDGE_TYPES`, a READ of the vocabulary, read again at `:2543`) and `derive_stitch.py:158`,
`:159` (the drop-on-read, **re-read at HEAD after TO-CG-H-2 changed this file**) and `:255` (the
emit). The remainder are this project's own instruments and fixtures across slots `~1` and `~2`,
plus the `tsgraph_spike` pair.

> The face flagged that `tsgraph_spike` being "inert" was **HELD, not measured** -- W2-S25 declared
> it harmless *for a different question*. That flag did not need to be cashed: the branch is
> NOT_RETIRED on three other grounds, so the pair was read and left. **A population declared safe
> to ignore for one question is not thereby safe for another**, and it is still not measured here.

### BLOCKER 2 -- 2 of the 15 are outside the grant

`~2/g2_card_evidence.py:67,217,221,222` and `~2/g2_shrink_probe.py:45,46,49,93`. The second
**constructs** `STORED_IN` edge triples. Both are round-7 deliverables of slot `~2` -- they did
not exist when the round-7 census the grant was cut from ran. **A grant derived from a census
inherits that census's vintage, and nothing in the grant says so.** Row W1-S46. Not acted on:
widening is the issuer's act, and slot `~2` is live in that folder this round.

### BLOCKER 3 -- condition 2, on a mechanical axis nobody had measured

Round 7 filed the **semantic** half (row W1-S37, still open): widening `OWNED_BY`'s stated intent
to absorb location changes what three readers mean. That objection stands and is re-cited below.
**This cell adds the mechanical half, and it is the one that decides the act.**

CLAUDE.md's NEVER#1 requires counting the **writers** of a named property before signing an act on
it -- *"a property with N writers needs N rules read, and N is a number the half PRINTS."* No such
census existed in this project's record. Measured here, and **it needs no guess about which other
producer writes it**, because it is a subtraction on the served graph:

```
FOLD_OCCURRENCES_OF_OWNED_BY=0     derive_stitch.py + derive_runner.py contain the token
                                   OWNED_BY zero times between them, in ANY form
SERVED_OWNED_BY_S3KEY_EDGES=232    and the served graph carries 232 S3Key -OWNED_BY-> S3_BUCKET
                                   edges anyway, {1: 232}, on the ARN-keyed bucket node
```

**Two independent instruments on two different planes agree on that 232:** CG-s-32's served census
read through the projection service (`CG-s-32...result.md:1506-1508`), and
`cse_emit_graphhead.py:126`, which names *"the 232 S3Key edges"* in production source while
resolving them to `CONTAINS`. **Therefore those edges were written by a producer that is not this
fold, and `OWNED_BY` is not sole-written.**

Now put that against `derive_stitch.py`:

- `:147` `edges.extend(aws["edges"])` -- the fold reads back an **archived snapshot carrying other
  producers' edges**.
- `:155-157` -- the comment: *"STORED_IN is this producer's OWN edge type (nothing else in the
  estate writes one), so a STORED_IN arriving in the snapshot is by construction a previous
  cycle's output"*.
- `:158-159` -- and so it drops **every** `STORED_IN` in that snapshot, **unconditionally**.

**Re-point the emit onto `OWNED_BY` and that licence is false the same night.** The fold would
delete other producers' live `OWNED_BY` edges on every cycle, and the rollup seams the three named
readers traverse are among the casualties. The control being broken is **TO-CG-H-2's own
drop-on-read, merged into this worktree's history at `06ccb217db` while this order was being
cut** -- and **no criterion on either order would have seen it**, because the two orders are
graded separately and the coupling lives between them. Row W1-S47.

### The three containment readers, re-read at HEAD -- `OWNED_BY_CONTAINMENT_READERS=3 of 3 cited`

| file:line | line at HEAD | what it makes `OWNED_BY` mean |
|---|---|---|
| `cse_schema.py:323` | `"OWNED_BY": Relationship.OWNS,` | **OWNS** -- and it sits in the file's own *governance / auth / requires* section |
| `comp_marker_read.py:121` | `_DRILL_FORWARD, _DRILL_REVERSE = ("RUNS", "CONTAINS"), ("OWNED_BY",)` | the **reverse (fine->coarse) rollup** seam |
| `comp_coverage_check.py:523` | `elif et == "OWNED_BY":` | the fine->coarse **`rolls_up` parent**, taken transitively |

All three re-read at HEAD and confirmed at the cited line. **All three are READ ONLY on both
branches and were not touched** -- changing what they mean in order to satisfy the condition that
measures them is the circular act this cell exists to prevent.

**AND A FOURTH, found while measuring and reported rather than absorbed:**
`cse_emit_graphhead.py:125-127` -- *"resolve `OWNED_BY` by the DST node_type -- S3_BUCKET dst =
CONTAINS (container-inverse, the 232 S3Key edges), actor dst = OWNS (custody)"*. This is the
containment objection confirmed on a reader the condition never named, **and it is the same fact
from the other side**: the location fact is already carried, so retiring `STORED_IN` adds nothing
to `OWNED_BY`. Which makes a **delete** arguable and a **re-point** unsafe.

---

## 4. WHAT WOULD UNBLOCK IT -- the part that stops the next seat re-running this census

Four things, in dependency order. The first two are cheap.

1. **A grant cut from a census run AT THE CUT, not from the prior round's row.** 15 files, listed
   with their lines in the capture. An issuer act. Awkward because 2 of them are a sibling slot's
   deliverables, so the cell must own that folder or be cut in a round where `~2` is idle.
2. **A ruling that picks the act: DELETE, not RE-POINT.** The ruling said *retire `STORED_IN` and
   re-point*. The writer census says the re-point is unsafe; a **delete is not**, because the fact
   is already in `OWNED_BY` on 135 of 135 keys (CG-s-32 s.3) and independently as the 232 S3Key
   edges. **These are not the same act and only one is available.**
3. **A replacement re-entrancy discriminator for `derive_stitch.py:158-159`.** Deleting the emit
   deletes the drop's subject, but the *shape* survives: the fold reads back an archived snapshot,
   so any type it sole-writes needs the same treatment and **any type it shares needs a per-cycle
   provenance mark rather than a type test** -- a type test can only ever be as sound as the type's
   writer count. This is the upstream remedy TO-CG-H-2 named and deliberately did not take. It is
   still not one cell with a retirement.
4. **A semantic ruling on what `OWNED_BY` means**, because four readers now depend on it and they
   do not all mean the same thing: `cse_schema` maps it to OWNS (governance), `cse_emit_graphhead`
   maps the **same edge** to CONTAINS when the destination is a bucket, and two rollup seams
   traverse it as containment. **A term that already means two things under one name is not a term
   another term can be folded into.** The third-term option is real -- a distinct `LOCATED_IN` /
   `CONTAINED_BY` would let `STORED_IN` retire into a term that means location and leave OWNS to
   mean custody -- and it is **not this cell's to take**: minting vocabulary is a schema act under
   Rule 24's four postulates with a word-boundary token census, not a worker's retirement cell.

---

## 5. THE MANIFEST AMENDMENT -- W1-S38's own stated remedy, made durable

28 comment lines added to `org/modules/graph/graph-call-manifest.yaml`, **0 removed, 0 added lines
that are not comments**, and the **parsed** manifest is structurally identical to its HEAD blob:

```
contract                      HEAD=3    WORKTREE=3    IDENTICAL
entries                       HEAD=128  WORKTREE=128  IDENTICAL
excluded_not_graph_use_cases  HEAD=17   WORKTREE=17   IDENTICAL
retired_aliases               HEAD=9    WORKTREE=9    IDENTICAL
tools_index                   HEAD=78   WORKTREE=78   IDENTICAL
MANIFEST_ENTRIES_CHANGED=0
```

The comparison is **structural, never a line count**, because a comment added and a route deleted
are both "a line changed"; and the read carries a positive control (the HEAD blob is 208,923
bytes, so a mangled ref returning clean-empty could not pass as "no entries, none lost").

The amendment says, on the manifest itself: this file is a **sound** denominator for *which routed
tool answers question X*, and an **unsound** one for *may this term be retired*; any vocabulary
retirement censused against it **must** also run an unscoped repository sweep, print both
denominators and print the delta; and where the two disagree, **the repository is the denominator
and this file is one input to it**. It lives there rather than in this project's record for one
measured reason: **the next vocabulary retirement in this estate will be censused against this
manifest, by an agent who has not read this project, and it will again read clean.**

---

## 6. THE HOLD

`timeout 120 bash .../h1_no_egress.sh` -> rc 0. Capture: `h1_ac4_output.txt`.

`ECS_RUN_TASK_CALLS=0` | `CODEBUILD_STARTS=0` | `S3_WRITES=0` | `IMAGE_PUSHES=0` |
`TERRAFORM_APPLIES=0` | `MANIFEST_ENTRIES_CHANGED=0` | `EGRESS_PROBE_CONTROL=FIRED` (five planted
positives, one per forbidden family, through the same patterns -- the zeros carry no information
until these fire).

**The detector is inside its own denominator, on purpose.** A verifier scoped to exclude itself
cannot see a call planted in the verifier. So nothing is excluded; instead both the patterns and
the plant are assembled from fragments at run time, so the literal act names never appear as text
in any delivered artifact and the sweep over the detector is a real zero rather than an arranged
one. Nothing was deployed, no producer was run, and the only production files touched are **none**.

---

## 7. WHAT THIS CELL DID NOT DO, stated so it is not read as coverage

- **It did not run the producer.** So the magnitude of any live effect of the re-point hazard is
  **unmeasured**; the shape is certain from the source and the number is not, and no number is
  manufactured here. The egress hold forbids the run that would produce it.
- **It did not touch `cse_schema.py`, `comp_marker_read.py` or `comp_coverage_check.py`** -- read
  only on both branches, always.
- **It did not take the upstream producer remedy** (one prior-cycle filter at the read in
  `derive_runner`/`load_aws_layer`), which sits on this cell's surface and belongs to a different
  act. Named, not taken.
- **It did not re-measure `tsgraph_spike`'s inertness**, which remains HELD.
- **It did not widen its own grant**, and the two out-of-grant consumers are named rather than
  edited.

---

## ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `NFRA_CLDGRPH-W1-S46` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~A`) | a write grant derived from a census inherits that census's vintage, and nothing in the grant says so |
| `NFRA_CLDGRPH-W1-S47` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~A`) | a consolidation and a deletion look like the same retirement from the vocabulary's side and are opposite acts from the producer's |
| `NFRA_CLDGRPH-W1-S48` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~A`) | a write grant that admits a source file but not the artifact that source obliges leaves the worker able to incur a debt and unable to discharge it |

Channel denominator after the append, by re-parsing every fenced block:
**201 blocks, 0 unparseable, 272 rows, W1 max = 48, 0 duplicate ids.**

**ON W1-S48 AND THE `org/modules/graph/` TOUCH, because the drain needs it stated plainly.** The
manifest amendment makes this commit a comp-system `_SOURCE` touch, and the pre-commit
`comp-system-gate` refuses it. Its own text rules out the regenerate-and-stage path for an
`org/modules/graph/` touch (comp-system would have to compile an uncommitted source) and names the
audited override as *"the legal path, not a lapse"* under CTO arch-gate ruling LD-0362. That path
was taken, with the reserved prefix `system-current-override: STRUCTURAL-TWOPHASE/rule-bank`. **The
discharge -- recompiling `infra/system/06_current_state.{md,json}` -- is NOT an act this worker may
perform, because `infra/system/` is not in this order's `<paths>`.** It is owed by whoever drains
this branch, and an undischarged STRUCTURAL override is a discipline event, which is why the row is
ARMED rather than INERT.

---

## THE ONE-SENTENCE VERSION

The manifest census that authorized this retirement did not merely under-count the readers -- **it
was scoped to a domain that holds none of them (0 of 94)** -- and once the readers are counted
against the repository the retirement is blocked three times over, most sharply by a number nobody
had printed: **the surviving term has other writers, and the retiring term's producer depends on
not having any.**
