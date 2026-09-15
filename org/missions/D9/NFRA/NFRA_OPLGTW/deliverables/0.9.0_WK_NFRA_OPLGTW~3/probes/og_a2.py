"""OG-a-2 probe (0.9.0_WK_NFRA_OPLGTW~3), TO-OG-a-2 as amended @adc6874dea.

AC13 (discriminating): for each of the three test modules granted FIXTURE-ONLY, the count of assert statements
(`assert`, `self.assert*`, `pytest.raises`) at HEAD equals the count at the cut base 3f94e0a024. Both vintages
are read from git objects (`git show <rev>:<path>`), never from the worktree; the worktree's agreement with HEAD
is printed as a disclosure only. A git read that fails or returns nothing is a FAIL, never a zero.

Usage:  <python> og_a2.py AC13
Prints per-module lines, then `VERDICT: PASS-OGA2-AC13` or `VERDICT: FAIL-OGA2-AC13 <reason>`.
"""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

BASE = "3f94e0a024"
MODULES = (
    "infra/aws/ec2/opal-gateway/tests/test_oauth_durable.py",
    "infra/aws/ec2/opal-gateway/tests/test_jwt_cve_lock.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_audit.py",
)
KINDS = ("assert", "self.assert*", "pytest.raises")


def _git(root, *args):
    proc = subprocess.run(["git", *args], cwd=str(root), capture_output=True)
    return proc.returncode, proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace")


def count(source: str) -> dict:
    """Assert statements by kind: `assert` statements, `self.assert*(...)` calls, `pytest.raises(...)` calls."""
    n = dict.fromkeys(KINDS, 0)
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Assert):
            n["assert"] += 1
        elif (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
              and isinstance(node.func.value, ast.Name)):
            owner, attr = node.func.value.id, node.func.attr
            if owner == "self" and attr.startswith("assert"):
                n["self.assert*"] += 1
            elif owner == "pytest" and attr == "raises":
                n["pytest.raises"] += 1
    return n


def _fmt(n: dict) -> str:
    return " ".join("%s=%d" % (k, n[k]) for k in KINDS) + " total=%d" % sum(n.values())


def ac13() -> int:
    # Positive control on the counter: one of each kind must count 1 each, and a non-assert call 0.
    control = count("def t(self):\n    assert x\n    self.assertEqual(a, b)\n    self.fail()\n"
                    "    with pytest.raises(E):\n        pass\n    pytest.skip()\n")
    if control != {"assert": 1, "self.assert*": 1, "pytest.raises": 1}:
        print("VERDICT: FAIL-OGA2-AC13 counter positive control read %s" % control)
        return 1
    print("counter positive control: %s (expected 1/1/1)" % _fmt(control))
    rc, top, err = _git(Path(__file__).resolve().parent, "rev-parse", "--show-toplevel")
    if rc != 0 or not top.strip():
        print("VERDICT: FAIL-OGA2-AC13 git rev-parse --show-toplevel rc=%d %s" % (rc, err.strip()))
        return 1
    root = Path(top.strip())
    rc, head, err = _git(root, "rev-parse", "--short=10", "HEAD")
    if rc != 0:
        print("VERDICT: FAIL-OGA2-AC13 git rev-parse HEAD rc=%d %s" % (rc, err.strip()))
        return 1
    head = head.strip()
    print("HEAD %s, cut base %s, modules %d" % (head, BASE, len(MODULES)))
    unequal = []
    for path in MODULES:
        counts = {}
        for label, rev in (("HEAD", head), ("base", BASE)):
            rc, src, err = _git(root, "show", "%s:%s" % (rev, path))
            if rc != 0 or not src.strip():
                print("VERDICT: FAIL-OGA2-AC13 git show %s:%s rc=%d bytes=%d %s"
                      % (rev, path, rc, len(src), err.strip()))
                return 1
            counts[label] = (count(src), len(src.encode("utf-8")))
        (h, hb), (b, bb) = counts["HEAD"], counts["base"]
        same = sum(h.values()) == sum(b.values())
        rc_wt, _, _ = _git(root, "diff", "--quiet", "HEAD", "--", path)
        print("%s: HEAD %s (%d bytes) | base %s (%d bytes) | %s | worktree==HEAD: %s"
              % (Path(path).name, _fmt(h), hb, _fmt(b), bb, "EQUAL" if same else "DIFFER",
                 "yes" if rc_wt == 0 else "no"))
        if h != b and same:
            print("  note: totals equal, kinds differ")
        if not same:
            unequal.append("%s HEAD=%d base=%d" % (Path(path).name, sum(h.values()), sum(b.values())))
    print("modules equal: %d of %d" % (len(MODULES) - len(unequal), len(MODULES)))
    if unequal:
        print("VERDICT: FAIL-OGA2-AC13 %s" % "; ".join(unequal))
        return 1
    print("VERDICT: PASS-OGA2-AC13")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] != ["AC13"]:
        print("usage: og_a2.py AC13", file=sys.stderr)
        sys.exit(2)
    sys.exit(ac13())
