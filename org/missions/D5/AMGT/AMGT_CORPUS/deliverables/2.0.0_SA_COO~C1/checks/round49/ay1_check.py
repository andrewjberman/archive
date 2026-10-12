"""AMGT_CORPUS round 49, CRPS-ay-1 (C-S64: the team's blocks, the reader half) -- the issuer's mechanical check. Issuer's file; a worker never edits it.

  PYTHONPATH=. python ay1_check.py                       fixtures: `ay1 build <b>/4 control <c>/2`
  PYTHONPATH=. python ay1_check.py <path to team_sheet.py>   the same against another copy of the module
  PYTHONPATH=. python ay1_check.py --snapshot            write ay1_base_snapshot.json from the module under test (run ONCE, at the base)
  PYTHONPATH=. python ay1_check.py --live <key>...       the stored workbooks of real names (S3 reads only)

The contract is decompositions/AMGT_CORPUS_DECOMP.md section 1 (v49.1; CTO round-48 ADDENDUM 1). Fixtures are built with openpyxl in memory:
  A  a 'Model' sheet, the ROG-like layout: a title row, a year row and four tables side by side whose label column repeats (`EPS`), then a
     second case block whose columns carry their own years and NO text separator, a value in a column no header of its block covers, and a
     header-less row that carries a label (`Average`); a control FIGURE row holding `NA`, `#N/A` and a range string; a year row that repeats
     the period header and a FIGURE row after it
  B  a 'Model NEW VERSION' sheet, the 9433 JP-like layout: a title cell inside the first body row, year rows beside it, a left table whose
     values sit under other years: a PERIOD block
  C  a plain sheet with no block (the control: its answer must equal the base's, key for key)
  D  a 'Model' sheet with a QUARTERLY block headed by text period labels (`1Q26`...): a PERIOD block, never a case table
"""
import importlib.util
import io
import json
import os
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT = os.path.join(HERE, "ay1_base_snapshot.json")


def _load(argv):
    paths = [a for a in argv if a.endswith(".py") and os.path.exists(a)]
    if paths:
        spec = importlib.util.spec_from_file_location("ay1_ts", paths[0])
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    from lib.research.corpus import team_sheet

    return team_sheet


def _canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


def _alpha(v):
    """The contract's (b): a text cell with a letter, not an error token, not NA/N/A/NM, not a range."""
    if not isinstance(v, str) or not v.strip():
        return False
    t = v.strip()
    return (any(ch.isalpha() for ch in t) and not t.startswith("#") and t.lower() not in ("na", "n/a", "nm")
            and not all(ch in "0123456789.,%x -" for ch in t))


def _put(ws, row, col, value, fmt=None):
    c = ws.cell(row=row, column=col, value=value)
    if fmt:
        c.number_format = fmt


def _figure_rows(ws, first, last, label_col, first_col, last_col, labels):
    for k, row in enumerate(range(first, last + 1)):
        _put(ws, row, label_col, labels[k % len(labels)] + (" %d" % k if k >= len(labels) else ""))
        for col in range(first_col, last_col + 1):
            _put(ws, row, col, round(10.0 + row + col / 7.0, 4), "#,##0.00")


def _book(sheet_title, build):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_title
    build(ws)
    out = io.BytesIO()
    wb.save(out)
    return out.getvalue()


