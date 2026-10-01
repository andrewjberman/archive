# DSGN_AMGTV1 round 10 -- the close walk (the COO's one real run)

**Seat:** 2.0.0_SA_COO~D (site Z). **Round:** 10 (decomposition v10 + AMENDMENT 1; AV-o-1..4 complete, o-3 re-opened and complete
again).
**Build walked:**
- Walk I: 5174 @6a9ce827, which contains DEV 5810586a.
- Walk J: 5174 @c1ef440d, which contains DEV 2bb60cc3 = walk I's build + the AMENDMENT 1 repair.
- Both were re-read by this seat: `--is-ancestor` true and `/` 200 (CTO~Z msgs 26944, 26978).

**Instrument:** walk.mjs at CLOUD (unchanged since round 8).

| walk | what | window | artifact (gitignored, site Z only) | verdict on the instrument |
|---|---|---|---|---|
| control | `round10/checks/walkvoid.sh`, signed OUT, before each walk | 05:56Z, 06:33Z | (the check's own run) | YES both times. Walker rc=3, 1 WALK VOID line, 0 account lines. |
| I | thread Valero, `--day "992 HK=2026-08-13"`; VLO, INTU, SAP GY, 992 HK, IMB LN, AZN LN, 6501 JP; the four routes | 05:56:58Z-06:05:37Z | `tmp/ui-walk/20260930T055658Z/` (221 shots) | VALID, disarm proven. Found row Z-S5 (below). 6501 never opened: only `/security/6501%20JP/peers` was requested, and every 6501 shot is a loading skeleton. |
| J | the same, with TSM US for 6501 | 06:33:47Z-06:42:12Z | `tmp/ui-walk/20260930T063347Z/` (242 shots) | VALID, disarm proven: "HTTP 401 -> REFUSED", and `status` read disabled with SSM ABSENT. 0 guard aborts. The one API issue is a 500 on `/api/scoped/advisor-intelligence/platinum/firm/leaderboard.json` (another page's route, not this project). |

## What walk I found, and the repair (row Z-S5 -> Z-S6)

- **AZN's Model tab (shot 192) read "Opal's opal's historical-multiple reference".**
  - Cause: three literal BACKSPACE bytes (0x08) where regexes meant `\b`.
  - `ModelTab.tsx:295` came in with o-3.
  - `HeaderBrief.tsx:48-49` has been there since round 1, so no description source ever read "from Bloomberg".
  - tsc and all 16 harnesses passed them. cases.cjs arm 2 asked only that a line START with "Opal's" (a named blind spot).
- **The repair:**
  - A new order file was refused by to-pipeline-gate LIMB 6 (one issuance per round), so the repair rides AV-o-3 AMENDMENT 1
    @c13bb7407f. It added AC4 = `round10/checks/bytes.cjs`.
  - It drained at CLOUD 4813813e75 / DEV 2bb60cc3.
  - CTO~Z read 0 files with 0x08 over all 991 portal src code files.

## Checks on the merged bytes (CLOUD + portal DEV 2bb60cc3, ~06:30Z)

```
ONE HOUSE DATE FORM 3/3 (0 visible ISO over 45 surfaces) | DOSSIER FIELDS ON THE PAGE 4/4 | TEAM CASES AND OPAL'S RULE CASES 3/3
NO SCALE ON AN UNRESOLVED UNIT 3/3 | NO CONTROL BYTES, LABELS READ RIGHT 3/3
kept: round 9 grain / strength / oneform / sidebar 3/3 each; round 8 daystate 3/3 | SIGNED-OUT CONTROL YES
tsc -b --noEmit (portal/): rc=0 after each of the five round-10 portal merges
```

## What walk J shows, per judgment criterion (observations for L9; the COO grades none of them)

- **o-1 AC3 (FWD-11), every date:**
  - The header reads "identity as of September 29th, 2026", and the posture line "Posture (as of September 16th, 2026)".
  - The timeline heading reads "DENSE FROM JANUARY 1ST, 2026", with axis ends "January 1st, 2026" and "September 29th, 2026",
    and "SEPTEMBER 29TH, 2026'S ARTICLES".
  - The news window reads "SEPTEMBER 1ST, 2026 TO SEPTEMBER 30TH, 2026", and the tabs "Updated September 30th, 2026".
  - The walk's `format:dates` check no longer fires (1 hit on walk G, 0 on walks I and J).
- **o-2 AC3 (CORPUS FWD-10/11/15/16/18):**
  - IMB's Thesis tab (walk I shot 147) heads "THE RESEARCH TEAM'S THESIS PILLARS". It shows six pillars, each with "Source:
    Imperial Brands Research Pack 2026 07 17_v1" and, where served, "Terms: ...".
  - The header and the Posture tab read "Fund of record: IDVZ; last stated position: Potential ADD in IDVZ (currently ~2.5%)."
  - TSM (walk J shot 204) shows two pillars ("Source: TSMC research pack 4_30_2026") and "No fund of record is stated in the
    research team's pack."
  - For the grader: IMB's machine posture reads "No call on this name yet" beside the research team's stated "Potential ADD in
    IDVZ". Both are on the face, each labelled whose.
- **o-3 AC3 (CORPUS FWD-12), AZN's Model tab (walk J shot 192):**
  - "THE RESEARCH TEAM'S BASE / UPSIDE / DOWNSIDE CASE", each a table as written with its source.
  - Beneath them: "Opal's rule-based upside: the method is to be agreed.", "Opal's historical-multiple reference: quote currency
    'GBp' and reporting currency 'USD' differ and this block converts nothing." and "Opal's rule-based downside: the method is to
    be agreed."
  - No "not in the pack yet" line appears beside a served team case.
- **o-4 AC3 (RESAPP FWD-30):**
  - TSM's header card (walk J shot 204) reads "Enterprise value TWD 71,993,494.73 (unit not resolved)".
  - The measured control, AZN's Financials window (shot 194), reads "USD 281B" and "USD 23.88B".
  - Per CTO~Z msg 26927, about a quarter of figures show raw until AMGT_CORPUS round 23; the walk expects that.
- **FWD-1 thread** was re-walked by name.

## Seen on the walk, not in round 10's rectangle (inputs for the round-10 analysis)

1. **FWD-11, machine words still on the face:**
   - the Posture tab reads "no pack for IMB_LN_Equity is carried in packs on this object" (a key and "on this object");
   - AZN's timeline reads "No chatter_daily rows exist for this security_key yet";
   - TSM's header shows "Price USD 451.15" beside "Enterprise value TWD ..." (two currencies on one face, as served).
2. **6501 JP never opened on walk I:** the search pick requested only `/peers` for "6501 JP". A resolution issue for that ticker,
   or the walker's pick, is unproven either way.
3. **Andrew-direct via COO~H (msg 26928):** a mention counter wherever articles display. The day list shows "named N times" since
   round 9; whether a more prominent counter is wanted is for Andrew, who picks up with this seat directly.
4. **Carried:** FWD-2 names on 7 of 22 rows and the driver series (AMGT_RESAPP r51); the `/timeline/day` latency (HARVST n-6).
