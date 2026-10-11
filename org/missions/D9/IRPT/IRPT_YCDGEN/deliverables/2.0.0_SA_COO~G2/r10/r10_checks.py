"""IRPT_YCDGEN round 10 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python r10_checks.py a10        _reason_line prints one sentence per not-held cause and no raw string
    python r10_checks.py a10suite   the ycharts/research tests: 0 failed, at least 247 passed

Prints one RESULT line: R10-<MODE>-OK or R10-<MODE>-FAIL <reason>; rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

KEPT = "Not available: Opal does not keep this figure in this version of the report."
COVERED = "Not available: Opal keeps this figure, but has no data for the securities this portfolio holds."
OTHER = "Not available: this figure could not be worked out for this portfolio."


def main(mode):
    if mode == "a10":
        sys.path.insert(0, "infra/aws/lambda/investor-reporting/ycharts/research")
        try:
            import layout_overview as lo
            p = lo.NOT_HELD_PREFIX
            got = {"NO_RULE": lo._reason_line(p + "NO_RULE:a sentence", False),
                   "NO_ROW": lo._reason_line(p + "NO_ROW:t.f is empty for all 3 holdings", False),
                   "FIELD_MISMATCH": lo._reason_line(p + "FIELD_MISMATCH:x", False),
                   "none": lo._reason_line(p + "no cause here", False)}
            same = {"niv": lo._reason_line(lo.NOT_IN_THIS_VERSION, False) == lo.NOT_IN_THIS_VERSION_LINE,
                    "budget": lo._reason_line(lo.OUTSIDE_BUDGET_REASON, False) == lo.OUTSIDE_BUDGET_LINE,
                    "generic_opal": lo._reason_line("INPUT_MISSING:holdings", False)
                    == "Not available: this element is not given for this portfolio. Reason: INPUT_MISSING:holdings",
                    "generic_vendor": lo._reason_line("INPUT_MISSING:holdings", True)
                    == "Not available: YCharts' data does not give this element for this portfolio. Reason: INPUT_MISSING:holdings"}
        except Exception as exc:
            print("R10-A10-FAIL %s: %s" % (type(exc).__name__, str(exc)[:200]))
            return 1
        want = {"NO_RULE": KEPT, "NO_ROW": COVERED, "FIELD_MISMATCH": OTHER, "none": OTHER}
        bad = [k for k in want if got[k] != want[k]] + [k for k, ok in same.items() if not ok]
        for k in want:
            print("%s -> %r" % (k, got[k]))
        if bad or any("NOT_HELD" in v for v in got.values()):
            print("R10-A10-FAIL wrong or changed: %s" % ", ".join(bad or ["a sentence contains NOT_HELD"]))
            return 1
        print("R10-A10-OK sentences=3 untouched_branches=4")
        return 0
    if mode == "a10suite":
        out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no",
                              "infra/aws/lambda/investor-reporting/ycharts/research/tests"], capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
        line = lines[-1].strip() if lines else "(no summary line)"
        print(line)
        m = re.search(r"([0-9]+) passed", line)
        passed = int(m.group(1)) if m else 0
        if out.returncode != 0 or "failed" in line or "error" in line or passed < 247:
            print("R10-A10SUITE-FAIL rc=%d passed=%d (need >= 247, 0 failed, 0 errors)" % (out.returncode, passed))
            return 1
        print("R10-A10SUITE-OK passed=%d" % passed)
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
