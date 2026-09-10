# CG-s-40 -- TWO SCORERS, ONE EDGE, FOUR DECLARED SHAPES: the item PLACED, not taken

**Task order:** `NFRA_CLDGRPH.TO-CG-H-5` - **worker:** `0.9.0_WK_NFRA_CLDGRPH~4` - **branch:**
`wk-cldgrph-8-4` @ cut `2fd5cae09f` - **2026-09-10**.
**Cell:** CG-s-40 (decomposition v0.11 s.1a), added on the CTO's round-7 analysis @`bb08a2ac62` s.6 item 5.
**Deliverable class:** a PLACEMENT. The CTO put this item outside NFRA_CLDGRPH's plane, so this order
censuses it, states it, and parks it on a carrier with an owner and an un-park condition. **Zero scorer
files and zero producer files were modified, measured on two arms each.**

## CUT DISCIPLINE -- the three things every number below carries

- **INSTRUMENT + COVERAGE.** Named per section with its denominator. Two different instruments were used
  deliberately: the consumer census walks the worktree in-process (`os.walk`, 29,616 files opened) and the
  cross-checks use `comp-find` (29,619-29,624 files scanned). They agree to within their printed floors,
  which is corroboration by a DIFFERENT method rather than a second run of the same one.
- **GRAIN.** Consumers at FILE grain. Edges at EDGE grain. Declarations at (file, line) grain. Shape
  classes at CLASS grain. Where a number is an edge rate it says so, because an edge rate and a fact rate
  are different sentences.
- **ENVIRONMENT of the stored baseline.** There is no stored baseline. Every count was measured in this
  process, in this worktree, on this run. The only comparison values are literal declaration strings read
  from source at `2fd5cae09f`, and the served-graph counts carry the projection's own vintage line:
  `2026-09-10T12:24:50.576632+00:00`, stitch source `stitch-codebuild built 2026-09-10T03:01:17Z`.

---

## 1. THE CONSUMER CENSUS -- 28, and the record named 2 (H5-AC1)

Invocation: `timeout 120 python .../h5_consumer_census.py`. Full capture: `h5_ac1_capture.txt`.

```
TREE_READ=WORKTREE
TREE_POSITIVE_CONTROL=FIRED
REPOSITORY_DENOMINATOR=29616 file(s) opened and read
CONSUMERS_FOUND=28
CLASSIFIED=28 of 28
BY_CLASS=FIXTURE=7 PRODUCER=2 PROSE=17 SCORER=2
BY_SUBTRACTION=true
```

**The subtraction, printed rather than recalled:**

```
 29616  files opened and read (REPOSITORY_DENOMINATOR)
-29487  files that never mention SERVED_FROM
=  129  files mentioning SERVED_FROM (CANDIDATES)
-    9  files this order authored or appended to on this run (excluded by name, all nine
        listed in the capture)
-   92  candidates that mention the family but declare NO target class and carry NO
        target-class dependency (a mention is not a consumer)
=   28  CONSUMERS
```

**TREE HONESTY.** The rail's caller-tree defect -- a linked worktree scanning the MAIN tree and returning
a well-formed zero with a real denominator -- is why `TREE_READ` and the control are printed. The control
is a file that exists ONLY on this branch: it appears in the sweep (`present_in_this_sweep=True`) and is
absent at the branch point (`git cat-file -e 2fd5cae09f:<path>` rc=128). A census that merely looks right
is exactly what the old rail produced; a denominator is not a tree.

**THE FINDING: the population is a vocabulary, not two files.** 21 of the 28 carry the WRONG class, 15
carry the intended one, several carry both. The consumers the census record did NOT name include:

| | path | why it matters |
|---|---|---|
| PRODUCER | `org/modules/graph/debtscan/summary_corpus.py:350` | a live module carrying `live: ServedURL-[SERVED_FROM]->S3_BUCKET_POLICY` beside a PROSE shape -- a third code consumer |
| FIXTURE | `infra/aws/globgrph/debtscan_scorecard_latest.json` | **the scored artifact itself**: `:5` and `:26` `scored_from`, `:17` `"ServedURL-SERVED_FROM->S3_BUCKET_POLICY": 29` |
| FIXTURE | `org/modules/graph/canon-patterns.yaml` | **the CTO-ratified canon both scorers consume**, which declares the family TWICE MORE and agrees with neither of them |
| PROSE | `org/tier2_senior/0.7.0_AE_CloudOps/task_orders/NFRA_DEBTSCAN.TO-D3...md` | the `<status>` of a CLOSED order records `ServedURL-SERVED_FROM->BUCKET_POLICY 29, 0 shape-outliers` |

