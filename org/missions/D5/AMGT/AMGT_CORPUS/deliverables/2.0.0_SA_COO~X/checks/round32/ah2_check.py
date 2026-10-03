"""AMGT_CORPUS round 32, CRPS-ah-2 (row Z-S76's enrichment item; round-31 analysis s.3) -- a BEST_DIV_YLD value under the
percent family's 0.3 magnitude line is decided by the same-name identity BEST_DIV_YLD = BEST_DPS / PX_LAST x 100 (PERCENT) or
BEST_DPS / PX_LAST (DECIMAL), on a same-currency read within RECONCILE_TOLERANCE; magnitude alone no longer labels it DECIMAL.
Offline (no network). The issuer's file.

  BUILD arms (FAIL at the base, PASS after): b1 BA's served 1FY yield reads PERCENT; b2 no BEST_DPS -> UNRESOLVED;
    b3 a currency mismatch -> UNRESOLVED; b4 an identity that reconciles neither way -> UNRESOLVED.
  CONTROL arms (PASS at the base and after): c1 a true decimal (DPS / PX) reads DECIMAL; c2 a yield >= 0.3 reads PERCENT with no
    header; c3 EQY_DVD_YLD_IND 0.25 still reads DECIMAL (no other mnemonic moves); c4 an exact zero is not decided here.
  -> one 'ARM <id> PASS|FAIL <got>' line per arm, then 'ah2 build <p>/4 control <q>/4'
"""
import importlib.util
import os
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
for p in (TOP, RES):
    if p not in sys.path:
        sys.path.insert(0, p)
spec = importlib.util.spec_from_file_location("bum", os.path.join(RES, "build_unit_map.py"))
bum = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bum)

DEC = "DECIMAL (differs from CRO's PERCENT reading on SAP)"
BA = {"PX_LAST": 196.8, "BEST_DPS": 0.005, "CRNCY": "USD", "EQY_FUND_CRNCY": "USD"}
BA_YLD = 0.002540650406504065  # BA's served 1FY BEST_DIV_YLD (block 20261001T070950Z) = 0.005 / 196.8 x 100


def label(mnemonic, value, header):
    return bum.classify_unit(mnemonic, value, "BA US Equity", header)[0]


def status(mnemonic, value, header):
    return bum.classify_unit(mnemonic, value, "BA US Equity", header)[1]


ARMS = [
    ("b1", "build", lambda: label("BEST_DIV_YLD", BA_YLD, BA), "PERCENT"),
    ("b2", "build", lambda: status("BEST_DIV_YLD", BA_YLD, {k: v for k, v in BA.items() if k != "BEST_DPS"}), "UNRESOLVED"),
    ("b3", "build", lambda: status("BEST_DIV_YLD", BA_YLD, dict(BA, EQY_FUND_CRNCY="EUR")), "UNRESOLVED"),
    ("b4", "build", lambda: status("BEST_DIV_YLD", 0.2, BA), "UNRESOLVED"),
    ("c1", "control", lambda: label("BEST_DIV_YLD", 0.005 / 196.8, BA), DEC),
    ("c2", "control", lambda: label("BEST_DIV_YLD", 2.5, None), "PERCENT"),
    ("c3", "control", lambda: label("EQY_DVD_YLD_IND", 0.25, BA), DEC),
    ("c4", "control", lambda: status("BEST_DIV_YLD", 0.0, BA), "UNRESOLVED"),
]

score = {"build": 0, "control": 0}
for aid, kind, fn, want in ARMS:
    try:
        got = fn()
    except Exception as e:  # an arm that raises is a FAIL with its cause printed
        got = "RAISED %s: %s" % (type(e).__name__, e)
    ok = got == want
    score[kind] += ok
    print("ARM %s %s %r" % (aid, "PASS" if ok else "FAIL", got))
print("ah2 build %d/4 control %d/4" % (score["build"], score["control"]))
