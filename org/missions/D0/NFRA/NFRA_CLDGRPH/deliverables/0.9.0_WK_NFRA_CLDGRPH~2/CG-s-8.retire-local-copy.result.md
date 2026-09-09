# CG-s-8 -- the RETIREMENT of the local copy (TO-CG-D-7, R7): result

**Worker:** `0.9.0_WK_NFRA_CLDGRPH~2` (spine-v3 subagent of `2.0.0_SA_COO~A`)
**Branch:** `wk-cldgrph-2-d7`, base `CLOUD@da35a5dfa0`. **Push state: LOCAL** (never pushed).
**Measured:** 2026-09-05 22:5xZ - 2026-09-06 00:0xZ, all invocations bounded by `timeout`.

> **READ P4.0 FIRST -- THE SECTIONS BELOW ARE IN PASS ORDER, NOT IN TRUTH ORDER.** This file
> is append-per-pass: sections 1-10 are PASS 1, `P2.*` PASS 2, `P3.*` PASS 3 and `P4.*` PASS 4,
> and each pass's CONCLUSION FIRST states the world AT THAT PASS. The conclusion immediately
> below is PASS 1's (2026-09-06 00:0xZ) and is kept verbatim as the record of what was true
> then. **The CURRENT state of this order is `P4.0`: 7 mechanical criteria PASS by output,
> `D7-AC8` recorded, `D7-AC2` at `0 of 29`.**

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

---

# PASS 3 -- the two ABSENCE ARMS RE-CUT AS BEHAVIOUR PROBES

**Worker:** `0.9.0_WK_NFRA_CLDGRPH~2` (same seat, same branch `wk-cldgrph-2-d7`).
**Base for this pass:** `565008157e` (`hand-off(NFRA_CLDGRPH.TO-CG-D-7 pass 3): merge CLOUD so the
behavioural AC1/AC2 are the grant`), carrying the issuer's amendment `e27c871ccf`.
**Push state: LOCAL** (never pushed, never merged, never rebased). **Measured:** 2026-09-06
02:5xZ - 03:3xZ, every invocation bounded by `timeout 120`.

**Everything above this line is PASS 1 and PASS 2 and stands.** Nothing in them is re-done. This
section adds the two new probes, the declaration the pass-3 face ordered, and the residue reading.

---

## P3.0 CONCLUSION FIRST

**`D7-AC1` now PASSES, and it passes for the right reason. `D7-AC2` FAILS -- and this time the
failure is WORLD, not INSTRUMENT. The order stays OPEN and the flip was not reached for.**

- **`D7-AC1` = `SEAM_REACHABLE=0 of 3`, `SEAM_PROBE_CONTROL=FIRED`, rc=0.** All three retired
  symbols raise `RuntimeError` through `getattr` on the real imported module; a constant the
  tombstone still defines returns through the same verb in the same process, so the zero is a
  refusal and not a dead import. The verb was separately shown to return `3 of 3` against a module
  where the seam IS present, so the arm can return non-zero on a positive.
- **`D7-AC2` = `CONSUMERS_OPENING_LOCAL_DB=3 of 30`, both controls FIRED, rc=1.** Three files
  inside the order's own `<paths>` open a local Kuzu database in CODE. One is the already-rowed
  stitch surface (`comp_debt.py:215`, `kuzu_stitch_db`, out of R7's scope by the cell's own text).
  **The other two hardcode `kuzu_nessie_db` itself** -- `kuzu_cost_enrich.py:227-231,242` and
  `kuzu_ac_traversals.py:28,83` -- **and `kuzu_ac_traversals.py:90` still prints `run
  kuzu_nessie_load.py first` to a user.** That is a live path to a local build, which is the exact
  question `D7-AC8` asks. Row **W2-S26**, ARMED.
- **This also corrects PASS 1.** The pass-1 census row 18 declared those two files as opening "a
  `--db` argument supplied by the caller, never `CANONICAL_DB_PATH`". That is wrong on the facts:
  neither file spells `CANONICAL_DB_PATH`, but both name the retired PATH STRING literally. The
  constant was retired; the string it pointed at was not. A pattern-shaped census could not see it;
  an AST-banded walk over a named population did.
- **The two out-of-lane spike openers are DECLARED, not touched** (`load_scratch_kuzu.py:97`,
  `load_clusters_scratch.py:43`) -- and the measurement adds the fact a line-number-only
  declaration would leave out: each opens its OWN scratch store under `tsgraph_spike/out/`, never
  `kuzu_nessie_db`. Row **W2-S25**, INERT.
- **`D7-AC5`'s three pins did NOT decay at `565008157e`.** `D7-AC3`, `D7-AC4`, `D7-AC6`, `D7-AC7`
  re-run and pass at this HEAD rather than being carried by citation.

**MECHANICAL RESULT: 6 PASS (`D7-AC1`, `D7-AC3`, `D7-AC4`, `D7-AC5`, `D7-AC6`, `D7-AC7`), 1 FAIL
(`D7-AC2`), 1 RECORDED-judgment (`D7-AC8`). THE ORDER STAYS OPEN.**

---

## P3.1 `D7-AC1` -- `seam_unreachable.sh`, and why a probe replaced a count

The file is
`org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/seam_unreachable.sh`.
It imports `infra/aws/globgrph/_canonical.py` the way a caller would, reaches for the three symbols
a caller would reach for, and counts how many hand back an object.

```
timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/seam_unreachable.sh
SEAM_PROBE_TARGET=C:\tmp\wk-cldgrph-2-d7\infra\aws\globgrph\_canonical.py
SEAM_PROBE_VERB=getattr(module, name) in-process; REACHABLE = returned without raising
  ensure_fresh           REFUSED  RuntimeError
  _full_rebuild_only     REFUSED  RuntimeError
  _append_fallback_sink  REFUSED  RuntimeError
SEAM_REACHABLE=0 of 3
SEAM_REFUSAL_KIND_RUNTIMEERROR=3 of 3  (an AttributeError here would be a SILENT refusal a hasattr() caller carries on past)
SEAM_PROBE_CONTROL=FIRED -- _RETIRED_BY -> 'NFRA_CLDGRPH PRD R7 / FWD-7, cell CG-s-8, task order TO-CG-D-7' returned through the SAME verb on the SAME module object, so attribute access is LIVE and the count above is a refusal
[rc=0 read UNPIPED]
```

**Three design points, each of which is a control rather than a decoration.**

- **`SEAM_PROBE_CONTROL` is what makes the zero mean anything.** A module that failed to import, or
  a module object with no live attribute access, prints a perfect `0 of 3` and proves nothing. The
  control reaches for `_RETIRED_BY` -- a constant the tombstone still defines, so `__getattr__`
  never fires for it -- through the SAME verb, on the SAME object, in the SAME process. An import
  failure never reaches the count at all: the script exits 2 as BLOCKED.
