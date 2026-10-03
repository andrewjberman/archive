"""HARVST round 41 HVST-an-3, CTO half @8e0fed682a condition 3: name each served event_id the rebuild does not reproduce,
with the reason under the current rule. Read-only.

Input: `round41/served_events_before_an3.json` (the 8 rows of the served part before the act). For each served event not in
the newest `chatter_event` part, report the rebuilt events on the same security whose span overlaps it (same story,
re-formed) and the per-field difference; with no overlapping event, the story's members under the current mention
snapshot and which threshold fails. Writes `round41/dropped_events.json`.
"""
import datetime
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
HERE = os.path.dirname(os.path.abspath(__file__))

from lib.research.harvest import publication_gold as pg  # noqa: E402


def day(v):
    return v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v)[:10])


def main():
    served = json.load(open(os.path.join(HERE, "served_events_before_an3.json"), encoding="utf-8"))["rows"]
    built = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE)
    mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    built_ids = {e["event_id"] for e in built}
    out = []
    for s in served:
        if s["event_id"] in built_ids:
            continue
        f, l_ = day(s["first_day"]), day(s["last_day"])
        over = [e for e in built if e["security_key"] == s["security_key"]
                and day(e["first_day"]) <= l_ and day(e["last_day"]) >= f]
        row = {"event_id": s["event_id"], "security_key": s["security_key"], "first_day": str(f), "last_day": str(l_),
               "lead_article_key": s["lead_article_key"], "articles_total": s["articles_total"],
               "served_article_keys": s["article_keys"]}
        if over:
            e = over[0]
            row["reformed_as"] = {"event_id": e["event_id"], "first_day": str(e["first_day"]), "last_day": str(e["last_day"]),
                                  "lead_article_key": e["lead_article_key"], "articles_total": e["articles_total"],
                                  "publishers_distinct": e["publishers_distinct"],
                                  "articles_added": sorted(set(e["article_keys"]) - set(s["article_keys"])),
                                  "articles_dropped": sorted(set(s["article_keys"]) - set(e["article_keys"]))}
            changed = [k for k in ("first_day", "last_day", "lead_article_key") if str(e[k]) != str(s[k])]
            row["reason"] = ("RE-FORMED: the same story is served as %s; the event_id is a hash of (security, first_day, "
                             "last_day, lead), and %s changed because the rebuilt mention table adds %d member(s)"
                             % (e["event_id"][:12], ", ".join(changed) or "membership", len(row["reformed_as"]["articles_added"])))
        else:
            members = [m for m in mention if m.get("security_key") == s["security_key"] and m.get("article_key") in set(s["article_keys"])]
            row["members_in_current_mention"] = len(members)
            row["members_guarded"] = sum(1 for m in members if pg._is_guarded(m))
            row["tier_a_publishers"] = sorted({m.get("publisher") for m in members if m.get("signal_tier") == "A"})
            row["reason"] = ("NOT RE-FORMED: %d of %d served members are in the current mention table, %d guarded, tier-A "
                             "publishers %s (rule: >= %d articles, >= %d tier-A publishers)"
                             % (len(members), len(s["article_keys"]), row["members_guarded"], row["tier_a_publishers"],
                                pg.EVENT_MIN_ARTICLES, pg.EVENT_MIN_PUBLISHERS))
        out.append(row)
        print("%s %s %s..%s: %s" % (s["event_id"][:12], s["security_key"], f, l_, row["reason"]))
    json.dump({"served": len(served), "built": len(built), "dropped": out}, open(os.path.join(HERE, "dropped_events.json"), "w",
              encoding="utf-8"), indent=1, default=str)
    print("DROPPED: %d of %d served; built %d" % (len(out), len(served), len(built)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
