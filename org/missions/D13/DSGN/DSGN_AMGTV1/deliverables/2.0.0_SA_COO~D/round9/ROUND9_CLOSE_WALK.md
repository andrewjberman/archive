# DSGN_AMGTV1 round 9 -- the close walk (the COO's one real run)

**Seat:** 2.0.0_SA_COO~D (site Z). **Round:** 9 (decomposition v9, AV-p-1..4, all complete).
**Build walked:** port 5174 at 5ce2867e, which contains site-Z portal DEV b6634ba0 (`--is-ancestor` true and `/` 200, both re-read
by this seat; CTO~Z msg 26898). b6634ba0 carries all four round-9 portal commits: 8c960dff p-4, 4414f159 p-1, 8a15fb90 p-3,
b5a31874 p-2. **Instrument:** walk.mjs at CLOUD @ac0fdbfc16 (unchanged this round).

| walk | what | window | artifact (gitignored, site Z only) | verdict on the instrument |
|---|---|---|---|---|
| control | `round9/checks/walkvoid.sh`, signed OUT | ~04:03Z | (the check's own run) | YES. Walker rc=3, 1 WALK VOID line, 0 account lines. |
| H | `--thread "Valero"`, `--day "992 HK=2026-08-13"`; names VLO US, INTU US, SAP GY, 992 HK; routes /security-analysis, /market, /positioning, /philosophy | 04:04:20Z-04:10:37Z | `tmp/ui-walk/20260930T040420Z/` (157 shots, `lead-lists.json`, `timeline-days.json`) | VALID. "walk void: no". 338 observations, 0 guard aborts, 0 API issues. Disarm proven: "HTTP 401 -> REFUSED", and `status` read disabled with SSM ABSENT. |

## Checks on the merged bytes (CLOUD + portal DEV b6634ba0, ~04:12Z)

```
COLUMN HEADED BY ITS GRAIN 3/3 | ARTICLE ROWS SHOW STRENGTH AND TIME 3/3 | ONE FOOTER FORM, PLAIN WORDS 3/3 (census 18 of 18)
SECURITY ANALYSIS UNDER TOOLS 3/3 | kept: round7 TIMELINE NOT SEARCHED AND EVENTS 3/3, ONE FOOTER FORM 3/3, WALK OPENS A DAY BY
DATE 3/3; round8 WALKER WAITS FOR DAY STATE 3/3, WALKER BOUND 3/3 | SIGNED-OUT CONTROL YES
tsc -b --noEmit (portal/): rc=0 after the four round-9 portal merges
```

## `timeline-days.json` -- every opened day

| via | name | day | state | waited_ms |
|---|---|---|---|---|
| newest | VLO US / INTU US / SAP GY / 992 HK | 2026-09-29 | empty | 1590-1606 |
| day | 992 HK | 2026-08-13 | rows (2) | 5848 |
| event | 992 HK | 2026-02-12 | rows | 5849 |

The two days with articles took 5.8 s. No day reached the ceiling and none read `failed`.

## What the walk shows, per criterion (observations for L9; the COO grades none of them)

- **p-1 AC3 (FWD-2), a lead list beside the Positioning breakdown (shots 005 and 146):**
  - The lead list heads its columns "Asset Class" and "Sector". It shows "Equity" beside "Energy", "Information Technology",
    "Utilities" and "Consumer Staples".
  - "Communication Services" wraps onto two lines, whole.
  - The note reads "Not served for this list yet: Industry group (finer than Sector), places moved since the last run."
  - Positioning's breakdown still heads "ASSET CLASS" and "SUB ASSET" over "Fixed Income" / "Ultra Short Duration" / "Large".
  - BP/ LN still shows "--" in both columns and has no company name (AMGT_RESAPP's names ask).
- **p-2 AC3 (HARVST FWD-5, FWD-11), 992 HK.**
  - **2026-08-13 (`timeline-days.json`; shot 115):** "Lenovo Posts Record Revenue, Expects to Hit $100 Billion Goal This Year"
    reads A, wsj, "named 8 times", "August 13th, 2026, 12:55a ET". "Lenovo Group jumps on strong Q1 revenue, AI growth" reads A,
    sa, "named 5 times", "August 13th, 2026, 10:19a ET".
  - **The event's day 2026-02-12 (shot 117):** sa "named 9 times", "February 12th, 2026, 11:28a ET", above wsj "named 7 times",
    "February 12th, 2026, 3:57a ET".
  - On both days the higher count leads, and no ISO time or "(instant)" is on the face.
- **p-3 AC3 (FWD-11), the lead footer beside a header card window (shots 005 and the `-open-` window shots):**
  - The lead footer reads "September 28th, 2026 | Source: ranked from Bloomberg prices (32 names); requested for September 30th,
    2026".
  - The line beneath it reads "This list is from September 28th, 2026, the newest available."
  - The header card windows are unchanged this round. They read "<long date>, <time> ET | Source: Bloomberg" per oneform.cjs's
    census (18 of 18), and on walk G's shot 121. I did not re-open a window shot on walk H.
- **p-4 (Andrew-direct; DIRECT-ACT, no L9), every signed-in shot:**
  - The Security Analysis icon, highlighted on this route, now sits in the lower (Tools) group, directly beneath the Security
    Scanner icon and above Portfolio Management.
  - In walk G (round 8) it sat in the upper (Analysis) group beneath Philosophy.
  - The route stays admin + Dev gated (CTO~Z msg 26898: App.tsx:134, routes :448-449).
- **FWD-1 thread** was re-walked by name (shots 013-017).

## Walk check hits (19 unique; 20 in walk G)

design:contrast 8, design:bands 3, timeline:no-event-element 3 (VLO / INTU / SAP GY serve no events), layout:truncated 2 (3 in walk
G; the classification cells no longer truncate), format:dates 1, format:money 1, design:tinted-status 1.

## Seen on the walk, not in round 9's rectangle (inputs for the round-9 analysis)

1. **FWD-11, ISO dates still on the 992 HK face (shot 117):**
   - "identity as of 2026-09-29";
   - "Posture (as of 2026-09-16)";
   - the timeline axis ("2026-01-01", "2026-09-29");
   - the coverage events ("2026-02-12, 2 articles");
   - the lead rows' movement windows ("(2026-08-31 -> 2026-09-28)");
   - the Thesis "Updated 2026-09-30";
   - the VLO Thesis source "filed 2026-02-25".
2. **Carried from the cut:** the bare-date "Dated" paths in `HeaderCards.tsx` / `ThesisCards.tsx`. They are unreached on served
   data.
3. **Queued by CTO~Z for this analysis:** the six outcomes' page render with whose-case labels (msg 26889), and "never print
   K/M/B/T on an UNRESOLVED unit" (msg 26894).
