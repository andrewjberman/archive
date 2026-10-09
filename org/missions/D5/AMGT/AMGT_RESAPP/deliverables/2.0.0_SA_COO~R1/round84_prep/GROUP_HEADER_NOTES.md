# AMGT_RESAPP round-84 PREP -- the running page header in cut 20-F sections (CTO~DELL1 round-83 analysis R1 item 3)

Grounding fork of `2.0.0_SA_COO~R1`, 2026-10-09 ~10:4xZ. READ-ONLY: the five cached 20-F texts (`.scratch/r82_20f/`), the cutter at
HEAD (`lib/research/filings/document.py`, hh-3 merged @41d58a74d0), and the live ASML NA and NU drafting/analysis objects read by
`get-object` (bucket `opal-data-harvest`; ASML drafting `AHblHQYs`, analysis `8efbNTID`; NU drafting `xe0hxE3l`, analysis `AWjDrLYs`).
No write, no model call.

## The furniture per filing (measured on the whole filing text)

| name | running header / page furniture | occurrences | form |
|---|---|---|---|
| ASML NA | `STRATEGIC REPORT` / `CORPORATE GOVERNANCE` / `SUSTAINABILITY` / `FINANCIALS` (nav tabs), `ASML Annual Report 2025`, page number; sustainability-chapter tabs `General disclosures`, `Environmental` | 347-349 each | a 6-line block per page |
| BABA | page number (`140`, `F- 12`, `ii`) then `Table of Contents` | 299 | 2-line block |
| NU | `Form 20-F \| 2025` then page number | 265 | 2-line block |
| PBR | `Annual Report and Form 20-F 2025 I <n>` (one line, page inline); F-pages: `PETROBRAS`, `NOTES TO THE FINANCIAL STATEMENTS`, `(Expressed in millions of US Dollars, ...)` | 295 | 1 line |
| SAP | page number (`118`, `F-7`) then `Table of Contents`; zero-width `​` lines around | 237 | 2-line block |

Rule that separates furniture from repeated table cells (`Total`, `RMB`, `NA`, XBRL members such as `nu:Stage#Member`): a line with
two or more letters and 8+ characters repeating 100+ times, 80%+ of whose occurrences sit next to a page-number line (or that carries
its page inline, `... I <n>`), grown to a fixpoint over lines 80%+ adjacent to furniture (ASML's tab block); page-number lines next to
furniture are furniture. `_page_headers` (`document.py:876-893`) sees only PBR's `<title> I <n>` form, so it is not the rule to reuse.

## Inside the 15 cut sections today (furniture lines / non-blank lines)

| name | business | risk | mdna |
|---|---|---|---|
| ASML NA | 115 / 1,738 | 48 / 988 | 72 / 942 |
| BABA | 28 / 196 | 26 / 164 | 46 / 1,535 |
| NU | 38 / 700 | 36 / 722 | 54 / 1,661 |
| PBR | 30 / 1,432 | 19 / 791 | 20 / 1,217 |
| SAP | 30 / 469 | 10 / 77 | 40 / 961 |

612 lines in all. In the passage maps they become their own passages (ASML: 42 of 549 passages carry header text, e.g.
`STRATEGIC REPORT CORPORATE GOVERNANCE SUSTAINABILITY FINANCIALS ASML Annual Report 2025`; NU: 64 of 660, `Form 20-F | 2025`).

## What is SERVED today (ASML NA, NU)

Of the passages the served draft sentences cite -- ASML 22 (21 sentences), NU 34 (38 sentences) -- **0** carry header text in their
text, in their `location` label, or in a served quoted span. The header passages exist in the passage maps but no served sentence
cites one. **So the strip changes no currently served passage for ASML NA or NU, and no store re-run is owed for them.** One caveat:
the `paragraph <n>` in a location label counts every passage under its heading, header passages included, so a LATER re-analysis
after the strip would renumber paragraphs (the served labels change only through a store write, never by the merge).

## Smallest repair -- in the cutter, so every consumer sees clean text

`lib/research/filings/document.py` `cut()` (`:1369-1376`, the `10-K`/`20-F` branch): for family `20-F` only, compute the filing's
furniture set ONCE from `text` with the rule above, then remove furniture lines (and their adjacent page-number lines) from each OK
section's `text` and recompute `chars`. Put the rule in one helper beside `_page_headers`. Not in `passages.py`: the excerpt text
(`fetch.build_source_object`, `sections_to_excerpt`), the analyzer prompt and the passage map would all still carry the header; the
cutter is the one point every consumer reads through. 20-F only keeps every 10-K byte; a fixture has no line repeating 100 times, so
it is a no-op there too. The caps are applied before `cut()` returns (`_cut_bounded` / `_cut_xref`), so a capped section shrinks by
the stripped lines (ASML business ~2-3k chars); stripping before the cap slice is the better variant if the cell can do it in the same
helper without moving start offsets.

**Must not move:** `round82_prep/checks/r82_cut.py --crit AC2` (10-K and fixture hashes) YES; `r82_cut --crit AC1` 15 of 15;
`round83_prep/checks/r83_pbr.py --crit AC1` YES (start offsets and headings are unchanged by a strip; its end bound is `<=`);
`round83_prep/checks/r83_passages.py --crit AC1` YES (ASML Item 4.B coverage stays well above 50%). `document.py` is a SITE-Z producer
path: the merge needs `1.0.0_SA_CTO~Z`'s half.

## The check

`round84_prep/checks/r84_header.py --crit AC1 [--cache DIR]`: cuts the five cached filings in-process; H1 0 furniture lines left in
the 15 sections (per name, per section denominators); H2 three look-alike lines planted in ASML's business section (a prose sentence
opening with the report title, a sentence ending in a number, a standalone number not next to furniture) all KEPT. Dry-run at the base
(py3.12): H1 FAIL 612 lines; H2 PASS 3 of 3; `R84 HEADER AC1: NO`, exit 1. ruff py39 clean.
