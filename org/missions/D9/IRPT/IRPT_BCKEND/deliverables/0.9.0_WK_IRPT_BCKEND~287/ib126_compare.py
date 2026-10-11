"""IB126 comparer (worker 0.9.0_WK_IRPT_BCKEND~287, IRPT_BCKEND.TO-IB-pr-428). READ ONLY, LOCAL ONLY.

For each route: load the envelope the handler returned in process (captured by ib126_capture_plugin.py into
<repo>/.scratch/answers/, synthetic test-fake values, git-ignored), validate the WHOLE envelope against the route's v1
response schema with the validator `_contracts/tests/test_seam_paired.py` itself uses (imported, not copied), and compare
the SHAPE of its `data` member with the producer fixture's `instance`: member names at each level and each member's JSON
type. VALUES ARE NEVER COMPARED AND NEVER WRITTEN to the output.

Usage: python ib126_compare.py <repo_root>   (writes IB126-1_handler_shape_vs_fixture.json beside this file)
"""
import copy
import importlib.util
import json
import os
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
HERE = os.path.dirname(os.path.abspath(__file__))
IR = os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting")
FIX = os.path.join(IR, "_contracts", "fixtures")
ANS = os.path.join(ROOT, ".scratch", "answers")
OUT = os.path.join(HERE, "IB126-1_handler_shape_vs_fixture.json")


