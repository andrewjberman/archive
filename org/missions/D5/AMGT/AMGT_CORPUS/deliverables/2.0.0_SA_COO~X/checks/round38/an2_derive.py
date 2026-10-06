"""AMGT_CORPUS round 38 CRPS-an-2 leg Ld -- the SERVED re-derive of every registered name with a block (the paired act).

The REAL stage_derive(..., sa_fallback=False) on each name's newest raw. A name that fails keeps its prior block and is listed
(Branch B); the loop never stops on one name. Prints one DERIVE / FAIL line per name, then `LD derived <n> failed <f> of <N>`.
No Bloomberg call, no Seeking Alpha call: stage_derive reads bronze only, and sa_fallback=False holds the forecast fallback off.
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
spec = importlib.util.spec_from_file_location("mbp_an2", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)

s3 = mbp._s3()
present = mbp._model_block_keys_in_store(s3)
keys = [k for k in mbp._registered_security_keys() if k in present]
ok = 0
failed = []
for key in keys:
    try:
        r = mbp.stage_derive(s3, key.replace("_", " "), raw_stamp=None, sa_fallback=False)
        ok += 1
        print("DERIVE: %s -> raw %s derived %s" % (key, r["model_block"].get("raw_stamp_used"), r["derived_stamp"]), flush=True)
    except Exception as exc:  # Branch B: the name keeps its prior block
        failed.append(key)
        print("FAIL: %s -> %s: %s" % (key, type(exc).__name__, str(exc)[:200]), flush=True)
print("LD derived %d failed %d of %d %s" % (ok, len(failed), len(keys), failed))
