# CG-s-42 -- THE FOLD'S LICENCE

**Order:** `NFRA_CLDGRPH.TO-CG-I-3.the-folds-licence` · **Worker:** `0.9.0_WK_NFRA_CLDGRPH~2`
**Tree:** `C:/tmp/wk-cldgrph-9-2` (LINKED WORKTREE) · **Branch:** `wk-cldgrph-9-2` · **Base:** `4ff4abd9a4`
**Push state:** LOCAL. Nothing deployed, nothing published, nothing retired.

---

## 0. THE HEADLINE

**THE OTHER WRITER HAS A NAME: `graphuni-storage`.** It declares **169 + 63 = 232** `S3Key
-OWNED_BY-> arn:aws:s3:::<bucket>` edges, and 232 is the exact integer round 8 measured on the
served plane. Two planes, two instruments, one number.

**THE BRANCH TAKEN IS `LICENCE_MOVED`.** `derive_stitch.py`'s prior-cycle drop is no longer
licensed by a comment. It consults `SOLE_WRITTEN_EDGE_TYPES`, it REFUSES and COUNTS a requested
type that is not in it, and the sole-writership claim is now something a run can falsify --
`i3_licence.py` falsifies it on `OWNED_BY` in the same run in which it confirms it on `STORED_IN`.

**THIS CELL DID NOT PERFORM THE RETIREMENT.** Four tells, each of which would go the other way
if it had: the `STORED_IN` emitter is unchanged, `OWNED_BY` appears in `derive_stitch.py` in
comment lines only (4 lines, 0 outside a comment), the licence admits `STORED_IN` and refuses
`OWNED_BY`, and `derive_runner.py` is byte-identical to the pin.

---

## 1. WHO WRITES `OWNED_BY` -- I3-AC1

Round 8 established BY SUBTRACTION that a second writer exists. Subtraction gives existence, not
identity, and the cell was explicit that a remedy resting on an unnamed writer being benign is
the shape it exists to prevent. Three instruments, on three different planes:

| | plane | denominator | what it decided |
|---|---|---|---|
| **A** | rail corpus (`comp-find`) | **30,110 files scanned**, corpus=all, 31 ephemeral-floor and 1,785 binary excluded on its own line | 222 files name the term |
| **B** | git index | **31,868 tracked**, 9,079 scannable, **9,070 read**, 9 excluded above a 4 MB cap | 53 name it, 10 match an emission shape |
| **C** | **live producer payloads** | **6 of 6** objects under `producers/`, the listing stored beside the capture | `OWNED_BY` = **232**, all from `graphuni-storage`; `STORED_IN` = **0** |

Every one of B's ten emission-shaped candidates is classified BY NAME in the run output --
three writers, seven readers/tests/indexes/harnesses. The count is a subtraction from a printed
denominator, not a forward list of what I happened to think of.

### The writer

**`graphuni-storage`** -- the NFRA_GRAPHUNI P1-A storage producer of lane `0.8.0_AE_CloudComp~A`.

- **Payloads (tracked):** `org/projects/NFRA_GRAPHUNI/NFRA_GRAPHUNI.P1-A.storage_producer.json`
  (169 edges, generated 2026-06-30) and `...storage_producer_phaseB.json` (63, 2026-07-01).
- **Served as:** `producers/graphuni/storage_s3keys.json` and `..._phaseB.json` in
  `s3://opal-313476888478-globgrph`.
- **Folded by:** `derive_runner.ingest_graphuni_producers`, called UNCONDITIONALLY on every
  derive (`derive_runner.py:2674`). The flag-gated `EXTRACT_PIPELINE_CLOUD` replacement that
  would skip the graphuni members is default OFF.
