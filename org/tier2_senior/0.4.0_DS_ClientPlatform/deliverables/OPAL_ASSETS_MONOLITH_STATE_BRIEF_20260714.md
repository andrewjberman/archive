# OPAL_ASSETS / OPAL_RUNNERS — Monolith State Brief (Andrew-commissioned recon)

**Author:** 0.4.0_DS_ClientPlatform · **Date:** 2026-07-14, measurements taken ~05:0x–05:3xZ
**Commission:** Andrew-direct, this session — *"I want to know how realized our monolith is... make sure
that we are covered as hell from the ground up on the monolith system"* before OPAL_RUNNERS engages.
**Method:** read-only throughout. comp-state (self-test 3/3) over registry/JSON/TO/PRD records; live S3
listings with run-time denominators; applied-truth AWS reads (bucket notification config, EventBridge
rules + targets, Lambda existence) — never TF-desired for a landed-state claim (Rule 22a).

---

## 1. VERDICT IN ONE PARAGRAPH

The monolith is REAL AND HALF-BUILT, exactly as its records say: bronze is live-accruing on 4 of 7
channels (~14.4K objects, ~26.9 GB) with deep backfill on two, **but the silver layer is ZERO BYTES and
the bucket carries NO event notifications** — every landed bronze byte currently just sits. The
bronze->silver machinery (C6 registry) is authored + mutant-exercised on real vendor bytes but not
deployed; wiring is the 0.7.0 container half, C7 deploy is AE. Paper tracks the estate within minutes.
OPAL_RUNNERS is correctly parked in Phase 0; its read-only evidence lanes (W2/W3/W5) are PRD-legal to
run parallel, and W3 doubles as the P-3 ligament table the monolith itself needs.

## 2. PAPER STATE

- **OPAL_ASSETS:** PRD v1.6.0; registry row fresh (~04:57Z). 13 TO files + 1 superseded. C1 complete;
  C2/C3/C4/C5/C6/C7/C10 pending; C11 staged (C3+C6); C12 pending; C9 phase-A-delivered/phase-B-at-CTO-gate;
  C8 absorbed; P0-A (DDB gold skeleton) pending at 0.8.0. comp-state: 7 BEHIND — ALL are records outrun
  by tonight's live movement by minutes (evidence 05:00–05:10Z: the 2,269-deletion authorization, C5
  premise verbatims, C9 Phase-A validation, all post-dating the 05:07Z convergence pass). No record
  contradicts the estate. DS-lane reconciliation committed: C10/C11 dated notes @ `bac1433ad`
  (fork-3 16-row resolution folded; statuses deliberately unchanged).
- **OPAL_RUNNERS:** PRD v0.1, Phase 0 pre-ratification; `depends_on OPAL_ASSETS`. W1 delivered-corrected
  + W4 delivered (DS); W2/W3 commissioned to 0.7.0 behind the C-series; W5 to 0.5.0 post-parity.
  **Zero TO files on disk** (W-series ran as MCP GOs); PRD §7 Evidence is a placeholder until W1–W5
  land -> ratification -> build waves.

## 3. PHYSICAL STATE — s3://opal-data-assets (run-time denominators)

