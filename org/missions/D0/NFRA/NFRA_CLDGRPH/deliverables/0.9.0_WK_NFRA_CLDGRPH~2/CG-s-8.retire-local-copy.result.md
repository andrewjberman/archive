# CG-s-8 -- the RETIREMENT of the local copy (TO-CG-D-7, R7): result

**Worker:** `0.9.0_WK_NFRA_CLDGRPH~2` (spine-v3 subagent of `2.0.0_SA_COO~A`)
**Branch:** `wk-cldgrph-2-d7`, base `CLOUD@da35a5dfa0`. **Push state: LOCAL** (never pushed).
**Measured:** 2026-09-05 22:5xZ - 2026-09-06 00:0xZ, all invocations bounded by `timeout`.

---

## CONCLUSION FIRST

**The PORT landed; the RETIREMENT did not, and could not inside this order's write grant.**

- Every user-facing consumer now reads the SERVED graph through `projection_client`. `kuzu.Database(`
  over `org/modules/graph .tools` fell from a population that opened the local canonical DB in six
  tools to **2 hits, both in `org/modules/graph/tsgraph_spike/` scratch loaders that open their own
  scratch path, not `kuzu_nessie_db`**. comp-blast, comp-find `--corpus aws`, comp-detect,
  comp-cluster, comp-canon-motif, comp-marker-read and comp-iam-live all answer from the service.
- **The `_canonical.py` seam is still there.** Removing it strands SIX importers that live outside
  this order's `<paths>` block, one of which -- `org/modules/heatmap/ms_heat_index.py` -- is a live
  class-B consumer that calls `_canonical.ensure_fresh` and that the cut's census could not see,
  because that census was scoped to `org/modules/graph`, `.tools` and `infra/aws/globgrph`. Row
  **W2-S13**. A path missing from the block is a wall, not an oversight to route around, so the seam
  was left in place and D7-AC1 is reported FAIL rather than met by an out-of-grant edit.
- **Two absence criteria cannot reach zero as written**, independently of the above: D7-AC1's own
  pattern is carried by two of the three engine files D7-AC5 pins byte-identical (row **W2-S12**),
  and 28 of D7-AC2's 41 surviving hits are in config/data/doc/spike files outside the grant (row
  **W2-S14**).
- **D7-AC3's invocation runs a Python file under `bash`** and can never produce its expect string
  (row **W2-S15**); under `python` the same call passes exactly.

**MECHANICAL RESULT: 4 PASS (D7-AC4, D7-AC5, D7-AC6, D7-AC7), 3 FAIL (D7-AC1, D7-AC2, D7-AC3),
1 RECORDED-judgment (D7-AC8). The order stays OPEN.**

---

## 1. THE CENSUS (step 1, read-only, mine -- not the issuer's)

The ordered invocation, run first, before any write:

```
python .tools/comp-find 'CANONICAL_DB_PATH|kuzu_nessie_db|_canonical|kuzu_cli|ensure_fresh' \
       org/modules/graph .tools infra/aws/globgrph --all --limit 200
  DENOMINATOR: 594 hit(s) across 881 file(s) scanned in scope [corpus=all]
    | 3 EPHEMERAL-FLOOR, NOT searched (--corpus raw reads these) | 5 BINARY, NOT searched
  BANDS (true totals, not this page): HEAD=97 DEF=21 SURFACED=189 CONFIG=202 TEST=68 DOC=17
  PAGE 1 of 1  (showing 594 of 594)          <- ONE page; every page read
```

