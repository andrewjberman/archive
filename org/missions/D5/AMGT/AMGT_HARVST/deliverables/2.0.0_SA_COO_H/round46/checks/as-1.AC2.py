"""Round 46 HVST-as-1 AC2: the collector's universe resolves the RANK's universe 191/191 to the declared-set join key.

The declared-set reader (`chatter_axis.publisher_universe_verdicts`) joins each concluded job on `gold_security_key`, which
`worker.run_job` stamps from the collector security's `security_key` (worker.py:467). So: every security that
`lib.opal_data_harvest.__main__.universe(<shipped config>)` returns must carry a `security_key`, and the set of those keys must
EQUAL the rank's universe (`chatter_axis.read_universe_names()`, pool `universe/v1/<newest>.json`). Also printed (informational):
per search identity, how many of the 191 carry it. Read-only: one pool read, no vendor call. Prints `AC2 RESULT: PASS|FAIL`.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
sys.path.insert(0, ROOT)

from lib.opal_data_harvest import __main__ as collector  # noqa: E402
from lib.research.metrics import chatter_axis  # noqa: E402


def main():
    config = json.load(open(os.path.join(ROOT, "lib", "opal_data_harvest", "config.json"), encoding="utf-8"))
    rank_names, meta = chatter_axis.read_universe_names()
    rank = {n["security_key"] for n in rank_names}
    try:
        secs = collector.universe(config)
    except Exception as exc:  # noqa: BLE001 -- a universe that cannot load is a FAIL, printed
        print("AC2: collector universe raised %s: %s" % (type(exc).__name__, exc))
        print("AC2 RESULT: FAIL")
        return 1
    keys = [s.get("security_key") for s in secs]
    have = {k for k in keys if k}
    print("AC2 rank universe: %d names (%s)" % (len(rank), meta.get("source")))
    print("AC2 collector universe: %d securities; with security_key %d; distinct %d" % (len(secs), len([k for k in keys if k]), len(have)))
    print("AC2 rank names resolved: %d of %d; missing %d; extra %d" % (len(rank & have), len(rank), len(rank - have), len(have - rank)))
    for k in sorted(rank - have)[:20]:
        print("  missing " + k)
    for field in ("company", "ticker", "sa_symbol"):
        print("AC2 identity %s present: %d of %d" % (field, sum(1 for s in secs if s.get(field)), len(secs)))
    ok = rank == have and len(keys) == len(have) and len(secs) == len(rank)
    print("AC2 RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
