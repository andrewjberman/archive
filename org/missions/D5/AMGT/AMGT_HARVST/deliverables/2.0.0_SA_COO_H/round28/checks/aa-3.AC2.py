"""HVST-aa-3 AC2 (issuer check, read-only): the rebuilt bbg rows are SERVED non-empty, and the 11 kept hash-keyed empty
rows are INERT (CTO ruling @803ea38a9e: keep them, no delete, no reader filter; any empty row reachable from a served
list is a STOP).

PASS requires, read through the merged `store.silver_latest`:
- served bbg keys = before + the signed NEW keys; every NEW row has a non-empty title AND >= 1 text block;
- every pre-existing key's served record_hash is unchanged (the 11 empty rows are KEPT, not rewritten);
- INERT: the served `article_security_mention` snapshot holds 0 pairs whose article_key is an empty bbg row -- the
  snapshot is what `/timeline/day` lists and what the company query joins, so 0 here means no served list reaches them;
- STOP guard: every bbg pair in the served mention snapshot maps to a NON-empty served silver row;
- idempotence: a re-run of the rebuild would write 0 rows.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aa3_common as c  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402


def empty(row):
    return not (row.get("title") or "").strip() or not (row.get("text_blocks") or [])


def main():
    failures = []
    before = c.load(os.path.join(c.WK, "aa3_before.json"))
    cl = c.client()
    latest, hashes = c.latest_hashes(cl)
    new = {t[1]: t[3] for t in before["expected_write"] if t[0] == "NEW"}
    want = set(before["latest_record_hash"]) | set(new)
    print("served bbg keys: before %d, after %d, expected %d" % (len(before["latest_record_hash"]), len(hashes), len(want)))
    if set(hashes) != want:
        failures.append("served keys differ from expected (+%d / -%d)" % (len(set(hashes) - want), len(want - set(hashes))))
    ok_new = [k for k in new if hashes.get(k) == new[k] and not empty(latest.get((k,), {}))]
    print("NEW rows served non-empty with the rebuilt hash: %d of %d" % (len(ok_new), len(new)))
    if len(ok_new) != len(new):
        failures.append("NEW rows served non-empty: %d of %d" % (len(ok_new), len(new)))
    changed = [k for k in before["latest_record_hash"] if hashes.get(k) != before["latest_record_hash"][k]]
    print("pre-existing keys unchanged: %d of %d" % (len(before["latest_record_hash"]) - len(changed), len(before["latest_record_hash"])))
    if changed:
        failures.append("%d pre-existing key(s) changed (first %s)" % (len(changed), changed[0]))
    empty_keys = sorted(k[0] for k, r in latest.items() if empty(r))
    print("empty bbg rows served (kept by ruling): %d" % len(empty_keys))
    mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    reach = [r for r in mention if r.get("article_key") in set(empty_keys)]
    print("INERT: served mention pairs on an empty bbg row: %d (0 = absent from /timeline/day and the company query)" % len(reach))
    if reach:
        failures.append("STOP: %d served mention pair(s) reach an empty bbg row (first %s)" % (len(reach), reach[0].get("article_key")))
    bbg_pairs = [r for r in mention if str(r.get("article_key", "")).startswith("bbg:")]
    unbacked = [r for r in bbg_pairs if (r.get("article_key"),) not in latest or empty(latest[(r.get("article_key"),)])]
    print("STOP guard: bbg mention pairs %d, on an empty or missing silver row %d" % (len(bbg_pairs), len(unbacked)))
    if unbacked:
        failures.append("STOP: %d bbg mention pair(s) on an empty or missing silver row" % len(unbacked))
    again = c.expected_write(c.rebuilt_rows(cl), latest)
    print("idempotence: a re-run would write %d row(s)" % len(again))
    if again:
        failures.append("a re-run would still write %d row(s)" % len(again))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
