"""AMGT_CORPUS round 33, CRPS-ai-1 (row Z-S81, round-32 analysis ruling 1) -- a percent-family value under the 0.3 magnitude
line is decided by a GROUND, never by magnitude: EQY_DVD_YLD_IND by its own fiscal rows' identity EQY_DPS / PX_LAST (x 100 ->
PERCENT, x 1 -> DECIMAL) on a same-currency read; any other percent field under the line with no ground -> UNRESOLVED (not DECIMAL).
BEST_DIV_YLD keeps ah-2's identity. Offline (no network). The issuer's file.

  BUILD arms (FAIL at the base, PASS after): b1 HEI-shaped rows (yield = DPS / PX x 100) read PERCENT; b2 SI_PERCENT_EQUITY_FLOAT
    0.0101 with no ground reads UNRESOLVED; b3 EQY_DVD_YLD_IND rows with no EQY_DPS read UNRESOLVED; b4 a currency mismatch reads
    UNRESOLVED.
  CONTROL arms (PASS at the base and after): c1 a percent field >= 0.3 reads PERCENT; c2 BEST_DIV_YLD's ah-2 identity still reads
    PERCENT; c3 a series median >= 0.3 (ORA ROIC 4.47) reads PERCENT; c4 an exact zero is not decided here.
  -> one 'ARM <id> PASS|FAIL <got>' line per arm, then 'ai1 build <p>/4 control <q>/4'
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

USD = {"PX_LAST": 306.33, "CRNCY": "USD", "EQY_FUND_CRNCY": "USD"}
# HEI-shaped fiscal rows: the yield is EQY_DPS / PX_LAST x 100 in every row (a 0.08% .. 0.23% yield).
ROWS = [{"date": "2025-10-31", "EQY_DPS": 0.24, "PX_LAST": 290.0, "EQY_DVD_YLD_IND": 0.24 / 290.0 * 100},
        {"date": "2024-10-31", "EQY_DPS": 0.22, "PX_LAST": 240.0, "EQY_DVD_YLD_IND": 0.22 / 240.0 * 100},
        {"date": "2023-10-31", "EQY_DPS": 0.20, "PX_LAST": 150.0, "EQY_DVD_YLD_IND": 0.20 / 150.0 * 100}]
NO_DPS = [{k: v for k, v in r.items() if k != "EQY_DPS"} for r in ROWS]
MED = sorted(abs(r["EQY_DVD_YLD_IND"]) for r in ROWS)[1]


def call(mnemonic, value, header, rows=None):
    if rows is None:
        return bum.classify_unit(mnemonic, value, "HEI US Equity", header)
    return bum.classify_unit(mnemonic, value, "HEI US Equity", header, hist_rows=rows)


ARMS = [
    ("b1", "build", lambda: call("EQY_DVD_YLD_IND", MED, USD, ROWS)[0], "PERCENT"),
    ("b2", "build", lambda: call("SI_PERCENT_EQUITY_FLOAT", 0.01013934, USD)[1], "UNRESOLVED"),
    ("b3", "build", lambda: call("EQY_DVD_YLD_IND", MED, USD, NO_DPS)[1], "UNRESOLVED"),
    ("b4", "build", lambda: call("EQY_DVD_YLD_IND", MED, dict(USD, EQY_FUND_CRNCY="EUR"), ROWS)[1], "UNRESOLVED"),
    ("c1", "control", lambda: call("OPER_MARGIN", 12.5, USD)[0], "PERCENT"),
    ("c2", "control", lambda: call("BEST_DIV_YLD", 0.002540650406504065,
                                   {"PX_LAST": 196.8, "BEST_DPS": 0.005, "CRNCY": "USD", "EQY_FUND_CRNCY": "USD"})[0], "PERCENT"),
    ("c3", "control", lambda: call("RETURN_ON_INV_CAPITAL", 4.46565, {"PX_LAST": 14.0, "CRNCY": "EUR",
                                                                       "EQY_FUND_CRNCY": "EUR"})[0], "PERCENT"),
    ("c4", "control", lambda: call("EQY_DVD_YLD_IND", 0.0, USD)[1], "UNRESOLVED"),
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
print("ai1 build %d/4 control %d/4" % (score["build"], score["control"]))
