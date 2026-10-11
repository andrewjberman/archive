"""AMGT_CORPUS round 46, CRPS-av-1 -- the team-sheet reader classes every counted row and carries the team's own period values.
Issuer's file. READ-ONLY (builds a workbook in memory; no S3, no network).

  PYTHONPATH=. python av1_check.py          prints  `av1 build <b>/4 control <c>/2`

The rule under test is the issuer's reading of the CTO's ADDENDUM 1 (ledger/ROUND_ANALYSIS.round44.md) and ADDENDUM 1 of the round-45
analysis, measured on the 32 own workbooks (a period header was found in all 32):
  * the PERIOD HEADER is the first counted row whose numeric cells are ALL integers in 1990..2100, at least 3 of them, strictly
    increasing; its numeric columns are the PERIOD COLUMNS, its numbers the period labels;
  * a counted row ABOVE the period header: CONTROL when its label is an upper-case identifier with at least one underscore
    (`^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$`), else HEADING;
  * the period header row itself, and any later row whose numeric cells are all such increasing years: HEADING;
  * a counted row BELOW the period header: FIGURE when it holds a numeric value in a period column; else CONTROL when the label has the
    identifier form, else HEADING;
  * `rows` stays every counted label in sheet order (the existing rule); `row_classes`, `row_numbers` (1-based sheet row) and
    `row_values` are aligned with it; `row_values[i]` is None except for a FIGURE row, where it is the list of that row's cells in
    the period columns, VERBATIM as the workbook saved them (a number as a number, a text such as '#VALUE!' as that text, a blank as None).
The fixture is a miniature of IMB LN's own sheet (info panel above the header, a side table to the right).
"""
import io
import sys

import openpyxl

from lib.research.corpus import dossier, team_sheet

HEADER_ROW = 9
YEARS = (2016, 2017, 2018, 2019, 2020)
PERIOD_COL0 = 5  # column E, 1-based


def workbook_bytes():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Model NEW VERSION"

    def put(row, col, value):
        ws.cell(row=row, column=col, value=value)

    # the info panel above the header: words and tokens, with numbers in the side columns
    put(2, 3, "Ticker:")
    put(2, 12, 1.392)
    put(2, 15, 497)
    put(3, 1, "FG_COMPANY_NAME")
    put(3, 9, 28.05)
    put(3, 15, 16118)
    put(5, 3, "Currency:")
    put(5, 9, 3.645)
    put(5, 12, 0.491)
    # the period header
    put(HEADER_ROW, 3, "Financial Summary")
    for k, year in enumerate(YEARS):
        put(HEADER_ROW, PERIOD_COL0 + k, year)
    # FIGURE rows
    figure_rows = [
        ("Revenue", [7976, 8671, 8700, 9009, 8753]),
        ("  y/y Growth", [None, 0.087, 0.003, 0.036, -0.028]),
        ("Operating Income", [2579, 2645, 2527, 3015, 3102]),
        ("Operating Margin", [0.183, 0.173, 0.164, 0.188, 0.187]),
        ("EBITDA", [3786, 3961, 3793, 3815, 3927]),
        ("Net debt", [11950, "#VALUE!", 12100, 12210, 12300]),
        ("Capex", [310, 320, 330, 340, 350]),
        ("Tax", [120, 125, 130, 135, 140]),
    ]
    row = HEADER_ROW + 1
    expected = []
    for label, values in figure_rows:
        put(row, 3, label)
        for k, v in enumerate(values):
            if v is not None:
                put(row, PERIOD_COL0 + k, v)
        expected.append((row, label.strip(), "FIGURE", values))
        row += 1
    # a CONTROL row inside the table: identifier form, numbers only in the side columns (outside the period columns)
    put(row, 3, "BEST_FPERIOD_OVERRIDE")
    put(row, 24, 2026)
    put(row, 25, 2027)
    expected.append((row, "BEST_FPERIOD_OVERRIDE", "CONTROL", None))
    row += 1
    # a HEADING row inside the table: words, numbers only in the side columns
    put(row, 3, "Notes on the sheet")
    put(row, 24, 1)
    put(row, 25, 2)
    expected.append((row, "Notes on the sheet", "HEADING", None))
    row += 1
    # a repeated period header
    put(row, 3, "Year")
    for k, year in enumerate(YEARS):
        put(row, PERIOD_COL0 + k, year)
    expected.append((row, "Year", "HEADING", None))
    # a second sheet, so model_rows_beside is exercised
    other = wb.create_sheet("Model")
    for i in range(1, 13):
        other.cell(row=i, column=1, value="Old line %d" % i)
        other.cell(row=i, column=2, value=i)
        other.cell(row=i, column=3, value=i * 2)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue(), expected


