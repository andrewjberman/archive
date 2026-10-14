"""IRPT_DASHBD round 109, cell 1 (the W171-S4 read gate), issuer 2.0.0_SA_COO~D2, a DIRECT ACT. READ ONLY.

Reproduces the Orion silver guard's set-identity for scope inflection (infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py:
expected_partitions over the run-time bronze listing, landed = the silver data.parquet keys, alien = landed minus expected), then ENUMERATES the alien
objects: key, size, LastModified, and the distinct values of the provenance riders inside each (to answer "whose data is it"). Names and counts only; it
prints and returns no client row. S3 LIST, HEAD and one GET per alien object under s3://opal-data-assets/orion/inflection/ ONLY; no write of any kind.

Usage: python -I alien_read_r109.py <repo_root> --out <record.json>
"""
import importlib.util
import io
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = sys.argv[sys.argv.index("--out") + 1]
BUCKET = "opal-data-assets"
SCOPE_PREFIX = "orion/inflection/"          # the ONLY prefix this script reads
LAMBDA_DIR = ROOT / "infra" / "aws" / "lambda" / "opal-assets" / "opal-assets-silver-orion"

sys.path.insert(0, str(LAMBDA_DIR))
spec = importlib.util.spec_from_file_location("mirror_conversion_orion", str(LAMBDA_DIR / "mirror_conversion.py"))
mc = importlib.util.module_from_spec(spec)
sys.modules["mirror_conversion_orion"] = mc  # a dataclass in the module resolves its own module by name
spec.loader.exec_module(mc)

import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

s3 = boto3.client("s3")


def guard(key):
    assert key.startswith(SCOPE_PREFIX), "outside the granted prefix: %s" % key
    return key


bronze = mc._list_all(s3, SCOPE_PREFIX + "bronze/", BUCKET)
expected = mc.expected_partitions(bronze, "orion")
landed = {k for k in mc._list_all(s3, SCOPE_PREFIX + "silver/", BUCKET) if k.endswith("/data.parquet")}
res = mc.set_identity(expected, landed, {})
alien = res["alien"]
rec = {"scope_prefix": SCOPE_PREFIX, "bronze_objects_listed": len(bronze), "expected": res["expected"], "landed": res["landed"], "matched": res["matched"],
       "missing": len(res["missing"]), "alien_count": len(alien), "verdict": res["verdict"], "alien": []}
prov = list(getattr(mc.ms, "PROVENANCE_COLS", ()))
rec["provenance_cols"] = prov
for k in alien:
    guard(k)
    head = s3.head_object(Bucket=BUCKET, Key=k)
    body = s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()
    t = pq.read_table(io.BytesIO(body))
    riders = {}
    for c in prov:
        if c in t.column_names:
            vals = sorted({str(x) for x in t.column(c).to_pylist() if x is not None})
            riders[c] = {"distinct": len(vals), "values_if_few": vals if len(vals) <= 3 else None}
    rec["alien"].append({"key": k, "size": head["ContentLength"], "last_modified": head["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                         "rows": t.num_rows, "columns": len(t.column_names), "riders": riders,
                         "table": k.split("/")[3] if len(k.split("/")) > 3 else "", "date_part": next((p for p in k.split("/") if p.startswith("date=")), "")})
# WHOSE DATA IS IT: the alien objects' account ids against Inflection's own account set (the private account_dim dry run of round 108), counts only
own = set()
try:
    own = {str(r["account_id"]) for r in pq.read_table("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~171/ACCOUNT_DIM_DRY_RUN.parquet").to_pylist() if r.get("account_id")}
except Exception as exc:  # noqa: BLE001
    rec["own_set_error"] = repr(exc)[:160]
rec["own_account_ids"] = len(own)
for a in rec["alien"]:
    body = s3.get_object(Bucket=BUCKET, Key=guard(a["key"]))["Body"].read()
    t = pq.read_table(io.BytesIO(body))
    col = next((c for c in t.column_names if c.lower() in ("accountid", "account_id")), None)
    if col is None:
        a["account_overlap"] = {"column": None}
        continue
    ids = {str(x) for x in t.column(col).to_pylist() if x is not None}
    a["account_overlap"] = {"column": col, "distinct_accounts": len(ids), "in_inflection_set": len(ids & own), "not_in_inflection_set": len(ids - own)}
# the bronze objects for the two alien dates, by NAME and class only
dates = sorted({a["date_part"][5:] for a in rec["alien"]})
rec["bronze_for_alien_dates"] = {d: sorted(k.split("/")[3] + "/" + k.split("/")[-1] for k in bronze if d in k) for d in dates}
rec["reads"] = {"s3_writes": 0, "vendor_calls": 0, "dynamodb_writes": 0}
Path(OUT).write_text(json.dumps(rec, indent=2, default=str), encoding="utf-8")
print("bronze %d expected %d landed %d matched %d missing %d alien %d verdict %s" % (len(bronze), res["expected"], res["landed"], res["matched"], len(res["missing"]), len(alien), res["verdict"]))
for a in rec["alien"]:
    print("ALIEN %s | %d bytes | %s | rows %d | riders %s" % (a["key"], a["size"], a["last_modified"], a["rows"], {c: v["values_if_few"] for c, v in a["riders"].items()}))
    print("   accounts: %s" % a.get("account_overlap"))
print("bronze for the alien dates: %s" % rec["bronze_for_alien_dates"])
