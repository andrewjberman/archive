"""HVST-k-1 AC2 -- THE DRY REBUILD of chatter_event UNDER THE NEW RULE (span rule + roundup guard), IN MEMORY,
over today's inputs, beside the SERVED newest event part. S3 LIST/GET only through the producer's own readers;
NO put, NO delete, NO vendor call, NO gold write.

The rule under test is the one in `publication_gold.event_rows` / `_story_runs` -- this script calls it, it does not
re-implement it. The j-2 census script (READ ONLY, another worker's deliverable) is imported for its reader helpers
and for its CANDIDATE function, which is the comparison object for criteria (b) and (c).

PASS only if (b), (c), (d) and (e) all hold; each is printed with its own verdict, and the exit code is the AND."""
import datetime
import importlib.util
import json
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 8))
sys.path.insert(0, REPO)

import pyarrow as pa  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "..", "k1_ac2_result.json")
J2_DIR = os.path.join(HERE, "..", "..", "0.9.0_WK_AMGT_HARVST~48")
_spec = importlib.util.spec_from_file_location("j2", os.path.join(J2_DIR, "scripts", "j2_ac1_story_span_census.py"))
j2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(j2)

a, canon = j2.a, j2.canon
HD_SEC, HD_ROUNDUP_TITLE_PREFIX = "HD_US_Equity", "6 Big Takeaways"


def guard_word(row):
    if row.get("is_roundup"):
        return "GUARDED(is_roundup)"
    if (row.get("co_mention_count") or 0) >= pg.EVENT_GUARD_CO_MENTIONS:
        return "GUARDED(co_mention=%d)" % row["co_mention_count"]
    return "core"


def rt(rows):
    return pa.Table.from_pylist(rows, schema=pg.GOLD_EVENT_SCHEMA).to_pylist()


def fields_equal(x, y):
    return all(canon(x.get(f)) == canon(y.get(f)) for f in set(x) | set(y))


def show(e, tag, row_of, title):
    print("   %s event %s %s first_day=%s last_day=%s (days_span=%d) articles=%d tier_a=%d tier_b=%d publishers=%d" % (
        tag, e["event_id"][:12], e["security_key"], e["first_day"], e["last_day"], e["days_span"], e["articles_total"],
        e["tier_a"], e["tier_b"], e["publishers_distinct"]))
    print("      lead: %s" % a(e["lead_headline"]))
    for k in e["article_keys"]:
        r = row_of[(k, e["security_key"])]
        print("      - %s | tier %s | %-7s | %-22s | %s | %s" % (
            pg._day_of(r["published_utc"]), r["signal_tier"], r["publisher"], guard_word(r), a(title(k), 100), a(k[:32])))