def _fixture_a(ws):
    # period header: B label, D..Q = 2016..2029 (14 periods)
    _put(ws, 4, 2, "Fiscal year")
    for k, col in enumerate(range(4, 18)):
        _put(ws, 4, col, 2016 + k)
    _figure_rows(ws, 5, 16, 2, 4, 17, ["Revenue", "Growth", "Gross profit", "Operating income", "Net income", "EPS growth"])
    _put(ws, 17, 2, "Dividend Yield")
    _put(ws, 17, 4, "2.8%-3.3%")
    _put(ws, 17, 5, "NA")
    _put(ws, 17, 6, "#N/A")
    for col in range(7, 18):
        _put(ws, 17, col, 0.03 + col / 1000.0, "0.0%")
    # block 1 (case): title row, year row, four side-by-side tables (label columns B F J N); R22 sits under no header of the block
    for col, text in ((2, "Upside Case"), (6, "Base Case"), (10, "Downside Case"), (14, "Upside / Downside")):
        _put(ws, 20, col, text)
    for start in (3, 7, 11, 15):
        for k in range(3):
            _put(ws, 21, start + k, 2026 + k)
    for row, label in ((22, "EPS"), (23, "Multiple"), (24, "Price"), (25, "Return")):
        for label_col, start, name in ((2, 3, label), (6, 7, label), (10, 11, label), (14, 15, {"EPS": "Ratio", "Multiple": "Tgt", "Price": "Multiple", "Return": "Return"}[label])):
            _put(ws, row, label_col, name)
            for k in range(3):
                _put(ws, row, start + k, round(1.5 * row + start + k, 3), "0.00" if row == 22 and start == 3 else None)
    _put(ws, 22, 18, 99.5)
    # block 2 (case): columns carry their own years, no text separator
    _put(ws, 27, 2, "Opal Case Assumptions")
    for col, text in ((2, "Upside Case"), (6, "Base Case"), (10, "Downside Case")):
        _put(ws, 28, col, text)
    _put(ws, 29, 2, "Year")
    for start in (3, 7, 11):
        for k in range(3):
            _put(ws, 29, start + k, 2026 + k)
    for row, label in ((30, "Rev Growth"), (31, "Earnings Margin"), (32, "EPS")):
        _put(ws, row, 2, label)
        for start in (3, 7, 11):
            for k in range(3):
                _put(ws, row, start + k, round(0.01 * row + start + k, 4), "0.0%")
    # a year row that repeats the period header, then a plain FIGURE row
    for k, col in enumerate(range(3, 14)):
        _put(ws, 34, col, 2015 + k)
    _put(ws, 35, 2, "Earning Margin")
    for col in range(4, 14):
        _put(ws, 35, col, round(0.1 + col / 100.0, 4), "0.0%")
    # a header-less row that carries a label inside the period columns: an UNREAD block
    _put(ws, 40, 4, " Average")
    for col in range(5, 9):
        _put(ws, 40, col, round(1.0 + col / 10.0, 2))


def _fixture_b(ws):
    _put(ws, 4, 3, "Year")
    for k, col in enumerate(range(5, 20)):
        _put(ws, 4, col, 2016 + k)
    _figure_rows(ws, 5, 16, 3, 5, 19, ["Revenue", "Operating Income", "EBITDA", "EPS", "DPS", "BVPS"])
    for k in range(5):
        _put(ws, 20, 15 + k, 2026 + k)                     # O..S: the same years as the period header there
    _put(ws, 21, 4, "Upside/Downside")
    _put(ws, 21, 13, "Consensus Case")
    _put(ws, 21, 14, "Revenue")
    for col in range(15, 19):
        _put(ws, 21, col, 6000.0 + col)
    _put(ws, 21, 19, "#N/A")
    for k in range(5):
        _put(ws, 22, 5 + k, 2026 + k)                     # E..I: other years than the period header there
    _put(ws, 22, 14, "y/y Growth")
    for col in range(15, 20):
        _put(ws, 22, col, 0.05 + col / 1000.0)
    _put(ws, 23, 4, "Ratio")
    for col in range(5, 10):
        _put(ws, 23, col, "#N/A")
    _put(ws, 23, 14, "EPS")
    for col in range(15, 19):
        _put(ws, 23, col, 200.0 + col)
    _put(ws, 24, 4, "Tgt")
    for col in range(5, 10):
        _put(ws, 24, col, 1000.0 + col)
    _put(ws, 24, 14, "y/y Growth")
    for col in range(15, 19):
        _put(ws, 24, col, 0.04 + col / 1000.0)
    _put(ws, 25, 4, "Multiple")
    for col in range(5, 9):
        _put(ws, 25, col, "#N/A")
    _put(ws, 26, 4, "Return")
    for col in range(5, 10):
        _put(ws, 26, col, "#N/A")
    for k, col in enumerate(range(5, 20)):                 # row 27 blank; the main grid's years again
        _put(ws, 28, col, 2016 + k)
    _put(ws, 29, 3, "Margin")
    for col in range(5, 20):
        _put(ws, 29, col, round(0.2 + col / 100.0, 4), "0.0%")


