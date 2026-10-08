"""AMGT_CORPUS round 40, CRPS-ap-7 AMENDMENT 2 -- each model-block fire records its Bloomberg draw in the shared budget ledger
(1.0.0_SA_CTO~Z rulings msg 31290 and msg 31295). Issuer's file. Offline: the ledger directory is a temp directory named by
RIVALFUNDS_BBG_BUDGET_DIR, so the Terminal machine's real ledger is never written. NO Bloomberg call, NO S3 call.

  python ap7_budget_check.py        (from the repository root, PYTHONPATH=.)

Prints `ap7b build <b>/2 control <c>/2`.
  build    b1  `model_block_pull.record_fire_budget(calls=768, security_fields=13824, figures=66879, records=4224,
               stamp="20261007T130000Z")`
               appends ONE line to the day's ledger through `bbg_budget.record`: mode "amgt-model-block", rows 4224 (RETURNED
               RECORDS, the ledger's one unit: CTO ruling msg 31815, AMENDMENT 3; a line of 66879 figures would tell every
               later leg that 56 percent of the day is gone when 3.5 percent is), and a batch_id that carries calls=768,
               security_fields=13824, figures=66879, records=4224 and `rows_unit=returned-records`;
           b2  `bbg_budget.spent()` for today then reads 4224 more than before.
  control  c1  with the ledger directory unwritable (a path under a FILE), the call returns False and raises nothing: a fire is
               never blocked by bookkeeping;
           c2  the Bloomberg calls per name are still 8 (the amendment adds no request).
"""
import importlib.util
import json
import math
import os
import subprocess
import sys
import tempfile

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
for p in (TOP, RES):
    if p not in sys.path:
        sys.path.insert(0, p)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tmp = tempfile.mkdtemp(prefix="ap7b_")
os.environ["RIVALFUNDS_BBG_BUDGET_DIR"] = tmp
os.environ.pop("PYTEST_CURRENT_TEST", None)
mbp = load("mbp_ap7b", os.path.join(RES, "model_block_pull.py"))
budget = load("bbg_budget_ap7b", os.path.join(TOP, "data", "etfs", "scripts", "rivalfunds", "bbg_budget.py"))

fn = getattr(mbp, "record_fire_budget", None)
b1 = b2 = c1 = 0
before = budget.spent()
detail = "record_fire_budget is not defined"
if callable(fn):
    try:
        ok = fn(calls=768, security_fields=13824, figures=66879, records=4224, stamp="20261007T130000Z")
        files = sorted(f for f in os.listdir(tmp) if f.endswith(".jsonl"))
        lines = []
        for f in files:
            with open(os.path.join(tmp, f), encoding="utf-8") as fh:
                lines.extend(json.loads(x) for x in fh if x.strip())
        detail = "returned %r; ledger files %d; lines %d: %s" % (ok, len(files), len(lines), json.dumps(lines)[:300])
        if ok is True and len(lines) == 1:
            line = lines[0]
            bid = str(line.get("batch_id", ""))
            b1 = 1 if (line.get("mode") == "amgt-model-block" and line.get("rows") == 4224 and "calls=768" in bid
                       and "security_fields=13824" in bid and "figures=66879" in bid and "records=4224" in bid
                       and "rows_unit=returned-records" in bid) else 0
        b2 = 1 if budget.spent() - before == 4224 else 0
    except Exception as exc:
        detail = "raised %s: %s" % (type(exc).__name__, exc)
    blocker = os.path.join(tmp, "a_file")
    with open(blocker, "w", encoding="utf-8") as fh:
        fh.write("x")
    os.environ["RIVALFUNDS_BBG_BUDGET_DIR"] = os.path.join(blocker, "under_a_file")
    try:
        c1 = 1 if fn(calls=1, security_fields=1, figures=1, records=1, stamp="20261007T130001Z") is False else 0
    except Exception as exc:
        detail += " | unwritable ledger raised %s" % type(exc).__name__
calls = 1 + math.ceil(len(mbp.HIST_FIELDS) / float(mbp.HIST_FIELDS_PER_REQUEST)) + len(mbp.FORECAST_OVERRIDES)
c2 = 1 if calls == 8 else 0
print(detail)
print("ap7b build %d/2 control %d/2" % (b1 + b2, c1 + c2))
sys.exit(0)
