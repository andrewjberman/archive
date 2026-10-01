# NEVER-WIDEN -- COO HALF: the HARVST served gold rebuild over the round-32 depth (`article_security_mention` + `chatter_daily`)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-01 ~11:4xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Why now:** the page (DSGN bubble chart via RESAPP's monthly chatter route; RESAPP FWD-32 counts) reads only the
NEWEST gold parts; the round-32 depth (sa backfill, quarantine-clean) is in silver but not in gold. Andrew's bar
(FWD-14) and the Friday demo (placement section 1: walk 18:00-21:00 ET, PROD by 09:00 ET Friday).

## WHAT THIS HALF SIGNS: A RULE, NOT A DIGEST

The sa backfill runs while this is signed, so silver grows and an exact digest cannot be fixed in advance. This half signs
the RULE, the BLAST RADIUS and the ROLLBACK; the act enforces the rule twice (before writing, on a fresh serializing dry
run; after writing, on the parts actually written).

**THE RULE** (`round32/checks/gold_rebuild.signing.py`, the gold builders' own code through a capturing client):
- `article_security_mention`: 0 previously served rows GONE, 0 CHANGED; rows only ADDED.
- `chatter_daily`: 0 rows GONE; every CHANGED row is on a security that gained an added mention (OTHER = 0). A new
  mention moves that security's `cumulative_ytd` and rolling sums (`baseline_30d_sum`, `trailing_7d_sum`,
  `trailing_30d_sum`) on every later day, and the day's own counts where it lands: measured, those are the only
  changed field-sets. ADDED rows are the new as-of day.

**Measured at signing (11:3xZ, 0 puts):** mention served 379 -> built 4,646 (gone 0, changed 0, added 4,267); daily
served 52,143 -> built 52,334 (gone 0, added 191, changed 27,272, all on the 152 securities with new mentions, OTHER 0).
RULE HOLDS. Record: `round32/gold_rebuild_signing.json`.

**Writers of the two tables (N = 1):** only `lib.research.harvest.publication_gold` writes them (`write_gold`, the
never-overwrite conditional put + read-back); its `build-mention` / `build-daily` CLI is the act. No scheduled producer
runs it (the scheduled task is Disabled), so no override path is created.

## BLAST RADIUS

- Per rebuild: exactly 2 new parts, `amgt/harvest/gold/article_security_mention/date=<as-of>/part-<stamp>.parquet`
  and `amgt/harvest/gold/chatter_daily/date=<as-of>/part-<stamp>.parquet`. Nothing else is written; nothing is
  deleted or overwritten.
- Readers of the newest part (RESAPP's routes over HARVST gold, the timeline reads) see the new rows.
- **Scope in time:** this half covers up to FOUR rebuilds under the same rule between signing and 2026-10-02 13:00Z
  (09:00 ET Friday), so the depth the backfill reaches can be served before the walk and again before PROD; each act
  is gated by the rule independently.

## BOTH BRANCHES

- **The rule holds before AND after the write:** done; the act record `round32/gold_rebuild_act_<stamp>.json` names
  the two parts and both digests.
- **The rule fails BEFORE the write:** STOP, nothing written.
- **The rule fails on the WRITTEN parts:** ROLLBACK -- the BEFORE snapshot rows are written back as a newer part of each
  table through `pg.write_gold` (never-overwrite, newer stamp), so readers see BEFORE again; the act record carries the
  digest-equality check of the rollback. Nothing is deleted.

## EXCLUDED

No other table, no silver or bronze write, no quarantine change, no deploy, no portal change.

## VERDICT: SIGNED (COO), pending the CTO half