def load_seam():
    path = os.path.join(IR, "_contracts", "tests", "test_seam_paired.py")
    spec = importlib.util.spec_from_file_location("ib126_seam_paired", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SEAM = load_seam()


def jtype(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, int):
        return "integer"
    if isinstance(v, float):
        return "number"
    if isinstance(v, str):
        return "string"
    if isinstance(v, dict):
        return "object"
    if isinstance(v, list):
        return "array"
    return type(v).__name__


def walk(v, path, types, opaque):
    """types[path] = set of JSON types seen; opaque = paths holding an empty object/array (children unobservable)."""
    types.setdefault(path, set()).add(jtype(v))
    if isinstance(v, dict):
        if not v:
            opaque.add(path)
        for k, x in v.items():
            walk(x, path + "." + k, types, opaque)
    elif isinstance(v, list):
        if not v:
            opaque.add(path)
        for x in v:
            walk(x, path + "[]", types, opaque)


def walk_paths(v):
    types, opaque = {}, set()
    walk(v, "data", types, opaque)
    return [p + ":" + "|".join(sorted(t)) for p, t in types.items() if p != "data"]


def remove_path(doc, path):
    """Delete the member `path` (dotted from "data"; `name[]` descends into every list element) from a deep copy of
    the envelope `doc`. Returns (copy, removed?)."""
    parts = path.split(".")[1:]
    removed = [False]

    def rec(node, idx):
        name = parts[idx]
        is_list = name.endswith("[]")
        key = name[:-2] if is_list else name
        last = idx == len(parts) - 1
        if not isinstance(node, dict) or key not in node:
            return
        if last and not is_list:
            del node[key]
            removed[0] = True
            return
        child = node[key]
        if is_list and not last:
            for item in (child if isinstance(child, list) else []):
                rec(item, idx + 1)
        elif not is_list:
            rec(child, idx + 1)

    out = copy.deepcopy(doc)
    rec(out["data"], 0)
    return out, removed[0]


def get_parent(doc, path):
    """The object that holds member `path` (list segments take element 0)."""
    node = doc["data"]
    for name in path.split(".")[1:-1]:
        is_list = name.endswith("[]")
        node = node[name[:-2] if is_list else name]
        if is_list:
            node = node[0]
    return node


def schema_errors(op, envelope):
    schema = SEAM.response_contract(op)
    validator = SEAM._response_validator(schema)
    return sorted(validator.iter_errors(envelope), key=lambda e: [str(p) for p in e.absolute_path])


def valid(op, envelope):
    return not schema_errors(op, envelope)


def oracle_form(op, envelope):
    """The envelope with any top-level member the response schema does not declare removed, so the optional-by-schema
    oracle asks about the `data` member alone. Used ONLY by the oracle; the schema verdict is always read on the
    envelope exactly as the handler returned it."""
    schema = SEAM.response_contract(op)
    declared = set(schema.get("properties", {}))
    if schema.get("additionalProperties") is False:
        return {k: v for k, v in envelope.items() if k in declared}
    return envelope


def envelope_differences(op, envelope):
    """Envelope-level members that make the handler's answer fail its own response schema, named."""
    out = []
    for e in schema_errors(op, envelope):
        where = "/".join(str(p) for p in e.absolute_path)
        if e.validator == "additionalProperties" and isinstance(e.instance, dict):
            declared = set(e.schema.get("properties", {}))
            for key in sorted(k for k in e.instance if k not in declared):
                out.append({"path": "envelope." + (where + "." if where else "") + key,
                            "handler": jtype(e.instance[key]),
                            "fixture": "not declared by the response schema, which sets additionalProperties false",
                            "optional_by_schema": False})
        else:
            out.append({"path": "envelope." + where, "handler": "fails schema keyword " + e.validator,
                        "fixture": "n/a", "optional_by_schema": False, "note": e.message[:160]})
    return out


def ancestors(path):
    """Proper ancestor member paths of `data.a[].b.c`: data.a[].b, data.a[], data.a (and data)."""
    out, cur = [], path
    while True:
        if cur.endswith("[]"):
            cur = cur[:-2]
        else:
            cut = cur.rfind(".")
            if cut <= 0:
                break
            cur = cur[:cut]
        out.append(cur)
    return out


def compare(op, answer, fixture_instance):
    """(differing, optional, unexercised, unobserved, fixture_valid) for answer["data"] against the fixture instance.
    Shapes only: member names and JSON types."""
    h_types, f_types, h_opaque, f_opaque = {}, {}, set(), set()
    walk(answer["data"], "data", h_types, h_opaque)
    walk(fixture_instance, "data", f_types, f_opaque)
    base_answer = oracle_form(op, answer)
    fixture_as_answer = dict(base_answer, data=copy.deepcopy(fixture_instance))
    fixture_valid_in_envelope = valid(op, fixture_as_answer)
    handler_valid_for_oracle = valid(op, base_answer)
    differing, optional, unexercised, unobserved = [], [], [], []
    one_sided = {p for p in set(h_types) | set(f_types) if (p in h_types) != (p in f_types)}

    def under_opaque(path, opaque):
        return any(path.startswith(o + ".") or path.startswith(o + "[]") for o in opaque)

    for path in sorted(set(h_types) | set(f_types)):
        if path == "data":
            continue
        in_h, in_f = path in h_types, path in f_types
        if in_h and in_f:
            hs, fs = h_types[path], f_types[path]
            if hs != fs:
                if hs < fs:
                    unexercised.append({
                        "path": path, "handler_sample": sorted(hs), "fixture": sorted(fs),
                        "note": "the handler's sample showed a subset of the fixture's types for this member (a nullable or "
                                "state-dependent member seen in one state); the other state was not exercised by this run"})
                else:
                    differing.append({"path": path, "handler": sorted(hs), "fixture": sorted(fs),
                                      "optional_by_schema": False, "note": "present on both sides with different JSON types"})
            continue
        if any(a in one_sided for a in ancestors(path)):
            continue                           # covered by its one-sided ancestor
        if under_opaque(path, h_opaque) or under_opaque(path, f_opaque):
            unobserved.append(path)            # the other side holds an empty container here: children cannot be compared
            continue
        side = "handler_only" if in_h else "fixture_only"
        probe_doc = base_answer if in_h else fixture_as_answer
        stripped, removed = remove_path(probe_doc, path)
        baseline_ok = handler_valid_for_oracle if in_h else fixture_valid_in_envelope
        optional_ok = bool(removed and baseline_ok and valid(op, stripped))
        free_form = False
        try:
            probe = copy.deepcopy(probe_doc)
            parent = get_parent(probe, path)
            if isinstance(parent, dict):
                parent["ib126_probe_member"] = "x"
                free_form = valid(op, probe)
        except (KeyError, IndexError, TypeError):
            pass
        entry = {"path": path, "side": side, "type": sorted((h_types if in_h else f_types)[path]),
                 "optional_by_schema": optional_ok, "parent_is_free_form_in_schema": free_form}
        if optional_ok:
            optional.append(entry)
        else:
            differing.append({"path": path, "handler": sorted(h_types[path]) if in_h else "ABSENT",
                              "fixture": sorted(f_types[path]) if in_f else "ABSENT", "optional_by_schema": False,
                              "note": "required by the schema on the side that holds it, absent on the other"})
    return differing, optional, unexercised, unobserved, fixture_valid_in_envelope


def judge(op, answer_file, fixture_file, label=None):
    with open(os.path.join(ANS, answer_file), encoding="utf-8") as fh:
        answer = json.load(fh)
    with open(os.path.join(FIX, fixture_file), encoding="utf-8") as fh:
        fixture = json.load(fh)["instance"]
    errs = schema_errors(op, answer)
    differing, optional, unexercised, unobserved, fixture_ok = compare(op, answer, fixture)
    env_diff = envelope_differences(op, answer)
    return {
        "answer_file": answer_file, "label": label,
        "envelope_keys": sorted(answer.keys()), "envelope_key_types": {k: jtype(v) for k, v in answer.items()},
        "handler_answer_vs_response_schema": "VALID" if not errs else "INVALID",
        "schema_failure_path": None if not errs else [
            "/".join(str(p) for p in e.absolute_path) + " :: " + e.message[:160] for e in errs[:5]],
        "fixture_instance_valid_in_the_handlers_envelope_without_undeclared_members": fixture_ok,
        "data_member_shape_vs_fixture": "SAME" if not differing else "DIFFERS",
        "handler_data_members": sorted(walk_paths(answer["data"])),
        "differing_members": env_diff + differing, "optional_omissions": optional,
        "unexercised_alternatives": unexercised,
        "unobserved_children_of_empty_containers": unobserved,
    }


def verdict_of(j):
    if j["handler_answer_vs_response_schema"] == "VALID" and not j["differing_members"]:
        return "SAME_AS_FIXTURE"
    return "DIFFERS" if j["differing_members"] else "NOT_ESTABLISHED"


PIN_FILES = {
    "directory-browse": ["directory/entry.py", "_authz/served.py"],
    "analysis-request-history": ["ops/owned_requests.py", "ops/entry.py", "reports/status_installed.py", "_authz/served.py"],
    "analysis-input-upload": ["intake/uploads.py", "intake/upload_entry.py", "reports/generate_installed.py", "_authz/served.py"],
    "custody-report-read": ["export/custody_read.py", "export/entry.py", "_authz/served.py"],
    "custody-report-persist": ["export/custody_persist.py", "export/entry.py", "_authz/served.py"],
    "comparison-catalogue": ["ycharts/generate/comparison_catalogue.py", "ycharts/generate/entry.py", "_authz/served.py"],
}


def pins_for(op, function):
    path = os.path.join(HERE, "ib126_source_map_pins.json")
    if not os.path.isfile(path):
        return None
    pins = json.load(open(path, encoding="utf-8"))
    block = pins["functions"][function]
    return {"function": function, "last_deployed_commit": block["last_deployed_commit"],
            "last_deployed_at": block["last_deployed_at"], "head_read": pins["head"],
            "files": {f: block["files"][f] for f in PIN_FILES[op] if f in block["files"]}}


def accounts_note(op, answer):
    if op == "custody-report-read":
        report = answer["data"].get("report")
        return (isinstance(report, dict) and isinstance(report.get("accounts"), list),
                "the handler's data.report is the persisted document passed through (export/custody_read.py:78); in this run it "
                "has no accounts member at all (members: %s)" % ", ".join(sorted(report)) if isinstance(report, dict) else "no report")
    if op == "custody-report-persist":
        return (None, "not applicable: the persist answer is the report's reference (kind, id, revision, sha256), never the document")
    return None


def main():
    facts = json.load(open(os.path.join(HERE, "ib126_route_facts.json"), encoding="utf-8"))
    result = {"method": facts["_method"], "routes": [], "control": None}
    keep = ("envelope_keys", "envelope_key_types", "handler_answer_vs_response_schema", "schema_failure_path",
            "fixture_instance_valid_in_the_handlers_envelope_without_undeclared_members",
            "data_member_shape_vs_fixture", "differing_members", "optional_omissions", "unexercised_alternatives",
            "unobserved_children_of_empty_containers", "handler_data_members")
    for op, f in facts["routes"].items():
        j = judge(op, f["answer_file"], f["fixture"])
        row = {k: f[k] for k in ("operation", "route_key", "function", "answer_built_at", "envelope_built_at",
                                 "evidence", "invocation", "tests_run_unaltered", "fixture")}
        row.update({k: j[k] for k in keep})
        row["also_observed"] = []
        for extra in f.get("also", []):
            r = judge(op, extra["answer_file"], f["fixture"], extra["label"])
            r.update({k: extra[k] for k in ("invocation", "answer_built_at")})
            r["verdict"] = verdict_of(r)
            row["also_observed"].append(r)
        row["verdict"] = verdict_of(j)
        row["why_not"] = None
        row["source_map_pin"] = pins_for(op, f["function"])
        with open(os.path.join(ANS, f["answer_file"]), encoding="utf-8") as fh:
            note = accounts_note(op, json.load(fh))
        if note is not None:
            row["custody_report_accounts_is_array"], row["custody_report_accounts_note"] = note
        result["routes"].append(row)
    c = facts["control"]
    cj = judge("comparison-catalogue", c["answer_file"], c["fixture"])
    result["control"] = {k: c[k] for k in ("operation", "route_key", "function", "answer_built_at", "envelope_built_at",
                                           "evidence", "invocation", "fixture")}
    result["control"].update({k: cj[k] for k in keep})
    result["control"]["verdict"] = verdict_of(cj)
    result["control"]["source_map_pin"] = pins_for("comparison-catalogue", c["function"])
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
        fh.write("\n")
    for r in result["routes"] + [result["control"]]:
        print("%-26s schema=%-8s data=%-7s verdict=%-16s differing=%d optional=%d unexercised=%d unobserved=%d" % (
            r["operation"], r["handler_answer_vs_response_schema"], r["data_member_shape_vs_fixture"], r["verdict"],
            len(r["differing_members"]), len(r["optional_omissions"]), len(r["unexercised_alternatives"]),
            len(r["unobserved_children_of_empty_containers"])))
    for r in result["routes"][2:3]:
        for x in r["also_observed"]:
            print("  also %-10s schema=%s data=%s verdict=%s" % (x["answer_file"], x["handler_answer_vs_response_schema"],
                                                             x["data_member_shape_vs_fixture"], x["verdict"]))


if __name__ == "__main__":
    main()
