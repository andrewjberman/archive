"""AMGT_CORPUS round 40, CRPS-ap-7 -- the six consensus-dispersion mnemonics ride the model-block pull (round-39 analysis
ruling 10). Issuer's file. Read-only, offline: it imports the pull module and reads its constants. NO Bloomberg call.

  python ap7_check.py        (from the repository root, PYTHONPATH=.)

Prints `ap7 build <b>/1 control <c>/2`, then the calls-per-name line.
  build    AMENDMENT 1 (CTO ruling msg 31086 on the one-name probe, evidence/r40_ap10_probe_BA_20261007.txt): each of the
           FOUR dispersion fields Bloomberg returns (BEST_CPS_STDDEV, BEST_CPS_NUMEST, BEST_EPS_STDDEV, BEST_EPS_NUMEST) is
           in `model_block_pull.FORECAST_FIELDS` exactly once, and NONE of the four names Bloomberg refused as
           BAD_FLD/INVALID_FIELD (BEST_CPS_STANDARD_DEV, BEST_CPS_AVG, BEST_EPS_STANDARD_DEV, BEST_EPS_AVG) is in any field
           list. The mean is BEST_CPS / BEST_EPS, already pulled.
  control  c1  the twelve forecast fields of round 39 are still the first twelve, in the same order;
           c2  the Bloomberg calls per name are still 8: 1 header call + the history chunk count + one call per forecast
               override (so 96 names stay at 768 calls per fire).
"""
import importlib.util
import math
import os
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
for p in (TOP, RES):
    if p not in sys.path:
        sys.path.insert(0, p)
spec = importlib.util.spec_from_file_location("mbp_ap7", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)

ROUND39_FORECAST = [
    "BEST_EPS", "BEST_SALES", "BEST_EBITDA", "BEST_PE_RATIO", "BEST_DPS", "BEST_DIV_YLD", "BEST_EBIT", "BEST_NET_INCOME",
    "BEST_CAPEX", "BEST_ESTIMATE_FCF", "BEST_BPS", "BEST_CPS",
]
four = ["BEST_CPS_STDDEV", "BEST_CPS_NUMEST", "BEST_EPS_STDDEV", "BEST_EPS_NUMEST"]
refused = ["BEST_CPS_STANDARD_DEV", "BEST_CPS_AVG", "BEST_EPS_STANDARD_DEV", "BEST_EPS_AVG"]
fields = list(mbp.FORECAST_FIELDS)
missing = [f for f in four if fields.count(f) != 1]
every_list = list(mbp.HEADER_FIELDS) + list(mbp.HIST_FIELDS) + fields
still_there = [f for f in refused if f in every_list]
build = 1 if (not missing and not still_there) else 0
c1 = 1 if fields[:12] == ROUND39_FORECAST else 0
calls = 1 + math.ceil(len(mbp.HIST_FIELDS) / float(mbp.HIST_FIELDS_PER_REQUEST)) + len(mbp.FORECAST_OVERRIDES)
c2 = 1 if calls == 8 else 0
print("four %s" % ",".join(four))
print("refused_names_still_listed %s" % (",".join(still_there) if still_there else "none"))
print("missing_or_repeated %s" % (",".join(missing) if missing else "none"))
print("calls_per_name %d forecast_fields %d (96 names: %d calls per fire)" % (calls, len(fields), 96 * calls))
print("ap7 build %d/1 control %d/2" % (build, c1 + c2))
sys.exit(0)
