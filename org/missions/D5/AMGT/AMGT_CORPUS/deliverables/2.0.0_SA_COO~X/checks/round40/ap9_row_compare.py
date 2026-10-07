"""AMGT_CORPUS round 40, CRPS-ap-9 -- FWD-12's row comparison (PRD v0.9 ADDENDUM D): the Model tab's rows, order and labels
against the team's own sheet, per research folder.

Read-only over the locally synced research library; it writes nothing. The team sheet is `Model NEW VERSION` where the workbook
holds it, else `Model`; a folder with no figure-carrying workbook is counted as "compare to the master template" and not compared
here (the master is not in the library root). For the workbooks that hold both sheets, `Model` is printed beside, reported and not
graded. No figure is read out: only row labels (the first text cell in columns A to D of a row that carries a label and two or
more numbers), compared after lowercasing and collapsing spaces.

  python ap9_row_compare.py        (PYTHONPATH=. from the repository root)

FIRST OUTPUT (the CTO's ask): how many labels ALL the `Model NEW VERSION` sheets share. Then, per workbook: team-sheet labels;
page rows found on the sheet (of the page's rows); of those, how many keep the page's order (longest run in sheet order).
"""
import collections
import json
import os
import re
import sys

import openpyxl

from lib.research.corpus import library

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_FIGURE_ROWS = 10


def norm(text):
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def labels_of(ws):
    out = []
    for row in ws.iter_rows(min_row=1, max_row=400, max_col=60, values_only=True):
        label = next((v for v in row[:4] if isinstance(v, str) and v.strip()), None)
        nums = sum(1 for v in row if isinstance(v, (int, float)) and not isinstance(v, bool))
        if label is not None and nums >= 2:
            out.append(norm(label))
    return out


def in_order(page, sheet_labels):
    """How many of the page's rows found on the sheet appear there in the page's own order (longest increasing run)."""
    pos = {}
    for i, lab in enumerate(sheet_labels):
        pos.setdefault(lab, i)
    seq = [pos[p] for p in page if p in pos]
    best = []
    for x in seq:
        lo, hi = 0, len(best)
        while lo < hi:
            mid = (lo + hi) // 2
            if best[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(best):
            best.append(x)
        else:
            best[lo] = x
    return len(seq), len(best)


def main():
    page_doc = json.load(open(os.path.join(HERE, "ap9_page_rows.json"), encoding="utf-8"))
    page = [norm(r) for g in page_doc["groups"] for r in g["rows"]]
    root = library.library_root()
    folders = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))
    rows = []
    folders_with_figures = set()
    for folder in folders:
        for dirpath, _dirs, files in os.walk(os.path.join(root, folder)):
            for name in sorted(files):
                if not name.lower().endswith(".xlsx") or name.startswith("~$"):
                    continue
                wb = openpyxl.load_workbook(os.path.join(dirpath, name), read_only=True, data_only=True)
                sheets = {s: labels_of(wb[s]) for s in ("Model NEW VERSION", "Model") if s in wb.sheetnames}
                wb.close()
                sheets = {s: v for s, v in sheets.items() if len(v) >= MIN_FIGURE_ROWS}
                if not sheets:
                    continue
                folders_with_figures.add(folder)
                team = "Model NEW VERSION" if "Model NEW VERSION" in sheets else "Model"
                rows.append((folder, name, team, sheets))
    new_sheets = [s["Model NEW VERSION"] for _f, _n, _t, s in rows if "Model NEW VERSION" in s]
    model_sheets = [s["Model"] for _f, _n, _t, s in rows if "Model" in s]
    print("page rows %d (one label list for every name: %s)" % (len(page), page_doc["source"]))
    print("library folders %d; with a figure-carrying workbook %d; to compare to the master template %d" % (
        len(folders), len(folders_with_figures), len(folders) - len(folders_with_figures)))
    print("workbooks compared %d: team sheet `Model NEW VERSION` %d, `Model` %d" % (
        len(rows), sum(1 for r in rows if r[2] == "Model NEW VERSION"), sum(1 for r in rows if r[2] == "Model")))
    for title, group in (("Model NEW VERSION", new_sheets), ("Model", model_sheets)):
        if not group:
            continue
        counts = collections.Counter(lab for labs in group for lab in set(labs))
        shared = [lab for lab, n in counts.items() if n == len(group)]
        print("`%s` sheets %d: distinct labels %d; labels ALL %d share %d; shared by 90%% or more %d; label rows per sheet min %d max %d" % (
            title, len(group), len(counts), len(group), len(shared),
            sum(1 for n in counts.values() if n >= 0.9 * len(group)), min(len(x) for x in group), max(len(x) for x in group)))
        print("   page rows among the labels all share: %d of %d" % (sum(1 for p in set(page) if p in shared), len(set(page))))
    print("")
    tot = collections.Counter()
    for folder, name, team, sheets in rows:
        found, ordered = in_order(page, sheets[team])
        beside = ""
        if team == "Model NEW VERSION" and "Model" in sheets:
            f2, o2 = in_order(page, sheets["Model"])
            beside = " | beside, `Model`: labels %d page rows found %d in order %d" % (len(sheets["Model"]), f2, o2)
        tot["found"] += found
        tot["ordered"] += ordered
        tot["n"] += 1
        tot["full"] += 1 if found == len(page) else 0
        print("%-32s %-18s labels %3d page rows found %2d of %d in order %2d%s" % (
            folder[:32], team, len(sheets[team]), found, len(page), ordered, beside))
    print("")
    print("workbooks %d; page rows found on the team sheet: mean %.1f of %d; in the page's order: mean %.1f; workbooks carrying all %d page rows %d" % (
        tot["n"], tot["found"] / float(tot["n"]), len(page), tot["ordered"] / float(tot["n"]), len(page), tot["full"]))
    on = collections.Counter()
    for _f, _n, team, sheets in rows:
        for p in set(page):
            if p in set(sheets[team]):
                on[p] += 1
    print("page rows by how many team sheets carry the same label (of %d):" % len(rows))
    for p in page:
        print("   %-52s %d" % (p[:52], on[p]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
