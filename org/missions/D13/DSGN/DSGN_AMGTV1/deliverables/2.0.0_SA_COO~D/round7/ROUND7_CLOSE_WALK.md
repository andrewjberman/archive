# DSGN_AMGTV1 round 7 -- the close walk (the COO's one real run)

**Seat:** 2.0.0_SA_COO~D (site Z). **Round:** 7 (decomposition v7, AV-s-1..4, all complete).
**Build walked:** port 5174 at 11691b1b, which contains site-Z portal DEV ab7e1e49 (`--is-ancestor` true, re-read by this seat;
CTO~Z msg 26834). ab7e1e49 carries every round-7 portal commit: 69737463 s-1, 2ab4329f s-2, c019d279 s-4, 0f9780a5 s-3.
**Instrument:** walk.mjs at CLOUD @4a0628755b. That is AV-s-3's `--day` plus the AV-v-2 and AV-u-4 steps the issuer restored
after the integrator merge 8b3f8e8833 dropped them (row Z-S4).

| walk | what | window | artifact (gitignored, site Z only) | verdict on the instrument |
|---|---|---|---|---|
| control | `round7/checks/walkvoid.sh`, signed OUT | 01:25:47Z | (the check's own run) | YES. Walker rc=3, 1 WALK VOID line, 0 account lines. |
| F | `--thread "Valero"`, `--day "992 HK=2026-08-13"`; names VLO US, INTU US, SAP GY, 992 HK; routes /security-analysis, /market, /positioning, /philosophy | 01:26:05Z-01:31:58Z | `tmp/ui-walk/20260930T012605Z/` (158 shots, `lead-lists.json`, `timeline-days.json`) | VALID. "walk void: no". 325 observations, 0 guard aborts, 0 API issues. Disarm proven: "HTTP 401 -> REFUSED", and `status` read disabled with SSM ABSENT. |

## Checks on the merged bytes (CLOUD + portal DEV ab7e1e49, ~01:26Z)

```
NO-CALL POSTURE IN WORDS 3/3 | ONE FOOTER FORM 3/3 | TIMELINE NOT SEARCHED AND EVENTS 3/3 | WALK OPENS A DAY BY DATE 3/3
LEAD COLUMNS AND NO PASS BADGE 3/3 | U1 8/8 | U2 5/5 | U3 3/3 | U4 5/5 | FWD-30 HARNESS READS THE REDESIGNED PAGE: YES
walker checks after the restoration: round5 pickstep 3/3, round6 walkthread 3/3, round7 walkday 3/3, round4 detect 6/6
tsc -b --noEmit (portal/): rc=0, 0 errors after the three round-7 portal merges
NON-PROSE CENSUS: 20 tokens over 14 surfaces (40 at base fd4deb75; the census now covers all four walked names)
```

## What the walk shows, per judgment criterion (observations for L9; the COO grades none of them)

- **s-1 AC4 (FWD-11), 992 HK (shots 116, 141).** The header reads "Posture (as of 2026-09-16): No call on this name yet -- no
  comparable company could be matched to this name yet". No file name, `AMGT-s-1` or `F2/G-24` is on the face.
- **s-2 AC4 (FWD-11).** The header card and Thesis window footers are in the walk's window shots (the thread's 015 and 017, and
  every `-open-` shot).
- **s-4 AC4 (FWD-2, FWD-11) (`lead-lists.json`, shots 002-012).**
  - Every served row now shows asset class and sub-asset class, e.g. "Valero Energy Corp VLO US +8.54% (...) equity Energy"
    and "992 HK ... equity Information Technology".
  - The unserved columns (sector, places moved) are named once.
  - Named rows are unchanged at 7 of 22, and Breakout x Chatter still serves 0 rows.
- **s-3 AC4 (HARVST FWD-5, FWD-6), 992 HK (shots 116-118).**
  - **FWD-6 is on the page.** Under "COVERAGE EVENTS -- PRESS ONE TO OPEN ITS FIRST DAY" the three served events read with
    their headline, dates and article count, e.g. "Lenovo Posts Record Revenue, Expects to Hit $100 Billion Goal This Year --
    2026-08-13 to 2026-08-14, 3 articles".
  - The legend reads "COMPLETE -- PARTIAL -- NOT SEARCHED". The day tooltip reads "2026-08-13: not searched on this day -- 2
    found anyway".
  - VLO, INTU and SAP GY record `timeline:no-event-element`, meaning no events are served for them.
  - **FWD-5 on pixels is NOT reached.** The 2026-08-13 day opened under "2026-08-13'S ARTICLES, STRONGEST FIRST" (shot 116),
    and the event's day 2026-02-12 opened the same way (shot 118). In both screenshots the article list is a LOADING
    SKELETON, and `timeline-days.json` reads `pressed: true, article_rows_in_page_order: []`.
  - The day routes answered HTTP 200 (`netlog.tsv`: `/timeline/day/2026-08-13` and `/2026-02-12`).
  - So the list had not rendered when the walker's 1.5 s settle took the shot. **Whether that is walker timing or the page not
    rendering a served day is unproven either way**; round 5 taught this seat not to read a mid-load shot as a defect.
- **u-4's thread (FWD-1)** was re-walked by name through the five hops (shots 013-017).

## Seen on the walk, not in round 7's rectangle (inputs for the round-7 analysis)

1. **FWD-5 on pixels:** the walker must wait for the day's article rows, or for a failed or empty state, before its shot.
   Otherwise "strongest first" cannot be graded. A static render of the served day (timeline7.cjs arm 1) lists the
   articles, so the page renders the served shape.
2. **FWD-2 residual:** sector and places moved are not served (AMGT_RESAPP asks); named rows 7 of 22 (ruling 7's crosswalk
   ask).
3. **FWD-11 residual:** the reference pages still read 10 / 6 / 2 bands (ruling 3: their owners). Carried: "$1,234" in
   drafted prose, and low-contrast captions on the Thesis windows.
