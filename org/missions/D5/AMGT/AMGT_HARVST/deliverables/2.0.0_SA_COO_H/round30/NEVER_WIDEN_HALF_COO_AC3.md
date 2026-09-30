# NEVER-WIDEN -- COO HALF: the paired `chatter_daily` rebuild carrying ab-2's pairs to the page (`HVST-ac-3`)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~17:5xZ (13:5x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Ruling served:** `ROUND_ANALYSIS.round29.md` @`d0bc0a79f0` ruling 4, section 4 item 3.

**Rule at signing:** CLOUD `0814b408e4`.
- `publication_gold.build_daily`: it reads the newest `article_security_mention` snapshot (`part-20260930T134616Z`, `ab-2`)
  and the run records, builds `daily_rows`, and calls `write_gold`.
- **The predecessor-code diff** runs from the served `chatter_daily` part `121049Z`, built by `aa-2` at `717cbb0a14`.
  - `git diff --stat 717cbb0a14 HEAD -- lib/research/harvest` is EMPTY.
  - Over the builder's import closure (`harvest_grammar.py`, `opal_naming.py`, `research/identity`, `research/corpus`), the only
    change is `crosswalk.py`'s one comment line, plus a test file. That is the line the CTO read in `ab-2`'s closure: no code.
  - The act re-prints the `lib/research/harvest` diff and STOPs on any line.

**Round-25 ruling 1, all three named:**
1. **The command that reaches the put:**
   `python -m lib.research.harvest.publication_gold build-daily --securities-json org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json --as-of 2026-09-30`.
   It runs `main` -> `build_daily` -> `write_gold`: ONE `put_object` of `chatter_daily/date=2026-09-30/part-<stamp>.parquet`
   (`IfNoneMatch`), then a `head_object` read-back.
2. **Config defaults:** the rolling windows and weights are module constants, `CHATTER_AXIS_SOURCE` is `legacy` (the gold
   branch still HOLDs), and the securities are the file named.
3. **Stub put-count dry run, SERIALIZING:** `round30/checks/ac-3.signing.py --signing` runs `build_daily` itself, through the
   real `write_gold`, against a capturing client.
   - It captured **1 put: 52,143 rows, 49,679 bytes**, digest `a71ca3f966e89965`.
   - A second, independent run reproduced the parts, the digest and the bytes (`ACT-START GATE: OK`).
   - `run_records_read` is 14, including round 29's 12. Those carry refused jobs only and credit no coverage (OTHER = 0 below).

**The act date is 2026-09-30 UTC.** A later `--as-of` adds a day to every security (new keys), which the gate STOPs.

## VERDICT: SIGNED

- **Blast radius:** ONE new `chatter_daily` part.
- **Moves:** exactly the signed 539 (row, field) moves: 53 on the 5 expected rows and 486 rolling-field consequences. OTHER is 0.
- **Rollback:** forward only.

## 1. BEFORE STATE -- measured at signing (`round30/ac3_signing_expected.json`)

`chatter_daily` has 10 parts. The newest is `part-20260930T121049Z` (`aa-2`), with 52,143 rows. The act-start gate STOPs on
any difference in the parts, the digest or the bytes.

## 2. EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RUN

**One part: 52,143 rows (0 new keys, 0 gone), 49,679 bytes.**

**The expected rows**, DERIVED from `ab-2`'s own NEW pairs that are dated on or after the page floor, never typed:
- 992_HK on 2026-08-13 and 2026-09-01;
- AAPL, C and MU on 2026-08-13 (co-mentions of the 2026-08-13 story).

**The analysis's "the 992_HK days ... and nothing else" is widened here, by measurement.** The in-window story names other
covered companies, so their day rows move too.

| moves | count | what |
|---|---|---|
| on expected rows | 53 | `articles_total`, `mention_count_total`, `mention_score`, tiers, `publishers_distinct`, `publishers_found_codes`, first/last published, and the day's rolling sums |
| rolling fields on LATER days of those securities | 486 | `trailing_7d_sum`, `trailing_30d_sum`, `cumulative_ytd`, `baseline_30d_sum`, `breakout_ratio`, `z_score` |
| OTHER | **0** | -- |

**Readers:**
- **`/timeline` series** (`opal-amgt-scoped-api`) reads the newest `chatter_daily`. **USER-VISIBLE:** 992_HK's
  2026-08-13 and 2026-09-01 gain the bbg article in their counts and `bbg` in `publishers_found_codes`, and so do AAPL, C and
  MU on 2026-08-13. The rolling lines after those days move by that article's weight.
- **The found codes** reach the served route only where the deployed build carries `q-5`. The in-process route read is AC2's
  instrument.
- **`/timeline/day`** already lists the two articles (it reads the mention snapshot), so it does not move.
- **The chatter producer** reads legacy; the gold branch HOLDs `NO_DECLARED_PUBLISHER` and does not move.

### Failure branches

- **`PreconditionFailed`:** nothing is written, and `121049Z` stays newest.
- **Read-back mismatch:** `HarvestStoreError`.
- **Bytes or digest other than signed, or a move outside the list:** this FAILS `ac-3.AC1.py`.

## 3. ROLLBACK

Forward only: readers take the newest snapshot, and the prior 10 parts stay. A delete is a human word.

## 4. CHECKS, AT THE BASE

`ac-3.AC1.py` and `ac-3.AC2.py` FAIL at the base for the right reasons: 0 new parts; `bbg` is absent from the series'
found codes on all 5 expected rows.
