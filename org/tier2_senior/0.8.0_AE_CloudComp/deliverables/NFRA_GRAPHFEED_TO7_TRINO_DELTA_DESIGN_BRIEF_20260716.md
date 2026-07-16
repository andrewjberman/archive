# NFRA_GRAPHFEED TO-7 -- Trino-layer-wide DELTA: the assessment + design brief (pre-DDL, CTO gate)

**Author:** 0.8.0_AE_CloudComp~Z · **Date:** 2026-07-16 ~04:4xZ · **Authority:** LD-0299 amend-1
(Andrew verbatim: "this is something i wanted to explore for the trino layer as a whole, as we
need delta on the trino analytics. i would refer it back to MSTR and 0.8.0_AE~Z")
**Rule of the wave:** this brief lands at CTO's gate BEFORE any DDL / derive-leg diff. Nothing
in this document is applied.

## 1. The principle (one sentence)

The graph SUBSTRATE is version-travelable (Nessie/Iceberg snapshots) but every analytics OVERLAY
on top of it overwrites itself -- "a snapshot that forgets yesterday" (LD-0298 sec-3) -- so the
fix is ONE standard: every STATE-shaped analytics surface gets a DATED APPEND-ONLY SNAPSHOT
SIBLING in Iceberg, making day-over-day delta a first-class Trino query instead of a rebuild.

## 2. The load-bearing distinction: STATE-shaped vs EVENT-shaped surfaces

- **STATE-shaped** (rows = current state; an overwrite DESTROYS yesterday): these NEED a sibling.
- **EVENT-shaped** (rows = timestamped events; the store is append-only or re-derivable from an
  append-only log): the log IS the delta substrate; a sibling adds nothing.
Applying a sibling to an event-shaped surface is pure storage waste; skipping one on a
state-shaped surface is the LD-0298 gap. Every ruling below states its shape first.

## 3. Per-surface enumeration + ruling (the denominators: 10 surfaces, every LD-0298 sec-3 row + the 2 born since)

| Surface | Shape today (grounded) | Shape class | RULING |
|---|---|---|---|
| code_heat | 2 parquets `repo=`, OVERWRITTEN per emit (live-listed; fresh 03:40:45Z) | STATE (per-path current heat) | **SIBLING YES** -- high value: band drift / cooling-trend queries; ~24k rows/emit, trivial for Iceberg |
| ms_heat | latest JSON + dated JSON snapshots (TO-5, live) | STATE | **SIBLING YES -- THE FIRST INSTANCE** (sec-5) |
| fedobs_observations | ONE S3 key, overwritten nightly 04:30Z | STATE (signal rollups) | **SIBLING YES** -- flatten the 3 signals to rows; ~1.1k pair-rows/night |
| obs_findings | parquet per `observer=`, NO date dim | STATE (findings-as-of) | **SIBLING YES** -- add the date dim via the sibling, not by mutating the existing store |
| tool_activity | 5 parquets `source=`, one per source, overwritten | VERIFY-FIRST (rows likely event-grain w/ timestamps -> re-derivable) | **HOLD for one check**: read one parquet's schema; if rows carry event timestamps + the emitter re-derives from append-only logs, rule NO (event-shaped); else sibling. The check is named, not assumed. |
| axes_history (comp-axes, TO-3) | append-only JSONL + per-run S3 objects | Already the pattern (local form) | **MIGRATE-OPTIONAL (phase 2)**: mirror into the SAME Iceberg convention so axis rows are Trino-queryable; the local store stays the comp-axes reader |
| CSE log (globgrph.cse) | append-only Iceberg, 56,497 rows | EVENT -- the exemplar | **NO sibling** (it IS the delta substrate) |
| graph_nodes/edges/contracts | Nessie/Iceberg snapshots, FOR VERSION AS OF proven | Versioned substrate | **NO sibling** (time-travel native) |
| comp-heat / nerves maps | derived-on-demand / rebuilt views BY DESIGN | Ephemeral views | **NO sibling** (their design is no-store; comp-axes snapshots already capture their headline rows daily) |
| node_health / comp_debt | UNMATERIALIZED (flag off) / reader ABSENT | N/A | **DEFERRED** -- rule each when it materializes; the convention below is what they conform to on arrival |

## 4. The ONE convention (what CTO gates; what STNDRD names)

**One Iceberg table per sibling'd surface, in the globgrph namespace, same Nessie catalog:**

- **Name:** `{surface}_snap` (PROPOSED -- the nomenclature line is 0.7.0~Z's/OPAL_STNDRD's to
  rule; ask sent, their grammar wins over my placeholder).
- **Schema:** the surface's own row shape, flattened (the cse_store precedent: hoisted query
  dims + fidelity JSON blocks where nesting exists), PLUS four standard columns:
  `snapshot_date` (string YYYY-MM-DD, identity partition key), `computed_at` (epoch ms),
  `producer_ref` (the emitting run/marker), `marker_head` (graph vintage at emit).
