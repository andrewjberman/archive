# NEVER-WIDEN -- COO HALF: rebuild the served sa silver article table (`HVST-o-4`)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~05:0xZ (01:0x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).

**Rule at signing:** CLOUD at `3886894d16`:
- the `n-2` builder (`lib/opal_data_harvest/silver_from_bronze.article_rows`, which keeps sa's `links`, `type` and `meta`);
- the writer `store.silver_append`: skip a row whose `record_hash` equals the latest served row for its `article_key`,
  write one `part-<run_stamp>.parquet` per fetch date, never-overwrite;
- the readers after `o-3`'s tie-break (`store.supersedes`): an equal `fetched_at` goes to the later part's `run_stamp`.

**Measured by:** `round25/checks/o-4.signing.py --signing`, whose output is `round25/o4_signing_expected.json`. The rebuild is
`o4_common.rebuilt_rows` (`n-2`'s lineage rules). The expected write is `o4_common.expected_write`, which mirrors
`silver_append`'s own filter. **That output IS the expected diff.**

**Dispatch order:** after `HVST-o-5` completes. `o-5`'s pair holds the sa root as a no-write control, and this act writes
there.

## VERDICT: SIGNED

- **Blast radius:** THREE new silver parts, 11 rows, in ONE table (`seeking-alpha` silver `article`).
- **Unchanged:** every pre-existing part and every bronze object.
- **User-visible:** nothing on `/timeline` or `/timeline/day` (see section 3).
- **Rollback:** forward only.

## 1. THE ACT

Run ONCE by `0.9.0_WK_AMGT_HARVST~64`, from CLOUD code at or after `3886894d16`, with a fresh `run_stamp`
(`store.stamp(now)`), which sorts after every existing part:

```
rows = [row for _key, row in o4_common.rebuilt_rows()]
store.silver_append("seeking-alpha", "article", rows, ("article_key",), <fresh run_stamp>)
```

There is no other writer, no bronze write, no gold build, no vendor call and no deploy.

## 2. BEFORE STATE -- measured at signing

| what | count |
|---|---|
| sa silver `article` parts | 35 |
| sa bronze `article` objects | 52 |
| served record keys (`silver_latest` by `article_key`) | 46 |
| rows rebuilt | 52 (one per bronze object) |

The per-object ETags and the per-key `record_hash`es are in `o4_signing_expected.json`. The act-start gate
(`o-4.signing.py` without `--signing`) STOPS on any difference.

## 3. EXPECTED OUTCOME, READ FROM THE MERGED RULE

**11 rows are written: MOVED 5, NEW 6. Three new parts, one per fetch date: 2026-09-11 (6), 2026-09-23 (3), 2026-09-26 (2).**

| kind | article_key | fetch date | why |
|---|---|---|---|
| MOVED | `sa:4411320`, `sa:4411819`, `sa:4429803` | 09-23 | the rebuilt row gains `links`, `type` and `meta` (`n-2` AC2: the only differing columns) |
| MOVED | `sa:4640637`, `sa:4640871` | 09-26 | same |
| NEW | `sa:4934221`, `sa:4934799`, `sa:4941330`, `sa:4943384`, `sa:4943496`, `sa:4944152` | 09-11 | unlabelled `fullArticle` bronze objects with no served row. `retrieval_mode` is ASSUMED `backfill`; `fetched_at` and `run_stamp` come from the bronze key's stamp (`n-2`'s rule, printed as assumed) |

**After the act:**
- Served record keys go from 46 to 52.
- Each MOVED key serves its rebuilt row, because its `fetched_at` ties and the later part wins.
- The other 41 keys are unchanged.
- A re-run writes 0 rows.

**Readers:**
- **The `/timeline` and `/timeline/day` routes** (`opal-amgt-scoped-api`) read silver for article keys named in the served
  MENTION snapshot. They read only `article_key`, `fetched_at`, `title` and `published_precision`
  (`publication_gold._TIMELINE_SILVER_COLUMNS`, ~:894).
  - The MOVED rows differ only in `links`, `type` and `meta`, so the bodies do not move.
  - The NEW keys are not in the mention snapshot, so they are not served until a mention rebuild.
  - The deployed function still carries the pre-`o-3` reader, which keeps the first row on a tie. On these four
    columns the old and rebuilt rows are equal, so either reader gives the same body.
- **`build_mention`** reads all silver. It is not run by this act, and a later mention rebuild is its own pair.
- **No scheduled reader or writer** touches sa silver: the collector task is Disabled with 0 triggers, and
  `CHATTER_AXIS_SOURCE=legacy`.

### Failure branches

- A `PreconditionFailed` on a part name writes nothing for that date; the act STOPS and reports. The fresh stamp makes
  this effectively unreachable.
- Any written row outside the 11, any pre-existing part moved, or any bronze change fails `o-4.AC1.py`.
- A MOVED key not served as rebuilt, or any other key changing, fails `o-4.AC2.py`.

## 4. ROLLBACK

- Forward only. A further rebuild writes a newer part; readers take the newest `fetched_at`, then the later part.
- Deleting a part is an S3 delete, which is a human word.
- The three new part keys are named in the worker's report.