**594, not 136 -- and the difference is not a disagreement.** The face's `33 files / 136
occurrences` came from a NARROWER pattern (`CANONICAL_DB_PATH|kuzu_nessie_db|import _canonical|from
_canonical|_canonical\.|kuzu_cli`) over a NARROWER pathspec (`org/modules/graph/*.py, .tools/comp-*,
.tools/*.py, infra/aws/globgrph/*.py, .tools/tests/*.py`). The ordered census pattern here contains
the bare token `_canonical`, which is a SUBSTRING of `nna_canonical`, `c2_canonical_compose`,
`_canonical_schema`, `build_canonical_prices` and `test_tooltip_canonical_exclusion` -- 142 of the
594 hits are one JSON data file (`org/modules/graph/nerves-risk-edges.json`) alone. **The number
that decides anything is the COUPLING census below, not this one.** The 594 is recorded because the
order asked for it and because its denominator (881 files scanned) is the proof the instrument was
reading a real corpus.

### The coupling census -- who actually TOUCHED the local database

```
python .tools/comp-find 'import kuzu|kuzu\.Database|kuzu\.Connection|import _canonical|_canonical\.|CANONICAL_DB_PATH' \
       org/modules/graph .tools infra/aws/globgrph --all --limit 200
  DENOMINATOR: 269 hit(s) across 881 file(s) scanned in scope [corpus=all]
```

| # | file | class | disposition | note |
|---|---|---|---|---|
| 1 | `org/modules/graph/comp_blast_universe.py` | B | **REPOINTED** | `load_kuzu_universe` now pulls nodes+edges over `projection_client`; `_import_globgrph` is a named refusal; a `db_path` argument is REFUSED, not ignored |
| 2 | `org/modules/graph/cli.py` | B | **REPOINTED** | `_kuzu_vintage` -> `_served_vintage`; new `_format_served_vintage_line` / `_served_vintage_dict`; `STALE-SERVED` arm REMOVED (s.4) |
| 3 | `org/modules/graph/comp_marker_read.py` | B | **REPOINTED** | `load_marker_head_graph` reads the served graph; head pin = the service's `manifest_sha256`; a local `db_path` RAISES |
| 4 | `org/modules/graph/comp_iam_live.py` | B | **REPOINTED** | `kuzu_iam_rows` served; `KUZU_DB` constant deleted |
| 5 | `.tools/comp-find` (`--corpus aws`) | B | **REPOINTED** | `_aws_corpus` no longer spawns `kuzu_cli.py`; one in-process HTTPS pull; VINTAGE moved ABOVE the DENOMINATOR |
| 6 | `infra/aws/globgrph/comp_detect.py` | B | **REPOINTED** | `freshness_assert` served; `run()` uses `projection_client.connect()` |
| 7 | `infra/aws/globgrph/comp_debt.py` | B | **REPOINTED (nessie leg)** | nessie leg served; the STITCH leg still opens `kuzu_stitch_db` locally -- row **W2-S17** |
| 8 | `infra/aws/globgrph/comp_cluster_cli.py` | B | **REPOINTED** | `_connect` served; `DEFAULT_DB_PATH` is now a surface name, not a path |
| 9 | `infra/aws/globgrph/canon_motif_scorer.py` | B | **REPOINTED** | `freshness_assert` + `run()` served |
| 10 | `infra/aws/globgrph/debtscan_canon_scorer.py` | B | **REPOINTED** | `import kuzu` and `import _canonical` both removed; `_freshness_gate`/`_conn` served |
| 11 | `.tools/tests/test_g2_disclosure_battery.py` | E | **TEST-REPOINTED** | 6 arms -> 7; stale-served arm INVERTED; `import _canonical` removed; stubbed payloads, no network |
| 12 | `.tools/tests/test_comp_find_battery.py` | E | **TEST-REPOINTED** | `_aws_exercisable` probes the SERVICE; G5 orphan arms -> spawn-free arms with a positive control; 10 arms -> 12 |
| 13 | `.tools/tool_index.py` | B (prose) | **REPOINTED (prose)** | one `ensure_fresh` mention retired |
| 14 | `infra/aws/globgrph/projection_client.py` | (client) | **EXTENDED, stated** | see s.2 |
| 15 | `infra/aws/globgrph/kuzu_cli.py`, `.tools/comp-kuzu` | A | already thin (TO-CG-D-3) | not re-done here |
| 16 | `org/modules/graph/cse_schema.py`, `infra/aws/globgrph/{cse_emit_graphhead,c2c3_liveness_acceptance}.py` | B->A | **DECLARED already-served** | they reach the graph by SUBPROCESS to `kuzu_cli.py`, which D-3 already made a thin client; nothing local remains on their path |
| 17 | `org/modules/graph/iam_cli.py` | B->A | **DECLARED already-served** | calls `comp_iam_live.kuzu_iam_rows()`, repointed at row 4 |
| 18 | `infra/aws/globgrph/{kuzu_ac_traversals,kuzu_cost_enrich}.py` | (engine-side) | **DECLARED** | they open a `--db` argument supplied by the caller, never `CANONICAL_DB_PATH`; they are loader-side enrichment, not user-facing consumers |
| 19 | `infra/aws/globgrph/{kuzu_nessie_load,kuzu_incremental_refresh,projection_worker,projection_server,_provenance}.py` | C | **DECLARED-CLOUD-ENGINE** | untouched; D7-AC5 pins three of them |
| 20 | `infra/aws/globgrph/_canonical.py` | D | **NOT REMOVED -- BLOCKING** | row **W2-S13** |
| 21 | `org/modules/heatmap/ms_heat_index.py` | **B, MISSED BY THE CUT** | **BLOCKING-ROW** | opens `CANONICAL_DB_PATH`, calls `ensure_fresh`; NOT in `<paths>` |
| 22 | `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/NFRA_EDGES_P3_c3_subgraph.py` | B | **BLOCKING-ROW** | `ensure_fresh` + `refresh_failure`; NOT in `<paths>` |
| 23 | `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/l1a_item1b/sensor_kuzu_schema_residue.py` | B | **BLOCKING-ROW** | `CANONICAL_DB_PATH`; NOT in `<paths>` |
| 24 | `infra/aws/globgrph/tests/test_canonical_rebuild_liveness.py` | E | **BLOCKING-ROW** | 10 hits; its entire subject is the mutex/heartbeat being removed; NOT in `<paths>` |
| 25 | `infra/aws/globgrph/tests/test_canonical_refresh_failure_signal.py` | E | **BLOCKING-ROW** | 3 hits; NOT in `<paths>` |
| 26 | `infra/aws/globgrph/tests/test_comp_cluster_cli.py` | E | **BLOCKING-ROW** | `_DB = Path(_canonical.CANONICAL_DB_PATH)`; NOT in `<paths>` |
| 27 | `org/modules/graph/tsgraph_spike/{load_scratch_kuzu,load_clusters_scratch}.py` | (spike) | **BLOCKING-ROW** | the only two remaining `kuzu.Database(` opens under the tool homes; own scratch DB; NOT in `<paths>` |
| 28 | `.tools/tests/{test_cg6_thin_client_battery,test_cg7_status_read_battery}.py` | E | **BLOCKING-ROW** | name `kuzu_nessie_db` in FORBIDDEN-token lists and fixtures; NOT in `<paths>` |
| 29 | `org/modules/graph/debtscan/{comp_similar,summary_corpus}.py` | E-adjacent | **BLOCKING-ROW** | parse a `DB: kuzu_nessie_db` provenance header; `.tools/tests/test_comp_similar_battery.py` (in grant) must keep the matching fixture string; NOT in `<paths>` |
| 30 | `org/modules/graph/compproof/tool_probe.py`, `comp_tool_health{,_gate}.py`, `infra/aws/globgrph/extract_gold_compute.py`, `org/modules/graph/tests/test_{pulse_map_autorefresh,cycle_a_ensure_fresh_wire,cycle_a1_gate_feed_readonly}.py`, `.tools/{stitch-refresh,comp-stitch-refresh}` | **NOT THIS SEAM** | **DECLARED-UNRELATED** | they carry the TOKEN `ensure_fresh` for a DIFFERENT freshness family (tool_probe's health corpus, the pulse-map danger map, the TraceGraph fold). D7-AC1's pattern cannot tell them apart from the Kuzu seam; 21 of its 55 surviving hits are these. NOT in `<paths>` |

**The census's own denominator line, quoted from the tool:**
`DENOMINATOR: 269 hit(s) across 881 file(s) scanned in scope [corpus=all] | 5 EPHEMERAL-FLOOR, NOT searched (--corpus raw reads these) | 5 BINARY, NOT searched`

---

## 2. THE CLIENT EXTENSION -- stated, as the face requires

The face permits extending `projection_client.py` "only if a consumer needs a `query_all(statements)`
helper -- say so". **I did, and here is what and why.** `projection_client` gained, after `health()`:

- `ServedResult` -- a kuzu-RESULT lookalike (`has_next()` / `get_next()` / `get_column_names()` /
  `dicts()`), and `ServedConnection` -- a kuzu-CONNECTION lookalike (`execute()`), plus `connect()`,
  `query_all(statements)` and `vintage_line(source, counts)`.
- **It is an ADAPTER, never a second transport.** Every statement still leaves through the same
  `_request` -> `/graph/cypher`. Nothing in it opens, names, caches or writes a local database, and
  it holds a response only for the life of the call.
- **Why once instead of fifteen times:** ~15 retired consumers share exactly one call shape
  (`conn.execute(q)` then `res.has_next()` / `res.get_next()`). Porting that shape once is the
  minimum code that works (build ladder rung 7) and it removes fifteen chances to get row ordering
  wrong.
- **Row ordering is not assumed, it is grounded:** `projection_server.KuzuAdapter.query` builds each
  row as `dict(zip(result.get_column_names(), result.get_next()))`
  (`infra/aws/globgrph/projection_server.py:246-252 @da35a5dfa0`), and both `json.dumps` server-side
  and `json.loads` client-side preserve insertion order, so `list(row.values())` reproduces kuzu's
  own `get_next()` tuple. This is written into the module's comment, not left implicit.

---

## 3. THE SEAM -- what was removed, what was not, and exactly why

**Removed: nothing in `_canonical.py`.** The order's step 3 asked for `ensure_fresh`, the rebuild
functions, the mkdir mutex, the heartbeat/liveness block, the `_FALLBACK_SINK_SUFFIX` sink writer and
the refresh-status writer to go, and for the file to be deleted if nothing imports it.

An UNSCOPED census (`python .tools/comp-find 'import _canonical' . --all --limit 60` ->
`41 hit(s) across 28949 file(s)`) found **six live importers, five of them outside the `<paths>`
block** -- rows 21-26 of the table above. Removing the seam turns each into an ImportError or
AttributeError at runtime in a file this worker may not edit. `org/modules/heatmap/ms_heat_index.py`
is not a test: it is a class-B consumer by this order's own definition, and it was invisible to the
cut because the cut's census was scoped to three directories that do not include `org/modules/heatmap`.

**So the seam stands, D7-AC1 is FAIL, and the sink still has its writer** -- though no consumer left
calls it:

```
python .tools/comp-find '_FALLBACK_SINK_SUFFIX|_append_fallback_sink|kuzu_nessie_db\.fallback' \
       .tools org/modules/graph infra/aws/globgrph --all --limit 40
  DENOMINATOR: 4 hit(s) across 883 file(s) scanned
    infra/aws/globgrph/_canonical.py:489  _FALLBACK_SINK_SUFFIX = ".fallback.jsonl"
    infra/aws/globgrph/_canonical.py:496  return db_path.rstrip("/\\") + _FALLBACK_SINK_SUFFIX
    infra/aws/globgrph/_canonical.py:499  def _append_fallback_sink(...)
    infra/aws/globgrph/_canonical.py:603  _append_fallback_sink(db_path, behind_n, served, "inc-served-labeled-stale", log)
```

All four are the definition and its own internal call. **Zero consumers.** What remains is a seam
nothing on a user-facing path can reach -- which is most of the retirement's EFFECT without its FORM,
and the difference is exactly what row W2-S13 hands back to the issuer.

---

## 4. THE DISCLOSURE LINE (CE-g-2's engine half, carried)

**Before** (`org/modules/graph/cli.py`, TO-CE-G-2 @`65a85beb44`):
`VINTAGE: DB: kuzu_nessie_db (19917 nodes / 34948 edges)  built: <ISO> (age: 12.4h)  STALE-SERVED: inc-served-labeled-stale`

**After:**
`VINTAGE: Built from the estate as of 2026-09-05 12:54:31 UTC.  [vintage=2026-09-05T12:54:31.241426+00:00 manifest=1b619cc0e6a7 nodes=27292 edges=58771]`

**The `STALE-SERVED` arm is REMOVED, and here is the reasoning, said out loud as the face asks.** On
a served graph the POINTER IS THE VINTAGE: the service installs a generation atomically and hands
every caller that generation, so there is no state in which a caller is served one vintage while a
fresher one is withheld. Both of the old label's carriers are gone with it -- the on-disk
`._refresh_status.json` marker (written by `_incremental_or_serve_stale`) and the live
`needs_refresh` predicate. A disclosure field that can never be populated is a false reassurance,
not a disclosure, so it was deleted rather than left rendering a permanent `None`.

**It was not deleted silently.** `test_g2_disclosure_battery.py`'s stale-served arm is INVERTED
rather than dropped: `test_no_stale_served_arm` asserts the renderer never emits the label AND
carries a RED mutant that DOES emit one, so the arm still discriminates. An OLD vintage is still
fully disclosed (the arm checks that removing the label did not remove the age). comp-trace's half is
untouched -- its universe is still a local head-pinned TraceGraph cache, so it still reports
`VINTAGE: DB: graph.json (2131 nodes / 2922 edges) built: ... (age: 0.1h)`.

---

## 5. THE REAL RUNS -- every repointed tool, quoted whole, with wall time

**Gateway health, first act:**
`{'status': 'ok', 'vintage': '2026-09-05T12:54:31.241426+00:00', 'pointer_read_at': '2026-09-05T12:56:35.199998+00:00', 'last_swap': '2026-09-05T12:56:35.206930+00:00'}` (2.89 s)

### 5.1 Per-consumer latency and payload through the gateway (D7-AC8's substance)

| call | rows | wall | response bytes | budget | verdict |
|---|---|---|---|---|---|
| `MATCH (n:CloudNode) RETURN count(n)` | 1 | 2.94 s | ~200 B | -- | -- |
| **universe NODES** (`n.node_id, n.node_type, n.name, n.layer, n.arn, n.source, n.drift_class`) | 27 292 | **4.34 s** | **6 994 953 B** | -- | -- |
| **universe EDGES** (`a.node_id, b.node_id, e.edge_type`) | 58 771 | **1.56 s** | **11 911 107 B** | -- | -- |
| **comp-blast** end to end (both of the above + traversal) | -- | **14.05 s** | 18.9 MB total | 90 s | **within** |
| **comp-find --corpus aws** unscoped pull | 2 158 nodes | **2.80 s** (tool-reported `used 2.8 s`) | -- | 120 s | **within** |
| **comp-detect** gate (7 detector queries) | -- | **5.30 s** | -- | -- | **within** |
| **comp-cluster** `--coverage` | -- | **4.92 s** | -- | -- | **within** |
| **comp-canon-motif** full scorecard | -- | **5.59 s** | -- | -- | **within** |
| **comp-debt** | -- | 5.34 s | -- | -- | **REFUSED on the STITCH surface** (row W2-S17) |

**Largest response measured: 11 911 107 bytes (11.36 MiB)**, the edge pull. The gateway's 1 MiB limit
is on the REQUEST body; the largest request sent was 118 bytes of Cypher. **NO consumer exceeded its
own `--budget` through the gateway**, so no OBSERVATION row was owed on latency and none was filed on
that ground. The t4g.nano single worker served an 18.9 MB two-query universe in 5.9 s of wall time.

### 5.2 The runs themselves

**comp-find --corpus aws** (`python .tools/comp-find --corpus aws 'opal-globgrph' --budget 120 --limit 5`):
```
comp-find [aws content] 'opal-globgrph'
  WITHIN BUDGET: scanned 1 of 1 pull; budget: 120 s (flag), used 2.8 s
  DEFERRED: 0 of 1 pull(s) did not return -- each names its reason below
  VINTAGE: Built from the estate as of 2026-09-05 12:54:31 UTC.  manifest: 1b619cc0e6a7
  DENOMINATOR: 87 hit(s) across 2158 aws node(s) scanned [corpus=aws]
  DRIFT (scanned): unset=232 AWS_MANAGED=37 DECLARED=1563 LIVE-INCREMENTAL=3 LIVE-no-DECLARED=323
  BANDS = node_type (true totals, not this page): DYNAMODB_TABLE=2 ECS_CLUSTER=1 ECS_TASK_DEFINITION=9
          EVENT_RULE=4 IAM_POLICY=33 IAM_ROLE=19 LAMBDA=1 LOG_GROUP=7 SCHEDULE=1 SECURITY_GROUP=6 SQS_QUEUE=4
  PAGE 1 of 18  (showing 5 of 87)
```
**A DISPLAY-ORDER CHANGE I MADE AND AM NAMING:** at base this block printed DENOMINATOR ABOVE VINTAGE.
D7-AC3's expect (`VINTAGE: ...[\s\S]*hit\(s\) across`) requires the reverse order, and the vintage is
the frame the number is read inside, so I moved the VINTAGE line above the DENOMINATOR. No battery
pinned the old order (checked: `test_comp_find.py`, `test_comp_find_battery.py` parse the DENOMINATOR
line by content, not position).

**comp-blast** (`bash .tools/comp-blast component:AdvisorsTab.tsx --budget 90`, rc=3, 14.05 s):
```
=== served cloud graph (opal-globgrph projection) ===
  Built from the estate as of 2026-09-05 12:54:31 UTC.
  vintage: 2026-09-05T12:54:31.241426+00:00
  manifest: 1b619cc0e6a7524e1ed89d80825c38e612795c1acb63beb239cbb4891ce384af
  artifact: projection/2026-09-05T12:54:31.241426+00:00/
  universe: 27292 nodes / 58771 edges (served, whole estate)
  transport: HTTPS /graph/cypher -- no local database, no cache, no fallback
VINTAGE: Built from the estate as of 2026-09-05 12:54:31 UTC.  [vintage=2026-09-05T12:54:31.241426+00:00 manifest=1b619cc0e6a7 nodes=27292 edges=58771]
NOT-FOUND: no graph node matches 'component:AdvisorsTab.tsx' -- ...
  denominator: 27292 nodes (CANONICAL KUZU GRAPH) -- C2Motif=6303, MS_FILE=5049, Field=4969, ...
ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS
```
rc=3 is the tool's ratified NOT-FOUND state, not a failure: the subject `component:AdvisorsTab.tsx`
is genuinely absent (the real node is
`component:portal/src/pages/AdvisorIntelligence/_shared/tabs/AdvisorsTab.tsx`, which the near-match
block names). The criterion's expect is on the VINTAGE line, which is present.

**comp-detect** (`python infra/aws/globgrph/comp_detect.py`, 5.30 s):
```
=== comp-detect (NFRA_TSGRAPH P3-3 fold-tool) -- gate ===
graph: served cloud graph  status=current  snapshot=8205589666541874180
ID   TIER          NAME                             ROWS    NEW EXEMPLAR
D1   autonomous    detect-silent-display-fork          5      0 caught
D2   autonomous    detect-cross-firm-asymmetry         2      0 caught
D3   advisory      detect-hardcoded-firm-literal       4      0 MISS
D4   candidate-gen detect-dead-component             121      0 caught
D5   advisory      detect-orphan-endpoint             49      0 caught
D6   skip          detect-prop-drill-depth             0      0 -
D7   advisory      detect-render-without-null-gua    197      0 caught
GATE: clean (exit 0)
```

**comp-cluster** (`python infra/aws/globgrph/comp_cluster_cli.py --coverage`, 4.92 s):
```
VINTAGE: Built from the estate as of 2026-09-05 12:54:31 UTC.  [vintage=2026-09-05T12:54:31.241426+00:00]
page-tree coverage: 118/119 assigned, 1 VISIBLE unresolved (0 silent)
  UNRESOLVED: portal/src/pages/Attribution/constants/holdings-shared.tsx  (page .tsx not in any cluster -- barrel/constants/no-RC)
```

**comp-canon-motif** (`python infra/aws/globgrph/canon_motif_scorer.py`, 5.59 s):
```
=== comp-canon-motif scorecard (NFRA_DEBTSCAN TO-D3) ===
graph: served cloud graph  status=current  canon=v0.1  suppression=22 classes
[SERVED_LINEAGE_CANON]  dominant (ServedURL)-[SERVED_FROM]->(S3) = 27/45 (60%) MEETS>=60% | recompute/guarded=482 conditioned=23
  ** AC4 NOVEL: SERVED_LINEAGE_CANON/recompute_fork -- 2 site(s)
[AUTH_CANON]  naive missing_auth_edge=131 -> suppressed=131 (FP_API_LAMBDA,FP_LEDGE) -> filed RED=0
AC4 novel-candidate(s): 1 -> SERVED_LINEAGE_CANON/recompute_fork
```

**comp-debt** (`python infra/aws/globgrph/comp_debt.py`, 5.34 s): `REFUSE: kuzu_stitch_db not found
at C:\tmp\wk-cldgrph-2-d7\infra\aws\globgrph\kuzu_stitch_db -- the REACHABILITY stitch surface.` The
nessie leg is repointed; the STITCH leg is a SECOND local Kuzu graph no cell of this project retires.
Row **W2-S17**.

---

## 6. THE BATTERIES (class E), direct AND under pytest at the file grain

| battery | direct | pytest (file grain) | change |
|---|---|---|---|
| `.tools/tests/test_g2_disclosure_battery.py` | `PASS`, `7 of 7 arm(s)` | pass | 6 arms -> 7; `import _canonical` removed; stale-served arm INVERTED; new `test_no_local_db_arm` proves the loader REFUSES a local path |
| `.tools/tests/test_comp_find_battery.py` | `12/12 PASS (denominator 12)` | pass | was `6/10` at base (4 arms SKIPped for "no local Kuzu CLI/DB on this box"); `_aws_exercisable` now probes the SERVICE; G5 orphan arms replaced by spawn-free arms + a positive control |
| `.tools/tests/test_comp_similar_battery.py` | `PASS (12/12)` | pass | unchanged; its one `kuzu_nessie_db` string is a MUTANT FIXTURE fed to `summary_corpus._capture_kuzu_vintage`, whose parser is out of grant (row W2-S14) |

```
python -m pytest .tools/tests/test_comp_find_battery.py .tools/tests/test_g2_disclosure_battery.py \
                 .tools/tests/test_comp_similar_battery.py -q
9 passed in 38.16s
```

**The G5 repoint is the one worth reading.** The original arms guarded an ORPHANED GRANDCHILD:
comp-find shelled out to `kuzu_cli.py`, which spawned `kuzu_incremental_refresh.py`, so a killed
budgeted client left the grandchild holding the rebuild mutex (row NFRA_COMPEFFICACY-S6, PID 25896,
743 s past its ceiling). **That class is now removed by CONSTRUCTION, not by supervision** -- the aws
corpus is one in-process HTTPS call, so there is no child, hence no grandchild and no mutex. The arm
therefore pins the stronger property (the aws path spawns NOTHING, read from the tool's own source)
with a POSITIVE CONTROL running the same detector over a source that DOES spawn -- so its zero is a
measured absence rather than a matcher that cannot fire.

---

## 7. THE RETIREMENT PROOF (step 5) -- every zero beside a control

**D7-AC1's pattern, as written:**
```
DENOMINATOR: 55 hit(s) across 882 file(s) scanned in scope [corpus=all]   rc=0 (read UNPIPED)
```
NOT zero. 12 in `_canonical.py` (the seam, W2-S13); 2 in the D7-AC5-pinned engine files (W2-S12);
21 in the UNRELATED `ensure_fresh` family (table row 30); the rest in out-of-grant tests. Baseline
before any edit was 71, so this branch removed 16. **The 55 IS its own positive control**: the same
verb over the same paths returns non-zero with a real denominator, so this is a measured presence.

**D7-AC2's pattern, as written:**
```
comp-find: WARNING: pattern contains '\|' / '\(' / '\)' -- python re treats these as LITERAL
  characters ... A 0-hit result below may be this, not a real absence.
DENOMINATOR: 41 hit(s) across 798 file(s) scanned in scope [corpus=all]   rc=0 (read UNPIPED)
```
NOT zero (baseline 46). 13 in-grant, all prose or a deliberate negative assertion; 28 out of grant
(W2-S14). **Note the tool prints its own false-zero warning on this criterion's pattern**, so even a
true zero here would have arrived with a caveat attached.

**The SUBSTANTIVE measurement, with its positive control on the same verb and the same paths:**
```
python .tools/comp-find 'kuzu\.Database\(' org/modules/graph .tools --all --limit 50
  DENOMINATOR: 2 hit(s) across 798 file(s) scanned in scope [corpus=all]
    org/modules/graph/tsgraph_spike/load_scratch_kuzu.py:97:    db = kuzu.Database(DB_PATH)
    org/modules/graph/tsgraph_spike/load_clusters_scratch.py:43: db = kuzu.Database(DB_PATH)

POSITIVE CONTROL, same verb, same paths, same corpus:
python .tools/comp-find 'projection_client' org/modules/graph .tools --all --limit 5
  DENOMINATOR: 35 hit(s) across 798 file(s) scanned in scope [corpus=all]
```
**798 files scanned, not 0** -- so neither reading is out-of-corpus. Both surviving opens are spike
scratch loaders opening their OWN `DB_PATH`, not `kuzu_nessie_db`, and both are outside the grant.

**The cloud engine's hashes (D7-AC5), re-derived:**
```
8b79ca1bdfd51c1823c0c6780086d55d7e9c751d7651820f873cf1d4b42a5b3d   kuzu_nessie_load.py
80d60f8ffa3c3c5da735c781d695d233496d31ac7bd2b7dabde034b718b1ef71   kuzu_incremental_refresh.py
9dd104db29d558e48ecb5a28f8df9464fdca502eb25acffc680fdf696b7fe059   projection_server.py
```
All three match the criterion's expect exactly. **The pin did not decay under this worker.**

---

## 8. D7-AC8 (judgment; NO verdict -- `3.0.0_SA_CVO` grades this at L9)

- **The census table** is s.1. **Per-consumer latency and payload** is s.5.1. **No consumer failed
  its own budget through the gateway**, so no latency ROW was owed and none was filed on that ground.
  The largest response measured was 11 911 107 bytes.
- **Does anything user-facing still hold a path to a local build?** Reading the evidence rather than
  asserting: **no tool a user invokes can trigger a local rebuild any more** -- every entry point
  that used to call `ensure_fresh` (comp-blast, comp-find `--corpus aws`, comp-detect, comp-debt's
  nessie leg, comp-cluster, comp-canon-motif, comp-marker-read, the debtscan scorer) now reaches the
  service, and the thin `kuzu_cli.py` has had no `--mode`/`--refresh` flag since TO-CG-D-3.
  **But three things qualify that:** (i) `_canonical.ensure_fresh` still EXISTS and
  `org/modules/heatmap/ms_heat_index.py` still calls it -- a user running the heatmap index still
  triggers a local rebuild attempt (W2-S13); (ii) `kuzu_stitch_db` is a second local graph with a
  local producer (`.tools/comp-stitch-refresh`) that this project never retired (W2-S17); (iii) the
  laptop's own `kuzu_nessie_db*` directory is the issuer's to delete at the drain and is not in this
  worktree, so what this branch proves is that the CODE no longer reads it -- not that the bytes are
  gone.
- **The instrument caveat the CVO should carry:** D7-AC1 and D7-AC2 are TOKEN censuses, and a token
  census cannot distinguish "this file calls the seam" from "this file mentions the seam in a
  comment" or "this file has a same-named function in a different subsystem". 21 of AC1's 55
  surviving hits are the third case. The criterion that actually measures the retirement is the
  `kuzu\.Database\(` count in s.7, and it reads 2 -- both out of grant, neither on a user path.

---

## 9. ROWS FILED (all six, at `NFRA_CLDGRPH-W2-S<k>` continuing this seat's W2 numbering)

Channel denominator: **101 rows before this append, 107 after**, counted by PARSING every fenced
json block and summing their lengths (101 in 99 blocks -> 107 in 105 blocks), never by an id grep.
W2-S1..W2-S11 are this seat's prior rows from TO-CG-D-3; none is edited or renumbered.

| id | class | hazard | one line |
|---|---|---|---|
| `NFRA_CLDGRPH-W2-S12` | BLOCKING | INERT | D7-AC1's zero is unreachable: its pattern is carried by two engine files D7-AC5 pins byte-identical |
| `NFRA_CLDGRPH-W2-S13` | BLOCKING | **ARMED** (`2.0.0_SA_COO~A`) | the seam cannot be removed: SIX out-of-grant importers, one a class-B consumer the scoped census could not see |
| `NFRA_CLDGRPH-W2-S14` | BLOCKING | INERT | D7-AC2's zero is unreachable: 28 of 41 hits outside the grant |
| `NFRA_CLDGRPH-W2-S15` | BLOCKING | INERT | D7-AC3 runs a Python file under `bash`; it cannot produce its expect for any state of the world |
| `NFRA_CLDGRPH-W2-S16` | OBSERVATION | INERT | `comp-find --corpus aws` was already BLOCKED at base -- D-3's thin client stranded it two orders ago |
| `NFRA_CLDGRPH-W2-S17` | OBSERVATION | **ARMED** (`2.0.0_SA_COO~A`) | `kuzu_stitch_db`: a second local Kuzu graph no cell retires; comp-debt REFUSES without it |

**Untracked artifact, not committed:** `infra/aws/globgrph/tsgraph_detect_ledger.json` was written by
the comp-detect run in s.5.2. It is not in this order's `<paths>` and is left in the worktree.

---

## 10. WHAT THE NEXT ORDER NEEDS

1. A `<paths>` grant covering `org/modules/heatmap/ms_heat_index.py`,
   `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/NFRA_EDGES_P3_c3_subgraph.py`,
   `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/l1a_item1b/sensor_kuzu_schema_residue.py`,
   `infra/aws/globgrph/tests/test_canonical_{rebuild_liveness,refresh_failure_signal}.py`,
   `infra/aws/globgrph/tests/test_comp_cluster_cli.py`. With those six, the seam removal and the
   deletion of `_canonical.py` are a single small act -- every other consumer is already repointed.
2. D7-AC1 re-cut to EXCLUDE `infra/aws/globgrph` (or to exclude the two pinned engine files by name),
   and to use a pattern that word-boundaries the seam's `ensure_fresh` away from `tool_probe`'s.
3. D7-AC2 re-cut to the substantive predicate (`kuzu\.Database\(` opens) rather than a token census
   over config, data and documentation.
4. D7-AC3's invocation corrected from `bash` to `python`.
5. A ruling on `kuzu_stitch_db` (W2-S17): retire it, or state that the estate keeps one local graph.


---
---

# PASS 2 -- the RETIREMENT, executed on the AMENDED order

**Worker:** `0.9.0_WK_NFRA_CLDGRPH~2` (same seat, same branch `wk-cldgrph-2-d7`).
**Base for this pass:** `3aab23b264` (the issuer merged CLOUD in, bringing the amended order).
**Push state: LOCAL** (never pushed). **Measured:** 2026-09-06 00:5xZ - 01:3xZ, every invocation
bounded by `timeout`.

**Everything above this line is PASS 1 and stands.** This section EXTENDS it. Pass 1's ten
repointed consumers, its three green batteries and its census table are carried by citation, and
where this pass moved one of them it says so by name.

---

## P2.0 CONCLUSION FIRST

**The RETIREMENT landed. Two absence CRITERIA still do not read zero, and neither zero is
reachable by any act -- so the order stays OPEN.**

- **The seam is gone.** `infra/aws/globgrph/_canonical.py` went from **746 lines to 78**: no
  `ensure_fresh`, no rebuild functions, no mkdir mutex, no heartbeat/liveness block, no atomic
  swap, no supervised rebuild child, no `.fallback.jsonl` sink writer, no `._refresh_status.json`
  failure-marker writer. What remains is a TOMBSTONE that REFUSES.
- **The last live consumer is repointed.** `org/modules/heatmap/ms_heat_index.py` -- the class-B
  consumer the cut's scoped census could not see -- now reads the served graph:
  **6,134 MS nodes in 4.56 s**, `served_manifest=a2e68928695068b5`, dry run `0 writes`.
- **The three seam tests moved with the behaviour they pin**: two DELETED (their subject no longer
  exists), one REPOINTED (its subject survives), and the properties that outlive the seam carried
  into a new battery that passes **6 of 6 with its RED MUTANT convicted 10 of 10**.
- **D7-AC1 = 36 hits, D7-AC2 = 54 hits. Both FAIL by output.** And **zero of the 36 and zero of
  the 54 is a live call into, or a live open of, the retired surface.** The anchored measurement
  of actual calls returns **3, all three prose**; of actual local opens, **2, both out-of-grant
  spike loaders on their own scratch path**. Row **W2-S21**.
- **D7-AC3 passes on the corrected interpreter.** D7-AC4, AC5, AC6, AC7 re-run and pass; **D7-AC5's
  three pins did NOT decay** at this HEAD.

**MECHANICAL RESULT: 5 PASS (D7-AC3, D7-AC4, D7-AC5, D7-AC6, D7-AC7), 2 FAIL (D7-AC1, D7-AC2),
1 RECORDED-judgment (D7-AC8). THE ORDER STAYS OPEN.** The flip was not reached for.

---

## P2.1 (a) THE MISSED CONSUMER -- `org/modules/heatmap/ms_heat_index.py`, repointed

`read_ms_nodes()` opened the local canonical DB after calling `_canonical.ensure_fresh(db_path)`.
It now does what every other class-B consumer does:

```
conn = projection_client.connect()
q = conn.execute("MATCH (n:CloudNode) WHERE n.node_type IN ['MS_FILE','MS_FOLDER'] "
                 "RETURN n.node_id, n.node_type, n.props")
```

**Three things changed beyond the transport, and each is stated rather than left implicit.**

1. **The refresh call is not replaced by a poll -- it is unnecessary.** The service installs one
   generation atomically, so a reader cannot be handed one vintage while a fresher one is
   withheld, which is the exact condition `ensure_fresh` existed to remove. An unreachable service
   RAISES instead of computing heat over a stale local copy: a visible gap, never a silent old
   answer.
2. **`db_path_basename` is gone from `graph_vintage`, replaced by `served_vintage` /
   `served_manifest` / `served_artifact` / `transport`.** It named a FILE, not a generation. A
   census before removing it found **1 hit across 28,986 files -- the producing line itself, zero
   consumers**, so nothing downstream reads it.
3. **One header invariant was AMBIGUOUS and is now precise.** The module docstring said "it opens
   no gateway call". In context that meant the MICROSOFT Graph API, and it is still true -- but
   the module now does make one call to the opal-globgrph projection gateway, so the sentence was
   rewritten to say which gateway it means instead of quietly becoming false.

**EXERCISED LIVE, not asserted:**

| call | rows | wall | payload | result |
|---|---|---|---|---|
| `read_ms_nodes()` | **6 134** | **4.56 s** | -- | `served_vintage=2026-09-06T00:50:34.138427+00:00`, `served_manifest=a2e68928695068b512b086d88a1196b20d18e9302f7fbcca6c30f2e5ea9e0e2f` |
| the same query measured at the client | 6 134 | 4.71 s | **5 198 893 B** | -- |
| `ms_heat_index.py --dry-run` end to end | 6 134 | -- | -- | `OK: MS_HEAT_COMPUTED scored=6134/6134 bands={'hot': 59, 'warm': 268, 'cold': 5807} clusters=1071` / `OK: DRY_RUN (0 writes)` |
| `ms_heat_index.py --self-test` | -- | -- | -- | `=== 9/9 PASS ===` (pure logic, unchanged by the repoint) |

There is **no budget flag on this tool**, so it cannot exceed one; the 4.56 s read is recorded
against the largest gateway response pass 1 measured (11 911 107 B) for scale.

---

## P2.2 (c) THE SEAM -- what was removed, what remains, and who imports it

**`infra/aws/globgrph/_canonical.py`: 746 lines -> 78. Removed in full:** `ensure_fresh`,
`_full_rebuild_only`, `_incremental_or_serve_stale`, `_incremental_or_full_rebuild`,
`_default_rebuild`, `_run_child_supervised`, the mkdir mutex (`_owns_lock`, `_rmlock`, `_gen_path`,
`_write_gen`, `ORPHAN_LOCK_S`, `MUTEX_WAIT_S`), the liveness block (`_liveness_on`, `_Heartbeat`,
`_beat`, `_hb_path`, `_hb_age`, `HEARTBEAT_INTERVAL_S`, `HEARTBEAT_STALE_S`), `_atomic_swap`,
`_unique_tmp`, `_gc_stale_tmps`, `_rm`, `_rm_kuzu`, the sink (`_FALLBACK_SINK_SUFFIX`,
`_fallback_sink_path`, `_append_fallback_sink`), the refresh-status writer
(`_refresh_status_path`, `_write_refresh_failure`, `_clear_refresh_failure`, `refresh_failure`),
`needs_refresh`, `is_canonical`, `_served_vintage`, `_served_age_str`, `_parse_changed`,
`_apply_summary_overlay`, and the constants `CANONICAL_DB_NAME` / `CANONICAL_DB_PATH` /
`REBUILD_TIMEOUT_S` / `INCREMENTAL_TIMEOUT_S` / `TMP_GC_AGE_S` / `SWAP_RETRY*` / `RECHECK_SLEEP_S`.

**WHAT REMAINS: a tombstone that REFUSES.** A module docstring stating the retirement and naming
the replacement, and a PEP 562 module `__getattr__` that raises `RuntimeError` for every attribute,
naming R7, the order and `projection_client`.

**WHY IT WAS NOT DELETED, said plainly, because the face asked for exactly this.** The order
offered both: state what remains and who imports it, OR delete the file and say so. **Two files
outside this order's write grant still import it and call into it, and they are another seat's
deliverables -- historical records, not live tool surface:**

| importer | what it reaches for | disposition |
|---|---|---|
| `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/NFRA_EDGES_P3_c3_subgraph.py:427` | `_canonical.ensure_fresh` (:413 doc, :451 doc), `_canonical.refresh_failure` (:443), `_canonical.CANONICAL_DB_PATH` (:429) | **KNOWN-STALE-IMPORTERS-OUT-OF-LANE** -- untouched |
| `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/l1a_item1b/sensor_kuzu_schema_residue.py:216` | `_canonical.CANONICAL_DB_PATH` (:218); and at **:88** it lists `_GLOBGRPH / "_canonical.py"` BY PATH in a set it opens | **KNOWN-STALE-IMPORTERS-OUT-OF-LANE** -- untouched |

**SO: SAYING IT PLAINLY, AS ORDERED.** *Deleting `_canonical.py` would break both of those files'
imports outright, and would additionally break `sensor_kuzu_schema_residue.py:88`, which does not
import the module but READS IT AS A FILE. Retiring the seam breaks their CALLS either way -- there
is no version of this retirement in which `ensure_fresh` still works for them. Repointing them is
THEIR OWNERS' CALL, not this worker's: the grant that retired the seam does not reach another
seat's deliverables, and a path missing from `<paths>` is a wall, not an oversight to route
around.*

**The tombstone is the better of the two options for them, and here is the reasoning rather than
the preference.** Deletion gives them `ImportError: No module named '_canonical'` -- a message that
names Python, not the decision, and that reads identically to a broken checkout. The tombstone
gives them:

```
RuntimeError: _canonical.ensure_fresh is RETIRED (NFRA_CLDGRPH PRD R7 / FWD-7, cell CG-s-8,
task order TO-CG-D-7). The local canonical Kuzu database and its rebuild seam no longer exist:
the estate graph is BUILT in the cloud and SERVED, so there is no local copy to refresh and no
rebuild to trigger. Use infra/aws/globgrph/projection_client.py (connect() / query() /
vintage_line()). If this call is reached from a file outside NFRA_CLDGRPH's grant, repointing it
belongs to that file's owner.
```

**Two design points in the refusal are load-bearing and are not stylistic.**

- **It is `RuntimeError`, NOT `AttributeError`.** A caller writing
  `getattr(_canonical, "ensure_fresh", None)` or `hasattr(...)` would read an AttributeError as
  "older build, no refresh available" and carry on over whatever it found locally. There is no
  local database left to carry on over, so the loud stop IS the safe behaviour. Both soft-probe
  forms are pinned to raise (arm 2 of the new battery).
- **It is `__getattr__`, NOT a list of retired names.** A hand-kept enumeration drifts; a symbol
  nobody thought to enumerate would resolve to `AttributeError` and degrade silently. Module
  `__getattr__` is MECE over the module's whole attribute space by construction, and the battery
  proves it with a control name that never existed (`a_symbol_that_never_existed` refuses exactly
  like `ensure_fresh`). Dunders fall through to a normal `AttributeError` so `inspect`, pytest
  collection and the import machinery keep working -- a tombstone that broke introspection would
  make the retirement look like a broken install.

**`_provenance.py` is UNTOUCHED (the BOUNDS), and the dependency runs the other way.** `_canonical`
referenced `_provenance._REFRESH_STATUS_SUFFIX`, not the reverse; `_provenance` owns its own
`_read_refresh_failure`. Removing the WRITER therefore strands nothing -- it leaves a reader that
is now inert. That reader's soundness is pinned rather than assumed (arm 4 below).

**The anchored importer census, with the trap the face named.** `import _canonical` matches
`_canonical_silver_lib` as a SUBSTRING and drags in twelve `data/canonical/schwab/*` files from
another lane. Anchored:

```
python .tools/comp-find 'import _canonical\b|from _canonical\b' . --all --limit 60
  DENOMINATOR: 84 hit(s) across 28984 file(s) scanned in scope [corpus=all]
```
Filtered to first-party `.py` (the rest are this channel, this deliverable and the order itself):
**six importers**, and one of the six is a COMMENT (`kuzu_incremental_refresh.py:344`, "Run as a
SUBPROCESS from _canonical"), not an import -- so the live population is **five**, of which
**three were in grant and are now resolved** (`ms_heat_index.py` repointed; the two seam tests
deleted; `test_comp_cluster_cli.py` repointed off it) and **two are out of lane** (the table above).

---

## P2.3 (b) THE THREE SEAM TESTS -- moved with the behaviour they pin

**They were already broken before this pass touched them**, by pass 1's repoint of
`comp_cluster_cli.py`. Baseline, measured first:

```
python -m pytest infra/aws/globgrph/tests/test_comp_cluster_cli.py \
                 infra/aws/globgrph/tests/test_canonical_rebuild_liveness.py \
                 infra/aws/globgrph/tests/test_canonical_refresh_failure_signal.py -q
2 failed, 4 passed, 3 skipped, 6 errors in 0.34s
```

| test | 232+97+146 lines of subject | disposition |
|---|---|---|
| `tests/test_canonical_rebuild_liveness.py` | the #17 mutex / heartbeat / stale-lock steal / per-unique tmp / ownership-check-at-swap | **DELETED** -- with no local database there is no rebuild, hence no winner, no lock, no steal, no swap. (The 6 pytest ERRORs were `fixture 'td' not found`: it is a `__main__` script battery whose functions take a temp-dir argument, so pytest could never have collected it.) |
| `tests/test_canonical_refresh_failure_signal.py` | the #25 failure-marker lifecycle: written on failure, surfaced by the header, cleared on recovery | **DELETED** -- the marker can no longer be written. Its ONE surviving half (the reader must not read a corrupt marker as healthy) is CARRIED, not dropped: arm 4 below. |
| `tests/test_comp_cluster_cli.py` | the stdout/stderr split and the honest denominator | **REPOINTED** -- that subject SURVIVES, so the test moves with the source rather than with the seam. |

**DELETING THEM SILENTLY WOULD HAVE LEFT THE RETIREMENT UNPINNED**, so the properties that outlive
the seam are carried into a new battery: `.tools/tests/test_cg8_seam_retired_battery.py`.

```
python .tools/tests/test_cg8_seam_retired_battery.py
OK seam_machinery: 0 of 10 seam token(s) in _canonical.py; RED MUTANT convicted on 10 of 10
OK retired_symbols: 18 of 18 name(s) refused with RuntimeError (incl. 1 never-existed control); both soft-probe forms also refused
OK import_sane: tombstone imports; 5 dunders resolve; __all__ -> AttributeError
OK marker_reader: 4 of 4 -- absent reads None, corrupt reads unreadable-marker, header agrees with both
OK no_importers: 0 importer(s) across 486 python file(s) in 4 tool home(s); POSITIVE CONTROL 20 file(s) import projection_client/_provenance; matcher convicts a real import and spares _canonical_silver_lib
OK replacement: 5 of 5 client symbols present; 0 of 3 local-DB tokens; RED MUTANT convicted
DENOMINATOR: 6 of 6 arm(s) recorded a pass
PASS                                                                        [rc=0]
```

**THE BATTERY CONVICTED ITS OWN AUTHOR TWICE BEFORE IT PASSED, AND BOTH ARE WORTH THE READING**,
because in each case the arm was right and the instrument was wrong:

1. **Arm 1 first failed on `['kuzu_nessie_db', 'os.replace']` -- inside the tombstone's own
   docstring**, where they appear in the sentence explaining that neither exists any more. A
   retirement notice has to be able to NAME what it retired. The arm was reading text, not
   machinery, so `_code_only()` was added: it strips the module docstring (via `ast`) and every
   `#` comment (via `tokenize`, BLANKING each comment in place). **String literals inside
   functions are deliberately kept** -- a database path in a constant is machinery, not
   commentary.
2. **The first `_code_only` returned the token stream joined by newlines, which silently broke
   every multi-token pattern** (`os.mkdir` became `os`, `.`, `mkdir`), so the RED MUTANT went from
   10 of 10 to 6 of 10 -- and the arm FAILED ON ITS OWN MUTANT rather than reporting a clean
   estate it had not actually inspected. **That is precisely what the mutant is for**, and it is
   the reason the sweep is trustworthy now.

**Arm 5's import matcher carries TWO anchors and both were forced by a measured miss:** the
trailing `(?![\w])` excludes `_canonical_silver_lib`, and the leading `^[ \t]*` requires the
import at STATEMENT position -- without it the arm convicted `test_comp_cluster_cli.py` for
listing `"import _canonical"` in a forbidden-token tuple, i.e. for FORBIDDING the thing. Both
directions are asserted in the arm itself, alongside a lazy-import-inside-a-function positive.

**The repointed `test_comp_cluster_cli.py`, and the oracle failure it exposed:**

```
python -m pytest infra/aws/globgrph/tests/test_comp_cluster_cli.py -q -rs
9 passed, 1 skipped in 21.76s
```

- the CL2 header arm now matches `print(projection_client.vintage_line(...), file=sys.stderr)`;
- the INFO/WARN refresh-diagnostic arm is **INVERTED** -- it asserts those two strings are ABSENT
  (a diagnostic for a branch that cannot run is a false reassurance) and that every surviving
  diagnostic still targets stderr, with a RED mutant on the stderr half;
- a new `test_cl3_no_local_database_is_opened` pins the CLI to the served client;
- **the integration gate no longer skips forever.** It was `skipif(not (kuzu importable and
  CANONICAL_DB_PATH exists))` -- both permanently false, so all three integration arms would have
  SKIPPED on every future run and reported green. It now probes the SERVICE and a skip names why.
- **the independent-denominator arm caught a REAL instrument defect, row `NFRA_CLDGRPH-W2-S20`:**
  `git -C portal ls-files 'src/pages/**/*.tsx'` returned **0** in this worktree and the arm read it
  as `tool denominator 119 vs independent 0`. **`git -C` into an EMPTY submodule directory does not
  fail -- it walks UP and answers from the PARENT repository.** Measured:
  `git -C .../portal rev-parse --show-toplevel` -> `C:/tmp/wk-cldgrph-2-d7`, and
  `git -C .../portal rev-parse HEAD` -> `3aab23b2641be309850d0b4bfbbdbb00b10873ae`, the worktree's
  OWN head. The arm now resolves `--show-toplevel` first and SKIPS with a named reason, and asserts
  `indep > 0` so a checked-out portal yielding zero is still a loud oracle failure. **Four other
  first-party code sites shell the same shape** and are handed over in the row, not touched.

