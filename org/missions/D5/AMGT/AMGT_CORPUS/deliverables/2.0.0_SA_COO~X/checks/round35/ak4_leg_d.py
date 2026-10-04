"""AMGT_CORPUS round 35, CRPS-ak-4 leg d -- one re-derive of every registered name that has a model block, on its newest
landed raw, under the map commit <m>. Reads landed raw only: no Bloomberg call, no Seeking Alpha call (sa_fallback=False).
The security string is the refresh's own (`key.replace("_", " ")`). Branch B: a name that fails is listed and the rest proceed.
The issuer's file.

Prints one DERIVE / DERIVE FAILED line per name, then:
  leg_d registered <N> with_block <K> derived <D> failed <F>
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
spec = importlib.util.spec_from_file_location("bum_ak4d", os.path.join(RES, "build_unit_map.py"))
bum = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bum)
mbp = bum._mbp

s3 = mbp._s3()
registered = mbp._registered_security_keys()
present = mbp._model_block_keys_in_store(s3)
with_block = [k for k in registered if k in present]
derived, failed = 0, []
for key in with_block:
    security = key.replace("_", " ")
    try:
        stamps = bum._stamps_with_refdata(s3, key)
        if not stamps:
            raise RuntimeError("no raw landed")
        d = mbp.stage_derive(s3, security, raw_stamp=stamps[0], sa_fallback=False)
        derived += 1
        print("DERIVE: %s -> raw %s derived %s" % (key, stamps[0], d["derived_stamp"]), flush=True)
    except Exception as exc:  # noqa: BLE001 -- Branch B: one name failing must not hide the others
        failed.append(key)
        print("DERIVE FAILED: %s: %s: %s" % (key, type(exc).__name__, exc), flush=True)
print("leg_d registered %d with_block %d derived %d failed %d %s"
      % (len(registered), len(with_block), derived, len(failed), failed))
