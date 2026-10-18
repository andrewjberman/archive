# AMGT_RESAPP round 122 -- the live hop: the CEO profile of TSM US and HD US read under a REAL login (no stub) on a local build of PROD `d729ee6d`, `2.0.0_SA_COO~R1` (`AMGT-cd-3`), 2026-10-18 ~18:2xZ

The CTO's round-121 analysis item 2: *one read of TSM US and HD US, on the PROD Security Analysis page and in the PDF, under a real staff login (no stub); the corrupt case stays a fixture.* Push state of every commit named: LOCAL on box/dell1, unread. Evidence (gitignored, outside the commit; research data, no client account): `tmp/ui-walk/20261018T182415Z/` (61 screenshots, `summary.md`) and `tmp/ui-walk/20261018T182820Z/probe-get.json`; `C:/dev/ui-walk-evidence/r122-walk.txt`, `r122-probe.txt`.

## 1. How (the sanctioned instrument, `/ui-walk`)

- **The build:** a scratch git worktree `C:/dev/int-r122` at PROD `d729ee6d` (portal-v2.1.241; the head the live site is tied to by bytes, `round121/LIVE_TIE_AND_PAGE_READ_D729EE6D.md`), served by `bun run dev:live --port 5174` (HTTP 200 before the walk). The walker refuses any base that is not `localhost`; the dev build reaches the LIVE data and the LIVE login (auth) front door through CloudFront: **the login is the real login hop, the data is the live data, nothing is stubbed.**
- **The login:** the dormant UI walker service account `opal-ui-walker@opal.test` (role admin, internal): ARMED by the walker at 18:24Z under its one-walk lease (the password is minted in process and never printed), `LOGGED IN`, walked, DISARMED: `OK: DISARMED at 2026-10-18T18:27:12.987876Z`, a login with the walk password after the disarm refused HTTP 401; the same for the second, short run (armed 18:28:22Z, `OK: DISARMED at 18:28:55Z`, the post-disarm login HTTP 401). The account reads `status=disabled armed=no` after both (read at ~18:30Z). 0 guard aborts (the walker admits GETs and four named POSTs only).
- **After the walks:** the dev server (PID of `scripts/dev-live.mjs`, port 5174) stopped and the port read free; the node_modules junction removed (its target untouched); the scratch worktree removed.

## 2. The page, read from the screenshots (Exec Management tab, the walker's own step shots `008-TSM-US-Exec-Management.png` and `038-HD-US-Exec-Management.png`)

| name | the CEO line the page prints (read) |
|---|---|
| TSM US | `CEO public profile: No CEO profile has been written for this company yet.` (below the officer table, under the `What is not on file` disclosure) |
| HD US | `CEO public profile (EDWARD P. DECKER): searched, nothing found -- The CEO web search returned 10 url(s), none of them on ir.homedepot.com, so no page could be confirmed as the company's own (a redirect or short link can hide where it leads).` |

Both pages loaded their real data (the identity header, price tiles, the research team's passage, the officer table), which the stubbed-session reads of round 121 could not (the stub showed an unloaded identity header). The two lines are the sentences the CTO named and equal the round-121 stub reads. The corrupt case stays a fixture (round 121).

## 3. The PDF under the same login

`--probe-get` (a same-origin GET from inside the signed-in page, with the page's own `authorization` header; only the header NAMES are written; a 2xx body is never kept) on the print route: **`/api/scoped/amgt/security/TSM_US_Equity/print?format=pdf` -> 200, 107766 bytes; `HD_US_Equity` pdf -> 200, 124242 bytes; `TSM_US_Equity` `format=rich` -> 200, 76535 bytes; the control without the headers: 401 on all three.** So the route answers a PDF to the real session and refuses the unauthenticated one. **The PDF's CONTENT under the login was NOT read** (the instrument keeps no body, and a download is not a click the walker makes); the printed CEO line of the two names is read from the SAME function by direct invocation, which is the 101-name census's source: TSM US `CEO public profile: No CEO profile has been written for this company yet.` and HD US `CEO public profile (EDWARD P. DECKER): The CEO web search returned 10 url(s), none of them on ir.homedepot.com, ...` in both the PDF and the rich export (`round122_prep/CEO_LINE_CENSUS_LIVE_BASE.md`, `cab11e50aa`). The byte counts of the probe (107766) and of my earlier direct fetch (113168) differ: a PDF carries its print day and its compression; no equality is claimed.

## 4. The walk's other findings (not graded here)

`summary.md`: 11 unique findings from 23 observations (classes: `unconnected-field` 3, `timeline:no-event-element` 2, `walker:control-missing` 1, `layout:truncated` 1, `walker:press-not-found` 1, `timeline:no-day-bar` 1, `format:dates` 1, `design:contrast` 1), 126 console errors, `walk void: no`. These are the walker's usual classes on these two names; nothing in them concerns the CEO line; the `--security-press` selector I passed matched no visible control (`walker:press-not-found`: my selector, not the page), and the walker's own per-tab step shots carry the Exec Management read. A walk grades nothing by itself.

## 5. Not verified

The live site opened by a staff person's own login (the walker's service account is the real login hop on a local build of the byte-tied head, not the browser on `www.opalinvest.dev`); the PDF's content under the login (above); names other than TSM US and HD US; the third sentence (an unknown reading) on the running page.
