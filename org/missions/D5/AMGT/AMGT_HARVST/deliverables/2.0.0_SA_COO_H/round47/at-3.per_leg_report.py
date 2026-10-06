"""Round 47 HVST-at-3: the per-leg report at the drain (CTO condition 4; CTO amendment 2 @69ce080222 on row Z-S89).

Per leg: job records of the collection run (`round46/as-1b.report.py`'s rule, plus the parallel sa root added 2026-10-06), jobs by
status, concluded keys out of the 191 pool keys AND out of the run's 234-name universe (HVST-at-5), how many of the 43 added names
concluded, the leg's stop reason from its checkpoint, and `chatter_axis.publisher_universe_verdicts` over the 191. Read-only:
local runtime files and one pool read. Writes `round47/at-3.per_leg_report.json`.
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
PUBS = ("sa", "barrons", "ft", "bbg", "wsj")
ROOTS = (".runtime/opal-data-harvest", ".runtime/opal-data-harvest-sa", ".runtime/opal-data-harvest-ft",
         ".runtime/opal-data-harvest-bbg", ".runtime/opal-data-harvest-wsj")
HB = os.path.join(ROOT, ".runtime", "harvest-backfill")
CHECKPOINTS = {"sa": ("r46_sa_barrons_checkpoint.json", "r47_sa_checkpoint.json"), "barrons": ("r46_sa_barrons_checkpoint.json",),
               "ft": ("r46_ft_checkpoint.json",), "bbg": ("r46_bbg_checkpoint.json",), "wsj": ("r46_wsj_checkpoint.json",)}
RUN_UNIVERSE = os.path.join(HERE, "rank_universe_20261005.json")
OUT = os.path.join(HERE, "at-3.per_leg_report.json")


def stop_reasons(pub):
    reasons = []
    for name in CHECKPOINTS[pub]:
        path = os.path.join(HB, name)
        if os.path.exists(path):
            stopped = json.load(open(path, encoding="utf-8")).get("stopped") or {}
            reasons.append("%s: %s" % (name, stopped.get(pub, "not stopped")))
        else:
            reasons.append("%s: ABSENT" % name)
    return reasons


def main():
    names, meta = chatter_axis.read_universe_names()
    pool = {n["security_key"] for n in names}
    run_doc = json.load(open(RUN_UNIVERSE, encoding="utf-8"))
    run = {e["security_key"] for e in run_doc["entries"]}
    added = run - pool
    records, seen = [], set()
    for root in ROOTS:
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
    verdicts = chatter_axis.publisher_universe_verdicts(records, PUBS, sorted(pool))
    print("pool universe %d (%s); run universe %d (+%d added by at-5); job records of this run %d"
          % (len(pool), meta.get("source"), len(run), len(added), len(records)))
    report = {"pool_universe": len(pool), "run_universe": len(run), "added": len(added), "job_records": len(records), "legs": {}}
    for pub in PUBS:
        c = concluded[pub]
        row = {"concluded_of_191": len(c & pool), "concluded_of_234": len(c & run), "concluded_of_added_43": len(c & added),
               "statuses": dict(by_pub[pub]), "stop": stop_reasons(pub),
               "verdict": {"in": verdicts[pub][0], "reason": verdicts[pub][1]}}
        report["legs"][pub] = row
        print("%-8s concluded %3d of 191, %3d of 234 (added %2d of 43); statuses %s" % (
            pub, row["concluded_of_191"], row["concluded_of_234"], row["concluded_of_added_43"], row["statuses"]))
        print("         stop: %s" % "; ".join(row["stop"]))
        print("         VERDICT %s  %s" % ("IN" if verdicts[pub][0] else "out", verdicts[pub][1]))
    declared = [p for p, (inside, _r) in verdicts.items() if inside]
    report["declared_set"] = declared
    print("DECLARED SET: %s" % (declared or "EMPTY"))
    json.dump(report, open(OUT, "w", encoding="utf-8"), indent=1)
    print("RECORD: %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
