# NEVER-WIDEN -- COO HALF: rebuild the served `article_security_mention` gold (`HVST-p-1`)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~06:3xZ (02:3x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).

**Rule at signing:** CLOUD `7f782796a4`; the harvest libs are unchanged since `b635dadc66`.
- `publication_gold.build_mention`: `_iter_latest_articles` (every source's silver `article` through `store.silver_latest`,
  with `o-3`'s tie-break), then `mention_rows` per security, then `write_gold`.

**Round-25 ruling 1, all three named:**
1. **The command that reaches the put:**
   `python -m lib.research.harvest.publication_gold build-mention --securities-json org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json --as-of <UTC date of the act>`.
   It runs `main` -> `build_mention` -> `write_gold`, which makes ONE `put_object` of
   `amgt/harvest/gold/article_security_mention/date=<as-of>/part-<stamp>.parquet` (`IfNoneMatch`), then one `head_object`
   read-back.
2. **Config defaults the argv leaves unset:**
   - `WEIGHTS` A 1.0 / B 0.6 / C 0.3 / D 0.1, `DEFAULT_SHARE_B` 0.3 and `DEFAULT_ROUNDUP_AT` 5 (module constants, no CLI
     override);
   - the run stamp is `store.stamp(now)`;
   - the securities are the file named.
3. **Stub put-count dry run:** `round26/checks/p-1.signing.py --signing` runs `build_mention` ITSELF against a pass-through
   client that captures the put. It captured **exactly 1 put**, and the captured parquet is the expected write, saved to
   `round26/p1_signing_expected.json`.

## VERDICT: SIGNED

- **Blast radius:** ONE new gold part.
- **Existing pairs:** 304 of 304 KEPT byte-identical; 0 CHANGED, 0 GONE.
- **NEW pairs:** 54, served on `/timeline/day`.
- **Rollback:** forward only.

## 1. BEFORE STATE -- measured at signing

- `article_security_mention`: **6 parts**. The newest served snapshot holds 304 rows over 115 articles, and
  `mention_count` is null on 0.
- The per-part ETags are in `p1_signing_expected.json`. The act-start gate (`p-1.signing.py` without `--signing`) STOPS on any
  difference in the parts OR in the expected rows.

## 2. EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RUN

**One part, 358 rows.**

| measure | value |
|---|---|
| pairs KEPT, byte-identical | 304 |
| pairs CHANGED | 0 |
| pairs NEW | 54: sa 6, wsj 48 |
| pairs GONE | 0 |
| `mention_count` null in the write | 0 |
| Lenovo (`992_HK_Equity`) pairs | 32 -> 43 |
| articles read | 148 |
| tiers | A 80, B 84, C 98, D 96 |

- **The 6 sa pairs** come from `o-4`'s NEW rows.
- **The 48 wsj pairs** come from `o-5`'s 11 Lenovo articles. The articles name other covered companies too, so they carry
  co-mention pairs; each pair carries its own `mention_count`.
- **bbg adds 0 pairs.** `o-5`'s 11 bbg rows are EMPTY in silver (title `''`, 0 text blocks). This is row `Z-S44`: carried as a
  repair cell, not a hazard. A later mention rebuild after the fix adds them.

**Readers:**
- **`opal-amgt-scoped-api` `/timeline/day`** reads the newest mention snapshot to choose a day's articles, then silver for
  their headline. **USER-VISIBLE:** the days of the 54 NEW pairs gain article rows, each with its `mention_count`. That is
  the ANDREW-DIRECT @`8135566a29` outcome, on backend data.
- **`/timeline` series** reads `chatter_daily`, which is not rebuilt here, so the series does not move.
- **`build_daily` / `build_event`** read this table later (`HVST-p-3` signs after this drain).
- **The chatter producer** reads legacy (`CHATTER_AXIS_SOURCE=legacy`).
- **No scheduled writer** exists for this table.

### Failure branches

- **`PreconditionFailed`:** nothing is written and the prior part stays newest.
- **Read-back mismatch:** `HarvestStoreError`; the object is distrusted, and a further rebuild corrects it (a delete is a
  human word).
- **A written row outside the 358**, a pre-existing part moved, or a served row lacking a count: this FAILS `p-1.AC1.py` /
  `p-1.AC2.py`.

## 3. ROLLBACK

Forward only: readers take the newest snapshot, so a further rebuild supersedes. The prior 6 parts stay. Removing the new
part is an S3 delete, which is a human word.
