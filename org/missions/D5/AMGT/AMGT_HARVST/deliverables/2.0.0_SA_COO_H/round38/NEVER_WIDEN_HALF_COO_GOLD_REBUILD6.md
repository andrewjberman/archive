# NEVER-WIDEN -- COO HALF: HARVST served gold rebuild #6 -- the ft QUARANTINE ALONE (STRICT)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-02 ~22:4xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed; CTO msgs 28715 ruling 3 and
28731).

**Why:** FT's terms, read verbatim (`4.0.0_SA_CRO~Z` @0fab00b8a0), bar automated reads, storing and ML use. The CTO ruled
that the stored ft articles are QUARANTINED: excluded from gold serving and every downstream use, with the bytes kept,
and deletion is Andrew's word. Then the CTO ruled (28731) that rebuild #6 carries the ft quarantine ALONE, because it
REDUCES exposure. The served event rebuild and any tone or window serving are HELD on Andrew's card
(`CARD_HARVST_PUBLISHER_TERMS_20261002.md` @8d20bc24c8). The cell is HVST-ak-4, merged @eff5c79d35 and graded at the
base.

## THE VARIANT THIS HALF SIGNS: STRICT (served minus ft; nothing added)

Two variants were dry-run on the round-33 universe (212 securities):
- **REBUILD from silver** (`round38/gold_rebuild6_signing.json`): the rule HOLDS, but the build also ADDS 3,633 mention
  rows (sa 3,325, bbg 308) collected since rebuild #5, plus 7,772 daily moves from them. That is new served output from
  publisher content, which "alone" does not cover.
- **STRICT** (`round38/gold_rebuild6_signing_strict.json`, `round38/gold_rebuild6_signing_strict.out`): the served mention
  snapshot minus the ft rows, and nothing added. **This half signs STRICT.** If the CTO half prefers REBUILD, it says so
  and names the 3,633 added rows; the act then needs this seat's re-sign.

**THE RULE** (`round38/gold_rebuild6.signing.py` with `HVST_R6_STRICT=1` before the write, and
`round38/gold_rebuild6.act.py` VERIFY after it):
- **`article_security_mention`:**
  - the written rows are exactly the BEFORE rows minus every quarantined (ft) row;
  - 0 extra rows, 0 missing rows, and 0 non-ft rows CHANGED on the pre-existing field set;
  - 0 ft rows;
  - every row carries `sentiment_finbert_label`, `sentiment_finbert_score` and `sentiment_scorer`, and every value is
    NULL. ak-1's schema is used; FWD-16 is HELD, so no score exists.
- **`chatter_daily`** (the builder's own `build-daily`, reading the mention part just written): 0 rows GONE, 0 ADDED,
  and every CHANGED row is inside the quarantine bounds (class q), with OTHER 0:
  - `publishers_enabled` moves 5 -> 4 (`GRADED_PUBLISHERS`: barrons, bbg, sa, wsj);
  - ft leaves `publishers_covered_codes` and `publishers_found_codes`, and no other code leaves;
  - `publishers_covered` = len(covered codes);
  - any other changed field is a count or status field of a security that had served ft rows, or (status only) the
    re-grade under the new denominator.

**Measured at signing (STRICT dry run, ~22:3xZ, PUTS SENT 0):**
- mention: served 23,691 (ft 926) -> 22,765 (ft 0); ft gone 926 of 926; non-ft gone 0; changed 0; added 0.
- tone: 0 rows missing a field; 0 rows with a value.
- daily: served 58,300 -> 58,300; gone 0; added 0; changed 58,300, all class q (publishers_enabled 5 -> 4 on every row);
  OTHER 0.
- data_status transitions: 1 PARTIAL -> DENIED, a day whose only covering publisher was ft. It is read from the
  builder's own grade, not predicted.
- RULE (rebuild #6): HOLDS.

**Writers of the two tables (N = 1):** only `lib.research.harvest.publication_gold.write_gold`, the never-overwrite
conditional put plus read-back. The act calls it once for mention and runs `build-daily` once. No scheduled producer
runs either, so no override path is created.

## BLAST RADIUS

- **Written:** exactly 2 new parts, `amgt/harvest/gold/article_security_mention/date=<as-of>/part-<stamp>.parquet` and
  `amgt/harvest/gold/chatter_daily/date=<as-of>/part-<stamp>.parquet`. Nothing else is written, and nothing is deleted
  or overwritten. The ft bronze and silver bytes are untouched.
- **Readers of the newest mention part** (RESAPP's timeline routes over HARVST gold): 926 ft rows disappear. Every other
  row is unchanged except for 3 new NULL fields; a reader that ignores unknown fields is unaffected.
- **Readers of the newest daily part:** every row reads `publishers_enabled` 4. ft leaves the coverage codes; ft-bearing
  securities' counts lose their ft contribution; 1 day re-grades PARTIAL -> DENIED.
- **Served events (`chatter_event`, 8 rows) are NOT rebuilt.** They carry 0 ft rows, as measured at the cut. Window and
  tone tables are not written.
- **Scope in time:** ONE act, at most 24 h after signing. A second act needs a new dry run and a re-sign.

## BOTH BRANCHES

- **The rule holds before AND after the write:** done. `round38/gold_rebuild6_act_<stamp>.json` names the two parts, the
  before and after digests, and the verify verdict.
- **The rule fails BEFORE the write** (the gate re-runs the STRICT dry run): STOP, and nothing is written.
- **The rule fails on the WRITTEN parts:** ROLLBACK. The BEFORE rows of both tables are written back as newer parts
  through `write_gold`, so readers see BEFORE again. The mention rollback rows carry the 3 tone fields as NULL under
  the current schema, so rollback equality is measured on the pre-existing field set. Nothing is deleted.

## EXCLUDED

No event, window or tone table; no silver or bronze write; no delete (the ft bytes stay, and deletion is Andrew's
word); no deploy; no portal change; no collection change (the pause stays readied, not flipped).

## VERDICT: SIGNED (COO, STRICT variant), pending the CTO half
