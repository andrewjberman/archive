# CG-s-41 -- THE KEY COLLISION, SETTLED THEN CLOSED AT THE WRITER

**Task order:** `NFRA_CLDGRPH.TO-CG-I-1.key-collision-settled-and-closed`
**Worker:** `0.9.0_WK_NFRA_CLDGRPH~1` -- worktree `C:/tmp/wk-cldgrph-9-1`, branch `wk-cldgrph-9-1`, cut at `0596d4fc98`
**Vintage of every live number below:** `2026-09-10T12:24:50.576632+00:00`, the branch-head marker the writer itself stamped. `graph_nodes` snapshot id `8962011897599565293`, agreeing with the marker.
**Push state:** LOCAL. **Deploy state:** NOTHING DEPLOYED.

---

## 1. THE CONCLUSION FIRST

The root is settled, and it is not an inference any more.

**The incremental updater's upsert filter matches a row by the RAW `node_id` column, and `node_id` is a short name that more than one node class can hold.** `table.overwrite(rows, filter)` is DELETE(filter) then APPEND(rows), so a row matched by the filter and not re-appended is destroyed. For `S3_BUCKET`, the filter's `node_id` limb names the `S3_BUCKET_POLICY` row of the same bucket -- whose own canonical key IS the bare bucket name -- and destroys it.

**The destroyed row, named:** the `S3_BUCKET_POLICY` row whose `node_id` equals the bucket name.
**The limb it matched on:** `node_id`. Not `arn` -- the bucket's `arn` column holds the full `arn:aws:s3:::<bucket>`, which no policy row carries.

**Three rows are already gone,** and this is measured on two independent planes rather than argued: `opal-data-bd`, `opal-data-cot`, `opal-data-inf` each have a LIVE bucket policy on the AWS control plane and NO `S3_BUCKET_POLICY` row in the warehouse -- and they are exactly the three buckets the Lambda has ever written (`source='incremental'`, 3 rows of 27,685). The falsifier cell for that attribution -- a bucket with a live policy, no row, and no Lambda write -- is EMPTY, 0 of 34.

**And the collision is wider than the cell states.** Filed as row `NFRA_CLDGRPH-W1-S49`.

---

## 2. AC1 -- THE SETTLE, AND THE INSTRUMENT NOBODY HAD USED

Row `W3-S19` labelled this INFERRED and said Trino or Athena would settle it, and that order had no grant. Neither was needed.

**The warehouse rows are readable from this laptop, with a READ.** `lambda_function.py:548-564` publishes `warehouse/_branch_head.main.json` to S3 for exactly this purpose, in its own words *"so dev-box readers (which cannot reach Nessie REST) learn HEAD from an S3 object"*. It carries the `metadata_location` of `graph_nodes`. `pyiceberg.table.StaticTable.from_metadata(<that location>)` then opens the table and `.scan()` returns the rows. The instrument the estate built to solve a different problem answers this one.

| arm | plane | instrument | what it settled |
|---|---|---|---|
| A | warehouse | `pyiceberg 0.9.1` StaticTable over S3 data files | 27,685 of 27,685 rows. `S3_BUCKET`=34, `S3_BUCKET_POLICY`=12, `source='incremental'`=3. Policy rows carry the BARE BUCKET NAME in BOTH `node_id` and `arn`, 12 of 12. |
| B | AWS control plane | `boto3 s3:GetBucketPolicy`, 34 of 34 buckets | live policy PRESENT=15, ABSENT=19. Destroyed cell (live policy, no row, Lambda-touched) = **3**. Falsifier cell (live policy, no row, untouched) = **0**. |
| C | filter replay | the writer's own predicate over arm A's rows | 12 of 34 buckets whose next upsert destroys a foreign-class row, `matched_on=node_id` every time. |

Arms A and B share no instrument, no service and no substrate. Confirming arm A with arm A would have been repetition.

**Provenance:** every number in this section is `measured`. Nothing here is `held`.

---

## 3. AC2 -- THE LAYER, WITH THE WRITERS COUNTED

**`KEY_SPACE_WRITERS=3`, counted rather than assumed**, by an UNSCOPED census first (135 hits across 30,050 files scanned) and only then narrowed (26 hits across 6,753). 52 candidate files, 49 subtracted with a per-file reason, 3 remain:

