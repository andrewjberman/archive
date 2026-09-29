"""HVST-i-1 AC2: UBS leaves the whole-brand list; nothing served moves. IN MEMORY, S3 GET/LIST only (no put,
no delete, no vendor call). OLD = round 18's securities file (~45), NEW = this cell's (~46).
(1) NEW equals a fresh universe_securities.build() at HEAD.
(2) UBS_US_Equity aliases / ticker_aliases, OLD vs NEW.
(3) All THREE tables rebuilt from OLD and from NEW over today's silver, set beside the SERVED newest parts;
    every moved row (served vs new) is attributed ALIAS (served == old-rebuild, so the new file moved it) or
    DRIFT (the silver grew / the range extended: old-rebuild already differs from served). ALIAS must be 0.
(4) UBS_US_Equity's mention hits per form, served vs new."""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i1_common as C  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

UBS = "UBS_US_Equity"


def mention_key(r):
    return (r["article_key"], r["security_key"])


def daily_key(r):
    return (r["security_key"], r["day"])


def event_key(r):
    return r["event_id"]


def attribution(s, o, n):
    """ALIAS when the served row equals the OLD rebuild (so only the securities file can have moved it),
    else DRIFT when the two rebuilds agree (the silver moved it), else ALIAS+DRIFT. Called when s != n."""
    if C.canon(s) == C.canon(o):
        return "ALIAS"
    if C.canon(n) == C.canon(o):
        return "DRIFT"
    return "ALIAS+DRIFT"


def table_report(name, served, old, new, key):
    s = {key(r): r for r in served}
    o = {key(r): r for r in old}
    n = {key(r): r for r in new}
    moved = sorted((k for k in set(s) | set(n) if C.canon(s.get(k)) != C.canon(n.get(k))), key=str)
    counts = {"ALIAS": 0, "DRIFT": 0, "ALIAS+DRIFT": 0}
    old_vs_new = [k for k in set(o) | set(n) if C.canon(o.get(k)) != C.canon(n.get(k))]
    print("\n== %s ==" % name)
    print("rows: served=%d old-rebuild=%d new-rebuild=%d; rows where NEW != OLD rebuild (the securities file's effect): %d" % (
        len(s), len(o), len(n), len(old_vs_new)))
    for k in moved:
        att = attribution(s.get(k), o.get(k), n.get(k))
        counts[att] += 1
        fields = C.diff_fields(s.get(k), n.get(k))
        if fields is None:
            what = "one side absent (served %s, new %s)" % ("present" if k in s else "absent", "present" if k in n else "absent")
        else:
            what = "fields=%s" % fields
        print("  [%s] %s | %s" % (att, C.a(str(k), 110), what))
    print("%s: moved (served vs new) = %d of %d served rows -> ALIAS=%d DRIFT=%d ALIAS+DRIFT=%d" % (
        name, len(moved), len(s), counts["ALIAS"], counts["DRIFT"], counts["ALIAS+DRIFT"]))
    return counts, len(old_vs_new)


