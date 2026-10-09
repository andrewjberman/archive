"""GS-h-3 AC1 (row D1-W13-S1): safe-merge --continue also refuses a CLEAN path the merge brought in and the drain reset in both the
index and the working copy, while a CONFLICTED path resolved by keeping the first parent's bytes stays admitted.

Runs `.tools/tests/test_safe_merge_continue.py` (GS-f-6's test, extended by this cell) and reads its per-case lines.
Arm 1: the test's last line reads ok=True and at least 16 cases.
Arm 2: a PASS case line names `clean-path-reset-both-ways-refused`.
Arm 3 (the negative arm): a PASS case line names `conflicted-keep-ours-admitted`.
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "round1_prep", "checks"))
from r1_common import run, tail  # noqa: E402

rc, out = run([sys.executable, ".tools/tests/test_safe_merge_continue.py"], None, timeout=115)
m = re.findall(r"SM-CONTINUE ok=(\w+) cases=(\d+)/(\d+)", out)
last = m[-1] if m else None
green = bool(last) and last[0] == "True" and int(last[1]) == int(last[2]) and int(last[2]) >= 16
lines = out.splitlines()
reset = any("PASS" in ln and "clean-path-reset-both-ways-refused" in ln for ln in lines)
keep = any("PASS" in ln and "conflicted-keep-ours-admitted" in ln for ln in lines)
arms = [
    ("test-green-16-plus", green, "rc=%s last=%s :: %s" % (rc, last, tail(out, 1))),
    ("reset-both-ways-refused", reset, "case line present=%s" % reset),
    ("keep-ours-admitted", keep, "case line present=%s" % keep),
]
for name, ok, detail in arms:
    print("  %s %s: %s" % ("PASS" if ok else "FAIL", name, detail))
bad = sum(1 for a in arms if not a[1])
print("GS-H3-RESET ok=%s arms=%d failed=%d" % (bad == 0, len(arms), bad))
sys.exit(0 if bad == 0 else 1)
