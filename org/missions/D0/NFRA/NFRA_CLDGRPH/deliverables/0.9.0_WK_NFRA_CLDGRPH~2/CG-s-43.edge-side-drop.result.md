# CG-s-43 -- THE EDGE-SIDE COUNTERPART, AND THE CHECK THAT WAS ANSWERING A QUESTION ABOUT A DIFFERENT MOMENT

**TO:** `NFRA_CLDGRPH.TO-CG-I-2.edge-side-drop-and-the-blind-check` · **cell** CG-s-43 (decomp v0.12 s.1a)
**Worker:** `0.9.0_WK_NFRA_CLDGRPH~2`, spine-v3 L7 subagent of `2.0.0_SA_COO~A`, round 9
**Worktree:** `C:/tmp/wk-cldgrph-9-2`, branch `wk-cldgrph-9-2`, cut from CLOUD at `b5bb2f16a0`
**Push state:** LOCAL -- never pushed, never merged, never rebased, never measured against origin by this worker.
**Deploy state:** NOTHING IS DEPLOYED. The producer change is COMMITTED-NOT-DEPLOY-SCOPE and the moved key set has never run against the live snapshot.

---

## 1. THE ANSWER FIRST

The window is real, it was **observed and not described**, and the remedy chosen is **`AWS_KEYS_MOVED`** -- the
0-dangling check's key set is now rebuilt AFTER the collapse, from the nodes that will actually be emitted.
The edge-side drop was **considered and NOT taken**, for a reason the source itself supplies (below, s.4).

On a fixture driven through the producer's own `build_stitched_graph()`:

| arm | producer's own `genuine_dangling` | node-absent/edge-present edges |
|---|---|---|
| pre-remedy bytes @`b5bb2f16a0` | **0** of 2 edges -- `OK:` | **1** |
| this worktree's bytes | **1** of 2 edges -- `ERROR:` | 1 |
| negative control (an endpoint in NEITHER key set) | 1 of 3 -- the check is ALIVE | n/a |

**THE MAGNITUDE ON THE LIVE SNAPSHOT REMAINS UNMEASURED AND WAS NOT MANUFACTURED.** Counting the archived
stitch edges a real run would find pointing at a dropped node needs a producer run against the live snapshot,
which the egress hold forbids. Row `W1-S44` refused to guess it; so does this record. What IS certain from the
source is the SHAPE, and the shape is now demonstrated rather than argued.

---

## 2. I2-AC1 -- THE BLINDNESS, OBSERVED

`i2_window.py` loads the producer source **at the pinned pre-remedy commit** (`git show b5bb2f16a0:...`) as a
module and drives its real `build_stitched_graph()` over a fixture. The graded number is the producer's own
`meta["genuine_dangling"]`, not a re-implementation of its predicate -- **a harness transcribed from the
implementation would score the blind spot as a pass**, so nothing here is transcribed.

- **GRAIN:** the producer's own function and its own metric; only the three INPUT loaders are replaced.
- **COVERAGE:** ONE synthetic fixture -- 3 nodes, 2-3 archived edges. It certifies the SHAPE, never the magnitude.
- **ENVIRONMENT:** bytes pinned at `b5bb2f16a0`, resolved BY CONTENT (`'| aws_keys'` present, `'CG-s-43'` absent), never by an ancestry test.
- **TREE:** `C:/tmp/wk-cldgrph-9-2`, branch `wk-cldgrph-9-2`.

The fixture: an archived stitch node (`comp:i2-retired`) this cycle does not re-emit, plus an archived
`FETCHES` edge onto it -- **not** `STORED_IN`, so `derive_stitch.py:158-159` does not drop it. The collapse
drops the node (`prior_cycle_not_reemitted=1`), the edge survives, **and the producer reports
`genuine_dangling=0`.** The negative-control arm adds an edge onto an id in neither key set and the same
check reports 1 -- so arm A's zero is blindness, not a dead instrument.

**WHY THE PIN AND NOT THE WORKTREE FILE:** this criterion is graded after the remedy lands in the same file.
Read from the worktree it would grade the remedy, not the baseline. Pinning keeps it a baseline at every
later grading, and the pin is re-derived on each run rather than stored.

## 3. I2-AC2 -- WHO ELSE DEPENDS ON THAT KEY SET (and the finding nobody was looking for)

Two instruments on **two different axes** -- a text census cannot tell a live read from a dead assignment.

- **INSTRUMENT 1, repo census:** `comp-find 'aws_keys|_index_aws' --all`, **6 consumer lines of ~139 hits
  across 30,057 files scanned** (`corpus=all`), classified BY SUBTRACTION from the printed denominator:
  parsed hit lines - non-executable mentions - substring-different-symbol (`comp_aws_keys_in_comp_tools`,
  `aws_keys.txt`) - this order's own harnesses - comment/docstring lines = consumers.
  **TREE_READ=WORKTREE with the positive control FIRED** (a file existing only on this branch appears in the hits).
