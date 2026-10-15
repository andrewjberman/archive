"""IRPT_DASHBD round 119, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the build input for the second zip: the source-map re-pin and the build-time registry test.

  DBC119-1-AC1 the source map differs from the commit this round was issued at in the scopes.json `pin` and `sha256` fields of the two holdings-performance functions and in NOTHING else
  DBC119-2-AC1 the build-time test exists, passes on the staged pins, and FAILS when the staged scopes.json pin is put back to the old commit (the planted negative control)

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BASE = "ad799ad40b"  # the commit this round was issued at
SRC_MAP = "infra/aws/lambda/ci/lambda-source-map.json"
FUNCS = ("irpt-holdings-performance-lambda", "irpt-inf-holdings-performance-lambda")
NEW_PIN = "69679b90e3dc52b670d33fddd96d06be1deaac90"
NEW_SHA = "6ce64167c26588521fded21330dc59e0109450e9a01c92e0f6ca9aa90b53cfae"
OLD_PIN = "14b52ca13a467e4be0e47231fb6840611bbb134a"
TEST = "infra/aws/lambda/investor-reporting/holdings-performance/tests/test_zip_registry_resolves.py"
REG = "infra/logic/registry/scopes.json"


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True)
    need(r.returncode == 0, "git " + " ".join(args[:2]) + " failed: " + r.stderr.decode("utf-8", "replace")[:100])
    return r.stdout.decode("utf-8")


def ac_1(root):
    now = json.loads((Path(root) / SRC_MAP).read_text(encoding="utf-8"))
    base = json.loads(git(root, "show", BASE + ":" + SRC_MAP))
    for fn in FUNCS:
        for s in now["functions"][fn]["staged_from"]:
            if s["repo_path"] == REG:
                need(s["pin"] == NEW_PIN and s["sha256"] == NEW_SHA, "the scopes.json entry of %s is not the new pin and sha256" % fn)
                s["pin"], s["sha256"] = OLD_PIN, base_entry(base, fn)["sha256"]
    need(now == base, "the source map differs from the base in more than the scopes.json pin and sha256 of the two functions")
    stat = git(root, "diff", "--numstat", BASE, "--", SRC_MAP).split()
    need(len(stat) >= 2 and int(stat[0]) == int(stat[1]) == 2 * len(FUNCS), "the diff is not exactly one pin line and one sha256 line per function: %s" % stat[:2])
    others = [ln for ln in git(root, "diff", "--name-only", BASE, "--", "infra/aws/lambda/ci", "infra/aws/lambda/investor-reporting/holdings-performance", "infra/logic/registry", "data/assets/scripts/gold/irpt_holdings_performance").splitlines() if ln and ln not in (SRC_MAP, TEST)]
    need(not others, "files changed outside the order's surface: " + ", ".join(others[:4]))


def base_entry(base, fn):
    for s in base["functions"][fn]["staged_from"]:
        if s["repo_path"] == REG:
            return s
    raise Fail("base entry absent for " + fn)


def ac_2(root):
    t = Path(root) / TEST
    need(t.is_file() and "def test_" in t.read_text(encoding="utf-8"), "the build-time test is absent")
    cmd = [sys.executable, "-m", "pytest", str(t), "-q", "-p", "no:cacheprovider"]
    ok = subprocess.run(cmd, capture_output=True, text=True, cwd=str(root), timeout=100)
    need(ok.returncode == 0 and re.search(r"\d+ passed", ok.stdout) is not None, "the test does not pass on the staged pins: " + ok.stdout[-200:])
    env = dict(os.environ, HP_REGISTRY_SCOPES_PIN=OLD_PIN)
    bad = subprocess.run(cmd, capture_output=True, text=True, cwd=str(root), timeout=100, env=env)
    need(bad.returncode != 0 and "failed" in bad.stdout, "the planted negative control did not fail: the test passes with the old scopes.json pin")


ARMS = {"DBC119-1-AC1": ac_1, "DBC119-2-AC1": ac_2}


def main(argv):
    root, cid = argv[0], argv[1]
    try:
        need(cid in ARMS, "unknown criterion " + cid)
        ARMS[cid](root)
    except Fail as e:
        print(str(e))
        print(cid + " FAIL")
        return 1
    except Exception as e:
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
