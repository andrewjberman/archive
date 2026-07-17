# NFRA_KUZUSPLIT — P0 INSTRUMENT: measured sizing basis

**Author:** 0.8.0_AE_CloudComp~D (globgrph platform build lane) · **TO:** NFRA_KUZUSPLIT.P0-P1 (COO)
**Date:** 2026-07-17 · **Box:** the dev host this session runs on (single per-box canonical)
**Citation vintage:** all `file:line` resolve at CLOUD HEAD `8a0e1f5c5` (2026-07-17). Source-grounded per Rule 22.
**Method discipline (Rule 22a):** every cost below is EXERCISED (a timed subprocess run), not a config-read.
Full-reload + incremental were run into a **scratch `--db` path** (`.p0_kuzu_scratch/`), so the shared canonical
(`infra/aws/globgrph/kuzu_nessie_db`) was never disturbed by the measurement.

---

## 0. TL;DR — the numbers that size the fix

| # | What | MEASURED | vs PRD assumption |
|---|---|---|---|
| **M1** | Full local projection (`kuzu_nessie_load --force`), per-box | **482.26 s (~8.0 min)** | PRD said ~356 s / ~6 min — **real is +35% WORSE** |
| **M2** | Incremental refresh, warm / at-HEAD (the every-agent pre-query) | **5.20 s** | PRD ~3.9 s — consistent (M2 was a 0-delta run incl. cold-Python + S3 HEAD read) |
| **M3** | The **morning ambush** = detect-large-delta + fall to full | **4.85 s + 482 s ≈ 487 s (~8.1 min)** | this is the AC-1 number the split exists to remove |
| — | full ÷ inc ratio | **482 / 5.2 ≈ 93×** | corroborates the "92× faster" claim |
| **M4** | Empirical fallback rate | **~1 full/day/box on active days** (4 ambush-days over the 4 active days 07-14→07-17) | PRD assumed ~1/day — confirmed, and the rate is currently **UN-instrumented** |
| **M5** | Shared-warm benefit (one agent warms the box for peers) | **CONFIRMED** — a 2nd caller sees `needs_refresh=False` and pays ~0 | premise holds |
| **M6** | The operator habit being replaced | the **involuntary post-nightly comp-kuzu ambush**, NOT a hand-run `comp-aws derive` | brief's derive≠full resolution holds |

**Bottom line for sizing:** the split is worth *more* than the PRD estimated. Today, on every active day, the
first agent to query comp-kuzu after the ~02:00Z nightly eats **~8 minutes** of blocking full-reload at random.
`comp-kuzu-full` at MSTR startup moves that one 482 s cost to a deterministic, non-blocking moment; every other
agent that day then pays **~5 s** (M2). The §4 hard gate (`-inc` serves labeled-stale, never full) is validated
as necessary: M3 proves the *current* code makes a worker eat the full 482 s on a large delta — the detect step
alone is only 4.85 s, so "serve the labeled-stale complete DB + LOUD log" costs ~5 s, a **~97× improvement** for a
worker that queries before MSTR's startup-full has landed.

---

## 1. The mechanism (source-grounded, HEAD 8a0e1f5c5)

- `comp-kuzu` → `kuzu_cli.py` with `GLOBGRPH_KUZU_INCREMENTAL_REFRESH=1` default-on (`.tools/comp-kuzu`).
- On a BEHIND query, `_canonical.ensure_fresh` → `_incremental_or_full_rebuild` (`_canonical.py:345-395`):
  runs `kuzu_incremental_refresh.py`; **rc=0** = incremental applied; **rc=2** = fallback (large delta / cold);
  **rc=1** = error. rc≠0 → `_default_rebuild` = full `kuzu_nessie_load` (`_canonical.py:336-342,395`).
- **The fallback gate is on NODES only** (`kuzu_incremental_refresh.py:168-176`):
  `changed = |to_upsert| + |to_delete|`; trips when `changed >= FALLBACK_MIN_ABS(4000) AND changed >= 0.25 * head_nodes`.
  Head = **20,429 nodes** → the binding threshold is **≥ 5,108 node-changes** (25% > the 4000 floor).
