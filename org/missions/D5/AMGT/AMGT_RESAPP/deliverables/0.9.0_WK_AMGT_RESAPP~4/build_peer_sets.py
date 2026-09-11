"""
build_peer_sets.py -- AMGT_RESAPP.TO-AMGT-s-8's driver: calls
lib/research/peers/engine.py's peers() once per security_key AMGT-s-1
landed a model_block for, and writes each result to
peer_set_<security_key>.json beside this script.

No new Bloomberg call, no new security (F2/G-24): the three security_keys
below are exactly the three AMGT-s-1 already landed
(model_block_{BABA_US,BA_US,SAP_GY}_Equity.json); nothing else is read.

candidate_universe is not supplied -- at this cut no candidate pool has
been classified by GICS_SECTOR_NAME (a quota decision, F2, this cell does
not spend; see AMGT-s-8's cell text s.(c)) -- so every call below is
expected to, and does, return basis="absent".

Run: python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~4/build_peer_sets.py
"""
from __future__ import annotations

import json
import os
import sys

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = _THIS_DIR
for _ in range(7):
    _REPO_ROOT = os.path.dirname(_REPO_ROOT)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from lib.research.peers import engine  # noqa: E402

SECURITY_KEYS = ["BABA_US_Equity", "BA_US_Equity", "SAP_GY_Equity"]


def main() -> int:
    for security_key in SECURITY_KEYS:
        result = engine.peers(security_key)
        out_path = os.path.join(_THIS_DIR, "peer_set_%s.json" % security_key)
        with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(result, fh, indent=2, ensure_ascii=True)
            fh.write("\n")
        print(
            "%s: basis=%s members=%d reason=%s"
            % (security_key, result["basis"], len(result["members"]), result["reason"])
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
