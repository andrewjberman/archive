# WALK_ROUND74 -- AMGT-ax-6, worker 0.9.0_WK_AMGT_RESAPP~256

Records what was seen; no verdict on any judgment read. Role: the walker account is role admin, so role-gated differences are NOT covered.

## Build, instrument, safety

- Build walked: local dev build `http://localhost:5174`, started by this worker with `bun run dev:live --port 5174` from `C:/tmp/r74-256/portal` (port 5174 read 000 before; stopped at the end). Portal `6de76f0509` (ax-2's /freshness candidate). Backend: deployed `opal-amgt-scoped-api` after ax-5 (function `0MZWPl7n`).
- Walker slot: `ui_walker_account.py status` read `status=disabled armed=no armedBy=none; SSM ABSENT` before each of the two runs; no other holder appeared. Each run was armed and disarmed by the walker itself and printed `DISARM ... -> HTTP 401 ... REFUSED`. Final status: `row PRESENT opal-ui-walker@opal.test status=disabled role=admin userType=Dev armed=no armedBy=none; SSM ABSENT`.
- Instrument (`instrument/`): `walk_ax6.mjs` is a copy of the r73 instrument (`.claude/skills/ui-walk/walk.mjs` plus one hook: when `AX6_MODULE` is set it imports that module after sign-in and skips stock routes). `ax6_walk.mjs` is the walk (FWD-4, FWD-5 button, FWD-7); `ax6_print.mjs` is the print GET. The walker's own `secret` call, network guard and disarm `finally` are unchanged: 0 guard aborts. Every data read is a GET with the page's own bearer. The module aborts, in the browser context, any document request to a host that is not localhost or an Opal CloudFront/opalinvest host, so no third-party page loads.
- Positive control on every capture: the record carries `location.pathname` and the five tab labels read from the DOM (`data/captures.json`): 9 of 9 captures carry the route; 4 of 4 security-page captures carry all five labels `Thesis, Exec Management, Peers, Model, Posture` (the 5 `/freshness` captures have no tabs and carry `/freshness`).
- Walk stamps (gitignored under `tmp/ui-walk/`, never committed): `20261006T083846Z` (the walk: 9 screenshots; 0 guard aborts, 0 API issues; the 2 console errors are the sign-in page's 401s before login); `20261006T084238Z` (the print GETs: 3 PDFs, 0 screenshots). The first run's Print-button click also fetched the PDF, but Playwright `response.body()` of that blob read 0 bytes (the same limit r73 recorded), so the bytes come from the second run's page-side GET (the call `requestPrintPack` makes), as in r73.
- The order cites PRD lines `:505-507`, `:521-525`, `:539-542`; at the bytes the FWD-4, FWD-5 and FWD-7 DONE WHENs sit at lines 522, 531 and 549. Text quoted below is read at those lines (prd_version v0.40).

## FWD-5 -- three rendered prints (BA, AMD, ASML_NA)

DONE WHEN (quoted, v0.38 text in the PRD): "EXERCISED -- (v0.38) a seat prints the pack on demand for three covered names, and each reads as a document: Opal Brand form, every figure traceable to its page field, no raw code, no dashboard chrome (a JUDGMENT read at L9). Adam's actual forward stays the ACCEPT"

- The Print button was pressed on `/security-analysis/<key>` for BA US, AMD US and ASML NA (captures `fwd5-<key>-print-modal`: route and five tab labels present). The same GET `/api/scoped/amgt/security/<key>/print` was then read for bytes: BA 139,161 bytes, 23 pages; AMD 146,408 bytes, 25 pages; ASML_NA 151,417 bytes, 26 pages; 200 and `application/pdf` on 3 of 3. Saved to `print/BA_US_Equity.pdf`, `print/AMD_US_Equity.pdf`, `print/ASML_NA_Equity.pdf`.
- Form, read from the PDFs with PyMuPDF and by eye on rendered pages: Letter pages (612 x 792 pt); one family, Lato (Regular 9 pt for body, Bold 11 pt for section headings, Bold 14 pt for the title); every text span in ink #163372 (navy); no images; 44-47 vector drawings per file (the thin rules under the title and each heading); no logo, no colour fill, no header or footer band.
- Layout: title "<NAME> [<KEY> Equity] Research Note" (on AMD it wraps, "Note" alone on the second line); then "Model figures" with sub-headings "Header" and "Fiscal year 2016" through "Fiscal year 2028"; each field is one line "Label: value - as of <date> - Bloomberg" in a single left column, long lines wrapped with a hanging indent; then "Recommendation", "Company description", "Investment thesis", "Risks and considerations", "Management/Board". Units are in words ("USD 152,984.0 million", "7,458,798 shares", "3.04x").
- Last five sections read, on all 3 names: "No recommendation has been written for this company yet." / the Bloomberg company description (BA, 1 paragraph) / "No investment thesis has been written for this company yet." / "No risks or considerations have been written for this company yet." / "No chief executive or board biography has been written for this company yet." On the BA page in the same walk the Thesis tab shows an Investment thesis card (2 points), a Risks card (3 points) and a Recommendation card (9 points, labelled a machine draft). Row `AMGT_RESAPP-Z-W256-S1`.
- Measured (PyMuPDF; the patterns are counted on the PDF text): upper-case underscore code tokens 0 of 3; figures with 5 or more decimals 0 of 3; Python repr marks 0 of 3. "as of" dates: 743 of 743 (BA), 820 of 820 (AMD), 856 of 856 (ASML_NA) read 2026-10-06, including lines under Fiscal year 2016-2024 headings. Page figures match: BA page Price USD 193.56 and Market cap USD 153B against print "USD 193.56 per share" and "USD 152,984.0 million".
- Not read here (judgment): whether it reads as an Opal Brand document and has no dashboard chrome. The page face the print opens from (Print and Export buttons at the top right of the Security Analysis page) is a separate capture.

## FWD-7 -- the /freshness page

DONE WHEN (quoted, v0.39 in the PRD): "EXERCISED -- (v0.39) a seat opens the one place on demand, sees every covered company with its last-refreshed date, and finds a stale one without opening any folders. Adam's own use stays the ACCEPT"

- Route `/freshness` (nav "Freshness"). Captures `fwd7-freshness-first`, `-sort-Stalest first`, `-sort-Freshest first`, `-sort-Company name`, `-second`.
- First paint of the table, from navigation start (`page.goto` begin to the first `tbody tr`): **9,135 ms** cold (DOMContentLoaded at 173 ms; the `/api/scoped/amgt/freshness` read started at 756 ms and took 8,139 ms, 1,065,906 bytes encoded, 2,850,172 decoded). Second visit in the same session: 1,993 ms (read 545 ms). r73 read 11,958 ms to the first row.
- Seen: 95 rows; columns Company, Last refreshed, Bloomberg, Seeking Alpha, Web search, Research pack, Stale; summary line "95 of 95 covered companies have an input that is stale (older than 7 trading days, or never read)." and "Web search is not collected yet." Every Last refreshed reads 2026-10-04 (1 distinct value). 92 rows read "Seeking Alpha has never been read" and 3 (Alibaba BABA, Boeing BA, Costco COST) "Seeking Alpha last read 2026-09-11". 95 of 95 rows carry the stale flag. Three sort buttons (Stalest first pressed by default, Freshest first, Company name). No folder is opened to see any row.
- A stale name is found without opening a folder, but the flag does not separate one name from the rest. The page now draws a light ground with dark text and a left purple rule on the title (the r73 capture's dark-navy card is gone). Row `AMGT_RESAPP-Z-W256-S2`.

## FWD-4 -- BA's feed, one link followed out

DONE WHEN (quoted, v0.40): "EXERCISED -- an analyst has read one and followed it out"

- HARVST gold #6 has landed: BA's served `/overlay` feed is `coverage_status SERVED`, 78 items, 72 with a `url` (not 0), read in 12,523 ms. The page markup holds 78 `[data-feed-item]` and 72 with an anchor `href`.
- On the page (`fwd4-BA-feed`, route `/security-analysis/BA_US_Equity`, five tab labels): the card "RECENT NEWS -- NEWEST FIRST (SEPTEMBER 7TH, 2026 TO OCTOBER 6TH, 2026)" shows one item open, "Why Boeing Stock Isn't Up More After Good FAA 737 MAX News", "Barron's -- October 5th, 2026, 8:54a ET", and "Expand (77 more)".
- Followed out: the first item's anchor reads `href=https://www.barrons.com/articles/boeing-stock-price-faa-737-max-glitch-9f4dea6d`, `target=_blank`. The click opened a new tab whose first URL was that address; the browser context aborted the third-party document request (1 request aborted, the Barron's URL), so the popup read `chrome-error://chromewebdata/` and the portal tab's URL did not change. Stopped at the target URL; no third-party page loaded.
- Of the first 5 items, 4 carry a link; the second (The Wall Street Journal, "How a Boeing 737 MAX Survived a Nosedive...") has no `url` and prints as plain text. 6 of 78 BA items have no link. Record: `data/fwd4/fwd4.json` in the stamp.

## Rows filed

`AMGT_RESAPP-Z-W256-S1` (print form vs page: thesis, risks, recommendation and the as-of date), `AMGT_RESAPP-Z-W256-S2` (/freshness: 95 of 95 flagged, timing). Both OBSERVATION, INERT, `disarm_owner` `2.0.0_SA_COO~Z`.
