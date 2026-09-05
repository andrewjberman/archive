# CG-s-10 -- the FULL-FALLBACK DURATION of the KuzuDB projection, MEASURED

**Task order:** `NFRA_CLDGRPH.TO-CG-V-1` @`d0c21677c7` · **Cell:** `CG-s-10` (decomp v0.1 @`994c9381d0` s.1a,
ROUND 1) · **PRD:** v0.4 @`25c66d3358` s.6 R5 / s.7 S10 · **Seat:** `0.7.0_AE_CloudOps~Q` · **Fabric:** laptop
**Measured:** 2026-09-03 07:10:07Z - 07:51:30Z · **GO:** msg 93277 from `2.0.0_SA_COO~A`, READ-acked 07:0xZ

> **NO RUNTIME IS CHOSEN IN THIS DELIVERABLE.** The fit table in s.4 is a FINDING. `CG-s-2`'s task order
> reads it and decides. The absence of a runtime choice here is criterion `V1-AC4`.

---

## 0. THE NUMBER, up front

**A full projection rebuild of the KuzuDB graph takes 935.5-1001.2 s (15.6-16.7 min) and peaks at
6,752 MB of resident memory.** The full-FALLBACK duration -- what R5 actually sizes the worker against --
is the fallback *trigger* plus that load: **940.6-1006.3 s (15.68-16.77 min)**.

**Every one of the four prior figures is lower than every one of my measured runs.** The closest (Andrew's
9-10 min) is 1.6-1.8x short; the two document figures (~6 min / 356 s) are 2.7x short. I did not move my
numbers toward any of them, and s.5 says which operation each of the four was actually about.

**The cost is not I/O.** The full load reads **1.88 MiB** of Iceberg data and spends ~16 minutes turning it
into a 44.8 MB Kuzu database. This is CPU/memory work inside the graph engine, not network or storage work
-- which is the single most decision-relevant fact in this deliverable for `CG-s-2`.

---

## 1. `V1-AC1` -- THE TWO OPERATIONS, NAMED AT `file:line @ commit`

Every citation below was taken from a `comp-read` of the file (the `<compiler_tools_mandate>` reads), not
from memory. **Blob identity was checked rather than assumed** for each pin -- `git rev-parse <pin>:<path>`
against `git hash-object <worktree>` -- so a worktree read IS the read at the pin:

| file | lines | pin | blob (pin == worktree) |
|---|---|---|---|
| `infra/aws/globgrph/kuzu_nessie_load.py` | 417 | `e445642c5f` | `8ed0108820852e4be03ee5a06647e4e17a4f251f` |
| `infra/aws/globgrph/kuzu_incremental_refresh.py` | 350 | `aebe0d0a67` | `3d33fad758a7d365a469d32f94f808a4ec9b7568` |
| `infra/aws/globgrph/_canonical.py` | 746 | `173dd335f4` | `df194dd3d871714776fcb7d0c25db66a60a09749` |
| `infra/aws/globgrph/_provenance.py` | 641 | `996fcad53e` | `7bd413b05cca64473105bccde6a5b1d47d9244ff` |

### (a) The FULL load entry point
- **`infra/aws/globgrph/kuzu_nessie_load.py:74` @`e445642c5f`** -- `def main() -> int:`; CLI at `:372`
  (`if __name__ == "__main__":`), invoked as `python3 kuzu_nessie_load.py --db PATH [--force]` (`:27`).
- Output DB path chosen at **`:76`** -- `ap.add_argument("--db", default=DEFAULT_DB_PATH)`, where
  `DEFAULT_DB_PATH` (**`:43`**) is `<script dir>/kuzu_nessie_db`, the CANONICAL surface. **`--db` is the
  only thing that keeps a run off the canonical DB.**
- `--force` (drop + rebuild) is the **DEFAULT** (`:78-83`); `--no-force` opts into a MERGE.
- Reads from Nessie/Iceberg at **`:96-101`** -- the branch-head marker supplies
  `table_metadata[graph_nodes|graph_edges].metadata_location`; `read_iceberg_table` (**`:64-71`**) opens each
  via `pyiceberg.table.StaticTable`. Absent marker -> `WARN: HEAD-ORACLE UNKNOWN` + mtime-scan fallback (`:104`).

### (b) The INCREMENTAL entry point
- **`infra/aws/globgrph/kuzu_incremental_refresh.py:134` @`aebe0d0a67`** --
  `def refresh(current_db_path, tmp_db_path, log=None) -> tuple[str, dict]`; CLI at **`:322`**, invoked as
  `--current <live db> --db <tmp out>`. Exit codes are the `_canonical` signal (**`:326-327`**):
  **0 = incremental applied, 2 = FALLBACK (caller runs the full load), 1 = error**.
