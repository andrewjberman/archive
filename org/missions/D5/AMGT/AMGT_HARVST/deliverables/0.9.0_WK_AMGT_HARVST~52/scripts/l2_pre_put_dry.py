"""HVST-l-2 clause 4: the PRE-PUT dry step. S3 LIST/GET and Lambda GetFunctionConfiguration only (no put, no delete, no
vendor call). Takes NO arguments and will NOT silently rerun: it refuses if l2_before_state.json exists (write-once; a
rerun is a deliberate act, by removing that file in the open; row Z-W45-S4). Records every part of the three tables with
its ETag, the newest per table with its row count, and reader 1's CodeSha256, each beside the halves' value; prints STOP
on any difference. rc 0 only if every comparison is EQUAL."""
import datetime
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l2_common as G  # noqa: E402


def main():
    if len(sys.argv) > 1:
        print("REFUSED: this dry step takes no arguments (got %r)" % sys.argv[1:])
        return 2
    if os.path.exists(G.BEFORE_JSON):
        print("REFUSED: %s already exists; the dry step is write-once and does not rerun silently"
              % os.path.relpath(G.BEFORE_JSON, G.C.REPO))
        return 2
    client = G.store._default_client()
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    print("== HVST-l-2 PRE-PUT DRY STEP (read-only) ==  now UTC date=%s" % today)
    problems = []
    if today not in ("2026-09-29", "2026-09-30"):
        problems.append("today UTC %s is outside both halves (signed 2026-09-30 ~00:1xZ-00:2xZ)" % today)
    sha, lm = G.lambda_sha()
    print("\nREADER 1 %s: CodeSha256=%s LastModified=%s\n   halves CodeSha256   =%s -> %s" % (
        G.LAMBDA_NAME, sha, lm, G.LAMBDA_SHA, "EQUAL" if sha == G.LAMBDA_SHA else "DIFFERENT"))
    if sha != G.LAMBDA_SHA:
        problems.append("reader 1 CodeSha256 differs")
    parts = G.list_parts(client)
    state = {"recorded_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of_candidate": today,
             "lambda": {"name": G.LAMBDA_NAME, "code_sha256": sha, "last_modified": lm}, "tables": {}}
    for t in G.TABLES:
        p = parts[t]
        newest = p[-1]
        rows = G.read_rows(client, newest["key"])
        n_parts, s_key, s_etag, s_rows = G.SECTION3[t]
        print("\n-- %s: parts=%d (halves: %d)" % (t, len(p), n_parts))
        for x in p:
            print("     %s  etag=%s  size=%d" % (x["key"], x["etag"], x["size"]))
        print("   NEWEST key   =%s\n   halves key   =%s   -> %s" % (newest["key"], s_key, "EQUAL" if newest["key"] == s_key else "DIFFERENT"))
        print("   NEWEST etag  =%s\n   halves etag  =%s  -> %s" % (newest["etag"], s_etag, "EQUAL" if newest["etag"] == s_etag else "DIFFERENT"))
        print("   NEWEST rows  =%d  halves rows=%d  -> %s" % (len(rows), s_rows, "EQUAL" if len(rows) == s_rows else "DIFFERENT"))
        if len(p) != n_parts:
            problems.append("%s parts %d != %d" % (t, len(p), n_parts))
        if newest["key"] != s_key:
            problems.append("%s newest key differs" % t)
        if newest["etag"] != s_etag:
            problems.append("%s newest ETag differs" % t)
        if len(rows) != s_rows:
            problems.append("%s newest rows differ" % t)
        state["tables"][t] = {"parts": p, "newest_key": newest["key"], "newest_etag": newest["etag"], "newest_rows": len(rows)}
    with open(G.BEFORE_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(state, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("\nBEFORE state written to %s" % os.path.relpath(G.BEFORE_JSON, G.C.REPO))
    for pr in problems:
        print("PROBLEM: %s" % pr)
    print("PRE-PUT DRY RESULT: %s" % ("EQUAL TO THE HALVES -- clear to put" if not problems else "STOP -- put nothing"))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
