"""IRPT_BCKEND round 65 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cells IB-pr-343..345 (PRD v0.30 items 33-36, W142-S4).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB65-1-AC1  export/tests/test_covered_account_ids.py passes (names covered_account_ids; an empty list is refused; derived at
              freeze), and the export suite has no failure beyond the six pypdf-only tests. Base: FAIL (no test).
  IB65-1-AC2  both ExportReceipt.schema.json copies require facts.covered_account_ids with minItems >= 1. Base: FAIL.
  IB65-2-AC1  export/tests/test_backfill_covered_account_ids.py passes, and the committed dry-run census IB65-2_backfill_census.json
              reads read = filled + unfillable with its sources named and wrote nothing. Base: FAIL.
  IB65-3-AC1  the committed exposure census IB65-3_exposure_census.json names its log groups and window, prints a count equal to the
              entries listed, and a non-zero count names a BLOCKING row present in the channel. Base: FAIL.
  IB65-G-<n>  A GUARD for slot ~<n>: that worker's own commits touch only its grant. Base: PASS.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "31b26bff2d"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
EXP = "infra/aws/lambda/investor-reporting/export"
CH = P + "/surprise-channel/investigations/INVESTIGATION_v1.md"
TO = P + "/task-orders/IRPT_BCKEND.TO-IB-pr-"
SCHEMAS = ("docs/contracts/investor-reporting/v1/ExportReceipt.schema.json",
           "infra/aws/lambda/investor-reporting/_contracts/ExportReceipt.schema.json")
PYPDF_ONLY = {
    "tests/test_export.py::test_the_content_hash_is_stable_and_the_validator_reads_a_real_pdf",
    "tests/test_export.py::test_the_validator_fails_a_non_pdf_rather_than_raising",
    "tests/test_export.py::test_the_forbidden_marker_census_is_measured_not_asserted",
    "tests/test_export_path_b.py::test_the_receipt_names_the_frozen_as_of",
    "tests/test_submit_async.py::test_the_marked_event_builds_and_the_handle_reaches_the_receipt",
    "tests/test_submit_service.py::test_submit_then_first_read_after_the_render_finalizes_the_receipt",
}
GRANTS = {
    "145": (EXP + "/entry.py", EXP + "/receipt.py", EXP + "/bundle.py", EXP + "/tests/test_covered_account_ids.py",
            EXP + "/backfill_covered_account_ids.py", EXP + "/tests/test_backfill_covered_account_ids.py") + SCHEMAS
           + (CH, TO + "343.", TO + "344.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~145/"),
    "146": (CH, TO + "345.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~146/"),
}


def _run(cmd, cwd, timeout=110):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def _export_suite(root):
    rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf", "tests/"], root / EXP)
    failed = {}
    for ln in out.splitlines():
        m = re.match(r"FAILED (\S+?)(?: - (.*))?$", ln.strip())
        if m:
            failed[m.group(1).replace("\\", "/")] = m.group(2) or ""
    extra = [k for k in failed if k not in PYPDF_ONLY or "pypdf" not in failed[k]]
    return _last(out), extra


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB65"))
        sys.exit(1)

    if cid == "IB65-1-AC1":
        t = root / EXP / "tests/test_covered_account_ids.py"
        if not t.is_file():
            fail("no export/tests/test_covered_account_ids.py")
        if "covered_account_ids" not in t.read_text(encoding="utf-8"):
            fail("the test never names covered_account_ids")
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_covered_account_ids.py"], root / EXP)
        last = _last(out)
        if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
            fail("new tests: %s" % last)
        last2, extra = _export_suite(root)
        if extra or re.search(r"\d+ error", last2):
            fail("export suite: %s; failures beyond the six pypdf-only tests: %s" % (last2, extra[:6]))
        print("OK: new %s; export suite %s" % (last, last2))
    elif cid == "IB65-1-AC2":
        for s in SCHEMAS:
            d = json.loads((root / s).read_text(encoding="utf-8"))
            facts = (d.get("properties") or {}).get("facts") or {}
            prop = (facts.get("properties") or {}).get("covered_account_ids") or {}
            if "covered_account_ids" not in (facts.get("required") or []) or (prop.get("minItems") or 0) < 1:
                fail("%s: facts.covered_account_ids is not required with minItems >= 1" % s)
        print("OK: both schema copies require a non-empty facts.covered_account_ids")
    elif cid == "IB65-2-AC1":
        t = root / EXP / "tests/test_backfill_covered_account_ids.py"
        if not t.is_file():
            fail("no export/tests/test_backfill_covered_account_ids.py")
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_backfill_covered_account_ids.py"], root / EXP)
        last = _last(out)
        if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
            fail("backfill tests: %s" % last)
        f = root / P / "deliverables/0.9.0_WK_IRPT_BCKEND~145/IB65-2_backfill_census.json"
        if not f.is_file():
            fail("no IB65-2_backfill_census.json")
        d = json.loads(f.read_text(encoding="utf-8"))
        if not all(isinstance(d.get(k), int) for k in ("read", "filled", "unfillable")) or d["read"] != d["filled"] + d["unfillable"]:
            fail("read/filled/unfillable do not reconcile: %r" % {k: d.get(k) for k in ("read", "filled", "unfillable")})
        if not d.get("sources") or d.get("wrote") not in (0, False):
            fail("sources missing or the dry run wrote something (wrote=%r)" % d.get("wrote"))
        print("OK: %s; read %d = filled %d + unfillable %d, wrote nothing" % (last, d["read"], d["filled"], d["unfillable"]))
    elif cid == "IB65-3-AC1":
        f = root / P / "deliverables/0.9.0_WK_IRPT_BCKEND~146/IB65-3_exposure_census.json"
        if not f.is_file():
            fail("no IB65-3_exposure_census.json")
        d = json.loads(f.read_text(encoding="utf-8"))
        if not d.get("log_groups") or not d.get("window"):
            fail("log_groups or window missing")
        entries = d.get("cross_scope_reads") or []
        if not isinstance(d.get("count"), int) or d["count"] != len(entries):
            fail("count %r != entries listed %d" % (d.get("count"), len(entries)))
        if d["count"] > 0:
            row = d.get("blocking_row") or ""
            if not row or ('"id": "%s"' % row) not in (root / CH).read_text(encoding="utf-8"):
                fail("non-zero exposure with no BLOCKING row present in the channel (blocking_row=%r)" % row)
        print("OK: %d cross-scope export read(s) over %s across %d log group(s)" % (d["count"], d["window"], len(d["log_groups"])))
    elif cid.startswith("IB65-G-"):
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