**All five batteries together, at file grain:**
```
python -m pytest .tools/tests/test_comp_find_battery.py .tools/tests/test_g2_disclosure_battery.py \
   .tools/tests/test_comp_similar_battery.py .tools/tests/test_cg8_seam_retired_battery.py \
   infra/aws/globgrph/tests/test_comp_cluster_cli.py -q
24 passed, 1 skipped in 69.00s
```

---

## P2.4 (d) THE CRITERIA RE-RUN -- every zero, and every non-zero, beside its control

### D7-AC1 -- **FAIL by output.** 36 hits, and none of them is the seam.

```
python .tools/comp-find 'ensure_fresh|_full_rebuild_only|_incremental_or_serve_stale|GLOBGRPH_KUZU_INCREMENTAL_REFRESH|GLOBGRPH_KUZU_REBUILD_LIVENESS|_FALLBACK_SINK_SUFFIX' \
       .tools org/modules/graph org/modules/heatmap --all --limit 50
  DENOMINATOR: 36 hit(s) across 810 file(s) scanned in scope [corpus=all]
    | 77 EPHEMERAL-FLOOR, NOT searched | 5 BINARY, NOT searched
  BANDS (true totals, not this page): HEAD=3 DEF=1 SURFACED=11 CONFIG=2 TEST=19
  PAGE 1 of 1  (showing 36 of 36)                                       [rc=0 read UNPIPED]

POSITIVE CONTROL -- same verb, same three paths, a pattern that IS present:
python .tools/comp-find 'projection_client' .tools org/modules/graph org/modules/heatmap --all --limit 3
  DENOMINATOR: 46 hit(s) across 810 file(s) scanned in scope [corpus=all]
```
**810 files scanned on both, so neither reading is `0 hit(s) across 0 file(s)` out-of-corpus.**

