"""DSGN_IRPTV1 round 31 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 6625: the round list after the rounds 24-30 slug.

Cells: IV-e-120 the Total Assets base sits inside the shared card (row D2-W60-S1, the CTO's grant on CategoryViewTree.tsx);
IV-e-121 an ACCOUNT row picked in the header starts Performance's Account select on that account, proven on a rendered page
(row D2-S24); IV-e-122 the vendor report's face carries the validation line and the source line from the wire's
extraction_validation (row D2-S21).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV120-AC1  ~68/TOTAL_BASE_IN_CARD.json: base_in_card true; caption_above_removed true; prop {file, name}; census {mounts_found
             (int >= 1), pages_rendered_before_after (int == mounts_found), unchanged_outside_holdings true, partner_login_pages
             (list), denominator_source}; test {file, mutant_failed true}; lint_errors 0; typecheck_errors 0; suite_base.fail and
             suite_after.fail ints with after no greater than base and suite_after.new_failing_ids []; screenshots (1 or more,
             each an existing file) with screenshot_read true; product_files_changed non-empty, each under
             src/pages/InvestorReporting/ or exactly src/components/CategoryViewTree.tsx; portal_commit a 40-hex string.
  IV121-AC1  ~69/ACCOUNT_PICK_RENDERED.json: header_yields ACCOUNT_ROW / CLIENT_ROW with header_basis; rendered {account_select_
             starts_on_picked true, holdings_opens_on_picked true, row_kind_rendered ACCOUNT_ROW}; product_change bool (a change
             needs product_files_changed non-empty); test {file, mutant_failed true}; lint_errors 0; typecheck_errors 0; suite_base
             and suite_after as above; screenshots read; portal_commit a 40-hex string.
  IV122-AC1  ~70/VALIDATION_SOURCE_LINES.json: validation_line {on_face true, inside_closed_details false, keys_read the four
             keys status / checks_run / checks_failed / notes}; source_line {on_face true, from}; opal_report_unchanged true; test
             {file, mutant_failed true}; lint_errors 0; typecheck_errors 0; suite as above; screenshots read; product_files_changed
             under src/pages/InvestorReporting/; portal_commit a 40-hex string.
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/"
FOUR_KEYS = {"status", "checks_run", "checks_failed", "notes"}


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV31"))
        sys.exit(1)

    def record(folder, name):
        p = root / (M + folder) / name
        if not p.is_file():
            fail("no record %s/%s" % (folder, name))
        return json.loads(p.read_bytes().decode("utf-8")), root / (M + folder)

    def common(r, folder, allowed):
        t = r.get("test") or {}
        if not str(t.get("file") or "").strip() or t.get("mutant_failed") is not True:
            fail("test needs its file and a mutant that failed")
        if r.get("lint_errors") != 0 or r.get("typecheck_errors") != 0:
            fail("lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
        sb, sa = r.get("suite_base") or {}, r.get("suite_after") or {}
        if not is_int(sb.get("fail")) or not is_int(sa.get("fail")) or sa["fail"] > sb["fail"] or sa.get("new_failing_ids") != []:
            fail("suite: base fail %r, after fail %r, new_failing_ids %r" % (sb.get("fail"), sa.get("fail"), sa.get("new_failing_ids")))
        shots = r.get("screenshots") or []
        if not shots or r.get("screenshot_read") is not True or any(not (folder / str(s)).is_file() for s in shots):
            fail("screenshots must each exist in the worker's folder and be read")
        if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("portal_commit") or "")):
            fail("portal_commit %r" % r.get("portal_commit"))
        pf = [str(x).replace("\\", "/") for x in (r.get("product_files_changed") or [])]
        for x in pf:
            if not any(x.endswith(a) if a.startswith("src/components/") else a in x for a in allowed):
                fail("product file outside the grant: %r" % x)
        return pf

    if cid == "IV120-AC1":
        r, folder = record("0.9.0_WK_DSGN_IRPTV1~68", "TOTAL_BASE_IN_CARD.json")
        if r.get("base_in_card") is not True or r.get("caption_above_removed") is not True:
            fail("base_in_card and caption_above_removed must both be true")
        pr = r.get("prop") or {}
        if not str(pr.get("file") or "").strip() or not str(pr.get("name") or "").strip():
            fail("prop needs its file and name")
        ce = r.get("census") or {}
        if not is_int(ce.get("mounts_found")) or ce["mounts_found"] < 1 or ce.get("pages_rendered_before_after") != ce["mounts_found"] \
                or ce.get("unchanged_outside_holdings") is not True or not isinstance(ce.get("partner_login_pages"), list) \
                or not str(ce.get("denominator_source") or "").strip():
            fail("census %r" % {k: ce.get(k) for k in ("mounts_found", "pages_rendered_before_after", "unchanged_outside_holdings", "partner_login_pages")})
        pf = common(r, folder, ("src/pages/InvestorReporting/", "src/components/CategoryViewTree.tsx"))
        if not pf:
            fail("product_files_changed is empty")
        print("OK: the Total Assets base is inside the card; %d mount(s) censused and rendered before and after; %d screenshot(s) read"
              % (ce["mounts_found"], len(r["screenshots"])))
    elif cid == "IV121-AC1":
        r, folder = record("0.9.0_WK_DSGN_IRPTV1~69", "ACCOUNT_PICK_RENDERED.json")
        if r.get("header_yields") not in ("ACCOUNT_ROW", "CLIENT_ROW") or not str(r.get("header_basis") or "").strip():
            fail("header_yields (ACCOUNT_ROW / CLIENT_ROW) and header_basis are required")
        rd = r.get("rendered") or {}
        if rd.get("account_select_starts_on_picked") is not True or rd.get("holdings_opens_on_picked") is not True \
                or rd.get("row_kind_rendered") != "ACCOUNT_ROW":
            fail("rendered %r" % rd)
        if not isinstance(r.get("product_change"), bool):
            fail("product_change must be true or false")
        pf = common(r, folder, ("src/pages/InvestorReporting/",))
        if r["product_change"] and not pf:
            fail("product_change true needs product_files_changed")
        print("OK: an ACCOUNT row picked in the header starts Performance's Account select on it and Holdings opens on it, rendered; header yields %s; product_change %s"
              % (r["header_yields"], r["product_change"]))
    elif cid == "IV122-AC1":
        r, folder = record("0.9.0_WK_DSGN_IRPTV1~70", "VALIDATION_SOURCE_LINES.json")
        v = r.get("validation_line") or {}
        if v.get("on_face") is not True or v.get("inside_closed_details") is not False or set(v.get("keys_read") or []) != FOUR_KEYS:
            fail("validation_line %r" % v)
        s = r.get("source_line") or {}
        if s.get("on_face") is not True or not str(s.get("from") or "").strip():
            fail("source_line needs on_face true and where it is read from")
        if r.get("opal_report_unchanged") is not True:
            fail("opal_report_unchanged must be true")
        pf = common(r, folder, ("src/pages/InvestorReporting/",))
        if not pf:
            fail("product_files_changed is empty")
        print("OK: the vendor report face carries its validation line (four keys) and its source line; %d screenshot(s) read" % len(r["screenshots"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