**Two was the null result and this is not it.** The count that matters is not 28 against 2; it is that a
defect adopted as canon propagates into every artifact class the estate has -- code, config, scored output,
proof-of-spec instances, task-order status fields and rulings -- and each copy reads as a definition.

## 2. THE DISAGREEMENT, MADE CHECKABLE (H5-AC2)

Invocation: `timeout 120 python .../h5_disagreement.py`. Full capture: `h5_ac2_capture.txt`.

| | shape | declared at @`2fd5cae09f` | served today | committed re-point |
|---|---|---|---|---|
| **A** | `ServedURL-[SERVED_FROM]->S3_BUCKET_POLICY` | `debtscan_canon_scorer.py:48,144` | **YES**, 27 of 27 | no |
| **B** | `(ServedURL)-[SERVED_FROM]->(S3)` | `canon_motif_scorer.py:94,131` | no | **YES** |

```
QUERY_FORM=edge_type-as-property
MATCHES_SERVED_TODAY=A
MATCHES_COMMITTED_REPOINT=B
BREAKS_ON_DEPLOY=A
POSITIVE_CONTROL=FIRED
```

`edge_type` is read as a PROPERTY: the typed form `MATCH ()-[e:SERVED_FROM]->()` errors at the binder, and
a binder error is a wrong-form signal, never a zero (banked as S112). **The control is the part that makes
the single-class answer mean something:** the SAME statement shape on `OWNED_BY` returns two distinct
target classes (`S3_BUCKET` 232, `MS_USER` 6153), so `SERVED_FROM` landing 27-of-27 on `S3_BUCKET_POLICY`
is a property of the DATA, not of the query. A non-existent `edge_type` returns 0 as the negative arm.

**The committed re-point was read at the EMIT SITE, not file-wide.** `derive_runner.py`'s SERVED_FROM
stitch (lines 1870-1979 at `2fd5cae09f`, emit at 1959) now resolves its target through
`canonical_node_key(n)` at :1905 under the CG-s-33 marker at :1898, and the pre-fix bare-name form is gone
FROM THAT BLOCK. It is still present ONCE elsewhere in the same file, which is exactly why a file-wide
token test would have answered a question about the FILE rather than about this edge.

**AND THE CANON IS A THIRD AND FOURTH VOICE.** `org/modules/graph/canon-patterns.yaml` (CTO-ratified
`ef6110129`), which both scorers name as their source, declares:

- `:54` `(S3_BUCKET)-[SERVED_FROM|IS_ENDPOINT]->(ServedURL|API_ROUTE)` -- **the opposite direction**;
- `:116` `(Field gold)-[SERVED_FROM]->(ServedURL)` -- a different source AND a different target;
- `:121`, `:137` comments recording the live shape as `ServedURL->S3_BUCKET_POLICY 29`.

and at `:124` it says of itself: *"OPEN (untraced -- do NOT rewrite the motif blind) ... Trace the
SERVED_LINEAGE scorer's consumers (comp-blast) before replacing the motif."* **That trace was asked for on
2026-07-18 and never run. Section 1 is that trace.**

## 3. THE PREDICTED BREAKAGE IS NOT THE REAL ONE -- row `NFRA_CLDGRPH-W4-S7`

The census record and this order's cell both predict that the deploy flips debtscan's dominant shape and
its threshold and yields a 100 percent outlier rate. Re-running `score_auth_canon`'s own arithmetic
(`:160-177`) on both sides, with `outlier_frac` read from the canon at `:147`:

| | before | after |
|---|---|---|
| shapes | `ROUTES_TO->LAMBDA` 86, `SERVED_FROM->S3_BUCKET_POLICY` 27 | `ROUTES_TO->LAMBDA` 86, `SERVED_FROM->S3_BUCKET` 27 |
| dominant | `API_ROUTE-ROUTES_TO->LAMBDA` (86) | same |
| threshold | 8 | 8 |
| outlier candidates | `[]` | `[]` |

**Nothing spikes.** `S3_BUCKET_POLICY` occurs in that file only at `:48` and `:144`, both PROSE, over a
377-line denominator; the arithmetic reads `t.node_type` at runtime and is class-agnostic. `canon_motif`'s
number is invariant too -- `score_served_lineage` counts DISTINCT `ServedURL` sources and never reads the
target class at all. **So the deploy does not break a computation. It falsifies A's declaration and repairs
B's, silently, and `:48` is the per-class SOURCE PROVENANCE string that gets copied verbatim into the
emitted scorecard.** An owner waiting for the predicted red number will see green.

That is filed as an ARMED row with `0.7.0_AE_CloudOps` as disarm owner, because an inherited prediction of
a loud failure becomes a detector nobody built.

## 4. THE 2026-07-10 CLEAR_TO_DELETE, AND WHY BOTH BRANCHES ARE LIVE (H5-AC3)

