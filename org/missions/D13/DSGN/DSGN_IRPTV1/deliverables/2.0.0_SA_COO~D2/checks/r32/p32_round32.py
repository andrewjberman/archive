"""DSGN_IRPTV1 round 32 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 6671: the round list after the round-31 slug.

Cells: IV-e-123 (row D2-W69-S2) one read of the holdings producer: is an ACCOUNT node's id equal to the account id on every served path, and where it is not,
the page maps the node ref to the account id before the focus post; IV-e-124 (row D2-W70-S4) the unsupported-card reason on an UNCERTIFIED vendor report is worded
like the face's one validation sentence, with no producer token.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV123-AC1  ~72/NODE_ID_READ.json: producer_reads (list, 1 or more, each {file, line int, rule}); denominator {paths_enumerated int >= 1, paths_read int equal to
             it, basis}; ids_equal_on_all bool; product_change bool, true exactly when ids_equal_on_all is false; when product_change: page_maps_node_ref true,
             test {file, mutant_failed true}, lint_errors 0, typecheck_errors 0, suite_base / suite_after (after fail no greater than base, new_failing_ids []),
             product_files_changed non-empty and each under src/pages/InvestorReporting/tabs/holdings/, portal_commit 40 hex; when not product_change:
             product_files_changed [].
  IV124-AC1  ~73/UNSUPPORTED_REASON.json: reason_sentence (non-empty string) holding none of CERTIFIED, UNCERTIFIED, FAILED, 'extraction validation', 'reasonCode';
             contains_producer_token false; vendor_only true; opal_report_unchanged true; test {file, mutant_failed true}; lint_errors 0; typecheck_errors 0;
             suite_base / suite_after as above; screenshots (1 or more, each existing) with screenshot_read true; product_files_changed non-empty, each under
             src/pages/InvestorReporting/tabs/analysis/; portal_commit 40 hex.
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/"
BANNED = ("CERTIFIED", "UNCERTIFIED", "FAILED", "extraction validation", "reasonCode")


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV32"))
        sys.exit(1)

    def record(folder, name):
        p = root / (M + folder) / name
        if not p.is_file():
            fail("no record %s/%s" % (folder, name))
        return json.loads(p.read_bytes().decode("utf-8")), root / (M + folder)

    def build_gates(r, allowed):
        t = r.get("test") or {}
        if not str(t.get("file") or "").strip() or t.get("mutant_failed") is not True:
            fail("test needs its file and a mutant that failed")
        if r.get("lint_errors") != 0 or r.get("typecheck_errors") != 0:
            fail("lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
        sb, sa = r.get("suite_base") or {}, r.get("suite_after") or {}
        if not is_int(sb.get("fail")) or not is_int(sa.get("fail")) or sa["fail"] > sb["fail"] or sa.get("new_failing_ids") != []:
            fail("suite: base fail %r, after fail %r, new_failing_ids %r" % (sb.get("fail"), sa.get("fail"), sa.get("new_failing_ids")))
        if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("portal_commit") or "")):
            fail("portal_commit %r" % r.get("portal_commit"))
        pf = [str(x).replace("\\", "/") for x in (r.get("product_files_changed") or [])]
        if not pf or any(allowed not in x for x in pf):
            fail("product_files_changed %r must be non-empty and under %s" % (pf, allowed))

    if cid == "IV123-AC1":
        r, _ = record("0.9.0_WK_DSGN_IRPTV1~72", "NODE_ID_READ.json")
        reads = r.get("producer_reads")
        if not isinstance(reads, list) or not reads or any(
                not str((x or {}).get("file") or "").strip() or not is_int((x or {}).get("line")) or not str((x or {}).get("rule") or "").strip() for x in reads):
            fail("producer_reads needs 1 or more entries, each with file, line (int) and rule")
        d = r.get("denominator") or {}
        if not is_int(d.get("paths_enumerated")) or d["paths_enumerated"] < 1 or d.get("paths_read") != d["paths_enumerated"] or not str(d.get("basis") or "").strip():
            fail("denominator %r" % d)
        if not isinstance(r.get("ids_equal_on_all"), bool) or not isinstance(r.get("product_change"), bool) \
                or r["product_change"] != (not r["ids_equal_on_all"]):
            fail("ids_equal_on_all and product_change must be booleans, product_change true exactly when the ids differ")
        if r["product_change"]:
            if r.get("page_maps_node_ref") is not True:
                fail("product_change true needs page_maps_node_ref true")
            build_gates(r, "src/pages/InvestorReporting/tabs/holdings/")
        elif r.get("product_files_changed") not in ([], None):
            fail("no product change, so product_files_changed must be empty")
        print("OK: %d of %d path(s) read; ids_equal_on_all %s; product_change %s"
              % (d["paths_read"], d["paths_enumerated"], r["ids_equal_on_all"], r["product_change"]))
    elif cid == "IV124-AC1":
        r, folder = record("0.9.0_WK_DSGN_IRPTV1~73", "UNSUPPORTED_REASON.json")
        s = str(r.get("reason_sentence") or "")
        if not s.strip() or any(b in s for b in BANNED) or r.get("contains_producer_token") is not False:
            fail("reason_sentence must be non-empty and carry no producer token (%r)" % (BANNED,))
        if r.get("vendor_only") is not True or r.get("opal_report_unchanged") is not True:
            fail("vendor_only and opal_report_unchanged must both be true")
        build_gates(r, "src/pages/InvestorReporting/tabs/analysis/")
        shots = r.get("screenshots") or []
        if not shots or r.get("screenshot_read") is not True or any(not (folder / str(x)).is_file() for x in shots):
            fail("screenshots must each exist in the worker's folder and be read")
        print("OK: the unsupported-card reason reads %r; %d screenshot(s) read" % (s[:80], len(shots)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
