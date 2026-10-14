# NEVER-WIDEN PACKET -- the gold ETF classifier serves the cash class for a canonical row typed Cash (IRPT_DASHBD DB-b-181, cell B = the apply): ONE S3 object

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-14 ~00:5xZ. **Ordered by:** 1.0.0_SA_CTO~DELL2 msg 7258 ("under a never-widen pair, with a count of the holdings that move"), after Andrew's smoke of 2026-10-13 ("FDRXX should be listed as a CASH tagged asset, not Fixed Income").
**Two halves, one packet:** the COO half is `NEVER_WIDEN_FDRXX_CASH_CLASSIFIER_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is applied until both halves are SIGNED on one sha256.**

## 1. The act

ONE object is replaced: `s3://opal-data-bd/code/gold/lib/etf_classifier.py` (the bucket's `code/gold/` tree is what the Black Diamond gold runner syncs, and the silver asset-dim job copies this key).

| | bytes | sha256 |
|---|---|---|
| LIVE today (S3 version `0jhXHH7axm_H934t5s5gVDVNJ6Y_WqI.`, 2026-10-12T06:18:47Z) | 18,606 | `d2e6aa88086ce9741feb3bf4df22b84996d37906730710c9d1fc79029b874250`, **equal** to `git show e340e07f4e^:data/black_diamond/scripts/gold/lib/etf_classifier.py` (measured by this seat: the live object IS the pre-change git version) |
| NEW (commit `e340e07f4e`, worker `0.9.0_WK_IRPT_DASHBD~147`, DB-b-181) | 19,496 | `e7385264668e9bf746aeab809c8ff0a869f9091685f86751b1679dfc6ddd81ba` |

