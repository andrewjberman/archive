"""DSGN_IRPTV1 round 20 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 4872: the census of portal readers of irpt-status routes.

Cell: IV-e-100 one read-only cell, at the portal's PROD commit and again at DEV's tip: for every irpt-status route the portal reads, the
reader with file and line, its key policy at each level it checks (EXACT or TOLERANT), and, against release 5's answer for that route, PASS
or the member that refuses. The sections reader and the single-request reader must not be skipped.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV100-AC1  ~56/READER_CENSUS.json: denominator {routes_served (int > 0), routes_read_by_portal (int > 0), how}; commits {prod, dev}
             both hex; rows cover routes_read_by_portal routes, each {route, reader {name, file, line}, levels [{level, policy EXACT or
             TOLERANT, evidence}], at_prod and at_dev each {result PASS / REFUSES / NOT_ESTABLISHED, member (when REFUSES), how}};
             the routes include a sections read and the single-request read (named in must_not_skip with their route names).
  IV100-AC2  the same record: joins_prod_push lists exactly the routes whose at_prod.result is REFUSES; every NOT_ESTABLISHED carries a
             reason; release5_answer_source non-empty per route; product_files_changed == [] and s3_or_live_calls == 0.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~56/"
HEX = re.compile(r"^[0-9a-f]{7,40}$")
RES = ("PASS", "REFUSES", "NOT_ESTABLISHED")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV20"))
        sys.exit(1)

    def text(v):
        return str(v or "").strip()

    p = root / (D + "READER_CENSUS.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    rows = r.get("rows") or []
    if cid == "IV100-AC1":
        dn = r.get("denominator") or {}
        if not isinstance(dn.get("routes_served"), int) or dn["routes_served"] <= 0 or not isinstance(dn.get("routes_read_by_portal"), int) \
                or dn["routes_read_by_portal"] <= 0 or not text(dn.get("how")):
            fail("denominator %r" % dn)
        cm = r.get("commits") or {}
        if not HEX.match(text(cm.get("prod"))) or not HEX.match(text(cm.get("dev"))):
            fail("commits %r" % cm)
        if len(rows) != dn["routes_read_by_portal"] or len(set(text(x.get("route")) for x in rows)) != len(rows):
            fail("%d row(s) for %d route(s) read by the portal" % (len(rows), dn["routes_read_by_portal"]))
        for x in rows:
            rd = x.get("reader") or {}
            if not text(x.get("route")) or not text(rd.get("name")) or not text(rd.get("file")) or not isinstance(rd.get("line"), int):
                fail("row %r lacks its reader with file and line" % x.get("route"))
            lv = x.get("levels") or []
            if not lv or any(not text(v.get("level")) or v.get("policy") not in ("EXACT", "TOLERANT") or not text(v.get("evidence")) for v in lv):
                fail("row %r lacks a key policy per level with evidence" % x.get("route"))
            for side in ("at_prod", "at_dev"):
                s = x.get(side) or {}
                if s.get("result") not in RES or not text(s.get("how")) or (s["result"] == "REFUSES" and not text(s.get("member"))):
                    fail("row %r %s %r" % (x.get("route"), side, s))
        mns = r.get("must_not_skip") or {}
        names = set(text(x.get("route")) for x in rows)
        for k in ("sections_read", "single_request_read"):
            if text(mns.get(k)) not in names:
                fail("must_not_skip.%s %r is not among the rows" % (k, mns.get(k)))
        print("OK: %d of %d served route(s) are read by the portal; each has its reader, key policy per level and a result at PROD and at DEV"
              % (dn["routes_read_by_portal"], dn["routes_served"]))
    elif cid == "IV100-AC2":
        refuses = sorted(text(x.get("route")) for x in rows if (x.get("at_prod") or {}).get("result") == "REFUSES")
        if sorted(text(v) for v in (r.get("joins_prod_push") or [])) != refuses:
            fail("joins_prod_push %r, the rows say %r" % (r.get("joins_prod_push"), refuses))
        for x in rows:
            if not text(x.get("release5_answer_source")):
                fail("row %r lacks release5_answer_source" % x.get("route"))
            for side in ("at_prod", "at_dev"):
                s = x.get(side) or {}
                if s.get("result") == "NOT_ESTABLISHED" and not text(s.get("reason")):
                    fail("row %r %s is NOT_ESTABLISHED without a reason" % (x.get("route"), side))
        if r.get("product_files_changed") != [] or r.get("s3_or_live_calls") != 0:
            fail("a read-only cell changed a product file or made a live call")
        print("OK: %d route(s) join the PROD push %r; nothing changed, no live call" % (len(refuses), refuses))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
