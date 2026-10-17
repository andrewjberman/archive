# AMGT_RESAPP round 114 -- the issuer's real-browser walk of the INTEGRATED candidates (`bu-1`, `bu-2`, `bu-4`), `2.0.0_SA_COO~R1`, 2026-10-17 ~23:2xZ

Evidence outside the repository: `C:/dev/ui-walk-evidence/r114-int/` (`walk1.txt`, `run/` = the walker's output folder with 84 screenshots, `findings.json`, `crop_cue_icicibc.png`, `devserver.log`). Client data stays local; nothing here is a screenshot.

## 1. What was walked

A scratch worktree `C:/dev/int-r114` cut at PROD `d1bed0fb` with the three portal candidates merged in (no conflict): `a3f2b727` (bu-1), `9a8ef5e451` (bu-2), `dac528b0` (bu-4); integrated head `468b64d6` (scratch, never pushed, never registered). `bun run dev:live --port 5174` served it (a fetch of `priceCurrency.ts` and `ModelTab.tsx` from the dev server confirmed `currencyCodeOf` and `data-grid-scroll-cue`). The walker, a throwaway copy with the 20-click cap raised to 80 (deleted after), on `/security-analysis` for RIO LN, ICT PM and ICICIBC IN (the name with the fewest figure mnemonics, the CTO's msg 7767 read), `--open-first "All figures"`. The walk was not void (0 guard aborts; the account was armed once and DISARMED at 23:26:45Z, a login with the walk password after disarm refused HTTP 401).

## 2. Results

10 unique findings from 50 observations. Against the round-113 close walk of PROD `d1bed0fb` (11 findings):

| class | at PROD `d1bed0fb` | on the integrated build |
|---|---|---|
| `format:dates` | 1 (ICT PM: the scalar next-earnings row printed ISO) | **ABSENT** |
| `occluded-popover` | absent | absent |
| `layout:clipped` | 2 (ruled by design, row S60) | 2 (151 on RIO LN, 149 on ICT PM; unchanged, the same ruling) |
| the rest | `control-missing`, `truncated`, `timeline:no-day-bar`, `timeline:no-event-element` x3, `unconnected-field withheld` x2 | the same classes, the same routing (S59, DSGN's and AIFILL's) |

- **The scroll cue is visible:** the crop `crop_cue_icicibc.png` reads `All figures` with `Scroll sideways to see every year.` directly under it, above the year header row (read from the full-page shot of ICICIBC IN, Model tab expanded).
- **W503-S1, the CTO's rule (msg 7767) applied:** the `All figures` fold on the smallest-mnemonic name ICICIBC IN rendered **113 table rows** (RIO LN 145, ICT PM 143; the walker's `OPEN-FIRST` count). The rule says 20 or more closes W503-S1 NOT A DEFECT: it does. Caveat stated: the walker counts every table row in the fold, including heading rows and the rows that say the research team keeps no workbook for a line; `gridFigureRows` in `ModelTab.tsx` excludes the absent-reason rows, so the figure-row count is lower than 113 and was not separately counted. The clip needs an upward bubble within a bubble's height of the scroller's top, and a grid of 113 rows is thousands of pixels tall.
- **The thumb:** the walker runs headless Chromium, which hides scrollbars (row S60), so the screenshot cannot show a thumb. Instead a probe (`thumb_probe.mjs`) loaded the dev server's own transformed `src/index.css` plus the scroller's exact class string from `ModelTab.tsx` into a bare page and read `getComputedStyle(el, '::-webkit-scrollbar-thumb')`: a plain `overflow-x-auto` control reads `rgba(0, 0, 0, 0)`; the grid scroller reads `rgba(24, 36, 62, 0.35)` and `scrollbar-color` `rgba(24, 36, 62, 0.35) rgba(0, 0, 0, 0)`. **A first run of the probe read transparent for both, because the bare page did not define `--palette-navy`** (the portal defines its palette tokens somewhere the transformed stylesheet does not carry, which I did not locate); the second run defined it by hand (`221 44% 17%`) and the reading above is the second. So the cascade is proven (the trailing-bang utility beats the unlayered global `::-webkit-scrollbar-thumb { background: transparent }`), the colour is not the page's own token value, and a thumb on the running page is NOT looked at.

## 3. Not verified

- The live site (nothing is pushed or promoted yet); a staff login on the live page.
- The thumb on the running page, in a headed browser.
- The four date bypasses deferred by `bu-2` to `ModelTab.tsx` and `PeersTab.tsx` (rows W505-S1 and S2) are not shown by this walk (no `format:dates` finding on the three names in the states walked); the walk does not prove they print nothing in other states.
- Any name other than RIO LN, ICT PM and ICICIBC IN; every What Changed pair.
- The printed pack (`bu-3` is not served: `AMGT-bu-7`).