The message (read in place from the main tree; the inbox is untracked and absent from this worktree --
row `NFRA_CLDGRPH-W4-S8`) says, verbatim:

> *"the only reader of debtscan_scorecard_latest.json anywhere in the tree (grep, non-doc/non-log) is
> debtscan_canon_scorer.py ITSELF -- the file you're deleting."*
> *"DISPOSITION: CLEAR TO DELETE debtscan_canon_scorer.py + its _latest.json output ... Recommend to CTO:
> clear the CM1 delete."*

**Two months later the file is still at HEAD and has been maintained since.** `git log --full-history`:
last substantive commit `7f0a9d249c` (2026-09-05, `0.9.0_WK_NFRA_CLDGRPH~2`, TO-CG-D-7/CG-s-8) -- **this
project ported the cleared-for-deletion scorer onto `projection_client`, 57 days after the clearance.**
Nobody in that chain was wrong; nobody was carrying the clearance either.

**RETIRE is therefore live beside RE-POINT, and this order does not choose between them.** The carrier
offers three branches and hands over ONE decidable question with its measurement attached: does anything
other than the scorer itself read `debtscan_scorecard_latest.json` today? Re-measured over 29,624 files
scanned, 73 hits across 41 files: **exactly one code file names it -- its own writer.** The single thing
left to open is `org/tier1_exec/4.0.0_SA_CRO~A/deliverables/NFRA_C3MATERIALIZE.TO-L2-CROA/L2_VIEW_ARTIFACTS.json`,
which DECLARES it as a view input (a declaration is not a read).

**OWNER: `0.7.0_AE_CloudOps`**, verified from the record on two independent documents -- `NFRA_DEBTSCAN.TO-D3`'s
`<assigned_to>` (the order that shipped `debtscan_canon_scorer.py`, named in its own `<status>`), and the
2026-07-10 message's `To:` header calling `canon_motif_scorer.py` *"YOUR live canon_motif_scorer.py"*.
**NOT `0.8.0_AE_CloudComp`**, which WROTE the clearance -- authorship of a clearance is not ownership of a
file, and that seat is the dependent in the exchange. The LANE is recorded as NON-evidence:
`.owned-paths.yaml` resolves both scorers to `CLOUD_OPS_OR_ETL`, which admits both candidate serials, so a
lane check returns a pass for either and proves neither. RETIRE additionally needs `1.0.0_SA_CTO`, because
the message routes that delete to the CTO.

**UN-PARK CONDITION:** the CG-s-33 re-point reaching the SERVED plane -- one statement, no judgment:
the `SERVED_FROM` target-class query returning `S3_BUCKET` instead of `S3_BUCKET_POLICY`. Andrew-gated
today (every globgrph derive publishes to a topic with a live SMS subscription; rows W2-S72/S104/S106), so
the clock is real but is not running by itself. A second, earlier trigger is named on the carrier: the
first re-run of the scorer AFTER the deploy is what freezes the false provenance line into a new artifact.

Carrier: `PARKED_scorer-canonical-shape-disagreement.md`, beside this file. It also lists what nobody
should do meanwhile -- including *not* rewriting the canon's motif blind, which the canon itself forbids.

## 5. THE HOLD (H5-AC4)

```
ECS_RUN_TASK_CALLS=0  CODEBUILD_STARTS=0  S3_WRITES=0  IMAGE_PUSHES=0  TERRAFORM_APPLIES=0
PRODUCER_FILES_MODIFIED=0   CHANGE_MANAGEMENT_ENTRIES_BY_THIS_SERIAL=0   EGRESS_PROBE_CONTROL=FIRED
```

Population: the union of `git status --porcelain -uall` and `git diff --name-only 2fd5cae09f` -- every path
this order could have written -- with `SCANNED_FILES_ACTUALLY_OPENED` printed beside the counts, because a
scan that opened nothing returns the same zeros as a clean one. Patterns are invocation-shaped
(`aws ecs run-task`, not the word "ECS"), since the carrier NAMES the held acts in order to forbid them.
The control is a planted probe carrying all five acts, scanned by the SAME function: 1/1/1/1/1.
`PRODUCER_FILES_MODIFIED` covers `infra/aws/globgrph`, `canon-patterns.yaml` and `org/modules/graph/debtscan`
on two arms (committed and working-tree) -- wider than the two files the cell named. The one thing a byte
scan cannot see, said plainly on the script: an act leaving no byte here; the change-management arm is the
independent plane for that, and it is empty for this serial.

The only live-plane act this order took was a READ: Cypher against the projection service, which the order
expressly permits.

## 6. THE READING (H5-AC5) -- a reading act; NO verdict; `3.0.0_SA_CVO` grades this at L9