- It diffs against the live DB through a **read-only handle** -- **`:158`**,
  `kuzu.Database(current_db_path, read_only=True)` -- and applies to a file-copy, never to `--current`.

### (c) The FULL-FALLBACK TRIGGER and its threshold value
- **`infra/aws/globgrph/kuzu_incremental_refresh.py:174` @`aebe0d0a67`**:
  `if changed >= FALLBACK_MIN_ABS and changed >= FALLBACK_FRACTION * total:` -> `return "fallback", {...}`.
- Threshold values, **`:44-45`**: `FALLBACK_MIN_ABS = 4000` (env `GLOBGRPH_KUZU_INCR_FALLBACK_ABS`) and
  `FALLBACK_FRACTION = 0.25` (env `GLOBGRPH_KUZU_INCR_FALLBACK_FRAC`). `changed = len(to_upsert) + len(to_delete)`
  (`:168`), `total = max(len(head_keys), 1)` (`:169`).
- **Both conditions must hold**, so at the measured head size of 27,133 nodes the effective gate is
  `max(4000, 0.25 x 27133) = 6,784 changed nodes`.
- A **second, independent** fallback exists: the post-apply **count guard** at **`:227-232`** -- if the
  rebuilt counts do not equal the head set exactly, it removes the tmp and returns
  `"fallback", {"guard": "count"}` ("never swap in a wrong DB", `:27`).

### (d) The local orchestrator that wraps them
- **`infra/aws/globgrph/_canonical.py:610` @`173dd335f4`** -- `def ensure_fresh(db_path, ...)`.
- Constants it governs (census by `comp-read --enumerate`, **26 hits across 746 lines**, 17 whole-value):
  `CANONICAL_DB_PATH` **`:42`** (= `<script dir>/kuzu_nessie_db`) · `MUTEX_WAIT_S = 180.0` **`:44`** ·
  `ORPHAN_LOCK_S = 900.0` **`:47`** · `INCREMENTAL_TIMEOUT_S = 600` **`:67`** · `REBUILD_TIMEOUT_S = 1800` **`:66`**.
- It calls the incremental as a supervised child at **`:454`** / **`:579`** with `timeout=INCREMENTAL_TIMEOUT_S`.

### What "a projection rebuild" means in each carrier I later reconcile

| carrier | what it calls a "rebuild" | is it the projection? |
|---|---|---|
| `NFRA_KUZUSPLIT_PRD.md:45` col 1 (`comp-aws derive`) | LIVE AWS -> Iceberg/Nessie commit | **NO** -- cloud PRODUCER |
| `NFRA_KUZUSPLIT_PRD.md:45` col 2 (`comp-kuzu-full`) | Iceberg HEAD -> local KuzuDB | **YES** -- `kuzu_nessie_load` |
| `NFRA_GRAPHS.md:18`, `:61` (`comp-aws derive`) | live boto3 + TF state -> cloud graph | **NO** -- the producer again |
| `NFRA_KUZUSPLIT_PRD.md:22` ("3.9s vs 356s") | incremental vs full **projection** | **YES**, both halves |
| Andrew, brief `:7` ("9-10 min") | "refresh that representation" | **operation not pinned** (s.5) |

---

## 2. `V1-AC2` -- TWO FULL LOADS, MEASURED INTO A TEMP PATH

Both runs: `python kuzu_nessie_load.py --db <scratchpad>/full{1,2}_db`, invoked through the harness
`measure_run.py` (checked in beside this file, so these numbers are reproducible rather than asserted).

| | **FULL-1** | **FULL-2** |
|---|---|---|
| started / ended (UTC) | 07:10:07Z / 07:26:48Z | 07:31:15Z / 07:46:51Z |
| **wall clock** | **1001.172 s** (16.686 min) | **935.500 s** (15.592 min) |
| **peak memory** | **7,079,927,808 B** (6,751.9 MB) | **7,079,985,152 B** (6,752.0 MB) |
| corroborating sampled peak RSS | 7,079,829,504 B | 7,079,006,208 B |
| gap between the two instruments | 98,304 B (0.0014%) | 978,944 B (0.0138%) |
| samples taken | 12,783 @ 50 ms | 12,049 @ 50 ms |
| process I/O read / write | 54,281,856 B / 142,819,284 B | 54,281,851 B / 142,819,284 B |
| output DB file on disk (`ls`) | 46,993,408 B (44.8 MB) | 46,993,408 B (44.8 MB) |
| output DB + manifest sidecar (harness) | 46,994,310 B | 46,994,310 B |
| exit code | 0 | 0 |

