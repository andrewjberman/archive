# OPAL_ASSETS.C4 — ETF cloud producer bronze landing retargeted → the one bucket (pre-cutover, now)

<issued_to>0.5.0_AE_OpalETL</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<hold_released date="2026-07-14 ~01:15Z" by="2.0.0_SA_COO" corrected="2026-07-14 ~02:2xZ per Andrew-ordered review finding [0]">
THE HOLD (Andrew ~00:25Z: "Wait to dispatch until I give the go, I want to respawn the workers first" -- NO work, staged only, GO from CTO after Andrew's word) IS RELEASED. The full authority chain, cited because a release without its chain is indistinguishable from a breach:
  1. Andrew's release protocol (relayed by CTO, msg 20260714T005942Z): "Andrew is spawning YOU + DS + 0.6.2... Protocol he set: spawned agents reach out to ME confirming readiness; I validate against the live roster and GO the staged TOs in dependency order." The GO condition Andrew set = respawn + readiness confirms, with CTO holding the GO.
  2. Andrew ~01:07Z (verbatim, to CTO): "You can direct these through COO, I do not want you to be distracted with Coordination. That can be their job."
  3. CTO's pre-authorization (msg 20260714T010814Z, verbatim): "GO RELAYS against the staged TOs AS WRITTEN (the TO files + PRD v1.3.1 are the spec...) -- 0.5.0 on his registration: C4" -- "pre-authorized, no round-trip to me needed."
  4. Roster-verified at relay: 0.5.0_AE_OpalETL LIVE, PID 16876.
SCOPE OF THE RELEASE: PREP ONLY -- author + plan + commit. NOTHING APPLIES until (a) C1 verified-landed on the live primitive AND (b) CTO's apply gate -- which he PRE-CLEARED for this TO's delta 9989a27a3 (msg 20260714T015047Z) conditional only on C1-verified, with the GetObject usage boundary: re-derive TRANSFORMATION only, never landing-verification (that stays listing-based per ruling 13c). Every apply gate stays with 1.0.0_SA_CTO.
STATE (2026-07-14 ~04:4xZ reconciliation): THE FLIP IS EXECUTED -- a5e817278 applied ~03:04Z (0/2/0,
0-diff; APPLIED truth read from the live lambda config; SILVER_ROOT/ETFS_BUCKET untouched; fence incl.
the Door-6 key implicitDeny exercised from this role). AC1 (first monolith bronze at the ruled keys,
listing-based) verifies off the 22:00Z scheduled run -- apply != landing, no ad-hoc trigger.
</hold_released>
<project>OPAL_ASSETS — Grand Consolidation P1</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 (TO-C4)</prd>

## Scope
Retarget your cloud ETF net-assets producer's **bronze** landing to the monolith, at the RULED grammar
(ruling 9 v1.2 layer-inside-tree; ruling 15 v1.3.3 vendor-delivery scope; v1.3.6 ratified `{feed}`
tokens — these ARE your own implemented landing map, ratified as chosen 2026-07-14 ~01:47Z):
```
trueshares/{TICKER}/bronze/netassets/{YYYYMMDD}/          divz.html, idvz.html
pathfinder/filepoint/bronze/holdings/{YYYYMMDD}/          ETF_Holdings.csv  (ONE file, BOTH funds --
pathfinder/filepoint/bronze/dailynav/{YYYYMMDD}/          DailyNAV.csv       whole and raw; per-fund
                                                          scope materializes at SILVER only)
msn/{TICKER}/bronze/netassets/{YYYYMMDD}/{iid}.{tag}.json fallback tier, homed by ruling 15
```
Raw as-fetched bytes, mid-migration, so the new bucket accrues from day one. This ABSORBS G8-bronze
(CLOSED-ABSORBED — Andrew accepted the G-series disposition 2026-07-14 ~01:5xZ, PRD v1.3.7).
*(The original grammar in this TO's v1.0 text — `bronze/{source}/{scope}/{date}` layer-first with hive
dates — is SUPERSEDED and must not be built; the v1.2 revision block below documents the pivot.)*

**Gate:** C1 (bucket Terraform) must land first — `0.7.0_AE_CloudOps` owns it (v1.3.1 container/content
split); plans at CTO's gate. Prep the retarget now (config/env delta authored + committed, applied on C1
landing — DONE at d69efaad2 + 9989a27a3, pre-cleared by CTO).

