"""IB29-3-AC3 -- (c) the existing _authz, export and holdings suites pass unchanged (plus _render_identity, whose grant.py the
order also grants: 45 passed at the base).

Runs each suite in its OWN pytest process (the three folders share module names such as `handler` and `entry`; one process imports
the wrong one), each bounded at 110 s, with --color=no -rf. Grades: export/tests, holdings/tests and _render_identity/tests fail 0; _authz/tests fails ONLY
the six test_unguarded_census tests that already fail at the base (measured 2026-10-02 ~10:4xZ at CLOUD @11340658da; IRPT_BCKEND
STATUS~P "Parked": 6 failures since 2026-09-27) -- any other failure, or a seventh, is a FAIL. Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

B = "infra/aws/lambda/investor-reporting/"
BASELINE_AUTHZ = {
    B + "_authz/tests/test_unguarded_census.py::test_zero_of_n_over_the_routes_this_order_may_open",
    B + "_authz/tests/test_unguarded_census.py::test_the_whole_file_census_is_zero",
    B + "_authz/tests/test_unguarded_census.py::test_the_census_fires_when_one_handler_is_unregistered[0]",
    B + "_authz/tests/test_unguarded_census.py::test_the_census_fires_when_one_handler_is_unregistered[3]",
    B + "_authz/tests/test_unguarded_census.py::test_the_census_fires_when_one_handler_is_unregistered[7]",
    B + "_authz/tests/test_unguarded_census.py::test_every_entry_carries_the_published_route_table_it_serves",
}


def fail(msg):
    print("FAIL: " + msg)
    print("IB29-3-AC3 FAIL")
    sys.exit(1)


def run(root, suite):
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "-rf", B + suite],
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("%s exceeded 110 s" % suite)
    out = (r.stdout or "") + (r.stderr or "")
    failed = {m.group(1) for m in re.finditer(r"^FAILED (\S+)", out, re.M)}
    errored = re.search(r"(\d+) error", out)
    passed = re.search(r"(\d+) passed", out)
    if errored:
        fail("%s: %s" % (suite, errored.group(0)))
    return failed, int(passed.group(1)) if passed else 0


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    lines = []
    for suite in ("export/tests", "holdings/tests", "_render_identity/tests"):
        failed, n = run(root, suite)
        if failed:
            fail("%s fails %d: %s" % (suite, len(failed), sorted(failed)[:3]))
        lines.append("%s %d passed" % (suite, n))
    failed, n = run(root, "_authz/tests")
    new = failed - BASELINE_AUTHZ
    if new:
        fail("_authz/tests fails beyond the baseline: %s" % sorted(new)[:3])
    lines.append("_authz/tests %d passed, %d baseline failures only" % (n, len(failed)))
    print("OK: " + "; ".join(lines))
    print("IB29-3-AC3 PASS")


if __name__ == "__main__":
    main()