- **`SEAM_REFUSAL_KIND_RUNTIMEERROR` catches a degradation the count cannot see.** A symbol that
  raised `AttributeError` would still score 0 REACHABLE, but a caller writing
  `getattr(_canonical, "ensure_fresh", None)` would read that as "older build, skip the refresh" and
  carry on over whatever it found locally. There is nothing local left to carry on over, so the
  loud stop is the safe behaviour, and the kind line is where its loss would show.
- **The arm can return non-zero on a positive, and was shown to.** The same verb, run against a
  scratch module in `.scratch/` that DEFINES the three symbols:
  `ensure_fresh REACHED <function ...>` / `_full_rebuild_only REACHED` /
  `_append_fallback_sink REACHED` / `SEAM_REACHABLE=3 of 3`. A detector that cannot return non-zero
  on the positive case is a constant wearing a measurement's clothes; this one is not.

**Why the predecessor could not work, stated once for the record and not re-litigated.** The old
arm counted TEXT over a corpus. On this population the text count is ANTI-CORRELATED with the
property: the tombstone must NAME what it retires, the CG-8 battery must NAME the symbols it
asserts refuse, and the unanchored pattern collides with two unrelated freshness families. The
count rose 29 -> 36 across the pass that removed the seam. The probe asks the question the property
poses, and its answer moves the right way.

---

## P3.2 `D7-AC2` -- `consumers_no_local_db.sh`, the closed population, and the three real openers

The file is
`org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/consumers_no_local_db.sh`.
Its population is transcribed from `TO-CG-D-7 <paths>` (lines 218-253 @`565008157e`), **32
declared, 2 absent, N = 30** -- not a corpus sweep, because the criterion asks a question about a
NAMED SET and a sweep answers a question about the corpus.

```
timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/consumers_no_local_db.sh
CONSUMER_POPULATION_DECLARED=32  (the file list in TO-CG-D-7 <paths>)
  ABSENT (excluded from the denominator): infra/aws/globgrph/tests/test_canonical_rebuild_liveness.py
  ABSENT (excluded from the denominator): infra/aws/globgrph/tests/test_canonical_refresh_failure_signal.py
CONSUMER_POPULATION_ABSENT=2
CONSUMER_BAND_RULE=ast.Call on kuzu.Database / ast.Name|Attribute CANONICAL_DB_PATH; comments and string constants (docstrings, forbidden-token tuples, mutant fixtures) never inspected
  OPENS  infra/aws/globgrph/comp_debt.py:215  [kuzu.Database(]  conn = kuzu.Connection(kuzu.Database(path, read_only=True))
  OPENS  infra/aws/globgrph/kuzu_cost_enrich.py:127  [kuzu.Database(]  db = kuzu.Database(db_path)
  OPENS  infra/aws/globgrph/kuzu_cost_enrich.py:197  [kuzu.Database(]  db = kuzu.Database(db_path)
  OPENS  infra/aws/globgrph/kuzu_ac_traversals.py:92  [kuzu.Database(]  conn = kuzu.Connection(kuzu.Database(args.db, read_only=True))
CONSUMERS_OPENING_LOCAL_DB=3 of 30
CONSUMER_PROBE_CONTROL=FIRED -- planted opener caught 2 of 2 signature(s) CANONICAL_DB_PATH,kuzu.Database( at line(s) 2,4,4 through the SAME detector, in-process, on a temp string (never a tracked file)
CONSUMER_PROBE_BAND_CONTROL=FIRED -- the same two tokens planted in a docstring, a comment and a string tuple scored 0, so the banding is exercised and not merely asserted
[rc=1 read UNPIPED]
```

**The two absent files are the two seam tests PASS 2 deleted with the behaviour they pinned.** They
are printed by name and excluded from the denominator rather than dropped in silence: a file that
vanished and a file that passed are different findings, and only one of them belongs in a
denominator.

**THE BANDING IS EXERCISED, NOT ASSERTED, and this matters more than the headline.** The AST walk
inspects `ast.Call` nodes whose callee is the attribute `kuzu.Database`, and `ast.Name`/
`ast.Attribute` nodes spelling `CANONICAL_DB_PATH`. Comments do not survive parsing; string
constants are never inspected. So the following are excluded **by construction**, not by a
hand-kept skip list that would drift:

| excluded site | what it is | why a text match would have counted it |
|---|---|---|
| `infra/aws/globgrph/_canonical.py:24,33,35` | module docstring | the tombstone must NAME `CANONICAL_DB_PATH` to say what it retired |
| `org/modules/graph/comp_aws_cli.py:2857` | `#` comment | it explains the OLD default to a reader |
| `.tools/tests/test_cg8_seam_retired_battery.py:92,182,350,366,370,371` | string literals | the battery's forbidden-token tuple and its RED mutant fixture |
| `infra/aws/globgrph/tests/test_comp_cluster_cli.py:29,126,136` | docstring + string tuple | the same, for the repointed cluster battery |

`CONSUMER_PROBE_BAND_CONTROL` plants the same two tokens in a docstring, a comment and a string
tuple and requires a score of **0**. Without it, "banding" would be an unexercised claim, and a
detector that also ignored real calls would satisfy the opposite control and still read clean.

### The three openers, classified

| # | site | opens | disposition |
|---|---|---|---|
| 1 | `infra/aws/globgrph/comp_debt.py:215` | `STITCH_DB = os.path.join(_HERE, "kuzu_stitch_db")` (`comp_debt.py:40`) | **OUT OF R7's SCOPE.** The cell's own text at `comp_debt.py:207-209` says so: "the STITCH surface is a SEPARATE local graph this order does not retire -- CG-s-8 retires `kuzu_nessie_db` only". Its nessie leg is served. Already carried by row **W2-S17** |
| 2 | `infra/aws/globgrph/kuzu_cost_enrich.py:127,197` | `os.path.join(WORKSPACE, 'kuzu_nessie_db')` and `kuzu_stitch_db`, built at `:227-231`; `:242` opens the nessie path a second time | **THE RETIRED STORE, HARDCODED.** No argparse exists in this file; the caller supplies nothing. It WRITES (`ALTER TABLE CloudNode ADD cost_mtd_usd`, `SET`) |
| 3 | `infra/aws/globgrph/kuzu_ac_traversals.py:92` | `args.db`, whose default at `:83` is `DEFAULT_DB_PATH` = `os.path.join(dirname(__file__), "kuzu_nessie_db")` (`:28`) | **THE RETIRED STORE, AS THE BARE-INVOCATION DEFAULT.** `:90` prints `ERROR: Kuzu DB not found at {args.db} -- run kuzu_nessie_load.py first` |

**PASS 1'S CENSUS ROW 18 IS WRONG AND THIS IS ITS CORRECTION.** It read: "`kuzu_ac_traversals`,
`kuzu_cost_enrich` -- DECLARED -- they open a `--db` argument supplied by the caller, never
`CANONICAL_DB_PATH`; they are loader-side enrichment, not user-facing consumers." Neither file
spells `CANONICAL_DB_PATH` -- that half is true and is exactly why a pattern-shaped census missed
them. But both name the retired PATH STRING literally, and `kuzu_cost_enrich.py` takes no argument
at all. **The constant was retired; the string it pointed at was not.**

