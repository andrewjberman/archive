"""bk-3: second walk of the real scoped_amgt.read_feed for the bj-1 twelve. Read-only; no verdict."""
import json
import sys
from pathlib import Path

from lib.research.api import scoped_amgt
from lib.research.harvest import publication_gold

HERE = Path(__file__).resolve().parent
BJ1 = HERE.parent / "0.9.0_WK_AMGT_HARVST~115" / "BJ1_FEED_WALK.json"
FIRST_PART = "amgt/harvest/gold/article_security_mention/date=2026-10-08/part-20261008T055319Z.parquet"
KEYS = ["CAT_US_Equity", "CSL_AU_Equity", "HEI_US_Equity", "BP_US_Equity", "SAP_GY_Equity",
        "ASML_US_Equity", "AIG_US_Equity", "NOKIA_FH_Equity", "GSK_LN_Equity", "ICT_US_Equity",
        "META_US_Equity", "LLY_US_Equity"]
FAILED = ("NOT_ASKED", "INCOMPLETE")
REPORTED = "Bond Traders Bet on Fed Delivering 25 BP Rate Increase"


def ident(d):
    """BJ1_FEED_WALK.json carries no article_key; identity is (date, publisher, title)."""
    return (str(d.get("published_date")), d.get("publisher"), d.get("title"))


def main():
    feeds = {k: scoped_amgt.read_feed(k) for k in KEYS}
    cached = publication_gold._GOLD_SNAPSHOT_CACHE.get("article_security_mention")
    part = cached[0][0] if cached else None
    snapshot = cached[1] if cached else []
    out = ["SERVED PART READ: {0}, rows {1}".format(part, len(snapshot)),
           "FIRST WALK'S PART: {0}".format(FIRST_PART)]
    if part == FIRST_PART:
        out.append("WALK FAIL: no newer part is served")
        sys.stdout.write("\n".join(out) + "\n")
        (HERE / "bk3_feed_walk.out").write_text("\n".join(out) + "\n", encoding="utf-8")
        return
    mention = {(r.get("security_key"), r.get("article_key")): r for r in snapshot}
    first = {s["security_key"]: s for s in json.loads(BJ1.read_text(encoding="utf-8"))["securities"]}
    md = ["# BK3 feed walk", "", "Second walk of the real `scoped_amgt.read_feed(<key>)` for the twelve securities "
          "of the first walk. Served part: `{0}`. First walk's part: `{1}`. No verdict or grade is given here."
          .format(part, FIRST_PART), "",
          "Comparison basis: BJ1_FEED_WALK.json stores no article_key and only the newest 15 items per security, so "
          "items are matched on (published_date, publisher, title). For a security whose first-walk feed exceeded 15 "
          "items, the older first-walk items are not in the packet and cannot be compared.", ""]
    js = {"served_part": part, "first_walk_part": FIRST_PART, "securities": []}
    not_read = []
    reported_in = False
    for key in KEYS:
        f = feeds[key]
        st = f.get("coverage_status")
        items = f["items"]
        fs = first[key]
        stored = fs["items"]
        n0 = fs["items_total"]
        cur_ids = {ident(i) for i in items}
        old_ids = {ident(i) for i in stored}
        gone = [i for i in stored if ident(i) not in cur_ids]
        if len(stored) < n0:
            new = [i for i in items if ident(i) not in old_ids]
            partial = True
        else:
            new = [i for i in items if ident(i) not in old_ids]
            partial = False
        line = ("{0}: coverage_status {1}, items {2} (first walk {3}), items no longer in the feed {4}, "
                "items new {5}").format(key, st, f.get("item_count"), n0, len(gone), len(new))
        if partial:
            line += " [first walk stored {0} of {1}; counts compare against those {0}]".format(len(stored), n0)
        out.append(line)
        if st in FAILED or f.get("reason"):
            out.append("  reason: {0}".format(f.get("reason")))
        if st in FAILED:
            not_read.append(key)
        if key == "BP_US_Equity":
            reported_in = any(i["title"] == REPORTED for i in items)

        def rec(it):
            m = mention.get((key, it["article_key"])) or {}
            return {"published_date": it["published_date"], "publisher": it["publisher"], "title": it["title"],
                    "url": it["url"], "url_reason": it["url_reason"],
                    "match_forms": m.get("match_forms"), "mention_count": m.get("mention_count")}
        rows = [rec(i) for i in items[:15]]
        newr = [rec(i) for i in new]
        md += ["## " + key, "", line, "", "Newest 15:", ""]
        for r in rows:
            md.append("- {published_date} | {publisher} | {title} | {u} | match_forms={match_forms} | "
                      "mention_count={mention_count}".format(u=r["url"] or r["url_reason"], **r))
        md += ["", "Left the feed ({0}):".format(len(gone)), ""]
        for g in gone:
            md.append("- {published_date} | {publisher} | {title} | match_forms={match_forms}".format(**g))
        md += ["", "New ({0}):".format(len(new)), ""]
        for r in newr:
            md.append("- {published_date} | {publisher} | {title} | match_forms={match_forms}".format(**r))
        md.append("")
        js["securities"].append({"security_key": key, "header": line, "reason": f.get("reason"),
                                 "items_total": f.get("item_count"), "first_walk_items_total": n0,
                                 "items": rows, "left_the_feed": gone, "new": newr})
    out.append("THE REPORTED ITEM: \"{0}\" on BP_US_Equity {1}".format(
        REPORTED, "in the feed" if reported_in else "not in the feed"))
    js["reported_item_in_feed"] = reported_in
    out.append("WALK OK" if not not_read else "WALK FAIL: not read: " + ",".join(not_read))
    (HERE / "BK3_FEED_WALK.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (HERE / "BK3_FEED_WALK.json").write_text(json.dumps(js, indent=1, default=str), encoding="utf-8")
    text = "\n".join(out) + "\n"
    (HERE / "bk3_feed_walk.out").write_text(text, encoding="utf-8")
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
