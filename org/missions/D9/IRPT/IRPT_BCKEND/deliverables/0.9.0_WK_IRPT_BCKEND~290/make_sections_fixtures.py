"""IB-pr-432: make the three sections producer fixtures BY THE HANDLER'S OWN CODE PATH.

Run from infra/aws/lambda/investor-reporting/:
  python -m pytest <this file> -q -p no:cacheprovider -s
Drives ops/owned_report.py OwnedAnalysisReader.sections over the existing offline fakes (ops/tests/test_owned_report.py
report_world) and writes the handler's answer into the wrapper form of the _contracts/fixtures folder. Nothing is
hand-written: the vendor answer is the existing synthetic vendor report, the Opal answer is the existing
AnalysisReport.v2.opal.valid.json document published through the same reader; the invalid fixture is the Opal answer
with `extraction_validation` added (the one deliberate edit, stated in `_fixture`).
Also validates each answer against the changed response schema's `data` member (the record's handler_answers).
"""
import copy
import json
import os
import sys
from pathlib import Path

PKG = Path(os.getcwd()).resolve()          # run from infra/aws/lambda/investor-reporting/
assert PKG.name == "investor-reporting", PKG
REPO = PKG.parents[3]
for p in (PKG / "ops/tests", PKG / "ops", PKG / "intake/tests", PKG / "ycharts/generate"):
    sys.path.insert(0, str(p))

import jsonschema  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

import test_owned_report as support  # noqa: E402
from test_owned_report import report_world  # noqa: E402,F401  (fixture)
from test_owned_requests import retention_world, world  # noqa: E402,F401  (fixtures)

OUT = PKG / "_contracts/fixtures"
V1 = REPO / "docs/contracts/investor-reporting/v1"
RESP = V1 / "responses/analysis-report.response.schema.json"
HERE = Path(__file__).resolve().parent


def _registry():
    resources = []
    for base in (V1, PKG / "_contracts"):
        for f in sorted(base.glob("*.schema.json")):
            doc = json.loads(f.read_text(encoding="utf-8"))
            if "$id" in doc:
                resources.append((doc["$id"], Resource(contents=doc, specification=DRAFT202012)))
    return Registry().with_resources(resources)


def _wrap(kind, instance, expect, source):
    return {"_fixture": kind, "_source": source, "_expect": expect, "instance": instance}


def _data_validator():
    data = json.loads(RESP.read_text(encoding="utf-8"))["properties"]["data"]
    return jsonschema.Draft202012Validator(data, registry=_registry())


def test_make_fixtures(report_world):  # noqa: F811
    r = report_world
    v = _data_validator()
    answers = []

    vendor = r.reader.sections(r.w.case.principal, r.id)
    v.validate(vendor)
    answers.append({"form": "YCHARTS", "built_by": "infra/aws/lambda/investor-reporting/ops/owned_report.py:OwnedAnalysisReader.sections",
                    "answer_members": sorted(vendor), "validates": True})

    document = support._opal_document(r.report["request_ref"])
    support._publish(r, document)
    opal = r.reader.sections(r.w.case.principal, r.id)
    assert opal["provider"] == "OPAL_ENGINE" and "extraction_validation" not in opal
    v.validate(opal)
    answers.append({"form": "OPAL_ENGINE", "built_by": "infra/aws/lambda/investor-reporting/ops/owned_report.py:OwnedAnalysisReader.sections",
                    "answer_members": sorted(opal), "validates": True})

    bad = copy.deepcopy(opal)
    bad["extraction_validation"] = copy.deepcopy(vendor["extraction_validation"])
    refused = False
    try:
        v.validate(bad)
    except jsonschema.ValidationError:
        refused = True
    assert refused
    answers.append({"form": "OPAL_ENGINE+extraction_validation", "built_by": "the OPAL_ENGINE answer plus the vendor extraction_validation member",
                    "answer_members": sorted(bad), "validates": False})

    src = ("ops/owned_report.py OwnedAnalysisReader.sections (the handler irpt-status serves for operation analysis-report), "
           "driven by %s")
    vendor_src = src % "the offline report_world fixture of ops/tests/test_owned_report.py over the synthetic vendor report"
    opal_src = src % ("the same fakes with ops/tests/test_owned_report.py _publish of AnalysisReport.v2.opal.valid.json "
                      "(_opal_document)")
    files = {
        "analysis-report.sections.vendor.valid.json": _wrap(
            "VALID instance of the analysis-report `data` member, VENDOR form (no provider)", vendor,
            "jsonschema Draft202012 accepts this document", vendor_src),
        "analysis-report.sections.opal.valid.json": _wrap(
            "VALID instance of the analysis-report `data` member, OPAL_ENGINE form", opal,
            "jsonschema Draft202012 accepts this document", opal_src),
        "analysis-report.sections.opal.invalid.json": _wrap(
            "INVALID instance of the analysis-report `data` member: the OPAL_ENGINE answer plus the vendor member "
            "`extraction_validation` (the one added member; the vendor value is the vendor answer's own)", bad,
            "jsonschema Draft202012 REFUSES this document: the Opal form is closed and carries no extraction_validation",
            opal_src),
    }
    for name, wrapper in files.items():
        (OUT / name).write_text(json.dumps(wrapper, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (HERE / "handler_answers.json").write_text(json.dumps(answers, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("firm_id of the fakes:", r.w.case.principal["firm_id"])
