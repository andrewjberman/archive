# ADVI_BDPRCE -- ROUND 2 CLOSE PACKET (L7 drain, task-order compile) -- 2.0.0_SA_COO~K1, 2026-10-14 ~01:1xZ, dell1

Round 2 = build THE rule with no served write (decomposition v2 @e48e036784, issuance @73a2b77c3c, `fanout: 5 of 5 chains, cap 8`). All eight orders `LOCAL`; **nothing served moved.**
Push state: LOCAL on `box/dell1` (not pushed). This packet states what was measured; it grades no FWD. The grade is the CTO's.
`round-close-check.py --project ADVI_BDPRCE --round 2` -> `verdict=MAY-CLOSE` (8 orders, 7 complete, 1 superseded; proofs structural 7 of 7). Drain hygiene: `py_compile` on 19 committed `.py` files clean; `test_bd_price_rule.py` `OK 15 arms`.

## 1. The cells

| cell | merge | slot | criteria re-run by the issuer |
|---|---|---|---|
| `BP-b-4` the trace follows the served row | @a20f7a405f | ~8 | selftest 7 arms; probe `followed=canonical trades=4 match=true`; a live run on the probe inputs agreed |
| `BP-b-3` the lot census | @7cf9277743 | ~7 | `objects=3510 lots=198295 off_canonical=1859 listed_untickered=1`; extract sha256 equal; a sampled lot re-opened |
| `BP-b-1` THE rule R1 as one module | @18e0afcdcb | ~5 | 15 test arms; probe 716 asset rows, deterministic; the module run on the held partitions |
| `BP-b-6` the lot-export patch (nothing applied) | @e33999e30b | ~10 | 7 fixture arms; `legacy_equal=true lots=484447 keyed_on_lot=true`; diff read |
| `BP-b-5` cause of the missing daily files and lagging objects | @34f44e3331 | ~9 | `dates=6 determined=2 undetermined=4`; sentinel 404, header-only export and missing price files re-read |
| `BP-b-8` FWD-1's thread on an unlisted holding | @96eefbea99 | ~12 | `rule=R1 distinct_trades=2 sources_checked=8 equal=true`; the served object re-opened, R1 recomputed |
| `BP-b-2` R1 replayed into the before/after list | @4a03d59451 | ~6 | `served=1657 changed=824 unchanged=621 deterministic=true`; list md5 and sha256 equal the record's; four random changed rows recomputed equal; EXXON and MIAMI-DADE re-read |
| `BP-b-7` the FWD-7 packet | SUPERSEDED, not merged | ~11 | none: stopped five minutes in with no commit (section 3) |

Amendments, all the issuer's, none graded by a gate limb: face notes on BP-b-2 and BP-b-8 (the module probe's findings, @8956787a11) and BP-b-7 (@71d4dd56f7), then BP-b-7 marked superseded with its pointer.

## 2. The one real run: FWD-1's thread, re-opened by the issuer

Served object `opal-data-49financial/advi/49financial/platinum/entities/clients/z08188711/detail.json`, VersionId `HYPH2uKxlFNG38t2uQTVea9AhSB_8JHQ`, `data_as_of` 2026-10-09: ALLSPRING CORE BOND CIT CLASS E2, 72 lots, ticker null on all, ONE `current_price` 10.3525.
R1 variant A with the merged module over the held partitions: no trade on 2026-10-09; on 2026-10-02 two Buys (distinct ids 742108391 and 742108404), R1 price 10.3525. The served value is R1's carry of the last observed trade (observation date 2026-10-02); eight ticker sources checked, none gives a ticker.
Limits, not hidden: the SERVED row is canonical `linear_interpolation` (the label the CTO banned; row W12-S1, ARMED); the kind (a collective investment trust) is judged from the name and the dimension; no unlisted group prices from a same-day trade, and of 33 evaluable carries 20 equal R1 and 13 do not.

## 3. R1 Amendment 1 and why BP-b-7 was superseded

