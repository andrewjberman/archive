"""IRPT_DASHBD round 76 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 5721.

Cells: DB-b-143 the ORIGINAL Black Diamond transactions store's shape on one day (a transaction once per id, or once per id and
portfolio group), and, only if it repeats, every reader of it in the workspace, portal, opal_ai and mcportal, classed as keyed on the id
or not; DB-b-144 (row D2-W114-S1) "59 of 90 tie" re-derived with each transaction id counted once.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB76-1-AC1  ~116/ORIGINAL_STORE_SHAPE.json: shape {read (bool), day, rows, distinct_ids, ids_with_more_than_one_row, repeats
              (true / false / "NOT_ESTABLISHED")}; a shape not read carries a reason. repeats false or NOT_ESTABLISHED: readers_census
              is "NOT_NEEDED" or "NOT_DONE" with why. repeats true: trees has an entry for each of workspace, portal, opal_ai,
              mcportal, each {searched (bool), files_searched or reason}; readers each {tree, file, line, sums_amounts (bool),
              keys_on_transaction_id (bool), what_it_serves, served (bool), owner}; unkeyed_and_served is exactly the files of readers
              with sums_amounts true, keys_on_transaction_id false and served true. corrected == 0; s3_writes == 0; no string holds
              a run of 8 or more digits.
  DB76-2-AC1  ~117/TIE_59_OF_90_REDERIVED.json: denominator 90; naive {tie, do_not_tie} summing to 90; id_once {tie, do_not_tie}
              summing to 90; moved (how many segments change side); client_figures == 0; s3_writes == 0; no long digit run.
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RUN = re.compile(r"\d{8,}")
TREES = ["mcportal", "opal_ai", "portal", "workspace"]


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB76"))
        sys.exit(1)

    def record(rel):
        p = root / (M + rel)
        if not p.is_file():
            fail("no record %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB76-1-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~116/ORIGINAL_STORE_SHAPE.json")
        s = r.get("shape") or {}
        if not isinstance(s.get("read"), bool):
            fail("shape.read is not a bool")
        rep = s.get("repeats")
        if rep not in (True, False, "NOT_ESTABLISHED"):
            fail("shape.repeats %r" % rep)
        if s["read"]:
            for k in ("rows", "distinct_ids", "ids_with_more_than_one_row"):
                if not isinstance(s.get(k), int):
                    fail("shape.%s missing" % k)
            if not str(s.get("day") or "").strip():
                fail("shape.day missing")
            if (rep is True) != (s["ids_with_more_than_one_row"] > 0) and rep != "NOT_ESTABLISHED":
                fail("shape.repeats %r does not follow ids_with_more_than_one_row %d" % (rep, s["ids_with_more_than_one_row"]))
        elif not str(s.get("reason") or "").strip() or rep != "NOT_ESTABLISHED":
            fail("a shape not read gives its reason and repeats NOT_ESTABLISHED")
        if rep is True:
            tr = r.get("trees") or {}
            if sorted(tr) != TREES:
                fail("trees %r, want %r" % (sorted(tr), TREES))
            for k, v in tr.items():
                if not isinstance(v.get("searched"), bool) or (v["searched"] and not isinstance(v.get("files_searched"), int)) \
                        or (not v["searched"] and not str(v.get("reason") or "").strip()):
                    fail("tree %s lacks searched, its denominator or its reason" % k)
            rd = r.get("readers")
            if not isinstance(rd, list):
                fail("readers is not a list")
            for x in rd:
                if x.get("tree") not in TREES or not str(x.get("file") or "").strip() or not x.get("line") \
                        or any(not isinstance(x.get(b), bool) for b in ("sums_amounts", "keys_on_transaction_id", "served")) \
                        or not str(x.get("what_it_serves") or "").strip() or not str(x.get("owner") or "").strip():
                    fail("reader %r lacks a member" % x.get("file"))
            want = sorted({"%s:%s" % (x["tree"], x["file"]) for x in rd if x["sums_amounts"] and not x["keys_on_transaction_id"] and x["served"]})
            if sorted(set(r.get("unkeyed_and_served") or [])) != want:
                fail("unkeyed_and_served %r, the readers give %r" % (sorted(set(r.get("unkeyed_and_served") or [])), want))
            tail = "%d reader(s) over the trees searched; %d sum without the id and serve something" % (len(rd), len(want))
        else:
            if r.get("readers_census") not in ("NOT_NEEDED", "NOT_DONE") or not str(r.get("readers_census_why") or "").strip():
                fail("with repeats %r the record states readers_census NOT_NEEDED or NOT_DONE and why" % rep)
            tail = "readers census %s" % r["readers_census"]
        if r.get("corrected") != 0 or r.get("s3_writes") != 0:
            fail("corrected %r, s3_writes %r" % (r.get("corrected"), r.get("s3_writes")))
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: the original store repeats a transaction per portfolio group: %s; %s" % (rep, tail))
    elif cid == "DB76-2-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~117/TIE_59_OF_90_REDERIVED.json")
        if r.get("denominator") != 90:
            fail("denominator %r" % r.get("denominator"))
        for k in ("naive", "id_once"):
            v = r.get(k) or {}
            if not isinstance(v.get("tie"), int) or not isinstance(v.get("do_not_tie"), int) or v["tie"] + v["do_not_tie"] != 90:
                fail("%s %r does not sum to 90" % (k, v))
        if not isinstance(r.get("moved"), int):
            fail("moved missing")
        if r.get("client_figures") != 0 or r.get("s3_writes") != 0:
            fail("client_figures %r, s3_writes %r" % (r.get("client_figures"), r.get("s3_writes")))
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: of 90, the naive sum ties %d; each id counted once ties %d; %d segment(s) change side"
              % (r["naive"]["tie"], r["id_once"]["tie"], r["moved"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
