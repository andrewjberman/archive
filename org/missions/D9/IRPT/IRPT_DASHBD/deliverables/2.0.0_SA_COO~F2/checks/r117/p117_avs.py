"""IRPT_DASHBD round 117, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- DB-f-506, the by_row reading of the sixteen avs benchmark members (row D2-S64).

  DB-f-506 (~506) a NEW test file that pins the report model's reading of the sixteen `avs.<window>.benchmark_<kind>` members as by_row per account,
                  on a document shaped as the contract's per_row_member_form. Test only: no source file changes.
  DBF117-1-AC1  the test file exists, carries the title words and passes with at least 8 tests
  DBF117-1-AC2  bounds: the portal diff from the candidate head e23ddb8e is that one test file and nothing else

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
TEST = IR + "__tests__/irpt-dashbd/avs-by-row.test.tsx"
BASE_SHA = "e23ddb8e34035bb6fa6dc5e59d7f83220e83d65c"
ALLOWED = ("src/pages/InvestorReporting/__tests__/irpt-dashbd/avs-by-row.test.tsx",)
TITLE_WORDS = ("by_row", "account", "benchmark", "absent", "household", "window")
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def missing_tokens(text, tokens):
    return [t for t in tokens if t not in text]


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
    p = Path(root) / rel
    need(p.is_file(), "missing file " + rel)
    return p.read_text(encoding="utf-8")


def run_bun(root, test_rel):
    bun = shutil.which("bun")
    need(bun is not None, "bun not on PATH")
    env = {k: v for k, v in os.environ.items() if k != "FORCE_COLOR"}
    env["NO_COLOR"] = "1"
    p = subprocess.run([bun, "test", test_rel[len("portal/"):]], cwd=str(Path(root) / "portal"), capture_output=True,
                       text=True, timeout=100, env=env)
    passes, fails = bun_result((p.stdout or "") + (p.stderr or ""))
    need(p.returncode == 0 and fails == 0, "bun test rc=%s fail=%s" % (p.returncode, fails))
    return passes


def ac_test(root):
    ttl = titles_of(read_text(root, TEST))
    mt = missing_title_words(ttl, TITLE_WORDS)
    need(not mt, "test titles lack " + repr(mt))
    passes = run_bun(root, TEST)
    need(passes >= 8, "tests pass %d < 8" % passes)


def changed_files(root):
    p = subprocess.run(["git", "-C", str(Path(root) / "portal"), "diff", "--name-only", BASE_SHA + "..HEAD"],
                       capture_output=True, text=True, timeout=60)
    need(p.returncode == 0, "git diff rc=%s" % p.returncode)
    return [x.strip() for x in p.stdout.splitlines() if x.strip()]


def outside_allowed(files):
    return [f for f in files if f not in ALLOWED]


def ac_bounds(root):
    files = changed_files(root)
    need(len(files) > 0, "the portal branch carries no change from the candidate head")
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

    arm("missing-green", missing_tokens("a b", ("a", "b")), [])
    arm("missing-red", missing_tokens("a", ("a", "b")), ["b"])
    arm("titles", titles_of("test('a b', () => {})"), ["a b"])
    arm("words-red", missing_title_words(["by_row only"], TITLE_WORDS), ["account", "benchmark", "absent", "household", "window"])
    arm("bun-ansi", bun_result("\x1b[32m 7 pass\x1b[0m\n\x1b[2m 0 fail\x1b[0m\n"), (7, 0))
    arm("bun-red", bun_result("\n 7 pass\n 2 fail\n"), (7, 2))
    arm("allowed-green", outside_allowed(list(ALLOWED)), [])
    arm("allowed-red", outside_allowed([ALLOWED[0], "src/App.tsx"]), ["src/App.tsx"])
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF117-1-AC1": ac_test, "DBF117-1-AC2": ac_bounds}
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
