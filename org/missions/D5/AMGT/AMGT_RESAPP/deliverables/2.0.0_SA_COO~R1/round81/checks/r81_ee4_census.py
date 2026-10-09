"""AMGT_RESAPP round 81 -- AMGT-ee-4, the store half over the five stored 20-F names: every name re-cut by today's parser.

  python r81_ee4_census.py

Runs dd-1's read-only census (`python -m lib.research.filings.section_census --stored`) and reads its lines.
E1 the census names exactly five stored 20-F names (ASML_NA_Equity, BABA_US_Equity, NU_US_Equity, PBR_US_Equity, SAP_GY_Equity);
E2 every one of the five reads parser opal-filings-fetch/2.0.0 (re-cut by the merged cutter), none 1.0.0;
E3 ASML_NA_Equity's line reads business: OWN-HEADING;
E4 no risk item reads FALLBACK (the removed fallback heading is gone from every stored 20-F).
Verdict: R81 EE4 CENSUS: YES|NO (exit 0|1). At the base (2026-10-09) it reads NO: 5 of 5 at parser 1.0.0, ASML business NONE.
"""
from __future__ import annotations

import re
import subprocess
import sys

NAMES = {"ASML_NA_Equity", "BABA_US_Equity", "NU_US_Equity", "PBR_US_Equity", "SAP_GY_Equity"}
PARSER = "opal-filings-fetch/2.0.0"


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def main():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    p = subprocess.run([sys.executable, "-m", "lib.research.filings.section_census", "--stored"], cwd=root,
                       capture_output=True, text=True, env=dict(__import__("os").environ, PYTHONPATH=root))
    out = p.stdout or ""
    print(out.strip())
    lines = {m.group(1): m.group(0) for m in re.finditer(r"^(\S+_Equity) .*$", out, re.M)}
    r = [say(p.returncode == 0 and set(lines) == NAMES, "E1 the census names the five stored 20-F names: %s" % sorted(lines))]
    old = [k for k, v in lines.items() if PARSER not in v]
    r.append(say(bool(lines) and not old, "E2 every name reads %s (not yet re-cut: %s)" % (PARSER, sorted(old))))
    r.append(say("business: OWN-HEADING" in lines.get("ASML_NA_Equity", ""), "E3 ASML_NA_Equity's business item is cut from its own heading"))
    fb = [k for k, v in lines.items() if "risk: FALLBACK" in v]
    r.append(say(bool(lines) and not fb, "E4 no stored risk item comes from the fallback heading (still: %s)" % sorted(fb)))
    ok = all(r)
    print("R81 EE4 CENSUS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
