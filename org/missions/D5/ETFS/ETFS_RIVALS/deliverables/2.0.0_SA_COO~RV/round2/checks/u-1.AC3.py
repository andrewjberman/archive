"""RIV-u-1 AC3 -- the round-1 stages read the universe, not a ticker literal, and BASG's round-1 behaviour is unchanged:
no 'BASG' string literal remains in gold_canonical_shape.py, gold_trade_schedule.py or publish_page.py, and the round-1
checks s-1.AC1, g-1.AC1, g-2.AC1 and p-1.AC1 still PASS in this tree."""
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

R1 = pathlib.Path(__file__).resolve().parents[2] / "round1" / "checks"


def run(v):
    root = c.setup_path()
    pkg = root / "data" / "etfs" / "scripts" / "rivalfunds"
    for f in ["gold_canonical_shape.py", "gold_trade_schedule.py", "publish_page.py"]:
        txt = (pkg / f).read_text(encoding="utf-8")
        lits = re.findall(r"""['"]BASG['"]""", txt)
        v.check(not lits, f"{f}: no BASG string literal ({len(lits)} found)")
    for chk in ["s-1.AC1", "g-1.AC1", "g-2.AC1", "p-1.AC1"]:
        out = subprocess.run([sys.executable, str(R1 / f"{chk}.py")], capture_output=True, text=True, cwd=root, timeout=900)
        last = (out.stdout.strip().splitlines() or ["<no output>"])[-1]
        v.check(out.returncode == 0 and "PASS 0 failures" in last, f"round-1 {chk}: {last}")


failures = c.guarded("AC3", run)
if failures == 0:
    print("AC3 RESULT: PASS 0 failures")
else:
    print(f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