def _fixture_c(ws):
    _put(ws, 3, 2, "Year")
    for k, col in enumerate(range(4, 12)):
        _put(ws, 3, col, 2018 + k)
    _figure_rows(ws, 4, 16, 2, 4, 11, ["Revenue", "Growth", "Margin", "EPS"])
    _put(ws, 17, 2, "Dividend Yield")
    _put(ws, 17, 4, "NM")
    _put(ws, 17, 5, "#DIV/0!")
    _put(ws, 17, 6, "12.4x-15.6x")
    for col in range(7, 12):
        _put(ws, 17, col, 0.02 + col / 1000.0)


def _fixture_d(ws):
    _put(ws, 4, 2, "Fiscal year")
    for k, col in enumerate(range(4, 14)):
        _put(ws, 4, col, 2016 + k)
    _figure_rows(ws, 5, 16, 2, 4, 13, ["Revenue", "Growth", "Margin", "EPS"])
    _put(ws, 20, 2, "Quarterly view")
    for k, col in enumerate(range(4, 8)):
        _put(ws, 21, col, "%dQ26" % (k + 1))
    for row, label in ((22, "Revenue"), (23, "EPS")):
        _put(ws, row, 2, label)
        for col in range(4, 8):
            _put(ws, row, col, round(2.0 * row + col, 3), "0.00")


def _answers(ts):
    out = {}
    for name, title, build in (("A", "Model", _fixture_a), ("B", "Model NEW VERSION", _fixture_b), ("C", "Model", _fixture_c),
                               ("D", "Model", _fixture_d)):
        reading = ts.sheet_reading(_book(title, build))
        detail = reading[title]
        out[name] = {"answer": ts._answer("own_model", (None, "fixture/%s.xlsx" % name, title, detail, None)),
                     "master": ts._answer("master", (None, "fixture/%s.xlsx" % name, title, detail, None))}
    return out


def _rows_of(answer, klass):
    return [n for n, c in zip(answer["row_numbers"], answer["row_classes"]) if c == klass]


def _span(blocks):
    return [(x["first_row"], x["last_row"], x["kind"]) for x in blocks]


