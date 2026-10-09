"""IRPT_ANLREQ round 1, workstream ~G: the checks for AR-g-11 and AR-g-12 (issuer 2.0.0_SA_COO~G2).

    python ar1_g2_checks.py g11        the READY signal tests pass (test_ready_signal.py)
    python ar1_g2_checks.py g12        the package tests pass (test_layout_commentary.py, test_opal_packager.py)
    python ar1_g2_checks.py g13        the resident's I4 poll tests pass (test_package_poll.py)
    python ar1_g2_checks.py regress    the generate and research suites: no file newly red against the base

Run from the worktree root. Prints one RESULT line: AR1-G2-<MODE>-OK or AR1-G2-<MODE>-FAIL <reason>; rc 0 only on OK.
Base reading (box/dell2 @7c202254ea, 2026-10-09): generate 2 failed, 32 errors, all in BASE_RED below; research 165 passed.
"""
import re
import subprocess
import sys

Y = "infra/aws/lambda/investor-reporting/ycharts"
BASE_RED = {Y + "/generate/tests/test_custody_retained.py", Y + "/generate/tests/test_custody_entry.py"}
FILES = {
    "g11": [Y + "/generate/tests/test_ready_signal.py"],
    "g12": [Y + "/research/tests/test_layout_commentary.py", Y + "/research/tests/test_opal_packager.py"],
    "g13": [Y + "/generate/tests/test_package_poll.py"],
}
MIN_PASSED = {"g11": 4, "g12": 5, "g13": 5}
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def pytest(paths):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rfE"] + paths,
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    return out.returncode, ANSI.sub("", out.stdout + out.stderr)


def summary(text):
    lines = [ln for ln in text.splitlines() if re.search(r"\d+ (passed|failed|error)", ln)]
    return lines[-1].strip() if lines else "(no summary line)"


def main(mode):
    if mode in FILES:
        rc, text = pytest(FILES[mode])
        line = summary(text)
        print(line)
        m = re.search(r"(\d+) passed", line)
        passed = int(m.group(1)) if m else 0
        if rc != 0 or "failed" in line or "error" in line or passed < MIN_PASSED[mode]:
            print("AR1-G2-%s-FAIL rc=%d passed=%d (need >= %d, 0 failed)" % (mode.upper(), rc, passed, MIN_PASSED[mode]))
            return 1
        print("AR1-G2-%s-OK passed=%d" % (mode.upper(), passed))
        return 0
    if mode == "regress":
        red = set()
        for suite in ("generate", "research"):
            _, text = pytest([Y + "/" + suite + "/tests"])
            print(suite + ": " + summary(text))
            red |= {i.split("::")[0] for i in re.findall(r"^(?:FAILED|ERROR) (\S+)", text, re.M)}
        new = sorted(red - BASE_RED)
        if new:
            print("AR1-G2-REGRESS-FAIL newly red: " + ", ".join(new))
            return 1
        print("AR1-G2-REGRESS-OK red files %d, all in the base set of %d" % (len(red), len(BASE_RED)))
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
