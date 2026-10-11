"""IRPT_BCKEND round 128 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one DIRECT-ACT order:
  IB128-1  IB-pr-430  the four closed v1 response schemas that omit `unprojected_grant` declare it, as the other 17 do
                      (CTO msg 4858; row D2-W287-S1).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB128-1-AC1  all 21 response schemas declare `unprojected_grant` with ONE identical declaration, list it as required,
               and stay closed (additionalProperties false). Base: FAIL (17 of 21 declare it).
  IB128-1-AC2  the `_contracts` suite fails on nothing new: its failing tests are a subset of the two that fail at base
               (both `analysis-request-original`), and at least 203 pass. Base: PASS (a bound; measured 2 failed, 203 passed).
  IB128-1-AC4  (a fourth, added by CTO msg 4865) the two thin producer fixtures hold the identities their handlers keep:
               every DirectoryPage entry carries the page's own 64-hex directory_revision, and the upload result's
               portfolio.source.upload_id equals its upload_id; the record names the handler path that made each.
               Base: FAIL (the entry's revision is 18 characters and differs; the portfolio is empty).
  IB128-1-AC3  the record shows, for each of the four routes: an envelope carrying the member validates, one without it
               is refused, and one with a foreign extra member is refused. Base: FAIL (no record).
"""
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~289/"
REC = D + "IB128-1_schema_member_record.json"
RESP = "docs/contracts/investor-reporting/v1/responses"
PKG = "infra/aws/lambda/investor-reporting"
FOUR = ("analysis-request-pdf", "comparison-catalogue", "custody-report-persist", "custody-report-read")
BASE_FAILING = ("test_every_declared_route_has_a_response_contract_whose_refs_resolve",
                "test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]")
BASE_PASSED = 203
MEMBER = "unprojected_grant"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB128"))
        sys.exit(1)

    if cid == "IB128-1-AC1":
        files = sorted(glob.glob(str(root / RESP / "*.response.schema.json")))
        if len(files) < 21:
            fail("%d response schemas found, at least 21 expected" % len(files))
        forms, lacking, not_required, open_ones = {}, [], [], []
        for p in files:
            s = json.loads(Path(p).read_text(encoding="utf-8"))
            name = os.path.basename(p).replace(".response.schema.json", "")
            decl = (s.get("properties") or {}).get(MEMBER)
            if decl is None:
                lacking.append(name)
                continue
            forms.setdefault(json.dumps(decl, sort_keys=True), []).append(name)
            if MEMBER not in (s.get("required") or []):
                not_required.append(name)
            if s.get("additionalProperties") is not False:
                open_ones.append(name)
        if lacking:
            fail("%d of %d do not declare %s: %s" % (len(lacking), len(files), MEMBER, lacking))
        if len(forms) != 1:
            fail("%d different declarations of %s: %s" % (len(forms), MEMBER, [v[:2] for v in forms.values()]))
        if not_required or open_ones:
            fail("not required in %s; not closed: %s" % (not_required, open_ones))
        print("OK: %d of %d response schemas declare %s, one identical declaration, required, closed" % (len(files), len(files), MEMBER))
    elif cid == "IB128-1-AC2":
        p = subprocess.run([sys.executable, "-m", "pytest", "_contracts", "-q", "-p", "no:cacheprovider", "-rf", "--color=no"],
                           cwd=str(root / PKG), capture_output=True, timeout=110)
        out = p.stdout.decode("utf-8", "replace")
        failed = re.findall(r"^FAILED \S+::(\S+)", out, re.MULTILINE)
        m = re.search(r"(\d+) passed", out)
        passed = int(m.group(1)) if m else 0
        new = [f for f in failed if f not in BASE_FAILING]
        if new:
            fail("%d test(s) fail that did not fail at base: %s" % (len(new), new[:4]))
        if passed < BASE_PASSED:
            fail("%d passed, %d at base" % (passed, BASE_PASSED))
        print("OK: _contracts suite: %d failed (all among the 2 base failures), %d passed (base %d)" % (len(failed), passed, BASE_PASSED))
    elif cid == "IB128-1-AC3":
        f = root / REC
        if not f.is_file():
            fail("no %s" % REC)
        a = json.loads(f.read_text(encoding="utf-8"))
        rows = {r.get("operation"): r for r in a.get("routes") or []}
        if sorted(rows) != sorted(FOUR):
            fail("routes recorded %r" % sorted(rows))
        for op, r in rows.items():
            if r.get("with_member_validates") is not True or r.get("without_member_refused") is not True \
                    or r.get("foreign_member_refused") is not True or not r.get("invocation"):
                fail("%s %r" % (op, {k: r.get(k) for k in ("with_member_validates", "without_member_refused", "foreign_member_refused")}))
        if not isinstance(a.get("files_changed"), list) or not a["files_changed"]:
            fail("files_changed is empty")
        if not isinstance(a.get("packaged_in_functions"), list):
            fail("packaged_in_functions is not stated")
        print("OK: 4 of 4 routes: with the member VALID, without it refused, a foreign member refused; %d files changed" % len(a["files_changed"]))
    elif cid == "IB128-1-AC4":
        fx = root / PKG / "_contracts" / "fixtures"
        page = json.loads((fx / "DirectoryPage.valid.json").read_text(encoding="utf-8")).get("instance") or {}
        rev = page.get("directory_revision")
        if not isinstance(rev, str) or not re.fullmatch(r"[0-9a-f]{64}", rev):
            fail("the page's directory_revision is not 64 hex")
        entries = page.get("entries") or []
        bad = [i for i, e in enumerate(entries) if ((e.get("revision") or {}).get("directory_revision")) != rev]
        if not entries or bad:
            fail("%d of %d entries do not carry the page's directory_revision" % (len(bad), len(entries)))
        up = json.loads((fx / "AnalysisUploadResult.valid.json").read_text(encoding="utf-8")).get("instance") or {}
        src = ((up.get("portfolio") or {}).get("source") or {})
        if not up.get("upload_id") or src.get("upload_id") != up.get("upload_id"):
            fail("portfolio.source.upload_id %r does not equal upload_id" % src.get("upload_id"))
        f2 = root / REC
        if not f2.is_file():
            fail("no %s" % REC)
        made = json.loads(f2.read_text(encoding="utf-8")).get("fixtures_made_by_handler") or []
        names = {m.get("fixture") for m in made if m.get("built_by") and m.get("invocation")}
        if not {"DirectoryPage.valid.json", "AnalysisUploadResult.valid.json"} <= names:
            fail("the record does not name the handler code path and invocation that made both fixtures: %r" % sorted(n for n in names if n))
        print("OK: %d of %d directory entries carry the page's 64-hex revision; the upload's portfolio source names its upload_id; both made by a named handler path" % (
            len(entries), len(entries)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
