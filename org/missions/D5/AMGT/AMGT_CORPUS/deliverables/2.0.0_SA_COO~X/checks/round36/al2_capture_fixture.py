"""AMGT_CORPUS round 36 -- capture the al-2 fixture from the REAL read path (issuer's file, run once at the cut).

For BA_US_Equity (December FYE, few gaps) and 1299_HK_Equity (non-December FYE: whole V3 rows unresolved with a reason), it
records what the Model tab is handed: `scoped_amgt.read_model`'s fiscal_year_figures / fiscal_years / forecast_figures, the
block's header-scope figures, and the block's fiscal-scope `unresolved` entries (the list CRPS-al-1 serves as
`fiscal_unresolved`). Writes al2_fixture.json beside this file. Reads S3 only.
"""
import json
import os
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, TOP)
from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.checkface.scopes import SCOPE_FISCAL_YEAR_LINE_ITEM, SCOPE_HEADER  # noqa: E402

out = {}
for key in ("BA_US_Equity", "1299_HK_Equity"):
    block = scoped_amgt.read_model_block(key)
    model = scoped_amgt.read_model(key, model_block=block)
    out[key] = {
        "fiscal_year_figures": model["fiscal_year_figures"],
        "fiscal_years": model["fiscal_years"],
        "forecast_figures": model["forecast_figures"],
        "header_figures": [f for f in block.get("figures", []) if f.get("scope") == SCOPE_HEADER],
        "fiscal_unresolved": [
            {"mnemonic": u.get("mnemonic"), "fiscal_year": u.get("fiscal_year"), "reason": u.get("reason")}
            for u in block.get("unresolved", [])
            if u.get("scope") == SCOPE_FISCAL_YEAR_LINE_ITEM
        ],
        "block_raw_stamp": block.get("raw_stamp_used"),
    }
    print("captured %s fiscal %d forecast %d header %d fiscal_unresolved %d"
          % (key, len(out[key]["fiscal_year_figures"]), len(out[key]["forecast_figures"]),
             len(out[key]["header_figures"]), len(out[key]["fiscal_unresolved"])))
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "al2_fixture.json")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, indent=1, sort_keys=True, ensure_ascii=True)
    fh.write("\n")
print("wrote", path)
