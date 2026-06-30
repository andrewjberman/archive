# Deploy-Completion Ledger — ADVI_BREAKS TO-3 49F: 431167 unrealized facts-catalog restore (the served un-freeze)

**Status:** OPEN
**Opened:** 2026-06-30T16:55Z by 0.4.0_DS_ClientPlatform~B
**Deploy:** Restore the BD-DataMining unrealized template (49F) facts catalog: `facts:[]` -> 1 Fact / 11 measures, ONLY id 17 Market Value selected (BD needs >=1 measure for non-empty output). The empty facts catalog (06-25 re-provision) is the 49F served-freeze ROOT (empty unrealized -> B_01 mass-close -> D_03 empty -> D_04 publish halt). Dims byte-preserved; only the `facts` key changed (verified field-for-field vs live 431167).
**Owners:** 0.4.0_DS~B (commit, Rule 13 + verify) / 0.6.0_AE_PartnerETL (--provision + test-pull, dedicated 49F AE).
**Pairs with:** the B_01 non-empty-unrealized safety gate (closed ledger 20260630T1424Z) — this is the FEED restore behind it.

| leg | owner | step | proof required | status |
|---|---|---|---|---|
| L1 | DS~B | commit populated unrealized.json (repo-track) + s3 cp to opal-data-bd/code/bronze/templates/ | commit hash + S3 facts=1 | CLOSED 82009e463; live S3 facts=1/id17 verified |
| L2 | 0.6.0_AE | `--provision` unrealized -> BD mints NEW persisted id N carrying populated facts | created-template facts!=[] + id N | CLOSED id N=486228; BD GET /template/486228 facts=1/id17 verified |
| L3 | DS~B | write templateId=N + re-commit + s3 cp | commit hash + S3 templateId=N | CLOSED c36aa98ca; live S3 templateId=486228/facts=1/id17 verified |
| L4 | 0.6.0_AE | test-pull --table unrealized --date <run-date> (persisted N) | row-count ~100K (06-24=103,022) non-empty | OPEN |
| L5 | DS~B | VERIFY: silver/unrealized run-date + legacy key non-empty; next scheduled gold run B_01 delta-0 -> D_03 non-empty -> D_04 republish -> 49F served data_as_of ADVANCES (NEVER#4, no ad-hoc) | served header un-freeze + penny-test | OPEN |

**Closure:** all 5 legs proven + RAVC COO+CTO+Andrew. Unclosed at session end = COO alarm.

## BRANCH-A (2nd broken feed) -- discovered during the value-parity anchor pin
- 20260630T1851Z FOUND: 49F served total.aua = cert.certified_aua (NOT gold_aua); C_02 computes certified from silver/ALLOCATIONS, which is EMPTY (0-row 06-26+, BD allocations export pull-stopped; worked thru 06-24=$1.815B). D_00 had no zero-guard -> tonight's gold would serve $0 (silent-wrong). Escalated COO+Andrew.
- 20260630T1900Z no-$0 GUARD DEPLOYED commit b5a95c9f5 (safe-deploy PASS): D_00._resolve_served_aua at the 3 served-value sites + C_02 skip-degenerate-cert. FLOOR: never serves <=0. Parameterized DEGENERATE_CERT_MODE: 'hold' (default, last-good certified $1.815B) | 'gold' (position sum ~$1.62B) -- Andrew b/c contingency via env flag. (+ added from __future__ import annotations to C_02.)
- 20260630T1901Z ALLOCATIONS RESTORE co-driven (0.6.0_AE, the CLEAN fix -> guard moot if it lands): root = bronze pull stopped (390224 facts fine); re-pulled 06-29=32,633 rows; clearing manifest-skip + merge --allocations -> silver/allocations/06-29 ~6,800. Cert valid tonight IFF silver/alloc/06-29 non-empty AND client_performance advances to 06-29. Co-verifying once silver lands.

## Log
- 20260630T1655Z OPENED. Block verified field-for-field (only `facts` 0->1; id17 MV; B_01 4 identity dims intact). CTO-co-sign-gated before serving.
- 20260630T1658Z L1 CLOSED: commit 82009e463 + s3 cp; live S3 unrealized.json verified facts=1/id17. Handed 0.6.0_AE GO for L2 --provision.
- 20260630T1708Z L2 DELAYED ~15m (0.6.0_AE): --provision failed on the handed-off bd-49f-auto-login box (browser-login-only: no boto3 / opal-data-bd 403) -> rerouting. L1 unaffected (live S3 facts=1 stands). Awaiting id N.
- 20260630T1713Z L2 CLOSED: 0.6.0_AE --provisioned (local/ad-hoc, BD session not IP-bound) -> NEW persisted templateId 486228; BD GET /template/486228 verified facts=1/id17. L3 GO.
- 20260630T1715Z L3 CLOSED: templateId 431167->486228 committed c36aa98ca + s3 cp; live S3 verified templateId=486228/facts=1/id17.
- 20260630T1734Z L4 CLOSED (0.6.0_AE): persisted 486228 test-pull NON-EMPTY (06-24/26/29 all ~470K lot-rows, MV 99.7%); landed forwardfill_v2/unrealized/UNREALIZED_DAILY_2026-06-29.xlsx (471,601 rows). 06-30 empty = BD T+N freshest-date lag.
- 20260630T1745Z L5 (DS~B) in progress:
  (i) GRAIN reconciled (converter source): process_unrealized_xlsx_to_parquet dedups (account_id,asset_name) -> bronze ~471K LOT-grain collapses to ~103K HOLDING-grain silver. AC1 103K = correct silver-post-convert target (NOT stale). MV = additive column, harmless (B_01/B_02 read by name).
  (ii) FRONTIER-SELECT guard DEPLOYED commit 2acfb0401: converter skips 0-row freshest-date stubs (no empty silver partition); pairs with B_01 gate.
  (iii) BLOCKER FOUND+FIXED: silver merge is filename-keyed (incremental_unrealized_manifest); UNREALIZED_DAILY_2026-06-29.xlsx was already processed (old empty stub) -> would SKIP the corrected bronze. CLEARED the 06-29 entry from the manifest (backed up) so the next merge re-processes the 471K bronze -> silver/06-29 ~103K.
  (iv) SILVER VERIFIED (1752Z): 0.6.0_AE ran merge --unrealized; silver/unrealized/2026-06-29.parquet = 102,862 rows / 3.03MB (independently verified, NEVER#5). Grain EXACT: 471,601 lots -> dedup(account_id,asset_name) -> 102,862 holdings (matches ~103K target). My manifest-clear + 2acfb0401 guard both worked (06-30 empty SKIPPED, no empty silver). Identity cols: account_id 100%/asset_name 100%/cusip 99.9%/open_date 92.4%. B_01 veto rebuilds to 102,721 (acct,cusip) pairs (was 0 during freeze). B_01._resolve_unrealized_key(06-30) -> resolves 06-29 (delta=1, in 2d cap, non-empty) -> no mass-close PROVEN.
  (v) PENDING served-flip verify: next 23:00Z gold (cron 0 23 MON-SAT) -> B_01 delta-resolve 06-29 -> D_03 non-empty -> D_04 republish -> served data_as_of advances off 06-24. Verify on the scheduled run (NEVER#4) + penny-test, w/ 0.6.0_AE + CTO co-sign, tomorrow AM. LEGACY unrealized_gain_loss.parquet (B_02) = separate follow-on (not on the served-header path).
- 20260630T2004Z ANDREW RULED (via COO): SERVE the clean ~$1.83B tonight -- default auto-serve, NO hold-flag. Aligns with deployed state: _resolve_served_aua returns cert.certified_aua when >0, so the VALID ~$1.83B cert serves naturally; the DEGENERATE_CERT_MODE='hold' degenerate path only fires on cert<=0 (won't trigger). NO code change; explicitly NOT adding a hold-flag. L5 verify contract reaffirmed (4 ties: data_as_of 06-24->06-29; served total.aua==certified_aua; certified_aua==silver/alloc[06-29] mv-sum excl-mask to the cent; gold_aua==holdings[06-29] mv-sum to the cent). Co-verify w/ 0.7.0 (independent served) + CTO on the 23:00Z run; RAVC COO+CTO+CVO. $97M cert legitimacy stays CVO tomorrow-AM = the formal 49F-GREEN gate.