- **Its materializer is NOT in the repository.** `org/projects/NFRA_GRAPHUNI/storage_producer.py`
  is UNTRACKED (10,137 B; the CTO's `MATERIALIZER_CENSUS_20260827_REPO_PLANE.md:208`). A
  repository census can name this writer only because its OUTPUT is tracked. Had the payloads
  been untracked too, the honest answer would have been `WRITER=UNIDENTIFIED`, and instrument C
  is what covers that hole.

**A second writer, a different family.** `infra/aws/globgrph/ms_cloud_extract.py` emits
`MsDriveItem -OWNED_BY-> MS_USER` inside `_crawl_drive`. Its edges are NOT the 232. Of the 6,385
served `OWNED_BY` edges round 8 counted, **6,153 are not S3Key-family**; attributing those to
this file is `inferred`, printed as such, and this order does not query the served graph to
convert that into a measurement.

### And it is not assumed benign

The payloads have not been regenerated since **2026-07-01** -- ten weeks -- yet they are re-read
and re-folded every night. `graphuni-storage`'s edges are therefore re-created each cycle from
frozen bytes whose materializer is not in the repository. That is a stated fact about the writer,
not a judgement about whether it is safe, and it is exactly the sort of fact "another producer
probably re-emits it" would have papered over.

**One thing the estate already knew.** `.tools/tool_index.py:4378-4381` carries
`"Producer=graphuni-storage (~A)"` in its edge-type catalogue. The name was in the repository the
whole time. Round 8's census could not see it because that census looked for a WRITER-SHAPED
line and the name lived in a DESCRIPTION -- the same shape as the seating-rule census in Rule 27
that returned zero because the rule lived in an enforcement surface. **An emission-shaped sweep
cannot find a fact recorded as prose, and the fix is not a better regex, it is a second band.**

---

## 2. THE LICENCE STOPS BEING A COMMENT -- I3-AC2

**Before** (at `4ff4abd9a4`, retrieved by content with a control on the retrieval): one line,

```
edges = [e for e in edges if str(e.get("edge_type", "")) != "STORED_IN"]
```

licensed by the comment above it -- *"STORED_IN is this producer's OWN edge type (nothing else in
the estate writes one)"*. Occurrences of any registry token in those bytes: **0**. No value, no
predicate, no field a consumer could reject on.

**After:** the condition is DATA and the drop is a function.

- `SOLE_WRITTEN_EDGE_TYPES: frozenset = frozenset({"STORED_IN"})` -- the licence.
- `SOLE_WRITERSHIP_EVIDENCE` -- one row per member, carrying `claim`, `emitters_in_estate`,
  `emitter`, `instrument`, `vintage`. A value carries its claim in a field a consumer can reject.
- `PRIOR_CYCLE_DROP_REQUEST: tuple = ("STORED_IN",)` -- **deliberately separate from the
  licence.** The request is the caller's intent; the licence is the condition; only their
  INTERSECTION is dropped. A caller cannot talk the fold into an unlicensed delete.
- `drop_prior_cycle_edges(edges, requested, sole_written)` -- pure, returns
  `(kept, dropped, refused)`, and the call site prints a `WARN: PRIOR_CYCLE_DROP_REFUSED` line
  per refused type. **A silent refusal would be a licence that is still a belief.**

**And the falsifier RUNS.** `i3_licence.py` arm 3 executes the sole-writership census on the
registry's member and on a term with several writers **in the same run**: `STORED_IN` holds,
`OWNED_BY` does not. A detector that cannot return False on the positive case is a constant
wearing a measurement's clothes; this one returns both values over a printed denominator
(31,868 tracked / 9,070 read / 9 excluded), with every excluded member named.

**The bound, stated rather than narrowed.** The census is a REPOSITORY sweep. It cannot see a
writer that exists only as deployed bytes -- which is not hypothetical here, since this writer's
own materializer is untracked. And sole-writership is **a fact about today, not a property of
the term**: a new producer falsifies a member without touching `derive_stitch.py`. That is why
the check is re-runnable rather than a one-time sign-off, and why the registry's comment says
adding a type to it is a governed act with a named falsifier.

---

## 3. THE BRANCH, AND WHY -- I3-AC3

**`BRANCH=LICENCE_MOVED`. 6 of 6 arms PASS. `NEGATIVE_CONTROL=FIRED`.**

| arm | what it shows |
|---|---|
| 1 | the licensed type is still dropped -- `STORED_IN` kept 0, dropped 2 |
| 2 | `OWNED_BY` **survives** an explicit drop request, and survives it alongside the licensed type |
| 3 | the refusal is **counted** (`refused={'OWNED_BY': 2}`), never silent |
| 4 | a bystander type is untouched in all four kept-sets |
| 5 | the shipped request reproduces the pin's kept-set **element for element** (object identity) |
| 6 | **negative control** -- the pin's OWN expression re-pointed onto `OWNED_BY` deletes 2 of 2 |

Arm 6 is the load-bearing one. Arm 2 alone proves nothing: a harness that cannot observe a
deletion cannot certify its absence. Arm 6 takes the drop expression **lifted verbatim from the
pin's bytes**, applies ruling 94872's re-point to it, and watches `graphuni-storage`'s edges
disappear. That is the CTO's withdrawn assumption executed rather than argued about.

Arm 5 is the regression bar: the fold's behaviour on `STORED_IN` is unchanged, not
approximately but by object identity of the surviving edges.

**Why this branch, labelled HELD and not measured.** Re-cutting the remedy leaves the
unconditional delete in place for the next type someone wants to retire; moving the licence
makes the property checkable for every type, `STORED_IN` included. That is a judgement. The
alternative branch stays open, and the face was explicit that it does not prefer one.

