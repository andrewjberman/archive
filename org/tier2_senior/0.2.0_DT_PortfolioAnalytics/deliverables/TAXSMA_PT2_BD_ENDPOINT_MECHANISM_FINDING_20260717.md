# De-Risk Finding: 49F Tax SMA BD reporting-endpoint mechanism (closes Design-Brief Decision 2)

**Author:** 0.2.0_DT_PortfolioAnalytics · 2026-07-17 · **archetype:** DIAGNOSE
**Grounded on:** the HAR `bd3.bdreporting.com` request/response headers + bodies (read-only, no live calls).
**Feeds:** `TAXSMA_PT2_BD_TABLE_DESIGN_SCOPE_BRIEF_20260717.md` sec 6 Decision 2.

## Result: RESOLVED -- the reporting endpoints pull off our EXISTING `.bd.identity` session. No second login box.

The `portfolioreporting/api/*` REST endpoints authenticate off the **same `.bd.identity` OIDC cookie**
our 49F pipeline already holds (`blackdiamond/49f/session`). The only new auth step vs. the existing
datamining pull is a different bearer mint.

### The auth chain (grounded in the HAR)
1. **`.bd.identity` cookie** -- the idsrv OIDC session. WE HAVE THIS (`blackdiamond/49f/session`, minted by
   `bd-49f-auto-login`). Same cookie the datamining pull uses.
2. **`GET /session/token`** (cookie-authed) -> `{"access_token": "<bearer>"}`. This is the ClientView /
   portfolioreporting bearer -- **distinct from** the datamining bearer (`GET /datamining/auth/token`) the
   existing `opal-assets-bd49f-daily-pull` mints, but derived from the SAME cookie. (Token was opaque, no
   token_type/expires_in in the body; treat TTL as short, re-mint per run -- same discipline as datamining.)
3. **`POST /portfolioreporting/api/{endpoint}`** with headers `Authorization: bearer <token>` +
   `Content-Type: application/json` + `Referer: /PortfolioReporting/ClientView`, body `{"parameters": {...}}`.

### The exact pull surface for the 4 report classes (of the 13 endpoints ClientView hits)
| Report class | Endpoint | Body essentials |
|---|---|---|
| Performance (net of fees) | `POST /portfolioreporting/api/performance/performancePeriod` | `accountFilters.accounts:[<bdAccountId>]`, `dateRanges:[{Custom Q}, {CalendarYear}, {SinceInception}...]`, `groupings:["Account","Asset"]` -- **all windows in ONE call** |
| Cap gains (tax) | `POST /portfolioreporting/api/costBasis` | `accountFilters.accounts:[<bdAccountId>]`, `dateRange:{start,end}`, `gainLossMethod:"Both"`, `groupings:["Account","Class","Segment","Asset"]` |
| Sectors + holdings | `POST /portfolioreporting/api/allocation` | `accountFilters.accounts:[<bdAccountId>]`, `asOfDate:{asOfDate}`, `groupings:["Account","Class","Segment","Asset"]` |
| (supporting, optional) | `performance/performanceSeries` (TWR chart), `transactions/star`, `income/projected` | same shape |

### Implications (all confirm the brief's scope)
- **Reuse the 49F session end-to-end** -- do NOT stand up a second login box. The new bronze producer adds
  exactly: (a) the `GET /session/token` mint, (b) the 3 POSTs above, per account, per run.
- **Account key = BD `accountId`** in the request body (Chiles = 22596361); the response carries
  `externalId z08...` + masked `accountNumber`. Bridge BD accountId <-> Schwab account number via the
  existing `blackdiamond/49f/silver/dim_account_xref` (dependency, not new). Roster/account discovery via
  `template_roster`.
- **Small + fast** -- 3 live accounts x ~3 POSTs = ~9 calls/run; **no chunking, no backfill** (confirmed).
- **Bronze rule 17a**: land each raw JSON response byte-for-byte (they carry client names -> anonymize at
  the serve/parse-down layer, not in bronze).

### One thing to verify at build time (named, not blocking)
`/session/token` was observed as a browser/ClientView flow. Confirm it mints cleanly from the
**headless** `.bd.identity` cookie the box holds (vs. needing a browser-context handshake). The cot REST
chain (`cot_bronze_ingest.py`) is the reference for how the headless session drives REST calls; verify the
`/session/token` mint against it before wiring the producer. Low risk (same cookie, standard OIDC session
token endpoint), but exercise it first.
