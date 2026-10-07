"""IRPT_BCKEND round 62 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cells IB-pr-336..339.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB62-1-AC1  render host: tests/test_template_kind.cjs passes (it names performance-landscape-letter,
              analysis-portrait-letter and an unknown name that is refused), and tests/test_print_query.cjs still passes.
              Base: FAIL (no test).
  IB62-2-AC1  release-census.py irpt-directory-refresh --pin HEAD prints changed_members=1 and the one member is refresh.py.
              Base: FAIL (2: handler.py rides).
  IB62-3-AC1  the committed census IB62-3_reader_census.json: reader_count > 0 equal to readers listed; at least one reader under
              an IRPT_CUSTDY path; every reader records plain and over_age as PASS or FAIL with the test that ran it.
              Base: FAIL (no census).
  IB62-4-AC1  _ids: the seam file's index holds 0 'None' values, and the new test naming 'None' plus the _ids suite pass.
              Base: FAIL (826 'None').
  IB62-1-AC2  E-P9 submit: export/tests/test_submit_client_report.py passes (names client-report) and the export suite has no
              failure beyond the six pypdf-only tests (amendment 1, row W138-S1).
              Base: FAIL (no test).
  IB62-1-AC3  E-P9 package: render_manifest/manifest.ts lists a 'client-report' kind with a schemaVersion entry, and the portal
              render package (portal/src/pages/InvestorReporting/render/) names 'client-report'. Base: FAIL.
  IB62-4-AC2  E-P8 writer: deliverables/~141/seam_writer.txt has a line "WRITER: <repo path that exists>" or
              "NOT IN REPO: <row id present in the channel>". Base: FAIL.
  IB62-5-AC1  E-P10: IB62-5_gated_fixtures.json: route_count > 0 = routes listed; every gated route has an allowed and a denied
              fixture file that exists; battery_overall_pass true. Base: FAIL.
  IB62-G-<n>  A GUARD for slot ~<n>: that worker's own commits touch only its order's grant. Base: PASS.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "bc794d2770"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
EX = "infra/aws/ec2/investor-reporting-export"
CI = "infra/aws/lambda/ci"
IDS = "infra/aws/lambda/investor-reporting/_ids"
CH = P + "/surprise-channel/investigations/INVESTIGATION_v1.md"
TO = P + "/task-orders/IRPT_BCKEND.TO-IB-pr-"
GRANTS = {
    "138": (EX + "/render_export.cjs", EX + "/tests/test_template_kind.cjs", "infra/aws/lambda/investor-reporting/export/",
            "portal", "docs/contracts/investor-reporting/v1/ExportBundle.schema.json",
            "infra/aws/lambda/investor-reporting/_contracts/ExportBundle.schema.json",
            "infra/aws/lambda/investor-reporting/reports/repository.py", "infra/aws/lambda/investor-reporting/reports/tests/",
            CH, TO + "336.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~138/"),
    "139": (CI + "/lambda-source-map.json", CH, TO + "337.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~139/"),
    "140": ("portal", "data/assets/scripts/gold/irpt_custody/tests/test_directory_search_overage_reader.py",
            "infra/aws/lambda/investor-reporting/directory/tests/test_search_readers_overage.py", CH, TO + "338.",
            P + "/deliverables/0.9.0_WK_IRPT_BCKEND~140/"),
    "141": (IDS + "/", CH, TO + "339.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~141/"),
    "142": ("infra/aws/lambda/investor-reporting/intake/uploads.py",
            "infra/aws/lambda/investor-reporting/intake/tests/test_uploads_refusal_class.py",
            CH, TO + "340.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~142/"),
}


def _run(cmd, root, timeout=110):
    r = subprocess.run(cmd, cwd=str(root), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB62"))
        sys.exit(1)

    if cid == "IB62-1-AC1":
        t = root / EX / "tests/test_template_kind.cjs"
        if not t.is_file():
            fail("no %s/tests/test_template_kind.cjs" % EX)
        src = t.read_text(encoding="utf-8")
        for w in ("performance-landscape-letter", "analysis-portrait-letter", "custody-report"):
            if w not in src:
                fail("test never names %r" % w)
        rc, out = _run(["node", str(t)], root)
        if rc:
            fail("test_template_kind: %s" % _last(out))
        rc2, out2 = _run(["node", str(root / EX / "tests/test_print_query.cjs")], root)
        if rc2:
            fail("test_print_query regressed: %s" % _last(out2))
        print("OK: test_template_kind and test_print_query pass")
    elif cid == "IB62-2-AC1":
        head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(root), capture_output=True, text=True).stdout.strip()
        rc, out = _run([sys.executable, str(root / CI / "release-census.py"), "irpt-directory-refresh", "--pin", head], root)
        m = re.search(r"changed_members=(\d+)", out)
        if rc or not m:
            fail("census rc %d: %s" % (rc, _last(out)))
        changed = re.findall(r"^(?:changed|added|removed) (\S+)", out, re.M)
        if int(m.group(1)) != 1 or changed != ["refresh.py"]:
            fail("changed_members=%s members=%s (expected exactly refresh.py)" % (m.group(1), changed))
        print("OK: changed_members=1 (refresh.py)")
    elif cid == "IB62-3-AC1":
        f = root / P / "deliverables/0.9.0_WK_IRPT_BCKEND~140/IB62-3_reader_census.json"
        if not f.is_file():
            fail("no census %s" % f.name)
        d = json.loads(f.read_text(encoding="utf-8"))
        readers = d.get("readers") or []
        if not readers or d.get("reader_count") != len(readers):
            fail("reader_count %r vs %d listed" % (d.get("reader_count"), len(readers)))
        if not any("irpt_custody" in (r.get("path") or "").lower() or "irpt_custdy" in (r.get("path") or "").lower() for r in readers):
            fail("no IRPT_CUSTDY reader in the census")
        for r in readers:
            for arm in ("plain", "over_age"):
                a = r.get(arm)
                if not isinstance(a, dict) or a.get("result") not in ("PASS", "FAIL") or not a.get("test"):
                    fail("reader %s arm %s: %r" % (r.get("path"), arm, a))
        fails = [r.get("path") for r in readers if r["plain"]["result"] == "FAIL" or r["over_age"]["result"] == "FAIL"]
        print("OK: %d readers, every arm recorded; %d with a FAIL (release holds on any): %s" % (len(readers), len(fails), fails[:6]))
    elif cid == "IB62-4-AC1":
        seam = json.loads((root / IDS / "data/custodian_key_seam.json").read_text(encoding="utf-8"))
        idx = seam.get("index") or {}
        nones = sum(1 for v in idx.values() if v == "None")
        if nones:
            fail("seam index still holds %d 'None' values" % nones)
        tests = list((root / IDS / "tests").glob("test_*.py"))
        if not any("'None'" in t.read_text(encoding="utf-8") or '"None"' in t.read_text(encoding="utf-8") for t in tests):
            fail("no _ids test names the string 'None'")
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/"], root / IDS)
        last = _last(out)
        if rc or re.search(r"\d+ (failed|error)", last) or "passed" not in last:
            fail("_ids suite: %s" % last)
        print("OK: 0 'None' of %d index values; _ids %s" % (len(idx), last))
    elif cid == "IB62-1-AC2":
        t = root / "infra/aws/lambda/investor-reporting/export/tests/test_submit_custody_report.py"
        if not t.is_file():
            fail("no export/tests/test_submit_custody_report.py (amendment 2: custody naming, PRD v0.29)")
        if "custody_report_ref" not in t.read_text(encoding="utf-8") or "CUSTODY_REPORT" not in t.read_text(encoding="utf-8"):
            fail("test never names custody_report_ref and CUSTODY_REPORT")
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_submit_custody_report.py"],
                       root / "infra/aws/lambda/investor-reporting/export")
        last = _last(out)
        if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
            fail("new tests: %s" % last)
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf", "tests/"],
                       root / "infra/aws/lambda/investor-reporting/export")
        last2 = _last(out)
        # Amendment 1 (issuer, row W138-S1): these six fail at the base too, only because pypdf is not on this box
        # (no egress to fetch it). Any OTHER failure, or one of these failing for another reason, still fails AC2.
        pypdf_only = {
            "tests/test_export.py::test_the_content_hash_is_stable_and_the_validator_reads_a_real_pdf",
            "tests/test_export.py::test_the_validator_fails_a_non_pdf_rather_than_raising",
            "tests/test_export.py::test_the_forbidden_marker_census_is_measured_not_asserted",
            "tests/test_export_path_b.py::test_the_receipt_names_the_frozen_as_of",
            "tests/test_submit_async.py::test_the_marked_event_builds_and_the_handle_reaches_the_receipt",
            "tests/test_submit_service.py::test_submit_then_first_read_after_the_render_finalizes_the_receipt",
        }
        failed = {}
        for ln in out.splitlines():
            m = re.match(r"FAILED (\S+?)(?: - (.*))?$", ln.strip())
            if m:
                failed[m.group(1).replace("\\", "/")] = m.group(2) or ""
        extra = [k for k in failed if k not in pypdf_only or "pypdf" not in failed[k]]
        if re.search(r"\d+ error", last2) or extra:
            fail("export suite: %s; failures outside the six pypdf-only tests: %s" % (last2, extra[:6]))
        print("OK: new %s; export suite %s (%d pypdf-only failures admitted by amendment 1)" % (last, last2, len(failed)))
    elif cid == "IB62-1-AC3":
        m = (root / "infra/aws/lambda/investor-reporting/export/render_manifest/manifest.ts").read_text(encoding="utf-8")
        if "'custody-report'" not in m and '"custody-report"' not in m:
            fail("render_manifest/manifest.ts has no 'custody-report' kind")
        if not re.search(r"custody-report[\s\S]{0,800}schemaVersion|schemaVersion[\s\S]{0,800}custody-report", m):
            fail("no schemaVersion entry beside the custody-report kind")
        pr = root / "portal/src/pages/InvestorReporting/render"
        hits = [f.name for f in pr.glob("*.ts*") if "custody-report" in f.read_text(encoding="utf-8", errors="replace")] if pr.is_dir() else []
        if not hits:
            fail("the portal render package names no 'custody-report' (portal/src/pages/InvestorReporting/render/)")
        for c in ("docs/contracts/investor-reporting/v1/ExportBundle.schema.json",
                  "infra/aws/lambda/investor-reporting/_contracts/ExportBundle.schema.json"):
            if "custody_report_ref" not in (root / c).read_text(encoding="utf-8"):
                fail("%s has no custody_report_ref (amendment 2)" % c)
        if "CUSTODY_REPORT" not in (root / "infra/aws/lambda/investor-reporting/reports/repository.py").read_text(encoding="utf-8"):
            fail("reports/repository.py KINDS has no CUSTODY_REPORT (amendment 2)")
        print("OK: manifest kind + schemaVersion; portal render files: %s" % hits)
    elif cid == "IB62-4-AC2":
        f = root / P / "deliverables/0.9.0_WK_IRPT_BCKEND~141/seam_writer.txt"
        if not f.is_file():
            fail("no seam_writer.txt")
        t = f.read_text(encoding="utf-8")
        mw = re.search(r"^WRITER: (\S+)", t, re.M)
        mn = re.search(r"^NOT IN REPO: (IRPT_BCKEND-\S+)", t, re.M)
        if mw and (root / mw.group(1)).exists():
            print("OK: writer %s" % mw.group(1))
        elif mn and ('"id": "%s"' % mn.group(1)) in (root / CH).read_text(encoding="utf-8"):
            print("OK: not in repo, row %s" % mn.group(1))
        else:
            fail("seam_writer.txt names no existing writer path and no row present in the channel")
    elif cid == "IB62-5-AC1":
        f = root / P / "deliverables/0.9.0_WK_IRPT_BCKEND~142/IB62-5_gated_fixtures.json"
        if not f.is_file():
            fail("no IB62-5_gated_fixtures.json")
        d = json.loads(f.read_text(encoding="utf-8"))
        routes = d.get("routes") or []
        if not routes or d.get("route_count") != len(routes):
            fail("route_count %r vs %d listed" % (d.get("route_count"), len(routes)))
        for r in routes:
            if r.get("gated"):
                for k in ("allowed_fixture", "denied_fixture"):
                    if not r.get(k) or not (root / r[k]).is_file():
                        fail("route %s: %s missing" % (r.get("route"), k))
        if d.get("battery_overall_pass") is not True:
            fail("battery_overall_pass %r" % d.get("battery_overall_pass"))
        print("OK: %d routes, %d gated with both fixtures, battery green" % (len(routes), sum(1 for r in routes if r.get("gated"))))
    elif cid.startswith("IB62-G-"):
        slot = cid.rsplit("-", 1)[1]
        grant = GRANTS.get(slot)
        if not grant:
            fail("unknown slot %r" % slot)
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~%s" % slot, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(grant)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~%s's grant" % (len(changed), slot))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
