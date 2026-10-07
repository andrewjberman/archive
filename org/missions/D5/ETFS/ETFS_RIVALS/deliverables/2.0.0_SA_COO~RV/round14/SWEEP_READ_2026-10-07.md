# ETFS_RIVALS round 14 -- the 2026-10-07 13:00Z sweep, read by 2.0.0_SA_COO~RV at ~13:1xZ

The proof round 14's deploy (pin 22844f744f, ledger `etfs-rivalfunds-r14` CLOSED @cc02eeac7d) was waiting on: the first
scheduled sweep after it. Read-only reads of live S3 (`opal-data-etfs`, rivalfunds); nothing was written.

Served page: `s3://opal-data-etfs/rivalfunds/etfs/platinum/page/date=2026-10-07/index.html`
(gateway: `/rivalfunds/2026-10-07`).

| Gate item (handoff 2026-10-07_0627Z, round-14 gate) | Read | Verdict |
|---|---|---|
| a1_refresh succeeds | New table objects at date=2026-10-07 written by the sweep: holding_contribution 13:00:55Z, buying_trend 13:01:40Z, input_census 13:02:25Z (each beside the 11:04Z-11:05Z object of the vehicle run). The publish step that followed records each as SKIPPED, "2 object(s) already at date=2026-10-07", which is the refresh having already landed | MET |
| The AI run is the scheduled one | manifest `a1_produced.research_hypotheses_run`: status OK, run_id 20261007T130226Z-ai, run_path "scheduled"; gold research_hypotheses date=2026-10-07 holds research_hypotheses-20261007T130226Z-ai.parquet | MET |
| ai_grounding.earlier 0 | manifest `ai_grounding`: earlier 0, served 25 (2026-10-06: earlier 24, served 0). The words "Grounded on an earlier build" appear 0 times in the page | MET |
| IDVZ Petrobras equals the panel | The IDVZ account says Petrobras "was the top thirty-day contributor at +0.97%" and "the top year-to-date contributor at +2.53%"; gold holding_contribution (13:00:55Z object) for IDVZ, Petroleo Brasileiro SA - Petrobras: R30 0.009707, YTD 0.025275 | MET |
| A SKIPPED_TIME is a row the same hour (Z-W1-S49) | No SKIPPED_TIME: the run's status is OK | n/a |

Page manifest: batch_id ai-2026-10-07-204ef465, status published, generated_at 2026-10-07T13:07:29Z, 13 of 13 funds,
index.html 1,286,540 B, audit.html 1,243,556 B, runtime etfs-rivalfunds-daily-lambda.

Not read here: the sweep's CloudWatch REPORT line and the attempt record; the other 24 accounts' figures against their
panels (the gate names the one Petrobras figure). Those are the CVO's to sample for RIV-ab-1 J1.
