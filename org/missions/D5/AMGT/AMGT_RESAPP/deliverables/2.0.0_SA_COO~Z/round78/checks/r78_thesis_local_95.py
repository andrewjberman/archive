"""AMGT_RESAPP round 78 -- a pre-deploy read for bb-18: every covered name's /thesis through the handler IN-PROCESS on the tree.

  python r78_thesis_local_95.py

The two bounds of the deployed list (r78_bb5, r78_bb6) read the deployed function only. This is the same breadth on the tree's
code, run before the deploy: every covered name's /thesis answers 200, and the dossier each one serves states its method
version. Read-only: store reads, no write. Exit 0 when every read answers 200.
"""
from __future__ import annotations

import collections
import json
import subprocess
import sys


def main():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    sys.path.insert(0, root)
    from lib.research.api import scoped_amgt
    from lib.research.corpus import dossier
    from lib.research.coverage.covered_universe import covered_security_keys

    covered = sorted(covered_security_keys())
    status = collections.Counter()
    failed = []
    for key in covered:
        event = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}},
                 "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
        try:
            r = scoped_amgt.handler(event)
            code = r.get("statusCode")
            json.loads(r.get("body") or "{}")
        except Exception as exc:  # noqa: BLE001 -- a raised read is the finding this script exists to print
            code = "RAISED %s" % type(exc).__name__
        status[code] += 1
        if code != 200:
            failed.append((key, code))
    print("tree HEAD %s; dossier reader METHOD_VERSION %s" % (
        subprocess.run(["git", "rev-parse", "--short=10", "HEAD"], capture_output=True, text=True).stdout.strip(),
        dossier.METHOD_VERSION))
    print("covered names %d; /thesis status counts %s" % (len(covered), dict(status)))
    print("not 200: %d %s" % (len(failed), failed[:6]))
    ok = bool(covered) and not failed
    print("R78 THESIS LOCAL 95: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
