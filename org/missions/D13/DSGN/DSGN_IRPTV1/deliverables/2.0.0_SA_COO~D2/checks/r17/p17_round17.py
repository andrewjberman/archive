"""DSGN_IRPTV1 round 17 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ROUND-17 ANALYSIS @e4345abd6e, section 4, items 1 to 4.

Cells: IV-e-95 the test repairs (the excused set by name, the smoke map at 22 with two named excuses, the stale goldens and the
newline pins); IV-e-96 the Holdings face opens on the picked account's category split; IV-e-97 the tooling hygiene (the lock refreshed
once, playwright-core, the calendar's provenance). Nothing is cut for the Performance hop (section 2; CTO msg 4705).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV95-AC1  ~53/TEST_REPAIRS.json: excused_sets has two entries, each {test_file, excused_by_name (non-empty list of route names),
            mutant {what, failed true}}; regold has the IVE115 and IVE69 ids, each DONE (with ruling, before, after) or STOPPED (row).
  IV95-AC2  the same record's smoke_map (AMENDMENT 2): routes_declared == 22; excused is the MEASURED set, each {route, reason_class,
            reason, evidence}, reason_class NO_PRODUCER_FIXTURE or READER_REFUSES_PRODUCER_FIXTURE (the latter's evidence is the
            parser's own refusal text), at most 4; keys == 22 minus the excused count; sourced [{route, source, reader}] one per key
            and none excused; pins_followed non-empty [{file, before, after}]; producer_pin {file, outcome PLACED, owner}.
  IV95-AC3  the same record's newline_pins {files_searched > 0, found, fixed == found}; suite_after.new_failing_ids == []; portal_commit hex.
  IV96-AC1  ~53/HOLDINGS_FACE.json: behaviour {test_id, passes true, mutant {what, failed true}}; default_view_before and
            default_view_after non-empty and different; product_files_changed non-empty; suite_after.new_failing_ids == []; portal_commit hex.
  IV96-AC2  the same record's screenshots: at least two [{state, path, canvas}], each path an existing file in the worker's folder and
            each canvas "rgb(244, 246, 250)"; contract_clauses non-empty.
  IV97-AC1  ~53/TOOLING.json: lock {refreshed true, package_json_dependencies_changed false, packages_moved int, build_equal true with
            equal non-empty before and after hashes, happy_dom "20.14.5"}; suite_after.new_failing_ids == []; portal_commit hex.
  IV97-AC2  the same record's playwright_core {outcome DECLARED or SKIP_STATED, evidence} and calendar_source {outcome REFUSES_FALLBACK
            or CARRIES_CLAIM, test_id, passes true}.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~53/"
HEX = re.compile(r"^[0-9a-f]{7,40}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV17"))
        sys.exit(1)

    def load(name):
        p = root / (D + name)
        if not p.is_file():
            fail("no record %s" % name)
        return json.loads(p.read_bytes().decode("utf-8"))

    def text(v):
        return str(v or "").strip()

    def suite(r):
        s = r.get("suite_after") or {}
        if s.get("new_failing_ids") != [] or not HEX.match(text(r.get("portal_commit"))):
            fail("want suite_after.new_failing_ids == [] and a portal_commit")
        return s

    if cid == "IV95-AC1":
        r = load("TEST_REPAIRS.json")
        es = r.get("excused_sets") or []
        if len(es) != 2:
            fail("excused_sets holds %d entries, want 2" % len(es))
        for e in es:
            m = e.get("mutant") or {}
            if not text(e.get("test_file")) or not e.get("excused_by_name") or not text(m.get("what")) or m.get("failed") is not True:
                fail("excused set %r lacks its names or a failing mutant" % e.get("test_file"))
        rg = r.get("regold") or []
        for want in ("IVE115", "IVE69"):
            hit = [x for x in rg if want in text(x.get("id"))]
            if len(hit) != 1:
                fail("regold does not hold exactly one %s entry" % want)
            x = hit[0]
            if x.get("outcome") == "DONE":
                if not text(x.get("ruling")) or not text(x.get("before")) or not text(x.get("after")):
                    fail("%s is DONE without its ruling, before and after" % want)
            elif x.get("outcome") != "STOPPED" or not text(x.get("row")):
                fail("%s outcome %r" % (want, x.get("outcome")))
        print("OK: two excused sets pinned by name, each with a failing mutant; goldens %r" % [x.get("outcome") for x in rg])
    elif cid == "IV95-AC2":
        sm = load("TEST_REPAIRS.json").get("smoke_map") or {}
        ex = sm.get("excused") or []
        pp = sm.get("producer_pin") or {}
        classes = ("NO_PRODUCER_FIXTURE", "READER_REFUSES_PRODUCER_FIXTURE")
        if sm.get("routes_declared") != 22 or len(ex) > 4:
            fail("smoke_map routes_declared %r with %d excuse(s): want 22 declared and at most four measured excuses" % (sm.get("routes_declared"), len(ex)))
        for x in ex:
            if not text(x.get("route")) or x.get("reason_class") not in classes or not text(x.get("reason")) or not text(x.get("evidence")):
                fail("excuse %r lacks a reason_class of %r, a reason or its evidence" % (x.get("route"), classes))
        if sm.get("keys") != 22 - len(ex):
            fail("smoke_map keys %r, want %d (22 declared minus %d excused)" % (sm.get("keys"), 22 - len(ex), len(ex)))
        src = sm.get("sourced") or []
        if len(src) != sm["keys"] or any(not text(x.get("route")) or not text(x.get("source")) or not text(x.get("reader")) for x in src)                 or set(text(x.get("route")) for x in src) & set(text(x.get("route")) for x in ex):
            fail("sourced lists %d entr(ies) for %d key(s), lacks a source or reader, or names an excused route" % (len(src), sm["keys"]))
        if not sm.get("pins_followed") or any(not text(x.get("file")) or "after" not in x for x in sm["pins_followed"]):
            fail("pins_followed missing")
        if not text(pp.get("file")) or pp.get("outcome") != "PLACED" or not text(pp.get("owner")):
            fail("producer_pin %r" % pp)
        print("OK: the smoke map at %d keys of 22 declared routes, %d excused by name, every body sourced, %d pin(s) followed, the producer's pin placed"
              % (sm["keys"], len(ex), len(sm["pins_followed"])))
    elif cid == "IV95-AC3":
        r = load("TEST_REPAIRS.json")
        n = r.get("newline_pins") or {}
        if not isinstance(n.get("files_searched"), int) or n["files_searched"] <= 0 or not isinstance(n.get("found"), int) or n.get("fixed") != n.get("found"):
            fail("newline_pins %r" % n)
        s = suite(r)
        print("OK: %d file(s) searched for newline-anchored pins, %d found and fixed; no new failing id; %s still failing"
              % (n["files_searched"], n["found"], s.get("failed")))
    elif cid == "IV96-AC1":
        r = load("HOLDINGS_FACE.json")
        b = r.get("behaviour") or {}
        m = b.get("mutant") or {}
        if not text(b.get("test_id")) or b.get("passes") is not True or not text(m.get("what")) or m.get("failed") is not True:
            fail("behaviour %r" % b)
        if not text(r.get("default_view_before")) or not text(r.get("default_view_after")) or r["default_view_before"] == r["default_view_after"]:
            fail("default_view_before and default_view_after must both be stated and differ")
        if not r.get("product_files_changed"):
            fail("product_files_changed empty")
        suite(r)
        print("OK: the Holdings default view moved, a test holds it and a mutant breaks it; no new failing id")
    elif cid == "IV96-AC2":
        r = load("HOLDINGS_FACE.json")
        sh = r.get("screenshots") or []
        if len(sh) < 2:
            fail("%d screenshot(s), want at least two" % len(sh))
        for x in sh:
            p = root / text(x.get("path"))
            if not text(x.get("state")) or not text(x.get("path")).startswith(D) or not p.is_file() or x.get("canvas") != "rgb(244, 246, 250)":
                fail("screenshot %r: want a state, an existing file in the worker's folder and the canvas colour" % x.get("path"))
        if not r.get("contract_clauses"):
            fail("contract_clauses empty")
        print("OK: %d screenshot(s) on the light canvas, read against %d contract clause(s)" % (len(sh), len(r["contract_clauses"])))
    elif cid == "IV97-AC1":
        r = load("TOOLING.json")
        k = r.get("lock") or {}
        if k.get("refreshed") is not True or k.get("package_json_dependencies_changed") is not False or not isinstance(k.get("packages_moved"), int) \
                or k.get("build_equal") is not True or not text(k.get("build_hash_before")) or k.get("build_hash_before") != k.get("build_hash_after") \
                or k.get("happy_dom") != "20.14.5":
            fail("lock %r" % {x: k.get(x) for x in ("refreshed", "package_json_dependencies_changed", "packages_moved", "build_equal", "happy_dom")})
        suite(r)
        print("OK: the lock refreshed once (%d package(s) moved), the build byte-equal, happy-dom held; no new failing id" % k["packages_moved"])
    elif cid == "IV97-AC2":
        r = load("TOOLING.json")
        p = r.get("playwright_core") or {}
        c = r.get("calendar_source") or {}
        if p.get("outcome") not in ("DECLARED", "SKIP_STATED") or not text(p.get("evidence")):
            fail("playwright_core %r" % p)
        if c.get("outcome") not in ("REFUSES_FALLBACK", "CARRIES_CLAIM") or not text(c.get("test_id")) or c.get("passes") is not True:
            fail("calendar_source %r" % c)
        print("OK: playwright-core %s; the calendar's provenance %s" % (p["outcome"], c["outcome"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
