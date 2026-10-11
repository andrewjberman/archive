"""DSGN_IRPTV1 round 22 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msgs 5037 (the print and export document), 4992 (row D2-W54-S1),
4888 (the 130% weight) and 4864 / 2.0.0_SA_COO~P2 msg 4959 (the two corrected fixtures).

Cells: IV-e-105 the print and export document of an Opal report prints no vendor wording; IV-e-104 the batched test repairs (the smoke map
takes the two corrected routes; the ids that waited on the response schemas are re-run; IVE26-AC3's third arm; IV-e-97's flip);
IV-e-103 the 130% weight on a two-account client, read first.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV105-AC1  ~58/OPAL_DOCUMENT.json: surfaces lists every surface an Opal report can be printed or exported from, each {surface, file,
             line, vendor_words_before (list), opal_reads_after}; no opal_reads_after carries "vendor" or "extraction"; vendor_unchanged
             true; test {id, passes true, mutant {what, failed true}}; evidence >= 1 existing file in the worker's folder for an Opal
             document and one for a vendor document; typecheck_errors == 0; suite_after.new_failing_ids == []; product_files_changed
             non-empty; portal_commit hex.
  IV104-AC1  ~58/REPAIRS_22.json: smoke_map {routes_declared 22, keys, excused [{route, reason_class, reason}]} with keys == 22 minus
             the excused count and neither directory-browse nor analysis-input-upload excused unless that entry carries
             still_refused true with the refusal text; rerun_ids lists the five ids each PASS or FAIL with a reason; ive26 {outcome
             FIXED or NOT_FIXED with a reason}; ive97_flip {status_complete (bool), proof_valid (bool)}.
  IV104-AC2  the same record: build_equal true with equal non-empty before and after hashes; suite_after.new_failing_ids == [];
             product_files_changed == []; portal_commit hex.
  IV103-AC1  ~58/WEIGHT_130.json: reproduced (bool) with how RENDERED or TEST; weight_base {file, line, what} (the line that sets the
             denominator); verdict PAGE_DEFECT, FIXTURE_DEFECT or NOT_ESTABLISHED with a reason; PAGE_DEFECT carries fix {portal_commit,
             test {id, passes true, mutant {what, failed true}}} and product_files_changed non-empty; FIXTURE_DEFECT carries
             what_the_fixture_gets_wrong and product_files_changed == []; suite_after.new_failing_ids == [].
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~58/"
HEX = re.compile(r"^[0-9a-f]{7,40}$")
FIVE = ("content-pins", "content-pins", "content-pins", "producer-fixtures", "IVE17-AC3")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV22"))
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

    def tested(t):
        m = (t or {}).get("mutant") or {}
        return bool(text((t or {}).get("id"))) and (t or {}).get("passes") is True and bool(text(m.get("what"))) and m.get("failed") is True

    def clean(r):
        return (r.get("suite_after") or {}).get("new_failing_ids") == []

    if cid == "IV105-AC1":
        r = load("OPAL_DOCUMENT.json")
        ss = r.get("surfaces") or []
        if not ss:
            fail("surfaces empty")
        for s in ss:
            if not text(s.get("surface")) or not text(s.get("file")) or not isinstance(s.get("line"), int) or not isinstance(s.get("vendor_words_before"), list) \
                    or not text(s.get("opal_reads_after")):
                fail("surface %r lacks its file, line, vendor words or what an Opal report reads" % s.get("surface"))
            if re.search(r"vendor|extraction", text(s["opal_reads_after"]), re.I):
                fail("surface %r still reads a vendor word for an Opal report" % s.get("surface"))
        ev = r.get("evidence") or {}
        if r.get("vendor_unchanged") is not True or not tested(r.get("test")) or not infolder(ev.get("opal")) or not infolder(ev.get("vendor")):
            fail("vendor_unchanged, the test with its mutant, or the two evidence files")
        if r.get("typecheck_errors") != 0 or not clean(r) or not r.get("product_files_changed") or not HEX.match(text(r.get("portal_commit"))):
            fail("typecheck, suite_after, product_files_changed or portal_commit")
        print("OK: %d print/export surface(s); an Opal document reads no vendor word; a vendor document is unchanged" % len(ss))
    elif cid == "IV104-AC1":
        r = load("REPAIRS_22.json")
        sm = r.get("smoke_map") or {}
        ex = sm.get("excused") or []
        if sm.get("routes_declared") != 22 or sm.get("keys") != 22 - len(ex):
            fail("smoke_map keys %r with %d excuse(s) of 22 declared" % (sm.get("keys"), len(ex)))
        for x in ex:
            if not text(x.get("route")) or not text(x.get("reason_class")) or not text(x.get("reason")):
                fail("excuse %r" % x.get("route"))
            if text(x["route"]) in ("directory-browse", "analysis-input-upload") and (x.get("still_refused") is not True or not text(x.get("refusal_text"))):
                fail("%s is still excused without a measured refusal of the corrected fixture" % x["route"])
        rr = r.get("rerun_ids") or []
        if len(rr) != 5 or any(x.get("result") not in ("PASS", "FAIL") or not text(x.get("id")) or (x["result"] == "FAIL" and not text(x.get("reason"))) for x in rr):
            fail("rerun_ids wants the five ids, each PASS or FAIL with a reason")
        iv = r.get("ive26") or {}
        if iv.get("outcome") not in ("FIXED", "NOT_FIXED") or (iv["outcome"] == "NOT_FIXED" and not text(iv.get("reason"))):
            fail("ive26 %r" % iv)
        fl = r.get("ive97_flip") or {}
        if not isinstance(fl.get("status_complete"), bool) or not isinstance(fl.get("proof_valid"), bool):
            fail("ive97_flip %r" % fl)
        print("OK: the smoke map at %d keys with %d excuse(s); five ids re-run %r; IVE26-AC3 %s; IV-e-97 flipped: %s"
              % (sm["keys"], len(ex), [x["result"] for x in rr], iv["outcome"], fl["status_complete"]))
    elif cid == "IV104-AC2":
        r = load("REPAIRS_22.json")
        if r.get("build_equal") is not True or not text(r.get("build_hash_before")) or r.get("build_hash_before") != r.get("build_hash_after"):
            fail("the build hash is not equal before and after")
        if not clean(r) or r.get("product_files_changed") != [] or not HEX.match(text(r.get("portal_commit"))):
            fail("suite_after, product_files_changed (must be []) or portal_commit")
        print("OK: the production build is byte-equal; no product file changed; no new failing id")
    elif cid == "IV103-AC1":
        r = load("WEIGHT_130.json")
        wb = r.get("weight_base") or {}
        if not isinstance(r.get("reproduced"), bool) or r.get("how") not in ("RENDERED", "TEST") or not text(wb.get("file")) or not isinstance(wb.get("line"), int) or not text(wb.get("what")):
            fail("reproduced / how / weight_base")
        v = r.get("verdict")
        if v not in ("PAGE_DEFECT", "FIXTURE_DEFECT", "NOT_ESTABLISHED") or not text(r.get("reason")):
            fail("verdict %r" % v)
        if v == "PAGE_DEFECT":
            fx = r.get("fix") or {}
            if not HEX.match(text(fx.get("portal_commit"))) or not tested(fx.get("test")) or not r.get("product_files_changed"):
                fail("PAGE_DEFECT wants a fix with a test, a failing mutant and product_files_changed")
        elif r.get("product_files_changed") != [] or (v == "FIXTURE_DEFECT" and not text(r.get("what_the_fixture_gets_wrong"))):
            fail("%s with product files changed, or no statement of what the fixture gets wrong" % v)
        if not clean(r):
            fail("suite_after.new_failing_ids")
        print("OK: the 130%% weight: %s (%s)" % (v, text(r["reason"])[:80]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
