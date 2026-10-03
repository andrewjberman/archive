"""Round 42 (IRPT_BCKEND ~P, row S307) -- the API Gateway authorizer (V2, opal-portal-authorizer) admits a render token on the 49F
reporting SERIES route, as the edge (V3) already does, so a PATH B export's render-delegate read is no longer denied.

Usage: python <this file> <repo_root> <criterion_id>
  IB42-1-AC1  infra/aws/users/lambda/portal-authorizer/index.mjs, imported under node: RENDER_ROUTE_CLAIMS holds
              'GET /api/scoped/investor-reporting/reporting/{account_id}/{which}' beside the three existing routes; then
              infra/aws/users/lambda/portal-authorizer/tests/test_render_reporting_series.mjs names 'series', 'manifest',
              'accountSetId' and 'summary', and node --test passes at least 6 tests, 0 failed. Needs the authorizer's
              node_modules at that path (gitignored; copied locally, never installed).
  IB42-1-AC2  a GUARD: every line index.mjs changes against the base 3376d7b446 lies inside the render branch
              (RENDER_ROUTE_CLAIMS through the end of authorizeRenderToken) -- the human token path is byte-unchanged.
              Base: PASS (no change).
Bounded at 110 s per node run. Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import re
import subprocess
import sys
from pathlib import Path

AUTH = "infra/aws/users/lambda/portal-authorizer/"
ROUTE = "GET /api/scoped/investor-reporting/reporting/{account_id}/{which}"
OLD = ("GET /api/scoped/investor-reporting/performance/{accountSetId}",
       "GET /api/scoped/investor-reporting/analysis/{jobId}/sections",
       "GET /api/scoped/investor-reporting/narrative/{reportId}")
BASE = "3376d7b446"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB42"))
        sys.exit(1)

    adir = root / AUTH
    if cid == "IB42-1-AC1":
        if not (adir / "node_modules" / "jsonwebtoken").is_dir():
            fail("no node_modules/jsonwebtoken under %s (copy the main tree's, never install)" % AUTH)
        # The source text, not an import: index.mjs's shared key module resolves @aws-sdk from a directory with no
        # node_modules (the Lambda runtime supplies it), so a bare import cannot be the instrument here.
        src_idx = (adir / "index.mjs").read_text(encoding="utf-8")
        m = re.search(r"const RENDER_ROUTE_CLAIMS = Object\.freeze\(\{(.*?)\}\);", src_idx, re.S)
        if not m:
            fail("no RENDER_ROUTE_CLAIMS = Object.freeze({...}); block in index.mjs")
        keys = re.findall(r"'([^']+)'\s*:", m.group(1))
        if ROUTE not in keys or not all(k in keys for k in OLD):
            fail("RENDER_ROUTE_CLAIMS keys are %s" % keys)
        t = adir / "tests" / "test_render_reporting_series.mjs"
        if not t.is_file():
            fail("no %stests/test_render_reporting_series.mjs" % AUTH)
        src = t.read_text(encoding="utf-8")
        for w in ("series", "manifest", "accountSetId", "summary"):
            if w not in src:
                fail("the test never names %r" % w)
        try:
            r = subprocess.run(["node", "--test", "tests/test_render_reporting_series.mjs"], cwd=str(adir),
                               capture_output=True, text=True, timeout=110)
        except subprocess.TimeoutExpired:
            fail("node --test exceeded 110 s")
        out = re.sub(r"\x1b\[[0-9;]*m", "", (r.stdout or "") + (r.stderr or ""))
        p = re.search(r"\bpass (\d+)", out)
        f = re.search(r"\bfail (\d+)", out)
        if r.returncode or not p or int(p.group(1)) < 6 or (f and int(f.group(1)) > 0):
            fail("node --test: %s" % out[-400:])
        print("OK: RENDER_ROUTE_CLAIMS %s; %s tests passed, 0 failed" % (keys, p.group(1)))
    elif cid == "IB42-1-AC2":
        base_src = subprocess.run(["git", "show", "%s:%sindex.mjs" % (BASE, AUTH)], cwd=str(root),
                                  capture_output=True).stdout.decode("utf-8")
        now_src = (adir / "index.mjs").read_text(encoding="utf-8")
        if not base_src:
            fail("cannot read the base index.mjs at %s" % BASE)
        b, n = base_src.splitlines(), now_src.splitlines()

        def branch(lines):
            s = next((i for i, ln in enumerate(lines) if ln.startswith("const RENDER_ROUTE_CLAIMS")), None)
            e = next((i for i, ln in enumerate(lines) if i > (s or 0) and ln.startswith("function extractToken")), None)
            if s is None or e is None:
                fail("cannot find the render branch bounds")
            return lines[:s], lines[e:]
        bh, bt = branch(b)
        nh, nt = branch(n)
        if bh != nh or bt != nt:
            fail("index.mjs changed outside the render branch (head %s, tail %s)" % (bh == nh, bt == nt))
        print("OK: index.mjs outside the render branch is byte-unchanged against %s" % BASE)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
