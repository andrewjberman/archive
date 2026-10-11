"""DSGN_IRPTV1 round 29 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 5852: the Holdings tab passes PanelFooter its light ground.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV117-AC1  ~65/HOLDINGS_FOOTER_LIGHT.json: footers (2 or more) each {file (under the Holdings tab folder), line (int), ground
             "light"}; shared_ui_changed false; product_files_changed non-empty, every entry under
             src/pages/InvestorReporting/tabs/holdings/; navy_strips {before (int), after (int), removed (int >= 2) with
             before - after == removed, how}; footer_text_contrast {ratio (number >= 4.5), how}; test {file, mutant_failed true};
             lint_errors 0; typecheck_errors 0; suite_after {fail 0}; screenshots (1 or more) each an existing file, with
             screenshot_read true; portal_commit a 40-hex string.
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/"
HOLD = "src/pages/InvestorReporting/tabs/holdings/"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV117"))
        sys.exit(1)

    if cid != "IV117-AC1":
        fail("unknown criterion %r" % cid)
    folder = root / (M + "0.9.0_WK_DSGN_IRPTV1~65")
    p = folder / "HOLDINGS_FOOTER_LIGHT.json"
    if not p.is_file():
        fail("no record 0.9.0_WK_DSGN_IRPTV1~65/HOLDINGS_FOOTER_LIGHT.json")
    r = json.loads(p.read_bytes().decode("utf-8"))
    ft = r.get("footers") or []
    if len(ft) < 2:
        fail("%d footer(s), want 2 or more" % len(ft))
    for f in ft:
        if HOLD not in str(f.get("file") or "").replace("\\", "/") or not isinstance(f.get("line"), int) or f.get("ground") != "light":
            fail("footer %r is not a Holdings tab file with its line and ground light" % f.get("file"))
    if r.get("shared_ui_changed") is not False:
        fail("shared_ui_changed %r" % r.get("shared_ui_changed"))
    pf = [str(x).replace("\\", "/") for x in (r.get("product_files_changed") or [])]
    if not pf or any(HOLD not in x for x in pf):
        fail("product_files_changed must be non-empty and all under the Holdings tab folder: %r" % pf)
    ns = r.get("navy_strips") or {}
    if not all(isinstance(ns.get(k), int) for k in ("before", "after", "removed")) or ns["removed"] < 2 \
            or ns["before"] - ns["after"] != ns["removed"] or not str(ns.get("how") or "").strip():
        fail("navy_strips %r" % {k: ns.get(k) for k in ("before", "after", "removed")})
    c = r.get("footer_text_contrast") or {}
    if not isinstance(c.get("ratio"), (int, float)) or isinstance(c.get("ratio"), bool) or c["ratio"] < 4.5 or not str(c.get("how") or "").strip():
        fail("footer_text_contrast %r" % c.get("ratio"))
    t = r.get("test") or {}
    if not str(t.get("file") or "").strip() or t.get("mutant_failed") is not True:
        fail("test needs its file and a mutant that failed")
    if r.get("lint_errors") != 0 or r.get("typecheck_errors") != 0:
        fail("lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
    if (r.get("suite_after") or {}).get("fail") != 0:
        fail("suite_after.fail %r" % (r.get("suite_after") or {}).get("fail"))
    shots = r.get("screenshots") or []
    if not shots or r.get("screenshot_read") is not True or any(not (folder / str(s)).is_file() for s in shots):
        fail("screenshots must each exist in the worker's folder and be read")
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("portal_commit") or "")):
        fail("portal_commit %r" % r.get("portal_commit"))
    print("OK: %d Holdings footer(s) on the light ground; navy strips %d -> %d; footer text contrast %.2f; %d screenshot(s) read"
          % (len(ft), ns["before"], ns["after"], c["ratio"], len(shots)))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
