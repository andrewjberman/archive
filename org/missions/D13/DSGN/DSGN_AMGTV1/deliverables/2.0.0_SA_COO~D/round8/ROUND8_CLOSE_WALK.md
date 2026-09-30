# DSGN_AMGTV1 round 8 -- the close walk (the COO's one real run)

**Seat:** 2.0.0_SA_COO~D (site Z). **Round:** 8 (decomposition v8, AV-q-1..3, all complete).
**Build walked:** port 5174 at fa5ba517, which contains site-Z portal DEV 29c8226a (`--is-ancestor` true and `/` 200, both
re-read by this seat; CTO~Z msg 26855). 29c8226a carries both round-8 portal commits: 761deafa q-3 and fac7c101 q-2.
**Instrument:** walk.mjs at CLOUD @ac0fdbfc16 (AV-q-1's `waitForDayState`, ceiling 20,000 ms).

| walk | what | window | artifact (gitignored, site Z only) | verdict on the instrument |
|---|---|---|---|---|
| control | `round8/checks/walkvoid.sh`, signed OUT | ~02:38Z | (the check's own run) | YES. Walker rc=3, 1 WALK VOID line, 0 account lines. |
| G | `--thread "Valero"`, `--day "992 HK=2026-08-13"`; names VLO US, INTU US, SAP GY, 992 HK; routes /security-analysis, /market, /positioning, /philosophy | 02:39:16Z-02:45:41Z | `tmp/ui-walk/20260930T023916Z/` (157 shots, `lead-lists.json`, `timeline-days.json`) | VALID. "walk void: no". 331 observations, 0 guard aborts, 0 API issues. Disarm proven: "HTTP 401 -> REFUSED", and `status` read disabled with SSM ABSENT. |

## Checks on the merged bytes (CLOUD + portal DEV 29c8226a, ~02:48Z)

```
WALKER WAITS FOR DAY STATE 3/3 | WALKER BOUND 3/3 | LEAD SOURCE LINE IN THE FOOTER FORM 3/3
CLASSIFICATION LABELS PER POSITIONING 3/3 | round 7 kept: LEAD COLUMNS AND NO PASS BADGE 3/3, ONE FOOTER FORM 3/3,
WALK OPENS A DAY BY DATE 3/3 | SIGNED-OUT CONTROL YES
tsc -b --noEmit (portal/): rc=0 after each of the two round-8 portal merges
```

## `timeline-days.json` -- every opened day, with the state the walker saw

| via | name | day | state | waited_ms |
|---|---|---|---|---|
| newest | VLO US | 2026-09-29 | empty | 1859 |
| newest | INTU US | 2026-09-29 | empty | 1856 |
| newest | SAP GY | 2026-09-29 | empty | 1637 |
| day | 992 HK | 2026-08-13 | rows (2) | 5309 |
| newest | 992 HK | 2026-09-29 | empty | 1593 |
| event | 992 HK | 2026-02-12 | rows | 5577 |

No day reached the ceiling and none read `failed`. The two days with articles took 5.3 s and 5.6 s, which matches the ~5.5 s
/timeline/day latency CTO~Z measured in the round-7 analysis.

## What the walk shows, per judgment criterion (observations for L9; the COO grades none of them)

- **q-1 AC4 (HARVST FWD-5, FWD-6), 992 HK.**
  - **2026-08-13 (shot 115):** "2026-08-13'S ARTICLES, STRONGEST FIRST", then "NOT SEARCHED ON THIS DAY", then two rows:
    - "Lenovo Posts Record Revenue, Expects to Hit $100 Billion Goal This Year" -- A, wsj, `2026-08-13T04:55:00+00:00
      (instant)`, in headline: yes, in lead: yes;
    - "Lenovo Group jumps on strong Q1 revenue, AI growth" -- A, sa, `2026-08-13T14:19:23+00:00 (instant)`, in headline:
      yes, in lead: yes.
  - **The event "Lenovo Posts Earnings Beat on AI-Driven Demand" opened 2026-02-12 (shot 117):** two rows, sa 16:28 then
    wsj 08:57, both A with headline yes and lead yes.
  - **Not a skeleton in either shot.** The day's articles are on pixels for the first time in this project.
  - For the grader: on both days the two rows carry the same visible strength marks (A, headline yes, lead yes), so the page
    shows no visible reason for their order. On 08-13 the rows run earliest first; on 02-12 they run latest first.
  - The article times print as raw ISO strings with "(instant)".
  - The event covers "2026-08-13 to 2026-08-14, 3 articles", and its first day lists 2.
- **q-2 AC3 (FWD-11), the footers side by side:**
  - lead lists (shots 002, 005): "Dated September 28th, 2026 | Source: ranked from Bloomberg prices (32 names); requested
    for September 30th, 2026". The next line reads "this list is older than the date requested, shown as such rather than
    silently".
  - header card window (shot 121, 992 HK Market features): "September 28th, 2026, 10:45p ET | Source: Bloomberg".
  - Positioning (shot 146): "September 28th, 2026, 5:00p ET | Source: Bloomberg." on all three panels; the model window
    (shot 147) prints "September 28th, 2026, 5:00p ET" with no source.
  - The lead line is date-only by ruling 4 (no clock is served). It is the only footer that starts with "Dated".
- **q-3 AC4 (FWD-2), a lead list beside the Positioning breakdown (shots 005 and 146):**
  - **The headers match:** both tables head their columns "Asset Class" and "Sub Asset".
  - **The values differ:**
    - Asset Class: Positioning shows "Fixed Income" and "Equity"; the lead list shows "equity" in lower case.
    - Sub Asset: Positioning shows sub-asset buckets ("Ultra Short Duration", "Short Duration", "High Yield", "Large"). The
      lead list shows sector names ("Energy", "Information Technology", "Utilities", "Consumer Staples").
  - So the lead list's "Sub Asset" column holds sector names under Positioning's heading. The unserved note reads "Not served
    for this list yet: Industry group (finer than Sub Asset), places moved since the last run."
  - One lead cell is truncated ("Communication Servic..."). BP/ LN shows "--" in both columns and has no company name.
- **FWD-1 thread** was re-walked by name through its five hops (shots 013-017).

## Walk check hits (20 unique; confirmed on the shots where listed above)

design:contrast 8, layout:truncated 3, design:bands 3, timeline:no-event-element 3 (VLO / INTU / SAP GY serve no events),
format:dates 1, format:money 1, design:tinted-status 1 (Breakout x Chatter: "No committed ranking ... on this date").

## Seen on the walk, not in round 8's rectangle (inputs for the round-8 analysis)

1. **FWD-2:** the lead list's "Sub Asset" column carries sector names, not Positioning's sub-asset buckets. The label now
   matches and the domain does not. Either serve Positioning's sub-asset value, or head the served field by its own grain.
   The asset-class value's case also differs.
2. **FWD-5:** with equal visible marks, "strongest first" has no visible tie-break, and the two days order their rows in
   opposite time directions.
3. **FWD-11:**
   - the raw ISO article times;
   - "Dated" as a prefix only on the lead line;
   - the lead list's second line about the date sounds like a system message;
   - the Positioning model window's footer has no source.
