# AMGT_RESAPP round-83 PREP -- PBR's real 20-F sections (row D1-W323-S1)

Grounding fork of `2.0.0_SA_COO~R1`, 2026-10-09 ~09:0xZ. READ-ONLY: the cached filing `.scratch/r82_20f/PBR_US_Equity.txt`
(1,290,695 chars; no fetch, no model call, no write). Cutter: `lib/research/filings/document.py` as merged @9f252e010a.

## What the cutter does today

| item | status | start | chars (full) | heading | true section? |
|---|---|---|---|---|---|
| business | OK | 198,623 | 11,085 | `About us` | NO: the About Us section (contents p.23-24) |
| risk | OK | 209,708 | 70,000 (94,490) | `Risk Factors` | YES: inside Risks (Item 3.D), ends at the Cybersecurity heading (304,198) |
| mdna | OK | 568,965 | 19,885 | `Liquidity and Capital Resources` | NO: the 5.B/5.E sub-section only (contents p.179) |

## The cross-reference table (offset 866,987, "Cross-Reference to Form 20-F")

- **Item 4.B, "B. Business overview"** (867,664): `About Us (Overview); Our Business (Exploration & Production; Refining, Transportation & Marketing;
  Gas & Low Carbon Energies; Mergers and Acquisitions); Business Plan 2026-30 (BP 2026-30); Legal and Tax (Regulation)`, pages
  `25, 64, 97, 117, 133, 141, 252`.
- **Item 3.D, "D. Risk factors"** (867,472): `Risks (Risk Factors)`, page `30`.
- **Item 5** (868,191): `A. Operating results -> Operating and Financial Review and Prospects 170`; `B. Liquidity and capital resources ->
  Operating and Financial Review and Prospects (Liquidity and Capital Resources) 179`; C -> ESG 159, 164; D -> Our Business; Risks; OFR
  63, 30, 170; E -> OFR (Liquidity and Capital Resources) 179.

## The true sections, by the report's own contents page and running page headers

The report's contents (offset ~157,700) list `<name>\n<page>`. Each body page opens with the header line
`Annual Report and Form 20-F 2025 I <n>` (295 of them, pages 4-298). **Contents page p = header page p-1**, measured on a name with both
(`About us`: contents 24, body heading on header page 23 at 198,623).

| section (table item) | contents p. | body | start | first line | ends |
|---|---|---|---|---|---|
| Risks (3.D) | 30-31 | header 30 | 208,986 (`Risks` 209,024; `Risk Factors` 209,708) | `Risks` | `Cybersecurity Framework and Risk Management`, header 57, 304,198 |
| **Our Business (4.B)** | 63 (divider) | header 62 blank; content header 63 | **319,023** | `Exploration & Production` | sub-sections E&P 64, RTM 97, G&LCE 117, M&A 133; next non-child entry `External Business Environment`, header 135 (468,608) |
| **Operating and Financial Review and Prospects (5)** | 170 (divider) | header 169 blank; content header 170 | **549,889** | `Consolidated Financial Performance` | `Management and Employees` divider, header 191 (593,198) |

## Why the cutter picked the wrong two (cause)

1. **The parent sections have no body heading line.** "Our Business" and "Operating and Financial Review and Prospects" open on divider
   pages that extract as NOTHING (header page 62 is followed directly by header page 63; 169 by 170): 22 blank header pages in the
   report. Their only text occurrences are the contents page and the table. `_xref_body_headings` (`document.py:780`, the whole-line
   test at `:796`) therefore finds 0 usable body headings for either name.
2. **`_cut_xref` takes the FIRST named section that has a body heading** (`document.py:840-845`). For 4.B the table's first name is
   `About Us`: the tokenizer splits `About Us (Overview)` on `(` (`_XREF_SPLIT_RE`, `:689`; `:731`) into the parent `About Us` and the
   child `Overview`, so the parent wins although the table cites only its Overview sub-section, and `Our Business` (0 headings) is
   skipped. For Item 5 the first name `Operating and Financial Review and Prospects` has 0 headings, so the next token,
   `Liquidity and Capital Resources` (the 5.B parenthetical child), is cut.
3. **Length passed both:** 11,085 and 19,885 chars are plausible section lengths, and r82_cut graded status and length only.

## The smallest repair (in `document.py`, xref mode only)

1. **A contents-page fallback in `_cut_xref`:** when a name the table gives has no usable body heading, resolve it through the report's
   own contents page and running page headers. Find the name as a `<name>\n<page>` contents entry before the table. Measure the
   contents-to-header offset on a name the same report prints both ways (here -1). Start at the first content line after the header
   line of that page, skipping a blank divider page. End at the next contents entry whose page is greater and which is NOT a child the
   table cites in this name's parentheses (for OFR that end is wrong; the end rule is in the note below).
   Gate it: the mode runs only when the report has running page headers (a regex `^<title> I <n>$` matched on 100 or more lines), so
   ASML (which finds its headings) and every 10-K and fixture never reach it.
2. **Rank the 4.B names by what the table cites:** a `Parent (child)` with ONE child cites only that child sub-section, and a
   `Parent (c1; c2; ...)` with two or more cites the whole parent. For `business`, try the parent cited whole first (`Our Business`).
   For `mdna`, try the names in table order, so Item 5.A's whole-section citation, `Operating and Financial Review and Prospects`, wins
   over the 5.B parenthetical `Liquidity and Capital Resources`.

**The OFR end needs care:** OFR's children are not in the table (only `Liquidity and Capital Resources`), so "the next non-child
contents entry" would close it at `Consolidated Financial Performance` (171), one page in. The OFR end must be the next DIVIDER-page
section (a contents entry whose header page p-1 is blank): `Management and Employees` (192 -> header 191, 593,198). The same rule gives
Our Business an end at the next divider-page entry, `Environment Social and Governance` (150 -> header 149). That still sits inside the
60,000 cap, which `Our Business` (149,585 chars to External Business Environment) exceeds anyway. Prefer the divider rule for both. It
is one rule, and the 22 divider pages are measured.

**Not moved (P4 grades it):** ASML, BABA, NU and SAP's 12 cells stay byte-identical (ASML reaches xref mode, but its headings are found;
the fallback runs only on a 0-heading name in a report with page headers). The 10-K and fixture hashes stay unchanged (r82_cut AC2).

## The check

`round83_prep/checks/r83_pbr.py --crit AC1 [--cache DIR]` cuts all five cached filings in-process and grades SECTION IDENTITY:
- **P1:** business starts on header page 63 (318,985-319,100) and opens `Exploration & Production`.
- **P2:** risk starts inside header page 30 and ends at the Cybersecurity heading (+-2).
- **P3:** mdna starts on header page 169/170 (549,850-549,960), opens `Consolidated Financial Performance` and ends at or before 593,198.
- **P4:** the other four names' 12 cells keep their start, chars and sha256 prefix (baseline measured at @9f252e010a).

Lengths are printed, never graded. **Base dry-run (2026-10-09, py3.12 and py3.14):** FAIL P1 (`About us` 198,623), PASS P2 (end 304,198 =
heading 304,198), FAIL P3 (`Liquidity and Capital Resources` 568,965), PASS P4 12 of 12 -> `R83 PBR AC1: NO`, exit 1. ruff py39 is clean.

**Producer path:** `document.py` is a site-Z producer path (CTO msg 1267 rule; round 82's gg-1 merged under `1.0.0_SA_CTO~Z`'s half).
This repair's merge needs that half again.
