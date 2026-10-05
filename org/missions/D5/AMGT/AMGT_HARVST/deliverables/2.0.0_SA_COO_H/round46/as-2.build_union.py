"""Round 46 HVST-as-2: the `chatter_window` build list = the served list UNION the rank universe UNION RESAPP's covered set.

- served list: `round33/securities.universe.r33.json`, the 212 names the served table was built from (GONE 0 by construction);
- rank universe: `chatter_axis.read_universe_names()` (pool `universe/v1/<newest>.json`, 191);
- RESAPP covered set: `covered_universe.covered_security_keys()` (95, round-67 ruling 2 @2db6fd3e3d).
Writes `round46/securities.union.r46.json` (the r33 entry shape; `window_tone.build_window` reads `security_key`) and prints the
denominators. Read-only on S3.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 8)))
sys.path.insert(0, ROOT)

from lib.research.coverage import covered_universe  # noqa: E402
from lib.research.metrics import chatter_axis  # noqa: E402

OUT = os.path.join(HERE, "securities.union.r46.json")


def main():
    served = json.load(open(os.path.join(DELIV, "round33", "securities.universe.r33.json"), encoding="utf-8"))
    rank, meta = chatter_axis.read_universe_names()
    covered = covered_universe.covered_security_keys()
    by_key = {s["security_key"]: s for s in served}
    rank_by_key = {n["security_key"]: n for n in rank}
    union = dict(by_key)
    for key in sorted(set(rank_by_key) | set(covered)):
        if key in union:
            continue
        n = rank_by_key.get(key, {})
        union[key] = {"aliases": [], "company": n.get("name"), "composite_figi": None, "key": key, "security_key": key,
                      "ticker": n.get("ticker"), "ticker_aliases": []}
    out = [union[k] for k in sorted(union)]
    json.dump(out, open(OUT, "w", encoding="utf-8", newline="\n"), indent=1)
    s, r, c = set(by_key), set(rank_by_key), set(covered)
    print("served %d; rank %d (%s); covered %d" % (len(s), len(r), meta.get("source"), len(c)))
    print("rank not served %d; covered not served %d (%s)" % (len(r - s), len(c - s), ", ".join(sorted(c - s))))
    print("served not in rank|covered %d (kept: GONE 0)" % len(s - (r | c)))
    print("UNION %d -> %s" % (len(out), OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
