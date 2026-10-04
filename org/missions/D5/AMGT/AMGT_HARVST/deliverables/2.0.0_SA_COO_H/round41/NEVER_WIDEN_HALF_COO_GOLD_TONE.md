# NEVER-WIDEN -- COO HALF: the HARVST served gold tone rebuild (`article_security_mention` + `chatter_daily`, round 41 HVST-an-2)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-03 ~21:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Authority:** Andrew-direct ~20:3xZ card 2, "yes to all recommendations"
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261003_20xxZ_YES_TO_ALL_SEVEN_OPEN_CALL_RECS.md` @9fe6e6f111):
"run FinBERT scoring over the stored articles, and the event rebuild". Decomposition section 54. The scores are in
(HVST-an-1: 5 `article_sentiment` parts, 13,224 scored + 11 no-text markers, 0 errors; `round41/an-1.batch01-05.out`).

## WHAT THIS HALF SIGNS: A RULE, NOT A DIGEST

This half signs the RULE, the BLAST RADIUS and the ROLLBACK. The act (`round41/gold_tone.act.py`) enforces the rule
twice: on a fresh dry run through a capturing client before writing, and on the parts actually written.

**THE RULE** (`round41/gold_tone.signing.py`, the gold builders' own code through a capturing client):
- `article_security_mention`: 0 served rows GONE; 0 CHANGED on the PRE-EXISTING field set (the 4 `sentiment_*` fields
  alone never count); every built row carries the 4 fields; every row whose `sentiment_content_key` has a score carries
  that score's label and signed score (JOIN MISMATCH 0).
- `chatter_daily`: 0 rows GONE; every CHANGED row is EXPLAINED, either (a) its security gained an added mention, or
  (b) COVERAGE-ONLY on the as-of day (the rebuild-#5 bounds, CTO half @b69262724d). OTHER must be 0.

**Measured at signing (21:4xZ, 0 puts; `round41/gold_tone_signing.out` + `gold_tone_signing.json`):**
- scores read 13,224;
- mention served 23,691 -> built 31,042: gone 0, changed (pre-existing) 0, added 7,351;
- tone: 31,042 rows, all 4 fields present, all content-keyed and all scored, join mismatch 0;
  labels positive 12,117, negative 10,034, neutral 8,891; every publisher's rows labelled (barrons 637, bbg 3,133,
  ft 926, sa 25,519, wsj 827);
- daily served 58,300 -> built 58,512: gone 0, added 212 (the new as-of day), changed 27,594, all on securities with an
  added mention; coverage-only 0; OTHER 0.
RULE HOLDS.

**The 7,351 ADDED mention rows, named so the CTO half signs them knowingly.** They are articles already in silver and not
yet in gold: sa +7,043 (served 18,476 -> 25,519; the sa backfill finished 2026-10-03 04:46Z) and bbg +308 (2,825 -> 3,133).
barrons 637, ft 926 and wsj 827 are unchanged. The served mention part
was built 2026-10-02 16:51Z (restored byte-for-byte on Andrew's ~17:3xZ release). The builder always reads the newest
silver, so a tone rebuild through the builders' own CLI serves them too. No collection runs or ran for this act: 0
collectors, the Scheduled Task is Disabled, and STOP_FT is unchanged. A tone-only rebuild that served exactly the 23,691
rows would need new code outside the builders, which this half does not propose.

**Writers of the two tables (N = 1):** only `lib.research.harvest.publication_gold` writes them (`write_gold`, the
never-overwrite conditional put + read-back); its `build-mention` / `build-daily` CLI is the act. No scheduled producer
runs it.

## BLAST RADIUS

- Exactly 2 new parts, `amgt/harvest/gold/article_security_mention/date=<as-of>/part-<stamp>.parquet` and
  `amgt/harvest/gold/chatter_daily/date=<as-of>/part-<stamp>.parquet`. Nothing else is written; nothing is deleted or
  overwritten.
- Readers of the newest parts see the new rows and the 4 tone fields on every mention row. RESAPP's chatter route keeps
  serving `tone` null, because it does not read these fields yet (`rolling_windows.TONE_REASON`, c20fd8cc98).
- One act, once. A second run needs a new half.

## BOTH BRANCHES

- **The rule holds before AND after the write:** done. The act record `round41/gold_tone_act_<stamp>.json` names the
  two parts and both digests.
- **The rule fails BEFORE the write:** STOP, nothing written.
- **The rule fails on the WRITTEN parts:** ROLLBACK. The BEFORE rows of each table are written back as a newer part
  through `write_gold` (never-overwrite), so readers see BEFORE again. The act record carries the rollback's
  digest-equality check on the pre-existing field set. Nothing is deleted.

## EXCLUDED

No other table, no silver or bronze write, no collection, no deploy, no portal change. The window-tone table (FWD-17,
`chatter_window`) is NOT built by this act.

## VERDICT: SIGNED (COO), pending the CTO half