def _build(ts, snap):
    ans = _answers(ts)
    a, b, c, d = ans["A"]["answer"], ans["B"]["answer"], ans["C"]["answer"], ans["D"]["answer"]
    arms, controls = {}, {}

    # d1: fixture A -- the BLOCK rows, nothing else moved
    want = [22, 23, 24, 25, 29, 30, 31, 32, 40]
    figures_a = _rows_of(a, "FIGURE")
    arms["d1"] = (_rows_of(a, "BLOCK") == want and 17 in figures_a and 35 in figures_a and all(n in figures_a for n in range(5, 17))
                  and all(a["row_values"][i] is None and a["row_formats"][i] is None for i, k in enumerate(a["row_classes"]) if k == "BLOCK")
                  and a["row_counts"].get("BLOCK") == 9 and sum(a["row_counts"].values()) == len(a["rows"])
                  and set(a["row_counts"]) == {"FIGURE", "HEADING", "CONTROL", "BLOCK"})
    # d2: fixture A -- the blocks as the sheet wrote them, each with its kind; a value under no header of its block is withheld
    blocks = a.get("blocks") or []
    ok = _span(blocks) == [(20, 25, "case"), (27, 32, "case"), (40, 40, "unread")]
    if ok:
        b1, b2, b3 = blocks
        rows1 = {r["row_number"]: r for r in b1["rows"]}
        cols = b1["columns"]
        ok = (cols[0] == "B" and cols[-1] == "R" and len(cols) == 17 and b1["withheld"] == 1 and b1["why"] is None
              and rows1[22]["cells"][cols.index("R")] is None
              and [r["row_number"] for r in b1["rows"]] == [20, 21, 22, 23, 24, 25]
              and rows1[20]["kind"] == "title" and rows1[21]["kind"] == "years" and rows1[22]["kind"] == "body"
              and not rows1[20]["block_row"] and rows1[22]["block_row"]
              and rows1[22]["cells"][cols.index("F")] == {"v": "EPS"} and rows1[22]["cells"][cols.index("N")] == {"v": "Ratio"}
              and rows1[21]["cells"][cols.index("D")]["v"] == 2027
              and rows1[22]["cells"][cols.index("C")] == {"v": round(1.5 * 22 + 3, 3), "f": "0.00"}
              and [r["row_number"] for r in b2["rows"]] == [27, 28, 29, 30, 31, 32]
              and {r["row_number"] for r in b2["rows"] if r["block_row"]} == {29, 30, 31, 32} and b2["withheld"] == 0
              and b3["columns"] == [] and b3["why"] and all(r["cells"] == [] for r in b3["rows"]) and b3["withheld"] == 0
              and [x["row_number"] for blk in blocks for x in blk["rows"] if x["block_row"]] == want)
    arms["d2"] = bool(ok)
    # d3: PERIOD blocks -- a year row beside a title cell (fixture B), a block headed by text period labels (fixture D)
    block_b = _rows_of(b, "BLOCK")
    bb = b.get("blocks") or []
    block_d = _rows_of(d, "BLOCK")
    bd = d.get("blocks") or []
    arms["d3"] = (block_b == [21, 23, 24] and 29 in _rows_of(b, "FIGURE")
                  and _span(bb) == [(20, 26, "period")]
                  and {r["row_number"]: r["block_row"] for r in bb[0]["rows"]} == {20: False, 21: True, 22: False, 23: True, 24: True, 25: False, 26: False}
                  and block_d == [22, 23] and _span(bd) == [(20, 23, "period")]
                  and [cell["v"] for cell in bd[0]["rows"][1]["cells"] if cell] == ["1Q26", "2Q26", "3Q26", "4Q26"]
                  and all(v is None for v in [d["row_values"][i] for i, k in enumerate(d["row_classes"]) if k == "BLOCK"]))
    # d4: a master answer keeps the BLOCK class and the block's words and carries no figure
    m = ans["A"]["master"]
    mb = m.get("blocks") or []
    numbers_in_cells = [cell["v"] for blk in mb for r in blk["rows"] for cell in r["cells"]
                        if cell and isinstance(cell["v"], (int, float)) and not isinstance(cell["v"], bool)]
    arms["d4"] = (_rows_of(m, "BLOCK") == want and all(v is None for v in m["row_values"]) and m["periods"] == []
                  and _span(mb) == [(20, 25, "case"), (27, 32, "case"), (40, 40, "unread")]
                  and len(numbers_in_cells) > 0 and all(isinstance(v, int) and 2026 <= v <= 2028 for v in numbers_in_cells)
                  and any(cell == {"v": "EPS"} for blk in mb for r in blk["rows"] for cell in r["cells"]))

    # controls: a sheet with no block equals the base's answer; fixture A's non-BLOCK rows equal the base's
    controls["c1"] = ("blocks" not in c and set(c["row_counts"]) == {"FIGURE", "HEADING", "CONTROL"}
                      and snap is not None and _canon(c) == _canon(snap["C"]))
    base_a = snap["A"] if snap is not None else None
    controls["c2"] = (base_a is not None and a["rows"] == base_a["rows"] and a["row_numbers"] == base_a["row_numbers"]
                      and a["row_labels"] == base_a["row_labels"] and a["periods"] == base_a["periods"]
                      and all(_canon(v) == _canon(bv) for v, bv, k in zip(a["row_values"], base_a["row_values"], a["row_classes"]) if k != "BLOCK")
                      and all(x == y or (x == "FIGURE" and y == "BLOCK") for x, y in zip(base_a["row_classes"], a["row_classes"])))
    return arms, controls


