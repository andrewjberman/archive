# CG-s-39 -- WHAT REPUBLISHED THE PROJECTION

**TO** `NFRA_CLDGRPH.TO-CG-H-4` | **cell** CG-s-39 (decomp v0.11 s.1a) | **worker**
`0.9.0_WK_NFRA_CLDGRPH~3` | **worktree** `C:/tmp/wk-cldgrph-8-3` | **branch** `wk-cldgrph-8-3`
| **cut from CLOUD @2fd5cae09f** | round 8.

**READ ONLY.** No `ecs run-task`, no CodeBuild start, no image act, no `safe-apply`, no S3
write, no republish, no act whose effect is an SNS publish. 37 AWS reads, every verb asserted
against a read-only allowlist before its subprocess ran (`h4_lib.READ_VERBS`). Evidence:
`h4_no_act.sh`.

---

## 0. THE ANSWER, IN ONE PARAGRAPH

The projection was republished at `2026-09-10T05:32:57.959776+00:00` by the **projection
worker**, woken by an **EventBridge Pipe** record, because the **`opal-globgrph-incremental-updater`
Lambda** advanced the Nessie branch head at `05:32:58.799Z` (request
`234a09eb-d30b-5c8f-bc61-6af791bd9ef1`). The Lambda was itself woken by SQS-delivered
resource-change events for **S3 object writes to `opal-data-bd`** (`platinum/firm/leaderboard.json`,
`dashboard.json`, `fee_efficiency.json`, `mix_summary.json`). No seat acted; no derive ran; no
stitch ran; no build ran. **It was not a cadence.** The 124 edges were never deleted from the
warehouse: the **edges snapshot id did not move at all** across the window
(`6492629246124063416` on both sides). One **node** left the nodes table, and the projection's
incremental refresh then deleted every edge that pointed at it -- `INCR_NODE_DELTA ... delete=1`
and `INCR_EDGE_DELTA ... delete=124` in the worker's own log, with
`edges_skipped_missing_endpoint` rising 388 -> 512, **the same 124**.

**And the loss did not stop.** A fourth reading taken for this cell at
`2026-09-10T12:24:50.576632+00:00` (manifest `aebbd9ce...`) returns `STORED_IN=0` and
`S3_BUCKET_POLICY` nodes = 12. The same mechanism fired again at `12:01:42` on `opal-data-inf`
and took the last 11.

---

## 1. THE TIMELINE (H4-AC1) -- `h4_timeline.py`

`WINDOW = 2026-09-10T03:31:02 .. 05:32:57`, closed interval (each endpoint IS a served
vintage). `MARGIN = 01:00:00 .. 08:00:00`. `BUILDS_FOUND=2`. `ARTIFACT_KEYS_SWEPT=8 of 8`.
`ARTIFACT_PREFIXES_TOTAL=245` -- every build ever published under `projection/`.

> **INSTRUMENT** `s3api list-objects-v2` over `s3://opal-313476888478-globgrph/projection/`,
> delimiter `/`, auto-paginated CLIENT-SIDE. **GRAIN** one CommonPrefix == one published
> projection build, keyed by its own `committed_at`. **ENVIRONMENT** live AWS, account
> 313476888478, us-east-1, read at run time.

| IN? | instant | writer_id | mode | nodes | edges | skipped | manifest_id |
|---|---|---|---|---|---|---|---|
| no | 01:27:30.508695 | derive_runner | full | 27665 | 60312 | 577 | `9ff1aa5a019b` |
| no | 02:12:05.682041 | derive_runner | full | 27665 | 60312 | 577 | `57ce55a318c5` |
| no | 02:28:23.048900 | derive_runner | full | 27665 | 60312 | 577 | `c4d5a482e0a6` |
| no | 03:02:00.831539 | derive_runner | full | 27665 | 59683 | 388 | `e0a94e2ff376` |
| **YES** | **03:31:02.025931** | cse_producers_nightly | incremental | 27665 | 59683 | 388 | `5361815924ce` |
| **YES** | **05:32:57.959776** | incremental_updater | incremental | 27664 | 59559 | 512 | `fb4766e16fdd` |
| no | 05:40:53.132475 | incremental_updater | incremental | 27664 | 59559 | 512 | `d2b9e5e9872d` |
| no | 05:57:16.403567 | incremental_updater | incremental | 27664 | 59559 | 512 | `8ea66ca427c1` |

