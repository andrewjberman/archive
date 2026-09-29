# DSGN_AMGTV1 round 4 -- the close walk (the COO's one real run)

**Seat:** 2.0.0_SA_COO~D (site Z). **Round:** 4 (decomposition v4, AV-w-1..6, all complete). Round 4 was resumed after
the 11:34 ET machine crash.
**Build walked:** port 5174, 1.0.0_SA_CTO~Z's walk worktree `/c/tmp/amgt-walk-5174` at 6d77d55c. It contains site-Z portal
DEV 09bd04b1 (`--is-ancestor` true; CTO~Z msg 26664), which carries every round-4 portal commit: 873afa81 w-2, 92d1b243
w-6, 9912c1ac w-3, 8f2c2293 w-4, a538d0b7 w-5.
**Instrument:** `/ui-walk` (walk.mjs at CLOUD, which now carries AV-w-1's WALK VOID guard), signed in as the dormant walker
account and armed and disarmed by the walker itself.

| walk | names | window | artifact (gitignored, site Z only) | verdict on the instrument |
|---|---|---|---|---|
| C | VLO US, INTU US, SAP GY | 19:13:45Z-19:17:38Z | `tmp/ui-walk/20260929T191345Z/` | VALID. "walk void: no": no step landed on the sign-in page (the guard is live, so this zero is proven). 103 shots, 156 observations, 0 guard aborts, 0 API issues, 2 console errors (the two login 401s). The disarm is proven: "LOGIN WITH THE WALK PASSWORD AFTER DISARM: HTTP 401 -> REFUSED"; `status` then read disabled and SSM ABSENT. |

One walk covered all three names, where round 3 needed two: the session held throughout. Screenshots never leave site Z.

## Static checks on the merged bytes (CLOUD + portal DEV 09bd04b1, repo root, 2026-09-29 ~19:15Z)

```
SIGN-IN DETECTOR: 6 of 6 cases
TICKERS AS WRITTEN: 5 of 5 arms
MODEL STATUS WORDS: 3 of 3 arms
EXEC BAND AND DETAIL: 3 of 3 arms
POSTURE EVIDENCE IN WORDS: 3 of 3 arms
HISTORY VIEW: 5 of 5 arms (series 12)
W2 BOUND 2 of 2 | W3 BOUND 2 of 2 | W4 BOUND 4 of 4 | W5 BOUND 2 of 2 | W6 BOUND 4 of 4
FWD-30 HARNESS READS THE REDESIGNED PAGE: YES          (AMGT_RESAPP vv-5.AC1)
tsc -p . --noEmit: 0 errors                            (after each of the five portal merges)
```

## The non-prose census (census.cjs, the CVO's instrument; not a verdict)

```
header: 0 of 183 | lead: 0 of 33 | thesis: 0 of 174 | exec: 0 of 54
model: 4 of 911 (status words 0) [["P/E",2],["P/B",1],["Revenue/Sh",1]]
posture: 4 of 438 (status words 2) [["[status] ABSENT",2],["Inc.'s",1],["2026-2027",1]]
NON-PROSE CENSUS: 8 token(s) over 6 surface(s)
```
Round 3 read 6. The instrument now has a status-word class, which round 3's did not, so the two counts are not the same
measure. On the Model face the status words read 0, where round 3 had 20+ "REFUSED --" lines on SAP GY. The two left on
Posture are listed below.

## What the walk shows, per judgment criterion (observations for L9; the COO grades none of them)

- **AV-w-2 AC3 (FWD-2).** The Trending x Price list (shot 004) prints "BP/ LN" and "WALMEX* MM" whole, as Bloomberg writes
  them.
- **AV-w-3 AC4 (FWD-11).** SAP GY Model (shot 093): the score tiles read "Robustness score / Peer valuation score / Forecast
  divergence score -- Not measured yet". The 19 unit-refused lines read "In the research pack, but this page cannot show it
  yet because its unit is not set up here." The absences read "No year-on-year growth rows: the pack carries none ...",
  "2026E, 2027E, 2028E: not in the pack -- it carries fiscal years 2016 to 2025 only.", and "Upside case: not in the pack
  yet -- the method is to be agreed." The Model header is white. Two of the score names were the worker's reading of the
  letter codes ("Peers V" -> "Peer valuation score", "Divergence D" -> "Forecast divergence score"), because `types.ts`
  does not define them.
- **AV-w-4 AC3 (FWD-7, FWD-11).** INTU Exec Management (shot 051): the header is white, not a band. "Read detail" opens to
  "Where we looked: the company's 10-K, section 'Item 10. Directors, Executive Officers and Corporate Governance' (filing
  0000896878-26-000037). The section did not list officers in a form this page can read." It is followed by the served
  reason, verbatim: "no declared shape read this section (4 usable line(s), 0 candidate(s)): neither a narrative entry per
  officer nor a Name/Age/Position or Name/Year/Year table."
- **AV-w-5 AC3 (FWD-10).** SAP GY Posture (shot 099): the comparable's gaps are said once, as three bullets plus "The
  comparable's evidence is incomplete: 3 source(s) are missing from ANET US's pack." The cites read "Operating margin,
  FY2025: 26.1332%", "Free cash flow, FY2025: 8,264 million" and "Net debt: -2,213 million".
- **AV-w-6 AC3 (FWD-3).** The Trending x Price chart (shot 005): one legend (the buttons below the chart), thinned dates and
  one line per name. The served window carries **10** names ("10 name(s) across 6 landed days"), not 12. No company name is
  served, so every label is the ticker as written. The CVO grades the pick-and-follow and the colour separation (the
  WALMEX* MM stroke sits close to VLO US's orange).

## Seen on the walk, not in round 4's rectangle (inputs for the round-4 analysis)

1. **Posture fit-score cites print a preset code and a status word:** "fit score PFOE: no score (status ABSENT; 0 of 16
   factors present (16 code(s) named by the preset))" (SAP GY, shot 099, reason 5). This is the census's 2 status words.
2. **Posture cite-not-resolved lines print passage ids:** "no served drafted sentence on this name's thesis carries passage
   P0102 ..." (shot 099, reasons 1-3).
3. **The lead chart's generations line prints status words and a generation id:** "Generations across 30 date(s): 24 ABSENT,
   6 SERVED; latest 2026-09-28 generation 20260929T111053Z-1947cb2f921e" (shot 005). The census does not cover this line.
4. **The Exec "Read detail" still carries the served machine reason verbatim** after the new words (shot 051): "no declared
   shape read this section (4 usable line(s), 0 candidate(s)) ...".
5. **The walker's design:bands check reads 2 bands on the load and lead-panel steps only (9 steps).** It never fires on a
   name's tabs, so the Exec header is resolved. The pair is the lead panel and its darker source footer (shots 001-009).
6. **FWD-3 labels need a served company name.** The chart and the list label by ticker because the rank series carries no
   `name` (the cell declared `name?` optional). This is a producer ask, not a page change.
7. **Carried, unchanged:** format:money ("USD 1,234" / "$1,234" inside drafted prose on INTU; the contract forbids rewriting
   served prose), format:dates ("2026-09-22" / "September 22nd, 2026"), design:contrast (1-4 elements under 3:1 on the
   Thesis windows, for example the "Company description" caption on the dark header).
