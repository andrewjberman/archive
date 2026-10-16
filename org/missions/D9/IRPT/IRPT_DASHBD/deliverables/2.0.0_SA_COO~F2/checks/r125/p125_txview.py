"""IRPT_DASHBD round 125, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the transactions table VIEW MODEL, new portal files only.

  DB-f-1101 (~1101) a pure view model for the transactions table (PRD workstream F item 3): the brief's 14 columns as a row type with
                  the absent ones nullable, the type filter, the symbol search, the sort, the export rows (CSV text with a guard
                  against spreadsheet formulas) and the virtualised window. NEW files, NOT MOUNTED, nothing imports them.
                  DBF125-1-AC1 (the tests: titles and a clean bun run), DBF125-1-AC2 (bounds: exactly the two new files)

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
READER = "src/pages/InvestorReporting/tabs/reporting/transactions/transactionsView.ts"
TEST = "src/pages/InvestorReporting/__tests__/irpt-dashbd/transactions-view.test.ts"
BASE_SHA = "a062c56e53b174eab043b1e50002c93eb7a56f8b"
ALLOWED_FILES = (READER, TEST)
TITLE_WORDS = ("filter", "search", "sort", "export", "window", "absent", "formula", "order")
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
    need(run_bun(root, TEST) >= 12, "tests pass fewer than 12")


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
    arm("words-green", missing_title_words(["filter search sort export window absent formula order"], TITLE_WORDS), [])
    arm("words-red", missing_title_words(["only filter"], TITLE_WORDS),
        ["search", "sort", "export", "window", "absent", "formula", "order"])
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
    table = {"DBF125-1-AC1": ac_tests, "DBF125-1-AC2": ac_bounds}
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
