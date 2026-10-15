"""IRPT_DASHBD round 115, workstream ~F2 (issuer 2.0.0_SA_COO~F2) -- DB-f-503, the export mount of the filled report.

  DB-f-503 (~503) the filled-report export: the page names a `FILLED_REPORT` source at submit, the preview and the print read the
                  report through the reader of round 114 (frozen by a version on a print), and the print renders the report document.
                  Portal branch only, inert until a route serves a report.
  DBF115-1-AC1  the export side (source builder, submit, button, preview, bundle resolution, the tab's export target)
  DBF115-1-AC2  the print side (print entry reads the report, the document renders it, the reader takes a version)
  DBF115-1-AC3  bounds: the portal diff from the round-114 head touches only the granted paths

The checker runs the named bun tests in the worker's portal worktree (<root>/portal) without colour, and reads the files for the
tokens the cell names.

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
T_EXPORT = IR + "__tests__/irpt-dashbd/export-filled-report.test.tsx"
T_PRINT = IR + "__tests__/irpt-dashbd/print-filled-report.test.tsx"
BASE_SHA = "d3c379663faceca7f4907366e0943d2b19022b6e"
ALLOWED_FILES = (
    "src/pages/InvestorReporting/tabs/reporting/ReportingTab.tsx",
    "src/pages/InvestorReporting/dashboard/report/reportRead.ts",
    "src/pages/InvestorReporting/__tests__/irpt-dashbd/export-filled-report.test.tsx",
    "src/pages/InvestorReporting/__tests__/irpt-dashbd/print-filled-report.test.tsx",
)
ALLOWED_PREFIXES = (
    "src/pages/InvestorReporting/export/",
    "src/pages/InvestorReporting/render/",
)
EXPORT_TOKENS = (
    (IR + "export/filledReportSource.ts", ("FILLED_REPORT", "export function filledReportSource")),
    (IR + "export/submit.ts", ("FILLED_REPORT",)),
    (IR + "export/ExportButton.tsx", ("clientId",)),
    (IR + "export/resolveBundle.ts", ("readReportAnswer", "filledReport")),
    (IR + "tabs/reporting/ReportingTab.tsx", ("buildFilledReportExportTarget",)),
)
PRINT_TOKENS = (
    (IR + "render/PrintEntry.tsx", ("client", "version")),
    (IR + "dashboard/report/reportRead.ts", ("version_id",)),
)
EXPORT_TITLE_WORDS = ("source", "submit", "preview", "served", "absent", "client", "fixture")
PRINT_TITLE_WORDS = ("print", "version", "client", "served", "absent", "falls back", "document")
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


def run_bun(root, test_rel):
    bun = shutil.which("bun")
    need(bun is not None, "bun not on PATH")
    rel = test_rel[len("portal/"):]
    env = {k: v for k, v in os.environ.items() if k != "FORCE_COLOR"}
    env["NO_COLOR"] = "1"
    p = subprocess.run([bun, "test", rel], cwd=str(Path(root) / "portal"), capture_output=True, text=True, timeout=100, env=env)
    out = (p.stdout or "") + (p.stderr or "")
    passes, fails = bun_result(out)
    need(p.returncode == 0 and fails == 0, "bun test %s rc=%s fail=%s" % (rel, p.returncode, fails))
    return passes


def read_text(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "missing file " + rel)
    return p.read_text(encoding="utf-8")


def token_problems(root, table):
    bad = []
    for rel, tokens in table:
        miss = missing_tokens(read_text(root, rel), tokens)
        if miss:
            bad.append("%s lacks %r" % (rel, miss))
    return bad


def ac_export(root):
    bad = token_problems(root, EXPORT_TOKENS)
    need(not bad, "; ".join(bad))
    mt = missing_title_words(titles_of(read_text(root, T_EXPORT)), EXPORT_TITLE_WORDS)
    need(not mt, "export test titles lack " + repr(mt))
    passes = run_bun(root, T_EXPORT)
    need(passes >= 8, "export tests pass %d < 8" % passes)


def ac_print(root):
    bad = token_problems(root, PRINT_TOKENS)
    need(not bad, "; ".join(bad))
    mounts = [p for p in (Path(root) / IR / "render").rglob("*.tsx")
              if p.name != "PerformanceReportDocument.tsx" and "PerformanceReportDocument" in p.read_text(encoding="utf-8")]
    need(len(mounts) > 0, "no render file other than the document itself mounts PerformanceReportDocument")
    mt = missing_title_words(titles_of(read_text(root, T_PRINT)), PRINT_TITLE_WORDS)
    need(not mt, "print test titles lack " + repr(mt))
    passes = run_bun(root, T_PRINT)
    need(passes >= 6, "print tests pass %d < 6" % passes)


def changed_files(root):
    p = subprocess.run(["git", "-C", str(Path(root) / "portal"), "diff", "--name-only", BASE_SHA + "..HEAD"],
                       capture_output=True, text=True, timeout=60)
    need(p.returncode == 0, "git diff rc=%s" % p.returncode)
    return [x.strip() for x in p.stdout.splitlines() if x.strip()]


def outside_allowed(files):
    return [f for f in files if f not in ALLOWED_FILES and not any(f.startswith(x) for x in ALLOWED_PREFIXES)]


def ac_bounds(root):
    files = changed_files(root)
    need(len(files) > 0, "the portal branch carries no change from the round-114 head")
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

    arm("tokens-green", missing_tokens("a b c", ("a", "c")), [])
    arm("tokens-red", missing_tokens("a b", ("a", "c")), ["c"])
    arm("titles", titles_of("test('a b', () => {})\nit(\"c\", () => {})"), ["a b", "c"])
    arm("words-green", missing_title_words(["print of a client", "version", "served", "absent", "falls back", "document"], PRINT_TITLE_WORDS), [])
    arm("words-red", missing_title_words(["only print"], PRINT_TITLE_WORDS), ["version", "client", "served", "absent", "falls back", "document"])
    arm("bun-green", bun_result("\n 7 pass\n 0 fail\n"), (7, 0))
    arm("bun-red", bun_result("\n 7 pass\n 2 fail\n"), (7, 2))
    arm("bun-ansi", bun_result("\x1b[32m 7 pass\x1b[0m\n\x1b[2m 0 fail\x1b[0m\n"), (7, 0))
    arm("bun-none", bun_result("nothing"), (0, -1))
    arm("allowed-green", outside_allowed(["src/pages/InvestorReporting/export/submit.ts", ALLOWED_FILES[0]]), [])
    arm("allowed-red", outside_allowed(["src/pages/InvestorReporting/export/submit.ts", "src/App.tsx"]), ["src/App.tsx"])
    arm("allowed-render", outside_allowed(["src/pages/InvestorReporting/render/PrintEntry.tsx"]), [])
    arm("allowed-dashboard-other", outside_allowed(["src/pages/InvestorReporting/dashboard/reportingRead.ts"]),
        ["src/pages/InvestorReporting/dashboard/reportingRead.ts"])
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF115-1-AC1": ac_export, "DBF115-1-AC2": ac_print, "DBF115-1-AC3": ac_bounds}
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
