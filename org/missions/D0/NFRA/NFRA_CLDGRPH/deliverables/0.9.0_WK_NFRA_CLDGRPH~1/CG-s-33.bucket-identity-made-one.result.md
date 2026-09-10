# CG-s-33 -- THE BUCKET IDENTITY MADE ONE, AT BOTH PLANES, ON A LOCAL FOLD

**Task order:** `NFRA_CLDGRPH.TO-CG-G-2` (cell CG-s-33), face at `@c16e3a4986` including the
CTO's 95004 RETIRE ruling.
**Worker:** `0.9.0_WK_NFRA_CLDGRPH~1`, branch `wk-cldgrph-7-1`.
**Status: the order is NOT flipped.** The RULED-unconditional half is done and its four
mechanical criteria pass. The RETIREMENT of `STORED_IN` is **BLOCKED** by condition 1 and
stopped exactly where the condition says to stop it -- row `NFRA_CLDGRPH-W1-S37`.

**Read only against the world.** No ECS run-task, no CodeBuild start, no image build/push,
no digest re-pin, no `safe-apply`, no S3 write, no act whose effect is an SNS publish.
Proven, not asserted: `G2-AC4`.

---

## 1. WHAT THE DEFECT ACTUALLY WAS -- the join's key rule, found and cited

The census in CG-s-32 said *where* the edges landed. This order had to find *why*, and the
answer is one line in a file neither producer owns:

```
kuzu_nessie_load.py:204   key = graph_key(row.get("arn")) or graph_key(row.get("node_id"))
kuzu_nessie_load.py:249   src = graph_key(row.get("src_id"))      # endpoints matched RAW
```

**A node's SERVED key is `arn if present else node_id`, and edge endpoints are matched raw
against that key space.** In the derive graph, measured on the real `snapshots/20260910`
artifact, an `S3_BUCKET` node carries `id='opal-data-bd'` and `arn='arn:aws:s3:::opal-data-bd'`,
so its served key is the **ARN**. An `S3_BUCKET_POLICY` node carries `id='opal-data-bd'` and
`arn='opal-data-bd'` -- **the bucket's NAME in its own arn column** -- so its served key is
the **NAME**. An edge built onto the name therefore does not dangle. It lands on the policy.
Every dangling check in the estate read clean while 162 boundary facts pointed at the wrong
class.

That is why this is a JOIN defect and not an edge-builder defect, and it is why the CTO put
the normalization at the fold.

## 2. WHAT CHANGED, both planes, in one act

**THE FOLD (`derive_runner.py`)** -- `canonical_node_key()` restates the join's own rule at
the derive; `_canonical_endpoint_aliases()` builds `alias -> canonical` for every two-named
node and **refuses** any alias two resources claim; `normalize_edge_endpoints()` rewrites
every edge endpoint once, after every producer fold and before drop/relabel/commit, so one
pass covers all of them; `_stitch_endpoint_keys()` widens the fold's both-ends ADMISSION to
hold both identities.

**THE PRODUCERS** -- `derive_stitch._index_aws` now yields `arn or nid` for a bucket
(34 of 34 canonical, measured on the real snapshot), reversing CG-s-31's `nid or arn` with
the ruling recorded in the docstring rather than left contradicting the code. And
`derive_runner.stitch_served_from` now takes `canonical_node_key(n)` instead of
`n.get("id")` -- which is what **its own docstring already claimed** it did: *"the edge
targets that node's ACTUAL node_id (the arn-form id ...) NOT ... the bare bucket-name
(which would dangle)"*. It was handing back the bare bucket name. It did not dangle; it
landed on the policy, 27 of 27 times.

**WHY BOTH HALVES HAD TO MOVE TOGETHER, mechanically.** Round 6 measured the fold admitting
`0 of 955` when the edge named the ARN. That is not a historical note -- it is what would
have happened to the producer change alone, because `fold_stitch_document`'s both-ends test
held short ids only. Fixture arm 6 exercises exactly that: `admitted=1 of 1` with the
canonical endpoint, against a pre-fix id set that would have admitted `0 of 1`.

## 3. THE MEASUREMENTS