The three reads this cell inherits map to builds `5361815924ce` (R1, CG-s-32 baseline),
`fb4766e16fdd` (R2, the loss read) and `8ea66ca427c1` (R3, the issuer's third read) -- matched
on the served vintage string, which IS the artifact prefix, with no inference.

### THE DELTA, READ OFF THE TWO MANIFESTS

```
nodes                          27665 -> 27664    (-1)
edges (stored)                 59683 -> 59559    (-124)
edges_skipped_missing_endpoint   388 ->   512    (+124)
nodes_snapshot_id              682701759662556333 -> 3134279746947811755   MOVED
edges_snapshot_id              6492629246124063416 -> 6492629246124063416  UNMOVED
stitch source                  2026-09-10T03:01:17Z -> same                UNMOVED
writer_id                      cse_producers_nightly -> incremental_updater
```

**The edge fall and the skip rise are the SAME number.** That is arithmetic, not a hypothesis:
the 124 edges are still in the warehouse and are now unloadable because their endpoint node is
gone. It also settles what the cell called the strongest argument in the round -- the boundary
edges were parented to a policy node, and a policy node churned.

### BLIND INSTRUMENTS -- `BLIND_INSTRUMENTS=3`, each measured, none a zero

1. **S3 object version history of `projection/current.json`** -- `get-bucket-versioning` returns
   no `Status`; versioning was never enabled (Andrew-locked OFF, GLOBGRPH s.0 lock #5). One
   version, no history. *(The issuer flagged this as the most useful fact in its block, and it
   is: the instrument a reader reaches for first does not exist here.)*
2. **ECS stopped-task control-plane history** -- `list-tasks --desired-status STOPPED` returns 0
   retained tasks. ECS keeps stopped task records about an hour; the window closed hours before
   this run. **Their LOGS survive; the TASK RECORDS do not.**
3. **CloudTrail `lookup-events` for the S3 PutObject that IS the publish** -- the lookup plane
   serves management events only; an object-level `PutObject` is a DATA event. The publish act
   cannot be read from CloudTrail at any retention. The worker's own `POINTER_PUT_OK` is used
   instead.

One instrument was measured **NOT** blind and is reported as such: the Container Insights
performance stream (retention 1 day) returned 1216 events inside the window.

---

## 2. THE ACTOR (H4-AC2) -- `h4_actor.py`

`ATTRIBUTION=ATTRIBUTED` | `INSTRUMENTS_SWEPT=9 of 9` | `ELIMINATION_USED=false`.

**The binding is positive, not eliminative, and that is the point of the method.** Each build's
`_build_manifest.json` carries `nessie_commit_hash` -- the branch head the projection loaded.
Every writer that advances that head logs the SAME hash in its own `MARKER_STAMPED` line
(`infra/aws/globgrph/_provenance.py:416`). Attribution is a match on a 64-hex content identity
computed independently at both ends. Nobody is named because the others were ruled out.

| build | actor | evidence |
|---|---|---|
| `03:31:02.025931` | **ECS task, family `globgrph-cse-producer`** (writer_id `cse_producers_nightly`), the nightly CSE producer | `/ecs/globgrph-cse-producer` @03:31:02Z: `OK: MARKER_STAMPED writer=cse_producers_nightly hash=a85b5269... nodes_snap=682701759662556333 edges_snap=6492629246124063416` -- hash MATCH, nodes_snap MATCH |
| `05:32:57.959776` | **AWS Lambda `opal-globgrph-incremental-updater`** (writer_id `incremental_updater`), SQS-triggered | `/aws/lambda/opal-globgrph-incremental-updater` @05:32:58Z, request `234a09eb-d30b-5c8f-bc61-6af791bd9ef1`: `OK: MARKER_STAMPED writer=incremental_updater hash=667d3188... nodes_snap=3134279746947811755 edges_snap=6492629246124063416` -- hash MATCH, nodes_snap MATCH |

### WHAT WOKE THE ATTRIBUTED WRITER

Two Lambda invocations, `05:32:40` and `05:32:41`, each `BATCH_START records=2`, deriving five
distinct ARNs, all on `opal-data-bd`:

```
DERIVED arn=arn:aws:s3:::opal-data-bd                                    type=S3_BUCKET
DERIVED arn=arn:aws:s3:::opal-data-bd/platinum/firm/leaderboard.json     type=S3_BUCKET
DERIVED arn=arn:aws:s3:::opal-data-bd/platinum/firm/dashboard.json       type=S3_BUCKET
DERIVED arn=arn:aws:s3:::opal-data-bd/platinum/firm/fee_efficiency.json  type=S3_BUCKET
DERIVED arn=arn:aws:s3:::opal-data-bd/platinum/firm/mix_summary.json     type=S3_BUCKET
```

The first invocation stamped `nodes_snap=4193517708359833032` at `05:32:53`; the second hit
`ICEBERG_COMMIT_CONFLICT attempt=1/5`, retried, and stamped `3134279746947811755` at
`05:32:58`. **The projection built ONCE for the two stamps** -- there is no
`projection/2026-09-10T05:32:53*` prefix. The worker coalesced them.

### THE CONSUMER SIDE, FROM THE WORKER'S OWN LOG (`/aws/ecs/opal-globgrph-projection-worker`)

```
05:33:13  PROJECTION_EVENT {"kind": "pipe-filtered-records", ...}
05:33:18  INFO: INCR_HEAD_READ nodes=27687 edges=62327 nodes_snap=3134279746947811755 edges_snap=6492629246124063416
05:33:20  INFO: INCR_NODE_DELTA head=27664 cur=27665 upsert=1 delete=1 (0.0% of head)
05:33:20  INFO: INCR_EDGE_DELTA head=59559 cur=59683 upsert=0 delete=124
05:33:21  OK: INCR_REFRESH_COMPLETE {'node_upsert': 1, 'node_delete': 1, 'edge_upsert': 0, 'edge_delete': 124,
                                     'nodes': 27664, 'edges': 59559, 'edges_skipped_missing_endpoint': 512}
05:33:24  POINTER_VERIFY_OK prefix=projection/2026-09-10T05:32:57.959776+00:00/ ... node_count=27664 edge_count=59559
05:33:24  POINTER_PUT_OK key=projection/current.json vintage=2026-09-10T05:32:57.959776+00:00
05:33:29  PROJECTION_ERROR {"detail": "same-vintage artifact collision refused ...", "error": "PublicationRefused"}
```

`PROJECTION_EVENT kind=pipe-filtered-records` is the trigger, and it **falsifies the HELD
hypothesis this cell was handed.** The projection does not republish from Iceberg on its own
cadence; it republishes when an EventBridge Pipe delivers a warehouse-write record. There is no
period to find, because there is no clock. *(The issuer said: falsify it, do not confirm it.)*

### THE COVERAGE TABLE (abridged; full table in the AC2 output)

| instrument | verdict | retention | cannot see |
|---|---|---|---|
| `/aws/lambda/opal-globgrph-incremental-updater` | SEES | 14 d | the ECS derive plane |
| `/ecs/globgrph-cse-producer` | SEES | 30 d | the Lambda plane |
| `/ecs/globgrph/derive-runner` | SEES | 90 d | the Lambda plane |
| `/aws/ecs/opal-globgrph-projection-worker` | SEES | 90 d | **WHY** the warehouse moved, only that it did |
| CodeBuild `globgrph-derive-build` | SEES | AWS-managed | 57 builds retained, **0 started inside the sweep** |
| CodeBuild `opal-stitch-produce` | SEES | AWS-managed | 74 builds retained, **0 started inside the sweep** |
| CloudTrail `lookup-events` (management) | SEES | 90 d | S3 data events and Lambda Invoke -- i.e. the publish itself. Inclusive-second control run BOTH ways: `start=03:31:02` -> 50 events; `start=03:31:03` -> 50 events (both bounded at `--max-items 50`) |
| S3 pointer version history | **BLIND** | n/a | everything -- versioning never enabled |
| ECS stopped-task history | **BLIND** | ~1 h | anything older than about an hour |

---

## 3. WHY A NODE LEFT -- MEASURED WHERE MEASURED, INFERRED WHERE INFERRED

This is one layer beneath the cell's question and it is reported with its grain, because the
remedy depends on it.

**MEASURED, from source at `infra/aws/lambda/globgrph/incremental_updater/lambda_function.py`:**

* `:264-272` -- an S3 event is collapsed to bucket grain and emitted as
  `{"id": bucket, "arn": bucket_arn, "type": "S3_BUCKET", ...}`. **The `id` is the BARE BUCKET
  NAME; the `arn` is the ARN.**
* `:390-404` `_match_filter` -- `In("arn", arns) Or In("node_id", ids)`.
* `:441` + `:501` -- upsert keys and delete keys share ONE filter, and
  `table.overwrite(pa_table, overwrite_filter=combined_filter)` is `delete(filter) + append(rows)`.

**MEASURED, from the served graph (`h4_fourth_point.py`, same vintage as the fourth point):**

* `S3_BUCKET` nodes are keyed by **ARN** (`arn:aws:s3:::opal-data-bd` is present, 34 of them).
* `S3_BUCKET_POLICY` nodes are keyed by the **BARE NAME** (`opal-data-assets`, `opalinvest-portal`,
  ... 12 of them), and `opal-data-bd` is **NOT** among them.
* No node with `node_id = 'opal-data-bd'` exists at all.

**MEASURED, from source at `infra/aws/globgrph/derive_runner.py:2307`:** in this estate **exactly
one class uses a short name string as ITS canonical key -- `S3_BUCKET_POLICY`.**

**THE INFERENCE, stated as one:** the Lambda's upsert filter carries `node_id IN
['opal-data-bd']`, and the only row in the canonical nodes table keyed by that exact string is
the `S3_BUCKET_POLICY` row. The single overwrite therefore deletes it and appends one
`S3_BUCKET` row in its place. **WHAT WOULD CONFIRM IT:** a direct read of
`globgrph.graph_nodes` for `node_id = 'opal-data-bd'` through Trino or Athena -- an instrument
this order has no grant to run. **WHAT IS ALREADY CERTAIN WITHOUT IT:** a node left, 124 edges
went with it, and the Lambda's own `BATCH_END nodes_deleted=0` did not see it.

---

## 4. THE FOURTH POINT (H4-AC3) -- `h4_fourth_point.py`

`SERVED_VINTAGE=2026-09-10T12:24:50.576632+00:00` | `MANIFEST_ID=aebbd9cef8c4cfd5515c42dc75793cf4ffcee1f57ad91f444d01be8ea968d5da`
 |  `QUERY_FORM=edge_type-as-property`.

**NEGATIVE control (row W1-S112's trap, exercised rather than quoted):**
`MATCH ()-[e:STORED_IN]->()` RAISED -- *"Binder exception: Table STORED_IN does not exist."* A
binder error is a wrong-form signal, never a zero, and running it proves the zero below came
from the working form.

**POSITIVE control:** `OWNED_BY=6385` through the identical statement shape, same run.
`POSITIVE_CONTROL=FIRED`.

| vintage | STORED_IN | S3_BUCKET_POLICY | nodes | edges | OWNED_BY | source |
|---|---|---|---|---|---|---|
| 03:31:02 | 135 | 15 | 27665 | 59683 | 6385 | CG-s-32 baseline (row W1-S39) |
| 05:32:57 | 11 | 14 | 27664 | 59559 | 6385 | CG-s-33 loss read (row W1-S39) |
| 05:57:16 | 11 | 14 | -- | -- | 6385 | issuer's third read |
| **12:24:50** | **0** | **12** | **27662** | **59548** | **6385** | **THIS READ** |

**THE LOSS DID NOT STOP.** 135 -> 11 -> 11 -> **0**. The three-point reading that it had stopped
was a plateau between two drops -- which is precisely what three points cannot distinguish from
a halt when the process is event-driven rather than periodic. The second drop is in the worker's
own log:

```
12:01:42  INFO: INCR_NODE_DELTA head=27662 cur=27663 upsert=1 delete=1
12:01:43  INFO: INCR_EDGE_DELTA head=59548 cur=59559 upsert=0 delete=11
```

and the Lambda batch that caused it, at `12:01:00`, was processing S3 writes to
**`opal-data-inf`** -- a bucket whose policy node is likewise now absent from the 12 that remain.
**Same mechanism, different bucket, six and a half hours later.**

**AND THE MECHANISM IS STILL LOADED.** `SERVED_FROM=27`, and measured in the same run,
**27 of 27** hang off `S3_BUCKET_POLICY`. The next S3 write to any of those 12 buckets removes
its policy node and every `SERVED_FROM` edge on it.

---

## 5. THE INVESTIGATOR DID NOT CREATE THE EVENT (H4-AC4) -- `h4_no_act.sh`

```
ECS_RUN_TASK_CALLS=0     CODEBUILD_STARTS=0     S3_WRITES=0
IMAGE_PUSHES=0           TERRAFORM_APPLIES=0    PRODUCER_FILES_MODIFIED=0
PATHS_OUTSIDE_WRITE_GRANT=0                     AWS_READS=37 (permitted)
EGRESS_PROBE_CONTROL=FIRED   (the detector found 5 of 5 planted acts)
```

Three arms on three different instruments -- a static scan of this order's own executable
artifacts, the worktree's own unscoped `git status --porcelain`, and `h4_lib`'s per-call read
ledger. The control runs FIRST: the detector is shown to find five planted acts in an inert
scratch file before its zero over the real corpus is allowed to mean anything. The permitted
reads are printed as a non-zero count on purpose, so that *"took no reads"* and *"took only the
allowed reads"* are distinguishable in the record.

---

## 6. THE READING (H4-AC5) -- judgment; graded by `3.0.0_SA_CVO` at L9, NOT self-graded

**Can a count read off this plane be cited today, and under what condition?**

> **Yes -- but only as an instantaneous reading carrying its vintage AND its manifest id, and
> only for a family whose parent class is stable. It cannot be cited as a property of the
> estate.** A `STORED_IN`, `SERVED_FROM` or any other count parented to `S3_BUCKET_POLICY` is a
> reading of a value that changes whenever anybody writes an object to the corresponding bucket
> -- with no derive, no deploy and no schedule involved. Three such counts fell to zero in nine
> hours today with every producer input unmoved. The condition is therefore: **cite the number
> with `<vintage> / <manifest_id>`, and do not carry it across any interval in which an S3 write
> could have occurred -- which is every interval.**

**Can the deferred `F11-AC3` served re-take be made readable by anything short of an attribution?**

> It already is, now that the attribution exists -- and it would NOT have been without it. The
> re-take's failure mode was exactly the one the CTO named: *"the fix did not reach the served
> plane"* and *"the projection dropped the family again"* render identically as a low count. The
> discriminator that now exists is **not** the count: it is the pair
> (`nodes_snapshot_id`, `edges_snapshot_id`) plus `edges_skipped_missing_endpoint` in the served
> build's own manifest, and the worker's `INCR_NODE_DELTA` / `INCR_EDGE_DELTA` lines. A drop
> caused by this mechanism shows an UNMOVED edges snapshot, a MOVED nodes snapshot, and a rise in
> `edges_skipped_missing_endpoint` **equal to** the edge fall. A fix that failed to reach the
> plane shows none of that. So the re-take is readable if and only if it reads the manifest
> beside the count. Read on its own, the count is still ambiguous, and no attribution can repair
> that.

**Explain this republish, or make the family immune by re-parenting?**

> **Re-parent.** Explaining it is done and it does not help anybody: the republish was correct
> behaviour by every component in the chain. The Lambda upserted a bucket node because a bucket
> was written to; the projection worker rebuilt because the branch head advanced; the incremental
> refresh deleted edges whose endpoint no longer existed. Nothing here is a bug that can be
> switched off, and the moratorium correctly forbids standing up a monitor to watch it happen
> again. **The defect is the PARENT CHOICE.** `OWNED_BY S3Key -> S3_BUCKET` sat at 232 through
> the whole event and `S3Key` at 381 -- the ARN-parented family did not move by one edge, in the
> same graph, in the same window. That is a controlled comparison, not an argument. The
> re-parenting round 7 committed and did not deploy is the remedy, and the case for it is now
> stronger than when it was written: it was justified on volatility, and the volatility has since
> been measured at 124 + 11 edges and 3 policy nodes in nine hours, with 27 `SERVED_FROM` edges
> still standing on the same footing.
>
> One qualifier I will not leave out, because it changes who has to act. Re-parenting fixes the
> BLAST RADIUS. It does not fix the collision that fires the gun: a Lambda writing
> `node_id = <bare bucket name>` into a table where that exact string is another class's
> canonical key. After a re-parent, the same overwrite still destroys an `S3_BUCKET_POLICY` node
> on every S3 write -- it just stops taking a boundary-edge family with it. Whether that residue
> is acceptable is a decision above this cell, and it is stated here so that nobody reads a
> deployed re-parent as a closed key-space problem.

---

## 7. WHAT THIS CELL DID NOT MEASURE

* Which Iceberg row the overwrite actually removed -- inferred from source and served state,
  not read from `graph_nodes`. Trino/Athena would settle it; no grant here.
* Whether the same collision reaches classes other than `S3_BUCKET_POLICY`. `derive_runner.py:2307`
  says exactly one class is short-name-keyed, and that sentence was read, not verified against a
  census of every class's key shape.
* Anything about round 7's re-parenting commit beyond the fact, quoted from the face, that it was
  committed and not deployed.

## 8. ROWS FILED

* `NFRA_CLDGRPH-W3-S18` -- the loss did not stop; the cell's "one-time drop" premise is false at
  a fourth reading, and the same mechanism is still loaded under `SERVED_FROM`.
* `NFRA_CLDGRPH-W3-S19` -- the producer's own `nodes_deleted` counter cannot see a row its own
  overwrite filter destroys, so the deletion is invisible on the writing side and visible only
  on the reading side.
