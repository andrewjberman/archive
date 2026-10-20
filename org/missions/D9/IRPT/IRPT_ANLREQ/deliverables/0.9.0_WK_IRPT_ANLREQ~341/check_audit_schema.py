"""AR467-y-AC1 (IRPT_ANLREQ AR-y-467): AnalysisAudit.v1 meta-validates; the good sample passes; the four one-linkage-missing
samples (ticket, form_as_filed, filer, package) are rejected. Offline, stdlib plus jsonschema (importable here, measured).
Prints exactly one line: AUDIT-SCHEMA-OK good=1 bad_rejected=4, or AUDIT-SCHEMA-BAD <why>. ASCII only."""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[7]  # org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<this>/ -> repo root
SCHEMA = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "_contracts" / "AnalysisAudit.v1.schema.json"

GOOD = {
    "schema_version": "AnalysisAudit.v1",
    "request_id": "REQ-ab12ab12ab12ab12ab12ab12",
    "firm_id": "cottonwood",
    "filed_at": "2026-10-20T15:52:27Z",
    "ticket": {"ticket_id": "TCK-20261009-0a1b2c3d", "ticket_type": "analysis_request"},
    "form_as_filed": {"report_type": "absent", "commentary": "present", "advisor": "Dev Advisor"},
    "filer": {"principal_id": "p1", "user_type": "client"},
    "package": {
        "report_ref": "RPT-d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1",
        "pdf_ref": "{\"artifact_id\":\"ART-x\",\"sha256\":\"" + "e7" * 32 + "\",\"version_id\":\"ver-pdf-1\"}",
        "commentary_ref": "{\"artifact_id\":\"ART-c\",\"sha256\":\"" + "c0" * 32 + "\",\"version_id\":\"ver-c-1\"}",
        "original_ref": "UPL-fixture-0001",
    },
    "written_at": "2026-10-20T18:00:00Z",
}


def bad_samples():
    """Each sample is GOOD with exactly one linkage removed."""
    out = []
    for linkage in ("ticket", "form_as_filed", "filer", "package"):
        sample = copy.deepcopy(GOOD)
        del sample[linkage]
        out.append((linkage, sample))
    return out


def main():
    try:
        import jsonschema
    except ImportError as exc:
        print("AUDIT-SCHEMA-BAD jsonschema not importable (%s)" % type(exc).__name__)
        return 1
    with open(str(SCHEMA), encoding="utf-8") as handle:
        schema = json.load(handle)
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError:
        print("AUDIT-SCHEMA-BAD schema does not meta-validate under Draft 2020-12")
        return 1
    validator = jsonschema.Draft202012Validator(schema)
    if list(validator.iter_errors(GOOD)):
        print("AUDIT-SCHEMA-BAD the good sample is refused")
        return 1
    rejected = 0
    for linkage, sample in bad_samples():
        if list(validator.iter_errors(sample)):
            rejected += 1
        else:
            print("AUDIT-SCHEMA-BAD sample without %s is admitted" % linkage)
            return 1
    print("AUDIT-SCHEMA-OK good=1 bad_rejected=%d" % rejected)
    return 0


if __name__ == "__main__":
    sys.exit(main())