**Where the 36 live, from the tool's own banded output:**

| n | population | example |
|---|---|---|
| **22** | the **`tool_probe.ensure_fresh` family** -- a DIFFERENT tool-health freshness subsystem that shares the token | `org/modules/graph/compproof/tool_probe.py:1226 def ensure_fresh(...)`, `test_pulse_map_autorefresh.py` x6 (`_ensure_fresh_danger_map`) |
| **10** | the batteries that must NAME the retired symbols to assert they REFUSE | `test_cg8_seam_retired_battery.py:182-185`, `test_cg6_thin_client_battery.py:59` (a FORBIDDEN-token list) |
| **2** | prose explaining what was removed | `ms_heat_index.py:97,101` |
| **2** | config/data quotes | `comp-coverage-map.yaml:959`, `nerves-risk-edges.json:17610` |
| **0** | **a live call into the retired Kuzu seam** | -- |

**THE SUBSTANTIVE MEASUREMENT, same three paths:**
```
python .tools/comp-find '_canonical\.ensure_fresh|_canonical\.CANONICAL_DB_PATH|_canonical\.needs_refresh|_canonical\.refresh_failure' \
       .tools org/modules/graph org/modules/heatmap --all --limit 20
  DENOMINATOR: 3 hit(s) across 810 file(s) scanned in scope [corpus=all]
    org/modules/graph/cli.py:397        (docstring: what the removed STALE-SERVED arm used to read)
    org/modules/graph/comp_aws_cli.py:2857  (comment)
    org/modules/heatmap/ms_heat_index.py:97 (docstring: what this function used to do)
```
**Three hits, three pieces of prose, zero calls.**

