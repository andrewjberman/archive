"""CB5e1-AC1 check (2.0.0_SA_COO~C2, round 5): each Commonwealth script that reads the trading calendar refuses to run
when the calendar does not cover its table's dates.

Runs the three scripts as they are on this box and counts the ones that exit non-zero AND print a CALENDAR-UNCOVERED line.
A script still running at its per-script bound counts as NOT refused (a refusal comes before the heavy reads).
Writes nothing that persists: every script's output goes to one temporary directory, deleted on exit (CTO ruling A of 08:5xZ:
no dell2 artifact dated before 2024 is produced through the calendar until the fix lands).
LAST line: CALENDAR-REFUSAL refused=<n> of 3 calendar=<calendar_source()>
"""
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[8]
sys.path.insert(0, str(ROOT / "lib"))
import trading_calendar  # noqa: E402

SCRIPTS = [
    ["data/assets/scripts/silver/commonwealth_account_links.py", "--out", "{tmp}/links",
     "--cache", ".scratch/advi_cotbkf/tx_cache"],
    ["data/assets/scripts/analysis/commonwealth_price_census.py", "--out-dir", "{tmp}/census"],
    ["data/assets/scripts/analysis/commonwealth_price_need.py", "--out", "{tmp}/need"],
]
BOUND_S = 35


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        return run(tmp)


def run(tmp: str) -> int:
    refused = 0
    for raw in SCRIPTS:
        argv = [a.format(tmp=tmp) for a in raw]
        name = pathlib.Path(argv[0]).name
        try:
            r = subprocess.run([sys.executable] + argv, cwd=ROOT, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=BOUND_S)
        except subprocess.TimeoutExpired:
            print("%s: still running at %d s -> NOT refused" % (name, BOUND_S))
            continue
        lines = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.startswith("CALENDAR-UNCOVERED")]
        ok = r.returncode != 0 and bool(lines)
        refused += ok
        print("%s: rc=%d %s -> %s" % (name, r.returncode, lines[0] if lines else "(no CALENDAR-UNCOVERED line)",
                                      "refused" if ok else "NOT refused"))
    print("CALENDAR-REFUSAL refused=%d of 3 calendar=%s" % (refused, trading_calendar.calendar_source()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
