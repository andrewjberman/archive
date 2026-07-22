# The graph freshness headers measure the CONTAINER's write-time, not the CONTENTS' observation-time

**Author:** `0.8.0_AE_CloudComp` · **Date:** 2026-07-22 · **For:** Andrew (direct)
**Trigger (verbatim):** *"I think we need to concretely establish the provenance of these headers,
because I suspect they may be slightly misleading. There is the nessie/iceberg layer that should be
refreshing every night at 2a or so. There is the comp-aws derive which is a full re-derive of local
kuzudb (as I understand). Then there is a mechanism we built more recently which is effectively an
incremental update of the local kuzudb."*

**Verdict: SUSPICION CONFIRMED, and it is worse than "slightly misleading" on one specific line.**
Four clocks exist. The header prints three of them and the one it labels most prominently as a
freshness PASS is the one that says least about the data.

---

## The four clocks, measured

| # | Clock | What it actually measures | Value | Age at 19:0xZ |
|---|---|---|---|---|
| 1 | `built:` | when the LOCAL kuzu DB was assembled from nessie | 2026-07-22T16:54:58Z | 2.2h |
| 2 | `graph_nodes: last-write` | when the NESSIE TABLE was last written to | ~2026-07-22T14:37Z | 4.5h |
| 3 | `snapshot_ts` on the rows | **when the estate was actually OBSERVED** | 2026-07-22T02:00:31Z | **17.1h** |
| 4 | `comp_aws_derive_iam.json` mtime | the on-disk derive artifact | 2026-07-14T09:58:58Z | **201.1h** |

Clock 3 confirms your 2am nightly: the full re-derive stamps every node it writes with a single
`snapshot_ts`, and that value is `02:00:31Z`.

## The defect: a 2-node write makes a 14,708-node corpus look fresh

```
source                    nodes   snapshot_ts (all rows)
full-derive              14,708   2026-07-22T02:00:31Z    <- 17.1h old
ms                        5,649   2026-07-22T02:00:31Z
semctl-c2c3-materialize      23   2026-07-22T02:00:31Z
incremental                   2   2026-07-22T14:37:22Z    <- 4.5h old
```

**Every one of the 193 `IAM_ROLE` nodes is `full-derive` at 02:00:31Z.** The incremental updater has
contributed **two nodes in total**. Yet those two nodes are what set the table's last-write time, and
the header reports:

> `graph_nodes: last-write 4.5h ago (< 6h cadence)`

That line is TRUE about the table and FALSE about the data. It renders a PASS verdict — `< 6h cadence`
— against a clock the data does not live on. Measured against clock 3, the same check reads
**17.1h > 6h cadence = FAIL**.

> **A LAST-WRITE TIMESTAMP IS A PROPERTY OF THE CONTAINER, NOT OF THE CONTENTS. One row written now
> makes a corpus of any age report as current, and the smaller the incremental write, the more
> misleading the header becomes.** The mechanism is monotonic in the wrong direction: a healthier,
> more granular incremental updater would make the staleness signal *worse*, not better.

This is the same family as `aws s3 ls` printing local time with no TZ marker, and the IAM census
carrying no `generated_utc`: **an instrument reporting a number that is adjacent to the question and
is read as the answer to it.**

## It also invalidates part of what I built an hour ago

`comp-iam live` reads clock 4 — the on-disk derive JSON, 201.1h old, 183 roles. Its vintage gate fires
correctly and REFUSES it, so it is not lying. But it is reading the **wrong artifact**: kuzu carries a
17.1h view of the same estate (193 roles) and live AWS has 205. Three populations, none of them "live":

```
comp_aws_derive_iam.json (clock 4, 201h)  183 roles
kuzu CloudNode           (clock 3,  17h)  193 roles
live AWS (fresh census)  (clock 0,   0h)  205 roles
```

The flip's premise stands — live-primary is right, and kuzu's `drift_class` resolves the
`${each.key}` fleets that a name-join cannot. What does NOT stand is treating any of these snapshots
as "the live state" without stating which clock it is on.

## What follows (proposed, not built)

1. **`comp-iam live` must key its vintage on `snapshot_ts` (clock 3), not file mtime (clock 4)** —
   read the population from kuzu, not the derive JSON, and report the observation time the rows carry.
2. **The comp-kuzu freshness header should report a DATA vintage per source**, e.g.
   `graph_nodes: table-write 4.5h | data (full-derive) 17.1h | incremental 4.5h [2 nodes]`.
   Keeping the table-write line is fine; presenting it alone as *the* cadence check is not.
3. **The `< 6h cadence` verdict should evaluate against clock 3.** As written it cannot fail while any
   incremental write is landing, which makes it a check that cannot report the condition it names.
4. **The 2-node incremental population is itself a finding** — either the incremental updater is
   barely running, or it is running and finding almost nothing to update. Those are very different
   states and the graph cannot currently distinguish them. NOT DIAGNOSED here.

## Not claimed

- WHY the incremental updater has only 2 nodes (not investigated).
- Whether the 02:00Z full-derive is scheduled, and whether it ran successfully today beyond writing
  these rows (not verified — the rows prove a write, not a complete run).
- Whether other node types have the same single-`snapshot_ts` shape for reasons unrelated to the
  nightly (all four sources show one `snapshot_ts` per source, which is consistent with batch writes,
  but I did not read the writer).
- `comp-aws derive --classes iam` does NOT exist as a flag (`unrecognized arguments`); the correct
  invocation was not determined, so the derive JSON was not refreshed.
