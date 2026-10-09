"""LGIC_ENFORCE round 20 -- the issuer's close run of FWD-5 (2.0.0_SA_COO~B1), disarming row LGIC_ENFORCE-D1-W1-S1.

The r20 census (EN-z-1) carried round 13's cards forward. A card holds a name only while grade() RAISES on it; 121 of the
carried entries now read. This run keeps a card only if some item it matches, at its own type, still RAISES; every other
card is dropped so its name is judged and ranked. Then it runs the real census with the pruned list.

Run from the repo root: python <this file>
Writes, beside this file: NOT_JUDGED_R20_CLOSE.json, NAMING_CENSUS_REPORT.r20.close.md, CLOSE_CENSUS_R20.json.
"""
import json
import os
import re
import sys

sys.path.insert(0, "lib")
import opal_naming as on  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NOT_JUDGED_R20.json"
REL = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~B1/r20_close/"


def main():
    cards = json.load(open(SRC, encoding="utf-8"))
    v, schema = on._vocab(), on._schema()
    nodes, vintage, _ = on.census_live(600)
    items = [{"plane": "live", "type": nd["type"], "current": nd["name"]} for nd in nodes
             if nd["type"] not in v.not_graded and not on._aws_fixed(nd["type"], nd["name"], nd["arn"], schema)]
    ritems, _ = on.census_repo()
    items += ritems
    raises = set()
    matched = set()
    for it in items:
        key = (it["plane"], it["current"])
        matched.add(key)
        try:
            on.grade(it["current"], it["type"])
        except on.RaiseDefect:
            raises.add(key)
    kept, dropped, unmatched = [], [], []
    for c in cards:
        key = (c.get("plane"), c.get("name"))
        if key in raises:
            kept.append(c)
        elif key in matched:
            dropped.append(c)
        else:
            unmatched.append(c)
    # a card matching no item this run holds nothing; keep it (inert) so the list stays a superset of the live need
    pruned = kept + unmatched
    nj_path = os.path.join(HERE, "NOT_JUDGED_R20_CLOSE.json")
    with open(nj_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(pruned, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    report = os.path.join(HERE, "NAMING_CENSUS_REPORT.r20.close.md")
    lines = []
    rc = on.census(live=True, repo=True, report=report, budget=600, not_judged_file=nj_path, out=lines.append)
    doc = json.loads(re.search(r"```json\n(.*?)\n```", open(report, encoding="utf-8").read(), re.S).group(1))
    den = doc["denominators"]
    verdicts = {}
    for r in doc["rows"]:
        k = "%s:%s" % (r["plane"], r["verdict"])
        verdicts[k] = verdicts.get(k, 0) + 1
    rec = {"claim": "measured", "builder": REL + "build_close_census_r20.py", "rc": rc, "last_line": lines[-1],
           "vintage": doc["vintage"], "cards_in": len(cards), "cards_kept_raising": len(kept),
           "cards_dropped_now_readable": len(dropped), "cards_matching_no_item": len(unmatched),
           "dropped_names": sorted(set("%s:%s" % (c.get("plane"), c.get("name")) for c in dropped)),
           "denominators": den, "verdicts": dict(sorted(verdicts.items())),
           "disarms": "LGIC_ENFORCE-D1-W1-S1"}
    with open(os.path.join(HERE, "CLOSE_CENSUS_R20.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print("cards in=%d kept=%d dropped=%d unmatched=%d" % (len(cards), len(kept), len(dropped), len(unmatched)))
    print("live=%d nameable=%d judged_live=%d carded_live=%d repo=%d judged_repo=%d carded_repo=%d" % (
        den["live"], den["live_nameable"], den["judged_live"], den["carded_live"], den["repo"], den["judged_repo"],
        den["carded_repo"]))
    print(lines[-1])
    return rc


if __name__ == "__main__":
    sys.exit(main())
