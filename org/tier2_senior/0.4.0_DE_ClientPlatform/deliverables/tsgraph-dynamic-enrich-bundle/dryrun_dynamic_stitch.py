"""LOCAL dry-run of stitch_served_from_dynamic -- NO commit, NO deploy, NO graph write.
Builds a minimal graph dict (3 real firm S3 nodes + Endpoint nodes from the resolution table +
2 control non-table endpoints), runs the real derive against LIVE S3, prints the formed edges.
Validates: matching, per-firm fan-out, both-ends head_object verify, 0 dangling, control-skip."""
from __future__ import annotations
import json, sys, os

GLOBGRPH = r"C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph"
# Extract ONLY the function + its 2 constants from the real file (byte-identical) and exec in
# isolation -- avoids derive_runner's deployed-/app import chain (comp_aws_cli/ms_cloud_extract).
import boto3  # noqa: E402
src = open(os.path.join(GLOBGRPH, "derive_runner.py"), encoding="utf-8").read()
start = src.index("_DYN_FIRMS = {")
end = src.index("# =============================================================================\n# NFRA_GRAPHS.D8-FP", start)
ns = {"os": os, "json": json, "boto3": boto3, "__file__": os.path.join(GLOBGRPH, "derive_runner.py")}
exec(compile(src[start:end], "derive_runner_slice", "exec"), ns)
derive_runner = type("M", (), ns)  # shim so derive_runner.stitch_served_from_dynamic works

table = json.load(open(os.path.join(GLOBGRPH, "tsgraph_dynamic_served_resolution.json")))["endpoint_to_platinum_key"]

# minimal graph dict in the shape the derive expects (classes_data{class:{nodes:[...]}} + edges)
endpoint_nodes = [{"id": f"endpoint:{lbl}", "type": "Endpoint", "name": lbl} for lbl in table]
# 2 controls that are NOT in the table -> must be skipped (no edge)
endpoint_nodes += [{"id": "endpoint:getAUMMetrics", "type": "Endpoint", "name": "getAUMMetrics"},
                   {"id": "endpoint:warmLambda", "type": "Endpoint", "name": "warmLambda"}]
s3_nodes = [
    {"id": "arn:aws:s3:::opal-data-bd", "type": "S3_BUCKET", "name": "opal-data-bd"},
    {"id": "arn:aws:s3:::opal-data-cot", "type": "S3_BUCKET", "name": "opal-data-cot"},
    {"id": "arn:aws:s3:::opal-data-inf", "type": "S3_BUCKET", "name": "opal-data-inf"},
]
graph = {"classes_data": {"ts_semantic": {"nodes": endpoint_nodes}, "aws": {"nodes": s3_nodes}}, "edges": []}

print("=== running stitch_served_from_dynamic (live head_object) ===")
derive_runner.stitch_served_from_dynamic(graph)

edges = graph["edges"]
print(f"\n=== RESULT: {len(edges)} edges formed ===")
by_ep = {}
for e in edges:
    by_ep.setdefault(e["source"].replace("endpoint:", ""), []).append(f'{e["firm"]}:{e["s3_key"]}')
for ep, fs in sorted(by_ep.items()):
    print(f"  {ep}: {sorted(fs)}")

# assertions
srcs = {e["source"] for e in edges}
assert "endpoint:warmLambda" not in srcs, "CONTROL FAIL: non-table endpoint formed an edge"
assert "endpoint:getAUMMetrics" not in srcs, "CONTROL FAIL: getAUMMetrics (not in table) formed an edge"
assert all(e["target"].startswith("arn:aws:s3:::") for e in edges), "DANGLING: an edge targets a non-arn node id"
assert all(e["tier"] == "dynamic" and e["verified"] == "object+node" for e in edges), "prop check failed"
print(f"\nOK: controls skipped, 0 dangling, all edges tier=dynamic+verified. matched {len(by_ep)}/{len(table)} table endpoints.")
