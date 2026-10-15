"""IRPT_DASHBD round 125, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the apply of the signed Cottonwood account_dim pair (DB-c-19) by 0.7.0_AE_CloudOps~DB2.

  DBC125-1-AC1 the gates, the ledger, the build (package test rc 0, landed zip = built zip) and the plan (exactly 7 adds, all irpt_account_dim, no change, no destroy, a clean re-plan)
  DBC125-2-AC1 the ONE key: a fresh LIST of the account_dim gold prefix holds exactly date=2026-10-13/data.parquet, its size and ETag equal the record, it was written in the apply window,
               its parquet reads back with the recorded row count and a schema hash equal to the contract's
  DBC125-3-AC1 the live state: the function, its role and layer, the schedule ENABLED at cron(45 8 ? * MON-FRI *) America/New_York on the function, the 0/1/0 enable plan, the ledger not closed

The checker RECOMPUTES from fresh AWS and S3 reads (get_function_configuration, get_schedule, head/get/list) and the repo; it writes nothing.
Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import datetime as dt
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p117", str(HERE.parent / "r117" / "p117_bcw.py"))
p117 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p117)
p114, Fail, need = p117.p114, p117.Fail, p117.need

D = p114.D
REC = D + "0.7.0_AE_CloudOps~DB2/ACCOUNT_DIM_APPLY_RECORD.json"
PACKET = D + "0.9.0_WK_IRPT_DASHBD~412/NEVER_WIDEN_PACKET_DB-c-19_R123_ACCOUNT_DIM.md"
BLOB = "ed09e2768fd13983291ceafbed44ddd54ac69e13"
COO_HALF = D + "2.0.0_SA_COO~C2/NEVER_WIDEN_DB-c-19_R123_ACCOUNT_DIM_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_DB-c-19_R123_ACCOUNT_DIM_CTO_HALF.md"
CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_DIM_CONTRACT.json"
FN = "irpt-cot-account-dim-lambda"
ROLE = "irpt-cot-account-dim-role"
SCHED = "irpt-cot-account-dim-daily"
CRON = "cron(45 8 ? * MON-FRI *)"
DAY = "2026-10-13"
REGION = "us-east-1"


def utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def ac_1(root):
    root = Path(root)
    r = p114.load(root, REC)
    p117.clean(r)
    need(r.get("claim") == "measured", "claim is not measured")
    need(r["reads"].get("vendor_calls") == 0 and r["reads"].get("secret_reads") == 0, "vendor or secret reads recorded")
    g = r["gates"]
    need(g["packet_blob"] == BLOB and p117.git(root, "hash-object", PACKET) == BLOB, "the packet blob is not the signed one")
    for key, half in (("coo_half_signed", COO_HALF), ("cto_half_signed", CTO_HALF)):
        t = (root / half).read_text(encoding="utf-8")
        need(g[key] is True and BLOB in t and re.search(r"SIGNED", t) is not None, "half not signed at the blob: " + half)
    for k in ("role_name_matches_cot", "bucket_policy_admits_role", "layer_exists"):
        need(g[k] is True, "gate not true: " + k)
    cands = list((root / "org/critical_paths/change_management").glob("*" + r["ledger_entry"] + "*"))
    need(len(cands) >= 1, "the ledger entry is absent: " + r["ledger_entry"])
    lt = cands[0].read_text(encoding="utf-8")
    need(FN in lt and ROLE in lt, "the ledger does not name the function and the role")
    b = r["build"]
    need(b["package_test_rc"] == 0 and b["built_equals_landed"] is True, "the package test or the landed-equals-built record fails")
    need("lambda_function.py" in b["members"] and len(b["members"]) >= 15, "the zip members are not the entry's")
    pl = r["plan"]
    need(pl["add"] == 7 and len(pl["add_addresses"]) == 7 and all("irpt_account_dim" in a for a in pl["add_addresses"]), "the plan did not add exactly seven irpt_account_dim resources")
    need(pl["change"] == 0 and pl["destroy"] == 0 and pl["replan_no_changes"] is True, "the plan changed or destroyed something, or the re-plan was not clean")
    need(r["before"]["account_dim_objects"] == 0 and all(v == "ABSENT" for v in r["before"]["resources_absent"].values()), "the before-state was not absence")


def ac_2(root):
    root = Path(root)
    naming, _cal = p114.lib(root)
    r = p114.load(root, REC)
    key_uri = naming.address("irpt", "cottonwood", "gold", "account_dim", "date=" + DAY, "data.parquet")
    bucket, key = p117.split(key_uri)
    need(r["invoke"]["date"] == DAY and r["invoke"]["count"] == 1 and r["invoke"]["landed"] is True, "the invoke record is not one landed invoke for " + DAY)
    need(r["after"]["keys"] == [key_uri], "the recorded keys are not exactly the one key")
    s3 = p114.s3client()
    prefix = key[: key.index("date=")]
    found = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        found += [o["Key"] for o in page.get("Contents", [])]
    need(found == [key], "the account_dim prefix does not hold exactly the one key (%d objects)" % len(found))
    h = s3.head_object(Bucket=bucket, Key=key)
    need(h["ContentLength"] == r["after"]["size"] and h["ETag"].strip('"') == str(r["after"]["etag"]).strip('"'), "size or ETag differs from the record")
    need(h["LastModified"] >= utc(r["apply_started_utc"]), "the key was not written inside the apply window")
    import pyarrow.parquet as pq
    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    tbl = pq.read_table(io.BytesIO(body))
    need(tbl.num_rows == r["after"]["rows"] and tbl.num_rows > 0, "row count differs from the record")
    lines = sorted("%s:%s" % (f.name, f.type) for f in tbl.schema)
    sh = hashlib.sha256("\n".join(lines).encode("ascii")).hexdigest()
    want = json.loads((root / CONTRACT).read_text(encoding="utf-8"))["schema_hash"]
    need(sh == want and r["after"]["schema_hash"] == want and r["after"]["schema_hash_equals_contract"] is True, "the schema hash differs from the contract's")
    need(r["after"]["silver_unchanged"] is True and r["after"]["other_prefixes_unchanged"] is True, "the silver or other-prefix comparison is not recorded true")


def ac_3(root):
    r = p114.load(root, REC)
    import boto3
    lam = boto3.client("lambda", region_name=REGION)
    sch = boto3.client("scheduler", region_name=REGION)
    c = lam.get_function_configuration(FunctionName=FN)
    need(c["Handler"] == "lambda_function.lambda_handler" and c["Runtime"] == "python3.12", "handler or runtime wrong")
    need(c["Role"].endswith("/" + ROLE) and re.fullmatch(r".*role/.*-cot-.*", c["Role"]) is not None, "the function's role is not " + ROLE)
    need(len(c.get("Layers", [])) >= 1, "no layer attached")
    s = sch.get_schedule(Name=SCHED)
    need(s["State"] == "ENABLED" and s["ScheduleExpression"] == CRON and s.get("ScheduleExpressionTimezone") == "America/New_York", "the schedule is not ENABLED at " + CRON + " America/New_York")
    need(s["Target"]["Arn"].endswith(":function:" + FN), "the schedule does not target the function")
    en = r["enable"]
    need(en["plan"] == {"add": 0, "change": 1, "destroy": 0} and en["after_read_before_enable"] is True, "the enable step is not a 0/1/0 plan after the after-read")
    need(r["ledger_closed"] is False, "the ledger was closed; the issuer closes it after the first scheduled fire")
    t = subprocess.run([sys.executable, "-m", "pytest", str(Path(root) / "infra/aws/lambda/investor-reporting/account-dim-cot/tests"), "-q", "-p", "no:cacheprovider"],
                       capture_output=True, text=True, timeout=110)
    need(t.returncode == 0, "the account-dim-cot tests do not pass")


ARMS = {"DBC125-1-AC1": ac_1, "DBC125-2-AC1": ac_2, "DBC125-3-AC1": ac_3}


def main(argv):
    root, cid = argv[0], argv[1]
    try:
        need(cid in ARMS, "unknown criterion " + cid)
        ARMS[cid](root)
    except Fail as e:
        print(str(e))
        print(cid + " FAIL")
        return 1
    except Exception as e:
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
