"""AMGT_CORPUS round 37 -- capture the am-3 fixture from the REAL read path (issuer's file, run once at the cut).

TSM_US_Equity (mixed block: quote USD, reporting TWD; some money figures already carry a currency, most do not) and
1299_HK_Equity (non-December FYE: showing rows with served per-year reasons for their gap years). Records what the Model tab is
handed: `scoped_amgt.read_model`'s fiscal_year_figures / fiscal_years / forecast_figures / fiscal_unresolved, plus the block's
header-scope figures. Writes am3_fixture.json beside this file. Reads S3 only.
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
for key in ("TSM_US_Equity", "1299_HK_Equity"):
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
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "am3_fixture.json")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, indent=1, sort_keys=True, ensure_ascii=True)
    fh.write("\n")
print("wrote", path)
