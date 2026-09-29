"""Round 21 AC1 (IB-pr-212) -- every served copy of HoldingsSnapshot.schema.json is the additive CATEGORY revision at
a69fe8e33e (2.0.0_SA_COO~M 102599, step 1 of NEVER_WIDEN_HALF_REQUEST_HOLDINGS_L0_CATEGORIES_20260929.md).

Usage: python p21_2_ac1_holdings_contract_repin.py <worktree root>
Pass: (1) in infra/aws/lambda/ci/lambda-source-map.json, irpt-holdings and irpt-ycharts-generate stage
docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json at a pin whose blob equals a69fe8e33e's, with the
recorded sha256 equal to that blob's; (2) infra/aws/lambda/investor-reporting/_contracts/HoldingsSnapshot.schema.json
in the worktree is byte-equal to that blob; (3) the node_kind enum there contains CATEGORY and every member of the
previous enum (additive).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
DOC = "docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json"


def show(ref, path):
    return subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (ref, path)], capture_output=True, check=True).stdout


want = show("a69fe8e33e", DOC)
want_sha = hashlib.sha256(want).hexdigest()
m = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_text(encoding="utf-8"))
fns = m.get("functions", m)
ok = True
for fn in ("irpt-holdings", "irpt-ycharts-generate"):
    rows = [s for s in fns[fn].get("staged_from", []) if s.get("repo_path") == DOC]
    good = len(rows) == 1 and show(rows[0]["pin"], DOC) == want and rows[0].get("sha256") == want_sha
    print("%s: pin %s sha %s -> %s" % (fn, rows[0]["pin"][:10] if rows else None, rows[0].get("sha256", "")[:8] if rows else None, good))
    ok = ok and good
lam = (root / "infra/aws/lambda/investor-reporting/_contracts/HoldingsSnapshot.schema.json").read_bytes()
same = lam.replace(b"\r\n", b"\n") == want.replace(b"\r\n", b"\n")
print("_contracts copy byte-equal to a69fe8e33e (line endings normalised): %s" % same)


def kinds(b):
    found = []
    def walk(x):
        if isinstance(x, dict):
            if "node_kind" in x and isinstance(x["node_kind"], dict) and "enum" in x["node_kind"]:
                found.append(set(x["node_kind"]["enum"]))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(json.loads(b))
    return set().union(*found) if found else set()


old = kinds(show("a69fe8e33e~1", DOC))
new = kinds(lam)
additive = "CATEGORY" in new and old <= new
print("node_kind enum: CATEGORY present and every prior member kept: %s" % additive)
ok = ok and same and additive
print("P21-2-AC1 PASS" if ok else "P21-2-AC1 FAIL")
sys.exit(0 if ok else 1)
