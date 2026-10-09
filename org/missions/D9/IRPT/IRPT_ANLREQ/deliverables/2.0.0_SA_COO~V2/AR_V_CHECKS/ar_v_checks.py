"""IRPT_ANLREQ round 1, workstream ~V2 (the ticket) -- the issuer's mechanical checks (2.0.0_SA_COO~V2).

  v11-form     AR11-v-AC1  portal: the form offers catalogue checkboxes + an other-ETF field and files I1 (upload, ticket, POST
                           /analysis with ticket_id) with no "Request report" click            [--portal <dir>]
  v12-packager AR12-v-AC1  ticket_center: package_principal is NAMED and firm-bound by its PROFILE row LIST (fail closed)
  v13-open     AR13-v-AC1  portal: the ticket page lists the package files and opens each through I6           [--portal <dir>]
  v21-package  AR21-v-AC1  ticket_center (round 2): the package route admits I5' (original_ref null) and reads pdf_ref and
                           commentary_ref as I7 canonical JSON
  v21-page     AR21-v-AC2  portal (round 2): the PDF opens through analysis-request-pdf; the I5' sentence; I7 refs shown, never
                           linked by guess                                                                       [--portal <dir>]
  regress      AR-v-AC2    the whole ticket_center tests directory passes (>= 131 passed, 0 failed)
  portal-tsc   AR-v-AC3    `bun x tsc -b` in the portal worktree exits 0                                          [--portal <dir>]

Each named test must EXIST and PASS; a missing name is a FAIL. Prints <TOKEN>-OK or <TOKEN>-FAIL <reason>; exit 0/1.
Run from the workspace worktree root.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

PY_TESTS = {
    "v12-packager": (Path("infra/aws/lambda/ticket_center/tests/test_package_principal.py"),
                     ["test_package_principal_named_in_type_definition", "test_packager_admitted_for_firm_in_its_profile_list",
                      "test_packager_refused_for_firm_outside_its_list", "test_packager_refused_without_profile_list",
                      "test_packager_non_list_scope_refused", "test_other_principals_still_refused"]),
    "v21-package": (Path("infra/aws/lambda/ticket_center/tests/test_package_i5p_i7.py"),
                    ["test_package_admits_null_original_ref", "test_package_still_requires_report_pdf_commentary",
                     "test_package_admits_i7_canonical_refs", "test_package_refuses_non_canonical_i7_ref",
                     "test_package_refuses_i7_ref_with_extra_or_missing_field"]),
}
BUN_TESTS = {
    "v11-form": (Path("src/pages/TicketCenter/__tests__/analysis-form-i1.test.tsx"),
                 ["offers the Opal model checkboxes from the catalogue", "takes other ETFs as typed keys",
                  "files upload then ticket then analysis with ticket_id", "never shows a Request report button on a new filing",
                  "sends at most five comparison keys", "retries the analysis step without refiling",
                  "the client admits ticket_id only beside input_id"]),
    "v13-open": (Path("src/pages/TicketCenter/__tests__/package-open.test.tsx"),
                 ["lists the four package files on the ticket", "opens the report and the PDF through the owned reader",
                  "names a file with no reader instead of linking it", "makes no call for a ticket without a package"]),
    "v21-page": (Path("src/pages/TicketCenter/__tests__/package-r2.test.tsx"),
                 ["the real client opens the branded PDF through analysis-request-pdf",
                  "shows the custody sentence when original_ref is null", "shows an I7 ref by its artifact id",
                  "shows an unparseable ref as text and never links it",
                  "the real client opens the original file through analysis-request-original"]),
}
STRIP = re.compile(r"\x1b\[[0-9;]*m")


def _pytest(path, names):
    if not path.exists():
        return False, "absent: %s" % path.as_posix()
    src = path.read_text(encoding="utf-8")
    missing = [n for n in names if not re.search(r"^\s*def %s\(" % re.escape(n), src, re.M)]
    if missing:
        return False, "missing test(s): %s" % ", ".join(missing)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", path.as_posix(), "-k",
                        " or ".join(names)], capture_output=True, text=True, timeout=170)
    out = STRIP.sub("", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    if r.returncode != 0 or passed < len(names):
        return False, "rc=%d passed=%d of %d" % (r.returncode, passed, len(names))
    return True, "passed=%d" % passed


def _bun(portal, path, names):
    test = Path(portal) / path
    if not test.exists():
        return False, "absent: %s" % test.as_posix()
    src = test.read_text(encoding="utf-8")
    missing = [n for n in names if ("'%s'" % n) not in src and ('"%s"' % n) not in src]
    if missing:
        return False, "missing test(s): %s" % ", ".join(missing)
    bun = shutil.which("bun")
    if not bun:
        return False, "bun not on PATH"
    r = subprocess.run([bun, "test", path.as_posix()], cwd=str(portal), capture_output=True, text=True, timeout=170)
    out = STRIP.sub("", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) pass", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) fail", out) or [0, 0])[1])
    if r.returncode != 0 or failed or passed < len(names):
        return False, "rc=%d pass=%d fail=%d of %d" % (r.returncode, passed, failed, len(names))
    return True, "pass=%d" % passed


def _regress():
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "infra/aws/lambda/ticket_center/tests"],
                       capture_output=True, text=True, timeout=170)
    out = STRIP.sub("", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) failed", out) or [0, 0])[1])
    if r.returncode != 0 or failed or passed < 131:
        return False, "rc=%d passed=%d failed=%d (floor 131)" % (r.returncode, passed, failed)
    return True, "passed=%d failed=0" % passed


def _tsc(portal):
    bun = shutil.which("bun")
    if not bun:
        return False, "bun not on PATH"
    r = subprocess.run([bun, "x", "tsc", "-b"], cwd=str(portal), capture_output=True, text=True, timeout=170)
    return r.returncode == 0, "rc=%d" % r.returncode


def main(argv):
    if not argv:
        print("usage: ar_v_checks.py {v11-form|v12-packager|v13-open|v21-package|v21-page|regress|portal-tsc} [--portal <dir>]")
        return 2
    sub = argv[0]
    portal = argv[argv.index("--portal") + 1] if "--portal" in argv else None
    if sub in PY_TESTS:
        ok, why = _pytest(*PY_TESTS[sub])
    elif sub in BUN_TESTS or sub == "portal-tsc":
        if not portal:
            print("%s-FAIL --portal <dir> required" % sub.upper())
            return 1
        ok, why = _tsc(portal) if sub == "portal-tsc" else _bun(portal, *BUN_TESTS[sub])
    elif sub == "regress":
        ok, why = _regress()
    else:
        print("unknown subcommand %s" % sub)
        return 2
    print("%s-%s %s" % (sub.upper(), "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
