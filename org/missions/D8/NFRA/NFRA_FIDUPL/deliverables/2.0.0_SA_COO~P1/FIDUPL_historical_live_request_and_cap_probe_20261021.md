# FIDUPL: the live Historical request (10/15/2026) and the cap probe, measured 2026-10-21

Author 2.0.0_SA_COO~P1, 2026-10-21 ~14:20Z, on CTO msgs 9085 and 9091 (CRO 9089). Dates, counts, bytes and statuses only; no account number, group name, client name, cookie or token. Request ids appear as sha8.

## Session

One agent sign-in on the warmed agent profile: 13:25Z, `outcome=SIGNED_IN`, no 403. Logout 14:12Z, statuses `204,400`. The hourly count before it was 0. Writes: only `POST .../export/v1/historicalExport.json` (17 requests, listed below) and `status.json` reads; every call went through a two-path allowlist. No profile was saved, changed or deleted. The profile used is the daily's saved Custom profile (the one the daily six files carry, sha8 `fff16c7d`; positions and prices both enabled). The create body (array `fileTypes`): `profileId`, `profileName`, `exportFormat "3"`, `historicalDate MM/dd/yyyy`, `fileFormat ""`, `fileTypes ["POS","PRC"]`, `indicatorName ""`, with the page's `x-xsrf-token` header.

## Where the files appear (the 10/15 request, 13:30:13Z)

- The POST answers 200 `{"statusIndicator":"S","statusMessage":""}` and the request is queued.
- The files appear in the Export Status list of the **REQUEST day** (`dateString` 2026-10-21), never the historical date (those lists stay empty). Names carry the date: `position101526.txt`, `prices101526.txt`; a new request id and a new (temporary) profile id per request; types `EXPOS`, `EXPRC`.
- Ready in about 30 seconds (`IN PROCESS`, then `COMPLETED`). Download is the standing `downloadExport.do` with the row's `fileName`, `fileType`, `profileId`, `requestId`.
- Layout equals the standing custom files: position 62 comma-separated columns, prices 44, CRLF, as-of date in column 0. Bytes 30,298,806 and 646,264.
- **A historical request for date D carries as-of D** (20261015), unlike the standing export, whose file for export day D carries the previous trading day.
- Against the landed standing 20261016 files, a 10/16 historical request differs: position 30,326,735 against 30,326,543 bytes, same 67,944 rows with 28 rows different; prices 645,728 against 645,722, 1 row different. The routes are not byte-identical, so the lander's never-overwrite rule stands (the 10/16 copy was not landed).

## The cap is NOT 120 days, and it differs by file type

An older date than the data window is **accepted** (POST `S`) and then finishes `COMPLETED WITH ERRORS`; download answers a 125-byte `<status>` stub, code -2, "The file you requested does not exist". No POST was refused (no 4xx, no refusal text).

| days back | historicalDate | positions | prices |
|---|---|---|---|
| 5 | 2026-10-16 | served | served |
| 6 | 2026-10-15 | served | served |
| 30 | 2026-09-21 | served | served |
| 60 | 2026-08-21 | served | served |
| 120 | 2026-06-23 | served | served |
| 121 | 2026-06-22 | served | served |
| 124 | 2026-06-18 | served | served |
| 126 | 2026-06-17 | served | **no file** |
| 128 | 2026-06-15 | served | **no file** |
| 131 | 2026-06-12 | no file | no file |
| 135 | 2026-06-08 | no file | no file |
| 150 | 2026-05-22 | no file | no file |
| 180 | 2026-04-24 | no file | no file |
| 270 | 2026-01-23 | no file | no file |
| 365 | 2025-10-21 | no file | no file |
| 730 | 2024-10-21 | no file | no file |

**Proven floor on 2026-10-21: positions 2026-06-15 (128 days), prices 2026-06-18 (124 days).** Neither floor was probed on the days between 128 and 131 for positions (06-12 is the next earlier trading day and errors, so 06-15 is the edge at the trading-day grain) and 124 and 126 for prices (06-17 errors, 06-18 serves). The window is relative to today, so it moves daily; it is a retention depth of about four months, not the wizard's 120-day picker. The Custom route with the daily's profile returned position and prices files only; balances come only through Standard Format A (`PBL`), which was not requested and is unmeasured. Every earlier statement should read "positions to about 128 days, prices to about 124 days; proven 2026-10-21".

## Landed (WORLD write, CTO 9085 and 9091: served files land by content date)

`land.land()` on a partial handoff folder per date (listing source `historical-wizard`, failure null), scope `alongside`, never overwriting. 15 files, 8 content dates, every landed byte count equal to the downloaded bytes:

| content date | position | prices |
|---|---|---|
| 20260615 | 26,429,282 | none served |
| 20260617 | 26,504,650 | none served |
| 20260618 | 26,548,176 | 520,931 |
| 20260622 | 26,637,367 | 525,709 |
| 20260623 | 26,654,646 | 527,326 |
| 20260821 | 29,211,030 | 631,316 |
| 20260921 | 29,892,191 | 652,875 |
| 20261015 | 30,298,806 | 646,264 |

Each date's run record reads `PARTIAL` (the other four files of the six are absent by design). Keys: `fidelity/alongside/bronze/<position|prices>/<YYYYMMDD>/<name>`.

## Not done: the per-account transactions probe

`POST /ssc/transaction-history/wc/channel/api/v1/historical-transactions` answers 400 `TXH-400` "invalid searchBy" for the values tried (empty, ALL, S, A, T, SYMBOL, SECURITY, TRANSACTION, NONE); with ISO dates and no searchBy it answers "searchBy must not be null". The app route `/app/transaction-history` redirects home without an account context, so the valid `searchBy` value (and the date format) is unread. It needs one capture of the page's own call (or the module's code) from an account's transaction page. Nothing was sent that changes state.

## Counts

17 `historicalExport.json` POSTs (two requests for 06-22 by an accident of my own tooling; the second returned identical bytes). One sign-in. Local files: `C:/tmp/fidupl-hist/` on dell1 (not in the repo).
