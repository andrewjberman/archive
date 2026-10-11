"""DSGN_IRPTV1 round 19 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 4806: irpt-status release 5 returns only after the
portal's history reader admits the new members, on PROD, in that order.

Cell: IV-e-99 the history reader admits BOTH shapes the service can serve (the two-key answer live after the rollback, and the contract's
answer with unreadable_rows and the per-item client_id / client_claim), and still refuses anything else.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV99-AC1  ~55/HISTORY_READER.json: accepts {old_shape true, new_shape true, producer_fixture true}; refuses {unknown_top_key true,
            unknown_item_key true, wrong_type_unreadable_rows true, bad_client_claim true}; test {id, passes true, mutant {what, failed
            true}}; contract_lines non-empty [{member, file, line}].
  IV99-AC2  the same record: carried lists the members the view now carries; rendered_changes is a list (empty means the page shows
            nothing new); typecheck_errors == 0; suite_after.new_failing_ids == []; product_files_changed non-empty; portal_commit hex.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~55/"
HEX = re.compile(r"^[0-9a-f]{7,40}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV19"))
        sys.exit(1)

    p = root / (D + "HISTORY_READER.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    if cid == "IV99-AC1":
        a, x = r.get("accepts") or {}, r.get("refuses") or {}
        for k in ("old_shape", "new_shape", "producer_fixture"):
            if a.get(k) is not True:
                fail("accepts.%s is %r" % (k, a.get(k)))
        for k in ("unknown_top_key", "unknown_item_key", "wrong_type_unreadable_rows", "bad_client_claim"):
            if x.get(k) is not True:
                fail("refuses.%s is %r" % (k, x.get(k)))
        t = r.get("test") or {}
        m = t.get("mutant") or {}
        if not str(t.get("id") or "").strip() or t.get("passes") is not True or not str(m.get("what") or "").strip() or m.get("failed") is not True:
            fail("test %r" % {k: t.get(k) for k in ("id", "passes")})
        cl = r.get("contract_lines") or []
        if not cl or any(not str(c.get("member") or "").strip() or not (root / str(c.get("file") or "")).is_file() or not isinstance(c.get("line"), int) for c in cl):
            fail("contract_lines must name each member with a file and line that resolve")
        print("OK: the reader takes the two-key answer, the contract's answer and the producer's fixture, and refuses four malformed ones; %d contract line(s) cited" % len(cl))
    elif cid == "IV99-AC2":
        if not r.get("carried") or not isinstance(r.get("rendered_changes"), list):
            fail("carried or rendered_changes missing")
        if r.get("typecheck_errors") != 0:
            fail("typecheck_errors %r" % r.get("typecheck_errors"))
        s = r.get("suite_after") or {}
        if s.get("new_failing_ids") != [] or not r.get("product_files_changed") or not HEX.match(str(r.get("portal_commit") or "")):
            fail("want suite_after.new_failing_ids == [], product_files_changed and a portal_commit")
        print("OK: %d member(s) carried, %d rendered change(s); typecheck 0 errors; no new failing id" % (len(r["carried"]), len(r["rendered_changes"])))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
