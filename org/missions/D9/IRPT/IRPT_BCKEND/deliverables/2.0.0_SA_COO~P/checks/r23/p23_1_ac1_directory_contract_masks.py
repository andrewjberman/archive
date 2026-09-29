"""Round 23 AC1 (IB-pr-231) -- the lambda-tree contract copy carries AD-10's `account_masks`, byte-equal to the docs
copy 2.0.0_SA_COO~M committed @4ecbaca410 (blob 27d9a8f7; ~M 102775), and the change is additive.

Usage: python p23_1_ac1_directory_contract_masks.py <worktree root>
Pass: (1) infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json in the worktree has git blob
27d9a8f700889f2e234c267faf02d37f6d23d9a4 (line endings normalised to LF); (2) it defines `account_masks` and keeps
every top-level property the committed HEAD copy defines.
"""
import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
REL = "infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json"
WANT = "27d9a8f700889f2e234c267faf02d37f6d23d9a4"
body = (root / REL).read_bytes().replace(b"\r\n", b"\n")
blob = subprocess.run(["git", "-C", str(root), "hash-object", "--stdin"], input=body, capture_output=True, check=True).stdout.decode().strip()
print("worktree blob %s, want %s: %s" % (blob[:10], WANT[:10], blob == WANT))
head = json.loads(subprocess.run(["git", "-C", str(root), "show", "HEAD:" + REL], capture_output=True, check=True).stdout)
now = json.loads(body)
kept = set(head.get("properties", {})) <= set(now.get("properties", {}))
masks = "account_masks" in now.get("properties", {})
print("account_masks defined: %s | every HEAD property kept: %s" % (masks, kept))
ok = blob == WANT and masks and kept
print("P23-1-AC1 PASS" if ok else "P23-1-AC1 FAIL")
sys.exit(0 if ok else 1)
