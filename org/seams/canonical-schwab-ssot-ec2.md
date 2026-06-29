# SEAM: Canonical Schwab-SSOT — EC2 end-to-end (MACRO, decomposed)

**archetype:** VALIDATE
**author:** 0.4.0_DS_ClientPlatform | **date:** 2026-06-29 | **for:** Andrew (pre-external-EC2 deploy) + DATA_SSOTMG cutover
**scale:** MACRO — full pipeline, decomposed into 9 constituent seams. **Weakest-seam-binds.**

## Why this record exists
Andrew is pushing the whole canonical Schwab-SSOT pipeline (incl. the Quartz/SI2 raw ETL) to an external
EC2 for a few-days parallel-observation run before cutover. The risk is **orphaned manual steps that never
get hooked into scheduled orchestration** — the chain "looks built" because the logic exists, but nothing
fires it unattended. This seam pass grounds every joint against live state so the hookup checklist is on
the record and nothing is forgotten.

## Seam map + verdicts (raw -> served)

| Seam | A -> B | MECH | DECL | SEM | grounded note |
|---|---|---|---|---|---|
| S1 | SI2/Quartz (EC2) -> opal-data-schwab/01_raw/ | FAIL | FAIL | n/a | UPDATE 2026-06-29: EC2 i-0f3d57a97f14727af BUILT (0.6.2, DERISK-1 closed) + landing raw -- BUT in `01_raw_quartz_validation/` (segregated), while the orchestrator reads `Prefix="01_raw/"`. **PREFIX MISMATCH** -> S1->S2 mechanically broken until reconciled. Held for Andrew cutover steer (promote validation->prod, or point orchestrator at the validation prefix for the parallel run) |
| S2 | 01_raw/ -> canonical/schwab/silver/ (17f+5d) | PASS | PASS | PASS | build_canonical_daily.py, single-partition incremental (verified) |
| S3 | silver -> canonical/schwab/gold/ G1-G10 | PASS | PASS | PASS | wired 1026138a7, dry-run 21/21, reconciles to served AUA |
| S4 | SCHEDULER -> build_canonical_daily.py | FAIL | FAIL | n/a | **NO scheduled trigger** — runs only as the manual /49-schwab-conv Step 7.5 tail |
| S5 | silver -> gold G11-G14 | PASS | PASS | PASS | CLOSED 47cc26a7f -- G11-G14 wired into GOLD_EXT (advisor_attribution/fee_efficiency/partner_analytics/split_reconciliation); dry-run 25/25 (was: materialized but un-wired) |
| S6 | cross-bucket IAM + SSE (EC2 instance role) | UNVER | PASS | — | runs on local creds today; EC2 role not provisioned |
| S7 | canonical gold -> parity harness (observe) | UNVER | PASS | — | CVO comp-parity map grounded (b65335016) but not yet scheduled for the parallel window |
| S8 | ordering: raw-land -> silver -> gold (per run) | PARTIAL | PASS | PASS | silver->gold sequential OK; raw-land -> trigger ordering undefined on EC2 |
| S+ | canonical build scripts -> EC2 (code deploy path) | PASS | PARTIAL | — | STAGED 2026-06-29: 28 scripts -> s3://opal-data-bd/code/canonical/schwab/ (verified MATCH/AES256, EC2 i-0f3d57a97f14727af can pull). DECL=PARTIAL: io-estate registration (estate-coverage-manifest) routed to CVO -- resolver is generated, not hand-edited |
| S9 | BD silver/allocations -> canonical dim_advisor_role | PASS | PASS | PASS | NEW edge (TO-7 6d48d4782): same-firm 49f bridge, vintage-flagged, <=date fallback non-fatal |

## The hookup checklist — every un-hooked seam, in deploy order (the deliverable)

1. **S1 — SI2/Quartz raw ETL (AE/DT, DERISK-1 CLOSED 2026-06-29):** EC2 `i-0f3d57a97f14727af` is BUILT + landing
   raw, but in a SEGREGATED prefix `opal-data-schwab/01_raw_quartz_validation/` while the orchestrator reads
   `Prefix="01_raw/"`. **RAW-PREFIX MISMATCH = the live S1->S2 break** — the orchestrator won't see Quartz raw until
   reconciled. Cutover options (Andrew steer): (a) promote `01_raw_quartz_validation/` -> `01_raw/` once validated, or
   (b) param the orchestrator's `SRC_BUCKET`/prefix at the validation prefix for the parallel-observation window. Keep
   the daily-AM schedule + `--sse AES256` (bucket DENIES PutObject without it — only seam that writes the raw bucket).
