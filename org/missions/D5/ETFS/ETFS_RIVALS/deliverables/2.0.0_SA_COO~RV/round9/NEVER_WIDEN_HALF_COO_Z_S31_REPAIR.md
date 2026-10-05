# NEVER-WIDEN -- COO HALF: ETFS_RIVALS row Z-S31 -- deploy the holding_contribution fail-soft at CLOUD b8b47bb8e7, republish 2026-10-05 ONCE with refresh

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-05 ~21:4xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why (row Z-S31, @ca39e20a20):** round 9's nm-3 made `gold_holding_contribution` list `gold/security_names`, which the deployed daily
and publish-page roles cannot do (no grant in `gen_policies.py`). The D12 Step B refresh republish (21:16Z, ledger
etfs-rivalfunds-d12-step-b CLOSED @b8b47bb8e7) therefore failed holding_contribution with AccessDenied: the served page still reads the
prior holding_contribution object, so IDVZ's rankings read a window from 2026-08-21, and tomorrow's page day would have NO
holding_contribution object at all. The repair (my lane): the names read is optional -- unreadable means no stored names, recorded in
the manifest. The IAM grant itself is lane CLOUD_OPS_OR_ETL: its patch is `round9/Z-S31_IAM_GRANT_FOR_AE.patch`, routed through
1.0.0_SA_CTO~Z; until it lands, stored names are skipped (none exist yet) and the sweep's security_universe step reports FAILED
(caught; the page is unaffected).

## VERDICT: SIGNED

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (slug `etfs-rivalfunds-z-s31-repair`).
2. **`safe-apply` of `C:/tmp/rv_apply21.tfplan`** from `C:/tmp/rv-r8` detached at b8b47bb8e7: 0 to add, 5 to change, 0 to destroy, code hashes
   only; before = the D12 set (daily uEUmJ+ny, fetch 9Qn1CeZF, canonical 0BUVdGFS, silver RK3Hk+9t, publish 0GpPs6dP). The package
   differs from 35c6b3a923 in `gold_holding_contribution.py` (fail-soft) and tests only; `leg_gates.json` unchanged (D12 "1").
3. **ONE republish:** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda {"only":["publish-page"],"date":"2026-10-05","mode":"daily",
   "batch_id":"rv-publish-1005s31","sink":"s3","refresh_a1":true}`; AI SKIPPED_EXISTS.

## EXPECTED OUTCOME -- MEASURED ON A POST-BACKFILL MIRROR

`rivalfunds/etfs/` synced at 21:3xZ (after Step B), the pin's `publish_page.handler_entry` with the event above: status PARTIAL
(freshness elsewhere), holding_contribution **OK, refused 0** (g4_tri 897, holding_implied 486, missing 44, mixed 1,951); page
1,865,203 B (cap 2,097,152); data-refused 0; IDVZ **"Data available since 2026-01-02, through 2026-10-02, 188 trading days"** (served
today: since 2026-08-21). holding_contribution alone peaks at 473 MB post-backfill (650 MB pre-backfill, 3,853 vs 3,837 rows), and
round 8's A1 refresh already ran on the 1,024 MB Lambda.

## BLAST RADIUS, PER KEY

| key | before | after | rollback |
|---|---|---|---|
| five Lambdas' code | the 35c6b3a923 set | the b8b47bb8e7 set | a saved plan at 35c6b3a923, `safe-apply` |
| gold/{holding_contribution,buying_trend,input_census}/date=2026-10-05/ | newest objects | +1 object each | republish after the code rollback |
| platinum/page/date=2026-10-05/{index.html,manifest.json} | batch rv-publish-1005d12, kept under revisions/ | batch rv-publish-1005s31 | republish after the code rollback |
