# NEVER-WIDEN -- COO HALF: rebuild the served `article_security_mention` gold so the 11 bbg story-id articles gain their pairs (`HVST-ab-2`)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~13:3xZ (09:3x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).

**Rule at signing:** CLOUD `123befacf8`.
- `publication_gold.build_mention`: `_iter_latest_articles` (every source's silver `article` through `store.silver_latest`),
  then `mention_rows` per security, then `write_gold`.
- **The predecessor-code diff** (standing ruling 3) runs from the served snapshot's code to HEAD. The served part is
  `062354Z`, written by `HVST-p-1` under the pair at `5b407d86a1` / `c698bf6ad0`.
  - `git diff 01e5499ae7 HEAD` over `publication_gold.py`, `store.py` and `harvest_grammar.py` (the builder's imports) is
    ONE change: `91b74a9047` (`q-5`).
  - That change appends `publishers_found_codes` to `GOLD_DAILY_SCHEMA` and `daily_rows`. It touches the DAILY builder only;
    `build_mention`, `mention_rows` and the mention schema are byte-unchanged.
  - Therefore the only input that moved is silver: `aa-3`'s 11 story-id rows (`part-20260930T114206Z`).

**Round-25 ruling 1, all three named:**
1. **The command that reaches the put:**
   `python -m lib.research.harvest.publication_gold build-mention --securities-json org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json --as-of <UTC date of the act>`.
   It runs `main` -> `build_mention` -> `write_gold`: ONE `put_object` of
   `amgt/harvest/gold/article_security_mention/date=<as-of>/part-<stamp>.parquet` (`IfNoneMatch`), then one `head_object`
   read-back.
2. **Config defaults the argv leaves unset:**
   - `WEIGHTS` A 1.0 / B 0.6 / C 0.3 / D 0.1, `DEFAULT_SHARE_B` 0.3 and `DEFAULT_ROUNDUP_AT` 5 (module constants);
   - the run stamp is `store.stamp(now)`;
   - the securities are the file named.
3. **Stub put-count dry run, SERIALIZING** (the `aa-3` lesson): `round29/checks/ab-2.signing.py --signing` runs
   `build_mention` itself, through the real `write_gold`, against a pass-through client that captures the put.
   - It captured **exactly 1 put: 379 rows, 44,376 bytes.**
   - A second, independent dry run reproduced the parts, the rows AND the bytes (`BEFORE == signing ... OK`).
   - The expected write is saved in `round29/ab2_signing_expected.json`.

## VERDICT: SIGNED

- **Blast radius:** ONE new gold part.
- **Existing pairs:** 358 of 358 KEPT byte-identical; 0 CHANGED, 0 GONE.
- **NEW pairs:** 21, all on the 11 story ids.
- **Rollback:** forward only.

## 1. BEFORE STATE -- measured at signing

- `article_security_mention` has **7 parts**. The newest served snapshot is `062354Z`: 358 rows, with `mention_count`
  null on 0.
- The per-part ETags are in `ab2_signing_expected.json`.
- The act-start gate (`ab-2.signing.py` without `--signing`) STOPS on any difference in the parts, the expected rows or
  the expected bytes.

## 2. EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RUN

**One part: 379 rows, 44,376 bytes.**

| measure | value |
|---|---|
| pairs KEPT, byte-identical | 358 |
| pairs CHANGED | 0 |
| pairs NEW | **21, all bbg; 0 outside the 11 story ids** |
| pairs GONE | 0 |
| story ids with at least 1 pair | 11 of 11 |
| pairs on the 11 hash-keyed EMPTY bbg rows | **0** (inert, per the CTO ruling @`803ea38a9e`) |
| `mention_count` null in the write | 0 |
| NEW pairs by security | 992_HK 11, AAPL 4, VZ 1, HSBA_LN 1, HSBC 1, DELL 1, C 1, MU 1 |
| Lenovo (`992_HK_Equity`) pairs | 43 -> 54 |
| articles read | 159 |
| tiers | A 90, B 89, C 98, D 102 |

**THE PAGE WINDOW -- stated, not predicted (row `Z-S46`):**
- 9 of the 11 story ids' 992_HK pairs are dated 2015-01-07..2019-05-23. Only 2 are inside the page window: 2026-08-13 and
  2026-09-01.
- `/timeline/day` first requires a `chatter_daily` row for the day, and 992_HK's rows begin at `BACKFILL_FLOOR`
  2026-01-01. So the route will list the **2** in-window pairs. The 9 pre-floor pairs are served in gold and reach no page
  day by design.
- AC2 requires the 2 and counts and names the 9.
- The cause is upstream, in collection: a backfill fetches dated pre-floor hits. It is fixed for new runs by
  `HVST-ab-1` AMENDMENT 1. The 9 existing pairs are kept, because gold is the pair store and a delete is a human word.

**Readers:**
- **`/timeline/day`** (`opal-amgt-scoped-api`) reads the newest mention snapshot to choose a day's articles, then silver for
  their headline. **USER-VISIBLE:** 2026-08-13 and 2026-09-01 on 992_HK gain a bbg article each with its
  `mention_count`, and so do the co-mentioned securities' in-window days.
- **The `/timeline` series** reads `chatter_daily`, which is NOT rebuilt here, so the series does not move.
- **`build_daily` / `build_event`** read this table on a later paired rebuild.
- **The chatter producer** reads legacy. **No scheduled writer** exists for this table.

### Failure branches

- **`PreconditionFailed`:** nothing is written, and `062354Z` stays newest.
- **Read-back mismatch:** `HarvestStoreError`; the object is distrusted, and a further rebuild corrects it (a delete is a
  human word).
- **A written row outside the 379**, a byte size other than 44,376, a pre-existing part moved, or a served pair on an empty
  row: this FAILS `ab-2.AC1.py` / `ab-2.AC2.py`.

## 3. ROLLBACK

Forward only: readers take the newest snapshot, so a further rebuild supersedes. The prior 7 parts stay. Removing the new
part is an S3 delete, which is a human word.

## 4. CHECKS, AT THE BASE

`ab-2.AC1.py` and `ab-2.AC2.py` FAIL at the base for the right reasons: 0 new parts; 358 != 379; 0 of 11 story ids served.
The inert limb already holds: 0 pairs on an empty row.
