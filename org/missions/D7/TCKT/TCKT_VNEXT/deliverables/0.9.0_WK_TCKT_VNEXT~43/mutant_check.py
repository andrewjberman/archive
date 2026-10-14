"""AC2 (TO TCKT_VNEXT.TO-R18-TR1): the one mutant that must fire.

Copies ATTACH_ADDRESS.json to a fresh folder OUTSIDE the worktree (a tempfile directory), changes key_template so that
{firm} appears twice, points address_check.py at the copy through ATTACH_ADDRESS_JSON, and prints MUTANT-FIRES only when
the checker prints ADDRESS-BAD with exit 1. Otherwise MUTANT-SURVIVES, exit 1. The unmutated record is checked first:
if it is not ADDRESS-OK the mutant result is meaningless and the script stops with BASELINE-BAD.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, "address_check.py")
RECORD = os.path.join(HERE, "ATTACH_ADDRESS.json")


def run_checker(record_path):
    env = dict(os.environ)
    env["ATTACH_ADDRESS_JSON"] = record_path
    proc = subprocess.run([sys.executable, CHECKER], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=env, timeout=110)
    return proc.returncode, proc.stdout.decode("utf-8", "replace").strip()


def main():
    rc, out = run_checker(RECORD)
    if rc != 0 or not out.startswith("ADDRESS-OK "):
        print("BASELINE-BAD unmutated record did not pass: rc=%d %s" % (rc, out))
        sys.exit(1)

    with open(RECORD, encoding="utf-8") as fh:
        rec = json.load(fh)
    rec["key_template"] = "portal/{firm}/{firm}/state/ticket-attachments/trade-form/"  # {firm} twice

    scratch = tempfile.mkdtemp(prefix="attach_mutant_")
    try:
        copy = os.path.join(scratch, "ATTACH_ADDRESS.json")
        with open(copy, "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1)
        rc, out = run_checker(copy)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    if rc == 1 and out.startswith("ADDRESS-BAD "):
        print("MUTANT-FIRES checker rc=1: " + out)
        sys.exit(0)
    print("MUTANT-SURVIVES checker rc=%d: %s" % (rc, out))
    sys.exit(1)


if __name__ == "__main__":
    main()