def main():
    problems = []
    as_of = datetime.datetime.now(datetime.timezone.utc).date()

    # (1) the securities file equals a fresh build at HEAD
    print("== (1) securities file vs a fresh universe_securities.build() at HEAD ==")
    fresh, summary = us.build()
    fresh = json.loads(json.dumps(fresh, sort_keys=True))
    new_sec = C.load_json(C.NEW_PATH)
    old_sec = C.load_json(C.OLD_PATH)
    equal = fresh == new_sec
    print("universe: %s %s; whole_brand list_entries=%s admitted=%d refused=%d" % (
        summary["universe"]["source"], summary["universe"]["denominators"],
        summary["whole_brand_denominator"]["list_entries"], len(summary["whole_brand_admitted"]),
        len(summary["whole_brand_refused"])))
    print("NEW file (%d securities) equals fresh build (%d securities): %s" % (
        len(new_sec), len(fresh), "EQUAL" if equal else "DIFFERENT"))
    if not equal:
        problems.append("securities file differs from a fresh build")
    old_by, new_by = C.sec_map(old_sec), C.sec_map(new_sec)
    differing = sorted(k for k in set(old_by) | set(new_by) if old_by.get(k) != new_by.get(k))
    print("securities differing OLD vs NEW (any field): %d of %d  %s" % (len(differing), len(new_by), differing))

    # (2) UBS OLD vs NEW
    print("\n== (2) %s aliases / ticker_aliases, OLD (~45) vs NEW (~46) ==" % UBS)
    for label, by in (("OLD", old_by), ("NEW", new_by)):
        print("  %s aliases=%s ticker_aliases=%s" % (label, by[UBS]["aliases"], by[UBS].get("ticker_aliases")))
    if "UBS" in new_by[UBS]["aliases"] or new_by[UBS].get("ticker_aliases") != ["UBS"]:
        problems.append("UBS_US_Equity is not ticker-only in the NEW file")
    brand_entries = [e for e in C.load_json(C.BRAND_PATH)["whole_brands"]
                     if e["security_key"] == UBS or e["brand"].upper() == "UBS"]
    print("  whole-brand entries for UBS in the shipped list: %d" % len(brand_entries))
    if brand_entries:
        problems.append("UBS still on the whole-brand list")

    # (3) three tables
    articles, hits, served = C.fetch()
    print("\nsilver articles=%d listing_hit rows=%d as_of=%s" % (len(articles), len(hits), as_of))
    for t in (pg.GOLD_TABLE, pg.GOLD_DAILY_TABLE, pg.GOLD_EVENT_TABLE):
        key, parts, rows = served[t]
        print("SERVED newest %-26s %s (parts=%d, rows=%d)" % (t, key, parts, len(rows)))
    old_t, _oe = C.build_memory(old_sec, articles, hits, as_of)
    new_t, _ne = C.build_memory(new_sec, articles, hits, as_of)
    tot = {"ALIAS": 0, "DRIFT": 0, "ALIAS+DRIFT": 0}
    for name, table, key in (("article_security_mention", pg.GOLD_TABLE, mention_key),
                             ("chatter_daily", pg.GOLD_DAILY_TABLE, daily_key),
                             ("chatter_event", pg.GOLD_EVENT_TABLE, event_key)):
        counts, n_eff = table_report(name, served[table][2], old_t[table], new_t[table], key)
        for c in tot:
            tot[c] += counts[c]
        if counts["ALIAS"] or counts["ALIAS+DRIFT"] or n_eff:
            problems.append("%s: ALIAS=%d ALIAS+DRIFT=%d new-vs-old rows=%d" % (
                name, counts["ALIAS"], counts["ALIAS+DRIFT"], n_eff))

    # (4) UBS hits per form
    print("\n== (4) %s mention hits per form ==" % UBS)
    ubs_new = new_by[UBS]
    per_form = {}
    for art in articles:
        for _where, text in C.texts_of(art):
            for _s, _e, _m, label, kind in C.spans_with_forms(
                    text, pg._security_aliases(ubs_new), pg._security_exact_aliases(ubs_new)):
                per_form[(kind, label)] = per_form.get((kind, label), 0) + 1
    total = sum(per_form.values())
    ticker_spans = per_form.get(("ticker", "UBS"), 0)
    print("spans found in silver under the NEW aliases: %d  per form: %s" % (
        total, {"%s:%s" % k: v for k, v in sorted(per_form.items())}))
    print("carried by the ticker form UBS: %d of %d" % (ticker_spans, total))
    for label, rows in (("SERVED", served[pg.GOLD_TABLE][2]), ("NEW-rebuild", new_t[pg.GOLD_TABLE])):
        mine = [r for r in rows if r["security_key"] == UBS]
        print("  %s mention rows for %s: %d  mention_count sum=%d  match_forms=%s" % (
            label, UBS, len(mine), sum(r["mention_count"] for r in mine), sorted({f for r in mine for f in r["match_forms"]})))
    srv = sorted((C.canon_row(r) for r in served[pg.GOLD_TABLE][2] if r["security_key"] == UBS), key=lambda r: r["article_key"])
    nw = sorted((C.canon_row(r) for r in new_t[pg.GOLD_TABLE] if r["security_key"] == UBS), key=lambda r: r["article_key"])
    print("  UBS mention rows served == new rebuild row by row: %s" % ("EQUAL" if srv == nw else "DIFFERENT"))
    if srv != nw:
        problems.append("UBS mention rows differ served vs new")
    if total != ticker_spans:
        problems.append("UBS spans not all carried by the ticker form")

    print("\nTOTAL across the three tables: ALIAS=%d DRIFT=%d ALIAS+DRIFT=%d; problems: %d" % (
        tot["ALIAS"], tot["DRIFT"], tot["ALIAS+DRIFT"], len(problems)))
    for p in problems:
        print("PROBLEM: %s" % C.a(p))
    print("AC2 RESULT: %s" % ("PASS" if not problems else "FAIL"))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
