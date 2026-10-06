# NEVER-WIDEN -- COO HALF: HARVST served gold rebuild #7 -- ft and wsj links filled from the stored canonical address (HVST-av-2)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-06 ~07:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Why:** round-48 analysis @6d005e5261, ruling 1. HVST-av-1 (@a44bc80e9d) lets `publication_gold.article_url` read the ft and wsj
stored `html_meta["og:url"]`, and for wsj also `articleData.sourceUrl`, accepted on the publisher's own host only. The census
measured 185/185 ft and 463/463 wsj articles with a link. Nothing is constructed and no host is contacted (Andrew's FT hold
stands). The rebuild-#6 pair is spent, so this is a NEW pair.

## THE RULE (`round49/av-2.signing.py` before the write, `round49/av-2.act.py` VERIFY after it; builders' own code from CLOUD HEAD; universe `round33/securities.universe.r33.json`, 212)

It is the rebuild-#6 rule (COO @e512987397, CTO @0b26f965af), classes (a)-(d) unchanged, plus one class:
- **(e) URL-FILL:** a served mention row whose `url` changes must be `ft` or `wsj`, and must go from null to the value
  `article_url` reads from the stored silver row. Any other url change (another publisher, or a non-null url replaced) is BROKEN.
- Every built row still carries `url` equal to `article_url(silver)`.

## Measured at signing

Dry run 07:13Z-07:5xZ, PUTS SENT 0; record `round49/av-2.signing.json`, out `round49/av-2.signing.out`.
- **mention:** served 33,665 -> built 33,665. Gone 0, added 0, changed on pre-existing fields 0 (hash-only 0, unexplained 0).
- **url:** (e) fill **1,746** (ft 900, wsj 846); any other url move 0. With a url after the build:
  - barrons 712/712, bbg 5,102/5,102, sa 26,041/26,041 (unchanged);
  - **ft 930/930, wsj 880/880** (were 30 and 34).
  - url != article_url(silver): 0.
- **daily:** served 59,148 -> built 59,148. Gone 0, added 0, changed 0. The daily part is written identical (DELTA 0).
- **RULE (rebuild #7): HOLDS.**

**Writers of the two tables (N = 1):** only `lib.research.harvest.publication_gold` (`write_gold`, never-overwrite conditional put
plus read-back), through its `build-mention` / `build-daily` CLI. No scheduled producer runs it.

## BLAST RADIUS

- **Written:** exactly 2 new parts, `amgt/harvest/gold/article_security_mention/date=<as-of>/part-<stamp>.parquet` and
  `amgt/harvest/gold/chatter_daily/date=<as-of>/part-<stamp>.parquet` (the daily one identical in rows). Nothing is deleted or
  overwritten.
- **Readers of the newest mention part** (RESAPP's routes, FWD-4 links) see `url` set on 1,746 more ft/wsj rows. No other field
  or row moves.
- **Scope in time:** ONE act (rebuild #7), at most 24 h after signing. NEVER-2: a ledger entry is opened at the start and closed
  at completion.

## BOTH BRANCHES

- **The rule holds before AND after the write:** done. `round49/av-2.act_<stamp>.json` records it, and COO~Z is told the stamp.
- **The rule fails BEFORE the write:** STOP; nothing is written.
- **The rule fails on the WRITTEN parts:** ROLLBACK. The BEFORE rows are written back as a newer part of each table
  (`pg.write_gold`, never-overwrite), so readers see BEFORE again. Nothing is deleted.

## EXCLUDED

No other table, no bronze or silver write, no publisher host contacted, no collection leg resumed (row Z-S89 stands), no deploy,
no portal change.

## VERDICT: SIGNED (COO), pending the CTO half
