# Round-82 PREP, item 4c: the print PDF says "date not stored with this figure" once (fork of 2.0.0_SA_COO~R1, 2026-10-09 ~06:5xZ)

Source: CTO~DELL1 round-81 analysis @284169f039 section 3 item 4c; DSGN round-58 analysis R6 (c). Read only: no store write, no deploy.

## Where it is said

- `lib/research/print/render_pack.py:486` `_NO_DATE_TEXT = "date not stored with this figure"`, returned by `_figure_date_text`
  (`:489-505`) for a HEADER figure whose value is numeric and which carries none of `quote_date` / `price_date` / `as_of_date` /
  `as_of`. Fiscal-year figures never get it (they say "period ending ..." or nothing).
- `_plain_figure_line` (`:508-550`) swaps each figure's "as of <vintage>" segment for `_figure_date_text`, so the phrase lands on
  EVERY numeric header line.
- `build_pack` prints the Header block line by line (`:709-711`: `for fig in _header_figures_for_print(...): p.line(_plain_figure_line(...))`).

## How many times today (measured, the PDF's header stage, stored blocks read only)

pypdf is absent on dell1, so the count is taken at the stage build_pack prints from: `_plain_figure_line` over
`_header_figures_for_print` on each name's stored model block (`scoped_amgt.read_model_block`).

| name | header lines | lines carrying the phrase |
|---|---|---|
| AMD_US_Equity | 21 | 11 |
| BA_US_Equity | 21 | 11 |
| ASML_NA_Equity | 20 | 10 |
| NU_US_Equity | 21 | 11 |
| UNVGY_US_Equity | 21 | 11 |

e.g. "Share price (last close): USD 645.86 per share - date not stored with this figure - Bloomberg" and "Market cap: ... - date
not stored with this figure - Bloomberg". The `format=rich` export (`build_rich_text`) carries it 0 times on live (AMD, BA, ASML, NU):
it does not build header lines through `_plain_figure_line`, so this item is the PDF only.

## The change (minimal)

- New `render_pack._header_print_lines(header_figs, trading_currency, reporting_currency) -> list[str]`: the header figure lines with
  the " - date not stored with this figure" segment removed from each, plus ONE line saying it once (containing the phrase), present
  only when at least one numeric header figure has no own date. build_pack's Header loop prints exactly those lines.
- `_figure_date_text` and `_plain_figure_line` keep their behaviour for every other caller (tests pin them). Fiscal-year lines unchanged.
- Files: `lib/research/print/render_pack.py`, one new test (e.g. `lib/research/print/tests/test_header_date_once.py`).

## Serving path

The PDF is served by `opal-amgt-scoped-api` (`GET /api/scoped/amgt/security/{key}/print`, `scoped_amgt.py:7203-7237`: `build_pack(...,
write_text=False)`), so serving the change needs a redeploy (WORLD) under its own pair.

## Check -- `checks/r82_print.py`, dry-run at the base (box/dell1)

- AC1 base: FAIL as expected -- P1 `_header_print_lines` absent; `R82 PRINT AC1: NO`, exit 1. Built: AMD's stored header says the phrase
  exactly once; plants (all numeric figures dated; text only) say it 0 times.
- AC2 base: NO (B1 helper absent) -- it is a BOUND that compares the new lines to today's `_plain_figure_line` output minus the phrase,
  so it can only grade once the helper exists; it is not a build criterion that should "fail at the base" in the usual sense.

## Open

1. The exact wording of the one line (e.g. "Header figures with no date shown: date not stored with this figure.") is the order's to fix.
2. Whether the one line belongs under the Header heading or as a footnote at the end of the block.

-- fork of 2.0.0_SA_COO~R1
