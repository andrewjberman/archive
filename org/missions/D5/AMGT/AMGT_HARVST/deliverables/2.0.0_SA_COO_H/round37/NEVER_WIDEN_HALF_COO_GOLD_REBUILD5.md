# NEVER-WIDEN -- COO HALF: HARVST served gold rebuild #5 -- `title` + `published_precision` join the gold mention rows (track C step 1)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-02 ~15:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed; CTO msg 28509 / 28525
condition 3).
**Why:** CTO track-C ruling (msg 28509; RESAPP r62 addendum @40e1d622aa) puts the timeline headline in gold, so the RESAPP
day route (round 63) reads gold and no silver at request time. The cells are aj-7 (builder, merged @385f4a76cc) and
aj-8 (barrons dict titles, merged @2268853761; 149 rows re-derived). The round-32 pair's 4 rebuilds are spent, so this
is a NEW pair.

## WHAT THIS HALF SIGNS: A RULE, NOT A DIGEST

The sa and bbg backfills keep landing silver, so an exact digest cannot be fixed in advance. This half signs the RULE,
the BLAST RADIUS and the ROLLBACK. The act enforces the rule twice: before writing, on a fresh dry run, and after
writing, on the parts actually written.

**THE RULE** (`round37/gold_rebuild5.signing.py` before the write, `round37/gold_rebuild5.act.py` VERIFY after it; the
gold builders' own code):
- **`article_security_mention`:**
  - 0 served rows GONE;
  - 0 CHANGED on the PRE-EXISTING field set (the two added fields alone never count);
  - rows otherwise only ADDED;
  - EVERY row carries `title` (VERBATIM against the silver article, null where silver has none, never "") and
    `published_precision` (equal to silver's).
- **`chatter_daily`:** 0 rows GONE, and every CHANGED row is EXPLAINED by one of two classes:
  - (a) its security gained an added mention, which moves its rolling sums and counts (the round-32 class);
  - (b) **COVERAGE-ONLY:** the row is the as-of day, and its changed fields are a subset of {`data_status`,
    `publishers_covered`, `publishers_covered_codes`}.
  OTHER must be 0.
- **Class (b), measured.** Dry run 1 (15:1xZ) found 6 such rows (CICHY, CNI, IBN, ICICIBC, ST_SP, WALMEX* on
  2026-10-02). `round37/gold_rebuild5_other6_diff.json` diffs them field by field. All 6 move only DENIED -> PARTIAL,
  publishers_covered 0 -> 1, and codes [] -> ['barrons']. Today's barrons backfill covered those securities after
  rebuild #4 (06:03Z) and found 0 articles. 0 mention rows were added or gone for them. Read from the producer's own
  rule (`build_daily`'s coverage fields), never predicted.

**Measured at signing (dry run 2, 15:53Z, PUTS SENT 0; record `round37/gold_rebuild5_signing.json`):**
- mention: served 14,375 -> built 22,510; gone 0; changed (pre-existing fields) 0; added 8,135.
- The new fields: 22,510 rows, 0 missing a field, 0 title not verbatim, 0 precision mismatch, 22,510 titled.
- daily: served 58,300 -> built 58,300; gone 0; added 0; changed 32,556 (32,550 by added mention on 186 securities, 6
  coverage-only, OTHER 0).
- RULE (rebuild #5): HOLDS.

**Writers of the two tables (N = 1):** only `lib.research.harvest.publication_gold` writes them (`write_gold`, the
never-overwrite conditional put plus read-back), and its `build-mention` / `build-daily` CLI is the act. No scheduled
producer runs it, so no override path is created. The schema change (two appended nullable mention fields) is the
builder's own, merged @385f4a76cc.

## BLAST RADIUS

- **Written:** exactly 2 new parts, `amgt/harvest/gold/article_security_mention/date=<as-of>/part-<stamp>.parquet` and
  `amgt/harvest/gold/chatter_daily/date=<as-of>/part-<stamp>.parquet`. Nothing else is written; nothing is deleted or
  overwritten.
- **Readers of the newest mention part** (RESAPP's routes over HARVST gold, the timeline reads) see two NEW fields on
  every row, plus the added rows. A reader that ignores unknown fields is unaffected. The day route switches to
  `title` in RESAPP round 63, after this act.
- **Readers of the newest daily part** see the added-mention moves and the 6 coverage-only moves above.
- **Scope in time:** this half covers ONE act (rebuild #5), at most 24 h after signing. A second rebuild under this
  pair needs a new dry run and this seat's re-sign.

## BOTH BRANCHES

- **The rule holds before AND after the write:** done. The act record `round37/gold_rebuild5_act_<stamp>.json` names the
  two parts, the before and after digests, and the verify verdict.
- **The rule fails BEFORE the write:** STOP; nothing is written.
- **The rule fails on the WRITTEN parts:** ROLLBACK. The BEFORE snapshot rows are written back as a newer part of each
  table through `pg.write_gold` (never-overwrite, newer stamp), so readers see BEFORE again. The mention rollback rows
  carry the two new fields as null, so rollback equality is measured on the pre-existing field set. Nothing is
  deleted.

## EXCLUDED

No other table, no bronze write, no further silver write (the 149 barrons rows were re-derived under aj-8, before this
half), no quarantine change, no deploy, no portal change.

## VERDICT: SIGNED (COO), pending the CTO half
