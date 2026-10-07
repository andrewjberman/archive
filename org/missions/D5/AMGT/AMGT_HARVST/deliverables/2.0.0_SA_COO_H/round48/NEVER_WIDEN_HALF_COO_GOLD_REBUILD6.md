# NEVER-WIDEN -- COO HALF: HARVST served gold rebuild #6 -- the stored `url` joins the gold mention rows (HVST-au-3)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-06 ~05:2xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Why:** round-47 analysis @acc5c6e750, enrichment item 3. `2.0.0_SA_COO~Z` sent the ask in msg 29872: AMGT_RESAPP.TO-AMGT-au-3
(@69c017d520) adds the nullable `url` to `GOLD_MENTION_SCHEMA`, and aw-5 (@9d2b7b3d7c) widens `article_url` to the stored ft and
wsj top-level url. The served gold has no `url` column yet, so RESAPP FWD-4's links appear only after this build. The rebuild-#5
pair is spent, so this is a NEW pair.

## WHAT THIS HALF SIGNS: A RULE, NOT A DIGEST

This half signs the RULE, the BLAST RADIUS and the ROLLBACK. The act enforces the rule twice: on a fresh dry run before the
write, and on the parts actually written after it.

**THE RULE** (`round48/au-3.signing.py` before the write, `round48/au-3.act.py` VERIFY after it; the gold builders' own code,
from CLOUD HEAD; universe `round33/securities.universe.r33.json`, 212, the same as every served build so far):
- **`article_security_mention`:** 0 served rows GONE. Every built row carries `url`, equal to
  `publication_gold.article_url` of that article's stored silver row (null where silver has none). That function reads stored
  silver only; **no publisher host is fetched**. A served row CHANGED on a pre-existing field is allowed only in class:
  - **(c) HASH-ONLY:** `record_hash` is the ONLY changed field, and the built value equals the `record_hash` of that article's
    CURRENT stored silver row. Silver was re-written by round 45's re-derivation (ar-1) and round 47's column union (at-4), so
    no content field moves. Any other changed field is BROKEN.
- **`chatter_daily`:** 0 rows GONE, and every CHANGED row is EXPLAINED by one of three classes:
  - (a) its security gained an added mention;
  - (b) as-of-day COVERAGE-ONLY, under the four bounds of CTO half @b69262724d;
  - **(d) PAST-DAY COVERAGE-ONLY:** bounds 2-4 of that half hold (only `data_status` / `publishers_covered` /
    `publishers_covered_codes` change; each grows or holds; no mention gained), with bound 1 (the as-of day) lifted, because the
    collection run's backfill jobs now cover past days.
  OTHER must be 0.

**Measured at signing.** Dry run 3, 04:41Z-05:18Z, PUTS SENT 0; record `round48/au-3.signing.json`, out `round48/au-3.signing.out`.
- **mention:** served 31,042 -> built 33,665. Gone 0; added 2,623; changed (pre-existing fields) 5,363, ALL class (c),
  unexplained 0.
  - Changed field census: `record_hash` 5,363, nothing else. By publisher: barrons 596, bbg 3,078, ft 896, wsj 793.
- **url:** 33,665 rows; missing 0; url != article_url(silver) 0. With a url, by publisher:
  - barrons 712/712, bbg 5,102/5,102, sa 26,041/26,041;
  - ft 30/930, wsj 34/880 (only stored top-level urls; nothing fetched).
- **daily:** served 58,512 -> built 59,148. Gone 0; added 636; changed 28,628 = (a) 28,070 + (b) 0 + (d) 558; OTHER 0.
  - The (d) rows are 9433_JP 276 and AIZ_US 276, plus CICHY, PBR, RIO, ST_SP, WALMEX* and GPN 1 each. Each one only grows
    coverage (dry run 2's shape census: as_of False, coverage fields only True, grows True on all 558).
  - Dry run 1 (BROKEN under the rebuild-#5 rule) is what found classes (c) and (d). Read from the producer's own rule,
    never predicted.
- **RULE (rebuild #6): HOLDS.**

**Writers of the two tables (N = 1):** only `lib.research.harvest.publication_gold` writes them (`write_gold`, never-overwrite
conditional put plus read-back). Its `build-mention` / `build-daily` CLI is the act. No scheduled producer runs it, so no
override path is created.

## BLAST RADIUS

- **Written:** exactly 2 new parts, `amgt/harvest/gold/article_security_mention/date=<as-of>/part-<stamp>.parquet` and
  `amgt/harvest/gold/chatter_daily/date=<as-of>/part-<stamp>.parquet`. Nothing else is written, deleted or overwritten.
- **Readers of the newest mention part** (RESAPP's routes and the timeline) see the NEW `url` field on every row, the added rows,
  and the new `record_hash` on 5,363 rows. A reader that ignores unknown fields is unaffected.
- **Readers of the newest daily part** see the added-mention moves and 558 past-day coverage-only moves.
- **Scope in time:** ONE act (rebuild #6), at most 24 h after signing. A second rebuild needs a new dry run and this seat's
  re-sign.
- **NEVER-2:** a ledger entry is opened at the start of the act and closed at completion.

## BOTH BRANCHES

- **The rule holds before AND after the write:** done. `round48/au-3.act_<stamp>.json` names the two parts, the before and after
  digests, and the verify verdict. COO~Z is told the build stamp.
- **The rule fails BEFORE the write:** STOP; nothing is written.
- **The rule fails on the WRITTEN parts:** ROLLBACK. The BEFORE snapshot rows are written back as a newer part of each table
  through `pg.write_gold` (never-overwrite, newer stamp), so readers see BEFORE again. The rollback mention rows carry `url` as
  null, so equality is measured on the pre-existing field set. Nothing is deleted.

## EXCLUDED

No other table, no bronze or silver write, no publisher host fetched, no collection leg resumed (row Z-S89 stands), no deploy, no
portal change.

## VERDICT: SIGNED (COO), pending the CTO half
