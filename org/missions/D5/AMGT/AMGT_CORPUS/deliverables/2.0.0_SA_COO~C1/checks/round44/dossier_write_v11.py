"""AMGT_CORPUS round 44, CRPS-at-10 legs 0 and w -- the /11 dossier write. Issuer's file (2.0.0_SA_COO~C1).

Leg 0 (CTO half condition, msg 3401): BEFORE the first write, per name, print whether a /10 object exists, with the count over the
denominator. A name without one is listed and LEFT OUT of leg w (it is written only with leg p), because the pick rule falls back to
ALL objects when none is at the reader's method and the deployed /10 API would serve its /11 object at once.
Leg w: dossier.write_one per name in 6 threads of ONE process, the REAL fitz asserted first (a stub aborts).

  PYTHONPATH=. python dossier_write_v11.py            leg 0 then leg w
  PYTHONPATH=. python dossier_write_v11.py --leg0     leg 0 only (read-only)
"""
import sys
from concurrent.futures import ThreadPoolExecutor

import fitz

if not (hasattr(fitz, "open") and hasattr(fitz, "Document")) or type(fitz).__name__ != "module" or not getattr(fitz, "__file__", None):
    print("ABORT: fitz is not the real library", flush=True)
    sys.exit(2)
print("fitz real version %s file %s" % (getattr(fitz, "VersionBind", None), fitz.__file__), flush=True)

from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

METHOD = "amgt-corpus-dossier/11"
PRIOR = "amgt-corpus-dossier/10"
print("method %s" % dossier.METHOD_VERSION, flush=True)
if dossier.METHOD_VERSION != METHOD:
    print("ABORT: method is not /11", flush=True)
    sys.exit(2)

client = store._default_client()
keys = sorted(dossier._resolved_security_keys(client=client), reverse=True)


def _has_prior(key):
    """True when the name holds at least one stored object whose method_version is /10 (read at the reader's own /10)."""
    current = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = PRIOR
    try:
        return dossier.read_dossier(key, client=client)["document"].get("method_version") == PRIOR
    except LookupError:
        return False
    finally:
        dossier.METHOD_VERSION = current


has, lacks = [], []
for k in keys:
    ok = _has_prior(k)
    print("LEG0 %s has_/10 %d" % (k, int(ok)), flush=True)
    (has if ok else lacks).append(k)
print("LEG0 names_with_a_/10_object %d of %d" % (len(has), len(keys)), flush=True)
for k in lacks:
    print("LEG0 LEFT-OUT (no /10 object; written only with leg p) %s" % k, flush=True)
if "--leg0" in sys.argv:
    sys.exit(0)


def one(k):
    try:
        r = dossier.write_one(k, client=client)
        return "OK %s wrote %d uri %s" % (k, int(r["wrote"]), r["uri"])
    except Exception as exc:  # a failed write is listed, never swallowed (Branch B)
        return "FAIL %s %s: %s" % (k, type(exc).__name__, str(exc)[:200])


wrote = failed = 0
with ThreadPoolExecutor(max_workers=6) as pool:
    for line in pool.map(one, has):
        print(line, flush=True)
        if line.startswith("OK ") and " wrote 1 " in line:
            wrote += 1
        elif line.startswith("FAIL "):
            failed += 1
print("threads done names %d wrote %d failed %d left_out %d" % (len(has), wrote, failed, len(lacks)), flush=True)
