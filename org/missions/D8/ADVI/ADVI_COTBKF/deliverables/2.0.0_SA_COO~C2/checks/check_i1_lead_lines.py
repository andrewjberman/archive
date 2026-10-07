"""CB9i1-AC2 check (2.0.0_SA_COO~C2, round 9): the new FWD-6 page adds a RETURNS lead line and changes no other lead line.

Compares the lead lines (lines starting with "- " under the first "## " heading, up to the second) of the round-9 page against round 8's committed page.
LAST line: LEAD-LINES old=<n> new=<m> returns_added=<bool> others_unchanged=<bool>
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[8]
D = ROOT / "org/missions/D8/ADVI/ADVI_COTBKF/deliverables"
OLD = D / "0.9.0_WK_ADVI_COTBKF~24/COVERAGE_STATEMENT.md"
NEW = D / "0.9.0_WK_ADVI_COTBKF~25/COVERAGE_STATEMENT.md"


def lead(path: pathlib.Path) -> list:
    if not path.is_file():
        return []
    out, heads = [], 0
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            heads += 1
            if heads == 2:
                break
            continue
        if heads == 1 and ln.startswith("- "):
            out.append(ln.strip())
    return out


def main() -> int:
    old, new = lead(OLD), lead(NEW)
    returns = [ln for ln in new if ln.upper().startswith("- RETURNS")]
    others = [ln for ln in new if not ln.upper().startswith("- RETURNS")]
    print("LEAD-LINES old=%d new=%d returns_added=%s others_unchanged=%s"
          % (len(old), len(new), len(returns) == 1, bool(old) and others == old))
    return 0


if __name__ == "__main__":
    sys.exit(main())
