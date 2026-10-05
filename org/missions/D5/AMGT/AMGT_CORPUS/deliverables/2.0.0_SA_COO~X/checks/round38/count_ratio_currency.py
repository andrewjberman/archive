"""AMGT_CORPUS round 38 -- count and ratio figures carry NO currency. Issuer's file. Read-only (puts captured in --derive mode).

  python count_ratio_currency.py --served            census over every registered name's newest SERVED block
  python count_ratio_currency.py --derive K1,K2,...  re-derive those names IN MEMORY through the REAL stage_derive on each served
                                                    block's own raw stamp (sa_fallback=False; every put captured, never sent),
                                                    and compare with the served block
A COUNT-OR-RATIO figure has a unit containing "(share count)", or beginning RATIO or PERCENT. A MONEY figure has a unit beginning
MILLIONS / ABSOLUTE / PER SHARE and no "(share count)".
Prints, then the verdict line:
  count_ratio <n> with_currency <c>      (round-38 target: c == 0)
  money <m> unlabelled <u>               (round 37's result must hold: u == 0)
  --derive also: values_moved <v> money_labels_changed <l>   (both must be 0)
  --served:  `crc served build <0|1>/1 control <0|1>/1`
  --derive:  `crc derive build <0|1>/1 control <0..2>/2`
"""
import argparse
import collections
import importlib.util
import os
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
for p in (TOP, RES):
    if p not in sys.path:
        sys.path.insert(0, p)
spec = importlib.util.spec_from_file_location("mbp_crc", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)
from lib.research.api import scoped_amgt  # noqa: E402


def is_count_ratio(unit):
    u = str(unit or "")
    return "(share count)" in u or u.startswith("RATIO") or u.startswith("PERCENT")


def is_money(unit):
    u = str(unit or "")
    return "(share count)" not in u and (u.startswith("MILLIONS") or u.startswith("ABSOLUTE") or u.startswith("PER SHARE"))


def has_ccy(f):
    return isinstance(f.get("currency"), str) and bool(f.get("currency").strip())


def unlabelled(f):
    basis = str(f.get("currency_basis") or "")
    return not has_ccy(f) and not (basis.startswith("UNMEASURED") or basis.startswith("UNSTATED"))


def key_of(f):
    return (f.get("scope"), str(f.get("fiscal_year")), str(f.get("fiscal_period") or f.get("period")), f.get("mnemonic"))


class CapturingS3:
    def __init__(self, real):
        self._real = real
        self.captured = 0

    def put_object(self, **kwargs):
        self.captured += 1
        return {"ETag": '"captured-not-sent"'}

    def __getattr__(self, name):
        return getattr(self._real, name)


ap = argparse.ArgumentParser()
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--served", action="store_true")
g.add_argument("--derive", default="")
a = ap.parse_args()

tot = collections.Counter()
mn = collections.Counter()
if a.served:
    for key in mbp._registered_security_keys():
        b = scoped_amgt.read_model_block(key)
        if not b:
            continue
        tot["names"] += 1
        for f in b.get("figures", []):
            if is_count_ratio(f.get("unit")):
                tot["count_ratio"] += 1
                if has_ccy(f):
                    tot["with_currency"] += 1
                    mn[f.get("mnemonic")] += 1
            elif is_money(f.get("unit")):
                tot["money"] += 1
                tot["unlabelled"] += unlabelled(f)
    print("served names %d count_ratio %d with_currency %d %s" % (tot["names"], tot["count_ratio"], tot["with_currency"],
                                                                   mn.most_common(4)))
    print("served money %d unlabelled %d" % (tot["money"], tot["unlabelled"]))
    print("crc served build %d/1 control %d/1" % (int(tot["with_currency"] == 0), int(tot["unlabelled"] == 0)))
else:
    s3 = CapturingS3(mbp._s3())
    for key in [k for k in a.derive.split(",") if k]:
        served = scoped_amgt.read_model_block(key) or {}
        new = mbp.stage_derive(s3, key.replace("_", " "), raw_stamp=served.get("raw_stamp_used"), sa_fallback=False)["model_block"]
        sv = {key_of(f): f for f in served.get("figures", [])}
        for f in new.get("figures", []):
            if is_count_ratio(f.get("unit")):
                tot["count_ratio"] += 1
                if has_ccy(f):
                    tot["with_currency"] += 1
                    mn[f.get("mnemonic")] += 1
            elif is_money(f.get("unit")):
                tot["money"] += 1
                tot["unlabelled"] += unlabelled(f)
            old = sv.get(key_of(f))
            if old is not None:
                tot["values_moved"] += old.get("value") != f.get("value")
                if is_money(f.get("unit")) and has_ccy(old) and f.get("currency") != old.get("currency"):
                    tot["money_labels_changed"] += 1
    print("derive puts_captured %d (none sent)" % s3.captured)
    print("derive count_ratio %d with_currency %d %s" % (tot["count_ratio"], tot["with_currency"], mn.most_common(4)))
    print("derive money %d unlabelled %d values_moved %d money_labels_changed %d"
          % (tot["money"], tot["unlabelled"], tot["values_moved"], tot["money_labels_changed"]))
    c = int(tot["unlabelled"] == 0) + int(tot["values_moved"] == 0 and tot["money_labels_changed"] == 0)
    print("crc derive build %d/1 control %d/2" % (int(tot["with_currency"] == 0), c))
