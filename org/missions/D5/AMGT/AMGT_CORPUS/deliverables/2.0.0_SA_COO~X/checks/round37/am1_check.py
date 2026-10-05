"""AMGT_CORPUS round 37, CRPS-am-1 -- every money figure the producer derives carries its currency. Issuer's file.

For TSM_US_Equity (quote USD, reporting TWD), 1299_HK_Equity (quote HKD, reporting USD), SAP_GY_Equity (EUR) and BA_US_Equity
(USD), it re-derives each block IN MEMORY through the REAL `stage_derive` on the raw stamp the served newest block used, with
`sa_fallback=False`. The S3 client is wrapped: reads go through, and every put_object is CAPTURED and never sent, so nothing is
written. A MONEY figure has a unit beginning MILLIONS, ABSOLUTE or PER SHARE (but not a "(share count)" unit; amended 2026-10-05, row Z-W1-S33).
Prints one line per arm, then `am1 build <p>/1 control <q>/2`.
  b1  over the 4 derived blocks, money figures with currency null AND a basis that does not begin UNMEASURED/UNSTATED read 0
      (the before-count on the served blocks is printed beside it).
  c1  no figure VALUE moved against the served newest block (same raw, same keys: scope, fiscal_year, period, mnemonic).
  c2  no figure that carried a currency on the served block now carries a different one (the 8,578 already labelled hold).
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
spec = importlib.util.spec_from_file_location("mbp_am1", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)
from lib.research.api import scoped_amgt  # noqa: E402

KEYS = ("TSM_US_Equity", "1299_HK_Equity", "SAP_GY_Equity", "BA_US_Equity")


class CapturingS3:
    def __init__(self, real):
        self._real = real
        self.captured = []

    def put_object(self, **kwargs):
        self.captured.append(kwargs.get("Key"))
        return {"ETag": '"captured-not-sent"'}

    def __getattr__(self, name):
        return getattr(self._real, name)


def is_money(unit):
    u = str(unit or "")
    if "(share count)" in u:
        return False
    return u.startswith("MILLIONS") or u.startswith("ABSOLUTE") or u.startswith("PER SHARE")


def unlabelled(fig):
    cur = fig.get("currency")
    basis = str(fig.get("currency_basis") or "")
    return not (isinstance(cur, str) and cur.strip()) and not (basis.startswith("UNMEASURED") or basis.startswith("UNSTATED"))


def key_of(f):
    return (f.get("scope"), str(f.get("fiscal_year")), str(f.get("fiscal_period") or f.get("period")), f.get("mnemonic"))


s3 = CapturingS3(mbp._s3())
before_u = after_u = 0
moved_values, moved_ccy = [], []
notes = []
for key in KEYS:
    served = scoped_amgt.read_model_block(key) or {}
    stamp = served.get("raw_stamp_used")
    r = mbp.stage_derive(s3, key.replace("_", " "), raw_stamp=stamp, sa_fallback=False)
    derived = r["model_block"]
    b = sum(1 for f in served.get("figures", []) if is_money(f.get("unit")) and unlabelled(f))
    a = sum(1 for f in derived.get("figures", []) if is_money(f.get("unit")) and unlabelled(f))
    before_u += b
    after_u += a
    sv = {key_of(f): f for f in served.get("figures", [])}
    for f in derived.get("figures", []):
        old = sv.get(key_of(f))
        if old is None:
            continue
        if old.get("value") != f.get("value"):
            moved_values.append((key, key_of(f)[3], key_of(f)[1]))
        oc = old.get("currency")
        if isinstance(oc, str) and oc.strip() and f.get("currency") != oc:
            moved_ccy.append((key, key_of(f)[3], oc, f.get("currency")))
    notes.append("%s raw %s unlabelled money before %d after %d" % (key, stamp, b, a))

print("CAPTURED puts (never sent): %d" % len(s3.captured))
b1 = after_u == 0
c1 = not moved_values
c2 = not moved_ccy
print("ARM b1 %s unlabelled money figures before %d after %d %s" % ("PASS" if b1 else "FAIL", before_u, after_u, notes))
print("ARM c1 %s values moved %d %s" % ("PASS" if c1 else "FAIL", len(moved_values), moved_values[:4]))
print("ARM c2 %s labelled currencies changed %d %s" % ("PASS" if c2 else "FAIL", len(moved_ccy), moved_ccy[:4]))
print("am1 build %d/1 control %d/2" % (int(b1), int(c1) + int(c2)))
