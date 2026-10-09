"""TO-DB-b-69 (S32), SUPPLEMENTARY to DB-b-43's own pytest run (which is the recorded result): the same four test bodies on the kit, with
the module's run() never switching `future.infer_string` on -- the served runtime's setting (pandas 2.2.3, option off). It is NOT the
DB-b-43 test (that test forces the option ON); it measures only whether the producer's classify_and_sum itself passes the four assertions
on the kit when the option stays at the kit's default.

Usage (worktree root, kit python): python <this file>
"""
import importlib.util
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[7]
TEST = ROOT / "data/assets/scripts/gold/irpt_reporting/tests/test_account_return_daily_none.py"
spec = importlib.util.spec_from_file_location("t43", TEST)
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
t.pd.set_option = lambda *a, **k: None          # leave the option exactly as the kit has it
opt = pd.get_option("future.infer_string")
res = {"pandas": pd.__version__, "future.infer_string": opt, "passed": 0, "failed": 0, "failures": []}
for name in sorted(n for n in dir(t) if n.startswith("test_")):
    try:
        getattr(t, name)()
        res["passed"] += 1
    except Exception as exc:  # noqa: BLE001
        res["failed"] += 1
        res["failures"].append("%s: %s: %s" % (name, type(exc).__name__, str(exc)[:100]))
print(json.dumps(res, indent=1))
sys.exit(0)
