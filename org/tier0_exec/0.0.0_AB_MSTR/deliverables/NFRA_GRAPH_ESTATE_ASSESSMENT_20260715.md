# NFRA Graph-Estate Assessment — 2026-07-15 (Andrew-direct special task)

**Author:** 0.0.0_AB_MSTR · **Assessed:** 2026-07-15 ~17:40–18:40Z · **Mode:** read-only (LD-0297 hold honored — zero dispatches)
**Method:** live instrument exercise (comp-kuzu x4, comp-fedobs, comp-learns-status, rail-log walks) + registry/PRD/TO cross-check + source grounding. Every negative claim re-measured live; retrieval denominators printed in-session.

---

## 1. The learning loop (SEMCTL: MOTIF / PROMOTE / FEDOBS + kin)

**Architecture (closed 07-09):** five planes — CSE (C0 event spine) → COMPILERKIT (compilation) → FEDOBS (horizontal federation) → MOTIF (C2/C3 vertical composition) → PROMOTE (directive writeback, human-ratified). All five component projects closed complete 07-08/09, each CVO exercise-certed, and the loop closed on a REAL end-to-end promotion.

**What is genuinely alive:**
- **FEDOBS runs nightly on schedule** — EventBridge cron(30 4 * * ? *), verified against this morning's served vintage (04:30:38Z). Queries are Iceberg-snapshot-pinned with the marker-pin bracket (follow-on (b) LANDED). comp-fedobs reader works, vintage-honest.
- **PROMOTE is alive event-driven** — a SECOND real promotion materialized 07-14 (motif:silent-display-fork RATIFIED→MATERIALIZED, commission CTO-PROMOTE-20260714T0950Z, GOV-B materialize_live exercised: hot-registered + verified in the live dispatch set). Lifecycle store: 22 events — small but real, and the invariants (zero auto-mutation, CTO ratifier) held.
- **comp-learns** (04:00 cron) + comp-learns-status GAP×HEAT "build-next" surface work. **LIVELEARN active** (07-12): the EFFECTIVE sensor loop, CYCLE A gated on CTO's G1 cadence ruling (consumption-driven ensure_fresh vs scheduled sweep).

**The load-bearing gap — the loop observes a frozen past:**
- **`iceberg.globgrph.cse` is STATIC at 342 events** — identical count at SEMCTL close (07-09) and today (07-15, verified via comp-fedobs `cse_log_total`). The emitters exist as code (cse_emit_agent / deploy / frontend_coevolution / graphhead / promote) but **no standing emitters run**; the `graph_head --full` (~55k-event) stream and "standing/scheduled emitters" follow-ons never landed. The observation planes federate nightly over a seed corpus that stopped growing the day the loop was certed. **The loop is CLOSED but not yet FED.**

## 2. comp-which — state and efficacy

- **Adoption is total and fabric-wide:** 12,765 rail-log lines; since 07-08 alone: **7,564 ROUTE-POSTERIOR** routings across every active lane (top: 0.7.0 x67 serial-tagged events, DS x49, 0.5.0 x40, 0.8.0~Z x33...).
- **Corrected quality numbers** (COMPASSURANCE §0 errata, full-tally adjudication 07-13 — supersedes three wrong measurements, each a retrieval-pattern defect): posterior share **80.2%**, legacy cascade **18.8%**, true abstain **2.5%**, **zero-result rate ~34%** — a third of routings return nothing decision-useful. That zero-rate is the real efficacy ceiling today.
- **The Rule-21 rail is live and biting:** since 07-08, 168 DENY + 41 audited RUN-OVERRIDE; DENYs observed firing minutes before this assessment. comp-grep/comp-glob on-rails fallbacks carry real traffic (692 + 270 runs since 07-08).
- **Andrew's 07-13 top-k redesign is NOT built.** The COMPASSURANCE PRD (CTO~Z: "top-5 with attached description") exists; `.tools/comp-which` (1,710 lines) has no top-k path. ~Z-lane execution was redirected 07-14; the build awaits the wave being directed. **Verdict: comp-which is heavily used, honestly instrumented, materially imperfect (34% zero-rate), with the ratified fix designed but parked.**
- Routing self-test (`comp-which-routing-test.py`) had not completed after ~10 min at write time — consistent with the cold-path latency pattern below.

