# NEVER-WIDEN -- COO HALF: served gold rebuild #12 (R30, the capital-initial alias rule, served)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-09 ~09:4xZ. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (owed). **Word:**
`ledger/ROUND_ANALYSIS.round74.md` ADDENDUM (msg 1939: "the served act goes under its own pair") and ADDENDUM 2 (msg 2181:
"Cut the served pair naming both classes with counts and the total mention delta. Anything else is a STOP."). Gold is not a
site-Z path, so no site-Z half is owed.

## THE ACT

`PYTHONPATH=. python org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_W1/round75/gold_rebuild12.act.py`, once,
from the dell1 workspace root, as a DECLARED detached job (`.tools/detached-job.sh run`), so the reaper does not stop it.
The steps:
1. BEFORE: the script refuses unless the newest parts are rebuild #11's.
2. The two builders' own CLI, once each, with the r75 list and `--as-of 2026-10-08`.
3. VERIFY on the written rows, with both classes computed by br-1's classifier.
4. ROLLBACK on any break.
5. RECORD.

## THE GOLD KEYS

- **BEFORE (rebuild #11, served 2026-10-09):**
  `s3://opal-data-harvest/amgt/harvest/gold/article_security_mention/date=2026-10-08/part-20261009T045809Z.parquet` (52,709 rows)
  and `s3://opal-data-harvest/amgt/harvest/gold/chatter_daily/date=2026-10-08/part-20261009T061012Z.parquet` (68,002 rows).
- **Written:** one new part under each `date=2026-10-08` prefix, with stamps set by the builder and named in the act record.
  Nothing is deleted or overwritten.

## WHAT MOVES -- THE TWO SIGNED CLASSES (HVST-bs-5 @a7a06fbc3c, merged @c1f750dd0a; PUTS SENT 0)

| class | rows | mention delta |
|---|---|---|
| R30 REMOVAL: a served pair gone, which br-1's classifier counts under the pre-R30 rule and not under R30 | 285 over 16 securities (census 280 of 48,358) | 425 |
| R30-PARTIAL COUNT-DOWN: a kept pair whose own fields changed, which the classifier counts before > after > 0 | 113 (V 59, BKNG 14, ORA_FP 6, ORANY 6, ...) | 337 (V 234, BKNG 24, ORA 21, ORANY 21) |
| **total** | 398 | **762** |

- The rest of the diff: 744 co-mention changes (class f), all tied to the removals. Mention lost 0, added 0. Daily gone 0,
  changed 2,904 (class a), OTHER 0. The list does not move.
- Removals by security: CDNS 74, BKNG 73, V 40, ORA_FP 26, ORANY 26, MNST 12, GPN 11, AAPL 6, META 4, UBER 4, WDAY 3,
  WM 2, INTC 1, INTU 1, MU 1, NG/_LN 1.
- The act's counts MAY differ from these. r47 adds Seeking Alpha silver while it runs, so the build sees more articles. The
  act prints each class count and the delta beside the dry run's. Added pairs are reported and are not a rule reason. Only a
  row outside the two classes is a STOP.

## THE GRADE

After the serve, `3.0.0_SA_CVO` grades:
- the 30 removed pairs in `0.9.0_WK_AMGT_HARVST~131/REBUILD12_REMOVED_SAMPLE.md` (R30 (b): wrong pairs);
- about 20 count-downs across V, BKNG and ORA (ADDENDUM 2): is the lower count right for the article?

A refused grade means rollback, reported to the CTO.

## BLAST RADIUS

- **Writers of the served parts, N = 2:** `publication_gold.build_mention` and `build_daily`, each run once.
- **Readers:** the latest part under each prefix (the research application's news read; `scoped_amgt.read_feed`).
- **Not touched:** silver, bronze, the collector, the runner, `config.json`, the pointer.

## BOTH BRANCHES

- **VERIFY holds (only the two classes) and the grade accepts:** done; the ledger closes.
- **VERIFY breaks (any row outside the two classes, a lost pair, a daily OTHER, missing classifier input):** the script
  writes the BEFORE rows again at once and records whether the digests are equal.
- **The grade refuses:** the rollback below, on the CTO's word, the same session.

## ROLLBACK, per key (NOT a delete)

Rebuild #11's rows are written again as the newest part under each prefix, through `publication_gold.write_gold` with the
same schemas, and read back as an equal digest of each table.

## CONDITIONS

- **C-a.** A ledger entry is opened before the act and closed after VERIFY and the grade (NEVER-2).
- **C-b.** No other gold build is alive at launch (process list, positive control).
- **C-c.** The act runs as a declared detached job (the 08:08Z reap of bs-5's dry run is the reason).
- **C-d.** The served baseline at launch is rebuild #11's two parts. The script refuses otherwise.

## EXCLUDED

No list change. No collector or runner change. No delete. No silver or bronze write. No portal change.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~DELL1`'s half