- **INSTRUMENT 2, AST dataflow** inside `build_stitched_graph`: every bind and read of `aws_keys`/`all_keys`.

**THE CONSUMERS, NAMED:** `derive_stitch.py:74` (the definition), `:128` (the bind), `:144` (the dead bind, below),
`:487` (the union, now the rebuild), and `g2_local_fold.sh:163/:165` -- a round-7 capture harness that calls
`_index_aws` DIRECTLY. That last one is why the remedy leaves `_index_aws` untouched: the only consumer
outside this producer reaches the function, not the call site, so a change at the call site cannot reach it.

**AND THE FINDING THE CRITERION PAID FOR (row `NFRA_CLDGRPH-W2-S79`):** `all_keys` is **bound TWICE**. The
bind at `:144` (`all_keys = aws_keys | portal_keys`) -- the line whose text most looks like the defect, and the
one a reader goes to -- is **DEAD**: no read of `all_keys` occurs between it and the rebind. The check's key
set was only ever the second one. The cell's diagnosis was right; the line everyone would have edited was not
the line that mattered. **After this remedy, `aws_keys` has 0 LIVE reads** -- its only remaining read is on
that dead bind. It is NOT removed here: deleting it is a second act on a file the next order in this worker's
own queue also writes.

**HELD, NOT MEASURED:** `aws_keys` also carries the DUAL IDENTITY of an AWS node (`arn` AND `id`,
`_index_aws:83-85`, row W2-S68). A remedy that merely DELETED the union would drop the arn alias for every
AWS node whose id != arn and re-open W2-S68. The remedy therefore **re-derives the alias** from the
post-collapse population rather than dropping it.

## 4. I2-AC3 -- THE REMEDY, AND WHY THIS ONE

**REMEDY = `AWS_KEYS_MOVED`.** `derive_stitch.py` `all_keys` is now built from the surviving nodes only,
keeping both identities (`id` and `arn`) of any node that has two. `_index_aws` is unchanged; `:158-159` is
unchanged; the drop's licence and comment (CG-s-42's surface) are untouched.

**WHY NOT THE EDGE-SIDE DROP -- the source decides it.** `STORED_IN` can be dropped by its literal type
because nothing else in the estate writes one (`:155-157`). The other stitch edge types --
`WRITES`, `READS`, `ROUTES_TO`, `DERIVES_FROM` -- **collide with the AWS layer's own ARN-keyed
READS/WRITES/ASSUMES edges, carried in unchanged** (module docstring `:20-21`). A type-shaped drop would
delete estate this order never touched, and the archived edges carry no distinguisher this producer can
trust; measuring whether one exists needs a producer run the hold forbids. **A remedy whose safety I cannot
measure is not the remedy I ship under a hold.**

**AND THE DEEPER REASON: the check is the general control, the drop is a point fix.** Dropping the edge
closes THIS window and leaves the check still answering a question about the moment before the collapse --
the next shrinking emission is invisible again. Moving the key set makes the producer SAY the number instead
of hiding it, and it is the only path by which the unmeasured magnitude ever gets measured: **the first real
run prints it.**

**THE COST, STATED RATHER THAN DISCOVERED:** `main()` returns 1 when `genuine_dangling != 0`, so the first
nightly run after this lands can print `ERROR:` where it printed `OK:`. That is the finding surfacing, and it
can only fire on exactly the window -- an archived stitch edge naming a node this cycle did not re-emit.
**It is a CONSEQUENCE, not a side effect, and it is named here rather than at 02:00Z.**

## 5. I2-AC4 -- THE HOLD, AND THE NUMBER NOT INVENTED

`ECS_RUN_TASK_CALLS=0 · CODEBUILD_STARTS=0 · S3_WRITES=0 · IMAGE_PUSHES=0 · TERRAFORM_APPLIES=0`, over 7
authored files plus git's own diff of the one production file, **with the probe FIRING 5 of 5** -- a detector
that cannot go non-zero is a constant wearing a measurement's clothes. `MAGNITUDE_MANUFACTURED=false`, checked
mechanically: every magnitude claim in every capture reads `UNMEASURED`. **No AWS call of any kind was made:**
the producer's `load_aws_layer()` -- its only S3 read -- is replaced before `build_stitched_graph()` runs.
The detector EXCLUDES ITSELF from the scanned set and says so: its five command literals ARE the probe.

## 6. I2-AC5 -- THE READING (no verdict; graded by `3.0.0_SA_CVO` at L9)

