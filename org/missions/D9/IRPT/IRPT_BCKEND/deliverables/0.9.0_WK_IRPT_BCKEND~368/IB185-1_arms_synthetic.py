"""Four arms on SYNTHETIC receipts, offline (no Lambda invoke, no S3 write).

Usage: python -I arms.py <built_schema.json> <live_schema.json>
The synthetic receipt is filled from the BUILT schema's own required lists (all made-up values).
Verdict = what jsonschema's validator returns: 'valid' when no error is yielded, else 'refused'.
"""
import copy
import json
import re
import sys

import jsonschema
from jsonschema import Draft202012Validator

CANDIDATES = ["0" * 64, "2026-10-13", "2026-10-13T00:00:00Z", "SYN-0001", "x"]


def fill(node, root):
    if "$ref" in node:
        raise SystemExit("unexpected $ref in schema")
    if "const" in node:
        return copy.deepcopy(node["const"])
    if "enum" in node:
        return node["enum"][0]
    t = node.get("type")
    if isinstance(t, list):
        t = [x for x in t if x != "null"][0]
    if t == "object" or (t is None and "properties" in node):
        out = {}
        props = node.get("properties", {})
        for k in node.get("required", []):
            out[k] = fill(props[k], root)
        return out
    if t == "array":
        n = max(1, node.get("minItems", 0))
        return [fill(node["items"], root) for _ in range(n)]
    if t == "string":
        pat = node.get("pattern")
        for c in CANDIDATES:
            if len(c) < node.get("minLength", 0):
                continue
            if pat is None or re.search(pat, c):
                return c
        raise SystemExit("no candidate string matches pattern %r" % pat)
    if t == "integer":
        return max(1, node.get("minimum", 1))
    if t == "number":
        return max(1, node.get("minimum", 1))
    if t == "boolean":
        return True
    raise SystemExit("unhandled schema node: %r" % node)


def verdict(instance, schema):
    v = Draft202012Validator(schema)
    errs = sorted(v.iter_errors(instance), key=lambda e: list(e.path))
    if not errs:
        return "valid", []
    return "refused", [e.message[:160] for e in errs]


def main():
    built = json.load(open(sys.argv[1], encoding="utf-8"))
    live = json.load(open(sys.argv[2], encoding="utf-8"))
    Draft202012Validator.check_schema(built)
    Draft202012Validator.check_schema(live)
    r12 = fill(built, built)
    assert "covered_account_ids" in r12["facts"], "built schema must require facts.covered_account_ids"
    rpre = copy.deepcopy(r12)
    del rpre["facts"]["covered_account_ids"]
    arms = [
        ("v12_receipt_on_live", r12, live),
        ("v12_receipt_on_built", r12, built),
        ("pre12_receipt_on_built", rpre, built),
        ("pre12_receipt_on_live", rpre, live),
    ]
    for name, inst, sch in arms:
        vd, msgs = verdict(inst, sch)
        print("ARM %s verdict=%s errors=%d" % (name, vd, len(msgs)))
        for m in msgs[:3]:
            print("    " + m)
    print("facts keys in v12 receipt: %s" % sorted(r12["facts"].keys()))
    print("facts keys in pre12 receipt: %s" % sorted(rpre["facts"].keys()))
    print("jsonschema %s" % jsonschema.__version__ if False else "jsonschema imported")


if __name__ == "__main__":
    main()