| accept | measured | denominator |
|---|---|---|
| `G2-AC1` | `FIXTURE_ARMS=6 of 6 passed`, `NEGATIVE_CONTROL=FIRED` | 4 fixture graphs, 11 nodes, 5 edges; 1 mutant run |
| `G2-AC2` | `STORED_IN 137 of 137` and `SERVED_FROM 27 of 27` on `S3_BUCKET`; `ON_S3_BUCKET_POLICY=0 across both families`; `DERIVES_FROM_RESOLVED=216 of 216` | 3 of 3 families, 59,887 resolved edges, `snapshots/20260910/graph-20260910.tar.gz` |
| `G2-AC3` | `RECONCILED admitted=1790 merged+created=1790 lost=0`; `GRAIN-SENTINEL: PASS`; `MAGNITUDES_UNCHANGED=5 of 5` | 1 artifact, 27,688 nodes, 5 signed magnitudes |
| `G2-AC4` | all five counters `0`, `EGRESS_PROBE_CONTROL=FIRED` | 3 watched objects, 596 executable lines, 5 of 5 planted acts caught |

**THE BEFORE/AFTER, on the same snapshot, through the same simulated join:**

```
BEFORE   STORED_IN    {'S3_BUCKET_POLICY': 135}   keys=135
         SERVED_FROM  {'S3_BUCKET_POLICY':  27}   keys=27
AFTER    STORED_IN    {'S3_BUCKET':        137}   keys=137
         SERVED_FROM  {'S3_BUCKET':         27}   keys=27
```

**The 137 is not a typo and it is not fan-out.** `resolvable_before=64078`,
`resolvable_after=64080`: the widened admission **recovered the two edges** that were
round 6's `135 of 137`. One fact per key holds -- 137 edges over 137 keys.

**`SERVED_FROM` never needed the rewrite.** `by_edge_type={"STORED_IN": 137}` -- the
normalization touched only `STORED_IN`, because the patched `stitch_served_from` emitted its
27 endpoints canonically at source. Producer and fold each did their own half, visibly.

## 4. WHAT A LOCAL FOLD CAN AND CANNOT PROVE

It proves what the **next derive would commit**: these are the real snapshot's bytes, the
real stitch artifact verified sha256-against-its-own-marker, the real `fold_stitch_document`
and the real `normalize_edge_endpoints`, with the join re-implemented from
`kuzu_nessie_load`'s own two lines. It does **not** prove the served plane, and nothing in
this record should be read as a served claim. The served re-take belongs to the same
deferred pass that owes `F11-AC3`'s, gated on the egress hold.

