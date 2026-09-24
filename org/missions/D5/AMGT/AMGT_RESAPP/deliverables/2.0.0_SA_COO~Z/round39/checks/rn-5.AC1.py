"""AMGT_RESAPP round 39, AMGT-rn-5 AC1 -- the SERVED fixture exists: the deployed function's own responses for
BA_US_Equity, captured by the cell's script into a tabsFixture-shaped JSON, carrying the SAME top-level keys as the
landed fixture plus a `_served` provenance block (function name, CodeSha256, invoke timestamps, route paths).
usage (from the repo root): python <this> <path to served fixture JSON>"""
from __future__ import annotations

import json
import sys

served_path = sys.argv[1] if len(sys.argv) > 1 else ""
landed = json.load(open("portal/src/pages/SecurityAnalysis/__harness__/tabsFixture.BA_US_Equity.json", encoding="utf-8"))
try:
    served = json.load(open(served_path, encoding="utf-8"))
except (OSError, ValueError) as exc:
    print("served fixture unreadable at %r: %s" % (served_path, exc))
    sys.exit(1)
want = sorted(k for k in landed.keys() if not k.startswith("_"))
have = sorted(k for k in served.keys() if not k.startswith("_"))
missing = [k for k in want if k not in have]
prov = served.get("_served") or {}
prov_ok = all(prov.get(k) for k in ("function", "code_sha256", "invoked_at", "routes"))
print("landed top-level keys: %d; served carries %d of them; missing: %s" % (len(want), len(want) - len(missing), missing or "none"))
print("_served provenance: function=%r code_sha256=%r invoked_at=%r routes=%d -> %s"
      % (prov.get("function"), prov.get("code_sha256"), prov.get("invoked_at"), len(prov.get("routes") or []), "OK" if prov_ok else "MISSING"))
sys.exit(0 if not missing and prov_ok else 1)
