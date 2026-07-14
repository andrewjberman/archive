# OPAL_ASSETS.C4 — ETF cloud producer bronze landing retargeted → the one bucket (pre-cutover, now)

<issued_to>0.5.0_AE_OpalETL</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<project>OPAL_ASSETS — Grand Consolidation P1</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 (TO-C4)</prd>

## Scope
Retarget your cloud ETF net-assets producer's **bronze** landing to
`s3://opal-data-assets/bronze/trueshares/{DIVZ|IDVZ}/{YYYY-MM-DD}/...` and
`.../bronze/pathfinder/{PFOE|PFDE}/{YYYY-MM-DD}/...` — raw as-fetched bytes, mid-migration, so the new
bucket accrues from day one of its existence. This ABSORBS G8-bronze (pending Andrew's formal nod on the
G-series disposition — the bytes land either way; only the ledger label waits).

**Gate:** C1 (bucket Terraform) must land first — staffing-forked to Andrew. Prep the retarget now
(config/env delta authored + committed, applied on C1 landing).

## ⚠ THE PARITY PROTOCOL IS UNTOUCHED — this TO must be provably incapable of corrupting it
- **THE LAPTOP STAYS ON.** Parity 2/3 on 07-14 and 3/3 on 07-15 proceed exactly as ordered.
- Silver parity stays quarantined to `_cloudprobe/` until 3/3; the cutover order
  (3d artifact parity → `SILVER_ROOT=""` → verify live write → ONLY THEN disable) is UNCHANGED.
- This TO touches the BRONZE landing target only. If your producer's bronze and parity-measurement paths
  share any config, split them before retargeting — state in your RAVC close how the parity path was
  isolated from the retarget.
- Your IAM fence precedent (role cannot reach `opal-data-inf` at all) is the model: the retargeted role
  gets WRITE on `opal-data-assets/bronze/{trueshares,pathfinder}/*` and nothing wider.

## <compiler_tools_mandate>
Phase 1: re-read the parity-window record (`project_etfs_netassets_cloud_parity_window`); enumerate
current landing config. New-bucket write perms verified on the live primitive per 22a (one
`--resource-arns` per call, positive control separate — comp-iam FAILS GREEN on a new bucket).
Phase 2: `.tools/commit-gate.sh`; `from __future__ import annotations` if any pipeline .py touched.
Phase 3: head-object the first landed bronze object per ticker; confirm `_cloudprobe/` artifacts
untouched (listing mtimes unchanged by this TO's deploy).
</compiler_tools_mandate>

## <cross_domain_coordination>
`_cloudprobe/` parity artifacts (your own lane) — this TO must not disturb them. The router (C2, TBD
assignee) may temporarily mirror your legacy landing; MCP the C2 assignee when native landing goes live
so the map row is retired. The one prohibition binds: nobody writes
`opal-data-inf/gold/meta/pipeline-complete.json`.
</cross_domain_coordination>

## <acceptance_criteria>
1. First trading day post-C1: 4 tickers' raw as-fetched files present under
   `opal-data-assets/bronze/{trueshares,pathfinder}/`, head-object verified. NO parquet under bronze/.
2. Parity measurements for 07-14/07-15 recorded per the standing order, unaffected (quote them).
3. An absent day is ABSENT: no roll-forward, no zeros written (attest by construction, cite the code path).
4. Session log with Compiler Tools section; RAVC close to CTO with evidence.
</acceptance_criteria>
