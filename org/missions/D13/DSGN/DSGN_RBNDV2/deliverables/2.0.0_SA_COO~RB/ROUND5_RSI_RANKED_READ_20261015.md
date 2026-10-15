# DSGN_RBNDV2 -- round 5: the RSI modal's Ranked view, read live (CTO round-4 analysis @93c3fb9a2f, enrichment item 1)

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 13:3xZ. **Branch read:** `feature/dsgn-rbndv2-light` @7f8731df (LOCAL, never pushed), dev build at port 5174.
**Method:** the scratch walker copy (`walk-rbprobe.mjs`, untracked, deleted at round close) signed in as the walker, clicked a Global RSI chart bar (`.recharts-bar-rectangle path`, 3 matches), pressed the dialog button **Ranked**, and read the computed colour of every text element in the dialog and of every SVG text element. Disarm was REFUSED after each run (HTTP 401).

## What the Ranked view holds

- 141 text elements (Spotlight view: 53). `.recharts-wrapper` count **0**; SVG text elements **0**; the two `svg` nodes are icons. **The Ranked view draws no chart, so it has no axis label and no tick.** (The CTO's analysis expected axes there; the finding corrects that.)
- Computed text colour by element count: ink `rgb(10, 23, 51)` 83 (names, rows, chip labels), title `rgb(22, 51, 114)` 1, active chip `Ranked` white `rgb(255, 255, 255)` on violet 1 (intended). **No text is white or white-alpha on the silver or white surface.**
- Signal colours on the white surface: green `rgb(34, 197, 94)` 4, lime `rgb(132, 204, 22)` 14, orange `rgb(249, 115, 22)` 16, yellow `rgb(234, 179, 8)` 12, red `rgb(239, 68, 68)` 2, plus `Hottest` / `Coldest` labels at 0.7 alpha green and red (`oklab(...) / 0.7`) 8. These are the FWD-5 population (faint signal colours), held on Andrew's YES to call `3c44`.

## Disposition of the CTO's cell

The cell reads "press Ranked, read one axis label and one tick against the ink tokens; if white on silver, fix and re-read". The read finds no axis or tick in this view and no white-on-silver text, so the fix branch is vacuous and **no task order is cut** (no cell is cut for coverage alone). `W10-S2` (RSI reachable, Spotlight has no axis) is now read for Ranked: no defect. The Full view was not read (the run was cut at the 170 s timeout; the walker was left armed by the killed run and disarmed by hand with its holder token, status disabled).

## Walker note

A killed walk leaves the account armed: `ui_walker_account.py disarm <holder>` with the `armedBy` holder token from `status` clears it. The post-disarm login is REFUSED.
