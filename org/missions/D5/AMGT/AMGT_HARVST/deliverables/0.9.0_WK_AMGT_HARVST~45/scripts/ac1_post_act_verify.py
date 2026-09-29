"""HVST-g-2 AC1 (read-only, S3 LIST/GET/HEAD only): THE REBUILD LANDED INSIDE THE PAIR ON THE SERVED PLANE.
Reads, after the act, from S3: (a) the newest part per table (the one this cell wrote) with its ETag and row count,
and the BEFORE state recorded by the dry step; (b) the moved rows per table set against the pair's expected diff
(the COO's g2_signing_ac2_rerun.txt): every moved security named, any row the pair did not name printed as
OUTSIDE THE PAIR; (c) every served event mapped to kept / moved / gone, and every new event named; (d) every
event_id unique; (e) every prior part still exists with its ETag unchanged."""
import ast
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g2_common as G  # noqa: E402

C, pg = G.C, G.pg


def parse_pair(path):
    """From the pair's expected-diff file: mention (security, headline90) multiset, daily per-security expectation,
    the daily columns dict, and the headline totals."""
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    mention = collections.Counter()
    for ln in lines:
        m = re.match(r"^  \[ALIAS\] (\S+) \| (.*?) \| forms hit: ", ln)
        if m:
            mention[(m.group(1), m.group(2))] += 1
    daily, cols_total, in_b = {}, None, False
    for ln in lines:
        if ln.startswith("-- per security the cells that move"):
            in_b = True
            continue
        if in_b and ln.startswith("securities with DRIFT cells"):
            in_b = False
        if in_b:
            m = re.match(r"^  (\S+)\s+cells=(\d+)\s+(\S+)\.\.(\S+) columns=(\[.*?\])\s+\(DRIFT", ln)
            if m:
                daily[m.group(1)] = (int(m.group(2)), m.group(3), m.group(4), sorted(ast.literal_eval(m.group(5))))
        m = re.match(r"^ALIAS moved cells \(new vs old\): (\d+) cells across (\d+) securities; columns moved: (\{.*\})$", ln)
        if m:
            cols_total = (int(m.group(1)), int(m.group(2)), ast.literal_eval(m.group(3)))
    return mention, daily, cols_total


