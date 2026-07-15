"""OPAL_BBGTML /bbg-pull -- one-command daily Bloomberg pull (leg 1) + tripwire (leg 2).

Runs Yang's two notebooks headlessly on THIS machine (the Bloomberg Terminal must be
running and logged in -- the pull uses the terminal's own entitlement, exactly like
clicking through the notebooks by hand), then validates the two output PKLs with the
leg-2 tripwire. On PASS, the files are already syncing to SharePoint via OneDrive and
are ready for /bbg-send.

The notebooks are UNTOUCHED -- this wraps them. Both are idempotent by date: if
today's PKL already exists they load it instead of re-downloading, so re-running
this after a partial failure is safe.

Usage:
    python run_daily_pull.py [--skip-pull] [--allow-stale N]
        --skip-pull      only run the tripwire (files already produced today)
        --allow-stale N  pass through to the tripwire (US-holiday mornings)

Lives in <project>/tools/ ; the project root is the parent of this file's folder.
No non-ASCII in output (CLAUDE.md code-quality rule).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
NOTEBOOKS = [
    "market_indices_data_pull.ipynb",
    "model_portfolio_regression_analysis.ipynb",
]


def run_notebook(name: str) -> None:
    """Execute a notebook in place with the current env's kernel. cwd=src so the
    notebooks' own `dir_wkdir = dirname(realpath('.'))` resolves to the project root
    (that is how they find input/ and output/)."""
    path = os.path.join(SRC_DIR, name)
    if not os.path.exists(path):
        raise SystemExit(f"ERROR: notebook not found: {path}")
    print(f"RUN:  {name} (this calls the Bloomberg Terminal; minutes, not seconds)")
    t0 = time.time()
    cmd = [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook", "--execute", "--inplace",
        "--ExecutePreprocessor.timeout=3600",
        "--ExecutePreprocessor.kernel_name=python3",
        path,
    ]
    proc = subprocess.run(cmd, cwd=SRC_DIR)
    if proc.returncode != 0:
        raise SystemExit(
            f"ERROR: {name} failed (exit {proc.returncode}). Common causes: Bloomberg "
            "Terminal not running/not logged in; the 'tia' package missing from this "
            "env; a template path issue. Open the notebook in Jupyter to see the cell error."
        )
    print(f"OK:   {name} completed in {time.time() - t0:.0f}s")


def main() -> int:
    ap = argparse.ArgumentParser(description="OPAL_BBGTML daily pull runner")
    ap.add_argument("--skip-pull", action="store_true", help="tripwire only")
    ap.add_argument("--allow-stale", type=int, default=0)
    args = ap.parse_args()

    print("OPAL_BBGTML daily pull")
    print(f"  project: {PROJECT_ROOT}")

    if not args.skip_pull:
        for nb in NOTEBOOKS:
            run_notebook(nb)
    else:
        print("SKIP: pull skipped (--skip-pull); running tripwire only")

    print()
    print("TRIPWIRE (leg 2):")
    trip = os.path.join(TOOLS_DIR, "bbg_pkl_tripwire.py")
    cmd = [sys.executable, trip, OUTPUT_DIR]
    if args.allow_stale:
        cmd += ["--allow-stale", str(args.allow_stale)]
    rc = subprocess.run(cmd).returncode
    if rc != 0:
        print()
        print("STOP: tripwire FAILED -- do not send. Fix or rerun, then run this again.")
        return rc

    print()
    print("NEXT: the PKLs are syncing to SharePoint via OneDrive (give it a minute if")
    print("      you just ran the pull). Then in Claude, run the /bbg-send skill to")
    print("      push them through the portal /data-refresh channel and confirm display.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
