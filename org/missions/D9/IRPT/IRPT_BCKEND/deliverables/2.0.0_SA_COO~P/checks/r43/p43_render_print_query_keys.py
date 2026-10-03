"""Round 43 (IRPT_BCKEND ~P, row S308) -- the export render host forwards the PATH B print query: account and version (and an
Analysis print's request) reach the print URL; unlisted keys are still dropped.

Usage: python <this file> <repo_root> <criterion_id>
  IB43-1-AC1  infra/aws/ec2/investor-reporting-export/render_export.cjs: PRINT_QUERY_KEYS (read from the source) holds the seven
              existing keys plus account, version and request; then tests/test_print_query.cjs (beside it) names 'account',
              'version', 'selection' and 'request', and node --test passes at least 4 tests, 0 failed.
  IB43-1-AC2  a GUARD: against base cd24c46d57, every changed line of render_export.cjs is the PRINT_QUERY_KEYS line or lies in
              an appended export block after the last original line (the render flow itself is unchanged); node --check passes.
              Base: PASS (no change).
Bounded at 110 s per node run. Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import re
import subprocess
import sys
from pathlib import Path

DIR = "infra/aws/ec2/investor-reporting-export/"
OLD = ["bundle", "tenant", "revision", "kind", "selection", "start", "end"]
NEW = ["account", "version", "request"]
BASE = "cd24c46d57"
KEYLINE = re.compile(r"^const PRINT_QUERY_KEYS = \[(.*)\];\s*$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB43"))
        sys.exit(1)

    d = root / DIR
    src = (d / "render_export.cjs").read_text(encoding="utf-8")
    if cid == "IB43-1-AC1":
        line = next((ln for ln in src.splitlines() if KEYLINE.match(ln)), None)
        if line is None:
            fail("no 'const PRINT_QUERY_KEYS = [...];' line")
        keys = re.findall(r"'([^']+)'", KEYLINE.match(line).group(1))
        if not all(k in keys for k in OLD + NEW):
            fail("PRINT_QUERY_KEYS is %s" % keys)
        t = d / "tests" / "test_print_query.cjs"
        if not t.is_file():
            fail("no %stests/test_print_query.cjs" % DIR)
        ts = t.read_text(encoding="utf-8")
        for w in ("account", "version", "selection", "request"):
            if w not in ts:
                fail("the test never names %r" % w)
        try:
            r = subprocess.run(["node", "--test", "tests/test_print_query.cjs"], cwd=str(d), capture_output=True,
                               text=True, timeout=110)
        except subprocess.TimeoutExpired:
            fail("node --test exceeded 110 s")
        out = re.sub(r"\x1b\[[0-9;]*m", "", (r.stdout or "") + (r.stderr or ""))
        p = re.search(r"\bpass (\d+)", out)
        f = re.search(r"\bfail (\d+)", out)
        if r.returncode or not p or int(p.group(1)) < 4 or (f and int(f.group(1)) > 0):
            fail("node --test: %s" % out[-400:])
        print("OK: PRINT_QUERY_KEYS %s; %s tests passed, 0 failed" % (keys, p.group(1)))
    elif cid == "IB43-1-AC2":
        base = subprocess.run(["git", "show", "%s:%srender_export.cjs" % (BASE, DIR)], cwd=str(root),
                              capture_output=True).stdout.decode("utf-8").splitlines()
        now = src.splitlines()
        if not base:
            fail("cannot read the base render_export.cjs at %s" % BASE)
        if len(now) < len(base):
            fail("lines were removed (%d -> %d)" % (len(base), len(now)))
        for i, (a, b) in enumerate(zip(base, now)):
            if a != b and not (KEYLINE.match(a) and KEYLINE.match(b)):
                fail("line %d changed outside PRINT_QUERY_KEYS: %r" % (i + 1, b[:100]))
        r = subprocess.run(["node", "--check", "render_export.cjs"], cwd=str(d), capture_output=True, text=True,
                           timeout=110)
        if r.returncode:
            fail("node --check: %s" % (r.stderr or "")[-300:])
        print("OK: only PRINT_QUERY_KEYS changed (plus %d appended line(s)); node --check passes"
              % (len(now) - len(base)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
