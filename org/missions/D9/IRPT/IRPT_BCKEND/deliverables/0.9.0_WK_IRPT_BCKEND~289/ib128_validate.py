"""IB128-1 (0.9.0_WK_IRPT_BCKEND~289): prints (1) the three-envelope result per changed route and (2) the two re-made fixtures'
validation results; writes .scratch/ib128_validation_results.json. Run from the repo root:
    python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~289/ib128_validate.py
Valid envelopes are built by served.response_envelope (the handlers' own envelope function, member at zero) around the route's
valid `data` fixture; the validator is test_seam_paired.validate_against_response_contract (referencing registry over the v1 files)."""
import copy
import json
import os
import sys
ROOT = os.getcwd()
PKG = os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting")
sys.path.insert(0, PKG)
sys.path.insert(0, os.path.join(PKG, "_contracts", "tests"))
sys.path.insert(0, os.path.join(PKG, "_authz"))
import test_seam_paired as seam  # noqa: E402
from test_seam_paired import validate_against_response_contract as validate, _response_validator  # noqa: E402
import importlib  # noqa: E402
try:
    served = importlib.import_module("_authz.served")
except Exception:
    served = importlib.import_module("served")
FX = os.path.join(PKG, "_contracts", "fixtures")
V1 = seam.V1
MEMBER = "unprojected_grant"
FIRM = "fir_" + "0123456789abcdef01234567"

def inst(name):
    return json.load(open(os.path.join(FX, name), encoding="utf-8"))["instance"]

ROUTES = {
    "analysis-request-pdf": "AnalysisRequestPdf.valid.json",
    "comparison-catalogue": "ComparisonCatalogue.valid.json",
    "custody-report-persist": "custody-report-persist.response.valid.json",
    "custody-report-read": "custody-report-read.response.valid.json",
}
out = {"routes": [], "fixtures": []}
for op, fx in ROUTES.items():
    env = served.response_envelope(op, FIRM, inst(fx))
    assert env[MEMBER] == {"count": 0, "denominator": 0, "kinds": {}}, env
    a = validate(op, env)
    no = copy.deepcopy(env)
    no.pop(MEMBER)
    b = validate(op, no)
    fo = copy.deepcopy(env)
    fo["foreign_member"] = {"x": 1}
    c = validate(op, fo)
    row = {"operation": op, "data_fixture": fx, "with_member": a, "without_member": b, "foreign_member": c,
           "with_member_validates": a[0] is True, "without_member_refused": b[0] is False, "foreign_member_refused": c[0] is False}
    out["routes"].append(row)
    print("%-24s with=%s without_refused=%s (%s) foreign_refused=%s (%s)" % (
        op, a[0], row["without_member_refused"], b[1][:60], row["foreign_member_refused"], c[1][:60]))

def type_validator(schema_name):
    schema = json.load(open(os.path.join(V1, schema_name), encoding="utf-8"))
    return _response_validator(schema)
FIXT = [("DirectoryPage", "directory-browse"), ("AnalysisUploadResult", "analysis-input-upload")]
for doc, op in FIXT:
    v = inst(doc + ".valid.json")
    bad = inst(doc + ".invalid.json")
    t_ok = not list(type_validator(doc + ".schema.json").iter_errors(v))
    t_bad_refused = bool(list(type_validator(doc + ".schema.json").iter_errors(bad)))
    resp = seam.response_contract(op)
    data_schema = resp["properties"]["data"]
    # data-member validation: the response schema's data subschema, resolved through the v1 registry
    dv = _response_validator(data_schema)
    d_ok = not list(dv.iter_errors(v))
    d_bad_refused = bool(list(dv.iter_errors(bad)))
    r = {"fixture": doc + ".valid.json", "validates_type_schema": t_ok, "validates_response_data": d_ok,
         "invalid_sibling_refused_by_type_schema": t_bad_refused, "invalid_sibling_refused_by_response_data": d_bad_refused}
    out["fixtures"].append(r)
    print(r)
json.dump(out, open(os.path.join(ROOT, ".scratch", "ib128_validation_results.json"), "w"), indent=1)
