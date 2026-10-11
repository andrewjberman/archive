"""DSGN_IRPTV1 round 14 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ROUND-13 ANALYSIS @72e8e2bb59, section 4, items 2 to 5.

Cells: IV-e-89 F40-AC5 the calendar; IV-e-90 the 43-id table; IV-e-91 the portal half catches up to the contract; IV-e-92 bun from the
environment, the press test off the private dispatcher, F47-AC6. Item 1 (the rendered walk) is an ask carried by the managers, not a cell.

The baseline is ~43/SUITE_SAMPLE.json: 43 failing ids, each with its proposed ruling and row.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV89-AC1  ~49/CALENDAR_FIX.json: the F40-AC5 id is in suite_after.fixed_ids; suite_after.new_failing_ids == []; product_files_changed
            non-empty; portal_commit hex; one_frontier {text, source: {file, line}}.
  IV90-AC1  ~50/FAILING_ID_TABLE.json: rows cover EXACTLY the baseline's 43 ids; each disposition is REGRESSION_OWNED (with owner and
            cell) or RETIREMENT_ASKED (with reason and the assertion it retires); none is any other word.
  IV91-AC1  ~49/CONTRACT_CATCHUP.json: every baseline id whose row is DSGN_IRPTV1-D2-W43-S2 is in suite_after.fixed_ids or listed under
            not_fixed with a reason; new_failing_ids == []; workspace_commit and portal_commit hex; product_files_changed non-empty.
  IV92-AC1  ~49/TEST_HYGIENE.json: bun {hardcoded_paths_left == 0, source [{file, line}]}; press {supports in TESTING_LIBRARY /
            NATIVE_ACT / NEITHER; NEITHER carries a row and rewritten false; otherwise rewritten true and uses_private_internals
            false}; f47 {outcome FIXED or RULING_ASKED, with reason}; suite_after.new_failing_ids == []; portal_commit hex. When
            dev_dependency is present (AMENDMENT 2): a name, an exact version, lockfile_other_packages_moved == 0, build_equal true with
            equal before and after hashes, and press.supports == NATIVE_ACT.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~"
HEX = re.compile(r"^[0-9a-f]{7,40}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV14"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    base = load(D + "43/SUITE_SAMPLE.json")
    rulings = base.get("rulings") or []
    ids = [x["id"] for x in rulings]
    if len(ids) != 43:
        fail("the baseline holds %d ids, not 43" % len(ids))

    def suite(r):
        s = r.get("suite_after") or {}
        if not isinstance(s.get("fixed_ids"), list) or s.get("new_failing_ids") != []:
            fail("suite_after %r: want fixed_ids as a list and new_failing_ids == []" % {k: s.get(k) for k in ("failed", "new_failing_ids")})
        return set(s["fixed_ids"])

    if cid == "IV89-AC1":
        r = load(D + "49/CALENDAR_FIX.json")
        target = [i for i in ids if "F40-AC5" in i]
        if len(target) != 1:
            fail("the baseline does not hold exactly one F40-AC5 id")
        if target[0] not in suite(r):
            fail("F40-AC5 is not in suite_after.fixed_ids")
        of = r.get("one_frontier") or {}
        src = of.get("source") or {}
        if not r.get("product_files_changed") or not HEX.match(str(r.get("portal_commit") or "")) or not str(of.get("text") or "").strip() \
                or not src.get("file") or not isinstance(src.get("line"), int):
            fail("product_files_changed, portal_commit or one_frontier missing")
        print("OK: F40-AC5 fixed, no new failing id, the portal's fallback named from the one frontier")
    elif cid == "IV90-AC1":
        r = load(D + "50/FAILING_ID_TABLE.json")
        rows = r.get("rows") or []
        if sorted(x.get("id") for x in rows) != sorted(ids):
            fail("rows do not cover exactly the baseline's 43 ids (%d rows)" % len(rows))
        n = {"REGRESSION_OWNED": 0, "RETIREMENT_ASKED": 0}
        for x in rows:
            d = x.get("disposition")
            if d not in n:
                fail("%r disposition %r" % (x.get("id"), d))
            if d == "REGRESSION_OWNED" and (not str(x.get("owner") or "").strip() or not str(x.get("cell") or "").strip()):
                fail("%r is REGRESSION_OWNED without an owner and a cell" % x.get("id"))
            if d == "RETIREMENT_ASKED" and (not str(x.get("reason") or "").strip() or not str(x.get("assertion_retired") or "").strip()):
                fail("%r is RETIREMENT_ASKED without a reason and the assertion it retires" % x.get("id"))
            n[d] += 1
        print("OK: 43 ids: %r" % n)
    elif cid == "IV91-AC1":
        r = load(D + "49/CONTRACT_CATCHUP.json")
        fixed = suite(r)
        target = [x["id"] for x in rulings if x.get("row") == "DSGN_IRPTV1-D2-W43-S2"]
        if not target:
            fail("the baseline holds no id under row DSGN_IRPTV1-D2-W43-S2")
        nf = {x.get("id"): x for x in (r.get("not_fixed") or [])}
        for i in target:
            if i not in fixed and not str((nf.get(i) or {}).get("reason") or "").strip():
                fail("%r is neither fixed nor listed under not_fixed with a reason" % i)
        if not HEX.match(str(r.get("workspace_commit") or "")) or not HEX.match(str(r.get("portal_commit") or "")) or not r.get("product_files_changed"):
            fail("workspace_commit, portal_commit or product_files_changed missing")
        print("OK: %d of %d contract-family ids fixed, the rest reasoned; no new failing id" % (len([i for i in target if i in fixed]), len(target)))
    elif cid == "IV92-AC1":
        r = load(D + "49/TEST_HYGIENE.json")
        suite(r)
        b = r.get("bun") or {}
        if b.get("hardcoded_paths_left") != 0 or not b.get("source"):
            fail("bun %r" % b)
        p = r.get("press") or {}
        if p.get("supports") not in ("TESTING_LIBRARY", "NATIVE_ACT", "NEITHER"):
            fail("press.supports %r" % p.get("supports"))
        if p["supports"] == "NEITHER":
            if p.get("rewritten") is not False or not str(p.get("row") or "").strip():
                fail("press NEITHER wants rewritten false and a row id")
        elif p.get("rewritten") is not True or p.get("uses_private_internals") is not False:
            fail("press %r: want rewritten true and uses_private_internals false" % p)
        dd = r.get("dev_dependency")
        if dd is not None:
            # AMENDMENT 2 (CTO msg 4358): ONE dev dependency, devDependencies only, nothing else moved, the production build byte-equal.
            if not dd.get("name") or not re.match(r"^\d+\.\d+\.\d+", str(dd.get("version") or "")) or dd.get("lockfile_other_packages_moved") != 0                     or dd.get("build_equal") is not True or not dd.get("build_hash_before") or dd.get("build_hash_before") != dd.get("build_hash_after"):
                fail("dev_dependency %r is outside the CTO's conditions" % {k: dd.get(k) for k in ("name", "version", "lockfile_other_packages_moved", "build_equal")})
            if p["supports"] != "NATIVE_ACT":
                fail("a dev dependency was added and press.supports is %r, want NATIVE_ACT" % p["supports"])
        f = r.get("f47") or {}
        if f.get("outcome") not in ("FIXED", "RULING_ASKED") or not str(f.get("reason") or "").strip():
            fail("f47 %r" % f)
        if not HEX.match(str(r.get("portal_commit") or "")):
            fail("portal_commit missing")
        print("OK: bun from the environment; press %s; F47-AC6 %s; no new failing id" % (p["supports"], f["outcome"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
