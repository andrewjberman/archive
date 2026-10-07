"""AMGT_RESAPP round 77 -- AMGT-ba-4 checks (the /freshness PAGE: FWD-7 rulings 1-2 and FWD-14's owner line).

  python r77_ba4.py --crit AC1|AC2 [--portal portal]

AC1 (build, the page's own tests): `bun test src/pages/Freshness/` passes in the portal checkout, and the test file carries
    the five new cases by name (see CASES).
AC2 (build, the source): the page asks for the page view, renders the served flag and keyed date, hides an input no
    covered name has, does not set the not-collected note in the muted text colour, and renders the owner line and the
    out-of-date statement.

Prints PASS/FAIL clause lines and `R77 BA4 <CRIT> SERVED: YES|NO`; exit 0 on YES.
"""
import argparse
import os
import re
import subprocess
import sys

CASES = (
    "a never-collected input is not flagged",
    "the date column shows the keyed date",
    "an input no covered name has is not a column",
    "the lists owner line is shown",
    "the lists out-of-date statement is shown",
)


def _read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except (IOError, OSError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    ap.add_argument("--portal", default="portal")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("{0} {1} {2}".format("PASS" if cond else "FAIL", name, detail))

    def verdict():
        yes = bool(ok) and all(ok)
        print("R77 BA4 {0} SERVED: {1}".format(a.crit, "YES" if yes else "NO"))
        return 0 if yes else 1

    page_dir = os.path.join(a.portal, "src", "pages", "Freshness")
    page = _read(os.path.join(page_dir, "Freshness.tsx"))
    tests = _read(os.path.join(page_dir, "Freshness.test.tsx"))
    client = _read(os.path.join(a.portal, "src", "api", "endpoints", "amgt-lead-panel.ts"))
    if page is None or tests is None or client is None:
        clause("C0 the page, its tests and the client file are readable under {0}".format(a.portal), False,
               "page {0}, tests {1}, client {2}".format(page is not None, tests is not None, client is not None))
        return verdict()

    if a.crit == "AC1":
        missing = [c for c in CASES if c not in tests]
        print("   new cases named in the test file: {0} of {1}; missing {2}".format(len(CASES) - len(missing), len(CASES),
                                                                                  missing))
        clause("C1 the five new cases are in the test file by name", not missing, "{0}".format(len(missing)))
        try:
            p = subprocess.run(["bun", "test", "src/pages/Freshness/"], cwd=a.portal, capture_output=True, timeout=600)
            out = (p.stdout + p.stderr).decode("utf-8", errors="replace")
            code = p.returncode
        except Exception as err:  # noqa: BLE001
            out, code = "{0}: {1}".format(type(err).__name__, err), -1
        tail = [ln for ln in out.splitlines() if re.search(r"\b(pass|fail|expect\(\) calls|Ran )\b", ln)][-4:]
        for ln in tail:
            print("   bun test: " + ln.strip())
        failed = re.search(r"(\d+) fail", out)
        clause("C2 the Freshness tests pass", code == 0 and failed is not None and int(failed.group(1)) == 0,
               "exit {0}".format(code))
        return verdict()

    note = re.search(r'data-slot="uncollected-note"[^>]*>', page)
    clause("C1 the client asks for the page view", re.search(r"freshness\?view=page|view:\s*'page'|view=page", client)
           is not None)
    clause("C2 the page renders the served flag and keyed date", "keyed_date" in page + _read(
        os.path.join(page_dir, "freshnessRows.ts")) and 'data-slot="keyed-date"' in page)
    clause("C3 the not-collected note is not set in the muted text colour", note is not None
           and "semantic-text-muted" not in note.group(0), note.group(0)[:80] if note else "no note element")
    clause("C4 the table head is drawn from the inputs some covered name has, not from every input; a cell for a name "
           "that lacks a collected input still reads 'Not collected'",
           re.search(r"\{\s*INPUTS\.map\(", page) is None and "Not collected" in page)
    clause("C5 the owner line and the out-of-date statement have their own slots", 'data-slot="lists-owner"' in page
           and 'data-slot="lists-out-of-date"' in page)
    return verdict()


if __name__ == "__main__":
    sys.exit(main())