**(a) BUG OR CATEGORY ERROR? A category error wearing a bug's clothes, and it recurs by construction.** The
check was never miscomputing. It computed correctly over a collection sampled at t0 and asserted a property
of the collection at t1. The general form: **when a producer both reads and writes one collection, every set
derived from it is DATED, and a validation carrying an undated derived set validates a moment nobody is going
to publish.** The proof that this is structural and not carelessness is that **the same file does the same
thing on purpose, correctly, six lines away**: `fresh_objs` is taken early with a comment saying exactly why
(after the union a fresh node and its archived copy are indistinguishable). The discriminator between the two
is whether **the early take IS THE POINT**. `fresh_objs`' early take is load-bearing. `aws_keys`' early take
is incidental -- it happened early because that is where `_index_aws` was called to build `lam_by_name` and
`bkt_by_name`, and the key set rode out of the same function in the same tuple. **THE REUSABLE TELL: a value
that arrives in a tuple beside values that genuinely need an early moment inherits their VINTAGE without
inheriting their REASON, and nothing at the call site records which it was.**

Why it was invisible: the check asks "is every endpoint in the key set", and the stale endpoints and the
stale keys came out of the SAME archive. **Two instruments on one substrate agree and convict falsely** --
here they agreed on innocence. The narrow rule this yields: **A CHECK ON AN ARTIFACT MUST TAKE EVERY TERM
FROM THE ARTIFACT.** After this remedy `all_keys` has no input term at all; it is derived only from what will
be written. That is a stronger statement than "move it later", and it is the one worth carrying: any term a
validation borrows from an INPUT is a term that can be stale in the same direction as the defect.

Where it will recur: any producer whose input contains its own prior output -- which is this producer's
standing condition, since `derive_runner` folds the artifact into the snapshot this reads back. It has already
recurred once per carrier (nodes, props, edges: rounds 6-8) and once per check (this one). It will keep
recurring until the door is closed upstream, which is `derive_runner`'s surface and not this order's.

**(b) SHOULD THE NODE-SIDE DROP HAVE SHIPPED WITHOUT ITS EDGE-SIDE HALF? Yes -- and the fault is not the
half, it is which half.** Before CG-s-37 a node the producer stopped emitting was SERVED FOREVER: a false
fact, resolvable, indistinguishable from a live one. After it, that node is gone and an edge onto it is a
dangling reference -- a claim that is **visibly** wrong instead of **invisibly** wrong. The half-fix strictly
reduced the false facts served and converted the residue into a shape the estate already has an instrument
for. Shipping half of a two-part repair is ordinary. **What is not ordinary is that the half that shipped
SILENCED THE DETECTOR FOR THE OTHER HALF** -- the 0-dangling check kept printing `OK:` precisely because the
drop had happened. That is the thing to name: not "half a fix", but "half a fix that suppresses the alarm for
the other half".

Which is why the correct ORDER was the reverse. **Move the check first.** Moving a check is inert -- it
changes only what the producer SAYS, never what it emits, and it is reversible in one line. Had the key set
moved first, CG-s-37's very first run would have printed its own edge-side consequence as a number, and the
magnitude this cell must still report as UNMEASURED would already be known. **THE RULE: when a repair will
create a state a check might not see, move the check BEFORE the repair -- the check's move is the cheap,
reversible, non-emitting one, and it is the only one that can measure the repair.**

And the mechanism did work as designed, which is worth recording beside the criticism: the worker who shipped
the node-side drop **filed a row against its own fix** (`W1-S44`), refused to widen, and refused to invent
the magnitude. That row is the entire reason this cell exists one round later. A defect that arrives with its
own row is a defect the fabric is handling; the price was one round.

---

## 7. WHAT IS NOT CLAIMED

- **The magnitude on the live snapshot.** UNMEASURED. It needs a producer run; the hold forbids it. It can be
  bounded only trivially (>= 0, and <= the number of archived non-`STORED_IN` stitch edges), and neither bound
  is worth a number without a run.
- **That the remedy is safe for a consumer reaching the key set through neither `aws_keys` nor `_index_aws`.**
  Declared out of reach of the census, not assumed away.
- **That the fixture resembles the live snapshot in SIZE or COMPOSITION.** It resembles it in SHAPE only, and
  the shape is what the criterion asks for.
- **Determinism of the AC2 census's full stdout.** UNSTABLE BY CONSTRUCTION and stated: the comp-rail logs its
  own invocation into the corpus it scans, so the hit count grows by the tool's own telemetry between runs.
  The GRADED token lines are stable across back-to-back runs; the consumer count did not move.

## 8. ROWS AND SURFACES

- **Filed:** `NFRA_CLDGRPH-W2-S79` -- OBSERVATION, INERT, UNDER_INVESTIGATION. The double bind of `all_keys`
  and the dead `:144`. Appended to
  `org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md` (283 rows after
  the append, counted by parsing every fenced json block).
- **Touched:** `infra/aws/globgrph/derive_stitch.py` (the `all_keys` rebuild + the `_collapse_stitch_copies`
  docstring bound (2), which this change falsified and which is corrected rather than left standing).
- **Deliberately untouched:** `:158-159` and the drop's licence/comment (CG-s-42's surface, next in this
  worker's own queue); `_index_aws`; the `:144` dead bind; the round-7 cards (READ ONLY).
