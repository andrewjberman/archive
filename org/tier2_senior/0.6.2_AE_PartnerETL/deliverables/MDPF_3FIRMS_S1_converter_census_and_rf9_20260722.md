# TO 3F-S1 — Converter Mechanism Census + RF-9 Regex Fix (my halves) — 0.7.0's TF half PENDING

**Agent:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-22 ~21:5xZ · **Joint:** 0.7.0_AE_CloudOps (TF apply
half — his authorization at fire time; ⛔ my pre-hold apply GO was WITHDRAWN and nothing here restores it).

## (a) Per-source census — {event rule, sweep rule, converter, DEPLOYED hash}

Event paths are S3-notification -> converter (TF `silver.tf`, DESIRED); where noted, the event path is
additionally BEHAVIOR-proven from landing latencies measured this session. Sweep rules cited from
`describe-rule` verbatim. Deployed hashes from `get-function-configuration` (applied truth).

| source | event path | sweep rule (all ENABLED) | converter Lambda | deployed CodeSha256 @ LastModified |
|---|---|---|---|---|
| orion | S3 notif (DESIRED) | `opal-assets-silver-orion-sweep-daily` cron(0 16) | opal-assets-silver-orion | `rwI6QN5q...` @ 2026-07-15T22:32:26Z |
| eclipse | S3 notif `.json` (belt-1; `/_meta/` excluded belt-2) | `opal-assets-silver-eclipse-sweep-daily` cron(0 16) | opal-assets-silver-eclipse | `5hRkhhxI...` @ 2026-07-22T14:50:08Z |
| blackdiamond (tables) | S3 notif `.xlsx` — **BEHAVIOR-proven: 07-20 file bronze 03:30:26Z -> silver 03:30:34Z (8s)** | `opal-assets-silver-blackdiamond-sweep-daily` cron(0 5) | opal-assets-silver-blackdiamond | `RzyHVtFy...` @ 2026-07-22T14:29:35Z |
| blackdiamond (rebalancer_*) | ⚠ **TF EVENT WIRING = 0.7.0's PENDING HALF** (`.json` under `rebalancer_*` + on_success grant); sweep covers meanwhile | same cron(0 5) sweep (roster admitted @6d1a15ef2) | opal-assets-silver-blackdiamond | same as above |
| schwab | S3 notif — **BEHAVIOR-proven: pull fire 10:15Z -> fact_rps_s2 partition 10:16:01Z (60s)** | `opal-assets-silver-schwab-sweep-daily` cron(15 12) | opal-assets-silver-schwab | `yMma9jOm...` @ 2026-07-15T18:40:47Z |
| smartx | S3 notif (DESIRED) | `opal-assets-silver-smartx-sweep-daily` cron(0 16) | opal-assets-silver-smartx | `aHX6HfHn...` @ 2026-07-20T19:23:28Z |
| etf | S3 notif (DESIRED) | `opal-assets-silver-etf-sweep-daily` cron(30 23) | opal-assets-silver-etf | `a14fYacw...` @ 2026-07-15T23:24:02Z |

`comp-pipescript deployed` (no-arg firm-separated sweep) ran as phase-1 input; mdpf tree summary:
17 MATCH / 3 STALE (`dim_mdpf_account_distribution`, `dim_mdpf_aggregate_aua_timeseries`,
`dim_mdpf_non_model_assets` — the actively-edited revamp producers; check-only tree) / 6 MISSING_ON_S3
(backfill/audit one-shots). Recorded as census input, not failures.

## FINDING: RF-9's "committed NOT deployed" premise is STALE — the WS-5 CONVERTER half IS DEPLOYED

Verified against the RUNTIME ARTIFACT, not the config: downloaded the live
`opal-assets-silver-blackdiamond` zip (CodeSha256 `RzyHVtFy...`, modified 2026-07-22T14:29:35Z — 0.7.0's
stream_parquet vendor-closure rebuild) and read its bytes: `_REBALANCER_RE` PRESENT,
`rebalancer_conversion.py` + `rebalancer_schemas.py` + `stream_parquet.py` all vendored. The @6d1a15ef2
converter half rode 0.7.0's rebuild into production. **What remains of S1(b) is exactly: the TF EVENT
wiring for `rebalancer_*` (S3 notification + the on_success/invoke grant) and the two-path exercise with
manifest `mode=="event"` asserted** — both 0.7.0's half, both gated on his own authorization. The sweep
backstop is meanwhile live (fact_model_assignment partitions exist for both feed days).