**WHY THIS WORKER DID NOT FIX THEM, although both ARE inside `<paths>`.** The pass-3 face
enumerates five things and says "nothing else", and neither repointing nor deleting these two is
among them. The choice is not cosmetic either: `kuzu_cost_enrich.py` WRITES, and the served graph
is read-only over HTTPS, so it has no repoint target -- its only honest dispositions are DELETE or
DECLARE-AS-DEAD, and a worker choosing between them on someone else's cell text is widening the
order. `kuzu_ac_traversals.py` reads and could be repointed, but it is an NFRA_DEBTSCAN-era
acceptance harness whose retirement is a scope call. **So the arm is reported FAIL by output at
3 of 30, the flip is not reached for, and the order stays open.** Row **W2-S26**, ARMED,
`disarm_owner` `2.0.0_SA_COO~A`.

**A SECOND, SEPARABLE DIVERGENCE THE ISSUER SHOULD SEE BEFORE RE-CUTTING.** The arm's predicate
counts ANY `kuzu.Database(` call, so the stitch open at row 1 keeps it non-zero even after rows 2
and 3 are resolved. The predicate is wider than R7. Narrowing it here would have been the same
move the amendment was written to stop -- improving a number by editing the instrument -- so it was
not made; it is stated instead.

---

## P3.3 DECLARED, NOT TOUCHED -- the two openers outside `<paths>` (the pass-3 face's item 3)

| site | line | statement | opens | in `<paths>`? | act |
|---|---|---|---|---|---|
| `org/modules/graph/tsgraph_spike/load_scratch_kuzu.py` | **97** | `db = kuzu.Database(DB_PATH)` | `DB_PATH` at **:32** = `os.path.join(HERE, "out", "scratch_kuzu_db")`; **:93** `shutil.rmtree(DB_PATH)  # our own scratch artifact` | **NO** | **DECLARED, untouched** |
| `org/modules/graph/tsgraph_spike/load_clusters_scratch.py` | **43** | `db = kuzu.Database(DB_PATH)` | `DB_PATH` at **:23** = `os.path.join(HERE, "out", "scratch_clusters_db")`; **:40** `shutil.rmtree(DB_PATH)` | **NO** | **DECLARED, untouched** |

**Both opens are real, both are CODE band, and both are harmless to R7** -- which is the part a
line-number-only declaration would leave unsaid. Neither file imports `_canonical`, neither names
`CANONICAL_DB_PATH`, and neither reads or writes the retired canonical store: each builds a
throwaway spike database from its own inputs and deletes it first. **So nothing user-facing here
holds a path back to a local CANONICAL build.** They are also outside `D7-AC2`'s population by
construction, so they neither raise nor lower its count.

Whether FWD-7 obliges this cell to retire a scratch loader at all is a SCOPE question the issuer
put to `1.0.0_SA_CTO` in the same tick as the amendment (msg 94454). This worker is not waiting on
it: declaring them is its act under either resolution, and the wall is the grant, not the
difficulty. Row **W2-S25**.

---

## P3.4 THE CRITERIA AT `565008157e` -- every one re-run, none carried by citation

| id | verdict | invocation | deciding line | rc |
|---|---|---|---|---|
| `D7-AC1` | **PASS** | `bash .../seam_unreachable.sh` | `SEAM_REACHABLE=0 of 3` then `SEAM_PROBE_CONTROL=FIRED` | 0 |
| `D7-AC2` | **FAIL** | `bash .../consumers_no_local_db.sh` | `CONSUMERS_OPENING_LOCAL_DB=3 of 30` | 1 |
| `D7-AC3` | **PASS** | `python .tools/comp-find --corpus aws 'opal-globgrph' --budget 120 --limit 5` | `VINTAGE: Built from the estate as of 2026-09-06 02:09:08 UTC.  manifest: faee7c538910` / `DENOMINATOR: 87 hit(s) across 2161 aws node(s) scanned` | 0 |
| `D7-AC4` | **PASS** | `bash .tools/comp-blast component:AdvisorsTab.tsx --budget 90` | `VINTAGE: Built from the estate as of 2026-09-06 02:09:08 UTC.  [... nodes=27299 edges=58780]` | 3 (the ratified NOT-FOUND state) |
| `D7-AC5` | **PASS** | `for f in ...; do git show HEAD:$f \| sha256sum; done` | `8b79ca1b...` / `80d60f8f...` / `9dd104db...` -- **all three still match at `565008157e`** | 0 |
| `D7-AC6` | **PASS** | `python .tools/tests/test_g2_disclosure_battery.py` | `DENOMINATOR: 7 of 7 arm(s) recorded a pass` then `PASS` | 0 |
| `D7-AC7` | **PASS** | `bash .../commit_gate_all.sh` | `pre-commit gate clean (17 .py file(s) + .tools/comp-find; denominator 18 of 18)` | 0 |
| `D7-AC8` | **RECORDED** | reading act | no verdict -- `3.0.0_SA_CVO` grades at L9 | n/a |

**`D7-AC5`: the pins did not decay.** Measured at HEAD `565008157e` by the criterion's own
`git show HEAD:<f> | sha256sum`: `kuzu_nessie_load.py` ->
`8b79ca1bdfd51c1823c0c6780086d55d7e9c751d7651820f873cf1d4b42a5b3d`,
`kuzu_incremental_refresh.py` ->
`80d60f8ffa3c3c5da735c781d695d233496d31ac7bd2b7dabde034b718b1ef71`, `projection_server.py` ->
`9dd104db29d558e48ecb5a28f8df9464fdca502eb25acffc680fdf696b7fe059`. The cloud engine is untouched
by all three passes.

**`D7-AC7`'s list did not change this pass** -- the two new files are `.sh`, and `commit-gate.sh`
dispatches by suffix. `MANIFEST-ADVISORY: 4 graph-access finding(s) ... Advisory -- not blocking`
recurred exactly as row **W2-S22** describes (four string literals inside the battery's own
forbidden-token tuple).

---

## P3.5 `D7-AC8` -- the reading act, PASS 3 addendum (judgment; NO verdict; `3.0.0_SA_CVO` grades this at L9)

Pass 1's s.8 and pass 2's s.P2.5 stand. **This addendum answers one half of `D7-AC8` that the two
earlier passes answered too generously: "whether anything user-facing still holds a path to a local
build."** The census the amendment retired was not wasted -- it found real things, and they are
named here with their lines. **All of them are DOCUMENTATION or DEFAULTS, none is the seam, and
together they are a retirement the estate's own instructions still sell against.**

### (a) The estate's dependency manifest still ROUTES a repointed consumer back to the retired surface

`org/modules/graph/graph-call-manifest.yaml` is the file CLAUDE.md rule 20 sends every seat to
before any cloud/infra/data change. At `565008157e` it still carries, measured by
`python .tools/comp-read ... --enumerate 'comp-kuzu|kuzu_nessie_db|canonical DB path'` -> **61
hits**:

