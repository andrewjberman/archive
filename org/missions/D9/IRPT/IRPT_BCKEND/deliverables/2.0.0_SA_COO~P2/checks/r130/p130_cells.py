"""IRPT_BCKEND round 130 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order:
  IB130-1  IB-pr-432  the published sections response (operation analysis-report) admits the Opal-made report form that the
                      handler already answers (rows IRPT_YCDGEN-W2-S13, IRPT_YCDGEN-W6-S4; CTO msg 4923; PRD ADDENDUM v0.28 item 29).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB130-1-AC1  four arms on the response schema's `data` member, validated here with every schema file of the two contract
               folders in one registry:  (a) an Opal-form answer validates [base: FAIL]; (b) the vendor-form answer still
               validates [control: PASS at base]; (c) an Opal-form answer that also carries extraction_validation is refused;
               (d) an answer naming provider OPAL_ENGINE without computation_validation is refused. Base: FAIL on (a).
  IB130-1-AC2  the `_contracts` suite fails on nothing new (failing tests are a subset of the two base failures) and at least
               203 pass. Base: PASS (a bound).
  IB130-1-AC3  the record shows the HANDLER's own Opal-form sections answer (ops/owned_report.py, made by its code path) and its
               vendor-form answer both validating against the changed schema, with the invocation. Base: FAIL (no record).
"""
import copy
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~290/"
REC = D + "IB130-1_sections_response_record.json"
V1 = "docs/contracts/investor-reporting/v1"
PKG = "infra/aws/lambda/investor-reporting"
RESP = V1 + "/responses/analysis-report.response.schema.json"
FX = PKG + "/_contracts/fixtures/"
BASE_FAILING = ("test_every_declared_route_has_a_response_contract_whose_refs_resolve",
                "test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]")
BASE_PASSED = 203
OPAL_KEYS = ("provider", "request_ref", "sections", "computation_validation")
RECEIPT = {"artifact_id": "synthetic"}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB130"))
        sys.exit(1)

    if cid == "IB130-1-AC1":
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        resources = []
        files = glob.glob(str(root / V1 / "*.json")) + glob.glob(str(root / V1 / "responses" / "*.json")) \
            + glob.glob(str(root / PKG / "_contracts" / "*.schema.json"))
        for p in files:
            try:
                doc = json.loads(Path(p).read_text(encoding="utf-8"))
            except ValueError:
                continue
            if isinstance(doc, dict) and doc.get("$id"):
                resources.append((doc["$id"], Resource.from_contents(doc)))
        registry = Registry().with_resources(resources)
        schema = json.loads((root / RESP).read_text(encoding="utf-8"))
        validator = Draft202012Validator({"$ref": schema["$id"] + "#/properties/data"}, registry=registry)

        def inst(name):
            doc = json.loads((root / FX / name).read_text(encoding="utf-8"))
            return doc.get("instance", doc)

        opal_doc, vendor_doc = inst("AnalysisReport.v2.opal.valid.json"), inst("AnalysisReport.valid.json")
        receipt = opal_doc.get("retained_ref") or vendor_doc.get("retained_ref")
        opal = {k: copy.deepcopy(opal_doc[k]) for k in OPAL_KEYS}
        vendor = {k: copy.deepcopy(vendor_doc[k]) for k in ("request_ref", "sections", "extraction_validation")}
        if receipt is not None:
            opal["retained_ref"] = copy.deepcopy(receipt)
        mixed = dict(opal, extraction_validation=vendor["extraction_validation"])
        bare = {k: v for k, v in opal.items() if k != "computation_validation"}

        def ok(doc):
            try:
                return not list(validator.iter_errors(doc))
            except Exception as exc:  # an unresolvable reference is a failed arm, named
                print("  (validation raised %s: %s)" % (type(exc).__name__, str(exc)[:120]))
                return None

        arms = (("a Opal-form answer validates", ok(opal), True), ("b vendor-form answer validates", ok(vendor), True),
                ("c Opal form with extraction_validation refused", ok(mixed), False),
                ("d provider OPAL_ENGINE without computation_validation refused", ok(bare), False))
        bad = [n for n, got, want in arms if got is not want]
        for n, got, want in arms:
            print("  arm %s: %s" % (n, "as expected" if got is want else "NOT as expected (validates=%r)" % got))
        if bad:
            fail("%d of 4 arms not as expected: %s (%d schema files in the registry; receipt on the fixture: %s)" % (
                len(bad), [b[:1] for b in bad], len(resources), receipt is not None))
        print("OK: 4 of 4 arms as expected over %d schema files" % len(resources))
    elif cid == "IB130-1-AC2":
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
    elif cid == "IB130-1-AC3":
        f = root / REC
        if not f.is_file():
            fail("no %s" % REC)
        a = json.loads(f.read_text(encoding="utf-8"))
        rows = {r.get("form"): r for r in a.get("handler_answers") or []}
        for form in ("OPAL_ENGINE", "YCHARTS"):
            r = rows.get(form) or {}
            if r.get("validates") is not True or not r.get("built_by") or not r.get("invocation"):
                fail("handler answer %s: validates=%r, built_by or invocation missing" % (form, r.get("validates")))
        if not isinstance(a.get("files_changed"), list) or not a["files_changed"]:
            fail("files_changed is empty")
        if not isinstance(a.get("readers_named"), list) or not isinstance(a.get("packaged_in_functions"), list):
            fail("readers_named and packaged_in_functions are not stated")
        print("OK: the handler's Opal-form and vendor-form answers both validate; %d files changed" % len(a["files_changed"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
