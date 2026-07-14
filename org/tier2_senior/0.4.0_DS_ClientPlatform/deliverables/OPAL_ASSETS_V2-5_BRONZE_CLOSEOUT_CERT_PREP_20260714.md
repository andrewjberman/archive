# OPAL_ASSETS V2-5 — Bronze Close-out Certificate: PREP SKELETON (NOT THE EMISSION)

**Status: PREP.** Final emission is GATED on V2-1/V2-2/V2-4 landing + V2-3 orion CLEAN; any role/grant
that changes after 0.7.0's sweep gets re-verified before emission. Acceptance gate: CTO.
**Joint authorship:** DS = certificate + census + AC3 · 0.7.0 = IAM (blocks @ `fee17bd46`, attribution
"0.7.0 (simulate, 20260714T0622Z)"). **Measured:** 2026-07-14 ~05:0x–06:3xZ, read-only throughout.
**TO:** `OPAL_ASSETS.V2-5` @ `99e97b2e0` (AC3 per ruling 26).

## The table (state as measured; UNKNOWN is a row, never a blank)

| channel | 1 BACKFILL (set-identity / holes) | 2 DAILY INTERVAL | 3 IAM (0.7.0, simulate 0622Z) | 4 ROBUSTNESS (C5 std) | AC3 CONTENT |
|---|---|---|---|---|---|
| schwab/0833 | **COMPLETE**: 6,932 obj, 18 types, 20240708→current; 3-tier remap-verified (C3); pre-floor 257 = named Glacier leg | rules `canonical-schwab-si2-08335338` cron(45 9,21) **ENABLED**; landed bytes @ 0710 verified via census parses | **CLEAN**: Q01–Q10, M01–M10 | PARTIAL-CITED: 3-tier verify + session lock + xref-success rule (0.6.2's machinery); full producer characterization NOT done by DS — cite or read before emission | **PASS++**: T1-tied parses, latest partition per type (b62919644) |
| schwab/0824 | **COMPLETE-STAGING / monolith LANDED (delta 08:2xZ)**: staging 5,966/5,966 terminal (17 types, 20230712 floor→0710 frontier, per-type sum ties exactly); **monolith bronze now 5,970 obj live (comp-assets census 07:38Z; 5,966 remap + the 07-14 morning C3 fire — run-time denominators, not a discrepancy); feed roster carries NO fam/slm, matching the W4 17-type census on landed bytes**; set-identity cell awaits 0.6.2's guard verdict on the remap | same rule family, cron(15 10,22) **ENABLED**; **07-14 morning fire verified on landed bytes (newest write 06:47:48Z + _ops/daily_pull sidecar)** | **CLEAN**: Q01–Q10, M01–M10 | same as 0833 row | **PASS++**: T1-tied parses incl. rlw (250,201×75) |
| orion | **DEEP + CORRUPT-PENDING-REPAIR**: 6,909 obj, 2020-04-24→07-10, 2,269 dates; 2,269 type-collapsed keys; Andrew AUTHORIZED deletion ~05:1xZ → V2-3 clean re-backfill (source intact) | mirror cron(15 14) **ENABLED** → deployed `opal-assets-ingest-mirror` | **CLEAN**: R01, R04–R09 (R07 = labeled mode-2 instrument row) | PARTIAL: C2 machinery (skip-if-landed, 13c) — its verify SELF-CAUGHT the collision = control exercised | **PASS**: 07-10 transactions jsonl.gz = 1,394,630 real records |
| eclipse | **COMPLETE-AS-HELD**: 624 obj, 2026-05-15→07-10, 48 days (source history extent), correct per C2 verify | mirror cron **ENABLED** (same rule/lambda) | **CLEAN**: R02 + shared negatives | PARTIAL: same C2 machinery | **PASS**: 07-10 portfolios_full.json = 856 real portfolio records |
| cottonwood | **MAP-RULED-BACKFILL-PENDING** (was HOLE; CTO ruling 063019Z): monolith tree = 30/30 markers, zero data — mirror was faithful to a marker-only prefix; **cot row re-scoped to `forwardfill_v2/` ({table} preserved), markers OUT of the mirror**; characterized **(a) BRONZE-IN-FACT @ 7904b7b91** (vendor xlsx byte-passthrough, no fill, deployed==repo). Row closes on 277 guard-verified backfill; the 30 mirrored markers = legacy surplus, raise-on-growth, cleanup on Andrew's next deletion word | source producer cron `cot-bd-session-daily` 02:00Z ENABLED; mirror cron(30 3) ENABLED (re-scope applies next cycle) | **CLEAN**: R03 + shared negatives | cot producer = **STRONG** (content gates `_export_has_data_rows`, sidecars, retry-net, fail-loud polling — cited at source) | **SHELL as the tree stands today** (ruling-26 live instance, caught by AC3 7 min after the bar landed); flips on the 277 backfill. Shells 06-22..07-09 mirror AS DELIVERED = legitimately-sparse (bronze honesty); upstream freeze stays with its 0.6.0/CTO thread (close-nothing) |
| etf (trueshares/pathfinder/msn) | **PENDING-BY-DESIGN**: 0 obj; first monolith bronze = TONIGHT 22:00Z (C4); historic (opal-data-etfs, 537 obj) remap design owed by 0.5.0 | `etfs-netassets-daily` cron(0 22) **ENABLED**, producer retargeted; C4 IAM pre-flight PASS (E01) | **CLEAN**: E01–E08. Footnote: **no deny fence** (no-grant-only); fence AFTER C4 cutover (E05 measured) — routed to CTO | UNKNOWN until first landing (0.5.0's parity protocol governs) | **UNKNOWN** — no bytes yet (honest row, verify on tonight's landing) |
| smartx | **LANDING IN FLIGHT (delta 08:3xZ — was 0 obj at skeleton time)**: C5 backfill RUNNING — 9,525 allocation-scope holdings + model feeds (changerequests/holdings/model_allocations/model_aum/performance) + platform (access_roster + 2 silver + meta/pulls manifests), landed 02:0x–06:4xZ (comp-assets census 07:38Z + live opens); per-scope set-identity = 0.5.0's guard on completion | role TF **APPLIED + fence ATTACHED, 22a-exercised** (0.5.0 @ 46646f054: isolated positive control on monolith write; opal-data-etfs + Door-6 sentinel EXPLICITDENY; policy v1 unconditioned; applied truth via list-attached-role-policies). **Behavioral leg PENDING-DEPLOY** until the C5 daily lambda first fires — UNKNOWN stays a row | **CLEAN**: S01–S07 superseded by the 46646f054 battery for the fence half; no-fence footnote RESOLVED (fence attached) | PARTIAL-LIVE: pull manifests landing at the ruling-21 meta home (meta/pulls/{date}/manifest.json — the C5-standard machinery live); full characterization on C5 close | **MIXED (opened 08:3xZ, 3 objects):** holdings.json = 11 real holdings rows (NON-SHELL PASS); platform access.json = real fullAccess roster (NON-SHELL PASS); **model_allocations/allocations.json = 267 B `data:[], count:0` — a LIVE landed instance of ruling 26's exact reference case** (the reports/model/{id}/allocations empty-payload endpoint; landed 03:56Z, BEFORE the ~05:59Z near-miss finding). Bronze honesty: the raw bytes stay; the question — is the DEPLOYED pull's feed map still hitting the dead endpoint, or did the re-ground land? — is 0.5.0's, routed this pass. The cert's smartx AC3 row cannot read PASS while a known-empty feed lands beside populated ones |

## Evidence index
- Column census + type-set divergence + T1 parses: `b62919644` (engine re-runnable; both-masters inventory JSON).
- IAM sweep: `fee17bd46` — 7/7 channels, 5/5 live roles, 46 calls one-resource-each, separate positive
  controls, negatives = firm bucket + Door-6 key + out-of-scope prefix; coverage denominator + honest
  limits in the doc header; raw simulate JSONs alongside.
- **POST-SWEEP RE-VERIFIES (the TO's re-verify clause, delta 08:3xZ):** (1) router
  `router_read_sources` re-scoped by the C2 cot-map apply ~07:1xZ (CTO-gated 59249227c) — 0.7.0's
  4-invocation 22a battery stands as the re-verify (072552Z: forwardfill_v2 allowed / isolated inf
  positive control / dropped cot-bronze implicitDeny / templates rider allowed; applied truth on live
  get-role-policy; deploy ledger 20260714T0711Z_c2-cot-map-apply closed 4/4) — the cottonwood cert row
  cites THIS, not the swept state, for that role. (2) smartx-assets-pull-role fence ATTACHED
  post-sweep — 0.5.0's battery @ 46646f054 (behavioral leg PENDING-DEPLOY, stays a row).
- Cottonwood mechanism chain: markers (monolith + source opened), forwardfill_v2 characterization at
  vintage `7904b7b91` with line citations (CTO msg 062851Z); deployed==repo diff.
- AC3 opens: eclipse + orion this session (record counts above); schwab via census; cottonwood = marker.
- Wiring reads (notification config EMPTY, rule table, targets): this session, applied-truth primitives.

## Cert rules (CTO, 063019Z — bind the emission)
- **Read a completion sentinel's ENUMERATED TABLE LIST, never its presence.** A file named
  `_BRONZE_COMPLETE` firing an EventBridge rule manufactures channel-level green; the sentinel is
  honest about its subset — the cert must be too.
- **The ruling-26 emptiness contract classifies as-delivered shells `legitimately-sparse-AS-DELIVERED`**
  (bronze honesty preserved; upstream defects adjudicate in their own threads). Carried into V2-8's
  cot converter when it lands.

## What emission still needs
1. V2-1 / V2-2 / V2-4 landed; **V2-3 orion CLEAN** (deletion authorized; 0.6.2 sequence) → re-measure orion row.
2. CTO's cottonwood map ruling → cottonwood row re-rendered (extension makes it a backfill task, not a cert edit).
3. Tonight's 22:00Z: C4 first landing (etf rows 1/2/AC3) — listing-based verification.
4. C5 TF applied + first pull → smartx rows.
5. Schwab producer robustness citation (0.6.2) or DS read → close the two PARTIAL-CITED cells.
6. Re-verify any role/grant changed post-sweep; then emit, CTO accepts, COO dispatches V2-7 on it.

*Coverage denominator of this prep (updated 08:3xZ): all 7 channels enumerated; 6 of 7 now have landed
bytes (smartx joined 02:0x–06:4xZ; etf remains tonight's 22:00Z); every landed channel's content
OPENED (AC3) — 2 via T1-parse, 2 via record-count open, 1 marker-SHELL (cottonwood, flips on the 277),
smartx 3-object open = MIXED (2 NON-SHELL + the 267B ruling-26 instance, routed to 0.5.0).
Nothing modified; INF hold / Door 6 / frozen-3 untouched.*

## Delta log
- **08:3xZ (this pass, per COO's "prep now" dispatch):** 0824 monolith row LANDED + morning fire
  verified on landed bytes; smartx rows re-rendered off the live C5 landing (fence battery folded,
  behavioral leg held as UNKNOWN); AC3 smartx 3-object open (the 267B model_allocations find — ruling
  26's reference case, live in bronze, question to 0.5.0); post-sweep IAM re-verify section added
  (router re-scope + smartx fence); cottonwood map re-scope APPLIED ~07:1xZ (277 backfill rides the
  next 03:30Z mirror cycle — row flips on guard-verified landing, comp-assets is the reading
  instrument). Emission gates unchanged: V2-1/V2-2/V2-4 + V2-3 orion CLEAN.