While worker ~11 ran BP-b-7 (five minutes, no commit), the CTO ruled R1 AMENDMENT 1 (msg 5323; `ledger/CTO_RULING_R1_THE_PRICE_RULE_20261013.md`) on the two calls this seat queued from BP-b-2: Dividend Reinvestment and Income Reinvestment buys count as trades; Transfer In, Journal, cash legs and every row without an executed market price stay out;
par-quoted bonds serve the per-unit price (executed price divided by 100 where the asset dimension's class says par-quoted), the price-to-market-value ratio corroborating and a disagreement withheld. The CTO asked that the replay be re-run on that variant so the list Andrew reads carries it.
A packet over the variant-A list would have shown Andrew a superseded rule, and the decomposition is frozen mid-round, so this seat stopped the worker, marked the order superseded and closed. The amended module, the re-run replay and the packet are round 3.

## 4. What round 2 measured (carried, not decided)

1. **Replay, variant A as built (superseded by the amendment):** of 1,657 served `transaction_observed` rows over 2026-09-16..10-13: UNCHANGED 621; CHANGED 539 (524 up, 15 down); NOW_CARRY_FORWARD 285 (13 equal the served price, so 811 prices move); NOT_RECOMPUTABLE 212 (no R1 trade anywhere from 2020-03-06). Variant B changes 780.
   Under the amendment: the 77 reinvestment-sourced carry-forwards price from buys, the 153 Transfer-In-sourced stay carry-forwards with their dates, and the 8 par-quoted rows read UNCHANGED. The re-run produces the real figures.
2. **Estimated rows:** 18,566 `linear_interpolation` rows over 886 assets in the window; the replay lists what R1 would show for each (15,554 a last-traded date under A).
3. **The replay's limits:** the lookback reads trade dates t and t+1 while 61,583 trade rows land more than a day late (up to 519 days, W6-S3); `silver/transactions` has gaps (50 dates in 2026, 436 in 2020-2025, W6-S5); the canonical window carries no `carry_forward` source value (W6-S4).
4. **The census:** 1,859 of 5,121 non-cash untickered lots (36.3 percent) are priced off no canonical row (300 equal a canonical price more than 5 days away, 1,559 equal none); 21,614 of 198,261 lots break `market_value = quantity x current_price` (16,297 with market_value 0); one listed-but-untickered asset by name.
5. **The missing daily files:** on every Monday and Tuesday run date from 2026-09-14 to 2026-10-13 the first transactions export is header-only, the bronze sentinel is withheld, `bd-silver-merge` never fires and `bd-price-update` (no schedule of its own) never runs. Not determined: why those exports are header-only upstream.
6. **The lag of the detail objects** is inherited from `account_performance.parquet` (max date 2026-10-09), not a T-1 rule (`D_02.advisor_client_detail.py:2874`, `:2937`); 243 of 3,510 objects are older.
7. **The lot key** folded 15,553 export rows; ruled by the CTO (PRD v1.1: add `relationship_id` or the export's own lot id). The fixture proof re-runs before any apply.

## 5. ARMED rows (11, all this seat's) and what disarms each

54 rows in the channel, 27 open, 15 adjudicated (round 1), 11 ARMED: W1-S3, W2-S2, W2-S4, W3-S3, W3-S4, W4-S2, W4-S8 (round 1) and W6-S2, W7-S4, W10-S2, W12-S1 (round 2). None disarms in round 2: each disarms only by a served move under FWD-7, except W10-S2 (the re-run fixture proof).

| row | brought within reach by | disarmed by (round 3+) |
|---|---|---|
| `W2-S2` repeated ids in the median | R1 counts each id once (BP-b-1) | writers import R1 |
| `W2-S4` two readers of one rule | R1 (BP-b-1) | writers import R1 |
| `W1-S3` Lambda rank copy lacks `scoped_override` | R1 carries the full rank table | the Lambda imports R1 or is retired |
| `W3-S3` which rule is THE rule | R1 and Amendment 1 (ruled) | the writers' served output equals R1 on the census |
| `W3-S4` dividend rows set the median to 1.0 | R1 excludes non-trade rows | writers import R1 |
| `W4-S2` lots priced off no canonical row | BP-b-3's census names the 1,859 | the fix of their source |
| `W4-S8` market value off quantity x price | the census counts 21,614 lots | per-lot UNVERIFIED under FWD-7 |
| `W6-S2` par-quoted bonds 100x | Amendment 1 rules the unit | the amended module and the re-run replay |
| `W7-S4` the identity breaks on 21,614 lots | the census | as W4-S8 |
| `W10-S2` lot key folds 15,553 rows | PRD v1.1 rules the key | the re-run fixture proof reads zero rows folded and zero colliding groups still differing |
| `W12-S1` the served row is the banned interpolation | R1 carry matches the value | the writer stops writing `linear_interpolation` as a served source (FWD-2 and FWD-7) |

## 6. Proposed round-3 enrichment list (the CTO's analysis rules it)

1. **R1 Amendment 1 into the module, then the replay re-run on it:** reinvestment buys in, par-quoted per-unit, the 153 Transfer-In carry-forwards each with their observation date; determinism arm; the list Andrew reads. The lookback read widened to late-landed trades (W6-S3) or its limit stated in the list.
2. **The FWD-7 packet (BP-b-7 re-cut):** the dollar effect on the latest snapshot, the movers, and the downstream readers each fix reaches, with the eight 100x rows no longer in it.
3. **The lot-key fixture proof re-run** (call 239a), then the WORLD apply of the Units and Cost Basis switch under its never-widen pair.
4. **Writers import R1** under FWD-7 pairs, after Andrew's review, in this order: the S_00 build and inject stage, the Lambda, the silver script.
5. **The Monday and Tuesday header-only export:** the upstream cause, read-only.
6. **The 1,859 off-canonical lots:** their source named.

-- 2.0.0_SA_COO~K1
