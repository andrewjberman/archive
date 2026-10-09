"""TO-DB-b-78 A4: DELTA on the served account_return_daily partition of <day> against a LOCAL run of the round-25 handler
(git show 5ffd7b740d:<handler> with that commit's sources.json) for the first 20 accounts of the standing sample.

Usage (worktree root):  python <this file> <day> <outdir>
Reads S3 only (the served partition via boto3 get_object from the address builder output); writes local files only (outdir).
Prints one JSON object: rows compared, columns compared, differing cells (DELTA), the 20 accounts as sha256 prefixes (never ids).
"""
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
HANDLER_REL = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
SOURCES_REL = "data/assets/scripts/gold/irpt_reporting/sources.json"
PIN = "5ffd7b740d"
SAMPLE = ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json"


def gs(rel):
    return subprocess.run(["git", "show", "%s:%s" % (PIN, rel)], cwd=str(ROOT), capture_output=True, check=True).stdout


def main(day, outdir):
    import boto3
    import pandas as pd
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    accts = [str(a) for a in json.loads(SAMPLE.read_text(encoding="utf-8"))["accounts"][:20]]
    shim = out / "w" / "x" / "y"
    shim.mkdir(parents=True, exist_ok=True)
    (shim / "handler.py").write_bytes(gs(HANDLER_REL))
    decl = out / "sources_5ffd7b740d.json"
    decl.write_bytes(gs(SOURCES_REL))
    # the round-25 handler resolves its own _ROOT five levels up: keep the shim at <root>-relative depth like round 23
    shim2 = ROOT / ".scratch" / "before" / "w" / "x" / "y"
    shim2.mkdir(parents=True, exist_ok=True)
    (shim2 / "handler.py").write_bytes(gs(HANDLER_REL))
    spec = importlib.util.spec_from_file_location("handler_before", str(shim2 / "handler.py"))
    h = importlib.util.module_from_spec(spec)
    sys.modules["handler_before"] = h
    spec.loader.exec_module(h)
    orig = h.ard.load_declaration
    h.ard.load_declaration = lambda path=decl: orig(path)
    h.local(day, out / "returns.parquet", accounts=accts, class_out=str(out / "class.parquet"))
    local = pd.read_parquet(out / "returns.parquet")
    uri = h.ard.opal_naming.address("irpt", "49financial", "gold", "account_return_daily", "date=%s" % day) + "/data.parquet"
    bucket, key = h.ard._split(uri)
    body = boto3.client("s3", region_name="us-east-1").get_object(Bucket=bucket, Key=key)["Body"].read()
    served = pd.read_parquet(io.BytesIO(body))
    served = served[served["account_id"].astype(str).isin(set(accts))]
    cols = [c for c in local.columns if c in served.columns]
    pk = [c for c in ("firm", "account_id", "business_date", "window", "return_method") if c in cols]
    a = local[cols].sort_values(pk).reset_index(drop=True)
    b = served[cols].sort_values(pk).reset_index(drop=True)
    delta = None
    if len(a) == len(b):
        delta = 0
        for c in cols:
            x, y = a[c], b[c]
            same = (x.astype(str) == y.astype(str)) | (x.isna() & y.isna())
            if not same.all():
                try:
                    same = same | ((pd.to_numeric(x, errors="coerce") - pd.to_numeric(y, errors="coerce")).abs() == 0)
                except Exception:
                    pass
            delta += int((~same).sum())
    res = {"day": day, "local_rows": int(len(a)), "served_rows_for_sample": int(len(b)), "columns_compared": len(cols),
           "primary_key_cols": pk, "delta_cells": delta, "local_columns_not_in_served": sorted(set(local.columns) - set(served.columns)),
           "served_columns_not_in_local": sorted(set(served.columns) - set(local.columns)),
           "accounts_sha256_prefix": [hashlib.sha256(x.encode()).hexdigest()[:10] for x in accts],
           "served_key": key, "pandas_local": pd.__version__}
    print(json.dumps(res, indent=1))
    (out / "a4_result.json").write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
