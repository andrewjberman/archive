# CRPS-s-1 model-block census, round 17

Worker `0.9.0_WK_AMGT_CORPUS~1`, cut head `1d58fd0c2e`. Rows and evidence: `MODEL_BLOCK_CENSUS_ROUND17.json` (beside this file).

## Counts

- Population: 96 folders in the live research library, 96 resolved through `crosswalk/v1/2026-09-29.json`, 0 unresolved, 0 ambiguous
  (`lib.research.corpus.backlog.build(library_root())`, `folders_read` 96).
- Store read: `s3://opal-data-harvest/derived/model_block/` (the producer's `BUCKET`, `model_block_pull.py:74`), one paginated
  `list_objects_v2`, 618 objects, 99 distinct `<security_key>` prefixes, all 618 matching `<key>/<stamp>/model_block.json`.
- Present 95, absent 1.
- Absent: `6501_JP_Equity` (folder `Hitachi 6501 JP`), 0 objects under `derived/model_block/6501_JP_Equity/`.
- 4 prefixes in the store are not library folders (`6861_JP_Equity`, `CAT_US_Equity`, `CSL_AU_Equity`, `NVDA_US_Equity`): 95 + 4 = 99.
- Slash keys: the producer writes `security.replace(' ', '_')` (`model_block_pull.py:401`), NOT `slash_safe_key`, so the two slash names
  sit under a literal `/` prefix: `BP/_LN_Equity` (newest 20260925T200039Z) and `NG/_LN_Equity` (newest 20260925T200133Z). No `-SLASH-` key
  exists in the listing.

## Producer chain

Writer: `integrations/bloomberg/research/model_block_pull.py` (stage `pull` :550, stage `derive` :1117, derived key :1319).

Callers found (4), every one needs a caller to NAME the security:
1. CLI `main()` :1613-1628, `--securities` REQUIRED (:1616), at most 3 (:1621-1622), "no population default" (:29). Run by hand.
2. `pull_consumer.py:98-99` imports and calls `stage_pull` then `stage_derive` per SQS message `body['ticker']` (:82-83); started by hand
   (`--once` or drain to empty), never a service.
3. `infra/aws/lambda/research/pull_enqueue/lambda_function.py:100` sends `{ticker, security_key, requested_at}` to queue
   `opal-research-pull-requests`, reached by `POST /api/private/research/pull` (`api-gateway.tf:106`) or a direct lambda invoke.
4. `lib/research/api/scoped_amgt.py:4375-4380` the `refresh` route only DECLARES that carrier and enqueues nothing.

Triggers: none. Task Scheduler read (207 tasks, 5 matching name or action filter): none runs the producer or the consumer. The two
research tasks (`OpalResearch-ExecManagement`, `OpalResearch-FilingsAnalyzer`) run `management/batch.py` and `filings/batch.py`; the
daily Bloomberg task runs `run_daily_pull.py`; none contains `model_block` or `pull_consumer` (0 hits each). Registration and induction
code (`lib/research/corpus`, `lib/research/identity`) never calls the producer or blpapi.

`admits_new_registrations` = **false**. No caller derives its list from the current crosswalk or registrations; a name registered today
is pulled only by a manual act (the past legs, e.g. the 5 no-block names of 2026-09-25, were hand-run under change-management ledgers).

## The one exercising act for Hitachi

Who: the issuer's act under a never-widen pair (CTO + COO), executed by a cloud-ops seat on the Bloomberg box with the terminal
signed in (a vendor call plus a served write; this worker ran nothing). Open a `org/critical_paths/change_management/` entry first.

What, on demand, scripted and stopping at the first non-zero rc:

```
python integrations/bloomberg/research/model_block_pull.py pull   --securities "6501 JP Equity"
python integrations/bloomberg/research/model_block_pull.py derive --securities "6501 JP Equity"
```

The ticker string is the crosswalk row's `bloomberg_security` field, read in `crosswalk/v1/2026-09-29.json`: `6501 JP Equity` (HITACHI LTD).
Expected mint: `derived/model_block/6501_JP_Equity/<stamp>/model_block.json` in `opal-data-harvest`, plus raw stamps under
`bloomberg/harvest/bronze/{refdata,histdata,bestdata}/security_key=6501_JP_Equity/`. Then the census re-run should read 96 present, 0 absent.
Precedent: the rr-1 five-no-block-names ledger `20260925T2156Z_amgt-rr-1-five-no-block-names_deploy_completion.md` (pull, derive, landed and
served-page checks). Alternative route with the same effect: `POST /api/private/research/pull {"ticker": "6501 JP Equity"}` then
`python integrations/bloomberg/research/pull_consumer.py --once` on the box.

Not run here: a pull is a vendor call and a served write.
