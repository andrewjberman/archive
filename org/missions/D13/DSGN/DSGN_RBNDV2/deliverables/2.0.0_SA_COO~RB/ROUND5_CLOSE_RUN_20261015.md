# DSGN_RBNDV2 -- round 5 close run: Andrew's Market Overview fixes (criteria RB5X1-AC3 to RB5X6-AC3)

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 ~16:0xZ. **Branch read:** `feature/dsgn-rbndv2-light` @d0cb67d0 (LOCAL, never pushed), dev build at port 5174, against the real backend.
**Method:** the scratch UI walker copy (`walk-rbprobe.mjs`, untracked, deleted at this round's close; it takes a JSON step file in env `RB_STEPS`) signed in as the walker (armed, one load, one action, disarmed; the login after disarm was REFUSED, HTTP 401, every time), hovered or clicked, and read computed styles in the page. Source of the work: `ANDREW_DIRECT_20261015_MARKET_OVERVIEW_FEEDBACK.md` (his words verbatim, 11 items).

## Drain (merge-time checks)

| order | worker | proof (re-run in its worktree before the merge) | portal merge | workspace merge |
|---|---|---|---|---|
| RV-x-6 Trending Topics popup on the frame | ~18 | VALID | 906db9f4 | 4eb0cb2071 |
| RV-x-1 on-fill ink block (116 selectors) | ~13 | VALID | 9027a72d | f21447250a |
| RV-x-3 RSI panel, Trend case, select width | ~15 | VALID | merged before 5269d02c | aa63b3cb74 |
| RV-x-4 Fear and Greed dial, tile hover | ~16 | VALID | 5269d02c | 4b4fdb391d |
| RV-x-5 cloud glow, hover resolves to ink | ~17 | VALID | merged before d0cb67d0 | dbc174c3aa |
| RV-x-2 panel footer case | ~14 | VALID | d0cb67d0 | 9651b4b28a |

At the last portal merge: typecheck `tsc --noEmit` rc=0 (0 errors); `src/__tests__/dsgn-rbndv2` 14 pass 0 fail (11 files); panels, modal and market-performance test folders 18 pass 0 fail (18 files); eslint rc=0 on the touched files and the test folder. Every diff reviewed: 0 non-ASCII bytes added. Worktrees and worker branches removed; nothing pushed.

## Live reads (computed, on the running build)

| Andrew's item | read | result |
|---|---|---|
| 5 Tooltip text white on indigo (Index Performance history modal; Global RSI panel; Daily Cloud) | text elements of the indigo box | header and values `rgb(255, 255, 255)`, labels `rgba(255, 255, 255, 0.85)` in all three; the help-icon tooltip also `rgb(255, 255, 255)` |
| 1 Trend arrow white | tile arrows | `rgb(255, 255, 255)` inside `data-ink="on-fill"` (the old small trending icon in the header stays ink) |
| 4 Trending Topics popup in light mode | pressing a topic row | dialog on the light frame: white surface, 1368 by 765, title "Trending Topic"; 30 ink and 11 ink-3 text elements, signal colours for the figures, source chips white on the dark hero, hero arrow white |
| 3 Footers proper capitalization | six panel footers on `/market` | `text-transform: none`, letter-spacing normal, "October 15th, 2026, 7:20a ET \| Source: Bloomberg, CNBC, Financial Times, and more." |
| 6 Daily Cloud no glow | three words | `filter: none` |
| 8 RSI panel labels | SVG text and strokes | tick text `rgb(74, 88, 120)`, category names `rgb(10, 23, 51)`, marker strokes `rgb(10, 23, 51)` |
| 9 RSI Full view Trend and Asset Class | RSI modal, Full | Trend value "Cooling Down" with `text-transform: none`; Asset Class select 160 px wide with 36 px right padding |
| 10 Fear and Greed dial and text | gauge SVG | needle stroke and hub fill `rgb(10, 23, 51)`, Fear and Greed end labels `rgb(74, 88, 120)`, value `rgb(10, 23, 51)` |
| 11 Component Indicators hover | tile under the pointer | background indigo at alpha 0.1; other tiles unchanged |
| 7 Topic modal row title after a hover | NOT read live | the modal's analysis does not load for the walker (two runs, 30 s and 60 s, only the Close button rendered), so the check rests on the source: the leave handler now assigns `''` and no inline `style.color = 'white'` remains in any non-test `.tsx` file (the test walks 344 files) |

## Carried, not cut

- Item 2 (tooltip placement, `002b`): waits on Andrew. FWD-4 (heat maps): his answer is owed at this terminal (call `be0b` was closed by the CTO on his word that he answers it here).
- A footer source reads "Source: Global news." (`SentimentGauge.tsx` line 128); "proper capitalization" likely means "Global News". One-word fix batched into the next round's cell, not cut alone.
- The Fear and Greed and Trending Topics signal colours (green `rgb(25, 210, 154)`, yellow, orange on white) are the FWD-5 faint-colour population for his page-by-page walk; he has not named them yet.

## Surprise rows (workers' rows, all OBSERVATION)

`W13-S1` INERT (marker absent until x-6 merged: now present); `W13-S2` ARMED, disarm owner this seat: read live, the help tooltip text computes white, no defect; `W14-S1..S3`, `W15-S1..S2`, `W16-S1`, `W17-S1`, `W18-S1` INERT (commit gate does not grade `.tsx`; branch base was a descendant of the difference-control base).