- **:156, :169** -- `freshness: "kuzu DB ...; DEFAULT surface = canonical Nessie kuzu_nessie_db;
  auto-refreshes ENGINE-INTERNALLY on Nessie-HEAD-advance"`. The engine-internal auto-refresh IS
  the seam this order removed.
- **:213-216** -- a whole section header, `# ---- LOCAL-PROJECTION REFRESH MODES (comp-kuzu --mode
  full / --mode inc ...) ----`.
- **:221** -- `canonical_call: "comp-kuzu --mode full [--json] [--limit N] \"<Cypher>\"   # forces a
  FULL kuzu_nessie_load unconditionally, then serves the query"`.
- **:229** -- `anti_pattern: "running --mode full mid-task to answer a traversal (a 482s full
  rebuild to serve a read) -> bare comp-kuzu (auto) or --mode inc"`.
- **:235** -- `canonical_call: "comp-kuzu --mode inc ...   # incremental-OR-serve-labeled-stale"`.

**THE RECOMMENDED CALL IS DEAD, and this was exercised rather than reasoned:**

```
timeout 120 bash .tools/comp-kuzu --mode full "MATCH (n:CloudNode) RETURN count(n)"
usage: kuzu_cli.py [-h] [--json] [--limit LIMIT] [--schema] [query]
kuzu_cli.py: error: unrecognized arguments: --mode MATCH (n:CloudNode) RETURN count(n)
[rc=2 read UNPIPED]
```

So two registered tool entries in the manifest name a `canonical_call` the tool refuses to parse.
Row **W2-S23** already carries the advisory half of this (the manifest's REMEDY fires on every
correctly-repointed consumer); the `--mode` entries are the same defect one layer up, in the
registry rather than the advisory. `graph-call-manifest.yaml` is NOT in this order's `<paths>` and
is untouched.

### (b) `.tools/tool_index.py` -- the help text a user reads still describes the retired default

Measured by `python .tools/comp-read .tools/tool_index.py --enumerate
'kuzu_nessie_db|auto-refresh|auto refresh|ENGINE-INTERNAL|engine-internal'` -> **19 hits, all CODE
band** (they are dict values in the help tables, not docstrings). **Six lines name
`kuzu_nessie_db`: :1067, :1087, :1103, :1173, :3269, :4054.** The canonical shape, at :1067-1068:

```
'above); DEFAULT surface (no --db-path) = canonical Nessie kuzu_nessie_db; auto-refreshes '
'on Nessie-HEAD-advance ENGINE-INTERNALLY (Rule 20 QUERY-default posture UNCHANGED -- '
```

and the rebuild-flavoured ones at **:3269** and **:4054** (`(SAME kuzu_nessie_db store, not a new
surface) -- forces a FULL ...`). The auto-refresh prose recurs at :860, :1982, :2460, :2503, :3456,
:4230, :5100. `.tools/tool_index.py` IS in `<paths>`; pass 1 repointed ONE `ensure_fresh` mention
in it and these were not part of pass 3's five, so they are named here rather than edited.

### (c) `org/modules/graph/comp_aws_cli.py` -- one comment and one LIVE PRINT

- **:2857** (comment): `#   comp-kuzu's DEFAULT surface is _canonical.CANONICAL_DB_PATH =
  kuzu_nessie_db,` -- and `_canonical.CANONICAL_DB_PATH` now raises `RuntimeError`.
- **:2866** (a `print`, i.e. text SERVED to an operator at runtime, not a comment):
  `print("  comp-kuzu's canonical surface (kuzu_nessie_db, Nessie-sourced) still serves its")`
  followed by :2867-2869 telling the operator how to "publish to THAT surface". **This is the
  strongest item in the residue**, because it is the only one a user meets without opening a file.

### (d) `org/modules/graph/debtscan/comp_similar.py:591` -- an equality on the retired name, in CODE

`and cap.get("corpus_db") == "kuzu_nessie_db"` inside a self-check block, with :595 feeding
`_capture_kuzu_vintage("=== comp-kuzu provenance ===\n  DB: kuzu_nessie_db\n")`. This is a
provenance-header fixture, so it is a CORRECT thing for a test to hold today; it becomes wrong the
moment the served header stops spelling that string. It is NOT in `<paths>` (the order grants
`.tools/tests/test_comp_similar_battery.py`, a different file) and is untouched. Pass 1's census
row 29 anticipated it.

### The reading, stated plainly

**Nothing user-facing can still BUILD the local copy through the retired seam** -- `D7-AC1`
measures that behaviourally and the three symbols refuse. **But two things user-facing still POINT
AT one**: `kuzu_ac_traversals.py:90` prints `run kuzu_nessie_load.py first`, and
`kuzu_nessie_load.py` still exists and is byte-pinned by `D7-AC5`, so that instruction is
executable rather than merely stale; and `comp_aws_cli.py:2866` tells an operator at runtime that
`kuzu_nessie_db` "still serves". **A retirement the estate's own manifest, help text and runtime
output continue to recommend is the shadow path R7 exists to close.** Whether that is enough to
call the retirement REAL is `3.0.0_SA_CVO`'s call at L9; this section states what was measured and
takes no verdict.

**Per-consumer latency/payload through the gateway** is unchanged from pass 2's s.P2.5 and is not
re-measured here: no consumer was repointed this pass, so a re-run would answer a question already
answered at the same HEAD.

---

## P3.6 ROWS FILED THIS PASS

The channel header claimed **114 rows**; **VERIFIED by parsing every fenced json block and summing
their lengths -- 114 rows in 112 blocks, 114 unique ids, `W2-S1..W2-S24` contiguous** -- so the
next id is `W2-S25` as the face said. After this append: **116 rows in 114 blocks**, restated in
the header.

| id | class | hazard | one line |
|---|---|---|---|
| `NFRA_CLDGRPH-W2-S25` | OBSERVATION | INERT | the two out-of-lane `tsgraph_spike` openers, DECLARED with their lines and what each opens -- both open their own scratch store, never `kuzu_nessie_db` |
| `NFRA_CLDGRPH-W2-S26` | BLOCKING | **ARMED** (`disarm_owner` `2.0.0_SA_COO~A`) | `D7-AC2` fails on WORLD at 3 of 30; two files in the order's own `<paths>` hardcode the retired `kuzu_nessie_db` and one prints a local-rebuild instruction -- and this corrects pass 1's census row 18 |

---

## P3.7 WHAT THE NEXT ORDER NEEDS

1. **`D7-AC2` needs a decision, not a re-cut of the instrument.** The probe is sound and both its
   controls fire. The question is what to DO with `kuzu_cost_enrich.py` and `kuzu_ac_traversals.py`:
   DELETE (they target a store that no longer exists), REPOINT (only `kuzu_ac_traversals.py` can be
   -- the other WRITES), or DECLARE-AS-DEAD with the census note corrected. All three are one-file
   acts inside the existing `<paths>`; none is a worker's call to make unasked.
2. **If the predicate stays as written, the stitch open keeps the arm non-zero forever.** Either
   the criterion names `kuzu_nessie_db` specifically, or `comp_debt.py`'s stitch leg is carried as
   a standing declared exception -- row **W2-S17** is the place it already lives.
