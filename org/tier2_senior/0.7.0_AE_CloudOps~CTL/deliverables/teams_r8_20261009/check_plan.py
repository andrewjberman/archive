"""Reject every deviation from TO19 signed branch A."""

import base64
import hashlib
import json
import pathlib

p = pathlib.Path(__file__).resolve().parent
plan = json.loads((p / "plan.json").read_text(encoding="utf-8-sig"))
expected = {
    "module.ldo_001.aws_lambda_function.handler",
    "module.ldo_001.aws_lambda_function.ingress[0]",
}
sha = base64.b64encode(
    hashlib.sha256(
        pathlib.Path(
            "infra/aws/lambda/teams-chat-assist/dist/teams-chat-assist.zip"
        ).read_bytes()
    ).digest()
).decode()
changes = [
    r
    for r in plan.get("resource_changes", [])
    if r["change"]["actions"] != ["no-op"] and r.get("mode") != "data"
]
assert {r["address"] for r in changes} == expected, "Unexpected changed addresses"
result = []
for r in changes:
    c = r["change"]
    assert c["actions"] == ["update"], "Unexpected actions"
    before = c["before"]
    after = c["after"]
    keys = {k for k in before.keys() | after.keys() if before.get(k) != after.get(k)}
    assert keys <= {"source_code_hash", "last_modified"}, f"Unexpected keys {keys}"
    assert "source_code_hash" in keys and after["source_code_hash"] == sha, (
        "Hash mismatch"
    )

    def unknown(v):
        if isinstance(v, dict):
            return any(unknown(x) for x in v.values())
        if isinstance(v, list):
            return any(unknown(x) for x in v)
        return v is True

    assert {k for k, v in c.get("after_unknown", {}).items() if unknown(v)} <= {
        "last_modified"
    }, "Unexpected computed values"
    result.append(
        {
            "address": r["address"],
            "actions": c["actions"],
            "changed_keys": sorted(keys),
            "after_hash": sha,
        }
    )
out = {"branch": "A", "add": 0, "change": 2, "destroy": 0, "resources": result}
(p / "plan-verdict.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
