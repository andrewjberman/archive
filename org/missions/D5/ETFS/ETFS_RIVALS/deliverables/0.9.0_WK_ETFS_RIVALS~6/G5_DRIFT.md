# G5 history drift -- classification (RIV-gd-1, row Z-S29)

A read: live newest G5 vs a G5 built by the current code (local sink), 13 funds less IDVZ/PFOE, report dates 2026-01-02..2026-10-02. Written by `rivalfunds/tools/g5_drift.py`; no S3 write, no replay.

- dates compared: **189**; rows compared (union of the two sides): **9477**; rows differing (any column or presence): **9477**, of which in trade facts (not only G3 labels): **1344**, the other 8133 differ only in their G3 revision labels (three G3 pulls landed after the live build); **unclassified rows: 0**.
- columns est_price_source, key_resolution are new on 186 dates (the older live objects lack them; additive, not a changed value).

| class | cause commit | cell | columns | dates | rows | on the page | reproduced at the commit |
|---|---|---|---|---|---|---|---|
| key_resolution_out_of_confidence | `b723f89d22` | RIV-h-6 | confidence, key_resolution | 178 | 1040 | yes: confidence, key_resolution | 51 of 51 |
| full_exit_priced | `ab0a58eaa4` | RIV-x-1 | action, est_price, est_notional, est_notional_base, discretionary_shares, residual_pct_prior, confidence, est_price_source | 100 | 266 | yes: action, est_price, est_notional, est_notional_base, discretionary_shares, confidence | 39 of 39 |
| own_prior_pairing | `5cd27dc0d2` | RIV-t-5 | row_presence | 1 | 7 | yes: row_presence | 7 of 7 |
| implausible_window_refused | `b137069123` | RIV-h-5 | row_presence | 2 | 10 | yes: row_presence | 10 of 10 |
| g3_currency_in_income_conversion | `2a655a0180` | RIV-e-2 | income_funded | 1 | 7 | yes: income_funded | 7 of 7 |
| g3_minor_unit_dividend_currency | `0b2981d770` | RIV-e-2 | income_funded | 4 | 13 | yes: income_funded | 13 of 13 |
| g3_latest_pull_supersession | `4fa3e25f5e` | RIV-g-4 | corporate_action_ref, corporate_actions_applied, dividends_applied, corporate_actions_revision, income_funded | 189 | 9467 | yes: income_funded | 9467 of 9467 |

## What each class is

- **key_resolution_out_of_confidence** -- an unresolved key no longer overrides `confidence` (the key's state is its own column, key_resolution): UNRESOLVED -> CLEAN or FLOW-WINDOW. Not shown on the page: none.
- **full_exit_priced** -- a line kept at quantity 0 is an EXIT priced from the prior valuation (was a trim with no price); an exit is no longer read against the flow factor. Not shown on the page: residual_pct_prior, est_price_source.
- **own_prior_pairing** -- the daily/backfill build pairs a fund with ITS OWN prior report date; a fund back after a gap gets its window (the live object, built pairing with the global previous date, has none). Not shown on the page: none.
- **implausible_window_refused** -- a fund-window whose flow factor is outside the band (or with too many zero-quantity lines) is REFUSED: zero trades. Not shown on the page: none.
- **g3_currency_in_income_conversion** -- G5 dividend_ccy prefers the G3 `currency` (DVD_CRNCY); the 10-02 G3 pull carries it, the 09-30 import pull did not, so a dividend converts at another rate and the income-funded label flips. Not shown on the page: none.
- **g3_minor_unit_dividend_currency** -- a G3 dividend in a minor-unit currency (GBp/GBX, ZAr/ZAc, ILs/ILa) converts at the major rate / 100; the 10-02 G3 pull carries those currencies, so the income received in the window, and the income-funded label, change. Not shown on the page: none.
- **g3_latest_pull_supersession** -- per security the LATEST G3 pull is read and every pull read is joined into the revision labels: pulls landed after the live build change every row's G3 label, the revision inside a corporate_action_ref and, where a pull adds income events (a money-market line's daily accrual), the income-funded label under UNCHANGED code. Not shown on the page: corporate_action_ref, corporate_actions_applied, dividends_applied, corporate_actions_revision.

## Reading it

- The first four classes are changes of CODE. The two RIV-e-2 income classes are code that acts only on G3 data landed after the live build (the 10-02 pull carries `currency`). The last class is the G3 DATA itself under unchanged code. History is never rewritten in place, a replay writes new revisions. Whether a class is a defect in the old values is the CTO's call, not this file's.
- `row_presence` is not a column: the class adds or removes whole rows (own_prior_pairing adds, implausible_window_refused removes).
- The brief's `est_price_source and key_resolution new on 183` reads 186 here because a date counts when any compared row lacks the column (the six newest live objects carry both).
- `rows` counts a row once per class it sits in (a row may sit in two classes); the sum of class rows may exceed rows differing.
- Reproduction: the package at the commit's parent and at the commit was built over a sample of the class's dates; the class columns equal the live values at the parent and move at the commit.
