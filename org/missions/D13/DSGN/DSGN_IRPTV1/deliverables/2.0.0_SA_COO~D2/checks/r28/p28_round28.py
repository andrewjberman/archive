"""DSGN_IRPTV1 round 28 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 5782 on row DSGN_IRPTV1-D2-W63-S2.

Cell: IV-e-116 a vendor card whose Label equals its title prints the title once; and a READ of whether the wire's section_id carries
a field slug the pinned census can name exactly (no product change for that part).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV116-AC1  ~64/LABEL_ONCE.json: label_equals_title {printed_once true, where {file, line}}; label_differs_unchanged true;
             opal_unchanged true; field_slug_read {census_fields (int), slugs_derivable (int), exact_matches (int), method,
             product_change false}; test {id, passes true, mutant {what, failed true}}; screenshots (1 or more existing, each in
             screenshots_read); lint_errors 0; typecheck_errors 0; suite_after.new_failing_ids == []; product_files_changed
             non-empty; portal_commit hex.
"""
import json
import re
import sys
from pathlib import Path

HEX = re.compile(r"^[0-9a-f]{7,40}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV28"))
        sys.exit(1)

    if cid != "IV116-AC1":
        fail("unknown criterion %r" % cid)
    folder = root / "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~64"
    p = folder / "LABEL_ONCE.json"
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    le = r.get("label_equals_title") or {}
    w = le.get("where") or {}
    if le.get("printed_once") is not True or not str(w.get("file") or "").strip() or not w.get("line"):
        fail("label_equals_title %r" % le)
    if r.get("label_differs_unchanged") is not True or r.get("opal_unchanged") is not True:
        fail("label_differs_unchanged %r, opal_unchanged %r" % (r.get("label_differs_unchanged"), r.get("opal_unchanged")))
    fs = r.get("field_slug_read") or {}
    if any(not isinstance(fs.get(k), int) for k in ("census_fields", "slugs_derivable", "exact_matches"))             or not str(fs.get("method") or "").strip() or fs.get("product_change") is not False:
        fail("field_slug_read %r" % fs)
    t = r.get("test") or {}
    mu = t.get("mutant") or {}
    if not str(t.get("id") or "").strip() or t.get("passes") is not True or not str(mu.get("what") or "").strip() or mu.get("failed") is not True:
        fail("the test lacks an id, a pass, or a failing mutant")
    s = r.get("screenshots") or []
    if not s or any(not (folder / str(x)).is_file() for x in s) or sorted(r.get("screenshots_read") or []) != sorted(s):
        fail("screenshots: one or more existing files, each in screenshots_read")
    if r.get("lint_errors") != 0 or r.get("typecheck_errors") != 0:
        fail("lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
    if (r.get("suite_after") or {}).get("new_failing_ids") != []:
        fail("suite_after.new_failing_ids %r" % (r.get("suite_after") or {}).get("new_failing_ids"))
    if not r.get("product_files_changed") or not HEX.match(str(r.get("portal_commit") or "")):
        fail("product_files_changed empty or portal_commit missing")
    print("OK: a label equal to its title prints once; of %d census fields %d slugs are derivable and %d match exactly; %d screenshot(s) read"
          % (fs["census_fields"], fs["slugs_derivable"], fs["exact_matches"], len(s)))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
