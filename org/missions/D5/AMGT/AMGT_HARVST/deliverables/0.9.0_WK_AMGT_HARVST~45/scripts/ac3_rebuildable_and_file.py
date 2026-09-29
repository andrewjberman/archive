"""HVST-g-1 AC3: (1) the securities file equals a fresh universe_securities.build() at HEAD; (2) every entry of the
whole-brand file carries its census citation; (3) two in-memory builds of mention, daily and event from the same
inputs are equal row by row. S3 GET/LIST only: no put, no delete, no vendor call."""
import datetime
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402


def main():
    problems = []
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=C.REPO, capture_output=True, text=True).stdout.strip()
    print("== HVST-g-1 AC3: rebuildable + whole-brand file + determinism ==  (git HEAD %s; the rule code is the working tree's)" % head)

    # ---- (1) file == fresh build ------------------------------------------------------------------------
    print("\n-- (1) securities.universe.json vs a fresh universe_securities.build() --")
    fresh, summary = us.build()
    fresh_json = json.loads(json.dumps(fresh, sort_keys=True))
    on_disk = C.load_json(C.NEW_PATH)
    print("universe read: %s  as_of=%s  names_read=%d  securities: file=%d fresh=%d" % (
        summary["universe"].get("source"), summary["universe"].get("as_of"), summary["names_read"], len(on_disk), len(fresh_json)))
    equal = fresh_json == on_disk
    print("file == fresh build (whole list equality, every field of every security): %s" % equal)
    if not equal:
        f_by, d_by = C.sec_map(fresh_json), C.sec_map(on_disk)
        for k in sorted(set(f_by) | set(d_by)):
            if f_by.get(k) != d_by.get(k):
                print("  DIFF %s: file=%s fresh=%s" % (k, d_by.get(k), f_by.get(k)))
        problems.append("securities file differs from a fresh build")
    print("summary: ticker_aliases_added=%d of %d; refused by reason=%s; whole_brand admitted=%d refused=%d already=%d not_in_universe=%s" % (
        summary["ticker_aliases_added"], summary["securities"], summary["ticker_forms_refused_by_reason"],
        len(summary["whole_brand_admitted"]), len(summary["whole_brand_refused"]),
        len(summary["whole_brand_already_an_alias"]), summary["whole_brand_not_in_universe"]))
    for r in summary["whole_brand_refused"]:
        print("  whole-brand entry REFUSED in code: %s" % json.dumps(r, sort_keys=True))
    for r in summary["whole_brand_admitted"]:
        print("  whole-brand entry admitted: %s" % json.dumps(r, sort_keys=True))
    print("ticker forms refused, named: %s" % json.dumps(summary["ticker_forms_refused_named"], sort_keys=True))

    # ---- (2) every entry cites its census ---------------------------------------------------------------
    print("\n-- (2) whole_brand_aliases.json: every entry carries its census citation --")
    rule = C.load_json(C.BRAND_PATH)
    total = missing = 0
    for section in ("whole_brands", "ticker_refusals", "parent_brand_refusals"):
        n_sec = len(rule[section])
        bad = [e for e in rule[section] if not str(e.get("census") or "").strip()]
        total += n_sec
        missing += len(bad)
        print("  %-22s entries=%d without census=%d  %s" % (section, n_sec, len(bad),
                                                            [e.get("brand") or e.get("ticker") for e in rule[section]]))
    print("entries with a census citation: %d of %d" % (total - missing, total))
    if missing:
        problems.append("%d entries lack a census citation" % missing)
    for e in rule["whole_brands"]:
        cited = "ADJUDICATION_v25" in e["census"] and "ac1_output.txt" in e["census"]
        print("  %-16s %-8s cites ac1_output.txt + ADJUDICATION_v25: %s" % (e["security_key"], e["brand"], cited))
        if not cited:
            problems.append("brand %s does not cite both census sources" % e["brand"])

    # ---- (3) determinism: two in-memory builds equal row by row ----------------------------------------
    print("\n-- (3) two in-memory builds from the same inputs, equal row by row --")
    articles, hits, _served = C.fetch()
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    print("inputs: silver articles=%d listing_hit rows=%d securities=%d as_of=%s" % (len(articles), len(hits), len(on_disk), as_of))
    one, _e1 = C.build_memory(on_disk, articles, hits, as_of)
    two, _e2 = C.build_memory(on_disk, articles, hits, as_of)
    for table in (pg.GOLD_TABLE, pg.GOLD_DAILY_TABLE, pg.GOLD_EVENT_TABLE):
        a_rows = [C.canon_row(r) for r in one[table]]
        b_rows = [C.canon_row(r) for r in two[table]]
        row_equal = len(a_rows) == len(b_rows) and all(x == y for x, y in zip(a_rows, b_rows))
        unequal = sum(1 for x, y in zip(a_rows, b_rows) if x != y)
        print("  %-26s build1=%d rows build2=%d rows  rows unequal=%d  ->  %s" % (
            table, len(a_rows), len(b_rows), unequal, "EQUAL row by row" if row_equal else "NOT EQUAL"))
        if not row_equal:
            problems.append("%s: two builds differ" % table)

    for p in problems:
        print("PROBLEM: %s" % C.a(p))
    print("AC3 RESULT: %s" % ("PASS" if not problems else "FAIL"))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
