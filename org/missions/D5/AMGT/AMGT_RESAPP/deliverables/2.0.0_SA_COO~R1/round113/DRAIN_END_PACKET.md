# AMGT_RESAPP round 113 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FILLED, 2026-10-17 ~22:2xZ; every order cut in round 113 is terminal (`bt-1`, `bt-3`, `bt-5`, `bt-6` complete; `bt-2` complete with its REAL grade NOT MET; `bt-4` is the issuer's reads).** Round 113 is the CTO's round-112 analysis for the R1 track (`ledger/ROUND_ANALYSIS.round112.R1.md`, msg 7733), issued at `e3ce07f86d` under this seat's keys (decomposition s.122 and its AMENDMENT 1). `python .tools/round-close-check.py --project AMGT_RESAPP --round 113` reads `orders=6 judgment=0 graded=0 ungraded=0 verdict=MAY-CLOSE`: the round carries NO judgment criterion, so no L9 grade is owed; the packet is the L8 compile and the ground for your L10 slug. Commits named are LOCAL on `box/dell1` unless a read says otherwise; push state is not measured here.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bt-1` | the earnings row and its detail print dates in the house long form (S59 class 8) | complete | worker ~500 (merged 2a575f68cd); candidate `cand/dell1/amgt-sa-earnings-long-dates` @c4e4f96af3, `WhatChangedPanel.tsx` three lines; fresh-checkout re-runs `EARNINGS LONG DATES HARNESS YES (7 of 7)`, `CHANGED LIST VALUE YES (16 of 16)`, `CHANGED OBJECT CELLS YES (6 of 6)`; row 5058; DEV `1847fff5` |
| `AMGT-bt-2` | the first candidate for items 2 and 3 (tooltip z-index, label wrap) | complete -- **real grade NOT MET** | worker ~501 (merged 3eb59201d4); the harness 6 of 6, but the issuer's real-browser walk of a build of the candidate read `occluded-popover` 3 of 9 and `layout:clipped` 151/149 UNCHANGED; the walker's own diagnostics showed the grid's `overflow-x-auto` scroller clips the bubble, no stacking trap; NOT registered, NOT promoted (findings under `C:/dev/ui-walk-evidence/r113-bt2/`) |
| `AMGT-bt-6` | the recut of item 2: the last `min(12, floor(N/2))` rows' figure tooltips open upward | complete | worker ~503 (merged 422eb8d52f); candidate `cand/dell1/amgt-sa-model-tooltip-last-rows` @be136f28eb; fresh-checkout `MODEL TOOLTIP ROWS HARNESS YES (9 of 9)`; the CTO's grade (the walker on the built page): `occluded-popover` ABSENT in two walks; row 044d; DEV `eea01c16` |
| `AMGT-bt-3` | the shared price-currency helper trims a padded served code (W497-S2) | complete | worker ~502 (merged 27beeaea9c); candidate `cand/dell1/amgt-sa-price-currency-trim` @4f8299bddd, `priceCurrency.ts` two lines; fresh-checkout `PRICE CURRENCY RULE HARNESS YES (7 of 7)` and `PEERS CURRENCY HARNESS YES (6 of 6)`; row 3af9; DEV `b7cae4b8` |
| `AMGT-bt-4` | the item-4 reads | issuer reads, done | `round113/READS_ITEM4.md` @4be78400c2: truncated names reachable by title and aria-label (read in source); FWD-6 exercised on RIO LN; a printed pack for three names read (PDFs 24 pages, 0 mnemonics), ISO days observed |
| `AMGT-bt-5` | the chosen-set PROD promote and the fold-back | complete | H2: PROD `856fb37b` to `d1bed0fb` (the three features), CI run 39073112254 success, tag `portal-v2.1.238`; fold-back under the CTO's one-time named waiver (@1b1fbd5af0, 121 shas, row a997): DEV `eb2c7b20168f` (issuer's fetch and `ls-remote` read), DEV tree unchanged, `origin/DEV..origin/PROD` = 0; AC1-AC4 PASS |
| `AMGT-bp-5` | (carried) the G4 positive-arm read | NOT DUE: Mon 2026-10-19 after the 11:30Z fire | instrument `round109_prep/checks/r109_g4_positive_arm_read.py` @7bec5b4251 |

