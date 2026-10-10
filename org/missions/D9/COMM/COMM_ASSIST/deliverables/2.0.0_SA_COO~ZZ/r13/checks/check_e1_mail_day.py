"""COMM_ASSIST round 13, criterion CAe1-AC1 (issuer's check; the worker reads it and never edits it).

FWD-4 EXERCISED: the round-12 reader `d2_mail_day.py` reports texted_ok>=1 for the UTC day named by --day (the day the driven
mail was sent). Counts log lines only; never reads mail content.

    python org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~ZZ/r13/checks/check_e1_mail_day.py --day YYYY-MM-DD

LAST line: `E1-TEXTED day=<day> texted_ok=<n> ok=<True|False>`. At the base (no driven mail sent) it prints ok=False.
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
READER = os.path.normpath(os.path.join(HERE, "..", "..", "r12", "checks", "d2_mail_day.py"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", required=True)
    day = ap.parse_args().day
    proc = subprocess.run([sys.executable, READER, "--day", day], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=110)
    out = proc.stdout or ""
    for line in out.splitlines():
        if line.startswith("MAIL"):
            print(line)
    m = re.search(r"MAIL-CLOSE day=\S+ texted_ok=(\d+)", out)
    n = int(m.group(1)) if m else -1
    if not m:
        print("ERROR: the reader printed no MAIL-CLOSE line (rc=%d): %s" % (proc.returncode, (proc.stderr or "")[-300:]))
    print("E1-TEXTED day=%s texted_ok=%d ok=%s" % (day, n, n >= 1))


if __name__ == "__main__":
    main()
