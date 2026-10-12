"""DSGN_IRPTV1 round 27 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 5664 on row DSGN_IRPTV1-D2-S21.

Cell: IV-e-115 the page maps a vendor section's code to its census name (the 33 names copied from the pinned census, with a test that
fails if the copy differs) and maps the 12 unit tokens the producer sends; an unmapped code prints the code and an unmapped token
prints the token, never "unknown".

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV115-AC1  ~63/SECTION_NAMES_UNITS.json: census {path, pin, sha256} where the workspace file at path hashes to sha256 and holds 33
             sections; names {copied 33, copy_file, drift_test {id, passes true, mutant {what, failed true}}};
             unmapped_code_prints_code true; units {tokens (12), mapped (12), unmapped_token_prints_token true};
             fixtures_changed (a list); screenshots (1 or more existing, each in screenshots_read); lint_errors 0;
             typecheck_errors 0; suite_after.new_failing_ids == []; product_files_changed non-empty; portal_commit hex.
"""
import hashlib
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
        print("%s FAIL" % (cid or "IV27"))
        sys.exit(1)

    if cid != "IV115-AC1":
        fail("unknown criterion %r" % cid)
    folder = root / "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~63"
    p = folder / "SECTION_NAMES_UNITS.json"
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    c = r.get("census") or {}
    cp = root / str(c.get("path") or "")
    if not cp.is_file() or not str(c.get("pin") or "").strip():
        fail("census path or pin missing")
    raw = cp.read_bytes()
    if hashlib.sha256(raw).hexdigest() != c.get("sha256"):
        fail("the census file does not hash to the record's sha256")
    if len(json.loads(raw.decode("utf-8")).get("sections") or []) != 33:
        fail("the census does not hold 33 sections")
    n = r.get("names") or {}
    dt = n.get("drift_test") or {}
    mu = dt.get("mutant") or {}
    if n.get("copied") != 33 or not str(n.get("copy_file") or "").strip() or not str(dt.get("id") or "").strip() or dt.get("passes") is not True \
            or not str(mu.get("what") or "").strip() or mu.get("failed") is not True:
        fail("names: 33 copied, the copy's file, and a drift test with a failing mutant are required")
    if r.get("unmapped_code_prints_code") is not True:
        fail("unmapped_code_prints_code %r" % r.get("unmapped_code_prints_code"))
    u = r.get("units") or {}
    if len(u.get("tokens") or []) != 12 or len(u.get("mapped") or []) != 12 or sorted(u["tokens"]) != sorted(u["mapped"]) \
            or u.get("unmapped_token_prints_token") is not True:
        fail("units: 12 tokens, all 12 mapped, and an unmapped token printing itself are required")
    if not isinstance(r.get("fixtures_changed"), list):
        fail("fixtures_changed is not a list")
    s = r.get("screenshots") or []
    if not s or any(not (folder / str(x)).is_file() for x in s) or sorted(r.get("screenshots_read") or []) != sorted(s):
        fail("screenshots: one or more existing files, each in screenshots_read")
    if r.get("lint_errors") != 0 or r.get("typecheck_errors") != 0:
        fail("lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
    if (r.get("suite_after") or {}).get("new_failing_ids") != []:
        fail("suite_after.new_failing_ids %r" % (r.get("suite_after") or {}).get("new_failing_ids"))
    if not r.get("product_files_changed") or not HEX.match(str(r.get("portal_commit") or "")):
        fail("product_files_changed empty or portal_commit missing")
    print("OK: 33 census names copied with a drift test; 12 of 12 unit tokens mapped; an unmapped code or token prints itself; %d screenshot(s) read" % len(s))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