| Tree | Objects | Size | Backfill (data dates) | State |
|---|---|---|---|---|
| schwab/08335338/bronze | 6,932 | 14.36 GB | 2024-07-08 -> current; 18 CRS types (acc/rps/trn/uln/upn/upt/ult/sec/fam 505 · slm 501 · rld/tcf 753 · tcfx 182 · tnn 102 · rlu/rtu 12 · rly/rty 36) | 3-tier verified, DONE |
| schwab/08242234 | 0 | — | staging pull 5,509/~5,966 (92%) at measurement | C3a remap on pull-terminal |
| orion/inflection/bronze | 6,909 | 12.46 GB | 2020-04-24 -> 2026-07-10, 2,269 dates (deepest) | CORRUPT: 2,269 type-collapsed keys; deletion AUTHORIZED (Andrew ~05:1xZ) -> delete + clean re-backfill; source intact |
| eclipse/inflection/bronze | 624 | 87 MB | 2026-05-15 -> 07-10 (48 days) | correct per C2 verify |
| blackdiamond/cottonwood/bronze | 30 | 7.5 KB | 06-13 -> 07-14 (30 daily flat-gen rows) | correct per C2 verify |
| smartx/* | 0 | — | historic queued: 1,386 obj / ~95 MB GUI-era exports (opal-data-smartx-v2) | zero-bytes BY DESIGN (C5 gate); holdings history vendor-unrecoverable, accrues day-one |
| trueshares/pathfinder/msn | 0 | — | historic queued: opal-data-etfs, 537 obj | first monolith bronze = TONIGHT 22:00Z (C4); 0.5.0 owes historic-remap design |
| **silver/** (all sources) | **0** | — | — | **THE GAP** |
| gold/** | 0 | — | — | reserved-not-built by design (P0-A = DDB first) |
| _probe/ | 10 | 350 B | — | the 9-pair target topology, present |

## 4. WIRING — APPLIED TRUTH (live reads, not TF)

**Bronze scheduled ingestion: LIVE.**
- `canonical-schwab-si2-08242234-daily-pull` cron(15 10,22) ENABLED + `-08335338-` cron(45 9,21)
  ENABLED -> SSM RunPowerShellScript on the si2 terminal (both masters, twice daily).
- `opal-assets-ingest-mirror-inf-daily` cron(15 14) + `-cot-daily` cron(30 3) ENABLED -> deployed
  Lambda `opal-assets-ingest-mirror`.
- `etfs-netassets-daily` cron(0 22) ENABLED, producer retargeted — tonight is the first monolith landing.
- SmartX: the ONE channel with no live pull — `smartx-assets-pull-role` TF authored NOT applied
  (awaiting 0.7.0); Secrets-Manager auth bundle landed (27a229d17).

**Silver event wiring: NOT SET UP.** `get-bucket-notification-configuration` on `opal-data-assets`
returns EMPTY; no silver-conversion Lambda exists in the account (list-functions checked). C6 code
ready; wiring = 0.7.0 container half; C7 deploy = AE.

**Emitter:** `opal-assets-daily-emitter` deployed, cron(15 17) ENABLED — still legacy-sourced until C11.

**Coverage denominators of this recon:** S3 = full recursive listing (14,527 keys incl. probes);
wiring = the notification config + full rule table (147 rules) + 4 rule-target resolutions + one
name-filtered Lambda listing; NOT covered: Door-6 explicitDeny re-measure (taken from the registry's
measured claim), per-object 3-tier re-verification (taken from C2/C3's own verifies), CloudWatch
execution histories.

## 5. GAP LIST TO "COVERED AS HELL" (= PRD §4b acceptance, priority order)

1. **Silver end-to-end** — deploy C6 + bucket ObjectCreated wiring + P-2 backfill over every held
   bronze partition (~14.4K objects today). The entire second floor is missing; everything else is one
   channel at a time.
2. **C2 orion repair** — delete the 2,269 authorized orphans, clean re-backfill (0.7.0; source intact).
3. **C3a** — 0824 remap on pull-terminal (~457 objects remained at measurement); Glacier-257 background.
4. **Tonight 22:00Z** — C4 first-landing verify (listing-based) + 0.5.0's ETF historic-remap design (537 obj).
5. **C5** — 0.7.0 applies role TF -> first pull (full-history performance/aum day-one) -> GUI-era mirror
   (1,386 obj, channel-labeled).
6. **P-3 ligament table** — fire/run/land/verify per connector, BOTH layers; the §4b acceptance
   instrument; does not exist yet (W3-adjacent, 0.7.0).
7. **C11 + P0-A** — emitter one-bucket + DDB gold skeleton (P3 capstone, correctly last).

## 6. OPAL_RUNNERS POSTURE (recommendation)

Correctly parked. Let the read-only evidence lanes accrue NOW in parallel (W2 cost profile + W3 trigger
census at 0.7.0 — W3 IS the ligament table; W5 auth census at 0.5.0 post-parity); hold every build wave
until silver is populated and the ligament table shows four green verdicts per live connector. Wave 1
(ingestion canonicalization) then extends the C-series naturally into the gold-analytics middle.

---
*Read-only recon; no state was modified beyond own-lane TO reconciliation notes (`bac1433ad`) and this
brief. INF hold / Door 6 / never-summed all untouched and unimplicated.*
