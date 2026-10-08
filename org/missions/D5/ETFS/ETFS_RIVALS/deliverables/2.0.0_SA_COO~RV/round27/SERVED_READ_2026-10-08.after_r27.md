# ETFS_RIVALS round 27 -- the deployed package's first run: one publish of 2026-10-08 (CTO ruling msg 31818)

**Reader:** `2.0.0_SA_COO~RV`, 2026-10-08. Ledger `etfs-rivalfunds-r27`. Package pin 325bd4e0f8, applied 14:57Z.

- Payload (the one run under ledger `etfs-rivalfunds-r26` leg L3, round 26): `{"only": ["publish-page"], "date": "2026-10-08",
  "mode": "daily", "batch_id": "rv-publish-1008r27", "sink": "s3", "refresh_a1": true}` to `etfs-rivalfunds-daily-lambda`.
- Invoke 15:07:23Z to 15:09:39Z: StatusCode 200, no FunctionError, status OK. REPORT RequestId
  8af02722-bac9-4be0-8c6b-ed1a8119207c: Duration 132.3 s, Max Memory Used 930 MB of 3008 MB.
- No Bloomberg leg was running (newest file in opal_bbg_logs: the 12:23:19Z collector recovery log).
- Returned detail: holding_contribution SKIPPED "2 object(s) already at date=2026-10-08"; buying_trend SKIPPED the same;
  input_census "3 object(s) already"; AI SKIPPED_EXISTS.

## The keys it may write: before (15:05Z) and after (15:10Z)

Prefixes listed: gold/holding_contribution, gold/buying_trend, gold/input_census, platinum/page, each at date=2026-10-08
(under `s3://opal-data-etfs/rivalfunds/etfs/`). Before 38 keys, after 39. The ONE difference:

    + gold/input_census/date=2026-10-08/input_census-20261008T150929Z-3bc36465cd6c.parquet  14715  2026-10-08T15:09:30Z

Every other key has the same size and LastModified after as before, the page's three objects included (index.html
1,688,097 bytes 13:08:16Z; audit.html 1,124,242 bytes 13:08:16Z; manifest.json 104,686 bytes 13:08:18Z). Not listed: the
`state/` prefix, where the run's marker `state/publish_page/date=2026-10-08/rv-publish-1008r27.json` is new.

## The page

