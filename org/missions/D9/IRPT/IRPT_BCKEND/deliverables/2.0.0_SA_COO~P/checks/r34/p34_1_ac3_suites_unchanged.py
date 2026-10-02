"""IB34-1-AC3 -- the export entry and the source map are shared, so the suites they reach pass unchanged.

Runs each suite in its OWN pytest process (the folders share module names), each bounded at 110 s, with --color=no -rf. Baselines at
CLOUD 2026-10-02 ~14:5xZ: export 158 passed, _contracts 185 passed, _render_identity 45 passed, 0 failed; _authz 201 passed + the six
test_unguarded_census failures. Grades: each suite fails only its listed baseline ids. Base: PASS (a regression guard).
Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

B = "infra/aws/lambda/investor-reporting/"
U = B + "_authz/tests/test_unguarded_census.py::"
BASELINE = {
    "_authz/tests": {U + "test_zero_of_n_over_the_routes_this_order_may_open", U + "test_the_whole_file_census_is_zero",
                     U + "test_the_census_fires_when_one_handler_is_unregistered[0]",
                     U + "test_the_census_fires_when_one_handler_is_unregistered[3]",
                     U + "test_the_census_fires_when_one_handler_is_unregistered[7]",
                     U + "test_every_entry_carries_the_published_route_table_it_serves"},
    "export/tests": set(), "_contracts": set(), "_render_identity/tests": set(),
}


def fail(msg):
    print("FAIL: " + msg)
    print("IB34-1-AC3 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    lines = []
    for suite, allowed in BASELINE.items():
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "-rf",
                                B + suite], cwd=str(root), capture_output=True, text=True, timeout=110)
        except subprocess.TimeoutExpired:
            fail("%s exceeded 110 s" % suite)
        out = (r.stdout or "") + (r.stderr or "")
        failed = {m.group(1) for m in re.finditer(r"^FAILED (\S+)", out, re.M)}
        errored = re.search(r"(\d+) error", out)
        passed = re.search(r"(\d+) passed", out)
        if errored:
            fail("%s: %s" % (suite, errored.group(0)))
        new = failed - allowed
        if new:
            fail("%s fails beyond its baseline: %s" % (suite, sorted(new)[:3]))
        lines.append("%s %s passed, %d baseline failure(s)" % (suite, passed.group(1) if passed else "0", len(failed)))
    print("OK: " + "; ".join(lines))
    print("IB34-1-AC3 PASS")


if __name__ == "__main__":
    main()