def main():
    problems, outside = [], []
    client = G.store._default_client()
    with open(G.BEFORE_JSON, "r", encoding="utf-8") as fh:
        before = json.load(fh)
    exp_mention, exp_daily, exp_cols = parse_pair(G.SIGNING_RERUN)
    print("== HVST-g-2 AC1: THE REBUILD LANDED INSIDE THE PAIR ON THE SERVED PLANE (read from S3 after the act) ==")
    print("pair's expected diff: %s  (mention rows named=%d over %d securities; daily securities named=%d, cells=%s)" % (
        os.path.relpath(G.SIGNING_RERUN, C.REPO), sum(exp_mention.values()), len({k[0] for k in exp_mention}),
        len(exp_daily), exp_cols[0] if exp_cols else None))
    print("BEFORE state recorded by the dry step at %s (file %s)" % (before["recorded_utc"], os.path.relpath(G.BEFORE_JSON, C.REPO)))
    after = G.list_parts(client)

    # ---------------- (a) newest part per table ----------------
    print("\n== (a) per table the newest part is the one this cell wrote ==")
    new_part = {}
    as_of_parts = set()
    for t in G.TABLES:
        b = before["tables"][t]
        b_keys = {p["key"] for p in b["parts"]}
        added = [p for p in after[t] if p["key"] not in b_keys]
        newest = after[t][-1]
        n_parts, s_key, s_etag, s_rows = G.SECTION3[t]
        before_eq = (b["newest_key"] == s_key and b["newest_etag"] == s_etag and b["newest_rows"] == s_rows and len(b["parts"]) == n_parts)
        rows = G.read_rows(client, newest["key"])
        print("%s: parts before=%d after=%d; parts added by this cell=%d" % (t, len(b["parts"]), len(after[t]), len(added)))
        print("   BEFORE newest: %s etag=%s rows=%d -> equals COO half section 2/3: %s" % (b["newest_key"], b["newest_etag"], b["newest_rows"], before_eq))
        print("   AFTER  newest: %s etag=%s rows=%d size=%d" % (newest["key"], newest["etag"], len(rows), newest["size"]))
        ok = len(added) == 1 and added[0]["key"] == newest["key"]
        print("   the newest part is the one this cell wrote (exactly 1 added, and it is newest): %s" % ok)
        if not before_eq:
            problems.append("%s: BEFORE state differs from section 3" % t)
        if not ok:
            problems.append("%s: newest part is not the single part this cell wrote" % t)
        new_part[t] = {"key": newest["key"], "etag": newest["etag"], "rows": rows, "before_key": b["newest_key"]}
        as_of_parts.add(G.partition_date(newest["key"]))
    total_after = sum(len(after[t]) for t in G.TABLES)
    print("total parts under the three prefixes: before=18 after=%d (3 puts expected -> 21)" % total_after)
    if total_after != 21:
        problems.append("total parts after != 21")
    as_of = sorted(as_of_parts)
    print("as-of date= partitions of the three new parts: %s" % as_of)
    if len(as_of) != 1 or as_of[0] not in ("2026-09-29", "2026-09-30"):
        problems.append("as-of outside both halves: %s" % as_of)
    as_of = as_of[0] if as_of else None

    title_of = {r["article_key"]: r.get("title") for r in pg._iter_latest_articles(client=client)}

    # ---------------- (b) moved rows vs the pair ----------------
    print("\n== (b) moved rows per table, set against the pair's expected diff ==")
    b_m = {(r["article_key"], r["security_key"]): r for r in G.read_rows(client, new_part[pg.GOLD_TABLE]["before_key"])}
    a_m = {(r["article_key"], r["security_key"]): r for r in new_part[pg.GOLD_TABLE]["rows"]}
    moved = sorted(k for k in set(b_m) | set(a_m) if C.canon(b_m.get(k)) != C.canon(a_m.get(k)))
    left = collections.Counter(exp_mention)
    sec_moved = collections.Counter()
    print("-- article_security_mention: rows before=%d after=%d; moved (added/changed/removed)=%d; pair names %d" % (
        len(b_m), len(a_m), len(moved), sum(exp_mention.values())))
    n_outside_m = 0
    for k in moved:
        name = (k[1], C.a(title_of.get(k[0]), 90))
        sec_moved[k[1]] += 1
        kind = "REMOVED" if k not in a_m else ("ADDED" if k not in b_m else "CHANGED")
        if k not in a_m or left[name] <= 0:
            n_outside_m += 1
            outside.append("mention %s %s | %s" % (kind, k[1], name[1]))
            print("   OUTSIDE THE PAIR: %s %s | %s" % (kind, k[1], name[1]))
        else:
            left[name] -= 1
    unmoved_named = sum(v for v in left.values() if v > 0)
    print("   moved mention rows named by the pair: %d of %d moved; pair-named rows that did NOT move: %d" % (
        len(moved) - n_outside_m, len(moved), unmoved_named))
    if unmoved_named:
        problems.append("%d mention rows the pair named did not move" % unmoved_named)
        for name, v in left.items():
            if v > 0:
                print("   PAIR-NAMED BUT NOT MOVED: %s | %s x%d" % (name[0], name[1], v))
    exp_sec_counts = collections.Counter(k[0] for k in exp_mention.elements())
    print("   moved securities (%d), rows moved per security [pair-named]: %s" % (
        len(sec_moved), ", ".join("%s=%d[%d]" % (s, n, exp_sec_counts[s]) for s, n in sorted(sec_moved.items()))))
    if len(moved) != 186:
        problems.append("moved mention rows %d != 186" % len(moved))
    # daily
    b_d = {(r["security_key"], r["day"]): r for r in G.read_rows(client, new_part[pg.GOLD_DAILY_TABLE]["before_key"])}
    a_d = {(r["security_key"], r["day"]): r for r in new_part[pg.GOLD_DAILY_TABLE]["rows"]}
    b_last = max(k[1] for k in b_d)
    moved_d = [k for k in set(b_d) | set(a_d) if C.canon(b_d.get(k)) != C.canon(a_d.get(k))]
    ext = [k for k in moved_d if k not in b_d and k[1] > b_last]
    removed_d = [k for k in moved_d if k not in a_d]
    changed_d = [k for k in moved_d if k in b_d and k in a_d]
    other_new = [k for k in moved_d if k not in b_d and k[1] <= b_last]
    print("-- chatter_daily: cells before=%d after=%d (BEFORE last day %s); moved=%d = changed %d + extension %d + removed %d + other-new %d" % (
        len(b_d), len(a_d), b_last, len(moved_d), len(changed_d), len(ext), len(removed_d), len(other_new)))
    per_sec, cols, cols_by_sec = collections.defaultdict(list), collections.Counter(), collections.defaultdict(set)
    for k in changed_d:
        per_sec[k[0]].append(k[1].isoformat())
        for f in C.diff_fields(b_d[k], a_d[k]):
            cols[f] += 1
            cols_by_sec[k[0]].add(f)
    for sec in sorted(per_sec, key=lambda s: (-len(per_sec[s]), s)):
        days = sorted(per_sec[sec])
        got = (len(days), days[0], days[-1], sorted(cols_by_sec[sec]))
        exp = exp_daily.get(sec)
        if exp is None:
            tag = "OUTSIDE THE PAIR (security not among the pair's %d)" % len(exp_daily)
            outside.append("daily security %s: %d cells" % (sec, len(days)))
        elif exp != got:
            tag = "DIFFERS FROM THE PAIR: expected %s" % (exp,)
            outside.append("daily security %s differs from the pair's expectation" % sec)
        else:
            tag = "as named by the pair"
        print("   %-22s cells=%-4d %s..%s columns=%s -> %s" % (sec, got[0], got[1], got[2], got[3], tag))
    missing = sorted(set(exp_daily) - set(per_sec))
    print("   pair-named securities whose daily cells did not move: %d %s" % (len(missing), missing))
    if missing:
        problems.append("pair-named daily securities did not move: %s" % missing)
    print("   changed cells=%d across %d securities (pair: %d across %d); columns moved: %s (pair: %s)" % (
        len(changed_d), len(per_sec), exp_cols[0], exp_cols[1], dict(sorted(cols.items())), exp_cols[2]))
    if dict(cols) != exp_cols[2] or len(changed_d) != exp_cols[0]:
        outside.append("daily columns/cell totals differ from the pair")
    if "FDX_US_Equity" in per_sec:
        print("   FDX_US_Equity daily cells moved: %d -> OUTSIDE THE PAIR" % len(per_sec["FDX_US_Equity"]))
    if removed_d or other_new:
        outside.append("daily cells removed=%d / new-inside-range=%d" % (len(removed_d), len(other_new)))
        print("   OUTSIDE THE PAIR: %d daily cells REMOVED, %d NEW inside the served range" % (len(removed_d), len(other_new)))
    if as_of == "2026-09-29":
        ok = not ext
        print("   as-of 2026-09-29: extension rows must be 0 -> %d %s" % (len(ext), "OK" if ok else "OUTSIDE THE PAIR"))
    else:
        ok = len(ext) == 191 and len({k[0] for k in ext}) == 191 and {k[1].isoformat() for k in ext} == {as_of}
        print("   as-of %s: extension rows must be exactly 191 (one day x 191 securities) -> %d %s" % (as_of, len(ext), "OK" if ok else "OUTSIDE THE PAIR"))
    if not ok:
        outside.append("daily extension rows %d not permitted for as-of %s" % (len(ext), as_of))

    # ---------------- (c) events ----------------
    print("\n== (c) every served event mapped to what it became ==")
    b_e = {r["event_id"]: r for r in G.read_rows(client, new_part[pg.GOLD_EVENT_TABLE]["before_key"])}
    a_e = {r["event_id"]: r for r in new_part[pg.GOLD_EVENT_TABLE]["rows"]}
    fates = collections.Counter()
    for eid in sorted(b_e, key=lambda i: (b_e[i]["security_key"], b_e[i]["first_day"], i)):
        s = b_e[eid]
        if eid not in a_e:
            fate = "gone"
        else:
            fate = "moved" if C.diff_fields(s, a_e[eid]) else "kept"
        fates[fate] += 1
        print("   SERVED %-5s %-18s %s..%s id=%s | %s" % (fate, s["security_key"], s["first_day"], s["last_day"], eid[:12], C.a(s["lead_headline"], 80)))
        if fate != "kept":
            outside.append("event %s %s" % (fate, eid))
    new_ev = [a_e[i] for i in a_e if i not in b_e]
    print("   served events %d -> kept=%d moved=%d gone=%d; NEW events=%d" % (len(b_e), fates["kept"], fates["moved"], fates["gone"], len(new_ev)))
    for e in new_ev:
        outside.append("event NEW %s" % e["event_id"])
        print("   NEW event OUTSIDE THE PAIR: %s %s..%s id=%s | %s" % (e["security_key"], e["first_day"], e["last_day"], e["event_id"][:12], C.a(e["lead_headline"], 80)))
    if len(a_e) != 8:
        problems.append("event count after %d != 8" % len(a_e))

    # ---------------- (d) uniqueness ----------------
    print("\n== (d) key uniqueness in the NEW newest parts ==")
    ids = [r["event_id"] for r in new_part[pg.GOLD_EVENT_TABLE]["rows"]]
    print("   event_id: %d events, %d distinct -> %s" % (len(ids), len(set(ids)), "UNIQUE" if len(ids) == len(set(ids)) else "DUPLICATE"))
    mk = [(r["article_key"], r["security_key"]) for r in new_part[pg.GOLD_TABLE]["rows"]]
    dk = [(r["security_key"], r["day"]) for r in new_part[pg.GOLD_DAILY_TABLE]["rows"]]
    print("   mention (article, security): %d rows, %d distinct -> %s" % (len(mk), len(set(mk)), "UNIQUE" if len(mk) == len(set(mk)) else "DUPLICATE"))
    print("   daily (security, day): %d rows, %d distinct -> %s" % (len(dk), len(set(dk)), "UNIQUE" if len(dk) == len(set(dk)) else "DUPLICATE"))
    if len(ids) != len(set(ids)) or len(mk) != len(set(mk)) or len(dk) != len(set(dk)):
        problems.append("a key is not unique")

    # ---------------- (e) prior parts ----------------
    print("\n== (e) every prior part still exists with its ETag unchanged (HEAD read after the act) ==")
    n_ok = n = 0
    for t in G.TABLES:
        for p in before["tables"][t]["parts"]:
            n += 1
            try:
                e = G.head_etag(client, p["key"])
            except Exception as exc:  # noqa: BLE001
                e = "MISSING(%s)" % type(exc).__name__
            good = e == p["etag"]
            n_ok += int(good)
            if not good:
                problems.append("prior part %s: ETag before %s now %s" % (p["key"], p["etag"], e))
                print("   CHANGED/MISSING %s before=%s now=%s" % (p["key"], p["etag"], e))
    print("   prior parts with ETag unchanged: %d of %d" % (n_ok, n))

    print("\nOUTSIDE THE PAIR rows: %d" % len(outside))
    for o in outside:
        print("   OUTSIDE THE PAIR: %s" % C.a(o))
    for p in problems:
        print("PROBLEM: %s" % C.a(p))
    ok = not problems and not outside
    print("AC1 RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
