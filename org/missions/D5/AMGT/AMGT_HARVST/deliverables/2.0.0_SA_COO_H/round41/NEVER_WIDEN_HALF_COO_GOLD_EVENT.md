# NEVER-WIDEN -- COO HALF: the HARVST served `chatter_event` rebuild (round 41 HVST-an-3)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-03 ~21:3xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Authority:** Andrew-direct ~20:3xZ card 2, "yes to all recommendations"
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261003_20xxZ_YES_TO_ALL_SEVEN_OPEN_CALL_RECS.md` @9fe6e6f111):
"run FinBERT scoring over the stored articles, and the event rebuild". Decomposition section 54.

## WHAT THIS HALF SIGNS: A RULE, NOT A DIGEST

The event rebuild runs AFTER the tone rebuild (HVST-an-2), whose mention snapshot it reads, so the exact event set cannot
be fixed here. This half signs the RULE, the BLAST RADIUS and the ROLLBACK. The act (`round41/gold_event.act.py`)
enforces the rule twice: on a fresh dry run through a capturing client before writing, and on the part actually written.
The written part's digest must also equal the dry run's.

**THE RULE** (`round41/gold_event.signing.py`, the builder's own `build_event` through a capturing client):
- built events > 0; every `event_id` unique;
- every event's `security_key` is in the universe file (`round33/securities.universe.r33.json`, 212 securities);
- every `article_keys` entry is a mention row of that security in the newest served mention snapshot (ORPHAN 0);
- `lead_article_key` is the first non-guarded entry of `article_keys` (the builder's own rule in `event_rows`: a member with
  `co_mention_count >= 4` never leads); `articles_total == len(article_keys)`;
- every `lead_headline` equals the silver headline of its lead article (HEADLINE MISMATCH 0).

**Measured at signing (dry run over the CURRENT served mention snapshot, 23,691 rows; 0 puts):** served 8 events on 6
securities -> built 438 events on 63 securities; duplicate ids 0, out of universe 0, orphan 0, lead rule 0, total
mismatch 0, headline mismatch 0, headline null 0. 4 of the 8 served event_ids are reproduced exactly. RULE HOLDS.
The 438 matches the HVST-ak-3 census's dry build (438). After the tone rebuild the mention
snapshot grows (dry run: 23,691 -> 31,042 rows), so the act's gate is expected to build MORE than 438 events. The rule,
not the count, is what is signed.

**Writers of `chatter_event` (N = 1):** only `lib.research.harvest.publication_gold.build_event` (`write_gold`,
never-overwrite conditional put + read-back). No scheduled producer runs it (the collector's Scheduled Task is Disabled).

## BLAST RADIUS

- Exactly 1 new part, `amgt/harvest/gold/chatter_event/date=2026-10-03/part-<stamp>.parquet`. Nothing else is written;
  nothing is deleted or overwritten.
- Readers of the newest event part (RESAPP's timeline route) see the rebuilt events instead of the 8. The served event set
  is REPLACED, not appended: 4 of the 8 served events are not reproduced by the current rule over the current mention.
  Those 4 were built 09-30 over a 9,521-row mention table.
- One act, once. A second run needs a new half.

## BOTH BRANCHES

- **The rule holds before AND after the write, and the written digest equals the dry run's:** done. The act record
  `round41/gold_event_act_<stamp>.json` names the part and both digests.
- **The rule fails BEFORE the write:** STOP, nothing written.
- **The rule fails on the WRITTEN part:** ROLLBACK. The 8 BEFORE rows are written back as a newer part through
  `write_gold` (never-overwrite), so readers see the 8 again. The act record carries the rollback's digest-equality
  check. Nothing is deleted.

## EXCLUDED

No other table, no silver or bronze write, no deploy, no portal change, no collection.

## VERDICT: SIGNED (COO), pending the CTO half