**AND THE COUNT WENT UP UNDER THIS PASS -- 29 before any edit, 36 after -- which is the finding,
not an accident.** The delta is `+9` battery lines `+2` prose lines `-4` `ms_heat_index` seam
lines. An arm shaped as a token census over the tool homes is **ANTI-CORRELATED with the
retirement being properly pinned**: the better the absence is tested, the worse the arm reads.
**The tokens were not contrived away.** Dropping them from the battery would leave the refusal
unpinned in order to satisfy a matcher, which is the act this channel exists to refuse. Row
**`NFRA_CLDGRPH-W2-S21`**.

### D7-AC2 -- **FAIL by output.** 54 hits; 2 real opens, both out of grant.

```
python .tools/comp-find 'kuzu\.Database\(|CANONICAL_DB_PATH|kuzu_nessie_db' org/modules/graph .tools --all --limit 50
  comp-find: WARNING: pattern contains '\|' / '\(' / '\)' -- python re treats these as LITERAL
    characters ... A 0-hit result below may be this, not a real absence.
  DENOMINATOR: 54 hit(s) across 800 file(s) scanned in scope [corpus=all]   [rc=0 read UNPIPED]

POSITIVE CONTROL -- same verb, same paths:
python .tools/comp-find 'projection_client' org/modules/graph .tools --all --limit 3
  DENOMINATOR: 44 hit(s) across 800 file(s) scanned in scope [corpus=all]

THE SUBSTANTIVE MEASUREMENT -- an actual local DB OPEN, same paths:
python .tools/comp-find 'kuzu.Database\(' org/modules/graph .tools --all --limit 20
  DENOMINATOR: 6 hit(s) across 800 file(s) scanned in scope [corpus=all]
    org/modules/graph/tsgraph_spike/load_scratch_kuzu.py:97:  db = kuzu.Database(DB_PATH)      <- own scratch path, OUT OF GRANT
    org/modules/graph/tsgraph_spike/load_clusters_scratch.py:43: db = kuzu.Database(DB_PATH)   <- own scratch path, OUT OF GRANT
    .tools/tests/test_cg8_seam_retired_battery.py:350,366,370,371                              <- forbidden-token literals
```
**Two real opens, both on a spike loader's OWN `DB_PATH`, neither on `kuzu_nessie_db`, both outside
this order's `<paths>`.** Baseline before this pass was 46; the +8 is this order's new battery
naming what it forbids. **Note the tool prints its own false-zero warning on this criterion's
pattern**, so even a true zero here would arrive with a caveat attached. Row **W2-S14** (pass 1)
carries the out-of-grant half unchanged.

