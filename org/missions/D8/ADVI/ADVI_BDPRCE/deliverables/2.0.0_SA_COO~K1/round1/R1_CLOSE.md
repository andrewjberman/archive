# ADVI_BDPRCE -- ROUND 1 CLOSE PACKET (L7 drain, L8 task-order compile) -- 2.0.0_SA_COO~K1, 2026-10-13 ~15:2xZ, dell1

Round 1 = the FWD-1 thread (decomposition `decompositions/ADVI_BDPRCE_DECOMP.md` @6b1cacce5d; issuance @f75da01777, `fanout: 3 of 3 chains, cap 8`). All four orders are `LOCAL`, read-only against AWS; **nothing served moved**.
Push state: LOCAL on `box/dell1` (not pushed). This packet states what was measured; it does not grade FWD-1. The grade is the CTO's.

## 1. The cells

| cell | order | merge | slot | AC1 | AC2 (AC3) | issuer re-run |
|---|---|---|---|---|---|---|
| `BP-a-1` writers of the served T-1 price | `TO-BP-a-1` | @f565ce0410 | ~1 | `WRITERS record ok writers=6 unidentified=0 versions_read=665` | scope OK 6 changed | PASS, record read, no write verb in 18 calls |
| `BP-a-2` the trace instrument | `TO-BP-a-2` | @fead753225 | ~2 | `TRACE SELFTEST: OK 7 arms` | AC2 `TRACE record ok ... trades=4 match=true`; AC3 scope OK 5 | PASS; the only file write is `--out` |
| `BP-a-3` the served-versus-recomputed gap | `TO-BP-a-3` | @1a44a44918 | ~3 | `GAP record ok served=1657 equal=1148 explained=429 unexplained=64` | scope OK 9 | PASS; two rows re-read from the day's partition |
| `BP-a-4` the thread (join) | `TO-BP-a-4` | @ff308443a4 | ~4 (re-seated once) | `THREAD record ok ... trades=4 equal=true` | scope OK 9 | PASS; the served object re-opened (section 2) |

Amendments, all by the issuer, none graded by a gate limb (criteria and paths unchanged): `f3643b94f9` (row ids carry the D1 coordinate), `368aeb5029` (BP-a-4 admits the carry-forward chain shape and un-parks),
`de5e6840f2` (BP-a-4: a normal client entity, one served price for the asset). The first BP-a-4 record (a lot in the catch-all client `0`, where the asset also showed two served prices) was REJECTED by the issuer
and is kept in `THREAD_TRACE.md` as a rejected candidate. The finished seat could not be resumed (no transcript), so the slot was re-seated in the same worktree with its prior commits named as inherited state.

Hygiene at the drain: `py_compile` on the six committed `.py` files, OK; `round-close-check.py --project ADVI_BDPRCE --round 1` -> `verdict=MAY-CLOSE` (4 orders, 4 complete, 4 proofs structural OK).

## 2. The one real run: the thread, re-opened by the issuer

Served object `opal-data-49financial/advi/49financial/platinum/entities/clients/z08334146/detail.json`, VersionId `ZCjWpzPR1n2uZl849onevhS.pIvSQhVA` (LastModified 2026-10-13T05:39:47Z), `data_as_of` 2026-10-09.
- Entity key class `z0` (a normal client: 3 accounts, 110 open lots).
- Asset `EXXONMOBIL HOLDINGS CORP COM SHS`: 2 open lots, served `ticker` null, both lots `current_price` 168.94.
- `silver/transactions/2026-10-09.parquet`: 4 valid rows, 1 distinct `transaction_id` (745369343), median of `|market_value|/|units|` = 168.94. Recompute equals served.
- Canonical row for the date: `transaction_observed`, 168.94. Rule: `bd_price_update.py:327-344` (median), applied through the S_00 stage's writer per `WRITERS.json`.
- Account reference (sha256 first 12 hex): `420deb1a5526`; no raw account id in any committed file.

**What this does and does not show.** It shows one real served untickered lot whose price traces to a written rule and one trade id and recomputes equal. Four things stand beside it, each a row:
1. **Tie, inside the thread's own row (W4-S5/S6).** The daily `silver/prices/2026-10-09.parquet` reads this asset at 162.155 `carry_forward`; canonical reads 168.94 `transaction_observed`. The served lot took canonical. The instrument's default stable pick names the daily row, so it reports a mismatch on this asset; the worker traced canonical with a helper that calls the instrument's function unchanged. The brief's S33 reading was "latent, 0 of 11,108 decided by a tie"; this is a same-date source disagreement in a served row, and it is the CTO's to re-read.
2. **The lot's market value is not quantity x price (W4-S8).** 5,000.79 against 12,332.62: the cap's scaling (FWD-8). The price is unaffected.
3. **The asset is a listed common stock with a null served ticker (W4-S9).** The "no public ticker" condition as written selects it; the ticker mapping is a gap, and a genuinely unlisted holding is a better exemplar.
4. **One trade id on four rows (W4-S7)**, so the median over repeats equals the distinct value here. It is not a case that separates FWD-4's repeated-row weighting.

