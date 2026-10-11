"""DSGN_IRPTV1 round 21 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's rulings msg 4924 and msg 4958 (IRPT_YCDGEN ROUND-12 ANALYSIS
@71a14ece46, section 2): two page cells, ahead of the wire-folder regeneration.

Cells: IV-e-101 an Opal report opened on the page prints no vendor wording; IV-e-102 the report can be opened after a Prospect upload
(a rendered read first).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV101-AC1  ~57/OPAL_WORDING.json: provider_known {how, file, line}; wording.opal and wording.vendor each {attribution, validation};
             the opal words contain neither "vendor" nor "extraction" (any case); the vendor words equal vendor_before (unchanged);
             test {id, passes true, mutant {what, failed true}}.
  IV101-AC2  the same record: screenshots >= 2 [{state, path, canvas}], states naming an opal and a vendor report, each path an existing
             file in the worker's folder, canvas "rgb(244, 246, 250)"; typecheck_errors == 0; suite_after.new_failing_ids == [];
             product_files_changed non-empty; portal_commit hex.
  IV102-AC1  ~57/PROSPECT_OPEN.json: measured {opener_mounts_without_client (bool), how RENDERED, evidence (an existing file in the
             worker's folder)}; outcome FIXED, NOT_A_DEFECT or STOPPED (STOPPED carries a row); the outcome agrees with the measurement
             (mounts already -> NOT_A_DEFECT; does not mount -> FIXED or STOPPED).
  IV102-AC2  the same record: FIXED -> test {id, passes true, mutant {what, failed true}}, after {opener_mounts_without_client true,
             evidence existing file}, product_files_changed non-empty; NOT_A_DEFECT or STOPPED -> product_files_changed == [].
             Always: typecheck_errors == 0, suite_after.new_failing_ids == [], portal_commit hex.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~57/"
HEX = re.compile(r"^[0-9a-f]{7,40}$")
CANVAS = "rgb(244, 246, 250)"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV21"))
        sys.exit(1)

    def text(v):
        return str(v or "").strip()

    def load(name):
        p = root / (D + name)
        if not p.is_file():
            fail("no record %s" % name)
        return json.loads(p.read_bytes().decode("utf-8"))

    def infolder(path):
        return text(path).startswith(D) and (root / text(path)).is_file()

    def tail(r):
        if r.get("typecheck_errors") != 0 or (r.get("suite_after") or {}).get("new_failing_ids") != [] or not HEX.match(text(r.get("portal_commit"))):
            fail("want typecheck_errors 0, suite_after.new_failing_ids == [] and a portal_commit")

    def tested(t):
        m = (t or {}).get("mutant") or {}
        return bool(text((t or {}).get("id"))) and (t or {}).get("passes") is True and bool(text(m.get("what"))) and m.get("failed") is True

    if cid == "IV101-AC1":
        r = load("OPAL_WORDING.json")
        pk = r.get("provider_known") or {}
        if not text(pk.get("how")) or not text(pk.get("file")) or not isinstance(pk.get("line"), int):
            fail("provider_known %r" % pk)
        w = r.get("wording") or {}
        o, v, vb = w.get("opal") or {}, w.get("vendor") or {}, r.get("vendor_before") or {}
        for k in ("attribution", "validation"):
            if not text(o.get(k)) or not text(v.get(k)):
                fail("wording lacks %s for opal or vendor" % k)
            if re.search(r"vendor|extraction", text(o[k]), re.I):
                fail("the opal %s wording %r still carries a vendor word" % (k, o[k]))
            if v[k] != vb.get(k):
                fail("the vendor %s wording moved: %r, before %r" % (k, v[k], vb.get(k)))
        if not tested(r.get("test")):
            fail("test %r" % r.get("test"))
        print("OK: an Opal report reads %r / %r; a vendor report is unchanged; a test holds it and a mutant breaks it" % (o["attribution"], o["validation"]))
    elif cid == "IV101-AC2":
        r = load("OPAL_WORDING.json")
        sh = r.get("screenshots") or []
        states = " ".join(text(x.get("state")).lower() for x in sh)
        if len(sh) < 2 or "opal" not in states or "vendor" not in states or any(not infolder(x.get("path")) or x.get("canvas") != CANVAS for x in sh):
            fail("screenshots: want an opal and a vendor state, each an existing file in the worker's folder on the light canvas")
        if not r.get("product_files_changed"):
            fail("product_files_changed empty")
        tail(r)
        print("OK: %d screenshot(s) read on the light canvas; typecheck clean; no new failing id" % len(sh))
    elif cid == "IV102-AC1":
        r = load("PROSPECT_OPEN.json")
        m = r.get("measured") or {}
        if not isinstance(m.get("opener_mounts_without_client"), bool) or m.get("how") != "RENDERED" or not infolder(m.get("evidence")):
            fail("measured %r: want a bool, how RENDERED and an evidence file in the worker's folder" % {k: m.get(k) for k in ("opener_mounts_without_client", "how")})
        oc = r.get("outcome")
        if oc not in ("FIXED", "NOT_A_DEFECT", "STOPPED") or (oc == "STOPPED" and not text(r.get("row"))):
            fail("outcome %r" % oc)
        if m["opener_mounts_without_client"] and oc != "NOT_A_DEFECT":
            fail("the opener already mounts, so the outcome is NOT_A_DEFECT, not %r" % oc)
        if not m["opener_mounts_without_client"] and oc == "NOT_A_DEFECT":
            fail("the opener does not mount, so NOT_A_DEFECT is not the outcome")
        print("OK: rendered read: the opener %s with no client in the header; outcome %s" % ("mounts" if m["opener_mounts_without_client"] else "does NOT mount", oc))
    elif cid == "IV102-AC2":
        r = load("PROSPECT_OPEN.json")
        oc = r.get("outcome")
        if oc == "FIXED":
            a = r.get("after") or {}
            if not tested(r.get("test")) or a.get("opener_mounts_without_client") is not True or not infolder(a.get("evidence")) or not r.get("product_files_changed"):
                fail("FIXED wants a test with a failing mutant, a rendered after-read and product_files_changed")
        elif r.get("product_files_changed") != []:
            fail("outcome %r with product files changed" % oc)
        tail(r)
        print("OK: outcome %s; typecheck clean; no new failing id" % oc)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