**Variance between the two runs: 65.672 s** -- mean **968.336 s**, spread **+/-3.39%** about the mean
(FULL-2 = 0.9344 x FULL-1). **Peak memory varied by 57,344 bytes -- 0.0008%.**

### The instruments, and why two of them
- **Wall clock:** `time.monotonic()` around `subprocess.Popen`/`wait` -- monotonic, so immune to clock adjustment.
- **Peak memory (headline):** the **OS's own** peak working set, `GetProcessMemoryInfo` via psutil's Windows
  `memory_info().peak_wset`. Kernel-maintained and monotonic, so it does **not** depend on my sampling cadence.
- **Peak RSS (corroborating):** max of polled RSS over the process tree at 50 ms. **A different failure mode**
  -- blind to a spike between samples. It came within **98,304 B (0.0014%)** of the OS
  peak on FULL-1 and **978,944 B (0.0138%)** on FULL-2. The sampled value sits BELOW the OS peak in both
  runs -- the direction the instruments' construction predicts, since sampling can miss a peak but never
  invent one. That is what agreement between two genuinely different methods looks like, with the residual
  falling the right way.
- **Residual, stated not hidden:** `peak_wset` is read by polling a live process, so a spike in the final
  50 ms before exit is not captured. Bounded by 50 ms against a ~1000 s run.

### Input sizes
Identical for both runs -- **the branch-head marker did not move at any point during any of the four runs**
(`marker_moved_during_run: false` in all four records), so all four read the same input.

- **Marker / HEAD oracle:** `warehouse/_branch_head.main.json` (`_provenance.py:96` MARKER_KEY),
  `committed_at_iso` **2026-09-03T05:53:54.509091+00:00**, `writer_id` `incremental_updater`,
  `nessie_commit_hash` `9a0e597f3623f245a69f3f46e1c6b408b132c30e28d27a2220892782191e985c`.