## 3. What the round measured (carried, not decided)

- **The fourth writer is identified (BP-a-1).** It is the S_00 gold stage: `build_canonical_prices_v2.py` (put at :660) auto-chaining `inject_scoped_overrides.py` (put at :253); 25 runs in 7 days, each 15-16 s pair is one run. The Lambda `bd-price-update` ran 7 times; the silver script `bd_price_update.py` has 0 runs.
  Three rule copies apply today; the Lambda's rank table has no `scoped_override` key (W1-S3).
- **The rule as written does not produce 509 of 1,657 served `transaction_observed` rows (BP-a-3).** The window is 2026-09-16..10-13 (1,657, not 1,610). EQUAL 1,148; multi-day window 197; other 232; unexplained 64; not recomputable 16; version at write 0.
  The "other" class is two rules found in code or by test: JOB 2's price-column-first median (169 rows, `bd_price_update.py:677-706`) and a post-hoc price-column median that excludes cash dividends (62 rows; chance agreement not excluded, so NOT an established cause).
  Cash-dividend rows (price 1.0, units equal to the cash amount) pull the T1 median to 1.0 on 19 of the 64 unexplained rows (W3-S4); BLACKROCK INC COM 2026-09-22 serves 1,073.16 against a recompute of 1.0 (re-read by the issuer).
  The brief's candidate cause "the file's state at write time" is NOT a cause: no version of any window-date partition reproduces any non-equal row.
- **The served detail objects are dated 2026-10-09 against a T-1 of 2026-10-12 (W4-S1), and 9 of 120 sampled normal objects are older still (W4-S10).**
- **61 of 586 sampled untickered lots carry a price that matches no canonical row on the as-of date (W4-S2).** The sample is 26 objects, not a census (W4-S4).

## 4. ARMED rows (7), each with its owner and the act that disarms it

All seven name `2.0.0_SA_COO~K1` as disarm owner. None can be disarmed in round 1: each disarm is a served-price or served-lot change, which moves only under Andrew's review of a named before/after list (FWD-7). So each is carried to the cell that disarms it.

| row | hazard (left alone) | disarm act | cell (PRD) | un-park |
|---|---|---|---|---|
| `D1-W2-S2` | daily path takes the median over repeated `transaction_id` (6,210 of 6,278 rows repeat) | de-duplicate before the median | C6 (FWD-4) | the one rule's home exists; Andrew's review per fix |
| `D1-W2-S4` | two readers of one rule: backfill de-duplicates, the daily path does not | one rule, imported by every writer | C5 build half (FWD-2) | `BP-a-1`'s writer list (done) |
| `D1-W1-S3` | the Lambda's rank copy lacks `scoped_override` | the Lambda imports the one rule | C5 build half (FWD-2) | same |
| `D1-W3-S3` | the rule as written reproduces 1,148 of 1,657 served rows; two other rules are live | a ruling on which rule is THE rule, then one home | C5 build half, C6 | CTO ruling at the round-1 analysis |
| `D1-W3-S4` | cash-dividend rows set a per-unit price of 1.0 and dominate the median | exclude non-trade rows from the median (a rule change, served) | C6 (new item) | CTO ruling; Andrew's review |
| `D1-W4-S2` | untickered lots priced off no canonical row on the as-of date | trace the 61-of-586 and fix its source | new item, after C5 | a census over all 3,509 objects first (read-only) |
| `D1-W4-S8` | served lot market value off quantity x price on 7 of 110 lots | the cap's per-lot UNVERIFIED (Andrew's ruling) | C4 (FWD-8) | C2's measure; Andrew's review |

The other 20 rows are OBSERVATION/INERT and are carried by the same record. The CVO's adjudication and channel compile have not run (adjudication rows 0, watermark absent); `LOCAL` risk needs no CVO grade.

## 5. Recommended enrichment list for round 2 (the CTO's analysis rules it)

1. **C1 exact-data switch** (Units and Cost Basis on in the qt4 template; the lot table): the longest-latency item, one scheduled export; reversible. Start first.
2. **A ruling on THE rule** (W3-S3 and W3-S4): which of the three rules live today (T1 as written, JOB 2 price-first, the price-column median that excludes dividends) is the producer's intent. Everything in C5 to C8 reads it.
3. **C5 build half**: the rule's home, and every writer (S_00 build, inject, the Lambda, the silver script) imports it or is retired.
4. **C6 / C7 / C8** under FWD-7 pairs, in that order, each with its named before/after list.
5. **C2 and C3** (measure and reader census), then **C4** (unit authority and UNVERIFIED).
6. **A read-only census** of the 61-of-586 and the ticker-mapping gap (W4-S2, W4-S9) over all 3,509 client objects, and a better thread exemplar (a genuinely unlisted holding).

-- 2.0.0_SA_COO~K1
