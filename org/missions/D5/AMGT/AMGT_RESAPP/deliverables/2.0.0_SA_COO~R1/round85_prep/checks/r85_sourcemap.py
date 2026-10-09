"""AMGT_RESAPP round-85 PREP -- row AMGT_RESAPP-D1-S7: the deploy recorders stop writing lambda-source-map.json's top-level
`_last_deploy_recorded`, which is derived on read instead (CTO~DELL1 msgs 2169, 2197; laptop CTO msg 107888).

  python r85_sourcemap.py --crit AC1

    M1 none of the three recorders writes the SOURCE MAP's top-level key: no line in infra/aws/lambda/ci/record-terraform-deploy.sh,
       record-resource-deploy.sh or record-deploy-scope.py assigns `sm...._last_deploy_recorded` (lines printed). The shared-infra
       resource map's own key (`rm[...]` in record-resource-deploy.sh) is out of scope;
    M2 infra/aws/lambda/ci/lambda-source-map.json carries no top-level `_last_deploy_recorded`;
    M3 (negative arm) the derived value still reads: the newest `functions[*].last_deployed_at` is printed with the count of entries
       that carry one, and at least one does.
Verdict: R85 SOURCEMAP AC1: YES|NO (exit 0|1). At the base (2026-10-09): NO -- three source-map assignment lines in two recorders; the key is
present ("2026-10-09T10:16:39Z"); M3 PASS (183 of 235 entries, newest 2026-10-09T11:12:54Z).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

CI = "infra/aws/lambda/ci"
RECORDERS = ("record-terraform-deploy.sh", "record-resource-deploy.sh", "record-deploy-scope.py")
KEY = "_last_deploy_recorded"
SM_RE = re.compile(r"\bsm\b")  # the lambda source map only; rm (shared-infra-resource-map) is out of scope
ASSIGN_RE = re.compile(r"""[\[.]\s*['"]?%s['"]?\s*\]?\s*=(?!=)""" % KEY)


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or "."
    hits = []
    for name in RECORDERS:
        path = os.path.join(root, CI, name)
        for n, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
            if ASSIGN_RE.search(line) and SM_RE.search(line) and not line.lstrip().startswith("#"):
                hits.append("%s:%d: %s" % (name, n, line.strip()[:100]))
    for h in hits:
        print("   assigns: %s" % h)
    m1 = say(not hits, "M1 no recorder assigns the top-level %s: %d assignment line(s) in %d recorders" % (KEY, len(hits), len(RECORDERS)))
    sm = json.load(open(os.path.join(root, CI, "lambda-source-map.json"), encoding="utf-8"))
    m2 = say(KEY not in sm, "M2 lambda-source-map.json carries no top-level %s (read %r)" % (KEY, sm.get(KEY)))
    funcs = sm.get("functions") or {}
    stamps = [v.get("last_deployed_at") for v in funcs.values() if isinstance(v, dict) and v.get("last_deployed_at")]
    m3 = say(bool(stamps), "M3 the derived last deploy reads: %d of %d entries carry last_deployed_at, newest %s" % (
        len(stamps), len(funcs), max(stamps) if stamps else None))
    ok = m1 and m2 and m3
    print("R85 SOURCEMAP AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
