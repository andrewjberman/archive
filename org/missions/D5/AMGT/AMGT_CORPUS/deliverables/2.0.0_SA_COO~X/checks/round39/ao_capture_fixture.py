"""AMGT_CORPUS round 39 -- capture the ao-3/ao-4 fixture from the REAL read path (issuer's file, run once at the cut).

TSM_US_Equity (mixed block: quote USD, reporting TWD; EPS/DPS/P-E forecasts with no served history; EV unit unresolved; net
debt and EV currency UNMEASURED), BA_US_Equity (the control: a resolved EV with its currency) and ASML_NA_Equity (FWD-21's
second clipped name). Records what the Model tab is handed, as round 37's am3_capture_fixture.py did. Reads S3 only.
"""
import json
import os
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, TOP)
from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.checkface.scopes import SCOPE_HEADER  # noqa: E402

out = {}
for key in ("TSM_US_Equity", "BA_US_Equity", "ASML_NA_Equity"):
    block = scoped_amgt.read_model_block(key)
    model = scoped_amgt.read_model(key, model_block=block)
    out[key] = {
        "fiscal_year_figures": model["fiscal_year_figures"],
        "fiscal_years": model["fiscal_years"],
        "forecast_figures": model["forecast_figures"],
        "fiscal_unresolved": model["fiscal_unresolved"],
        "header_figures": [f for f in block.get("figures", []) if f.get("scope") == SCOPE_HEADER],
        "currencies": block.get("currencies"),
    }
    print("captured %s fiscal %d forecast %d header %d fiscal_unresolved %d currencies %s"
          % (key, len(out[key]["fiscal_year_figures"]), len(out[key]["forecast_figures"]), len(out[key]["header_figures"]),
             len(out[key]["fiscal_unresolved"]), json.dumps(out[key]["currencies"])))
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ao_fixture.json")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, indent=1, sort_keys=True, ensure_ascii=True)
    fh.write("\n")
print("wrote", path)
