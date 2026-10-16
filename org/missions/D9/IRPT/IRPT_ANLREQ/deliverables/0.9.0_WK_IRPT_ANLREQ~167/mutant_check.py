"""AR-y-373 mutant check (0.9.0_WK_IRPT_ANLREQ~167): the one mutant that must fail.

Copies the edited helper to a scratch folder OUTSIDE the product tree (a system temp folder), loosens readback_ok so a
row with NO allowedFirmIds is accepted, runs test_fwd1_mint.py against that copy (FWD1_MINT_PATH), and prints
MUTANT-FIRES only when that run FAILS. Otherwise MUTANT-SURVIVES and exit 1. No AWS, no network.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HELPER = os.path.normpath(os.path.join(HERE, "..", "0.9.0_WK_IRPT_ANLREQ~149", "fwd1_driver", "fwd1_mint.py"))
TESTS = os.path.join(HERE, "test_fwd1_mint.py")
ANCHOR = 'and row.get("allowedFirmIds") == {"L": [{"S": RUN_FIRM}]}'
MUTANT = 'and ("allowedFirmIds" not in row or row.get("allowedFirmIds") == {"L": [{"S": RUN_FIRM}]})'


def main():
    with open(HELPER, encoding="utf-8") as fh:
        src = fh.read()
    n = src.count(ANCHOR)
    if n != 1:
        print("MUTANT-SURVIVES anchor found " + str(n) + " times, expected 1; the mutant was not applied")
        return 1
    mutated = src.replace(ANCHOR, MUTANT)
    scratch = tempfile.mkdtemp(prefix="fwd1_mint_mutant_")
    copy_path = os.path.join(scratch, "fwd1_mint.py")
    try:
        with open(copy_path, "w", encoding="utf-8") as fh:
            fh.write(mutated)
        env = dict(os.environ, FWD1_MINT_PATH=copy_path)
        run = subprocess.run([sys.executable, TESTS], env=env, capture_output=True, text=True, timeout=120)
    except Exception as e:  # noqa: BLE001
        print("MUTANT-SURVIVES run error " + type(e).__name__)
        return 1
    finally:
        try:
            os.remove(copy_path)
            os.rmdir(scratch)
        except OSError:
            pass
    first = (run.stdout or "").strip().splitlines()[:1]
    if run.returncode != 0:
        print("MUTANT-FIRES readback_ok admits a row with no allowedFirmIds; test rc=" + str(run.returncode)
              + " " + (first[0] if first else ""))
        return 0
    print("MUTANT-SURVIVES the tests passed on the mutant; rc=" + str(run.returncode))
    return 1


if __name__ == "__main__":
    sys.exit(main())