`index.html` fetched after the run is byte-equal to the 13:08Z page (1,688,097 bytes). Accounts reading "earlier build":
0. Badges reading served: 25 (the 26th is TXUE's grounding FAIL, as at 13:08Z). BRANCH A of the COO half: nothing but the
census object and the marker was written; no figure moved; no badge moved.

## Full listing before

    gold/holding_contribution/date=2026-10-08/holding_contribution-20261008T110358Z-83932dd85862.parquet	121258	2026-10-08T11:04:00+00:00
    gold/holding_contribution/date=2026-10-08/holding_contribution-20261008T130053Z-db6b4ec57a4e.parquet	122338	2026-10-08T13:00:55+00:00
    gold/buying_trend/date=2026-10-08/buying_trend-20261008T110451Z-ac65106e37db.parquet	70246	2026-10-08T11:04:53+00:00
    gold/buying_trend/date=2026-10-08/buying_trend-20261008T130145Z-ebed8c26b96b.parquet	70608	2026-10-08T13:01:47+00:00
    gold/input_census/date=2026-10-08/input_census-20261008T110527Z-997dd47e1d8d.parquet	15366	2026-10-08T11:05:28+00:00
    gold/input_census/date=2026-10-08/input_census-20261008T130223Z-da88756ea773.parquet	14731	2026-10-08T13:02:24+00:00
    platinum/page/date=2026-10-08/audit.html	1124242	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/BASG.json	382219	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/BIDD.json	495832	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/CGIC.json	1137936	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/ETFT.json	311025	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/GQGU.json	530606	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/IDVZ.json	366038	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/INEQ.json	492921	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/PCLG.json	319518	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/PFOE.json	245337	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/SCHY.json	436128	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/TSEL.json	274141	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/TXUE.json	414016	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/WCMG.json	318461	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/index.html	1688097	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/manifest.json	104686	2026-10-08T13:08:18+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/audit.html	705733	2026-10-08T13:08:12+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/BASG.json	382568	2026-10-08T13:08:15+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/BIDD.json	496947	2026-10-08T13:08:13+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/CGIC.json	1128869	2026-10-08T13:08:13+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/ETFT.json	314919	2026-10-08T13:08:15+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/GQGU.json	531016	2026-10-08T13:08:15+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/IDVZ.json	370126	2026-10-08T13:08:13+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/INEQ.json	507411	2026-10-08T13:08:14+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/PCLG.json	321120	2026-10-08T13:08:15+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/PFOE.json	247110	2026-10-08T13:08:14+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/SCHY.json	442225	2026-10-08T13:08:14+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/TSEL.json	276093	2026-10-08T13:08:15+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/TXUE.json	428730	2026-10-08T13:08:13+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/WCMG.json	314581	2026-10-08T13:08:14+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/index.html	1458895	2026-10-08T13:08:12+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/manifest.json	102578	2026-10-08T13:08:12+00:00

## Full listing after

    gold/holding_contribution/date=2026-10-08/holding_contribution-20261008T110358Z-83932dd85862.parquet	121258	2026-10-08T11:04:00+00:00
    gold/holding_contribution/date=2026-10-08/holding_contribution-20261008T130053Z-db6b4ec57a4e.parquet	122338	2026-10-08T13:00:55+00:00
    gold/buying_trend/date=2026-10-08/buying_trend-20261008T110451Z-ac65106e37db.parquet	70246	2026-10-08T11:04:53+00:00
    gold/buying_trend/date=2026-10-08/buying_trend-20261008T130145Z-ebed8c26b96b.parquet	70608	2026-10-08T13:01:47+00:00
    gold/input_census/date=2026-10-08/input_census-20261008T110527Z-997dd47e1d8d.parquet	15366	2026-10-08T11:05:28+00:00
    gold/input_census/date=2026-10-08/input_census-20261008T130223Z-da88756ea773.parquet	14731	2026-10-08T13:02:24+00:00
    gold/input_census/date=2026-10-08/input_census-20261008T150929Z-3bc36465cd6c.parquet	14715	2026-10-08T15:09:30+00:00
    platinum/page/date=2026-10-08/audit.html	1124242	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/BASG.json	382219	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/BIDD.json	495832	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/CGIC.json	1137936	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/ETFT.json	311025	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/GQGU.json	530606	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/IDVZ.json	366038	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/INEQ.json	492921	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/PCLG.json	319518	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/PFOE.json	245337	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/SCHY.json	436128	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/TSEL.json	274141	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/charts/TXUE.json	414016	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/charts/WCMG.json	318461	2026-10-08T13:08:17+00:00
    platinum/page/date=2026-10-08/index.html	1688097	2026-10-08T13:08:16+00:00
    platinum/page/date=2026-10-08/manifest.json	104686	2026-10-08T13:08:18+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/audit.html	705733	2026-10-08T13:08:12+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/BASG.json	382568	2026-10-08T13:08:15+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/BIDD.json	496947	2026-10-08T13:08:13+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/CGIC.json	1128869	2026-10-08T13:08:13+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/ETFT.json	314919	2026-10-08T13:08:15+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/GQGU.json	531016	2026-10-08T13:08:15+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/IDVZ.json	370126	2026-10-08T13:08:13+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/INEQ.json	507411	2026-10-08T13:08:14+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/PCLG.json	321120	2026-10-08T13:08:15+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/PFOE.json	247110	2026-10-08T13:08:14+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/SCHY.json	442225	2026-10-08T13:08:14+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/TSEL.json	276093	2026-10-08T13:08:15+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/TXUE.json	428730	2026-10-08T13:08:13+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/charts/WCMG.json	314581	2026-10-08T13:08:14+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/index.html	1458895	2026-10-08T13:08:12+00:00
    platinum/page/date=2026-10-08/revisions/20261008T130811Z/manifest.json	102578	2026-10-08T13:08:12+00:00
