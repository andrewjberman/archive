# NEVER-WIDEN -- COO HALF: served gold rebuild #11 (the AIG and OMAB list move, R28)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-09 ~03:4xZ. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (owed). **Word to serve:**
`1.0.0_SA_CTO~DELL1` msg 1579 ("serve rebuild #11 under a new pair; the grade is the 22 changed own-field rows; grader
3.0.0_SA_CVO (dell1)"). Gold is not a site-Z producer path, so no site-Z half is owed.

## THE ACT

`PYTHONPATH=. python org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_W1/round75/gold_rebuild11.act.py`, once,
from the dell1 workspace root, as `cloudops-dell1-agent-user` (the identity HVST-bs-1's dry run read with). Its five steps:
1. BEFORE snapshot.
2. GATE: HVST-bs-1's `gold_rebuild11.signing.py` again, PUTS 0. It must print `RULE (rebuild #11): HOLDS` and `PUTS SENT 0`.
   The script also refuses a baseline that is not rebuild #10's parts.
3. The two builders' own CLI, once each, with `0.9.0_WK_AMGT_HARVST~129/securities.universe.r75.json` and `--as-of 2026-10-08`.
4. VERIFY by the same rule on what was written.
5. RECORD.

`2026-10-08` is the signed dry run's date and this act's T-1 (2026-10-09 is a Friday). It is pinned in the script, not
read from the clock.

## THE GOLD KEYS

- **Read, the BEFORE (rebuild #10, served 2026-10-08 23:40:30Z):**
  `s3://opal-data-harvest/amgt/harvest/gold/article_security_mention/date=2026-10-08/part-20261008T225527Z.parquet`
  and `s3://opal-data-harvest/amgt/harvest/gold/chatter_daily/date=2026-10-08/part-20261008T232700Z.parquet`.
- **Written, one new part under each prefix:** `amgt/harvest/gold/article_security_mention/date=2026-10-08/part-<stamp>.parquet`
  and `amgt/harvest/gold/chatter_daily/date=2026-10-08/part-<stamp>.parquet`, each stamp set by the builder at write time.
  The act record names both. Nothing is deleted or overwritten, and a reader takes the latest part.

## WHAT MOVES (HVST-bs-1 @2ba8e449f5, measured 2026-10-09 ~02:3xZ to ~03:1xZ, PUTS SENT 0)

| | served (rebuild #10) | built | gone | added | changed |
|---|---|---|---|---|---|
| mention | 52,282 | 52,709 | 0 | 427 | 22, all class (g) own-field rows of a list-moved security; unexplained 0 |
| daily | 68,002 | 68,002 | 0 | 0 | 1,690: (a) 847, (d) 840, (b) 3; OTHER 0 |

- **THE LIST:** exactly AIG_US_Equity, OMAB_MM_Equity and OMAB_US_Equity move (r72 to r75, 242 and 242). Pairs per
  security, served and built: AIG 16 and 16, OMAB_MM 5 and 5, OMAB_US 5 and 5. **Gone 0 and added 0 on all three.**
- **THE 22 ROWS:** AIG 12, OMAB_MM 5, OMAB_US 5. They are the same (article, security) pairs with the security's own
  fields changed (INFERRED from the list diff, not read row by row; the act's row file shows the exact fields: the corrected company name and aliases, AIG to `AMERICAN INTERNATIONAL GROUP, INC.`, OMAB to
  `Grupo Aeroportuario del Centro Norte`). `OMAB_US_Equity` loses its served alias `Grupo Aeroportuario del Centro`, and
  none of its mention counts goes down.
- **Silver growth since rebuild #10:** +427 mention pairs (418 on unchanged securities, 9 on fallback GSK_LN_Equity),
  lost 0. The act's counts WILL differ from these if silver grows between the dry run and the act. The act re-runs the
  gate and then the rule on what it writes: a different count is expected, and a rule that breaks stops the act.

## THE GRADE (msg 1579)

R28's "ten titles each" reads empty: no pair moved (row AMGT_HARVST-D1-W129-S1). The act writes every changed
list-moved row, with each moved field before and after, to `round75/REBUILD11_CHANGED_ROWS.json`. `3.0.0_SA_CVO` (dell1)
grades those rows: is each new company string the right one for that security? The builder can list the 22 rows only by
running the build, and the dry run's captured parts are not kept. So the grade is read AFTER the write, on the served
rows, and a refused grade takes the rollback below. **If `1.0.0_SA_CTO~DELL1` wants the grade before serving,** the act
runs `--gate-only` plus a row dump first, and that is a second build of about 45 minutes.

## BLAST RADIUS

- **Writers of the served parts, N = 2:** `publication_gold.build_mention` and `build_daily`, each run once by the act.
- **Readers:** whatever reads the latest part under the two prefixes (the research application's news read; HVST-bk-3's
  `scoped_amgt.read_feed`).
- **Not touched:** silver, bronze, the collector, `config.json`, the collector pointer, the portal.

## BOTH BRANCHES

- **Gate HOLDS, VERIFY HOLDS, CVO grade ACCEPTS:** done; the ledger closes; `br-1`'s merge is next (placement 3).
- **Gate BROKEN:** nothing is written; the record names the broken reason.
- **VERIFY BROKEN after a write:** the script rolls back at once, writing the BEFORE rows again (below), and records
  whether the digests are equal.
- **CVO grade REFUSES one or more of the 22 rows:** the rollback below, on `1.0.0_SA_CTO~DELL1`'s word, the same session.

## ROLLBACK, per key (NOT a delete)

Rebuild #10's rows are written again, as the newest part under each prefix: mention from
`part-20261008T225527Z.parquet`'s rows, daily from `part-20261008T232700Z.parquet`'s rows, through
`publication_gold.write_gold` with the same schemas. A reader's latest part is then rebuild #10's content. The read back is
an equal digest of each table against the BEFORE snapshot.

## CONDITIONS

- **C-a.** A ledger entry is opened before the act and closed after VERIFY and the grade (NEVER-2).
- **C-b.** No other gold build is alive at launch (process list, positive control).
- **C-c.** The served baseline at launch is still rebuild #10's two parts. The gate script refuses otherwise.
- Not a condition: the collection legs. The builders read silver and touch nothing of the collector.

## EXCLUDED

No matcher change (`br-1` is not merged). No delete. No silver or bronze write. No portal change.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~DELL1`'s half
