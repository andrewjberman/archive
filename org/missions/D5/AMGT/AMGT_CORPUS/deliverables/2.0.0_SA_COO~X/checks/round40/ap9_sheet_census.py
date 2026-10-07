"""AMGT_CORPUS round 40, CRPS-ap-9 -- FWD-12's sheet census (round-39 analysis ADDENDUM 1, ruling 2): for each research
folder's own workbook, which of the sheets `Model` and `Model NEW VERSION` carries the company's figures.

Read-only over the locally synced research library (`library.library_root()`); it opens each `.xlsx` with openpyxl in
read-only, values-only mode and writes nothing. It copies NO workbook content: per sheet it prints only the sheet's name and
counts (rows with a text label in the first four columns; numeric cells; rows that carry a label AND at least two numbers).

  python ap9_sheet_census.py            (PYTHONPATH=. from the repository root)

FINGERPRINT (added after the first run read 24 workbooks with figures on BOTH sheets): a sheet's fingerprint is a hash of its
numeric cells in reading order, rounded to 4 significant figures. Two DIFFERENT companies' workbooks sharing a fingerprint on a
sheet means that sheet holds the same numbers in both, so it is not that company's own figures (a sheet left as the template
shipped it, or as copied from another name). The census prints, per sheet, how many figure-carrying workbooks have a fingerprint
no other folder shares (OWN) and how many share one (SHARED), and re-reads the BOTH class on that basis.

A sheet "carries figures" when it has at least MIN_FIGURE_ROWS rows with a label and two or more numbers. The census prints, per
workbook, both counts side by side, then the totals: workbooks read, workbooks holding each sheet, and how many carry figures on
`Model` only, on `Model NEW VERSION` only, on both (a split, reported and not averaged) or on neither.
"""
import collections
import hashlib
import os
import sys

import openpyxl

from lib.research.corpus import library

SHEETS = ("Model", "Model NEW VERSION")
MIN_FIGURE_ROWS = 10
MAX_ROWS = 400
MAX_COLS = 60


def sheet_counts(ws):
    labelled = numeric = figure_rows = 0
    digest = hashlib.sha256()
    for row in ws.iter_rows(min_row=1, max_row=MAX_ROWS, max_col=MAX_COLS, values_only=True):
        has_label = any(isinstance(v, str) and v.strip() for v in row[:4])
        nums = sum(1 for v in row if isinstance(v, (int, float)) and not isinstance(v, bool))
        for v in row:
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                digest.update(("%.4g|" % v).encode("ascii"))
        labelled += 1 if has_label else 0
        numeric += nums
        figure_rows += 1 if (has_label and nums >= 2) else 0
    return labelled, numeric, figure_rows, digest.hexdigest()[:12]


def main():
    root = library.library_root()
    folders = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))
    books = []
    for folder in folders:
        for dirpath, _dirs, files in os.walk(os.path.join(root, folder)):
            for name in sorted(files):
                if name.lower().endswith(".xlsx") and not name.startswith("~$"):
                    books.append((folder, os.path.join(dirpath, name)))
    print("library folders %d workbooks %d (every .xlsx under a folder)" % (len(folders), len(books)))
    tally = collections.Counter()
    holds = collections.Counter()
    per_folder = collections.defaultdict(list)
    prints = {s: collections.defaultdict(set) for s in SHEETS}
    carried = []
    unread = []
    for folder, path in books:
        name = os.path.basename(path)
        try:
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        except Exception as exc:  # a workbook that cannot be opened is listed, never skipped silently
            unread.append((folder, name, "%s: %s" % (type(exc).__name__, str(exc)[:80])))
            continue
        names = list(wb.sheetnames)
        counts = {}
        for sheet in SHEETS:
            if sheet in names:
                holds[sheet] += 1
                counts[sheet] = sheet_counts(wb[sheet])
        wb.close()
        if not counts:
            tally["neither sheet present"] += 1
            verdict = "NEITHER-PRESENT"
        else:
            carries = [s for s in SHEETS if s in counts and counts[s][2] >= MIN_FIGURE_ROWS]
            if carries == ["Model"]:
                verdict = "MODEL"
            elif carries == ["Model NEW VERSION"]:
                verdict = "MODEL-NEW-VERSION"
            elif len(carries) == 2:
                verdict = "BOTH"
            else:
                verdict = "NEITHER-CARRIES"
            tally[verdict] += 1
        per_folder[folder].append(verdict)
        for s in SHEETS:
            if s in counts and counts[s][2] >= MIN_FIGURE_ROWS:
                prints[s][counts[s][3]].add(folder)
        carried.append((folder, name, verdict, {s: counts[s][3] for s in counts if counts[s][2] >= MIN_FIGURE_ROWS}))
        cells = " | ".join("%s labelled %d numeric %d figure_rows %d fp %s" % ((s,) + counts[s]) if s in counts else "%s ABSENT" % s
                           for s in SHEETS)
        print("%-34s %-70s %-18s %s" % (folder[:34], name[:70], verdict, cells))
    print("")
    print("workbooks opened %d of %d; could not open %d" % (len(books) - len(unread), len(books), len(unread)))
    for folder, name, why in unread:
        print("  UNREAD %s / %s -- %s" % (folder, name, why))
    print("workbooks holding sheet `Model` %d; holding `Model NEW VERSION` %d" % (holds["Model"], holds["Model NEW VERSION"]))
    print("carries figures (>= %d rows with a label and two numbers): %s" % (
        MIN_FIGURE_ROWS, "; ".join("%s %d" % (k, tally[k]) for k in (
            "MODEL", "MODEL-NEW-VERSION", "BOTH", "NEITHER-CARRIES", "neither sheet present"))))
    print("")
    for s in SHEETS:
        own = sum(1 for _f, _n, _v, fps in carried if s in fps and len(prints[s][fps[s]]) == 1)
        shared = sum(1 for _f, _n, _v, fps in carried if s in fps and len(prints[s][fps[s]]) > 1)
        print("sheet `%s`: figure-carrying workbooks %d; fingerprint OWN (no other folder has it) %d; SHARED with another folder %d; "
              "distinct fingerprints %d" % (s, own + shared, own, shared, len(prints[s])))
    both = [(f_, n_, fps) for f_, n_, v_, fps in carried if v_ == "BOTH"]
    reread = collections.Counter()
    for f_, n_, fps in both:
        m_own = len(prints["Model"][fps["Model"]]) == 1
        n_own = len(prints["Model NEW VERSION"][fps["Model NEW VERSION"]]) == 1
        key = ("both own" if (m_own and n_own) else "only `Model NEW VERSION` own" if n_own else "only `Model` own" if m_own
               else "neither own")
        reread[key] += 1
        print("  BOTH %-34s %-66s Model %s | Model NEW VERSION %s" % (f_[:34], n_[:66], "OWN" if m_own else "SHARED",
                                                                    "OWN" if n_own else "SHARED"))
    print("the BOTH class (%d workbooks) re-read by fingerprint: %s" % (len(both), "; ".join(
        "%s %d" % (k, reread[k]) for k in ("both own", "only `Model NEW VERSION` own", "only `Model` own", "neither own"))))
    with_book = len(per_folder)
    print("folders with at least one workbook %d of %d; folders with none %d" % (with_book, len(folders), len(folders) - with_book))
    return 0


if __name__ == "__main__":
    sys.exit(main())
