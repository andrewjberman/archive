# Round-82 PREP, the 20-F cutter repair (row AMGT_RESAPP-D1-W321-S1): grounding notes (2.0.0_SA_COO~R1 fork, 2026-10-09 ~06:5xZ)

Not cut, not issued. Read-only: one SEC EDGAR GET per name (the filing `fetch.latest_filing` names, CIK from each stored silver row's
`filing_identity`), text built with `fetch.html_to_text` exactly as `build_source_object` does (`fetch.py:346-376`), NO persist, NO model
call. Cached at `.scratch/r82_20f/<KEY>.txt` (gitignored). Probes: `.scratch/r82_20f/probe.py`, `probe2.py`, `sim.py`.

## 1. What the merged cutter finds today (document.cut, parser opal-filings-fetch/2.0.0)

| name | business (4.B) | risk (3.D) | mdna (5) | the filing's shape |
|---|---|---|---|---|
| ASML_NA_Equity | FAILED | FAILED | FAILED | integrated annual report: item headings exist ONLY in the closing "Form 20-F cross reference" table (`pos ~1.337M`: "D. Risk Factors -> Risk - Risk factors 66", "B. Business Overview -> At a glance 6"); the body uses the report's own section names |
| BABA_US_Equity | OK 208,203 | OK 350,005 | OK 131,933 | a classic 20-F: "B. Business Overview", "D. Risk Factors", "ITEM 5. OPERATING ..." in the body |
| NU_US_Equity | OK 220,925 | FAILED | OK 93,288 | classic, but the body risk section is headed **"A. Risk Factors"** under "Item 3. Key Information" (`pos 329374`, followed by "Risk Factors Summary"); the only "D. Risk Factors" line is the contents entry (`59375`) |
| PBR_US_Equity | FAILED | FAILED | FAILED | integrated "Annual Report and Form 20-F": cross-reference table at `~867k` ("B. Business overview -> About Us (Overview); Our Business ... 25, 64, ..."); body headings "Risk Factors" (`209708`, whole line), "Our Business" |
| SAP_GY_Equity | FAILED | FAILED | OK 86,338 | body headings "ITEM 4. INFORMATION ABOUT SAP" (`239867`, line start) and a whole-line "Risk Factors" (`206122`); no "B. Business Overview" line at all |

Total: **6 of 15** cells cut.

## 2. Why `_cut_bounded` (`document.py:555`) rejects the real headings

- The start patterns require the item LETTER and title together (`item3 d riskfactors` / `d riskfactors`; `item4 b businessoverview` /
  `b businessoverview`). Integrated reports (ASML, PBR) and SAP never print "B. Business Overview" in the body; NU prints "A." not "D.".
- Where a pattern does match a real body line it is often mid-line (cross-references such as "see Item 3. Key Information-D. Risk
  Factors") -- rejected by `_at_line_start` (correctly).
- The remaining matches are table-of-contents or cross-reference-table lines, rejected by `_is_contents_line` (a page number within the
  next 3 lines) -- also correct.
- The bare `riskfactors` fallback was removed (D9) because it took the LAST bare match, which on ASML was "Risk factors - Cybersecurity
  and other security" and ran unbounded (the parser-1.0.0 failure this project is repairing).

## 3. The proposed change (three narrow additions; nothing existing moves)

1. **risk -- whole-line bare heading, FIRST qualified:** after the two existing start patterns, accept a line whose whole stripped text
   is "Risk Factors" (case-insensitive; optional leading "A."-"D." letter), at line start, not a contents entry; take the FIRST such line
   (not the last), bounded by the next whole-line Item 4 / Item 5 heading, else the cap. Simulated: ASML OK (100,438 full, capped 70,000),
   SAP OK (33,745), NU OK expected via the letter-tolerant form ("A. Risk Factors"); **PBR runs 657,804 to the cap** -- its bound needs a
   body end heading (open question 2).
2. **business -- the Item 4 heading itself as a fallback:** after the two 4.B patterns, `item4 information(on|about)` at line start, not a
   contents entry, closed by Item 4A / Item 5: the whole of Item 4. Simulated: SAP OK (78,104). No effect on ASML or PBR (no body Item 4).
3. **integrated reports (ASML, PBR) -- a cross-reference reader, its own cell:** read the "Form 20-F cross reference" table's entry for
   the item, take the report section it names ("At a glance", "Our Business", "Financial performance"), and cut that whole-line body
   heading. This is a new cutting MODE, larger than 1-2; it is what business and mdna on ASML and PBR need.

The 10-K patterns, the existing 20-F start/end patterns and dd-1's fixtures are not touched (AC2 below).

## 4. The check -- `round82_prep/checks/r82_cut.py`, dry-run at the base (box/dell1 after 74132a59ba)

- **AC1** (build): the 5 x 3 grid on the cached real filings, all 15 OK with >= 1500 chars and a non-empty heading. **Base: NO, 6 of 15**
  (FAIL as expected). A cell may honestly read FAILED after the repair (e.g. if the round scopes out the cross-reference mode); the round
  then states which cells it targets and the check is amended to that list.
- **AC2** (bound): `round80/checks/r80_dd1.py --crit AC3` -- the 10-K and 20-F fixture hashes. **Base: YES** (PASS as expected).

## 5. Open questions

1. Scope: changes 1-2 alone take the grid to an estimated 10 of 15 (ASML risk; NU risk; SAP risk and business; PBR risk with a weak end).
   ASML and PBR business/mdna need change 3.
2. PBR's risk body ends where? The whole-line rule needs a body end heading for integrated reports (the next whole-line top section).
3. `document.py` is a site-Z producer path (CTO~DELL1 msgs 1267/1394): the merge needs `1.0.0_SA_CTO~Z`'s half, as ee-3 did.
4. The store half (re-cut + re-analysis) re-runs only after AC1 reads YES on the targeted cells, under a new pair.

-- fork of 2.0.0_SA_COO~R1
