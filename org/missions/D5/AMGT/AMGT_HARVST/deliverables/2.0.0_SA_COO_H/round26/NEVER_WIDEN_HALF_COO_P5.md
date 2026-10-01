# NEVER-WIDEN -- COO HALF: one span-bearing Lenovo bbg/wsj run, its upload, and the coverage rebuild that reads it (`HVST-p-5`, `p-3` part (b))

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~07:5xZ (03:5x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Ruling served:** `ledger/CTO_RULING_ROUND26_P3_SPLIT_AND_FWD7_DENOMINATOR_20260930.md` s.2 (b): the run-record path's positive
arm, after (a) (drained @`c2b1a57ebd`).
**Vendor authority:** R-21 @`b390c36444`, on its mechanism: the collector script.
**Code pin:** harvest libs as of `2023d17e46`, the `p-2` merge; nothing in them has changed since. The act prints
`git diff --stat 2023d17e46 HEAD -- lib/opal_data_harvest lib/research/harvest` and STOPS on any line.

## ROUND-25 RULING 1 -- the put paths, the config defaults, the stub put-counts

| # | command (the one that reaches the put) | puts |
|---|---|---|
| 1 | `run --harvest-grammar --retrieval-mode backfill --floor 2026-01-01 --new-only --security-json <Lenovo> --publishers bbg wsj --max-jobs 2 --runtime-root <main>` | **exactly 1** S3 put, the run record (`worker._persist_run_record` -> `store.bronze_put("amgt","run_record", date=<start>, <run_id>.json)`, never-overwrite). Articles and listings queue to the local outbox (`harvest_raw_outbox`, `harvest_listing_outbox`); no S3. |
| 2 | `upload-harvest --max-objects 60 --retrieval-mode backfill --runtime-root <main>` | Per queued article: 1 bronze put (`put_article_bronze`) plus its silver row. Per listing page: 1 bronze put (unless a same-day object exists) plus silver `listing_hit` rows. Measured on `o-5`'s upload: 22 articles and 10 listings gave 27 bronze and 30 silver parts. |
| 3 | `build-daily --securities-json <universe> --as-of <act date>` | **exactly 1** put, `chatter_daily`. Stub-captured in `p-3`(a) (`p-3.signing.py`). |

**Stub evidence for put 1:** `lib/opal_data_harvest/test_o1_run_record_reach.py` exercises `_persist_run_record` on a stub
client (`o-1` AC1; the trunk suite passes). **For 2:** `o-5`'s act-3 receipt. **For 3:** the `p-3`(a) signing dry run.

**Config defaults the argv leaves unset** (`lib/opal_data_harvest/config.json`):
- `jobs_per_run` is 1, **overridden to 2**;
- `minimum_request_seconds` is 15 and `jitter_seconds` is 10;
- `max_listing_pages` is 25 per publisher, the ceiling;
- `SUCCESSFUL_RUN_STATUSES` (`publication_gold` ~:561) decides which jobs a span credits.

## VERDICT: SIGNED

- **Blast radius:**
  - 1 new run-record object;
  - new bronze and silver ONLY under the bbg and wsj harvest roots;
  - 1 new `chatter_daily` part.
- **Unmoved:** barrons, ft and sa gain nothing, and no pre-existing object moves.
- **Rollback:** forward only.

## 1. BEFORE -- measured at signing (`round26/p5_signing_before.json`)

| root | objects |
|---|---|
| bbg | 1006 |
| wsj | 84 |
| barrons (no-write) | 30 |
| ft (no-write) | 28 |
| sa (no-write) | 106 |
| `amgt` `run_record` | **0** |
| `chatter_daily` | 9 parts |

The outbox holds 0 pending rows. The act-start gate (`p-5.before.py`) STOPs on any difference or a pending row.

## 2. EXPECTED OUTCOME, READ FROM THE PRODUCERS' RULES, BOTH BRANCHES

- **Collection, Branch A (a job succeeds):**
  - the job's status is in `SUCCESSFUL_RUN_STATUSES`, including `no_new_articles`;
  - its run-record entry carries a `reached_span` (`o-1`) and `p-2`'s per-key outcomes;
  - ONE run record is persisted.
  - Lenovo's articles are mostly held already (`o-5`), so few new articles are expected. Listing pages are re-walked.
- **Collection, Branch B (a job refuses):** recorded and not retried. It contributes no span, and the record still persists.
- **Upload:** new objects under bbg and wsj only. Every pending bbg/wsj outbox row reads `uploaded`.
- **Rebuild:**
  - `run_records_read >= 1`. It was 0 in `p-3`(a).
  - Lenovo's coverage from the run records ALONE (`run_record_spans`, no listing hits) holds a span for each successful job.
  - The served Lenovo rows carry that publisher's code on the span's days.
  - Lenovo stays PARTIAL, because 2 of 5 publishers cover it. Other names' coverage is unchanged, except by any new listing
    hits this run brings.
  - RESOLVED stays 0 of 191, by the guard's rule. FWD-7's denominator is round 27's work.
- **Row `Z-S44` stands:** new bbg articles may be empty in silver. That is not this act's measure.

**Readers:** `/timeline` reads the newest `chatter_daily`, and `/timeline/day` reads silver for keys in the mention snapshot,
which is not rebuilt here. The chatter producer reads legacy. No scheduled writer exists.

## 3. ROLLBACK

Forward only. Every put is never-overwrite, and readers take the newest part. A delete is a human word.
