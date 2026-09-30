"""HVST-l-2 AC1 (read-only; S3 LIST/GET/HEAD and Lambda GetFunctionConfiguration only): THE REBUILD LANDED INSIDE THE
PAIR ON THE SERVED PLANE, read after the act from S3.
 (a) the newest chatter_event part is the one this cell wrote (ETag, rows; equals the key the act printed), the BEFORE
     state recorded by the dry step equals the halves, and the newest mention and daily parts are unchanged (key, ETag);
 (b) every served event is mapped to what it became (KEPT / CHANGED / MERGED / GONE) against the pair's expected diff;
     any event the pair did not name (a different verdict, a field off the pair, a NEW event) is printed as OUTSIDE THE
     PAIR and FAILS the run;
 (c) every event_id is unique;
 (d) every prior part of the three tables still exists with its ETag unchanged."""
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l2_common as G  # noqa: E402

C, pg = G.C, G.pg


def main():
    problems, outside = [], []
    client = G.store._default_client()
    with open(G.BEFORE_JSON, "r", encoding="utf-8") as fh:
        before = json.load(fh)
    print("== HVST-l-2 AC1: THE REBUILD LANDED INSIDE THE PAIR ON THE SERVED PLANE (read from S3 after the act) ==")
    print("BEFORE state recorded by the dry step at %s (file %s)" % (before["recorded_utc"], os.path.relpath(G.BEFORE_JSON, C.REPO)))
    after = G.list_parts(client)

    # ---------------- (a) ----------------
    print("\n== (a) the newest event part is the one this cell wrote; mention and daily unchanged ==")
    bl = before["lambda"]
    print("BEFORE reader 1 CodeSha256=%s (halves %s) -> %s" % (bl["code_sha256"], G.LAMBDA_SHA, "EQUAL" if bl["code_sha256"] == G.LAMBDA_SHA else "DIFFERENT"))
    if bl["code_sha256"] != G.LAMBDA_SHA:
        problems.append("BEFORE reader 1 CodeSha256 differs from the halves")
    sha_now, lm_now = G.lambda_sha()
    print("AFTER  reader 1 CodeSha256=%s LastModified=%s -> %s" % (sha_now, lm_now, "UNCHANGED" if sha_now == G.LAMBDA_SHA else "CHANGED"))
    if sha_now != G.LAMBDA_SHA:
        problems.append("reader 1 CodeSha256 moved during the act")
    new_part = None
    for t in G.TABLES:
        b = before["tables"][t]
        b_keys = {p["key"] for p in b["parts"]}
        added = [p for p in after[t] if p["key"] not in b_keys]
        newest = after[t][-1]
        n_parts, s_key, s_etag, s_rows = G.SECTION3[t]
        before_eq = (b["newest_key"] == s_key and b["newest_etag"] == s_etag and b["newest_rows"] == s_rows and len(b["parts"]) == n_parts)
        print("%s: parts before=%d after=%d; parts added=%d" % (t, len(b["parts"]), len(after[t]), len(added)))
        print("   BEFORE newest: %s etag=%s rows=%d -> equals the halves: %s" % (b["newest_key"], b["newest_etag"], b["newest_rows"], before_eq))
        if not before_eq:
            problems.append("%s: BEFORE state differs from the halves" % t)
        if t == pg.GOLD_EVENT_TABLE:
            rows = G.read_rows(client, newest["key"])
            print("   AFTER  newest: %s etag=%s rows=%d size=%d" % (newest["key"], newest["etag"], len(rows), newest["size"]))
            ok = len(added) == 1 and added[0]["key"] == newest["key"] and newest["key"] != b["newest_key"]
            print("   exactly 1 part added and it is the newest: %s" % ok)
            if not ok:
                problems.append("event: newest part is not the single part this cell wrote")
            with open(G.ACT_OUTPUT, "r", encoding="utf-8") as fh:
                act = json.loads(fh.read().strip().splitlines()[-1])
            print("   the act printed key=%s events=%s -> equals newest: %s, rows equal: %s" % (
                act["key"], act["events"], act["key"] == newest["key"], act["events"] == len(rows)))
            if act["key"] != newest["key"] or act["events"] != len(rows):
                problems.append("act output does not match the newest event part")
            as_of = G.partition_date(newest["key"])
            print("   as-of date= partition: %s" % as_of)
            if as_of not in ("2026-09-29", "2026-09-30"):
                problems.append("as-of %s outside both halves" % as_of)
            new_part = {"key": newest["key"], "etag": newest["etag"], "rows": rows, "before_key": b["newest_key"]}
        else:
            unchanged = (len(added) == 0 and newest["key"] == b["newest_key"] and newest["etag"] == b["newest_etag"])
            print("   AFTER  newest: %s etag=%s -> parts added 0, key and ETag unchanged: %s" % (newest["key"], newest["etag"], unchanged))
            if not unchanged:
                problems.append("%s moved" % t)
    total_after = sum(len(after[t]) for t in G.TABLES)
    total_before = sum(len(before["tables"][t]["parts"]) for t in G.TABLES)
    print("total parts under the three prefixes: before=%d after=%d (1 put expected)" % (total_before, total_after))
    if total_after != total_before + 1:
        problems.append("total parts after != before + 1")

    # ---------------- (b) ----------------
    print("\n== (b) every served event mapped to what it became, against the pair's expected diff ==")
    served = G.read_rows(client, new_part["before_key"])
    new = new_part["rows"]
    print("served (BEFORE newest) event part %s: %d events; new part: %d events" % (new_part["before_key"], len(served), len(new)))
    mapped, unclaimed = G.map_events(served, new)
    counts = {}
    n_expected_matched = 0
    for s, verdict, tg in mapped:
        counts[verdict] = counts.get(verdict, 0) + 1
        k = G.ekey(s)
        exp = G.EXPECTED.get(k, "UNNAMED")
        head = "%-7s %s %s..%s n=%s id=%s" % (verdict, k[0], k[1], k[2], s.get("articles_total"), s["event_id"][:12])
        if verdict in ("KEPT",):
            print(head)
            if exp is not None:
                outside.append("%s %s..%s became KEPT, the pair names %s" % (k[0], k[1], k[2], "an event not in the pair" if exp == "UNNAMED" else "CHANGED"))
            else:
                n_expected_matched += 1
            continue
        t = tg[0] if tg else None
        print(head)
        if t is not None:
            print("    -> %s..%s n=%s id %s -> %s lead=%r" % (t["first_day"], t["last_day"], t.get("articles_total"),
                                                         s["event_id"][:12], t["event_id"][:12], C.a(t.get("lead_headline") or "", 80)))
        if verdict != "CHANGED" or exp in (None, "UNNAMED"):
            outside.append("OUTSIDE THE PAIR: %s %s..%s became %s (pair: %s)" % (k[0], k[1], k[2], verdict, "KEPT" if exp is None else "not named"))
            continue
        f0, l0, n0, oid, nid, lead0 = exp
        got = (C.canon(t["first_day"]), C.canon(t["last_day"]), t.get("articles_total"), s["event_id"][:12], t["event_id"][:12],
               (t.get("lead_headline") or "").startswith(lead0))
        want = (f0, l0, n0, oid, nid, True)
        print("    pair says: %s..%s n=%s id %s -> %s lead startswith %r -> %s" % (f0, l0, n0, oid, nid, lead0, "AS NAMED" if got == want else "DIFFERS got=%s" % (got,)))
        if got == want:
            n_expected_matched += 1
        else:
            outside.append("OUTSIDE THE PAIR: %s %s..%s changed, but not as the pair names: got %s want %s" % (k[0], k[1], k[2], got, want))
    for e in unclaimed:
        print("NEW     %s %s..%s n=%s id=%s lead=%r" % (e["security_key"], e["first_day"], e["last_day"], e.get("articles_total"), e["event_id"][:12], C.a(e.get("lead_headline") or "", 70)))
        outside.append("OUTSIDE THE PAIR: NEW event %s %s..%s" % (e["security_key"], e["first_day"], e["last_day"]))
    print("COUNTS served=%d %s NEW=%d new-part events=%d; served events matching the pair: %d of %d" % (
        len(served), " ".join("%s=%d" % (v, counts.get(v, 0)) for v in ("KEPT", "CHANGED", "MERGED", "SPLIT", "GONE")),
        len(unclaimed), len(new), n_expected_matched, len(G.EXPECTED)))
    named_missing = [k for k in G.EXPECTED if k not in {G.ekey(s) for s in served}]
    if named_missing:
        outside.append("pair-named served event(s) absent from the served part: %s" % named_missing)
    if (counts.get("KEPT", 0), counts.get("CHANGED", 0), counts.get("GONE", 0), len(unclaimed)) != (5, 3, 0, 0):
        outside.append("counts KEPT/CHANGED/GONE/NEW %s != pair 5/3/0/0" % ((counts.get("KEPT", 0), counts.get("CHANGED", 0), counts.get("GONE", 0), len(unclaimed)),))

    # ---------------- (c) ----------------
    print("\n== (c) every event_id is unique ==")
    ids = [r["event_id"] for r in new]
    print("event_ids in the new part: %d, distinct: %d -> %s" % (len(ids), len(set(ids)), "UNIQUE" if len(ids) == len(set(ids)) else "DUPLICATES"))
    if len(ids) != len(set(ids)):
        problems.append("duplicate event_id in the new part")

    # ---------------- (d) ----------------
    print("\n== (d) every prior part still exists with its ETag unchanged (HEAD read after the act) ==")
    n_ok = n = ne_ok = ne = 0
    for t in G.TABLES:
        for p in before["tables"][t]["parts"]:
            n += 1
            try:
                e = G.head_etag(client, p["key"])
            except Exception as exc:  # noqa: BLE001
                e = "MISSING(%s)" % type(exc).__name__
            good = e == p["etag"]
            n_ok += int(good)
            if t == pg.GOLD_EVENT_TABLE:
                ne += 1
                ne_ok += int(good)
            if not good:
                problems.append("prior part %s: ETag before %s now %s" % (p["key"], p["etag"], e))
                print("   CHANGED/MISSING %s before=%s now=%s" % (p["key"], p["etag"], e))
    print("prior event parts with ETag unchanged: %d of %d; prior parts of all three tables with ETag unchanged: %d of %d" % (ne_ok, ne, n_ok, n))

    print("\nOUTSIDE THE PAIR rows: %d" % len(outside))
    for o in outside[:60]:
        print("   OUTSIDE THE PAIR: %s" % C.a(o))
    for p in problems:
        print("PROBLEM: %s" % C.a(p))
    ok = not problems and not outside
    print("AC1 RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