- **The nightly trips it BY CONSTRUCTION** (`_canonical.py:360-367`): the ~02:00Z Fargate full-derive
  whole-table-overwrites `graph_nodes` with a fresh `batch_ts`, so the first post-nightly query sees all
  20,429 node snapshot_ts changed (100% of head) ≫ 5,108 → fallback → full reload. `_canonical.py:385`
  classifies this specific branch (`"full-derive overwrite"` in the message) as the **designed daily reset,
  NOT a defect** (NFRA_GRAPHFEED TO-6(a) / LD-0298 correction).

## 2. Evidence, per measurement (observed vs expect)

### M1 — full reload cost (the thing MSTR-startup will own)
- **Run:** `python kuzu_nessie_load.py --db .p0_kuzu_scratch/full_tmp --force` (timed, subprocess).
- **Observed:** `rc=0 elapsed_s=482.26`. Iceberg read nodes=20,429 edges=36,096 → written nodes=20,429
  edges=35,752 (344 skipped-missing-endpoint). Pin = nodes_snap `4632313928956909122` / edges_snap
  `2745220434298642181`, marker committed_at `2026-07-17T18:43:39Z`.
- **Expect (PRD):** ~356 s. **Δ: +35% (482 vs 356).** The morning ambush is meaningfully worse than assumed.

### M2 — incremental refresh cost (the every-agent pre-query)
- **Run:** `python kuzu_incremental_refresh.py --current <live canonical> --db .p0_kuzu_scratch/inc_tmp`.
- **Observed:** `rc=0 elapsed_s=5.20`; delta was 0 (`upsert=0 delete=0 0.0% of head` — canonical already at HEAD).
- **Read:** 5.2 s is the *floor* (subprocess spawn + Python import + S3 Iceberg HEAD read dominate; a small
  non-zero delta adds only the MERGE/DELETE apply, still sub-10 s). Matches the PRD's ~3.9 s within measurement
  noise. This is what "all other agents `comp-kuzu-inc`" costs.

### M3 — the morning ambush (AC-1 evidence)
- **Setup:** copied the live canonical to `.p0_kuzu_scratch/stale_current`; mutated ALL 20,429 nodes'
  `snapshot_ts` (faithful simulation of the nightly whole-table overwrite).
- **Run:** `python kuzu_incremental_refresh.py --current .p0_kuzu_scratch/stale_current --db .p0_kuzu_scratch/m3_tmp`.
- **Observed:** `rc=2 elapsed_s=4.85`; `INCR_NODE_DELTA head=20429 cur=20429 upsert=20429 delete=0 (100.0% of head)`;
  `status=fallback ... 'delta 20429 >= 4000 and >= 25% of head (full-derive overwrite) -- bulk reload cheaper'`.
- **Expect:** the exact `"full-derive overwrite"` branch (`kuzu_incremental_refresh.py:174-176`) → the
  `_canonical.py:385` designed-daily-reset classification. **MATCH.**
- **Composite ambush cost = M3 detect (4.85 s) + M1 full (482 s) ≈ 487 s (~8.1 min)** on the first
  post-nightly worker, TODAY. **This is the cost the split removes** — and it is the number that justifies
  the §4 hard gate: without it, `-inc` on a large delta keeps eating 482 s.

### M4 — empirical fallback rate (+ an instrumentation gap finding)
- **Source finding:** there is **NO persistent local-refresh/fallback log sink.** The fallback/mode decisions
  are emitted only through `_canonical`'s `log()` callback to the *invoking process's stderr* (ephemeral). So
  the fallback rate is, today, **not observable after the fact** — this is the "UNSURFACED" gap in the brief
  (§4/§109-110) made concrete, and it argues for the P3 `comp-graph status` "last mode + behind-by-N + last-full-at" line.
- **Empirical proxy (the number I *can* measure):** `org/mcp/comp-tool-runs.jsonl` (the COMPCLOSE second-granular
  sink, live since 2026-07-14) logged **64 comp-kuzu calls across 4 distinct UTC days (07-14→07-17)**. The first
  query each active day pays the ambush → **~1 full/day/box on active days** (≈4 ambush events over 4 active
  days). Consistent with the by-construction floor. Caveat (denominator honesty): this sink began 07-14 and
  captures only comp-kuzu-wrapped calls — direct `kuzu_cli.py`/Lambda paths are not in it; "4 days" is the
  *sink's* lifetime, not the tool's. The RATE (1 full/active-day/box) is the decision-useful, corroborated number.

