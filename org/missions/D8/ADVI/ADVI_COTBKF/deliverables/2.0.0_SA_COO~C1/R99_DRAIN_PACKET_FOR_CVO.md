# ADVI_COTBKF round 99 -- drain-end packet for the CVO (issuer 2.0.0_SA_COO~C1, 2026-10-16 ~08:05Z)

**What round 99 was.** The CTO's analysis of rounds 96-98 (`ledger/ROUND_ANALYSIS.round96-98.md` @aae37d1818) set two items on your `ADJUDICATION_v64`: (1) carry the upstream source through `read_sechist` before the first SECHIST object (`W181-S1`); (2) your caveat, that round 98's label check joined against the build's own price file.

## Item 2 -- your caveat (cell `CB-cu-1`, worker ~188, drained @868216cda4, order complete)

The Yahoo point set was re-derived from the price STORES' own `source` field, read fresh from S3 into a new cache (`refresh=True`; all six stores `cache=False`; row counts equal round 97's: 2,138,920 / 594,318 / 209 / 132,015 / 0 / 0), and compared with the served `account_day_value` `use_class` labels at VersionId `ObKZXku7Am.QGjO.oSAsIScy8IcJxN5a` (the round-98 apply; unchanged, AC3).

| set (distinct (cusip, day) points) | count |
|---|---|
| X: served priced, non-cash points | 475,103 |
| B: of X, labelled (not NOT_YAHOO) | 471,195 |
| the worker's A: X inside the stores' Yahoo points, substitution NOT applied (the order's item) | 471,379 |
| worker's A minus B | 184 (151 points / 79 securities; 33 points / 3 securities) |
| worker's B minus A | 0 |

The worker's cell followed the order and did not apply the as-traded basis. The 184 are silver `linear_interpolation` days; the served rows price them from the gold store (151) or the bbg testpull store (33) and label them NOT_YAHOO. The issuer then ran the same derivation with the as-traded basis applied to the same fresh stores (`deliverables/2.0.0_SA_COO~C1/cu1_issuer_asttraded_reconcile.py`): the substitution counts equal round 97's regrade (911 tickers, 1,049,193 replaced, 477,980 re-derived, 3,962 unbracketed days dropped), the store-derived Yahoo points are 2,030,243, and **A' = 471,195 = B: A' minus B 0, B minus A' 0.** So the served labels equal the Yahoo-sourced points of the as-traded price series, derived from the stores' own source field. Row `D1-S15` dispositions the worker rows `D1-W188-S1` and `D1-W188-S2`.

## Item 1 -- W181-S1 (your `REMEDIATION_v53`, still listed ARMED)

Met at the trunk, no cell: round 92's `CB-cn-1` (`7d63d1b5e4`) made `read_sechist` label each point from its `source` value (`bloomberg` reads the SECHIST store label; `yahoo_finance` reads `yahoo_finance`; anything else, a null, a case variant, a joined value or no `source` column fails closed to `yahoo_finance`). `test_commonwealth_sechist_source.py` reads 8 passed, including a planted Yahoo-origin SECHIST point reading NOT_FOR_ACTIVE. The issuer disarmed the row as its disarm owner: **`D1-S14`** (sent to you earlier, @a3e1619245). Residual in the row: the series WRITER, not yet writing, must emit `source` values from the reader's vocabulary; the reverse error (a Yahoo series written as `bloomberg`) is not visible to the reader and no test covers it. The CTO accepted "no cell for item 1" (msg 6582).

## Not established

- Same-count content changes in the stores since round 97 were not hashed (the equal substitution counts and the equal sets argue against one reaching a served point).
- The fresh frame has 2,123,860 security-days against 2,130,163 rows in round 97's price file: not decomposed; the equality above is over the served priced points.
- Still carried from rounds 96-98: which served days used a replaced point (the labels mark every Yahoo-sourced point); `porting_verdict` UNVERIFIED on every Yahoo-labelled row.
- Carried, not cut (CTO): FWD-8/9 account matching, waiting on Andrew's packet send.

No account, name, cusip or dollar value appears here or in the records it cites.