## 3. Trino outputs layer — axes, display, and the delta question

**What exists (LIVE since 06-29):** single-node Trino on Fargate over three catalogs — `iceberg.globgrph.{graph_nodes,graph_edges,graph_contracts}` (Nessie), `code_heat` (hive+Glue over vintage-stamped parquet), `tool_activity` (Behavior×Change×Estate 3-plane JOIN). Canonical federated queries exist in `_trino_fed.py` (heat bands hot/warm/cold, coldest-files, etc.; verified JOIN: 374 portal files = 312 cold / 50 warm / 12 hot).

**How axes are displayed:** stdout tables only — comp-fedobs (3 signals), comp-learns-status (GAP×HEAT), comp-heat, comp-pulse. Ad-hoc Trino = in-VPC one-shot Fargate, **~3–4 min/call** (the sub-second persistent endpoint is SCTY-gated, HELD). No dashboard, no HTML surface, no aggregate "axis map."

**Is anything stored so we can track delta? Effectively NO — this is the estate's biggest analytic gap:**

| Axis surface | Persistence | Delta-capable? |
|---|---|---|
| code_heat parquet | vintage-stamped snapshot, **overwritten** per emit | NO — and **STALE since 07-08 (153h)**: the in-derive emit flag `GLOBGRPH_CODEHEAT_ENABLED` is day-one-off and absent from the task-def; the recurring-trigger decision is an **open Andrew call** (freshness_alarm.tf note, routed COO~B). comp-learns-status currently self-flags BEHIND on this binding. |
| fedobs_observations.json | single S3 key, overwritten nightly | NO |
| obs_findings parquet | per-observer partition, **no date dimension** | NO |
| comp-heat | no store at all (derived-on-demand, by design) | NO |
| nerves danger map (comp-pulse) | local JSON, rebuilt | NO |
| comp_debt_baseline.json | one baseline | one-shot delta only |
| node_health | built, **NOT materialized** (GLOBGRPH_HEALTH_ENABLED off, pending post-L6 flip) | N/A |
| CSE log | append-only Iceberg — the designed time-series | YES in design — but static at 342 |
| graph tables themselves | Nessie/Iceberg snapshots (`FOR VERSION AS OF` proven in fedobs) | YES — graph-STRUCTURE delta is queryable; the analytics OVERLAYS are not |

**Net:** the graph substrate is version-travelable; every analytic axis on top of it is a snapshot that forgets yesterday.

## 4. Should we build an axis-director comp tool? — YES, thin

The axes exist but are scattered across 8+ readers (pulse/heat/freshness/debt/debris/depth/learns/fedobs) with no single entry point and no memory. comp-which already ROUTES an axis-shaped question correctly — the misses are **discovery** (an agent must know to ask) and **delta** (nothing can answer "what got hotter since last week").

**Recommendation: one thin `comp-axes` (or `comp-pulse map`) that does two things and computes nothing new:**
1. **The directory:** print every axis with its live vintage + top-3 entries + the canonical drill command (hot→comp-heat, danger→comp-pulse, cold/debris→comp-debris, data-freshness→comp-freshness, gaps→comp-learns-status, signals→comp-fedobs). Read-only aggregation over existing surfaces; also becomes the natural comp-which route target for "where should I look."
2. **The missing time-series:** on each run, append one dated snapshot row per axis to an append-only store (local jsonl + S3 mirror). That single mechanism retrofits delta-tracking onto every axis at once — "delta since <date>" becomes a diff of two rows, not a rebuild.

Estimated small build (1–2 sessions, 0.8.0/~Z-lane shaped). Pairs naturally with flipping `GLOBGRPH_CODEHEAT_ENABLED=1` (in-derive nightly emit) so the heat axis it reports is actually fresh — that flip is the single highest-leverage one-liner in this report, and it is Andrew's call per the standing trigger question.

## 5. MS graph — quality / depth / coverage — and kuzu/cypher adequacy

