"""IB31-1-AC2 -- (b) the ExportBundle takes exactly one of narrative_packet_ref or analysis_report_ref; every stored client-bundle
fixture validates unchanged; every reader of narrative_packet_ref handles an Analysis bundle or provably never receives one.

Grades, in order:
  1. export/tests/test_bundle_report_ref.py names analysis_report_ref, narrative_packet_ref, "both" and "neither"; at least 3 tests
     pass, 0 failed or errored (bounded at 110 s).
  2. The stored fixtures, read by THIS check with jsonschema Draft 2020-12 against the packaged
     infra/aws/lambda/investor-reporting/_contracts/ExportBundle.schema.json: ExportBundle.valid.json validates and
     ExportBundle.invalid.json does not.
  3. The reader census deliverables/0.9.0_WK_IRPT_BCKEND~101/NARRATIVE_REF_READERS_R31.json:
     {"files_scanned": n, "census_command": "...", "readers": [{"path", "how", "disposition": "handles"|"never-receives", "why"}]}
     files_scanned > 0; the four readers export/submit_service.py, export/narrative_submit.py, export/handler.py, export/bundle.py
     are each listed; every listed path exists; every disposition is one of the two words and every "why" is non-empty.
Usage: python <this file> <repo_root>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

B = "infra/aws/lambda/investor-reporting/"
TEST = B + "export/tests/test_bundle_report_ref.py"
SCHEMA = B + "_contracts/ExportBundle.schema.json"
FIX = B + "_contracts/fixtures/ExportBundle.%s.json"
REC = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~101/NARRATIVE_REF_READERS_R31.json"
READERS = [B + "export/submit_service.py", B + "export/narrative_submit.py", B + "export/handler.py", B + "export/bundle.py"]


def fail(msg):
    print("FAIL: " + msg)
    print("IB31-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8")
    for word in ("analysis_report_ref", "narrative_packet_ref", "both", "neither"):
        if word not in src:
            fail("the test file never names %r" % word)
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", TEST],
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("pytest exceeded 110 s")
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    passed = re.search(r"(\d+) passed", out)
    if bad:
        fail("pytest: %s" % bad.group(0))
    if not passed or int(passed.group(1)) < 3:
        fail("fewer than 3 tests passed: %s" % (passed.group(0) if passed else out.strip()[-200:]))

    import jsonschema
    schema = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
    v = jsonschema.Draft202012Validator(schema)
    # the stored fixtures are ENVELOPES ({_fixture, _source, _expect, instance}); the document graded is the `instance`
    # (row IRPT_BCKEND-W101-S10: the wrapper itself fails the schema at the base, so it was never the thing graded)
    good = json.loads((root / (FIX % "valid")).read_text(encoding="utf-8"))["instance"]
    badfx = json.loads((root / (FIX % "invalid")).read_text(encoding="utf-8"))["instance"]
    errs = list(v.iter_errors(good))
    if errs:
        fail("the stored valid client fixture no longer validates: %s" % errs[0].message[:160])
    if not list(v.iter_errors(badfx)):
        fail("the stored invalid fixture now validates")

    rp = root / REC
    if not rp.is_file():
        fail("no reader census at %s" % REC)
    rec = json.loads(rp.read_text(encoding="utf-8"))
    if int(rec.get("files_scanned") or 0) <= 0:
        fail("files_scanned is not positive")
    readers = rec.get("readers") or []
    listed = {str(x.get("path", "")).replace("\\", "/") for x in readers}
    missing = [p for p in READERS if p not in listed]
    if missing:
        fail("the census does not list %s" % missing)
    for x in readers:
        if not (root / str(x.get("path", ""))).is_file():
            fail("listed reader does not exist: %s" % x.get("path"))
        if x.get("disposition") not in ("handles", "never-receives"):
            fail("disposition %r for %s is not handles|never-receives" % (x.get("disposition"), x.get("path")))
        if not str(x.get("why") or "").strip():
            fail("no why for %s" % x.get("path"))
    print("OK: %s; client fixtures unchanged (valid validates, invalid refused); %d reader(s) of %d file(s) scanned" % (
        passed.group(0), len(readers), int(rec["files_scanned"])))
    print("IB31-1-AC2 PASS")


if __name__ == "__main__":
    main()