2. **S+ — code deploy path (DS): STAGED 2026-06-29** (COO GO 182930Z). 28 scripts -> `s3://opal-data-bd/code/canonical/schwab/{,silver/,gold/}` (verified MATCH/AES256; EC2 i-0f3d57a97f14727af can pull, Rule-12). Residual: io-estate registration (the "Unknown script in tree" close) routed to CVO -- the resolver is generated from CVO's authoritative estate-coverage-manifest; tooling-visibility, NOT a runtime blocker.
3. **S4 — orchestration trigger (DS+AE):** EventBridge cron (or S3-event on the last `01_raw/` land) -> SSM
   RunCommand / EC2 cron -> `build_canonical_daily.py --upload`. Without this the canonical layer never advances unattended. **#1 finding.**
4. **S5 — wire G11-G14 into the orchestrator (DS, my lane): DONE 47cc26a7f** (COO GO 175112Z). Added
   GOLD_EXT (G11 advisor_attribution -> G12 advisor_fee_efficiency -> G13 partner_analytics v3.0 -> G14
   advisor_split_reconciliation[_firm]) after GOLD_CORE; dry-run 25/25. The full G1-G14 set now rolls daily.
5. **S6 — EC2 instance-role IAM (AE/DT):** `s3:GetObject` on `opal-data-schwab/01_raw/*` + `s3:{Get,Put,List}` on
   `opal-data-bd/canonical/schwab/*` (SSE-AES256). comp-iam-check before first run.
6. **S8 — ordering (DS+AE):** fire the orchestrator AFTER the day's raw fully lands (S3 sentinel or sequenced
   cron-with-margin), else a partial/stale partition. `dates_to_build()` is RPS-keyed so a missing day SKIPs (surfaced, not silent) — but still a missed day.
7. **S7 — parity-harness scheduling (CVO):** `comp-parity` must itself run on schedule (each day's canonical
   gold vs BD-served gold/*, after both land) to accumulate the N-clean-days observation verdict.

## What is SOUND (do not re-litigate)
- **S2 (raw->silver), S3 (silver->gold G1-G10), S9 (TO-7 dim bridge):** all 3 axes PASS — single-partition
  incremental, dependency-ordered, dry-run 21/21, reconciles. The data-flow joints are solid.
- **DECLARATIVE structure:** the believed 17-fact/5-dim/13-gold layout is TRUE to live S3 (every prefix verified
  2026-06-29). Bucket split (opal-data-schwab raw / opal-data-bd/canonical/schwab silver+gold) consistent + firm-sep-clean (both 49f).

## Verdict
**MACRO seam = BROKEN@MECHANICAL.** Not the data joints (S2/S3/S9 sound) — the **orchestration joints** (S1 build,
S+ deploy-path, S4 schedule, S5 wire) are un-hooked, plus S6/S7 unverified-until-provisioned. The canonical
LOGIC is deploy-ready; the AUTONOMY WIRING is not. None is hard — standard scheduler + IAM + deploy-path + the
G11-G13 wire — but each is a place where "it looks built" hides "nothing fires it." Re-run this seam pass after
each hookup lands to flip the FAILs to PASS before cutover.

## grounding (Rule 22, per causal claim)
- S4/S5/S+ MECHANICAL FAIL: **SOURCE-CONFIRMED** — `build_canonical_daily.py` GOLD_CORE (G3-G10 only, no G11-13);
  `/49-schwab-conv` SKILL.md Step 7.5 (manual tail = the only invoker); `comp-pipescript io` "Unknown script in tree" for the canonical scripts (no deploy-graph entry).
- S1/S6/S7/S9 verdicts: **live-state-grounded** — no Schwab EC2 in `EC2_MANIFEST.json`; scripts run on local
  creds; harness map grounded but unscheduled; S9 verified vs the live materialized dim_advisor_role asof=2026-06-24 (schema_version 2.0, 6753 rows).

## Residual / unknowns
- S1/S6/S7 are UNVERIFIED-until-provisioned (the EC2 + role + scheduled harness don't exist yet to exercise).
- S2/S3 are dry-run-verified, NOT yet exercised on a live scheduled EC2 run (the validation surface is the first
  scheduled daily build, per NEVER#4 — no ad-hoc full exec to validate).

## Compiler Tools
| tool | use | result |
|---|---|---|
| boto3 (live S3) | bucket structure + materialization grounding | PASS — 17/5 silver, 13 gold, dim 2.0 all verified live |
| comp-pipescript io | canonical scripts deploy-graph check | "Unknown script in tree" -> confirms S+ (no deploy path) |
| comp-freshness bd | bd-silver state (S9 allocations dependency) | allocations PASS / txn-realized-unreal FAIL (the freeze, separate) |
| git show | TO-7 6d48d4782 diff verify (S9 guards) | PASS — both guards honored, write target unchanged |
