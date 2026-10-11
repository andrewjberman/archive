"""DSGN_IRPTV1 round 26 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 5562 on the laptop walk's three rows.

Cells: IV-e-112 (row D2-S22) the reads the walk saw refused with FIRM_BINDING: which face each feeds, and that face says the refusal in
words; IV-e-113 (row D2-S21) page or producer: whether the served sections answer sends a title and a unit, beside what the adapter
does with them; IV-e-114 (row D2-S23) one hygiene cell: the React warning, the low-contrast eyebrow text, the bands counted against C3.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV112-AC1  ~62/FIRM_BINDING_FACES.json: reads (2 or more) each {route, reader {file, line}, feeds_face, on_refusal_before,
             on_refusal_after}; every on_refusal_after is non-empty words; test {id, passes true, mutant {what, failed true}};
             screenshots (1 or more existing files in the folder, each in screenshots_read); lint_errors 0; typecheck_errors 0;
             suite_after.new_failing_ids == []; product_files_changed non-empty; portal_commit hex.
  IV113-AC1  ~62/SECTION_TITLE_UNIT.json: for each of title and unit: {contract_declares (bool), contract_where,
             producer_fixture_sends (bool), fixture_where, adapter_reads (bool), adapter_where, page_prints_when_absent};
             verdict PAGE, PRODUCER, BOTH or NOT_ESTABLISHED with a reason; served_answer_read (bool) with how or why not;
             product_files_changed == [].
  IV114-AC1  ~62/HYGIENE_26.json: colgroup_warning {present_before (bool), present_after false, how_measured}; contrast {failing_before
             (int), failing_after (int <= failing_before), how_measured}; bands {count, per_design_law, where}; screenshots (1 or
             more existing, each in screenshots_read); lint_errors 0; typecheck_errors 0; suite_after.new_failing_ids == [];
             portal_commit hex.
"""
import json
import re
import sys
from pathlib import Path

F = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~62"
HEX = re.compile(r"^[0-9a-f]{7,40}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    folder = root / F

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV26"))
        sys.exit(1)

    def record(name):
        p = folder / name
        if not p.is_file():
            fail("no record %s" % name)
        return json.loads(p.read_bytes().decode("utf-8"))

    def clean(r):
        if r.get("lint_errors") != 0 or r.get("typecheck_errors") != 0:
            fail("lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
        if (r.get("suite_after") or {}).get("new_failing_ids") != []:
            fail("suite_after.new_failing_ids %r" % (r.get("suite_after") or {}).get("new_failing_ids"))
        if not HEX.match(str(r.get("portal_commit") or "")):
            fail("portal_commit missing")

    def shots(r):
        s = r.get("screenshots") or []
        if not s or any(not (folder / str(x)).is_file() for x in s) or sorted(r.get("screenshots_read") or []) != sorted(s):
            fail("screenshots: one or more existing files, each in screenshots_read")
        return len(s)

    if cid == "IV112-AC1":
        r = record("FIRM_BINDING_FACES.json")
        reads = r.get("reads") or []
        if len(reads) < 2:
            fail("%d read(s), want 2 or more" % len(reads))
        for x in reads:
            rd = x.get("reader") or {}
            if not str(x.get("route") or "").strip() or not str(rd.get("file") or "").strip() or not rd.get("line") \
                    or not str(x.get("feeds_face") or "").strip() or "on_refusal_before" not in x or not str(x.get("on_refusal_after") or "").strip():
                fail("read %r lacks its reader, its face, or what the face says on a refusal" % x.get("route"))
        t = r.get("test") or {}
        mu = t.get("mutant") or {}
        if not str(t.get("id") or "").strip() or t.get("passes") is not True or not str(mu.get("what") or "").strip() or mu.get("failed") is not True:
            fail("the test lacks an id, a pass, or a failing mutant")
        n = shots(r)
        clean(r)
        if not r.get("product_files_changed"):
            fail("product_files_changed is empty")
        print("OK: %d refused read(s) traced to their faces; each face now states the refusal in words; %d screenshot(s) read" % (len(reads), n))
    elif cid == "IV113-AC1":
        r = record("SECTION_TITLE_UNIT.json")
        for k in ("title", "unit"):
            v = r.get(k) or {}
            for b in ("contract_declares", "producer_fixture_sends", "adapter_reads"):
                if not isinstance(v.get(b), bool):
                    fail("%s.%s is not a bool" % (k, b))
            for w in ("contract_where", "fixture_where", "adapter_where", "page_prints_when_absent"):
                if not str(v.get(w) or "").strip():
                    fail("%s.%s is empty" % (k, w))
        if r.get("verdict") not in ("PAGE", "PRODUCER", "BOTH", "NOT_ESTABLISHED") or not str(r.get("reason") or "").strip():
            fail("verdict %r or no reason" % r.get("verdict"))
        if not isinstance(r.get("served_answer_read"), bool) or not str(r.get("served_answer_how") or "").strip():
            fail("served_answer_read is not a bool, or served_answer_how is empty")
        if r.get("product_files_changed") != []:
            fail("product_files_changed %r in a read cell" % r.get("product_files_changed"))
        print("OK: title and unit traced through contract, producer fixture and adapter; verdict %s; served answer read: %s"
              % (r["verdict"], r["served_answer_read"]))
    elif cid == "IV114-AC1":
        r = record("HYGIENE_26.json")
        cw = r.get("colgroup_warning") or {}
        if not isinstance(cw.get("present_before"), bool) or cw.get("present_after") is not False or not str(cw.get("how_measured") or "").strip():
            fail("colgroup_warning %r" % cw)
        ct = r.get("contrast") or {}
        if not isinstance(ct.get("failing_before"), int) or not isinstance(ct.get("failing_after"), int) or ct["failing_after"] > ct["failing_before"] \
                or not str(ct.get("how_measured") or "").strip():
            fail("contrast %r" % ct)
        b = r.get("bands") or {}
        if not isinstance(b.get("count"), int) or not str(b.get("per_design_law") or "").strip() or not str(b.get("where") or "").strip():
            fail("bands %r" % b)
        n = shots(r)
        clean(r)
        print("OK: the colgroup warning is gone; low-contrast texts %d -> %d; %d band(s) counted against the design law; %d screenshot(s) read"
              % (ct["failing_before"], ct["failing_after"], b["count"], n))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
