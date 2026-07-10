# B4 DESIGN — comp_learns serving-layer vintage disclosure (D-4 terminal-lies fix)

**Author:** `0.8.0_AE_CloudComp~E` · **Date:** 2026-07-10 · **archetype:** DIAGNOSE (design)
**Assigned:** `1.0.0_SA_CTO~A` (B4, 2026-07-10) · **Shared seam:** `0.7.0_AE_CloudOps~B` (flagged D-4 in the P3a audit `d24659b07`)
**Status:** DESIGN for arch-gate — NO build yet (routing to CTO~A first, per B4). Coordination with 0.7.0~B in flight.
**Sovereign boundary:** globgrph tool-use loop only; no bd/49F/Schwab.

## The defect (D-4, source-grounded)

`infra/aws/globgrph/comp_learns_produce.py:180-206` `produce()` assembles the served status
(`s3://opal-313476888478-globgrph/served/comp_learns_status.json`) with exactly ONE freshness field:

```
:189  "computed_at": now_ts,                    # int(time.time()) -- when produce RAN
:190  "computed_at_iso": ...gmtime(now_ts)...,
```

`now_ts` is stamped fresh EVERY run and is **never derived from the underlying catalog vintage**. The
views (DEMAND/GAP/COST) are computed over the Trino federation (tool_activity x code_heat x iceberg), but
if any catalog is stale — e.g. `tool_activity` hasn't been emitted in 2 days — the served status STILL
reads `computed_at: <now>`. A consumer sees a fresh stamp and trusts stale-derived numbers. **The
artifact's own freshness stamp lies about the freshness of the data it serves = terminal-lies at the
SERVING layer** — the same shape as the P3a leg-3 producer problem, one layer up (the audit's D-4). It is
worse than an absent field: a confident-wrong freshness reads as healthy.

Grounding: `comp_learns_produce.py:189 @ b2389745b`; the parity columns that make the fix possible are
`tool_activity_emit.py:27-28 @ working-tree` (`{repo_head_sha, computed_at}` are ACTUAL columns "so the
comp-drift Trino per-catalog sweep can SELECT DISTINCT the vintage and detect a stale-read"); code_heat
mirrors the same parity columns; the estate already uses a `source_vintage` + `_provenance._nessie_head_status`
pattern (`kuzu_load.py:272`, `_canonical.py:82`).

## The fix (design)

**Separate "when assembled" from "how fresh the data is," and DISCLOSE the binding vintage.** In `produce()`:

1. **Read each catalog's vintage** via the same Trino transport (`run_trino`), reusing the parity column
   the comp-drift sweep already reads — one cheap query per catalog:
   - `tool_activity`: `SELECT max(computed_at), arbitrary(repo_head_sha) FROM tool_activity`
   - `code_heat`: same parity columns (`max(computed_at)`, `repo_head_sha`)
   - `iceberg`: its latest snapshot timestamp (`$snapshots` / `max(committed_at)`)
2. **Add `source_vintage` to the status dict:**
   ```
   "source_vintage": {
     "tool_activity": {"computed_at": <ts>, "iso": ..., "repo_head_sha": <sha>},
     "code_heat":     {"computed_at": <ts>, "iso": ..., "repo_head_sha": <sha>},
     "iceberg":       {"snapshot_ts": <ts>, "iso": ...},
     "overall": {"computed_at": <STALEST of the three>, "iso": ..., "status": "current|BEHIND",
                 "lag_seconds": now_ts - <stalest>}
   }
   ```
   `overall` is the STALEST input — a federation is only as fresh as its stalest catalog (the binding
   freshness). `status` reuses the estate's head-status vocabulary (`current`/`BEHIND`), mirroring the
   mdpf `source_vintage.overall=BEHIND` convention. On a HEAD mismatch (`repo_head_sha != ajb HEAD`) or a
   lag over threshold -> `BEHIND`.
3. **`computed_at` stays but is RELABELED** in the schema/note: "when this status was ASSEMBLED — NOT the
   data freshness; read `source_vintage.overall`." Bump `schema` -> `comp_learns_status/v2`.
4. **Fail-honest, never fail-fresh:** if a vintage read FAILS (Trino error / column absent), the catalog's
   `source_vintage` entry records the error and `overall.status = BEHIND` (unknown vintage is treated as
   stale, never silently `current`) — the same honesty rule as P3c's disclosure and the leg-4 "unknown
   vintage is a signal" convention. A missing/failed vintage MUST NOT read as fresh.

## Single-vintage-definition (coordination with 0.7.0~B — RESOLVED, 195549Z)

~B confirmed and sharpened the shared definition — TWO planes, one canonical logical vintage:

- **The authoritative logical vintage = `max(computed_at)` per catalog, read DIRECTLY via Trino** (the
  same parity column comp-drift's sweep uses, `emit.py:27-29`). ~B: "it IS the single-writer parity vintage
  I recommended." **Do NOT consume ~B's number** — its gate exposes only a CloudWatch metric
  (`ParquetAgeHours`), a host-independent monitor plane, not a Trino-readable vintage. My producer already
  queries Trino, so it reads the catalog directly.
- **~B's freshness gate measures S3 object `LastModified` age** (`tool_activity_freshness/lambda_function.py:40-43`,
  a cheap hourly HEAD) — a **host-liveness PROXY** ("is the producer still WRITING?" = anti-fail-silent), a
  DIFFERENT thing from my DATA vintage ("how old is the data I'm SERVING?" = logical staleness). Both legit,
  different planes. In the normal single-writer path they agree within seconds; they diverge in exactly ONE
  case — the 0-row-skip (`emit.py:503-524`: a source with 0 parsed rows freezes both its `LastModified` and
  its `computed_at` while other partitions advance). That per-partition divergence is ~B's B2 (per-host-only
  coverage); my `overall=stalest` correctly catches it because a frozen partition's `max(computed_at)` lags.

**CAVEAT — `repo_head_sha` is EMITTER-HOST HEAD, not origin (~B's B5).** The host trigger does not git-sync
before compute (`tool_activity_emit_local.sh`; the CTO 2026-07-08 contract req#1 is unmet), so on a lagging
host `repo_head_sha` can be behind `origin/CLOUD`. It is an honest vintage of the data-AS-EMITTED, so the
disclosure MUST label it **`repo_head_sha` = "emitter-host HEAD"**, NOT "origin HEAD" — claiming origin HEAD
would itself be a terminal-lie. ~B routes B5 (fetch+disclose, not force-sync-the-live-tree) to CTO~A separately;
this design consumes `repo_head_sha` as-emitted and labels it accordingly (does not depend on B5 landing).

**LIVE VALIDATION (not hypothetical):** ~B's D-2 finding — `code_heat`'s parquet is ~2d stale (LastModified
2026-07-08 18:45Z). So the moment this disclosure ships, `source_vintage.overall.status = BEHIND` binds on
code_heat immediately — proof the fix catches the ACTUAL staleness in the estate right now, not a contrived case.

## BUILD RESULTS (2026-07-10, post CTO~A arch-gate APPROVE + COO~A P3d formalize)

Built + exercised (NOT deployed — the served write is CTO~A's diff-gate step). Files: `comp_learns_produce.py`
(`read_catalog_vintages` thin Trino wrapper + `assemble_source_vintage` PURE + `produce()` wire + `--self-test`)
and `comp_learns_status.py` (`_vintage_lines` reader surfaces the real vintage + BEHIND warning, v1-tolerant).

**PRINCIPLED DEVIATION from the design — 2 catalogs, not 3 (flagged to CTO~A).** The design said
`{tool_activity, code_heat, iceberg}`. Grounding the views (`comp_learns_views.sql`) showed they read ONLY
`tool_activity` + `code_heat` — **no view reads iceberg.** Disclosing an iceberg vintage the status does not
derive from would be its own terminal-lie, so the build scopes `source_vintage` to the two catalogs actually
read (`_VINTAGE_CATALOGS`). The `federation` string still names 3 planes aspirationally; the vintage discloses
the 2 real ones. Honest map-to-territory.

**Exercise — `comp_learns_produce.py --self-test` 6/6 PASS:**
```
AC-B4c all_fresh_current                  overall=current lag=3600
AC-B4a stale_binds_BEHIND                 overall=BEHIND binding=code_heat
AC-B4b unreadable_is_BEHIND_not_fresh     fail-honest: a trino-down catalog -> BEHIND, lag None, error surfaced
AC-B4  repo_head_sha_labeled_emitter_host keys carry repo_head_sha_emitter_host, never an origin-claiming key
AC-B4d reader_v2_surfaces_vintage_and_warns   real reader render(v2) -> "DATA VINTAGE ... BEHIND" + WARNING
AC-B4d reader_v1_backward_compatible          real reader render(v1) -> no break, honest "v1 not disclosed" label
```
Live-validated render (code_heat 2d stale): the consumer now sees
`assembled-at: <now> | DATA VINTAGE: <2d-ago> (BEHIND, binding=code_heat, lag=48.0h)` + a loud WARNING — the
terminal-lie is closed end-to-end (producer discloses, consumer surfaces).

**Consumer audit (COO load-bearing #1+#2 — additive-compat EXERCISED + no-firm-sep confirmed):** the ONLY
runtime consumer of `comp_learns_status.json` is `comp_learns_status.py` (the reader, via `.tools/comp-learns-status`).
`comp-blast comp_learns_status.json` = NOT-FOUND (an S3 artifact, not a code node — honest NOT-FOUND, not a
clear). No bd/inf/cot/schwab/49/portal/customer consumer (the "inf" grep hits are `infra/` path substrings, not
the inf firm). The no-firm-sep classification HOLDS; additive v1->v2 compat is EXERCISED against the real reader
(AC-B4d), not asserted. commit-gate clean on both files.

## Acceptance (exercise, not assert)

- **AC-B4a** — with a catalog artificially aged (or a fixture whose `max(computed_at)` < `now_ts` by > the
  threshold), the served status shows `source_vintage.overall.status = BEHIND` + a nonzero `lag_seconds`,
  while `computed_at` is still now. Exercised by injecting a stale-vintage fixture and reading the emitted status.
- **AC-B4b** — a vintage-read FAILURE (Trino error / missing column) yields `overall.status = BEHIND`
  (fail-honest), never `current`. Exercised by forcing the vintage query to raise.
- **AC-B4c** — all catalogs fresh -> `overall.status = current`, `lag_seconds ~ 0`. No false BEHIND.

## Scope / sequencing

- comp_learns_produce.py is my lane (`0.8.0_AE_CloudComp~E`-authored); the vintage-read query is additive,
  fail-safe, and does not change the views. No served-schema consumer breaks (additive fields + a v2 bump;
  `comp_learns_status.py` reader gets a one-line "show source_vintage.overall" follow-on).
- **Design routes to CTO~A for arch-gate BEFORE build** (B4 instruction). On GO + ~B's vintage confirmation,
  I build + exercise (AC-B4a/b/c) + route the diff to CTO~A, same discipline as P3b/P3c.
