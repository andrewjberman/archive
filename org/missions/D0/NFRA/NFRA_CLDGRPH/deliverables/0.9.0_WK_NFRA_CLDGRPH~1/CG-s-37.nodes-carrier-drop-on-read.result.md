# CG-s-37 -- THE NODES CARRIER'S MISSING DROP-ON-READ

TO `NFRA_CLDGRPH.TO-CG-H-2` - worker `0.9.0_WK_NFRA_CLDGRPH~1` - branch `wk-cldgrph-8-1`,
worktree `C:/tmp/wk-cldgrph-8-1`, cut from CLOUD at `2fd5cae09f`. ROUND 8. PUSH STATE: LOCAL --
never pushed, never merged, never rebased, and not measured against origin by this worker.

**One sentence.** `derive_stitch` reads back the snapshot it archives; of the three carriers of
that one mechanism, EDGES dropped its prior-cycle members on read and PROPS dropped its retired
key, while NODES only de-duplicated -- so a node the producer STOPPED emitting survived forever,
invisible under a fixed emission and wrong under a shrinking one. The drop is now in the producer
with its own counter (`prior_cycle_not_reemitted`), proved by an arm that went RED on the pre-fix
source and GREEN on the current one, and the three-figure disagreement row W2-S75 left open is
resolved to three different POPULATIONS -- on bytes that turned out not to be the bytes anyone
cited, which is its own row.

---

## 1. THE ASYMMETRY, READ OUT OF THE SOURCE, SIDE BY SIDE (H2-AC1)

`timeout 120 python .../h2_carrier_asymmetry.py` - rc 0 - capture `h2_ac1_output.txt`.

INSTRUMENT: a python `ast` parse of the whole producer file (312 statements, denominator printed,
nothing excluded). Not a grep, and not the card: the four round-7 cards are a CORROBORATING read
and a disagreement is reported rather than reconciled.

| carrier | behaviour BEFORE this order | behaviour AFTER | deciding line (post-fix) | counter |
|---|---|---|---|---|
| NODES | **DEDUPE** -- `archived and nid in fresh_ids` | **DROP** | `derive_stitch.py:494` -- `archived` | `prior_cycle_not_reemitted` (new) |
| PROPS | DROP | DROP | `derive_stitch.py:508` -- `for k in RETIRED_STITCH_PROPS: n.pop(k, None)` | `retired_props_dropped` |
| EDGES | DROP | DROP | `derive_stitch.py:159` -- `edges = [e for e in edges if str(e.get('edge_type','')) != 'STORED_IN']` | `stored_in_prior_cycle_dropped` |

CLASSIFICATION RULE, stated so it can be argued with: a removal whose test does NOT consult this
cycle's emission removes the archived member whatever this cycle emitted -- a DROP. A removal
keyed on the id being IN `fresh_ids` only resolves a collision -- a DEDUPE. That is why the
pre-fix NODES rule classifies as DEDUPE even though it deletes nodes.

`CARD_VS_SOURCE_DISAGREEMENTS=1 reported`: the NODES card (vintage `f3b5f26f77`) says DEDUPE and
the source now says DROP. The card is a READ-ONLY surface for this order and is NOT edited. The
disagreement is the fix landing, not a defect -- and it is printed rather than silently absorbed
because a card that quietly tracks the code is no longer a corroborating instrument.

**Why one output rather than three.** Three cells looked at one carrier each (W2-S61 nodes,
W2-S69 props, W2-S71 edges, pattern row S103) and each found the same disease separately. A check
scoped to the members cannot see a defect in what the members share; the shared thing here is the
archive-read, and it is only visible when the three answers are printed together.

## 2. THE ARM THAT WENT RED FIRST (H2-AC2)

`timeout 120 python .../h2_shrink_arm.py` - rc 0 - capture `h2_ac2_output.txt`.

The fixture SHRINKS by construction: cycle 1 emits `n1..n5`, cycle 2 emits `n1,n2`. Both arms
execute REAL producer source -- the baseline lifted by `ast` out of `git show
2fd5cae09f:infra/aws/globgrph/derive_stitch.py`, the current arm out of the worktree file -- so
the red baseline stays reproducible at any later commit instead of being an assertion that it
once failed. Only `_collapse_stitch_copies`, `STITCH_SOURCE` and `RETIRED_STITCH_PROPS` are
lifted, so the harness cannot reach boto3, the portal extractor or AWS.

