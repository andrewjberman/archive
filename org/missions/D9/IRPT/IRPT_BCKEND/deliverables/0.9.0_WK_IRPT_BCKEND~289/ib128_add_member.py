"""Add unprojected_grant to the four closed response schemas, declaration copied as JSON from status-job."""
import json
R = "docs/contracts/investor-reporting/v1/responses/"
SRC = "status-job"
FOUR = ["analysis-request-pdf", "comparison-catalogue", "custody-report-persist", "custody-report-read"]
def load(n):
    raw = open(R + n + ".response.schema.json", "rb").read()
    return raw, json.loads(raw.decode("utf-8"))
_, src = load(SRC)
decl = src["properties"]["unprojected_grant"]
for n in FOUR:
    raw, doc = load(n)
    rt = (json.dumps(doc, indent=2, ensure_ascii=False) + ("\n" if raw.endswith(b"\n") else "")).encode("utf-8")
    assert rt == raw, "roundtrip not byte-identical for " + n
    assert "unprojected_grant" not in doc["properties"] and "unprojected_grant" not in doc["required"]
    doc["properties"]["unprojected_grant"] = json.loads(json.dumps(decl))
    doc["required"].append("unprojected_grant")
    out = (json.dumps(doc, indent=2, ensure_ascii=False) + ("\n" if raw.endswith(b"\n") else "")).encode("utf-8")
    open(R + n + ".response.schema.json", "wb").write(out)
    print("OK:", n)