**Registry is stale** (`NFRA_MSGRAPH.json` says "decomposing"); the real state is far ahead:
- **S2 is DEPLOYED and LIVE in the nightly derive** (`GLOBGRPH_MS_ENABLED=1`), correctly guarded: a content/comms LEAK fails the derive closed; a gateway hiccup fails open (WARN, AWS derive continues).
- **In the graph today: 5,520 MS nodes** — 4,498 MS_FILE + 1,021 MS_FOLDER + library/site/users; full containment tree (folder→folder 952 nested) + OWNED_BY edges. Per-file props are strong: path, file_type, mime, size, **last_modified_dt**, owner_upn, web_url — write-heat is derivable from what's already carried.
- **Coverage is narrow: ONE site (`/sites/Shared`), ONE library.** OneDrive and other sites not ingested (Decision #1 re-target executed). Depth good, breadth thin.
- **S3 (heat-map) TO is authored-ahead with GO held on "live MS nodes flowing into comp-kuzu" — that condition is now MET** (verified in comp-kuzu this session) but the confirming RAVC never landed (assignee 0.8.0 base not live). **Component 3 — the findability comp-tools layer, Andrew's headline — is not built** (zero MS-facing comp tools exist).

**kuzu/cypher adequacy (exercised live, 4 queries):**
- Whole graph: **20,283 nodes / 35,490 edges** (aws + portal/TS-semantic + pipeline + MS layers).
- The good: auto-refresh is honest (detected BEHIND Nessie HEAD, rebuilt, pin==HEAD after); the provenance header is exemplary (per-table vintages, snapshot ids, cadence checks); warm queries answer in seconds.
- The friction: **(a) cold path ~10 min** (incremental refresh rc=2 → full-reload fallback — the incremental updater path failing over is the latency); **(b) untyped projection** — every node is one `CloudNode` label with `node_type` as a property and `props` as a JSON *string*, so cypher gets no label indexing and property drilling needs string ops; **(c) marker hygiene**: `graph_contracts` last-write 695h (~29 days — static or dead?), and the `cse` table is absent from the marker because `incremental_updater` doesn't stamp it (vintage unverifiable by the instrument that checks vintage).
- **Verdict: adequate for warm interactive use; not adequate for cold-start or type-rich queries.** Fixes are known-shape: make the incremental path stop failing over (rc=2 root-cause), stamp cse in the marker, and (larger, optional) typed node tables or a props-flattening pass in the kuzu loader.

## 6. Recommended actions (all gated on your word — nothing dispatched, per the hold)

1. **Feed the loop:** land standing CSE emitters (the ~55k `graph_head --full` stream + scheduled per-producer emits). Everything downstream (FEDOBS signals, MOTIF co-occurrence, PROMOTE effectiveness) is currently re-reading a 342-event seed corpus. Highest architectural leverage in this report.
2. **Flip `GLOBGRPH_CODEHEAT_ENABLED=1`** (in-derive nightly heat emit) — one env var; un-stales the heat axis and comp-learns-status; the standing trigger question was already routed to you.
3. **Approve the thin `comp-axes` build** (directory + dated snapshot rows) — retrofits delta-tracking onto all axes at once.
4. **Direct the ~Z/0.8.0 wave** you already have queued if you want the comp-which top-k redesign (your 07-13 directive) built — it is designed, parked, and the 34% zero-rate is the number it attacks.
5. **MSGRAPH:** the S3 heat-map GO condition is met — issuing the GO (+ re-staffing, 0.8.0 base not live) unblocks write-heat; Component 3 (MS findability comp-tools) needs a decomposition decision; widen ingestion breadth (sites/OneDrive) when wanted.
6. **Hygiene singles:** RCA the kuzu incremental-updater rc=2 fallback (kills the 10-min cold path); stamp `cse` in the marker; disposition `graph_contracts` (29 days static); refresh the stale NFRA_MSGRAPH registry JSON.

**One-line verdict:** the graph substrate and the loop machinery are real, certed, and partially self-running — but the loop is starving (static CSE spine), the analytics axes have no memory (no delta anywhere), and the two Andrew-directed upgrades (top-k comp-which, MS findability tools) are designed-but-parked. Feeding the spine + one env-var flip + one thin tool closes most of the distance.