```
BASELINE (pre-fix @2fd5cae09f): prior-cycle-only survivors 3 of 3   -> RED
CURRENT  (worktree, fixed)    : prior-cycle-only survivors 0 of 3   -> GREEN
                                counters {"prior_cycle_copy": 2, "prior_cycle_not_reemitted": 3, ...}
NEGATIVE CONTROL: the node BOTH cycles emit survives exactly once and the survivor is THIS
cycle's object (id() in fresh_objs). Exercised against a MUTANT collapse that drops every stitch
node: the control catches it (that node survives 0 times) -> NEGATIVE_CONTROL=FIRED.
SECOND CONTROL: a NON-stitch id present in two class buckets stays at 2 rows in every arm -- the
producer's promise never to collapse a legitimate two-bucket canonical id.
```

BASELINE ENVIRONMENT: same process, same python 3.12.10, same fixture; the only variable is the
producer source.

## 3. THE FIX, AND THE BRANCH I TOOK (deliverable 3)

`infra/aws/globgrph/derive_stitch.py`, `_collapse_stitch_copies`, immediately after the collision
rule it completes:

```python
                if archived and nid in fresh_ids:
                    dropped["prior_cycle_copy"] += 1
                    continue
                if archived:
                    # CG-s-37: THE DROP-ON-READ. ...
                    dropped["prior_cycle_not_reemitted"] += 1
                    continue
```

**UNCONDITIONAL, and here is the reasoning rather than the result.** `source=portal-stitch` is
this producer's OWN stamp and nothing else in the estate writes it (W2-S61), so a stitch node
arriving in the snapshot is by construction a previous cycle's output -- the identical argument
the EDGES carrier already makes about `STORED_IN`. The producer is a projection rebuilt every
cycle: the emission is the fact and the archive is a copy of last night's fact. A member this
cycle re-emits is kept (the fresh object wins, unchanged behaviour); a member it does not re-emit
was nobody's claim this cycle.

TWO COUNTERS, NOT ONE, because they answer different failures: `prior_cycle_copy` is a DUPLICATE
and `prior_cycle_not_reemitted` is a RETIREMENT, and only the second moves under a shrinking
emission. Both ride out through `unify_stats["collapsed_copies"]` into the artifact's `meta` and
through the existing `STITCH_UNIFY_COLLAPSED` log line, so a shrink now reads as a NUMBER.

**TWO BOUNDS, written into the function's docstring rather than patched around.**
1. The drop is only as good as `fresh_objs`. On the fallback path (no emission handed in),
   `archived` still rests on the `retyped_from` mark, and W2-S69 measured that mark going quiet
   the moment the snapshot itself carries canonical names. There the drop UNDER-fires; it does
   not over-fire.
2. It drops NODES only. Archived stitch EDGES other than `STORED_IN` still arrive, and the
   producer's 0-dangling check resolves against `aws_keys`, which `_index_aws` builds from the
   snapshot BEFORE the collapse runs -- so an archived edge onto a node dropped here still
   resolves and the check stays TRUE and BLIND. **Row `NFRA_CLDGRPH-W1-S44`.** Not widened: the
   BOUNDS put the edges carrier and `derive_runner` outside this order.

**NOT DEPLOYED, and that is the order's instruction, not an omission.** No `ecs run-task`, no
CodeBuild start, no image act, no `safe-apply`, no S3 write -- every globgrph derive publishes to
a topic with a live SMS subscription to a personal mobile. The producer change is COMMITTED and
UNDEPLOYED, and the counter has therefore never fired against the live snapshot. What is proved
is the code's behaviour on a fixture built from the real union's shape; what is NOT proved is a
number from a real cycle.

## 4. W2-S75 RESOLVED -- THREE FIGURES, THREE POPULATIONS (H2-AC3)

`timeout 120 python .../h2_snapshot_census.py` - rc 0 - `CENSUS_STATUS=DONE` - capture
`h2_ac3_output.txt`, machine-readable `h2_snapshot_census.capture.json`.

**FIRST, THE THING THE READ FOUND THAT NOBODY WAS LOOKING FOR.**
`s3://opal-313476888478-globgrph/snapshots/20260909/graph-20260909.tar.gz` now carries
`LastModified 2026-09-10T00:09:02Z`. Every one of the three figures describes the **21:05:21Z**
bytes of that same key. `get-bucket-versioning` returns rc 0 with no `Status`, and
`list-object-versions` returns exactly one version with `VersionId 'null'` -- the cited bytes are
gone and are not recoverable by anyone. The key grammar READS as a dated immutable archive and IS
a mutable pointer. **Row `NFRA_CLDGRPH-W1-S43`.** So the census below runs on the surviving bytes
and every attribution carries its basis.

