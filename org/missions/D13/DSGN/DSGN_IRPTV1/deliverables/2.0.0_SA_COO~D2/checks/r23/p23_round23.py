"""DSGN_IRPTV1 round 23 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ROUND-23 ANALYSIS @b417e9ee3c, section 4.

Cells: IV-e-106 the PROD candidate record, with retained_ref carried by the sections reader; IV-e-108 the Holdings face names the picked
account and labels its totals, and the header's picker hands the tabs the picked account; IV-e-109 hygiene (the raw NUL byte, the
generator and the tracked request fixture, ui-smoke picking a client). Item 2 of the list (the ask for the laptop's rendered walk) is the
issuer's own document and carries no order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV106-AC1  ~59/PROD_CANDIDATE.json: candidate_commit (40 hex), prod_commit starting 37aa1247ee, pushed false; files_changed (int > 0);
             pages [{page, class (CLIENT_FACING or OPAL_INTERNAL), files (int)}] whose files sum to files_changed; status_reads has
             exactly analysis-request-pdf and analysis-request-original, each CARRIED or NOT_CARRIED with where; retained_ref {carried
             true, test {id, passes true, mutant {what, failed true}}}; lint_errors 0; typecheck_errors 0;
             suite_after.new_failing_ids == [].
  IV108-AC1  ~60/HOLDINGS_FACE.json: picked_account_named {where, text}; totals_labelled (2 or more) each {total, label};
             header_picker {hands_tabs (bool), how}; a false carries a reason and a row id; test {id, passes true, mutant {what,
             failed true}}; screenshots: 2 or more existing files in the worker's folder, each named in screenshots_read; lint_errors 0;
             typecheck_errors 0; suite_after.new_failing_ids == []; product_files_changed non-empty; portal_commit hex.
  IV109-AC1  ~59/HYGIENE_23.json: nul_byte {bytes_before (int >= 1), bytes_after 0}; generator {captured_member_kept true, test or
             how}; ui_smoke {can_pick_client (bool), how}; a false carries a reason; lint_errors 0; typecheck_errors 0;
             suite_after.new_failing_ids == []; build_equal true with equal non-empty hashes; product_files_changed == [];
             portal_commit hex.
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX = re.compile(r"^[0-9a-f]{7,40}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV23"))
        sys.exit(1)

    def record(rel):
        p = root / (M + rel)
        if not p.is_file():
            fail("no record %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def test_ok(t, what):
        t = t or {}
        mu = t.get("mutant") or {}
        if not str(t.get("id") or "").strip() or t.get("passes") is not True or not str(mu.get("what") or "").strip() or mu.get("failed") is not True:
            fail("%s: the test lacks an id, a pass, or a failing mutant" % what)

    def clean(r):
        if r.get("lint_errors") != 0 or r.get("typecheck_errors") != 0:
            fail("lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
        if (r.get("suite_after") or {}).get("new_failing_ids") != []:
            fail("suite_after.new_failing_ids %r" % (r.get("suite_after") or {}).get("new_failing_ids"))

    if cid == "IV106-AC1":
        r = record("0.9.0_WK_DSGN_IRPTV1~59/PROD_CANDIDATE.json")
        if not HEX40.match(str(r.get("candidate_commit") or "")) or not str(r.get("prod_commit") or "").startswith("37aa1247ee") or r.get("pushed") is not False:
            fail("candidate_commit, prod_commit or pushed is not as required")
        pages = r.get("pages") or []
        n = r.get("files_changed")
        if not isinstance(n, int) or n < 1 or not pages:
            fail("files_changed %r, pages %d" % (n, len(pages)))
        for p in pages:
            if not str(p.get("page") or "").strip() or p.get("class") not in ("CLIENT_FACING", "OPAL_INTERNAL") or not isinstance(p.get("files"), int):
                fail("a page lacks its name, class or file count: %r" % p.get("page"))
        if sum(p["files"] for p in pages) != n:
            fail("the pages' files sum to %d, files_changed is %d" % (sum(p["files"] for p in pages), n))
        sr = r.get("status_reads") or {}
        if sorted(sr) != ["analysis-request-original", "analysis-request-pdf"]:
            fail("status_reads keys %r" % sorted(sr))
        for k, v in sr.items():
            if (v or {}).get("state") not in ("CARRIED", "NOT_CARRIED") or not str(v.get("where") or "").strip():
                fail("status read %s lacks its state or where" % k)
        rr = r.get("retained_ref") or {}
        if rr.get("carried") is not True:
            fail("retained_ref.carried %r" % rr.get("carried"))
        test_ok(rr.get("test"), "retained_ref")
        clean(r)
        print("OK: candidate %s over PROD %s: %d file(s) across %d page(s), %d client-facing; retained_ref carried; the two status reads: %s"
              % (r["candidate_commit"][:10], r["prod_commit"][:10], n, len(pages), sum(1 for p in pages if p["class"] == "CLIENT_FACING"),
                 ", ".join("%s %s" % (k, sr[k]["state"]) for k in sorted(sr))))
    elif cid == "IV108-AC1":
        folder = root / (M + "0.9.0_WK_DSGN_IRPTV1~60")
        r = record("0.9.0_WK_DSGN_IRPTV1~60/HOLDINGS_FACE.json")
        pa = r.get("picked_account_named") or {}
        if not str(pa.get("where") or "").strip() or not str(pa.get("text") or "").strip():
            fail("picked_account_named lacks where or text")
        tl = r.get("totals_labelled") or []
        if len(tl) < 2 or any(not str(t.get("total") or "").strip() or not str(t.get("label") or "").strip() for t in tl):
            fail("totals_labelled wants 2 or more, each with its total and label")
        hp = r.get("header_picker") or {}
        if not isinstance(hp.get("hands_tabs"), bool) or not str(hp.get("how") or "").strip():
            fail("header_picker lacks hands_tabs or how")
        if hp["hands_tabs"] is False and (not str(hp.get("reason") or "").strip() or not str(hp.get("row") or "").strip()):
            fail("header_picker false with no reason or row")
        test_ok(r.get("test"), "the Holdings face")
        shots = r.get("screenshots") or []
        if len(shots) < 2 or any(not (folder / str(s)).is_file() for s in shots) or sorted(r.get("screenshots_read") or []) != sorted(shots):
            fail("screenshots: 2 or more existing files, each in screenshots_read")
        clean(r)
        if not r.get("product_files_changed") or not HEX.match(str(r.get("portal_commit") or "")):
            fail("product_files_changed empty or portal_commit missing")
        print("OK: the picked account is named (%s); %d totals labelled; the header's picker hands the tabs the account: %s; %d screenshot(s) read"
              % (pa["where"], len(tl), hp["hands_tabs"], len(shots)))
    elif cid == "IV109-AC1":
        r = record("0.9.0_WK_DSGN_IRPTV1~59/HYGIENE_23.json")
        nb = r.get("nul_byte") or {}
        if not isinstance(nb.get("bytes_before"), int) or nb["bytes_before"] < 1 or nb.get("bytes_after") != 0:
            fail("nul_byte %r" % nb)
        g = r.get("generator") or {}
        if g.get("captured_member_kept") is not True or not str(g.get("how") or "").strip():
            fail("generator %r" % g)
        u = r.get("ui_smoke") or {}
        if not isinstance(u.get("can_pick_client"), bool) or not str(u.get("how") or "").strip():
            fail("ui_smoke lacks can_pick_client or how")
        if u["can_pick_client"] is False and not str(u.get("reason") or "").strip():
            fail("ui_smoke false with no reason")
        clean(r)
        b = r.get("build") or {}
        if r.get("build_equal") is not True or not str(b.get("before") or "").strip() or b.get("before") != b.get("after"):
            fail("build_equal %r with hashes %r" % (r.get("build_equal"), b))
        if r.get("product_files_changed") != [] or not HEX.match(str(r.get("portal_commit") or "")):
            fail("product_files_changed %r or portal_commit missing" % r.get("product_files_changed"))
        print("OK: %d NUL byte(s) removed; the generator keeps the captured member; ui-smoke can pick a client: %s; build equal"
              % (nb["bytes_before"], u["can_pick_client"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
