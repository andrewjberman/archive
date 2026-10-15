"""AR-y-359 AC3: the one mutant that must fail. The amended driver's EMAIL is put back to the retired producer address in a
copy under the system temp directory (outside the product tree); the copy's own --selftest must FAIL.

Prints MUTANT-FIRES when the mutant's selftest exits non-zero and reports SELFTEST-BAD, else MUTANT-SURVIVES (exit 1).
Run: python <worktree>/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~156/mutant_check.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent / "0.9.0_WK_IRPT_ANLREQ~149" / "fwd1_driver"
DRIVER = FOLDER / "fwd1_driver.mjs"
MINT = FOLDER / "fwd1_mint.py"
GOOD_LINE = "const EMAIL = 'fwd1-staff-r41b@opal.invalid'"
MUTANT_LINE = "const EMAIL = 'fwd1-staff-r41a@opal.invalid'"


def main():
    text = DRIVER.read_bytes().decode("utf-8")
    hits = text.count(GOOD_LINE)
    if hits != 1:
        print("MUTANT-SURVIVES no-op: the amended EMAIL line occurs %d times (want 1)" % hits)
        return 1
    mutant_text = text.replace(GOOD_LINE, MUTANT_LINE)
    scratch = Path(tempfile.mkdtemp(prefix="ar359_mutant_"))
    try:
        (scratch / "fwd1_driver.mjs").write_bytes(mutant_text.encode("utf-8"))
        shutil.copyfile(str(MINT), str(scratch / "fwd1_mint.py"))
        node = shutil.which("node") or "node"
        p = subprocess.run([node, str(scratch / "fwd1_driver.mjs"), "--selftest"],
                           capture_output=True, timeout=120)
        out = p.stdout.decode("utf-8", "replace")
        tail = [ln for ln in out.splitlines() if ln.startswith("SELFTEST-")]
        deciding = tail[-1] if tail else "no SELFTEST line (rc=%d)" % p.returncode
        print("mutant rc=%d deciding: %s" % (p.returncode, deciding[:120]))
        if p.returncode != 0 and any(ln.startswith("SELFTEST-BAD") for ln in out.splitlines()):
            print("MUTANT-FIRES")
            return 0
        print("MUTANT-SURVIVES")
        return 1
    finally:
        shutil.rmtree(str(scratch), ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