## (c) RF-9 regex fix — LANDED @1a7706dc1 (canonical + vendored, tests green)

- **Before:** `.xlsx` hardcoded — `data/assets/scripts/silver/mirror_conversion.py:94-96 @HEAD~1`
  (`_BD_RE ... \.xlsx$`).
- **After @1a7706dc1:** `mirror_schemas.BD_TABLE_EXTENSIONS = ("xlsx",)` — the extension is a DECLARED
  vendor-shape fact under the explicit-schema law; `_BD_RE` is COMPILED from it
  (`mirror_conversion.py:94-106`); a BD-shaped key with an UNDECLARED extension classifies LOUD
  (`classify_key` near-miss branch, vendor-drift detail) instead of silently skipping.
- Tests: 4 added incl. the re-hardcode MUTANT GUARD (pattern tail must derive from the manifest verbatim)
  + declared-path regression + loud near-miss + the `.parquet`/17a class preserved. Suite 28 passed.
- Vendored copies refreshed BYTE-IDENTICAL into the lambda package dir (BUILD_MANIFEST law: repo files
  are source of truth). **Deployed artifact does NOT yet carry the fix** (zip check:
  `BD_TABLE_EXTENSIONS` absent from the live bytes) — it rides 0.7.0's next rebuild, correctly.

## Reprocess clause: EMPTY SET, MEASURED (not waived)

The TO's reprocess was predicated on "files previously skipped because they were not `.xlsx`". Census over
ALL 413 BD bronze objects: old regex data-matches 275, new regex data-matches 275, **delta 0**;
undeclared-extension near-misses present today: **0**. The fix is structural (manifest-driven + loud
near-miss) with an IDENTICAL current match set — there is nothing to reprocess, and that is a measured
statement with its denominator, not an assumption. DS (3F-S2) notified: census denominators UNCHANGED by
this commit.

## Acceptance state

1. Census table: THIS DOCUMENT ✓  2. WS-5 deploy: CONVERTER half deployed (verified in runtime bytes);
TF event-wiring + exercise = 0.7.0, PENDING ✓(scoped)  3. Regex fix at the regex, manifest-driven,
before/after cited ✓  4. Two-path exercise: PENDING 0.7.0 (event path UNVALIDATED for rebalancer_* until
then — stated, not assumed; xlsx event path behavior-proven 8s)  5. Reprocess: empty set, measured ✓
6. Session log Compiler Tools rows: in the closing session log ✓

## SUPERSESSION (2026-07-23 ~11:20Z): S1(b)'s "PENDING TF half / event path UNVALIDATED" is CLOSED-BY-THE-ESTATE

0.7.0's v0.31.0 apply (2026-07-22 14:03Z, his ledger 6/6) landed the rebalancer event wiring AFTER this
census was written -- and BOTH paths proved on TODAY'S SCHEDULED RUNS, verified by me at the artifacts:
`meta/conversions/20260723T060051Z-40954490.json` = **mode=='event'**, 4 results (cron(0 6) runner ->
OnSuccess=opal-assets-silver-blackdiamond) and `20260723T050009Z-8530904b.json` = **mode=='sweep'**
(0 pending -- the backstop finding nothing, itself healthy). The S3-notification variant in my ask was a
DESIGN ERROR on my side: per-object rebalancer_* events are the shape CTO's WS-5 ruling rejected
(self-race / legacy-marker admission / converter-writes-own-trigger-prefix); completion-keyed on_success
IS the ruled event mechanism, and it is what fired. Residual on S1: ONLY the blackdiamond-converter
REBUILD carrying the RF-9 regex fix (one rebuild to carry both DS's S5 twin + RF-9, CTO sequencing).
