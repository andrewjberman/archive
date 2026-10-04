# DSGN_AMGTV1 -- ROUND 35 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-04 ~21:4xZ) -- WHAT CHANGED IN WORDS, NO SYSTEM WORD, THE WORD CLOUD

**Input:** decomposition v35 and the issuance @f7ad5dc777, over PRD v0.15 @237d5d742f (ADMITTED). Rectangle: `round34/ROUND34_CLOSE.md`
section 4, per `1.0.0_SA_CTO~Z` msg 29179. Base: portal 055ba370, which landed on DEV meanwhile (MSTR~Z, DEV 2c792c27, CI 37234623154
success, msg 29239/29241). This round re-made after the 18:58Z site-Z crash; the first cut left nothing on disk.

## 1. THE CELLS (3 of 3 terminal, drained)

| order | cell | worker | portal | AC1 / AC2 (issuer re-run in the worker's tree) | outer drain |
|---|---|---|---|---|---|
| `AV-zm-1` | What changed in words (FWD-25, 27) | ~94 | 83a1d32ecf | changed35 5/5; battery29 0 skipped | b3b711eab6 |
| `AV-zm-2` | No system word on the face (FWD-27) | ~95 (light) | 9ccab6548d | payload35 4/4; battery29 0 skipped | 4e56f98b2f |
| `AV-zm-3` | The timeline's word cloud (FWD-5) | ~96 | ae19f161cd | cloud35 5/5; battery29 0 skipped | 67615038c1 |

Each proof instance is VALID (worker-side proof-of-spec-check rc=0). No rows were filed.

## 2. THE CANDIDATE -- portal `d60a0f90` (worktree 92, branch `dsgn-r35-onto-dev`, LOCAL)

The candidate is origin/DEV 2c792c27 (which carries 055ba370) plus the three cell branches, merged with `--no-ff` (efc8fe33, d53debb9,
d60a0f90). Against DEV it moves 12 files, all under `src/pages/SecurityAnalysis/`, +200/-31. Issuer run on the candidate:
- `round29/checks/battery29.sh` with no skip: ALL PASS (tsc 0, eslint 0).
- round 35: changed35 5/5, payload35 4/4, cloud35 5/5. round 34: labels34 4/4, repairs34 4/4, peername34 4/4.

## 3. THE CLOSE WALK -- `walk/closewalk35.mjs`, read-20261004T212050Z

Instrument: `round34/walk/gapread.mjs` copied whole, with two changes. FWD-24's sector/country control accepts the round-35 sentence.
A new read per name, `r35-faces`, probes the landing view and all five tabs for: the word cloud, the fixed phrase, rows printing
"-100.0%", and any visible "payload". Run on 5174 = d60a0f90 against the live API, 21:20-21:32Z. The walker was ARMED 21:20:51Z and
DISARMED 21:31:59Z; a login after the disarm was REFUSED. Both notices went to MSTR~Z.
**23 reads: 20 PASS, 2 FAIL, 1 ERROR.** Graded:

| read | result | issuer grade |
|---|---|---|
| fwd21-labels-30/90/365D, fwd21-no-clear-tone, fwd2-bubbles, fwd2-bars | PASS | 57/67/70 labels; 9/14/14 shortened labels, each with a full-name hover |
| fwd24-overlay-census x3, tabs-dialog-closed x3, nonusd-header, no-officer-exec ASML NA, account-menu-escape, display-names x3 | PASS | one display name per security on every surface ("The Boeing Co" x10) |
| r35-faces VLO US, AMD US | PASS | cloud on the landing view, 40 terms each (refinery:10, oil:9 ...; chip:20, amd:18 ...); 0 unnamed lines, 0 "payload" over 6 views |
| **r35-faces BA US** | FAIL | **PASS on reading -- the probe over-matched.** Its one hit is "Consensus estimate of dividends per share (fiscal year 2026) 0.01 -> 0.00, -0.01, -100.0%". The served values are 0.005 -> 0.0 and the prints differ, so it is a real move to zero, not an equal print. AV-zm-1's rule is about equal prints, and the 6 equal-print rows all read "unchanged at this precision". Cloud, names and wording on BA are clean. |
| **fwd5-timeline-hover** | FAIL | **Pre-existing, outside this round's cells.** The 2026-09-28 bar's tooltip printed "China moves closer to finalizing 200-jet Boeing order", which is the covering event's lead headline. TimelinePanel uses that as a fallback "until the day route loads" (`:362-368`). The hover was read 2 s after the previous read, before the day route answered. The label still says "Strongest headline" for a headline that is not the day's strongest. AV-zm-3 added 4 lines to TimelinePanel (the type and the mount) and did not touch the tooltip. -> round 36. |
| fwd24-control-any-name | ERROR | As in round 34: none of BA, VLO or AMD lacks a checked overlay field. The control passed on MSFT US in round 34 (read-20261004T012802Z). |

**L9 read of the PNGs:**
- `r35-BA-US-cloud.png`: "Words in the headlines -- Headlines from January 1st, 2026 to October 3rd, 2026". The served terms are in
  served order, sized from "max" (40) down, in one blue hue, with no sentiment colour. The cloud sits in the timeline card under the
  chart (`r35-*-landing.png`).
- `tabs-BA-US-4-Model.png`: What changed names all 37 rows in words ("Consensus estimate of earnings per share (fiscal year 2026)",
  "Enterprise value", "Beta"). The 6 equal-print rows read "unchanged at this precision" with "--". Seen, not in scope: tiny moves
  print "-0.00%" and "+0.00%" (capital expenditure 2027, free cash flow 2027/2028).

## 4. OPEN -> ROUND 36 (enrichment list)

1. **FWD-20 instrument re-anchor** (carried from v35). Its check `round35/checks/instrument/instrument35.cjs` reads 0/4 at base 055ba370
   (776 s) and 4/4 on a scratch reference re-anchor (`INSTRUMENT_DIR`). Paths: `scripts/ui-contract-check.mjs`,
   `scripts/ui-measure.mjs`, `__harness__/tests/uiContractFixtures.json`.
2. **FWD-20 page faults the re-anchored instrument sees** on the list state: font sizes 8, 9 and 10 (below 11) and radii 5px.
   (72 PASS / 4 FAIL with the reference re-anchor.)
3. **FWD-5 tooltip:** do not print the covering event's lead headline under "Strongest headline" while the day route loads.
4. **FWD-27 What changed:** a percent move that rounds to zero prints "-0.00%" / "+0.00%".
**Elsewhere:** the CTO's product-file review of d60a0f90, then its DEV push (CLAUDE.md Portal); the 7 reopened outcomes of round 34
(FWD-12, 18, 21, 23, 25, 26, 27) are now on DEV 2c792c27 for grading; RESAPP aq-1 (a company's own words in its cloud, e.g. "amd") is
upstream at COO~Z.
