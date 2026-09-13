#!/usr/bin/env python3
"""
POSN_ASTTAX.TO-T4-1 / cell AT3-s-4 / T4-AC1 -- per-copy membership census of
ETF_MANAGEMENT_STYLE for the six-ticker retag set, WORKTREE and HEAD stated separately.

INSTRUMENT: ast.literal_eval over the map's own assignment node. NOT a token grep --
a string census cannot separate a KEY from a comment or a docstring mention, and the
question here is whole-value membership in a dict. The module is never imported (no
import side effects, and the three copies would shadow each other on sys.modules).

DENOMINATOR DISCIPLINE: every count printed beside what it counts. The copy set is not
recalled -- it is the file list comp-find printed for 'ETF_MANAGEMENT_STYLE' [corpus=all],
MINUS the files that only mention the symbol without defining the map (the re-export in
_shared/__init__.py and the consumer lambda), which this script proves by finding no
assignment node in them rather than by asserting it.
"""
import ast
import os
import sys

RETAG_SET = ["DBC", "GLD", "GSG", "IAU", "SLV", "USO"]
MAP_NAME = "ETF_MANAGEMENT_STYLE"

# (label, worktree path, HEAD-blob dump path)
# Every file comp-find returned in the SURFACED band is carried here, including the two
# that are expected NOT to define the map -- an expectation that is tested, not assumed.
COPIES = [
    ("_shared",
     "infra/aws/lambda/v2_portal/_shared/etf_classification.py",
     ".scratch/head/_shared_etf_classification.py"),
    ("partners",
     "infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/etf_classification.py",
     ".scratch/head/partners_lambdas_opal-partners-data_etf_classification.py"),
    ("etf-returns",
     "infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-generate-etf-returns/etf_classification.py",
     ".scratch/head/yang_pipeline_portfolios_yang-generate-etf-returns_etf_classification.py"),
    ("_shared/__init__ (re-export?)",
     "infra/aws/lambda/v2_portal/_shared/__init__.py",
     None),
    ("positioning consumer (mention?)",
     "infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-positioning/lambda_function.py",
     None),
]


def read_text(path):
    if path is None or not os.path.exists(path):
        return None
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8")


def extract_map(src, name):
    """Return the dict literal assigned to `name`, or None if this file does not define it."""
    if src is None:
        return None
    tree = ast.parse(src)
    for node in tree.body:
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            continue
        for tgt in targets:
            if isinstance(tgt, ast.Name) and tgt.id == name:
                return ast.literal_eval(node.value)
    return None


def census(label, path, head_path):
    rows = {}
    for plane, p in (("WORKTREE", path), ("HEAD", head_path)):
        src = read_text(p)
        if src is None:
            rows[plane] = ("NO-SUCH-FILE", None)
            continue
        m = extract_map(src, MAP_NAME)
        if m is None:
            rows[plane] = ("NO-MAP-DEFINED", None)
        else:
            rows[plane] = ("MAP", m)
    return rows


def main():
    print("T4-AC1 -- ETF_MANAGEMENT_STYLE MEMBERSHIP, PER COPY, RETAG SET = %s (n=%d)"
          % (", ".join(RETAG_SET), len(RETAG_SET)))
    print("=" * 108)

    definers = []
    results = {}
    for label, path, head_path in COPIES:
        rows = census(label, path, head_path)
        results[label] = (rows, path)
        wt_kind, wt_map = rows["WORKTREE"]
        hd_kind, hd_map = rows.get("HEAD", ("NOT-DUMPED", None))
        print("")
        print("COPY: %s" % label)
        print("  path: %s" % path)
        if wt_kind != "MAP":
            print("  WORKTREE: %s  -> NOT A COPY OF THE MAP; it references the symbol only."
                  % wt_kind)
            continue
        definers.append(label)
        print("  WORKTREE: map defined, %d key(s)" % len(wt_map))
        if hd_kind == "MAP":
            print("  HEAD    : map defined, %d key(s)" % len(hd_map))
        else:
            print("  HEAD    : %s" % hd_kind)

    print("")
    print("=" * 108)
    print("DEFINING COPIES (the denominator for the table below): %d -- %s"
          % (len(definers), ", ".join(definers)))
    print("NON-DEFINING files that carry the symbol: %d -- counted by comp-find, excluded here "
          "because ast finds no assignment node in them." % (len(COPIES) - len(definers)))
    print("")

    for plane in ("WORKTREE", "HEAD"):
        header = "%-6s | " % "TICKER" + " | ".join("%-14s" % d for d in definers) + " | PRESENT-IN"
        print("PLANE = %s" % plane)
        print(header)
        print("-" * len(header))
        present_total = 0
        for t in RETAG_SET:
            cells = []
            n_present = 0
            for d in definers:
                rows, _ = results[d]
                kind, m = rows[plane]
                if kind != "MAP":
                    cells.append("%-14s" % "N/A")
                    continue
                if t in m:
                    cells.append("%-14s" % ("PRESENT=%s" % m[t]))
                    n_present += 1
                else:
                    cells.append("%-14s" % "ABSENT")
            present_total += n_present
            print("%-6s | " % t + " | ".join(cells) + " | %d of %d" % (n_present, len(definers)))
        print("-" * len(header))
        print("TOTAL PRESENT CELLS: %d of %d (6 tickers x %d copies)"
              % (present_total, len(RETAG_SET) * len(definers), len(definers)))
        print("")

    # The neighbouring control: VIXY is the ticker AT2-s-5 measured as ALREADY carrying a
    # real value and therefore excluded from its write set. If this census said ABSENT for
    # VIXY too it would be measuring the wrong thing.
    print("DISCRIMINATION CONTROL -- a ticker that MUST read PRESENT for this instrument to")
    print("be able to report PRESENT at all (AT2-s-5 excluded VIXY from its write set because")
    print("VIXY already read 'passive'):")
    for d in definers:
        rows, _ = results[d]
        kind, m = rows["WORKTREE"]
        print("  %-14s VIXY -> %s" % (d, ("PRESENT=%s" % m["VIXY"]) if "VIXY" in m else "ABSENT"))

    return 0


if __name__ == "__main__":
    sys.exit(main())
