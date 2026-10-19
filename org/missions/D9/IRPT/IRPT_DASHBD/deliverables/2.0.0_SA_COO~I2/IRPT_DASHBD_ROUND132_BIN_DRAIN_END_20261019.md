# IRPT_DASHBD round 132, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-19 ~14:0xZ)

**One order (a LOCAL read: GET and LIST of Opal's own silver and bronze, nothing written outside a private folder), drained and graded on the LANDED tree; no vendor call, no secret read, nothing deployed, no client value in the repo.** Issued @5c2eda88be (merged @0a33db4973), drained: `DB-i-19` (~319, merged @7725398090). On the merged tree `DBI132-1-AC1` PASSES (and passed in the worker's tree on my own run); the proof instance reads VALID; `round-close-check --project IRPT_DASHBD --round 132 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin.

## What exists

`deliverables/0.9.0_WK_IRPT_DASHBD~319/live_read.py` (the read script, built on `InflectionSilverReader`, trading days from `lib/trading_calendar.py`, no write or vendor token), `SCOPE_LIVE_READ_R132.json` (the record: counts and verdict words only), `SESSION_LOG_DB_I19.json`, the proof instance. The private extract and the wrapper's output stay under `C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~319/`.

## What the first real run read (counts only)

- The Scope feed's silver table holds **1 landed day**; its bronze manifest holds 1. The silver row count **agrees** with the feed's own manifest on that day (1 agree, 0 disagree, 0 days with failed households).
- Run status `RAN`. 863 accounts in the feed, 863 mapped, 0 unmapped. **795 PRESENT, 68 ABSENT**; accounts x trading days = 863 x 1 = 863 accounted, 0 unaccounted. ABSENT by reason class: `NO_START_DATE_AT_SOURCE` 39, `GROUP_NO_SERIES` 17, `NO_GROUP` 12. All 795 PRESENT rows carry `market_value_eod_claim` = measured (a single day has no next-day start value to infer from).
- 14 S3 reads (10 inside the run, 4 after); 0 writes, 0 vendor calls, 0 secret reads.
- The boundary measure read **0 pairs** and the chain check read `WINDOW_TOO_SHORT` (0 accounts checked): one landed day cannot test either. They are not passed; they are not yet tested.

## What this establishes and what it does not

It establishes that the round-127 wrapper accepts the feed's real first silver (the round-125 and round-130 partition-key defects do not recur on real rows) and that the wrapper's PRESENT + ABSENT equals the accounts the feed carries. It does not establish any return value against Orion, the compounding across days (one day), the boundary between a pull and the next (0 pairs), or the trading-calendar behaviour across a weekend or holiday (the window is one trading day, so the calendar arithmetic is exercised only at its trivial case). The calendar was answered from the library's hardcoded NYSE table (it prints that `pandas_market_calendars` is absent and the table covers 2010 to 2027; row `W319-S2`).

## What the issuer read for itself

Re-ran AC1 in the worker's tree and on the merged tree (PASS), the proof check (VALID), the worker's diff against its base (two commits, all paths inside the grant), and scanned the worker's added lines for dates, partition names, identifier-length digit runs and non-ASCII (the only date-like strings are the three rows' own `surfaced_at` filing stamps; no client value, id or partition name). Before the cut I looked at the landed table once myself: one LIST and one row and column count, no value. **Not a grade.**

## Rows

`W319-S1` (the envelope's `households_without_id` is an integer count, not a list; the integer was kept), `S2` (the calendar fallback above) and `S3` (boundary and chain measures read nothing on one landed day): all INERT. Mine: **S60 and S61 stay ARMED.** Half (2) of S60's disarm, "the feed carries the account as ABSENT with a reason class, no household aggregate built from the feed's rows", is now seen at the count level (68 ABSENT rows, none zero-filled, 12 of them `NO_GROUP`), but I have not yet shown that S60's account is among those 12 rather than among the 39 `NO_START_DATE_AT_SOURCE` (its record has a null start date, so it may carry that class instead). That is a membership check by hash on private data; it is the next read, not this one.

## Open

1. **More landed days.** The daily chain adds one day a day. I will cut the same read again once 3 landed days exist, so the boundary measure and the chain check have pairs to test, unless the CTO's round-132 analysis says otherwise.
2. **The history backfill** waits for the bronze-writer fix the CTO ruled first (IB-pn-5, option B); not mine.
3. **The page reader** is cut on the CTO's analysis. Contract 0.4.2's own L9 is the CVO's.
4. The order's record face carries an `issued_date` three days earlier than the cut, copied from my draft. A record-face slip, no effect on the work.

**Andrew:** nothing from this workstream.

-- 2.0.0_SA_COO~I2
