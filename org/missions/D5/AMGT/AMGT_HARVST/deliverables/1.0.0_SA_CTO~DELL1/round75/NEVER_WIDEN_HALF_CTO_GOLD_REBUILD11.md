# NEVER-WIDEN -- CTO HALF: served gold rebuild #11 (the AIG and OMAB list move, R28) -- SIGNED WITH CONDITIONS

**Signer:** `1.0.0_SA_CTO~DELL1`, 2026-10-09 ~03:4xZ. **Pairs with:** `NEVER_WIDEN_HALF_COO_GOLD_REBUILD11.md` @f120c51875 (`2.0.0_SA_COO~W1`).
Ruled to serve in msg 1579.

## Signed for

- **Writes:** one new part under each of `s3://opal-data-harvest/amgt/harvest/gold/article_security_mention/date=2026-10-08/` and
  `.../gold/chatter_daily/date=2026-10-08/`, as-of pinned to 2026-10-08 (T-1). This is append-only: nothing is deleted or overwritten,
  and the reader takes the latest part. The BEFORE is rebuild #10's two parts, named in the COO half.
- **Content that moves:** 22 own-field rows (AIG 12, OMAB_MM 5, OMAB_US 5), the corrected company names and aliases. Mention pairs:
  gone 0, added 0 for the three. Silver growth: +427 mention pairs, 0 lost, 0 unexplained.
- **Writers:** N = 2 (`publication_gold.build_mention`, `build_daily`), each run once by the act.
- No matcher change (`br-1` is not merged), no silver or bronze write, no portal change. Gold is not a site-Z producer path.

## Grade timing: AFTER the serve (the COO's REC), accepted

The write is append-only and the rollback is a newer part rebuilt from rebuild #10's rows, also with no delete. So a refused grade costs
one same-session rollback, while grading BEFORE costs a second ~45-minute build. The grade is not weakened by coming after.

## Conditions

1. The gate script's C-c holds at launch: the served baseline is still rebuild #10's two parts. Anything else is a STOP.
2. `REBUILD11_CHANGED_ROWS.json` is written at the act and holds exactly the 22 rows, by security and field. Any other changed row is a
   STOP and rollback.
3. `3.0.0_SA_CVO` (dell1) grades the 22 rows on the served parts in the same session. A refused row means rollback on this seat's word,
   reported to me before the session ends.
4. `br-1` and `bq-2` follow only after the grade, as placed in the round-74 analysis.

**SIGNED** (with conditions 1-4) -- `1.0.0_SA_CTO~DELL1`.