### D7-AC3 -- **PASS by output** on the corrected interpreter (`python`, not `bash`).
```
python .tools/comp-find --corpus aws 'opal-globgrph' --budget 120 --limit 5
  WITHIN BUDGET: scanned 1 of 1 pull; budget: 120 s (flag), used 7.36 s
  VINTAGE: Built from the estate as of 2026-09-06 00:50:34 UTC.  manifest: a2e689286950
  DENOMINATOR: 87 hit(s) across 2158 aws node(s) scanned [corpus=aws]
  DRIFT (scanned): unset=232 AWS_MANAGED=37 DECLARED=1563 LIVE-INCREMENTAL=3 LIVE-no-DECLARED=323
  PAGE 1 of 18  (showing 5 of 87)                                                 [rc=0]
```
Pass 1's row **W2-S15** named the `bash`-on-a-`python3`-shebang defect; the amendment fixed it and
this is the measurement that closes it.

### D7-AC4 -- **PASS by output.** 9 s wall (was 14.05 s in pass 1), rc=3 = the ratified NOT-FOUND state.
```
=== served cloud graph (opal-globgrph projection) ===
  universe: 27292 nodes / 58771 edges (served, whole estate)
  transport: HTTPS /graph/cypher -- no local database, no cache, no fallback
VINTAGE: Built from the estate as of 2026-09-06 00:50:34 UTC.  [vintage=2026-09-06T00:50:34.138427+00:00 manifest=a2e689286950 nodes=27292 edges=58771]
ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS
```

