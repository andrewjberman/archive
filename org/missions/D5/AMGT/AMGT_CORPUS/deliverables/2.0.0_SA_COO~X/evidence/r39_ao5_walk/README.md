# AMGT_CORPUS round 39 CRPS-ao-5 -- the real run of FWD-20 / FWD-21 on the page (2.0.0_SA_COO~X, 2026-10-06 20:14Z-20:30Z)

Walks (signed in as the walker, viewport 1440 x 900, local dev build on :5174 reaching the live backend):
- `tmp/ui-walk/20261006T201404Z` -- TSM US, ASML NA, SAP GY, BA US, every tab; 125 shots; walk void: no; DISARM proof REFUSED.
- `tmp/ui-walk/20261006T202441Z` -- IMB LN, `--deep`; 56 shots; walk void: no; DISARM proof REFUSED.

Build walked: portal `e1ee93a9` = candidate `90816273` (ao-3 `d0c3f21b` + ao-4) merged with origin/DEV `6b4e89a8`. DEV
fast-forwards to it; the diff against DEV is the cell's 5 files (+61/-23). On that tree: typecheck clean; `ao3_check` currency,
marks, words each build 1/1 control 1/1; `ao4_check` control 2/2; modelPattern harness passes.

What the captures show (crops of the Model-expanded shots, kept here):
- `tsm_header.png` -- Enterprise value: "Not shown: Bloomberg's figure does not say whether it is in units or millions"; Net debt:
  "-2.00T (currency not confirmed by Bloomberg)". No raw figure.
- `tsm_sheet_a.png`, `tsm_sheet_b.png` -- all 13 year columns inside the card at 1440 px, 2028E the last (EBITDA 6,752,435); every
  in-row "--" carries mark 1 ("Bloomberg reports no history for this line") or 2 ("No consensus estimate is served for this
  line"); the header-fact line reads "Average daily value traded (three months): USD 4,863,543,808; Market capitalisation: USD
  2,519,589 million".
- `asml_sheet_a.png` -- 13 year columns inside the card on ASML, each "--" marked.
- `ba_header.png` (control) -- "USD 184B", "USD 26.96B": unchanged. `sap_header.png`, `asml_header.png` for the CVO's read.

Carried for the CVO, not this cell's: ASML's row label "Minority (non-controlling) interest (zero-dominated: no magnitude: 10 of
10 fiscal years are zero)" is a machine phrase in a row label.

NOT driven by these walks (still owed under ao-5): the FWD-10 pillar opener, FWD-11 ABSENT name and roster count, FWD-12 template
comparison, FWD-15 posture citation and byte compare, FWD-16 docx before/after, FWD-18 term filter. `--deep` pressed the page
chrome only (Print, Refresh, the tab buttons); a pillar opener and a term filter need named presses.
