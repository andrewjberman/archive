"""AMGT_RESAPP round 46, AMGT-uu-3 AC2 -- THE PAGE AND THE EXPORT MOVE TOGETHER (FWD-30's seam, before the redeploy).

Over two pinned served captures (round46/checks/fixtures/captures: GOOGL_US_Equity, the raw-float name; RKT_LN_Equity, the
GBp minor-unit name; captured 2026-09-28T20:2xZ against CodeSha256 vBSCqd71...Mrew=): the page fixture's two case copies
(thesis.model.cases and thesis.model_cases -- both equal scoped_amgt._model_cases(block) at capture, measured) are REPLACED by
this tree's `scoped_amgt._model_cases(block)`; the rich export is REBUILT in process from this tree's code (round45's sweep
`rebuild`, every reader stubbed from the capture); then this tree's portal harness compares them. Expect, per name:
harness rc=0 and "CASES page=3 rich=3 same=3 missing=0 extra=0". Base: PASS (both sides unchanged move together); the
criterion guards that the page (ModelTab.tsx) and the export (render_pack.py) print the SAME new case line after the change.
usage: python <this>   (from the repo root; needs node and portal/node_modules)"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.getcwd())
ROOT = Path(os.getcwd())
CK = ROOT / "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z"
SWEEP = CK / "round45/checks/sweep.py"
CAP = CK / "round46/checks/fixtures/captures"
HARNESS = "src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs"


def main():
    spec = importlib.util.spec_from_file_location("sweep45", str(SWEEP))
    sw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sw)
    from lib.research.api import scoped_amgt as sa
    ok = 0
    keys = sorted(p.name for p in CAP.iterdir() if p.is_dir())
    with tempfile.TemporaryDirectory() as tmp:
        for key in keys:
            d = Path(tmp) / key
            shutil.copytree(CAP / key, d)
            fx = next((d / "served").glob("served_fixture.*.json"))
            block = json.loads((d / "model_block.json").read_text(encoding="utf-8"))
            bundle = json.loads(fx.read_text(encoding="utf-8"))
            cases = sa._model_cases(block)
            bundle["thesis"]["model"]["cases"] = cases
            bundle["thesis"]["model_cases"] = cases
            fx.write_text(json.dumps(bundle), encoding="utf-8")
            rich = d / "local.rich.md"
            err = sw.rebuild(key, str(fx), str(rich))
            if err:
                print("%s: REBUILD FAILED %s" % (key, err))
                continue
            p = subprocess.run(["node", HARNESS, "--fixture", str(fx), "--rich", str(rich)], cwd=str(ROOT / "portal"),
                               capture_output=True, text=True, encoding="utf-8", timeout=100)
            m = re.search(r"^CASES page=(\d+) \S+=(\d+) same=(\d+) missing=(\d+) extra=(\d+)", p.stdout, re.M)
            base_line = next((ln for ln in rich.read_text(encoding="utf-8").splitlines() if ln.lstrip("-* ").startswith("Base case:")), "")
            good = p.returncode == 0 and m is not None and m.groups()[2:] == ("3", "0", "0") and m.group(1) == "3"
            print("%s: harness rc=%s; %s; export %r" % (key, p.returncode, m.group(0) if m else "no CASES line: " + (p.stderr or p.stdout)[-160:], base_line[:90]))
            ok += good
    print("PAGE AND EXPORT PRINT THE SAME CASES: %d of %d names" % (ok, len(keys)))
    return 0 if keys and ok == len(keys) else 1


if __name__ == "__main__":
    sys.exit(main())
