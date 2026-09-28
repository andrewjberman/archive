"""IB-pr-191 AC3 -- the boundary names EngineReturnImplausible DEPENDENCY_UNAVAILABLE, not the MRO's OBJECT_NOT_COVERED.

Usage: python p19_1_ac3_boundary_code.py <worktree root>
Reads performance/entry.py's reasons table (build_entry) as text: an engine answer our checks refuse is a
dependency the caller does not control (the InflectionPerformanceRefused precedent), never "this account is not
covered". Control: the existing EnginePerformanceRefused -> OBJECT_NOT_COVERED line is unchanged.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
text = (root / "infra/aws/lambda/investor-reporting/performance/entry.py").read_text(encoding="utf-8")
ok = True
if re.search(r'"EngineReturnImplausible"\s*:\s*"DEPENDENCY_UNAVAILABLE"', text):
    print("PASS A: EngineReturnImplausible -> DEPENDENCY_UNAVAILABLE")
else:
    print("FAIL A: no EngineReturnImplausible -> DEPENDENCY_UNAVAILABLE line in the reasons table")
    ok = False
if re.search(r'"EnginePerformanceRefused"\s*:\s*"OBJECT_NOT_COVERED"', text):
    print("PASS B: EnginePerformanceRefused -> OBJECT_NOT_COVERED unchanged")
else:
    print("FAIL B: the EnginePerformanceRefused line changed")
    ok = False
if ok:
    print("P19-1-AC3 PASS")
else:
    print("P19-1-AC3 FAIL")
sys.exit(0 if ok else 1)
