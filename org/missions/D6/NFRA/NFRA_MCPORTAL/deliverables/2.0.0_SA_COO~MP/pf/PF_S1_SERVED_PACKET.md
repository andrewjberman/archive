# NFRA_MCPORTAL -- S1 SERVED ARM (L8 input) -- 2.0.0_SA_COO~MP, 2026-10-16 ~11:0xZ

**Cell:** S1 = `MP-pf-4` (CTO PE+PF round-2 analysis, msg 34676): the served /gateway read. **Risk:** WORLD on the order, SERVED in the analysis. **Judgment criterion for the CVO:** S1 item (iii), legibility of the served page at 1280 and 390 px.
**State:** the segmentation is REALIZED on the served body; the served page FAILS the 390 px criterion on real data (row Z-S64, BLOCKING, below). Andrew's own signed-in look at mcp.opalinvest.dev/gateway (call 21d9) has NOT happened; this run is the served body through the page code, not the live page.

## The served arm (`pf4.served.sh`, PASS at ~10:57Z)

| limb | reading |
|---|---|
| 1. the deployed release carries the PF handler | `deployed_commit` 0cb4a87bcb (MX-r-15 landed 10:38:53Z on 3d5c9c8bf1, OG-ap-23 live 09:21:54Z): its blobs of `admin_gateway_breakdown.py`, `admin_people.py` and `test_admin_gateway_breakdown.py` equal the PF merge's (3 of 3), by CONTENT (ancestry is false for a release built by taking files whole, CLAUDE.md 22a); control: the old live d577e0e729's blobs differ (3 of 3) |
| 2. the bundle | `mcportal_commit` 090b9cdc85 descends from 421f8fb: yes |
| 3. a resolved segment is served | the served `_compute` (one read-only SSM command): **14 channels, 127 tools**, `opal-data-assets` with **8 segments**, each a resolved (vendor, firm): blackdiamond/49financial 3, blackdiamond/cottonwood 3, commonwealth/cottonwood 3, eclipse/inflection 1, orion/inflection 2, schwab/49financial 3, smartx/49financial 3, smartx/multi 1 (tool counts per segment; a tool serving several pairs is in several) |

Denominator and the page's own words: "14 groups, 127 tools ... 0 tool(s) declare no source". The earlier fear (four Schwab helpers in a red gap segment) did not occur: an integration spec wins placement (rule 1), so `schwab_describe_dataset`, `schwab_get_access`, `schwab_list_files` and `schwab_prepare_download` sit in the `schwab` integration channel, and `opal-data-bd` has no channel because its one tool belongs to the `blackdiamond` integration. My preview before the landing was wrong on that point (it did not apply rule 1).

## The one real run, for your grade (S1 item iii)

The SERVED body (read 10:59:30Z over SSM by `s1_served_body.sh`; every holder name redacted before anything was written) rendered through the real `GatewayView` and CSS at mcportal 090b9cdc85, looked at in a real browser.
Evidence, `deliverables/2.0.0_SA_COO~MP/pf/evidence_s1_served_0cb4a87bcb/`: `s1_1280_top.png` (the summary table: the eight segments indented under `opal-data-assets`), `s1_1280_card_smartx_multi.png` (a segment card), `s1_390_top.png`, `s1_390_page_scrolls_sideways_harvest.png`.
- **1280 px: reads well.** A summary table with each segment a link, then bordered cards with `Vendor / Firm` headings, counts, one-line tables.
- **390 px: FAILS.** `documentElement.scrollWidth` **561 against 390**: the page scrolls sideways. Cause (row **Z-S64**, BLOCKING, issuer-owned): `p.gateway-indexes`, the comma-joined index names of a channel, holds one unbroken name of about 65 characters, wider than its 328 px column, so six sections overflow (assets 530, etfs 382, harvest 438, portal-v2 433, Dynamodb 359, the Portal precomputed group 462) and widen the page. The MP-pf-2 fixture used short names (`idx-positions`), so its nine tests and my first render passed. The tables themselves hold (each scrolls inside its own box, the cue shows).
- **Cosmetic, unchanged:** a faint white band at a table's right edge (the cue's white cover on the light canvas).

NOT committed, on purpose: the full-page and assets-segment screenshots and the body JSON. The real index names carry Schwab master numbers (8-digit runs) and this box's client-data check is not running (row Z-S63), so I read every image before keeping it and kept only views with no 7-digit run.

## What the fix would be (not cut: a defect found at the close is the next analysis's first item)

One LOCAL mcportal cell: the Indexes paragraph scrolls inside its own box (`overflow-x: auto`), a real 60-plus character index name goes into the checked-in fixture so the 390 px render sees it, and one test pins both. I have asked the CTO to carry it.

## Still open

S1 stays NOT REALIZED until Andrew's signed-in look and your grade; the sign-in window for call f0d2 (MP-v-2, amended to the 12-route census @3ba8807816) waits on the word that Andrew is at the box.
