"""Round 46 HVST-as-1b report (CTO condition 4): per leg, concluded jobs of THIS run out of 191, and the declared-set verdicts
from `chatter_axis.publisher_universe_verdicts` over this run's job records. Read-only (local runtime files + one pool read).

A job record of this run is `<runtime root>/runs/<job_id>.json` with `started_at` at or after the launch (01:44:37Z). Each is
passed to the verdict function as one run record `{started_at, jobs: [record]}` (the function unions jobs across records).
"""

import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 8)))
sys.path.insert(0, ROOT)

from lib.research.harvest.publication_gold import SUCCESSFUL_RUN_STATUSES  # noqa: E402
from lib.research.metrics import chatter_axis  # noqa: E402

LAUNCH = "2026-10-05T01:44:37"
ROOTS = {"sa": ".runtime/opal-data-harvest", "barrons": ".runtime/opal-data-harvest", "ft": ".runtime/opal-data-harvest-ft",
         "bbg": ".runtime/opal-data-harvest-bbg", "wsj": ".runtime/opal-data-harvest-wsj"}


def main():
    names, meta = chatter_axis.read_universe_names()
    universe = [n["security_key"] for n in names]
    records, seen = [], set()
    for root in sorted(set(ROOTS.values())):
        for f in glob.glob(os.path.join(ROOT, root, "runs", "*.json")):
            try:
                r = json.load(open(f, encoding="utf-8"))
            except ValueError:
                continue
            if str(r.get("started_at") or "") < LAUNCH or r.get("job_id") in seen:
                continue
            seen.add(r.get("job_id"))
            records.append({"started_at": r.get("started_at"), "jobs": [r]})
    by_pub = collections.defaultdict(collections.Counter)
    concluded = collections.defaultdict(set)
    for rec in records:
        j = rec["jobs"][0]
        by_pub[j.get("publisher")][j.get("status")] += 1
        if j.get("status") in SUCCESSFUL_RUN_STATUSES:
            concluded[j.get("publisher")].add(j.get("gold_security_key"))
    print("universe %d (%s); job records of this run %d" % (len(universe), meta.get("source"), len(records)))
    for pub in ("sa", "barrons", "ft", "bbg", "wsj"):
        print("%-8s concluded %3d of %d; statuses %s" % (pub, len(concluded[pub] & set(universe)), len(universe), dict(by_pub[pub])))
    verdicts = chatter_axis.publisher_universe_verdicts(records, ("sa", "barrons", "ft", "bbg", "wsj"), universe)
    for pub, (inside, reason) in verdicts.items():
        print("VERDICT %-8s %s  %s" % (pub, "IN" if inside else "out", reason))
    declared = [p for p, (inside, _r) in verdicts.items() if inside]
    print("DECLARED SET: %s" % (declared or "EMPTY"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