### M5 — shared-warm benefit
- **Run:** `_canonical.needs_refresh("infra/aws/globgrph/kuzu_nessie_db")` → `False, reason='current'`.
- **Read:** once one agent has warmed the canonical to HEAD, a peer's pre-query returns `needs_refresh=False`
  and pays ~0 — it rides the warm shared DB (fixed module-relative `DEFAULT_DB_PATH`, one per-box canonical
  shared via mkdir-mutex + atomic-swap, `kuzu_nessie_load.py:42` + `_canonical` swap path). **This is the
  premise the whole design rests on** (MSTR's startup-full warms the box for every subsequent agent). CONFIRMED.

### M6 — the operator habit being replaced
- **Telemetry:** in `comp-tool-runs.jsonl` — `comp-aws derive` = **0** invocations; `comp-kuzu` = **64**.
- **Read:** the recurring full-reload cost the operator feels is the **involuntary post-nightly comp-kuzu
  ambush** (M3), NOT a hand-run `comp-aws derive`. This confirms (does not merely inherit) the brief's
  source-resolution that `comp-aws derive` ≠ `comp-kuzu-full` and must NOT be MSTR's startup command
  (deriving+committing the cloud graph is the nightly Fargate's job). **NOT AMBIGUOUS** in the direction that
  matters — no P1 sizing risk from a mis-named habit. (Residual, non-blocking: whether anyone occasionally
  hand-runs `comp-aws derive` off-log — flag to CTO/Andrew as an aside, not a gate.)

## 3. Sizing conclusions for P1 (what these numbers authorize)

1. **`comp-kuzu-full` (MSTR startup) = one 482 s cost/day/box**, deterministic + non-blocking, replacing a
   ~487 s ambush that today lands on a *random* worker each active day.
2. **`comp-kuzu-inc` (every other agent) = ~5 s** warm (M2); on a large delta it must **serve the labeled-stale
   complete DB + LOUD log in ~5 s** (M3 shows detect is already only 4.85 s) — **NEVER the 482 s full** (§4).
   A worker serving labeled-stale is safe: the DB is a COMPLETE prior-vintage projection, never half-built.
3. **The §4 divergence is load-bearing, not cosmetic:** M3 proves the *current* fallback makes a worker eat the
   full 482 s. Keeping the full-fallback in `-inc` would silently reintroduce the exact ambush the project removes.
4. **P3 should surface the rate:** add `last mode + behind-by-N + last-full-at` to `comp-graph status` so the
   fallback rate stops being invisible (M4's instrumentation gap).
5. **No change to `comp-aws derive`** — the fix lives entirely in the comp-kuzu projection path (M6).

## 4. Reproducibility appendix (exact commands)
```
# M1 full (~482s): python infra/aws/globgrph/kuzu_nessie_load.py --db <scratch> --force
# M2 inc  (~5s):   python infra/aws/globgrph/kuzu_incremental_refresh.py --current <canonical> --db <scratch>
# M3 ambush:       cp <canonical> <stale>; kuzu SET all node snapshot_ts; then M2-form on <stale>  -> rc=2 "full-derive overwrite"
# M4 rate:         distinct UTC days of tool=="comp-kuzu" in org/mcp/comp-tool-runs.jsonl
# M5 shared-warm:  _canonical.needs_refresh("infra/aws/globgrph/kuzu_nessie_db") -> (False,'current')
# M6 habit:        count tool=="comp-aws" & "derive" vs tool=="comp-kuzu" in the runs sink
```
Scratch artifacts under `.p0_kuzu_scratch/` (gitignored working area; not committed). Gate arithmetic knobs:
`GLOBGRPH_KUZU_INCR_FALLBACK_ABS` (4000), `GLOBGRPH_KUZU_INCR_FALLBACK_FRAC` (0.25) — `kuzu_incremental_refresh.py:42-43`.

**P0 status:** COMPLETE. Real per-box cost + fallback rate measured and committed as the sizing basis (AC-1),
exercised not estimated. Hands off to P1 (command split) behind CTO's code arch-gate; COO sequences.
