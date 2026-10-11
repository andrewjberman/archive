# AMGT_RESAPP round 89 -- the issuer's reads (`AMGT-nn-8`, and the measurements behind decomposition s.97a)

Each read answers its question; a read that finds a defect becomes a round-90 cell, never a mid-round one.

## nn-8 / Z-W266-S3 (2026-10-11 ~03:3xZ) -- does a drafted name's driver have a numeric source?

Live `/thesis` through the scoped handler (KlosR/ap8O; the route's own `thesis_driver_chart`, no store written), the five drafted names
and BA as the control. The route serves a chart by one of two branches (`thesis_driver_chart`, scoped_amgt.py:3939): (1) the driver's
series equals a model-block fiscal series by exact mnemonic or definition; (2) at least TWO of the driver's own points carry a
verified `span` and the driver's `resolution` is not held or absent.

| name | driver series | resolution | points emitted | with span | held_uncited | model-block series probed | chart |
|---|---|---|---|---|---|---|---|
| ASML_NA_Equity | EUV system revenue recognition (units) | cited | 1 | 1 | 1 | 80 | ABSENT |
| NU_US_Equity | Total revenue (US$ millions) | series-name-located | 0 | 0 | 0 | 75 | ABSENT |
| SAP_GY_Equity | Current cloud backlog (constant currency growth) | cited | 1 | 1 | 2 | 79 | ABSENT |
| BABA_US_Equity | Cloud Intelligence Group revenue (RMB millions) | cited | 0 | 0 | 2 | 52 | ABSENT |
| PBR_US_Equity | Total oil and gas production incl. NGL (mboed) | cited | 0 | 0 | 1 | 41 | ABSENT |
| BA_US_Equity (control) | Commercial Airplanes aircraft deliveries | cited | 3 | 3 | 0 | -- | SERVED (filing) |

**Answer.** None of the five has a model-block mnemonic or definition equal to its series (branch 1 misses on all five), so the chart
can only come from the filing's own points (branch 2). The producer EMITS points for four of them and the verifier HOLDS them:
ASML 1 of 2 verified (a point's value "not found as a whole number inside the block carrying" its span); SAP 1 of 3 (same reason);
BABA 0 of 2 -- the held reasons read "no period label for FY2025 / FY2026 was located in the excerpt" for values 118,028 and
158,132 RMB millions; PBR 0 of 1 (value 2.99 mboed "not found as a whole number"). NU is different in kind: the excerpt "states no
numbered periods for this series" (absent_reason), so its absence is honest on the source. The chart's absence is therefore NOT a
route defect for any of the five; it is the verification rule (producer side, the analyzer's span location), and the served reason
already says why in plain words. **Defect candidate for round 90, owner AMGT_FILINGS / the analyzer (not read to its cause here):**
BABA, PBR and SAP lose emitted points at the verifier under two held reasons -- "no period label ... was located in the excerpt" and
"value not found as a whole number inside the block carrying" its span -- on figures the producer did emit with a period and a unit.
Whether that is a locator limitation or a figure the excerpt does not hold is the owner's read, which this read did not make. The
analysis rules whether a round-90 cell reads it or the honest absence stands.

## decomposition s.97a measurements (for the record)

- D1-S16: `crosswalk.resolve` over the ten United States members of ASML's stored peer set: bare ticker 0 of 10 MEASURED; `<T> US`
  form 7 of 10 (INTC, AMAT, LRCX, AMD, NFLX, MU, DELL); CSCO, ORCL, PANW UNRESOLVED.
- D1-S14: the scanner's `universe_data.json` for sp500 and acwx -- entry keys country, divzWeight, industryGroup, mktVal, name,
  price, sector, ticker, universeWeight, values; document keys asOf, securities, sourceUniverseColumn, universeId; no currency field at
  either level. The model-block pool: INTC, CSCO, MU, DELL, 700 HK, 000660 KS ABSENT; AMD SERVED.
- D1-S15: stored subject cap 541,931.78 @ 2026-09-19T07:53:19Z against the subject's current block 621,657.44 @ 2026-10-10T13:01:55Z.
- Item 7: portal `origin/DEV` is 46 commits ahead of `origin/PROD` (IRPT_ANLREQ, ADVI_BILLING, DSGN_AMGTV1, CRPS-at-2, AV-zzm..zzs).

checked 1 of 1 issuer reads (Z-W266-S3)
