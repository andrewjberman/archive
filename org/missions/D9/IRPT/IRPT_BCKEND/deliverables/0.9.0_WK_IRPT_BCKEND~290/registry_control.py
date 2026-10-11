"""IB-pr-432 AMENDMENT 1 control: the test registry resolves the v2 report $id and no other non-v1 id.
Run from infra/aws/lambda/investor-reporting/_contracts/tests/ : python <this file>"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import jsonschema  # noqa: E402
import test_seam_paired as t  # noqa: E402

v2 = t._v2_report_id()


def resolves(ref):
    s = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$ref": ref}
    try:
        t._response_validator(s).validate("OPAL_ENGINE")
    except jsonschema.ValidationError:
        return True          # the ref resolved and the instance was graded
    except Exception:        # noqa: BLE001 -- Unresolvable
        return False
    return True


v2_ref = v2 + "#/$defs/opal_engine/properties/provider"
other = "opal://irpt/contracts/v2/Other.schema.json#/x"
out = {
    "v2_id": v2,
    "_ref_published_path(v2 ref)": os.path.relpath(t._ref_published_path(v2_ref), t._REPO).replace(os.sep, "/"),
    "_ref_published_path(other v2-folder id)": t._ref_published_path(other),
    "_ref_published_path(foreign id)": t._ref_published_path("opal://example/contracts/v9/AnalysisReport.schema.json#/x"),
    "registry_control": {"v2_ref_resolves": resolves(v2_ref), "other_non_v1_ref_resolves": resolves(other)},
}
print(json.dumps(out, indent=2))