- **Partitioning:** identity on `snapshot_date` + the surface's existing partition key
  (`repo`, `observer`, `source`...), mirroring the cse (source, event_date) precedent.
- **Write path:** the surface's OWN producer appends one batch per emit, AFTER its primary
  write, BEST-EFFORT (a sibling failure never fails the primary emit -- the derive_runner
  :1966-1975 pattern, already house law). Append-only; one Nessie commit per batch; the
  cse_store ICEBERG-409 retry treatment.
- **Read path:** delta = a Trino self-join / window over two `snapshot_date`s. comp-axes delta
  stays the local ad-hoc reader; Trino carries the analytical queries (band transitions,
  cooling trends, cluster drift -- the queries COO's ms_heat proposal named).
- **Retention:** rows retained indefinitely by default (they are small: the full ruled set sums
  to <30k rows/day); Iceberg snapshot-metadata maintenance rides the EXISTING nightly
  run_iceberg_maintenance leg. No S3 lifecycle on Iceberg data (Iceberg owns its files).
- **Size math (printed, per day):** code_heat ~24k rows; ms_heat ~5.5k; fedobs ~1.2k;
  obs_findings ~0.1k. Sum ~31k rows/day ~= 11M rows/yr -- comfortably Trino-scale.
- **SIBLING-FAILURE VISIBILITY (CTO rider R1, 043919Z -- part of the convention, ships WITH
  every sibling's DDL phase):** best-effort-never-fails-the-primary stays the write-path
  priority, but a silently-failing sibling is a silently-gapped delta series -- the LD-0298
  hole one layer up. Therefore EVERY sibling ships with a freshness twin on its latest
  snapshot_date (the freshness_alarm.tf registry pattern: one map entry per sibling watching
  a per-sibling heartbeat key the append leg writes; a lapsed sibling ALARMS, never ages
  silently). The twin is part of the phase's DDL+writer change, not a follow-up.
- **DEV-BOX WRITER PATH (CTO rider R2, named check for P2+):** Nessie REST is IN-VPC ONLY
  (cse_store.py:33-36 -- "not reachable from the dev box"), so any DEV-BOX-RESIDENT producer
  (code_heat post the TO-2 option-(a) ruling; potentially ms_heat's local runs) CANNOT append
  its sibling direct. The house answer already exists: STAGE-THEN-INGEST -- the dev-box writer
  stages the sibling batch as JSONL/parquet to the warehouse staging prefix and the in-VPC
  nightly leg appends it (the cse_ingest sweep pattern, live since the 03:30Z producer). P2's
  plan carries this as a VERIFIED CELL: exercise one staged batch end-to-end (stage -> sweep ->
  Iceberg count) before code_heat_snap's DDL is called done. No direct dev-box->Nessie
  credential path is created for this.

## 5. ms_heat: the first instance (concrete, gated, small)

Phase 1 DDL (post-CTO-GO): `ms_heat_snap` per the convention; writer = a sibling append in
ms_heat_index.py's persist() (the engine already builds the rows; the append is a projection);
runs on the COO-ruled nightly-post-derive leg. The TO-5 JSON snapshots continue unchanged (the
S4 tools read the JSON index; Trino reads the sibling) until CTO says otherwise. This also
subsumes CTO's option-(c) backlog note from TO-2: a Trino-queryable heat sibling is the natural
home for any future container-visible heat re-source.

## 6. Sequencing proposal (all gated; nothing moves without the GO)

P1: STNDRD nomenclature line (0.7.0~Z) -> CTO gates this brief -> ms_heat_snap DDL + writer.
P2: code_heat_snap (highest analytical value: the heat axis over time) + fedobs_snap.
P3: obs_findings_snap + the tool_activity VERIFY-FIRST check -> its ruling.
P4 (optional): axes_history Iceberg mirror.
Each phase: one DDL + one producer-side best-effort append + exercised counts, RAVC'd.

## 7. What this brief does NOT do

No DDL, no derive-leg diff, no producer edits -- assessment + convention only, per the wave
rule. The tool_activity ruling is explicitly HELD on its named check rather than assumed.