| writer | verb | can it destroy a foreign row? |
|---|---|---|
| `infra/aws/globgrph/derive_runner.py:346` | full-table overwrite | **No** -- it replaces the whole table; it has no delete predicate. |
| `org/modules/graph/comp_aws_cli.py:3201` | full-table overwrite | **No** -- same. (But see row `NFRA_CLDGRPH-W1-S50`.) |
| `infra/aws/lambda/globgrph/incremental_updater/lambda_function.py:501,504` | **filtered** overwrite / delete | **Yes.** The only one of the three that deletes BY KEY. |

That asymmetry is the whole argument for the layer, and it is measured: **the collision needs two producers' conventions to exist, but only ONE writer to destroy.**

Four layers were enumerated -- the three places a key can be decided (write-time predicate / table identity / read-time fold) plus the one place the ambiguity is minted (the producer of the contended string):

| layer | closes it for BOTH classes? | why |
|---|---|---|
| **L1 writer match filter** | **YES** | Strict narrowing of the delete predicate; closes all five colliding pairs, both directions. |
| L2 table key definition | in principle only | Iceberg enforces no primary key, so a composite identity is honoured only by a writer's predicate. It is L1 **plus** a migration, not an alternative. |
| L3 fold admission (`CG-s-33`) | **NO -- masks** | It rewrites EDGE endpoints. It touches no node row and no delete predicate. Nothing in `normalize_edge_endpoints` is reachable from `commit_batch`. |
| L4 policy producer key | **NO -- one pair of five** | It could fix the S3 pair at its source, but a Lambda and its execution role sharing a name is CORRECT, not a defect, and renaming cannot close those. Also outside this order's `<paths>`. |

**`LAYER_CHOSEN=L1_WRITER_MATCH_FILTER`.**

