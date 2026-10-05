"""AMGT_CORPUS round 37 -- the money-currency census over the served newest model blocks. Issuer's file. Read-only.

  python money_currency_census.py [--keys K1,K2,...] [--cutoff <stamp prefix>]
A MONEY figure is one whose served `unit` begins MILLIONS, ABSOLUTE, or PER SHARE
(but not a "(share count)" unit; amended 2026-10-05, row Z-W1-S33).
Over every scope (header, fiscal_year_line_item, forecast) of each name's newest block (or, with --cutoff, only names whose
newest block stamp >= cutoff), it counts:
  money            money figures
  labelled         currency is a non-empty string
  null_reasoned    currency null and currency_basis begins UNMEASURED or UNSTATED (a held-out figure that names why)
  null_unlabelled  currency null and any other basis (e.g. "invariant") -- the defect row Z-W2-S20 names
Prints one line per name with null_unlabelled > 0 (first 40), the TSM line always, then
  CENSUS names <n> money <m> labelled <l> null_reasoned <r> null_unlabelled <u>
"""
import argparse
import collections
import json
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, TOP)
from lib.research.api import scoped_amgt  # noqa: E402


def is_money(unit):
    u = str(unit or "")
    if "(share count)" in u:
        return False
    return u.startswith("MILLIONS") or u.startswith("ABSOLUTE") or u.startswith("PER SHARE")


ap = argparse.ArgumentParser()
ap.add_argument("--keys", default="")
ap.add_argument("--cutoff", default="")
a = ap.parse_args()

mbp = scoped_amgt  # the reader's own block access
if a.keys:
    keys = [k for k in a.keys.split(",") if k]
else:
    import importlib.util
    import os
    res = os.path.join(TOP, "integrations", "bloomberg", "research")
    sys.path.insert(0, res)
    spec = importlib.util.spec_from_file_location("mbp_census", os.path.join(res, "model_block_pull.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    keys = m._registered_security_keys()

tot = collections.Counter()
names = 0
for key in keys:
    block = scoped_amgt.read_model_block(key)
    if not block:
        continue
    if a.cutoff and str(block.get("derived_stamp") or block.get("generated_at") or "") < a.cutoff:
        pass
    names += 1
    c = collections.Counter()
    for f in block.get("figures", []):
        if not is_money(f.get("unit")):
            continue
        c["money"] += 1
        cur = f.get("currency")
        basis = str(f.get("currency_basis") or "")
        if isinstance(cur, str) and cur.strip():
            c["labelled"] += 1
        elif basis.startswith("UNMEASURED") or basis.startswith("UNSTATED"):
            c["null_reasoned"] += 1
        else:
            c["null_unlabelled"] += 1
    tot.update(c)
    if key == "TSM_US_Equity" or (c["null_unlabelled"] and names <= 40):
        print("  %s money %d labelled %d null_reasoned %d null_unlabelled %d currencies %s"
              % (key, c["money"], c["labelled"], c["null_reasoned"], c["null_unlabelled"],
                 json.dumps(block.get("currencies"))))
print("CENSUS names %d money %d labelled %d null_reasoned %d null_unlabelled %d"
      % (names, tot["money"], tot["labelled"], tot["null_reasoned"], tot["null_unlabelled"]))