def _headerless_values(blocks):
    """Numeric value cells of a period/case block that have no header-like cell above them in their column within the block."""
    n = 0
    for blk in blocks:
        if blk["kind"] == "unread":
            continue
        headed = set()
        for r in blk["rows"]:
            for j, cell in enumerate(r["cells"]):
                is_num = cell is not None and isinstance(cell["v"], (int, float)) and not isinstance(cell["v"], bool)
                if is_num and r["kind"] == "body" and j not in headed:
                    n += 1
            if r["kind"] in ("title", "years"):
                headed.update(j for j, cell in enumerate(r["cells"]) if cell is not None)
    return n


def _live(ts, keys):
    from lib.research.harvest import store

    client = store._default_client()
    names = block_rows = left = headerless = 0
    by_kind = {"period": 0, "case": 0, "unread": 0}
    split_ok = True
    for key in keys:
        ans = ts.rows_for(key, client=client)
        n = sum(1 for k in ans["row_classes"] if k == "BLOCK")
        blocks = ans.get("blocks") or []
        in_blocks = sum(1 for blk in blocks for r in blk["rows"] if r["block_row"])
        kinds = {"period": 0, "case": 0, "unread": 0}
        for blk in blocks:
            kinds[blk["kind"]] += sum(1 for r in blk["rows"] if r["block_row"])
        text_left = sum(1 for k, v in zip(ans["row_classes"], ans["row_values"]) if k == "FIGURE" and v and any(_alpha(x) for x in v))
        hv = _headerless_values(blocks)
        print("LIVE %s class %s block_rows %d blocks %d period %d case %d unread %d withheld %d figure_rows_with_text_separator %d" % (
            key, ans["class"], n, len(blocks), kinds["period"], kinds["case"], kinds["unread"],
            sum(blk["withheld"] for blk in blocks), text_left))
        names += int(n > 0 and len(blocks) > 0)
        block_rows += n
        for k, v in kinds.items():
            by_kind[k] += v
        split_ok = split_ok and in_blocks == n and sum(kinds.values()) == n
        left += text_left
        headerless += hv
    print("ay1 live block_names %d/%d block_rows %d split period %d case %d unread %d split_ok %s text_separator_rows_left %d headerless_values %d" % (
        names, len(keys), block_rows, by_kind["period"], by_kind["case"], by_kind["unread"], str(split_ok).lower(), left, headerless))
    return int(names == len(keys) and split_ok and left == 0 and headerless == 0 and block_rows > 0)


def main():
    argv = sys.argv[1:]
    ts = _load(argv)
    if "--snapshot" in argv:
        ans = _answers(ts)
        snap = {k: v["answer"] for k, v in ans.items()}
        with open(SNAPSHOT, "w", encoding="utf-8", newline="") as fh:
            json.dump(snap, fh, sort_keys=True, ensure_ascii=True, indent=1)
        print("ay1 snapshot written", SNAPSHOT, {k: len(v["rows"]) for k, v in snap.items()})
        return 0
    if "--live" in argv:
        keys = [a for a in argv[argv.index("--live") + 1:] if not a.startswith("--") and not a.endswith(".py")]
        return 0 if _live(ts, keys) else 1
    snap = json.load(open(SNAPSHOT, encoding="utf-8")) if os.path.exists(SNAPSHOT) else None
    try:
        arms, controls = _build(ts, snap)
    except Exception as exc:  # noqa: BLE001 -- a fault is a failed arm, printed, never a silent zero
        print("ay1 FAULT %s: %s" % (type(exc).__name__, str(exc)[:200]))
        arms, controls = {k: False for k in ("d1", "d2", "d3", "d4")}, {"c1": False, "c2": False}
    for k, v in sorted(arms.items()):
        print("ay1 %s ok %s" % (k, str(bool(v)).lower()))
    for k, v in sorted(controls.items()):
        print("ay1 %s ok %s" % (k, str(bool(v)).lower()))
    b, c = sum(1 for v in arms.values() if v), sum(1 for v in controls.values() if v)
    print("ay1 build %d/4 control %d/2" % (b, c))
    return 0 if (b == 4 and c == 2) else 1


if __name__ == "__main__":
    sys.exit(main())
