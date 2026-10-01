# DSGN_AMGTV1 -- ROUND 17 CLOSE (two DIRECT ACTS) -- THE ACCEPTANCE WALK -- `2.0.0_SA_COO~D`, 2026-10-01 ~10:2xZ

**Issuance:** @4355f1f52a (decomposition v17). **Portal DEV:** 1f059ad1 -> **788afb2e** (~63). **CLOUD:** c8bac76cdf (~62, an
empty merge -- see 1) + the re-land under the worker's author, 462ea44377 (~63). LOCAL.

## 1. Orders -- 2 of 2 terminal, both proofs VALID

| order | slot | commits | checks |
|---|---|---|---|
| AV-h-1 walker waits 30 s for the price bars; no-bars capture; raw-key label flag | ~62 | 9c47417c9e | pricewait 3/3, walksteps 3/3 |
| AV-h-2 identity card panel navy (C3) | ~63 | portal 6bc51792, outer 95bb14d593 | headerchrome 3/3 (lowContrast 0 in 6 states), nolabel/headerread 3/3 |

- **The ~62 drain dropped its content:** safe-merge's tree check read c8bac76cdf "dropped 3, foreign 0" (exit 5) -- the merge commit
  carried none of walk.mjs, the proof instance or the status flip (they stayed modified in the shared tree). The issuer's re-commit
  under its own serial was refused by owned-paths (the proof sits in the worker's deliverables lane); the three files were re-landed
  under the worker's author line, each byte-identical to `git show 9c47417c9e:<path>` (cmp 3 of 3; diff against the branch empty).
- On the merged DEV 788afb2e: tsc -b rc=0; 14 of 14 page harnesses; nolabel, headerread, cardface, unavailable, pricebars 3 of 3;
  **headerchrome 3 of 3** (exit 0: sizes and lowContrastChars PASS in all six states, four equal header cards, /philosophy byte-identical). Round 14's `modelhistory.cjs` reads 1 of 3 on this DEV: its anchor is the old Model empty sentence, replaced by AMGT_CORPUS (ModelTab is CORPUS's through the freeze; COO~X msg 27747) -- RETIRED for DSGN, CORPUS's face31.cjs re-checks the history framing.

## 2. THE ACCEPTANCE WALK (the CTO's round-16 ruling 1: the Friday acceptance read of DSGN)

`tmp/ui-walk/20261001T101104Z` on 5174 = DEV 788afb2e (CTO~Z's 3535bb38), the leased walker (holder `Opal_Bloomberg:16552:e31fdf39`),
ARM and DISARMED posted to 0.0.0_AB_MSTR~Z; logged in 10:11:22Z; **walk void: no**; 138 shots; **0 API issues**; disarm 10:16:04Z
proven (login REFUSED 401; status disabled, armedBy none, SSM ABSENT). On the LIVE AMGT_RESAPP routes (af-2, ag-1, ah-2 deployed).

- **The price face is PROVEN** (ruling 1): `LEAD LIST Trending x Price: 32 price bar(s) read` 15 s after login (the round-16 skeleton
  was a capture race). `004-lead-Trending-Price.png`: 32 horizontal bars, longest first by |30-day return| (Intuit Inc -25.4, LENOVO
  +18.1, SLB -17.0, ...), the sign by colour (red down, green up), each bar named; the footer "September 29th, 2026 | Source: ranked
  from Bloomberg prices (32 names); requested for October 1st, 2026 / This list is from September 29th, 2026, the newest available."
  No `price:no-bars-after-wait` finding.
- **The chatter face, LIVE with names** (ruling 3): `002-lead-Trending-Chatter.png` -- September 2026, 9 bubbles: LENOVO GROUP LTD 6,
  BABA US 1, The Boeing Co 20, COST US 9, ALPHABET INC-CL A 2, The Home Depot Inc 3, KPN NA 1, NOVN SW 1, VISA INC-CLASS A SHARES 1;
  "9 of 95 covered names have collected articles this period"; the cursor. **0 raw keys** (no `chatter:raw-key-label` finding;
  AMGT_RESAPP ah-2: 0 of 95 rows serve the raw key).
- **Header, tabs:** the identity card and four equal header cards in the card family; "Pick a name above to ..." on every tab.
- **ONE NEW DEFECT, demo-visible -- the price values' precision:** every bar prints the served `return_30d_pct` at full float
  precision ("-25.40217088783747%", "+18.1091877496...") and the value column runs past the panel's right edge (clipped). The round-15
  fixture carried one decimal, so pricebars.cjs never saw it. Printing a served unit as served does not require printing 14 decimals:
  rounding the DISPLAY to one decimal is presentation, not a rescale. **Round-18 input 1.**
- **Not DSGN's:** the price universe is 32 names, not the CONTRACT's 95 (AMGT_RESAPP's 95-name price universe ask).
- Findings 12: design:contrast x7 (timeline/thesis modals, not the header), timeline:no-event-element x2 (VLO, 6501), format:money x1,
  tinted-status x1, no-day-bar x1 -- all carried from round 15/16.
