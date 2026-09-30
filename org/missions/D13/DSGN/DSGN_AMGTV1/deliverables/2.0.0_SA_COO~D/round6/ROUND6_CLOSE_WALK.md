# DSGN_AMGTV1 round 6 -- the close walk (the COO's one real run)

**Seat:** 2.0.0_SA_COO~D (site Z). **Round:** 6 (decomposition v6, AV-u-1..5, all complete).
**Build walked:** port 5174, 1.0.0_SA_CTO~Z's walk worktree at e45fd9b2. It contains site-Z portal DEV fd4deb75
(`--is-ancestor` true, re-read by this seat; CTO~Z msg 26777), which carries every round-6 portal commit: 955fe079 u-1,
938df6af u-2, 42869c60 u-3, ae1be3c8 + ecaa197e u-5. u-4 is the walker itself, at CLOUD.
**Instrument:** `/ui-walk` (walk.mjs with AV-u-4's `--thread`, `lead-lists.json` and timeline steps), signed in as the
dormant walker account and armed and disarmed by the walker.

| walk | what | window | artifact (gitignored, site Z only) | verdict on the instrument |
|---|---|---|---|---|
| control | `round6/checks/walkvoid.sh`, signed OUT | 23:20:48Z | (the check's own run) | YES. Walker rc=3, 1 WALK VOID line, 0 account lines. |
| E | `--thread "Valero"`; names VLO US, INTU US, SAP GY, 992 HK; routes /security-analysis, /market, /positioning, /philosophy | 23:21:12Z-23:26:56Z | `tmp/ui-walk/20260929T232112Z/` (156 shots, `lead-lists.json`) | VALID. "walk void: no". 223 observations, 0 guard aborts, 0 API issues. Console: the 2 login 401s plus 1. Disarm proven: "HTTP 401 -> REFUSED", and `status` read disabled with SSM ABSENT. |

## Checks on the merged bytes (CLOUD + portal DEV fd4deb75, repo root, ~23:22Z)

```
TIMELINE PANEL IN WORDS 3/3 | POSTURE PHRASING IN WORDS 3/3 | HISTORY DOTS AND NAMES 3/3 | WALK GRADES BY NAME 3/3
FWD-30 ATTRIBUTES 3/3 | U1 2/2 | U2 2/2 | U3 3/3 | U5 7/7 (bounds) | FWD-30 HARNESS READS THE REDESIGNED PAGE: YES
tsc -b --noEmit (portal/): rc=0, 0 errors after each of the four portal merges
NON-PROSE CENSUS: 17 tokens over 8 surfaces (30 at base 4f927ad0; the census now carries a machine-phrase class)
AMGT_RESAPP sweep.py --only SAP_GY/VLO_US/INTU_US: FWD-30 GRADE: equal 3 of 3 identified names; cases page=9 rich=9 same=9
```

## What the walk shows, per judgment criterion (observations for L9; the COO grades none of them)

- **u-4 AC3, DSGN FWD-1 (the thread, shots 013-017).**
  - The walker found Valero's row by its served company name, "Valero Energy Corp" (#2 in Trending x Price, shot 013); no
    `thread:name-not-found`.
  - It then opened the header's four cards (014), the Financials window (015), the Thesis as the driver-chart state plus
    three cards (016), and the Recommendation window (017).
  - Shot 016's card reads "THE RESEARCH TEAM'S BASE CASE IS NOT IN THIS PACK / A MACHINE DRAFT, NOT THE RESEARCH TEAM'S VIEW".
- **u-4 AC4, DSGN FWD-2 (`lead-lists.json`, shots 002-012).**
  - Trending x Chatter: 2 rows, 2 named.
  - Trending x Price: 10 rows, 3 named (Valero Energy Corp, Petroleo Brasileiro SA, ASML Holding NV); the rest print the
    ticker as written.
  - Breakout x Chatter: 0 rows.
  - Breakout x Price: 10 rows, 2 named.
  - Each row shows name (where served), ticker, the period figure and its window. **No row shows Opal's asset class,
    sub-asset class, sector or places moved**, which FWD-2's ACCEPT names.
- **u-4 AC5, DSGN FWD-11 (the side-by-side, shots 144-156).**
  - Market (144), Positioning (145-150, its five duration windows opened) and Philosophy (151-156, its five pillars opened)
    were walked with the same checks.
  - The walker reads design:bands **10** on Market, **6** on Positioning and **2** on Philosophy, against 0 on Security
    Analysis's name steps.
  - It reads design:contrast 46-50 on Positioning.
  - The reference pages break C3 themselves; the CVO judges which pieces are "the same".
- **u-4 AC6, AMGT_HARVST FWD-5 (shots 019, 051, 084, 116).**
  - On each name the walker pressed the newest day bar. VLO's 2026-09-29 is a denied day: the dissection reads
    "2026-09-29'S ARTICLES, STRONGEST FIRST / DENIED DAY -- RETRIEVAL WAS DENIED FOR THIS DAY / No articles this day."
  - No walked name's newest day carried articles, so "articles strongest first" was reached only as its empty state.
- **u-4 AC7, AMGT_HARVST FWD-6.** `timeline:no-event-element` on all four names: the panel builds no event layer, so no
  marked event with a headline is on the page.
- **u-1 AC3 (FWD-5, FWD-11).**
  - The legend reads "COMPLETE -- PARTIAL -- DENIED" in band ink with colour swatches (shot 019).
  - No failed call occurred on this walk (0 API issues), so the error state was graded only by timeline.cjs's planted 500.
  - No walked day was PARTIAL, so the "Searched: ..." line appears only in the check's served-fixture render (992 HK wsj,
    ASML sa).
- **u-2 AC3 (FWD-10).** The Posture cites and footer on SAP GY, in the walk's Posture shots.
- **u-3 AC3 (FWD-3).** The "-Chart-picked" shots 004, 007 and 012: unpicked lines' dots now mute with their lines.

## Seen on the walk, not in round 6's rectangle (inputs for the round-6 analysis)

1. **FWD-2's row columns are not built.** No list row shows asset class, sub-asset class, sector or places moved. Is that a
   page cell, a producer ask, or both? Whether the served list rows carry these fields is unmeasured by this seat.
2. **HARVST FWD-6 (marked events) has no page element.** The panel builds no event layer, which is a page cell once
   HARVST serves the events.
3. **HARVST FWD-5 is reached only on denied or empty days.** A name with articles on a walked day is needed to grade
   "strongest first" on pixels.
4. **FWD-11's reference pages break C3** (10 / 6 / 2 bands) and read 46-50 low-contrast elements on Positioning. The CTO
   rules what "the same pieces" means against pages that do not meet the law themselves.
5. **Carried:** "$1,234" in INTU drafted prose; two date forms, the long one in served prose; low-contrast captions on the
   Thesis windows (8 contrast findings, mostly the same captions).
