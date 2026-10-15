"""IRPT_DASHBD round 125, workstream B-49F (worker 0.9.0_WK_IRPT_DASHBD~209) -- DB-b-256, the dim_return_method CLAIMS READ.

READ-ONLY. GET and LIST only. Reads:
  1. the producer's claim columns: an ast scan of account_return_daily.py (THRESHOLD_VALUES, each + "_claim", plus
     threshold_claims_source); the producer is not imported;
  2. the 49 Financial dim_return_method prefix, derived by lib/opal_naming.py address(): one LIST of the prefix, and for
     each method_version=N/data.parquet the parquet SCHEMA (column names only; no value is read out of the file);
  3. every call of emit_method_row in the producer tree and the gold Lambda tree (an ast scan; test folders excluded;
     comments and definitions do not count);
  4. the investor-reporting Terraform files whose uncommented text names the prefix, and whether the uncommented
     irpt_rg_gold_write_arns list of the reporting-gold locals.tf names it.
Writes: one counts-and-names private file under the worker's private evidence folder. Nothing else.

Usage: python -I <this file> <repo_root>
"""
import ast
import hashlib
import io
import json
import os
import re
import sys

FIRM_KEY = "49financial"
TABLE = "dim_return_method"
PRODUCER_REL = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
SCAN_DIRS = ("data/assets/scripts/gold/irpt_reporting", "infra/aws/lambda/investor-reporting")
TF_DIR = "infra/aws/terraform/investor-reporting"
GOLD_LOCALS_REL = "infra/aws/terraform/investor-reporting/reporting-gold/locals.tf"
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~209"
PRIVATE_NAME = "method_row_read_r125_counts.json"
ANALYSIS_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~209/method_row_read_r125.py"


class Reader(object):
    """GET and LIST only. There is deliberately no method that changes a remote object."""

    def __init__(self):
        import boto3
        self._s3 = boto3.client("s3")
        self.calls = 0

    def list_keys(self, bucket, prefix):
        keys = []
        token = None
        while True:
            kw = {"Bucket": bucket, "Prefix": prefix}
            if token is not None:
                kw["ContinuationToken"] = token
            self.calls += 1
            r = self._s3.list_objects_v2(**kw)
            keys.extend(o["Key"] for o in r.get("Contents", []))
            if not r.get("IsTruncated"):
                break
            token = r["NextContinuationToken"]
        return keys

    def get_bytes(self, bucket, key):
        self.calls += 1
        return self._s3.get_object(Bucket=bucket, Key=key)["Body"].read()


def uncommented(text):
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))


def claim_columns_of(src):
    tree = ast.parse(src)
    tv = None
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "THRESHOLD_VALUES" for t in n.targets):
            tv = ast.literal_eval(n.value)
    if not tv:
        raise SystemExit("STOP: THRESHOLD_VALUES not found in the producer")
    return sorted([v + "_claim" for v in tv] + ["threshold_claims_source"])


def call_sites_of(rel, src):
    """'rel::function' for each call of emit_method_row; a call at module level is '<module>'."""
    tree = ast.parse(src)
    out = []

    def visit(node, fn):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit(ch, ch.name)
                continue
            if isinstance(ch, ast.Call):
                f = ch.func
                nm = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
                if nm == "emit_method_row":
                    out.append("%s::%s" % (rel, fn))
            visit(ch, fn)

    visit(tree, "<module>")
    return sorted(set(out))


def write_list_names_table(text):
    t = uncommented(text)
    m = re.search(r"irpt_rg_gold_write_arns\s*=\s*\[(.*?)\n\s*\]", t, re.S)
    if m is None:
        raise SystemExit("STOP: no irpt_rg_gold_write_arns list in the reporting-gold locals.tf")
    return TABLE in m.group(1)


def read_text(root, rel):
    with open(os.path.join(root, *rel.split("/")), "rb") as fh:
        return fh.read().decode("utf-8")


def main(argv):
    root = os.path.abspath(argv[1] if len(argv) > 1 else ".")
    sys.path.insert(0, root)
    from lib import opal_naming
    import pyarrow.parquet as pq

    claims = claim_columns_of(read_text(root, PRODUCER_REL))

    addr = opal_naming.address("irpt", FIRM_KEY, "gold", TABLE, "method_version=1", "data.parquet")
    bucket, key = addr[len("s3://"):].split("/", 1)
    prefix = key.split("method_version=", 1)[0]

    reader = Reader()
    keys = reader.list_keys(bucket, prefix)
    pat = re.compile(re.escape(prefix) + r"method_version=(\d+)/data\.parquet")
    versions = []
    for k in keys:
        m = pat.fullmatch(k)
        if m is None:
            continue
        cols = sorted(pq.read_schema(io.BytesIO(reader.get_bytes(bucket, k))).names)
        versions.append({"method_version": int(m.group(1)), "columns": cols,
                         "claim_columns_present": sorted(set(cols) & set(claims))})
    versions.sort(key=lambda v: v["method_version"])
    if not versions:
        raise SystemExit("STOP: no served method row listed under the prefix")
    newest = set(versions[-1]["columns"])

    sites = []
    for d in SCAN_DIRS:
        base = os.path.join(root, *d.split("/"))
        for dp, dn, fn in os.walk(base):
            dn[:] = [x for x in dn if x != "__pycache__" and x != "tests"]
            for name in fn:
                if not name.endswith(".py"):
                    continue
                full = os.path.join(dp, name)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                with open(full, "rb") as fh:
                    txt = fh.read().decode("utf-8", errors="replace")
                if "emit_method_row" in txt:
                    sites.extend(call_sites_of(rel, txt))
    sites = sorted(set(sites))
    scheduled = [s for s in sites if s.startswith("infra/aws/lambda/")]

    tf_hits = []
    tf_base = os.path.join(root, *TF_DIR.split("/"))
    for dp, dn, fn in os.walk(tf_base):
        for name in fn:
            if name.endswith(".tf"):
                full = os.path.join(dp, name)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                with open(full, "rb") as fh:
                    if TABLE in uncommented(fh.read().decode("utf-8", errors="replace")):
                        tf_hits.append(rel)
    tf_hits = sorted(tf_hits)

    has_prefix = write_list_names_table(read_text(root, GOLD_LOCALS_REL))

    result = {
        "served_versions": versions,
        "producer_claim_columns": claims,
        "missing_in_newest": sorted(set(claims) - newest),
        "call_sites": sites,
        "scheduled_function_call_sites": scheduled,
        "terraform_files_naming_prefix": tf_hits,
        "reporting_gold_write_list_has_prefix": has_prefix,
        "s3_reads": reader.calls,
        "analysis_file": ANALYSIS_REL,
        "analysis_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest(),
    }
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    with open(os.path.join(PRIVATE_DIR, PRIVATE_NAME), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("served versions (method_version: column count, claim columns present): %s" % json.dumps(
        [[v["method_version"], len(v["columns"]), len(v["claim_columns_present"])] for v in versions]))
    print("producer claim columns (%d): %s" % (len(claims), ", ".join(claims)))
    print("missing in newest served version (%d): %s" % (len(result["missing_in_newest"]), ", ".join(result["missing_in_newest"])))
    print("call sites (%d): %s" % (len(sites), ", ".join(sites)))
    print("scheduled function call sites (%d)" % len(scheduled))
    print("terraform files naming the prefix (%d): %s" % (len(tf_hits), ", ".join(tf_hits)))
    print("reporting-gold write list has the prefix: %s" % has_prefix)
    print("S3 calls (LIST pages and GET): %d" % reader.calls)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
