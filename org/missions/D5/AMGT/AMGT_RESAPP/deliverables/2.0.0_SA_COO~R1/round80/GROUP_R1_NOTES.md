# Round 80, cell R1: grounding notes (2.0.0_SA_COO~R1 fork, 2026-10-09 ~01:5xZ)

Input: CTO~Z round-79 analysis R1 (`ledger/ROUND_ANALYSIS.round79.md` @c249be336b) and the CVO grade
(`org/tier1_exec/3.0.0_SA_CVO/deliverables/AMGT_RESAPP_ROUND79_L9_GRADE_20261009.md`, on origin/CLOUD).
Base: box/dell1 @0e77b427cd. Every read below is read only. No SEC, vendor, model or Bloomberg call was made.

## 1. What produced ASML NA's stored text, and why it is wrong

- **Stored object:** silver `filing_source` (vendor `sec`), `ASML_NA_Equity` / accession `000162828026011378`,
  `asml-20251231.htm`, filed 2026-02-25, **`parser_version` `opal-filings-fetch/1.0.0`**. The same bytes are in the
  retired pool at `s3://opal-data-harvest/filings/v1/ASML_NA_Equity/000162828026011378.source.json` (2026-09-17).
  The excerpt holds ONE item, `risk`: 70,000 chars kept of `full_chars` 1,091,017. There is no `mdna`.
- **Producer:** `lib/research/filings/fetch.py` `build_source_object` (EDGAR-by-CIK path, `:346-470`) ->
  `extract_sections` -> the cutter (now `lib/research/filings/document.py` `cut` `:800`, `_cut_bounded` `:555`).
  Written by `fetch.persist(..., write_pool=True)` `:486` to silver via `lib/research/harvest/filings.py`
  `write_filing_source_silver` `:230`.
- **The fault:** parser 1.0.0's 20-F risk patterns (`8abfd829a7:lib/research/filings/fetch.py:128`) ended in a bare
  `r"riskfactors"` fallback. The cutter takes the LAST qualified heading. In ASML's integrated 20-F that is the line
  "Risk factors – Cybersecurity and other security" inside the cybersecurity item. No Item 4 end heading follows it,
  so the body ran unbounded to the end of the document (1.09M chars) and the 70,000-char cap kept cybersecurity text,
  then share capital and board holdings. Those are the passages the page drew (`P0064`/`P0065`, "Board holdings ...
  0.01%"). D9 removed that fallback later (`document.py:739-748`); the stored object predates the removal.
- **No `business` key exists anywhere.** `document.py` 20-F keys = risk / mdna / officers (`:739-770`).
  `fetch.EXCERPT_ITEMS` = `{"10-K": ["risk","mdna"], "20-F": ["risk","mdna"]}` (`fetch.py:89`). Item 4.B
  Business overview is never cut. The thesis card's passages come from the excerpt's passage map
  (`passages.build_passage_map`, `passages.py:180`). The driver series and the "FILED DETAIL (DOES NOT DESCRIBE THE
  BUSINESS)" card draw from the analysis built on that excerpt (`lib/research/filings/analyze.py`, model
  `claude-opus-5` `:60`, `anthropic_call` `:321`).

## 2. What a real repair of ASML's stored text needs

- **No local or S3 copy of the document exists.** SEC bronze under `s3://opal-data-harvest/sec/harvest/bronze/` holds
  1 object (company_tickers); comp-find for `asml-20251231` finds no copy of the document. So re-cutting ASML needs
  **one SEC EDGAR GET** (egress), then a **silver write** (served data path), then a **re-analysis** (Anthropic model
  call, vendor egress) and the drafting rebuild before the page changes. No Bloomberg Terminal is needed on the
  EDGAR-by-CIK path. `battery.py:507-519` is the Terminal leg of the battery path only.
- **Site Z?** The census (@6a308cd424, row `:28`) names `filings/battery.py:507-519` as a site-Z hand-run, and the
  `-FilingsAnalyzer` task (DISABLED, `:29`). `document.py` and `fetch.py` are not named, but battery imports
  them, so a hand-run battery on site Z would pick up the new cutter after box-sync. **Open call for
  1.0.0_SA_CTO~DELL1:** is a `document.py` change a "producer path" under msg 1267?
- **dell1 environment:** PyMuPDF does not import here (3.14: not installed; 3.12: `DLL load failed ... _extra`).
  `document.py` imports `fitz` at module top (`:56`), so the filings test folder errors at collection on dell1
  (16 errors). `r80_r1.py` stubs `fitz`; `cut()` does not use it.

