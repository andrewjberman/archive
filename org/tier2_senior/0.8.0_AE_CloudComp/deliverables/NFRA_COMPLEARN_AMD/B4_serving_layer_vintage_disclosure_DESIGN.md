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

## Single-vintage-definition (coordination with 0.7.0~B — CTO's "coordinate with ~B")

The vintage READ here is the SAME primitive ~B's P3a freshness GATE needs: ~B BLOCKS/ALARMS on a stale
catalog; this DISCLOSES it in the served status. Per ~B's own single-writer parity-vintage recommendation,
there must be ONE definition of "catalog vintage," consumed by both. **Open with ~B (message 195437Z):**
does the freshness gate measure the served-parquet S3 `LastModified` age or `max(computed_at)`, and if they
can differ, which is authoritative? The disclosure will read whatever the gate treats as canonical (prefer
consuming ~B's number over recomputing). This design assumes `max(computed_at)` pending ~B's confirmation.

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
