"""Round 24 AC2 (IB-pr-241) -- the ingest mirror's stale DOOR 5 paragraph is corrected (1.0.0_SA_CTO 102969: the July
hold is no longer in force; raw restarted 5fdbe38637, INF-REDEPLOY closed 69a15bf90e).

Usage: python p24_1_ac2_mirror_door5_comment.py <worktree root>
Pass: infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py no longer carries the sentence
"It is NOT ruled, NOT recommended, NOT yours", cites both 5fdbe38637 and 69a15bf90e, and still compiles; Ruling 16
(COERCED_SUFFIXES) is unchanged.
"""
import py_compile
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
p = root / "infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py"
t = p.read_text(encoding="utf-8")
stale = "It is NOT ruled, NOT recommended, NOT yours" in t
cites = "5fdbe38637" in t and "69a15bf90e" in t
m = re.search(r"COERCED_SUFFIXES\s*=\s*\(([^)]*)\)", t)
ruling16 = bool(m) and m.group(1).strip().rstrip(",") == '".parquet"'
try:
    py_compile.compile(str(p), doraise=True)
    compiles = True
except py_compile.PyCompileError:
    compiles = False
print("stale DOOR 5 sentence present: %s | cites 5fdbe38637 + 69a15bf90e: %s | Ruling 16 unchanged: %s | compiles: %s"
      % (stale, cites, ruling16, compiles))
ok = not stale and cites and ruling16 and compiles
print("P24-1-AC2 PASS" if ok else "P24-1-AC2 FAIL")
sys.exit(0 if ok else 1)