def main():
    client = store._default_client()
    ev_key, ev_parts = j2.newest_part(client, pg.GOLD_EVENT_TABLE)
    mn_key, mn_parts = j2.newest_part(client, pg.GOLD_TABLE)
    served = j2.read_rows(client, ev_key)
    mention = j2.read_rows(client, mn_key)
    arts = {r["article_key"]: r for r in pg._iter_latest_articles(client=client)}
    enriched = [dict(r, title=arts.get(r["article_key"], {}).get("title")) for r in mention]
    title = lambda k: arts.get(k, {}).get("title")  # noqa: E731
    row_of = {(r["article_key"], r["security_key"]): r for r in mention}

    print("== HVST-k-1 AC2: THE DRY REBUILD of chatter_event under the span rule + roundup guard (in memory; no write) ==")
    print("inputs: served event part %s (%d parts; %d events)" % (ev_key, ev_parts, len(served)))
    print("        served mention part %s (%d parts; %d rows; tier A/B rows %d; guarded tier A/B rows %d); silver articles %d" % (
        mn_key, mn_parts, len(mention), sum(1 for r in mention if r["signal_tier"] in ("A", "B")),
        sum(1 for r in mention if r["signal_tier"] in ("A", "B") and guard_word(r) != "core"), len(arts)))

    new = rt(pg.event_rows(enriched))
    old_rule_baseline = rt(pg.event_rows([{k: v for k, v in r.items() if k not in ("is_roundup", "co_mention_count")}
                                          for r in enriched], max_gap_days=pg.EVENT_MAX_GAP_DAYS))
    n_by = {r["event_id"]: r for r in new}

    # ---------------- (a) per served event ----------------
    print("\n== (a) PER SERVED EVENT under the new rule (denominator %d served events) ==" % len(served))
    status, new_ids, merged = j2.classify(served, new)
    counts = {"KEPT": 0, "MERGED": 0, "CHANGED": 0, "GONE": 0}
    for s in served:
        st, touch = status[s["event_id"]]
        # j2.classify calls an event KEPT when the members and the id agree; the row-equal test is stricter
        if st == "KEPT" and not fields_equal(s, n_by[s["event_id"]]):
            st = "CHANGED"
        counts[st] += 1
        print("   %-7s %s %s served first_day=%s last_day=%s articles=%d -> new %s" % (
            st, s["event_id"][:12], s["security_key"], s["first_day"], s["last_day"], s["articles_total"],
            ", ".join("%s(%s..%s,%d)" % (t[:12], n_by[t]["first_day"], n_by[t]["last_day"], n_by[t]["articles_total"]) for t in touch) or "-"))
        status[s["event_id"]] = (st, touch)
    print("   COUNTS of %d served: KEPT=%d CHANGED=%d MERGED=%d GONE=%d (sum %d); NEW events (share no article with a served event)=%d; "
          "new-rule events total=%d" % (len(served), counts["KEPT"], counts["CHANGED"], counts["MERGED"], counts["GONE"],
                                        sum(counts.values()), len(new_ids), len(new)))
    print("\n   SERVED events, members with guard status:")
    for s in served:
        show(s, status[s["event_id"]][0] + "/served", row_of, title)
    print("\n   NEW-RULE events, members with guard status:")
    for e in new:
        touched = [s["event_id"][:12] for s in served if set(s["article_keys"]) & set(e["article_keys"])]
        show(e, ("NEW" if e["event_id"] in new_ids else "new-rule") + (" (touches served %s)" % ",".join(touched) if touched else ""), row_of, title)

    # ---------------- (b) the 5 that j-2 kept ----------------
    j2_cand = j2.candidate_event_rows(enriched)
    j2_cand_rt = rt(j2_cand)
    j2_status, _j2_new, _j2_merged = j2.classify(served, j2_cand_rt)
    j2_kept = [s for s in served if j2_status[s["event_id"]][0] == "KEPT"]
    j2_json = json.load(open(os.path.join(J2_DIR, "j2_census_result.json"), encoding="utf-8"))
    print("\n== (b) the events j-2 KEPT, row-equal to the served rows under the new rule ==")
    print("j-2 result file: KEPT=%d of %d served, candidate events=%d; recomputed j-2 candidate here: KEPT=%d, events=%d" % (
        j2_json["counts"]["KEPT"], j2_json["served_events"], j2_json["candidate_events"], len(j2_kept), len(j2_cand_rt)))
    b_equal = 0
    for s in j2_kept:
        n = n_by.get(s["event_id"])
        ok = n is not None and fields_equal(s, n)
        b_equal += ok
        print("   %s %s %s..%s : %s" % ("ROW-EQUAL" if ok else "NOT-EQUAL", s["event_id"][:12], s["security_key"], s["first_day"],
                                        "all %d fields equal" % len(pg.GOLD_EVENT_SCHEMA) if ok else (
            "no new-rule event with this id" if n is None else "; ".join(
                "%s served=%s new=%s" % (f, a(canon(s.get(f)), 60), a(canon(n.get(f)), 60)) for f in sorted(s) if canon(s.get(f)) != canon(n.get(f))))))
    b_ok = (len(j2_kept) == j2_json["counts"]["KEPT"] == 5) and b_equal == len(j2_kept)
    print("(b) %d of %d j-2-kept events row-equal to the served rows (expect 5 of 5) -> %s" % (b_equal, len(j2_kept), "HOLDS" if b_ok else "FAILS"))

    # ---------------- (c) 992_HK and AMZN changed events equal j-2's candidate ----------------
    print("\n== (c) 992_HK_Equity and AMZN_US_Equity CHANGED events equal j-2's candidate events (span, member set, lead) ==")
    j2_text = open(os.path.join(J2_DIR, "j2_ac1_output.txt"), encoding="utf-8").read()
    c_ok = True
    c_detail = {}
    for sec in ("992_HK_Equity", "AMZN_US_Equity"):
        changed_served = [s for s in served if s["security_key"] == sec and j2_status[s["event_id"]][0] == "CHANGED"]
        for s in changed_served:
            cand_ids = j2_status[s["event_id"]][1]
            for cid in cand_ids:
                c = next(e for e in j2_cand_rt if e["event_id"] == cid)
                m = re.search(r"CHANGED event %s %s span (\S+)\.\.(\S+) \(days_span=(\d+)\) articles=(\d+)" % (cid[:12], sec), j2_text)
                text_ok = bool(m) and (m.group(1), m.group(2), int(m.group(4))) == (str(c["first_day"]), str(c["last_day"]), c["articles_total"])
                json_ok = True
                if sec == "AMZN_US_Equity":
                    json_ok = [{"span": [str(c["first_day"]), str(c["last_day"])], "articles": c["articles_total"]}] == j2_json["amzn_candidate"]
                mine = [e for e in new if e["security_key"] == sec and set(e["article_keys"]) & set(c["article_keys"])]
                same = len(mine) == 1 and (mine[0]["first_day"], mine[0]["last_day"]) == (c["first_day"], c["last_day"]) \
                    and set(mine[0]["article_keys"]) == set(c["article_keys"]) and mine[0]["lead_article_key"] == c["lead_article_key"]
                c_ok &= same and text_ok and json_ok
                c_detail[sec] = {"j2_candidate": {"first_day": str(c["first_day"]), "last_day": str(c["last_day"]), "articles": c["articles_total"],
                                                  "lead": c["lead_article_key"]},
                                 "new_rule": [{"first_day": str(e["first_day"]), "last_day": str(e["last_day"]), "articles": e["articles_total"],
                                               "lead": e["lead_article_key"]} for e in mine], "equal": same}
                print("   %s: j-2 candidate %s span %s..%s members=%d lead=%s (matches j-2's own output text: %s; j2_census_result.json: %s)" % (
                    sec, cid[:12], c["first_day"], c["last_day"], c["articles_total"], a(c["lead_headline"], 70), text_ok,
                    "n/a (file carries AMZN only) " if sec != "AMZN_US_Equity" else json_ok))
                for e in mine:
                    print("      new-rule %s span %s..%s members=%d lead=%s  -> %s" % (
                        e["event_id"][:12], e["first_day"], e["last_day"], e["articles_total"], a(e["lead_headline"], 70),
                        "EQUAL" if same else "NOT EQUAL"))
                    if not same:
                        print("         members only in j-2's candidate: %s" % sorted(set(c["article_keys"]) - set(e["article_keys"])))
                        print("         members only in the new rule:    %s" % sorted(set(e["article_keys"]) - set(c["article_keys"])))
                        print("         lead differs: %s (j-2) vs %s (new rule); lead guard status in j-2: %s" % (
                            c["lead_article_key"], e["lead_article_key"], guard_word(row_of[(c["lead_article_key"], sec)])))
    print("(c) -> %s" % ("HOLDS" if c_ok else "FAILS"))

    # ---------------- (d) HD ----------------
    print("\n== (d) HD_US_Equity's event ends 2026-08-18; the 2026-08-20 '6 Big Takeaways' article is a MEMBER flagged by the guard ==")
    hd = [e for e in new if e["security_key"] == HD_SEC and datetime.date(2026, 8, 17) <= e["first_day"] <= datetime.date(2026, 8, 20)]
    d_ok = False
    for e in hd:
        takeaways = [k for k in e["article_keys"] if (title(k) or "").startswith(HD_ROUNDUP_TITLE_PREFIX)]
        flagged = [k for k in takeaways if guard_word(row_of[(k, HD_SEC)]) != "core"]
        d_ok = e["last_day"] == datetime.date(2026, 8, 18) and bool(takeaways) and takeaways == flagged \
            and pg._day_of(row_of[(takeaways[0], HD_SEC)]["published_utc"]) == datetime.date(2026, 8, 20)
        print("   HD event %s first_day=%s last_day=%s members=%d; '6 Big Takeaways' members=%s guard=%s stored is_roundup=%s co_mention_count=%s" % (
            e["event_id"][:12], e["first_day"], e["last_day"], e["articles_total"], takeaways,
            [guard_word(row_of[(k, HD_SEC)]) for k in takeaways], [row_of[(k, HD_SEC)]["is_roundup"] for k in takeaways],
            [row_of[(k, HD_SEC)]["co_mention_count"] for k in takeaways]))
    print("(d) %d HD event(s) in the window -> %s" % (len(hd), "HOLDS" if d_ok and len(hd) == 1 else "FAILS"))
    d_ok = d_ok and len(hd) == 1

    # ---------------- (e) uniqueness ----------------
    ids = [e["event_id"] for e in new]
    e_ok = len(ids) == len(set(ids))
    dup = sum(1 for e in new for k in e["article_keys"] if [x for x in new if x["security_key"] == e["security_key"] and k in x["article_keys"]][1:])
    print("\n== (e) EVENT_ID UNIQUENESS ==")
    print("(e) new-rule events=%d, distinct event_ids=%d -> %s (informational: article memberships shared by two events of one security: %d)" % (
        len(ids), len(set(ids)), "HOLDS" if e_ok else "FAILS", dup))

    # ---------------- informational: why a check fails ----------------
    gone = [s for s in served if status[s["event_id"]][0] == "GONE"]
    if gone:
        print("\n== INFORMATIONAL (no verdict): the GONE served events, and what the same rows give with the guard columns removed ==")
        for s in gone:
            unguarded = [e for e in old_rule_baseline if e["security_key"] == s["security_key"] and set(e["article_keys"]) & set(s["article_keys"])]
            print("   GONE %s %s: all %d members are guarded (%s); with the guard columns stripped the span-rule event would be %s" % (
                s["event_id"][:12], s["security_key"], s["articles_total"],
                ", ".join(guard_word(row_of[(k, s["security_key"])]) for k in s["article_keys"]),
                ", ".join("%s..%s (%d members)" % (e["first_day"], e["last_day"], e["articles_total"]) for e in unguarded) or "none"))

    ok = b_ok and c_ok and d_ok and e_ok
    result = {"served_event_key": ev_key, "served_mention_key": mn_key, "served_events": len(served), "counts": counts,
              "new_events_not_touching_a_served_event": len(new_ids), "new_rule_events": len(new),
              "b_row_equal": b_equal, "b_of": len(j2_kept), "b_ok": b_ok, "c_ok": c_ok, "c_detail": c_detail, "d_ok": d_ok, "e_ok": e_ok,
              "gone": [{"event_id": s["event_id"], "security_key": s["security_key"]} for s in gone], "pass": ok}
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("\nAC2 RESULT: %s  ((b)=%s (c)=%s (d)=%s (e)=%s)" % ("PASS" if ok else "FAIL", b_ok, c_ok, d_ok, e_ok))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
