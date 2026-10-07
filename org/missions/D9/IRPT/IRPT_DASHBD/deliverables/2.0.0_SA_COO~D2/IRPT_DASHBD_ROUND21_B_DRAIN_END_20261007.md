# L8 drain end -- IRPT_DASHBD round 21, workstream B

**Issuer:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~12:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @75717e8580

The one order of the round is terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, re-run by the issuer before
the drain). 0 JUDGMENT criteria. Risk SERVED (a gold producer), but this cell wrote NOTHING to S3: build and local run only. The worktree
and branches were removed. On: `1.0.0_SA_CTO~DELL2`'s round-20 analysis @58f3ed0501 item E1 (FWD-3).

## The order

| order | drain | criteria (issuer re-run) | result |
|---|---|---|---|
| DB-b-33 (`account_class_daily` and its contract, 49F) | @75717e8580 (worker ~18: 306eed4ab1, 25868ed7dc) | DB21-1-AC1..AC3 PASS | 61 sampled accounts (seed 20261007) over 2026-09-29..2026-10-05; 52 produce rows; 254 measured account-days, classes sum to the account within 2.1e-16; 6 not measurable (5 CLASS_VALUES_DO_NOT_SUM_TO_ACCOUNT, 1 ACCOUNT_RETURN_NOT_MEASURABLE); 78 distinct holdings, 45 unclassified |

Files: `data/assets/scripts/gold/irpt_reporting/account_class_daily.py` (beside the served producer, which it imports read-only),
`.../tests/test_account_class_daily.py` (20 tests), `org/standards/IRPT_DASHBD_ACCOUNT_CLASS_DAILY_CONTRACT.json` (9 columns, seven-class
enum, method_version 1 and its limits). Drain hygiene: commit-gate clean on both `.py`; the folder's suite 42 passed; the served
producer, its handler and the Lambda code show a 0-line diff over the cell.

## Read before grading

- **The sum identity is earned, not plugged.** Cash is the custodian's measured cash lines; a day ties only if the classes' summed values
  meet the account's value within half a cent (positions carry 4 decimals, the balance 2), and only then does cash take the sub-cent
  residual. A day that does not tie is null with a reason (5 account-days on one account).
- **Row IRPT_DASHBD-W18-S2, a FWD-3 quality question for the CTO.** The classification module @63fa1a2e32 names 197 tickers, all ETFs or
  funds. Single stocks and money-market funds therefore land in `unclassified`: 45 of the sample's 78 holdings, about 16% of position
  value on 2026-10-01. The table follows the rule ("nothing is guessed"), but a served view would show about a sixth of the book as
  unclassified. The question: release as is, or first have MDPF_SECCLASS cover single stocks and money-market funds.
- **Row IRPT_DASHBD-W18-S1:** the producer's trade-leg tokens (`tr_cd` TR, `trade_typcd` BUY/SELL) sit in one block in the producer
  because `sources.json` was outside the grant. The release cell moves them into the declaration.
- **Method limits, stated in the contract:** income, fees and withholding land in `cash`; a trade settling after its trade date moves
  positions and cash on different days; the in-kind path is covered offline only (0 in-kind legs in the sample; 220 trade legs exercised).

## What the round leaves

- The served release of `account_class_daily` (upload under rule 13, first gold write, schedule, under never-widen halves) is the next
  cell of the decomposition (section 21). It waits on the CTO's answer to W18-S2.
- FWD-8 stays HELD on Andrew's per-use word for the split BD pull (2,299 accounts, 2,299 calls, 4,598 ranges).
- The live thread trace (FWD-1 hop 5) was not re-run: the cell was a local build and dell2 holds no signed-in portal session. Its last
  exercised run stays 2026-10-02 (STATUS~D).

## Rows in the round

| row | class | standing |
|---|---|---|
| W18-S1 | OBSERVATION, INERT | open: trade-leg tokens to move into `sources.json` at release |
| W18-S2 | OBSERVATION, INERT | open: 45 of 78 holdings unclassified (single stocks, money-market funds), for the CTO |

OPEN 2, ARMED 0 (comp-surprise after the drain).
