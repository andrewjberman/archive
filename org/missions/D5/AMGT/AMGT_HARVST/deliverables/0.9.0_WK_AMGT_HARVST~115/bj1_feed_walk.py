"""bj-1: walk the real scoped_amgt.read_feed for twelve securities. Read-only; no verdict on content."""
import json
import sys
from pathlib import Path

from lib.research.api import scoped_amgt
from lib.research.harvest import publication_gold

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
REMOVALS = ROOT / ("org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round64/"
                   "REBUILD9_NAMED_REMOVALS.json")
EXPECT_PART = "amgt/harvest/gold/article_security_mention/date=2026-10-08/part-20261008T055319Z.parquet"
KEYS = ["CAT_US_Equity", "CSL_AU_Equity", "HEI_US_Equity", "BP_US_Equity", "SAP_GY_Equity",
        "ASML_US_Equity", "AIG_US_Equity", "NOKIA_FH_Equity", "GSK_LN_Equity", "ICT_US_Equity",
        "META_US_Equity", "LLY_US_Equity"]
FAILED = ("NOT_ASKED", "INCOMPLETE")


def main():
    out = []
    feeds = {}
    for key in KEYS:
        feeds[key] = scoped_amgt.read_feed(key)
    cached = publication_gold._GOLD_SNAPSHOT_CACHE.get("article_security_mention")
    part = cached[0][0] if cached else None
    snapshot = cached[1] if cached else []
    out.append("SERVED PART READ: {0} (established from the seam's own snapshot cache after the calls; rows {1})".format(
        part, len(snapshot)))
    out.append("DENOMINATOR: securities 12")
    mention = {(r.get("security_key"), r.get("article_key")): r for r in snapshot}
    md = ["# BJ1 feed walk", "",
          "Called the real `scoped_amgt.read_feed(<key>)` (no fixture, no patch, `as_of_date` left to today) for twelve "
          "securities. It read the served part `{0}`. The question per security is: does this feed read as coverage "
          "of this company. No verdict or grade is given here; a reviewer grades it.".format(part), ""]
    js = {"served_part": part, "securities": []}
    not_read = []
    for key in KEYS:
        f = feeds[key]
        st = f.get("coverage_status")
        win = f.get("window") or {}
        idstat = "MEASURED" if st not in ("NOT_ASKED",) else "UNRESOLVED"
        line = "{0}: coverage_status {1}, items {2}, window {3} to {4}, identity {5}".format(
            key, st, f.get("item_count"), win.get("start_date"), win.get("end_date"), idstat)
        out.append(line)
        if st in FAILED or f.get("reason"):
            out.append("  reason: {0}".format(f.get("reason")))
        if st in FAILED:
            not_read.append(key)
        md += ["## " + key, "", line, ""]
        rows = []
        for it in f["items"][:15]:
            m = mention.get((key, it["article_key"])) or {}
            rec = {"published_date": it["published_date"], "publisher": it["publisher"], "title": it["title"],
                   "url": it["url"], "url_reason": it["url_reason"],
                   "match_forms": m.get("match_forms"), "mention_count": m.get("mention_count")}
            rows.append(rec)
            md.append("- {published_date} | {publisher} | {title} | {u} | match_forms={match_forms} | "
                      "mention_count={mention_count}".format(u=rec["url"] or rec["url_reason"], **rec))
        md.append("")
        js["securities"].append({"security_key": key, "header": line, "reason": f.get("reason"),
                                 "items_total": f.get("item_count"), "items": rows})
    removals = json.loads(REMOVALS.read_text(encoding="utf-8"))["rows"]
    walked = set(KEYS)
    rel = [r for r in removals if r["security_key"] in walked]
    still = []
    for r in rel:
        if any(i["article_key"] == r["article_key"] for i in feeds[r["security_key"]]["items"]):
            still.append(r)
    out.append("NAMED REMOVALS STILL IN A WALKED FEED: {0} of {1}".format(len(still), len(rel)))
    for r in still:
        out.append("  still present: {0} {1}".format(r["security_key"], r["article_key"]))
    js["named_removals_still_present"] = still
    fails = []
    if not_read:
        fails.append("not read: " + ",".join(not_read))
    if part != EXPECT_PART:
        fails.append("part read {0} is not {1}".format(part, EXPECT_PART))
    if still:
        fails.append("named removals present: {0}".format(len(still)))
    out.append("WALK OK" if not fails else "WALK FAIL: " + "; ".join(fails))
    (HERE / "BJ1_FEED_WALK.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (HERE / "BJ1_FEED_WALK.json").write_text(json.dumps(js, indent=1, default=str), encoding="utf-8")
    text = "\n".join(out) + "\n"
    (HERE / "bj1_feed_walk.out").write_text(text, encoding="utf-8")
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