3. **The residue in P3.5(a)-(c) is a documentation act inside two files this order already grants**
   (`.tools/tool_index.py`, `org/modules/graph/comp_aws_cli.py`) plus one it does not
   (`graph-call-manifest.yaml`). A single narrow order could close all three.

---

# PASS 4 -- the DISPOSITION EXECUTED: the writer DELETED, the last reader REPOINTED, the predicate NARROWED

**Worker:** `0.9.0_WK_NFRA_CLDGRPH~2` (a FRESH spawn on the same branch; the pass-3 subagent died with
every Claude seat at 2026-09-06 03:59Z). **Branch:** `wk-cldgrph-2-d7`, HEAD at spawn `5eb0324a7b`.
**Push state: LOCAL** (never pushed; not measured against a remote and not claimed).
**Measured:** 2026-09-09 13:3xZ - 14:2xZ, every invocation bounded by `timeout`.

## P4.0 CONCLUSION FIRST

**THE RETIREMENT IS COMPLETE INSIDE THIS CELL, AND THE ARM THAT SAID SO IS THE ONE THAT REFUSED TO
SAY IT FOR THREE PASSES.** `D7-AC2` reads `CONSUMERS_OPENING_LOCAL_DB=0 of 29` with **all three**
controls FIRED. Seven mechanical criteria PASS by output; `D7-AC8` is recorded without a verdict.

- **`infra/aws/globgrph/kuzu_cost_enrich.py` is DELETED** (`git rm`), on `1.0.0_SA_CTO`'s ruling
  94466 @`1266d65641`. The four findings that ruling rests on were **re-measured here at my own
  HEAD with my own denominators printed beside his** (P4.2). It was the last WRITER against the
  retired store, and deleting it also removes the stitch store's only writer.
- **`infra/aws/globgrph/kuzu_ac_traversals.py` is REPOINTED** through `projection_client` and
  exercised twice against the served graph. The line that told a user to `run kuzu_nessie_load.py
  first` is gone; so is the `--db` flag, because a served graph has no path to point at (row
  **W2-S27**).
