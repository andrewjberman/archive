"""T5-AC4 -- clause (c): find, in PORTAL SOURCE AT THE PIN, the code that decides WHICH asset-class
groups render, and what it does with a group key it does not know.

Instrument: portal submodule object store at e85f6eb84f (the superproject pin). Read-only.
"""
import re
import subprocess
import sys

PORTAL = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/portal"
PIN = "e85f6eb84f"

# The DECIDER shapes: a literal enumeration of class names, or a keyed map of them.
CLASS_LIT = re.compile(r"'(Fixed Income|Equity|Cash|Hedge|Commodities|Structured|Alternatives|Fixed Income / Cash)'"
                       r"|\"(Fixed Income|Equity|Cash|Hedge|Commodities|Structured|Alternatives)\"")
DECIDER = re.compile(r"assetClassOrder|ASSET_CLASS|assetClasses|groupedHoldings|\.map\(|\.filter\(|Object\.keys|Object\.entries|order\s*=|ORDER\s*=|CATEGORY|categories")

files = [ln.strip() for ln in open(sys.argv[1]) if ln.strip()]
for f in files:
    r = subprocess.run(["git", "-C", PORTAL, "cat-file", "blob", "%s:%s" % (PIN, f)], capture_output=True)
    if r.returncode != 0:
        print("\n##### %s -- UNREADABLE rc=%d %s" % (f, r.returncode, r.stderr.decode()[:160]))
        continue
    lines = r.stdout.decode("utf-8", "replace").splitlines()
    lit = [(i + 1, ln.rstrip()) for i, ln in enumerate(lines) if CLASS_LIT.search(ln)]
    print("\n##### %s  (%d lines) -- %d line(s) carrying a CLASS-NAME LITERAL" % (f, len(lines), len(lit)))
    for n, ln in lit:
        mark = "  <== DECIDER" if DECIDER.search(ln) else ""
        print("  :%-5d %s%s" % (n, ln.strip()[:175], mark))