## 3. Section census (prototype at the base, stored silver, read only)

Denominator: 5 stored 20-F names (silver `filing_source`, 14 rows across `sec` 13 + `issuer-site` 1).

| name | parser | risk came from | mdna came from | business |
|---|---|---|---|---|
| ASML_NA_Equity | 1.0.0 | FALLBACK "Risk factors – Cybersecurity and other security" (full 1,091,017) | NONE | NONE |
| BABA_US_Equity | 1.0.0 | OWN-HEADING "D. Risk Factors" | OWN-HEADING Item 5 | NONE |
| NU_US_Equity | 1.0.0 | FALLBACK "Risk Factors" in this annual report..." (a cross-reference) | Item 5 (heading wraps a line) | NONE |
| PBR_US_Equity | 1.0.0 | FALLBACK "Risk Factors - 2.a) Our controlling shareholder..." (a cross-reference) | NONE | NONE |
| SAP_GY_Equity | 1.0.0 | FALLBACK "Risk Factors" (bounded, 33,745; reads as the real section) | OWN-HEADING Item 5 | NONE |

So 4 of 5 stored 20-F risk items came from the removed fallback, and 0 of 5 hold a business section. The
classifier must compact the first TWO lines after the label, because NU's "Item 5. Operating" heading wraps.

## 4. Proposed cell (LOCAL): code and census only, no store write

Files: `lib/research/filings/document.py`, `lib/research/filings/fetch.py` (EXCERPT_ITEMS line only),
new `lib/research/filings/section_census.py`, new `lib/research/filings/tests/test_section_census.py`, tests in
`lib/research/filings/tests/test_document.py`.

1. `document.py`: add a 20-F key `business` = ("Item 4.B. Business Overview", start
   `[item4 SEP b SEP businessoverview, b SEP businessoverview]`, end `[c SEP organi[sz]ationalstructure,
   item4a SEP unresolved, item5 SEP operating]`), with `ITEM_CAPS["business"] = 60000`. The 10-K patterns, the
   three existing 20-F keys and `sections_to_excerpt` stay as they are.
2. `fetch.py`: `EXCERPT_ITEMS["20-F"] = ["business", "risk", "mdna"]`. Nothing else in `fetch.py` changes.
3. `section_census.py`: `--stored` reads the latest silver `filing_source` rows (read only), and prints for each
   20-F one line `<security_key> <parser_version> | risk: <CLASS> ...; mdna: <CLASS> ...; business: <CLASS> ...`,
   where CLASS is OWN-HEADING / FALLBACK / NONE / OTHER, judged by today's start patterns on the first two lines
   after the item label. The last line reads `SECTION CENSUS: <k> of <n> stored 20-F names carry a business section
   from its own heading; <j> of <n> risk items came from their own heading`. No write.

Criteria (`deliverables/2.0.0_SA_COO~R1/round80/checks/r80_r1.py`), dry-run at the base 2026-10-09 ~01:5xZ:
- AC1 (build): business cut from its own heading on a fixture; FAILED with a reason when absent; EXCERPT_ITEMS carries
  it. **Base: A1/A2/A3 FAIL, `R80 R1 AC1 SERVED: NO`, exit=1 (FAIL as expected).**
- AC2 (build): the census names every stored 20-F, its denominator equals the checker's own silver count, and
  ASML NA's line reads `risk: FALLBACK`. **Base: C0 FAIL (module absent), exit=1 (FAIL as expected).**
- AC3 (bound): the 10-K fixture's three sections and the 20-F risk/mdna/officers sections hash as at the base.
  **Base: 6 of 6 B PASS, `R80 R1 AC3 SERVED: YES`, exit=0 (PASS as expected).**

## 5. What the cell does NOT do (the WORLD half, a separate act)

Re-fetching ASML NA's 20-F (SEC egress), writing its silver row, re-running `analyze.py` (Anthropic) and rebuilding
the draft. Until that runs, FWD-18 on ASML NA stays NOT REALIZED whatever the code says. It needs: the egress word
(SEC + model call, per CLAUDE.md "NEVER call an external vendor API without Andrew's explicit per-use word"),
a never-widen pair for the silver write, and the site-Z ruling above. An alternative within R1's own words: walk
FWD-18 on BABA or SAP (risk/mdna from their own headings) and keep ASML's repair for the round that has the word.