- **`D7-AC2`'s predicate is NARROWED to the canonical store**, as the pass-3 amendment directed and
  under the same split `1.0.0_SA_CTO` ruled at 94456. `comp_debt.py:215` (the `kuzu_stitch_db`
  reader, the issuer's placed manifest row) now prints as **`DECLARED-OUT-OF-CELL`** beside the
  count -- named, never dropped. **The narrowing is exercised in BOTH directions by a third
  control**, because a scope filter that quietly matched everything would read exactly like a clean
  population.
- **Nothing about the residue changed and nothing about it is claimed to have.** `tool_index.py`'s
  six help-text hits, `comp_aws_cli.py:2857/2866`, `comp_similar.py:591` and the manifest advisory
  are re-measured at this HEAD and are **unchanged**; they travel to L9 in `D7-AC8` exactly as pass
  3 left them.

**MECHANICAL RESULT: 7 PASS-by-output (D7-AC1..D7-AC7), 1 RECORDED-judgment (D7-AC8).**

## P4.1 RE-GROUNDING AT MY HEAD (the amendment's act 1) -- four premises, all TRUE

| premise | instrument | reading |
|---|---|---|
| the pass-3 instance validates rc 0 | `python .tools/proof-of-spec-check.py <instance> D7-AC1..D7-AC8` | `VALID (rc=0)`, `acceptance rows=8 \| violations=0`, `surprises-frame: 15 entries; 15 resolve to a channel row`; the D7-AC2 row reads `FAIL` |
| `kuzu_cost_enrich.py` EXISTS | `test -f` + `wc -l` | EXISTS, 259 lines |
| `_canonical.py` is the 78-line tombstone | `wc -l` | 78 lines |
| `projection_client.py` exists | `test -f` + `wc -l` | EXISTS, 338 lines |

`git rev-parse --abbrev-ref HEAD` -> `wk-cldgrph-2-d7`; `test -d org && test -d .tools` -> `TREE-OK`;
`git rev-parse HEAD` -> `5eb0324a7b74444f5c41a8a00d38d3a019fa80b7`.

**And the arm's BASELINE was taken before any write**, so the delta this pass produced is measured
rather than asserted: `bash .../consumers_no_local_db.sh` at `5eb0324a7b` -> **`CONSUMERS_OPENING_LOCAL_DB=3 of 30`**,
`CONSUMER_PROBE_CONTROL=FIRED`, `CONSUMER_PROBE_BAND_CONTROL=FIRED`, rc=1 -- the same three openers
pass 3 recorded, at the same lines.

## P4.2 (iii) THE DELETE -- `infra/aws/globgrph/kuzu_cost_enrich.py`

**THE ACT:** `git rm infra/aws/globgrph/kuzu_cost_enrich.py` -> `rm 'infra/aws/globgrph/kuzu_cost_enrich.py'`, rc=0.

**THE CTO'S FOUR FINDINGS, RE-MEASURED AT MY HEAD, WITH BOTH DENOMINATORS.** The instruction was to
re-measure and print mine beside his -- not to restate his.

| finding | CTO @`4510dcaa2a` | MINE @`5eb0324a7b` | verdict |
|---|---|---|---|
| one-off session artifact of a closed project | `--full-history` is ONE commit | `git log --full-history --oneline -- infra/aws/globgrph/kuzu_cost_enrich.py` -> **exactly one line**, `f8ba82b894 costrecon(TO-D4): full lever census + kuzu cost_mtd_usd enrichment ...` | CONFIRMED |
| callers | 0 of 18 token hits | token census `comp-find 'kuzu_cost_enrich' --all --files --limit 200` -> **`114 hit(s) across 29033 file(s) scanned`, 36 files**, bands `HEAD=1 SURFACED=19 CONFIG=11 DOC=83`; CODE-caller census `comp-find 'import kuzu_cost_enrich\|from kuzu_cost_enrich\|kuzu_cost_enrich[.][a-z_]+[(]' --all` -> **`4 hit(s) across 29033 file(s)`**, and all four are non-callers (3 are THIS session's own comp-tool logs, 1 is prose in `ADJUDICATION_v1.md:761`) | **0 code callers CONFIRMED**; file count differs and the difference is explained below |
| consumers of `cost_mtd_usd` | 0 of 14, none code | `comp-find 'cost_mtd_usd' --all --files --limit 200` -> **`65 hit(s) across 29033 file(s)`, 22 files**; `--band SURFACED` -> `26` hits of which **20 are inside `kuzu_cost_enrich.py` itself** (`:3,:25,:62,:124,:132,:133,:149,:162,:175,:184,:201,:202,:203,:213,:245,:246,:247,:250,:255`), the rest tool logs and `commits.jsonl` | **0 code consumers outside the file CONFIRMED** |
| it OPENS and ALTERs the retired store | `:127`/`:197` open, `:132` writes, `:228`/`:242` hardcode | `:127` and `:197` `db = kuzu.Database(db_path)`; `:132` `conn.execute('ALTER TABLE CloudNode ADD cost_mtd_usd DOUBLE DEFAULT 0.0')`; `:227-231` `dbs = [os.path.join(WORKSPACE, 'kuzu_nessie_db'), os.path.join(WORKSPACE, 'kuzu_stitch_db')]`; no argparse in the file | CONFIRMED |

⚠ **THE FILE COUNTS DIFFER AND THE DIFFERENCE IS NOT A DISAGREEMENT -- state it rather than let a
reader reconcile two numbers.** His 18 and 14 are native `Grep` over the repo at `4510dcaa2a`; mine
are `comp-find --corpus all`, which is `.gitignore`-BOUNDED (tracked + untracked + gitignored minus
a printed ephemeral floor) and therefore also reads `.scratch/`, `.comp-graph/` and
`org/mcp/*.jsonl`; and my branch carries the pass-1..pass-3 artifacts that POSTDATE his HEAD (this
deliverable, the proof instance, this order's own face amendments, `consumers_no_local_db.sh`, the
channel rows). **The two censuses agree exactly where the ruling rests: ZERO code callers and ZERO
code consumers of the attribute.** The wider corpus can only ADD non-code carriers, which is the
direction that cannot hide a caller.

**THE SHA, so the deleted bytes are identifiable after the delete:**
`git show HEAD:infra/aws/globgrph/kuzu_cost_enrich.py | sha256sum` ->
`ead4be09c28f523cacbac5fcad1b18e054aebbc7825e08aa552ea61b55a64af5` -- the same digest
`3.0.0_SA_CVO` recorded at its program-grain exercise (ADJUDICATION_v1 C-S21).

**CENSUS ROW 18, CORRECTED (this seat's own pass-1 row, wrong twice and corrected twice).**

| # | file | class | disposition (PASS 4) |
|---|---|---|---|
| 18 | `infra/aws/globgrph/kuzu_cost_enrich.py` | B (mis-classified at pass 1 as a caller-supplied `--db` consumer; corrected at pass 3 to a hardcoded opener; corrected here to its final disposition) | **REMOVED -- WRITER AGAINST A RETIRED LOCAL STORE, NO REPOINT TARGET.** Methodology preserved at `f8ba82b894` and `org/modules/graph/debtscan/2026-06-12_D4_costrecon_ae.md`. Callers 0; `cost_mtd_usd` consumers 0. The CAPABILITY (cost attribution on graph nodes) is PLACED by `1.0.0_SA_CTO` as a producer-side manifest row at L10, lane `0.8.0_AE_CloudComp` -- not this cell's act and not carried here. |

**AND ONE CONSEQUENCE WORTH NAMING:** deleting it removes the **stitch store's only WRITER**. The
stitch READER (`comp_debt.py:215`) is the issuer's placed row and was not touched.

## P4.3 (ii) THE REPOINT -- `infra/aws/globgrph/kuzu_ac_traversals.py`

**BEFORE** (@`5eb0324a7b`, 114 lines): `:28` `DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kuzu_nessie_db")`;
`:83` `ap.add_argument("--db", default=DEFAULT_DB_PATH)`; `:87` `import kuzu`;
`:90` `print(f"ERROR: Kuzu DB not found at {args.db} -- run kuzu_nessie_load.py first")`;
`:92` `conn = kuzu.Connection(kuzu.Database(args.db, read_only=True))`.

**AFTER** (129 lines): no `DEFAULT_DB_PATH`, no `--db`, no `import kuzu`, no `os` import at all.
`main()` calls `projection_client.vintage_line()` and `projection_client.connect()` inside one
`try`, and the refusal line reads:

```
ERROR: the SERVED cloud graph is unreachable ({type}: {ex}) -- this harness reads the served
projection (infra/aws/globgrph/projection_client.py) and has NO local copy to fall back to;
check the gateway, never rebuild a local database
```

An unreachable service now exits **3** -- a REFUSAL, distinguishable from `FAIL` (1) and
`SUBSTRATE-MISSING` (2), which is the same fail-honest discipline the file already carried for
absent substrate. **Two shape changes the face did not name are recorded as row W2-S27**: the
`--db` flag is REMOVED rather than defaulted (there is no path to default to), and the preflight
interpolates its node class because `ServedConnection.execute` carries no parameter dict; every
value comes from `AC_SUBSTRATE`, a module-level literal in the same file.

**THE REAL RUNS (bounded, quoted whole):**

```
$ timeout 60 python infra/aws/globgrph/kuzu_ac_traversals.py --help
usage: kuzu_ac_traversals.py [-h] [--ac {AC5,AC8,AC9}]

options:
  -h, --help          show this help message and exit
  --ac {AC5,AC8,AC9}  run one AC only
rc=0
```

```
$ timeout 120 python infra/aws/globgrph/kuzu_ac_traversals.py --ac AC8
VINTAGE: Built from the estate as of 2026-09-09 12:23:34 UTC.  [vintage=2026-09-09T12:23:34.893879+00:00]
AC8: SUBSTRATE-MISSING -- absent node classes: PORTAL_PAGE, PORTAL_COMPONENT, PORTAL_HOOK, REACT_QUERY_KEY, PORTAL_UTIL
VERDICT: UNVALIDATED -- substrate missing; absence is NOT a pass (P2 stitch / P3-A / P3-C builds land the missing layers)
rc=2   wall_s=2.55
```

```
$ timeout 120 python infra/aws/globgrph/kuzu_ac_traversals.py --ac AC5
VINTAGE: Built from the estate as of 2026-09-09 12:23:34 UTC.  [vintage=2026-09-09T12:23:34.893879+00:00]
AC5: SUBSTRATE-MISSING -- absent node classes: PORTAL_COMPONENT, S3_DATA_KEY, GOLD_SCRIPT
VERDICT: UNVALIDATED -- substrate missing; absence is NOT a pass (P2 stitch / P3-A / P3-C builds land the missing layers)
rc=2   wall_s=3.04
```

⛔ **A `SUBSTRATE-MISSING` VERDICT AND A DEAD QUERY READ IDENTICALLY, so the preflight was shown to
return a non-zero on a class that IS present** -- the same statement shape, the same transport, in
the same tick: `MATCH (n:CloudNode) WHERE n.node_type = 'S3_BUCKET' RETURN count(*)` ->
`rows=[{'COUNT_STAR()': 34}]`, `response_bytes=301`, `preflight_stmt_bytes=67`, `wall_s=1.77`. The
absences above are real absences in the served universe, not a harness that cannot count.

**Per-consumer gateway cost (D7-AC8's substance, this consumer):** 6 round trips for `--ac AC8`
(1 health + 5 preflights) in 2.55 s; 8 for `--ac AC5` in 3.04 s; largest response measured **301 B**.
Well inside any budget; the 1 MiB REQUEST limit is untouched (largest statement 254 B).

## P4.4 (i) THE NARROWING -- and why it is not a softening

**THE RULE, and its authority.** CG-s-8 retires four surfaces and every one is `kuzu_nessie_db` or
its seam. An opener on a DIFFERENT local store is FWD-7's territory, not this cell's -- the split
`1.0.0_SA_CTO` ruled at 94456 for the scratch loaders and the pass-3 amendment applied to the
stitch open. So `consumers_no_local_db.sh` now RESOLVES each opener to the store it names and
counts only CANONICAL ones.

**RESOLUTION IS FAIL-CLOSED, WHICH IS THE ONLY WAY A NARROWING IS HONEST.** The resolver walks the
opener's first argument through that file's own bindings -- module and function assignments, `for`
targets over literal tuples, argparse defaults, `os.path.join` segments, f-strings, `BinOp`
concatenation -- and collects every reachable string literal. Canonical -> **counted**. Some other
store-shaped literal and no canonical -> **`DECLARED-OUT-OF-CELL`, printed with the store**. **No
store literal reachable at all -> COUNTED AS CANONICAL**, because an opener whose target cannot be
read is exactly the case a narrowing must not be allowed to swallow. The bindings index is
deliberately over-inclusive (a name assigned twice contributes both expressions): a union that is
too wide can only ever COUNT an opener a narrower read would have excused, never the reverse.

**A THIRD CONTROL, BECAUSE THE NARROWING IS A NEW PREDICATE AND AN UNEXERCISED NARROWING IS A
PROMISE.** `CONSUMER_NARROWING_CONTROL` plants two sources and asserts both directions in the same
process, through the same detector: a stitch-store opener reached through a `for` target over a
literal tuple (the exact shape of `comp_debt.py:215`) must classify OUT-OF-CELL on
`kuzu_stitch_db`, and an opener on an unresolvable function parameter must classify
`UNRESOLVED-COUNTED`. Either failing prints `=DEAD` and exits 1.

**THE ARM, quoted whole:**

```
CONSUMER_POPULATION_DECLARED=32  (the file list in TO-CG-D-7 <paths>)
  ABSENT (excluded from the denominator): infra/aws/globgrph/kuzu_cost_enrich.py
  ABSENT (excluded from the denominator): infra/aws/globgrph/tests/test_canonical_rebuild_liveness.py
  ABSENT (excluded from the denominator): infra/aws/globgrph/tests/test_canonical_refresh_failure_signal.py
CONSUMER_POPULATION_ABSENT=3
CONSUMER_BAND_RULE=ast.Call on kuzu.Database / ast.Name|Attribute CANONICAL_DB_PATH; comments and string constants (docstrings, forbidden-token tuples, mutant fixtures) never inspected
CONSUMER_PREDICATE_SCOPE=the CANONICAL store 'kuzu_nessie_db' only (CG-s-8 retires that store and its seam; an opener on another local store is FWD-7 territory, not this cell -- the same split 1.0.0_SA_CTO ruled at 94456). Each opener is resolved to the store it names through its own file's bindings; an opener whose target cannot be resolved is COUNTED, never excused.
  DECLARED-OUT-OF-CELL  infra/aws/globgrph/comp_debt.py:215  [kuzu.Database(]  store=kuzu_stitch_db  conn = kuzu.Connection(kuzu.Database(path, read_only=True))
CONSUMERS_OPENING_OUT_OF_CELL_STORE=1 (printed above, excluded from the count by the narrowing, NOT dropped)
CONSUMERS_OPENING_LOCAL_DB=0 of 29
CONSUMER_PROBE_CONTROL=FIRED -- planted opener caught 2 of 2 signature(s) CANONICAL_DB_PATH,kuzu.Database( at line(s) 2,4,4 through the SAME detector, in-process, on a temp string (never a tracked file), both classified CANONICAL
CONSUMER_PROBE_BAND_CONTROL=FIRED -- the same two tokens planted in a docstring, a comment and a string tuple scored 0, so the banding is exercised and not merely asserted
CONSUMER_NARROWING_CONTROL=FIRED -- a planted stitch-store opener resolved through a `for` target over a literal tuple classified OUT-OF-CELL (store=kuzu_stitch_db, line 8) and a planted opener on an unresolvable parameter classified UNRESOLVED-COUNTED (line 3), so the narrowing is exercised in BOTH directions and the fail-closed limb is not a promise
rc=0
```

**THE THREE-TO-ZERO IS ACCOUNTED FOR MEMBER BY MEMBER, so no reader has to infer which change did
what:** `kuzu_cost_enrich.py:127,197` -> the file is DELETED and prints on the ABSENT line;
`kuzu_ac_traversals.py:92` -> REPOINTED, no `kuzu.Database(` remains in it; `comp_debt.py:215` ->
still there, still opening, now classified `DECLARED-OUT-OF-CELL` on the stitch store. Denominator
falls 30 -> 29 for exactly one reason: one more declared file is absent.

## P4.5 THE CRITERIA AT `5eb0324a7b` + this pass's writes -- every one re-run, none carried by citation

| id | verdict | invocation (bounded) | deciding output | rc |
|---|---|---|---|---|
| D7-AC1 | **PASS by output** | `bash .../seam_unreachable.sh` | `SEAM_REACHABLE=0 of 3` / `SEAM_REFUSAL_KIND_RUNTIMEERROR=3 of 3` / `SEAM_PROBE_CONTROL=FIRED` | 0 |
| D7-AC2 | **PASS by output** | `bash .../consumers_no_local_db.sh` | `CONSUMERS_OPENING_LOCAL_DB=0 of 29` / `CONSUMER_PROBE_CONTROL=FIRED` / `CONSUMER_PROBE_BAND_CONTROL=FIRED` / `CONSUMER_NARROWING_CONTROL=FIRED` | 0 |
| D7-AC3 | **PASS by output** | `python .tools/comp-find --corpus aws 'opal-globgrph' --budget 120 --limit 5` | `VINTAGE: Built from the estate as of 2026-09-09 12:23:34 UTC.  manifest: 83c6e1335f43` then `DENOMINATOR: 87 hit(s) across 2158 aws node(s) scanned [corpus=aws]`; `WITHIN BUDGET: scanned 1 of 1 pull ... used 2.17 s` | 0 |
| D7-AC4 | **PASS by output** | `bash .tools/comp-blast component:AdvisorsTab.tsx --budget 90` | `VINTAGE: Built from the estate as of 2026-09-09 12:23:34 UTC.  [vintage=... manifest=83c6e1335f43 nodes=27304 edges=58794]`; `transport: HTTPS /graph/cypher -- no local database, no cache, no fallback` | 3 (the ratified NOT-FOUND state, as at passes 1-3; rc is not in the expect) |
| D7-AC5 | **PASS by output. THE PINS DID NOT DECAY** | `for f in ...; do git show HEAD:$f \| sha256sum ...` | `8b79ca1bdfd51c18...` / `80d60f8ffa3c3c5d...` / `9dd104db29d558e4...` -- all three identical to the cut | 0 |
| D7-AC6 | **PASS by output** | `python .tools/tests/test_g2_disclosure_battery.py` | `DENOMINATOR: 7 of 7 arm(s) recorded a pass` then `PASS`; every arm's RED mutant convicted | 0 |
| D7-AC7 | **PASS by output** | `bash .../commit_gate_all.sh` | `pre-commit gate clean (18 .py file(s) + .tools/comp-find; denominator 19 of 19)` | 0 |
| D7-AC8 | RECORDED (judgment; NO verdict) | P4.6 below | -- | -- |

**`commit_gate_all.sh` gained ONE row and lost none it could keep:**
`infra/aws/globgrph/kuzu_ac_traversals.py` was added (18 files, was 17).
`infra/aws/globgrph/kuzu_cost_enrich.py` is NOT in the list and cannot be -- a removed file has no
bytes to gate, the same reason the two deleted seam tests are absent, and listing it would make the
script exit 2 on its own success.

**THE BATTERIES, direct AND under pytest at the file grain** (the compiler-tools mandate):
`test_cg8_seam_retired_battery.py` -> `DENOMINATOR: 6 of 6 arm(s)` + `PASS`;
`test_comp_find_battery.py` -> `COMP-FIND BATTERY: 12/12 PASS (denominator 12)`;
`test_comp_similar_battery.py` -> `=== comp-similar battery: PASS (12/12) ===`;
`test_comp_cluster_cli.py` -> rc=0; and
`python -m pytest -q <the five files>` -> **`24 passed, 1 skipped in 40.69s`**.

## P4.6 `D7-AC8` -- the reading act, PASS 4 addendum (judgment; NO verdict; `3.0.0_SA_CVO` grades this at L9)

**(1) Does anything USER-FACING still hold a path to a local build?** On the executable plane, no:
`SEAM_REACHABLE=0 of 3`, `CONSUMERS_OPENING_LOCAL_DB=0 of 29`, and the two `kuzu.Database(` calls
that survive anywhere in this order's population are `comp_debt.py:215` (stitch, declared, placed)
and -- outside the population entirely -- the two `tsgraph_spike` scratch loaders declared at row
W2-S25, each of which `rmtree`s and rebuilds its OWN store. **The last file that could re-create the
canonical store on the machine it ran on is gone**: `kuzu_cost_enrich.py` opened
`os.path.join(WORKSPACE, 'kuzu_nessie_db')` unguarded, and `kuzu.Database` CREATES an absent store
(`3.0.0_SA_CVO`'s measurement, kuzu 0.11.3, ADJUDICATION_v1 C-S20/C-S21).

**(2) THE DOCUMENTATION PLANE IS UNCHANGED, AND THAT IS THE PART STILL WORTH GRADING.** Every item
pass 3 named is re-measured at this HEAD and none moved:

| residue | instrument at this HEAD | reading |
|---|---|---|
| `.tools/tool_index.py` help text | `comp-read .tools/tool_index.py --enumerate 'kuzu_nessie_db'` | **`6 hit(s) across 5789 lines`, `DOCSTRING=0 COMMENT=0 DEF=0 CODE=6`** (3 whole-value, 3 substring) at `:1067, :1087, :1103, :1173, :3269, :4054` -- still telling a user the DEFAULT surface is `kuzu_nessie_db` which "auto-refreshes ENGINE-INTERNALLY". Unchanged from pass 3. |
| `org/modules/graph/comp_aws_cli.py` | `sed -n '2857p;2866p'` | `:2857` comment `comp-kuzu's DEFAULT surface is _canonical.CANONICAL_DB_PATH = kuzu_nessie_db,`; `:2866` a LIVE `print(...)` -- `comp-kuzu's canonical surface (kuzu_nessie_db, Nessie-sourced) still serves its`. Unchanged. |
| `org/modules/graph/debtscan/comp_similar.py:591` | `sed -n '591p'` | `and cap.get("corpus_db") == "kuzu_nessie_db"` -- an equality on the retired name, in CODE. Unchanged. (Note the PATH: it is under `debtscan/`, not `org/modules/graph/` directly, and it is outside this order's `<paths>`.) |
| `org/modules/graph/graph-call-manifest.yaml` | the commit gate's own MANIFEST-ADVISORY output, this pass | 25 findings, 5 "would block", still advising a repointed consumer to "Route graph queries through comp-kuzu so they hit the canonical persisted Kuzu DB". Row **W2-S23**, unchanged. |

**The reading, stated plainly and without a verdict:** the retirement is real on the plane that
executes and unfinished on the plane that instructs. Four of those five carriers are outside this
order's `<paths>` or outside its cell; `tool_index.py` and `comp_aws_cli.py` are inside it, and this
pass did not edit them because the amendment carried the residue "exactly as before, unchanged" and
a worker does not widen its own order. Whether a retirement the estate's own manifest still argues
against is COMPLETE is `3.0.0_SA_CVO`'s call at L9.

**(3) Gateway cost, cumulative across the passes:** no repointed consumer exceeded its own budget in
any pass; this pass's new consumer costs 6-8 round trips and a 301 B largest response. No cache, no
shadow copy, no ephemeral download, no second transport was built at any point.

## P4.7 ROWS FILED THIS PASS

The channel header claimed **116 rows**; **VERIFIED by parsing every fenced json block and summing
their lengths -- 116 rows in 114 blocks, 116 unique ids, `W2-S1..W2-S26` contiguous** -- so the next
id is `W2-S27`. After this append: **117 rows in 115 blocks, 117 unique ids**, restated in the
header.

| id | class | hazard | one line |
|---|---|---|---|
| `NFRA_CLDGRPH-W2-S27` | OBSERVATION | INERT | the repoint of `kuzu_ac_traversals.py` could not be like-for-like: the served client carries neither a DB PATH nor a Cypher PARAMETER DICT, so the `--db` flag was removed outright and the preflight interpolates a module-level literal |

**NO EXISTING ROW IS EDITED.** `W2-S26` (BLOCKING/ARMED, `disarm_owner` `2.0.0_SA_COO~A`) recorded
`D7-AC2` failing at 3 of 30; this pass answers it at 0 of 29, but the disarm is the issuer's to
record and the append-only rule forbids editing the row. It travels ANSWERED-BUT-ARMED.

## P4.8 WHAT REMAINS, NAMED

1. **The laptop's own `kuzu_nessie_db*` directory** (~47 MB, gitignored, in the MAIN workspace) is
   the issuer's act at the drain (Andrew's word @`61d5ef55dd`), never this worker's. This branch
   proves the CODE no longer reads it.
2. **`comp_debt.py:215`'s stitch open** is FWD-7 territory and the issuer's placed manifest row.
   The stitch store now has a READER and no WRITER on this branch.
3. **The documentation residue** in P4.6(2): two carriers inside this order's `<paths>`
   (`tool_index.py`, `comp_aws_cli.py`), two outside (`comp_similar.py:591`,
   `graph-call-manifest.yaml`). A single narrow order closes all four.
4. **Cost attribution on graph nodes** -- the capability `kuzu_cost_enrich.py` stood for -- is
   PLACED by `1.0.0_SA_CTO` at L10 as a producer-side manifest row, lane `0.8.0_AE_CloudComp`.