---

## 4. THE HOLD, AND WHAT WAS NOT DONE -- I3-AC4

Five families at zero over 9 authored files plus 5,869 bytes of diff, with a probe that lights
up all five. **The read-only AWS calls this order DID make are disclosed by name in the output**
(one object listing and six object reads under `producers/`) rather than left for a reader to
discover: the face permits every read of Opal infrastructure and forbids every act whose effect
is a publish. Nothing was published, no task was run, no image act occurred, and there was no
Terraform apply.

`RETIREMENT_PERFORMED=false`, on four tells that are properties of the bytes rather than
assertions about intent. This cell makes the retirement AVAILABLE. Performing it is a later
cut's act on a decision nobody has taken.

---

## 5. ONE ROW FILED -- `NFRA_CLDGRPH-W2-S80`

The withdrawal's hazard is real, and the record's statement of its MECHANISM is incomplete in a
way that points at the file this cell may only read.

`derive_stitch`'s drop runs inside `derive_stitch`'s own artifact. `derive_runner` then folds
that artifact through `STITCH_EDGE_TYPES = frozenset({ROUTES_TO, WRITES, READS, DERIVES_FROM,
STORED_IN})` -- an **allow-list of five**, and `OWNED_BY` is not in it -- while ingesting
`graphuni-storage`'s payloads separately and unconditionally. **So a re-point of the EMIT alone
never reaches graphuni's edges. The deletion becomes reachable only once `OWNED_BY` is ALSO
added to that allow-list, and then it bites exactly as the withdrawal says.**

The conclusion is unchanged and the withdrawal was correct. What is incomplete is the mechanism
as written, and the cost is a reader's: a future cut reading only the round-8 text would look
for the hazard in `derive_stitch.py`, find a licence that now refuses it, and could conclude the
hazard was disposed of -- while the second gate sat one edit away in `derive_runner.py`. Filed
INERT, not acted on, because `derive_runner.py` is not in this order's `<paths>` and widening to
it would be an override rather than a row.

**The reusable form.** When a producer and its fold are separate processes, *"the producer
deletes X"* and *"X disappears from the served graph"* are DIFFERENT claims separated by the
fold's admission rule. A mechanism written without that rule reads as one claim.

---

## 6. I3-AC5 -- THE READING (judgment; NO verdict; graded by `3.0.0_SA_CVO` at L9)

### (a) Is a licence grounded in sole-writership safe even when true?

**No -- it is safe only for as long as it stays true, and nothing in the estate watches.**

Sole-writership is a fact about a POPULATION AT A DATE. It is not a property of the term, it is
not enforced by any namespace, and no gate refuses a new producer that starts emitting
`STORED_IN`. The registry I landed makes the property *checkable*; it does not make it *stable*,
and the honest reading is that I moved the licence from "a comment a reader must believe" to "a
value a run can falsify" -- which is a real improvement and is not the same as a guarantee.

Three things about the check are worth stating plainly, because each is a way it could read
green while being wrong:

1. **It is repository-scoped.** A producer that exists only as deployed bytes is invisible to
   it. This is not hypothetical: the very writer this cell was asked to name has an UNTRACKED
   materializer, and only its output happens to be committed. The estate already knows this
   class of hole -- `MATERIALIZER_CENSUS_20260827` counted two of forty-three materializers
   missing from the repository -- and the check inherits it.
2. **It runs when someone runs it.** It is not wired into a commit gate, and I did not wire one:
   an agent-made gate nobody asked for is manufactured friction. So the property is `DESIRED`
   with an `EXERCISED` proof for today's population and no cadence. **A declared-but-unrun
   falsifier is a promise, not a control** -- this one has been run once, by me, in this run.
3. **Emission-shaped matching is a declared domain with an uncovered member.** My own AC1 found
   the writer's name sitting in a DESCRIPTION that no emission regex would match. A check built
   on the same shape as the census that missed it inherits the same blind spot.

What would make it genuinely safe is a different thing entirely: **a distinguisher on the edge**.
If this producer stamped its own edges with its own provenance, the drop would not need to be
type-shaped at all -- it would be *mine-shaped*, and sole-writership would stop being load-bearing.
The producer's own docstring already says so (`:491-493`: a type-shaped edge drop "needs a
distinguisher this producer does not currently write"). **The licence is a workaround for a
missing field, and it should be read as one.** I did not build it: my own previous order refused
the edge-side drop on the source's own evidence, and re-opening that here would be widening.

### (b) Should the retirement be re-attempted at all once the licence moves?

**Not as ruled, and the honest answer is that the ruling's PURPOSE has not been restated since
its mechanism died.**

