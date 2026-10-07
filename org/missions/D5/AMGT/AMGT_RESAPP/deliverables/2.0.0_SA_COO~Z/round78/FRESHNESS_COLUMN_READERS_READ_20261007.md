# The freshness view's input columns: the table each READS against the table its collector WRITES today

`2.0.0_SA_COO~Z`, 2026-10-07 ~14:5xZ. Term 3 of CTO ruling msg 31034 on row `AMGT_RESAPP-Z-S367`, read before the round-78 cut.
Store reads only (`s3://opal-data-harvest`); no vendor call; nothing written. Covered names: 95 (`covered_security_keys()`).

## Two readers carry the same table sets

- `lib/research/freshness/build_view.py` (the hand-run view): `_BLOOMBERG_BRONZE_REQUESTS` 6 tables, `_SEEKING_ALPHA_BRONZE_TABLES`
  (symbol, report, analysis, news), `_BRIGHT_DATA_SERP_BRONZE_PREFIX`, and `packs/<key>/`.
- `lib/research/api/scoped_amgt.py`, the block near line 5425 to 5446 (the DEPLOYED reader behind `/freshness`): its own copies, the same six Bloomberg
  tables and the same four Seeking Alpha tables as frozensets, the same serp prefix, `PACKS_PREFIX`. It lists each prefix once
  and joins in memory. **A repair made in one of the two and not the other leaves the page wrong; the cell edits the served one.**

## Per column

| column | what the view reads | what is in the store today | verdict |
|---|---|---|---|
| **Bloomberg** | newest stamp across `bloomberg/harvest/bronze/{refdata, histdata, histdata_daily_px, bestdata, identity, exec_officers}/security_key=<key>/` | all six are written per security today: refdata 687 objects over 100 partitions (newest 13:13Z today), histdata 687 / 100, bestdata 645 / 99, exec_officers 93 / 91 (11:37Z today), identity 68 / 68 (13:22Z today), histdata_daily_px 2 / 2 (2026-09-22). The view's date is present on **95 of 95** covered names and reads **2026-10-07 on 95 of 95** | **SOUND.** It reads the tables the collector writes. One omission, harmless today: `segments` (87 objects, 85 partitions, new today) is a seventh per-security table the writer's `BRONZE_REQUESTS` holds and neither reader's set does. Three other tables under the same root are not per-security and are rightly not read: `article` (2,864, by article hash), `news_listing` (884, by date), `price_history_px_last` (4, by date) |
| **Seeking Alpha** | newest stamp across `seeking-alpha/harvest/bronze/{symbol, report, analysis, news}/security_key=<key>/` | those four tables hold **3 partitions** (BABA, BA, COST), 4 objects each, all 2026-09-11T04:0xZ: the September pilot. The collector writes `article/article_hash=<hash>/` (14,951 partitions, through 12:58Z today), `news_listing/date=<day>/` (8 days), and silver parquet by date | **STALE READER** (row Z-S367): 3 false stale, 92 false "not collected". 95 of 95 wrong |
| **Web search** | `bright-data/harvest/bronze/serp/security_key=<key>/` | the bucket has NO `bright-data/` prefix at all (24 top-level prefixes listed; that one is absent). The SERP writer is code-only and off (round-77 cell ba-12's read) | **TRUE "not collected"**, 0 of 95. The reader and the absent collector agree. But it is read from an EMPTY PARTITION, which is exactly what term 2 of the ruling forbids as evidence: it is right today by coincidence of nothing being written |
| **The research pack** | `packs/<key>/` (the newest object's time) | 105 folders; **95 of 95** covered names have one; the newest object per covered name is **2026-10-07 on 95 of 95**; the object is `input_ledger.json` (102 of them) | **SOUND** as a date. One oddity: 2 objects sit under a path segment named `_LN_Equity`, which is a slash name (`BP/`, `NG/`) written with its raw slash, so its "folder" is `BP` or `NG`. The same key-shape trap as row Z-S365, in a third place; whether the pack reader finds them was not traced |

## Collectors that write today and have NO column

The view has three vendor columns and the pack. These homes are written by live collectors and no column reads them:

| home | objects | newest write |
|---|---|---|
| `wsj/` | 1,940 | 2026-10-07T12:46Z |
| `barrons/` | 1,062 | 2026-10-07T04:46Z |
| `ft/` | 367 | 2026-10-05T02:00Z |
| `bloomberg/harvest/bronze/article/` | 2,864 | 2026-10-07T14:25Z |
| `social/`, `issuer-site/`, `publications/`, `publication-links/` | 1, 1, 7, 7 | September |

That is not a stale reader; it is a set of inputs the page does not state. Whether the freshness page should carry them is an
outcome question (FWD-7's text), not decided here.

## What the Seeking Alpha repair can read (terms 1 and 2 of the ruling), measured

- **The join exists, in silver.** `seeking-alpha/harvest/silver/article/date=<day>/part-*.parquet` carries `discovered_for`,
  `fetched_at`, `published_utc`, `article_key` and `bronze_key` per article (one file opened; those five column names read from it). The bronze article
  object carries only Seeking Alpha's own tag ids under `relationships.primaryTickers` (e.g. `{"id": "1202", "type": "tag"}`),
  not our key.
- **The deployed reader cannot open parquet.** `scoped_amgt.py` says in its own comment beside `_BLOOMBERG_BRONZE_REQUESTS` that the adapter "never gains
  ... pyarrow" (its build vendors exactly one non-pure wheel).
- **The collector's record of a finished job is device-local.** Row `AMGT_HARVST-Z-S100` cites
  `.runtime/opal-data-harvest-sa/run_records/` and `.runtime/harvest-backfill/r47_sa_checkpoint.json` on the collector's box.
  Nothing under `seeking-alpha/harvest/` is a state or job-record prefix (its two children are `bronze/` and `silver/`).
- **So the repair has two halves in two projects:** (1) the collector lands a small JSON record per finished job in the store,
  keyed by the pool key, saying when it finished, what span it reached and how many articles it stored (AMGT_HARVST's writer);
  (2) the freshness reader takes "last read" and "not collected" from that record (this project, the served reader in
  `scoped_amgt.py`, through a new module). Half 2 can be built and proved on fixtures before half 1 lands; the page is right only
  when both have.
- Until then the honest served state for the Seeking Alpha column is neither a pilot date nor "not collected". The reader cell's
  first act can be to stop serving the pilot objects as a last-read date.
