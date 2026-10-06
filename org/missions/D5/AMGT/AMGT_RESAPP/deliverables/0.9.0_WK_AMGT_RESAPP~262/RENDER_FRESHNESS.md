# RENDER_FRESHNESS -- /freshness at portal 6de76f0509, round 76, `AMGT-az-1`

Served from `C:/tmp/r76-262/portal` (`bun run dev:live --port 5174`), signed in as the UI walker (role admin), 2026-10-06 17:56Z. The page read
`GET /api/scoped/amgt/freshness` (HTTP 200) and drew 95 rows. Guard aborts: 0. Walker disarmed 17:56:53Z (login with the walk password then
HTTP 401). Driver: `instrument/freshness_render.mjs` (row `AMGT_RESAPP-Z-W262-S1`). Every capture opens in a fresh browser context built from the signed-in state. Times are UTC.

**First-paint time (capture 1, 1280x900, fresh context):** browser first paint 288 ms; first contentful paint 620 ms; heading drawn 1645 ms;
table rows drawn 3010 ms; all from the navigation start. Recorded in `captures/first-paint-time.json`.

| file | what it shows | time |
|---|---|---|
| captures/01-first-visit-1280-full.png | /freshness first visit, fresh context, full page, 1280 px; default sort (stalest first) | 17:56:37Z |
| captures/02-sort-stalest-1280-full.png | "Stalest first" pressed. First five: AIA Group, Hon Hai 2317 TT, Tokyo Electron 8035 JP, Mitsubishi UFJ Financial Group 8306 JP, Sumitomo Mitsui Financial Group 8316 JP | 17:56:38Z |
| captures/03-sort-freshest-1280-full.png | "Freshest first" pressed. First five: Costco COST, Boeing BA, Alibaba BABA, Zurich Insurance ZURN SW, Zoetis ZTS US | 17:56:39Z |
| captures/04-sort-name-1280-full.png | "Company name" pressed. First five: Adobe ADBE US, AIA Group, Air Liquide AI FP, Alibaba BABA, Alphabet GOOGL US | 17:56:40Z |
| captures/05-uncollected-note-closeup.png | The summary line and the stated never-collected input above the table: "Web search is not collected yet." | 17:56:40Z |
| captures/06-row-cells-closeup.png | First row (stalest first), cells close up | 17:56:41Z |
| captures/07-width-1280-full.png | Full page at 1280 px wide (document scrollWidth 1280) | 17:56:44Z |
| captures/08-width-390-full.png | Full page at 390 px wide (document scrollWidth 390); the table's right-hand columns are cut at the card edge | 17:56:48Z |

Side files: `captions.txt` (first five rows per sort), `captures/contrast-readings.json`, `capture-manifest.json`.

Readings, no verdict (a JUDGMENT read is the CTO's):
- Summary line: "95 of 95 covered companies have an input that is stale (older than 7 trading days, or never read)."
- Contrast, computed at 1280: name, input and stale-flag cells ink rgb(22,51,114) on white = 12:1; the never-collected line ink rgb(168,177,194) on white = 2.16:1 (row `AMGT_RESAPP-Z-W262-S2`).
- The 01 and 02 images are byte-identical (stalest is the default sort).