Two honest limits on the numbers above, neither absorbed. The grain sentinel's own coverage
line says `35 of 59 live node type(s) band-checked; 24 UNCOVERED` -- its PASS is a pass over
35 types, not 59. And the join re-implementation is *my* reading of two cited lines; it
agrees with the served plane on the BEFORE figures (135 and 27, exactly CG-s-32's census),
which is the only cross-check available under the hold, and that agreement is corroboration
on one axis, not proof of the loader.

## 5. THE RETIREMENT: CENSUSED, AND BLOCKED WHERE THE CONDITION SAYS TO BLOCK

Condition 1 was executed as a **subtraction**, unscoped, and the result is the most
interesting number in this order:

```
MANIFEST_CONSUMER_DENOMINATOR: 78 tools, 128 entries      MANIFEST_TOOLS_TOUCHING_STORED_IN = 0 of 78
UNSCOPED_SWEEP: 31,293 tracked files -> 52 carry the literal
  MINUS 7   this order's own artifacts
  MINUS 11  another worker's round-6 deliverables (carried into the blocking read, not dropped)
  MINUS 30  prose-only (comment, docstring, .md, JSON prose field)
  =     7   surviving consumers: 2 IN-PATHS, 5 OUT-OF-PATHS
RETIREMENT_BLOCKED=true
```

**The manifest-scoped census would have returned EMPTY and authorized the retirement.**
78 of 78 declared tools touch `STORED_IN` zero times; the five real consumers are all
outside the declaration. That is Rule 22's shared-dependency limb arriving on a retirement
question, and it is why condition 1's own denominator is not sufficient for condition 1's
own decision. Row `NFRA_CLDGRPH-W1-S38`, ARMED, because the next retirement will be
censused the same way.

The five outside the grant, each with its line, are in row `NFRA_CLDGRPH-W1-S37`. Nothing
outside `<paths>` was edited and the grant was not widened. **Condition 2 is blocked by the
same wall** and was measured, not attempted: `OWNED_BY`'s meaning is consumed by
`cse_schema.py:323` (mapped to `Relationship.OWNS`), `comp_marker_read.py:121`
(`_DRILL_REVERSE`, a rollup seam) and `comp_coverage_check.py:523` (fine->coarse parent) --
absorbing LOCATION into a term three tools use as a CONTAINMENT seam is a semantic change to
those tools, not a docstring edit. **Condition 3** (absence with a positive control) is not
reached: there is nothing to prove absent, because nothing was retired.

## 6. THE CONSEQUENCE FOR THE SCORERS, MEASURED AND NOT REPAIRED

`EDGES_TOUCHING_S3_BUCKET_POLICY_AFTER=0 of 59,887`. The two families that landed there were
that class's **only** edges, in either direction, so after this change `S3_BUCKET_POLICY`
becomes an island. `debtscan_canon_scorer.py:48` and `:144` declare
`ServedURL-[SERVED_FROM]->S3_BUCKET_POLICY` as AUTH_CANON's live shape and **will** score
differently -- its dominant shape and its outlier threshold both move. Neither scorer was
edited; both are outside this order's `<paths>` and the order says so explicitly.

## 7. THE SEAM SHED 124 FACTS WHILE THIS ORDER WAS RUNNING

Between CG-s-32's read (served vintage `03:31:02`) and a re-read at `05:32:57`, with the
snapshot, the stitch artifact and its marker **all unmoved** at `03:01-03:02`:

```
STORED_IN -> S3_BUCKET_POLICY   135 -> 11        S3_BUCKET_POLICY nodes  15 -> 14
total edges                  59,683 -> 59,559    total nodes         27,665 -> 27,664
OWNED_BY S3Key -> S3_BUCKET     232 -> 232 (unchanged)
```

One policy node left the graph and took 124 boundary facts with it. No derive stands behind
it. **The correctly-parented family did not move at all** -- which is the counterfactual, and
the argument for this fix stated by the world rather than by me. Row
`NFRA_CLDGRPH-W1-S39`, ARMED; why the node left is the projection owner's question, not this
lane's.

## 8. DOES NORMALIZING AT ADMISSION RISK A PRODUCER THAT ALREADY EMITS ARNS?

No, and it is measured rather than argued. An endpoint already canonical maps to itself and
is skipped (`ARN_ENDPOINT_UNCHANGED`), an endpoint on a one-named node is untouched
(`SINGLE_IDENTITY_UNTOUCHED`), and the pass is **non-losing by construction** because it maps
one present key to another present key -- `resolvable_before` and `resolvable_after` are both
counted and printed on every run, and a fall would print its own WARN. On the real snapshot
they read 64,078 and 64,080.

The one real bound: **18 short names in this estate are claimed by two resources** (an
EventBridge rule and a Lambda; an IAM role and a Lambda; a CodeBuild project and a role), and
the fold refuses all 18 rather than guessing, printing both claimants each time. No edge in
today's graph is affected. Row `NFRA_CLDGRPH-W1-S40`.

## 9. HOW TO RE-RUN

```
timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/g2_fixture_fold.py
timeout 120 bash  org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/g2_local_fold.sh
timeout 120 bash  org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/g2_local_fold.sh --reconcile
timeout 120 bash  org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/g2_no_egress.sh
timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/g2_reader_census.py
```

Every one is a read plus arithmetic. The fixture touches no network at all.

## 10. ROWS FILED

`W1-S37` BLOCKING/INERT -- the retirement blocked, five readers named with their lines |
`W1-S38` OBSERVATION/ARMED -- the manifest-scoped census would have read EMPTY |
`W1-S39` OBSERVATION/ARMED -- 124 served facts lost with no derive behind it |
`W1-S40` OBSERVATION/INERT -- 18 aliases the fold must refuse |
`W1-S41` OBSERVATION/INERT -- `G2-AC4`'s shell-history instrument substituted upward |
`W1-S42` OBSERVATION/INERT -- the `g1_`/`g2_` prefix carry-over in STANDING LAW.