- **Snapshots pinned:** `graph_nodes` `1242378212505298814`, `graph_edges` `1026441646305052092`.
- **Rows read (loader's own report, both runs identical):** `ICEBERG_READ nodes=27156 edges=61071`;
  `NODES_DEDUP unique=27133 (from 27156 rows, key_collisions=0)`;
  `EDGES_WRITTEN written=60688 skipped_missing_endpoint=383`.
- **Iceberg BYTES read** (measured separately against the same two pinned snapshots via pyiceberg
  `plan_files()`, summing `file_size_in_bytes` of that snapshot's data files -- not the whole table
  directory across all history, which would be a different and wrong number):

  | table | data files | bytes | records (from manifests) |
  |---|---|---|---|
  | `graph_nodes` | 2 | 1,309,906 (1.25 MiB) | 27,156 |
  | `graph_edges` | 1 | 662,719 (0.63 MiB) | 61,071 |
  | **total** | **3** | **1,972,625 (1.88 MiB)** | **88,227** |

  The manifest record counts (27,156 / 61,071) match the loader's `ICEBERG_READ` line exactly -- two
  independent instruments (pyiceberg manifest metadata vs. the loader's pyarrow read) agreeing on the input.
- **Node layer breakdown, both runs identical:** aws 2,102 · ms 6,102 · pipeline 1,337 · portal 11,338 ·
  semctl 6,254 (sum 27,133). `UNTYPED_NODES count=0`.

⚠ **Two carriers of the edge count disagree, and I report both rather than picking one.** The build manifest
each full load wrote says `edge_count: 60688`; a direct Cypher query against the built DB
(`MATCH ()-[r:CloudEdge]->() RETURN count(*)`) returns **58,432**, on both DBs. `node_count` agrees exactly
(27,133). The manifest field is a MERGE-attempt counter, and MERGE collapses duplicate
`(src,dst,edge_type,props)` identities. Filed as **`NFRA_CLDGRPH-S8`**.

### Environment
Windows-11-10.0.26100-SP0 · Intel64 Family 6 Model 189 Stepping 1 · 8 logical / 8 physical cores ·
31.7 GB RAM total, **8.0 GB available at start** · Python 3.12.10 · kuzu 0.11.3 · pyiceberg 0.9.1 ·
pyarrow 18.1.0 · boto3 1.42.54 · psutil 7.2.2.
**Network path to S3:** public internet -> `s3.us-east-1.amazonaws.com`. This is a **dev laptop, NOT in-VPC**
-- Nessie's REST endpoint is unreachable from here, which is why the engine anchors on the S3 marker
(`kuzu_nessie_load.py:11-17`).

### THE CONTROL THAT CAN FAIL: the canonical DB was never touched

`infra/aws/globgrph/kuzu_nessie_db` -- a fingerprint of size + full-ISO mtime, hashed:

| when | size | mtime | listing md5 |
|---|---|---|---|
| BEFORE any run (07:0xZ) | 82,661,376 | 2026-09-02 20:36:15.505342500 -0400 | `711b0b3c78f0bfecff7a92bcdcd49193` |
| mid FULL-1 (07:19Z) | 82,661,376 | 2026-09-02 20:36:15.505342500 -0400 | `711b0b3c78f0bfecff7a92bcdcd49193` |
| after FULL-1 (07:31Z) | 82,661,376 | 2026-09-02 20:36:15.505342500 -0400 | `711b0b3c78f0bfecff7a92bcdcd49193` |
| **after ALL four runs (07:52Z)** | **82,661,376** | **2026-09-02 20:36:15.505342500 -0400** | **`711b0b3c78f0bfecff7a92bcdcd49193`** |

**This control can fail:** the hash covers the mtime to 100 ns, so any write, touch or truncation moves it.
It did not move. For the incremental measurement I went further and never let the engine open the canonical
DB at all -- I ran it against a **file copy** (s.3), so the canonical was only ever read by `cp`.

`_canonical.py`'s mkdir mutex was **never touched by this seat**: invoking the engines directly bypasses
`_canonical` entirely. The loader's *own* singleton lock is a different object and a temp-path run does take
it -- filed as **`NFRA_CLDGRPH-S3`**, whose ARMED condition is now discharged (s.6).

---

## 3. `V1-AC3` -- THE INCREMENTAL PATH, MEASURED

**This is the second of the two operations the four figures conflate, and it is labelled as such throughout.**

The marker did not advance between 05:53:54Z and the end of my window (07:51:30Z) -- **1h 58m with no new
stamp**, against R5's sizing input of 45 stamps/24 h. So **a mid-sized real delta did not exist to measure**;
that is a MEASURED ABSENCE, not a skipped criterion. I measured the two deltas the world actually offered,
which bracket the path:

| | **INC-A** -- fallback trigger | **INC-B** -- apply path |
|---|---|---|
| `--current` | copy of the canonical (vintage 00:36:15Z) | `full1_db` (vintage 05:53:54Z = HEAD) |
| **wall clock** | **5.094 s** | **7.531 s** |
| **peak memory** | **481,992,704 B** (459.7 MB) | **488,116,224 B** (465.5 MB) |
| samples | 78 @ 50 ms | 105 @ 50 ms |
| status / exit code | `fallback` / **rc=2** | `incremental` / **rc=0** |
| head vs current | head=27,133 cur=27,122 | head=27,133 cur=27,133 |
| **delta: rows applied** | **0 applied** -- upsert 27,133 / delete 0 **detected**, none applied | **0** (node_upsert 0, node_delete 0, edge_upsert 0, edge_delete 0) |
| delta as % of head | **100.0%** | 0.0% |
| **count-guard fired?** | **No** -- execution never reached it (`:227`); the *delta-size gate* `:174` fired first | **No** -- guard evaluated and PASSED (27,133 nodes / 58,432 edges == head set exactly) |
| output DB | none (removed on non-zero rc, `:344`) | 46,993,408 B, manifest `edge_count: 58432` |

**INC-A is the full-fallback trigger itself**, verbatim from its stdout:
`INCR_RESULT status=fallback stats={'reason': 'delta 27133 >= 4000 and >= 25% of head (full-derive overwrite) -- bulk reload cheaper', 'changed': 27133}`

⚠ **The most decision-relevant thing in this section: 100% of head read as changed.** Only 11 nodes actually
appeared (27,122 -> 27,133), yet all 27,133 were marked for upsert -- because the nightly whole-table
overwrite rewrites every row's `snapshot_ts`, and the diff keys on `snapshot_ts` (`:165-166`). So **the
full-fallback is not an edge case; it is the daily path after every whole-table overwrite.** This is exactly
what `NFRA_KUZUSPLIT_PRD.md:22-28` predicted in prose and it is now measured.

**INC-B is a ZERO-delta run and is therefore the FLOOR of the incremental path**, not a typical cost: it
measures head read + diff + file copy + count-guard + manifest stamp with no MERGE work at all. A real
non-zero delta adds MERGE cost on top of 7.531 s. **I am not presenting 7.531 s as "the incremental cost".**

### FULL-FALLBACK DURATION -- the cell's actual subject, decomposed

`trigger detection` + `full load`:

| | seconds | minutes |
|---|---|---|
| minimum (INC-A + FULL-2) | **940.594** | 15.68 |
| mean (INC-A + mean full) | **973.430** | 16.22 |
| maximum (INC-A + FULL-1) | **1006.266** | 16.77 |

The trigger is **0.5%** of the total; the full load is the whole cost.

---

## 4. `V1-AC4` -- THE FIT TABLE (a FINDING; no runtime is chosen)

Lambda ceilings as stated in the task order: **900 s timeout · 10,240 MB memory · 10 GB ephemeral storage.**

| measured figure | value | vs 900 s timeout | vs 10,240 MB memory | vs 10 GB ephemeral |
|---|---|---|---|---|
| FULL-1 wall | 1001.172 s | **DOES NOT FIT** -- over by 101.2 s (11.2%) | -- | -- |
| FULL-2 wall | 935.500 s | **DOES NOT FIT** -- over by 35.5 s (3.9%) | -- | -- |
| full load, mean | 968.336 s | **DOES NOT FIT** -- over by 68.3 s (7.6%) | -- | -- |
| **full-fallback, min** | **940.594 s** | **DOES NOT FIT** -- over by 40.6 s (4.5%) | -- | -- |
| **full-fallback, max** | **1006.266 s** | **DOES NOT FIT** -- over by 106.3 s (11.8%) | -- | -- |
| full load peak memory | 6,752.0 MB | -- | **FITS** -- uses 65.9%, headroom 3,488.0 MB | -- |
| full load peak on disk | ~53.8 MB (DB 44.8 + WAL <=9.0) | -- | -- | **FITS** -- uses 0.53% |
| INC-A trigger | 5.094 s / 459.7 MB | FITS (0.6% of budget) | FITS -- 4.5% | FITS |
| INC-B apply floor | 7.531 s / 465.5 MB | FITS (0.8% of budget) | FITS -- 4.5% | FITS |

**Margins, stated:**
- **Timeout: not marginal. Every measured full run exceeds 900 s**, the closest by 35.5 s (3.9%). The margin
  is on the wrong side of the ceiling in 2 of 2 runs, and the run-to-run spread (+/-3.39%) is smaller than
  the shortfall, so this is not a case where a lucky run fits.
- **Memory: fits, but the headroom is 34.1%**, and a Lambda sized for it would be at/near the 10,240 MB
  maximum -- there is no larger Lambda tier to grow into.
- **Ephemeral: fits with ~190x headroom.** Not a constraint.

**ECS one-off task on the existing `opal-globgrph` cluster:** no wall-clock ceiling, so the 940.6-1006.3 s
full-fallback **FITS** on the timeout axis by construction; memory is a task-size parameter, and ~6.75 GB
peak means a task sized at 8 GB or more. ⛔ **Cold-start of a task on that cluster is UNMEASURED by this task
order** -- I did not start an ECS task and will not infer a number for one.

⛔ **NO RUNTIME IS CHOSEN HERE.** `CG-s-2` decides, reading this table.

---

## 5. `V1-AC5` -- THE FOUR PRIOR FIGURES, RECONCILED **AFTER** MEASURING

**My raw numbers were fixed before I opened any of these sources for reconciliation, and they appear
unchanged in s.2 and s.3: 1001.172 s, 935.500 s, 5.094 s, 7.531 s.** Nothing below moved them.

| # | figure, verbatim | source | which of the two operations | consistent with my measurement? |
|---|---|---|---|---|
| 1 | *"\| Cost \| ~10 min \| ~6 min \|"* | `NFRA_KUZUSPLIT_PRD.md:45` | col 1 = `comp-aws derive` (**producer, NOT the projection**); col 2 = `comp-kuzu-full` = **the full projection** | **NO** for the ~6 min limb: measured mean is **2.69x** it. The ~10 min limb is **out of scope** -- a different operation I did not run. |
| 2 | *"`comp-aws derive` REBUILDS from live AWS (~8 min)"* | `NFRA_GRAPHS.md:18`, table `:61` | **`comp-aws derive` -- the cloud PRODUCER, not the projection at all** | **NOT APPLICABLE.** My measurement does not bear on it. This figure was never about the projection, and its presence in a four-figure set about "the rebuild" is the conflation itself. |
| 3 | *"92x faster (3.9s vs 356s)"* | `NFRA_KUZUSPLIT_PRD.md:22` | **both halves are the projection**: 3.9 s incremental, 356 s full | **NO** for the full limb: 356 s vs measured mean 968.3 s = **2.72x**. **PARTLY** for the incremental limb: 3.9 s vs my 7.531 s zero-delta floor -- same order of magnitude, within ~2x, and mine is a floor on different hardware. My measured ratio is **128.6x**, vs the claimed 92x. |
| 4 | *"it can take 9-10 min to do so"* | Andrew, brief `:7` (verbatim prompt) | **operation NOT pinned** -- "that representation" | **NO, and it is the CLOSEST of the four**: 540-600 s vs measured mean 968.3 s = **1.61-1.79x**. |

### Why they disagree, and what I will not claim
Figures 1 and 3 agree with **each other** (~6 min / 356 s) and are the two document claims about the
projection. Both are ~2.7x below what I measured. **I cannot reconstruct the gap, and here is precisely why:**

> **NOT RECONSTRUCTIBLE.** **None of the four figures carries an input size, a measurement date, a machine,
> or an instrument.** Figure 3's 356 s traces to the 2026-07-08 incremental-engine work -- ~8 weeks before my
> run -- and the graph may have been materially smaller then, but no recorded row count accompanies it, so
> that is a hypothesis I cannot test from the record. A reconciliation would require re-running the prior
> figures' own conditions, which no longer exist in a stated form.

**One candidate explanation I CAN test, and it fails:** graph growth does not explain it. The brief measured
the canonical DB at **27,107 nodes / 60,636 edges** on 2026-09-01; I measured **27,133 nodes / 60,688 merges**
on 2026-09-03. That is +0.1% in two days -- nowhere near a 2.7x cost difference.

**One candidate I CANNOT resolve, named rather than buried:** this box had **8.0 GB RAM available at start**
against a **6.75 GB peak**, so memory pressure may have inflated my wall clock. I did not instrument paging,
so I am not claiming it did or did not. It is a live alternative for part of the gap, and it argues the
measured figure should be re-taken on the target runtime before anything irreversible is sized to it --
which is `CG-s-2`'s call, not mine.

⛔ **What I refuse to do:** pick one of the four, or split the difference. `4.0.0_SA_CRO` declined to
reconcile them because choosing manufactures a measurement; the decomp inherited that refusal; measuring
does not retroactively license it. The four are now **attributed**, which is what was owed.

---

## 6. SURPRISE ROWS FILED, and one discharge

Filed by this seat into `org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md`
(channel denominator at last read: **8 rows**, all schema-valid, no id collisions):

- **`NFRA_CLDGRPH-S2`** (OBSERVATION, ARMED) -- `kuzu_incremental_refresh.py:27` says the incremental path is
  "Gated OFF by default ... pending CTO arch-gate"; `_canonical.py:450` defaults the same flag ON and
  `NFRA_KUZUSPLIT_PRD.md:22` records the GO as landed. The stale carrier is the file a reader opens first.
- **`NFRA_CLDGRPH-S3`** (OBSERVATION, ARMED, `disarm_owner` = this seat) -- the TO's bound "run to the temp
  path in parallel, which needs no lock" is false for the loader's own singleton (`:294` keys it to the
  SCRIPT dir, `:401` acquires unconditionally). **DISCHARGE CONDITION NOW MET:** both full loads completed and
  `infra/aws/globgrph/.kuzu_nessie_load.lock` is **ABSENT** at 07:52Z -- released by the engine's `finally`
  (`:412`). *Surfaced for `3.0.0_SA_CVO~A` to disposition at L8; this seat does not adjudicate its own row.*
- **`NFRA_CLDGRPH-S4`** (OBSERVATION, INERT) -- two orphaned local rebuilds left mutex + tmp + WAL residue
  inside 40 minutes, both **before** this seat ran. Residue observed; cause NOT established, and explicitly
  not asserted against CE-G-5.
- **`NFRA_CLDGRPH-S8`** (OBSERVATION, ARMED) -- the full loader's `_build_manifest.edge_count` overstates the
  stored edge count by 2,256 (3.9%); the incremental path writes the correct number for the same graph.

---

## 7. BOUNDS -- how each was kept

| bound | how it was kept |
|---|---|
| READ-ONLY against AWS | Only `s3:GetObject`/`ListBucket`-class reads by the engines and by the Iceberg sizing read. **No object written**, no IAM, no Terraform, no Lambda/ECS resource created. **No IAM refusal was met** -- had one occurred it would be carried here as a CG-s-12 finding. |
| No edit to any repo source | Zero files changed under `infra/`, `docs/`, `.tools/`. The only files this seat wrote are its own deliverables + the shared surprise channel. The engines were invoked, never modified. |
| Never the canonical DB, never its mutex, never kill a rebuild | `--db` always a session-unique scratchpad path; the canonical fingerprint is byte-identical across four runs (s.2); the incremental ran against a **copy**, so the engine never opened the canonical at all; `_canonical`'s mkdir mutex was never touched (direct invocation bypasses it); **no process was killed** -- the one stale singleton lock was cleared by the engine's own dead-holder path, not by hand. |
| Temp path not shared with `0.7.0_AE_CloudOps~P` | All paths under this session's own scratchpad `.../b6334f48-be18-4d4d-b18e-4bf3abd316eb/scratchpad/cgs10/`, which is session-keyed and cannot collide. |
| Do not pick a runtime / do not size the worker | s.4 states fit/does-not-fit/margin per ceiling and stops. No runtime named as a recommendation anywhere in this file. |
| Divergence -> a ROW, then keep working; never a message | Four rows filed mid-execution (s.6); no message sent about any of them; `3.0.0_SA_CVO~A` was not messaged. |

---

## 8. `V1-AC6` -- PUSH STATE, MEASURED

Read at report time by `git ls-remote origin CLOUD` + `git merge-base --is-ancestor` -- see the report
message for the values as measured at that instant. **LOCAL is the expected reading under the integrator's
cadence** (push cadence is Andrew's; the GO says to expect LOCAL and say so).

---

```json
{
  "cell": "CG-s-10",
  "task_order": "NFRA_CLDGRPH.TO-CG-V-1",
  "task_order_commit": "d0c21677c7",
  "seat": "0.7.0_AE_CloudOps~Q",
  "claim": "measured",
  "measured_window_utc": ["2026-09-03T07:10:07Z", "2026-09-03T07:51:30Z"],
  "input_vintage": {
    "marker_key": "warehouse/_branch_head.main.json",
    "committed_at_iso": "2026-09-03T05:53:54.509091+00:00",
    "writer_id": "incremental_updater",
    "nessie_commit_hash": "9a0e597f3623f245a69f3f46e1c6b408b132c30e28d27a2220892782191e985c",
    "graph_nodes_snapshot_id": 1242378212505298814,
    "graph_edges_snapshot_id": 1026441646305052092,
    "marker_moved_during_any_run": false,
    "iceberg_data_files": 3,
    "iceberg_data_bytes_read": 1972625,
    "rows_read": {"nodes": 27156, "edges": 61071},
    "nodes_after_dedup": 27133,
    "edges_merged": 60688,
    "edges_stored_queried": 58432,
    "edges_skipped_missing_endpoint": 383
  },
  "full_load": {
    "operation": "kuzu_nessie_load.py --db <temp>",
    "runs": [
      {"label": "FULL-1", "wall_clock_s": 1001.172, "peak_memory_bytes": 7079927808,
       "sampled_peak_rss_bytes": 7079829504, "samples": 12783, "returncode": 0,
       "io_read_bytes": 54281856, "io_write_bytes": 142819284,
       "output_db_bytes": 46994310, "output_db_file_bytes": 46993408,
       "started_iso": "2026-09-03T07:10:07Z", "ended_iso": "2026-09-03T07:26:48Z"},
      {"label": "FULL-2", "wall_clock_s": 935.5, "peak_memory_bytes": 7079985152,
       "sampled_peak_rss_bytes": 7079006208, "samples": 12049, "returncode": 0,
       "io_read_bytes": 54281851, "io_write_bytes": 142819284,
       "output_db_bytes": 46994310, "output_db_file_bytes": 46993408,
       "started_iso": "2026-09-03T07:31:15Z", "ended_iso": "2026-09-03T07:46:51Z"}
    ],
    "mean_wall_clock_s": 968.336,
    "variance_wall_clock_s": 65.672,
    "variance_pct_about_mean": 3.39,
    "peak_memory_delta_bytes": 57344,
    "peak_memory_delta_pct": 0.0008,
    "outputs_identical": true
  },
  "incremental": {
    "operation": "kuzu_incremental_refresh.py --current <db> --db <temp>",
    "runs": [
      {"label": "INC-A-fallback-trigger", "current": "copy of canonical (vintage 2026-09-03T00:36:15Z)",
       "wall_clock_s": 5.094, "peak_memory_bytes": 481992704, "sampled_peak_rss_bytes": 478846976, "samples": 78, "returncode": 2, "status": "fallback",
       "delta_detected": 27133, "delta_pct_of_head": 100.0, "rows_applied": 0,
       "count_guard_fired": false, "count_guard_reached": false,
       "gate_that_fired": "delta-size gate kuzu_incremental_refresh.py:174"},
      {"label": "INC-B-apply-path", "current": "full1_db (vintage 2026-09-03T05:53:54Z = HEAD)",
       "wall_clock_s": 7.531, "peak_memory_bytes": 488116224, "sampled_peak_rss_bytes": 487079936, "samples": 105, "output_db_bytes": 46994310, "returncode": 0, "status": "incremental",
       "delta_detected": 0, "delta_pct_of_head": 0.0, "rows_applied": 0,
       "count_guard_fired": false, "count_guard_reached": true, "count_guard_result": "PASS",
       "note": "ZERO-delta run: the FLOOR of the incremental path, not a typical cost"}
    ],
    "real_mid_sized_delta_available": false,
    "real_delta_absence_reason": "the branch-head marker did not advance between 2026-09-03T05:53:54Z and the end of the measurement window at 07:51:30Z -- 1h58m with no new stamp, against R5's sizing input of 45 stamps/24h"
  },
  "full_fallback_duration_s": {"min": 940.594, "mean": 973.43, "max": 1006.266,
    "composition": "INC-A trigger 5.094 s (0.5%) + full load 935.5-1001.172 s (99.5%)"},
  "fit_table": {
    "lambda_timeout_900s": {"verdict": "DOES NOT FIT",
      "margin": "every measured full run exceeds it; closest by 35.5 s (3.9%), worst by 106.3 s (11.8%)",
      "runs_over_ceiling": "2 of 2"},
    "lambda_memory_10240mb": {"verdict": "FITS", "margin": "peak 6752.0 MB = 65.9% of ceiling, headroom 3488.0 MB",
      "caveat": "a Lambda sized for this sits at/near the maximum tier; there is no larger tier to grow into"},
    "lambda_ephemeral_10gb": {"verdict": "FITS", "margin": "peak ~53.8 MB = 0.53% of ceiling"},
    "ecs_one_off_task": {"verdict": "FITS on the timeout axis (no wall-clock ceiling)",
      "memory": "requires a task sized >= ~6.75 GB peak, i.e. 8 GB or more",
      "cold_start": "UNMEASURED -- no ECS task was started by this task order"}
  },
  "prior_figures_reconciled": [
    {"figure": "~6 min", "source": "NFRA_KUZUSPLIT_PRD.md:45 col 2", "operation": "full projection (comp-kuzu-full)",
     "consistent": false, "measured_ratio": 2.69},
    {"figure": "~10 min", "source": "NFRA_KUZUSPLIT_PRD.md:45 col 1", "operation": "comp-aws derive -- NOT the projection",
     "consistent": "OUT-OF-SCOPE -- different operation, not run by this task order"},
    {"figure": "~8 min", "source": "NFRA_GRAPHS.md:18 and :61", "operation": "comp-aws derive -- NOT the projection",
     "consistent": "NOT APPLICABLE -- this figure was never about the projection"},
    {"figure": "356 s", "source": "NFRA_KUZUSPLIT_PRD.md:22", "operation": "full projection",
     "consistent": false, "measured_ratio": 2.72},
    {"figure": "3.9 s", "source": "NFRA_KUZUSPLIT_PRD.md:22", "operation": "incremental projection",
     "consistent": "PARTLY -- same order of magnitude vs the 7.531 s zero-delta floor, on different hardware"},
    {"figure": "92x", "source": "NFRA_KUZUSPLIT_PRD.md:22", "operation": "ratio full:incremental",
     "consistent": "DIRECTIONALLY -- measured ratio 128.6x"},
    {"figure": "9-10 min", "source": "brief docs/briefs/globgrph-cloud-compile-and-gateway-traversal-20260901.md:7 (Andrew, verbatim)",
     "operation": "NOT PINNED", "consistent": false, "measured_ratio": [1.61, 1.79],
     "note": "closest of the four to the measurement"}
  ],
  "reconciliation_residual": "NOT RECONSTRUCTIBLE -- no prior figure carries an input size, date, machine or instrument. Graph growth is EXCLUDED as the explanation (+0.1% nodes in the two days since the brief's 27,107). Memory pressure on this box (8.0 GB available vs 6.75 GB peak) is a NAMED, UNRESOLVED candidate.",
  "control_canonical_db_untouched": {
    "path": "infra/aws/globgrph/kuzu_nessie_db",
    "size_before": 82661376, "size_after": 82661376,
    "mtime_before": "2026-09-02 20:36:15.505342500 -0400",
    "mtime_after": "2026-09-02 20:36:15.505342500 -0400",
    "listing_md5_before": "711b0b3c78f0bfecff7a92bcdcd49193",
    "listing_md5_after": "711b0b3c78f0bfecff7a92bcdcd49193",
    "verdict": "UNTOUCHED", "can_fail": "the hash covers mtime to 100ns; any write, touch or truncation moves it"
  },
  "surprise_rows_filed": ["NFRA_CLDGRPH-S2", "NFRA_CLDGRPH-S3", "NFRA_CLDGRPH-S4", "NFRA_CLDGRPH-S8"],
  "runtime_chosen": null,
  "runtime_choice_owner": "CG-s-2"
}
```