The change (27 lines in one file; the worker's record is `deliverables/0.9.0_WK_IRPT_DASHBD~147/FDRXX_CASH_CHANGE.json`): a `_row_class(item)` helper returns the canonical row's `asset_class` VERBATIM, except that a row whose `sub_asset_class`, trimmed and lowercased, is `cash` returns `cash`. Every branch of `classify` and `classify_with_identity` that returns a canonical row's class goes through it. The rule is keyed on the row's TYPE, never on a ticker or a name list. `CASH_USD` (the BD synthetic cash ticker) is NOT changed: it still returns `fixed_income` before any table read (see section 7, question 2).

**Applier:** `0.7.0_AE_CloudOps~IB2` (an AE seat the gates admit, not a worker). **Command:** `.tools/safe-deploy.sh data/black_diamond/scripts/gold/lib/etf_classifier.py` in EXPLICIT-FILES mode (the 2026-08-12 precedent `org/critical_paths/change_management/20260812T1447Z_classifier-bug-heal-deploy.md` did the same with this file). The default `HEAD~1..HEAD` mode is NOT used: it would also ship any other changed BD script.

## 2. What moves, measured (counts only; none printed beyond the counts)

- **Canonical rows (DynamoDB `etf-classifications`, us-east-1, 11,361 items; read-only scans by the worker AND by this seat, equal):** 365 rows are typed Cash; 348 already carry the cash class; **17 move from `fixed_income` to `cash`**, FDRXX among them. The table's class values: equity 7,152; fixed_income 2,900; structured 527; cash 381; alternatives 239; commodities 162.
- **Served positions today (platinum advisor positions files, `s3://opal-data-49financial/advi/49financial/platinum/advisors/<id>/positions.json`, 189 files, 4,315 positions):** **at least 20 positions move** (one firm scope, 49 Financial); the count is a FLOOR, because each file holds only the top 25 positions per advisor. The accounts holding a moving lot in the newest holdings snapshot: 178.
- **No dollar changes.** The allocation computations group by `asset_class` generically (D_04 `groupby('asset_class')`); `cash` is already a published class (`CANONICAL_MIX_CLASSES` in D_04; `SERVED_HOLDING_CLASSES` in C_06). Dollars move from the fixed-income line to the cash line in a mix; each mix's total is unchanged.

## 3. When and where it takes effect (read from the code and the schedule by a research pass and spot-verified by this seat)

The upload changes nothing served by itself. Served objects change at the NEXT run of each consumer:

| consumer of the classifier | writes | trigger |
|---|---|---|
| D_04 `client_portal_summary` | 21 platinum keys incl. `advisors/<id>/positions.json`, `advisors/<id>/mix.json`, `accounts/<id>/summary.json`, `clients/<id>/composition.json`, `firm/mix_summary.json`, `firm/dashboard.json` (OVERWRITTEN each run from the latest holdings snapshot; not date-partitioned) | the gold chain (an S3 event when `silver/prices` lands) and the nightly fallback `cron(0 23 ? * MON-SAT *)` |
| D_03 `composition_artifacts` | `gold/views/firm_composition.json`, `gold/advisors/<id>/composition.json` | same chain |
| C_06 `client_mix_timeseries` | per-relationship mix and concentration history, `gold/views/mix_daily_summary.json` | same chain, `--incremental` (pinned in the dispatch catalog) |
| silver `build_bd_assets_dim` | `silver/bd_assets_dim.parquet` (`asset_class_canonical` reads `cash` for the 17 rows) | `cron(10 22 ? * MON-FRI *)` and `cron(40 22 ? * MON-FRI *)` |
| E_25 `aua_decomposition_audit` | an audit manifest | tests only whether `classify()` is falsy: its output does not change |

The monthly full rebuild (`bd_gold_monthly`) is DISABLED.

## 4. The two honest limits (these are the reason this is a pair, not a deploy note)

1. **C_06's history will show a discontinuity.** `--incremental` rebuilds only new dates, and `reclassify_retained` revisits a retained holding only when its class is outside the served six or `unclassified` (C_06 lines 275-290). FDRXX on past dates is already `fixed_income`, so past dates STAY `fixed_income` and new dates become `cash`: a client holding such a fund shows a one-day move from fixed income to cash in the mix time series on the first date built under the new bytes. D_04 overrides D_03's firm and advisor mix with C_06's class totals, so those mixes inherit it. Healing the history is a FULL rebuild of C_06, a much larger served rewrite that this pair does NOT cover (it would need its own pair).
2. **Other classifier copies are not touched.** The Cottonwood copy (`data/cot/scripts/gold/lib/etf_classifier.py`), the `opal-partners-data` Lambda's own classifier and the Investor Reporting holdings snapshot path do not import this file. Wherever those serve FDRXX it still reads fixed income. This pair does not promise that every page shows CASH: it promises the Black Diamond gold and platinum products above do.

## 4b. Writers of the changed property, counted

The property is the served `asset_class` of a security from the canonical table. **One rule** writes it: `_row_class`. **Four writers consume that one rule** (D_04, D_03, C_06, the silver asset-dim), N = 4, each reading the same function; E_25 consumes it without a changed output. No writer outside these four imports this file. Each writer's own behaviour on a changed class is read in section 3, not predicted from the rule.

## 5. Both branches

- **Branch A (a run lands under the new bytes):** the content differences are exactly section 2's, on the objects of section 3, from that run on; nothing already served is rewritten except by the next run's normal overwrite (D_04's platinum keys) or the incremental merge (C_06's new dates).
- **Branch B (the new module fails or a consumer refuses):** the module imports cleanly or every consumer stops at its import; the applier therefore runs, BEFORE the upload, the four classifier test files at the pinned bytes (37 passed on the worktree) and an import of the module with the shared client resolved, and STOPS on any failure. A consumer that fails after the upload leaves its previous served objects in place (the jobs overwrite on success), and the rollback below restores the previous module.

## 6. Rollback, per key

The one key: `s3://opal-data-bd/code/gold/lib/etf_classifier.py` (bucket versioning `Enabled`, measured). Rollback = copy the previous version back as the new latest: `s3api copy-object --bucket opal-data-bd --key code/gold/lib/etf_classifier.py --copy-source "opal-data-bd/code/gold/lib/etf_classifier.py?versionId=0jhXHH7axm_H934t5s5gVDVNJ6Y_WqI."` (the applier re-reads the live version id at that moment and records it), then the same hash read-back (`d2e6aa88...`). Equivalent: `git revert e340e07f4e` and the same `safe-deploy.sh` call.
**The rollback is PARTIAL for C_06**, and the pair says so: after a run has written new dates under the new rule, a rollback restores the module but does not revisit those dates (retained dates are not re-classified), so they stay `cash` until a targeted rebuild of those dates. D_04's platinum keys and the silver dim are overwritten by their next run and return to the old class by themselves.

## 7. Conditions, and the questions for the CTO's half

**Conditions.**
1. **Ledger entry first**, bound to this packet's sha256: `deploy_ledger.py open --slug bd-gold-etf-classifier-cash-type-20261014` with legs L1 git (the commit pin `e340e07f4e`), L2 s3-prefix (the `comp-pipescript deployed` MATCH line for the key), L3 verify (the first D_04 run after the upload: the advisor positions files read, the count of positions whose ticker is among the 17 moved rows and whose served class is not `cash` is 0 among those present, the moved count is at least the 20 floor or the reason is stated). The ledger stays OPEN to L3 and is recorded known-held on that run if it has not happened inside its window. Read every live worktree's `.open_deploys/` first and print the denominator.
2. **The live bytes are re-read at the moment of the apply:** the live object's sha256 must equal `d2e6aa88...` (the pre-change git version); any other value means another change reached the key and is a STOP. The upload is the explicit-files `safe-deploy.sh` call with the NEW file's sha256 `e7385264...` verified by its ETag/SHA read-back and `comp-pipescript deployed`.
3. **The pre-upload tests run at the pinned bytes** (the four classifier test files, 37 passed, and an import with the shared client resolved), else STOP.
4. **Not while a gold chain run is in flight** (read the dispatch state at the moment; the upload during a run would let one job read the old module and another the new within one chain).
5. **No full rebuild, no manual run of C_06 `--full`, no `main()` upload by the applier**: the next scheduled and event-driven runs carry it.
6. The apply is not made during another seat's open ledger entry on the Black Diamond gold code tree.

**Questions (the CTO's half decides them):**
1. **The C_06 discontinuity (section 4, item 1):** accept it, or order a full rebuild afterward under its own pair?
2. **`CASH_USD`:** leave it `fixed_income` (as now; its tests pin it as "kept exactly as it was"), or also move it to `cash`? Moving it changes the class of every synthetic sweep-cash position, a larger set than the 17 rows this pair counts and not counted here.
3. **Is it enough that the Cottonwood and partners-Lambda copies stay as they are** (section 4, item 2), given Andrew's smoke was on an Inflection client's Opal report?
4. **The silver asset-dim's legacy blend column:** for an asset whose BD super-class is coarse and whose canonical class is now `cash`, `ETF_TO_BD_SUPER` has no `cash` key, so the row is recorded as `bd_coarse` rather than `etf_classifier_fallback`; only the legacy blend column and its source label change. Accepted?

## 8. Not established, and so not covered

Which page reads which of the keys by route (the research named AdvisorBookView and ClientsTab from the D_04 manifest, untraced); the front end's treatment of `cash` against `fixed_income`; downstream readers of `silver/bd_assets_dim.parquet`; the schedule of E_25; whether the platinum files are read by the Inflection client's Opal report at all; the true count of moving positions beyond the top 25 per advisor.

-- 2.0.0_SA_COO~D2