### D7-AC5 -- **PASS by output. THE PINS DID NOT DECAY** at `3aab23b264`.
```
8b79ca1bdfd51c1823c0c6780086d55d7e9c751d7651820f873cf1d4b42a5b3d   kuzu_nessie_load.py
80d60f8ffa3c3c5da735c781d695d233496d31ac7bd2b7dabde034b718b1ef71   kuzu_incremental_refresh.py
9dd104db29d558e48ecb5a28f8df9464fdca502eb25acffc680fdf696b7fe059   projection_server.py
```
All three match the criterion's expect exactly. **Re-derived at THIS HEAD, not quoted forward from
pass 1** -- which is the whole point of a decaying pin.

### D7-AC6 -- **PASS by output.** `7 of 7 arm(s)` + `PASS`, rc=0, every arm's RED mutant convicted.

### D7-AC7 -- **PASS by output**, on a list extended by four.
```
pre-commit gate clean (17 .py file(s) + .tools/comp-find; denominator 18 of 18)     [rc=0]
```
The gate script gained `_canonical.py`, `test_comp_cluster_cli.py`, `ms_heat_index.py` and
`test_cg8_seam_retired_battery.py`. The two DELETED tests are deliberately NOT on the list and the
script says why: a gate cannot check a file that no longer exists, and listing them would make the
script `exit 2` on its own success. **It also emitted 4 `MANIFEST-ADVISORY` findings against the new
battery saying it "opens a Kuzu connection directly"** -- all four are the string literals
`"kuzu.Database("` in the forbidden-token tuple it uses to assert that nothing does. Advisory, not
blocking (`OK: pre-commit gate clean for 17 of 17 file(s)`), and filed as row **W2-S22**: this is
the THIRD instrument in this order to confuse a substring for code.