Item 3 of the CTO's list (`layout:clipped`) is NOT a cell: ruled by the CTO (msg 7741): a scrolling `overflow-x-auto` grid is not clipped text; the walker's probe is corrected by its owner (row `S60`); a visible scroll affordance is a round-114 candidate.

## 2. The issuer's real runs

- **Live site tied to PROD `d1bed0fb` by bytes** (`round113/LIVE_TIE_AND_CLOSE_WALK_D1BED0FB.md` @c7f3c75c64): `index.html`, six entry assets and the Security Analysis chunk `index-BMOOpovu.js` (250371 bytes) byte-equal to run 39073112254's artifact; `bt-6`'s class string `bottom-full left-0 z-10 hidden pb-1` is in the served chunk and in 0 chunks of the previous deploy's artifact (a content-level marker, which round 112 lacked).
- **Close walk on a local build of `d1bed0fb`** (RIO LN, ICT PM, GOOGL US): the first attempt VOID (a sign-in redirect), the second valid: 11 findings; **`occluded-popover` ABSENT**; `layout:clipped` unchanged at 2 (ruled); **`format:dates` 1 left, ICT PM only** (RIO LN's states no longer fire it).
- **Real-browser grading of a cell the harness had passed** (the CTO's rule): `bt-2` passed its harness and failed the walk; the diagnosis (a patched throwaway walker printing the ancestor chain and the clip container) located the cause and produced `bt-6`, which passes the walk.

## 3. Findings for your judgment (read, none graded by the issuer)

1. **A second `format:dates` instance** (CTO msg 7759: goes on round 114 in the long form with the same grade): ICT PM's What Changed row `Date of the issuer's next expected earnings report (a DATE, not a number)` prints `2026-11-06` and `2026-11-11` as ISO; `bt-1` changed only the earnings-dates LIST.
2. **The printed pack prints ISO days** (51 per PDF, read in `READS_ITEM4.md`): a served-path candidate on the print renderer (`lib/research/print`), the CTO's to want.
3. **The scroll affordance** (round 114, CTO msg 7741): the grid's horizontal scrollbar thumb is transparent until hover and sits 9291 px down the page; a bounded-height scroller or a visible cue, graded on a built page.
4. **`W502-S1`:** `PeersTab.tsx` passes the served `PX_LAST` currency to `formatStatValue` for the subject price cell outside the helper, so a padded code prints with two spaces on that one cell (no live name is padded; round 114).
5. **`W503-S1`:** a grid under about 20 figure rows could still clip an upward bubble at the scroller's top (arithmetic, unmeasured; RIO LN has 60).
6. **Row `S60`** (the walker-probe instrument row, for the walker's owner) and **S59's** routed classes (DSGN's timeline classes; the AIFILL class) are unchanged by this round.

**Not verified by the issuer:** the live site read with a staff login; `bt-1` and `bt-3` in the served chunk by a content marker (existing helper, a trim adds no string); the truncated names' full text on a live hover (read in source); every name's What Changed rows (the walk read three names).

## 4. Open and carried

- Round 114 (the CTO's analysis, after your slug): the scalar date row, the scroll affordance, the `PeersTab` subject-cell bypass, the short-grid limit.
- **`AMGT-bp-5`** Mon 2026-10-19; **A4 step 1** not before Tue 2026-10-20; **the Lusha plan tier** (Andrew); row `S57` (the fold-back verb) is the portal manager's (NFRA_DEVPLN), and every fold-back waits on a named waiver until it exists.
