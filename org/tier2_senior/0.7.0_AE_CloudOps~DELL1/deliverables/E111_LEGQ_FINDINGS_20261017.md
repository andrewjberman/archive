# TO-SC-e111b leg Q findings (0.7.0_AE_CloudOps~DELL1, 2026-10-17 ~08:40Z)

Claim words: `measured` = read this session.

## What ran (measured)
- Runner i-01003b035d2988dfb started 08:39:43Z, SSM online 08:40:04Z, FIRST command `systemctl stop gold-layer-runner` (CommandId 30f4e4c3-07f7-4422-a2f0-516fd909d5ff, Success, no gold process, no boot-chain step started).
- SECOND command (CommandId 0b53294a-e25f-4896-9a16-c9fc8092c762): `BD_PLATINUM_MODE=canonical bash /tmp/gold_dispatch.sh --single E_18`, script pulled from S3 (box md5 of gold_dispatch.sh 165933f6, of E_18 f5c03ee6). SINGLE-RC=0, wall 4.7s, 0 ERROR lines. Instance back to `stopped` by 08:44Z (the wrapper's own 2-minute shutdown).
- `etf-classifications` before vs after the single: 11375 items both; 13 seeded present, 9 held-out absent, first 200 sorted keys with `last_updated` identical (E111_LEGQ_TABLE_BEFORE/AFTER_20261017.json).

## Two reads that differ from the order's text
1. **The nine held-out tickers were NOT reported unresolved.** The output reads `Scheduled-classification candidates: 0`, `Already resolved (in resolution table): 9`, `Truly unresolved: 72` (tickerless names), and none of the nine tickers is printed. Measured locally (read-only, E_18's own helpers on the same holdings file `gold/holdings_lots/2026-10-09.parquet`): each of the nine is in open holdings (1 pair each), `pk in known = False` (absent from the canonical table, as intended), and `name in ticker_resolution = True` (4424 names). E_18's resolution check (`continue` at the `norm_name in resolved_names` line) skips them BEFORE the planner, so they are counted as "already resolved" and never listed. The request's measurement (PLANNED 0, UNRESOLVED 9) called the shared planner on the nine names directly and so bypassed that filter. Effect on the table: none (0 candidates, 0 writes). Whether this fails the order's leg Q read is the issuer's call.
2. **The single ran with `--upload`.** The dispatcher strips `--upload` from E_18 only when `DRY_RUN=1` (`gold_dispatch.sh:388-390`); `--single E_18` alone keeps the registry flag (`E_18|...|--upload`, header `flags: --upload`, log `Queued 72` = upload true). With 0 candidates there was no plan and no put, so nothing was written to the table. The no-upload form is `--dry-run --single E_18`.

## Other runner-written state (the single's own, as in the e102 singles)
- `gold/.checkpoints/2026-10-17/E_18.done` re-written 08:40:48Z (VersionId nca0gzFrxuuxS3_zqnYzYZdnZAxzCcFm; the 04:00Z fire's version RGRrPTrzzunavim.oGxonASJq9aH3nip, 05:04:50Z, is the prior). Read only under `GOLD_RESUME=1`.
- `gold/perf_report.json` re-written with the one-script report; archived copy `gold/perf_history/perf_report_2026-10-17_2026-10-17T084048Z.json`; telemetry `logs/gold-layer/telemetry/bd-gold-layer-runner/E_18/af6715ee5c90.jsonl`.

## Deploy-side note
`safe-deploy.sh` ships E_18 but treats `gold_dispatch.sh` as out of scope ("no deploy-scope script files detected"). The dispatcher was shipped by `aws s3 cp --sse AES256` (the FB-j-3 / FB-j-7 route), served ETag 165933f6 = repo md5, new VersionId fzd8_e.BSTe4C757WgGhHx88DBf.v0iy; base VersionId .bNYVetB5sGV8bZki7EgXBfChCH_uPyE.
