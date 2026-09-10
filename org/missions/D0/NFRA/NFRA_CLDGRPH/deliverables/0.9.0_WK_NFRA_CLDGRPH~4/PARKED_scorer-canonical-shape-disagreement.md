# PARKED: two scorers and the ratified canon declare different shapes for ONE edge, and the wrong one is baked into a scored artifact

**Parked by:** `0.9.0_WK_NFRA_CLDGRPH~4` 2026-09-10, on task order `NFRA_CLDGRPH.TO-CG-H-5` (cell CG-s-40).
**Source:** `1.0.0_SA_CTO` round-7 analysis @`bb08a2ac62` s.6 item 5, and the adjudication
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ADJUDICATION_NFRA_CLDGRPH_20260910T052xZ_RETIRE_STORED_IN_BUT_A_PRODUCER_CENSUS_IS_NOT_A_CONSUMER_CENSUS.md`
lines 97-104, in the CTO's own words: *"PLACED for its owner with the reason stated; it is not round 7's
and must not be widened into it."*
**Status:** PARKED. Not a task order, not a dispatch, not a fix. **No scorer file was edited to produce
this file, on either branch** -- the item is outside NFRA_CLDGRPH's plane and this carrier does not reach
into it.

## Why this file exists rather than a message

A placement with no carrier is a silent hole: an item that lives only in a message reads as delivered and
is owed by nobody. CLAUDE.md: *"Address a LIVE recipient, or PARK the item on its own carrier with an
OWNER and the CONDITION that un-parks it."* Both fields are populated below.

---

## THE ONE SENTENCE AN OUTSIDE READER CAN ACT ON

**`debtscan_canon_scorer.py` declares `AUTH_CANON`'s live shape as
`ServedURL-[SERVED_FROM]->S3_BUCKET_POLICY`, which is TRUE of the served graph today (27 of 27 edges) and
becomes FALSE the morning the already-committed CG-s-33 re-point deploys -- and when it does, NOTHING IN
EITHER SCORER WILL RAISE, SPIKE OR CHANGE A NUMBER, because both scorers' declarations are literal strings
and both scorers' arithmetic is class-agnostic; the only thing that changes is which of them is lying.**

## THE DISAGREEMENT, MEASURED

| | shape | declared at (@`2fd5cae09f`) | matches SERVED today | matches COMMITTED re-point |
|---|---|---|---|---|
| **A** | `ServedURL-[SERVED_FROM]->S3_BUCKET_POLICY` | `infra/aws/globgrph/debtscan_canon_scorer.py:48` (`SCORED_FROM`), `:144` (docstring) | **YES** (27 of 27) | no |
| **B** | `(ServedURL)-[SERVED_FROM]->(S3)` | `infra/aws/globgrph/canon_motif_scorer.py:94`, `:131` (the emitted `dominant_motif` VALUE) | no | **YES** |

Served plane read at vintage `2026-09-10T12:24:50Z` (stitch source: stitch-codebuild built
`2026-09-10T03:01:17Z`), `edge_type` as a PROPERTY, positive control on the same statement shape
(`OWNED_BY` returns `S3_BUCKET` 232 and `MS_USER` 6153, so a single-class answer for `SERVED_FROM` is a
property of the DATA, not of the query form) and a negative control (a non-existent `edge_type` returns 0).

**AND THE RATIFIED CANON IS A THIRD AND FOURTH VOICE, not a tie-breaker.** `org/modules/graph/canon-patterns.yaml`
(CTO-ratified `ef6110129`) declares the same family:

- `:54` PIPELINE_CANON tail -- `(S3_BUCKET)-[SERVED_FROM|IS_ENDPOINT]->(ServedURL|API_ROUTE)`: **the
  opposite direction** from both scorers and from the served plane.
- `:116` SERVED_LINEAGE_CANON motif -- `(Field gold)-[SERVED_FROM]->(ServedURL)`: a different source AND a
  different target from both scorers.
- `:121` and `:137` comments record the live shape as `ServedURL->S3_BUCKET_POLICY 29`.

So the artifact both scorers claim to consume does not agree with either of them, and says so about itself
at `:124`:

> *"OPEN (untraced -- do NOT rewrite the motif blind): whether the fine Field-level SERVED_FROM lineage is
> a stitch GAP (should exist, absent) or a remodel (the coarse ServedURL->S3_BUCKET_POLICY serve edge
> replaced it). **Trace the SERVED_LINEAGE scorer's consumers (comp-blast) before replacing the motif.**"*

**That trace was asked for on 2026-07-18 and never done. It is done now and it is in this file** (28
consumers, below). The owner inherits a question that is one measurement smaller than it was.

## WHAT BREAKS ON DEPLOY, PRECISELY -- AND WHY IT IS WORSE THAN A SPIKE

`score_auth_canon` builds its shape counts from `t.node_type` AT RUNTIME (`debtscan_canon_scorer.py:160-177`),
so re-running each scorer's OWN arithmetic on both sides of the deploy gives:

| | before deploy | after deploy |
|---|---|---|
| shapes | `API_ROUTE-ROUTES_TO->LAMBDA` 86, `ServedURL-SERVED_FROM->S3_BUCKET_POLICY` 27 | `...->LAMBDA` 86, `ServedURL-SERVED_FROM->S3_BUCKET` 27 |
| dominant | `API_ROUTE-ROUTES_TO->LAMBDA` (86) | `API_ROUTE-ROUTES_TO->LAMBDA` (86) -- **unchanged** |
| threshold (`outlier_frac` 0.10) | 8 | 8 -- **unchanged** |
| outlier candidates | `[]` | `[]` -- **unchanged** |

**CORRECTION TO THE INHERITED PREMISE, and it matters for how the owner should look:** the CG-s-32 census
record predicted *"its census reads a 100 percent outlier rate the morning after"* and that is NOT
reproducible against the code as written -- the dominant does not flip, the threshold does not move, and
the outlier set is empty on both sides. Filed as `NFRA_CLDGRPH-W4-S7`. **An owner waiting for a red number
will see green and conclude nothing broke.** What actually breaks is that `:48` is the per-class SOURCE
PROVENANCE string -- recorded there deliberately so the canon-to-source decision is auditable -- and it is
COPIED VERBATIM into the emitted scorecard (`infra/aws/globgrph/debtscan_scorecard_latest.json:5` and `:26`,
`"scored_from"`, plus `:17` `"ServedURL-SERVED_FROM->S3_BUCKET_POLICY": 29`). After the deploy the audit
record keeps asserting a source shape that no longer describes the graph it scored, silently, forever.

`canon_motif_scorer.py` needs no code change on its arithmetic: `score_served_lineage` counts DISTINCT
`ServedURL` sources carrying a `SERVED_FROM` edge and never reads the target's class, so its number is
invariant under the re-point. Its LABEL is wrong today and is repaired by the same deploy that falsifies A.

## THE CONSUMER POPULATION -- 28, NOT 2

Swept by subtraction from a printed repository denominator (29,608 files opened and read in worktree
`wk-cldgrph-8-4` @`2fd5cae09f`, positive control fired), not from the list the census record happened to
name. Full output: `h5_consumer_census.py` beside this file.

| class | n | the ones that matter |
|---|---|---|
| SCORER | 2 | the two named at the cut |
| PRODUCER | 2 | `infra/aws/globgrph/derive_runner.py` (the emitter) and **`org/modules/graph/debtscan/summary_corpus.py:350`**, which was NOT named at the cut |
| FIXTURE | 7 | **`infra/aws/globgrph/debtscan_scorecard_latest.json` (the scored artifact itself, 3 declarations)**, `org/modules/graph/canon-patterns.yaml` (the ratified canon), two proof-of-spec instances, two captures, one CVO assessment JSON |
| PROSE | 17 | rulings, task orders, result records, session logs -- including `NFRA_DEBTSCAN.TO-D3`'s own `<status>` field, which records the shape census as `ServedURL-SERVED_FROM->BUCKET_POLICY 29, 0 shape-outliers` inside a CLOSED order |

**21 of the 28 carry the wrong class; 15 carry the intended one; several carry both.** The defect is not
in two files. It is in a vocabulary.

---

## OWNER

**`0.7.0_AE_CloudOps`** -- verified from the RECORD, not from message authorship:

1. `org/tier2_senior/0.7.0_AE_CloudOps/task_orders/NFRA_DEBTSCAN.TO-D3.ae-canon-motif-scorer-census.md`
   carries `<assigned_to>0.7.0_AE_CloudOps</assigned_to>`, and its `<status>` field names
   `infra/aws/globgrph/debtscan_canon_scorer.py` as the artifact that order SHIPPED. Both scorer files
   open with the docstring line `NFRA_DEBTSCAN TO-D3`.
2. The 2026-07-10 message below is addressed **To: `0.7.0_AE_CloudOps`** and calls
   `canon_motif_scorer.py` *"YOUR live canon_motif_scorer.py"* and `debtscan_canon_scorer.py` *"the file
   you're deleting"*.

**NOT `0.8.0_AE_CloudComp`.** That seat WROTE the clear-to-delete; writing a clearance is evidence of
authorship, not of ownership, and it is the DEPENDENT seat in that exchange, not the owning one. (The CTO's
own note at the same commit assigns CloudComp a DIFFERENT item -- the nodes-carrier missing drop-on-read --
which is exactly the kind of adjacency that makes a wrong owner look right.)

**The lane does NOT discriminate and is recorded as non-evidence:** `.owned-paths.yaml` resolves both
scorer files to lane `CLOUD_OPS_OR_ETL`, whose `permitted_agents` list contains BOTH `0.7.0_AE_CloudOps`
and `0.8.0_AE_CloudComp` (11 serials in total). A lane check here returns a pass for either seat and
therefore proves neither.

**CO-SIGNER, on the RETIRE branch only: `1.0.0_SA_CTO`.** The 2026-07-10 message routes the delete to the
CTO in its last line of disposition -- *"Recommend to CTO: clear the CM1 delete"* -- so the retire branch
is not CloudOps's to take alone. The re-point branch is.

## UN-PARK CONDITION

**The CG-s-33 re-point reaches the SERVED plane.** Machine-testable, one statement, no judgment:

```
MATCH (s:CloudNode)-[e:CloudEdge]->(t:CloudNode)
WHERE s.node_type = 'ServedURL' AND e.edge_type = 'SERVED_FROM'
RETURN t.node_type AS tt, count(*) AS c
```

Today this returns `[{'tt': 'S3_BUCKET_POLICY', 'c': 27}]`. **The moment it returns `S3_BUCKET`, this item
is live and shape A is a false declaration in an auditable artifact.** (`edge_type` is a PROPERTY: the
typed form `MATCH ()-[e:SERVED_FROM]->()` errors at the binder, and a binder error is a wrong-form signal,
never a zero.)

**That deploy is Andrew-gated today**, not scheduled: every globgrph ECS derive publishes to a topic
carrying a live SMS subscription to a personal mobile, and the decision on that subscription is RESERVED
FOR ANDREW (rows `NFRA_CLDGRPH-W2-S72`, `-S104`, `-S106`). So the clock is real but it is not running by
itself, which is the whole reason this can be parked rather than dispatched.

**A SECOND, EARLIER TRIGGER that does not need the deploy:** anyone re-running
`debtscan_canon_scorer.py` and re-emitting `debtscan_scorecard_latest.json` after the deploy freezes the
false provenance line into a NEW dated artifact. If the re-point lands while nobody is watching the
scorecard, the first re-run is when the record becomes wrong rather than merely stale.

---

## THE 2026-07-10 CLEAR_TO_DELETE, READ IN PLACE

`org/mcp/inbox/0.7.0_AE_CloudOps/~C/read/20260710T202210Z_0.8.0_AE_CloudComp_CLEAR_TO_DELETE_debtscan_canon_scorer.py.md`
(read in place; nothing drained, nothing moved; the file is UNTRACKED in this repo, so it is reachable
only from the main worktree -- see `NFRA_CLDGRPH-W4-S8`). Verbatim where it matters:

> **Subject:** *"CLEAR TO DELETE debtscan_canon_scorer.py -- NFRA_MSGRAPH has ZERO live dep on the
> scorecard JSON; the pattern-class census re-homes to YOUR live canon_motif_scorer.py (all 4 classes incl
> DEPLOY/PIPELINE). Grounded below."*
>
> *"the only reader of debtscan_scorecard_latest.json anywhere in the tree (grep, non-doc/non-log) is
> debtscan_canon_scorer.py ITSELF -- the file you're deleting. So the delete orphans the JSON, but nothing
> else reads the JSON. No NFRA_MSGRAPH code breaks."*
>
> *"DISPOSITION: CLEAR TO DELETE debtscan_canon_scorer.py + its _latest.json output. No convergence input
> stranded; the substrate re-homes to comp-canon-motif. Legs preserved in git history AND live in
> canon_motif_scorer.py. Recommend to CTO: clear the CM1 delete."*

**Two months later the file is still at HEAD, and it has been MAINTAINED since.** `git log --full-history`
on it: the last substantive commit is `7f0a9d249c` (2026-09-05, `0.9.0_WK_NFRA_CLDGRPH~2`,
`port(NFRA_CLDGRPH TO-CG-D-7 / CG-s-8, R7)`) -- this very project PORTED the cleared-for-deletion scorer
onto `projection_client`, giving it a new live dependency 57 days after it was cleared to delete. Nobody
in that chain was wrong; nobody was carrying the clearance either.

## THE BRANCHES -- three, and the decider between them

**BRANCHES_OFFERED=3. This carrier does NOT choose.** A placement that arrives pre-decided is an
instruction from a seat with no authority to give one.

1. **RE-POINT.** Update A's two declarations (`:48`, `:144`) and B's label (`:131`) to whatever the
   deployed edge actually says, and the canon's `:54`/`:116`/`:121`/`:137` with them. Cost: four files,
   no behaviour change, and a standing obligation for four declarations to keep agreeing with one graph.
2. **RETIRE.** Execute the 2026-07-10 disposition: delete `debtscan_canon_scorer.py` + `debtscan_scorecard_latest.json`.
   Removes 2 of the 21 wrong-class-carrying FILES outright -- and, more to the point, removes the SCORED
   ARTIFACT that launders the wrong class into an audit record. Needs the CTO co-sign the message already recommended.
3. **BOTH ARE LIVE** -- retire A, re-point B and the canon. This is the only branch under which the
   estate ends with ONE declared shape for this edge instead of four.

**THE DECIDER, as one question with a measured answer already attached:**

> **Does anything other than `debtscan_canon_scorer.py` itself read `debtscan_scorecard_latest.json`
> today -- and does `score_reachability_canon`, the 5th class that was WIP in 2026-07, live only in
> `debtscan_canon_scorer.py`?**

Re-measured for this placement, 2026-09-10, `comp-find 'debtscan_scorecard_latest'`, denominator **29,624
files scanned, 73 hits across 41 files**:

- **CODE naming the artifact: exactly ONE file, `infra/aws/globgrph/debtscan_canon_scorer.py` -- the
  writer.** The 2026-07-10 claim reproduces two months later.
- Everything else is a doc, a session log, a rail log or an audit archive copy -- with ONE exception the
  owner should look at before deleting: `org/tier1_exec/4.0.0_SA_CRO~A/deliverables/NFRA_C3MATERIALIZE.TO-L2-CROA/L2_VIEW_ARTIFACTS.json`
  DECLARES the artifact as a view input. A declaration is not a read, but it is a claim someone made, and
  it is one file to open.
- The second half of the question is NOT measured here: the 2026-07-10 message mentions CloudOps's
  *"uncommitted `score_reachability_canon` WIP: additive (a 5th class)"*. Whether that leg ever landed in
  `debtscan_canon_scorer.py` and would die with it is the owner's read, in the owner's own history.

**If the answer is "nothing reads it": branch 2 or 3 is cheaper than branch 1 and strictly reduces the
number of places this estate declares this edge. If something reads it: branch 1, and the re-point must
reach the CANON too, or the next scorer built from `canon-patterns.yaml` inherits the fourth shape.**

---

## WHAT NOBODY SHOULD DO IN THE MEANTIME

- **Do NOT edit either scorer file under NFRA_CLDGRPH.** The CTO placed this outside that project's plane;
  editing it there would be a project reaching into a surface it was told it does not own, under an egress
  hold that stops it proving the change anyway.
- **Do NOT rewrite `canon-patterns.yaml`'s motif to match the graph "while we're in there".** The canon's
  own comment at `:124` forbids exactly that (*"do NOT rewrite the motif blind"*) and names the trace that
  must come first. The trace is above; the reading of it is still the owner's.
- **Do NOT run the globgrph derive, an ECS task, a CodeBuild or a `safe-apply` to "make the graph agree".**
  Every derive publishes to a topic with a LIVE SMS subscription to a personal mobile; that decision is
  RESERVED FOR ANDREW and is not a scorer question.
- **Do NOT delete `debtscan_scorecard_latest.json` as tidy-up ahead of a decision.** It is the physical
  evidence that a wrong class reached an auditable artifact, and it is branch 2's own record of what it
  removed.
- **Do NOT read the `STORED_IN` retirement as covering this.** `1.0.0_SA_CTO`, same adjudication, line 91:
  *"`SERVED_FROM` IS RE-POINTED, NOT RETIRED, and I am saying so explicitly so 'retire' is not read as
  covering the seam."* `STORED_IN` is at 0 edges on the served plane today; `SERVED_FROM` is at 27 and
  still lands on the shadow class.
- **Do NOT wait for a red number.** See the correction above: on the arithmetic as written there isn't one.

## PROVENANCE OF THIS FILE

Every number above was measured in worktree `C:/tmp/wk-cldgrph-8-4` on branch `wk-cldgrph-8-4` at
`2fd5cae09f`, by `h5_consumer_census.py` and `h5_disagreement.py` beside this file, whose full captures are
`h5_ac1_capture.txt` and `h5_ac2_capture.txt`. The served-graph vintage is printed in the capture. No file
outside this deliverables folder was modified to produce it, and `h5_no_egress.sh` measures that claim
rather than asserting it.