---

## P2.5 D7-AC8 (judgment; NO verdict -- `3.0.0_SA_CVO` grades this at L9)

**THE CENSUS TABLE** is pass 1's s.1 as extended by P2.2's importer table above; rows 21, 24, 25
and 26 of pass 1's table are now RESOLVED (repointed or deleted) and rows 22 and 23 are
**KNOWN-STALE-IMPORTERS-OUT-OF-LANE**.

**PER-CONSUMER LATENCY AND PAYLOAD THROUGH THE GATEWAY.** Pass 1's table (s.5.1) stands; this pass
re-exercised every consumer after the tombstone removed 668 lines they used to be able to reach,
because a citation would not have been evidence for a tree that moved:

| consumer | wall (pass 2) | wall (pass 1) | budget | verdict |
|---|---|---|---|---|
| `comp-blast` (D7-AC4) | **9 s** | 14.05 s | 90 s | within |
| `comp-find --corpus aws` (D7-AC3) | **7.36 s** (tool-reported) | 2.8 s | 120 s | within |
| `comp-detect` | **5 s**, `GATE: clean (exit 0)` | 5.30 s | -- | within |
| `comp-cluster --coverage` | **7 s**, `118/119 assigned, 1 VISIBLE unresolved (0 silent)` | 4.92 s | -- | within |
| `comp-canon-motif` | **8 s**, `AC4 novel-candidate(s): 1` | 5.59 s | -- | within |
| `comp-marker-read` + `comp-iam-live` | **7 s** combined; `status=current`, `iam_live rows=216` | -- | -- | within |
| **`ms_heat_index`** (new this pass) | **4.56 s** read / 6 134 rows / 5 198 893 B | -- | none | within |
| `comp-debt` | 6 s | 5.34 s | -- | **REFUSED on the STITCH surface** (row W2-S17, unchanged) |

**NO CONSUMER EXCEEDED ITS BUDGET**, so no OBSERVATION row is owed on latency and none was filed on
that ground. The largest response measured across both passes remains **11 911 107 B** (pass 1's
edge pull); this pass's largest is the 5 198 893 B MS-node pull.

**DOES ANYTHING USER-FACING STILL HOLD A PATH TO A LOCAL BUILD? Reading the evidence rather than
asserting it:**

- **No. There is no longer any code path, in or out of grant, that can trigger a local canonical
  rebuild** -- because the code that performed one no longer exists. `ensure_fresh` is not
  bypassed, not disabled, not flag-gated: it is deleted, and every name that reached it raises.
  This is a stronger state than pass 1 could report, where the seam survived with zero callers.
- **Two qualifications remain, and they are different in kind from the one above.** (i)
  `kuzu_stitch_db` is a SECOND local Kuzu graph with a local producer (`.tools/comp-stitch-refresh`)
  that no cell of this project retires; `comp-debt` still REFUSES without it (row **W2-S17**,
  unchanged, still ARMED). (ii) Two out-of-lane deliverables still CALL retired names; they will
  now fail loudly rather than rebuild, which is the correct failure but is still a failure their
  owners have not been told about by anything except this document and the tombstone's own message.
- **What this branch proves and what it does not.** It proves the CODE no longer reads the local
  copy. It does not prove the BYTES are gone: the laptop's `kuzu_nessie_db*` directory is gitignored,
  is not in this worktree, and is the issuer's to delete at the drain. `CG-x-7` (two machines, same
  answer, local copy off) is the cell's stated closing condition and it is not this order's to run.
- **THE INSTRUMENT CAVEAT THE CVO SHOULD CARRY, restated with this pass's numbers.** D7-AC1 and
  D7-AC2 are TOKEN censuses, and a token census cannot distinguish "calls the seam" from "mentions
  the seam" from "forbids the seam" from "a same-named function in another subsystem". **All 36 of
  AC1's hits and all 54 of AC2's are one of the last three.** The predicates that measure the
  retirement are the anchored `_canonical.<symbol>` call census (**3, all prose**) and the
  `kuzu.Database(` open census (**2 real, both out-of-grant spike loaders on their own path**).

---

## P2.6 ROWS FILED THIS PASS

Channel denominator: **109 rows before this append, 113 after**, counted by PARSING every fenced
json block and summing their lengths (109 in 107 blocks -> 113 in 111 blocks), 0 unparseable
blocks and 0 duplicate ids, never by an id grep. **FOUR rows, not three: the fourth arrived from
the COMMIT ATTEMPT.** The surprise-row gate REFUSED the first commit because the three rows'
`surfaced_at` values were written `2026-09-06T01:2xZ`, which the schema's timestamp pattern
rejects -- a CORRECT refusal, and the rows were corrected before they ever entered the record
rather than edited after it. The same run's commit-gate output carried the advisory that is now
W2-S23. W2-S1..W2-S19 are this seat's prior rows; none is
edited or renumbered.

| id | class | hazard | one line |
|---|---|---|---|
| `NFRA_CLDGRPH-W2-S20` | OBSERVATION | **ARMED** (`2.0.0_SA_COO~A`) | `git -C <empty submodule dir>` answers from the PARENT repo, so an independent oracle returns a confident 0 and a denominator check reports a mismatch that is really an absent oracle; 4 more call sites named |
| `NFRA_CLDGRPH-W2-S21` | BLOCKING | **ARMED** (`2.0.0_SA_COO~A`) | the narrowed D7-AC1 still cannot reach zero: `ensure_fresh` names a second unrelated family, and the battery proving the seam is gone must name the seam |
| `NFRA_CLDGRPH-W2-S22` | OBSERVATION | INERT | the manifest advisory convicts the string literals in a forbidden-token list -- the third substring-for-code confusion in this order |
| `NFRA_CLDGRPH-W2-S23` | OBSERVATION | **ARMED** (`2.0.0_SA_COO~A`) | the same manifest advises routing a REPOINTED consumer back through `comp-kuzu` to 'hit the canonical persisted Kuzu DB' -- a remedy that names the surface this order retired |

**Pass 1 rows that this pass RESOLVES by act (the issuer disarms; this is the evidence):**
`W2-S12` (AC1 vs AC5 contradiction -- the amendment narrowed AC1's paths), `W2-S13` (the seam
could not be removed in grant -- the widened `<paths>` made it removable and it is removed, less
the two out-of-lane importers named above), `W2-S15` (AC3's interpreter -- corrected and passing).
`W2-S14`, `W2-S16` and `W2-S17` are unchanged.

**Untracked artifacts, not committed:** `infra/aws/globgrph/tsgraph_detect_ledger.json` (written by
the comp-detect runs) and `org/pipescript-suite-gate-audit.log`; neither is in this order's
`<paths>`. `.scratch/` is this worker's own scratch and is not committed.

---

## P2.7 WHAT THE NEXT ORDER NEEDS

1. **A ruling on D7-AC1 and D7-AC2**, which cannot reach zero for reasons no act inside this
   project can move (W2-S21, W2-S14). Both would measure the property if re-cut to the anchored
   predicates this pass ran beside them: `_canonical\.<symbol>` for the calls, `kuzu\.Database\(`
   for the opens -- each already carries a printed denominator and a positive control.
2. **A hand-off to the two out-of-lane owners** (`0.4.0_DS_ClientPlatform`,
   `0.8.0_AE_CloudComp`) that their deliverables now raise on `_canonical.*`. They are historical
   records; the correct act may well be "leave them", but that is a decision, not a default.
3. **A ruling on `kuzu_stitch_db`** (W2-S17): retire it, or state that the estate keeps one local
   graph. Unchanged from pass 1.
4. **`CG-x-7`** -- two machines, same answer, local copy off -- is the cell's stated closing
   condition and is the issuer's to run at the drain.