**What the fix does NOT move,** named rather than left implicit:
- It does **not** stop two classes SHARING a `node_id`. 30 strings still collide. It stops the sharing from being DESTRUCTIVE.
- It does **not** change which node a short-id edge endpoint resolves to in the served graph. That is L3 / `CG-s-33`, which stays necessary.
- It does **not** repair the three policy rows already destroyed; the nightly derive rewrites them.
- It leaves a **stale** foreign-class row after a genuine delete (a bucket's policy row outlives the bucket until the nightly derive). That is the accepted cost of narrowing, and it is the state the graph was in before the collision began.

---

## 4. THE FIX

One file: `infra/aws/lambda/globgrph/incremental_updater/lambda_function.py`. 143 lines added, 35 removed. Committed, **not deployed**.

**The rule:** *an ARN identifies a row on its own; a short `node_id` NEVER does, and is only ever used conjoined with its `node_type`.*

Four sites, because the collision had **three mouths**, not one:

1. **`_match_filter` (:391)** -- signature `(arns, ids)` becomes `(keys)` of `(arn, node_id, node_type)`. `In("arn", arns) OR In("node_id", ids)` becomes `In("arn", arns) OR And(In("node_id", ids_of_type_t), EqualTo("node_type", t))` per type. A key with neither an ARN nor a type contributes nothing and **logs that it does** rather than silently matching nothing.
2. **`commit_batch` (:436)** -- the second mouth: `up_arns = [(n.get("arn") or n.get("id")) ...]` put a BARE NAME into the `arn` limb, and a policy row carries the bare name in ITS `arn` column. The fallback is gone.
3. **`delete_keys_from_event` (:163)** -- returns 3-tuples; every branch names the class it may remove. The generic `resources[]` fallback carries `None` and is therefore matched **by ARN only**, never by its short name.
4. **`handler` (:715)** -- the third mouth: the create-then-delete cross-set drop unioned arns and bare ids, so a `DeleteFunction` would drop the upsert of a same-named IAM role from the batch. The ARN limb stays global; the name limb is now class-aware.

**It is a STRICT NARROWING:** every row the new predicate deletes, the old one also deleted. Its blast radius is bounded by construction, not by argument. `KEY_SPACE_WRITERS=3` and the other two have no delete predicate, so neither is affected. No schema change, no re-derive, no reader re-keying, no served-graph change.

---

## 5. AC3 -- THE ARM WENT RED FIRST

Not a mock. A real Iceberg table (`pyiceberg` `SqlCatalog` + local warehouse), the real 9-column `graph_nodes` schema, the real `table.overwrite(rows, overwrite_filter=F)` verb. The PRE-FIX predicate is **extracted from `git show HEAD:<file>`** -- retyping it would have tested my memory of the bug. The POST-FIX predicate is **imported from the module on disk**.

```
BASELINE_RED_CAPTURED=true      (capture: i1_arm_red_capture.txt, 3125 bytes)
DESTROYED_BEFORE=2              S3_BUCKET_POLICY killed by an S3_BUCKET upsert;
                                IAM_ROLE killed by a LAMBDA upsert
DESTROYED_AFTER=0
UPSERT_STILL_REPLACES=true      exactly 1 own-class row after, in every arm --
                                the narrowing did not turn the upsert into a duplicate
DISTINCT_KEYS_BOTH_SURVIVE=true
NEGATIVE_CONTROL=FIRED
```

Two colliding pairs were seeded, not one: a fix demonstrated on one pair is a fix demonstrated on one pair. The **delete** path was exercised in the same run: `DeleteBucket opal-data-bd` now removes the bucket row and leaves the policy row untouched, where before it removed both.

---

## 6. SERVED_FROM's 27 -- DEMONSTRATED, NOT ASSERTED

Measured live: `SERVED_FROM=27`, `STORED_IN=137`, `OWNED_BY=6385` (the positive control the cell names, non-zero, so a zero would have been visible as a zero).

**All 27 SERVED_FROM edges land on ONE endpoint string: `opal-data-portal-v2`** -- a `node_id` claimed by both `S3_BUCKET` and `S3_BUCKET_POLICY`, whose policy row is **still alive**. Resolved with the served loader's OWN key rule (`graph_key`, extracted by content from `kuzu_nessie_load.py`, not restated), the endpoint lands on the POLICY. All 27 are ARMED and none has fallen yet.

The contrast is the corroboration. `STORED_IN`'s endpoints -- `opal-data-bd` 124, `opal-data-inf` 11, `opal-data-mdpf` 2 -- now resolve to **NOTHING**. The policy row they landed on is destroyed and the bucket row does not answer to the bare name, because its served key is the full ARN. 124 + 11 = **the 135 that `derive_runner.py:2308` names**. The remaining 2 are on a bucket with no live policy at all, which never had a policy row to land on: a different cause with the same appearance, and the reason 137 is not 135.

Then the same arm, on the real 27 and 232 real node rows lifted from the live table:

```
SERVED_FROM_ORPHANED_BEFORE=27 of 27      (pre-fix predicate, parent policy row destroyed)
SERVED_FROM_ORPHANED_AFTER=0  of 27       (post-fix predicate, parent row alive)
NEGATIVE_CONTROL=FIRED                    (200 OWNED_BY edges unmoved in both arms)
SERVED_FROM_COVERED=YES
```

---

## 7. THE EGRESS HOLD

```
ECS_RUN_TASK_CALLS=0  CODEBUILD_STARTS=0  S3_WRITES=0  IMAGE_PUSHES=0
TERRAFORM_APPLIES=0   SNS_PUBLISHES=0     READS=6 (permitted)
EGRESS_PROBE_CONTROL=FIRED   (6 of 6 planted acts detected)
```

Counted by an AST walk over call nodes, because every script here CONTAINS the held verbs -- in the docstring saying it never calls them. A docstring is not a call node.

**The detector convicted my own harness on its first run**, of an image push and an infrastructure apply, because the control payload was embedded in the shell script and the weak-grain line scan cannot tell a payload from a command. The remedy was to move the payload onto a plane the strong grain can read and to teach the strong grain what an argv is -- **not** to soften the pattern until the number reached zero. A second correctness fix followed: the line scanner matched substrings, so an `s3://` URL beside the word "perform" scored as an S3 write. It matches whole tokens now, and still catches a real `aws s3 cp`.

---

## 8. AC5 -- THE READING (judgment; no verdict; graded by `3.0.0_SA_CVO` at L9)

**(a) Is the writer the right layer, or merely the reachable one?**

It is the right layer, and the thing that makes that more than a convenience is a measurement rather than a preference: **of the three writers of this key space, exactly one deletes by key.** The other two replace the whole table and are structurally incapable of destroying a row they did not write. A defect that only one writer can commit is closed at that writer. Had the census come back with two or three filtered writers, this answer would have inverted -- the fix would have belonged at the table's identity, because a per-writer fix on a shared seam is the per-member fix Rule 22 warns about.

But I want to be exact about what "right" covers, because there are two defects here and the writer layer closes only one. The DESTRUCTION is closed. The AMBIGUITY is not. After this fix, `opal-data-portal-v2` is still a string that two node classes both answer to, and an edge endpoint carrying that bare string still resolves to whichever of them holds it as its canonical key. That is `CG-s-33`'s territory and it remains live. Anyone reading this fix as "the key collision is fixed" will be wrong in a way that matters.

**(b) Is a key space two classes can both claim a schema defect that will recur under a different pair?**

It has already recurred, four more times, and I did not have to look far -- the unscoped read found it while a scoped one would not have. `IAM_ROLE + LAMBDA` (8), `EVENT_RULE + LAMBDA` (8), `CODEBUILD_PROJECT + IAM_ROLE` (1), `EVENT_RULE + SSM_DOCUMENT` (1). So the answer is yes, and it is stronger than "will recur": it already has, silently, and only the S3 pair was noticed because only the S3 pair had 135 edges hanging off it.

The deeper point is that **these are not naming mistakes and they must not be treated as ones.** A Lambda function and its execution role sharing a name is good practice. An EventBridge rule named after the function it targets is good practice. The estate is not going to stop doing that, and it should not. What is defective is a schema in which a resource's identity is a **short name in one column and a full ARN in another, with a rule that falls back between them**. `canonical_node_key` already states the correct rule -- ARN first, id only as a fallback -- and the failure was that the delete predicate did not use that rule; it ORed the two spaces instead. So the recurrence class is narrower and more actionable than "two classes share a key": it is **every place that treats `arn` and `node_id` as one match space instead of applying the canonical rule.** I found three such places in one file. I did not census the estate for others, and that is a real limit of this order's coverage rather than an absence.

**(c) Should `CG-s-33`'s re-point still deploy, or is it redundant once the collision is closed?**

It should still deploy, and the two are not substitutes -- they are the two halves of the same identity problem, and each leaves the other's failure standing.

The clean way to see it is to ask what each one fixes. `CG-s-33` fixes **where an edge lands**: an endpoint carrying a short id is rewritten onto the ARN, so `STORED_IN` and `SERVED_FROM` stop resolving onto a bucket policy that was never their subject. This order fixes **whether a node survives**: a class-blind delete predicate stops destroying rows it does not own. Deploy only `CG-s-33` and the edges point at the right node while the incremental updater goes on destroying policy rows -- fewer edges break, but the graph still silently loses nodes, and now they are nodes nothing points at, which is *harder* to notice, not easier. Deploy only this order and the policy rows survive while the 27 `SERVED_FROM` edges keep landing on a bucket policy that is not what they mean.

There is one honest asymmetry worth flagging to whoever sequences the deploy. **This fix is safe in either order; `CG-s-33` is safer after it.** `CG-s-33` moves edge endpoints onto ARNs, which changes which node the surviving rows are joined to; doing that while the destroyer is still live means re-pointing edges onto a population that is still being quietly thinned. The reverse -- close the destruction first, then re-point -- re-points onto a stable population. I am not issuing that as a sequencing instruction, which is not a worker's act; I am naming the ordering property I measured, because the cell asked whether `CG-s-33` becomes redundant and the more useful answer is that it does not, and that it has a preferred side of this change to land on.

---

## 9. ROWS FILED

| id | class | hazard | one line |
|---|---|---|---|
| `NFRA_CLDGRPH-W1-S49` | OBSERVATION | **ARMED** (`disarm_owner: 2.0.0_SA_COO`) | The collision is FIVE class pairs, not one; the canonical-space claim is true and does not bound the destruction, which runs in the raw `node_id` column. |
| `NFRA_CLDGRPH-W1-S50` | OBSERVATION | INERT | `graph_nodes` has a THIRD writer whose `pa.table` carries 7 columns where the live table carries 9 -- no `source`, no `props`. |

Channel denominator restated by parsing every fenced json block: **211 blocks / 282 rows before, 212 / 284 after**; highest `W1-S` index before this order was `S48`.

---

## 10. WHAT WAS NOT DONE

- **Nothing was deployed.** The Lambda change is committed on `wk-cldgrph-9-1` and nowhere else. The running function is unchanged and the collision is still live in production.
- **The three destroyed policy rows were not repaired.** The nightly derive rewrites them.
- **`org/modules/graph/comp_aws_cli.py` was not touched** -- outside `<paths>`. Its divergence is row `W1-S50`.
- **`infra/aws/globgrph/derive_runner.py` was not edited.** It is in `<paths>` and was granted "edit only if AC2 names this layer". AC2 named L1, so it stayed a read.
- **No estate-wide census** for other sites that treat `arn` and `node_id` as one match space. Named in the reading above as a limit, not reported as an absence.
