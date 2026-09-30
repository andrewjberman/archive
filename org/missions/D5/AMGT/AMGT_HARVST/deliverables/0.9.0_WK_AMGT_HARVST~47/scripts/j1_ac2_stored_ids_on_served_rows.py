"""HVST-j-1 AC2: the event route serves the stored event by its stored id, over the SERVED newest
chatter_event part. READ-ONLY: S3 GET/LIST through publication_gold._latest_gold_snapshot_rows
(the producer's own newest-snapshot reader) and nothing else. No PUT, no vendor call.

(a) per event: stored event_id beside the OLD code's recomputed id (old timeline_api at the base
    86ee31f531, via git show); count that differ.
(b) NEW get_timeline_event(stored id) returns that very row (first_day, last_day, event_id equal)
    with its articles: n of N.
(c) old first_day-keyed call and new id-keyed call return the same article set per event.
PASS only if (b) is N of N and (c) holds.
"""

import importlib.util
import json
import os
import subprocess
import sys

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
sys.path.insert(0, ROOT)

import lib.research.harvest.publication_gold as gold  # noqa: E402
import lib.research.harvest.timeline_api as new_api  # noqa: E402

BASE = "86ee31f531"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "j1_ac2_result.json")


def _load_old():
    src = subprocess.check_output(
        ["git", "show", "%s:lib/research/harvest/timeline_api.py" % BASE], cwd=ROOT
    ).decode("utf-8")
    spec = importlib.util.spec_from_loader("timeline_api_at_base", loader=None)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(src, "timeline_api@%s" % BASE, "exec"), mod.__dict__)
    return mod


def main():
    old_api = _load_old()
    events = gold._latest_gold_snapshot_rows("chatter_event")
    mentions = gold._latest_gold_snapshot_rows("article_security_mention")
    print("newest chatter_event part rows: %d ; article_security_mention rows: %d" % (len(events), len(mentions)))

    def event_loader(security_key):
        return [r for r in events if r.get("security_key") == security_key]

    def article_loader(security_key, event_row):
        wanted = set(event_row.get("article_keys") or [])
        rows = []
        for r in mentions:
            if r.get("security_key") == security_key and r.get("article_key") in wanted:
                m = dict(r)
                m["headline"] = r.get("title")
                rows.append(m)
        return rows

    total = len(events)
    differ = 0
    b_ok = 0
    c_ok = 0
    per = []
    for e in events:
        sk, fd, ld, stored = e["security_key"], e["first_day"], e["last_day"], e["event_id"]
        recomputed = gold._event_id(sk, fd, ld)
        old_body = old_api.get_timeline_event(sk, fd.isoformat(), event_loader, article_loader)
        old_served = old_body.get("event_id")
        d = stored != recomputed
        differ += d
        new_body = new_api.get_timeline_event(sk, stored, event_loader, article_loader)
        b = (
            not new_api.is_error_body(new_body)
            and new_body["first_day"] == fd.isoformat()
            and new_body["last_day"] == ld.isoformat()
            and new_body["event_id"] == stored
        )
        b_ok += b
        keys_new = sorted(a["article_key"] for a in new_body.get("articles", []))
        keys_old = sorted(a["article_key"] for a in old_body.get("articles", []))
        c = (not new_api.is_error_body(old_body)) and keys_new == keys_old
        c_ok += c
        per.append({
            "security_key": sk, "first_day": fd.isoformat(), "last_day": ld.isoformat(),
            "stored_event_id": stored, "old_code_recomputed_id": recomputed,
            "old_route_served_id": old_served, "differ": d,
            "new_returns_that_row": b, "new_articles": len(keys_new),
            "old_articles": len(keys_old), "same_article_set": c,
        })
        print("%s %s..%s stored=%s.. recomputed=%s.. differ=%s new_row=%s articles new/old=%d/%d same=%s" % (
            sk, fd, ld, stored[:12], recomputed[:12], d, b, len(keys_new), len(keys_old), c))
    print("(a) stored != old recomputed: %d of %d" % (differ, total))
    print("(b) new id-keyed call returns that very row with articles: %d of %d" % (b_ok, total))
    print("(c) old first_day-keyed and new id-keyed article sets equal: %d of %d" % (c_ok, total))
    ok = total > 0 and b_ok == total and c_ok == total
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"denominator": total, "a_differ": differ, "b_ok": b_ok, "c_ok": c_ok,
                   "pass": ok, "events": per}, fh, indent=1)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
