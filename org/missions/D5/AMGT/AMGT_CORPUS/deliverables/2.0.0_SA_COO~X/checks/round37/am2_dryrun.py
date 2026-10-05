"""AMGT_CORPUS round 37, CRPS-am-2 -- the serializing dry run of the served act: one re-derive of every registered name with a
block, IN MEMORY, through the REAL `stage_derive` (sa_fallback=False) on each served newest block's own raw stamp. The S3 client is
wrapped: reads go through, every put_object is CAPTURED and never sent. Issuer's file.
Prints:
  dryrun names <n> derived <d> failed <f> puts_captured <p>
  dryrun money <m> labelled_before <lb> labelled_after <la> null_reasoned_after <r> null_unlabelled_before <ub> after <ua>
  dryrun values_moved <v> labels_changed <c> (both expected 0)
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
spec = importlib.util.spec_from_file_location("mbp_am2", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)
from lib.research.api import scoped_amgt  # noqa: E402


class CapturingS3:
    def __init__(self, real):
        self._real = real
        self.captured = 0

    def put_object(self, **kwargs):
        self.captured += 1
        return {"ETag": '"captured-not-sent"'}

    def __getattr__(self, name):
        return getattr(self._real, name)


def is_money(unit):
    u = str(unit or "")
    if "(share count)" in u:
        return False
    return u.startswith("MILLIONS") or u.startswith("ABSOLUTE") or u.startswith("PER SHARE")


def state(fig):
    cur = fig.get("currency")
    basis = str(fig.get("currency_basis") or "")
    if isinstance(cur, str) and cur.strip():
        return "labelled"
    if basis.startswith("UNMEASURED") or basis.startswith("UNSTATED"):
        return "reasoned"
    return "unlabelled"


def key_of(f):
    return (f.get("scope"), str(f.get("fiscal_year")), str(f.get("fiscal_period") or f.get("period")), f.get("mnemonic"))


s3 = CapturingS3(mbp._s3())
registered = mbp._registered_security_keys()
present = mbp._model_block_keys_in_store(mbp._s3())
keys = [k for k in registered if k in present]
derived = failed = money = lb = la = ra = ub = ua = moved = relabelled = 0
fails = []
for key in keys:
    served = scoped_amgt.read_model_block(key) or {}
    try:
        r = mbp.stage_derive(s3, key.replace("_", " "), raw_stamp=served.get("raw_stamp_used"), sa_fallback=False)
    except Exception as exc:  # noqa: BLE001 -- Branch B: list, keep going
        failed += 1
        fails.append("%s: %s" % (key, type(exc).__name__))
        continue
    derived += 1
    new = r["model_block"]
    sv = {key_of(f): f for f in served.get("figures", [])}
    for f in served.get("figures", []):
        if is_money(f.get("unit")):
            st = state(f)
            lb += st == "labelled"
            ub += st == "unlabelled"
    for f in new.get("figures", []):
        if is_money(f.get("unit")):
            money += 1
            st = state(f)
            la += st == "labelled"
            ra += st == "reasoned"
            ua += st == "unlabelled"
        old = sv.get(key_of(f))
        if old is not None:
            if old.get("value") != f.get("value"):
                moved += 1
            oc = old.get("currency")
            if isinstance(oc, str) and oc.strip() and f.get("currency") != oc:
                relabelled += 1
print("dryrun names %d derived %d failed %d puts_captured %d %s" % (len(keys), derived, failed, s3.captured, fails[:4]))
print("dryrun money %d labelled_before %d labelled_after %d null_reasoned_after %d null_unlabelled_before %d after %d"
      % (money, lb, la, ra, ub, ua))
print("dryrun values_moved %d labels_changed %d" % (moved, relabelled))
