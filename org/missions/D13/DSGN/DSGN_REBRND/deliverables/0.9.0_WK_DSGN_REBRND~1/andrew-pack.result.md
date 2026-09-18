# DSGN_REBRND.TO-RB-s-15 -- Andrew's side-by-side pack: result

Worker `0.9.0_WK_DSGN_REBRND~1`, issuer `2.0.0_SA_COO~D`, 2026-09-14. Workspace worktree `C:/tmp/wk-dsgn-1k`, branch
`wk-dsgn_rebrnd-1k` (base 3327c5a890). AFTER portal `C:/tmp/wk-dsgn-1k/portal` @086371dd. BEFORE portal
`C:/tmp/wk-dsgn-before` @787015e8 (detached, read-only; `git status --porcelain` empty at the end).

## The pack

Open `rb-s-15_andrew-pack.html` in any browser. The PNGs sit beside it in this folder, and the page fetches nothing.
One composite image of the same page is `rb-s-15_pack_composite.png`.
`rb-s-15_pack_firstscreen_960.png` shows its first screen at 960 x 1080, half of a 1920-wide display, which is the
width it gets beside a competitor window.

The pack's first box is titled "Read this first: what this pack does NOT show". It says:
- the page bodies are still mostly dark-on-dark;
- no cell of this round inverted them (row `DSGN_REBRND-S2`; `portal/CLAUDE.md:44` counts 4,887 idioms);
- so the pair is not the finished rebrand;
- there is no data on either side;
- no competitor is captured.

The box sits wholly on the first screen at both widths (the renderer printed `bottom=353` of 1000 and `bottom=505`
of 1080).

The next box names what the AFTER side carries that Andrew asked for: the five identity accents (portal a7c4fa4f)
and the new favicon. It notes that the accents sit in the same places on the pre-round tree, so they look alike
across this pair. After that come a provenance table, the three pairs, and the old and new favicons at 64 px and
16 px.

| Route | BEFORE (portal 787015e8, port 5192) | AFTER (portal 086371dd, port 5191) |
|---|---|---|
| `/market` | `rb-s-15_market_before_1440.png` (capture 2 of 2) | `rb-s-15_market_after_1440.png` |
| `/positioning` | `rb-s-15_positioning_before_1440.png` | `rb-s-15_positioning_after_1440.png` |
| `/portfolio-management` | `rb-s-15_portfolio-management_before_1440.png` | `rb-s-15_pm_after_1440.png` |

Every capture used the AFTER tree's `scripts/ui-smoke.mjs`. The pre-round copy differs only in two `console.log`
lines, so the identity line's fallback applies. Every capture was 1440 x 900, full page, with no fixtures. The
canvas printed was `rgb(195, 202, 218)` on every BEFORE capture and `rgb(244, 246, 250)` on every AFTER capture.
All seven route PNGs were read, and so were the composite and the first screen.

## Criteria as run

- **RB15-AC1**: PASS by output. The verbatim invocation and its final output are in the proof instance's AC1 row;
  that run came after this file and the proof existed.
- **RB15-AC2**: PASS by output. `LOC   : /market`, `CANVAS: rgb(244, 246, 250) ...`, `rc=0`.
- **RB15-AC3**: PASS by output. `LOC   : /positioning`, `CANVAS: rgb(244, 246, 250) ...`, `rc=0`.
- **RB15-AC4**: PASS by output. `LOC   : /portfolio-management`, `CANVAS: rgb(244, 246, 250) ...`, `rc=0`.
- **RB15-AC5**: RECORDED as a judgment criterion (`UNVERIFIABLE-BY-INSTRUMENT`), for `3.0.0_SA_CVO` at L9. The
  grade of FWD-9 is Andrew's and is not given here.

## Controls

- **Negative arm for AC2-AC4:** the same script, routes and width on the pre-round tree printed a different canvas
  (`rgb(195, 202, 218)`) in 4 of 4 BEFORE captures, so the printed value moves with the tree.
- **AC1 arms:** on an empty deliverables tree the expression printed `VERDICT: ABSENT`; with one `x_pack.html` it
  printed `VERDICT: PACK-PRESENT`.
- **Determinism:** `/market` was captured twice per tree.
  - The AFTER tree gave the same settled state both times.
  - The BEFORE tree gave a spinner, then the settled error line (row `DSGN_REBRND-W1-S38`). The pack pairs the
    settled capture and keeps the spinner capture (`rb-s-15_market_before_1440_run1-loading.png`), disclosed on the
    page.
- **Pack render:** 10 of 10 images loaded, 18 `file:` requests and 0 non-file requests, on both runs.
  - The first run drew the favicons at 150 px, because a `figure img { height: auto }` rule overrode the `height`
    attributes. The fix uses explicit classes, and a full-size crop of the re-render shows 64 px and 16 px.

## Row filed

- `DSGN_REBRND-W1-S38` (OBSERVATION, INERT), committed alone at 8a43f2420b. On the pre-round tree, the `/market`
  tab body depends on capture timing even with equal inputs.

## Not done, by the order's own bounds

- No competitor site captured: that is egress.
- FWD-9 not graded.
- No page inverted (row S2).
- No data fixtures on either side.
- BEFORE `/positioning` and `/portfolio-management` captured once each.
- No portal write.
- Both dev servers were stopped: `taskkill` ended PIDs 37228 and 26828 and their children, and afterwards nothing
  listened on 5191 or 5192.
- `<WS>/.scratch/` stays uncommitted: the dev logs, the re-run captures, the AC1 mutant tree, and the row and
  composite scripts.
