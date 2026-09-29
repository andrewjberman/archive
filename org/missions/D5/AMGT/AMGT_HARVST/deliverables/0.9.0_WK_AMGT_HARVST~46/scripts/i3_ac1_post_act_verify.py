"""HVST-i-3 AC1 (read-only; S3 LIST/GET/HEAD and Lambda GetFunctionConfiguration only): THE REBUILD LANDED INSIDE THE
PAIR ON THE SERVED PLANE, read after the act from S3.
 (a) the newest chatter_daily part is the one this cell wrote (ETag, rows; equals the key the act printed), the BEFORE
     state recorded by the dry step equals the halves, and the newest mention and event parts are unchanged (key, ETag);
 (b) every PRE-EXISTING column is equal to the prior newest part on every row, and publishers_covered_codes equals the
     pair's expected values (DENIED [], the 149 PARTIAL rows as named, len == publishers_covered on every row); any cell
     the pair did not name is printed as OUTSIDE THE PAIR and FAILS the run;
 (c) every prior part still exists with its ETag unchanged."""
import collections
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i3_common as G  # noqa: E402

C, pg = G.C, G.pg


def main():
    problems, outside = [], []
    client = G.store._default_client()
    with open(G.BEFORE_JSON, "r", encoding="utf-8") as fh:
        before = json.load(fh)
    print("== HVST-i-3 AC1: THE REBUILD LANDED INSIDE THE PAIR ON THE SERVED PLANE (read from S3 after the act) ==")
    print("BEFORE state recorded by the dry step at %s (file %s)" % (before["recorded_utc"], os.path.relpath(G.BEFORE_JSON, C.REPO)))
    after = G.list_parts(client)

    # ---------------- (a) ----------------
    print("\n== (a) the newest daily part is the one this cell wrote; mention and event unchanged ==")
    bl = before["lambda"]
    print("BEFORE reader 1 CodeSha256=%s (halves %s) -> %s" % (bl["code_sha256"], G.LAMBDA_SHA, "EQUAL" if bl["code_sha256"] == G.LAMBDA_SHA else "DIFFERENT"))
    if bl["code_sha256"] != G.LAMBDA_SHA:
        problems.append("BEFORE reader 1 CodeSha256 differs from the halves")
    sha_now, lm_now = G.lambda_sha()
    print("AFTER  reader 1 CodeSha256=%s LastModified=%s -> %s" % (sha_now, lm_now, "UNCHANGED" if sha_now == G.LAMBDA_SHA else "CHANGED"))
    if sha_now != G.LAMBDA_SHA:
        problems.append("reader 1 CodeSha256 moved during the act")
    new_daily = None
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
        if t == pg.GOLD_DAILY_TABLE:
            rows = G.read_rows(client, newest["key"])
            print("   AFTER  newest: %s etag=%s rows=%d size=%d" % (newest["key"], newest["etag"], len(rows), newest["size"]))
            ok = len(added) == 1 and added[0]["key"] == newest["key"] and newest["key"] != b["newest_key"]
            print("   exactly 1 part added and it is the newest: %s" % ok)
            if not ok:
                problems.append("daily: newest part is not the single part this cell wrote")
            with open(G.ACT_OUTPUT, "r", encoding="utf-8") as fh:
                act = json.loads(fh.read().strip().splitlines()[-1])
            print("   the act printed key=%s rows=%s -> equals newest: %s, rows equal: %s" % (
                act["key"], act["rows"], act["key"] == newest["key"], act["rows"] == len(rows)))
            if act["key"] != newest["key"] or act["rows"] != len(rows):
                problems.append("act output does not match the newest daily part")
            new_daily = {"key": newest["key"], "etag": newest["etag"], "rows": rows, "before_key": b["newest_key"]}
            as_of = G.partition_date(newest["key"])
            print("   as-of date= partition: %s" % as_of)
            if as_of not in ("2026-09-29", "2026-09-30"):
                problems.append("as-of %s outside both halves" % as_of)
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
    print("\n== (b) every pre-existing column equal to the prior newest part; the new column equals the pair ==")
    prior = G.read_rows(client, new_daily["before_key"])
    new = new_daily["rows"]
    pre_cols = [n for n in pg.GOLD_DAILY_SCHEMA.names if n != G.NEW_COL]
    print("prior newest part %s: rows=%d, has the new column: %s" % (new_daily["before_key"], len(prior), G.NEW_COL in prior[0]))
    print("new part columns=%d (schema %d); pre-existing columns=%d; new column present on every new row: %s" % (
        len(new[0]), len(pg.GOLD_DAILY_SCHEMA.names), len(pre_cols), all(G.NEW_COL in r for r in new)))
    p_by = {G.dkey(r): r for r in prior}
    n_by = {G.dkey(r): r for r in new}
    print("denominator: prior rows=%d (distinct keys %d); new rows=%d (distinct keys %d)" % (len(prior), len(p_by), len(new), len(n_by)))
    if len(p_by) != len(prior) or len(n_by) != len(new):
        problems.append("a daily key is not unique")
    if [c for c in new[0] if c not in pre_cols] != [G.NEW_COL] or list(new[0])[:len(pre_cols)] != pre_cols:
        outside.append("column set/order of the new part differs from the 21 + 1")
    prior_last = max(k[1] for k in p_by)
    ext = sorted(k for k in n_by if k not in p_by and k[1] > prior_last)
    other_new = sorted(k for k in n_by if k not in p_by and k[1] <= prior_last)
    removed = sorted(k for k in p_by if k not in n_by)
    moved_cells = collections.Counter()
    moved_rows = 0
    for k in sorted(set(p_by) & set(n_by)):
        diff = [c for c in pre_cols if C.canon(p_by[k].get(c)) != C.canon(n_by[k].get(c))]
        if diff:
            moved_rows += 1
            for c in diff:
                moved_cells[c] += 1
                if moved_cells[c] <= 5:
                    print("   OUTSIDE THE PAIR: %s %s: prior=%s new=%s" % (k, c, C.a(C.canon(p_by[k].get(c))), C.a(C.canon(n_by[k].get(c)))))
            outside.append("pre-existing column(s) %s moved on %s" % (diff, k))
    print("rows present in both: %d; rows with ANY of the 21 pre-existing columns moved: %d (cells by column: %s)" % (
        len(set(p_by) & set(n_by)), moved_rows, dict(moved_cells)))
    print("rows removed=%d; rows new inside the prior range=%d; extension rows (after prior last day %s)=%d" % (
        len(removed), len(other_new), prior_last, len(ext)))
    if removed:
        outside.append("%d rows removed" % len(removed))
    if other_new:
        outside.append("%d rows new inside the prior range" % len(other_new))
    if as_of == "2026-09-29":
        ok = not ext
        print("as-of 2026-09-29: extension rows must be 0 -> %d %s" % (len(ext), "OK" if ok else "OUTSIDE THE PAIR"))
    else:
        ok = len(ext) == 191 and len({k[0] for k in ext}) == 191 and {k[1] for k in ext} == {as_of}
        print("as-of %s: extension rows must be exactly 191 (one day x 191 securities) -> %d %s" % (as_of, len(ext), "OK" if ok else "OUTSIDE THE PAIR"))
    if not ok:
        outside.append("extension rows %d not permitted for as-of %s" % (len(ext), as_of))

    classes = collections.Counter(r["data_status"] for r in new)
    print("new part row counts per data_status: %s (pair: %s)" % (dict(sorted(classes.items())), G.PAIR_CLASSES))
    if as_of == "2026-09-29" and dict(classes) != G.PAIR_CLASSES:
        outside.append("class counts differ from the pair: %s" % dict(classes))
    bad_len = n_named_ok = 0
    partial_seen = collections.defaultdict(list)
    for k, r in sorted(n_by.items()):
        codes = r.get(G.NEW_COL)
        if codes is None or len(codes) != r["publishers_covered"]:
            bad_len += 1
            outside.append("len(codes) != publishers_covered on %s: codes=%s covered=%s" % (k, codes, r["publishers_covered"]))
            continue
        exp = G.PAIR_PARTIAL.get(k[0])
        if k in p_by:
            if r["data_status"] == "PARTIAL":
                if exp is not None and codes == exp[1]:
                    n_named_ok += 1
                    partial_seen[k[0]].append(codes)
                else:
                    outside.append("PARTIAL row %s carries codes %s, the pair names %s" % (k, codes, exp))
            elif codes:
                outside.append("non-empty code list on a non-PARTIAL row %s: %s" % (k, codes))
        else:  # extension row (DRIFT): the same rule; a non-empty list must still be a PARTIAL row of a named security
            if codes and not (r["data_status"] == "PARTIAL" and exp is not None and codes == exp[1]):
                outside.append("extension row %s carries codes %s outside the pair" % (k, codes))
    print("rows where len(publishers_covered_codes) != publishers_covered: %d of %d" % (bad_len, len(n_by)))
    print("PARTIAL rows whose codes equal the pair's named value: %d (pair: 149)" % n_named_ok)
    for sk in sorted(G.PAIR_PARTIAL):
        got = partial_seen.get(sk, [])
        exp_n, exp_codes = G.PAIR_PARTIAL[sk]
        good = len(got) == exp_n and all(c == exp_codes for c in got)
        print("   %-16s PARTIAL days with codes %s: %d (pair: %d x %s) -> %s" % (sk, exp_codes, len(got), exp_n, exp_codes, "as named" if good else "DIFFERS"))
        if not good:
            outside.append("%s PARTIAL rows %d != pair %d" % (sk, len(got), exp_n))
    if n_named_ok != 149:
        outside.append("PARTIAL rows with the named codes %d != 149" % n_named_ok)
    nonempty = sum(1 for r in new if r[G.NEW_COL])
    print("rows with a non-empty code list in the new part: %d (pair: 149)" % nonempty)
    if nonempty != 149:
        outside.append("non-empty code lists %d != 149" % nonempty)

    # ---------------- (c) ----------------
    print("\n== (c) every prior part still exists with its ETag unchanged (HEAD read after the act) ==")
    n_ok = n = nd_ok = nd = 0
    for t in G.TABLES:
        for p in before["tables"][t]["parts"]:
            n += 1
            try:
                e = G.head_etag(client, p["key"])
            except Exception as exc:  # noqa: BLE001
                e = "MISSING(%s)" % type(exc).__name__
            good = e == p["etag"]
            n_ok += int(good)
            if t == pg.GOLD_DAILY_TABLE:
                nd += 1
                nd_ok += int(good)
            if not good:
                problems.append("prior part %s: ETag before %s now %s" % (p["key"], p["etag"], e))
                print("   CHANGED/MISSING %s before=%s now=%s" % (p["key"], p["etag"], e))
    print("prior daily parts with ETag unchanged: %d of %d; prior parts of all three tables with ETag unchanged: %d of %d" % (nd_ok, nd, n_ok, n))

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
