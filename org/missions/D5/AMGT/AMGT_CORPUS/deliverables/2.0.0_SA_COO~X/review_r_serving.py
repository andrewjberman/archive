"""Independent routine review of R's exact no-span serving repair; offline."""
from pathlib import Path
from contextlib import ExitStack
import ast
import copy
import hashlib
import importlib
import json
import socket
import subprocess
import sys
from unittest.mock import patch
import zipfile

TARGET = Path("C:/tmp/coo-x-review-r-dd91fd3126")
PIN = "dd91fd3126318f1056b0e5f426e855d84ee0d424"
MODULE = "lib/research/api/scoped_amgt.py"
for name in [MODULE, "lib/research/api/tests/test_drafted_sections.py"]:
    expected = subprocess.check_output(["git", "-C", str(TARGET), "show", PIN + ":" + name], encoding="utf-8")
    assert (TARGET / name).read_text(encoding="utf-8") == expected, "unpinned source " + name
package = Path("C:/tmp/amgt-r-no-span-package-20260923/candidate.zip")
package_sha = hashlib.sha256(package.read_bytes()).hexdigest()
assert package_sha == "0c44108821fe52850c77b119490039453b082c3639fae6dbf58de054b1397a55"
with zipfile.ZipFile(package) as candidate, zipfile.ZipFile(package.with_name("rollback.zip")) as baseline:
    assert len(candidate.namelist()) == len(set(candidate.namelist())) == 197
    assert candidate.namelist() == baseline.namelist()
    changed = [name for name in candidate.namelist() if candidate.read(name) != baseline.read(name)]
    assert changed == [MODULE]
    before, after = ast.parse(baseline.read(MODULE)), ast.parse(candidate.read(MODULE))
    assert hashlib.sha256(candidate.read(MODULE)).hexdigest() == "6c98b25ba5cf51558d3c28db1f9e0fecf5acef1aefeb5c3b3cdc896fefb29a38"
    names = {"_drafting_block", "read_drafted_sections"}
    local = ast.parse((TARGET / MODULE).read_text(encoding="utf-8"))
    local_functions = {n.name: n for n in local.body if isinstance(n, ast.FunctionDef)}
    for node in after.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            assert ast.dump(node) == ast.dump(local_functions[node.name])
    for tree in [before, after]:
        tree.body = [n for n in tree.body if not isinstance(n, ast.FunctionDef) or n.name not in names]
    assert ast.dump(before) == ast.dump(after)

sys.path.insert(0, str(TARGET))
api = importlib.import_module("lib.research.api.scoped_amgt")
fixtures = importlib.import_module("lib.research.api.tests.test_drafted_sections")
boto3 = importlib.import_module("boto3")
checks = []


def refuse(*args, **kwargs):
    raise AssertionError("offline external access refused")


def read(document, description=False):
    original = copy.deepcopy(document)
    with patch.object(api, "_read_drafting_document", return_value=(document, api.DRAFTING_SOURCE_LOCAL, None, True)):
        if description:
            result = api.read_description("CTRL_US_Equity", identity={"security_key": "CTRL_US_Equity"}, model_block={"figures": []})
        else:
            result = api.read_drafted_sections("CTRL_US_Equity")
    assert document == original, "reader mutated input"
    return result


with ExitStack() as stack:
    for target, attr in [(boto3, "client"), (boto3, "resource"), (socket, "socket"),
                         (subprocess, "run"), (subprocess, "Popen")]:
        stack.enter_context(patch.object(target, attr, side_effect=refuse))
    try:
        boto3.client("s3")
    except AssertionError:
        checks.append("external-access poison positive control fired")
    else:
        raise AssertionError("vacuous poison")
    doc = fixtures._document()
    doc["sections"][0]["sentences"][0]["quoted_spans"] = ["\u00a0\r\n\t"]
    # Unicode whitespace might fail existing verbatim normalization first; it
    # must never produce served company prose on either path.
    result = read(doc)
    assert not any(sec["section_id"] == "company_description" and sec["sentences"] for sec in result["drafted_sections"])
    assert read(doc, True)["text"] is None
    checks.append("Unicode whitespace-only span cannot supply description prose")
    doc = fixtures._document()
    doc["sections"][0]["sentences"][0]["quoted_spans"].append("")
    assert read(doc, True)["text"] == "The company manufactures aircraft."
    checks.append("valid span plus empty sibling preserves anchored description")
    for spans in [[7], [None], "manufactures aircraft"]:
        doc = fixtures._document()
        doc["sections"][0]["sentences"][0]["quoted_spans"] = spans
        result = read(doc)
        assert result["drafting_status"] == api.DRAFTING_INVALID and not result["drafted_sections"]
    checks.append("non-string members and non-array spans fail schema without reader exception")
    doc = fixtures._document()
    for i in [0, 1]:
        doc["sections"][i]["sentences"][0]["quoted_spans"] = []
    doc["held_no_span"] = [{"section": "risks", "text": "held", "evidence": ["P0002"], "reason": "no span"}] * 2
    doc["held_uncited"] = 3
    result = read(doc)
    assert result["drafting_status"] == api.DRAFTING_SERVED, result["drafting_reason"]
    assert result["held_no_span_on_object"] == result["held_no_span_at_read"] == 2
    assert result["held_no_span_count"] == 4 and result["held_uncited_count"] == 3
    assert sum(sec["held_no_span_at_read"] for sec in result["drafted_sections"]) == 2
    assert sum(len(sec["sentences"]) for sec in result["drafted_sections"]) == 2
    checks.append("producer2 + reader2 = no-span4; uncited3 stays distinct; section sum2")
    doc = fixtures._document()
    doc["sections"][0]["sentences"][0]["quoted_spans"] = ["this quotation does not exist"]
    assert read(doc)["drafting_status"] == api.DRAFTING_INVALID
    assert read(doc, True)["text"] is None
    checks.append("nonempty but false quotation still invalidates both consumers")

result = {"candidate_pin": PIN, "reviewer": "2.0.0_SA_COO~X", "verdict": "PASS",
          "evidence_level": "source plus offline exercise; static exact-package verification",
          "api_regressions": "227 passed in 27.02s in isolated exact-pin checkout", "independent_controls": checks,
          "candidate_zip_sha256": package_sha, "zip_members": 197,
          "changed_members": changed, "changed_function_scope": sorted(names),
          "limits": "No independent live retained-data replay, Linux Lambda execution, deployment, browser journey, CVO acceptance or never-widen authorization. Quotation existence is not claim entailment."}
out = Path(__file__).resolve().parent / "evidence" / "R_SERVING_REVIEW_dd91fd3126.json"
out.write_text(json.dumps(result, indent=2) + "\n", encoding="ascii")
print(json.dumps(result, indent=2))
