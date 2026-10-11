STATUS: WRITTEN, NOT SENT

# Price request: Bloomberg at site Z (fixed income and other)

**Size: 1,306 securities, 867,890 security-days of daily closes.** Nothing has been sent, queued or pulled.

## Read first: can READ_HERE.md support this request?
`integrations/bloomberg/READ_HERE.md` was read in full. It does **not** forbid a request of this shape and it does **not** establish one. What it shows: a `HistoricalDataRequest` returned a full `PX_LAST` series (lines 152-154, on an ETF). It names no fixed-income or other security, no history depth, and no identifier form (CUSIP or ticker). It says BQL is refused (lines 122-123), so this request is a plain historical-data request on `//blp/refdata`, not BQL. Its own rule at lines 161-162 applies: a result in one surface says nothing about the next. So this is written as a request to find out whether Bloomberg serves these closes and, if it does, to pull them. Whether it serves historical closes for these securities back to 2013 is **not established**.

## What is asked
A daily close (`PX_LAST`) for each security in `PRICE_REQUEST_BLOOMBERG.csv`, for the dates it is held with no price. Dates run from 2013-04-08 to 2026-06-22 across the list; each security's own first and last date are in the csv. This is Andrew's word: Bloomberg at site Z for fixed income and other, behind its budget (ADVI_COTBKF_PRD.md, v0.4 Addendum 2, lines 214-220).

## Which securities
1,306 securities, every kind the build does not send to Yahoo (commonwealth_price_need_file.py:45-46).

| Kind | Securities | Without a symbol | Security-days | Unpriced position rows |
|---|---|---|---|---|
| Alternative Investment | 22 | 17 | 8,971 | 13,523 |
| Annuity | 29 | 29 | 36,690 | 83,370 |
| Cash | 1 | 0 | 117 | 1,127 |
| Cash Equivalent | 482 | 458 | 136,583 | 208,376 |
| Fixed Income | 772 | 738 | 685,529 | 822,085 |

- **1,242 securities have no symbol.** The delivery carries their 9-character CUSIP; the csv lists it as the identifier (`identifier_type` = cusip). The other 64 carry a symbol, listed as the identifier.
- Annuity and Cash Equivalent items may have no market close at all. Not tested.
- 13 of the 1,306 securities are priced on some dates already; the request is for their unpriced dates only.

## Size and the budget
- 867,890 security-days (a security counted once per date it is held unpriced). If each security's whole first-to-last span is requested: 871,692 points.
- The repo's own backfill budget is a daily ceiling of 150,000 less a production reserve of 30,000, so 120,000 points a day before anything else is spent (bbg_budget.json:2-3, bbg_budget.py:99). At that rate this request needs **at least 8 separate days** (867,890 / 120,000 = 7.2). On 2026-10-05 about 175,000 rows of backfill used the Terminal's whole daily capacity and blocked the 07:00 ET production pulls (bbg_budget.py:3). Do not send this as one pull.
- The budget's unit was measured on BQL rows. What a historical refdata request spends is not established.
- Only a seat on the Terminal box can make the call (README.md:124-125), and Bloomberg pulls go through their queue (CLAUDE.md:267).

## Rules this request relies on
- `integrations/bloomberg/READ_HERE.md:41`: "**Two phases, on purpose. `fill` costs NOTHING and is repeatable; `submit` spends one of a"
- `integrations/bloomberg/READ_HERE.md:42`: "2-attempt budget.** Bloomberg locks the account after repeated failures, which is why the fill"
- `integrations/bloomberg/READ_HERE.md:122`: "**NOT SERVED:** the constituent LIST. `//blp/bqlsvc` opens and refuses **every** query with"
- `integrations/bloomberg/READ_HERE.md:123`: "*'User not authorized to use BQL'* -- including `get(px_last)for(['IBM US Equity'])`, which has"
- `integrations/bloomberg/READ_HERE.md:152`: "**CURRENT-DAY ONLY -- THE PROPERTY THAT COSTS MONEY.** A `HistoricalDataRequest` returns ZERO rows"
- `integrations/bloomberg/READ_HERE.md:153`: "for the derived fields while `PX_LAST` returns a full series **in the same call** (the control that"
- `integrations/bloomberg/READ_HERE.md:161`: "> wall sits on a surface that was never reached. **A clean, well-controlled zero measured inside one"
- `integrations/bloomberg/READ_HERE.md:162`: "> surface says nothing about the surface next door.** When you get a refusal, ask which SURFACE"
- `integrations/bloomberg/README.md:38`: "`server.py` exposes four read-only MCP tools over `blp_client.py`. Only `//blp/refdata` is opened;"
- `integrations/bloomberg/README.md:46-48`: "**Response caps:** `bloomberg_historical_data` accepts `max_data_points`. Measured 2026-08-12: it **binds**, returns the **LATEST N**, and is **PER-SECURITY** -- so a response is bounded by `securities x fields x min(days, cap)`."
- `integrations/bloomberg/README.md:124-125`: "**Remote reach.** The SSM tunnel is designed, not built: no `:8790` service, no SSM agent. Today the only path to these pipes is local, on the Terminal box."
- `CLAUDE.md:267`: "**Bloomberg pulls go only through their queue; other vendor APIs need no per-use word.**"
- `data/etfs/scripts/rivalfunds/bbg_budget.json:2-3`: "'daily_ceiling_rows': 150000, 'production_reserve_rows': 30000"
- `data/etfs/scripts/rivalfunds/bbg_budget.py:99`: "limit = int(cfg['daily_ceiling_rows']) - int(cfg['production_reserve_rows'])  (a backfill may spend ceiling - reserve - spent today = 120,000 points)"
- `data/etfs/scripts/rivalfunds/bbg_budget.py:3`: "Measured 2026-10-05: about 175k BQL rows of local backfill between 05:30Z and 07:06Z exhausted the Terminal's daily capacity and blocked the 07:00 ET production pulls."

## Where the prices land
In the securities history that MDPF_SECHIST owns (ADVI_COTBKF_PRD.md lines 220-221). This project does not own it and writes nothing there. A security Bloomberg does not price leaves its days unpriced.

## What it would unblank (upper bound)
Of 1,559,722 account-days that are blank for price:
- **119,078 (7.63 percent) would be fully priced by this request alone.**
- A further 183,461 (11.76 percent) need this request and the Yahoo one.
- These are UPPER BOUNDS. Bloomberg may not price every security asked for (see above), and a return also needs the prior day's value.

## What is not established
- That Bloomberg serves a daily close for fixed income and other securities back to 2013, by CUSIP or any other identifier.
- What a historical request spends against the daily capacity.
- How the queue is entered; READ_HERE.md has no queue section and none was found.
- Whether MDPF_SECHIST accepts this delivery; its owner has not seen it.
- Whether the denominator matches the returns table's own NOT_MEASURABLE count.

Measured from `account_day_value.parquet` (21,102,041 rows) and the silver transactions cache. Detail: `PRICE_REQUESTS.json`.