MEASURED NOW on those bytes: `BY_SOURCE_DENOMINATOR=27687` nodes over 46 class buckets, nothing
excluded. `source=portal-stitch` -> **335**, of which 269 canonical-named, 65 `API_ROUTE`, 1
`PORTAL_BUNDLE`, and **0 under any provisional name**.

| figure | population it actually counted | PORTAL_BUNDLE | canonical-named stitch | fresh emission | basis |
|---|---|---|---|---|---|
| **1,771** (W2-S61) | the ARCHIVED SNAPSHOT alone, all types, at 21:05:21Z | INSIDE (the `+1`) | OUTSIDE | OUTSIDE | MEASURED-THEN, not re-readable |
| **1,791** (`derive_stitch.py:311-314`) | the RUN-TIME union after retype + collapse: surviving archived members PLUS this cycle's emission | INSIDE | INSIDE | INSIDE | INFERRED |
| **1,790** (`139cbe1d40`: 1,521 merged + 269 carried) | `unify`'s `admitted`: run-time AND type-filtered to `STITCH_CANONICAL_TYPES` | OUTSIDE | INSIDE | INSIDE | MEASURED-THEN |

The arithmetic: 1,770 retyped archived members (the run's own `STITCH_UNIFY_PRIOR_CYCLE
retyped=1770`, which is 1,771 minus the one `PORTAL_BUNDLE` no re-type map names) + 20 fresh
members not already in the archive = 1,790 admitted, + that 1 `PORTAL_BUNDLE` = 1,791. **The
1,791-vs-1,790 gap is exactly one node**, and the 1,771-vs-1,791 gap is the fresh emission.

**MEASURED CORROBORATION, on a number nobody argued about.** The surviving stitch population is
269 canonical-named + 66 in no map = 335, and **269 is exactly figure 3's `carried`**. A stitch
member that MERGES onto a canonical id is removed by the unify (the canonical node stays,
`source=None`), so the 1,521 merged members can never appear in any later snapshot census. A
snapshot census and an admitted census are structurally different populations -- which is the
finding, not an excuse for the discrepancy.

The HELD hypothesis the issuer flagged (two populations under one sentence, not an arithmetic
slip) survived its falsification attempt and is now corroborated on an independent number.
**Row `NFRA_CLDGRPH-W1-S45`**; the misleading comment is NOT corrected here (that is prose in a
cell about a drop-on-read, and correcting it is a widening).

RESIDUAL, named rather than smoothed: the identity of the 20 members is unrecoverable, because it
needs the 21:05:21Z bytes.

AND THE TREND THAT MAKES THIS CELL URGENT RATHER THAN TIDY: the same key's stitch population is
**335 today against ~1,771 in the record** -- a 5.3x SHRINK. A shrinking stitch population is
precisely the condition under which the missing NODES drop carried stale members forward.

## 5. THE HOLD (H2-AC4)

`timeout 120 bash .../h2_no_egress.sh` - rc 0 - capture `h2_ac4_output.txt`.

`ECS_RUN_TASK_CALLS=0  CODEBUILD_STARTS=0  S3_WRITES=0  IMAGE_PUSHES=0  TERRAFORM_APPLIES=0`
over `SCANNED_DENOMINATOR=18` files (every `.py` in this worker's deliverable folder -- wider than
this order's own artifacts, which only strengthens the zeros -- plus the S3 ledger plus the
production diff from `2fd5cae09f`). Exclusions printed with reasons: this detector itself (it
contains the five patterns by construction) and prose `.md` (the record must quote the forbidden
verbs to state the hold).

`EGRESS_PROBE_CONTROL=FIRED` -- the same detector against a planted file carrying one line per
held act finds 5 of 5. `TREE_CONTROL=FIRED` -- a file existing only on branch `wk-cldgrph-8-1`
appears in the scanned population, so the scan read THIS tree.

`S3_READS=11 (permitted)`, enumerated one line each with its purpose in `h2_s3_reads.ledger`: 3
GETs of snapshot objects, 2 boto3 GETs by the census, 3 HEADs, 1 LIST, 1 versioning read, 1
`latest.txt`. Counted rather than hidden, so "I took no read" and "I took a read I was allowed"
are different facts in this record.

## 6. THE READING (H2-AC5 -- judgment; graded by `3.0.0_SA_CVO`, NO verdict here)

**(a) Is a drop-on-read the right remedy for the NODES carrier at all, or is the right remedy
upstream?** The right remedy is upstream, and the drop is the correct thing to ship anyway. The
disease is that this producer's INPUT contains its own OUTPUT -- `derive_runner` folds the stitch
artifact into the AWS snapshot and archives it, and `derive_stitch` reads that snapshot back. Every
carrier-level fix is a filter compensating for an input that should never have contained the
producer's own claims: three filters now, each with its own scope, each correct, and none of them
able to say anything about a fourth carrier. The upstream remedy is one line of ARCHITECTURE, not
of code: the producer should read the AWS layer WITHOUT its own prior emission -- either the fold
writes stitch members into a separate document from the aws-shape the producer loads, or
`load_aws_layer` strips `source=portal-stitch` at the door, ONE filter at ONE place instead of one
per carrier. That is `derive_runner`'s surface and the next order's, so this order does not take
it; but note the asymmetry of cost -- the door filter is a single unconditional statement whose
correctness argument is the same for every carrier, while the per-carrier filters cost a cell each
and are discovered by accident. The drop I shipped is right BECAUSE the door is not closed: with
the door open, a node this cycle did not emit is stale data being served, and no amount of
upstream elegance retro-fixes tonight's artifact.

**(b) What would a fourth carrier need for this class of defect to be caught by construction?**
Not a fourth check -- the third check is what proves checks do not generalise. The property that
must hold is: EVERY member of the union carries where it came from, and the producer refuses to
emit a member it did not derive THIS cycle. Concretely, three things and none of them is a
monitor. (i) A CYCLE STAMP on the artifact, not a source stamp: `source=portal-stitch` says WHO,
never WHEN, which is why the producer had to reach for Python `id()` -- an in-process identity
standing in for a freshness field the data does not carry. Give every emitted member the emitting
run's id and "did THIS cycle emit this?" becomes a data question instead of an object-identity
trick that no consumer, and no later reader of the artifact, can reproduce. (ii) ONE
prior-cycle filter at the READ, applied to the whole document before any carrier-specific logic
sees it -- then a new carrier inherits the answer rather than being asked the question again.
(iii) A RECONCILIATION THAT COUNTS INPUTS, not just outputs: the producer already prints
`admitted = merged + created, lost = 0`, which is a conservation law over what it ADMITTED and is
structurally incapable of noticing that the input contained 1,771 members it never derived. The
tell to look for in any future producer: a conservation law whose denominator is the producer's
own output.

**(c) Was the three carriers answering DIFFERENTLY ever defensible?** Only in sequence, never at
rest. Each answer was arrived at correctly under a different pressure -- the nodes rule was built
to survive a vocabulary change, the props rule to un-serve a retired stamp, the edges rule to stop
a 955-edge fan-out -- and each was a local repair by a seat that could see one carrier. What was
never defensible is the STATE that left: one mechanism, three answers, no document saying they
were answers to the same question, and a per-carrier check that passes on each. The estate's own
law names it -- a check scoped to the members cannot see a defect in what they share. The
practical rule I would draw is narrower and cheaper than "card everything": WHEN A PRODUCER READS
ITS OWN OUTPUT, THE ANSWER TO "IS THE PRIOR CYCLE INPUT OR NOISE?" IS A PROPERTY OF THE PRODUCER
AND MUST BE WRITTEN ONCE, AT THE READ. If it is being answered at the carrier, that is already the
defect, and the number of carriers is just how many times you will find it.

---

## SURPRISE ROWS FILED (3)

| id | class / hazard | one line |
|---|---|---|
| `NFRA_CLDGRPH-W1-S43` | OBSERVATION / **ARMED** (`0.8.0_AE_CloudComp`) | the snapshot object W2-S75 cites was overwritten and the bucket is unversioned -- the cited vintage is unrecoverable and the key grammar reads immutable |
| `NFRA_CLDGRPH-W1-S44` | OBSERVATION / **ARMED** (`0.8.0_AE_CloudComp`) | the node drop has no edge-side counterpart, and the producer's 0-dangling check is blind to the gap by construction |
| `NFRA_CLDGRPH-W1-S45` | OBSERVATION / INERT | the 1,791 comment names a population it does not count; W2-S75's held hypothesis survives falsification and is corroborated at 269 |

## WHAT THIS ORDER DID NOT DO

- Did not deploy, build, publish or run anything in AWS (the egress hold; H2-AC4 is the proof).
- Did not touch `derive_runner.py` (next order's surface), the edges carrier, or the four cards.
- Did not correct the `derive_stitch.py:311-314` comment (row W1-S45 instead of a widening).
- Did not measure how many archived stitch EDGES would now point at a dropped node: that needs a
  producer run against the live snapshot, which is a held act. The shape is certain, the number is
  not, and no number was manufactured.
