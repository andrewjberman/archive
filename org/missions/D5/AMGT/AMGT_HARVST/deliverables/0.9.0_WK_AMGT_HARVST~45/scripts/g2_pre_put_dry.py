"""HVST-g-2 clause 1.5: the PRE-PUT dry step. S3 LIST/GET only (no put, no delete, no vendor call).
Records the BEFORE state (every part of the three tables with its ETag; the newest per table with its row
count) to g2_before_state.json, and compares it with the COO half's section 3 and the CTO half's --as-of
condition. rc 0 only if every comparison is equal; any difference = STOP, put nothing."""
import datetime
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g2_common as G  # noqa: E402


def main():
    client = G.store._default_client()
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    print("== HVST-g-2 PRE-PUT DRY STEP (read-only) ==  now UTC date=%s" % today)
    problems = []
    if today not in ("2026-09-29", "2026-09-30"):
        problems.append("today UTC %s is outside both halves (2026-09-29 / 2026-09-30)" % today)
    parts = G.list_parts(client)
    state = {"recorded_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of_candidate": today, "tables": {}}
    total = 0
    for t in G.TABLES:
        p = parts[t]
        total += len(p)
        newest = p[-1]
        rows = G.read_rows(client, newest["key"])
        n_parts, s_key, s_etag, s_rows = G.SECTION3[t]
        print("\n-- %s: parts=%d (section 3: %d)" % (t, len(p), n_parts))
        for x in p:
            print("     %s  etag=%s  size=%d" % (x["key"], x["etag"], x["size"]))
        print("   NEWEST key   =%s\n   section 3 key=%s   -> %s" % (newest["key"], s_key, "EQUAL" if newest["key"] == s_key else "DIFFERENT"))
        print("   NEWEST etag  =%s\n   section 3 etag=%s  -> %s" % (newest["etag"], s_etag, "EQUAL" if newest["etag"] == s_etag else "DIFFERENT"))
        print("   NEWEST rows  =%d  section 3 rows=%d  -> %s" % (len(rows), s_rows, "EQUAL" if len(rows) == s_rows else "DIFFERENT"))
        if len(p) != n_parts:
            problems.append("%s parts %d != %d" % (t, len(p), n_parts))
        if newest["key"] != s_key:
            problems.append("%s newest key differs" % t)
        if newest["etag"] != s_etag:
            problems.append("%s newest ETag differs" % t)
        if len(rows) != s_rows:
            problems.append("%s newest rows differ" % t)
        state["tables"][t] = {"parts": p, "newest_key": newest["key"], "newest_etag": newest["etag"], "newest_rows": len(rows)}
    print("\nprior parts in all: %d (section 3: 18)" % total)
    if total != 18:
        problems.append("total parts %d != 18" % total)
    with open(G.BEFORE_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(state, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("BEFORE state written to %s" % os.path.relpath(G.BEFORE_JSON, G.C.REPO))
    for pr in problems:
        print("PROBLEM: %s" % pr)
    print("PRE-PUT DRY RESULT: %s" % ("EQUAL TO SECTION 3 -- clear to put" if not problems else "STOP -- put nothing"))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
