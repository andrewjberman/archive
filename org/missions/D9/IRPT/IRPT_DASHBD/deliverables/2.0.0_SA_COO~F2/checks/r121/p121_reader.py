"""IRPT_DASHBD round 121, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-3: the class-series READER, new portal files only.

  DB-f-801 (~801) a reader that fetches one account's class_series object (route GET .../reporting/{account_id}/class_series,
                  CTO call 3596 and ~S2 msg 8848; the object's shape is ~D2's, msg 8846) and turns the columnar document into the
                  rows the round-119 class model reads. NEW files, NOT MOUNTED, nothing imports them.
                  DBF121-1-AC1 (the tests: titles and a clean bun run), DBF121-1-AC2 (bounds: exactly the two new files)

The checker runs the named bun test in the worker's portal worktree (<root>/portal) without colour and reads the portal diff
against the class candidate head.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

IR = "portal/src/pages/InvestorReporting/"
READER = "src/pages/InvestorReporting/tabs/reporting/classes/classSeriesRead.ts"
TEST = "src/pages/InvestorReporting/__tests__/irpt-dashbd/class-series-read.test.ts"
BASE_SHA = "7fa808c949fbe5d9c9d4ea1aea3aa3006be7d2e8"
ALLOWED_FILES = (READER, TEST)
TITLE_WORDS = ("path", "columnar", "rows", "absent", "null", "misaligned", "unreadable", "tenant")
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def titles_of(text):
    return [m.group(2) for m in re.finditer(r"""\b(?:test|it)\(\s*(['"`])(.+?)\1""", text)]


def missing_title_words(titles, words):
    low = " | ".join(titles).lower()
    return [w for w in words if w not in low]


def bun_result(out):
    out = ANSI.sub("", out)
    fails = re.findall(r"^\s*(\d+) fail", out, re.M)
    passes = re.findall(r"^\s*(\d+) pass", out, re.M)
    return (int(passes[-1]) if passes else 0), (int(fails[-1]) if fails else -1)


def read_text(root, rel):
    p = Path(root) / "portal" / rel
    need(p.is_file(), "missing file " + rel)
    return p.read_text(encoding="utf-8")


def run_bun(root, test_rel):
    bun = shutil.which("bun")
    need(bun is not None, "bun not on PATH")
    env = {k: v for k, v in os.environ.items() if k != "FORCE_COLOR"}
    env["NO_COLOR"] = "1"
    p = subprocess.run([bun, "test", test_rel], cwd=str(Path(root) / "portal"), capture_output=True,
                       text=True, timeout=100, env=env)
    passes, fails = bun_result((p.stdout or "") + (p.stderr or ""))
    need(p.returncode == 0 and fails == 0, "bun test %s rc=%s fail=%s" % (test_rel, p.returncode, fails))
    return passes


def ac_tests(root):
    mt = missing_title_words(titles_of(read_text(root, TEST)), TITLE_WORDS)
    need(not mt, "test titles lack " + repr(mt))
    need(run_bun(root, TEST) >= 8, "tests pass fewer than 8")


def changed_files(root):
    p = subprocess.run(["git", "-C", str(Path(root) / "portal"), "diff", "--name-only", BASE_SHA + "..HEAD"],
                       capture_output=True, text=True, timeout=60)
    need(p.returncode == 0, "git diff rc=%s" % p.returncode)
    return [x.strip() for x in p.stdout.splitlines() if x.strip()]


def outside_allowed(files):
    return [f for f in files if f not in ALLOWED_FILES]


def ac_bounds(root):
    files = changed_files(root)
    need(READER in files and TEST in files, "the two new files are not both in the diff: " + repr(files))
    out = outside_allowed(files)
    need(not out, "files changed outside the grant: " + repr(out))


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    arm("titles", titles_of("test('a b', () => {})\nit(\"c\", () => {})"), ["a b", "c"])
    arm("words-green", missing_title_words(["path columnar rows absent null misaligned unreadable tenant"], TITLE_WORDS), [])
    arm("words-red", missing_title_words(["only path"], TITLE_WORDS),
        ["columnar", "rows", "absent", "null", "misaligned", "unreadable", "tenant"])
    arm("bun-ansi", bun_result("\x1b[32m 9 pass\x1b[0m\n\x1b[2m 0 fail\x1b[0m\n"), (9, 0))
    arm("bun-red", bun_result("\n 7 pass\n 2 fail\n"), (7, 2))
    arm("allowed-green", outside_allowed([READER, TEST]), [])
    arm("allowed-red", outside_allowed([READER, "src/App.tsx"]), ["src/App.tsx"])
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF121-1-AC1": ac_tests, "DBF121-1-AC2": ac_bounds}
    if ac not in table:
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        table[ac](root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
