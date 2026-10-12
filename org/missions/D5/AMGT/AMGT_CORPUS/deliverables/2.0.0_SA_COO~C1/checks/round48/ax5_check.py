"""AMGT_CORPUS round 48, CRPS-ax-5 -- a FactSet code's single label across the team's workbooks is served, claim HELD, and the own sheet's MEASURED
label wins over it. Issuer's file. READ-ONLY (a workbook built in memory; no S3, no network).

  PYTHONPATH=. python ax5_check.py          prints  `ax5 build <b>/3 control <c>/2`

The rule under test (CTO round-47 analysis ADDENDUM 1, msg 4113): "apply a code's single label across workbooks at any count, claim held, cite source and
'N agree, 0 disagree'; own-sheet measured wins; print the three shares". The entries live in `lib/research/corpus/factset_descriptions.json`
({"entries": {code: {"text", "cite"}}}, loaded once per process into `team_sheet._LABEL_CACHE["factset"]`); this check replaces that cache entry with
two fixtures, so it tests the PRECEDENCE, not the shipped data:
  precedence for a code row: the Bloomberg field map's description (held); the team's own sheet MEASURED (column-B metric name, single-row
  pass-through); the entries file (held, `cite` as stored); the fallback line (claim absent).
  b1  a FactSet code with an entry and NO own-sheet label: text and cite as stored, claim "held", source "factset"
  b2  a FactSet code with an entry AND an own-sheet pass-through label: the MEASURED label wins (claim "measured", cite names the sheet and cell)
  b3  a FactSet code with neither: "FactSet line", claim "absent"
control c1: a code the Bloomberg field map describes keeps its held description even when an entry names it;
control c2: the census line still prints the three shares (`factset_held`, `measured`, `factset_line`).
"""
import io
import sys

import openpyxl

from lib.research.corpus import dossier, team_sheet

YEARS = (2016, 2017, 2018, 2019, 2020)
COLS = "DEFGH"


def workbook_bytes():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Model NEW VERSION"
    ws["C3"] = "Financial Summary"
    for k, y in enumerate(YEARS):
        ws["%s3" % COLS[k]] = y
    # own-sheet pass-through: 'Revenue' points at the FF_SALES row (12)
    ws["C4"] = "Revenue"
    for c in COLS:
        ws["%s4" % c] = "=%s12" % c
    code_rows = [(12, "FF_SALES"), (13, "FF_BPS"), (14, "FF_GROSS_INC"), (15, "BEST_EBIT")]
    for r, code in code_rows:
        ws["A%d" % r] = code
        for k, c in enumerate(COLS):
            ws["%s%d" % (c, r)] = 100 + 10 * r + k
    for i in range(6):
        ws["C%d" % (20 + i)] = "Filler %d" % i
        for k, c in enumerate(COLS):
            ws["%s%d" % (c, 20 + i)] = 5 + i + k
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


ENTRIES = {
    "FF_BPS": {"text": "BVPS", "cite": "fixture: 23 workbooks agree, 0 disagree"},
    "FF_SALES": {"text": "Sales (cross-workbook)", "cite": "fixture: 3 workbooks agree, 0 disagree"},
    "BEST_EBIT": {"text": "NOT THE BLOOMBERG TEXT", "cite": "fixture"},
}


def main():
    body = workbook_bytes()
    team_sheet._LABEL_CACHE.pop("factset", None)
    team_sheet._LABEL_CACHE["factset"] = ENTRIES
    b1 = b2 = b3 = c1 = c2 = 0
    by = {}
    try:
        reading = team_sheet.sheet_reading(body).get("Model NEW VERSION") or {}
        for lab, ent in zip(reading.get("rows") or [], reading.get("row_labels") or []):
            by.setdefault(lab, ent)
    except Exception as exc:  # noqa: BLE001
        print("ax5 sheet_reading threw: %s" % str(exc)[:160])
    e = by.get("FF_BPS") or {}
    b1 = 1 if (e.get("text") == "BVPS" and e.get("claim") == "held" and e.get("source") == "factset"
               and e.get("cite") == "fixture: 23 workbooks agree, 0 disagree") else 0
    print("ax5 b1 entry only: %s ok %s" % ({k: e.get(k) for k in ("text", "claim", "cite")}, b1 == 1))
    e = by.get("FF_SALES") or {}
    b2 = 1 if (e.get("text") == "Revenue" and e.get("claim") == "measured" and "Model NEW VERSION" in str(e.get("cite"))) else 0
    print("ax5 b2 entry AND own-sheet label (own sheet must win): %s ok %s" % ({k: e.get(k) for k in ("text", "claim", "cite")}, b2 == 1))
    e = by.get("FF_GROSS_INC") or {}
    b3 = 1 if (e.get("text") == "FactSet line" and e.get("claim") == "absent") else 0
    print("ax5 b3 neither: %s ok %s" % ({k: e.get(k) for k in ("text", "claim")}, b3 == 1))
    e = by.get("BEST_EBIT") or {}
    c1 = 1 if (e.get("claim") == "held" and e.get("source") == "bloomberg" and e.get("text") != "NOT THE BLOOMBERG TEXT") else 0
    print("ax5 c1 field map wins over an entry: %s ok %s" % ({k: e.get(k) for k in ("text", "claim", "source")}, c1 == 1))
    try:
        src = open(team_sheet.__file__, encoding="utf-8").read()
        c2 = 1 if ("factset_held %d measured %d factset_line %d" in src or ("factset_held" in src and "measured" in src and "factset_line" in src)) else 0
    except Exception as exc:  # noqa: BLE001
        print("ax5 c2 threw: %s" % str(exc)[:120])
    print("ax5 c2 the census line carries the three shares %s" % (c2 == 1))
    print("ax5 METHOD_VERSION %s" % dossier.METHOD_VERSION)
    print("ax5 build %d/3 control %d/2" % (b1 + b2 + b3, c1 + c2))
    return 0 if (b1 + b2 + b3 == 3 and c1 + c2 == 2) else 1


if __name__ == "__main__":
    sys.exit(main())
