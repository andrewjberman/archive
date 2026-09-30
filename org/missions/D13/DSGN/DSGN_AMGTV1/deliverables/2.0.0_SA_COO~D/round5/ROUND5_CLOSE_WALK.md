# DSGN_AMGTV1 round 5 -- the close walk (the COO's one real run)

**Seat:** 2.0.0_SA_COO~D (site Z). **Round:** 5 (decomposition v5, AV-v-1..7, all complete).
**Build walked:** port 5174, 1.0.0_SA_CTO~Z's walk worktree `/c/tmp/amgt-walk-5174` at 6d316332. It contains site-Z portal
DEV 4f927ad0 (`--is-ancestor` true, re-read by this seat; CTO~Z msg 26725), which carries every round-5 portal commit:
ba7cd986 v-1, e7856b79 v-2, 0848d989 v-3, 9e327c9f v-4, 6efecd75 v-5, 80ca02af v-7, b8d0d3c5 v-6. The walk condition,
AMGT_RESAPP ww-1's V1 leg, has held since 19:56:55Z.
**Instrument:** `/ui-walk` (walk.mjs at CLOUD, now carrying AV-v-2's pick step), signed in as the dormant walker account and
armed and disarmed by the walker itself.

| walk | what | window | artifact (gitignored, site Z only) | verdict on the instrument |
|---|---|---|---|---|
| control | `round5/checks/walkvoid.sh`, signed OUT | 21:47:10Z | (the check's own run) | YES. Walker rc=3, 1 WALK VOID line, 0 account lines. |
| D | VLO US, INTU US, SAP GY, signed in | 21:47:28Z-21:51:14Z | `tmp/ui-walk/20260929T214728Z/` | VALID. "walk void: no". 106 shots, 155 observations, 0 guard aborts. **1 API issue:** GET `/api/scoped/amgt/security/INTU_US_Equity/timeline` returned HTTP 500 on the INTU Exec step, a served endpoint. Console: the two login 401s plus that 500. Disarm proven: "HTTP 401 -> REFUSED", and `status` read disabled with SSM ABSENT. |

## Static checks on the merged bytes (CLOUD + portal DEV 4f927ad0, repo root, ~21:48Z)

```
POSTURE CITES IN WORDS 3/3 | HISTORY PICK, EDGE AND COLOURS 3/3 | WALK PICKS A NAME 3/3 | GENERATIONS LINE AND ONE BAND 3/3
WHOSE BASE CASE 3/3 | MODEL READS THE SERVED WORDS 3/3 | PARITY ADMITS THE WORDS CASE LINE 2/2
ONE DATE FORM AND A READABLE LEGEND 3/3 | EXEC DETAIL WITHOUT THE MACHINE REASON 3/3
V1 2/2 | V2 3/3 | V3 4/4 | V5 4/4 | V6 4/4 (bounds) | FWD-30 HARNESS READS THE REDESIGNED PAGE: YES
tsc -b --noEmit (portal/): rc=0, 0 errors after each of the four portal merges (the real typecheck; see the round-4 correction)
```

## The non-prose census (census.cjs round 5, the CVO's instrument; not a verdict)

The count was 34 tokens over 8 surfaces at base 09bd04b1 and is **17** now:
- `chart`: 1 ("30-day").
- `model`: 4 (P/E x2, P/B, Revenue/Sh; 0 status words).
- `posture`: 4 (ABSENT x2 inside served reason prose).
- `posture-sap`: 8 (served EUR money forms in drafted prose, two dashes, and 1 ABSENT inside served reason prose).
- All other surfaces: 0.

Every "ABSENT" left sits inside a served drafted reason ("Fit scores are ABSENT (unmeasured) ..."), which is producer
prose and not a cite line.

## What the walk shows, per judgment criterion (observations for L9; the COO grades none of them)

- **AV-v-1 AC3 (FWD-10, FWD-11), SAP GY Posture (shot 102).**
  - The six uncarried passages read "cite not resolved -- a filing passage the research pack cites, which no drafted
    sentence on this name's thesis quotes, so this page does not carry its text".
  - The carried passage names "the company's filing, ITEM 5. OPERATING AND FINANCIAL REVIEW AND PROSPECTS / paragraph 140".
  - The fit-score cites read "No fit score for this name on one of the model portfolios' screens yet: none of its 16
    factors has a value."
  - The membership cite reads "Held in 1 of the model portfolios at the 2026-09-15 snapshot."
  - No passage id or preset code is on the face.
- **AV-v-2 AC4 (FWD-3), Trending x Price chart (shot 006) and the same chart with a name picked (shot 007).**
  - The picked 992 HK draws full and thick; the other nine are muted. The last tick "2026-09-28" is whole.
  - The palette is 12 distinct saturated strokes (min CIE76 dE 44.8).
  - Labels are tickers, because no company name is served (producer ask (a)).
  - The muted lines' point dots stay bright (see input 3).
  - Picked shots also exist for Trending x Chatter (004) and Breakout x Price (012).
- **AV-v-3 AC3 (FWD-11), shots 006 and 001-012.**
  - The generations line reads "Of the 30 dates in the window, 6 have a published ranking; the latest is 2026-09-28."
  - The source caption sits in the panel body.
  - The walker's `design:bands` check no longer fires on any step (round 4: 2 bands on 9 steps).
- **AV-v-4 AC4 (FWD-6, FWD-11), SAP GY Model (shot 096).**
  - The tile reads "DIVERGENCE FROM CONSENSUS FORECAST".
  - The rule case prints its served label as served: "Historical-multiple reference: 159.61 EUR (...)".
  - **The research team's Base case is now SERVED on SAP GY:** a table headed "THE RESEARCH TEAM'S BASE CASE", covering
    2026E-2030E with EPS / Multiple / Price / Return, sourced to "SAP RESEARCH PACK 2026 06 12_V1".
  - So both cases show on the face, and each names whose it is.
- **AV-v-5 AC3 (FWD-7, FWD-11), INTU Exec (shot 054).** "Read detail" ends at "... The section did not list officers in a
  form this page can read." No machine reason is shown.
- **AV-v-6 AC3 (FWD-11).**
  - The Model header reads "Updated 2026-09-29" (shot 096).
  - The timeline legend's "PARTIAL -- DENIED" words sit on the band's lightened tokens.
  - `format:dates` still reads two forms, the long one being served prose ("September 22nd, 2026"), as ruled at the cut.
- **AV-v-7 (no judgment criterion).** The rule case's formula prints the producer's own words ("Bloomberg consensus EPS
  (FY1) x adjusted trailing-median P/E"), not the page's older local phrase ("adjusted consensus EPS").

## Seen on the walk, not in round 5's rectangle (inputs for the round-5 analysis)

1. **CORRECTED (~22:4xZ):** INTU's mention timeline answered HTTP 500, served `/timeline`, on the INTU steps. Shot 054
   caught the panel MID-LOAD, not failing. Shot 059 shows the designed error state rendering ("The timeline could not be
   loaded ... Try again"). The residual defect is the visible machine cause "Cause: API request failed: 500 Internal Server
   Error -". The first reading here, a loading skeleton in place of an error state, came from one mid-load screenshot and
   was wrong.
2. **SAP GY's research-team Base case reads "unit $ as written in the team's pack"** for a EUR-quoted name (shot 096), with
   figures 144.28-237.58. They are printed as served; whether the pack's unit is right is the research team's question.
3. **In the history view with a name picked, the muted lines' point dots stay full-strength white** (shot 007), so the
   unpicked series still read as dotted columns.
4. **"Fit scores are ABSENT (unmeasured)" survives inside a served drafted reason** (Posture reason 5), which is producer
   prose (C-PRESENTATION-ONLY).
5. **Carried:** "$1,234" in INTU drafted prose; `design:tinted-status` (a #253456 note block on the lead panel and on the
   Exec band); 2-3 low-contrast captions on the Thesis windows.
6. **Producer asks still open (AMGT_RESAPP round 49, ruling 5):** a served company `name` on the rank series (FWD-3's
   labels); officers from a second source (FWD-7).
