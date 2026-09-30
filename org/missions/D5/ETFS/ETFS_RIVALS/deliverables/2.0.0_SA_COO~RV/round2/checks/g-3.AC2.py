"""RIV-g-3 AC2 -- round 1's BASG canonical output is unchanged apart from the new columns: round-1 checks g-1.AC1 and
p-1.AC1 still PASS in this tree, and the round-2 u-1.AC3 regression (no BASG literal; s-1/g-1/g-2/p-1) still PASSES."""
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
R1 = HERE.parents[1] / "round1" / "checks"


def run(v):
    root = c.setup_path()
    for script in [R1 / "g-1.AC1.py", R1 / "p-1.AC1.py", HERE / "u-1.AC3.py"]:
        out = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, cwd=root, timeout=1800)
        last = (out.stdout.strip().splitlines() or ["<no output>"])[-1]
        v.check(out.returncode == 0 and "PASS 0 failures" in last, f"{script.parent.parent.name}/{script.name}: {last}")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