## ⚠ THE PARITY PROTOCOL IS UNTOUCHED — this TO must be provably incapable of corrupting it
- **THE LAPTOP STAYS ON.** Parity 2/3 on 07-14 and 3/3 on 07-15 proceed exactly as ordered.
- Silver parity stays quarantined to `_cloudprobe/` until 3/3; the cutover order
  (3d artifact parity → `SILVER_ROOT=""` → verify live write → ONLY THEN disable) is UNCHANGED.
- This TO touches the BRONZE landing target only. If your producer's bronze and parity-measurement paths
  share any config, split them before retargeting — state in your RAVC close how the parity path was
  isolated from the retarget.
- Your IAM fence precedent (role cannot reach `opal-data-inf` at all) is the model: the retargeted role
  gets `opal-data-assets/{trueshares,pathfinder,msn}/*` — PutObject + scoped GetObject (the AC10
  re-derive TRANSFORMATION only, never landing-verification, per CTO's pre-rule) + prefix-conditioned
  ListBucket, NO DeleteObject, and nothing wider. Never `opal-data-assets/*`.

## <compiler_tools_mandate>
Phase 1: re-read the parity-window record (`project_etfs_netassets_cloud_parity_window`); enumerate
current landing config. New-bucket write perms verified on the live primitive per 22a (one
`--resource-arns` per call, positive control separate — comp-iam FAILS GREEN on a new bucket).
Phase 2: `.tools/commit-gate.sh`; `from __future__ import annotations` if any pipeline .py touched.
Phase 3: head-object the first landed bronze object per ticker; confirm `_cloudprobe/` artifacts
untouched (listing mtimes unchanged by this TO's deploy).
</compiler_tools_mandate>

## <cross_domain_coordination>
`_cloudprobe/` parity artifacts (your own lane) — this TO must not disturb them. The C2 router does NOT
carry ETF feeds (C2 mechanism ruling, 2026-07-14 ~02:23Z: the map is exactly three rows —
orion/eclipse/cot — and never grows; ETF lands NATIVE via this TO, "a producer's env var is the
producer's, not the estate's"). The one prohibition binds: nobody writes
`opal-data-inf/gold/meta/pipeline-complete.json`.
</cross_domain_coordination>

## <acceptance_criteria>
1. First trading day post-C1: the 4 raw as-fetched files present at the RULED keys
   (`trueshares/{TICKER}/bronze/netassets/…`, `pathfinder/filepoint/bronze/{holdings,dailynav}/…`),
   **verified LISTING-BASED — ListObjectsV2 key + ETag + Size (CTO ruling, msg 20260714T024205Z:
   head-object IS s3:GetObject and is NEVER the acceptance instrument; a listing is the only instrument
   that can prove the negative below).** NO parquet under any bronze/ path (provable only by enumeration).
2. Parity measurements for 07-14/07-15 recorded per the standing order, unaffected (quote them).
3. An absent day is ABSENT: no roll-forward, no zeros written (attest by construction, cite the code path).
4. Session log with Compiler Tools section; RAVC close **to COO** with evidence (gates and forks route to
   CTO through COO — the wave's standing routing).
</acceptance_criteria>

<revision v="1.2" date="2026-07-14 ~01:05Z" by="1.0.0_SA_CTO">
THE MONOLITH (Andrew-direct, PRD v1.2 ruling 9): one bucket stores canonical bronze+silver for EVERYTHING; grammar {source}/{scope}/{layer}/...; gold runners/platinum stay where they are. C4: landing becomes opal-data-assets/trueshares/{DIVZ|IDVZ}/bronze/{YYYYMMDD}/ and .../pathfinder/{PFOE|PFDE}/bronze/{YYYYMMDD}/ (layer INSIDE the source/scope tree). Silver mirrors at {source}/{scope}/silver/{feed}/date=YYYY-MM-DD/. Parity protocol still untouched.
</revision>
