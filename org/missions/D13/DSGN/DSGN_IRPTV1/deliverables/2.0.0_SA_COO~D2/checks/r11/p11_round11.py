"""DSGN_IRPTV1 round 11 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round analysis @10d7d46e49, section 4 (five items).

Cells: IV-e-82 the pinned three-run suite sample; IV-e-83 S61 the Holding cell names the corrected security; IV-e-84 S60 a component test that
presses the "Did you mean" button; IV-e-85 W35-S2 Export on the Analysis tab; IV-e-86 the per-outcome state table.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV82-AC1  ~43/SUITE_SAMPLE.json: dev_tip is 40 hex and equals ls_remote.sha; runs has exactly 3 entries, each at commit == dev_tip with a
            failing_ids list and int counts; identical == (the three failing sets are equal); when identical, rulings covers EXACTLY the
            failing ids, each REGRESSION / KNOWN-LEGACY / FLAKE and a KNOWN-LEGACY naming its row; when not identical, differing_ids equals
            the union minus the intersection and rulings is empty.
  IV83-AC1  ~46/S61_FIX.json: component_file and test_file named; fail_before {result FAIL, line}; after {result PASS}; portal_commit hex;
            product_files_changed is a non-empty list.
  IV84-AC1  ~44/PRESS_PIN.json: test_file named; head {result PASS}; mutants has at least 2 entries, each {name, result FAIL};
            product_files_changed == [] (a test-only change); portal_commit hex.
  IV85-AC1  ~46/EXPORT_ANALYSIS.json: finding is EXPORT_WIRED or NEEDS_SERVED_ROUTE; why_no_signal with evidence [{file, line}];
            NEEDS_SERVED_ROUTE carries a row id and product_files_changed == []; EXPORT_WIRED carries test_file, after {result PASS},
            fail_before {result FAIL} and portal_commit hex.
  IV86-AC1  ~45/FWD_STATE_TABLE.json: outcomes holds exactly FWD-1..FWD-23; each state is DESIRED / APPLIED / EXERCISED; evidence is the
            literal ABSENT or a non-empty list of {kind, ref}; APPLIED and EXERCISED never carry ABSENT.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX = re.compile(r"^[0-9a-f]{7,40}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV11"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def res(d, want):
        return isinstance(d, dict) and d.get("result") == want

    if cid == "IV82-AC1":
        r = load(D + "43/SUITE_SAMPLE.json")
        tip = str(r.get("dev_tip") or "")
        if not HEX40.match(tip) or (r.get("ls_remote") or {}).get("sha") != tip:
            fail("dev_tip %r is not 40 hex or differs from ls_remote.sha" % tip)
        runs = r.get("runs") or []
        if len(runs) != 3:
            fail("%d runs, want 3" % len(runs))
        sets = []
        for x in runs:
            if x.get("commit") != tip or not isinstance(x.get("failing_ids"), list):
                fail("a run is not at the dev tip or lacks failing_ids")
            for k in ("passed", "failed", "skipped"):
                if not isinstance(x.get(k), int):
                    fail("a run lacks int %s" % k)
            if x["failed"] != len(set(x["failing_ids"])):
                fail("a run's failed count %d differs from its %d failing ids" % (x["failed"], len(set(x["failing_ids"]))))
            sets.append(set(x["failing_ids"]))
        same = sets[0] == sets[1] == sets[2]
        if r.get("identical") is not same:
            fail("identical %r, the sets say %r" % (r.get("identical"), same))
        rulings = r.get("rulings") or []
        if same:
            if sorted(x.get("id") for x in rulings) != sorted(sets[0]):
                fail("rulings do not cover exactly the %d failing ids" % len(sets[0]))
            for x in rulings:
                if x.get("ruling") not in ("REGRESSION", "KNOWN-LEGACY", "FLAKE"):
                    fail("ruling %r on %r" % (x.get("ruling"), x.get("id")))
                if x["ruling"] == "KNOWN-LEGACY" and not str(x.get("row") or "").strip():
                    fail("KNOWN-LEGACY %r names no row" % x.get("id"))
        else:
            diff = (sets[0] | sets[1] | sets[2]) - (sets[0] & sets[1] & sets[2])
            if set(r.get("differing_ids") or []) != diff or rulings:
                fail("differing_ids do not equal the union minus the intersection, or rulings were written on unequal sets")
        print("OK: three runs at %s; identical=%s; %d failing id(s) in run 1" % (tip[:10], same, len(sets[0])))
    elif cid == "IV83-AC1":
        r = load(D + "46/S61_FIX.json")
        if not r.get("component_file") or not r.get("test_file") or not HEX.match(str(r.get("portal_commit") or "")):
            fail("component_file, test_file or portal_commit missing")
        if not res(r.get("fail_before"), "FAIL") or not str((r.get("fail_before") or {}).get("line") or "").strip() or not res(r.get("after"), "PASS"):
            fail("fail_before %r / after %r" % (r.get("fail_before"), r.get("after")))
        if not r.get("product_files_changed"):
            fail("product_files_changed empty")
        print("OK: S61 fix recorded with a test that failed before and passes after")
    elif cid == "IV84-AC1":
        r = load(D + "44/PRESS_PIN.json")
        if not r.get("test_file") or not HEX.match(str(r.get("portal_commit") or "")) or not res(r.get("head"), "PASS"):
            fail("test_file, portal_commit or head result missing")
        ms = r.get("mutants") or []
        if len(ms) < 2 or any(not m.get("name") or m.get("result") != "FAIL" for m in ms):
            fail("mutants %r: want at least 2, each caught (FAIL)" % ms)
        if r.get("product_files_changed") != []:
            fail("product_files_changed %r, want [] (a test-only change)" % r.get("product_files_changed"))
        print("OK: the pin presses the button; %d mutant(s) caught" % len(ms))
    elif cid == "IV85-AC1":
        r = load(D + "46/EXPORT_ANALYSIS.json")
        if r.get("finding") not in ("EXPORT_WIRED", "NEEDS_SERVED_ROUTE"):
            fail("finding %r" % r.get("finding"))
        w = r.get("why_no_signal") or {}
        ev = w.get("evidence") or []
        if not str(w.get("text") or "").strip() or not ev or any(not e.get("file") or not isinstance(e.get("line"), int) for e in ev):
            fail("why_no_signal lacks text or file-and-line evidence")
        if r["finding"] == "NEEDS_SERVED_ROUTE":
            if not str(r.get("row") or "").strip() or r.get("product_files_changed") != []:
                fail("NEEDS_SERVED_ROUTE without a row id, or with a product change")
        else:
            if not r.get("test_file") or not res(r.get("after"), "PASS") or not res(r.get("fail_before"), "FAIL") \
                    or not HEX.match(str(r.get("portal_commit") or "")):
                fail("EXPORT_WIRED without test_file, fail_before FAIL, after PASS and portal_commit")
        print("OK: Export on the Analysis tab: %s" % r["finding"])
    elif cid == "IV86-AC1":
        r = load(D + "45/FWD_STATE_TABLE.json")
        out = r.get("outcomes") or []
        want = ["FWD-%d" % i for i in range(1, 24)]
        if sorted(x.get("id") for x in out) != sorted(want):
            fail("outcomes %r, want FWD-1..FWD-23" % sorted(str(x.get("id")) for x in out))
        n = {"DESIRED": 0, "APPLIED": 0, "EXERCISED": 0}
        for x in out:
            if x.get("state") not in n:
                fail("%s state %r" % (x["id"], x.get("state")))
            ev = x.get("evidence")
            if ev != "ABSENT" and (not isinstance(ev, list) or not ev or any(not e.get("kind") or not e.get("ref") for e in ev)):
                fail("%s evidence is neither ABSENT nor a list of {kind, ref}" % x["id"])
            if x["state"] != "DESIRED" and ev == "ABSENT":
                fail("%s reads %s with evidence ABSENT" % (x["id"], x["state"]))
            n[x["state"]] += 1
        print("OK: 23 outcomes: %r" % n)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