**(a) Is a scorer adopting a defect as canon a scorer bug, or a signal that the canon was never checked
against the producer that fills it?**

Neither, on the evidence, and the third answer is the useful one. `debtscan_canon_scorer.py:48` is not a
mistake in the ordinary sense: it is a per-class SOURCE PROVENANCE entry, written deliberately under a CTO
auditability rider so that the canon-to-source decision would be *visible* rather than buried in logic. The
seat that wrote it looked at the live graph, saw `ServedURL-SERVED_FROM->S3_BUCKET_POLICY`, and recorded
what it saw. **It was doing the right thing -- recording the live shape rather than the idealized one --
and it recorded a defect, faithfully.** The canon's own comment at `:124` shows the same seat-cluster
noticing the drift on 2026-07-18 and correctly REFUSING to rewrite the motif blind. So the failure is not
that nobody checked; it is that the check produced an OPEN QUESTION, the open question was written down in
a comment, and a comment has no owner and no un-park condition. **The defect propagated through the
mechanism built to make it visible.** That is the finding: an auditability rider records what IS, and when
what is happens to be wrong, the rider is the propagation path. A provenance field wants a claim about its
own status -- `measured/inferred/held` -- exactly as CLAUDE.md requires of a value; `SCORED_FROM` carries a
shape with no field a consumer could reject on, and that is the repair worth more than either branch.

**(b) Is a scored artifact carrying a wrong class more dangerous than the wrong class itself?**

Yes, and this census can say why in numbers rather than in principle. The wrong class in the graph is 27
edges that a re-derive corrects in one act, and it is FALSIFIABLE: anyone who asks the graph gets the
current answer. The wrong class in `debtscan_scorecard_latest.json` is a dated, signed, non-re-derived
record that answers the question *without being asked again* -- and the census found it copied onward into
a CLOSED task order's `<status>` field, two proof-of-spec instances, a CVO assessment JSON, and fourteen
prose documents. 21 of 28 consumers carry it. **The graph's error has a lifetime; the artifact's error has
a readership.** And the asymmetry gets worse after the fix: the moment the graph is corrected, the graph
stops being wrong while every artifact stays wrong AND stays consistent with every other artifact -- a
closed loop of agreeing records with no member still connected to the thing they describe. That is the
laundering: not that the record is wrong, but that after the world is fixed the record is the only
remaining witness and it is unanimous.

**(c) Is parking this right at all, or does the deploy clock make it someone's now?**

Parking is right, and the measurement is what makes it right rather than convenient. The clock the cell
inherited was `the morning after the re-point, debtscan's census reads 100 percent outliers` -- an
imminent, loud, dated failure. That clock does not exist (s.3). What exists is a declaration that becomes
false on an act that is Andrew-gated and not scheduled, in a file whose owning project closed on
2026-08-25, whose delete was cleared 62 days ago and never executed. **Nothing degrades while this sleeps,
and the un-park condition is a one-statement query anyone can run.** Dispatching it now would take a seat
off live work to change two strings in a scorer that may be deleted instead.

But the honest version of that answer has a caveat, and it is the reason the carrier names a SECOND
trigger. **The un-park condition fires on the deploy; the DAMAGE fires on the first scorer re-run after
the deploy**, and those are different events with no ordering guarantee between them. If the re-point
lands and someone regenerates the scorecard before anyone reads this file, the false provenance line is
already in a new dated artifact -- the parked item will have been correct, on time, and too late. **A park
is safe when the un-park condition precedes the harm. Here it merely correlates with it**, which is the
strongest argument for branch 2 or 3: an artifact that no longer exists cannot be regenerated wrong.

---

## HOW TO RE-RUN EVERYTHING HERE

```
timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_consumer_census.py
timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_disagreement.py
timeout 120 bash   org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_placement.sh
timeout 120 bash   org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_no_egress.sh
```

`h5_disagreement.py` reads the live projection service, so its served counts carry that day's vintage;
`CONSUMERS_FOUND` moves if the estate gains or loses a file that declares the shape -- both are features,
and both print their denominator.

## SURPRISE ROWS FILED

- **`NFRA_CLDGRPH-W4-S7`** (OBSERVATION, **ARMED**, disarm `0.7.0_AE_CloudOps`) -- the predicted 100
  percent outlier rate is not reproducible; the real failure is silent.
- **`NFRA_CLDGRPH-W4-S8`** (OBSERVATION, INERT, disarm `2.0.0_SA_COO~A`) -- an ordered READ-ONLY surface
  is untracked and absent from every linked worktree.
- **`NFRA_CLDGRPH-W4-S9`** (OBSERVATION, INERT, disarm `2.0.0_SA_COO~A`) -- the face says row ids start at
  S1 for this slot; W4-S1..S6 already exist.