Ruling 94872 retired `STORED_IN` by re-pointing it onto `OWNED_BY`. Round 8 killed the mechanism.
This cell removed the precondition the CTO named. It would be easy -- and wrong -- to read
"precondition discharged" as "proceed", for three reasons:

1. **The re-point is a TWO-EDIT act and only one edit has ever been scored** (row W2-S80).
   `STITCH_EDGE_TYPES` in `derive_runner.py` is the second gate, and a cut that scores only the
   emit would repeat the exact defect round 8 repaired -- a requirement written onto a face with
   no criterion.
2. **`OWNED_BY` is polysemous and the estate has already ruled on it.** `cse_schema.map_cloudedge`
   resolves `OWNED_BY` by DESTINATION TYPE: to `OWNS` for an actor, to `CONTAINS` for a
   container. That target-typed design is deliberate (H1-AC5 was FAILED in round 8 for reading
   the custody default as the bucket result). Collapsing a boundary edge onto a term whose
   meaning already depends on its target adds a second polysemy to a vocabulary that just
   finished paying for the first, and `_OWNED_BY_CONTAINER_TYPES` would have to absorb it.
3. **`STORED_IN` and `OWNED_BY` do not currently mean the same thing.** `STORED_IN` is
   `S3_DATA_KEY -> S3_BUCKET(arn)`, this producer's boundary edge at key grain. `OWNED_BY` from
   `graphuni-storage` is `S3Key -> arn:aws:s3:::<bucket>` at object/prefix grain from a frozen
   enumeration. They look alike and they are not the same population, and a retirement that
   merges them merges their denominators too.

**The reading:** what needs re-cutting is not the remedy's mechanism but its OUTCOME. If the
purpose was one boundary-edge vocabulary, the cheaper act is to state which term survives and
migrate the READERS -- `comp_coverage_check`'s roll-up, `cse_schema`'s resolver,
`cse_emit_graphhead`'s DST-typed bump -- rather than to make one producer's emit impersonate
another's. That is a CTO call, not a worker's, and I am naming it rather than taking it.

### (c) Is "a producer that unconditionally deletes a class of its own prior output" a pattern to carry anywhere else?

**No. It is a compensation for an architecture that cannot tell whose edge an edge is, and it
should be read as debt wherever it appears.**

The pattern exists because of a specific accident: the fold archives the derived graph, the
producer reads that archive back as its INPUT, and the archive does not record who produced
what. The producer therefore cannot distinguish "an edge I made last night" from "an edge
somebody else made" except by TYPE -- and type is a property of the CLASS, never of the
AUTHOR. **Every use of this pattern is a bet that a class has exactly one author, and the bet is
re-run every night without anyone re-checking it.**

Three properties make it worse than it looks:

- **Its failure is silent and it fails in the safe-looking direction.** A wrong delete produces
  a SMALLER graph, and smaller graphs do not alarm; they read as clean. Round 8's own record
  shows the mirror case: `STORED_IN` going to zero was only noticed because someone counted.
- **The blast radius is not the producer's own output.** That is precisely what the withdrawal
  caught: the delete's key is the TYPE, so its radius is every edge of that type from every
  author, forever, whether or not the author has ever heard of this producer.
- **The licence lives at a distance from the act.** The condition is about the ESTATE; the code
  is in one file. Nothing connects them at run time -- which is exactly the gap I just closed
  for this one call site, and exactly the gap that still exists everywhere else the pattern is
  used.

The general remedy is not a better licence, it is **provenance on the object**: stamp the edge
with its producer and drop what you wrote, never what looks like what you wrote. Until then,
where this pattern must exist, the minimum bar is what CG-s-42 landed -- the condition as DATA,
a REFUSAL rather than a silent pass, a counter on both branches, and a falsifier that can be
re-run. **A comment is not a control, and a control nobody runs is a comment with better
punctuation.**

---

## 7. WHAT THIS ORDER CHANGED

| file | change |
|---|---|
| `infra/aws/globgrph/derive_stitch.py` | +86 / -2 -- the licence registry, its evidence table, the drop request, `drop_prior_cycle_edges`, and the call site routed through it |
| `org/.../deliverables/0.9.0_WK_NFRA_CLDGRPH~2/i3_*` | the four criterion harnesses, the shared fixture, two read-only captures, the tree control, and the run transcripts |
| `org/.../surprise-channel/investigations/INVESTIGATION_v1.md` | one row, `NFRA_CLDGRPH-W2-S80` (285 rows across 214 fenced blocks after the append, 0 unparsed) |

Nothing else. `derive_runner.py` was read and not touched, and its diff is 0 bytes -- which is
itself one of AC4's four tells.
