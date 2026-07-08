# FRESHGUARD leg-4: per-table vintage in the marker-oracle -- design for CTO arch-gate

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-08 · **Status:** DESIGN (staged for CTO arch-gate; NOT applied) · CTO-noted Non-P0
**TO:** NFRA_GLOBGRPH.FRESHGUARD (GOV-A I1: false-freshness at the freshness contract)

## Problem
The branch-head marker (`warehouse/_branch_head.main.json`) carries ONE `committed_at_iso` + ONE `writer_id` (whoever stamped LAST) + per-table `snapshot_id`. Any writer stamping the marker (cse_store / incremental_updater) refreshes `committed_at_iso` to "now" -- so the oracle header (`_provenance.format_provenance_header`) reads FRESH even when `graph_edges` (SOLE writer = the daily derive) is 23h+ stale. That masked the ~day derive freeze. A single HEAD timestamp cannot express per-table vintage.

## Fix (CTO ruling -- keep one HEAD, add per-table vintage)
1. **KEEP the one-marker-HEAD.** Single marker, all tables share ONE Nessie HEAD (version-consistency; CSE rides it). DO NOT split the marker -- this is the invariant.
2. **ADD per-table `last_write_iso` to the marker.** In `table_metadata[<table>]`, alongside `snapshot_id`/`metadata_location`, add `last_write_iso` = ISO of that table's CURRENT-snapshot timestamp (`snap.timestamp_ms`). GROUNDED-FREE: every marker-writer already calls `t.current_snapshot()` per table (derive_runner.py:419, incremental_updater.py:663, cse_store) -- `snap.timestamp_ms` is on the same object, zero extra I/O. This records WHEN each table's DATA was actually written, independent of who stamped the marker.
   - So even when cse_store stamps at 03:37Z, it records `graph_edges.last_write_iso = <the stale derive's snapshot ts>` (e.g. 07-07 03:38Z), not "now".
3. **ADD a per-table cadence-vs-vintage staleness flag in the oracle header.** Per-table expected max-age:
   - `graph_edges`: derive daily -> STALE if > 26h (one nightly + grace; mirrors DEFAULT_AGE_WARN_HOURS)
   - `graph_nodes`: incremental (SQS) -> STALE if > ~6h (frequent; tunable)
   - `cse`: append -> STALE if > ~26h (daily-ish)
   - `graph_contracts`: on-ratify -> lax / advisory (no hard cadence)
   `format_provenance_header` prints per-table `last-write Xh ago [STALE > Nh]`. A stalled sole-writer now reads `graph_edges: STALE 23.4h` even under a minutes-old marker `committed_at`.

## Consumer updates (the payoff)
- **`_provenance.format_provenance_header`**: add the per-table vintage + staleness block (the header stops lying "current" when a table is frozen).
- **INFRPT section C (`check_graph_head`, task #9)**: consume `graph_edges.last_write_iso` (not the bare marker `committed_at_iso`) -> closes section C's OWN edge-staleness blind spot (it currently reads the marker stamp, which self-heals on cse/node writes).
- **comp-kuzu header**: reads the marker -> gains per-table vintage; a consumer sees `graph_edges`' TRUE age even if comp-kuzu's local pin/rebuild is stuck.

## Folds in the corrected comp-kuzu finding (DS~B-triangulated; CTO escalated 130107Z)
The comp-kuzu `rc=143` Arrow-S3-FinalizeS3 bug is a MARKER-FINALIZE failure: the data-load may reach HEAD but the pin never advances -> the header flags BEHIND while serving HEAD (or serves stale existing) -- NON-DETERMINISTIC, and the provenance LABEL is untrustworthy either way + it re-rebuilds per call. CTO re-dispositioned this (130107Z): it is NOT "degraded-but-honest" -- it is genuine FALSE-FRESHNESS at the QUERY surface (same class as the derive-freeze, at comp-kuzu). Two consequences folded here:
- **TRUTHFUL-HEADER = REQUIREMENT (not a recommendation; CTO 130107Z):** an unfinalized pin -> the header MUST read a HARD `UNKNOWN/UNFINALIZED`, NEVER a soft `BEHIND` that might be wrong. The per-table vintage MUST reflect the ACTUAL committed pin, not a claimed one. leg-4 makes the S3 marker's per-table `last_write_iso` the authoritative freshness source consumers cross-check, independent of comp-kuzu's flaky local pin.
- **The FinalizeS3 rebuild-finalize bug itself = a SEPARATE LOAD-BEARING repair (CTO: prompt, graph-platform lane):** comp-kuzu is the Rule-20 DEFAULT estate query surface, so a stuck/untrustworthy pin hits every agent. leg-4 does NOT fix it (it makes the marker the trustworthy cross-check); the Arrow-S3 `FinalizeS3` fix in `kuzu_nessie_load` is tracked separately + prompt.

## Producer scope + the one design recommendation
The stamp logic is DUPLICATED across derive_runner / incremental_updater / cse_store. Adding `last_write_iso` in 3 places invites drift. RECOMMEND centralizing the marker-stamp into a shared helper in `_provenance.py` (it already owns `read_branch_head_marker` + `format_provenance_header`) -- one `stamp_marker(tables)` all writers call. If you'd rather keep the change minimal now, I add `last_write_iso` to the 3 sites + a TODO to centralize; your call.

## Blast radius / rollback / verify
- Additive marker field (older readers ignore `last_write_iso`; new readers gain per-table staleness). Header additive. One HEAD preserved -> version-consistency intact. Rollback = revert.
- I3 exercise: the RECENT INCIDENT is the natural red fixture (`graph_edges` 23h old under a fresh marker `committed_at` -> header must show `graph_edges STALE`). Green = post-fix all-current -> no STALE. Exercise both post-apply; CVO verifies.

## Ask
Arch-gate GO on: (a) the marker schema addition (`last_write_iso` per table), (b) the per-table cadence thresholds above, (c) centralize-the-stamp vs 3-site + TODO, (d) header degraded-on-unfinalized-pin. On GO I implement (touches the 3 marker-writers + `_provenance.py` + INFRPT section C), coordinated derive-image rebuild, exercise-verify -> RAVC you + CVO.
