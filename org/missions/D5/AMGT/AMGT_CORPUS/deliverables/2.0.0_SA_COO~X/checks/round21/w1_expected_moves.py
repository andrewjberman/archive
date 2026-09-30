"""AMGT_CORPUS round 21 -- what a dossier rewrite would MOVE, read per name from the producer's own path: the served document
(`read_dossier`) against the document `build()` makes now. Read-only (S3 reads; `build()` writes nothing). The issuer's file.

  -> per name with any change: 'MOVE <key> fields <comma list>'
  -> 'w1 expected names N built B errors E pack_shape_only P other_moves O pack_shape pdf a docx b mixed c none d'
"""
import concurrent.futures
import json
import sys

from lib.research.corpus import dossier
from lib.research.harvest import store


def one(key):
    client = store._default_client()
    stored = dossier.read_dossier(key, client=client)["document"]["fields"]
    fresh = dossier.build(key, client=client)["fields"]
    moved = sorted(f for f in set(stored) | set(fresh) if f != "pack_shape" and
                   json.dumps(stored.get(f), sort_keys=True, default=str) != json.dumps(fresh.get(f), sort_keys=True, default=str))
    return key, moved, (fresh.get("pack_shape") or {}).get("value")


keys = dossier._resolved_security_keys()
shape = {"pdf": 0, "docx": 0, "mixed": 0, "none": 0}
built = errors = only = other = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    futs = {pool.submit(one, k): k for k in keys}
    for fut in concurrent.futures.as_completed(futs):
        try:
            key, moved, ps = fut.result()
        except Exception as exc:  # noqa: BLE001 -- counted, never hidden
            errors += 1
            print("ERR %s %s: %s" % (futs[fut], type(exc).__name__, str(exc)[:120]), file=sys.stderr)
            continue
        built += 1
        shape["none" if ps is None else ps] = shape.get("none" if ps is None else ps, 0) + 1
        if moved:
            other += 1
            print("MOVE %s fields %s" % (key, ",".join(moved)))
        else:
            only += 1
print("w1 expected names %d built %d errors %d pack_shape_only %d other_moves %d pack_shape pdf %d docx %d mixed %d none %d" % (
    len(keys), built, errors, only, other, shape["pdf"], shape["docx"], shape["mixed"], shape["none"]))
