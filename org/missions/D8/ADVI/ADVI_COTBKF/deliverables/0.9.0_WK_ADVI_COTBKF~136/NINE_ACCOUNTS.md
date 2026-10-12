# NINE_ACCOUNTS (ADVI_COTBKF.TO-CB-bw-5, round 75)

Counts only; labels A1..A9 by descending changed account-days at the 1e-12 floor (ties by first changed date). No account id, value, flow or return. Changed: 1,577 (1e-12), 1,575 (1e-9), 554 dates, 9 accounts.

| label | changed days | <1bp | 1-10bp | >10bp | measured days | share changed | funds held on a changed day | trade days (purch/sales/reinv/transf) | first | last | higher | lower |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 312 | 42 | 221 | 49 | 315 | 0.9905 | ANCFX CWGIX | 10 (0/0/10/0) | 2022-02-16 | 2023-05-15 | 159 | 153 |
| A2 | 229 | 223 | 4 | 2 | 277 | 0.8267 | FCNTX | 3 (0/2/1/0) | 2025-02-28 | 2026-02-06 | 130 | 99 |
| A3 | 222 | 214 | 5 | 3 | 351 | 0.6325 | FCNTX | 2 (1/0/1/0) | 2025-03-12 | 2026-06-08 | 125 | 97 |
| A4 | 211 | 197 | 1 | 13 | 287 | 0.7352 | BALCX | 13 (10/0/3/0) | 2022-04-25 | 2023-02-28 | 108 | 103 |
| A5 | 211 | 32 | 160 | 19 | 232 | 0.9095 | BALCX | 3 (0/0/3/0) | 2022-04-25 | 2023-02-28 | 99 | 112 |
| A6 | 195 | 191 | 3 | 1 | 275 | 0.7091 | FCNTX | 1 (0/0/1/0) | 2025-04-21 | 2026-02-06 | 111 | 84 |
| A7 | 80 | 77 | 2 | 1 | 127 | 0.6299 | FCNTX | 3 (0/1/0/2) | 2025-02-11 | 2025-06-09 | 40 | 40 |
| A8 | 68 | 65 | 1 | 2 | 155 | 0.4387 | FCNTX | 2 (1/0/1/0) | 2025-10-24 | 2026-02-06 | 36 | 32 |
| A9 | 49 | 15 | 28 | 6 | 53 | 0.9245 | CAIBX CWGIX | 0 (0/0/0/0) | 2022-06-22 | 2022-08-30 | 20 | 29 |

Concentration: top 1 0.1978, top 2 0.3431, top 3 0.4838 of changed account-days; 0.5104 of the changes over 10 bp in the top label. Labels whose changes sit in one held fund: A2, A3, A4, A5, A6, A7, A8.
Holders of a moved fund: 377; with a measured day on a held day 10; without 367. Measured in both builds with no changed return: 1 (price ratio exactly 1 on all its held days: 0). Funds with a measured holder: 5.

Headline: 1,577 changed account-days (1,575 at 1e-9) on 554 dates sit in 9 accounts; 7 of the 9 hold a single moved fund on every changed day (FCNTX in 5, BALCX in 2; A1 and A9 hold two). The top 3 labels carry 48.38% of the changes and the top 1 carries 51.04% of the 96 changes over 10 bp. Of 377 accounts that hold one of the moved funds on some day, 10 have a measured day on a held day and 367 have none: nine is small because few holders are measured (9 of 10 change), not because the defect is small. 5 of the 19 funds (ANCFX, BALCX, CAIBX, CWGIX, FCNTX) carry a measured holder.

Labelling and type codes: A1..A9 in descending order of changed account-days at the 1e-12 floor (|variant - baseline| of the daily return, account-days measured in both builds), ties by earliest first changed date. Mapping kept in scratch only. trade_days = distinct changed dates on which the account has a share-moving transaction row (custodian type codes) in any moved fund held on that date; kinds: purchases={by}; sales={sl}; reinvestments={dvr, DVRX, ci}; transfers={trfi, TRFIR, trci, TRCISU, trfo, trco, li, LISU, lo}; corporate_action_or_qa_other={lica, licar, LICASU, loca, QA}; trade_days_by_kind counts distinct dates per kind so a date can sit in two kinds; trade_days is the distinct-date count across kinds. Bands: under 1bp <0.0001; 1-10bp 0.0001..0.001 inclusive; over 10bp >0.001. share_changed = changed_account_days / account's measured days in the baseline (non-null return).

Not established:
- Whether a changed day is caused by a trade in the moved fund versus only a held balance: the trade-day count is a coincidence of dates, not attribution.
- Which of the unmeasured holders would change if their days were measured: the table is blank on most days, so nothing is said about them.
- Per-account economic size: no amount, value, flow or return is reported by design.
- Cancel/reversal rows and corporate-action rows are classed by type code only; Trade_Date equals the changed return date by assumption (no settle-date lag tested).
- The one measured holder with no changed return: its held-fund price differs between builds on at least one held measured day, yet its return does not move above 1e-12; why is not examined here.
- Moved funds are counted as held when the baseline account_day_value has a non-null value; 18 of the 19 moved funds appear in any holding.
