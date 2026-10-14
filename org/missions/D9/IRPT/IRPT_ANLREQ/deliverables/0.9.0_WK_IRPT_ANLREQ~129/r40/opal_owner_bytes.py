"""Byte evidence for the OPAL_GLOBAL owner (cell AR-y-319, opal_global_unchanged).

Usage: python opal_owner_bytes.py <repo-root>
Imports _scope/interactive_access.py from the given tree (own process per tree), builds the prospect owner of the
offline OPAL_GLOBAL actor, and prints the canonical JSON bytes (length and sha256). Run once on the HEAD archive and
once on the worktree; equal lines mean the OPAL_GLOBAL owner is byte-identical.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

tree = Path(sys.argv[1]) / "infra" / "aws" / "lambda" / "investor-reporting"
for child in ("_scope", "_authz", "_keys", "_ids"):
    sys.path.insert(0, str(tree / child))
os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps({"49financial": "fixture-bd", "cottonwood": "fixture-cot"})
from interactive_access import InteractiveAccess  # noqa: E402

headers = {"x-origin-verify": "cloudfront", "x-user-email": "opal.staff@example.invalid",
           "x-firm-id": "opal-capital", "x-user-role": "admin"}
owner = InteractiveAccess(lambda: headers, "49financial", ordinary_authorizer=lambda *a: True).prospect_owner("49financial")
data = json.dumps(owner, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
print("OPAL-OWNER-BYTES len=%d sha256=%s" % (len(data), hashlib.sha256(data).hexdigest()))
print(data.decode("ascii"))