def main():
    body, expected = workbook_bytes()
    exp_above = [
        (2, "Ticker:", "HEADING", None),
        (3, "FG_COMPANY_NAME", "CONTROL", None),
        (5, "Currency:", "HEADING", None),
        (HEADER_ROW, "Financial Summary", "HEADING", None),
    ]
    want = exp_above + expected
    b1 = b2 = b3 = b4 = 0
    reading = None
    try:
        reading = team_sheet.sheet_reading(body).get("Model NEW VERSION")
    except Exception as exc:  # noqa: BLE001
        print("av1 sheet_reading threw: %s" % str(exc)[:160])
    if reading:
        got = list(zip(reading.get("row_numbers") or [], reading.get("rows") or [], reading.get("row_classes") or []))
        b1 = 1 if got == [(r, lab, cls) for r, lab, cls, _ in want] else 0
        print("av1 b1 classes equal expected %s (%d rows)" % (b1 == 1, len(got)))
        if b1 != 1:
            print("av1 b1 got %s" % (got[:6],))
        counts = {c: sum(1 for _, _, k in got if k == c) for c in ("FIGURE", "HEADING", "CONTROL")}
        n = len(reading.get("rows") or [])
        b2 = 1 if (sum(counts.values()) == n == len(reading.get("row_values") or []) and counts == {"FIGURE": 8, "HEADING": 5, "CONTROL": 2}) else 0
        print("av1 b2 class counts %s sum %d rows %d" % (counts, sum(counts.values()), n))
        values = reading.get("row_values") or []
        by_label = {lab: v for (_, lab, _), v in zip(got, values)}
        b3 = 1 if (by_label.get("Revenue") == [7976, 8671, 8700, 9009, 8753]
                   and by_label.get("y/y Growth") == [None, 0.087, 0.003, 0.036, -0.028]
                   and by_label.get("Net debt") == [11950, "#VALUE!", 12100, 12210, 12300]
                   and all(by_label.get(h) is None for h in ("Financial Summary", "BEST_FPERIOD_OVERRIDE", "Ticker:"))) else 0
        print("av1 b3 values verbatim (a text cell kept as text, a blank as None, non-figure rows None) %s" % (b3 == 1))
        periods = reading.get("periods") or []
        b4 = 1 if ([p.get("label") for p in periods] == [str(y) for y in YEARS]
                   and [p.get("column") for p in periods] == ["E", "F", "G", "H", "I"]) else 0
        print("av1 b4 periods %s" % (periods,))
    # control c1: `rows` is still the existing rule's counted labels, in sheet order
    c1 = 0
    try:
        base_rows = team_sheet.sheet_labels(body).get("Model NEW VERSION")
        c1 = 1 if base_rows == [lab for _, lab, _, _ in want] else 0
        print("av1 c1 sheet_labels unchanged %s (%d labels)" % (c1 == 1, len(base_rows or [])))
    except Exception as exc:  # noqa: BLE001
        print("av1 c1 threw: %s" % str(exc)[:160])
    # control c2: the sheet that is not the team sheet keeps its labels beside (model_rows_beside rule) in the old function
    c2 = 0
    try:
        both = team_sheet.sheet_labels(body)
        c2 = 1 if sorted(both) == ["Model", "Model NEW VERSION"] and len(both["Model"]) == 12 else 0
        print("av1 c2 both sheets carried %s" % (c2 == 1))
    except Exception as exc:  # noqa: BLE001
        print("av1 c2 threw: %s" % str(exc)[:160])
    print("av1 METHOD_VERSION %s" % dossier.METHOD_VERSION)
    print("av1 build %d/4 control %d/2" % (b1 + b2 + b3 + b4, c1 + c2))
    return 0 if (b1 + b2 + b3 + b4 == 4 and c1 + c2 == 2) else 1


if __name__ == "__main__":
    sys.exit(main())
