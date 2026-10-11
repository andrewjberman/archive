"""IB-pr-426 replay: the five changed contract schemas AS THE ZIP CARRIES THEM (<tree>/contracts/), through ONE extracted tree. Run as
    python -I schema_probe426.py <extracted_zip_dir> <label> <out_json>
Loads every packaged schema into a referencing Registry by $id, then validates small synthetic documents (no client data) that the NEW shapes
produce / the LEGACY shapes produced, and compares property names, required lists and enum value SETS file by file. Offline. ASCII only."""
import hashlib
import json
import sys
from pathlib import Path
zip_dir, label, out_path = sys.argv[1:4]
sys.dont_write_bytecode = True
import jsonschema  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

d = Path(zip_dir) / "contracts"
docs = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("*.schema.json"))}
reg = Registry()
for name, doc in docs.items():
    reg = reg.with_resource(doc["$id"], Resource.from_contents(doc, default_specification=DRAFT202012))
BASE = "opal://irpt/contracts/v1/"


def ok(schema_name, instance, pointer=""):
    schema = {"$ref": BASE + schema_name + pointer}
    try:
        jsonschema.Draft202012Validator(schema, registry=reg).validate(instance)
        return "valid"
    except jsonschema.ValidationError:
        return "invalid"
    except Exception as exc:  # noqa: BLE001 -- e.g. an unresolvable pointer on the live schema
        return "unresolvable:" + type(exc).__name__


IDENT = {"tenant_firm_id": "49financial", "request_id": "REQ-" + "a" * 24, "revision": 1, "immutable": True,
         "ingestion_gate_revision": "schemas-" + "a" * 64, "destination_policy_revision": "a" * 64}
ident_ok = ok("OwnedAnalysisRequest.schema.json", {"identity": IDENT, "accepted_at": 1700000000}, "")
new_row = {"identity": IDENT, "accepted_at": 1700000000, "client_id": "C-one", "client_claim": "SELECTED"}
old_row = {"identity": IDENT, "accepted_at": 1700000000}
out = {"label": label, "identity_sample_valid_against_OwnedAnalysisRequest": ident_ok,
       "history_new_shape": ok("OwnedAnalysisRequestHistory.schema.json", {"items": [new_row], "next_cursor": None, "unreadable_rows": 0}),
       "history_legacy_shape": ok("OwnedAnalysisRequestHistory.schema.json", {"items": [old_row], "next_cursor": None}),
       "analysis_report_retained_ref": ok("AnalysisReport.schema.json", {"report_id": "RPT-" + "a" * 32, "revision": "b" * 64, "sha256": "c" * 64,
                                          "report_kind": "ANALYSIS", "immutable": True}, "#/properties/retained_ref"),
       "holdings_asset_class_multi_asset": ok("HoldingsSnapshot.schema.json", "multi_asset", "#/properties/nodes/items/properties/asset_class"),
       "holdings_asset_class_equity": ok("HoldingsSnapshot.schema.json", "equity", "#/properties/nodes/items/properties/asset_class"),
       "export_receipt_covered_account_ids": ok("ExportReceipt.schema.json", ["acct-opaque-1"], "#/properties/facts/properties/covered_account_ids"),
       "export_receipt_facts_required": sorted(docs["ExportReceipt.schema.json"]["properties"]["facts"].get("required") or []),
       "owned_request_persist_inputs": ok("OwnedAnalysisRequest.schema.json", {"artifact_id": "ART-" + "a" * 64, "composition_sha256": "b" * 64,
                                          "retention_policy": "irpt-retention-v1", "report_index": None}, "#/properties/persist_inputs")}


def walk_enums(node, path, acc):
    if isinstance(node, dict):
        if isinstance(node.get("enum"), list):
            acc[path] = node["enum"]
        for k, v in node.items():
            walk_enums(v, path + "/" + k, acc)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk_enums(v, path + "/%d" % i, acc)


def props(doc):
    return sorted((doc.get("properties") or {}).keys())


facts = {}
for name in ("AnalysisReport", "ExportReceipt", "HoldingsSnapshot", "OwnedAnalysisRequest", "OwnedAnalysisRequestHistory"):
    doc = docs[name + ".schema.json"]
    enums = {}
    walk_enums(doc, "", enums)
    facts[name] = {"top_level_properties": props(doc), "required": sorted(doc.get("required") or []),
                   "enum_nodes": len(enums), "enum_nodes_with_duplicate_values": sum(len(v) != len(set(map(json.dumps, v))) for v in enums.values()),
                   "enum_value_sets_sha256": hashlib.sha256(json.dumps({k: sorted(set(map(json.dumps, v))) for k, v in sorted(enums.items())}).encode()).hexdigest()[:16],
                   "file_sha256_16": hashlib.sha256((d / (name + ".schema.json")).read_bytes()).hexdigest()[:16]}
out["files"] = facts
json.dump(out, open(out_path, "w"), indent=1, sort_keys=True)
print("OK", label, {k: v for k, v in out.items() if k not in ("files", "label")})
